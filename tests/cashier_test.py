import builtins
import unittest
from unittest.mock import patch
from pandas import DataFrame, testing
from cashier import cashier

transaction = cashier.Transaction()


class CashierTestCase(unittest.TestCase):
    def test_add_item(self):
        """
        Test adding an item to the transaction. This is a test to make sure we
        can add a new item
        """
        res = transaction.add_item("Apple", 1, 10000)
        assert isinstance(res, DataFrame)
        testing.assert_frame_equal(
            res,
            DataFrame(
                [
                    {
                        "item_name": "Apple",
                        "items_number": 1,
                        "item_price": 10000,
                        "total_price": 10000,
                    }
                ],
                range(1, 2),
            ),
        )

    def test_update_item_name(self):
        """
        Test updating item name in the data frame.
        """
        transaction.add_item("Banana", 1, 20000)
        res = transaction.update_item_name("Banana", "Cherry")
        assert isinstance(res, DataFrame)

    def test_update_item_qty(self):
        """
        Update item qty by item name and qty ( int ). Expect success. No
        exceptions raised in this
        """
        res = transaction.update_item_qty("Cherry", 2)
        assert isinstance(res, DataFrame)

    def test_update_item_price(self):
        """
        Test updating item price by item name ( Cherry 30000 ) in one
        transaction.
        """
        res = transaction.update_item_price("Cherry", 30000)
        assert isinstance(res, DataFrame)

    def test_delete_item(self):
        """
        Test deleting an item from the data frame.
        """
        transaction.add_item("Banana", 1, 20000)
        res = transaction.delete_item("Banana")
        assert isinstance(res, DataFrame)

    def test_check_order_not_confirmed(self):
        """
        Test check_order with non confirmed inputs.
        """
        with patch.object(builtins, "input", lambda _: "n"):
            res = transaction.check_order()
            assert isinstance(res, str)
            assert res == "\n"

    def test_check_order_total_less_than_200000(self):
        """
        Test check_order with total < 200000 is successful.
        """
        with patch.object(builtins, "input", lambda _: "y"):
            transaction_1 = cashier.Transaction()
            transaction_1.add_item("Apple", 1, 10000)
            transaction_1.add_item("Cherry", 2, 30000)
            transaction_1.check_order()
            res = transaction_1.get_total_price()
            assert isinstance(res, str)
            assert res == "the total amount to be paid is Rp. 70000"

    def test_check_order_total_between_200000_and_300000(self):
        """
        Test check_order with total between 200000 and 300000.
        """
        with patch.object(builtins, "input", lambda _: "y"):
            transaction_2 = cashier.Transaction()
            transaction_2.add_item("Apple", 1, 10000)
            transaction_2.add_item("Banana", 7, 20000)
            transaction_2.add_item("Cherry", 2, 30000)
            transaction_2.check_order()
            res = transaction_2.get_total_price()
            assert isinstance(res, str)
            assert res == "the total amount to be paid is Rp. 199500.0"

    def test_check_order_total_between_300000_and_500000(self):
        """
        Test check_order with total between 300000 and 500000.
        """
        with patch.object(builtins, "input", lambda _: "y"):
            transaction_3 = cashier.Transaction()
            transaction_3.add_item("Apple", 1, 10000)
            transaction_3.add_item("Banana", 7, 20000)
            transaction_3.add_item("Cherry", 2, 30000)
            transaction_3.add_item("Duku", 2, 50000)
            transaction_3.check_order()
            res = transaction_3.get_total_price()
            assert isinstance(res, str)
            assert res == "the total amount to be paid is Rp. 285200.0"

    def test_check_order_total_more_than_500000(self):
        """
        Test check_order with more than 500000 items in the transaction.
        """
        with patch.object(builtins, "input", lambda _: "y"):
            transaction_4 = cashier.Transaction()
            transaction_4.add_item("Apple", 1, 10000)
            transaction_4.add_item("Banana", 7, 20000)
            transaction_4.add_item("Cherry", 2, 30000)
            transaction_4.add_item("Duku", 2, 50000)
            transaction_4.add_item("Egg", 5, 40000)
            transaction_4.check_order()
            res = transaction_4.get_total_price()
            assert isinstance(res, str)
            assert res == "the total amount to be paid is Rp. 459000.0"

    def test_reset_transaction(self):
        """
        Test resetting a transaction to a blank state.
        """
        transaction_5 = cashier.Transaction()
        transaction_5.add_item("Apple", 1, 10000)
        res = transaction_5.reset_transaction()
        assert isinstance(res, str)
        assert res == "All items have been successfully deleted!"

    def test_check_order_empty_orders(self):
        """
        Check order fails if there are no orders in the transaction.
        """
        transaction_6 = cashier.Transaction()
        with patch.object(builtins, "input", lambda _: "y"):
            with self.assertRaises(ValueError):
                transaction_6.check_order()

    def test_check_order_wrong_value(self):
        """
        Check order fails with wrong value for check_order ().
        """
        transaction_7 = cashier.Transaction()
        with patch.object(builtins, "input", lambda _: "false"):
            with self.assertRaises(ValueError):
                transaction_7.check_order()

    def test_get_total_price_not_checked(self):
        """
        Test get_total_price when not checked.
        """
        transaction_8 = cashier.Transaction()
        with self.assertRaises(ValueError):
            transaction_8.get_total_price()
