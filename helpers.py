import random

def load_file_content(path_to_file):
    """
    Loads the content of the file and returns it as a string.
    :param path_to_file:
    :return: A string with the content of the file
    """
    with open(path_to_file, 'r') as f:
        return f.read()
def return_random_value_from_list(list_of_values):
    """
    Returns a random value from a list of values
    :param list_of_values:
    :return: A random value from the list
    """

    return random.choice(list_of_values)

def substitute_template_variables(template, template_variables,template_values):
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
        template_value = template_values[i]
        template = template.replace(template_variable, template_value)

    return template