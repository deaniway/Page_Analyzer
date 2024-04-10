### Hexlet tests and linter status:
[![Actions Status](https://github.com/deaniway/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/deaniway/python-project-83/actions)


# Page analyzer
## Follow the [link to view ](https://python-project-83-1-gyiq.onrender.com) my project :D


This is a site that analyzes specified pages for SEO suitability, similar to [PageSpeed](https://pagespeed.web.dev/)


#### Minimum Requirements:
 - [x] Python 
 - [x] Poetry
 - [x] Flask
 - [x] PostgreSQL
 - [x] Docker


Page Analyzer is a full-fledged application based on the Flask framework. 
Here the basic principles of building modern websites on MVC architecture are worked out: working with routing, 
request handlers and a template engine, interaction with the database.


### This is  use next tools:

|      Tools      | Version |
|:---------------:|:-------:|
|     python      |  3.11   |
|     poetry      |  1.6.1  |
|    gunicorn     | 21.2.0  |
|     flake8      |  6.1.0  |
|  python-dotenv  |  1.0.1  |
| psycopg2-binary |  2.9.9  |
|   validators    | 0.23.2  |
|    requests     | 2.31.0  |
|       bs4       |  0.0.2  |
|     Docker      | 23.0.3  |
|   PostgreSQL    |  16.3   |





### To get started, you need to perform the following operations:

| Step |                                   Instruction                                   |
|:----:|:-------------------------------------------------------------------------------:|
|  1   | Clone he repository to your PC:<br/>`github.com/deaniway/python-project-83.git` |
|  2   |                   Go to repository<br/>`cd python-project-83`                   |
|  3   |         Installing the application on your computer<br/>`make install`          | 
|  4   |                Run the command to create tables<br/>`make build`                | 
|  5   |                To start the Flask server, use the<br/>`make dev`                |





### *You must have:* 

- [Poetry](https://python-poetry.org) 

- [Flask](https://flask.palletsprojects.com/en/3.0.x/) 

- [PostgreSQL](https://www.postgresql.org/) 

- [Docker](https://www.docker.com/) 


## How to deploy a database?

| Step |                        Instruction                         |
|:----:|:----------------------------------------------------------:|
|  1   |      Install all necessary libraries and applications      |
|  2   | Customize the `.env` file by passing your key to variables |
|  3   |  Deploying a docker database container<br/>`make dev-db`   | 
|  4   |    To connect to the db use command<br/>`make enter-db`    | 

*P.S.* *If for some reason it was not possible to deploy the container with the database, use this command:*

```
docker run -d \
    --name dev_page_analyzer \
    -e POSTGRES_USER=pguser \
    -e POSTGRES_PASSWORD=pgpass \
    -e POSTGRES_DB=pgdb \
    -p 5432:5432 \
    postgres:latest
```
*To connect db we use this:*
```
docker exec -it dev_page_analyzer psql -U pguser -d pgdb psql
```



### Contributing

How can I help develop a project? Submit a pull request :)




## In the plans
- [x] Submit README
- [ ] Add Сelery to make the application work asynchronously
- [ ] Add functionality to the project



## Project team
- Denis Davydov (https://t.me/deway0) — Python developer
