# Python with Flask, SQLAlchemy and APIs Design Course
Training course for GotIt Internship, summer 2020

## Installation
`git clone` this repository.

You can create a virtual environment(virtualenv), running on Python3. 

`virtualenv .env `

`source .env/bin/activate`

And deactivate when you are done: `deactivate`

Then install required libraries.

`pip3 install -r requirements.txt`

It is also imperative that you set your own secret key for JWT by creating a 
`config.py`, that has this content:

`
SECRET = 'YOUR SECRET'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
`

Run the server: `python3 -m src.app` 

## Description
The project is a web api server that contains information of stores and items in 
each store. It is also accompanied with an authorization system for authenticated users.

## Example Request
You can test it in Postman with some of the sample requests by importing 
`flask_course.postman_collection.json` to your POSTMAN app.




## License 
[MIT](https://github.com/xoxwaw/flask_api_course/blob/master/LICENSE)
