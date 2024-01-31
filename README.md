# Objective of this repository
The objective of this repository is to offer a "quick-and-dirty" way to generate random datasets for a database.

# Structure of the created database
The file main.py will create (with the default settings) the SQL code to create the following tables:

- Table **customers**
- Table **products**
- Table **invoices**
- Table **product_categories**

The table names can be changed in the parameters in the file main.py

# Structure of table customers
- customer_id (INT, not null) - Primary Key
- first_name (String, not null)
- last_name (String, not null)
- street (String, not null)
- housenumber (String, not null)
- po (int, not null)
- city (String, not null)
- state (String, not null)

The names and street addresses are completely randomly generated (partly with the help of ChatGPT). 

# Structure of table products
- product_id (INT, not null) - Primary Key
- product_kategory_id (INT, not null) - Foreign key to table product_categories
- product_name (String, not null)

# Structure of table product_categories
- product_category_id (INT, not null) - Primary Key
- product_category_name (String, not null)

# Structure of table invoices
- id (INT, not null) - Primary key
- date (String, not null)
- invoice_id (INT, not null)- Invoice id can be repeated as one invoice id can appear multiple times if multiple items have been purchased)
- product_id (INT, not null) - Foreign key to table products
- number_units_purchased (INT, not null) - Number of items purchased (referring to a specific product_id)
- price_per_unit (FLOAT, not null) - The price for a single unit of a specific product

  # How to run
  To generate the datasets, you simply run python main.py.

  The SQL code to create the database can be found in database_files/create_database_customers.sql

  The SQL code to create the tables and insert the datasets can be found in database_files/customers.sql.

  # Parameters
  The following parameters can be adjusted in main.py

  - database_system: Currently only postgres is supported, but the generated queries should be usuable on other database systems as well with minimal adjustments.
    For each table creation/dataset insert operation, a template can be found in the folder templates. Each template name ends with the database system name as its suffix.
  - output_dir: The name of the output directory for the SQL statements to create the database, the tables and insert the data (default: database_files)
  - output_file_create_database_statement: The file name for the SQL to create the database (default: create_database_customers.sql)
  - output_file_sql_statements: The file name for the SQL statements to create the tables and insert the data (default: customers.sql)
  - database_name: The name of the database to create (default: db_customers)
  - table_name_customers: The table name for the customers table (default: customers)
  - table_name_invoices: The table name for the invoices table (default: invoices)
  - table_name_products: The table name for the products table (default: products)
  - table_name_product_categories: The table name for the product categories table (default: product_categories)
  - customer_start_value_primary_key: The start value of the primary key in customers table (customer_id is the primary key), default is 1
  - number_of_customer_entries_to_generate: How many random customer datasets to create (default: 500).
  - start_date_invoice_generation: The minimal date for the randomly generated invoices data (default: '2022-01-01')
  - end_date_invoice_generation: The maximum date for the randomly generated invoices data (default: '2023-12-31')
  - probability_invoice_per_customer_id_per_day: The probability that for a given customer_id for a given day an invoice dataset will be generated (default: 0.002, so 0.2%). So for each single day between start_date_invoice_generation
    and end_date_invoice_generation (inclusive), there will be (with the default value) a 0.2% chance that a random invoice dataset will be generated. With this parameter, you can finetune the number of invoices datasets generated.
  - minimum_number_different_products_per_invoice: The minimum number of unique products per invoice (default: 1)
  - maximum_number_different_products_per_invoice: The maximum number of unique products per invoice (default: 5). The actual number of different products per invoice dataset will be randomly chosen between the minimum and maximum number parameter
  - minimum_number_items_per_product: The minimum number of items in the invoice dataset per different product (default: 1)
  - maximum_number_items_per_product: The maximum number of items in the invoice dataset per different product (default: 10). The actual number will be randomly chosen between the minimum and maximum number parameter.
  - show_stats: Whether to show stats about the created datasets when running the file main.py (default: True)    
