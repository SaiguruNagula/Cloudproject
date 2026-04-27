# AWS Scalable Web App Mini Project
**Student Record Management System**

This is a complete 3-tier web application designed to be deployed entirely on AWS infrastructure as a college mini-project. 

## 🏗️ Architecture Diagram

```text
       +--------------------+
       |                    |
       |  End User Browser  |
       |                    |
       +---------+----------+
                 |
                 | HTTP/HTTPS
                 |
                 v
       +--------------------+
       |                    |
       |       AWS S3       |  <--- Hosts static frontend (HTML/CSS/JS)
       |  (Static Hosting)  |
       |                    |
       +---------+----------+
                 |
                 | API Calls (AJAX/Fetch)
                 |
                 v
       +--------------------+
       |                    |
       |      AWS EC2       |  <--- Hosts Flask Backend (Python)
       | (Ubuntu Instance)  |       Runs on Port 5000
       |                    |
       +---------+----------+
                 |
                 | Psycopg2 Connection
                 |
                 v
       +--------------------+
       |                    |
       |      AWS RDS       |  <--- Managed PostgreSQL Database
       |   (PostgreSQL)     |       Stores Student Records
       |                    |
       +--------------------+
```

## 🚀 AWS Setup & Deployment Instructions

### Step 1: Set up RDS (Database)
1. Go to AWS Console -> **RDS** -> **Create database**.
2. Choose **Standard create** -> **PostgreSQL**.
3. Under Templates, choose **Free tier** (IMPORTANT).
4. Set DB instance identifier (e.g., `student-db`), Master username (`postgres`), and Master password (`password123`).
5. Under Connectivity, set **Public access** to **Yes** (for easier testing/initial setup).
6. Create a new VPC security group or allow inbound rules on port `5432` from anywhere (`0.0.0.0/0`).
7. Expand **Additional configuration**, enter Initial database name as `student_db`.
8. Click **Create database**. Wait for it to become "Available" and note the **Endpoint** URL.

### Step 2: Initialize Database
1. Use MySQL Workbench, DBeaver, or CLI to connect to your RDS instance using the Endpoint, username, and password.
2. Run the SQL queries provided in `database.sql` to create the table and insert sample data.

### Step 3: Set up EC2 (Backend)
1. Go to AWS Console -> **EC2** -> **Launch Instance**.
2. Name it `Flask-Backend`.
3. Select **Ubuntu Server 22.04 LTS** as the AMI.
4. Instance type: **t2.micro** (Free tier).
5. Create or select a Key Pair (download the `.pem` file).
6. Network settings: Allow **SSH traffic**, allow **HTTPS/HTTP traffic**.
7. Edit security group to add a Custom TCP Rule -> Port **5000** -> Source: Anywhere (`0.0.0.0/0`).
8. Click **Launch Instance**.
9. Once running, copy the **Public IPv4 address**.

### Step 4: Deploy Backend to EC2
1. Open terminal and connect via SSH:
   `ssh -i your-key.pem ubuntu@YOUR_EC2_IP`
2. Create app folder and upload files (`app.py`, `config.py`, `requirements.txt`, `setup.sh`).
   *You can use SCP to upload or clone via Git:*
   `scp -i your-key.pem app.py config.py requirements.txt setup.sh ubuntu@YOUR_EC2_IP:~`
3. Edit `config.py` on EC2 to insert your RDS endpoint and credentials.
4. Run the setup script:
   `chmod +x setup.sh`
   `./setup.sh`
5. Test the backend by visiting `http://YOUR_EC2_IP:5000/students` in your browser.

### Step 5: Set up S3 (Frontend)
1. Edit `frontend/index.html`. Replace `YOUR_EC2_PUBLIC_IP` in the JS section with your actual EC2 IP.
2. Go to AWS Console -> **S3** -> **Create bucket**.
3. Name it (e.g., `student-app-frontend-1234`). Uncheck "Block all public access" and acknowledge the warning.
4. Click **Create bucket**.
5. Upload `index.html` to the bucket.
6. Go to bucket **Properties** -> Scroll down to **Static website hosting** -> Edit -> Enable -> Index document: `index.html` -> Save.
7. Go to bucket **Permissions** -> **Bucket Policy** -> Edit and paste:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "PublicReadGetObject",
               "Effect": "Allow",
               "Principal": "*",
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
           }
       ]
   }
   ```
8. Get the Bucket Website Endpoint URL from Properties and open it in your browser. Done!

---

## 👨‍🏫 10 Tough Professor Questions & Answers

**Q1: Why did you use S3 for the frontend instead of hosting the HTML files directly on the EC2 instance?**
> **Answer:** Hosting static assets on S3 offloads network traffic and computing resources from the EC2 backend instance. S3 is highly available, cheaper for static file storage, and can be easily integrated with a CDN (CloudFront) for global caching, making the architecture far more scalable than serving static files via Flask.

**Q2: What is CORS, and why did you have to use `flask-cors` in your backend?**
> **Answer:** CORS stands for Cross-Origin Resource Sharing. It's a browser security feature that prevents a website on one domain (our S3 bucket URL) from making API requests to a different domain (our EC2 IP). We use `flask-cors` to send specific HTTP headers from the EC2 server telling the browser that it is safe to allow the S3 frontend to access its data.

**Q3: Is your current RDS setup secure for a production environment?**
> **Answer:** No. Currently, the RDS instance might be set to "Publicly Accessible" for ease of development. In a true production environment, the RDS instance should be placed in a Private Subnet within a VPC, blocking all internet traffic. Only the EC2 instance (in a Public Subnet or connected via NAT Gateway) should be allowed to communicate with the RDS database via Security Group rules.

**Q4: How does your application handle concurrent user requests?**
> **Answer:** Flask's built-in development server (used here) is not optimized for high concurrency. However, each incoming HTTP request opens a new database connection (via `get_db_connection()`) and closes it, preventing connection bleed. For real scalability, we should use a WSGI server like Gunicorn and a connection pooler so we don't open/close connections on every single request.

**Q5: What happens if your EC2 instance crashes? How would you make this highly available?**
> **Answer:** If the EC2 instance crashes, the backend goes down. To make it highly available, we should create an Amazon Machine Image (AMI) of the configured EC2 instance, put it inside an Auto Scaling Group (ASG), and place an Application Load Balancer (ALB) in front. If an instance fails, the ASG will spin up a new one automatically.

**Q6: What is a REST API, and does your Flask app follow RESTful principles?**
> **Answer:** A REST API is an architectural style that maps HTTP methods (GET, POST, DELETE, PUT) to CRUD operations on resources. Yes, our app follows this: `GET /students` retrieves data, `POST /students` creates a record, and `DELETE /students/<id>` removes a record.

**Q7: Explain the `nohup` command used in your `setup.sh` script.**
> **Answer:** `nohup` stands for "no hangup". When you run a command via SSH, closing the SSH terminal usually kills all processes tied to that session. `nohup` ignores the hangup signal, allowing the Flask application to keep running in the background even after we close our SSH connection to the EC2 instance. The `&` symbol at the end puts the process in the background.

**Q8: Your frontend fetches data every 3 seconds (`setInterval`). What's the architectural flaw here, and how would you fix it?**
> **Answer:** This approach is called "polling". The flaw is that it constantly hammers the backend and database with queries even if no data has changed, wasting bandwidth and compute resources. A better solution would be using WebSockets for real-time bi-directional communication, or Server-Sent Events (SSE) so the server only pushes data when an update actually occurs.

**Q9: Why are we using `psycopg2.extras.RealDictCursor` in the database connection?**
> **Answer:** By default, database cursors return rows as tuples (e.g., `(1, 'Alice', ...)`), which is hard to map to JSON. `RealDictCursor` returns rows as Python dictionaries where column names are keys (e.g., `{'id': 1, 'name': 'Alice'}`). This makes it trivial to convert the SQL result directly into JSON using Flask's `jsonify()`.

**Q10: What is the purpose of the `requirements.txt` file, and why is it best practice?**
> **Answer:** `requirements.txt` lists all external Python libraries and their specific versions required to run the application. It ensures consistency across different environments (dev, staging, production). Without it, deploying to EC2 would require manually remembering and installing every dependency, which is error-prone.
