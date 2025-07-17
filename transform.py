"""Data transformation and cleaning for Engineering Consultancy Limited pipeline"""

from os import environ as ENV

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


MASTER_COLUMNS = ['project_id', 'project_name', 'record_date', 'task_id', 'task_name',
                  'assigned_to', 'progress_percent', 'hours logged', 'cost', 'budget_remaining',
                  'over_budget', 'issue_flag', 'issue_description', 'notes', 'due_date']


def rename_columns(dataframes: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """Renames df column headings to master columns"""

    for df in dataframes:
        cols = list(df.columns)
        head_change_dict = {cols[i]: MASTER_COLUMNS[i] for i in range(15)}
        df.rename(columns=head_change_dict, inplace=True)

    return dataframes


def clean_data(dataframes: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """Returns all three clean data frames"""

    renamed_col_dfs = rename_columns(dataframes)


def combine_dfs(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """Combine all three project dfs into single df"""
    ...


if __name__ == "__main__":

    alpha_df = pd.read_csv(ENV["ALPHA_PATH"])
    beta_df = pd.read_json(ENV["BETA_PATH"])

    rename_columns([alpha_df, beta_df])
