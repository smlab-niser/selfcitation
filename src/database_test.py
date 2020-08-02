"""Test module for database functions
before running this run the following to create the database and users
```
CREATE DATABASE {postgres_dbname};
CREATE USER {postgres_username} WITH PASSWORD '{postgres_password}';
GRANT ALL ON DATABASE {postgres_dbname} TO {postgres_username};
```

when done with the test, reset the database by deleting it
and creating one again
```
DROP DATABASE {postgres_dbname};
CREATE DATABASE {postgres_dbname};
GRANT ALL ON DATABASE {postgres_dbname} TO {postgres_username};
```
"""
from database import database
from variables import (
    postgres_username,
    postgres_password,
    postgres_dbname,
)

wrong = "❌"
correct = "👌"

try:
    db = database(postgres_dbname, postgres_username, postgres_password)
    print(correct + " connection to database successful")
except Exception as error:
    print(wrong + " cound not connect to the database")
    print(error)

db.setup(False)
print(correct + " database setup didn't ring any alarms")

try:
    db.addCitation("citekey", "citerKey")
    print(correct + " adding citation didn't raise any alarms")
except Exception as error:
    print(wrong + " adding citation didn't go as planned")
    print(error)
    raise Exception

try:
    db.addPublication(
        "Some paper I will write some day",
        "/key/of/publication",
        2001,
        "sometype of paper",
    )
    print(correct + " adding publication didn't raise any alarms")
except Exception as error:
    print(wrong + " adding publication didn't go as planned")
    print(error)
    raise Exception

try:
    db.addAuthorNAuthorship("Abhishek Anil Deshmukh", "/key/of/publication")
    print(correct + " adding Author didn't raise any alarms")
except Exception as error:
    print(wrong + " adding Author didn't go as planned")
    print(error)

try:
    db.close()
    print(correct + " saving and closing didn't raise any alarms")
except Exception as error:
    print(wrong + " saving and closing the database didn;t go as planned")
    print(error)
