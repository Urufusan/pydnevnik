from pprint import pprint
#from pydnevnik.dnevnikhelperlib import grades_exporter
from pydnevnik import helperlib, sesfuncs
from statistics import mean
if __name__ == "__main__":
    # import pydnevnik
    # pydnevnik.mainclass
    # pydnevnik.helper
    # pprint(pydnevnik.main())
    # print(grades_exporter(pydnevnik.main()[1]))
    ses = sesfuncs.create_edn_session(BL_DEBUG_MODE=False)
    # pprint(sesfuncs.return_all_courses_metadata(ses))
    # pprint(sesfuncs.get_all_grades_from_course(ses))
    avgtest = sesfuncs.get_all_grades_from_course(ses)
    pprint(avgtest)
    # pprint(avgtest)
    pprint(l_int_all_avgs := helperlib.calculate_avg_grade_from_all_grades(avgtest))
    print("Ukupna:", mean([helperlib.round_half_up(floateee) for floateee in l_int_all_avgs.values()]))
