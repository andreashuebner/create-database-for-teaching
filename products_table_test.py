from helpers import remove_linebreaks_whitespaces
from products import create_table_statement_products

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
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.products2
    OWNER to postgres;
        '''
        expected_statement = remove_linebreaks_whitespaces(expected_statement)
        product_table_create_statement = remove_linebreaks_whitespaces(product_table_create_statement)
        assert(expected_statement == product_table_create_statement)
