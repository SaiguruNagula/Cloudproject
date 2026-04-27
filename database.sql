CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL UNIQUE,
    marks INTEGER NOT NULL,
    grade TEXT NOT NULL
);

INSERT OR IGNORE INTO students (name, roll_no, marks, grade) VALUES
('Alice Johnson', 'CS001', 95, 'A'),
('Bob Smith', 'CS002', 82, 'B'),
('Charlie Brown', 'CS003', 76, 'C'),
('Diana Prince', 'CS004', 91, 'A'),
('Evan Wright', 'CS005', 65, 'D');
