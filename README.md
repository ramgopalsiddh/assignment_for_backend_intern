# FastAPI Expense Tracker

This is a simple expense tracking API built with FastAPI. The API allows users to create and manage expenses, split them among participants, and retrieve expense data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)

## Features

- Create expenses with a description and amount.
- Split expenses among multiple participants.
- Simple RESTful API for easy integration.

## Technologies Used

- **Python**: Version 3.7+
- **FastAPI**: Modern, fast web framework for building APIs.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) system.
- **Uvicorn**: ASGI server for serving the FastAPI application.

## Installation

### Prerequisites

- Ensure you have Python 3.7 or higher installed on your machine.

### Step 1: Get the code 


### Step 2: Create a Virtual Environment
`python -m venv venv`

### Step 3: Activate the Virtual Environment
 - Linux:

`source venv/bin/activate`

### Step 4: Install Dependencies

`pip install -r requirements.txt`


### Step 1: Run the Application
- Start the FastAPI application with Uvicorn:

`uvicorn app.main:app --reload`

### Step 2: Access the API
 - Open your browser and go to http://127.0.0.1:8000


---

# API Endpoints

### 1. Get User by ID
- Endpoint: /users/{id}
- Method: GET
- Request:

    `curl -X GET "http://127.0.0.1:8000/users/1"`

- Response Example:

    `{
    "id": 1,
    "name": "John",
    "email": "john@example.com"
    }`

### 2. Get Expenses by User ID
- Endpoint: /expenses/user/{user_id}
- Method: GET
- Request:

    `curl -X GET "http://127.0.0.1:8000/expenses/user/1"`
- Response Example:

    `[
    {"id": 1, "created_by": 1, "amount": 3000.0, "description": "Dinner"},
    {"id": 2, "created_by": 1, "amount": 3000.0, "description": "Dinner"},
    ...
    ]`

### 3. Get Balance Sheet
- Endpoint: /expenses/balance-sheet/
- Method: GET
- Request:

    `curl -X GET "http://127.0.0.1:8000/expenses/balance-sheet/"`

- Response Example:
    `{
    "total_expenses": 24000.0
    }`

### 4. Create Expense
- Endpoint: /expenses/
- Method: POST
- Request:

    `curl -X POST "http://127.0.0.1:8000/expenses/" -H "Content-Type: application/json" -d '{
    "amount": 3000,
    "description": "Dinner",
    "split_method": "equal",
    "participants": [1, 2, 3, 4]
    }'`

- Response Example:

    `{
    "id": 9,
    "description": "Dinner",
    "amount": 3000.0,
    "created_by": 1,
    "splits": [
        {"user_id": 1, "amount": 750.0},
        {"user_id": 2, "amount": 750.0},
        {"user_id": 3, "amount": 750.0},
        {"user_id": 4, "amount": 750.0}
    ]
    }`

### 5. Create User
- Endpoint: /users/
- Method: POST
- Request:

    `curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{
    "email": "user5@example.com",
    "name": "User Five",
    "mobile": "1734765890"
    }'`

- Response Example:
    `{
    "id": 5,
    "name": "User Five",
    "email": "user5@example.com"
    }`

