from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask App
app = Flask(__name__)

# Secret key for sessions
app.secret_key = "supersecretkey"

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -----------------------------
# REGISTER
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # Hash password
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect('/login')

        except:
            return 'User already exists!'

    return render_template('register.html')

# -----------------------------
# LOGIN
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM users WHERE username=?',
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):

            session['username'] = username

            return redirect('/dashboard')

        else:
            return render_template('error.html')

    return render_template('login.html')

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route('/dashboard')
def dashboard():

    if 'username' in session:

        return render_template(
            'dashboard.html',
            username=session['username']
        )

    return redirect('/login')

# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():

    session.pop('username', None)

    return redirect('/')

# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)