customers_start_value_primary_key = 1
number_of_customer_entries_to_generate = 1000

from collections import namedtuple
from customers_params import (first_names, last_names, street_names)
from helpers import return_random_value_from_list
import random


def populate_customer_table(start_value=customers_start_value_primary_key,
                            number_of_entries=number_of_customer_entries_to_generate):
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
    current_id = start_value
    for i in range(0, number_of_entries, 1):
        random_first_name = return_random_value_from_list(first_names)
        random_last_name = return_random_value_from_list(last_names)
        random_street_name = return_random_value_from_list(street_names) + ' Street'
        random_house_number = random.randint(1, 500)

        customer = Customer(customer_id=current_id,first_name=random_first_name,last_name=random_last_name,
                            street=random_street_name, housenumber=random_house_number, po=0, city='', state='')
        customers.append(customer)
        current_id += 1

    return customers
