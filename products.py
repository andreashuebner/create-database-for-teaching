from helpers import load_file_content
from helpers import substitute_template_variables


import os

def create_table_statement_products(template_dir,database_system, table_name):
    create_table_product_statement = load_file_content(
        os.path.join(template_dir, 'create_table_products' + '_' + database_system + '.txt'))
    create_table_product_statement = substitute_template_variables(create_table_product_statement,
                                                                     ['{{table_name}}'],
                                                                     [table_name])
    return create_table_product_statement

def populate_table_products(products,
                            start_value_primary_key_products=1,
                            start_value_primary_key_product_categories=1
                            ):
    '''
    Generates the datasets for the table products based on content in products_params.py
    :param products The list of products in the format as shown in products_params.py
    :param start_value_primary_key_products: The start value for the primary key in products table
    :param start_value_primary_key_product_categories=1
    :return: A list of tuples with the following elements:
    (product_id, product_category_id, product_name)
    '''
    return []