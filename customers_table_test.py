import pytest

from customers import populate_customer_table


class TestPopulateCustomerTable:
    def test_returns_correct_number_of_entries(self):
        customer_entries = populate_customer_table()
        assert(len(customer_entries) == 1000) # default value, if now parameters
        customer_entries = populate_customer_table(number_of_entries=205)
        assert (len(customer_entries) == 205)

    def test_creates_correct_primary_key_start_1(self):
        customer_entries = populate_customer_table()
        assert (customer_entries[0].customer_id == 1)
        assert (customer_entries[1].customer_id == 2)
        assert (customer_entries[999].customer_id == 1000)

    def test_creates_correct_primary_key_start_50(self):
        customer_entries = populate_customer_table(start_value=50)
        assert (customer_entries[0].customer_id == 50)
        assert (customer_entries[1].customer_id == 51)
        assert (customer_entries[999].customer_id == 1049)
