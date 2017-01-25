from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def homepage():

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    return render_template("homepage.html",
                           students=students,
                           projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)
    return render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            rows=rows)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student"""

    return render_template("student_add.html")    


@app.route("/new-student", methods=["POST"])
def new_student():
    """Add student to database"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(fname, lname, github)

    return render_template("new_student.html", github=github)

@app.route("/project-add")
def project_add():
    """Add a project"""

    return render_template("project_add.html")    


@app.route("/new-project", methods=["POST"])
def new_project():
    """Add project to database"""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("new_project.html", title=title)

@app.route("/project")
def list_project():
    """Displays a list of information about projects"""

    title = request.args.get('title')
    title, description, max_grade = hackbright.get_project_by_title(title)

    grades= hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           grades=grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
