# Log Analysis

Log Analysis is a small project that reflects basic understanding of Python DB API and PGSQL statements. It is built on Vagrant VM with Python and PostgreSQL.

## Dependencies
This project assumes that Python 2.7.12 and PGSQL (PostgreSQL 9.5.14) are installed on vagrant VM machine with Ubuntu 16.04.5 LTS.

## Usage
To load the database into psql type the following command:
`` psql -d news -f newsdata.sql ``
This command will load data from **newsdata.sql** into **news** file, the latter can be run using psql.

This program is dependent on two views that need to be created. To create views, run:
`psql news`  on vagrant in the logAnalysis directory. Once the psql command-line is ready, create the following views.

The first view:

`CREATE VIEW error_status AS SELECT time::DATE, COUNT(*) FROM log WHERE status = '404 NOT FOUND' GROUP BY time::DATE;`

The second view:

`CREATE VIEW all_status AS SELECT time::DATE, COUNT(*) FROM log GROUP BY time::DATE;`

After creating views, exit out of psql command-line by pressing CTRL + D. Once back in the vagrant terminal, type the following to run the program: `python logAnalysis.py`

## Output

The program takes a few seconds to load the data into **Output.txt** file. This can be viewed in any text editor of choice or by simply typing `cat Output.txt` in the terminal.   
## License
See this [License](./LICENSE.txt).
