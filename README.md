# Food Tinder

Food Tinder is a web application that I made as the final project for the CS50 Introduction to Computer Science course from Harvard University.

The app runs on a web Python server, using the Python framework Flask. The project uses a SQLite database to store user information and includes HTML, CSS and JavaScript / jQuery. The programme uses data from an API called spoonacular that holds a lot of recipes with very detailed information.

At first, the user has to register or login. The username and the hashed password are stored in SQLite database. After logging in or registering, the user gets asked if they have any special diet (vegetarian, vegan, dairy free etc). The user receives recipe suggestions, they can choose to like or dislike them. The liked recipes are stored in a personal library on the page "my favorites".

## API Reference

[https://api.spoonacular.com/recipes](https://api.spoonacular.com/recipes)


## Requirements

Python 3.0 or above.
Create a profile at [https://spoonacular.com/food-api](https://spoonacular.com/food-api/) and create your own API Key. 


## Installation

```bash
$ pip install Flask
$ python3 -m venv venv
$ . venv/bin/activate
$ pip requests
$ pip cs50
$ pip flask_session
```

## Starting the app

Please insert your own API Key here.

```bash
$ export API_KEY=09a737aad0d64a409d2fbb7d0a7861cd
$ flask run
```

## Video demonstration

Click here for a short video demonstration of the app:

[![Watch the video](https://img.youtube.com/vi/CWYAH6WVfMo/maxresdefault.jpg)](https://www.youtube.com/watch?v=CWYAH6WVfMo)

## License & copyright

A starter code for the backend server was provided for a previous project in the CS50 course ("Finance"). This code was reused and altered for the purpose of this project. All frontend code as well as the logic concerning the SQLite database and the "spoonacular" API were written by Stefanie Beyer, Berlin 2020.
