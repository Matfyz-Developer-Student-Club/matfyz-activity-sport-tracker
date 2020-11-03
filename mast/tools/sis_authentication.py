import requests
from bs4 import BeautifulSoup
import re


def authenticate_via_sis(name, surname, login=None, ukco=None, is_employee=False):
    """
    Simple authentication via sis.
    Employee must submit: name, surname
    Student must submit: name, surname, (login or ukco)
    :param name: name of the person - obligatory:
    :param surname: surname of the person - obligatory:
    :param login: login for students
    :param ukco: UKCO for students
    :param is_employee: bool if the person is employee
    :return: True if such person exists, False otherwise
    """
    if is_employee:
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
        if not login and not ukco:
            # expecting at least one of the following login, ukco
            print('Expected at least one of login, ukco\nLogin = {}\nUKCO = {}'.format(login, ukco))
            return False
        return __authenticate_student(name=name, surname=surname, login=login, ukco=ukco)


def __authenticate_student(name, surname, login=None, ukco=None):
    """
    Checks if such student exits when asked at is.cuni.cz/studium/kdojekdo
    :param name: name
    :param surname: surname
    :param login: login
    :param ukco: UKČO
    :return: True if such person exists, False otherwise
    """
    url = __build_url(is_employee=False, name=name, surname=surname, login=login, ukco=ukco)
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
    content = soup.select('#content > table >  tr > td.info_text > ul > li')
    for text in content:
        for part in text:
            if ("Number of students who do not have the right to seek:" in part) or \
                    ("Počet studentů, které nemáte právo vyhledat:" in part):
                return __get_number(part)
    return 0


def __get_number(text):
    return int(re.search(r'\d+', text).group())


def __build_url(is_employee, name=None, surname=None, login=None, ukco=None):
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
        url += 'sidos={}&'.format(ukco) if ukco is not None else 'sidos=&'
        url += 'sdruh=&svyjazyk=&r_zacatek=Z&pocet=50&vyhledej=Vyhledej'

    return url

if __name__ == '__main__':
    name = 'Jan'
    surname = 'Kleprlik'
    print("FALSE = " + str(authenticate_via_sis(name=name, surname=surname, is_employee=True)))    # False
    print()
    print("FALSE = " + str(authenticate_via_sis(name=name, surname=surname, is_employee=False)))  # ERROR
    print()
    print("FALSE = " + str(authenticate_via_sis(name=name, surname=surname, login='kleprlij', is_employee=True)))  # False
    print()
    print("TRUE = " + str(authenticate_via_sis(name=name, surname=surname, login='kleprlij', is_employee=False)))  # True
    print()


    name = 'Pavel'
    surname = 'Ježek'
    print("TRUE = " + str(authenticate_via_sis(name=name, surname=surname, is_employee=True)))    # True
    print()
    print("FALSE = " + str(authenticate_via_sis(name=name, surname=surname, is_employee=False)))   # ERROR
