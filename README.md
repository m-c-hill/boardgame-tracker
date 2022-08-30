# Board Game Tracker API

Board Game REST API built using Flask allowing users browse board games, add them to a personal collection and share reviews with other users.

The API is currently deployed through Heroku and can be [accessed here](https://board--game--tracker.herokuapp.com/api/). Find authentication information and API documentation below.

The project was created as the final project for the API Development and Documentation module of [Udacity's Full Stack Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

## Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses for our REST API.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are the ORM (Object-relatonal mapping) libraries of choice, used to define our domain models and handle all database interactions.

- [Alembic](https://alembic.sqlalchemy.org/en/latest/) and [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is a lightweight database migration tool used to manage changes to the domain models and update the database accordingly.

- [authlib](https://docs.authlib.org/en/latest/) and [Auth0](https://auth0.com/) to manage user authentication and authorization using JWT RBAC (Role-based access control).

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Used for encoding, decoding, and verifying JWTs, specifically to extract RBAC information for our application.

- [Swagger](https://swagger.io/) to document the API endpoints.

## Getting Started

### Install Dependencies

1. Create a new virtual environment: `python3 -m venv venv` and activate: `source venv/bin/activate`
2. Install all dependencies: `pip install -r requirements.txt`

### Set up the Database

With Postgres running, create the required databases for each configuration:

```bash
createdb boardgames
createdb boardgames_dev
createdb boardgames_test
```

These databases are initially seeded with dummy data when starting the Flask server.

### Running the Server

`python runserver.py`

Running the above will start the server on [localhost:5000/api](http://127.0.0.1:5000/api).

### Testing

[Pytest](https://docs.pytest.org/en/7.1.x/contents.html) was used as the testing framework for this project.

To deploy the tests, simply run:

```bash
python -m pytest
```

Example output:

```bash
platform linux -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/matt/dev/boardgame-tracker
plugins: mock-3.8.2
collected 52 items

tests/auth/test_auth0.py ......
tests/auth/test_rbac.py .
tests/integration/test_board_games.py ........
tests/integration/test_collections.py .....
tests/integration/test_reviews.py ..........
tests/integration/test_search.py .
tests/integration/test_users.py ..
tests/unit/test_board_game.py ....
tests/unit/test_collection.py .....
tests/unit/test_review.py .........
tests/unit/test_user.py .

============ 52 passed ============
```

A [Postman](https://www.postman.com/) collection is [also included](boardgame-tracker.postman_collection.json) in this repo which can be imported and run to test the authorization and authentication functionality of the API.

## Authorization

### Auth0

[Auth0](https://auth0.com/docs/get-started/auth0-overview) is a flexible, drop-in solution to add authentication and authorization services to applications. It minimises the cost, time, and risk associated with building an in-house solution to authenticate and authorize users.

### Setting Up Auth0

**The following is optional!** Users can link this API to their own Auth0 account using the following steps:

#### Create Auth0 App, API and Roles

1. Create a [new Auth0 Account](https://auth0.com/signup)
2. Select a unique tenant domain
3. Create a [new, single page web application](https://auth0.com/docs/get-started/auth0-overview/create-applications)
4. Register a [new API](https://auth0.com/docs/get-started/auth0-overview/set-up-apis)
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create [new API permissions](https://auth0.com/docs/manage-users/access-control/configure-core-rbac/manage-permissions):
   - `patch:designer`
   - `post:designers`
   - `post:reviews`
   - `patch:reviews`
   - `delete:review`
   - `post:games`
   - `patch:games`
   - `delete:games`
   - `post:publishers`
   - `patch:publisher`
   - `patch:reactions`
   - `post:genres`
   - `patch:genres`
   - `patch:collection`
6. Create new roles for:
   - User
     - can `delete:review`
     - can `patch:reactions`
     - can `patch:reviews`
     - can `post:reviews`
   - Admin
     - can perform **all actions**
7. Create two new accounts and assign the accounts a role from above.

#### Configure Locally

Update the following environmental variables in [.env](.env) by retrieving this values from your new Auth0 application:

- AUTH0_CLIENT_ID
- AUTH0_CLIENT_SECRET
- AUTH0_DOMAIN
- API_AUDIENCE

You will now be able to login to the API using the newly created users through your Auth0 account.

## API Reference

The API is currently hosted on [Heroku](https://www.heroku.com/) and can be accessed here: https://board--game--tracker.herokuapp.com/api

As discussed above, many of the API endpoints must be authorized using a JWT. Two dummy user accounts have been set up to allow users to generate JWTs with different permissions associated with them:

```
Admin
email: admin@games.io
password: Jdvru3$29W6A6aM

User
email: user@games.io
password: C8Jf&PPbUW&g$At
```

1. Go to https://board--game--tracker.herokuapp.com/auth/login
2. This will redirect you to the Auth0 login page.
3. Enter the credentials above.
4. Once logged in, you will be redirected to https://board--game--tracker.herokuapp.com/auth which will display the current JWT being used.
5. This JWT can then be used in further tests through Postman.

Alternatively, users are welcome to set up their own accounts.

## Documentation

Full API documentation can be found at https://board--game--tracker.herokuapp.com/swagger.

Below is a brief outline of some of the key endpoints:

### Auth

**GET /auth**

- Display current user ID and JWT

**GET /auth/login**

- Redirect users to Auth0 login page

**GET /auth/logout**

- Clear current user from the session and logout

### API

Base url: **/api**

#### Games

**GET, POST /games**

- Get all games (paginated) and add new games

**GET, PATCH, DELETE /games/{id}**

- Get a game by id, update a game and delete a game

**GET /games/{id}/reviews**

- Get all reviews for a game

#### Designers

**GET, POST /designers**

- Get all designer details and create new designers
  **GET, PATCH /api/designers/{id}**
- Get a designer by id and update a designer

#### Genres

**GET, POST /genres**

- Get all genre details and create new genres
  **GET, PATCH /genres/{id}**
- Get a genre by id and update a genre

#### Publishers

**GET, POST /publishers**

- Get all publisher details and create new publishers
  **GET, PATCH /publishers/{id}**
- Get a publisher by id and update a publisher

#### Search

**POST /search**

- Search for a board game where the title matches a search term

#### Reviews

**GET, POST /reviews**

- Get all reviews (paginated) and submit new reviews

**GET, PATCH, DELETE reviews/{id}**

- Get a review by id, update a review and delete a review

**GET, PATCH /reviews/{id}/reactions**

- Get all reactions for a review and like/dislike a review

#### Users

**GET /users/{id}/reviews**

- Get all reviews submitted by a user

#### Collections

**GET, PATCH /collections/{id}/games**

- Get all games in a collection; add/remove games from a collection

**PATCH /collections/{id}/privacy**

- Toggle the privacy of a collection

#### Future Goals

Further ideas for continued development of this project:

- Board game recommendation algorithm based on user's current collection and reviews.
- Allow users to log board game sessions and tag other users.
- Build out front end application.
