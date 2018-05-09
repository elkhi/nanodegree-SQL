#!/usr/bin/env python2.7

import psycopg2

DBNAME = "news"
questions = ["1. What are the most popular articles of all time?",
             "2. Who are the most popular authors of all time?",
             "3. On which days did more than 1% of requests lead to errors?"]
ERROR_MARGIN = 1 #in percent, margin for reporting

def top_articles():
    '''Database query for question 1'''
    conn = psycopg2.connect(database=DBNAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT title, num FROM article_dir JOIN article_views \
        ON article_dir.dir = article_views.path LIMIT 3;")
    article_views = cur.fetchall()
    conn.close()
    return article_views


def top_authors():
    '''Database query for question 2'''
    conn = psycopg2.connect(database = DBNAME)
    cur = conn.cursor()
    cur.execute(
         "SELECT name, count(*) AS num FROM log JOIN authors_dir ON \
         log.path = authors_dir.dir GROUP BY name ORDER BY num DESC \
         LIMIT 3;")
    author_views = cur.fetchall()
    conn.close()
    return author_views


def error_log():
    '''Database query for question 3'''
    conn = psycopg2.connect(database = DBNAME)
    cur = conn.cursor()
    error_string = "SELECT * FROM status_log where percent_error >" + str(ERROR_MARGIN)
    cur.execute(error_string)
    error_days = cur.fetchall()
    conn.close()
    return error_days


article_views = top_articles()
author_views = top_authors()
error_days = error_log()


print "\n", questions[0], "\n"
for title, views in article_views:
    print "-  '" + title + "': ", views, "views"

print "\n", questions[1], "\n"
for author, views in author_views:
    print "-  " + author + ": ", views, "views"

print "\n", questions[2], "\n"
for date, percent_error in error_days:
    print "- ", date, "-- ", percent_error, "% \n"