# The Art of Unit Testing, Third Edition (p.The Art of Unit Testing, Third Edition)

# Praise for the second edition (p.i)

# contents (p.vii)

# foreword to the second edition (p.xiv)

# foreword to the first edition (p.xvi)

# preface (p.xviii)

# acknowledgments (p.xx)

# about this book (p.xxi)

## What’s new in the third edition (p.xxi)

## Who should read this book (p.xxii)

## How this book is organized: A road map (p.xxii)

## Code conventions and downloads (p.xxiii)

## Software requirements (p.xxiii)

## liveBook discussion forum (p.xxiii)

## Other projects by Roy Osherove (p.xxiv)

## Other projects by Vladimir Khorikov (p.xxiv)

# about the authors (p.xxv)

# about the cover illustration (p.xxvi)

# Part 1—Getting started (p.1)

## 1 The basics of unit testing (p.3)

### 1.0 Introduction [auto-generated] (p.3)

### 1.1 The first step (p.5)

### 1.2 Defining unit testing, step by step (p.5)

### 1.3 Entry points and exit points (p.6)

### 1.4 Exit point types (p.11)

### 1.5 Different exit points, different techniques (p.12)

### 1.6 A test from scratch (p.12)

### 1.7 Characteristics of a good unit test (p.15)

#### 1.7.1 What is a good unit test? (p.15)

#### 1.7.2 A unit test checklist (p.16)

### 1.8 Integration tests (p.17)

### 1.9 Finalizing our definition (p.21)

### 1.10 Test-driven development (p.22)

#### 1.10.0 Introduction [auto-generated] (p.22)

#### 1.10.1 TDD: Not a substitute for good unit tests (p.24)

#### 1.10.2 Three core skills needed for successful TDD (p.25)

### 1.11 Summary (p.26)

## 2 A first unit test (p.28)

### 2.0 Introduction [auto-generated] (p.28)

### 2.1 Introducing Jest (p.29)

#### 2.1.1 Preparing our environment (p.29)

#### 2.1.2 Preparing our working folder (p.29)

#### 2.1.3 Installing Jest (p.30)

#### 2.1.4 Creating a test file (p.30)

#### 2.1.5 Executing Jest (p.31)

### 2.2 The library, the assert, the runner, and the reporter (p.33)

### 2.3 What unit testing frameworks offer (p.34)

#### 2.3.0 Introduction [auto-generated] (p.34)

#### 2.3.1 The xUnit frameworks (p.36)

#### 2.3.2 xUnit, TAP, and Jest structures (p.36)

### 2.4 Introducing the Password Verifier project (p.37)

### 2.5 The first Jest test for verifyPassword (p.37)

#### 2.5.0 Introduction [auto-generated] (p.37)

#### 2.5.1 The Arrange-Act-Assert pattern (p.38)

#### 2.5.2 Testing the test (p.39)

#### 2.5.3 USE naming (p.39)

#### 2.5.4 String comparisons and maintainability (p.40)

#### 2.5.5 Using describe() (p.40)

#### 2.5.6 Structure implying context (p.41)

#### 2.5.7 The it() function (p.42)

#### 2.5.8 Two Jest flavors (p.42)

#### 2.5.9 Refactoring the production code (p.43)

### 2.6 Trying the beforeEach() route (p.45)

#### 2.6.0 Introduction [auto-generated] (p.45)

#### 2.6.1 beforeEach() and scroll fatigue (p.47)

### 2.7 Trying the factory method route (p.49)

#### 2.7.0 Introduction [auto-generated] (p.49)

#### 2.7.1 Replacing beforeEach() completely with factory methods (p.50)

### 2.8 Going full circle to test() (p.52)

### 2.9 Refactoring to parameterized tests (p.52)

### 2.10 Checking for expected thrown errors (p.55)

### 2.11 Setting test categories (p.56)

### 2.12 Summary (p.57)

# Part 2—Core techniques (p.59)

## 3 Breaking dependencies with stubs (p.61)

### 3.0 Introduction [auto-generated] (p.61)

### 3.1 Types of dependencies (p.62)

### 3.2 Reasons to use stubs (p.64)

### 3.3 Generally accepted design approaches to stubbing (p.66)

#### 3.3.1 Stubbing out time with parameter injection (p.66)

#### 3.3.2 Dependencies, injections, and control (p.68)

### 3.4 Functional injection techniques (p.69)

#### 3.4.1 Injecting a function (p.69)

#### 3.4.2 Dependency injection via partial application (p.70)

### 3.5 Modular injection techniques (p.70)

### 3.6 Moving toward objects with constructor functions (p.73)

### 3.7 Object-oriented injection techniques (p.74)

#### 3.7.1 Constructor injection (p.74)

#### 3.7.2 Injecting an object instead of a function (p.76)

#### 3.7.3 Extracting a common interface (p.79)

### 3.8 Summary (p.81)

## 4 Interaction testing using mock objects (p.83)

### 4.0 Introduction [auto-generated] (p.83)

### 4.1 Interaction testing, mocks, and stubs (p.84)

### 4.2 Depending on a logger (p.85)

### 4.3 Standard style: Introduce parameter refactoring (p.87)

### 4.4 The importance of differentiating between mocks and stubs (p.88)

### 4.5 Modular-style mocks (p.89)

#### 4.5.0 Introduction [auto-generated] (p.89)

#### 4.5.1 Example of production code (p.90)

#### 4.5.2 Refactoring the production code in a modular injection style (p.91)

#### 4.5.3 A test example with modular-style injection (p.92)

### 4.6 Mocks in a functional style (p.92)

#### 4.6.1 Working with a currying style (p.92)

#### 4.6.2 Working with higher-order functions and not currying (p.93)

### 4.7 Mocks in an object-oriented style (p.94)

#### 4.7.1 Refactoring production code for injection (p.94)

#### 4.7.2 Refactoring production code with interface injection (p.96)

### 4.8 Dealing with complicated interfaces (p.98)

#### 4.8.1 Example of a complicated interface (p.98)

#### 4.8.2 Writing tests with complicated interfaces (p.99)

#### 4.8.3 Downsides of using complicated interfaces directly (p.100)

#### 4.8.4 The interface segregation principle (p.101)

### 4.9 Partial mocks (p.101)

#### 4.9.1 A functional example of a partial mock (p.101)

#### 4.9.2 An object-oriented partial mock example (p.102)

### 4.10 Summary (p.103)

## 5 Isolation frameworks (p.104)

### 5.0 Introduction [auto-generated] (p.104)

### 5.1 Defining isolation frameworks (p.105)

#### 5.1.1 Choosing a flavor: Loose vs. typed (p.105)

### 5.2 Faking modules dynamically (p.106)

#### 5.2.0 Introduction [auto-generated] (p.106)

#### 5.2.1 Some things to notice about Jest’s API (p.108)

#### 5.2.2 Consider abstracting away direct dependencies (p.109)

### 5.3 Functional dynamic mocks and stubs (p.109)

### 5.4 Object-oriented dynamic mocks and stubs (p.110)

#### 5.4.1 Using a loosely typed framework (p.110)

#### 5.4.2 Switching to a type-friendly framework (p.112)

### 5.5 Stubbing behavior dynamically (p.114)

#### 5.5.1 An object-oriented example with a mock and a stub (p.114)

#### 5.5.2 Stubs and mocks with substitute.js (p.116)

### 5.6 Advantages and traps of isolation frameworks (p.117)

#### 5.6.0 Introduction [auto-generated] (p.117)

#### 5.6.1 You don’t need mock objects most of the time (p.118)

#### 5.6.2 Unreadable test code (p.118)

#### 5.6.3 Verifying the wrong things (p.118)

#### 5.6.4 Having more than one mock per test (p.119)

#### 5.6.5 Overspecifying the tests (p.119)

### 5.7 Summary (p.119)

## 6 Unit testing asynchronous code (p.121)

### 6.0 Introduction [auto-generated] (p.121)

### 6.1 Dealing with async data fetching (p.122)

#### 6.1.0 Introduction [auto-generated] (p.122)

#### 6.1.1 An initial attempt with an integration test (p.123)

#### 6.1.2 Waiting for the act (p.124)

#### 6.1.3 Integration testing of async/await (p.124)

#### 6.1.4 Challenges with integration tests (p.125)

### 6.2 Making our code unit-test friendly (p.125)

#### 6.2.0 Introduction [auto-generated] (p.125)

#### 6.2.1 Extracting an entry point (p.126)

#### 6.2.2 The Extract Adapter pattern (p.131)

### 6.3 Dealing with timers (p.138)

#### 6.3.1 Stubbing timers out with monkey-patching (p.138)

#### 6.3.2 Faking setTimeout with Jest (p.139)

### 6.4 Dealing with common events (p.141)

#### 6.4.1 Dealing with event emitters (p.141)

#### 6.4.2 Dealing with click events (p.142)

### 6.5 Bringing in the DOM testing library (p.144)

### 6.6 Summary (p.145)

# Part 3—The test code (p.147)

## 7 Trustworthy tests (p.149)

### 7.0 Introduction [auto-generated] (p.149)

### 7.1 How to know you trust a test (p.150)

### 7.2 Why tests fail (p.150)

#### 7.2.0 Introduction [auto-generated] (p.150)

#### 7.2.1 A real bug has been uncovered in the production code (p.151)

#### 7.2.2 A buggy test gives a false failure (p.151)

#### 7.2.3 The test is out of date due to a change in functionality (p.152)

#### 7.2.4 The test conflicts with another test (p.152)

#### 7.2.5 The test is flaky (p.153)

### 7.3 Avoiding logic in unit tests (p.153)

#### 7.3.1 Logic in asserts: Creating dynamic expected values (p.153)

#### 7.3.2 Other forms of logic (p.155)

#### 7.3.3 Even more logic (p.156)

### 7.4 Smelling a false sense of trust in passing tests (p.156)

#### 7.4.0 Introduction [auto-generated] (p.156)

#### 7.4.1 Tests that don’t assert anything (p.157)

#### 7.4.2 Not understanding the tests (p.157)

#### 7.4.3 Mixing unit tests and flaky integration tests (p.158)

#### 7.4.4 Testing multiple exit points (p.158)

#### 7.4.5 Tests that keep changing (p.160)

### 7.5 Dealing with flaky tests (p.161)

#### 7.5.0 Introduction [auto-generated] (p.161)

#### 7.5.1 What can you do once you’ve found a flaky test? (p.163)

#### 7.5.2 Preventing flakiness in higher-level tests (p.163)

### 7.6 Summary (p.164)

## 8 Maintainability (p.165)

### 8.0 Introduction [auto-generated] (p.165)

### 8.1 Changes forced by failing tests (p.166)

#### 8.1.1 The test is not relevant or conflicts with another test (p.166)

#### 8.1.2 Changes in the production code’s API (p.166)

#### 8.1.3 Changes in other tests (p.169)

### 8.2 Refactoring to increase maintainability (p.173)

#### 8.2.1 Avoid testing private or protected methods (p.173)

#### 8.2.2 Keep tests DRY (p.175)

#### 8.2.3 Avoid setup methods (p.175)

#### 8.2.4 Use parameterized tests to remove duplication (p.176)

### 8.3 Avoid overspecification (p.177)

#### 8.3.1 Internal behavior overspecification with mocks (p.177)

#### 8.3.2 Exact outputs and ordering overspecification (p.179)

### 8.4 Summary (p.183)

# Part 4—Design and process (p.185)

## 9 Readability (p.187)

### 9.0 Introduction [auto-generated] (p.187)

### 9.1 Naming unit tests (p.188)

### 9.2 Magic values and naming variables (p.189)

### 9.3 Separating asserts from actions (p.190)

### 9.4 Setting up and tearing down (p.191)

### 9.5 Summary (p.192)

## 10 Developing a testing strategy (p.194)

### 10.0 Introduction [auto-generated] (p.194)

### 10.1 Common test types and levels (p.195)

#### 10.1.0 Introduction [auto-generated] (p.195)

#### 10.1.1 Criteria for judging a test (p.196)

#### 10.1.2 Unit tests and component tests (p.196)

#### 10.1.3 Integration tests (p.197)

#### 10.1.4 API tests (p.198)

#### 10.1.5 E2E/UI isolated tests (p.198)

#### 10.1.6 E2E/UI system tests (p.199)

### 10.2 Test-level antipatterns (p.199)

#### 10.2.1 The end-to-end-only antipattern (p.199)

#### 10.2.2 The low-level-only test antipattern (p.202)

#### 10.2.3 Disconnected low-level and high-level tests (p.204)

### 10.3 Test recipes as a strategy (p.205)

#### 10.3.1 How to write a test recipe (p.205)

#### 10.3.2 When do I write and use a test recipe? (p.207)

#### 10.3.3 Rules for a test recipe (p.207)

### 10.4 Managing delivery pipelines (p.208)

#### 10.4.1 Delivery vs. discovery pipelines (p.208)

#### 10.4.2 Test layer parallelization (p.209)

### 10.5 Summary (p.211)

## 11 Integrating unit testing into the organization (p.213)

### 11.1 Steps to becoming an agent of change (p.213)

#### 11.1.0 Introduction [auto-generated] (p.213)

#### 11.1.1 Be prepared for the tough questions (p.214)

#### 11.1.2 Convince insiders: Champions and blockers (p.214)

#### 11.1.3 Identify possible starting points (p.215)

### 11.2 Ways to succeed (p.216)

#### 11.2.0 Introduction [auto-generated] (p.216)

#### 11.2.1 Guerrilla implementation (bottom-up) (p.217)

#### 11.2.2 Convincing management (top-down) (p.217)

#### 11.2.3 Experiments as door openers (p.217)

#### 11.2.4 Get an outside champion (p.218)

#### 11.2.5 Make progress visible (p.219)

#### 11.2.6 Aim for specific goals, metrics, and KPIs (p.220)

#### 11.2.7 Realize that there will be hurdles (p.222)

### 11.3 Ways to fail (p.222)

#### 11.3.0 Introduction [auto-generated] (p.222)

#### 11.3.1 Lack of a driving force (p.223)

#### 11.3.2 Lack of political support (p.223)

#### 11.3.3 Ad hoc implementations and first impressions (p.223)

#### 11.3.4 Lack of team support (p.224)

### 11.4 Influence factors (p.224)

### 11.5 Tough questions and answers (p.226)

#### 11.5.1 How much time will unit testing add to the current process? (p.226)

#### 11.5.2 Will my QA job be at risk because of unit testing? (p.227)

#### 11.5.3 Is there proof that unit testing helps? (p.228)

#### 11.5.4 Why is the QA department still finding bugs? (p.228)

#### 11.5.5 We have lots of code without tests: Where do we start? (p.228)

#### 11.5.6 What if we develop a combination of software and hardware? (p.229)

#### 11.5.7 How can we know we don’t have bugs in our tests? (p.229)

#### 11.5.8 Why do I need tests if my debugger shows that my code works? (p.229)

#### 11.5.9 What about TDD? (p.229)

### 11.6 Summary (p.229)

## 12 Working with legacy code (p.231)

### 12.0 Introduction [auto-generated] (p.231)

### 12.1 Where do you start adding tests? (p.232)

### 12.2 Choosing a selection strategy (p.234)

#### 12.2.1 Pros and cons of the easy-first strategy (p.234)

#### 12.2.2 Pros and cons of the hard-first strategy (p.234)

### 12.3 Writing integration tests before refactoring (p.235)

#### 12.3.0 Introduction [auto-generated] (p.235)

#### 12.3.1 Read Michael Feathers’ book on legacy code (p.236)

#### 12.3.2 Use CodeScene to investigate your production code (p.236)

### 12.4 Summary (p.236)

# appendix—Monkey-patching functions and modules (p.238)

## A.1 An obligatory warning (p.238)

## A.2 Monkey-patching functions, globals, and possible issues (p.239)

### 12.5 A.2.1 Monkey-patching a function the Jest way (p.241)

### 12.6 A.2.2 Jest spies (p.241)

### 12.7 A.2.3 spyOn with mockImplementation() (p.241)

## A.3 Ignoring a whole module with Jest is simple (p.242)

## A.4 Faking module behavior in each test (p.243)

### 12.8 A.4.1 Stubbing a module with vanilla require.cache (p.244)

### 12.9 A.4.2 Stubbing custom module data with Jest is complicated (p.246)

### 12.10 A.4.3 Avoid Jest’s manual mocks (p.247)

### 12.11 A.4.4 Stubbing a module with Sinon.js (p.247)

### 12.12 A.4.5 Stubbing a module with testdouble (p.248)

# index (p.251)

## Symbols (p.251)

## A (p.251)

## B (p.252)

## C (p.252)

## D (p.252)

## E (p.253)

## F (p.253)

## G (p.254)

## H (p.254)

## I (p.254)

## J (p.254)

## K (p.255)

## L (p.255)

## M (p.255)

## N (p.256)

## O (p.256)

## P (p.256)

## Q (p.257)

## R (p.257)

## S (p.257)

## T (p.258)

## U (p.259)

## V (p.260)

## W (p.260)

## X (p.260)