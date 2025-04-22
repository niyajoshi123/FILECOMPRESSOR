from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image
import fitz

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootpassword'
app.config['MYSQL_DB'] = 'file_compression'

# File Uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        session['username'] = username
        return redirect(url_for('filepage'))
    else:
        return "Invalid credentials"

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing = cursor.fetchone()

    if existing:
        return render_template('register.html', error='Username already exists')

    cursor.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
    mysql.connection.commit()
    session['username'] = username
    return redirect(url_for('filepage'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/guest')
def guest():
    return redirect(url_for('filepage'))

@app.route('/filepage')
def filepage():
    username = session.get('username')
    files = []

    if username:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            user_id = user['id']
            cursor.execute("SELECT * FROM files WHERE user_id = %s", (user_id,))
            files = cursor.fetchall()

    return render_template('filepage.html', username=username, files=files)


@app.route('/compress/pdf', methods=['GET'])
def compress_pdf_page():
    return render_template('compress_pdf.html')

@app.route('/compress/png', methods=['GET'])
def compress_png_page():
    return render_template('compress_png.html')

@app.route('/compress/jpg', methods=['GET'])
def compress_jpg_page():
    return render_template('compress_jpg.html')

def compress_pdf_file(input_path, output_path, quality):
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

@app.route('/compress/pdf', methods=['POST'])
def compress_pdf():
    file = request.files['file']
    level = request.form['level']
    username = session.get('username', 'guest')

    if file:
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)

        # Set quality level based on user choice
        quality = 30 if level == 'high' else 50 if level == 'medium' else 70

        # Use PyMuPDF or Ghostscript to compress
        compressed_filename = f"compressed_{filename}"
        compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)
        compress_pdf_file(original_path, compressed_path, quality)

        original_size = round(os.path.getsize(original_path) / 1024, 2)
        compressed_size = round(os.path.getsize(compressed_path) / 1024, 2)

        if username != 'guest':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                cursor.execute("""
                    INSERT INTO files (user_id, filename, filetype, original_size, compressed_size, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, compressed_filename, 'pdf', original_size, compressed_size, datetime.now()))
                mysql.connection.commit()

        return render_template('compress_pdf.html',
                               original_size=original_size,
                               compressed_size=compressed_size,
                               download_link=url_for('download_file', filename=compressed_filename))


def compress_image(file_path, output_path, quality):
    img = Image.open(file_path)
    img.save(output_path, optimize=True, quality=quality)

@app.route('/compress/png', methods=['POST'])
def compress_png():
    file = request.files['file']
    level = request.form['level']
    username = session.get('username', 'guest')

    if file:
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)

        quality = 70 if level == 'high' else 50 if level == 'medium' else 30
        compressed_filename = f"compressed_{filename}"
        compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)
        compress_image(original_path, compressed_path, quality)

        original_size = round(os.path.getsize(original_path) / 1024, 2)
        compressed_size = round(os.path.getsize(compressed_path) / 1024, 2)

        if username != 'guest':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                cursor.execute("""
                    INSERT INTO files (user_id, filename, filetype, original_size, compressed_size, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, compressed_filename, 'png', original_size, compressed_size, datetime.now()))
                mysql.connection.commit()

        return render_template('compress_png.html',
                               original_size=original_size,
                               compressed_size=compressed_size,
                               download_link=url_for('download_file', filename=compressed_filename))

@app.route('/compress/jpg', methods=['POST'])
def compress_jpg():
    file = request.files['file']
    level = request.form['level']
    username = session.get('username', 'guest')

    if file:
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)

        quality = 70 if level == 'high' else 50 if level == 'medium' else 30
        compressed_filename = f"compressed_{filename}"
        compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)
        compress_image(original_path, compressed_path, quality)

        original_size = round(os.path.getsize(original_path) / 1024, 2)
        compressed_size = round(os.path.getsize(compressed_path) / 1024, 2)

        if username != 'guest':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                cursor.execute("""
                    INSERT INTO files (user_id, filename, filetype, original_size, compressed_size, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, compressed_filename, 'jpg', original_size, compressed_size, datetime.now()))
                mysql.connection.commit()

        return render_template('compress_jpg.html',
                               original_size=original_size,
                               compressed_size=compressed_size,
                               download_link=url_for('download_file', filename=compressed_filename))

@app.route('/download_history')
def download_history():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return "User not found"

    user_id = user['id']
    cursor.execute("SELECT * FROM files WHERE user_id = %s", (user_id,))
    files = cursor.fetchall()

    return render_template('download_history.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username or username == 'guest':
        return redirect(url_for('login'))  # or show an access denied page

    cursor = mysql.connection.cursor()

    # Total files compressed by the logged-in user
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return redirect(url_for('login'))

    user_id = user[0]

    cursor.execute("SELECT COUNT(*) FROM files WHERE user_id = %s", (user_id,))
    total_files = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(compressed_size / original_size)
        FROM files WHERE user_id = %s AND original_size > 0
    """, (user_id,))
    ratio = cursor.fetchone()[0]
    avg_ratio = round(ratio * 100, 2) if ratio else 0

    cursor.execute("""
        SELECT filetype, COUNT(*), SUM(original_size), SUM(compressed_size)
        FROM files
        WHERE user_id = %s
        GROUP BY filetype
    """, (user_id,))
    filetype_stats = cursor.fetchall()

    return render_template("dashboard.html",
                           total_files=total_files,
                           avg_ratio=avg_ratio,
                           filetype_stats=filetype_stats)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
