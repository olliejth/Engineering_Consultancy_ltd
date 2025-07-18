"""Matplotlib visualisation file"""


import pandas as pd

from matplotlib import pyplot as plt

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
                                                                    "") + '@gmail.com'

    fig, ax = plt.subplots()

    ax.axis("off")

    # MAKE BIGGER
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center')

    plt.title("Project Summary Table")
    plt.show()


if __name__ == "__main__":

    # pd.set_option('display.max_columns', 50)

    my_df = main()

    # chart1 = budget_over_time(my_df)

    chart_2 = issues_without_descriptions(my_df)
