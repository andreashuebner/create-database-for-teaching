
from collections import namedtuple
from customers_params import (first_names, last_names, street_names, city_states)
from helpers import load_file_content
from helpers import return_random_value_from_list
from helpers import substitute_template_variables
import os
import random


def create_insert_statement_customers(database_system,table_name,customer_id, first_name, last_name, street, housenumber, postal_code,city,
                                            state):
    insert_statement = load_file_content('templates/insert_customers_' + database_system + '.txt')
    insert_statement = substitute_template_variables(insert_statement,
                                                     ['{{table_name}}',
                                                       '{{customer_id}}',
                                                      '{{first_name}}',
                                                      '{{last_name}}',
                                                      '{{street}}',
                                                      '{{housenumber}}',
                                                      '{{postal_code}}',
                                                      '{{city}}',
                                                      '{{state}}'],
                                                     [
                                                         table_name,
                                                         customer_id,
                                                         first_name,
                                                         last_name,
                                                         street,
                                                         housenumber,
                                                         postal_code,
                                                         city,
                                                         state
                                                     ])

    return insert_statement

def create_table_statement_customers(template_dir,database_system, table_name):
    create_table_customers_statement = load_file_content(
        os.path.join(template_dir, 'create_table_customers' + '_' + database_system + '.txt'))
    create_table_customers_statement = substitute_template_variables(create_table_customers_statement,
                                                                     ['{{table_name}}'],
                                                                     [table_name])
    return create_table_customers_statement

def populate_table_customers(start_value=1,
                            number_of_entries=10000):
    '''
    Create the entries for the customer table
    :return: A list of named tuples with the following entries
    customer_id: Number
    first_name: String
    last_name: String
    street: String
    housenumber: String
    po: Number
    city: String
    state: String
    '''

    Customer = namedtuple('Customer', ['customer_id', 'first_name', 'last_name', 'street', 'housenumber',
                                       'po','city', 'state'])

    customers = []
    for i in range(start_value, start_value + number_of_entries, 1):
        random_first_name = return_random_value_from_list(first_names)
        random_last_name = return_random_value_from_list(last_names)
        random_street_name = return_random_value_from_list(street_names) + ' Street'
        random_house_number = random.randint(1, 500)
        random_po = random.randint(10000,99999)
        random_city_state = return_random_value_from_list(city_states)
        random_city = random_city_state[0]
        random_state = random_city_state[1]

        customer = Customer(customer_id=i,first_name=random_first_name,last_name=random_last_name,
                            street=random_street_name, housenumber=random_house_number, po=random_po, city=random_city, state=random_state)
        customers.append(customer)


    return customers
