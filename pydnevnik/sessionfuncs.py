import requests
from .dnevnikhelperlib import all_grades_data_fetcher, change_current_course_from_coursebook, course_selection_parser, login_creds_parser
from bs4 import BeautifulSoup
import atexit

def get_csrf(r_login_page_object: requests.Response) -> str:
    soup = BeautifulSoup(r_login_page_object.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})
    return csrf_token.attrs["value"]

def edn_logout(t_edn_session : requests.Session):
    print("Logging out...")
    t_req_obj = t_edn_session.get("https://ocjene.skole.hr/logout")
    t_req_obj.raise_for_status()
    atexit.unregister(edn_logout)
    return t_edn_session

def create_edn_session(t_l_login_data : list[str, str] = ["email", "password"], BL_DEBUG_MODE = False):
    """Create a Requests Session with E-Dnevnik creds
    """
    carnet_login_data = login_creds_parser(debugprint=BL_DEBUG_MODE) if t_l_login_data == ["email", "password"] else t_l_login_data
    s = requests.session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0", "DNT": "1", "Sec-GPC": "1"})
    glavniobj = s.get("https://ocjene.skole.hr/login")

    if BL_DEBUG_MODE: print("kolacici:", s.cookies.get_dict())
    s_csrf_token = get_csrf(glavniobj)
    if BL_DEBUG_MODE: print("dobiven csrf:", s_csrf_token)

    returnan_post = s.post("https://ocjene.skole.hr/login",
    data={
        "username": carnet_login_data[0],
        "password": carnet_login_data[1],
        "csrf_token": s_csrf_token,
    })
    atexit.register(edn_logout, t_edn_session=s)
    return s


def return_all_courses_metadata(req_session : requests.Session):
    """Returns all courses and all metadata inside earch course
    """
    s_html_coursesel_page = req_session.get("https://ocjene.skole.hr/class").text
    return course_selection_parser(s_html_coursesel_page)

def get_all_grades_from_course(t_session_obj : requests.Session, t_course_id : int|str = 0):
    t_course_id = ''.join(filter(str.isnumeric, str(t_course_id)))
    if t_course_id:
        change_current_course_from_coursebook(t_course_id, t_session_obj)
    t_s_grade_html_export = t_session_obj.get("https://ocjene.skole.hr/grade/all").text
    return all_grades_data_fetcher(t_s_grade_html_export)[1]