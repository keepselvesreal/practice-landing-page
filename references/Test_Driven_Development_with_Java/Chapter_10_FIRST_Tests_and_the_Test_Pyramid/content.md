Line 1: 
Line 2: --- 페이지 198 ---
Line 3: 10
Line 4: FIRST Tests and the 
Line 5: Test Pyramid
Line 6: So far in this book, we’ve seen the value of writing unit tests that run quickly and give repeatable 
Line 7: results. Called FIRST tests, these provide rapid feedback on our design. They are the gold standard 
Line 8: of unit tests. We’ve also seen how the hexagonal architecture helps us design our code in a way that 
Line 9: gets the maximum amount covered by FIRST unit tests. But we’ve also limited ourselves to testing 
Line 10: only our domain model – the core of our application logic. We simply have no tests covering how our 
Line 11: domain model behaves once it connects to the outside world.
Line 12: In this chapter, we will cover all the other kinds of tests that we need. We will introduce the test 
Line 13: pyramid, which is a way of thinking about the different kinds of tests needed, and how many of each 
Line 14: we should have. We’ll discuss what each kind of test covers and useful techniques and tools to help. 
Line 15: We’ll also bring the whole system together by introducing CI/CD pipelines and test environments, 
Line 16: outlining the critical role they play in combining code components to create a system for our end users.
Line 17: In this chapter, we’re going to cover the following main topics:
Line 18: •	 The test pyramid
Line 19: •	 Unit tests – FIRST tests
Line 20: •	 Integration tests
Line 21: •	 End-to-end and user acceptance tests
Line 22: •	 CI/CD pipelines and test environments
Line 23: •	 Wordz – integration test for our database
Line 24: Technical requirements
Line 25: The code for this chapter can be found at https://github.com/PacktPublishing/Test-
Line 26: Driven-Development-with-Java/tree/main/chapter10.
Line 27: To run this code, we will need to install the open source Postgres database locally.
Line 28: 
Line 29: --- 페이지 199 ---
Line 30: FIRST Tests and the Test Pyramid
Line 31: 176
Line 32: To install Postgres, do the following:
Line 33: 1.	
Line 34: Go to https://www.postgresql.org/download/ in your browser.
Line 35: 2.	
Line 36: Click on the correct installer for your operating system:
Line 37: Figure 10.1 – Postgres installer selection
Line 38: 3.	
Line 39: Follow the instructions for your operating system.
Line 40: The test pyramid
Line 41: A very useful way of thinking about different kinds of tests is by using the test pyramid. It is a simple 
Line 42: graphical representation of the different kinds of tests we need around our code and the relative 
Line 43: numbers of each. This section introduces the key ideas behind the test pyramid.
Line 44: The test pyramid in graphic form looks as follows:
Line 45: Figure 10.2 – The test pyramid
Line 46: 
Line 47: --- 페이지 200 ---
Line 48: The test pyramid
Line 49: 177
Line 50: We can see from the previous graphic that tests are divided into four layers. We have unit tests at the 
Line 51: bottom. Integration tests are layered on top of those. The pyramid is completed by end-to-end and 
Line 52: user acceptance tests at the top. The graphic shows unit tests in our system are the highest in number, 
Line 53: with fewer integration tests and the least number of acceptance tests.
Line 54: Some of these kinds of tests are new to this book. Let’s define what they are:
Line 55: •	 Unit tests
Line 56: These are familiar. They are the FIRST tests we have been using up until now. One defining 
Line 57: feature of these tests is that they do not require the presence of any external systems, such as 
Line 58: databases or payment processors.
Line 59: •	 Integration tests
Line 60: These tests verify that a software component is correctly integrated with an external system, 
Line 61: such as a database. These tests are slow and critically dependent on the external environment 
Line 62: being available and correctly set up for our test.
Line 63: •	 End-to-end tests
Line 64: These are the broadest of all tests. An end-to-end test represents something very close to the end 
Line 65: user experience. This test is performed against all the real components of the system – possibly 
Line 66: in test environments with test data – using the same commands as a real user would use.
Line 67: •	 User acceptance tests
Line 68: This is where the real system is tested as a user would use it. Here, we can confirm that the final 
Line 69: system is fit for purpose, according to the requirements the user has given us.
Line 70: It’s not obvious at first why having fewer tests of any kind would be an advantage. After all, everything 
Line 71: up until now in this book has positively praised the value of testing. Why do we not simply have all 
Line 72: the tests? The answer is a pragmatic one: not all tests are created equal. They don’t all offer equal value 
Line 73: to us as developers.
Line 74: The reason for the shape of this pyramid is to reflect the practical value of each layer of testing. Unit 
Line 75: tests written as FIRST tests are fast and repeatable. If we could build a system out of only these unit 
Line 76: tests, we surely would. But unit tests do not exercise every part of our code base. Specifically, they do 
Line 77: not exercise connections from our code to the outside world. Nor do they exercise our application in 
Line 78: the same way as a user would use it. As we progress up through the layers of testing, we move away 
Line 79: from testing the internal components of our software and move toward testing how it interacts with 
Line 80: external systems and, ultimately, the end user of our application.
Line 81: The test pyramid is about balance. It aims to create layers of tests that achieve the following:
Line 82: •	 Run as quickly as possible
Line 83: •	 Cover as much code as possible
Line 84: 
Line 85: --- 페이지 201 ---
Line 86: FIRST Tests and the Test Pyramid
Line 87: 178
Line 88: •	 Prevent as many defects as possible
Line 89: •	 Minimize duplication of the test effort
Line 90: In the following sections, we will look at a breakdown of the tests involved at each layer of the test 
Line 91: pyramid. We’ll consider the strengths and weaknesses of each kind of test, allowing us to understand 
Line 92: what the test pyramid is guiding us toward.
Line 93: Unit tests – FIRST tests
Line 94: In this section, we’re going to look at the base of the test pyramid, which consists of unit tests. We’ll 
Line 95: examine why this layer is critical to success.
Line 96: By now, we’re very familiar with FIRST unit tests. The preceding chapters have covered these in detail. 
Line 97: They are the gold standard of unit tests. They are fast to run. They are repeatable and reliable. They 
Line 98: run isolated from each other, so we can run one, or run many and run them in any order we choose. 
Line 99: FIRST tests are the powerhouses of TDD, enabling us to work with a rapid feedback loop as we code. 
Line 100: Ideally, all our code would fall under this feedback loop. It provides a fast, efficient way to work. At 
Line 101: every step, we can execute code and prove to ourselves that it is working as we intended. As a helpful 
Line 102: byproduct, by writing tests that exercise each possible desirable behavior in our code, we will end up 
Line 103: exercising every possible code path. We will get 100% meaningful test coverage of code under unit 
Line 104: tests when we work in this way.
Line 105: Because of their advantages, unit tests form the bedrock of our testing strategy. They are represented 
Line 106: as the base of the test pyramid.
Line 107: Unit tests have advantages and limitations, as summarized in the following table:
Line 108: Advantages
Line 109: Limitations
Line 110: These are the fastest-running tests and provide 
Line 111: the fastest possible feedback loop for our code.
Line 112: The smaller scope of these tests means that having 
Line 113: all unit tests pass is no guarantee that the system 
Line 114: as a whole is working correctly.
Line 115: Stable and repeatable, having no dependencies 
Line 116: on things outside of our control.
Line 117: They can be written with too strong a tie to 
Line 118: implementation details, making future additions 
Line 119: and refactoring difficult.
Line 120: Can provide very detailed coverage of a specific 
Line 121: set of logic. Locate defects accurately.
Line 122: Not helpful for testing interactions with 
Line 123: external systems.
Line 124: Table 10.1 – Unit test advantages and disadvantages
Line 125: In any system, we expect to have the largest number of tests at the unit level. The test pyramid represents 
Line 126: this graphically.
Line 127: 
Line 128: --- 페이지 202 ---
Line 129: Integration tests
Line 130: 179
Line 131: We can’t achieve full coverage by using unit tests alone in the real world but we can improve our 
Line 132: situation. By applying the hexagonal architecture to our application, we can get the majority of code 
Line 133: under unit tests. Our fast-running unit tests can cover a lot of ground like this and provide a lot of 
Line 134: confidence in our application logic. We can get as far as knowing that if the external systems behave 
Line 135: as we expect them to, our domain layer code will be able to correctly handle every use case we have 
Line 136: thought about.
Line 137: The test position when using unit tests alone is shown in the following diagram:
Line 138: Figure 10.3 – Unit tests cover the domain model
Line 139: Unit tests only test components of our domain model. They do not test external systems, nor do they 
Line 140: use external systems. They rely on test doubles to simulate our external systems for us. This gives us 
Line 141: advantages in development cycle speed but has the drawback that our connections to those external 
Line 142: systems remain untested. If we have a piece of unit-tested code that accesses a repository interface, we 
Line 143: know that its logic works with a stub repository. Its internal logic will even have 100% test coverage 
Line 144: and this will be valid. But we won’t know if it will work with the real repository yet.
Line 145: The adapter layer code is responsible for those connections, and it is not tested at the unit test level. To 
Line 146: test this layer, we’re going to need a different approach to testing. We will need to test what happens 
Line 147: when our domain layer code is integrated with actual external systems.
Line 148: The next section looks at how we test these external systems adapters using a kind of testing known 
Line 149: as integration tests.
Line 150: Integration tests
Line 151: In this section, we’re going to look at the next layer up in the test pyramid: integration testing. We’ll 
Line 152: see why it’s important, review helpful tools, and understand the role of integration testing in the 
Line 153: overall scheme of things.
Line 154: Integration tests exist to test that our code will successfully integrate with external systems. Our core 
Line 155: application logic is tested by unit tests, which, by design, do not interact with external systems. This 
Line 156: means that we need to test behavior with those external systems at some point.
Line 157: 
Line 158: --- 페이지 203 ---
Line 159: FIRST Tests and the Test Pyramid
Line 160: 180
Line 161: Integration tests are the second layer up in the test pyramid. They have advantages and limitations, 
Line 162: as summarized in the following table:
Line 163: Advantages
Line 164: Limitations
Line 165: Test that software components interact correctly 
Line 166: when connected
Line 167: Require test environments to be set up 
Line 168: and maintained
Line 169: Provide a closer simulation of the software 
Line 170: system as it will be used live
Line 171: Tests run more slowly than unit tests
Line 172: Susceptible to problems in the test environment, 
Line 173: such as incorrect data or network connection failures
Line 174: Table 10.2 – Integration test advantages and disadvantages
Line 175: There should be fewer integration tests than unit tests. Ideally, far fewer. While unit tests avoided 
Line 176: many problems of testing external systems by using test doubles, integration tests must now face those 
Line 177: challenges. By nature, they are more difficult to set up. They can be less repeatable. They generally run 
Line 178: more slowly than unit tests do, as they wait for responses from external systems.
Line 179: To give a sense of this, a typical system might have thousands of unit tests and hundreds of acceptance 
Line 180: tests. In between, we have several integration tests. Many integration tests point to a design opportunity. 
Line 181: We can refactor the code so that our integration test is pushed down to being a unit test or promoted 
Line 182: to being an acceptance test.
Line 183: Another reason to have fewer integration tests is due to flaky tests.  A flaky test is a nickname given to 
Line 184: a test that sometimes passes and sometimes fails. When it fails, it is due to some problem interacting 
Line 185: with the external system and not a defect in the code we are testing. Such a failure is called a false 
Line 186: negative test result – a result that can mislead us.
Line 187: Flaky tests are a nuisance precisely because we cannot immediately tell the root cause of the failure. 
Line 188: Without diving into error logs, we only know that the test failed. This leads to developers learning to 
Line 189: ignore these failed tests, often choosing to re-run the test suite several times until the flaky test passes. 
Line 190: The problem here is that we are training developers to have less faith in their tests. We are training 
Line 191: them to ignore test failures. This is not a good place to be.
Line 192: What should an integration test cover?
Line 193: In our design so far, we have decoupled external systems from our domain code using the Dependency 
Line 194: Inversion Principle. We have created an interface defining how we use that external system. There 
Line 195: will be some implementation of this interface, which is what our integration test will be covering. In 
Line 196: hexagonal architecture terms, this is an adapter.
Line 197: This adapter should only contain the minimum amount of code necessary to interact with the external 
Line 198: system in a way that satisfies our interface. It should have no application logic in it at all. That should 
Line 199: 
Line 200: --- 페이지 204 ---
Line 201: Integration tests
Line 202: 181
Line 203: be inside the domain layer and covered by unit tests. We call this a thin adapter, doing only enough 
Line 204: work to adapt to the external system. This means our integration test is nicely limited in scope.
Line 205: We can represent the scope of an integration test like so:
Line 206: Figure 10.4 – Integration tests cover the adapter layer
Line 207: Integration tests only test the adapter layer components, those pieces of code that directly interact with 
Line 208: external systems, such as databases and web endpoints. The integration test will create an instance 
Line 209: of the adapter under test and arrange for it to connect to a version of the external service. This is 
Line 210: important. We’re still not connecting to the production services yet. Until the integration test passes, 
Line 211: we’re not sure that our adapter code works correctly. So, we don’t want to access real services just yet. 
Line 212: We also want to have that extra level of control over these services. We want to be able to safely and 
Line 213: easily create test accounts and fake data to use with our adapter. That means we need a collection of 
Line 214: live-like services and databases to use. That means they have to live and run somewhere.
Line 215: Test environments are the name given to the arrangement of external systems we use in integration 
Line 216: tests. It is an environment for running web services and data sources, specifically for testing.
Line 217: A test environment enables our code to connect to test versions of real external systems. It’s one step 
Line 218: closer to production readiness, compared to the unit test level. There are some challenges involved 
Line 219: in using test environments, however. Let’s look into the good practices for testing integrations with 
Line 220: databases and web services.
Line 221: Testing database adapters
Line 222: The basic approach to testing a database adapter is to set up a database server in the test environment 
Line 223: and get the code under test to connect to it. The integration test will preload a known dataset into the 
Line 224: database as part of its Arrange step. The test then runs the code that interacts with the database in 
Line 225: the Act step. The Assert step can inspect the database to see if expected database changes happened.
Line 226: The biggest challenge in testing a database is that it remembers data. Now, this might seem a little 
Line 227: obvious, as that is the entire point of using a database in the first place. But it conflicts with one of the 
Line 228: goals of testing: to have isolated, repeatable tests. As an example, if our test created a new user account 
Line 229: 
Line 230: --- 페이지 205 ---
Line 231: FIRST Tests and the Test Pyramid
Line 232: 182
Line 233: for user testuser1 and that was stored in the database, we would have a problem running that test 
Line 234: again. It would not be able to create testuser1 and instead would receive a user already exists error.
Line 235: There are different approaches to overcoming this problem, each with trade-offs:
Line 236: •	 Delete all data from the database before and after each test case
Line 237: This approach preserves the isolation of our tests, but it is slow. We have to recreate the test 
Line 238: database schema before every test.
Line 239: •	 Delete all data before and after the full set of adapter tests run
Line 240: We delete data less often, allowing several related tests to run against the same database. This 
Line 241: loses test isolation due to the stored data, as the database will not be in the state expected at 
Line 242: the start of the next test. We have to run tests in a particular order, and they must all pass, to 
Line 243: avoid spoiling the database state for the next test. This is not a good approach.
Line 244: •	 Use randomized data
Line 245: Instead of creating testuser1 in our test, we randomize names. So, on one run, we might get 
Line 246: testuser-cfee-0a9b-931f. On the next run, the randomly chosen username would 
Line 247: be something else. The state stored in the database will not conflict with another run of the 
Line 248: same test. This is another way to preserve test isolation. However, it does mean that tests can 
Line 249: be harder to read. It requires periodic cleanup of the test database.
Line 250: •	 Rollback transactions
Line 251: We can add data required by our tests inside a database transaction. We can roll back the 
Line 252: transaction at the end of the test.
Line 253: •	 Ignore the problem
Line 254: Sometimes, if we work with read-only databases, we can add test data that will never be accessed 
Line 255: by the production code and leave it there. If this works, it is an attractive option requiring no 
Line 256: extra effort.
Line 257: Tools such as database-rider, available from https://database-rider.github.io/getting-
Line 258: started/, assist by providing library code to connect to databases and initialize them with test data.
Line 259: Testing web services
Line 260: A similar approach is used to test the integration with web services. A test version of the web service 
Line 261: is set to run in the test environment. The adapter code is set to connect to this test version of the web 
Line 262: service, instead of the real version. Our integration test can then examine how the adapter code behaves. 
Line 263: There might be additional web APIs on the test service to allow inspection by the assertions in our test.
Line 264: Again, the disadvantages are a slower running test and the risk of flaky tests due to issues as trivial 
Line 265: as network congestion.
Line 266: 
Line 267: --- 페이지 206 ---
Line 268: Integration tests
Line 269: 183
Line 270: Sandbox APIs
Line 271: Sometimes, hosting our own local service might be impossible, or at least undesirable. Third-party 
Line 272: vendors are usually unwilling to release test versions of their service for us to use in our test environment. 
Line 273: Instead, they typically offer a sandbox API. This is a version of their service that the third party hosts, 
Line 274: not us. It is disconnected from their production systems. This sandbox allows us to create test accounts 
Line 275: and test data, safe from affecting anything real in production. It will respond to our requests as their 
Line 276: production versions will respond, but without taking any action such as taking payment. Consider 
Line 277: them test simulators for real services.
Line 278: Consumer-driven contract testing
Line 279: A useful approach to testing interactions with web services is called consumer-driven contract testing. 
Line 280: We consider our code as having a contract with the external service. We agree to call certain API 
Line 281: functions on the external service, supplying data in the form required. We need the external service 
Line 282: to respond to us predictably, with data in a known format and well-understood status codes. This 
Line 283: forms a contract between the two parties – our code and the external service API.
Line 284: Consumer-driven contract testing involves two components, based on that contract, often using code 
Line 285: generated by tools. This is represented in the following figure:
Line 286: Figure 10.5 – Consumer-driven contract testing
Line 287: The preceding diagram shows that we’ve captured the expected interactions with an external service 
Line 288: as an API contract. Our adapter for that service will be coded to implement that API contract. When 
Line 289: using consumer-driven contract testing, we end up with two tests, which test either side of that contract. 
Line 290: If we consider a service to be a black box, we have a public interface presented by the black box, and 
Line 291: an implementation, whose details are hidden inside that black box. A contract test is two tests. One 
Line 292: test confirms that the outside interface is compatible with our code. The other test confirms that the 
Line 293: implementation of that interface works and gives the expected results.
Line 294: 
Line 295: --- 페이지 207 ---
Line 296: FIRST Tests and the Test Pyramid
Line 297: 184
Line 298: A typical contract test will need two pieces of code:
Line 299: •	 A stub of the external service: A stub of the external service is generated. If we are calling a 
Line 300: payment processor, this stub simulates the payment processor locally. This allows us to use it 
Line 301: as a test double for the payment processor service as we write our adapter code. We can write 
Line 302: an integration test against our adapter, configuring it to call this stub. This allows us to test our 
Line 303: adapter code logic without accessing the external system. We can verify that the adapter sends 
Line 304: the correct API calls to that external service and handles the expected responses correctly.
Line 305: •	 A replay of a set of calls to the real external service: The contract also allows us to run tests 
Line 306: against the real external service – possibly in sandbox mode. We’re not testing the functionality 
Line 307: of the external service here – we assume that the service provider has done that. Instead, we 
Line 308: are verifying that what we believe about its API is true. Our adapter has been coded to make 
Line 309: certain API calls in certain orders. This test verifies that this assumption is correct. If the test 
Line 310: passes, we know that our understanding of the external service API was correct and also that 
Line 311: it has not changed. If this test was previously working but now fails, that would be an early 
Line 312: indication that the external service has changed its API. We would then need to update our 
Line 313: adapter code to follow that.
Line 314: One recommended tool for doing this is called Pact, available at https://docs.pact.io. Read 
Line 315: the guides there for more details on this interesting technique.
Line 316: We’ve seen that integration tests get us one step nearer to production. In the next section, we look at 
Line 317: the final level of testing in the test pyramid, which is the most live-like so far: user acceptance tests.
Line 318: End-to-end and user acceptance tests
Line 319: In this section, we will progress to the top of the test pyramid. We’ll review what end-to-end and user 
Line 320: acceptance tests are and what they add to unit and integration testing.
Line 321: At the top of the test pyramid lies two similar kinds of tests called end-to-end tests and user acceptance 
Line 322: tests. Technically, they are the same kind of test. In each case, we start up the software fully configured 
Line 323: to run in its most live-like test environment, or possibly in production. The idea is that the system is 
Line 324: tested as a whole from one end to the other.
Line 325: One specific use of an end-to-end test is for user acceptance testing (UAT). Here, several key end-to-
Line 326: end test scenarios are run. If they all pass, the software is declared fit for purpose and accepted by the 
Line 327: users. This is often a contractual stage in commercial development, where the buyer of the software 
Line 328: formally agrees that the development contract has been satisfied. It’s still end-to-end testing that is 
Line 329: being used to determine that, with cherry-picked test cases.
Line 330: These tests have advantages and limitations, as summarized in the following table:
Line 331: .
Line 332: 
Line 333: --- 페이지 208 ---
Line 334: End-to-end and user acceptance tests
Line 335: 185
Line 336: Advantages
Line 337: Limitations
Line 338: Most comprehensive testing of functionality 
Line 339: available. We are testing at the same level that a 
Line 340: user of our system – either person or machine 
Line 341: – would experience our system.
Line 342: Slowest tests to run.
Line 343: Tests at this level are concerned with pure 
Line 344: behavior as observed from outside the system. 
Line 345: We could refactor and rearchitect large parts of 
Line 346: the system and still have these tests protect us.
Line 347: Reliability issues – many problems in the setup and 
Line 348: environment of our system can cause false negative 
Line 349: test failures. This is termed “brittleness” – our 
Line 350: tests are highly dependent on their environment 
Line 351: working correctly. Environments can be broken 
Line 352: due to circumstances beyond our control.
Line 353: Contractually important – these tests are the 
Line 354: essence of what the end user cares about.
Line 355: These are the most challenging of all the tests 
Line 356: to write, due to the extensive environment 
Line 357: setup requirements.
Line 358: Table 10.3 – End-to-end test advantages and disadvantages
Line 359: Acceptance tests having a spot at the top of the pyramid is a reflection that we don’t need many of 
Line 360: them. The majority of our code should now be covered by unit and integration tests, assuring us that 
Line 361: our application logic works, as well as our connections to external systems.
Line 362: The obvious question is what’s left to test? We don’t want to duplicate testing that has already been 
Line 363: done at the unit and integration levels. But we do need some way to validate that the software as a 
Line 364: whole is going to work as expected. This is the job of end-to-end testing. This is where we configure 
Line 365: our software so that it connects to real databases and real external services. Our production code has 
Line 366: passed all the unit tests with test doubles. These test passes suggest our code should work when we 
Line 367: connect these real external services. But should is a wonderful weasel word in software development. 
Line 368: Now, is the time to verify that it does, using an end-to-end test. We can represent the coverage of 
Line 369: these tests using the following diagram:
Line 370: Figure 10.6 – End-to-end/user acceptance tests cover the entire code base
Line 371: 
Line 372: --- 페이지 209 ---
Line 373: FIRST Tests and the Test Pyramid
Line 374: 186
Line 375: End-to-end tests cover the entire code base, both the domain model and the adapter layer. As such, 
Line 376: it repeats testing work already done by unit and integration tests. The main technical aspect we want 
Line 377: to test in end-to-end testing is that our software is configured and wired up correctly. Throughout 
Line 378: this book, we have used dependency inversion and injection to isolate us from external systems. We’ve 
Line 379: created test doubles and injected those. Now, we must create actual production code, the real adapter 
Line 380: layer components that connect to the production systems. We inject those into our system during its 
Line 381: initialization and configuration. This sets the code up to work for real.
Line 382: End-to-end tests will then duplicate a small amount of happy path testing already covered by unit and 
Line 383: integration tests. The purpose here is not to verify the behaviors that we have already tested. Instead, 
Line 384: these tests verify that we have injected the correct production objects, by confirming that the system 
Line 385: as a whole behaves correctly when connected to production services.
Line 386: A user acceptance test builds on this idea by running through key test scenarios considered critical 
Line 387: to accepting the software as complete. These will be end-to-end tests at a technical level. But their 
Line 388: purpose is broader than the technical goal of ensuring our system is correctly configured. They are 
Line 389: more of a legal contractual nature: Have we built what was asked of us? By using the iterative approach 
Line 390: in this book together with its technical practices, there’s a higher chance that we will have done so.
Line 391: Acceptance testing tools
Line 392: Various testing libraries exist to help us write automated acceptance and end-to-end tests. Tasks such 
Line 393: as connecting to a database or calling an HTTP web API are common to this kind of testing. We can 
Line 394: leverage libraries for these tasks, instead of writing code ourselves.
Line 395: The main differentiator among these tools is the way they interact with our software. Some are intended 
Line 396: to simulate a user clicking a desktop GUI, or a browser-based web UI. Others will make HTTP calls 
Line 397: to our software, exercising a web endpoint.
Line 398: Here are a few popular acceptance testing tools to consider:
Line 399: •	 RestEasy
Line 400: A popular tool for testing REST APIs: https://resteasy.dev/
Line 401: •	 RestAssured
Line 402: Another popular tool for testing REST APIs that takes a fluent approach to inspecting JSON 
Line 403: responses: https://rest-assured.io/
Line 404: •	 Selenium
Line 405: A popular tool for testing web UIs through the browser: https://www.selenium.dev/
Line 406: •	 Cucumber
Line 407: Available from https://cucumber.io/. Cucumber allows English language-like descriptions 
Line 408: of tests to be written by domain experts. At least, that’s the theory. I’ve never seen anybody 
Line 409: other than a developer write Cucumber tests in any project I’ve been part of.
Line 410: 
Line 411: --- 페이지 210 ---
Line 412: CI/CD pipelines and test environments
Line 413: 187
Line 414: Acceptance tests form the final piece of the test pyramid and allow our application to be tested 
Line 415: under conditions that resemble the production environment. All that is needed is a way to automate 
Line 416: running all those layers of testing. That’s where CI/CD pipelines come in, and they are the subject of 
Line 417: the next section.
Line 418: CI/CD pipelines and test environments
Line 419: CI/CD pipelines and test environments are an important part of software engineering. They are a 
Line 420: part of the development workflow that takes us from writing code to having systems in the hands of 
Line 421: users. In this section, we’re going to look at what the terms mean and how we can use these ideas in 
Line 422: our projects.
Line 423: What is a CI/CD pipeline?
Line 424: Let’s start with defining the terms:
Line 425: •	 CI stands for continuous integration
Line 426: Integration is where we take individual software components and join them together to make 
Line 427: a whole. CI means we do this all the time as we write new code.
Line 428: •	 CD stands for either continuous delivery or continuous deployment
Line 429: We’ll cover the difference later, but in both cases, the idea is that we are taking the latest and 
Line 430: greatest version of our integrated software and delivering it to a stakeholder. The goal of 
Line 431: continuous delivery is that we could – if we wanted to – deploy every single code change to 
Line 432: production with a single click of a button.
Line 433: It’s important to note that CI/CD is an engineering discipline – not a set of tools. However we achieve 
Line 434: it, CI/CD has the goal of growing a single system that is always in a usable state.
Line 435: Why do we need continuous integration?
Line 436: In terms of the test pyramid, the reason we need CI/CD is to pull all the testing together. We need a 
Line 437: mechanism to build the whole of our software, using the latest code. We need to run all the tests and 
Line 438: ensure they all pass before we can package and deploy the code. If any tests fail, we know the code is 
Line 439: not suitable for deployment. To ensure we get fast feedback, we must run the tests in order of fastest 
Line 440: to slowest. Our CI pipeline will run unit tests first, followed by integration tests, followed by end-to-
Line 441: end and acceptance tests. If any tests fail, the build will produce a report of test failures for that stage, 
Line 442: then stop the build. If all the tests pass, we package our code up ready for deployment.
Line 443: More generally, the idea of integration is fundamental to building software, whether we work alone 
Line 444: or in a development team. When working alone, following the practices in this book, we’re building 
Line 445: software out of several building blocks. Some we have made ourselves, while for others, we’ve selected 
Line 446: a suitable library component and used that. We’ve also written adapters – components that allow us 
Line 447: 
Line 448: --- 페이지 211 ---
Line 449: FIRST Tests and the Test Pyramid
Line 450: 188
Line 451: to access external systems. All of that needs integrating – bringing together as a whole – to turn our 
Line 452: lines of code into a working system.
Line 453: When working in a team, integration is even more important. We need to not only bring together 
Line 454: the pieces we have written but also all the other pieces written by the rest of our team. Integrating 
Line 455: work in progress from colleagues is urgent. We end up building on what others have already written. 
Line 456: As we work outside of the main integrated code base, there is a risk of not including the latest design 
Line 457: decisions and pieces of reusable code.
Line 458: The following figure shows the goal of CI:
Line 459: Figure 10.7 – Continuous integration
Line 460: The motivation behind CI was to avoid the classic waterfall development trap, where a team wrote 
Line 461: code as isolated individuals while following a plan and only integrated it at the end. Many times, that 
Line 462: integration failed to produce working software. There was often some misunderstanding or missing 
Line 463: piece that meant components did not fit together. At this late stage of a waterfall project, mistakes 
Line 464: are expensive to fix.
Line 465: It’s not just big teams and big projects that suffer from this. My turning point was while writing a 
Line 466: flight simulator game for Britain’s RAF Red Arrows display team. Two of us worked on that game to 
Line 467: a common API we had agreed on. When we first attempted to integrate our parts – at 03:00 A.M., in 
Line 468: front of the company managing director, of course – the game ran for about three frames and then 
Line 469: crashed. Oops! Our lack of CI provided an embarrassing lesson. It would have been good to know 
Line 470: that was going to happen a lot earlier, especially without the managing director watching.
Line 471: 
Line 472: --- 페이지 212 ---
Line 473: CI/CD pipelines and test environments
Line 474: 189
Line 475: Why do we need continuous delivery?
Line 476: If CI is all about keeping our software components together as an ever-growing whole, then CD is 
Line 477: about getting that whole into the hands of people who care about it. The following figure illustrates CD:
Line 478: Figure 10.8 – Continuous delivery
Line 479: Delivering a stream of value to end users is a core tenet of agile development. No matter which flavor 
Line 480: of agile methodology you use, getting features into the hands of users has always been the goal. We 
Line 481: want to deliver usable features at regular, short intervals. Doing this provides three benefits:
Line 482: •	 Users get the value they want
Line 483: End users don’t care about our development process. They only care about getting solutions 
Line 484: to their problems. Whether that’s the problem of being entertained while waiting for an Uber 
Line 485: ride, or the problem of paying everyone’s wages in a multinational business, our user just wants 
Line 486: their problem gone. Getting valuable features to our users becomes a competitive advantage.
Line 487: •	 We gain valuable user feedback
Line 488: Yes, that’s what I asked for – but it isn’t what I meant! That is extremely valuable user feedback 
Line 489: that agile approaches deliver. Once an end user sees the feature as we have implemented it, 
Line 490: sometimes, it becomes clear that it isn’t quite solving their problem. We can correct this quickly.
Line 491: •	 Aligns the code base and development team
Line 492: To pull off this feat, you do need to have your team and workflows together. You can’t effectively 
Line 493: do this unless your workflow results in known working software being continuously available 
Line 494: as a single whole.
Line 495: 
Line 496: --- 페이지 213 ---
Line 497: FIRST Tests and the Test Pyramid
Line 498: 190
Line 499: Continuous delivery or continuous deployment?
Line 500: Exact definitions of these terms seem to vary, but we can think of them like this:
Line 501: •	 Continuous delivery
Line 502: We deliver software to internal stakeholders, such as product owners and QA engineers
Line 503: •	 Continuous deployment
Line 504: We deliver software into production and to end users
Line 505: Out of the two, continuous deployment sets a much higher bar. It requires that once we integrate 
Line 506: code into our pipeline, that code is ready to go live – into production, to real users. This is, of course, 
Line 507: hard. It needs top-class test automation to give us confidence that our code is ready to deploy. It 
Line 508: also benefits from having a fast rollback system in production – some means of quickly reverting a 
Line 509: deployment if we discover a defect not covered by our tests. Continuous deployment is the ultimate 
Line 510: workflow. For all who achieve it, deploying new code last thing on Friday simply holds no fear. Well, 
Line 511: maybe a little less fear.
Line 512: Practical CI/CD pipelines
Line 513: Most projects use a CI tool to handle the sequencing chores. Popular tools are provided by Jenkins, 
Line 514: GitLab, CircleCI, Travis CI, and Azure DevOps. They all work similarly, executing separate build 
Line 515: stages sequentially. That’s where the name pipeline comes from – it resembles a pipe being loaded 
Line 516: at one end with the next build stage and coming out of the other end of the pipe, as shown in the 
Line 517: following diagram:
Line 518: Figure 10.9 – Stages in a CI pipeline
Line 519: A CI pipeline comprises the following steps:
Line 520: 1.	
Line 521: Source control: Having a common location in which to store the code is essential to CI/CD. 
Line 522: It is the place where code gets integrated. The pipeline starts here, by pulling down the latest 
Line 523: version of the source code and performing a clean build. This prevents errors caused by older 
Line 524: versions of code being present on the computer.
Line 525: 2.	
Line 526: Build: In this step, we run a build script to download all the required libraries, compile all the 
Line 527: code, and link it together. The output is something that can be executed, typically a single Java 
Line 528: archive .jar file, to run on the JVM.
Line 529: 
Line 530: --- 페이지 214 ---
Line 531: CI/CD pipelines and test environments
Line 532: 191
Line 533: 3.	
Line 534: Static code analysis: Linters and other analysis tools check the source code for stylistic violations, 
Line 535: such as variable length and naming conventions. The development team can choose to fail the 
Line 536: build when specific code issues are detected by static analysis.
Line 537: 4.	
Line 538: Unit tests: All the unit tests are run against the built code. If any fail, the pipeline stops. Test 
Line 539: failure messages are reported.
Line 540: 5.	
Line 541: Integration tests: All integration tests are run against the built code. If any fail, the pipeline is 
Line 542: stopped and error messages are reported.
Line 543: 6.	
Line 544: Acceptance tests: All acceptance tests are run against the built code. If all tests pass, the code 
Line 545: is considered to be working and ready for delivery/deployment.
Line 546: 7.	
Line 547: Delivery packaging: The code is packaged up into a suitable form for delivery. For Java web 
Line 548: services, this may well be a single Java archive .jar file containing an embedded web server.
Line 549: What happens next depends on the needs of the project. The packaged code may be deployed to 
Line 550: production automatically or it may simply be placed in some internal repository, for access by product 
Line 551: owners and QA engineers. Formal deployment would then happen later, after quality gatekeeping.
Line 552: Test environments
Line 553: One obvious problem caused by needing a CI pipeline to run integration tests is having a place to 
Line 554: run those tests. Ordinarily, in production, our application integrates with external systems such as 
Line 555: databases and payment providers. When we run our CI pipeline, we do not want our code to process 
Line 556: payments or write to production databases. Yet we do want to test that the code could integrate with 
Line 557: those things, once we configure it to connect to those real systems.
Line 558: The solution is to create a test environment. These are collections of databases and simulated external 
Line 559: systems that lie under our control. If our code needs to integrate with a database of user details, we 
Line 560: can create a copy of that user database and run it locally. During testing, we can arrange for our code 
Line 561: to connect to this local database, instead of the production version. External payment providers often 
Line 562: provide a sandbox API. This is a version of their service that, again, does not connect to any of their 
Line 563: real customers. It features simulated behavior for their service. In effect, it is an external test double.
Line 564: This kind of setup is called a live-like or staging environment. It allows our code to be tested with 
Line 565: more realistic integration. Our unit tests use stubs and mocks. Our integration tests can now use these 
Line 566: richer test environments.
Line 567: Advantages and challenges of using test environments
Line 568: Test environments offer both advantages and disadvantages, as summarized in the following table:
Line 569: 
Line 570: --- 페이지 215 ---
Line 571: FIRST Tests and the Test Pyramid
Line 572: 192
Line 573: Advantages
Line 574: Challenges
Line 575: The environment is self-contained
Line 576: We can create it and destroy it at will. It will 
Line 577: not affect production systems.
Line 578: Not production environments
Line 579: No matter how live-like we make them, these 
Line 580: environments are simulations. The risk is that our 
Line 581: fake environments give us false positives – tests that 
Line 582: pass only because they are using fake data. This can 
Line 583: give us false confidence, leading us to deploy code that 
Line 584: will fail in production.
Line 585: The real test happens when we set our code live. Always.
Line 586: More realistic than stubs
Line 587: The environment gets us one step closer 
Line 588: to testing under production loads 
Line 589: and conditions.
Line 590: Extra effort to create and maintain
Line 591: More development work is needed to set these 
Line 592: environments up and keep them in step with the 
Line 593: test code.
Line 594: Check assumptions about external systems
Line 595: Third-party sandbox environments allow 
Line 596: us to confirm that our code uses the latest, 
Line 597: correct API, as published by the supplier.
Line 598: Privacy concerns
Line 599: Simply copying over a chunk of production data isn’t 
Line 600: good enough for a test environment. If that data contains 
Line 601: personally identifiable information (PII) as defined 
Line 602: by GDPR or HIPAA, then we can’t legally use it directly. 
Line 603: We have to create an extra step to anonymize that 
Line 604: data or generate pseudo-realistic random test data. 
Line 605: Neither is trivial.
Line 606: Table 10.4 – Test environments advantages and challenges
Line 607: Testing in production
Line 608: I can hear the gasps already! Running our tests in production is generally a terrible idea. Our tests 
Line 609: might introduce fake orders that our production system treats as real ones. We may have to add test 
Line 610: user accounts, which can present a security risk. Worse still, because we are in a testing phase, there 
Line 611: is a very good chance that our code does not work yet. This can cause all sorts of problems – all while 
Line 612: connected to production systems.
Line 613: Despite these concerns, sometimes, things must be tested in production. Big data companies such 
Line 614: as Google and Meta both have things that can only be tested live due to the sheer scale of their data. 
Line 615: There is no way a meaningful live-like test environment can be created; it will simply be too small. 
Line 616: What can we do in cases like this?
Line 617: The approach is to mitigate the risks. Two techniques are valuable here: blue-green deployment and 
Line 618: traffic partitioning.
Line 619: 
Line 620: --- 페이지 216 ---
Line 621: CI/CD pipelines and test environments
Line 622: 193
Line 623: Blue-green deployment
Line 624: Blue-green deployment is a deployment technique designed for the rapid rollback of failed deployments. 
Line 625: It works by dividing the production servers into two groups. They are referred to as blue and green, 
Line 626: chosen as they are neutral colors that both denote success. Our production code will be running on 
Line 627: one group of servers at any one time. Let’s say we are currently running on the blue group. Our next 
Line 628: deployment will then be to the green group. This is shown in the following diagram:
Line 629: Figure 10.10 – Blue-green deployment
Line 630: Once the code has been deployed to the green group, we switch over the production configuration to 
Line 631: connect to green group servers. We retain the previous working production code on the blue servers. 
Line 632: If our testing goes well against the green group, then we’re done. Production is now working with the 
Line 633: latest green group code. If the testing fails, we revert that configuration to connect to the blue servers 
Line 634: once again. It’s a fast rollback system that enables our experimentation.
Line 635: Traffic partitioning
Line 636: In addition to blue-green deployment, we can limit the amount of traffic that we send to our test 
Line 637: servers. Instead of flipping production to wholly use the new code under test, we can simply send 
Line 638: a small percentage of user traffic there. So, 99% of users might be routed to our blue servers, which 
Line 639: we know to work. 1% can be routed to our new code under test in the green servers, as shown in the 
Line 640: following diagram:
Line 641: 
Line 642: --- 페이지 217 ---
Line 643: FIRST Tests and the Test Pyramid
Line 644: 194
Line 645: Figure 10.11 – Traffic partitioning
Line 646: If defects are discovered, only 1% of users will be affected before we revert to 100% blue servers. This 
Line 647: gives us a rapid rollback, mitigating problems in production caused by a failed deployment.
Line 648: We’ve now covered the roles of different kinds of tests and seen how they fit into a coherent system 
Line 649: known as the test pyramid. In the next section, we’ll apply some of this knowledge to our Wordz 
Line 650: application by writing an integration test.
Line 651: Wordz – integration test for our database
Line 652: In this section, we’ll review an integration test for our Wordz application to get a feel for what they look 
Line 653: like. We’ll cover the details of writing these tests and setting up the test tools in Chapter 14, Driving 
Line 654: the Database Layer, and Chapter 15, Driving the Web Layer.
Line 655: Fetching a word from the database
Line 656: As part of our earlier design work, we identified that Wordz would need a place to store the candidate 
Line 657: words to be guessed. We defined an interface called WordRepository to isolate us from the details 
Line 658: of storage. At that iteration, we had only got as far as defining one method on the interface:
Line 659: public interface WordRepository {
Line 660: String fetchWordByNumber( int wordNumber );
Line 661: }
Line 662: 
Line 663: --- 페이지 218 ---
Line 664: Wordz – integration test for our database
Line 665: 195
Line 666: The implementation of this WordRepository interface will access the database and return a word 
Line 667: given its wordNumber. We will defer implementing this to Chapter 14, Driving the Database Layer. 
Line 668: For now, let’s take an early look at what the integration test will look like, at a high level. The test uses 
Line 669: open source libraries to help write the test, and to provide the database. We’ve chosen the following:
Line 670: •	 An open source library called database-rider (available from https://database-
Line 671: rider.github.io/getting-started/) as a test tool
Line 672: •	 Postgres, a popular open source relational database, to store our data
Line 673: Here is the test code:
Line 674: package com.wordz.adapters.db;
Line 675: import com.github.database.rider.core.api.connection.
Line 676: ConnectionHolder;
Line 677: import com.github.database.rider.core.api.dataset.DataSet;
Line 678: import com.github.database.rider.junit5.api.DBRider;
Line 679: import org.junit.jupiter.api.BeforeEach;
Line 680: import org.junit.jupiter.api.Test;
Line 681: import org.postgresql.ds.PGSimpleDataSource;
Line 682: import javax.sql.DataSource;
Line 683: import static org.assertj.core.api.Assertions.assertThat;
Line 684: @DBRider
Line 685: public class WordRepositoryPostgresTest {
Line 686:     private DataSource dataSource;
Line 687:     @BeforeEach
Line 688:     void beforeEachTest() {
Line 689:         var ds = new PGSimpleDataSource();
Line 690:         ds.setServerNames(new String[]{"localhost"});
Line 691:         ds.setDatabaseName("wordzdb");
Line 692:         ds.setUser("ciuser");
Line 693:         ds.setPassword("cipassword");
Line 694:         this.dataSource = ds;
Line 695: 
Line 696: --- 페이지 219 ---
Line 697: FIRST Tests and the Test Pyramid
Line 698: 196
Line 699:     }
Line 700:     private final ConnectionHolder connectionHolder = () ->
Line 701:         dataSource.getConnection();
Line 702:     @Test
Line 703:     @DataSet("adapters/data/wordTable.json")
Line 704:     public void fetchesWord()  {
Line 705:         var adapter = new WordRepositoryPostgres(dataSource);
Line 706:         String actual = adapter.fetchWordByNumber(27);
Line 707:         assertThat(actual).isEqualTo("ARISE");
Line 708:     }
Line 709: }
Line 710: The fetchesWord() test method is marked by the @DataSet annotation. This annotation is 
Line 711: provided by the database-rider test framework and it forms the Arrange step of our test. It specifies a 
Line 712: file of known test data that the framework will load into the database before the test runs. The data file 
Line 713: is located underneath the root folder of src/test/resources. The parameter in the annotation 
Line 714: gives the rest of the path. In our case, the file will be located at src/test/resources/adapters/
Line 715: data/wordTable.json. Its content looks like this:
Line 716: {
Line 717:   "WORD": [
Line 718:     {
Line 719:       "id": 1,
Line 720:       "number": 27,
Line 721:       "text": "ARISE"
Line 722:     }
Line 723:   ]
Line 724: }
Line 725: This JSON file tells the database-rider framework that we would like to insert a single row into 
Line 726: a database table named WORD, with column values of 1, 27, and ARISE.
Line 727: We’re not going to write the adapter code to make this test pass just yet. There are several steps we 
Line 728: would need to take to get this test to compile, including downloading various libraries and getting 
Line 729: the Postgres database up and running. We’ll cover these steps in detail in Chapter 14, Driving the 
Line 730: Database Layer.
Line 731: 
Line 732: --- 페이지 220 ---
Line 733: Summary
Line 734: 197
Line 735: The overview of this integration test code is that it is testing a new class called 
Line 736: WordRepositoryPostgres that we will write. That class will contain the database access code. 
Line 737: We can see the tell-tale JDBC object, javax.sql.DataSource, which represents a database 
Line 738: instance. This is the clue that we are testing integration with a database. We can see new annotations 
Line 739: from the database testing library: @DBRider and @DataSet. Finally, we can see something instantly 
Line 740: recognizable – the Arrange, Act, and Assert steps of a test:
Line 741: 1.	
Line 742: The Arrange step creates a WordRepositoryPostgres object, which will contain our 
Line 743: database code. It works with the database-rider library’s @DataSet annotation to put 
Line 744: some known data into the database before the test runs.
Line 745: 2.	
Line 746: The Act step calls the fetchWordByNumber() method, passing in the numeric wordNumber 
Line 747: we want to test. This number aligns with the contents of the wordTable.json file.
Line 748: 3.	
Line 749: The Assert step confirms the expected word, ARISE, is returned from the database.
Line 750: As we can see, integration tests aren’t so different from unit tests in essence.
Line 751: Summary
Line 752: In this chapter, we’ve seen how the test pyramid is a system that organizes our testing efforts, keeping 
Line 753: FIRST unit tests firmly as the foundation for all we do, but not neglecting other testing concerns. First, 
Line 754: we introduced the ideas of integration and acceptance testing as ways of testing more of our system. 
Line 755: Then, we looked at how the techniques of CI and CD keep our software components brought together 
Line 756: and ready to release at frequent intervals. We’ve seen how to bring the whole build process together 
Line 757: using CI pipelines, possibly going on to CD. We’ve made a little progress on Wordz by writing an 
Line 758: integration test for the WordRepositoryPostgres adapter, setting us up to write the database 
Line 759: code itself.
Line 760: In the next chapter, we’ll take a look at the role of manual testing in our projects. It’s clear by now that 
Line 761: we automate as much testing as we can, meaning that the role of manual testing no longer means 
Line 762: following huge test plans. Yet, manual testing is still very valuable. How has the role changed? We’ll 
Line 763: review that next.
Line 764: Questions and answers
Line 765: The following are some questions and their answers regarding this chapter’s material:
Line 766: 1.	
Line 767: Why is the test pyramid represented as a pyramid shape?
Line 768: The shape depicts a broad foundation of many unit tests. It shows layers of testing above that 
Line 769: exercise a closer approximation to the final, integrated system. It also shows that we expect 
Line 770: fewer tests at those higher levels of integration.
Line 771: 2.	
Line 772: What are the trade-offs between unit, integration, and acceptance tests?
Line 773: 	 Unit tests: Fast, repeatable. Don’t test connections to external systems.
Line 774: 
Line 775: --- 페이지 221 ---
Line 776: FIRST Tests and the Test Pyramid
Line 777: 198
Line 778: 	 Integration tests: Slower, sometimes unrepeatable. They test the connection to the external system.
Line 779: 	 Acceptance tests: Slowest of all. They can be flaky but offer the most comprehensive tests 
Line 780: of the whole system.
Line 781: 3.	
Line 782: Does the test pyramid guarantee correctness?
Line 783: No. Testing can only ever reveal the presence of a defect, never the absence of one. The value 
Line 784: of extensive testing is in how many defects we avoid putting into production.
Line 785: 4.	
Line 786: Does the test pyramid only apply to object-oriented programming?
Line 787: No. This strategy of test coverage applies to any programming paradigm. We can write code 
Line 788: using any paradigm - object-oriented, functional, procedural, or declarative. The various 
Line 789: kinds of tests only depend on whether our code accesses external systems or makes up purely 
Line 790: internal components.
Line 791: 5.	
Line 792: Why don’t we prefer end-to-end tests, given they test the whole system?
Line 793: End-to-end tests run slowly. They depend directly on having either production databases 
Line 794: and web services running, or a test environment running containing test versions of those 
Line 795: things. The network connections required, and things such as database setup, can result in 
Line 796: tests giving us false negative results. They fail because of the environment, not because the 
Line 797: code was incorrect. Because of these reasons, we engineer our system to make maximum use 
Line 798: of fast, repeatable unit tests.
Line 799: Further reading
Line 800: To learn more about the topics that were covered in this chapter, take a look at the following resources:
Line 801: •	 Introduction to consumer-driven contract testing
Line 802: Pact.io produce a popular open source contract testing tool that’s available on their website, 
Line 803: https://docs.pact.io. The website features an explanatory video and a useful introduction 
Line 804: to the benefits of contract-driven testing.
Line 805: •	 Database-rider database testing library
Line 806: An open source database integration testing library that works with JUnit5. It is available 
Line 807: from https://database-rider.github.io/getting-started/.
Line 808: •	 Modern Software Engineering, Dave Farley, ISBN 978-0137314911
Line 809: This book explains in detail the reasons behind CD and various technical practices such as 
Line 810: trunk-based development to help us achieve that. Highly recommended.
Line 811: •	 Minimum CD
Line 812: Details on what is needed for CD: https://minimumcd.org/minimumcd/.