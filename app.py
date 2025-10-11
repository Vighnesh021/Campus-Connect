from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, user TEXT, content TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        content = request.form['content']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (user, content) VALUES (?, ?)", (session['username'], content))
        conn.commit()
        conn.close()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('dashboard.html', posts=posts, user=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
