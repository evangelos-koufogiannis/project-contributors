# Project-Contributors
Design and Implementation of an API for a company that operates worldwide and wants to provide a platform in which programmers state up to three programming languages that they have expertise on (together with their level i.e. “beginner”, “experienced”, “expert”), so that they are publicly reachable to contribute to open-source projects that anyone can submit. Programming languages options would be:  C++, Javascript, Python, Java, Lua, Rust, Go, Julia

We need you to implement a REST API, with endpoints for the users to:

  ● Allow for the registration of their principal information, such as first_name, last_name,
    email, age, country, residence, username
  ● Reset their password (if they are already registered).
  ● Add / Remove a skill. (remember that at most 3 skills can be registered at any time)
  ● Create a new project and look for collaborators (see below)
  ● Get projects with open seats and express their interest for the corresponding pools.
  ● Get their overall statistics, e.g. number of projects contributed, number of projects created
  
For the open-source projects we need API endpoints for:

  ● A registered user to create a new project with the following information: project_name,
    description, maximum_collaborators, collaborators.
  ● The completion or deletion of a project from the corresponding user.
  ● Accepting or declining the interest of another user to take part in the project. Note that
    only the username, email and sk

# Instructions to start the Django application.
1) Clone the project to the desired directory: git clone https://github.com/evangelos-koufogiannis/project-contributors.git
2) Change directory to project-contributors one: cd project-contributors/
3) Create a Python 3 virtual environmet: python -m venv venv or python3 -m venv venv according to your setup
4) Activate the newly created venv: source venv/bin/activate
5) Install application's requirements defined in requirements.txt file: pip install -r requirements.txt
6) Change directory to Django's project directory: cd contributors/
7) Start the Djnago server (specify deferent IP and/or Port if that's desired but Postmans calls are for the default server settings): python manage.py runserver
