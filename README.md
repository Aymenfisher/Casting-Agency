# Full Stack Capstone Project: Casting Agency


## Capstone Project: Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This application simplifies and streamline the processes that are:   

1. Display Actors - Name,Age and gender of the actor.
2. Display Movies - Movie title and release date. 
2. Delete Actors and Movies.
3. Add New Actors and Movies.
4. Modify the existing Actors and Movies .


## Getting started
## Prerequisites and installation
## Backend :
The backend side contains a completed Flask and SQLAlchemy server.

#### Installing Dependencies for the Backend

1. **Python 3** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the postgres database. You'll primarily work in `app.py` and can reference `models.py`. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
While postgres running,create a database named `casting_agency` by running :
```bash
create database casting_agence #for windows users

createdb casting_agency #mac/linux users
```
you can use the `casting_agency.sql` file to restore database datas. From the main folder in terminal run:
```bash
pg_restore -U <your postgres Username> -d casting_agency -v casting_agency.sql
```
### Running Database Migrations
Using Flask-migrate, you can run migrations (ensure that you are working using the virtual environment) using this command:
```bash
python -m flask db migrate -m "<your comment>"
python -m flask db migrate
```

### Running the server

First ensure you are working using your created virtual environment.

before running the server, make sure to set the database URI,DEBUG mode(True or False), and the JWT tokens for every Role as an environment variables, Mac/linux users can use the provided `setup.sh` file. By running:
```bash
source setup.sh
```
For windows users its better to set these environment variables using the commands(Git CMD is recommended):
```bash
set DATABASE_URL=<your database url> 
set DEBUG=<True or False>
set casting_assistant="<casting assistant role JWT token>"
set casting_director="<casting director role JWT roken>"
set executive_producer="<executive producer JWT token>"
```
Tokens are provided in `setup.sh` file.

To run the server locally, execute:

```bash
python app.py
```






## Running tests
The application includes a file named `test_app.py`.
This file contains multiple tests for each endpoint, also tests for each Role(RBAC tests).

JWTs for each role are automatically assigned from the environment variables .(they may expire)

To run the tests ,using your command line , cd to the project main folder, run this command:
```bash
python test_app.py
```
Feel free to to explore the test file.

## API reference :
## Introduction
The Casting Agency API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.
## Getting started
### Base URL
The Casting Agency  api can  be run locally using Flask (see previous sections).

And also is hosted in a base URL:

 `https://casting-agency-aymen.herokuapp.com/`
### Authentication: 
The Casting Agency API requires authentication, it grants authentication for three Roles:
1. Casting Assistant: Can view actors and movies.
2. Casting Manager: All permissions a Casting Assistant has plus:
   - Add or delete an actor from the Database.
   - Modify actors or movies.
3. Executive Producer: All permissions a Casting Director has plus :
   - Add or delete a movie from the Database 

## Error Handling
Errors are returned as JSON objects in the following format:
    Example for '`404: resource not found`' error:

```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return three error types when requests fail (excepting auth errors) :

- 404: resource not found
- 422: Unrocessable 
- 400: Bad request
### Authentication and Authorization Exceptions:
Two Exception types can be raised: 
1. For Authentication : `401:Unauthorized`.
On the following format : Example for bad token format:
```
{
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }
```
2. For Authorization : `403:forbidden`. Example: Permission not found.
```
{
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }
```


## Endpoints :


### GET '/actors'
- General: returns a list of actors object and number of total actors. Each actor object contains the name,age, and gender of the actor.
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample :
```bash 
curl --location --request GET 'https://casting-agency-aymen.herokuapp.com/actors' \
--header 'Authorization: Bearer <token>'
```
Output
```
{
    "actors": [
        {
            "age": 24,
            "gender": "male",
            "name": "aymen"
        },
        {
            "age": 65,
            "gender": "male",
            "name": "tom hanks"
        },
        {
            "age": 47,
            "gender": "male",
            "name": "leaonardo dicaprio"
        },
        {
            "age": 37,
            "gender": "female",
            "name": "scarlett johansson"
        },
        {
            "age": 40,
            "gender": "male",
            "name": "chris evans"
        },
        {
            "age": 46,
            "gender": "female",
            "name": "angelina jolie"
        },
        {
            "age": 55,
            "gender": "female",
            "name": "actor1"
        },
        {
            "age": 70,
            "gender": "male",
            "name": "actor2"
        },
        {
            "age": 80,
            "gender": "male",
            "name": "actor33"
        },
        {
            "age": 66,
            "gender": "female",
            "name": "actor55"
        }
    ],
    "total_actors": 12
}
```
- Sample 2 : page 2
```bash
curl --location --request GET 'https://casting-agency-aymen.herokuapp.com/actors?page=2' \
--header 'Authorization: Bearer <token>'
```
Output
```
{
    "actors": [
        {
            "age": 22,
            "gender": "female",
            "name": "actor6"
        },
        {
            "age": 66,
            "gender": "male",
            "name": "actor9"
        }
    ],
    "total_actors": 12
}
```
### GET '/movies'
- General: returns a list of movies object and number of total actors. Each movie object contains the title and the release date of the movie.
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample :
```bash 
curl --location --request GET 'https://casting-agency-aymen.herokuapp.com/movies' \
--header 'Authorization: Bearer <token>'
```
Output
```
{
    "movies": [
        {
            "release_date": "1994-9-22",
            "title": "the shawshank redemption"
        },
        {
            "release_date": "1972-3-24",
            "title": "the godfather"
        },
        {
            "release_date": "2008-7-18",
            "title": "the dark knight"
        },
        {
            "release_date": "1999-11-11",
            "title": "fight club"
        },
        {
            "release_date": "2010-7-8",
            "title": "inception"
        },
        {
            "release_date": "1997-10-2",
            "title": "movie1"
        },
        {
            "release_date": "1998-03-10",
            "title": "movie2"
        },
        {
            "release_date": "1999-10-4",
            "title": "movie3"
        },
        {
            "release_date": "2000-10-5",
            "title": "movie4"
        },
        {
            "release_date": "1997-10-6",
            "title": "movie5"
        }
    ],
    "total_movies": 17
}
```
- Sample 2 : page 2
```bash
curl --location --request GET 'https://casting-agency-aymen.herokuapp.com/movies?page=2' \
--header 'Authorization: Bearer <token>'
```
Output
```
{
    "movies": [
        {
            "release_date": "1997-10-7",
            "title": "movie6"
        },
        {
            "release_date": "1997-10-8",
            "title": "movie7"
        },
        {
            "release_date": "1997-10-9",
            "title": "movie8"
        },
        {
            "release_date": "1997-10-10",
            "title": "movie9"
        },
        {
            "release_date": "1997-10-11",
            "title": "movie10"
        },
        {
            "release_date": "1997-10-12",
            "title": "movie11"
        },
        {
            "release_date": "1997-10-13",
            "title": "movie12"
        }
    ],
    "total_movies": 17
}
```
### POST '/actors'
- General: Creates a new actor by submitting the actor's, name, age, and the gender :
    - The age must be an integer.
    - The gender must be either 'male' or 'female'.

it returns a list of success value, the name of the created actor, and number of total actors.
- Re-Creating an existing actor is not allowed.
- Sample:
```bash
curl --location --request POST 'https://casting-agency-aymen.herokuapp.com/actors' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"john cena",
    "age":44,
    "gender":"male"
}'
```

Output:
```
{
    "inserted": "john cena",
    "success": true,
    "total_actors": 13
}
```
### POST '/movies'
- General: Creates a new movie by submitting the movie's title and release date :
    - The release date must be in the form: yyyy-mm-dd .

it returns a list of success value, the title of the created movie, and number of total movies.
- Re-Creating an existing actor is not allowed.
- Sample:
```bash
curl --location --request POST 'https://casting-agency-aymen.herokuapp.com/movies' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title":"21 jump street",
    "release_date":"2012-03-16"
}'
```
Output:
```
{
    "inserted": "21 jump street",
    "success": true,
    "total_actors": 18
}
```
### DELETE '/actors/{actor_id}'
- General: Deletes the actor of the given ID if it exists.
It returns the success value, the ID of the deleted actor and the number of the total actors.
- Sample:
```bash
curl --location --request DELETE 'https://casting-agency-aymen.herokuapp.com/actors/5' \
--header 'Authorization: Bearer <token>'
```
Output:
```
{
    "deleted": 5,
    "success": true,
    "total_actors": 12
}
```
### DELETE '/movies/{movie_id}'
- General: Deletes the movie of the given ID if it exists.
It returns the success value, the ID of the deleted movie and the number of the total movies.
- Sample:
```bash
curl --location --request DELETE 'https://casting-agency-aymen.herokuapp.com/movies/5' \
--header 'Authorization: Bearer <token>'
```
Output:
```
{
    "deleted": 5,
    "success": true,
    "total_movies": 17
}
```
### PATCH '/actors/{actor_id}'
- General: Modifies the actor if the given ID using the data in the request JSON body if it exists. 
It returns the success value, the ID of the modified actor and the number of the total actors.
- Sample:
```bash
curl --location --request PATCH 'https://casting-agency-aymen.herokuapp.com/actors/3' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "age":48,
    "name":"LEONARDO DICAPRIO"
}'
```
Output:
```bash
{
    "success": true,
    "total_actors": 12,
    "updated": 3
}
```
### PATCH '/movies/{movie_id}'
- General: Modifies the movie if the given ID using the data in the request JSON body if it exists. 
It returns the success value, the ID of the modified movie and the number of the total movies.
- Sample:
```bash
curl --location --request PATCH 'https://casting-agency-aymen.herokuapp.com/movies/3' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title":"Batman the dark knight"
}'
```
Output:
```
{
    "success": true,
    "total_movies": 17,
    "updated": 3
}
```