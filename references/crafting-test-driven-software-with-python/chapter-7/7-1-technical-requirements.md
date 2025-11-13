# 7.1 Technical requirements (pp.165-165)

---
**Page 165**

Fitness Function with a Contact Book Application
Chapter 7
[ 165 ]
Technical requirements
We need a working Python interpreter with the PyTest framework installed. For the
behavior-driven development part, we are going to need the pytest-bdd plugin.
pytest and pytest-bdd can be installed using the following command:
$ pip install pytest pytest-bdd
The examples have been written on Python 3.7, pytest 6.0.2, and pytest-bdd 4.0.1, but
should work on most modern Python versions. You can find the code files present in this
chapter on GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-
Software-​with-​Python/​tree/​main/​Chapter07.
Writing acceptance tests
Our company has just released a new product; it's a mobile phone for extreme geeks that
will only work through a UNIX shell. All the things our users want to do will be doable via
the command line and we are tasked with writing the contact book application. Where do
we start?
The usual way! First, we prepare our project skeleton. We are going to expose the contact
book application as the contacts package, as shown here, and we are going to provide a
main entry point. For now, we are going to invoke this with python -m contacts, but in
the future, we will wrap this in a more convenient shortcut:
.
├── src
│   ├── contacts
│   │   ├── __init__.py
│   │   └── __main__.py
│   └── setup.py
└── tests
    ├── conftest.py
    ├── functional
    │   └── test_acceptance.py
    ├── __init__.py
    └── unit
For now, all our modules are empty, just placeholders are present, but the first thing we
surely want to have is a location where we can place our acceptance tests. So, the
test_acceptance module is born. Now, how do we populate it?


