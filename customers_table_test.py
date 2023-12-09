import pytest

from customers import create_insert_statement
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

    def test_creates_valid_customer_entries(self):
        customer_entries = populate
    def test_create_insert_statement(self):
        customer_id = 1
        first_name = 'Andreas'
        last_name = 'Huebner'
        street = 'Garden Street'
        housenumber = 50
        city = 'San Francisco'
        postal_code = 51000
        state = 'CA'
        statement = create_insert_statement(customer_id, first_name, last_name, street, housenumber, postal_code,city,
                                            state)
        expected_statement = "insert into customers (customer_id,first_name,last_name,street,housenumber,po,city,state) values (1,'Andreas','Huebner','Garden Street','50',51000,'San Francisco','CA');"

        assert(statement == expected_statement)
