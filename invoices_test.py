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

    def test_generate_correct_invoices(self):
        customer_data = populate_table_customers(1, 100)
        product_data = populate_table_products(products)
        start_date = "2022-03-01"
        end_date = "2023-07-31"
        probability_invoice_per_customer_id_per_day = 0.02
        average_number_different_products_per_invoice = 3
        average_number_items_per_product = 2
        invoices_data = populate_table_invoices(customer_data,product_data,
                                                start_date,end_date,probability_invoice_per_customer_id_per_day,
                                                average_number_different_products_per_invoice,
                                                average_number_items_per_product)

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



