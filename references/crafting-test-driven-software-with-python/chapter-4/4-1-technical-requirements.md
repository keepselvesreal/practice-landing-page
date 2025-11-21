# 4.1 Technical requirements (pp.114-115)

---
**Page 114**

4
Scaling the Test Suite
Writing one test is easy; writing thousands of tests, maintaining them, and ensuring they
don’t become a burden for development and the team is hard. Let’s dive into some tools
and best practices that help us define our test suite and keep it in shape.
To support the concepts in this chapter, we are going to use the test suite written for our
Chat application in Chapter 2, Test Doubles with a Chat Application. We are going to see how
to scale it as the application gets bigger and the tests get slower, and how to organize it in a
way that can serve us in the long term.
In this chapter, we will cover the following topics:
Scaling tests
Working with multiple suites
Carrying out performance testing
Enabling continuous integration
Technical requirements
A working Python interpreter and a GitHub.com account are required to work through the
examples in this chapter.
The examples we'll work through have been written using Python 3.7, but should work
with most modern Python versions.
The source code for the examples in this chapter can be found on GitHub
at https://github.com/PacktPublishing/Crafting-Test-Driven-Software-with-Python
/tree/main/Chapter04


---
**Page 115**

Scaling the Test Suite
Chapter 4
[ 115 ]
Scaling tests
When we started our Chat application in Chapter 2, Test Doubles with a Chat Application, the
whole code base was contained in a single Python module. This module mixed both the
application itself, the test suite, and the fakes that we needed for the test suite.
While that process fits well for the experimentation and hacking phase, it's not convenient
for the long term. As we already saw in Chapter 3, Test-Driven Development while Creating a
TODO List, it's possible to split tests into multiple files and directories and keep them
separated from our application code.
As our project grows, the first step is to split our test suite from our code base. We are going
to use the src directory for the code base and the tests directory for the test suite. The
src directory in this case will contain the chat package, which contains the modules for
the client and server code:
.
├── src
│   ├── chat
│   │   ├── client.py
│   │   ├── __init__.py
│   │   └── server.py
│   └── setup.py
The src/chat/client.py file will contain the previous Connection and ChatClient
classes, while in src/chat/server.py we are going to put the new_chat_server
function.
We also provide a very minimal src/setup.py to allow installation of the chat package:
from setuptools import setup
setup(name='chat', packages=['chat'])
Now that we can install the chat package through pip install -e ./src and then use
any class within it through import chat, our tests can be moved anywhere; they no longer
need to be in the same directory of the files they need to test. 


