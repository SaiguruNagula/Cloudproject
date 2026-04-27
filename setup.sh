#!/bin/bash
echo "Starting EC2 Setup for Flask Backend..."

# Update package lists
sudo apt-get update -y

# Install Python3 and pip
sudo apt-get install python3 python3-pip -y

# Allow port 5000 in the firewall
sudo ufw allow 5000/tcp
sudo ufw allow 22/tcp
sudo ufw --force enable

# Install Python requirements
# Assuming files are uploaded to /home/ubuntu/app
pip3 install -r requirements.txt || pip3 install flask flask-cors boto3

# Start the Flask app using nohup so it runs in background
echo "Starting Flask Application..."
nohup python3 app.py > flask_app.log 2>&1 &

echo "Setup complete. Flask is running on port 5000."
