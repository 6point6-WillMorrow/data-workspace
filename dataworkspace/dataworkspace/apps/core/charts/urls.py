from django.urls import path

from dataworkspace.apps.accounts.utils import login_required
from dataworkspace.apps.core.charts.views import (
    ChartDeleteView,
    ChartEditView,
    ChartListView,
    ChartQueryResultsView,
    ChartQueryStatusView,
)

urlpatterns = [
    path(
        "edit/<uuid:chart_id>/",
        login_required(ChartEditView.as_view()),
        name="edit-chart",
    ),
    path(
        "delete/<uuid:chart_id>/",
        login_required(ChartDeleteView.as_view()),
        name="delete-chart",
    ),
    path(
        "query-status/<uuid:chart_id>/",
        login_required(ChartQueryStatusView.as_view()),
        name="chart-query-status",
    ),
    path(
        "query-results/<uuid:chart_id>/",
        login_required(ChartQueryResultsView.as_view()),
        name="chart-query-results",
    ),
    path(
        "",
        login_required(ChartListView.as_view()),
        name="list-charts",
    ),
]
