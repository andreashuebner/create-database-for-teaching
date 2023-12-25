import pytest

from customers import create_insert_statement_customers
from customers import create_table_statement_customers
from customers import populate_table_customers


class TestPopulateCustomerTable:
    def test_returns_correct_number_of_entries(self):
        customer_entries = populate_table_customers(1,1000)
        assert(len(customer_entries) == 1000) # default value, if now parameters
        customer_entries = populate_table_customers(number_of_entries=205)
        assert (len(customer_entries) == 205)

    def test_creates_correct_primary_key_start_1(self):
        customer_entries = populate_table_customers(1,1000)
        assert (customer_entries[0].customer_id == 1)
        assert (customer_entries[1].customer_id == 2)
        assert (customer_entries[999].customer_id == 1000)

    def test_creates_correct_primary_key_start_50(self):
        customer_entries = populate_table_customers(start_value=50)
        assert (customer_entries[0].customer_id == 50)
        assert (customer_entries[1].customer_id == 51)
        assert (customer_entries[999].customer_id == 1049)

    def test_create_table_statement(self):
        table_statement = create_table_statement_customers('templates','postgres','customers2')
        table_statement = table_statement.replace('\n','')
        table_statement = table_statement.replace(' ','')
        expected_statement = '''
        CREATE TABLE public.customers2
(
    customer_id integer NOT NULL,
    first_name text COLLATE pg_catalog."default" NOT NULL,
    last_name text COLLATE pg_catalog."default" NOT NULL,
    street text COLLATE pg_catalog."default" NOT NULL,
    housenumber text COLLATE pg_catalog."default" NOT NULL,
    po integer NOT NULL,
    city text COLLATE pg_catalog."default" NOT NULL,
    state text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customers2_pkey PRIMARY KEY (customer_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customers2
    OWNER to postgres;
        '''
        expected_statement = expected_statement.replace('\n','')
        expected_statement = expected_statement.replace(' ','')
        assert(expected_statement == table_statement)
    def test_create_insert_statement(self):
        table_name = 'customers2'
        customer_id = 1
        first_name = 'Andreas'
        last_name = 'Huebner'
        street = 'Garden Street'
        housenumber = 50
        city = 'San Francisco'
        postal_code = 51000
        state = 'CA'
        statement = create_insert_statement_customers('postgres',table_name,customer_id, first_name, last_name, street, housenumber, postal_code,city,
                                            state)
        expected_statement = "insert into customers2 (customer_id,first_name,last_name,street,housenumber,po,city,state) values (1,'Andreas','Huebner','Garden Street','50',51000,'San Francisco','CA');"

        assert(statement == expected_statement)
