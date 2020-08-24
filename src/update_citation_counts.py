"""
Come to this once all the data from the xml has been moved into the database

Updates and calculates the citation_count and self_citation_count
in the author table

It is recommended to run index.py before running this.
"""
import multiprocessing as mp
import time

import psycopg2
from variables import (
    postgres_dbname,
    postgres_username,
    postgres_password,
    number_of_threads,
)


def main():
    start = time.time()
    conn = psycopg2.connect(
        f"""dbname='{postgres_dbname}'
            user='{postgres_username}'
            password='{postgres_password}'
        """
    )
    cur = conn.cursor()
    cur.execute("""SELECT count(*) FROM author;""")
    author_count = cur.fetchone()[0]
    print(f"We are dealing with {author_count} authors")

    per_thread_authors = int(author_count / number_of_threads)
    pool = mp.Pool(processes=number_of_threads)
    pool.map(send_query_for, range(1, author_count, per_thread_authors))

    cur.close()
    conn.close()
    end = time.time()
    print(f"DONE in: {end - start}")


def send_query_for(from_id):
    from variables import number_of_threads

    conn_in = psycopg2.connect(
        f"""dbname='{postgres_dbname}'
            user='{postgres_username}'
            password='{postgres_password}'
        """
    )
    conn_in.autocommit = True
    cur_in = conn_in.cursor()

    cur_in.execute("""SELECT count(*) FROM author;""")
    author_count = cur_in.fetchone()[0]
    per_thread_authors = int(author_count / number_of_threads)

    if from_id + per_thread_authors > author_count + 1:
        to_id = author_count + 1
    else:
        to_id = from_id + per_thread_authors

    for i in range(from_id, to_id):
        cur_in.execute(
            f"""WITH pubs AS (
                  SELECT publication_key
                  FROM authorship
                  WHERE author_id = {i}
                ), citer_keys AS (
                  SELECT citer_publication_key
                  FROM citation, pubs
                  WHERE citation.citee_publication_key =
                      pubs.publication_key
                ), self_citation_count AS (
                  SELECT COUNT(1)
                  FROM authorship, citer_keys
                  WHERE authorship.publication_key =
                      citer_keys.citer_publication_key
                    AND authorship.author_id = {i}
                ), citation_count AS (
                  SELECT Count(1)
                  FROM citer_keys
                )
                UPDATE author
                SET citation_count = citation_count.count,
                    self_citation_count = self_citation_count.count
                FROM citation_count, self_citation_count
                WHERE author.id = {i};
            """
        )
    cur_in.close()
    conn_in.close()
    print(f"done with {from_id}-{to_id}")
    return


if __name__ == "__main__":
    main()
