import datetime
import pytest

from helpers import date_to_string
from helpers import date_string_to_date
from helpers import load_file_content
from helpers import remove_linebreaks_whitespaces
from helpers import return_random_value_from_list
from helpers import substitute_template_variables
from helpers import InvalidDateStringError

from unittest import mock


class TestDateFunctions:

    def test_throws_error_invalid_date_string(self):
        test_cases = [
            "23-03-05",
            "2023-3-05",
            "2023-03-1"
        ]
        for test_case in test_cases:
            with pytest.raises(InvalidDateStringError, match=r'Date string must be in format yyyy-MM-dd'):
                date_string_to_date(test_case)
    def test_date_to_string(self):
        test_cases = [
            (2023,3,5,'2023-03-05'),
            (2023,1,25,'2023-01-25'),
            (2022,10,1,'2022-10-01')
        ]

        for test in test_cases:
            year = test[0]
            month = test[1]
            day = test[2]
            date_string_expected = test[3]
            date = datetime.date(year, month,day)
            date_string = date_to_string(date)
            assert(date_string_expected == date_string)


    def test_string_to_date(self):
        test_cases = [
            ('2023-03-05',2023,3,5),
            ('2023-01-25',2023,1,25),
            ('2022,10,01',2022,10,1)
        ]
        for test in test_cases:
            date_string = test[0]
            year = test[1]
            month = test[2]
            day = test[3]
            date_returned = date_string_to_date(date_string)
            assert(date_returned == datetime.date(year,month,day))
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
