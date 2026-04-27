# Comprehensive Viva Guide: AWS Scalable Web App

This document contains everything you need to know to confidently defend your mini-project during your college Viva/Presentation. Read through this carefully!

---

## 1. Project Overview (The "Elevator Pitch")
**If the professor asks: "Explain your project in 1 minute."**

> "My project is a **3-tier Cloud-Native Student Record Management System** deployed entirely on AWS. It separates the presentation, logic, and data layers to ensure scalability.
> 1. **Frontend (Presentation):** Built with HTML, JS, and Tailwind CSS. In production, it is hosted on **AWS S3** as a static website, making it incredibly fast and cheap to serve.
> 2. **Backend (Logic):** Built using **Python Flask**. It is hosted on an **AWS EC2** instance running Ubuntu. It acts as a REST API to process incoming data.
> 3. **Database (Data):** Uses **PostgreSQL** hosted on **AWS RDS** (Relational Database Service). This ensures our database is managed, backed up automatically, and highly available."

---

## 2. Core Concepts You Must Know

### A. The Three-Tier Architecture
*   **Tier 1 (Client):** The user's browser loads the static files (HTML/CSS/JS).
*   **Tier 2 (Application/Server):** The EC2 instance running Flask. It listens for HTTP requests (like GET or POST), processes them, and talks to the database.
*   **Tier 3 (Database):** The RDS Postgres instance that securely stores the actual student records.

### B. Ports Used in the Project
*   **Port 80 / 443:** Used by S3 and web browsers for standard HTTP/HTTPS web traffic.
*   **Port 5000:** The default port where our Flask application runs on EC2.
*   **Port 5432:** The default port for PostgreSQL databases. Our EC2 instance talks to RDS on this port.
*   **Port 22:** SSH port. You use this to remotely log into your EC2 Ubuntu instance from your laptop.

### C. AWS Services Used
*   **Amazon EC2 (Elastic Compute Cloud):** A virtual server in the cloud. It provides raw computing power. We use it to run our Python code.
*   **Amazon S3 (Simple Storage Service):** Object storage. Instead of storing our HTML files on EC2, we store them in S3 because it's cheaper, infinitely scalable, and AWS handles the web-serving for us.
*   **Amazon RDS (Relational Database Service):** A managed SQL database. We don't have to install Postgres manually; AWS installs it, manages backups, and handles hardware failures.

---

## 3. Top 15 Potential Viva Questions & Answers

### 🌐 Cloud & Architecture Questions

**Q1: Why did you use AWS instead of just hosting everything on one local computer?**
**A:** AWS provides high availability, scalability, and disaster recovery. If a local computer's hard drive fails, data is lost. In AWS, RDS handles automated backups, S3 is highly durable, and EC2 instances can be spun up in seconds if traffic increases.

**Q2: Why use S3 for the frontend instead of putting the HTML files on the EC2 instance?**
**A:** Decoupling. Serving static files (HTML/CSS) from EC2 wastes computing power (CPU/RAM). S3 is specifically designed to serve static files rapidly to millions of users at a fraction of the cost. This leaves the EC2 instance free to only process complex API logic.

**Q3: What are AWS Security Groups?**
**A:** They act as a virtual firewall for our AWS resources. For example, our EC2 Security Group only allows traffic on Port 5000 (for Flask) and Port 22 (for SSH). Our RDS Security Group only allows traffic on Port 5432.

**Q4: Is your current database setup secure for a real-world enterprise?**
**A:** No. For college testing, our RDS might be set to "Publicly Accessible". In the real world, RDS should be placed in a **Private Subnet** (no internet access). Only the EC2 instance (in a Public Subnet) should be allowed to talk to the RDS database.

### 🐍 Backend & Python Questions

**Q5: What is a REST API?**
**A:** REST stands for Representational State Transfer. It's an architectural style where the backend exposes "endpoints" (URLs), and the frontend uses standard HTTP methods to interact with data. 
*   `GET /students` (Read data)
*   `POST /students` (Create data)
*   `DELETE /students/<id>` (Delete data)

**Q6: What does the `flask-cors` library do in your project?**
**A:** CORS stands for **Cross-Origin Resource Sharing**. By default, browsers block a website on one domain (like an S3 bucket URL) from making API requests to a different domain (like our EC2 IP). `flask-cors` adds HTTP headers to the Flask server telling the browser: *"It's okay, allow this frontend to access my data."*

**Q7: What is `pg8000`? Why didn't you use an ORM like SQLAlchemy?**
**A:** `pg8000` is a pure-Python database driver that allows our Flask code to communicate with PostgreSQL. I used it instead of SQLAlchemy to keep the architecture lightweight and demonstrate a clear understanding of writing raw SQL queries.

**Q8: Explain the `nohup` command used in your EC2 setup script.**
**A:** `nohup` stands for "no hangup". Normally, if I SSH into EC2, start the Flask app, and close my laptop, the app dies. `nohup` tells Linux to keep the Flask app running in the background even after my SSH session is disconnected. The `&` symbol puts the process in the background.

### 🐘 Database Questions

**Q9: Why did you choose PostgreSQL over a NoSQL database like MongoDB?**
**A:** Student records are highly structured data with clear relationships (ID, Name, Roll No, Marks). Relational databases (SQL/Postgres) guarantee ACID properties (Atomicity, Consistency, Isolation, Durability) ensuring data integrity, whereas NoSQL is better for unstructured or rapidly changing data schemas.

**Q10: What does `SERIAL PRIMARY KEY` do in your SQL table?**
**A:** `PRIMARY KEY` ensures every student has a unique identifier, making it impossible to have duplicate rows. `SERIAL` tells Postgres to automatically auto-increment the ID number every time a new student is inserted, so we don't have to calculate it manually in Python.

**Q11: How do you prevent SQL Injection in your app?**
**A:** In the `app.py` POST route, I pass variables to the database using parameterized queries: `cursor.execute(sql, (name, roll_no, marks, grade))`. I do **not** concatenate strings (like `sql = "INSERT... " + name`). Parameterization forces the database engine to treat user input strictly as data, not executable code.

### 💻 Frontend & Javascript Questions

**Q12: How does your frontend communicate with the backend?**
**A:** It uses the modern Javascript `Fetch API`. It sends asynchronous HTTP requests to the Flask server. Because it's asynchronous, the web page doesn't freeze or reload while waiting for the database to respond.

**Q13: Why did you use Tailwind CSS instead of Bootstrap or plain CSS?**
**A:** Tailwind is a utility-first CSS framework. Instead of writing separate CSS files, I apply pre-existing styling classes directly to HTML elements (like `bg-slate-800` or `rounded-xl`). It leads to faster development, smaller file sizes, and more modern UI designs compared to Bootstrap's rigid components.

**Q14: I noticed the frontend updates automatically. How did you achieve that?**
**A:** I used the Javascript `setInterval()` function to call the `fetchStudents()` API every 3000 milliseconds (3 seconds). This is known as "polling".

**Q15: Is polling the best way to do real-time updates? What is the flaw?**
**A:** No, polling is resource-intensive. It hammers the backend with requests every 3 seconds even if no new student was added, wasting bandwidth and database compute. In a production environment, I would upgrade this to use **WebSockets** or **Server-Sent Events (SSE)**, so the server only pushes data to the frontend when an actual change occurs.
