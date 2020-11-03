import requests
from bs4 import BeautifulSoup
import re


def authenticate_via_sis(name, surname, login=None, ukco=None, is_employee=False):
    if is_employee:
        if name == None or surname == None:
            # expecting both name and surname
            print('Expected both name and surname\nName={}\nSurname={}'.format(name, surname))
            return False
        return authenticate_employee(name=name, surname=surname)
    else:
        if name == None or surname == None:
            # expecting both name and surname
            print('Expected both name and surname\nName = {}\nSurname = {}'.format(name, surname))
            return False
        if login == None and ukco == None:
            # expecting at least one of the following login, ukco
            print('Expected at least one of login, ukco\nLogin = {}\nUKCO = {}'.format(login, ukco))
            return False
        return authenticate_student(name=name, surname=surname, login=login, ukco=ukco)


def authenticate_student(name, surname, login=None, ukco=None):
    url = build_url(is_employee=False, name=name, surname=surname, login=login, ukco=ukco)
    page = requests.get(url)
    nubmer_of_results = get_number_of_students(page=page, name=name, surname=surname, login=login, ukco=ukco)

    if int(nubmer_of_results) >= 1:
        return True
    return False


def authenticate_employee(name, surname):
    url = build_url(is_employee=True, name=name, surname=surname)
    page = requests.get(url)
    nubmer_of_results = get_number_of_employees(page=page, name=name, surname=surname)

    if int(nubmer_of_results) >= 1:
        return True
    return False


def get_number_of_employees(page, name, surname):
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('#page_div > b:nth-child(3)')
    for text in content:
        for part in text:
            return get_number(part)
    return 0


def get_number_of_students(page, name, surname, login=None, ukco=None):
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select('#content > table >  tr > td.info_text > ul > li')
    for text in content:
        for part in text:
            if ("Number of students who do not have the right to seek:" in part) or \
                    ("Počet studentů, které nemáte právo vyhledat:" in part):
                return get_number(part)
    return 0


def get_number(text):
    return int(re.search(r'\d+', text).group())


def build_url(is_employee, name=None, surname=None, login=None, ukco=None):
    # dummy inicialization
    url = ''

    if (is_employee):
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
    pass
