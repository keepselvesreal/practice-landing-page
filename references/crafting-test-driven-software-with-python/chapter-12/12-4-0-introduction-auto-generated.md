# 12.4.0 Introduction [auto-generated] (pp.300-301)

---
**Page 300**

End-to-End Testing with the Robot Framework
Chapter 12
[ 300 ]
We can fix this by waiting for the search results to appear before performing the assertion,
so let's tweak our search test a bit more to include an explicit wait for the results:
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    ${BROWSER}
     Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
         cnsw
     Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
     Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
     Unselect Frame
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    SPACE
     Press Keys    name=q    ENTER
     Wait Until Page Contains Element    id=res
     Page Should Contain    Wikipedia
     Close Window
This last version of our test is finally able to pass in connection with all the browsers we
were concerned with, Firefox and Chrome, with both of them in headless mode too:
$ robot --variable browser:headlessfirefox searchgoogle.robot
=============================================================
Searchgoogle
=============================================================
Search On Google                                     | PASS |
-------------------------------------------------------------
Searchgoogle                                         | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
=============================================================
At this point, we know how to write tests in Robot and how to write them so that we can
verify them using multiple different browsers.
Extending the Robot Framework
As we have seen, Robot can be expanded with libraries that can add more keywords. That
can be a convenient feature also for us when writing tests. If we have a set of instructions
that we are going to repeat frequently in our tests, it would be convenient to factor them
into a single keyword that we can reuse. Furthermore, Robot can be expanded with new
custom commands that we can implement in Python.


---
**Page 301**

End-to-End Testing with the Robot Framework
Chapter 12
[ 301 ]
Adding custom keywords
To see how extending Robot with custom keywords works, we are going to create a very
simple customkeywords.robot test file, where we are going to write a basic script that
only greets us:
*** Test Cases ***
Use Custom Keywords
    Echo Hello
Running the script will fail as we have not yet implemented the Echo Hello keyword, so
how can we provide it? For this purpose, Robot supports a *** Keywords *** section,
where we can declare all our custom keywords, so let's declare our keyword there:
*** Keywords ***
Echo Hello
    Log Hello!
*** Test Cases ***
Use Custom Keywords
    Echo Hello
The Echo Hello keyword is just going to invoke the built-in Log keyword, passing a
hardcoded greeting string, so it's not very helpful, but we could actually list any kind or
amount of commands within a custom keyword, so we could make it do whatever we
needed.
Now that we have provided a declaration for the Echo Hello command, rerunning the
tests will succeed:
$ robot customkeywords.robot
===================================================
Customkeywords
===================================================
Use Custom Keywords                        | PASS |
---------------------------------------------------
Customkeywords                             | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
===================================================
The output of our logging is not visible on the shell from which we started the Robot
command, but if we open the log.html file, we will see that the string was correctly
logged in that document.


