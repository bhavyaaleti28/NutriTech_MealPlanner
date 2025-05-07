from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://127.0.0.1:5500')
# Simple CORS configuration
CORS(app, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin',FRONTEND_URL )
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept,Origin')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

print("Current working directory:", os.getcwd())
print("Database path:", os.path.abspath('users.db'))
# Initialize SQLite database
def init_db():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Always try to create the table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      email TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL,
                      age INTEGER,
                      gender TEXT,
                      height REAL,
                      weight REAL,
                      diet_type TEXT,
                      cuisine TEXT,
                      allergies TEXT,
                      health_goal TEXT,
                      activity_level TEXT)''')
        conn.commit()
        conn.close()
        print("Database and table ensured.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise
init_db()
@app.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        print("Received signup data:", data)
        
        if not data:
            print("No data received")
            return jsonify({'message': 'No data received'}), 400

        # Validate required fields
        if not all(k in data for k in ['name', 'email', 'password']):
            return jsonify({'message': 'Missing required fields'}), 400

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            # Insert user data into database
            c.execute('''INSERT INTO users 
                        (name, email, password)
                        VALUES (?, ?, ?)''',
                     (data.get('name'),
                      data.get('email'),
                      data.get('password')))
            
            conn.commit()
            print("Signup data saved successfully")
            return jsonify({'message': 'User registered successfully'}), 201
        except sqlite3.IntegrityError as e:
            print("Database error:", str(e))
            return jsonify({'message': 'Email already exists'}), 400
        finally:
            conn.close()
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        print("Received login data:", data)
        
        if not data:
            return jsonify({'message': 'No data received'}), 400

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        c.execute('SELECT name FROM users WHERE email = ? AND password = ?',
                 (data.get('email'), data.get('password')))
        user = c.fetchone()
        conn.close()

        if user:
            print("Login successful")
            return jsonify({
                'message': 'Login successful',
                'name': user[0]
            }), 200
        else:
            print("Invalid credentials")
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/update_user', methods=['POST', 'OPTIONS'])
def update_user():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        print("Received update data:", data)
        
        if not data:
            return jsonify({'message': 'No data received'}), 400

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            # Update user data
            c.execute('''UPDATE users 
                        SET age = ?, gender = ?, height = ?, weight = ?,
                            diet_type = ?, cuisine = ?, allergies = ?,
                            health_goal = ?, activity_level = ?
                        WHERE email = ?''',
                     (data.get('age'), data.get('gender'), data.get('height'),
                      data.get('weight'), data.get('diet'), data.get('cuisine'),
                      data.get('allergies'), data.get('healthGoals'),
                      data.get('activityLevel'), data.get('email')))
            
            conn.commit()
            print("User data updated successfully")
            return jsonify({'message': 'User data updated successfully'}), 200
        except Exception as e:
            print("Database error:", str(e))
            return jsonify({'message': 'Failed to update user data'}), 500
        finally:
            conn.close()
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        print("Initializing database...")
        init_db()
        print("Database initialized")
        print("Starting server...")
        app.run(port=5001, debug=True)
    except Exception as e:
        print(f"Failed to start server: {str(e)}") 