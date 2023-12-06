from customers import populate_customer_table
from helpers import load_file_content
from helpers import substitute_template_variables

import os

# Global options
database_system = 'postgres'  # supported options: currently only "postgres"
output_dir = 'database_files'  # output directory for all files created by script
output_file_create_database_statement = 'create_database_customers.sql'
output_file_sql_statements = 'customers.sql'  # The file name with all statements to create the customer database
# and populate it
database_name = 'db_customers'  # name of the database to create
table_name_customers = 'customers'
show_stats = True # Whether to print stats about the created data

# Global parameters (please do not modify)
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
        print('Statement to create database",database_name,"created')

    create_table_customers_statement = load_file_content(
        os.path.join(template_dir, 'create_table_customers' + '_' + database_system + '.txt'))
    create_table_customers_statement = substitute_template_variables(create_table_customers_statement, ['{{table_name}}'],
                                                              [table_name_customers])
    output_create_and_populate_tables += create_table_customers_statement
    output_create_and_populate_tables += '\n'
    if show_stats:
        print('Statement to create table', table_name_customers,'created')
    customer_entries = populate_customer_table()
    if show_stats:
        print('Statement for table',table_name_customers,'created with',len(customer_entries),'entries.')

    with open(os.path.join(output_dir,output_file_create_database_statement),'w') as output_file:
        output_file.write(output_create_database)
    with open(os.path.join(output_dir,output_file_sql_statements),'w') as output_file:
        output_file.write(output_create_and_populate_tables)

    if show_stats:
        print('Files written into folder',output_dir)



if __name__ == "__main__":
    create_database_files()
