from flask import Flask, render_template, request, redirect, url_for,send_from_directory, abort
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder and allowed extensions

UPLOAD_FOLDER = 'uploads'  # Make sure this folder exists
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload')
def upload_file():
    return render_template('upload.html')  # Render the HTML form


@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        f = request.files['file']  # Get the uploaded file
        
        if f.filename == '':
            return 'No selected file'
        
        # Save the file securely
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return render_template('success.html', filename=filename)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Ensure the filename is safe
        safe_filename = secure_filename(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER'], safe_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404) 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("1.html")

@app.route("/home", methods=["POST"])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    if name == "student" and password == "student":
        return render_template("2.html")
    elif name == "admin" and password == "admin":
        return render_template("2a.html")
    else:
        return render_template("11.html")

@app.route("/signout")
def signout():
    return render_template("1.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register")
def register():
    return render_template("r1.html")

@app.route("/student")
def student():
    return render_template("2.html")

@app.route("/reg", methods=["POST"])
def reg():
    # Retrieve form data
    name = request.form.get("name")
    father = request.form.get("father")
    number = request.form.get("num")
    email = request.form.get("email")
    rank = request.form.get("rank")
    telephone = request.form.get("telephone")
    file = request.files.get("file")  # Get the uploaded file

    # Check that all required fields have values
    if not all([name, father, number, email, rank, telephone]) or not file or not allowed_file(file.filename):
        return render_template("r1.html")  # Return to form page if validation fails

    # Save the file
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    with sql.connect("database.db") as con:
        cur = con.cursor()
        
        # Insert new record into the database
        cur.execute(
            "INSERT INTO STUDENTS (name, father, num, email, rank, telephone, file) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, father, number, email, rank, telephone, filename)  # Save filename in the database
        )
        con.commit()  # Commit the transaction
        return render_template("success.html")
    
@app.route('/delete/<string:name>', methods=['POST'])
def delete_student(name):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM STUDENTS WHERE name=?", (name,))
        con.commit()
    return redirect(url_for('list2'))  # Redirect to the list of students after deletion

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

@app.route('/list2')
def list2():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS")
    rows = cur.fetchall()
    return render_template("list2.html", rows=rows)

@app.route("/back")
def back():
    return render_template("2.html")

@app.route("/already")
def already():
    return render_template("alread.html")

@app.route("/see", methods=['POST'])
def see():
    phone = request.form.get("num")
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS WHERE num=?", (phone,))
    k = cur.fetchall()

    if k:
        return render_template("list.html", rows=k)
    else:
        return render_template("not.html")

@app.route("/admin")
def admin():
    return render_template("2a.html")

@app.route("/cutoff")
def cutoff():
    return render_template("cutoff.html")

@app.route("/see2", methods=['POST'])
def see2():
    name = request.form.get("name")
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENTS WHERE name=?", (name,))
    k = cur.fetchall()
    return render_template("list2.html", rows=k)

@app.route("/stationary")
def stationary():
    return render_template("stationary.html")

if __name__ == "__main__":
    app.run(debug=True)