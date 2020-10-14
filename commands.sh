#!/usr/bin/env bash

echo '.separator ","
.import data/category.csv api_category' | sqlite3 db.sqlite3

echo '.separator ","
.import "data/comments.csv" api_comments' | sqlite3 db.sqlite3

echo '.separator ","
.import "data/genre.csv" api_genre' | sqlite3 db.sqlite3

echo '.separator ","
.import "data/genre_title.csv" api_genre_title' | sqlite3 db.sqlite3

echo '.separator ","
.import "data/review.csv" api_review' | sqlite3 db.sqlite3

echo '.separator ","
.import "data/titles.csv" api_titles' | sqlite3 db.sqlite3

echo '.separator ","
.import "data/users.csv" api_users' | sqlite3 db.sqlite3

