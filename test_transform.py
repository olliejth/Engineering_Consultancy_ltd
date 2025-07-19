"""Test file for ECL transform file"""

import pytest
import pandas as pd

from transform import rename_columns, reformat_id


df = pd.read_csv('./data/Alpha_Tunnel.csv')


def test_rename_columns():
    """Tests that dataframe columns are renamed properly"""

    new_df = rename_columns([df])

    assert list(new_df[0].columns) == ['project_id', 'project_name', 'record_date', 'task_id', 'task_name',
                                       'assigned_to', 'progress_percent', 'hours_logged', 'cost', 'budget_remaining',
                                       'over_budget', 'issue_flag', 'issue_description', 'notes', 'due_date']


reformat_data = ([
    (101, "T00002"),
    (100, "T00001"),
    (None, None),
    ('Psjbsd', 'P002'),
    ('thfjk99', 'T00099')])


@pytest.mark.parametrize("a, expected", reformat_data)
def test_reformat_id(a, expected):
    """Tests that the reformat id function returns the correct format
        given different possible inputs"""

    assert reformat_id(a) == expected
