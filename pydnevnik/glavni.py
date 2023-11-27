import requests
from .dnevnikhelperlib import all_grades_data_fetcher, textual_grades_exporter, change_current_course_from_coursebook
from .sessionfuncs import create_edn_session, edn_logout
#import pickle
#from pprint import pprint



def force_logout(t_d_headders : dict, t_d_old_cookies : dict):
    #carnet_login_data = login_creds_parser(True)
    print(requests.get("https://ocjene.skole.hr/logout",
                    headers=t_d_headders,
                    cookies=t_d_old_cookies
                    ))


def main(t_id_gradebook_class : int|str = 0, bl_print_markdown : bool = False, t_l_login_data : list[str, str] = ["email", "password"], BL_DEBUG_MODE : bool = False) -> list[dict]:
    t_id_gradebook_class = ''.join(filter(str.isnumeric, str(t_id_gradebook_class)))
    #force_logout({}, {}, {})
    s = create_edn_session(t_l_login_data, BL_DEBUG_MODE)

    if t_id_gradebook_class: change_current_course_from_coursebook(t_id_gradebook_class, s)
    s_grade_html_export = s.get("https://ocjene.skole.hr/grade/all").text
    # if BL_DEBUG_MODE: print(s_grade_html_export)
    # s.get("https://ocjene.skole.hr/logout") # Log out nicely to prevent getting blacklisted
    edn_logout(s)

    t_l_processed_data = all_grades_data_fetcher(s_grade_html_export)
    if BL_DEBUG_MODE: print("Class ID:", t_l_processed_data[0])
    if bl_print_markdown: print(textual_grades_exporter(t_l_processed_data[1]))
    return t_l_processed_data



    # with open("./gradeallout.html", "w") as filectl:
    #     filectl.write(s_grade_html_export)
    # print("STOP GRADE ALL")
    #ppdb_dump(returnan_post, "./postdump.ppdb")
    #ppdb_dump(glavniobj, "./logindump.ppdb")

if __name__ == "__main__":
    main("https://ocjene.skole.hr/class_action/4905791380/course", bl_print_markdown=False, BL_DEBUG_MODE=True)

