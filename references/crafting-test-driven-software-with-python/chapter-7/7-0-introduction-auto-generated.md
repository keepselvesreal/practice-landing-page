# 7.0 Introduction [auto-generated] (pp.164-165)

---
**Page 164**

7
Fitness Function with a Contact
Book Application
We have already seen that in test-driven development, it is common to start development
by designing and writing acceptance tests to define what the software should do and then
dive into the details of how to do it with lower-level tests. That frequently is the foundation
of Acceptance Test-Driven Development (ATDD), but more generally, what we are trying
to do is to define a Fitness Function for our whole software. A fitness function is a function
that, given any kind of solution, tells us how good it is; the better the fitness function, the
closer we get to the result.
Even though fitness functions are typically used in genetic programming to select the
solutions that should be moved forward to the next iteration, we can see our acceptance
tests as a big fitness function that takes the whole software as the input and gives us back a
value of how good the software is.
All acceptance tests passed? This is 100% what it was meant to be, while only 50% of
acceptance tests have been passed? That's half-broken... As far as our fitness function really
describes what we wanted, it can save us from shipping the wrong application.
That's why acceptance tests are one of the most important pieces of our test suite and a test
suite comprised solely of unit tests (or, more generally, technical tests) can't really
guarantee that our software is aligned with what the business really wanted. Yes, it might
do what the developer wanted, but not what the business wanted.
In this chapter, we will cover the following topics:
Writing acceptance tests
Using behavior-driven development
Embracing specifications by example


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


