import requests
from bs4 import BeautifulSoup
import re


def authenticate_via_sis(name, surname, login=None, uk_id=None, is_employee='student'):
    """
    Simple authentication via sis.
    Employee must submit: name, surname
    Student must submit: name, surname, (login or uk_id)
    :param name: name of the person - obligatory:
    :param surname: surname of the person - obligatory:
    :param login: login for students
    :param uk_id: uk_id for students
    :param is_employee: bool if the person is employee
    :return: True if such person exists, False otherwise
    """
    if is_employee == 'employee':
        if not name or not surname:
            # expecting both name and surname
            print('Expected both name and surname\nName={}\nSurname={}'.format(name, surname))
            return False
        return __authenticate_employee(name=name, surname=surname)
    else:
        if not name or not surname:
            # expecting both name and surname
            print('Expected both name and surname\nName = {}\nSurname = {}'.format(name, surname))
            return False
        if not login and not uk_id:
            # expecting at least one of the following login, uk_id
            print('Expected at least one of login, uk_id\nLogin = {}\nuk_id = {}'.format(login, uk_id))
            return False
        return __authenticate_student(name=name, surname=surname, login=login, uk_id=uk_id)


def __authenticate_student(name, surname, login=None, uk_id=None):
    """
    Checks if such student exits when asked at is.cuni.cz/studium/kdojekdo
    :param name: name
    :param surname: surname
    :param login: login
    :param uk_id: UKČO
    :return: True if such person exists, False otherwise
    """
    url = __build_url(is_employee=False, name=name, surname=surname, login=login, uk_id=uk_id)
    page = requests.get(url)
    nubmer_of_results = __get_number_of_students(page=page)

    if int(nubmer_of_results) >= 1:
        return True
    return False


def __authenticate_employee(name, surname):
    """
    Checks if such employee exits when asked at is.cuni.cz/studium/kdojekdo
    :param name: name
    :param surname: surname
    :return: True if such person exists, False otherwise
    """
    url = __build_url(is_employee=True, name=name, surname=surname)
    page = requests.get(url)
    nubmer_of_results = __get_number_of_employees(page=page)

    if int(nubmer_of_results) >= 1:
        return True
    return False


def __get_number_of_employees(page):
    """
    Searches for number of results at queried page
    :param page: queried page with results
    :return: number of employees in the results
    """
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('#page_div > b:nth-child(3)')
    for text in content:
        for part in text:
            return __get_number(part)
    return 0


def __get_number_of_students(page):
    """
    Searches for number of results at queried page
    :param page: queried page with results
    :return: number of students in the results
    """
    soup = BeautifulSoup(page.content, 'html.parser')

    content = soup.select('#page_div > b:nth-child(3)')
    for text in content:
        for part in text:
            return __get_number(part)

    content = soup.select('#content > table >  tr > td.info_text > ul > li')
    for text in content:
        for part in text:
            if ("Number of students who do not have the right to seek:" in part) or \
                    ("Počet studentů, které nemáte právo vyhledat:" in part):
                return __get_number(part)
    return 0


def __get_number(text):
    return int(re.search(r'\d+', text).group())


def __build_url(is_employee, name=None, surname=None, login=None, uk_id=None):
    # dummy inicialization
    url = ''

    if is_employee:
        url = 'https://is.cuni.cz/studium/kdojekdo/index.php?do=hledani&koho=u&'
        url += 'fakulta=&'                  # change if we want to give access to all employees not just MFF
        url += 'prijmeni={}&'.format(surname)
        url += 'jmeno={}&'.format(name)
        url += 'inukat=0&exukat=0&neuci=0&pocet=50&vyhledej=Vyhledej'
    else:
        url = 'https://is.cuni.cz/studium/kdojekdo/index.php?do=hledani&koho=s&'
        url += 'fakulta=11320&'             # change if we want to give access to all students not just MFF
        url += 'prijmeni={}&'.format(surname)
        url += 'jmeno={}&'.format(name)
        url += 'login={}&'.format(login) if login is not None else 'login=&'
        url += 'sidos={}&'.format(uk_id) if uk_id is not None else 'sidos=&'
        url += 'sdruh=&svyjazyk=&r_zacatek=Z&pocet=50&vyhledej=Vyhledej'

    return url
