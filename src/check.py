import psycopg2


conn = psycopg2.connect(
    """dbname='dblp'
        user='abhishek'
        password='f6hgKDisr7'
        """
)
cursor = conn.cursor()
cursor.execute(
    """SELECT count(*) from author
        """
)
print(cursor.fetchall())
