"""Tester file"""

from os import environ as ENV
from matplotlib import table
import json

from requests import get
from dotenv import load_dotenv


load_dotenv()


def get_api_data() -> list[dict]:

    prods_response = get(f'{ENV["URL"]}products')

    carts_response = get(f'{ENV["URL"]}carts')

    return (prods_response.json(), carts_response.json())


def save_to_file(filename: str, data: list) -> None:
    """Saves json data to local file"""
    with open(f"./data/{filename}.json", "w", encoding='UTF-8') as f_obj:
        json.dump(data, f_obj, indent=4)


def load_from_file(data) -> list[dict]:
    """Load the stories from a file called stories.json"""
    with open(data, "r", encoding="UTF-8") as f_obj:
        return json.load(f_obj)


if __name__ == "__main__":

    api_data = get_api_data()

    save_to_file('products1', api_data[0])
    save_to_file('carts1', api_data[1])
