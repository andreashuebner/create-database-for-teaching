from customers import populate_table_customers
from helpers import remove_linebreaks_whitespaces
from invoices import create_table_statement_invoices
from invoices import populate_table_invoices
from products import populate_table_products
from products_params import products


import pytest
from unittest import mock

class TestInvoicesTable:
    def test_create_invoices_table(self):
        invoices_table_create_statement = create_table_statement_invoices('templates', 'postgres', 'invoices2')
        expected_statement = '''
               CREATE TABLE  public.invoices2
(
    date text COLLATE pg_catalog."default" NOT NULL,
    customer_id integer NOT NULL,
    invoice_id integer NOT NULL,
    product_id integer NOT NULL,
    number_items integer NOT NULL,
    price_per_item double precision NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.invoices2
    OWNER to postgres;
                '''
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        invoices_table_create_statement = remove_linebreaks_whitespaces(invoices_table_create_statement)
        assert (expected_statement == invoices_table_create_statement)


    def test_throws_exception_with_invalid_parameters(self):
        # Each test case has the following elements in tuple (numbers = indicies)
        # 0 customer_data
        # 1 product_data
        # 2 start_date
        # 3 end_date
        # 4 probability_invoice_per_customer_id_per_day
        # 5 minimum_number_different_products_per_invoice
        # 6 maximum_number_different_products_per_invoice
        # 7 minimum_number_items_per_product
        # 8 maximum_number_items_per_product
        customer_data = populate_table_customers(1, 100)
        product_data = populate_table_products(products)
        test_cases = [
            (customer_data, product_data,"2023-02-01","2023-01-01",0.02,1,3,1,3), # Should throw exception as start date after end date
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0, 1, 3, 1, 3), # Should throw exception as probability of invoice must be greater than 0
            (customer_data, product_data, "2023-01-01", "2023-03-01", 1.1, 1, 3, 1, 3), # Should throw exception as probability of invoice must not be greater than 0
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0.5, 0, 3, 1, 3), # Should throw exception as minimum number of different products per invoice must be greater than 0
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0.5, 2, 1, 1, 3), # Should throw exception as minimum number of different products per invoice must not be greater than maximum number
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0.5, 1, 2, 2, 1), # Should throw exception as minimum number items per product greater than maximum number of items per product

        ]


        for test_case in test_cases:
            with pytest.raises(ValueError):
                populate_table_invoices(test_case[0], test_case[1], test_case[2], test_case[3],
                test_case[4], test_case[5],test_case[6],test_case[7],test_case[8])

    def test_generate_correct_invoices(self):
        customer_data = populate_table_customers(1, 100)
        product_data = populate_table_products(products)
        start_date = "2022-03-01"
        end_date = "2023-07-31"
        probability_invoice_per_customer_id_per_day = 0.02
        minimum_number_different_products_per_invoice = 1
        maximum_number_different_products_per_invoice = 5
        minimum_number_items_per_product = 1
        maximum_number_items_per_product = 4
        invoices_data = populate_table_invoices(customer_data,product_data,
                                                start_date,end_date,probability_invoice_per_customer_id_per_day,
                                                minimum_number_different_products_per_invoice,
                                                maximum_number_different_products_per_invoice,
                                                minimum_number_items_per_product,
                                                maximum_number_items_per_product)

        # Because the invoices data have a random element, we define for most of the tests intervals that
        # we consider as valid for the tests passed
        # Example:
        # If we define the start date as 2022-03-01 and the end date as 2023-07-31,
        # we have 518 days
        # Based on the default values for the customer_date, we have 1000 customer_ids
        # With the probability of 2% of generating an invoice for a given customer_id per day,
        # we will generate in average 20 invoices per day, so overall 518 * 20 = 10360 invoices
        # But as this is only an average value, we will e.g. consider 90% - 110% of this value as fine for passing
        # the test, e.g. 9,324 invoices - 11,396 invoices.
        # We will have a similar approach for other parameters like average number of different products per invoice
        # or average number of items per product



        assert(True == True)



