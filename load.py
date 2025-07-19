"""Matplotlib visualisation file"""


from matplotlib import pyplot as plt
from datetime import datetime

import pandas as pd

from transform import main


def budget_over_time(df: pd.DataFrame):
    """Creates a layered line chart of budget over time for """

    df = df.sort_values('record_date', ascending=True).reset_index()

    alpha_data = df['budget_remaining'][df['project_id'] == 'P001']
    beta_data = df['budget_remaining'][df['project_id'] == 'P002']
    gamma_data = df['budget_remaining'][df['project_id'] == 'P003']

    alpha_dates = df['record_date'][df['project_id'] == 'P001']
    beta_dates = df['record_date'][df['project_id'] == 'P002']
    gamma_dates = df['record_date'][df['project_id'] == 'P003']

    f, axes = plt.subplots(3, 1)
    f.set_figheight(7)
    f.set_figwidth(14)

    axes[0].plot(alpha_dates, alpha_data, 'navy')
    axes[0].set_title('Alpha Tunnel Budget Over Time')

    axes[1].plot(beta_dates, beta_data, 'r')
    axes[1].set_title('Beta Bridge Budget Over Time')

    axes[2].plot(gamma_dates, gamma_data, 'g')
    axes[2].set_title('Gamma Tower Budget Over Time')

    plt.subplots_adjust(hspace=0.4)
    plt.show()


def issues_without_descriptions(df: pd.DataFrame):
    """Returns a table of the un-described flagged issues and
        corresponding engineers."""

    df = df.loc[
        df['issue_description'] == 'Issue flagged but no description provided',
        ['project_name', 'assigned_to', 'task_name', 'record_date']
    ]

    df['contact_email'] = df['assigned_to'].str.lower().str.replace(" ",
                                                                    "") + '@ecltd.com'

    plt.axis("off")
    table = plt.table(cellText=df.values,
                      colLabels=[name.replace('_', ' ').title()
                                 for name in df.columns],
                      loc='center',
                      cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(7.5)

    table.scale(1.2, 1.5)
    cells = table.get_celld()

    widths = [[0.17, 0.17, 0.17, 0.17],
              [0.17, 0.17, 0.17, 0.17],
              [0.35, 0.35, 0.35, 0.35],
              [0.25, 0.25, 0.25, 0.25],
              [0.28, 0.28, 0.28, 0.28]]

    for c, col in enumerate(widths):
        for r, row in enumerate(col):
            cells[(r, c)].set_width(widths[c][r])

    plt.title("Issues with no Description")
    plt.show()


def generate_project_spending_dfs(df: pd.DataFrame, ids: list[str]) -> list:
    """Separates the dataframe into projects"""

    months = {'01': 'Jan', '02': 'Feb', '03': 'Mar',
              '04': 'Apr', '05': 'May', '06': 'Jun',
              '07': 'Jul', '08': 'Aug', '09': 'Sep',
              '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    out_list = []

    for pid in ids:
        new_df = df.copy()
        new_df = new_df[new_df['project_id'] == pid]

        new_df = new_df.groupby('month', as_index=False)['cost'].sum()

        new_df = new_df.reset_index(drop=True)

        # new_df['year_month'][2:4]
        out_list.append(new_df)

    return out_list


def spending_per_month(df: pd.DataFrame):
    """Shows spending per month for all projects"""

    df['month'] = df['record_date'].dt.strftime('%Y-%m')

    a_spend, b_spend, g_spend = generate_project_spending_dfs(df,
                                                              ['P001', 'P002', 'P003'])

    f, axes = plt.subplots(3, 1)
    f.set_figheight(7)
    f.set_figwidth(14)

    axes[0].bar(a_spend['month'], a_spend['cost'], color='navy')
    axes[0].set_title('Alpha Tunnel spending per month')

    axes[1].bar(b_spend['month'], b_spend['cost'], color='r')
    axes[1].set_title('Beta Bridge spending per month')

    axes[2].bar(g_spend['month'], g_spend['cost'], color='g')
    axes[2].set_title('Gamma Tower spending per month')

    plt.subplots_adjust(hspace=0.4)

    plt.show()


if __name__ == "__main__":

    pd.set_option('display.max_columns', 50)

    my_df = main()

    chart1 = budget_over_time(my_df)

    chart_2 = issues_without_descriptions(my_df)

    chart_3 = spending_per_month(my_df)
