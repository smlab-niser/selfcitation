"""Indexing table for faster queries, they have been optimized according to
the most common queries and so on.
DO NOT EDIT IF YOU DON'T KNOW WHAT YOU ARE DOING.
"""
import psycopg2
import threading


from variables import postgres_username, postgres_dbname, postgres_password


def main():
    def connect_to_db():
        """returns a psycopg2 connection
        """
        try:
            conn = psycopg2.connect(
                f"""dbname='{postgres_dbname}'
                    user='{postgres_username}'
                    password='{postgres_password}'
                """
            )
            conn.autocommit = True
            return conn
        except Exception:
            print("Unable to connect to the database")
            raise Exception("Unable to connect to database")

    def index_authorship_table():
        print("started indexing authorship table...")
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """CREATE INDEX publication_key_author_id_authorship_idx
            ON authorship (author_id, publication_key);
            """
        )
        cur.close()
        conn.close()
        print("Indexing of authorship table is complete")

    def index_author_table():
        print("started indexing author table...")
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """CREATE INDEX id_idx
            ON author (id);
            """
        )
        cur.close()
        conn.close()
        print("Indexing of author table is complete")

    def index_publication_table():
        print("started indexing publication table...")
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """CREATE INDEX key_publish_year_idx
            ON publication (publish_year, key);
            """
        )
        cur.close()
        conn.close()
        print("Indexing of publication table is complete")

    def index_citation_table():
        print("started indexing citation table...")
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """CREATE INDEX citee_idx
            ON citation (citee_publication_key);
            """
        )
        cur.close()
        conn.close()
        print("Indexing of citation table is complete")

    # creating threads
    citation_thread = threading.Thread(target=index_citation_table)
    publication_thread = threading.Thread(target=index_publication_table)
    author_thread = threading.Thread(target=index_author_table)
    authorship_thread = threading.Thread(target=index_authorship_table)

    # starting threads
    citation_thread.start()
    publication_thread.start()
    author_thread.start()
    authorship_thread.start()

    # waiting for threads to finish
    citation_thread.join()
    publication_thread.join()
    author_thread.join()
    authorship_thread.join()

    print("Done")


if __name__ == "__main__":
    main()
