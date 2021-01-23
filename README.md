# Food Tinder

Food Tinder is a web application that I made as the final project for the CS50 Introduction to Computer Science course from Harvard University.

The app runs on a web Python server, using the Python framework Flask. The project uses a SQLite database to store user information and includes HTML, CSS and JavaScript / jQuery.

The user gets suggestions for recipes, based on some diet or preferences that they indicated. The programme uses data from an API called spoonacular that holds a lot of recipes and very detailed information about these recipes.

At first, the user has to register or login. The username and the hashed password are stored in the database, in a table called users. After registering, the new user gets asked if they have any special diet (vegetarian, vegan, dairy free etc). The user gets recipe suggestions, he can choose to like or dislike them. The liked recipes are stored in a personal library on the page "my favorites".

## API Reference

[https://api.spoonacular.com/recipes](https://api.spoonacular.com/recipes)


## Requirements

Python 3.0 or above
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

## Demonstration Video

[YouTube](https://youtu.be/6pqiYTB2pPA)

## License & copyright

© Stefanie Beyer, Berlin, Germany
