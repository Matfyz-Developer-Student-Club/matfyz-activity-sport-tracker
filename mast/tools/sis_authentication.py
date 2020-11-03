from urllib import request




def authenticate_via_sis(name=None, surname=None, login=None, ukco=None, is_employee = False):
    if is_employee:
        authenticate_employee(name, surname)
    else:
        pass


def authenticate_student(login=None, ukco=None):
    base_url_student = 'https://is.cuni.cz/studium/kdojekdo/index.php?do=hledani&koho=s&fakulta=&prijmeni=&jmeno=&login={}&sidos={}&sdruh=&svyjazyk=&r_zacatek=Z&pocet=50&vyhledej=Vyhledej'
    url = base_url_student.format(login, ukco)


def authenticate_employee(name, surname):
    base_url_employee = 'https://is.cuni.cz/studium/kdojekdo/index.php?do=hledani&koho=u&fakulta=&prijmeni={}&jmeno={}&inukat=0&exukat=0&neuci=0&pocet=50&vyhledej=Vyhledej'
    ulr = base_url_employee.format(surname, name)


def find_in_html(name=None, surname=None, login=None, ukco=None):
    pass

def build_url(is_employee, name=None, surname=None, login=None, ukco=None):
    # dummy inicialization
    url = ''

    if (is_employee):
        if name == None or surname == None:
            # expecting both name and surname
            pass
        url = 'https://is.cuni.cz/studium/kdojekdo/index.php?do=hledani&koho=u&fakulta=&'
        url += 'prijmeni={}&'.format(surname)
        url += 'jmeno={}&'.format(name)
        url += 'inukat=0&exukat=0&neuci=0&pocet=50&vyhledej=Vyhledej'
    else:
        if name == None or surname == None:
            # expecting both name and surname
            pass
        if login == None and ukco == None:
            # expecting at least one of the following login, ukco
            pass
        url = 'https://is.cuni.cz/studium/kdojekdo/index.php?do=hledani&koho=s&fakulta=&'
        url += 'prijmeni={}&'.format(surname)
        url += 'jmeno={}&'.format(name)
        url += 'login={}&'.format(login) if login is not None else 'login=&'
        url += 'sidos={}&'.format(ukco) if ukco is not None else 'sidos=&'
        url += 'sdruh=&svyjazyk=&r_zacatek=Z&pocet=50&vyhledej=Vyhledej'

    return url
