# MOVIFY

<img src="./static/images/logo.png" alt="movify logo" title="movify logo" width="200"/>

#### Video Demo: <URL HERE>

### Description:

This is a web application built with flask that provides general information about movies including recommendations, movie details, the ability to search a movie by title and creation of a personal watchlist.

### Data source

The data used in this project is obtained from the tmdb API which provides descriptive information about movies, tv shows, series and also actors and movie company details.

### Languages, frameworks and libraries.

In this project, I used a couple of tools which include

- python -> for server side logic
- Jinja -> for clientside templating
- HTML -> for client side user interface
- CSS -> for styling
- JavaScript -> for client side logic
- JQuery -> to ease the use of javascript in fetching json data from the flask API and updating the UI in real time
- tailwind CSS -> to ease styling through use of utility classes

### Modules and dependencies

The modules used include

#### standard

- json -> to convert python dictionaries to json objects returned as responses
- os -> to set and use environment variables
- sqlite3 -> to store users information and the respection watchlists

#### third-party

- dotenv -> used to store environment variables like tmdb API key in one file for easy setting and access
- flask -> module that contains all necessary functions and objects do develop a fully functional backend system
- flask_login -> used to manage user account logins an dsession management
- oauthlib -> used to communicate with the google API for authentication as a federated identity provider
- requests -> used to communicate with the tmdb API to fetch movie data
- werkzeug -> for password hashing and hash comparisons as used in account creation and login respectively

And the dependencies include

- @tailwindcss/forms -> tailwind plugin with utility classes used to style forms
- npm-run-all -> npm dependency that I used to execute multiple commands during development
- tailwindcss -> CSS framework that I used for the biggest portion of styling in this project
- tailwindcss-animated -> tailwind plugin that provides utility classes for animations.

### Design choices

In this project, alot of considerations were made in each and every part. Starting with choice of language up to color palette of the UI. Below are some of the design choices;

1. Language choices
   I chose flask for the backend logic because it is a light weighgt framework and easy to learn yet provided all the functionalities that I needed for the application's backend. It is easy to setup a project in flask than in any other language. And given my level of python, I couldn't easily manage some more complicated framework.

JQuery on the other hand stood out among all the javascript libraries I could use for my frontend because, it took me less than a day to learn it (very easy therefore). and also, it made things that were very complicated in vanilla JavaScript the easiest. For instance making API requests and updating the UI. to provides functions that are very easy to write and yet very powerful. It's ability to update the DOM as request data came was the major reason though for it's use. This is how I managed to give the user feedback therough changing the appearance of the heart icon a movie poster the moment they added it to their watchlist.

Lastly, tailwind CSS, the framework I used for styling the application's UI. It provides a very user-friendly guide at their website and is generally very easy to implement. It ensures consistency and and responsiveness throoughout the application through giving all elements similar styles to begin with. It then provides a set of standard color palettes and other standarsised DOM style properties, all accessible through the use of utility classes. Lastly, it is fully customisable meaning if I'm not happy with anything, I can simply change it to my custom values and everything works as planned.

Well... I said color palette too😊...
It is predominantly a skyblue palette since it is a vibrant color and therefore can easily interest the viewer into continuing to interact with the application. I also had nice well-contrasting shades in the tailwind universal color palette which I could use for both text and background.
Plus... skyblue is indeed my favorite color.😉

### Project directory

It's not a very clean tree though, but its as follows

- static
  - css
    - bin
      - my-styles.css -> the file in which I wrote my custom CSS styles.
      - output_styles.css -> the output file of tailwind style rules.
    - src
      - input_styles.css -> contains basic CSS @-rules that tailwind bases on to create the output.css rulse
    - images
      - logo.png -> the brand logo of movify.
    - js
      - base.js -> this is where I wrote vanilla JavaScript for the project.
      - jq.js -> and this is the file in which I wrote all the JQuery code for the project
- templates
  - apology.html -> the template that displays an apology in case of an error
  - base.html -> the base layout of the application (jinja sytntax)
  - details.html -> layout for displaying movie details about a movie selected by the user.
  - index.html -> The homepage of the application.
  - login.html -> The login page of the application.
  - search.html -> The page that holds the search results when a user searches for a movie by title.
  - signup.html -> The signup page of the application.
  - watchlist.html -> The watchlist page of the application. It lists all the movies selected by the user in their watchlist
- .env -> this file holds all the environment variables I used, including google client secrets and tmdb API key.
- .gitignore -> this holds the files that I didn't want to be uploaded to my remote origin on github, including the .env file, node_modules, and other files.
- app.py -> this is the file that hold the flask application code for the entire project.
- db.py -> this I used to create the db and set it up with some methods to help me select it easily whenever I needed to execute a query.
- movies.py -> this file holds all the functions that are mean't to communicate with the external tmdb API and query it for movie data.
- movify.db -> this is the sqlite3 database that holds user data and watchlists.
- package.json -> json file to keep track of the node modules used and basic information about the project.
- README -> descriptive file that has info about aspects of this project.
- requirements.txt -> this keeps track of all the python thirdparty modules I installed for the project.
- schema.sql -> contains the two schemas for the users' ands watchlist databses.
- tailwind.comfig.js -> this file holds the configuration code for tailwind CSS, including its plugins installed.
- user.py -> module created for general user account management tasks e.e. creation, among otthers.
- vercel.json -> this file provides configurations for vercel during deployment.
- watchlist.py -> used to create reusable methods for interacting with the watchlists database.

The project is not yet deployed though due to some unanticipated challenge. The sqlite3 database that I used in this project is not fully compatible with the free hosting service that I use (vercel) since it hosts serverless functions, It always creates new instances of the functions and runs those and therefore cannot write to the database. However it can read from it. So I'm thinking of either changing a hosting service or the database implementantion which in either case is a hard decision to make in a short while.

However, the project works perfectly locally. And... here are the steps one can follow to get it up and running.

1. install dependencies

- run `npm install` to install the node modules
- and `pip install -r requirements.txt` to install the python modules.
- then `npm run tw-build` to build the output.css file if not already built
- and finally `python app.py` to start the application.
- the application then runs on `http://127.0.0.1:5000/`

_note that all the above command are run in the terminal at the root of the project directory._

---

> _I am Davis and this was CS50._ 🦆
