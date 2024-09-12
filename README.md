# Kindergarten application

This project is designed to help employees to have a better insight into the arrangement of children by groups and their activities.
It is also designed to have insight into parents' data.

## Introduction

The Kindergarten is a Python-based application created to manage operations in one kindergarten. The project is developed using PyCharm environment.

## Features

* Employee management: Read, update, create and delete employee.
* Kids management: Read, update, create and delete kids from groups.
* Groups management: Read group, create group, update employee in a group, update kids in a group and delete group.
* Parent management: Read, update, create and delete parents.

## Technologies applied

* Python 3.9
* FastAPI 0.111.1

## Setup Instructions

To get started with the Kindergarten application, follow these steps: 
1. Clone the Repository: 

`https://github.com/aleksicjelena1/fastapi_test.git`

2. Navigate to the Project Directory:

`cd fastapi_test`

3. Create and Activate a Virtual Environment

`python -m venv venv`

`source venv/bin/activate`

Note: If you have problems with these commands, please check your Python version, install any other version that
is required and then type these commands.

4. Install Dependencies

`pip install -r requirements.txt`

5. Run the Applications

`uvicorn app.main:app --reload`

6. Open your browser and navigate to http://127.0.0.1:8000/docs to view the application.

## Conclusion

Good luck, have fun coding!