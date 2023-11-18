from pprint import pprint

from pydnevnik.dnevnikhelperlib import grades_exporter
if __name__ == "__main__":
    import pydnevnik
    # pydnevnik.mainclass
    # pydnevnik.helper
    # pprint(pydnevnik.main())
    print(grades_exporter(pydnevnik.main()[1]))