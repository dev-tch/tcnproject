# TicketCounterNotify

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)

## Project Description
**TicketCounterNotify** is a web-based application that allows users in a queue to receive real-time updates on the counters of selected offices. This helps them track the progress. The application also enables managers to monitor the number of tickets served at each window in the office. Additionally, it provides an interface for agents to increment the counter.

## Features
- User Authentication: Account creation, login, logout, and password reset via email.
- Role-Based Access: Different functionalities for managers, agents, and clients.
- Office Management: Managers can create, update, delete, and reset office counters.
- Agent Management: Assign agents to specific office windows.
- Real-Time Tracking: Real-time updates of counter statuses for clients.
- WebSocket Integration: Real-time communication for counter updates.
- Search and Selection: Users can search for offices and track their counters.

## Technologies Used
- **Backend**: Django, Django REST framework, Channels, Channels Redis
- **Frontend**: Bootstrap,  jQuery, Axios
- **Database**: PostgreSQL or MySQL
- **Messaging**: Redis
- **Deployment**: Render

## Setup and Installation
1. **Install MySQL server and start the service:**
   ```sh
   sudo apt install mysql-server
   sudo service mysql start 
2. **Install Redis server and start the service:**   
   ```sh
   sudo apt install redis
   sudo service redis start 
3. **Clone the repository:**
   ```sh
   git clone https://github.com/dev-tch/tcnproject.git
   cd tcnproject 
  4. **Install virtualenv, activate it, and install requirements:**
		```sh
		pip install virtualenv 
		virtualenv .venv
		source .venv/bin/activate
		pip install -r requirements.txt
 5. **Create a `.env` file and configure all the environment variables:**
	 ```sh
	 #config database credentials
	DB_ENGINE=django.db.backends.mysql
	DB_NAME=tcn_db
	DB_USER=***
	DB_PASSWORD=***
	DB_HOST=localhost
	DB_PORT=3306
	#config gmail smpt server
	EMAIL_HOST=smtp.gmail.com
	EMAIL_PORT=587
	EMAIL_USE_TLS=true
	EMAIL_HOST_USER=***
	EMAIL_HOST_PASSWORD=***
	#config redis credentials
	REDIS_HOST=localhost
	REDIS_PORT=6379
	# Replace *** with your credentials (MySQL, Gmail)
 6. **Make migrations and run migrate to create tables in the database:**
	  ```sh
	  sudo python manage.py makemigrations tcn
	  sudo python manage.py migrate
 7. **Run Daphne ASGI server to serve your HTTP and WebSocket requests:**
	   ```sh
	   sudo daphne -b 0.0.0.0 -p 8000 tcnproject.asgi:application
  
  8. **Open your browser and navigate to the home page:**
	   ```sh
	   http://localhost:8000