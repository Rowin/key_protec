import requests
import re
from bs4 import BeautifulSoup
from models import User, Habilitations
import pony.orm
from secrets import EPROTEC_ID, EPROTEC_PWD


def is_connected(eprotec_session):
    r = eprotec_session.get(url=f"{url_base}/index_d.php")
    if b"lost_session" in r.content:
        return False
    return True


def connect(login_dict, eprotec_session):
    if not is_connected(eprotec_session):
        r = eprotec_session.post(url=f"{url_base}/login.php", data=login_dict)
        if b"index.php" not in r.content:
            raise ConnectionError("Connection failed...")


def get_eprotec_page(page_name, eprotec_session, login_dict, params, method="get"):
    connect(login_dict, eprotec_session)
    url = f"{url_base}/{page_name}.php"
    if method == "get":
        r = eprotec_session.get(url=url, params=params)
    elif method == "post":
        r = eprotec_session.post(url=url, data=params)
    else:
        raise NotImplementedError(f"The method {method} is not supported yet.")

    return r


def get_hab_from_str(hab_str):
    if (hab := Habilitations.get(name=hab_str)) is None:
        hab = Habilitations(name=hab_str)
    return hab


def get_str_from_td(td):
    return td.text.replace("\xa0", "")


@pony.orm.db_session()
def refresh_users():
    params = {
        "filter": 37,  # Section ID
        "subsections": 1,  # Include subsections
        "exp": "groupes",  # groupes|roles
        "affichage": "ecran",  # xls|ecran
        "show": True,
    }

    r = get_eprotec_page("export", eprotec_session, login_dict, params)
    soup = BeautifulSoup(r.content)

    for tr in soup.find_all("tr")[1:]:
        tds = tr.find_all("td")
        user = {
            "id": re.search(r"pompier=(\d+)", tds[1].a.attrs["href"]).group(1),
            "firstname": get_str_from_td(tds[2]),
            "lastname": get_str_from_td(tds[1]),
        }
        hab1 = get_hab_from_str(get_str_from_td(tds[4]))
        hab2 = get_hab_from_str(get_str_from_td(tds[6]))
        user["habilitations"] = (hab1, hab2)

        if User.exists(id=user["id"]):
            User[user["id"]].set(**user)
        else:
            User(**user)
    pony.orm.commit()


if __name__ == "__main__":
    url_base = "https://test.franceprotectioncivile.org"
    eprotec_session = requests.Session()

    login_dict = {"id": EPROTEC_ID, "pwd": EPROTEC_PWD}
    refresh_users()
