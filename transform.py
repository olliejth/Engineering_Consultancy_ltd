"""Data transformation using pandas for Engineering Consultancy Limited pipeline"""

# pylint: disable=W0621

from os import environ as ENV

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


MASTER_COLUMNS = ['project_id', 'project_name', 'record_date', 'task_id', 'task_name',
                  'assigned_to', 'progress_percent', 'hours_logged', 'cost', 'budget_remaining',
                  'over_budget', 'issue_flag', 'issue_description', 'notes', 'due_date']

NO_PROG_PERC = ['project_id', 'project_name', 'record_date', 'task_id', 'task_name',
                'hours_logged', 'cost', 'budget_remaining', 'over_budget', 'issue_flag',
                'issue_description', 'notes', 'due_date']


def rename_columns(dataframes: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """Renames df column headings to master columns"""

    for df in dataframes:
        cols = list(df.columns)
        head_change_dict = {cols[i]: MASTER_COLUMNS[i] for i in range(15)}
        df.rename(columns=head_change_dict, inplace=True)

    return dataframes


def reformat_id(input_id) -> str:
    """Reformats input IDs into a standard format"""

    if not input_id:
        return None

    if isinstance(input_id, str):
        if input_id[0] == 'P':
            return 'P002'
        return 'T000' + input_id[-2:]

    return 'T000' + str(input_id+1)[-2:]


def clean_alpha_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans data-set alpha"""

    # Reformat ID to correct format
    df['task_id'] = df['task_id'].apply(reformat_id)

    return df


def clean_beta_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans data-set beta"""

    # Reformat ID to correct format
    df['task_id'] = df['task_id'].apply(reformat_id)

    # Reformat Project IDs
    df['project_id'] = df['project_id'].apply(reformat_id)

    # Converting cost_overrun_flag and issue_flag to bools
    df["over_budget"] = df["over_budget"].astype(bool)
    df["issue_flag"] = df["issue_flag"].astype(bool)

    return df


def clean_individual_dfs(dataframes: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """Returns all three clean data frames"""

    alpha_df, beta_df, gamma_df = rename_columns(dataframes)

    clean_alpha = clean_alpha_df(alpha_df)
    clean_beta = clean_beta_df(beta_df)

    clean_dataframes = [clean_alpha, clean_beta, gamma_df]

    return clean_dataframes


def combine_dfs(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """Combine all three project dfs into single df"""
    return pd.concat(dataframes)


def clean_combined(df: pd.DataFrame) -> pd.DataFrame:
    """Returns combined clean dataframe"""

    # Drop progress_percent column
    df = df.drop(columns='progress_percent')

    # Round and convert float hours into int
    df['hours_logged'] = df['hours_logged'].round().astype("Int64")

    # Convert string dates into datetime objects
    df["record_date"] = pd.to_datetime(
        df["record_date"], format="%Y-%m-%d")
    df["due_date"] = pd.to_datetime(
        df["due_date"], format="%Y-%m-%d")

    return df


if __name__ == "__main__":

    alpha_df = pd.read_csv(ENV["ALPHA_PATH"])
    beta_df = pd.read_json(ENV["BETA_PATH"])
    gamma_df = pd.read_csv(ENV["GAMMA_PATH"])

    clean_dfs = clean_individual_dfs([alpha_df, beta_df, gamma_df])
    combined_df = combine_dfs(clean_dfs)

    comb_clean_df = clean_combined(combined_df)

    my_df = comb_clean_df

    # COUNT = 1
    # for col_name in NO_PROG_PERC:

    #     print(f'\n{COUNT}) {col_name}\n')
    #     print(my_df[col_name].head(n=2))
    #     COUNT += 1

    # print('\n')
    # print(my_df.info())
