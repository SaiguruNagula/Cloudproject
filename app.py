from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import config
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    # Connect to the local SQLite file
    conn = sqlite3.connect(config.DB_FILE)
    # This allows us to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row 
    return conn

# Auto-initialize the database if it doesn't exist yet
def init_db():
    if not os.path.exists(config.DB_FILE):
        conn = get_db_connection()
        with open('database.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Initialized SQLite Database with sample data.")

# Serve the frontend UI at the root URL
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/students', methods=['GET'])
def get_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        
        # Convert sqlite3.Row objects to standard python dictionaries
        students = [dict(row) for row in cursor.fetchall()]
        
        connection.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    roll_no = data.get('roll_no')
    marks = data.get('marks')
    grade = data.get('grade')
    
    if not all([name, roll_no, marks, grade]):
        return jsonify({"error": "Missing data"}), 400
        
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # SQLite uses '?' as placeholders instead of '%s'
        sql = "INSERT INTO students (name, roll_no, marks, grade) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (name, roll_no, marks, grade))
        connection.commit()
        connection.close()
        return jsonify({"message": "Student added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Roll number already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM students WHERE id = ?"
        cursor.execute(sql, (id,))
        connection.commit()
        connection.close()
        return jsonify({"message": "Student deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Automatically create db on startup
    app.run(host='0.0.0.0', port=5000)
