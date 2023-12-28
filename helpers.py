import datetime
import random

error_message_invalid_date_string = 'Date string must be in format yyyy-MM-dd'
error_message_invalid_input_unique_values_from_list = 'First argument must be a non-empty list and second parameter (number of unique items) must be an integer greater than 0'


class InvalidDateStringError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def date_to_string(date):
    """
    Converts a datetime date to a string in format yyyy-MM-dd
    :param date: datetime.date object
    :return:
        A string representation in format yyyy-MM-dd
    """
    year_str = str(date.year)
    month_str = str(date.month)
    day_str = str(date.day)
    if len(month_str) == 1:
        month_str = '0' + month_str
    if len(day_str) == 1:
        day_str = '0' + day_str
    return year_str + '-' + month_str + '-' + day_str


def date_string_to_date(date_string):
    """
    Converts a string in format yyyy-MM-dd to datetime.date object
    :param date_string: A string in format yyyy-MM-dd
    :return: The string converted to datetime.date object
    """
    if len(date_string) != 10:
        raise InvalidDateStringError(error_message_invalid_date_string)
    year = date_string[0:4]
    month = date_string[5:7]
    day = date_string[8:]
    return datetime.date(int(year), int(month), int(day))


def load_file_content(path_to_file):
    """
    Loads the content of the file and returns it as a string.
    :param path_to_file:
    :return: A string with the content of the file
    """
    with open(path_to_file, 'r') as f:
        return f.read()


def remove_linebreaks_whitespaces(string_to_clean):
    clean_string = string_to_clean.replace('\n', '')
    clean_string = clean_string.replace(' ', '')
    return clean_string


def return_random_value_from_list(list_of_values):
    """
    Returns a random value from a list of values
    :param list_of_values:
    :return: A random value from the list
    """

    return random.choice(list_of_values)


def return_random_unique_values_from_list(list_of_values, number_unique_items_requested):
    if not isinstance(list_of_values, list) or not isinstance(number_unique_items_requested, int) or number_unique_items_requested <= 0:
        raise ValueError(error_message_invalid_input_unique_values_from_list)
    else:
        # Copy the unique items into a second list
        items_copied = {}
        items_unique = []
        for element in list_of_values:
            if element not in items_copied:
                items_unique.append(element)
                items_copied[element] = 1

        number_unique_items = len(items_unique)
        if number_unique_items < number_unique_items_requested:
            raise ValueError('Less unique items in list than requested')

        items_unique_to_return = []
        for i in range(number_unique_items_requested):
            random_element = random.choice(items_unique)
            items_unique_to_return.append(random_element)
            items_unique.remove(random_element)

        return items_unique_to_return




def substitute_template_variables(template, template_variables, template_values):
    """
    Substitutes one or more template variables in a string.
    Example call: substitute_template_variables(template_string, ['{{customer}}','{{customer2}}'],['andreas','peter])
    This will substitute {{customers}] with 'andreas' and {{customer2}} with 'peter'
    :param template: The template string
    :param template_variables: A list of template variables to substitute
    :param template_values: A list of template values that will substitute the template variables
    :return: The template string with all template variables replaced
    """

    for i in range(len(template_variables)):
        template_variable = template_variables[i]
        template_value = str(template_values[i])
        template = template.replace(template_variable, template_value)

    return template
