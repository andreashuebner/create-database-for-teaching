from helpers import remove_linebreaks_whitespaces
from products import create_table_statement_products
from products import create_table_statement_product_categories
from products import create_insert_statement_products
from products import create_insert_statement_product_categories
from products import populate_table_products

import pytest
from unittest import mock

class TestProductsTable:
    def test_create_product_table(self):
        product_table_create_statement = create_table_statement_products('templates','postgres','products2')
        expected_statement = '''
        CREATE TABLE public.products2
(
    product_id integer NOT NULL,
    product_category_id integer NOT NULL,
    product_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT products2_pkey PRIMARY KEY (product_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.products2
    OWNER to postgres;
        '''
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        product_table_create_statement = remove_linebreaks_whitespaces(product_table_create_statement)
        assert(expected_statement == product_table_create_statement)

    def test_create_product_categories_table(self):
        product_table_create_statement = create_table_statement_product_categories('templates', 'postgres', 'product_categories2')
        expected_statement = '''
        CREATE TABLE public.product_categories2
    (
        product_category_id integer NOT NULL,
        product_category_name text COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT product_categories2_pkey PRIMARY KEY (product_category_id)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.product_categories2
        OWNER to postgres;
            '''
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        product_table_create_statement = remove_linebreaks_whitespaces(product_table_create_statement)
        assert (expected_statement == product_table_create_statement)

    def test_populate_products_with_primary_keys_start_1(self):
        products = [
            ('Jeans', 'Clothes', 30.73),
            ('Smartwatch', 'Electronics', 120.46),
            ('Coffee Maker', 'Home and Kitchen', 40.3),
            ('Basketball', 'Sports and Outdoors', 80.96),
            ('Sunglasses', 'Fashion', 30.99),
            ('Facial Moisturizer', 'Beauty', 5.56),
            ('Jeans2', 'Clothes', 50.50),
            ('Chocolate', 'Sweets', 2)
        ]
        product_list = populate_table_products(products)
        assert(product_list[0][0] == 1) # First product id must be 1
        assert (product_list[0][1] == 1) # first product category id must be 1
        assert (product_list[0][2] == 'Jeans')
        assert (product_list[1][0] == 2)
        assert (product_list[1][1] == 2)
        assert (product_list[1][2] == 'Smartwatch')
        assert (product_list[2][0] == 3)
        assert (product_list[2][1] == 3)
        assert (product_list[2][2] == 'Coffee Maker')
        assert (product_list[3][0] == 4)
        assert (product_list[3][1] == 4)
        assert (product_list[3][2] == 'Basketball')
        assert (product_list[4][0] == 5)
        assert (product_list[4][1] == 5)
        assert (product_list[4][2] == 'Sunglasses')
        assert (product_list[5][0] == 6)
        assert (product_list[5][1] == 6)
        assert (product_list[5][2] == 'Facial Moisturizer')
        assert (product_list[6][0] == 7)
        assert (product_list[6][1] == 1) # Same product category as Jeans
        assert (product_list[6][2] == 'Jeans2')
        assert(product_list[7][0] == 8)
        assert(product_list[7][1] == 7)
        assert(product_list[7][2] == 'Chocolate')


    def test_create_insert_statement_products(self):
        insert_statement = create_insert_statement_products('postgres', 'products2', 5, 7, 'Jeans')
        insert_statement = remove_linebreaks_whitespaces(insert_statement)
        expected_statement = '''
        insert into products2 (product_id,product_category_id,product_name) values (5,7,'Jeans');
        '''
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        assert(insert_statement == expected_statement)

    def test_create_insert_statement_product_categories(self):
        products = [
            ('Jeans', 'Clothes', 30.73),
            ('Smartwatch', 'Electronics', 120.46),
            ('Coffee Maker', 'Home and Kitchen', 40.3),
            ('Basketball', 'Sports and Outdoors', 80.96),
            ('Sunglasses', 'Fashion', 30.99),
            ('Facial Moisturizer', 'Beauty', 5.56),
            ('Jeans2', 'Clothes', 50.50),
            ('Chocolate', 'Sweets', 2)
        ]
        # so we are expecting the following product categories
        # 1 = Clothes, 2 = Electronics, 3 = Home and Kitchen, 4 = Sports and Outdoors,
        # 5 = Fashion, 6 = Beauty, 7 = Sweets
        expected_statement = ''
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (1,'Clothes');"
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (2,'Electronics');"
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (3,'Home and Kitchen');"
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (4,'Sports and Outdoors');"
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (5,'Fashion');"
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (6,'Beauty');"
        expected_statement += "insert into product_categories2 (product_category_id,product_category_name) values (7,'Sweets');"

        insert_statement = create_insert_statement_product_categories('postgres','product_categories2',products)
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        insert_statement = remove_linebreaks_whitespaces(insert_statement)
        assert(insert_statement == expected_statement)






