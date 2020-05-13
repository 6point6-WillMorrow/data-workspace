from collections import defaultdict
from typing import List, Dict

import boto3
import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings

from dataworkspace.apps.core.utils import database_dsn
from dataworkspace.apps.datasets.models import MasterDataset


QUICKSIGHT_COLUMN_TYPES_MAP = defaultdict(
    lambda: 'STRING',
    **{
        "date": 'DATETIME',
        "smallint": 'INTEGER',
        "bigint": "INTEGER",
        "integer": "INTEGER",
        "boolean": 'BOOLEAN',
        "numeric": 'DECIMAL',
        "real": "DECIMAL",
        "double precision": "DECIMAL",
        "timestamp with time zone": "TIMESTAMP",
        "json": "JSON",
        "jsonb": "JSON",
    },
)

QS_DATASOURCE_ALL_PERMS = [
    'quicksight:UpdateDataSourcePermissions',
    'quicksight:DescribeDataSource',
    'quicksight:DescribeDataSourcePermissions',
    'quicksight:PassDataSource',
    'quicksight:UpdateDataSource',
    'quicksight:DeleteDataSource',
]

QS_DATASET_ALL_PERMS = [
    'quicksight:UpdateDataSetPermissions',
    'quicksight:DescribeDataSet',
    'quicksight:DescribeDataSetPermissions',
    'quicksight:PassDataSet',
    'quicksight:DescribeIngestion',
    'quicksight:ListIngestions',
    'quicksight:UpdateDataSet',
    'quicksight:DeleteDataSet',
    'quicksight:CreateIngestion',
    'quicksight:CancelIngestion',
]

QS_DATASET_USER_PERMS = [
    'quicksight:DescribeDataSet',
    'quicksight:DescribeDataSetPermissions',
    'quicksight:PassDataSet',
    'quicksight:DescribeIngestion',
    'quicksight:ListIngestions',
]


class Command(BaseCommand):
    '''Sync master datasets and user permissions from Data Workspace to AWS QuickSight.
    '''

    help = 'Sync master datasets and user permissions from Data Workspace to AWS QuickSight.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _make_dataset_id(self, dataset):
        return f"{settings.ENVIRONMENT.upper()}-{str(dataset.id)}"

    def _get_dataset_columns(self, connection, source_table):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s and table_name = %s",
                [source_table.schema, source_table.table],
            )
            return cursor.fetchall()

    def _format_input_columns(self, db_config, source_table):
        with psycopg2.connect(database_dsn(db_config)) as connection:
            columns = self._get_dataset_columns(connection, source_table)

        return [
            {"Name": column_name, "Type": QUICKSIGHT_COLUMN_TYPES_MAP[data_type]}
            for column_name, data_type in columns
        ]

    def _dataset_users_with_access(
        self, dataset: MasterDataset, quicksight_user_list: List[Dict[str, str]]
    ) -> set:
        if dataset.user_access_type == 'REQUIRES_AUTHENTICATION':
            return {user['Arn'] for user in quicksight_user_list}

        quicksight_user_emails = [user['Email'] for user in quicksight_user_list]
        authorized_users = set(
            user['user__email']
            for user in dataset.datasetuserpermission_set.filter(
                user__email__in=quicksight_user_emails
            ).values("user__email")
        )

        # The QS datasource owner should always have access to every dataset.
        principals_needing_access = {settings.QUICKSIGHT_DATASOURCE_USER_ARN}

        principals_needing_access.update(
            {
                user['Arn']
                for user in quicksight_user_list
                if user['Email'] in authorized_users
            }
        )

        return principals_needing_access

    def _grant_permissions_to_dataset(
        self, data_client, account_id, dataset, principals
    ):
        grant_arns = [
            {
                "Principal": principal,
                "Actions": QS_DATASET_ALL_PERMS
                if principal == settings.QUICKSIGHT_DATASOURCE_USER_ARN
                else QS_DATASET_USER_PERMS,
            }
            for principal in principals
        ]

        if grant_arns:
            data_client.update_data_set_permissions(
                AwsAccountId=account_id,
                DataSetId=self._make_dataset_id(dataset),
                GrantPermissions=grant_arns,
            )

    def _revoke_permissions_to_dataset(
        self, data_client, account_id, dataset, principals
    ):
        revoke_arns = [
            {"Principal": principal, "Actions": QS_DATASET_ALL_PERMS}
            for principal in principals
        ]

        if revoke_arns:
            data_client.update_data_set_permissions(
                AwsAccountId=account_id,
                DataSetId=self._make_dataset_id(dataset),
                RevokePermissions=revoke_arns,
            )

    def _sync_permissions_to_dataset(self, data_client, account_id, qs_users, dataset):
        data_set_permissions = data_client.describe_data_set_permissions(
            AwsAccountId=account_id, DataSetId=self._make_dataset_id(dataset)
        )['Permissions']
        self.stdout.write(
            f"-> Current principals with access: {[u['Principal'] for u in data_set_permissions]}"
        )

        all_principals_needing_access = self._dataset_users_with_access(
            dataset, qs_users
        )
        self.stdout.write(
            f"-> Principals that should have access: {all_principals_needing_access}"
        )
        principals_to_grant_access = all_principals_needing_access.difference(
            set(user['Principal'] for user in data_set_permissions)
        )
        self.stdout.write(f"-> Adding principals: {principals_to_grant_access}")
        self._grant_permissions_to_dataset(
            data_client, account_id, dataset, principals_to_grant_access
        )

        principals_to_revoke_access = set(
            user['Principal'] for user in data_set_permissions
        ).difference(all_principals_needing_access)
        self.stdout.write(f"-> Removing principals: {principals_to_revoke_access}")
        self._revoke_permissions_to_dataset(
            data_client, account_id, dataset, principals_to_revoke_access
        )

        final_data_source_principals = set(
            user['Principal']
            for user in data_client.describe_data_set_permissions(
                AwsAccountId=account_id, DataSetId=self._make_dataset_id(dataset)
            )['Permissions']
        )

        if all_principals_needing_access.symmetric_difference(
            final_data_source_principals
        ):
            self.stderr.write(
                "-> Error syncing permissions for dataset.\n"
                f"  Incorrectly DO have access: {final_data_source_principals - all_principals_needing_access}\n"
                f"  Incorrectly DO NOT have access: {all_principals_needing_access - final_data_source_principals}"
            )

    def _create_dataset(self, data_client, account_id, db_config, datasource, dataset):
        self.stdout.write(f"-> Creating dataset: {dataset}")
        sourcetables = dataset.sourcetable_set.all()
        physical_tables = {
            str(source_table.id): {
                "RelationalTable": {
                    "DataSourceArn": datasource['DataSource']['Arn'],
                    "InputColumns": self._format_input_columns(db_config, source_table),
                    "Name": source_table.table,
                    "Schema": source_table.schema,
                }
            }
            for source_table in sourcetables
        }
        logical_tables = {
            str(source_table.id): {
                "Alias": source_table.name,
                "Source": {"PhysicalTableId": str(source_table.id)},
            }
            for source_table in sourcetables
        }

        self.stdout.write(f"--> Physical tables: {str(physical_tables)}")
        self.stdout.write(f"--> Logical tables: {str(logical_tables)}")

        try:
            dataset_name = dataset.name
            if settings.ENVIRONMENT != "Production":
                dataset_name = f"{settings.ENVIRONMENT.upper()} - {dataset_name}"

            qs_dataset = data_client.create_data_set(
                AwsAccountId=account_id,
                DataSetId=self._make_dataset_id(dataset),
                Name=dataset_name,
                ImportMode='DIRECT_QUERY',
                PhysicalTableMap=physical_tables,
                LogicalTableMap=logical_tables,
                Permissions=[
                    {
                        "Principal": settings.QUICKSIGHT_DATASOURCE_USER_ARN,
                        "Actions": QS_DATASET_ALL_PERMS,
                    }
                ],
            )
            self.stdout.write(str(qs_dataset))
        except data_client.exceptions.ResourceExistsException as e:
            self.stdout.write(str(e))

        self.stdout.write("-> Done.")
        return data_client.describe_data_set(
            AwsAccountId=account_id, DataSetId=self._make_dataset_id(dataset)
        )

    def _create_datasource(self, data_client, account_id, db_name, db_config):
        data_source_id = f'data-workspace-{settings.ENVIRONMENT}'

        try:
            self.stdout.write(f"-> Creating data source: {data_source_id}")
            qs_datasource = data_client.create_data_source(
                AwsAccountId=account_id,
                DataSourceId=data_source_id,
                Name=f"Data Workspace - {settings.ENVIRONMENT} - {db_name}",
                Type='AURORA_POSTGRESQL',
                DataSourceParameters={
                    "AuroraPostgreSqlParameters": {
                        "Host": db_config['HOST'],
                        "Port": int(db_config['PORT']),
                        "Database": db_config['NAME'],
                    }
                },
                Credentials={
                    "CredentialPair": {
                        "Username": db_config['USER'],
                        "Password": db_config['PASSWORD'],
                    }
                },
                Permissions=[
                    {
                        'Principal': settings.QUICKSIGHT_DATASOURCE_USER_ARN,
                        'Actions': QS_DATASOURCE_ALL_PERMS,
                    }
                ],
                VpcConnectionProperties={
                    "VpcConnectionArn": settings.QUICKSIGHT_VPC_ARN
                },
            )
            self.stdout.write(str(qs_datasource))
        except data_client.exceptions.ResourceExistsException as e:
            self.stdout.write(str(e))

        return data_client.describe_data_source(
            AwsAccountId=account_id, DataSourceId=data_source_id
        )

    def handle(self, *args, **options):
        self.stdout.write('sync_sources_and_permissions_to_quicksight started')

        # QuickSight manages users in a single specific region
        user_client = boto3.client(
            'quicksight', region_name=settings.QUICKSIGHT_USER_REGION
        )
        # Data sources can be in other regions - so here we use the Data Workspace default from its env vars.
        data_client = boto3.client('quicksight')

        account_id = boto3.client('sts').get_caller_identity().get('Account')

        db = list(settings.DATABASES_DATA.keys())[0]
        db_config = settings.DATABASES_DATA[db]

        quicksight_user_list: List[Dict[str, str]] = user_client.list_users(
            AwsAccountId=account_id, Namespace='default'
        )['UserList']

        datasource = self._create_datasource(data_client, account_id, db, db_config)

        for dataset in MasterDataset.objects.live().filter(published=True):
            self._create_dataset(
                data_client, account_id, db_config, datasource, dataset
            )
            self._sync_permissions_to_dataset(
                data_client, account_id, quicksight_user_list, dataset
            )

        self.stdout.write(
            self.style.SUCCESS('sync_sources_and_permissions_to_quicksight finished')
        )


if __name__ == '__main__':
    settings.configure()
    Command().handle()