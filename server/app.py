import sqlite3
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Template folder ka path set kar rahe hain
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Check if templates folder exists
if not os.path.exists(TEMPLATE_DIR):
    print(f"⚠️ WARNING: 'templates' folder not found at {TEMPLATE_DIR}")
    print("👉 Please create a 'templates' folder inside 'server' and move 'index.html' there.")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

# Database Path
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def get_db_connection():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
#  NEW ROUTE: SERVE FRONTEND (Ye naya hai)
# ==========================================
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"<h1>Error: index.html not found</h1><p>Please make sure 'index.html' is inside the 'server/templates' folder.</p><p>Error details: {e}</p>", 404

# ==========================================
#  1. AUTHENTICATION
# ==========================================
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    conn = get_db_connection()
    if not conn: return jsonify({"message": "Database not initialized"}), 500
    user = conn.execute('SELECT * FROM students WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and user['password'] == password:
        return jsonify({"user": {"id": user['id'], "name": user['name'], "role": user['role']}})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"message": "Database not initialized"}), 500
    try:
        cur = conn.execute(
            "INSERT INTO students (name, email, password, course, year) VALUES (?, ?, ?, ?, ?)",
            (data['name'], data['email'], data['password'], data['course'], data['year'])
        )
        conn.commit()
        user_id = cur.lastrowid
        user = conn.execute('SELECT * FROM students WHERE id = ?', (user_id,)).fetchone()
        return jsonify({"user": {"id": user['id'], "name": user['name'], "role": user['role']}})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already exists"}), 400
    finally:
        conn.close()

# ==========================================
#  2. STUDENT DASHBOARD
# ==========================================
@app.route('/api/student/dashboard', methods=['GET'])
def student_dashboard():
    user_id = request.headers.get('x-user-id')
    if not user_id: return jsonify({"message": "Login Required"}), 401
    conn = get_db_connection()
    if not conn: return jsonify({"message": "Database error"}), 500
    student = conn.execute('SELECT name, course FROM students WHERE id = ?', (user_id,)).fetchone()
    if not student: return jsonify({"message": "Student not found"}), 404
    
    all_tasks = conn.execute('SELECT * FROM tasks ORDER BY order_no').fetchall()
    done_tasks = conn.execute('SELECT task_id FROM student_tasks WHERE student_id = ?', (user_id,)).fetchall()
    done_ids = [row['task_id'] for row in done_tasks]
    conn.close()
    
    total = len(all_tasks)
    progress = int((len(done_ids) / total) * 100) if total > 0 else 0
    health = 100
    if progress < 30: health -= 20
    
    tasks_res = []
    for t in all_tasks:
        is_done = t['id'] in done_ids
        urgent = (t['category'] == 'Fees' and not is_done)
        if urgent: health -= 15
        tasks_res.append({"id": t['id'], "title": t['title'], "category": t['category'], 
                          "status": "DONE" if is_done else "PENDING", "urgent": urgent})
    return jsonify({"student": dict(student), "progress": progress, "healthScore": max(0, health), "tasks": tasks_res})

@app.route('/api/student/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    user_id = request.headers.get('x-user-id')
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO student_tasks (student_id, task_id) VALUES (?, ?)", (user_id, task_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/student/docs', methods=['GET', 'POST'])
def handle_docs():
    user_id = request.headers.get('x-user-id')
    conn = get_db_connection()
    if request.method == 'POST':
        d = request.json
        conn.execute("INSERT INTO documents (student_id, doc_type, file_name) VALUES (?, ?, ?)", (user_id, d['doc_type'], d['file_name']))
        conn.commit()
        new = conn.execute('SELECT * FROM documents WHERE student_id=? ORDER BY id DESC LIMIT 1', (user_id,)).fetchone()
        conn.close()
        return jsonify(dict(new))
    else:
        docs = conn.execute("SELECT * FROM documents WHERE student_id=? ORDER BY uploaded_at DESC", (user_id,)).fetchall()
        conn.close()
        return jsonify([dict(row) for row in docs])

# ==========================================
#  3. ADMIN DASHBOARD
# ==========================================
@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    if request.headers.get('x-role') != 'admin': return jsonify({"message": "Forbidden"}), 403
    conn = get_db_connection()
    
    total_st = conn.execute("SELECT COUNT(*) FROM students WHERE role='student'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM documents WHERE status='PENDING'").fetchone()[0]
    students = conn.execute("SELECT id, name, course FROM students WHERE role='student'").fetchall()
    total_tasks = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    
    st_list = []
    at_risk = 0
    for s in students:
        done = conn.execute("SELECT COUNT(*) FROM student_tasks WHERE student_id=?", (s['id'],)).fetchone()[0]
        prog = int((done/total_tasks)*100) if total_tasks>0 else 0
        risk = "HIGH" if prog < 40 else "LOW"
        if risk == "HIGH": at_risk += 1
        st_list.append({"name": s['name'], "course": s['course'], "progress": prog, "risk": risk})
        
    queue = conn.execute("SELECT d.id, s.name as student, d.doc_type as docName FROM documents d JOIN students s ON d.student_id=s.id WHERE d.status='PENDING'").fetchall()
    conn.close()
    return jsonify({"totalStudents": total_st, "pendingDocs": pending, "atRisk": at_risk, "students": st_list, "verificationQueue": [dict(r) for r in queue]})

@app.route('/api/admin/doc/<int:id>', methods=['PATCH'])
def verify(id):
    conn = get_db_connection()
    conn.execute("UPDATE documents SET status=? WHERE id=?", (request.json['status'], id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ==========================================
#  4. CHATBOT
# ==========================================
@app.route('/api/chat', methods=['POST'])
def chat():
    msg = request.json.get('message', '').lower()
    if 'fee' in msg: r = "Fees deadline is approaching. Check Checklist."
    elif 'doc' in msg: r = "Please upload ID Proof in Documents tab."
    elif 'hostel' in msg: r = "Hostel registration is step 5."
    elif 'hello' in msg: r = "Hi! I am EduFlow AI."
    else: r = "I can help with Fees, Documents, or Hostels."
    return jsonify({"reply": r})

if __name__ == '__main__':
    print(f"🚀 Server running on http://127.0.0.1:5000")
    print(f"📂 Looking for templates in: {TEMPLATE_DIR}")
    app.run(port=5000, debug=True)