import requests
from .dnevnikhelperlib import get_csrf, login_creds_parser, all_grades_data_fetcher, grades_exporter
#import pickle
#from pprint import pprint

def change_class_gradebook(t_grade_id : int|str, t_requests_session : requests.Session) -> None:
    t_requests_session.get(f"https://ocjene.skole.hr/class_action/{t_grade_id}/course")

def force_logout(t_d_headders : dict, t_d_old_cookies : dict):
    #carnet_login_data = login_creds_parser(True)
    print(requests.get("https://ocjene.skole.hr/logout",
                    headers=t_d_headders,
                    cookies=t_d_old_cookies
                    ))


def main(t_id_gradebook_class : int|str = 0, bl_print_markdown = False, BL_DEBUG_MODE : bool = False) -> list[dict]:
    t_id_gradebook_class = ''.join(filter(str.isnumeric, str(t_id_gradebook_class)))
    #force_logout({}, {}, {})
    carnet_login_data = login_creds_parser(debugprint=BL_DEBUG_MODE)
    s = requests.session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0", "DNT": "1", "Sec-GPC": "1"})
    glavniobj = s.get("https://ocjene.skole.hr/login",)

    if BL_DEBUG_MODE: print("kolacici:", s.cookies.get_dict())
    s_csrf_token = get_csrf(glavniobj)
    if BL_DEBUG_MODE: print("dobiven csrf:", s_csrf_token)

    returnan_post = s.post("https://ocjene.skole.hr/login",
    data={
        "username": carnet_login_data[0],
        "password": carnet_login_data[1],
        "csrf_token": s_csrf_token,
    })

    if t_id_gradebook_class: change_class_gradebook(t_id_gradebook_class, s)
    s_grade_html_export = s.get("https://ocjene.skole.hr/grade/all").text
    # if BL_DEBUG_MODE: print(s_grade_html_export)
    s.get("https://ocjene.skole.hr/logout") # Log out nicely to prevent getting blacklisted

    t_l_processed_data = all_grades_data_fetcher(s_grade_html_export)
    if BL_DEBUG_MODE: print("Class ID:", t_l_processed_data[0])
    if bl_print_markdown: print(grades_exporter(t_l_processed_data[1]))
    return t_l_processed_data

    # with open("./gradeallout.html", "w") as filectl:
    #     filectl.write(s_grade_html_export)
    # print("STOP GRADE ALL")
    #ppdb_dump(returnan_post, "./postdump.ppdb")
    #ppdb_dump(glavniobj, "./logindump.ppdb")

if __name__ == "__main__":
    main("https://ocjene.skole.hr/class_action/4905791380/course", bl_print_markdown=False, BL_DEBUG_MODE=True)

