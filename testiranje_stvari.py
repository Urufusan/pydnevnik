from pprint import pprint
from lxml import etree
from bs4 import BeautifulSoup
#import requests

def span_text_fetch(t_xpath_element : etree._Element) -> str:
        #print((xpath_element))
        if len(t_xpath_element) == 1:
            return t_xpath_element[0].text
        else:
            return ""
            #print(NameError(f"A span doesn't exist within {t_xpath_element.tag}"))

def get_class_from_note(t_xpath_element : etree._Element) -> str:
    return t_xpath_element.getparent().getparent()[0][0].text

if __name__ == "__main__":
    # za_proveru : requests.Response = ppdb_read("./postdump.ppdb")
    # print(za_proveru.text)
    with open("gradeallout.html", "r") as filectl:
        hateemel_sors = filectl.read()

    soup = BeautifulSoup(hateemel_sors, "html.parser")
    #print(str(soup))
    dom : etree._Element = etree.HTML(str(soup))
    t_id_of_grade =             dom.xpath("/html/body/div[1]/div[3]/div[2]/ul")
    x_dates_path =              dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row']/div[1]")
    x_notes_path =              dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row']/div[2]")
    x_note_grading_types_path = dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row']/div[3]")
    x_note_grades_path =        dom.xpath("/html/body/div[1]/div[4]/div[2]/div/div[@class='flex-table row']/div[4]")
    #pprint(x_dates_path)
    print(int(''.join(filter(str.isnumeric,(t_id_of_grade[0].values()[0])))))
    exit()
    l_compiled_list_of_note_dicts = []
    print([[len(globals().get(xpathcomp)), xpathcomp] for xpathcomp in globals().keys() if xpathcomp.startswith("x_")])
    
    for t_i_entry in range(min([len(globals().get(xpathcomp))  for xpathcomp in globals().keys() if xpathcomp.startswith("x_")])):
        #print(span_text_fetch(x_dates_path[t_i_entry]))
        l_compiled_list_of_note_dicts.append({
            "date": span_text_fetch(x_dates_path[t_i_entry]),
            "note": span_text_fetch(x_notes_path[t_i_entry]),
            "graded_element" : span_text_fetch(x_note_grading_types_path[t_i_entry]),
            "grade" : span_text_fetch(x_note_grades_path[t_i_entry]),
            "class" : get_class_from_note(x_dates_path[t_i_entry])
        })
        #break
    pprint(l_compiled_list_of_note_dicts)
    #globals().item
    #print(len(x_dates_path), len(x_notes_path), len(x_note_grading_types_path), len(X_note_grades_path))
    # print((notes_path[0].getchildren()[0].tag))
    # print(([cachetext.text for cachetext in notes_path])) #, width=300)
    # print(len(notes_path))
    #print(dom.xpath("/html/body/div[1]/div[4]/div[2]/div[9]/div[4]/div[2]/span")[0].text)
    
    
# /html/body/div[1]/div[4]/div[2]/div/div[3]/div[2]/span
# /html/body/div[1]/div[4]/div[2]/div/div/div[2]/span

# /html/body/div[1]/div[4]/div[2]/div[9]/div[4]/div[2]/span