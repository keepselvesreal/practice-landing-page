# Unit Testing: Principles, Practices, and Patterns (p.i)

# brief contents (p.v)

# contents (p.vii)

# preface (p.xiv)

# acknowledgments (p.xv)

# about this book (p.xvi)

## Who should read this book (p.xvi)

## How this book is organized: A roadmap (p.xvii)

## About the Code (p.xvii)

## liveBook discussion forum (p.xviii)

### Other online resources (p.xviii)

# about the author (p.xix)

# about the cover illustration (p.xx)

# Part 1—The bigger picture (p.1)

## 1 The goal of unit testing (p.3)

### 1.0 Introduction [auto-generated] (p.3)

### 1.1 The current state of unit testing (p.4)

### 1.2 The goal of unit testing (p.5)

#### 1.2.0 Introduction [auto-generated] (p.5)

#### 1.2.1 What makes a good or bad test? (p.7)

### 1.3 Using coverage metrics to measure test suite quality (p.8)

#### 1.3.0 Introduction [auto-generated] (p.8)

#### 1.3.1 Understanding the code coverage metric (p.9)

#### 1.3.2 Understanding the branch coverage metric (p.10)

#### 1.3.3 Problems with coverage metrics (p.12)

#### 1.3.4 Aiming at a particular coverage number (p.15)

### 1.4 What makes a successful test suite? (p.15)

#### 1.4.0 Introduction [auto-generated] (p.15)

#### 1.4.1 It’s integrated into the development cycle (p.16)

#### 1.4.2 It targets only the most important parts of your code base (p.16)

#### 1.4.3 It provides maximum value with minimum maintenance costs (p.17)

### 1.5 What you will learn in this book (p.17)

### 1.6 Summary (p.18)

## 2 What is a unit test? (p.20)

### 2.0 Introduction [auto-generated] (p.20)

### 2.1 The definition of “unit test” (p.21)

#### 2.1.1 The isolation issue: The London take (p.21)

#### 2.1.2 The isolation issue: The classical take (p.27)

### 2.2 The classical and London schools of unit testing (p.30)

#### 2.2.1 How the classical and London schools handle dependencies (p.30)

### 2.3 Contrasting the classical and London schools of unit testing (p.34)

#### 2.3.1 Unit testing one class at a time (p.34)

#### 2.3.2 Unit testing a large graph of interconnected classes (p.35)

#### 2.3.3 Revealing the precise bug location (p.36)

#### 2.3.4 Other differences between the classical and London schools (p.36)

### 2.4 Integration tests in the two schools (p.37)

#### 2.4.0 Introduction [auto-generated] (p.37)

#### 2.4.1 End-to-end tests are a subset of integration tests (p.38)

### 2.5 Summary (p.39)

## 3 The anatomy of a unit test (p.41)

### 3.0 Introduction [auto-generated] (p.41)

### 3.1 How to structure a unit test (p.42)

#### 3.1.1 Using the AAA pattern (p.42)

#### 3.1.2 Avoid multiple arrange, act, and assert sections (p.43)

#### 3.1.3 Avoid if statements in tests (p.44)

#### 3.1.4 How large should each section be? (p.45)

#### 3.1.5 How many assertions should the assert section hold? (p.47)

#### 3.1.6 What about the teardown phase? (p.47)

#### 3.1.7 Differentiating the system under test (p.47)

#### 3.1.8 Dropping the arrange, act, and assert comments from tests (p.48)

### 3.2 Exploring the xUnit testing framework (p.49)

### 3.3 Reusing test fixtures between tests (p.50)

#### 3.3.0 Introduction [auto-generated] (p.50)

#### 3.3.1 High coupling between tests is an anti-pattern (p.52)

#### 3.3.2 The use of constructors in tests diminishes test readability (p.52)

#### 3.3.3 A better way to reuse test fixtures (p.52)

### 3.4 Naming a unit test (p.54)

#### 3.4.0 Introduction [auto-generated] (p.54)

#### 3.4.1 Unit test naming guidelines (p.56)

#### 3.4.2 Example: Renaming a test toward the guidelines (p.56)

### 3.5 Refactoring to parameterized tests (p.58)

#### 3.5.0 Introduction [auto-generated] (p.58)

#### 3.5.1 Generating data for parameterized tests (p.60)

### 3.6 Using an assertion library to further improve test readability (p.62)

### 3.7 Summary (p.63)

# Part 2—Making your tests work for you (p.65)

## 4 The four pillars of a good unit test (p.67)

### 4.0 Introduction [auto-generated] (p.67)

### 4.1 Diving into the four pillars of a good unit test (p.68)

#### 4.1.1 The first pillar: Protection against regressions (p.68)

#### 4.1.2 The second pillar: Resistance to refactoring (p.69)

#### 4.1.3 What causes false positives? (p.71)

#### 4.1.4 Aim at the end result instead of implementation details (p.74)

### 4.2 The intrinsic connection between the first two attributes (p.76)

#### 4.2.1 Maximizing test accuracy (p.76)

#### 4.2.2 The importance of false positives and false negatives: The dynamics (p.78)

### 4.3 The third and fourth pillars: Fast feedback and maintainability (p.79)

### 4.4 In search of an ideal test (p.80)

#### 4.4.0 Introduction [auto-generated] (p.80)

#### 4.4.1 Is it possible to create an ideal test? (p.81)

#### 4.4.2 Extreme case #1: End-to-end tests (p.81)

#### 4.4.3 Extreme case #2: Trivial tests (p.82)

#### 4.4.4 Extreme case #3: Brittle tests (p.83)

#### 4.4.5 In search of an ideal test: The results (p.84)

### 4.5 Exploring well-known test automation concepts (p.87)

#### 4.5.1 Breaking down the Test Pyramid (p.87)

#### 4.5.2 Choosing between black-box and white-box testing (p.89)

### 4.6 Summary (p.90)

## 5 Mocks and test fragility (p.92)

### 5.0 Introduction [auto-generated] (p.92)

### 5.1 Differentiating mocks from stubs (p.93)

#### 5.1.1 The types of test doubles (p.93)

#### 5.1.2 Mock (the tool) vs. mock (the test double) (p.94)

#### 5.1.3 Don’t assert interactions with stubs (p.96)

#### 5.1.4 Using mocks and stubs together (p.97)

#### 5.1.5 How mocks and stubs relate to commands and queries (p.97)

### 5.2 Observable behavior vs. implementation details (p.99)

#### 5.2.1 Observable behavior is not the same as a public API (p.99)

#### 5.2.2 Leaking implementation details: An example with an operation (p.100)

#### 5.2.3 Well-designed API and encapsulation (p.103)

#### 5.2.4 Leaking implementation details: An example with state (p.104)

### 5.3 The relationship between mocks and test fragility (p.106)

#### 5.3.1 Defining hexagonal architecture (p.106)

#### 5.3.2 Intra-system vs. inter-system communications (p.110)

#### 5.3.3 Intra-system vs. inter-system communications: An example (p.111)

### 5.4 The classical vs. London schools of unit testing, revisited (p.114)

#### 5.4.0 Introduction [auto-generated] (p.114)

#### 5.4.1 Not all out-of-process dependencies should be mocked out (p.115)

#### 5.4.2 Using mocks to verify behavior (p.116)

### 5.5 Summary (p.116)

## 6 Styles of unit testing (p.119)

### 6.0 Introduction [auto-generated] (p.119)

### 6.1 The three styles of unit testing (p.120)

#### 6.1.1 Defining the output-based style (p.120)

#### 6.1.2 Defining the state-based style (p.121)

#### 6.1.3 Defining the communication-based style (p.122)

### 6.2 Comparing the three styles of unit testing (p.123)

#### 6.2.0 Introduction [auto-generated] (p.123)

#### 6.2.1 Comparing the styles using the metrics of protection against regressions and feedback speed (p.124)

#### 6.2.2 Comparing the styles using the metric of resistance to refactoring (p.124)

#### 6.2.3 Comparing the styles using the metric of maintainability (p.125)

#### 6.2.4 Comparing the styles: The results (p.127)

### 6.3 Understanding functional architecture (p.128)

#### 6.3.1 What is functional programming? (p.128)

#### 6.3.2 What is functional architecture? (p.132)

#### 6.3.3 Comparing functional and hexagonal architectures (p.133)

### 6.4 Transitioning to functional architecture and output- based testing (p.135)

#### 6.4.1 Introducing an audit system (p.135)

#### 6.4.2 Using mocks to decouple tests from the filesystem (p.137)

#### 6.4.3 Refactoring toward functional architecture (p.140)

#### 6.4.4 Looking forward to further developments (p.146)

### 6.5 Understanding the drawbacks of functional architecture (p.146)

#### 6.5.0 Introduction [auto-generated] (p.146)

#### 6.5.1 Applicability of functional architecture (p.147)

#### 6.5.2 Performance drawbacks (p.148)

#### 6.5.3 Increase in the code base size (p.149)

### 6.6 Summary (p.149)

## 7 Refactoring toward valuable unit tests (p.151)

### 7.0 Introduction [auto-generated] (p.151)

### 7.1 Identifying the code to refactor (p.152)

#### 7.1.1 The four types of code (p.152)

#### 7.1.2 Using the Humble Object pattern to split overcomplicated code (p.155)

### 7.2 Refactoring toward valuable unit tests (p.158)

#### 7.2.1 Introducing a customer management system (p.158)

#### 7.2.2 Take 1: Making implicit dependencies explicit (p.160)

#### 7.2.3 Take 2: Introducing an application services layer (p.160)

#### 7.2.4 Take 3: Removing complexity from the application service (p.163)

#### 7.2.5 Take 4: Introducing a new Company class (p.164)

### 7.3 Analysis of optimal unit test coverage (p.167)

#### 7.3.1 Testing the domain layer and utility code (p.167)

#### 7.3.2 Testing the code from the other three quadrants (p.168)

#### 7.3.3 Should you test preconditions? (p.169)

### 7.4 Handling conditional logic in controllers (p.169)

#### 7.4.0 Introduction [auto-generated] (p.169)

#### 7.4.1 Using the CanExecute/Execute pattern (p.172)

#### 7.4.2 Using domain events to track changes in the domain model (p.175)

### 7.5 Conclusion (p.178)

### 7.6 Summary (p.180)

# Part 3—Integration testing (p.183)

## 8 Why integration testing? (p.185)

### 8.0 Introduction [auto-generated] (p.185)

### 8.1 What is an integration test? (p.186)

#### 8.1.1 The role of integration tests (p.186)

#### 8.1.2 The Test Pyramid revisited (p.187)

#### 8.1.3 Integration testing vs. failing fast (p.188)

### 8.2 Which out-of-process dependencies to test directly (p.190)

#### 8.2.1 The two types of out-of-process dependencies (p.190)

#### 8.2.2 Working with both managed and unmanaged dependencies (p.191)

#### 8.2.3 What if you can’t use a real database in integration tests? (p.192)

### 8.3 Integration testing: An example (p.193)

#### 8.3.0 Introduction [auto-generated] (p.193)

#### 8.3.1 What scenarios to test? (p.194)

#### 8.3.2 Categorizing the database and the message bus (p.195)

#### 8.3.3 What about end-to-end testing? (p.195)

#### 8.3.4 Integration testing: The first try (p.196)

### 8.4 Using interfaces to abstract dependencies (p.197)

#### 8.4.0 Introduction [auto-generated] (p.197)

#### 8.4.1 Interfaces and loose coupling (p.198)

#### 8.4.2 Why use interfaces for out-of-process dependencies? (p.199)

#### 8.4.3 Using interfaces for in-process dependencies (p.199)

### 8.5 Integration testing best practices (p.200)

#### 8.5.1 Making domain model boundaries explicit (p.200)

#### 8.5.2 Reducing the number of layers (p.200)

#### 8.5.3 Eliminating circular dependencies (p.202)

#### 8.5.4 Using multiple act sections in a test (p.204)

### 8.6 How to test logging functionality (p.205)

#### 8.6.1 Should you test logging? (p.205)

#### 8.6.2 How should you test logging? (p.207)

#### 8.6.3 How much logging is enough? (p.212)

#### 8.6.4 How do you pass around logger instances? (p.212)

### 8.7 Conclusion (p.213)

### 8.8 Summary (p.213)

## 9 Mocking best practices (p.216)

### 9.0 Introduction [auto-generated] (p.216)

### 9.1 Maximizing mocks’ value (p.217)

#### 9.1.0 Introduction [auto-generated] (p.217)

#### 9.1.1 Verifying interactions at the system edges (p.219)

#### 9.1.2 Replacing mocks with spies (p.222)

#### 9.1.3 What about IDomainLogger? (p.224)

### 9.2 Mocking best practices (p.225)

#### 9.2.1 Mocks are for integration tests only (p.225)

#### 9.2.2 Not just one mock per test (p.225)

#### 9.2.3 Verifying the number of calls (p.226)

#### 9.2.4 Only mock types that you own (p.227)

### 9.3 Summary (p.227)

## 10 Testing the database (p.229)

### 10.0 Introduction [auto-generated] (p.229)

### 10.1 Prerequisites for testing the database (p.230)

#### 10.1.1 Keeping the database in the source control system (p.230)

#### 10.1.2 Reference data is part of the database schema (p.231)

#### 10.1.3 Separate instance for every developer (p.232)

#### 10.1.4 State-based vs. migration-based database delivery (p.232)

### 10.2 Database transaction management (p.234)

#### 10.2.0 Introduction [auto-generated] (p.234)

#### 10.2.1 Managing database transactions in production code (p.235)

#### 10.2.2 Managing database transactions in integration tests (p.242)

### 10.3 Test data life cycle (p.243)

#### 10.3.1 Parallel vs. sequential test execution (p.243)

#### 10.3.2 Clearing data between test runs (p.244)

#### 10.3.3 Avoid in-memory databases (p.246)

### 10.4 Reusing code in test sections (p.246)

#### 10.4.1 Reusing code in arrange sections (p.246)

#### 10.4.2 Reusing code in act sections (p.249)

#### 10.4.3 Reusing code in assert sections (p.250)

#### 10.4.4 Does the test create too many database transactions? (p.251)

### 10.5 Common database testing questions (p.252)

#### 10.5.1 Should you test reads? (p.252)

#### 10.5.2 Should you test repositories? (p.253)

### 10.6 Conclusion (p.254)

### 10.7 Summary (p.255)

# Part 4—Unit testing anti-patterns (p.257)

## 11 Unit testing anti-patterns (p.259)

### 11.0 Introduction [auto-generated] (p.259)

### 11.1 Unit testing private methods (p.260)

#### 11.1.1 Private methods and test fragility (p.260)

#### 11.1.2 Private methods and insufficient coverage (p.260)

#### 11.1.3 When testing private methods is acceptable (p.261)

### 11.2 Exposing private state (p.263)

### 11.3 Leaking domain knowledge to tests (p.264)

### 11.4 Code pollution (p.266)

### 11.5 Mocking concrete classes (p.268)

### 11.6 Working with time (p.271)

#### 11.6.1 Time as an ambient context (p.271)

#### 11.6.2 Time as an explicit dependency (p.272)

### 11.7 Conclusion (p.273)

### 11.8 Summary (p.273)

# index (p.275)

## A (p.275)

## B (p.275)

## C (p.275)

## D (p.276)

## E (p.277)

## F (p.277)

## G (p.277)

## H (p.277)

## I (p.277)

## J (p.278)

## L (p.278)

## M (p.278)

## N (p.279)

## O (p.279)

## P (p.279)

## Q (p.280)

## R (p.280)

## S (p.280)

## T (p.281)

## U (p.281)

## V (p.282)

## W (p.282)

## X (p.282)

## Y (p.282)