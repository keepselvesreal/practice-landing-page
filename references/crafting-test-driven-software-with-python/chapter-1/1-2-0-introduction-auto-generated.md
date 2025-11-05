# 1.2.0 Introduction [auto-generated] (pp.7-8)

---
**Page 7**

Getting Started with Software Testing
Chapter 1
[ 7 ]
In this chapter, we will cover the following:
Introducing software testing and quality control
Introducing automatic tests and test suites
Introducing test-driven development and unit tests
Understanding integration and functional tests
Understanding the testing pyramid and trophy
Technical requirements
A working Python interpreter is all that's needed.
The examples have been written in Python 3.7 but should work in most modern Python
versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter01.
Introducing software testing and quality
control
From the early days, it was clear that like any other machine, software needed a way to 
verify it was working properly and was built with no defects.
Software development processes have been heavily inspired by manufacturing industry
standards, and early on, testing and quality control were introduced into the product
development life cycle. So software companies frequently have a quality assurance team
that focuses on setting up processes to guarantee robust software and track results.
Those processes usually include a quality control process where the quality of the built
artifact is assessed before it can be considered ready for users.
The quality control process usually achieves such confidence through the execution of a test
plan. This is usually a checklist that a dedicated team goes through during the various
phases of production to ensure the software behaves as expected.


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


