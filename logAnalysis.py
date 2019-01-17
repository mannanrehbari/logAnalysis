#!/usr/bin/env python
import psycopg2

def db_connection(dbname):
    """ Connects to db, returns db, cursor """
    try:
        conn = psycopg2.connect(dbname)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    curs = conn.cursor()

    return conn, curs

def execute_query(query, curs):
    """ Executes the query provided in the parameter """
    curs.execute(query)
    results = curs.fetchall()
    return results

def top_articles(curs, text_file):
    """ calls execute query for finding top articles """
    query1 = """SELECT A.title, L.views FROM articles A
                INNER JOIN (SELECT path,
                COUNT(*) AS views FROM log
                GROUP BY path) L ON L.path ='/article/' || A.slug
                ORDER BY views DESC
                LIMIT 3;"""
    results = execute_query(query1, curs)

    text_file.write("\n********** Top Articles **********\n");
    for row in results:
        text_file.write("{} -- {} views\n".format(row[0],row[1]))



def top_authors(curs, text_file):
    """ Finds the authors with most views on articles"""
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
    text_file.write("\n********** Top Authors **********\n");
    results = execute_query(query2, curs)
    for row in results:
        text_file.write("{} -- {} views\n".format(row[0], row[1]))

def over_1_pc(curs, text_file):
    """ Finds days where the error logs are over 1% of total logs """
    query3 = """select
                round((100.00 * error_status.count/all_status.count)::numeric,1)
                as fracT, error_status.time
                from error_status join all_status
                on error_status.time = all_status.time
                where round(100*error_status.count/all_status.count) > 1;"""
    text_file.write("\n********** Over 1% errors on **********\n");
    results = execute_query(query3, curs)
    for row in results:
        text_file.write("{} -- {} % errors\n".format(row[1], row[0]))

    text_file.write("\n");



if __name__ == "__main__":
    """ main function calls query functions  """
    dbname = "dbname=news"
    text_file = open("Output.txt", "w+")
    conn, curs = db_connection(dbname)

    print("Connection established! Please wait till processing is complete...")

    top_articles(curs, text_file)
    top_authors(curs, text_file)
    over_1_pc(curs, text_file)

    print("Done! The results were saved in Output.txt")

    text_file.close()
    curs.close()
    conn.close()
