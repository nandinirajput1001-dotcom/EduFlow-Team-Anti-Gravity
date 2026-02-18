DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS student_tasks;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS students;

-- 1. Students Table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    course TEXT,
    year TEXT,
    role TEXT DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tasks Table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    order_no INTEGER NOT NULL
);

-- 3. Student Progress
CREATE TABLE student_tasks (
    student_id INTEGER,
    task_id INTEGER,
    status TEXT DEFAULT 'DONE',
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, task_id),
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);

-- 4. Documents Table
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    doc_type TEXT,
    file_name TEXT,
    status TEXT DEFAULT 'PENDING',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES students(id)
);

-- SEED DATA
INSERT INTO tasks (title, category, order_no) VALUES
('Submit Identity Proof', 'Documents', 1),
('Upload 12th Marksheet', 'Documents', 2),
('Pay Semester 1 Fees', 'Fees', 3),
('Activate LMS Account', 'LMS', 4),
('Hostel Registration', 'LMS', 5);

-- Admin & Student Users
INSERT INTO students (name, email, password, role) 
VALUES ('System Admin', 'admin@eduflow.edu', 'adminpass2024', 'admin');

INSERT INTO students (name, email, password, course, year, role)
VALUES ('Rahul Sharma', 'student@eduflow.edu', 'password', 'B.Tech CS', '2024', 'student');