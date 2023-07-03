from typing import TypedDict
import pandas as pd
from pandas import DataFrame

ERROR_VALUE = "There is a data input error"


class Item(TypedDict):
    item_name: str
    items_number: int
    item_price: int
    total_price: int


class Transaction:
    def __init__(self) -> None:
        """
        Initialize the object. This is called by __init__ and should not be
        called directly.
        """
        self._items: list[Item] = []
        self._is_checked: bool = False

    def view(self) -> DataFrame:
        """
        View the data in the list.

        Returns:
                A dataframe containing the data in the list as well as the
                number of items in the list
        """
        return pd.DataFrame.from_records(
            self._items, range(1, len(self._items) + 1)
        )

    def _validate_string(self, string_value: str) -> None:
        """
        Validates that the string_value is a string. This is a helper method.

        Args:
                string_value: The string to validate as a string
        """
        # Checks if string_value is a string and if it's alphabetic
        if not isinstance(string_value, str) and string_value.isalpha():
            raise ValueError(ERROR_VALUE)

    def _validate_integer(self, integer_value: int) -> None:
        """
        Validates that integer_value is an integer. Raises : exc :
        ` ValueError ` if it is not.

        Args:
                integer_value: The value to validate as an integer
        """
        # Raises a ValueError if integer_value is not an integer greater than
        # or equal to 0
        if not isinstance(integer_value, int) and integer_value >= 0:
            raise ValueError(ERROR_VALUE)

    def add_item(
        self, item_name: str, items_number: int, item_price: int
    ) -> DataFrame:
        """
        Add an item to the order.

        Args:
                item_name: The name of the item. Must be unique.
                items_number: The number of items in the order. Must be
                greater than zero.
                item_price: The price of the item. Must be greater than zero.
        """
        self._validate_string(item_name)
        self._validate_integer(items_number)
        self._validate_integer(item_price)

        self._items.append(
            {
                "item_name": item_name,
                "items_number": items_number,
                "item_price": item_price,
                "total_price": items_number * item_price,
            }
        )

        return self.view()

    def update_item_name(
        self, item_name: str, new_item_name: str
    ) -> DataFrame:
        """
        Update the name of an item.

        Args:
                item_name: The name of the item to update.
                new_item_name: The new name that will be assigned to the item.
        """
        self._validate_string(item_name)
        self._validate_string(new_item_name)

        # Set the item_name of the item in the list of items in the list.
        for index, item in enumerate(self._items):
            # Set the item name of the item
            if item["item_name"] == item_name:
                self._items[index]["item_name"] = new_item_name
                break

        return self.view()

    def update_item_qty(
        self, item_name: str, new_items_number: int
    ) -> DataFrame:
        """
        Updates the quantity of an item in the order.

        Args:
                item_name: The name of the item to update.
                new_items_number: The new number of items to update.
        """
        self._validate_string(item_name)
        self._validate_integer(new_items_number)

        # Update the total price of all items in the collection.
        for index, item in enumerate(self._items):
            # update the total price of the item
            if item["item_name"] == item_name:
                self._items[index]["items_number"] = new_items_number
                self._items[index]["total_price"] = (
                    new_items_number * item["item_price"]
                )
                break

        return self.view()

    def update_item_price(
        self, item_name: str, new_item_price: int
    ) -> DataFrame:
        """
        Update the price of an item.

        Args:
                item_name: The name of the item to update the price of.
                new_item_price: The new price of the item.
        """
        self._validate_string(item_name)
        self._validate_integer(new_item_price)

        # Update the price of the items in the collection.
        for index, item in enumerate(self._items):
            # update the price of the item
            if item["item_name"] == item_name:
                self._items[index]["item_price"] = new_item_price
                self._items[index]["total_price"] = (
                    item["items_number"] * new_item_price
                )
                break

        return self.view()

    def delete_item(self, item_name: str) -> DataFrame:
        """
        Delete item from list.

        Args:
                item_name: Name of item to delete
        """
        self._validate_string(item_name)

        ind = float("nan")
        # Find the index of the first item in the list of items in the list.
        for index, item in enumerate(self._items):
            # Find the index of the item in the list
            if item["item_name"] == item_name:
                ind = index
                break

        if not pd.isna(ind):
            self._items.pop(ind)

        return self.view()

    def reset_transaction(self) -> str:
        """
        Reset transaction to empty.
        """
        self._items = []

        return "All items have been successfully deleted!"

    def check_order(self) -> DataFrame:
        """
        Check the order and print the total amount to be paid.
        This is done by asking the user for the correct order and
        checking the total amount of the items in the order.

        Returns:
                DataFrame if everything is fine otherwise an error message is
                printed to the screen and
                the program exits with an error
        """
        is_correct = input("Order is correct (y/n) ? ")

        self._validate_string(is_correct)
        # Raise ValueError if the value is not y or n
        if is_correct not in ["y", "n"]:
            raise ValueError(ERROR_VALUE)

        if is_correct != "y":
            return "\n"

        # Raise ValueError if the list is empty.
        if len(self._items) == 0:
            raise ValueError(ERROR_VALUE)

        self._is_checked = True

        return self.view()

    def get_total_price(self) -> str:
        """
        Calculate the total amount to be paid.
        """
        if not self._is_checked:
            raise ValueError(ERROR_VALUE)

        total = sum((item["total_price"] for item in self._items))

        # Calculate the total number of items in the total.
        if 200_000 < total <= 300_000:
            total = total - (5 / float(100) * total)
        elif 300_000 < total <= 500_000:
            total = total - (8 / float(100) * total)
        elif total > 500_000:
            total = total - (10 / float(100) * total)

        return f"the total amount to be paid is Rp. {total}"
