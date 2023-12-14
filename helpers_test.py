import pytest

from helpers import load_file_content
from helpers import remove_linebreaks_whitespaces
from helpers import return_random_value_from_list
from helpers import substitute_template_variables

from unittest import mock


class TestLoadFileContent:
    def test_read_existing_file(self):
        with mock.patch('builtins.open', mock.mock_open(read_data='Andreas Huebner\nPeter Panzer')):
            file_content = load_file_content('path')
            assert (file_content == 'Andreas Huebner\nPeter Panzer')


class TestRemoveWhiteSpaceLineBreaks:
    def test_returns_whitespaces_linebreaks_removed(self):
        test_string ='Andreas goes to school.\nHe likes school'
        clean_string = remove_linebreaks_whitespaces(test_string)
        assert(clean_string == 'Andreasgoestoschool.Helikesschool')

class TestReturnRandomValueFromList:
    def test_returned_value_is_in_list(self):
        list_of_values = ['Andreas', 'Peter', 'Lisa', 'Sandra']
        random_value = return_random_value_from_list(list_of_values)
        assert (random_value in list_of_values)


class TestSubstituteTemplateVariables:
    def test_substitutes_correctly_template_variables(self):
        template = '{{name}} went to holidays in {{city}}'
        template_with_substitution = substitute_template_variables(template,
                                                                   ['{{name}}', '{{city}}'],
                                                                   ['andreas', 'Berlin'])

        assert(template_with_substitution == 'andreas went to holidays in Berlin')
