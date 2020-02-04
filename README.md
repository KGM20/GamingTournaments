# Gaming Tourneys API

## Full Stack Web Developer Nanodegree - Capstone Project

This project is an API where players have the opportunity to search and get inscribed on tournaments of different categories and games. It's inspired on the growing gaming community that want to participate casually or professionally on different tourneys to show their skills and get recognized for it, but without forgetting the most important part, have fun.

This is a part of the Full-Stack Web Developer Nanodegree of Udacity, designed to focus on applying all the skills obtained during the course.

The production code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

The commit messages for this project follows [Udacity Git Commit Message Style Guide](https://udacity.github.io/git-styleguide/)

## Gaming Tourneys API - Backend

### Getting Started - Running the server locally

#### Installing Dependencies

##### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

##### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server

From within the source directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Testing
To run the tests, run:
```
python test_app.py
```

### Hosting instructions

The API is running live using [Heroku](https://www.heroku.com/) application platform.

The deployment for the application is done manually by [The Owner](https://github.com/KGM20/) of this repository after he verifies the status of the last commits and upload the project using the 'master' branch as source of the application.

The application URL is live on:
```
https://gaming-tournaments.herokuapp.com
```

## API Reference

You can find the API reference [here](API.md).