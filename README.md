# selfcitation

Finding Self Citations 

# Setup

### Database

Before running this let's create the database and user, do not put the curly brackets in the following

```
CREATE DATABASE {postgres_dbname};
CREATE USER {postgres_username} WITH PASSWORD {postgres_password};
GRANT ALL ON DATABASE {postgres_dbname} TO {postgres_username};
```
### Variables

Make a `variables.py` in `./src/`
make the following variables in then

- `folder` : The directory where the xml file precides
- `fileName` : The name of the xml file
- `postgres_dbname` : the name of the database which you used in the last section
- `postgres_username` : the user for the databse which you used in the last section
- `postgres_password` :  the password of the use which you used in the last section
- `discord_token` : THe discord token
- `discord_channel_id` : The discord channel id

# UML of the postgres database

![the uml](./uml.png)


# expected time things take

- Loading the `XML` into memory: `52 s`
- Types of tags: `35`
- One itteration over the complete xml with only reading the tag names: `20 s`
- all tags: 
	- 'dblp'
	- 'article'
	- 'author'
	- 'title'
	- 'journal'
	- 'year'
	- 'ee'
	- 'book'
	- 'publisher'
	- 'isbn'
	- 'volume'
	- 'month'
	- 'url'
	- 'note'
	- 'cdrom'
	- 'sup'
	- 'editor'
	- 'sub'
	- 'proceedings'
	- 'booktitle'
	- 'series'
	- 'inproceedings'
	- 'crossref'
	- 'www'
	- 'pages'
	- 'mastersthesis'
	- 'school'
	- 'incollection'
	- 'i'
	- 'cite'
	- 'number'
	- 'tt'
	- 'phdthesis'
	- 'chapter'
	- 'address'
