from helpers import load_file_content
from helpers import substitute_template_variables

import os


def create_table_statement_products(template_dir, database_system, table_name):
    create_table_product_statement = load_file_content(
        os.path.join(template_dir, 'create_table_products' + '_' + database_system + '.txt'))
    create_table_product_statement = substitute_template_variables(create_table_product_statement,
                                                                   ['{{table_name}}'],
                                                                   [table_name])
    return create_table_product_statement

def create_table_statement_product_categories(template_dir, database_system, table_name):
    create_table_product_categories_statement = load_file_content(
        os.path.join(template_dir, 'create_table_product_categories' + '_' + database_system + '.txt'))
    create_table_product_categories_statement = substitute_template_variables(create_table_product_categories_statement,
                                                                   ['{{table_name}}'],
                                                                   [table_name])
    return create_table_product_categories_statement

def create_insert_statement_products(database_system,table_name,product_id, product_category_id, product_name):
    insert_statement = load_file_content('templates/insert_products_' + database_system + '.txt')
    insert_statement = substitute_template_variables(insert_statement,
                                                     ['{{table_name}}',
                                                       '{{product_id}}',
                                                      '{{product_category_id}}',
                                                      '{{product_name}}'],
                                                     [
                                                         table_name,
                                                         product_id,
                                                         product_category_id,
                                                         product_name
                                                     ])

    return insert_statement

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
    product_list = []
    product_categories = {}
    current_product_id = start_value_primary_key_products
    current_product_category_id = start_value_primary_key_product_categories
    for i in range(len(products)):
        current_product_tuple = products[i]
        current_product = current_product_tuple[0]
        current_product_category = current_product_tuple[1]
        product_id_to_append = current_product_id
        current_product_id += 1
        if current_product_category not in product_categories:
            product_category_id_to_append = current_product_category_id
            product_categories[current_product_category] = product_category_id_to_append
            current_product_category_id += 1
        else:
           product_category_id_to_append = product_categories[current_product_category]

        product_entry = (product_id_to_append,product_category_id_to_append,current_product)
        product_list.append(product_entry)

    return product_list
