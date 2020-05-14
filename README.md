# Python with Flask, SQLAlchemy and APIs Design Course
Training course for GotIt Internship, summer 2020

## Installation
`git clone` this repository.

You can create a virtual environment(virtualenv), running on Python3. 

`python3 -m virtualenv venv`

`source venv/bin/activate`

And deactivate when you are done: `deactivate`

Then install required libraries.

`pip install -r requirements.txt`

You should modify the `SECRET` variable in .env file to your secret.

Run the server: `python -m src.app` 

## Description
The project is a web api server that contains information of stores and items in 
each store. It is also accompanied with an authorization system for authenticated users.

## Example Request
You can test the APIs with Postman. Available routes are in `app.py`

Example:

`POST http://localhost:5000/register`

`body:
{"username": "abc", "password": "123"}
`

## License 
[MIT](https://github.com/xoxwaw/flask_api_course/blob/master/LICENSE)
