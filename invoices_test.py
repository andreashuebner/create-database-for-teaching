from customers import populate_table_customers
from helpers import remove_linebreaks_whitespaces
from invoices import create_insert_statement_invoices
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
            (customer_data, product_data, "2023-02-01", "2023-01-01", 0.02, 1, 3, 1, 3),
            # Should throw exception as start date after end date
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0, 1, 3, 1, 3),
            # Should throw exception as probability of invoice must be greater than 0
            (customer_data, product_data, "2023-01-01", "2023-03-01", 1.1, 1, 3, 1, 3),
            # Should throw exception as probability of invoice must not be greater than 0
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0.5, 0, 3, 1, 3),
            # Should throw exception as minimum number of different products per invoice must be greater than 0
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0.5, 2, 1, 1, 3),
            # Should throw exception as minimum number of different products per invoice must not be greater than maximum number
            (customer_data, product_data, "2023-01-01", "2023-03-01", 0.5, 1, 2, 2, 1),
            # Should throw exception as minimum number items per product greater than maximum number of items per product

        ]

        for test_case in test_cases:
            with pytest.raises(ValueError):
                populate_table_invoices(test_case[0], test_case[1], test_case[2], test_case[3],
                                        test_case[4], test_case[5], test_case[6], test_case[7], test_case[8])

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
        invoices_data = populate_table_invoices(customer_data, product_data,
                                                start_date, end_date, probability_invoice_per_customer_id_per_day,
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

        # Overall, we have 518 days and 100 customers
        # So we would expect around 1,036 unique invoice ids (518 * 100 * 0.02)
        # Count the number of unique invoice ids. Because of low data volume, we choose a non-optimum algorithm
        # for the sake of keeping it simple, even when using a list for membership tests
        unique_invoice_ids = []
        unique_customer_ids = []
        unique_product_ids = []
        for invoice in invoices_data:
            customer_id = invoice[1]
            invoice_id = invoice[2]
            product_id = invoice[3]

            if customer_id not in unique_customer_ids:
                unique_customer_ids.append(customer_id)
            if invoice_id not in unique_invoice_ids:
                unique_invoice_ids.append(invoice_id)
            if product_id not in unique_product_ids:
                unique_product_ids.append(product_id)

        number_unique_invoices = len(unique_invoice_ids)
        assert (number_unique_invoices >= 950 and number_unique_invoices <= 1150)

        # In the invoices data, every customer_id should also be part of the customer datasets
        # and every product_id should be part of the product datasets
        customer_ids_in_customer_data = {}
        product_ids_in_product_data = {}
        for customer in customer_data:
            customer_ids_in_customer_data[customer.customer_id] = 1

        for product in product_data:
            product_ids_in_product_data[product[0]] = 1

        for customer_id in unique_customer_ids:
            assert (customer_id in customer_ids_in_customer_data)

        for product_id in unique_product_ids:
            assert (product_id in product_ids_in_product_data)

        # Check that primary keys are correctly populated
        sum_unique_invoice_ids = sum(unique_invoice_ids)
        check_sum_unique_invoice_ids = 0
        for i in range(len(unique_invoice_ids)):
            check_sum_unique_invoice_ids += (i + 1)

        assert (check_sum_unique_invoice_ids == sum_unique_invoice_ids)

        # Check that number of different products per invoice are correctly populated
        # Build a hash with each invoice id being the key and the unique product ids being the value in a list
        # Then go through each invoice id and make sure that the number of unique product ids is not below
        # the minimum and the maximum
        # Also ensure that the number of different products per invoice are about equally distributed

        hash_products_per_invoice = {}
        hash_counter_distribution_number_products_invoice = {}

        for invoice in invoices_data:
            invoice_id = invoice[2]
            product_id = invoice[3]
            if invoice_id not in hash_products_per_invoice:
                hash_products_per_invoice[invoice_id] = []

            if product_id not in hash_products_per_invoice[invoice_id]:
                hash_products_per_invoice[invoice_id].append(product_id)

        for invoice_id in hash_products_per_invoice:
            number_different_product_ids = len(hash_products_per_invoice[invoice_id])
            if number_different_product_ids not in hash_counter_distribution_number_products_invoice:
                hash_counter_distribution_number_products_invoice[number_different_product_ids] = 0
            hash_counter_distribution_number_products_invoice[number_different_product_ids] += 1
            assert (number_different_product_ids >= minimum_number_different_products_per_invoice)
            assert (number_different_product_ids <= maximum_number_different_products_per_invoice)

        # Check distribution of number_of_product_ids_per_invoice
        # First get the number of different combinations
        number_different_combinations = 0
        for key in hash_counter_distribution_number_products_invoice:
            number_different_combinations += 1

        reference_value_per_bucket = len(unique_invoice_ids) / number_different_combinations
        for key in hash_counter_distribution_number_products_invoice:
            number_combinations = hash_counter_distribution_number_products_invoice[key]
            # Check that each number_of_different_products_per_invoice_id is within 70% - 130% range
            assert (
                    number_combinations >= reference_value_per_bucket * 0.7 and
                    number_combinations <= reference_value_per_bucket * 1.3)

        # TODO: Add more tests here
    def test_create_insert_statement_invoices(self):
        insert_statement = create_insert_statement_invoices('postgres','invoices2', '2023-03-04',5,10,15,3,3.52)
        insert_statement = remove_linebreaks_whitespaces(insert_statement)
        expected_statement = '''
        insert into invoices2 (date,customer_id,invoice_id,product_id,number_items,price_per_item) values ('2023-03-04',5,10,15,3,3.52);
        '''
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        assert(expected_statement == insert_statement)

