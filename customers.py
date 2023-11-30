customers_start_value_primary_key = 1
number_of_customer_entries_to_generate = 1000

from collections import namedtuple
from customers_params import (first_names, last_names, street_names)
from helpers import return_random_value_from_list
import random


def create_customer_table():
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
    for i in range(1, number_of_customer_entries_to_generate + 1, 1):
        random_first_name = return_random_value_from_list(first_names)
        random_last_name = return_random_value_from_list(last_names)
        random_street_name = return_random_value_from_list(street_names) + ' Street'
        random_house_number = random.randint(1, 500)

        customer = Customer(customer_id=i,first_name=random_first_name,last_name=random_last_name,
                            street=random_street_name, housenumber=random_house_number, po=0, city='', state='')
        customers.append(customer)

    return customers
