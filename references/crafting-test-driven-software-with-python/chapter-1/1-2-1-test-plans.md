# 1.2.1 Test plans (pp.8-9)

---
**Page 8**

Getting Started with Software Testing
Chapter 1
[ 8 ]
Test plans
A test plan is composed of multiple test cases, each specifying the following:
Preconditions: What's necessary to be able to verify the case
Steps: Actions that have to succeed when executed in the specified order
Postconditions: In which state the system is expected to be at the end of the steps
A sample test case of software where logging in with a username and password is
involved, and we might want to allow the user to reset those, might look like the following
table:
Test Case: 2.2 - Change User Password
Preconditions:
• A user, user1 exists
• The user is logged in as user1
• The user is at the main menu
# Action
Expected Response
Success /
Fail
1 Click the change password button. The system shows a dialog to insert a new password.
2 Enter newpass.
The dialog shows 7 asterisks in the password field.
3 Click the OK button.
The system shows a dialog with a success message.
4 Wait 2 seconds.
The success dialog goes away.
Postconditions:
• The user1 password is now newpass
These test cases are divided into cases, are manually verified by a dedicated team, and a
sample of them is usually selected to be executed during development, but most of them
are checked when the development team declared the work done.
This meant that once the team finishes its work, it takes days/weeks for the release to
happen, as the whole software has to be verified by humans clicking buttons, with all the
unpredictable results that involves, as humans can get distracted, pressing the wrong
button or receiving phone calls in the middle of a test case.
As software usage became more widespread, and business-to-consumer products became
the norm, consumers started to appreciate faster release cycles. Companies that updated
their products with new features frequently were those that ended up dominating the
market in the long term.


---
**Page 9**

Getting Started with Software Testing
Chapter 1
[ 9 ]
If you think about modern release cycles, we are now used to getting a new version of our
favorite mobile application weekly. Such applications are probably so complex that they
involve thousands of test cases. If all those cases had to be performed by a human, there
would be no way for the company to provide you with frequent releases.
The worst thing you can do, by the way, is to release a broken product. Your users will lose
confidence and will switch to other more reliable competitors if they can't get their job done
due to crashes or bugs. So how can we deliver such frequent releases without reducing our
test coverage and thus incurring more bugs?
The solution came from automating the test process. So while we learned how to detect
defects by writing and executing test plans, it's only by making them automatic that we can
scale them to the number of cases that will ensure robust software in the long term.
Instead of having humans test software, have some other software test it. What a person
does in seconds can happen in milliseconds with software and you can run thousands of
tests in a few minutes.
Introducing automatic tests and test suites
Automated testing is, in practice, the art of writing another piece of software to test an
original piece of software.
As testing a whole piece of software has to take millions of variables and possible code
paths into account, a single program trying to test another one would be very complex and
hard to maintain. For this reason, it's usually convenient to split that program into smaller
isolated programs, each being a test case.
Each test case contains all the instructions that are required to set up the target software in a
state where the parts that are the test case areas of interest can be tested, the tests can be
done, and all the conditions can be verified and reset back to the state of the target software
so a subsequent test case can find a known state from which to start.
When using the unittest module that comes with the Python Standard Library, each test
case is declared by subclassing from the unittest.TestCase class and adding a method
whose name starts with test, which will contain the test itself:
import unittest
class MyTestCase(unittest.TestCase):
    def test_one(self):
        pass


