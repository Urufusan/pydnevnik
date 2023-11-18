# from pprint import pprint
from bs4 import BeautifulSoup
from lxml import etree
import pickle
import requests
import os
import subprocess


def span_text_fetch(t_xpath_element : etree._Element, t_s_default_string_if_not_found : str = "(Prazno)") -> str:
        #print((xpath_element))
        if len(t_xpath_element) == 1:
            return t_xpath_element[0].text
        else:
            return t_s_default_string_if_not_found

def get_class_from_note(t_xpath_element : etree._Element) -> str:
    return t_xpath_element.getparent().getparent()[0][0].text

def all_grades_data_fetcher(s_all_grade_html_content : str) -> tuple[int, list[dict]]:
    soup = BeautifulSoup(s_all_grade_html_content, "html.parser")
    #print(str(soup))
    dom : etree._Element = etree.HTML(str(soup))
    t_id_of_grade =                   int(''.join(filter(str.isnumeric,(dom.xpath("/html/body/div[1]/div[3]/div[2]/ul")[0].values()[0]))))
    x_xpath_dates_path =              dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row' or @class='flex-table row negative']/div[1]")
    x_xpath_notes_path =              dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row' or @class='flex-table row negative']/div[2]")
    x_xpath_note_grading_types_path = dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row' or @class='flex-table row negative']/div[3]")
    x_xpath_note_grades_path =        dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row' or @class='flex-table row negative']/div[4]")
    t_d_temp_locals = locals()
    #pprint(x_dates_path)
    l_compiled_list_of_note_dicts = []
    t_l_xpath_lenghts = []
    #print([[len(globals().get(xpathcomp)), xpathcomp] for xpathcomp in globals().keys() if xpathcomp.startswith("x_xpath_")])
    #pprint(locals())
    #print(len(x_xpath_dates_path), len(x_xpath_notes_path), len(x_xpath_note_grading_types_path), len(x_xpath_note_grades_path))
    for xpathcomp in t_d_temp_locals.keys():
        if xpathcomp.startswith("x_xpath_"):
            t_l_xpath_lenghts.append(len(t_d_temp_locals.get(xpathcomp)))
    #print("t_l", t_l_xpath_lenghts)
    
    t_i_max_iterations = min(t_l_xpath_lenghts)
    for t_i_entry in range(t_i_max_iterations):
        l_compiled_list_of_note_dicts.append({
            "date": span_text_fetch(x_xpath_dates_path[t_i_entry]),
            "note": span_text_fetch(x_xpath_notes_path[t_i_entry]),
            "graded_element" : span_text_fetch(x_xpath_note_grading_types_path[t_i_entry]),
            "grade" : span_text_fetch(x_xpath_note_grades_path[t_i_entry]),
            "class" : get_class_from_note(x_xpath_dates_path[t_i_entry])
        })
    
    return t_id_of_grade, l_compiled_list_of_note_dicts


def ppdb_read(s_filepath : str = ""):
    with open(s_filepath, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data

def ppdb_dump(given_data, s_filepath: str) -> None:
    with open(s_filepath, 'wb') as handle:
        pickle.dump(given_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_csrf(r_login_page_object: requests.Response) -> str:
    soup = BeautifulSoup(r_login_page_object.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})
    return csrf_token.attrs["value"]

def filepathprovider(wantedfilepath) -> str:
    return os.path.join(os.path.dirname(os.path.realpath('__file__')), wantedfilepath)

def login_creds_parser(debugprint : bool = False) -> list[str]:
    path_secrets_file = filepathprovider('.logininfo.secret')
    t_b_can_read_file = os.path.isfile(path_secrets_file) and os.access(path_secrets_file, os.R_OK)
    with open(path_secrets_file, "r" if t_b_can_read_file else "a+") as f:
        t_f_contents = f.readlines()
        t_f_contents = [content if not (content.startswith("#") or (not content.strip())) else "" for content in t_f_contents]
        t_s_filtered_file_content = ''.join(t_f_contents).strip()
        if debugprint: print(t_s_filtered_file_content, "\n", path_secrets_file)
        return t_s_filtered_file_content.splitlines()
    
def batprint(text : str, lang : str = "json"):
    # Your text content as a Python string
    #text = """This is some text that you want to display using 'bat'."""
    # sudo apt install batcat
    # Create a subprocess to run the 'bat -' command and pipe the text to it
    process = subprocess.Popen(['batcat', '-p', '--color', 'always', '--theme', 'gruvbox-dark', '--language', lang, '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Write the text to the 'bat' process
    stdout, stderr = process.communicate(input=text)

    # Get the return code
    return_code = process.returncode

    # Print the captured stdout and stderr
    #print("Captured STDOUT:")
    print(stdout)

    #print("\nCaptured STDERR:")
    #print(stderr)

    # Print the return code
    #print("\nReturn Code:", return_code)

def grades_exporter(t_l_grades: list[dict]) -> str:
    t_s_formatted_text = ""
    t_d_classes = {}
    
    for t_d_grade in t_l_grades:
        t_s_grade_class = t_d_grade["class"]
        
        if t_s_grade_class not in t_d_classes:
            t_d_classes[t_s_grade_class] = []

        # Append the grade details to the class
        t_d_classes[t_s_grade_class].append({
            "date": t_d_grade["date"],
            "note": t_d_grade["note"],
            "graded_element": t_d_grade["graded_element"],
            "grade": t_d_grade["grade"]
        })

    # Iterate through the classes and format the grades
    t_i_for_loop_counter = 0
    t_str_newline = "\n"
    for class_name, grades in t_d_classes.items():
        t_s_formatted_text += f"{t_str_newline if t_i_for_loop_counter else ''}## {class_name.upper()}\n---"

        for grade in grades:
            #t_s_formatted_text += "\n"
            # t_s_formatted_text += f"Datum: ``{grade['date']}``<br>\n"
            # t_s_formatted_text += f"Element vrednovanja: ``{grade['graded_element']}``<br>\n"
            # t_s_formatted_text += f"Bilješka:\n```\n{grade['note']}\n```\n"
            # t_s_formatted_text += f"### **Ocjena: ``{grade['grade']}``** <br>\n"
            # t_s_formatted_text += "<br>\n"
            t_s_formatted_text += f"""
Datum: ``{grade['date']}``<br>
Element vrednovanja: ``{grade['graded_element']}``<br>
Bilješka:
```
{grade['note']}
```
### **Ocjena: ``{grade['grade']}``** <br>
<br>""".replace("\n", "\n> ")
            t_s_formatted_text += "\n\n<br>\n"
            t_i_for_loop_counter += 1
    return t_s_formatted_text


if __name__ == "__main__":
    #moj_data = ppdb_read("./logindump.ppdb")
    #pprint(get_csrf(moj_data))
    print(login_creds_parser(debugprint=True))