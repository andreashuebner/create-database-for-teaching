from customers import create_customer_table

# Global options
output_dir = "database_files"

# Table specific options

# table customers
# See customers.txt for a documentation of table structure
# customers_input.txt contains helpers for some of the fields, many of them
# are also randomly generated
# specific options for table customers are set in customers.py


def create_database_files():
    customer_entries = create_customer_table()
    print(customer_entries)


if __name__ == "__main__":
    create_database_files()
