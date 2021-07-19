"""The Database class
"""
import psycopg2


class database:
    def __init__(self, dbname, username, password):
        """Constructor
        Parameters:
            - dbname: string
                the name of the database
            - username: string
                the name of the user
            - password: string
                the password for the aformentioned user
        Returns:
            -database object
        """
        self.to_say = True
        try:
            self.conn = psycopg2.connect(
                f"""dbname='{dbname}'
                    user='{username}'
                    password='{password}'
                """
            )
            self.conn.autocommit = True
        except Exception:
            raise Exception("Unable to connect to database")
            print("Unable to connect to database")
        cur = self.conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        self.__print(f"You are connected to - {record}")
        cur.close()
        return

    def __print(self, string, **args):
        """TThe custom print thing
        """
        if self.to_say:
            print(string)

    def setup(self, verbose=True):
        """Sets up the database with the pre-decided UML
        at [link]
        Parameters:
            - verbose: boolean
                decided if you want message for
                everything thats gets done
        Returns:
            nothing
        """
        self.to_say = verbose
        cur = self.conn.cursor()
        self.__print("Creating Author table...")
        cur.execute(
            """CREATE TABLE author (
                id                  SERIAL PRIMARY KEY,
                name                VARCHAR(255) NOT NULL,
                citation_count      INT,
                self_citation_count INT
                );
            """
        )
        self.__print("Author table created")

        # publication table
        self.__print("Creating Publication table...")
        cur.execute(
            """CREATE TABLE publication (
                title            VARCHAR(1000),
                key              VARCHAR(255) NOT NULL,
                publish_year     INT,
                publication_type VARCHAR(255)
                );
            """
        )
        self.__print("Publication table created")

        # authorship table
        self.__print("Creating Authorship Table...")
        cur.execute(
            """CREATE TABLE Authorship (
                author_id        INT,
                publication_key  VARCHAR(255)
                );
            """
        )
        self.__print("Authorship table created")

        # citation table
        self.__print("Creating citations table...")
        cur.execute(
            """CREATE TABLE citation (
                citee_publication_key VARCHAR(255) NOT NULL,
                citer_publication_key VARCHAR(255) NOT NULL
                );
            """
        )
        self.__print("Citation table created")
        # Note: foreign aren't set because order of entry is not defined
        cur.close()
        return

    def addCitation(self, citeeKey, citerKey):
        """Add the citation to the database on the cursor cur
        Parameters:
            - citeeKey: String
                key of the publication which is BEING cited
            - citerKey: String
                key of the publication which is citing
        Returns:
            nothing
        """
        cur = self.conn.cursor()
        cur.execute(
            f"""INSERT INTO
            citation (citee_publication_key, citer_publication_key)
            VALUES ('{citeeKey}','{citerKey}');"""
        )
        cur.close()
        return

    def addAuthorNAuthorship(self, authorName, publicationKey):
        """Adds author into the database if dosen't already exist and returns
        the id of the author
        Parameters:
            - auhorName: string
                name of the author
            - publicationKey: string
                publication key
        Returns:
            nothing
        """
        cur = self.conn.cursor()
        # adding author is dosen't already exist
        cur.execute(
            f"""DO $$
            BEGIN
            IF NOT EXISTS(SELECT * FROM author WHERE name='{authorName}')
            THEN
                INSERT INTO
                author (name, citation_count, self_citation_count)
                VALUES('{authorName}', 0, 0);
            END IF;
            END $$
            """
        )

        # getting the id of tha author
        cur.execute(
            f"""SELECT * FROM author WHERE name='{authorName}';
                """
        )
        authorId = cur.fetchone()[0]
        # adding authorship
        cur.execute(
            f"""INSERT INTO
                authorship (author_id ,publication_key)
                VALUES ({authorId}, '{publicationKey}');
                """
        )
        cur.close()
        return

    def addPublication(
        self, publicationTitle, publicationKey, publicationYear, publicationType
    ):
        """Adds publication into the database
        Parameters:
            - publicationTitle: string
                the title of the publication
            - publicationKey: string
                the key of the publication (it's one of the attributes)
            - publicationYear: string|int
                the year of the publication
            - publicationType: string
                the type of the publication (it's one of the attributes)
        """
        cur = self.conn.cursor()
        cur.execute(
            f"""INSERT INTO
                publication (
                    title,
                    key,
                    publish_year,
                    publication_type
                )
                VALUES (
                    '{publicationTitle}',
                    '{publicationKey}',
                    {publicationYear},
                    '{publicationType}'
                )
                """
        )
        cur.close()
        return

    def close(self):
        self.conn.commit()
        self.conn.close()
        return
