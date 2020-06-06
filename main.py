from flask import Flask, render_template, request
from util.backend import get_info, suggestion

app = Flask(__name__)

courses_display, area_display = get_info()
courses, areas = get_info()
defo_courses = []
want_courses = []
okay_courses = []
preferred_areas = []
data = []

@app.route('/')
def index():
    # Get solution
    global data, area_display
    if defo_courses and want_courses and okay_courses and preferred_areas:
        data = suggestion(defo_courses, want_courses, okay_courses, preferred_areas)
    return render_template("index.html", DEFO = defo_courses, WANT = want_courses, OKAY = okay_courses, PREF = preferred_areas, area = area_display, data = data)

@app.route('/reset')
def reset():
    # Get solution
    global data, area_display, defo_courses, want_courses, okay_courses, preferred_areas
    global courses, areas
    courses, areas = get_info()
    defo_courses = []
    want_courses = []
    okay_courses = []
    preferred_areas = []
    data = []
    if defo_courses and want_courses and okay_courses and preferred_areas:
        data = suggestion(defo_courses, want_courses, okay_courses, preferred_areas)
    return render_template("index.html", DEFO = defo_courses, WANT = want_courses, OKAY = okay_courses, PREF = preferred_areas, area = area_display, data = data)


@app.route('/info')
def info():
    # Get solution
    return render_template("info.html", courses = courses_display)


@app.route('/results')
def suggestion_web():
    # Get solution
    data = suggestion(defo_courses, want_courses, okay_courses)
    return render_template("results.html", data = data)

@app.route('/form/<type>')
def form(type):
    # Get solution
    return render_template("form.html", courses = courses, type = type)

@app.route('/get_form/<type>', methods=["POST"])
def get_form(type):
    print(request.form)
    courses_list = request.form.getlist("courseID")
    print(courses_list)
    index_list = []
    for index, i in enumerate(courses):
        if i[0] in courses_list:
            index_list.append(index)
    index_list.reverse()
    for i in index_list:
        courses.pop(i)
    if type == "DEFO":
        global defo_courses
        defo_courses = courses_list
    elif type == "WANT":
        global want_courses
        want_courses = courses_list
    elif type == "OKAY":
        global okay_courses
        okay_courses = courses_list

    return render_template("successful.html")

@app.route('/area')
def area():
    # Get solution
    return render_template("area.html", area = area_display)

@app.route('/get_area', methods=["POST"])
def get_area():
    print(request.form)
    global preferred_areas
    for i in range(1,5):
        preferred_areas.append(int(request.form.get(f"{i}")))
    print(preferred_areas)
    return render_template("successful.html")


if __name__ == '__main__':
    app.run()
