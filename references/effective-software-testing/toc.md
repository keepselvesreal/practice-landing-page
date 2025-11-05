# Effective Software Testing (p.Effective Software Testing)

# brief contents (p.v)

# contents (p.vii)

# forewords (p.xiii)

# preface (p.xvi)

# acknowledgments (p.xviii)

# about this book (p.xxi)

## Who should read this book (p.xxi)

## How this book is organized: A roadmap (p.xxii)

## What this book does not cover (p.xxiii)

## About the code (p.xxiv)

## liveBook discussion forum (p.xxiv)

# about the author (p.xxv)

# about the cover illustration (p.xxvi)

## 1 Effective and systematic software testing (p.1)

### 1.0 Introduction [auto-generated] (p.1)

### 1.1 Developers who test vs. developers who do not (p.2)

### 1.2 Effective software testing for developers (p.11)

#### 1.2.0 Introduction [auto-generated] (p.11)

#### 1.2.1 Effective testing in the development process (p.12)

#### 1.2.2 Effective testing as an iterative process (p.14)

#### 1.2.3 Focusing on development and then on testing (p.14)

#### 1.2.4 The myth of “correctness by design” (p.15)

#### 1.2.5 The cost of testing (p.15)

#### 1.2.6 The meaning of effective and systematic (p.15)

#### 1.2.7 The role of test automation (p.16)

### 1.3 Principles of software testing (or, why testing is so difficult) (p.16)

#### 1.3.1 Exhaustive testing is impossible (p.16)

#### 1.3.2 Knowing when to stop testing (p.17)

#### 1.3.3 Variability is important (the pesticide paradox) (p.17)

#### 1.3.4 Bugs happen in some places more than others (p.17)

#### 1.3.5 No matter what testing you do, it will never be perfect or enough (p.18)

#### 1.3.6 Context is king (p.18)

#### 1.3.7 Verification is not validation (p.18)

### 1.4 The testing pyramid, and where we should focus (p.19)

#### 1.4.1 Unit testing (p.19)

#### 1.4.2 Integration testing (p.20)

#### 1.4.3 System testing (p.21)

#### 1.4.4 When to use each test level (p.23)

#### 1.4.5 Why do I favor unit tests? (p.23)

#### 1.4.6 What do I test at the different levels? (p.24)

#### 1.4.7 What if you disagree with the testing pyramid? (p.25)

#### 1.4.8 Will this book help you find all the bugs? (p.27)

### 1.5 Exercises (p.27)

### 1.6 Summary (p.29)

## 2 Specification-based testing (p.30)

### 2.0 Introduction [auto-generated] (p.30)

### 2.1 The requirements say it all (p.31)

#### 2.1.0 Introduction [auto-generated] (p.31)

#### 2.1.1 Step 1: Understanding the requirements, inputs, and outputs (p.33)

#### 2.1.2 Step 2: Explore what the program does for various inputs (p.34)

#### 2.1.3 Step 3: Explore possible inputs and outputs, and identify partitions (p.35)

#### 2.1.4 Step 4: Analyze the boundaries (p.37)

#### 2.1.5 Step 5: Devise test cases (p.39)

#### 2.1.6 Step 6: Automate the test cases (p.41)

#### 2.1.7 Step 7: Augment the test suite with creativity and experience (p.43)

### 2.2 Specification-based testing in a nutshell (p.45)

### 2.3 Finding bugs with specification testing (p.46)

### 2.4 Specification-based testing in the real world (p.54)

#### 2.4.1 The process should be iterative, not sequential (p.54)

#### 2.4.2 How far should specification testing go? (p.55)

#### 2.4.3 Partition or boundary? It does not matter! (p.55)

#### 2.4.4 On and off points are enough, but feel free to add in and out points (p.55)

#### 2.4.5 Use variations of the same input to facilitate understanding (p.55)

#### 2.4.6 When the number of combinations explodes, be pragmatic (p.56)

#### 2.4.7 When in doubt, go for the simplest input (p.56)

#### 2.4.8 Pick reasonable values for inputs you do not care about (p.56)

#### 2.4.9 Test for nulls and exceptional cases, but only when it makes sense (p.56)

#### 2.4.10 Go for parameterized tests when tests have the same skeleton (p.57)

#### 2.4.11 Requirements can be of any granularity (p.57)

#### 2.4.12 How does this work with classes and state? (p.57)

#### 2.4.13 The role of experience and creativity (p.59)

### 2.5 Exercises (p.59)

### 2.6 Summary (p.61)

## 3 Structural testing and code coverage (p.63)

### 3.0 Introduction [auto-generated] (p.63)

### 3.1 Code coverage, the right way (p.64)

### 3.2 Structural testing in a nutshell (p.68)

### 3.3 Code coverage criteria (p.69)

#### 3.3.1 Line coverage (p.69)

#### 3.3.2 Branch coverage (p.69)

#### 3.3.3 Condition + branch coverage (p.70)

#### 3.3.4 Path coverage (p.71)

### 3.4 Complex conditions and the MC/DC coverage criterion (p.72)

#### 3.4.1 An abstract example (p.72)

#### 3.4.2 Creating a test suite that achieves MC/DC (p.73)

### 3.5 Handling loops and similar constructs (p.75)

### 3.6 Criteria subsumption, and choosing a criterion (p.75)

### 3.7 Specification-based and structural testing: A running example (p.77)

### 3.8 Boundary testing and structural testing (p.82)

### 3.9 Structural testing alone often is not enough (p.82)

### 3.10 Structural testing in the real world (p.84)

#### 3.10.1 Why do some people hate code coverage? (p.84)

#### 3.10.2 What does it mean to achieve 100% coverage? (p.86)

#### 3.10.3 What coverage criterion to use (p.88)

#### 3.10.4 MC/DC when expressions are too complex and cannot be simplified (p.88)

#### 3.10.5 Other coverage criteria (p.89)

#### 3.10.6 What should not be covered? (p.90)

### 3.11 Mutation testing (p.90)

### 3.12 Exercises (p.93)

### 3.13 Summary (p.96)

## 4 Designing contracts (p.97)

### 4.0 Introduction [auto-generated] (p.97)

### 4.1 Pre-conditions and post-conditions (p.98)

#### 4.1.0 Introduction [auto-generated] (p.98)

#### 4.1.1 The assert keyword (p.99)

#### 4.1.2 Strong and weak pre- and post-conditions (p.100)

### 4.2 Invariants (p.102)

### 4.3 Changing contracts, and the Liskov substitution principle (p.105)

#### 4.3.0 Introduction [auto-generated] (p.105)

#### 4.3.1 Inheritance and contracts (p.107)

### 4.4 How is design-by-contract related to testing? (p.109)

### 4.5 Design-by-contract in the real world (p.110)

#### 4.5.1 Weak or strong pre-conditions? (p.110)

#### 4.5.2 Input validation, contracts, or both? (p.110)

#### 4.5.3 Asserts and exceptions: When to use one or the other (p.112)

#### 4.5.4 Exception or soft return values? (p.113)

#### 4.5.5 When not to use design-by-contract (p.113)

#### 4.5.6 Should we write tests for pre-conditions, post-conditions, and invariants? (p.114)

#### 4.5.7 Tooling support (p.114)

### 4.6 Exercises (p.114)

### 4.7 Summary (p.116)

## 5 Property-based testing (p.117)

### 5.0 Introduction [auto-generated] (p.117)

### 5.1 Example 1: The passing grade program (p.118)

### 5.2 Example 2: Testing the unique method (p.122)

### 5.3 Example 3: Testing the indexOf method (p.124)

### 5.4 Example 4: Testing the Basket class (p.129)

### 5.5 Example 5: Creating complex domain objects (p.136)

### 5.6 Property-based testing in the real world (p.137)

#### 5.6.1 Example-based testing vs. property-based testing (p.137)

#### 5.6.2 Common issues in property-based tests (p.138)

#### 5.6.3 Creativity is key (p.139)

### 5.7 Exercises (p.139)

### 5.8 Summary (p.139)

## 6 Test doubles and mocks (p.141)

### 6.0 Introduction [auto-generated] (p.141)

### 6.1 Dummies, fakes, stubs, spies, and mocks (p.143)

#### 6.1.1 Dummy objects (p.143)

#### 6.1.2 Fake objects (p.144)

#### 6.1.3 Stubs (p.144)

#### 6.1.4 Mocks (p.144)

#### 6.1.5 Spies (p.144)

### 6.2 An introduction to mocking frameworks (p.145)

#### 6.2.1 Stubbing dependencies (p.145)

#### 6.2.2 Mocks and expectations (p.150)

#### 6.2.3 Capturing arguments (p.153)

#### 6.2.4 Simulating exceptions (p.157)

### 6.3 Mocks in the real world (p.158)

#### 6.3.0 Introduction [auto-generated] (p.158)

#### 6.3.1 The disadvantages of mocking (p.159)

#### 6.3.2 What to mock and what not to mock (p.160)

#### 6.3.3 Date and time wrappers (p.164)

#### 6.3.4 Mocking types you do not own (p.166)

#### 6.3.5 What do others say about mocking? (p.168)

### 6.4 Exercises (p.169)

### 6.5 Summary (p.170)

## 7 Designing for testability (p.172)

### 7.0 Introduction [auto-generated] (p.172)

### 7.1 Separating infrastructure code from domain code (p.173)

### 7.2 Dependency injection and controllability (p.181)

### 7.3 Making your classes and methods observable (p.184)

#### 7.3.1 Example 1: Introducing methods to facilitate assertions (p.184)

#### 7.3.2 Example 2: Observing the behavior of void methods (p.186)

### 7.4 Dependency via class constructor or value via method parameter? (p.189)

### 7.5 Designing for testability in the real world (p.191)

#### 7.5.0 Introduction [auto-generated] (p.191)

#### 7.5.1 The cohesion of the class under test (p.192)

#### 7.5.2 The coupling of the class under test (p.193)

#### 7.5.3 Complex conditions and testability (p.193)

#### 7.5.4 Private methods and testability (p.193)

#### 7.5.5 Static methods, singletons, and testability (p.194)

#### 7.5.6 The Hexagonal Architecture and mocks as a design technique (p.194)

#### 7.5.7 Further reading about designing for testability (p.195)

### 7.6 Exercises (p.195)

### 7.7 Summary (p.196)

## 8 Test-driven development (p.198)

### 8.0 Introduction [auto-generated] (p.198)

### 8.1 Our first TDD session (p.199)

### 8.2 Reflecting on our first TDD experience (p.206)

### 8.3 TDD in the real world (p.208)

#### 8.3.1 To TDD or not to TDD? (p.208)

#### 8.3.2 TDD 100% of the time? (p.209)

#### 8.3.3 Does TDD work for all types of applications and domains? (p.209)

#### 8.3.4 What does the research say about TDD? (p.209)

#### 8.3.5 Other schools of TDD (p.211)

#### 8.3.6 TDD and proper testing (p.212)

### 8.4 Exercises (p.212)

### 8.5 Summary (p.214)

## 9 Writing larger tests (p.215)

### 9.0 Introduction [auto-generated] (p.215)

### 9.1 When to use larger tests (p.216)

#### 9.1.1 Testing larger components (p.216)

#### 9.1.2 Testing larger components that go beyond our code base (p.224)

### 9.2 Database and SQL testing (p.229)

#### 9.2.1 What to test in a SQL query (p.229)

#### 9.2.2 Writing automated tests for SQL queries (p.231)

#### 9.2.3 Setting up infrastructure for SQL tests (p.236)

#### 9.2.4 Best practices (p.238)

### 9.3 System tests (p.239)

#### 9.3.1 An introduction to Selenium (p.239)

#### 9.3.2 Designing page objects (p.242)

#### 9.3.3 Patterns and best practices (p.251)

### 9.4 Final notes on larger tests (p.254)

#### 9.4.1 How do all the testing techniques fit? (p.254)

#### 9.4.2 Perform cost/benefit analysis (p.255)

#### 9.4.3 Be careful with methods that are covered but not tested (p.255)

#### 9.4.4 Proper code infrastructure is key (p.255)

#### 9.4.5 DSLs and tools for stakeholders to write tests (p.256)

#### 9.4.6 Testing other types of web systems (p.256)

### 9.5 Exercises (p.256)

### 9.6 Summary (p.257)

## 10 Test code quality (p.258)

### 10.0 Introduction [auto-generated] (p.258)

### 10.1 Principles of maintainable test code (p.259)

#### 10.1.1 Tests should be fast (p.259)

#### 10.1.2 Tests should be cohesive, independent, and isolated (p.259)

#### 10.1.3 Tests should have a reason to exist (p.260)

#### 10.1.4 Tests should be repeatable and not flaky (p.260)

#### 10.1.5 Tests should have strong assertions (p.261)

#### 10.1.6 Tests should break if the behavior changes (p.261)

#### 10.1.7 Tests should have a single and clear reason to fail (p.262)

#### 10.1.8 Tests should be easy to write (p.262)

#### 10.1.9 Tests should be easy to read (p.262)

#### 10.1.10 Tests should be easy to change and evolve (p.266)

### 10.2 Test smells (p.267)

#### 10.2.1 Excessive duplication (p.267)

#### 10.2.2 Unclear assertions (p.268)

#### 10.2.3 Bad handling of complex or external resources (p.268)

#### 10.2.4 Fixtures that are too general (p.269)

#### 10.2.5 Sensitive assertions (p.270)

### 10.3 Exercises (p.272)

### 10.4 Summary (p.275)

## 11 Wrapping up the book (p.276)

### 11.1 Although the model looks linear, iterations are fundamental (p.276)

### 11.2 Bug-free software development: Reality or myth? (p.277)

### 11.3 Involve your final user (p.278)

### 11.4 Unit testing is hard in practice (p.278)

### 11.5 Invest in monitoring (p.279)

### 11.6 What’s next? (p.280)

# Appendix—Answers to exercises (p.281)

## 12. Chapter 1 (p.281)

## 13. Chapter 2 (p.282)

## 14. Chapter 3 (p.283)

## 15. Chapter 4 (p.285)

## 16. Chapter 5 (p.285)

## 17. Chapter 6 (p.286)

## 18. Chapter 7 (p.286)

## 19. Chapter 8 (p.287)

## 20. Chapter 9 (p.287)

## 21. Chapter 10 (p.288)

# References (p.289)

# index (p.295)

## A (p.295)

## B (p.295)

## C (p.295)

## D (p.296)

## E (p.297)

## F (p.297)

## G (p.297)

## H (p.297)

## I (p.297)

## L (p.297)

## M (p.298)

## N (p.298)

## O (p.298)

## P (p.298)

## R (p.299)

## S (p.299)

## T (p.300)

## U (p.300)

## V (p.300)

## W (p.300)

## X (p.300)