import os
import time
import mysql.connector
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection(retries=5, delay=2):
    host = os.getenv("MYSQL_HOST", "db")
    user = os.getenv("MYSQL_USER", "root")
    pwd  = os.getenv("MYSQL_PASSWORD", "")
    db   = os.getenv("MYSQL_DATABASE", "todolist")
    for _ in range(retries):
        try:
            return mysql.connector.connect(host=host, user=user, password=pwd, database=db)
        except mysql.connector.Error:
            time.sleep(delay)
    raise

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todolist (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL
        )
    """)
    cur.execute("""
        GRANT ALL PRIVILEGES ON todolist.* TO 'user-test'@'%' IDENTIFIED BY 'dhanya00';
    """)

    # 3. Optional: Apply changes
    cur.execute("FLUSH PRIVILEGES;")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todolist")
    tasks = cur.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO todolist (task) VALUES (%s)", (task,))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todolist WHERE id=%s", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


