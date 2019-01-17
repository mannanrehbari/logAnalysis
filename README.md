# Log Analysis

Log Analysis script uses psycopg2 to query a mock PostgreSQL database for a fictional news website.
There are three tables in the **news** database: __articles__, __authors__, and __logs__. The structure
of each table can be accessed in psql using ``\d example_table`` command. __Articles__ has the following columns: author, title, slug, lead, body, time, and id.  __Authors__ has following columns: name, bio, and id. __log__ has the following columns: path, ip, method, status, time, and id. The logAnalysis.py script generates results for top articles, top authors, and date with highest '404 NOT FOUND' errors. In the same order, and saves it in output. The SQL queries can be seen inside __logAnalysis.py__ file.


## Dependencies
This project assumes that Python 2.7.12 and PostgreSQL 9.5.14 . This script was run on Vagrant v2.2.2 software (which runs on VirtualBox VM) installed on Windows 10 64bit with Ubuntu 16.04.5 LTS. Vagrant configuration file can be downloaded from this repository, and the following link can be used for downloading Vagrant:
[Vagrant](https://www.vagrantup.com/downloads.html)

## Usage
The mock news data can be downloaded from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). The Vagrantfile generates the __news__ database, but can also be generated manually by using the command ``psql -d news -f newsdata.sql ``.

This program is dependent on two views that need to be created. To create views, run:
`psql news`  on vagrant in the logAnalysis directory. Once the psql command-line is ready, create the following views.

The first view:

```sql
CREATE VIEW error_status AS
SELECT time::DATE, COUNT(*)
FROM log WHERE status = '404 NOT FOUND'
GROUP BY time::DATE;
```

The second view:

```sql
CREATE VIEW all_status AS
SELECT time::DATE, COUNT(*)
FROM log
GROUP BY time::DATE;
```

After creating views, exit out of psql command-line by pressing CTRL + D. Once back in the vagrant terminal, type the following to run the program: `python logAnalysis.py`

## Output

The program takes a few seconds to load the data into **Output.txt** file. This can be viewed in any text editor of choice or by simply typing `cat Output.txt` in the terminal.   
## License
See this [License](./LICENSE.txt).
