# 12.3.3 Testing multiple browsers (pp.297-300)

---
**Page 297**

End-to-End Testing with the Robot Framework
Chapter 12
[ 297 ]
Now that we have conditional execution of the instructions that caused problems when
using a headless browser, we can rerun our test:
$ robot searchgoogle.robot
=======================================================
Searchgoogle
=======================================================
Search On Google                               | PASS |
-------------------------------------------------------
Searchgoogle                                   | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
=======================================================
Now, our tests finally passed using a headless browser and we learned how to use
variables and conditional execution in Robot tests.
Testing multiple browsers
Now that we know how to run tests in Chrome, headless or not, it might be reasonable to
feel the need to verify that our web application actually works on other browsers, too. So
the question might be how we can also verify it on Firefox or Edge.
Luckily for us, we just refactored the browser in use to be a variable, so we can just change
that variable and have all our tests run on one browser or the other. 
But if we want to make this part of our CI, it's not very convenient to change the tests file in
the middle of our CI runs. For this reason, Robot allows the provision of variable values
through the command line using the --variable option. For example, to use Firefox, we
could pass --variables browser:firefox:
$ robot --variable browser:firefox searchgoogle.robot
=====================================================
Searchgoogle
=====================================================
Search On Google                             | FAIL |
Element with locator 'name=q' not found.
-----------------------------------------------------
Searchgoogle                                 | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
=====================================================


---
**Page 298**

End-to-End Testing with the Robot Framework
Chapter 12
[ 298 ]
Surprisingly, when run with Firefox, our test failed. This is not only because websites might
behave differently when using different browsers, but also because the browsers
themselves might behave differently.
For example, Firefox didn't select back the primary page after we accepted the privacy
policy, so it's still trying to act inside the iframe that contained the privacy policy. This
makes it impossible for the browser to find the input with name=q, where it's meant to
write the query string, and so the test is failing.
To fix this, we can modify our test slightly to Unselect Frame after we have finished with
it:
*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    ${BROWSER}
     Run Keyword If    ${NOTHEADLESS}    Wait Until Page Contains Element
         cnsw
     Run Keyword If    ${NOTHEADLESS}    Select Frame    //iframe
     Run Keyword If    ${NOTHEADLESS}    Submit Form    //form
     Unselect Frame
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    ENTER
     Page Should Contain    Wikipedia
     Close Window
This will make sure that the test is able to accept the privacy policy and go back to the
search field in both Chrome and Firefox, thus solving our problem. Now that we are able to
perform the search, let's go back to our tests and see what happens when rerunning them:
$ robot --variable browser:firefox searchgoogle.robot
=====================================================
Searchgoogle
=====================================================
Search On Google                             | FAIL |
Page should have contained text 'Wikipedia' but did not.
-----------------------------------------------------
Searchgoogle                                 | FAIL |
1 critical test, 0 passed, 1 failed
1 test total, 0 passed, 1 failed
=====================================================
Another apparent failure is that even though the search happened correctly, the browser
was unable to find Wikipedia in the results.


---
**Page 299**

End-to-End Testing with the Robot Framework
Chapter 12
[ 299 ]
In this case, the log.html output can immediately help us understand what's going wrong.
If we look at it, we will see that the problem is that by the time our test checks for
"Wikipedia", the web page has not yet loaded the results themselves. The search box is
still visible in the screenshot that the log file contains:
Figure 12.7 – The log for our test that failed because Firefox was slower than the test itself


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


