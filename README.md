# TicketCounterNotify

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)
6. [API Endpoints](#api-endpoints)

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
       ```

## api-endpoints

$${\color{red}Api<1> \space \color{blue}Assign  \space Agent \space To \space Window }$$

POST /api/windows/<int:number_window>/assign-agent/

This API endpoint allows an authenticated manager to assign an agent user to a specific office window

> Body Parameters

```json
{
  "agent_id": 12345,
  "office_id": "ref789"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Cookie|header|string| yes |require the user to be authenticated|
|body|body|object| yes |json data|
|» agent_id|body|integer| yes |the unique id of agent user|
|» office_id|body|string| yes |the unique reference of an office|

> Response Examples

> Success

```json
{
  "message": "Agent assigned to existing window successfully"
}
```

$${\color{red}Api<2> \space \color{blue}increment  \space Counter \space By \space Agent }$$

POST /api/offices/<str:ref_office>/increment-counter/

This API endpoint allows an authenticated Agent, assigned to a specific window within an office, to increment the office's counter

> Body Parameters

```json
{
  "agent_id": 12345,
  "number_window": 1
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Cookie|header|string| yes |require the user to be authenticated|
|body|body|object| yes |json data|
|» agent_id|body|integer| yes |the unique id of agent user|
|» number_window|body|integer| yes |the unique number of window |

> Response Examples

> Success

```json
{
  "counter": 80
}
```

$${\color{red}Api<3> \space \color{blue}enable  \space or  \space disable  \space tracking \space offices }$$

POST /api/offices/<int:id_user>/<str:action>/apply

This API endpoint allows an authenticated client to enable or disable tracking of an office counter

> Body Parameters

```json
{
   "ref_offices": ["ref01", "ref02", "ref03"]
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|action|query|string| yes |the value must be 'enable' or 'disable'|
|Cookie|header|string| yes |require the user to be authenticated|
|body|body|object| yes |json data|
|» ref_offices|body|array[string]| yes |Arrays of references to offices|

> Response Examples

> Success

```json
{
  "message": "enable notifications for offices applied successfully"
}
```

$${\color{red}Api<4> \space \color{blue}Delete  \space Office}$$

DELETE /api/offices/<str:ref_office>/delete

This API endpoint allows an authenticated manager to delete an office 

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|»ref_office|query|string| yes |the reference of an office|
|Cookie|header|string| yes |require the user to be authenticated|

> Response Examples

> Success

```json
{
  "message": "office was deleted successfully"
}
```


$${\color{red}Api<5> \space \color{blue}Delete  \space Agent \space From \space Office}$$

DELETE /api/offices/<str:ref_office>/agents/<int:agent_id>/delete

This API endpoint allows an authenticated manager to delete an Agent From Office 

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|»ref_office|query|string| yes |the reference of an office|
|»agent_id|query|int| yes |the id of an Agent user|
|Cookie|header|string| yes |require the user to be authenticated|

> Response Examples

> Success

```json
{
  "message": "Agent deleted successfully"
}
```
