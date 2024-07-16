from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
def get_db():
    try:
        db = mysql.connector.connect(
            host='db',  # Replace with your MySQL host
            user='profileapp_user',       # Replace with your MySQL username
            password='Frds@123',  # Replace with your MySQL password
            database='profileapp_db',      # Replace with your MySQL database name
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL)")
        db.commit()
        cursor.close()
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        try:
            db = get_db()
            if db:
                cursor = db.cursor()
                cursor.execute('INSERT INTO users (username) VALUES (%s)', (username,))
                db.commit()
                cursor.close()
                db.close()
                return redirect(url_for('profile', username=username))
            else:
                return "Failed to connect to database."
        except mysql.connector.Error as e:
            return f"An error occurred: {str(e)}"
    return render_template('index.html')

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)

@app.route('/users')
def users():
    try:
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute('SELECT username FROM users')
            all_users = cursor.fetchall()
            cursor.close()
            db.close()
            return render_template('users.html', users=all_users)
        else:
            return "Failed to connect to database."
    except mysql.connector.Error as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

