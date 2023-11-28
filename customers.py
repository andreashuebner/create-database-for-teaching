customers_start_value_primary_key = 1
number_of_customer_entries_to_generate = 1000

from collections import namedtuple


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
        customer = Customer(customer_id=i,first_name='',last_name='',
                            street='', housenumber='', po=0, city='', state='')
        customers.append(customer)

    return customers
