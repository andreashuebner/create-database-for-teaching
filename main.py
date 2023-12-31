from customers import create_insert_statement_customers
from customers import create_table_statement_customers
from customers import populate_table_customers
from helpers import load_file_content
from helpers import substitute_template_variables
from invoices import create_table_statement_invoices
from invoices import create_insert_statement_invoices
from invoices import populate_table_invoices
from products_params import products
from products import create_table_statement_products
from products import create_table_statement_product_categories
from products import create_insert_statement_products
from products import create_insert_statement_product_categories
from products import populate_table_products

import os

# Global options that can be adjusted #################################
database_system = 'postgres'  # supported options: currently only "postgres"
output_dir = 'database_files'  # output directory for all files created by script
output_file_create_database_statement = 'create_database_customers.sql'
output_file_sql_statements = 'customers.sql'  # The file name with all statements to create the customer database
# and populate it
database_name = 'db_customers'  # name of the database to create
table_name_customers = 'customers'
table_name_invoices = 'invoices'
table_name_products = 'products'
table_name_product_categories = 'product_categories'
customers_start_value_primary_key = 1
number_of_customer_entries_to_generate = 100
start_date_invoice_generation = '2022-01-01'
end_date_invoice_generation = '2023-12-31'
probability_invoice_per_customer_id_per_day = 0.002 # Probability to generate an invoice for a single customers per day
minimum_number_different_products_per_invoice = 1 # Minimum number of products to generate per invoice
maximum_number_different_products_per_invoice = 5 # Maximum number of products to generate per invoice
minimum_number_items_per_product = 1 # Minimum number of items to generate per product
maximum_number_items_per_product = 10 # Maximum number of items to generate per product
show_stats = True # Whether to print stats about the created data

# End global options that can be adjusted ##################################################

# Global parameters
template_dir = 'templates'


# Table specific options

# table customers
# See customers.txt for a documentation of table structure
# customers_input.txt contains helpers for some of the fields, many of them
# are also randomly generated
# specific options for table customers are set in customers.py


def create_database_files():
    create_database_statement = load_file_content(
        os.path.join(template_dir, 'create_database' + '_' + database_system + '.txt'))

    output_create_database = ''
    output_create_and_populate_tables = ''
    create_database_statement = substitute_template_variables(create_database_statement, ['{{database_name}}'],
                                                              [database_name])
    output_create_database += create_database_statement
    output_create_database += '\n'
    if show_stats:
        print('Statement to create database',database_name,'created')

    create_table_customers_statement = create_table_statement_customers(template_dir,database_system,'customers')
    output_create_and_populate_tables += create_table_customers_statement
    output_create_and_populate_tables += '\n'
    if show_stats:
        print('Statement to create table', table_name_customers,'created')
    customer_entries = populate_table_customers(1,10000)
    for entry in customer_entries:
        customer_id = entry.customer_id
        first_name = entry.first_name
        last_name = entry.last_name
        street = entry.street
        housenumber = entry.housenumber
        postal_code = entry.po
        city = entry.city
        state = entry.state
        statement = create_insert_statement_customers(database_system,table_name_customers,customer_id,first_name,last_name,street,housenumber,
                                            postal_code,city,state)
        output_create_and_populate_tables += statement
        output_create_and_populate_tables += '\n'
    if show_stats:
        print('Statement to populate table',table_name_customers,'created with',len(customer_entries),'entries.')
    output_create_and_populate_tables += '\n'
    create_table_products_statement = create_table_statement_products(template_dir,database_system,'products')
    output_create_and_populate_tables += create_table_products_statement
    output_create_and_populate_tables += '\n\n'
    if show_stats:
        print('Statement to create table',table_name_products,'created')

    product_entries = populate_table_products(products)
    for entry in product_entries:
        product_id = entry[0]
        product_category_id = entry[1]
        product_name = entry[2]
        insert_statement = create_insert_statement_products(database_system,table_name_products,product_id,product_category_id,product_name)
        output_create_and_populate_tables += insert_statement
        output_create_and_populate_tables += '\n'

    if show_stats:
        print('Statement to populate table',table_name_products,'created with',len(product_entries),'entries.')
    output_create_and_populate_tables += '\n\n'
    create_table_product_category_statement = create_table_statement_product_categories(template_dir, database_system, table_name_product_categories)
    output_create_and_populate_tables += create_table_product_category_statement
    output_create_and_populate_tables += '\n\n'
    if show_stats:
        print('Statement to create table', table_name_product_categories, 'created')

    insert_statement_product_categories = create_insert_statement_product_categories(database_system, table_name_product_categories,products)
    output_create_and_populate_tables += insert_statement_product_categories
    output_create_and_populate_tables += '\n\n'
    if show_stats:
        print('Statement to populate table', table_name_product_categories, 'created')

    output_create_and_populate_tables += '\n\n'
    create_table_invoices_statement = create_table_statement_invoices(template_dir, database_system,
                                                                                        table_name_invoices)
    output_create_and_populate_tables += create_table_invoices_statement
    output_create_and_populate_tables += '\n\n'
    if show_stats:
        print('Statement to create table', table_name_invoices, 'created')


    invoice_items = populate_table_invoices(customer_entries,product_entries,
                                        start_date_invoice_generation, end_date_invoice_generation,
                                        probability_invoice_per_customer_id_per_day,
                                        minimum_number_different_products_per_invoice, maximum_number_different_products_per_invoice,
                                        minimum_number_items_per_product, maximum_number_items_per_product)



    insert_statements = []
    for invoice_item in invoice_items:
        date = invoice_item[0]
        customer_id = invoice_item[1]
        invoice_id = invoice_item[2]
        product_id = invoice_item[3]
        number_items = invoice_item[4]
        item_price = invoice_item[5]
        insert_statement = create_insert_statement_invoices(database_system,
                                                        table_name_invoices,
                                                        date,
                                                        customer_id,
                                                        product_id,
                                                        invoice_id,
                                                        number_items,
                                                        item_price)

        insert_statements.append(insert_statement)


    insert_statement_string = '\n'.join(insert_statements)
    output_create_and_populate_tables += insert_statement_string
    if show_stats:
        print('Statement to populate table' ,table_name_invoices, 'created with',len(insert_statements), 'datasets')





    with open(os.path.join(output_dir,output_file_create_database_statement),'w') as output_file:
        output_file.write(output_create_database)
    with open(os.path.join(output_dir,output_file_sql_statements),'w') as output_file:
        output_file.write(output_create_and_populate_tables)

    if show_stats:
        print('Files written into folder',output_dir)



if __name__ == "__main__":
    create_database_files()
