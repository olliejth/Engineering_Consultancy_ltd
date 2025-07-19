"""Data transformation using pandas for Engineering Consultancy Limited pipeline"""

# pylint: disable=W0621

# NO_PROG_PERC = ['project_id', 'project_name', 'record_date', 'task_id', 'task_name',
#                 'hours_logged', 'cost', 'budget_remaining', 'over_budget', 'issue_flag',
#                 'issue_description', 'notes', 'due_date']

from os import environ as ENV

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


MASTER_COLUMNS = ['project_id', 'project_name', 'record_date', 'task_id', 'task_name',
                  'assigned_to', 'progress_percent', 'hours_logged', 'cost', 'budget_remaining',
                  'over_budget', 'issue_flag', 'issue_description', 'notes', 'due_date']


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

    # Convert string dates into datetime
    df["record_date"] = pd.to_datetime(
        df["record_date"], format="%Y-%m-%d")
    df["due_date"] = pd.to_datetime(
        df["due_date"], format="%Y-%m-%d")

    return df


def clean_gamma_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans data-set gamma"""

    # Reformat ID to correct format
    df['task_id'] = df['task_id'].apply(reformat_id)

    return df


def clean_individual_dfs(dataframes: list[pd.DataFrame]) -> list[pd.DataFrame]:
    """Returns all three clean data frames"""

    alpha_df, beta_df, gamma_df = rename_columns(dataframes)

    clean_alpha = clean_alpha_df(alpha_df)
    clean_beta = clean_beta_df(beta_df)
    clean_gamma = clean_gamma_df(gamma_df)

    clean_dataframes = [clean_alpha, clean_beta, clean_gamma]

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

    # Removes rows without key info
    df.dropna(subset=['project_id', 'project_name', 'record_date',
                      'task_id', 'task_name'], inplace=True)

    # Replaces NaN values with more useful information
    # Replace NaN hours logged with zeros
    df['hours_logged'] = df['hours_logged'].fillna(0)

    # Specify when an issue has been flagged but no description provided
    df.loc[
        (df['issue_flag'] == True) &
        (df['issue_description'].isna() |
         (df['issue_description'].str.strip().eq(''))),
        'issue_description'
    ] = 'Issue flagged but no description provided'

    # Replace empty descriptions with text
    df.loc[(df['issue_flag'] == False), 'issue_description'] = 'No issue'

    # Replace empty notes with text
    df.loc[(df['notes'].isna()) |
           (df['notes'].str.strip() == '') |
           (df['notes'].str.strip() == 'NaN'),
           'notes'] = 'No notes provided'

    return df


def main() -> pd.DataFrame:
    """Main transform and cleaning function"""

    alpha_df = pd.read_csv(ENV["ALPHA_PATH"],
                           parse_dates=['date_recorded', 'due_date'])
    beta_df = pd.read_json(ENV["BETA_PATH"])
    gamma_df = pd.read_csv(ENV["GAMMA_PATH"],
                           parse_dates=['record_date', 'due_date'])

    clean_dfs = clean_individual_dfs([alpha_df, beta_df, gamma_df])
    combined_df = combine_dfs(clean_dfs)

    comb_clean_df = clean_combined(combined_df)

    return comb_clean_df


if __name__ == "__main__":

    pd.set_option('display.max_columns', 50)

    my_df = main()

    # print(type(my_df.iloc[12:13]['notes']))
