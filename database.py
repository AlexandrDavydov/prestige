import sqlite3
from datetime import datetime

DB_NAME = "db.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS cards
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       price REAL NOT NULL,
                       lessons_count INTEGER NOT NULL,
                       duration TEXT NOT NULL,
                       color TEXT,
                       status TEXT NOT NULL,
                       creation_date TEXT
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS students
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       middle_name TEXT,
                       contacts TEXT,
                       birthday TEXT,
                       lessons_count INTEGER,
                       additional_info TEXT,
                       creation_date TEXT
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS groups
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       student_ids TEXT
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS coaches
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       middle_name TEXT,
                       contacts TEXT,
                       birthday TEXT,
                       lessons_count INTEGER,
                       lessons_paid INTEGER,
                       student_payment INTEGER,
                       additional_info TEXT,
                       creation_date TEXT
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS lessons
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT NOT NULL,
                       coach_id INTEGER NOT NULL,
                       student_ids TEXT,
                       status TEXT NOT NULL
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS sold_cards
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT NOT NULL,
                       card_id INTEGER NOT NULL
                     )
                   """)
    conn.commit()
    conn.close()


# Cards
def get_all_cards():
    conn = get_connection()
    cards = conn.execute("SELECT * FROM cards").fetchall()
    conn.close()
    return cards


def get_card_by_id(card_id):
    conn = get_connection()
    card = conn.execute("SELECT * FROM cards WHERE id=?", (card_id,)).fetchone()
    conn.close()
    return card


def create_card(name, price, lessons_count, duration, color, status):
    conn = get_connection()
    conn.execute("""
                 INSERT INTO cards (name, price, lessons_count, duration, color, status, creation_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)
                 """,
                 (name, price, lessons_count, duration, color, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def update_card(card_id, name, price, lessons_count, duration, color, status):
    conn = get_connection()
    conn.execute("""
                 UPDATE cards
                 SET name=?, price=?, duration=?, color=?, status=?  WHERE id = ?
                 """, (name, price, lessons_count, duration, color, status, card_id))
    conn.commit()
    conn.close()


def delete_card(card_id):
    conn = get_connection()
    conn.execute("DELETE FROM cards WHERE id=?", (card_id,))
    conn.commit()
    conn.close()


# Students
def get_all_students():
    conn = get_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return students


def get_student_by_id(student_id):
    conn = get_connection()
    student = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    conn.close()
    return student


def add_student(first_name, last_name, middle_name, contacts, birthday, lessons_count, additional_info):
    conn = get_connection()
    conn.execute("""
                 INSERT INTO students (first_name, last_name, middle_name, contacts, birthday, lessons_count,
                                       additional_info, creation_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                 """, (first_name, last_name, middle_name, contacts, birthday, lessons_count, additional_info,
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def update_student(student_id, first_name, last_name, middle_name, contacts, birthday, lessons_count, additional_info):
    conn = get_connection()
    conn.execute("""
                 UPDATE students
                 SET first_name=?, last_name=?, middle_name=?, contacts=?, birthday=?, lessons_count=?, additional_info=?
                 WHERE id = ?
                 """,
                 (first_name, last_name, middle_name, contacts, birthday, lessons_count, additional_info, student_id))
    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = get_connection()
    conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()


# Groups
def get_all_groups():
    conn = get_connection()
    groups = conn.execute("SELECT * FROM groups").fetchall()
    conn.close()
    return groups


def get_group_by_id(group_id):
    conn = get_connection()
    group = conn.execute("SELECT * FROM groups WHERE id=?", (group_id,)).fetchone()
    conn.close()
    return group


def add_group(student_ids):
    conn = get_connection()
    conn.execute("INSERT INTO groups (student_ids) VALUES (?)", (",".join(map(str, student_ids)),))
    conn.commit()
    conn.close()


def update_group(group_id, student_ids):
    conn = get_connection()
    conn.execute("UPDATE groups SET student_ids=? WHERE id=?", (",".join(map(str, student_ids)), group_id))
    conn.commit()
    conn.close()


def delete_group(group_id):
    conn = get_connection()
    conn.execute("DELETE FROM groups WHERE id=?", (group_id,))
    conn.commit()
    conn.close()


# Coaches
def get_all_coaches():
    conn = get_connection()
    coaches = conn.execute("SELECT * FROM coaches").fetchall()
    conn.close()
    return coaches


def get_coach_by_id(coach_id):
    conn = get_connection()
    coach = conn.execute("SELECT * FROM coaches WHERE id=?", (coach_id,)).fetchone()
    conn.close()
    return coach


def add_coach(first_name, last_name, middle_name, contacts, birthday, lessons_count, lessons_paid, student_payment, additional_info):
    conn = get_connection()
    conn.execute("""
                 INSERT INTO coaches (first_name, last_name, middle_name, contacts, birthday, lessons_count,
                                      lessons_paid, student_payment, additional_info, creation_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                 """, (first_name, last_name, middle_name, contacts, birthday, lessons_count, lessons_paid, student_payment,
                       additional_info, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def update_coach(coach_id, first_name, last_name, middle_name, contacts, birthday, lessons_count, lessons_paid, student_payment, additional_info):
    conn = get_connection()
    conn.execute("""
                 UPDATE coaches SET first_name=?, last_name=?, middle_name=?, contacts=?, birthday=?, lessons_count=?, 
                                    lessons_paid=?, student_payment=?, additional_info=?
                 WHERE id = ?
                 """,
                 (first_name, last_name, middle_name, contacts, birthday, lessons_count, lessons_paid, student_payment, additional_info, coach_id))
    conn.commit()
    conn.close()


def delete_coach(coach_id):
    conn = get_connection()
    conn.execute("DELETE FROM coaches WHERE id=?", (coach_id,))
    conn.commit()
    conn.close()
# ===== Lessons =====

def get_all_lessons():
    conn = get_connection()
    lessons = conn.execute("SELECT * FROM lessons").fetchall()
    conn.close()
    return lessons

def get_lesson_by_id(lesson_id):
    conn = get_connection()
    lesson = conn.execute(
        "SELECT * FROM lessons WHERE id=?", (lesson_id,)
    ).fetchone()
    conn.close()
    return lesson

def add_lesson(date, coach_id, student_ids, status):
    conn = get_connection()
    conn.execute("""
        INSERT INTO lessons (date, coach_id, student_ids, status)
        VALUES (?, ?, ?, ?)
    """, (date, coach_id, ",".join(student_ids), status))
    conn.commit()
    conn.close()

def update_lesson(lesson_id, date, coach_id, student_ids, status):
    conn = get_connection()
    conn.execute("""
        UPDATE lessons
        SET date=?, coach_id=?, student_ids=?, status=?
        WHERE id=?
    """, (date, coach_id, ",".join(student_ids), status, lesson_id))
    conn.commit()
    conn.close()

def delete_lesson(lesson_id):
    conn = get_connection()
    conn.execute("DELETE FROM lessons WHERE id=?", (lesson_id,))
    conn.commit()
    conn.close()

    conn.commit()
    conn.close()

def decrement_lessons_from_students(lesson_id):
    conn = get_connection()
    cursor = conn.cursor()

    lesson = cursor.execute(
        "SELECT student_ids FROM lessons WHERE id = ?",
        (lesson_id,)
    ).fetchone()

    if not lesson or not lesson["student_ids"]:
        conn.close()
        return

    student_ids = [
        int(sid)
        for sid in lesson["student_ids"].split(",")
        if sid.strip().isdigit()
    ]

    if not student_ids:
        conn.close()
        return

    placeholders = ",".join("?" for _ in student_ids)

    cursor.execute(
        f"""
        UPDATE students
        SET lessons_count = lessons_count - 1
        WHERE id IN ({placeholders})
        """,
        student_ids
    )

    conn.commit()
    conn.close()

def increment_lessons_to_couch(lesson_id):
    conn = get_connection()
    cursor = conn.cursor()

    lesson = cursor.execute(
        "SELECT student_ids, coach_id FROM lessons WHERE id = ?",
        (lesson_id,)
    ).fetchone()

    if not lesson or not lesson["student_ids"]:
        conn.close()
        return

    # Python считает количество
    student_ids = [
        int(sid)
        for sid in lesson["student_ids"].split(",")
        if sid.strip().isdigit()
    ]

    students_count = len(student_ids)
    coach_id = lesson["coach_id"]

    cursor.execute(
        """
        UPDATE coaches
        SET lessons_count = lessons_count + ?
        WHERE id = ?
        """,
        (students_count, coach_id)
    )

    conn.commit()
    conn.close()
