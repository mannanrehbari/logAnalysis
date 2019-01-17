#!/usr/bin/env python
import psycopg2


# function for log analysis will be called in main
def logAn():
    # connection object: if the db 'news exists' program will proceed
    try:
        conn = psycopg2.connect("dbname=news")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        quit()
    # cursor object: can be used to perform queries
    curs = conn.cursor()

    # textfile for output
    text_file = open("Output.txt", "w")

    # first query: 3 most popular articles
    query1 = """SELECT A.title, L.views FROM articles A
                INNER JOIN (SELECT path,
                COUNT(*) AS views FROM log
                GROUP BY path) L ON L.path ='/article/' || A.slug
                ORDER BY views DESC
                LIMIT 3;"""

    # execute query1  and retrieve all results
    curs.execute(query1)
    record1 = curs.fetchall()

    text_file.write("--------   Query1   ---------\n")
    for title, views in record1:
        text_file.write("{} -- {} views\n".format(title,views))

    # second query: author views descending
    query2 = """
        SELECT au.name AS authName, count(*) AS views
        FROM articles a
        INNER JOIN log l
        ON l.path = '/article/' || a.slug
        INNER JOIN authors AS au
        ON au.id = a.author
        GROUP BY authName
        ORDER BY views DESC;
        """


    curs.execute(query2)
    record2 = curs.fetchall()

    text_file.write("\n--------   Query2  ---------\n")
    for row in record2:
        text_file.write("{} -- {} views\n".format(row[0], row[1]))

    # third query: percent errors
    # the assumption is that views are already created

    query3 = """select
                round((100.00 * error_status.count/all_status.count)::numeric,2)
                as fracT, error_status.time
                from error_status join all_status
                on error_status.time = all_status.time
                where round(100*error_status.count/all_status.count) > 1;"""
    curs.execute(query3)
    record3 = curs.fetchall()
    text_file.write("\n--------    Query3   ---------\n")
    for row in record3:
        text_file.write("{} -- {} % errors\n".format(row[1], row[0]))

    print("Program results saved in Output.txt")

    # closing the text file, open cursor, and connection
    text_file.close()
    curs.close()
    conn.close()


if __name__ == "__main__":
    # function call: does everything when the program is run
    logAn()
