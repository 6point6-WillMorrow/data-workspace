import { render } from '@testing-library/react';

import DataDisplay, { Data } from '.';

const data: Data = [
  {
    label: 'Title 1',
    value: 100
  },
  {
    label: 'Title 2',
    value: 200
  }
];
describe('Data display', () => {
  it('should display data', () => {
    const { getByText } = render(<DataDisplay data={data} />);
    expect(getByText('Title 1')).toBeInTheDocument();
    expect(getByText('100')).toBeInTheDocument();
    expect(getByText('Title 2')).toBeInTheDocument();
    expect(getByText('200')).toBeInTheDocument();
  });
  it('should NOT display a footer note', () => {
    const { queryByTestId } = render(<DataDisplay data={data} />);
    expect(queryByTestId('data-usage-footer-note')).not.toBeInTheDocument();
  });
  it('should display a footer note', () => {
    const { queryByTestId, getByText } = render(
      <DataDisplay data={data} footerNote={<div>Some footer note</div>} />
    );
    expect(queryByTestId('data-usage-footer-note')).toBeInTheDocument();
    expect(getByText('Some footer note')).toBeInTheDocument();
  });
});
