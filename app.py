from flask import Flask, render_template, request, redirect, url_for, flash
import database as db

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Инициализация базы данных
db.init_db()

# ======= Главная =======
@app.route("/")
def index():
    return render_template("index.html")

# ======= Cards =======
@app.route("/cards")
def cards():
    cards = db.get_all_cards()
    return render_template("cards.html", cards=cards)

@app.route("/cards/add", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        db.create_card(
            name=request.form["name"],
            price=request.form["price"],
            lessons_count=request.form["lessons_count"],
            duration=request.form["duration"],
            color=request.form["color"],
            status=request.form["status"]
        )
        flash("Карточка создана!", "success")
        return redirect(url_for("cards"))
    return render_template("add_card.html")

@app.route("/cards/edit/<int:card_id>", methods=["GET", "POST"])
def edit_card(card_id):
    card = db.get_card_by_id(card_id)
    if request.method == "POST":
        db.update_card(
            card_id,
            name=request.form["name"],
            price=request.form["price"],
            lessons_count=request.form["lessons_count"],
            duration=request.form["duration"],
            color=request.form["color"],
            status=request.form["status"]
        )
        flash("Карточка обновлена!", "success")
        return redirect(url_for("cards"))
    return render_template("edit_card.html", card=card)

@app.route("/cards/delete/<int:card_id>")
def delete_card(card_id):
    db.delete_card(card_id)
    flash("Карточка удалена!", "success")
    return redirect(url_for("cards"))

# ======= Students =======
@app.route("/students")
def students():
    students = db.get_all_students()
    return render_template("students.html", students=students)

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        db.add_student(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            middle_name=request.form["middle_name"],
            contacts=request.form["contacts"],
            birthday=request.form["birthday"],
            lessons_count=request.form["lessons_count"],
            additional_info=request.form["additional_info"]
        )
        flash("Ученик добавлен!", "success")
        return redirect(url_for("students"))
    return render_template("add_student.html")

@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    student = db.get_student_by_id(student_id)
    if request.method == "POST":
        db.update_student(
            student_id,
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            middle_name=request.form["middle_name"],
            contacts=request.form["contacts"],
            birthday=request.form["birthday"],
            lessons_count=request.form["lessons_count"],
            additional_info=request.form["additional_info"]
        )
        flash("Данные ученика обновлены!", "success")
        return redirect(url_for("students"))
    return render_template("edit_student.html", student=student)

@app.route("/students/delete/<int:student_id>")
def delete_student(student_id):
    db.delete_student(student_id)
    flash("Ученик удален!", "success")
    return redirect(url_for("students"))

# ======= Coaches =======
@app.route("/coaches")
def coaches():
    coaches = db.get_all_coaches()
    return render_template("coaches.html", coaches=coaches)

@app.route("/coaches/add", methods=["GET", "POST"])
def add_coach():
    if request.method == "POST":
        db.add_coach(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            middle_name=request.form["middle_name"],
            contacts=request.form["contacts"],
            birthday=request.form["birthday"],
            lessons_count=request.form["lessons_count"],
            lessons_paid=request.form["lessons_paid"],
            student_payment=request.form["student_payment"],
            additional_info=request.form["additional_info"]
        )
        flash("Тренер добавлен!", "success")
        return redirect(url_for("coaches"))
    return render_template("add_coach.html")

@app.route("/coaches/edit/<int:coach_id>", methods=["GET", "POST"])
def edit_coach(coach_id):
    coach = db.get_coach_by_id(coach_id)
    if request.method == "POST":
        db.update_coach(
            coach_id,
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            middle_name=request.form["middle_name"],
            contacts=request.form["contacts"],
            birthday=request.form["birthday"],
            lessons_count=request.form["lessons_count"],
            lessons_paid=request.form["lessons_paid"],
            student_payment=request.form["student_payment"],
            additional_info=request.form["additional_info"]
        )
        flash("Данные тренера обновлены!", "success")
        return redirect(url_for("coaches"))
    return render_template("edit_coach.html", coach=coach)

@app.route("/coaches/delete/<int:coach_id>")
def delete_coach(coach_id):
    db.delete_coach(coach_id)
    flash("Тренер удален!", "success")
    return redirect(url_for("coaches"))

# ===== Lessons =====
@app.route("/lessons")
def lessons():
    lesson_templates = db.get_all_lesson_templates()
    lessons = db.get_all_lessons()
    students = db.get_all_students()
    coaches = db.get_all_coaches()
    return render_template(
        "lessons.html",
        lessons=lessons,
        students=students,
        coaches=coaches,
        lesson_templates=lesson_templates
    )

@app.route("/lessons/add", methods=["GET", "POST"])
def add_lesson():
    if request.method == "POST":
        db.add_lesson(
            request.form["date"],
            request.form["coach_id"],
            request.form.getlist("student_ids"),
            request.form["status"]
        )
        return redirect(url_for("lessons"))

    return render_template(
        "add_lesson.html",
        students=db.get_all_students(),
        coaches=db.get_all_coaches()
    )

@app.route("/lessons/edit/<int:lesson_id>", methods=["GET", "POST"])
def edit_lesson(lesson_id):
    lesson = db.get_lesson_by_id(lesson_id)
    if request.method == "POST":
        db.update_lesson(
            lesson_id,
            request.form["date"],
            request.form["coach_id"],
            request.form.getlist("student_ids"),
            request.form["status"]
        )
        return redirect(url_for("lessons"))

    return render_template(
        "edit_lesson.html",
        lesson=lesson,
        students=db.get_all_students(),
        coaches=db.get_all_coaches()
    )

@app.route("/lessons/delete/<int:lesson_id>")
def delete_lesson(lesson_id):
    db.delete_lesson(lesson_id)
    return redirect(url_for("lessons"))

@app.route("/lessons/<int:lesson_id>/done", methods=["GET", "POST"])
def lesson_done(lesson_id):
    db.decrement_lessons_from_students(lesson_id)
    db.increment_lessons_to_couch(lesson_id)
    return redirect(request.referrer or url_for("lessons"))

@app.route("/lesson_template/add/<int:lesson_template_id>")
def add_lesson_from_template_route(lesson_template_id):
    db.add_lesson_from_template(lesson_template_id)
    return redirect(url_for("lessons"))
#================================lesson template=============================

@app.route("/lesson_templates")
def lesson_templates():
    lesson_templates = db.get_all_lesson_templates()
    students = db.get_all_students()
    coaches = db.get_all_coaches()
    return render_template(
        "lesson_templates.html",
        lesson_templates=lesson_templates,
        students=students,
        coaches=coaches
    )

@app.route("/lesson_templates/add", methods=["GET", "POST"])
def add_lesson_template():
    if request.method == "POST":
        db.add_lesson_template(
            request.form["template_name"],
            request.form["coach_id"],
            request.form.getlist("student_ids"),
        )
        return redirect(url_for("lesson_templates"))

    return render_template(
        "add_lesson_template.html",
        students=db.get_all_students(),
        coaches=db.get_all_coaches()
    )

@app.route("/lesson_templates/edit/<int:lesson_template_id>", methods=["GET", "POST"])
def edit_lesson_template(lesson_template_id):
    lesson_template = db.get_lesson_template_by_id(lesson_template_id)
    if request.method == "POST":
        db.update_lesson_template(
            lesson_template_id,
            request.form["template_name"],
            request.form["coach_id"],
            request.form.getlist("student_ids"),
        )
        return redirect(url_for("lesson_templates"))

    return render_template(
        "edit_lesson_template.html",
        lesson_template=lesson_template,
        students=db.get_all_students(),
        coaches=db.get_all_coaches()
    )

@app.route("/lesson_templates/delete/<int:lesson_template_id>")
def delete_lesson_template(lesson_template_id):
    db.delete_lesson_template(lesson_template_id)
    return redirect(url_for("lesson_templates"))

if __name__ == "__main__":
    app.run(debug=True)
