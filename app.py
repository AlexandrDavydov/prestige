from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import database as db

app = Flask(__name__)
app.secret_key = "super-secret-key-l#aksjd@lakjsd"
USERNAME = "admin"
PASSWORD = "g@z"

db.init_db()
# ===============login=====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()  # очищаем сессию
    return redirect(url_for("login"))

def login_required(fn):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

# ======= Главная =======
@app.route("/index")
@login_required
def index():
    return render_template("index.html")

# ======= Cards =======
@app.route("/cards")
@login_required
def cards():
    cards = db.get_all_cards()
    return render_template("cards.html", cards=cards)

@app.route("/cards/buy/<int:student_id>", methods=["GET", "POST"])
@login_required
def buy_cards(student_id):
    cards = db.get_all_cards()
    return render_template("buy_cards.html", cards=cards, student_id=student_id)

@app.route("/cards/purchased/", methods=["GET", "POST"])
@login_required
def purchased_cards():
    if request.method == "POST":
        db.add_card_lessons_to_student(card_id=request.form["card_id"], student_id=request.form["student_id"])
        db.store_purchased_card(card_id=request.form["card_id"], student_id=request.form["student_id"])
    return redirect(url_for("students"))

@app.route("/cards/add", methods=["GET", "POST"])
@login_required
def add_card():
    if request.method == "POST":
        db.create_card(request.form["name"], request.form["price"], request.form["lessons_count"], request.form["duration"],
            request.form["color"],request.form["status"]
        )
        flash("Карточка с названием<b> "+request.form["name"]+" </b>создана!", "success")
        return redirect(url_for("cards"))
    return render_template("add_card.html")

@app.route("/cards/edit/<int:card_id>", methods=["GET", "POST"])
@login_required
def edit_card(card_id):
    card = db.get_card_by_id(card_id)
    if request.method == "POST":
        db.update_card(card_id, request.form["name"], request.form["price"], request.form["lessons_count"],
            request.form["duration"], request.form["color"], request.form["status"]
        )
        flash("Карточка с названием<b> "+request.form["name"]+" </b>обновлена!", "success")
        return redirect(url_for("cards"))
    return render_template("edit_card.html", card=card)

@app.route("/cards/delete/<int:card_id>")
@login_required
def delete_card(card_id):
    db.delete_card(card_id)
    flash("Карточка удалена!", "success")
    return redirect(url_for("cards"))

# ======= Students =======
@app.route("/students")
@login_required
def students():
    students = db.get_all_students()
    return render_template("students.html", students=students)

@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        middle_name = request.form.get("middle_name", "").strip()
        contacts = request.form.get("contacts", "").strip()
        birthday = request.form.get("birthday", "")
        lessons_count = request.form.get("lessons_count", 0)
        additional_info = request.form.get("additional_info", "").strip()

        # Проверяем, есть ли ученик с таким именем и фамилией
        if not db.is_student_exists(first_name, last_name):
            db.add_student(first_name, last_name, middle_name, contacts, birthday, int(lessons_count or 0), additional_info)
            flash(f"Ученик <b>{last_name} {first_name}</b> добавлен!", "success")
            return redirect(url_for("students"))
        else:
            flash(f"Ученик <b>{last_name} {first_name}</b> уже существует!", "error")

    # GET-запрос или если ученик уже существует
    return render_template("add_student.html")

@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = db.get_student_by_id(student_id)
    if request.method == "POST":
        db.update_student(student_id, request.form["first_name"], request.form["last_name"], request.form["middle_name"],
            request.form["contacts"], request.form["birthday"], request.form["lessons_count"], request.form["additional_info"])
        flash("Данные ученика <b>"+request.form["last_name"]+" "+request.form["first_name"]+"</b> обновлены!", "success")
        return redirect(url_for("students"))
    return render_template("edit_student.html", student=student)


@app.route("/students/delete/<int:student_id>")
@login_required
def delete_student(student_id):
    db.delete_student(student_id)
    flash("Ученик удален!", "success")
    return redirect(url_for("students"))


# ======= Coaches =======
@app.route("/coaches")
@login_required
def coaches():
    coaches_raw = db.get_all_coaches()
    coaches = []
    for c in coaches_raw:
        coach = dict(c)  # ← ключевой момент
        coach["lessons_paid"] = int(coach["lessons_paid"] or 0)
        coach["student_payment"] = int(coach["student_payment"] or 0)
        coach["lessons_count"] = int(coach["lessons_count"] or 0)
        coaches.append(coach)
    return render_template("coaches.html", coaches=coaches)


@app.route("/coaches/add", methods=["GET", "POST"])
@login_required
def add_coach():
    if request.method == "POST":
        db.add_coach(request.form["first_name"], request.form["last_name"], request.form["middle_name"], request.form["contacts"],
            request.form["birthday"], request.form["lessons_count"], request.form["lessons_paid"], request.form["student_payment"],
            request.form["additional_info"])
        flash("Тренер " + request.form["last_name"] + " " + request.form["first_name"] + " добавлен!", "success")
        return redirect(url_for("coaches"))
    return render_template("add_coach.html")


@app.route("/coaches/edit/<int:coach_id>", methods=["GET", "POST"])
@login_required
def edit_coach(coach_id):
    coach = db.get_coach_by_id(coach_id)
    if request.method == "POST":
        db.update_coach(coach_id, request.form["first_name"], request.form["last_name"], request.form["middle_name"],
            request.form["contacts"], request.form["birthday"], request.form["lessons_count"], request.form["lessons_paid"],
            request.form["student_payment"], request.form["additional_info"])
        flash("Данные тренера <b>" + request.form["last_name"] + " " + request.form["first_name"] + "</b> обновлены!",
              "success")
        return redirect(url_for("coaches"))
    return render_template("edit_coach.html", coach=coach)


@app.route("/coaches/delete/<int:coach_id>")
@login_required
def delete_coach(coach_id):
    db.delete_coach(coach_id)
    flash("Тренер <b>" + request.form["last_name"] + " " + request.form["first_name"] + "</b> удален!", "success")
    return redirect(url_for("coaches"))


@app.route("/coaches/money/<int:coach_id>")
@login_required
def give_money_to_coach(coach_id):
    coach = db.get_coach_by_id(coach_id)
    db.money_to_coach(coach_id)
    flash("Расчет с тренером <b>" + coach["last_name"] + " " + coach["first_name"] + "</b> произведен!", "success")
    return redirect(url_for("coaches"))


# ===== Lessons =====
@app.route("/lessons")
@login_required
def lessons():
    status_filter = request.args.get("status_filter")

    if status_filter is None:
        status_filter = "Запланировано"

    if status_filter == "Все":
        lessons = db.get_all_lessons()
    else:
        lessons = db.get_lessons_filtered_by_status(status_filter)

    students = db.get_all_students()
    coaches = db.get_all_coaches()
    lesson_templates = db.get_all_lesson_templates()

    return render_template("lessons.html", lessons=lessons, students=students, coaches=coaches,
        lesson_templates=lesson_templates, status_filter=status_filter)


@app.route("/lessons/add", methods=["GET", "POST"])
@login_required
def add_lesson():
    if request.method == "POST":
        db.add_lesson(request.form["date"], request.form["coach_id"], request.form.getlist("student_ids"), request.form["status"])
        return redirect(url_for("lessons"))
    return render_template("add_lesson.html", students=db.get_all_students(), coaches=db.get_all_coaches())

@app.route("/lessons/edit/<int:lesson_id>", methods=["GET", "POST"])
@login_required
def edit_lesson(lesson_id):
    lesson = db.get_lesson_by_id(lesson_id)
    if request.method == "POST":
        db.update_lesson(lesson_id, request.form["date"], request.form["coach_id"], request.form.getlist("student_ids"),
            request.form["status"])
        return redirect(url_for("lessons"))

    return render_template("edit_lesson.html", lesson=lesson, students=db.get_all_students(),
        coaches=db.get_all_coaches())

@app.route("/lessons/delete/<int:lesson_id>")
@login_required
def delete_lesson(lesson_id):
    db.delete_lesson(lesson_id)
    return redirect(url_for("lessons"))

@app.route("/lessons/<int:lesson_id>/done", methods=["GET", "POST"])
@login_required
def lesson_done(lesson_id):
    db.decrement_lessons_from_students(lesson_id)
    db.increment_lessons_to_couch(lesson_id)
    db.close_lessons(lesson_id)
    return redirect(request.referrer or url_for("lessons"))


# ================================lesson template=============================
@app.route("/lesson_template/add/<int:lesson_template_id>")
@login_required
def add_lesson_from_template_route(lesson_template_id):
    db.add_lesson_from_template(lesson_template_id)
    return redirect(url_for("lessons"))


@app.route("/lesson_templates")
@login_required
def lesson_templates():
    lesson_templates = db.get_all_lesson_templates()
    students = db.get_all_students()
    coaches = db.get_all_coaches()
    return render_template("lesson_templates.html", lesson_templates=lesson_templates,
        students=students, coaches=coaches
    )

@app.route("/lesson_templates/add", methods=["GET", "POST"])
@login_required
def add_lesson_template():
    if request.method == "POST":
        db.add_lesson_template(request.form["template_name"], request.form["coach_id"], request.form.getlist("student_ids"),)
        return redirect(url_for("lesson_templates"))

    return render_template("add_lesson_template.html", students=db.get_all_students(),
        coaches=db.get_all_coaches())

@app.route("/lesson_templates/edit/<int:lesson_template_id>", methods=["GET", "POST"])
@login_required
def edit_lesson_template(lesson_template_id):
    lesson_template = db.get_lesson_template_by_id(lesson_template_id)
    if request.method == "POST":
        db.update_lesson_template(lesson_template_id, request.form["template_name"], request.form["coach_id"],
            request.form.getlist("student_ids"),
        )
        return redirect(url_for("lesson_templates"))

    return render_template("edit_lesson_template.html", lesson_template=lesson_template,
        students=db.get_all_students(), coaches=db.get_all_coaches())

@app.route("/lesson_templates/delete/<int:lesson_template_id>")
@login_required
def delete_lesson_template(lesson_template_id):
    db.delete_lesson_template(lesson_template_id)
    return redirect(url_for("lesson_templates"))

@app.template_filter("ru_date")
@login_required
def ru_date(value):
    if not value:
        return ""

    for fmt in ("%Y.%m.%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%d.%m.%Y")
        except ValueError:
            pass

    return value  # если формат неожиданный


if __name__ == "__main__":
    app.run(debug=True)
