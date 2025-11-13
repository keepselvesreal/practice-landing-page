# Cover  (p.Cover)

# Contents (p.ix)

# Foreword (p.xv)

# Preface (p.xvii)

# Acknowledgments (p.xxi)

# About the Authors (p.xxiii)

# Part I: Introduction (p.1)

## 1. Chapter 1: What Is the Point of Test-Driven Development? (p.3)

### 1.1 Software Development as a Learning Process (p.3)

### 1.2 Feedback Is the Fundamental Tool (p.4)

### 1.3 Practices That Support Change (p.5)

### 1.4 Test-Driven Development in a Nutshell (p.6)

### 1.5 The Bigger Picture (p.7)

### 1.6 Testing End-to-End (p.8)

### 1.7 Levels of Testing (p.9)

### 1.8 External and Internal Quality (p.10)

## 2. Chapter 2: Test-Driven Development with Objects (p.13)

### 2.1 A Web of Objects (p.13)

### 2.2 Values and Objects (p.13)

### 2.3 Follow the Messages (p.14)

### 2.4 Tell, Don't Ask (p.17)

### 2.5 But Sometimes Ask (p.17)

### 2.6 Unit-Testing the Collaborating Objects (p.18)

### 2.7 Support for TDD with Mock Objects (p.19)

## 3. Chapter 3: An Introduction to the Tools (p.21)

### 3.1 Stop Me If You've Heard This One Before (p.21)

### 3.2 A Minimal Introduction to JUnit 4 (p.21)

### 3.3 Hamcrest Matchers and assertThat() (p.24)

### 3.4 jMock2: Mock Objects (p.25)

# Part II: The Process of Test-Driven Development (p.29)

## 4. Chapter 4: Kick-Starting the Test-Driven Cycle (p.31)

### 4.1 Introduction (p.31)

### 4.2 First, Test a Walking Skeleton (p.32)

### 4.3 Deciding the Shape of the Walking Skeleton (p.33)

### 4.4 Build Sources of Feedback (p.35)

### 4.5 Expose Uncertainty Early (p.36)

## 5. Chapter 5: Maintaining the Test-Driven Cycle (p.39)

### 5.1 Introduction (p.39)

### 5.2 Start Each Feature with an Acceptance Test (p.39)

### 5.3 Separate Tests That Measure Progress from Those That Catch Regressions (p.40)

### 5.4 Start Testing with the Simplest Success Case (p.41)

### 5.5 Write the Test That You'd Want to Read (p.42)

### 5.6 Watch the Test Fail (p.42)

### 5.7 Develop from the Inputs to the Outputs (p.43)

### 5.8 Unit-Test Behavior, Not Methods (p.43)

### 5.9 Listen to the Tests (p.44)

### 5.10 Tuning the Cycle (p.45)

## 6. Chapter 6: Object-Oriented Style (p.47)

### 6.1 Introduction (p.47)

### 6.2 Designing for Maintainability (p.47)

### 6.3 Internals vs. Peers (p.50)

### 6.4 No And's, Or's, or But's (p.51)

### 6.5 Object Peer Stereotypes (p.52)

### 6.6 Composite Simpler Than the Sum of Its Parts (p.53)

### 6.7 Context Independence (p.54)

### 6.8 Hiding the Right Information (p.55)

### 6.9 An Opinionated View (p.56)

## 7. Chapter 7: Achieving Object-Oriented Design (p.57)

### 7.1 How Writing a Test First Helps the Design (p.57)

### 7.2 Communication over Classification (p.58)

### 7.3 Value Types (p.59)

### 7.4 Where Do Objects Come From? (p.60)

### 7.5 Identify Relationships with Interfaces (p.63)

### 7.6 Refactor Interfaces Too (p.63)

### 7.7 Compose Objects to Describe System Behavior (p.64)

### 7.8 Building Up to Higher-Level Programming (p.65)

### 7.9 And What about Classes? (p.67)

## 8. Chapter 8: Building on Third-Party Code (p.69)

### 8.1 Introduction (p.69)

### 8.2 Only Mock Types That You Own (p.69)

### 8.3 Mock Application Objects in Integration Tests (p.71)

# Part III: A Worked Example (p.73)

## 9. Chapter 9: Commissioning an Auction Sniper (p.75)

### 9.1 To Begin at the Beginning (p.75)

### 9.2 Communicating with an Auction (p.78)

### 9.3 Getting There Safely (p.79)

### 9.4 This Isn't Real (p.81)

## 10. Chapter 10: The Walking Skeleton (p.83)

### 10.1 Get the Skeleton out of the Closet (p.83)

### 10.2 Our Very First Test (p.84)

### 10.3 Some Initial Choices (p.86)

## 11. Chapter 11: Passing the First Test (p.89)

### 11.1 Building the Test Rig (p.89)

### 11.2 Failing and Passing the Test (p.95)

### 11.3 The Necessary Minimum (p.102)

## 12. Chapter 12: Getting Ready to Bid (p.105)

### 12.1 An Introduction to the Market (p.105)

### 12.2 A Test for Bidding (p.106)

### 12.3 The AuctionMessageTranslator (p.112)

### 12.4 Unpacking a Price Message (p.118)

### 12.5 Finish the Job (p.121)

## 13. Chapter 13: The Sniper Makes a Bid (p.123)

### 13.1 Introducing AuctionSniper (p.123)

### 13.2 Sending a Bid (p.126)

### 13.3 Tidying Up the Implementation (p.131)

### 13.4 Defer Decisions (p.136)

### 13.5 Emergent Design (p.137)

## 14. Chapter 14: The Sniper Wins the Auction (p.139)

### 14.1 First, a Failing Test (p.139)

### 14.2 Who Knows about Bidders? (p.140)

### 14.3 The Sniper Has More to Say (p.143)

### 14.4 The Sniper Acquires Some State (p.144)

### 14.5 The Sniper Wins (p.146)

### 14.6 Making Steady Progress (p.148)

## 15. Chapter 15: Towards a Real User Interface (p.149)

### 15.1 A More Realistic Implementation (p.149)

### 15.2 Displaying Price Details (p.152)

### 15.3 Simplifying Sniper Events (p.159)

### 15.4 Follow Through (p.164)

### 15.5 Final Polish (p.168)

### 15.6 Observations (p.171)

## 16. Chapter 16: Sniping for Multiple Items (p.175)

### 16.1 Testing for Multiple Items (p.175)

### 16.2 Adding Items through the User Interface (p.183)

### 16.3 Observations (p.189)

## 17. Chapter 17: Teasing Apart Main (p.191)

### 17.1 Finding a Role (p.191)

### 17.2 Extracting the Chat (p.192)

### 17.3 Extracting the Connection (p.195)

### 17.4 Extracting the SnipersTableModel (p.197)

### 17.5 Observations (p.201)

## 18. Chapter 18: Filling In the Details (p.205)

### 18.1 A More Useful Application (p.205)

### 18.2 Stop When We've Had Enough (p.205)

### 18.3 Observations (p.212)

## 19. Chapter 19: Handling Failure (p.215)

### 19.1 What If It Doesn't Work? (p.215)

### 19.2 Detecting the Failure (p.217)

### 19.3 Displaying the Failure (p.218)

### 19.4 Disconnecting the Sniper (p.219)

### 19.5 Recording the Failure (p.221)

### 19.6 Observations (p.225)

# Part IV: Sustainable Test-Driven Development (p.227)

## 20. Chapter 20: Listening to the Tests (p.229)

### 20.1 Introduction (p.229)

### 20.2 I Need to Mock an Object I Can't Replace (without Magic) (p.230)

### 20.3 Logging Is a Feature (p.233)

### 20.4 Mocking Concrete Classes (p.235)

### 20.5 Don't Mock Values (p.237)

### 20.6 Bloated Constructor (p.238)

### 20.7 Confused Object (p.240)

### 20.8 Too Many Dependencies (p.241)

### 20.9 Too Many Expectations (p.242)

### 20.10 What the Tests Will Tell Us (If We're Listening) (p.244)

## 21. Chapter 21: Test Readability (p.247)

### 21.1 Introduction (p.247)

### 21.2 Test Names Describe Features (p.248)

### 21.3 Canonical Test Structure (p.251)

### 21.4 Streamline the Test Code (p.252)

### 21.5 Assertions and Expectations (p.254)

### 21.6 Literals and Variables (p.255)

## 22. Chapter 22: Constructing Complex Test Data (p.257)

### 22.1 Introduction (p.257)

### 22.2 Test Data Builders (p.258)

### 22.3 Creating Similar Objects (p.259)

### 22.4 Combining Builders (p.261)

### 22.5 Emphasizing the Domain Model with Factory Methods (p.261)

### 22.6 Removing Duplication at the Point of Use (p.262)

### 22.7 Communication First (p.264)

## 23. Chapter 23: Test Diagnostics (p.267)

### 23.1 Design to Fail (p.267)

### 23.2 Small, Focused, Well-Named Tests (p.268)

### 23.3 Explanatory Assertion Messages (p.268)

### 23.4 Highlight Detail with Matchers (p.268)

### 23.5 Self-Describing Value (p.269)

### 23.6 Obviously Canned Value (p.270)

### 23.7 Tracer Object (p.270)

### 23.8 Explicitly Assert That Expectations Were Satisfied (p.271)

### 23.9 Diagnostics Are a First-Class Feature (p.271)

## 24. Chapter 24: Test Flexibility (p.273)

### 24.1 Introduction (p.273)

### 24.2 Test for Information, Not Representation (p.274)

### 24.3 Precise Assertions (p.275)

### 24.4 Precise Expectations (p.277)

### 24.5 "Guinea Pig" Objects (p.284)

# Part V: Advanced Topics (p.287)

## 25. Chapter 25: Testing Persistence (p.289)

### 25.1 Introduction (p.289)

### 25.2 Isolate Tests That Affect Persistent State (p.290)

### 25.3 Make Tests Transaction Boundaries Explicit (p.292)

### 25.4 Testing an Object That Performs Persistence Operations (p.294)

### 25.5 Testing That Objects Can Be Persisted (p.297)

### 25.6 But Database Tests Are S-l-o-w! (p.300)

## 26. Chapter 26: Unit Testing and Threads (p.301)

### 26.1 Introduction (p.301)

### 26.2 Separating Functionality and Concurrency Policy (p.302)

### 26.3 Unit-Testing Synchronization (p.306)

### 26.4 Stress-Testing Passive Objects (p.311)

### 26.5 Synchronizing the Test Thread with Background Threads (p.312)

### 26.6 The Limitations of Unit Stress Tests (p.313)

## 27. Chapter 27: Testing Asynchronous Code (p.315)

### 27.1 Introduction (p.315)

### 27.2 Sampling or Listening (p.316)

### 27.3 Two Implementations (p.318)

### 27.4 Runaway Tests (p.322)

### 27.5 Lost Updates (p.323)

### 27.6 Testing That an Action Has No Effect (p.325)

### 27.7 Distinguish Synchronizations and Assertions (p.326)

### 27.8 Externalize Event Sources (p.326)

# Afterword: A Brief History of Mock Objects (p.329)

# Appendix A: jMock2 Cheat Sheet (p.335)

# Appendix B: Writing a Hamcrest Matcher (p.343)

# Bibliography (p.347)

# Index (p.349)

## A (p.349)

## B (p.350)

## C (p.350)

## D (p.351)

## E (p.351)

## F (p.352)

## G (p.352)

## H (p.352)

## I (p.352)

## J (p.353)

## L (p.353)

## M (p.354)

## N (p.354)

## O (p.355)

## P (p.355)

## Q (p.355)

## R (p.355)

## S (p.356)

## T (p.357)

## U (p.358)

## V (p.358)

## W (p.358)

## X (p.358)