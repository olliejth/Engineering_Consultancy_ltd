"""Matplotlib visualisation file"""


import pandas as pd

from matplotlib import pyplot as plt

from transform import main


def budget_over_time():
    ...


if __name__ == "__main__":

    pd.set_option('display.max_columns', 50)

    my_df = main()
    print(my_df.head())
