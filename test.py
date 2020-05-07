import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text)'
cursor.execute(create_table)

users = [
    (1, 'Jose', 'asd'),
    (2, 'Mary', 'asd'),
    (3, 'Kyle', 'asd')
]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.executemany(insert_query, users)

connection.commit()
connection.close()


