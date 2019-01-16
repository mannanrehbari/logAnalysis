# importing necessary libraries
import psycopg2


# function for log analysis will be called in main
def logAn():
    # connection object: if the db 'news exists' program will proceed
    try:
        conn = psycopg2.connect("dbname=news")
    except connectError:
        print("There was an error in connecting to database")
        quit()
    # cursor object: can be used to perform queries
    curs = conn.cursor()

    # textfile for output
    text_file = open("Output.txt", "w")

    # first query: 3 most popular articles
    query1 = """select A.title, L.views from articles A
                inner join (select substring(path from 10) as newT,
                count(*) as views from log
                where path like '/article/%'
                group by path order by views desc) L on L.newT = A.slug
                limit 3;"""

    # execute query1  and retrieve all results
    curs.execute(query1)
    record1 = curs.fetchall()

    text_file.write("--------   Query1   ---------\n")
    for row in record1:
        text_file.write("{} -- {} views\n".format(row[0], row[1]))

    # second query: author views descending
    query2 = """select authName, sum(authViews) as fViews
                from (select A.author as authID, Au.name as authName,
                A.title, L.views as authViews from articles A
                inner join (select substring(path from 10) as newT,
                count(*) as views from log where path like '/article/%'
                group by path order by views desc) L on L.newT = A.slug
                inner join authors as Au on Au.id = A.author) as tempQ
                group by authname order by fViews desc ;"""

    curs.execute(query2)
    record2 = curs.fetchall()

    text_file.write("\n--------   Query2  ---------\n")
    for row in record2:
        text_file.write("{} -- {} views\n".format(row[0], row[1]))

    # third query: percent errors
    # the assumption is that views are already created

    query3 = """select
                round((100 * error_status.count/all_status.count)::numeric,2)
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
