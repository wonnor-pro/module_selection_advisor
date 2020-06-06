import pandas as pd

class area():

    def __init__(self, ID, name, compulsory_courses, selective_courses, compulsory_numbers, preference_score):

        self.ID = ID
        self.name = name
        self.compulsory_courses = compulsory_courses
        self.selective_courses = selective_courses
        self.compulsory_numbers = compulsory_numbers
        self.courses_numbers = len(set(self.compulsory_courses).union(set(self.selective_courses)))
        self.preference = preference_score

    def __str__(self):
        output = f"{self.ID}. {self.name}, must finish {self.compulsory_numbers} courses {[self.preference]}"
        # output += f"\n   selective courses: {self.selective_courses}
        return output


class course():

    def __init__(self, ID, name, group, set, area, preference_score, pre = None):

        self.ID = ID       # "3F1"
        self.group = group # "F"
        self.name = name   # "Signal and Systems"
        self.set = set     # "IIAM4"
        self.area = area   # {}
        self.preference = preference_score
        self.pre = pre
        self.value = self.preference * 10
        self.term = self.set[3]

    def __str__(self):
        output = f"[{self.value}]{self.ID} in {self.term} Course: {self.name}"
        return output


def check_set_conflict(courseA, courseB):

    if courseA.set == courseB.set:
        return False
    else:
        return True

def preferenced(courseA):
    return courseA.preference

def value(courseA):
    return courseA.value

class student():

    def __init__(self, defo_courses, want_courses, okay_courses, preferred_areas):
        self.defo_courses = defo_courses
        self.want_courses = want_courses
        self.okay_courses = okay_courses
        self.preferred_areas = preferred_areas
        self.courses = {}
        self.courses_list = []
        self.areas_list = []

        self.M_candidate_courses = []
        self.L_candidate_courses = []
        self.M_courses = []
        self.L_courses = []

    def load_course_information(self, courses_filename):
        course_data = pd.read_excel(courses_filename)
        for index, row in course_data.iterrows():
            preference = 0
            if row["UNIT"] in self.defo_courses:
                preference = 3
            elif row["UNIT"] in self.want_courses:
                preference = 2
            elif row["UNIT"] in self.okay_courses:
                preference = 1
            self.courses[row["UNIT"]] = (
                course(row["UNIT"], row["TITTLE"], row["UNIT"][1], row["SET"], None, preference, None))
            self.courses_list.append(
                (course(row["UNIT"], row["TITTLE"], row["UNIT"][1], row["SET"], None, preference, None)))

    def load_area_information(self, total_area, area_fileame):
        area_data = []
        for i in range(1, 10):
            area_data.append(pd.read_excel(area_fileame, sheet_name=f"Sheet{i}"))

        for index, areas in enumerate(area_data):
            selective = []
            for number, row in areas.iterrows():
                selective.append(row["Number"])
            total_area[index][2] = selective

        for index, area_info in enumerate(total_area):
            preference = 0
            if index in self.preferred_areas:
                preference = 9 - self.preferred_areas.index(index)
            self.areas_list.append(area(index, area_info[0], area_info[1], area_info[2], area_info[3], preference))

    def check_set_conflict(self, courseA, courseB):

        if courseA.set == courseB.set:
            return False
        else:
            return True

    def initial_value(self, single_course):

        term_factor = []
        if len(self.M_courses) < 5:
            term_factor.append("M")
        if len(self.L_courses) < 5:
            term_factor.append("L")
        if single_course.term in term_factor:
            single_course.value += 5
        for area in self.areas_list:
            if area.preference == 0:
                continue
            if single_course.ID in area.compulsory_courses:
                single_course.value += area.preference * 5
            if single_course.ID in area.selective_courses:
                single_course.value += area.preference * 2

    def update_value(self, single_course):
        for i in self.M_courses:
            if not check_set_conflict(i, single_course):
                single_course.value -= 20

        for j in self.L_courses:
            if not check_set_conflict(j, single_course):
                single_course.value -= 20

    def classify_course(self):
        for single_course in self.courses_list:
            self.initial_value(single_course)
        self.courses_list.sort(key=value, reverse=True)

        for i in self.courses_list:
            if i.term == "M":
                self.M_candidate_courses.append(i)
            else:
                self.L_candidate_courses.append(i)

    def add_courses(self):
        if len(self.M_courses) < len(self.L_courses):
            if len(self.M_courses) < 5:
                self.M_courses.append(self.M_candidate_courses.pop(0))
        else:
            if len(self.L_courses) < 5:
                self.L_courses.append(self.L_candidate_courses.pop(0))

    def optimise(self):
        self.classify_course()
        while len(self.M_courses) < 5 or len(self.L_courses) < 5:
            self.add_courses()
            for m in self.M_candidate_courses:
                self.update_value(m)
            for l in self.L_candidate_courses:
                self.update_value(l)
            self.M_candidate_courses.sort(key=value, reverse=True)
            self.L_candidate_courses.sort(key=value, reverse=True)


def get_info():
    total_area = [["Mechanical engineering", [], [], 6, 0],
                  ["Energy, sustainability and the environment", [], [], 6, 0],
                  ["Aerospace and aerothermal engineering", ["3A1", "3A3"], [], 4, 0],
                  ["Civil, structural and environmental engineering", [], [], 6, 0],
                  ["Electrical and electronic engineering", [], [], 6, 2],
                  ["Information and computer engineering", [], [], 6, 3],
                  ["Electrical and information sciences", [], [], 8, 2],
                  ["Instrumentation and control", ["3F1", "3F2"], [], 5, 2],
                  ["Bioengineering", ["3G1", "3G2", "3G3", "3G4", "3G5"], [], 3, 2]]
    #
    # # Courses that you definitely gonna take
    # defo_courses = ["3F1", "3F2", "3F3", "3F4", "3F7", "3C5", "3C6",
    #                 "3M1"]  # ["3F1", "3F3", "3F7", "3F8", "3G3", "3G4", "3M1"]
    #
    # # Courses that you kinda want to take but not a strong desire
    # want_courses = ["3F8", "4M12", "3B2"]  # ["3B6", "3E1", "3E3"]
    #
    # # Courses that you find okay to take if necessary
    # okay_courses = ["3B1"]  # ["3G1", "3G5"] #
    #
    # preferred_areas = [5, 7, 6, 1]  # [5,6,8,7,4]

    IB_student = student([], [], [], [])
    IB_student.load_course_information("data/course_info.xls")
    IB_student.load_area_information(total_area, "data/area_info.xlsx")

    courses = []

    for i in IB_student.courses_list:
        courses.append([i.ID, i.name, i.term])
    return courses, total_area

def suggestion(defo_courses, want_courses, okay_courses, preferred_areas):

    total_area = [["Mechanical engineering", [], [], 6, 0],
                  ["Energy, sustainability and the environment", [], [], 6, 0],
                  ["Aerospace and aerothermal engineering", ["3A1", "3A3"], [], 4, 0],
                  ["Civil, structural and environmental engineering", [], [], 6, 0],
                  ["Electrical and electronic engineering", [], [], 6, 2],
                  ["Information and computer engineering", [], [], 6, 3],
                  ["Electrical and information sciences", [], [], 8, 2],
                  ["Instrumentation and control", ["3F1", "3F2"], [], 5, 2],
                  ["Bioengineering", ["3G1", "3G2", "3G3", "3G4", "3G5"], [], 3, 2]]

    IB_student = student(defo_courses, want_courses, okay_courses, preferred_areas)
    IB_student.load_course_information("data/course_info.xls")
    IB_student.load_area_information(total_area, "data/area_info.xlsx")
    IB_student.optimise()

    output = []
    for i in IB_student.M_courses:
        output.append([i.ID, i.name, i.term, i.set])
    for i in IB_student.L_courses:
        output.append([i.ID, i.name, i.term, i.set])

    return output


if __name__ == "__main__":
    suggestion()