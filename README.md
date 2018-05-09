#Logs Analysis Project
Project submitted for Back-End Development module of IPND. Klim MacKenzie 07 May 2018. Calls are made using psycopg2 in Python 2.7 script news_reports.py on the news database running Postgresql.

##Set up
The following views were created for this submission:

####Question 1:

`CREATE VIEW article_views AS
    SELECT path,count(*) AS num
    FROM log
    GROUP BY path
    ORDER BY num DESC;`

Counts number of distinct entries in table log for each article. Inputs are column **path** which is then counted and grouped by **path**, then sorted by count in descending order.

`CREATE VIEW article_dir AS
    SELECT title, CONCAT('/article/', slug) AS dir
    FROM articles;`

Takes article **title** and **slug** columns from article table, concatenates _/article/_ before the **slug** to get a string that is equivalent to **path** (in article_views View above).

####Question 2:

`CREATE VIEW authors_dir AS
    SELECT name, CONCAT('/article/', slug) AS dir
    FROM articles JOIN authors
    ON articles.author = authors.id;`

Takes article **slug** (concatenated with _/article/_ as for **article_dir** view above) and joins author **name** to the slug via author column in articles table which corresponds to **id** in authors table.

####Question 3:

`CREATE VIEW status_log as SELECT date(time), ROUND(
100.0 * (SUM(CASE WHEN status = '404 NOT FOUND' THEN 1
ELSE 0 END)::decimal / count(status)), 1) as percent_error
FROM log
GROUP BY date(time);`

Counts number of entries in **status** column within table log that are *'404 NOT FOUND'*, divides by total number of entries in **status** and multiplies up by 100 to get a percentage fraction. Percentage is then grouped by date which is extracted from **time** in log table.

##Usage

####Question 1
Function top_articles uses standard psycopg2 interface to query news database with the below query:

`SELECT title, num FROM article_dir JOIN article_views
        ON article_dir.dir = article_views.path LIMIT 3;`

Query uses views article_views and article_dir (defined above) and joins **dir** from article_dir onto **path** in article_views and reports top 3 articles in terms of view count.

####Question 2
Function top_authors uses standard psycopg2 interface to query news database with the below query:

`SELECT name, count(*) AS num FROM log JOIN authors_dir ON
         log.path = authors_dir.dir GROUP BY name ORDER BY num DESC
         LIMIT 3;`

Query uses view authors_dir (defined above) and joins **dir** from authors_dir onto **path** in log, groups by author **name** and reports top 3 authors in terms of view count.

####Question 3
Function error_log uses standard psycopg2 interface to query news database. Database query is formed as a concatenation of error margin (1% for the assignment) as **ERROR_MARGIN** with the below:

`"SELECT * FROM status_log where percent_error >" + str(ERROR_MARGIN)`

Query uses view status_log (defined above) and reports days where error percentage exceeds that defined in **ERROR_MARGIN** (given as 1%).


####Reporting
Answers to three questions are printed using print statements and concatenating the different parts of each string, spread out with necessary formatting.

##Example report:

####1. What are the most popular articles of all time?

-  'Candidate is jerk, alleges rival':  338647 views
-  'Bears love berries, alleges bear':  253801 views
-  'Bad things gone, say good people':  170098 views

####2. Who are the most popular authors of all time?

-  Ursula La Multa:  507594 views
-  Rudolf von Treppenwitz:  423457 views
-  Anonymous Contributor:  170098 views

####3. On which days did more than 1% of requests lead to errors?

-  2016-07-17 --  2.3 %
