from customers import create_customer_table
from helpers import load_file_content
from helpers import substitute_template_variables

import os

# Global options
database_system = 'postgres'  # supported options: currently only "postgres"
output_dir = 'database_files'  # output directory for all files created by script
output_file_sql_statements = 'customers.sql'  # The file name with all statements to create the customer database
# and populate it
database_name = 'db_customers'  # name of the database to create

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
    create_database_statement = substitute_template_variables(create_database_statement, ['{{database_name}}'],
                                                              [database_name])
    print(create_database_statement)
    # customer_entries = create_customer_table()
    # print(customer_entries)


if __name__ == "__main__":
    create_database_files()
