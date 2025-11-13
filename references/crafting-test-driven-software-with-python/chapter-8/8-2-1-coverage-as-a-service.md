# 8.2.1 Coverage as a service (pp.194-196)

---
**Page 194**

PyTest Essential Plugins
Chapter 8
[ 194 ]
Coverage as a service
Now that all our tests are passing and our code is fully verified, how can we make sure we
don't forget about verifying our coverage when we extend our code base? As we have seen
in Chapter 4, Scaling the Test Suite, there are services that enable us to run our test suite on
every new commit we do. Can we leverage them to also make sure that our coverage didn't
worsen?
Strictly speaking, ensuring that the coverage doesn't decrease requires comparing the
current coverage with the one of the previous successful run, which is something that
services such as Travis CI are not able to do as they don't persist any information after our
tests have run. So, the information pertaining to the previous runs is all lost.
Luckily, there are services such as Coveralls that integrate very well with Travis CI and
allow us to easily get our coverage in the cloud:
Figure 8.1 – Coveralls web page


---
**Page 195**

PyTest Essential Plugins
Chapter 8
[ 195 ]
As for Travis CI, we can log in with our GitHub account and add any repository that we
had on GitHub:
Figure 8.2 – Adding a repo on Coveralls
Once a repository is enabled, Coveralls is ready to receive coverage data for that repository.
But how can we get the coverage there?
First of all, we have to tell Travis CI to install support for Coveralls, so, in the install section
of our project, .travis.yml, we can add the relevant command:
install:
  - "pip install coveralls"
Then, given that we should already be generating the coverage data by running pytest --
cov, we have to tell Travis CI to send that data to Coveralls when the test run succeeds:
after_success:
  - coveralls
Our final .travis.yml file should look like the following:
install:
  - "pip install coveralls"
  - "pip install -e src"
script:
  - "pytest -v --cov=contacts"


---
**Page 196**

PyTest Essential Plugins
Chapter 8
[ 196 ]
after_success:
  - coveralls
If we have done everything correctly, we should see in Coveralls the trend of our coverage
reporting and we should be able to get notified when it lowers or goes below a certain
threshold:
Figure 8.3 – Coveralls coverage reporting
Now that we have our coverage reporting in place, we can move on to taking a look at the
other principal plugins that are available for PyTest.
Using pytest-benchmark for benchmarking
Another frequent need when writing applications used by many users is to make sure that
they perform in a reasonable way and, hence, that our users don't have to wait too long for
something to happen. This is usually achieved by benchmarking core paths of our code
base to make sure that slowdowns aren't introduced in those functions and methods. Once
we have a good benchmark suite, all we have to do is rerun it on every code change and
compare the results to previous runs. If nothing got slower, we are good to go.


