Line 1: 
Line 2: --- 페이지 172 ---
Line 3: 9
Line 4: Hexagonal Architecture –
Line 5: Decoupling External Systems
Line 6: We’ve already learned how to write tests using the arrange, act, and assert template. We’ve also learned 
Line 7: about some software design principles, known as the SOLID principles, that help us break our software 
Line 8: down into smaller components. Finally, we’ve learned how test doubles can stand in for collaborating 
Line 9: components to make FIRST unit tests easier to write. In this chapter, we’re going to combine all those 
Line 10: techniques into a powerful design approach known as the hexagonal architecture.
Line 11: Using this approach, we will benefit from getting more of our application logic under unit tests and 
Line 12: reducing the number of integration and end-to-end tests required. We will build in a natural resilience 
Line 13: to changes outside our application. Development chores such as changing a database supplier will 
Line 14: be simplified, by having fewer places where our code needs to be changed. We will also be able to 
Line 15: unit test across larger units, bringing some tests that require end-to-end testing in other approaches 
Line 16: under unit tests instead.
Line 17: In this chapter, we’re going to cover the following main topics:
Line 18: •	 Why external systems are difficult
Line 19: •	 Dependency inversion to the rescue
Line 20: •	 Abstracting out the external system
Line 21: •	 Writing the domain code
Line 22: •	 Substituting test doubles for external systems
Line 23: •	 Unit testing bigger units
Line 24: •	 Wordz – abstracting the database
Line 25: 
Line 26: --- 페이지 173 ---
Line 27: Hexagonal Architecture –Decoupling External Systems
Line 28: 150
Line 29: Technical requirements
Line 30: The code for this chapter can be found at https://github.com/PacktPublishing/
Line 31: Test-Driven-Development-with-Java/tree/main/chapter09.
Line 32: Why external systems are difficult
Line 33: In this section, we’re going to review the driving force behind the hexagonal architecture approach – 
Line 34: the difficulty of working with external systems. Dependencies on external systems cause problems in 
Line 35: development. The solution leads to a nice design approach.
Line 36: Let’s look at a simple way of handling external systems. The task of our user is to pull a report of this 
Line 37: month’s sales from a database. We will write one piece of code that does exactly that. The software 
Line 38: design looks like this:
Line 39: Figure 9.1 – One piece of code does everything
Line 40: In this design, we have sales data stored in a database in the usual way. We write some code to pull 
Line 41: the report on behalf of our user. It is a single piece of code that does the whole job as a single step. 
Line 42: It will connect to the database, send a query, receive the results, do some processing, and format the 
Line 43: results ready for the user to read.
Line 44: On the plus side, we know this style of coding works. It will achieve its aim of providing that sales 
Line 45: report to the user. On the downside, the code combines three different responsibilities – accessing a 
Line 46: database, performing logic, and formatting a report. It might mix up SQL statements to the database 
Line 47: with html5 tags to make a formatted report. As we saw in a previous chapter, this can make future 
Line 48: code changes in one area ripple out and impact the other areas. Ideally, that should not happen. But 
Line 49: the real challenge is writing a test for this one piece of code. We’ll need to parse and understand 
Line 50: whatever format we send the report to the user in. We’ll also need to work directly with that database.
Line 51: In the following subsections, we’ll review some wider challenges that external systems present to 
Line 52: testing. These include environmental problems, accidental transactions, uncertain data, operating 
Line 53: system calls, and third-party libraries.
Line 54: 
Line 55: --- 페이지 174 ---
Line 56: Why external systems are difficult
Line 57: 151
Line 58: Environmental problems bring trouble
Line 59: The environment that our software runs in often causes challenges. Suppose our code reads data from 
Line 60: a database. Even if the code is correct, it might not be able to read that data, due to problems in the 
Line 61: environment beyond our control. Such problems include the following:
Line 62: •	 Network connection dropped: Many reasons can cause this. Locally, a network cable is pulled 
Line 63: out by mistake. Maybe the database is hosted over the internet somewhere, and our ISP has 
Line 64: dropped the connection.
Line 65: •	 Power failures: A power failure on the database server, or a local network switch is enough to 
Line 66: put the database out of our reach.
Line 67: •	 Equipment limits: Maybe the database server itself has run out of disk space and cannot operate. 
Line 68: Maybe the exact query we have written is hitting the database in a way that takes a long time 
Line 69: to complete, perhaps due to missing indices.
Line 70: Whatever the cause, if our code cannot access the data in the database, it’s not going to work. As this 
Line 71: is a possibility, writing a test for our report generation code is made much harder.
Line 72: Even when our code can access the data in the database, it’s not that easy to work with in testing. 
Line 73: Suppose we write a test that verifies that we can read the production database correctly, by reading a 
Line 74: username. What username would we expect to read? We don’t know, because the test is not in control 
Line 75: of what data gets added. The available usernames will be whatever names were added by real users. 
Line 76: We could make the test add a known test username to the database – but then, we have just created 
Line 77: a fake user that real users can interact with. This is not what we want at all.
Line 78: A database stores data, causing further problems for our tests. Suppose we write a test against a test 
Line 79: database, which begins by writing a test username. If we have run this test before, the test username 
Line 80: will already be stored in the database. Typically, the database will report a duplicate item error and 
Line 81: the test will fail.
Line 82: Tests against databases need cleaning up. Any test data stored must be deleted after the tests have 
Line 83: been completed. If we attempt to delete data after the test has succeeded, the deletion code may never 
Line 84: run if the test fails. We could avoid this by always deleting the data before the test runs. Such tests 
Line 85: will be slow to run.
Line 86: Accidentally triggering real transactions from tests
Line 87: When our code is limited to only accessing a production system, then every time we use that code, 
Line 88: something will happen in production. The payment processor may issue charges. Real bank accounts 
Line 89: may become debited. Alarms may be activated, causing real evacuations. In a famous example from 
Line 90: Hawaii, a system test triggered a real text message saying Hawaii was under missile attack – which it 
Line 91: wasn’t. This is serious stuff.
Line 92: 
Line 93: --- 페이지 175 ---
Line 94: Hexagonal Architecture –Decoupling External Systems
Line 95: 152
Line 96: Hawaii false missile attack warning
Line 97: For details on this example of testing going wrong, see https://en.wikipedia.org/
Line 98: wiki/2018_Hawaii_false_missile_alert.
Line 99: Accidental real transactions can result in real losses to a company. They could end up as losses to 
Line 100: the 3Rs of a business – revenue, reputation, and retention. None of those are good. Our tests mustn’t 
Line 101: accidentally trigger real consequences from production systems.
Line 102: What data should we expect?
Line 103: In our sales report example, the biggest problem with writing a test is that we would need to know 
Line 104: what the correct answer is to the monthly sales report in advance. How do we do that when we are 
Line 105: connected to the production system? The answer will be whatever the sales report says it is. We have 
Line 106: no other way of knowing.
Line 107: The fact that we need the sales report code to be working correctly before we can test that the sales 
Line 108: report code is working correctly is a big problem here! This is a circular dependency we cannot break.
Line 109: Operating system calls and system time
Line 110: Sometimes, our code may need to make calls to the operating system to do its job. Perhaps it needs 
Line 111: to delete all the files in a directory from time to time or it may be dependent on the system time. An 
Line 112: example would be a log file cleanup utility, which runs every Monday at 02:00 A.M. The utility will 
Line 113: delete every file in the /logfiles/ directory.
Line 114: Testing such a utility would be difficult. We would have to wait until 02:00 A.M. on Monday and 
Line 115: verify that all the log files have been deleted. While we could make this work, it isn’t very effective. 
Line 116: It would be nice to find a better approach that allowed us to test anytime we liked, ideally without 
Line 117: deleting any files.
Line 118: Challenges with third-party services
Line 119: A common task in business software is to accept payment from a customer. For that, we inevitably 
Line 120: use a third-party payment processor such as PayPal or Stripe, as two examples. In addition to the 
Line 121: challenges of network connectivity, third-party APIs provide us with further challenges:
Line 122: •	 Service downtime: Many third-party APIs will have a period of scheduled maintenance where 
Line 123: the service is unavailable for a time. That spells “test failed” for us.
Line 124: •	 API changes: Suppose our code uses API version 1 and API version 2 is pushed live. Our 
Line 125: code will still be using version 1 calls, which might no longer work on version 2 of the API. 
Line 126: Now, that is considered rather bad practice – it’s called breaking a published interface – but it 
Line 127: can and does happen. Worse, with our one piece of code, the version 2 changes might cause 
Line 128: changes everywhere in our code.
Line 129: 
Line 130: --- 페이지 176 ---
Line 131: Dependency inversion to the rescue
Line 132: 153
Line 133: •	 Slow responses: If our code makes an API call to an external service, there is always a possibility 
Line 134: that the response will come back later than expected by our code. Our code will fail in some 
Line 135: way usually and cause tests to fail.
Line 136: Plenty of challenges exist when we mix external services and a single monolithic piece of code, 
Line 137: complicating both maintenance and testing. The question is what can we do about it? The next section 
Line 138: looks at how the Dependency Inversion Principle can help us follow a design approach known as a 
Line 139: hexagonal architecture, which makes external systems easier to deal with.
Line 140: Dependency inversion to the rescue
Line 141: In this section, we will review a design approach known as the hexagonal architecture, based on the 
Line 142: SOLID principles we already know. Using this approach allows us to use TDD more effectively across 
Line 143: more of our code base.
Line 144: We learned about the Dependency Inversion Principle previously in this book. We saw that it helps 
Line 145: us isolate some code we wanted to test from the details of its collaborators. We noted that was useful 
Line 146: for testing things that connected to external systems that were outside of our control. We saw how the 
Line 147: single responsibility principle guided us into splitting up software into smaller, more focused tasks.
Line 148: Applying these ideas to our earlier sales reporting example, we would arrive at an improved design, 
Line 149: as shown in the following diagram:
Line 150: Figure 9.2 – Applying SOLID to our sales report
Line 151: The preceding diagram shows how we have applied SOLID principles to splitting up our sales report 
Line 152: code. We have used the single responsibility principle to break down the overall task into three 
Line 153: separate tasks:
Line 154: •	 Formatting the report
Line 155: •	 Calculating the sales total
Line 156: •	 Reading the sales data from the database
Line 157: 
Line 158: --- 페이지 177 ---
Line 159: Hexagonal Architecture –Decoupling External Systems
Line 160: 154
Line 161: This already makes the application a little easier to work with. More importantly, we’ve isolated the 
Line 162: code that calculates the sales total from both the user and the database. This calculation no longer 
Line 163: directly accesses the database. It goes through another piece of code responsible for doing only that. 
Line 164: Likewise, the calculation result isn’t directly formatted and sent to the user. Another piece of code is 
Line 165: responsible for that.
Line 166: We can apply the Dependency Inversion Principle here as well. By inverting the dependencies on 
Line 167: the formatting and database access code, our calculated sales total is now free from knowing any of 
Line 168: their details. We’ve made a significant breakthrough:
Line 169: •	 The calculation code is now fully isolated from the database and formatting
Line 170: •	 We can swap in any piece of code that can access any database
Line 171: •	 We can swap in any piece of code that can format a report
Line 172: •	 We can use test doubles in place of the formatting and database access code
Line 173: The biggest benefit is that we can swap in any piece of code that can access any database, without 
Line 174: changing the calculation code. For example, we could change from a Postgres SQL database to a Mongo 
Line 175: NoSQL database without changing the calculation code. We can use a test double for the database 
Line 176: so that we can test the calculation code as a FIRST unit test. These are very significant advantages, 
Line 177: not just in terms of TDD and testing, but also in terms of how our code is organized. Considering 
Line 178: the one-piece sales report solution to this one, we have moved from pure writing code to software 
Line 179: engineering. We’re thinking beyond just getting code to work and focusing on making code easy to 
Line 180: work with. The next few subsections will look at how we can generalize this approach, resulting in 
Line 181: the hexagonal architecture. We will understand how this approach delivers a logical organization of 
Line 182: code that helps us apply TDD more effectively.
Line 183: Generalizing this approach to the hexagonal architecture
Line 184: This combination of the single responsibility principle and dependency inversion seems to have 
Line 185: brought us some benefits. Could we extend this approach to the entire application and get the same 
Line 186: benefits? Could we find a way to separate all our application logic and data representations from the 
Line 187: constraints of external influence? We most certainly can, and the general form of this design is shown 
Line 188: in the following diagram:
Line 189: 
Line 190: --- 페이지 178 ---
Line 191: Dependency inversion to the rescue
Line 192: 155
Line 193: Figure 9.3 – Hexagonal architecture
Line 194: The preceding diagram shows what happens when we generalize the use of dependency inversion 
Line 195: and single responsibility to an entire application. It is called the hexagonal architecture, also known 
Line 196: as ports and adapters after the original term used by Alastair Cockburn, who first described this 
Line 197: approach. The benefit is that it completely isolates the core logic of our application from the details 
Line 198: of external systems. This helps us with testing that core logic. It also provides a reasonable template 
Line 199: for a well-engineered design for our code.
Line 200: Overview of the hexagonal architecture’s components
Line 201: To provide us with this isolation of our core application logic, the hexagonal architecture divides the 
Line 202: whole program into four spaces:
Line 203: •	 External systems, including web browsers, databases, and other computing services
Line 204: •	 Adapters implement the specific APIs required by the external systems
Line 205: •	 Ports are the abstraction of what our application needs from the external system
Line 206: •	 The domain model contains our application logic, free of external system details
Line 207: The central core of our application is the domain model, surrounded by the support it needs from 
Line 208: external systems. It indirectly uses but is not defined by those external systems. Let’s walk through 
Line 209: each component in the hexagonal architecture in more detail, to understand what each one is and is 
Line 210: not responsible for.
Line 211: 
Line 212: --- 페이지 179 ---
Line 213: Hexagonal Architecture –Decoupling External Systems
Line 214: 156
Line 215: External systems connect to adapters
Line 216: External systems are all the things that live outside of our code base. They include things that the 
Line 217: user directly interacts with, such as the web browser and the console application in the preceding 
Line 218: diagram. They also include data stores, such as both the SQL database and the NoSQL database. 
Line 219: Other examples of common external systems include desktop graphical user interfaces, filesystems, 
Line 220: downstream web service APIs, and hardware device drivers. Most applications will need to interact 
Line 221: with systems like these.
Line 222: In the hexagonal architecture, the core of our application code does not know any details about how 
Line 223: the external systems are interacted with. The responsibility of communicating with external systems 
Line 224: is given to a piece of code known as an adapter.
Line 225: As an example, the following diagram shows how a web browser would connect to our code via a 
Line 226: REST adapter:
Line 227: Figure 9.4 – Browser connecting to a REST adapter
Line 228: In the preceding diagram, we can see the web browser connecting to a REST adapter. This adapter 
Line 229: understands HTTP requests and responses, which are the very core of the web. It also understands the 
Line 230: JSON data format, often using libraries to convert the JSON data into some internal representation 
Line 231: for our code. This adapter will also understand the specific protocol that we will have designed for 
Line 232: our application’s REST API – the precise sequence of HTTP verbs, responses, status codes, and JSON-
Line 233: encoded payload data we come up with as an API.
Line 234: Note
Line 235: Adapters encapsulate all the knowledge our system needs to interact with an external system 
Line 236: – and nothing else. This knowledge is defined by the external system’s specifications. Some of 
Line 237: those may be designed by ourselves.
Line 238: Adapters have the single responsibility of knowing how to interact with an external system. If that 
Line 239: external system changes its public interface, only our adapter will need to change.
Line 240: 
Line 241: --- 페이지 180 ---
Line 242: Dependency inversion to the rescue
Line 243: 157
Line 244: Adapters connect to ports
Line 245: Moving toward the domain model, adapters connect to ports. Ports are part of the domain model. 
Line 246: They abstract away the details of the adapter’s intricate knowledge of its external system. Ports answer 
Line 247: a slightly different question: what do we need that external system for? The ports use the Dependency 
Line 248: Inversion Principle to isolate our domain code from knowing any details about the adapters. They 
Line 249: are written purely in terms of our domain model:
Line 250: Figure 9.5 – Adapters connect to ports
Line 251: The REST adapter described previously encapsulates the details of running a REST API, using 
Line 252: knowledge of HTTP and JSON. It connects to a commands port, which provides our abstraction of 
Line 253: commands coming in from the web – or anywhere else, for that matter. Given our sales report example 
Line 254: earlier, the commands port would include a technology-free way of requesting a sales report. In code, 
Line 255: it might look as simple as this:
Line 256: package com.sales.domain;
Line 257: import java.time.LocalDate;
Line 258: public interface Commands {
Line 259:     SalesReport calculateForPeriod(LocalDate start,
Line 260:                                    LocalDate end);
Line 261: }
Line 262: This code fragment features the following:
Line 263: •	 No references to HttpServletRequest or anything to do with HTTP
Line 264: •	 No references to JSON formats
Line 265: 
Line 266: --- 페이지 181 ---
Line 267: Hexagonal Architecture –Decoupling External Systems
Line 268: 158
Line 269: •	 References to our domain model – SalesReport and java.time.LocalDate
Line 270: •	 The public access modifier, so it can be called from the REST adapter
Line 271: This interface is a port. It gives us a general-purpose way to get a sales report from our application. 
Line 272: Referring to Figure 9.3, we can see that the console adapter also connects to this port, providing the 
Line 273: user with a command-line interface to our application. The reason is that while users can access 
Line 274: our application using different kinds of external systems – the web and the command line – our 
Line 275: application does the same thing in either case. It only supports one set of commands, no matter where 
Line 276: those commands are requested from. Fetching a SalesReport object is just that, no matter which 
Line 277: technology you request it from.
Line 278: Note
Line 279: Ports provide a logical view of what our application needs from an external system, without 
Line 280: constraining how those needs should be met technically.
Line 281: Ports are where we invert dependencies. Ports represent the reason our domain model needs those 
Line 282: external systems. If the adapters represent the how, ports represent the why.
Line 283: Ports connect to our domain model
Line 284: The final step in the chain is connecting to the domain model itself. This is where our application 
Line 285: logic lives. Think of it as pure logic for the problem our application is solving. Because of the ports 
Line 286: and adapters, the domain logic is unconstrained by details of external systems:
Line 287: Figure 9.6 – Ports connect to the domain model
Line 288: The domain model represents the things our users want to do, in code. Every user story is described 
Line 289: by code here. Ideally, the code in this layer uses the language of the problem we are solving, instead 
Line 290: of technology details. When we do this well, this code becomes storytelling – it describes actions our 
Line 291: users care about in terms they have told us about. It uses their language – the language of our users 
Line 292: – not obscure computer language.
Line 293: The domain model can contain code written in any paradigm. It might use functional programming 
Line 294: (FP) ideas. It may even use object-oriented programming (OOP) ideas. It might be procedural. It 
Line 295: might even use an off-the-shelf library that we configure declaratively. My current style is to use OOP 
Line 296: 
Line 297: --- 페이지 182 ---
Line 298: Dependency inversion to the rescue
Line 299: 159
Line 300: for the overall structure and organization of a program, then use FP ideas inside the object methods 
Line 301: to implement them. It makes no difference to either the hexagonal architecture or TDD how we 
Line 302: implement this domain model. Whatever way suits your coding style is just fine here, so long as you 
Line 303: use the ideas of ports and adapters.
Line 304: Note
Line 305: The domain model contains code that describes how the user’s problem is being solved. This 
Line 306: is the essential logic of our application that creates business value.
Line 307: At the center of the entire application is the domain model. It contains the logic that brings the user’s 
Line 308: stories to life.
Line 309: The golden rule – the domain never connects directly to adapters
Line 310: To preserve the benefits of isolating the domain model from adapters and external systems, we follow 
Line 311: one simple rule: the domain model never connects directly to any of the adapters. This is always done 
Line 312: through a port.
Line 313: When our code follows this design approach, it is straightforward to check whether we’ve got the 
Line 314: ports and adapters split right. We can make two high-level structural decisions:
Line 315: •	 The domain model lives in a domain package (and sub packages)
Line 316: •	 The adapters live in an adapters package (and sub packages)
Line 317: We can analyze the code to check that anything in the domain package contains no import statements 
Line 318: from the adapters package. Import checks can be done visually in code reviews or pairing/mobbing. 
Line 319: Static analysis tools such as SonarQube can automate import checks as part of the build pipeline.
Line 320: The golden rules of the hexagonal architecture
Line 321: The domain model never connects directly to anything in the adapter layer so that our application 
Line 322: logic does not depend on details of external systems.
Line 323: The adapters connect to ports so that code connecting to external systems is isolated.
Line 324: Ports are part of the domain model to create abstractions of external systems.
Line 325: The domain model and the adapters depend on the ports only. This is dependency inversion 
Line 326: at work.
Line 327: These simple rules keep our design in line and preserve the isolation of the domain model.
Line 328: 
Line 329: --- 페이지 183 ---
Line 330: Hexagonal Architecture –Decoupling External Systems
Line 331: 160
Line 332: Why the hexagon shape?
Line 333: The idea behind the hexagon shape used in the diagram is that each face represents one external system. 
Line 334: In terms of a graphical representation of a design, having up to six external systems represented is 
Line 335: usually sufficient. The idea of the inner and outer hexagons to represent the domain model and adapter 
Line 336: layer shows graphically how the domain model is the core of our application and that it is isolated 
Line 337: from external systems by the ports and adapter layer.
Line 338: The critical idea behind the hexagonal architecture is the ports and adapters technique. The actual 
Line 339: number of sides depends on how many external systems there are. The number of those is not important.
Line 340: In this section, we introduced the hexagonal architecture and the benefits it provides, and provided 
Line 341: a general overview of how all the essential pieces fit together. Let’s turn to the next section and look 
Line 342: specifically at the decisions we need to make to abstract out an external system.
Line 343: Abstracting out the external system
Line 344: In this section, we will consider some of the decisions we need to make when applying the hexagonal 
Line 345: architecture approach. We’ll take a step-by-step approach to handling external systems, where we 
Line 346: will first decide what the domain model needs, then work out the right abstractions that hide their 
Line 347: technical details. We will consider two common external systems: web requests and database access.
Line 348: Deciding what our domain model needs
Line 349: The place to begin our design is with our domain model. We need to devise a suitable port for our 
Line 350: domain model to interact with. This port has to be free from any details of our external system, and 
Line 351: at the same time, it must answer the question of what our application needs this system for. We are 
Line 352: creating an abstraction.
Line 353: A good way to think about abstractions is to think about what would stay the same if we changed how 
Line 354: we performed a task. Suppose we want to eat warm soup for lunch. We might warm it in a pan on 
Line 355: the stove or perhaps warm it in the microwave. No matter how we choose to do it, what we are doing 
Line 356: stays the same. We are warming the soup and that is the abstraction we’re looking for.
Line 357: We don’t often warm soup in software systems unless we are building an automated soup vending 
Line 358: machine. But there are several common kinds of abstractions we will be using. This is because common 
Line 359: kinds of external systems are used when building a typical web application. The first and most obvious 
Line 360: is the connection to the web itself. In most applications, we will encounter some kind of data store, 
Line 361: typically a third-party database system. For many applications, we will also be calling out to another 
Line 362: web service. In turn, this service may call others in a fleet of services, all internal to our company. 
Line 363: Another typical web service call is to a third-party web service provider, such as a credit card payment 
Line 364: processor, as an example.
Line 365: Let’s look at ways of abstracting these common external systems.
Line 366: 
Line 367: --- 페이지 184 ---
Line 368: Abstracting out the external system
Line 369: 161
Line 370: Abstracting web requests and responses
Line 371: Our application will respond to HTTP requests and responses. The port we need to design represents 
Line 372: the request and the response in terms of our domain model, stripping away the web technology.
Line 373: Our sales report example could introduce these ideas as two simple domain objects. These requests 
Line 374: can be represented by a RequestSalesReport class:
Line 375: package com.sales.domain;
Line 376: import java.time.LocalDate;
Line 377: public class RequestSalesReport {
Line 378:     private final LocalDate start;
Line 379:     private final LocalDate end;
Line 380:     public RequestSalesReport(LocalDate start,
Line 381:                               LocalDate end){
Line 382:         this.start = start;
Line 383:         this.end = end;
Line 384:     }
Line 385:     public SalesReport produce(SalesReporting reporting) {
Line 386:         return reporting.reportForPeriod(start, end);
Line 387:     }
Line 388: }
Line 389: Here, we can see the critical pieces of our domain model of the request:
Line 390: •	 What we are requesting – that is, a sales report, captured in the class name
Line 391: •	 The parameters of that request – that is, the start and end dates of the reporting period
Line 392: We can see how the response is represented:
Line 393: •	 The SalesReport class will contain the raw information requested
Line 394: We can also see what is not present:
Line 395: •	 The data formats used in the web request
Line 396: •	 HTTP status codes, such as 200 OK
Line 397: •	 HTTPServletRequest and HttpServletResponse or equivalent framework objects
Line 398: 
Line 399: --- 페이지 185 ---
Line 400: Hexagonal Architecture –Decoupling External Systems
Line 401: 162
Line 402: This is a pure domain model representation of a request for a sales report between two dates. There 
Line 403: is no hint of this having come from the web, a fact that is very useful as we can request it from other 
Line 404: input sources, such as a desktop GUI or a command line. Even better, we can create these domain 
Line 405: model objects very easily in a unit test.
Line 406: The preceding example shows an object-oriented, tell-don’t-ask approach. We could just as easily choose 
Line 407: an FP approach. If we did, we would represent the request and response as pure data structures. The 
Line 408: record facility that was added to Java 17 is well suited to representing such data structures. What’s 
Line 409: important is that the request and response are written purely in domain model terms – nothing of 
Line 410: the web technology should be present.
Line 411: Abstracting the database
Line 412: Without data, most applications aren’t particularly useful. Without data storage, they become rather 
Line 413: forgetful of the data we supply. Accessing data stores such as relational databases and NoSQL databases 
Line 414: is a common task in web application development.
Line 415: In a hexagonal architecture, we start by designing the port that the domain model will interact with, 
Line 416: again in pure domain terms. The way to create a database abstraction is to think about what data 
Line 417: needs storing and not how it will be stored.
Line 418: A database port has two components:
Line 419: •	 An interface to invert the dependency on the database.
Line 420: The interface is often known as a repository. It has also been termed a data access object. 
Line 421: Whatever the name, it has the job of isolating the domain model from any part of our database 
Line 422: and its access technology.
Line 423: •	 Value objects representing the data itself, in domain model terms.
Line 424: A value object exists to transfer data from place to place. Two value objects that each hold 
Line 425: the same data values are considered equal. They are ideal for transferring data between the 
Line 426: database and our code.
Line 427: Returning to our sales report example, one possible design for our repository would be this:
Line 428: package com.sales.domain;
Line 429: public interface SalesRepository {
Line 430:     List<Sale> allWithinDateRange(LocalDate start,
Line 431:                                   LocalDate end);
Line 432: }
Line 433: 
Line 434: --- 페이지 186 ---
Line 435: Abstracting out the external system
Line 436: 163
Line 437: Here, we have a method called allWithinDateRange() that allows us to fetch a set of individual 
Line 438: sales transactions falling within a particular date range. The data is returned as java.util.List 
Line 439: of simple Sale value objects. These are fully featured domain model objects. They may well have 
Line 440: methods on them that perform some of the critical application logic. They may be little more than 
Line 441: basic data structures, perhaps using a Java 17 record structure. This choice is part of our job in 
Line 442: deciding what a well-engineered design looks like in our specific case.
Line 443: Again, we can see what is not present:
Line 444: •	 Database connection strings
Line 445: •	 JDBC or JPA API details – the standard Java Database Connectivity library
Line 446: •	 SQL queries (or NoSQL queries)
Line 447: •	 Database schema and table names
Line 448: •	 Database stored procedure details
Line 449: Our repository designs focus on what our domain model needs our database to provide but does not 
Line 450: constrain how it provides. As a result, some interesting decisions have to be taken in designing our 
Line 451: repository, concerning how much work we put into the database and how much we do in the domain 
Line 452: model itself. Examples of this include deciding whether we will write a complex query in the database 
Line 453: adapter, or whether we will write simpler ones and perform additional work in the domain model. 
Line 454: Likewise, will we make use of stored procedures in the database?
Line 455: Whatever trade-offs we decide in these decisions, once again, the database adapter is where all those 
Line 456: decisions reside. The adapter is where we see the database connection strings, query strings, table names, 
Line 457: and so on. The adapter encapsulates the design details of our data schema and database technology.
Line 458: Abstracting calls to web services
Line 459: Making calls to other web services is a frequent development task. Examples include calls to payment 
Line 460: processors and address lookup services. Sometimes, these are third-party external services, and 
Line 461: sometimes, they live inside our web service fleet. Either way, they generally require some HTTP calls 
Line 462: to be made from our application.
Line 463: Abstracting these calls proceeds along similar lines to abstracting the database. Our port is made up 
Line 464: of an interface that inverts the dependency on the web service we are calling, and some value objects 
Line 465: that transfer data.
Line 466: An example of abstracting a call to a mapping API such as Google Maps, for example, might look 
Line 467: like this:
Line 468: package com.sales.domain;
Line 469: public interface MappingService {
Line 470: 
Line 471: --- 페이지 187 ---
Line 472: Hexagonal Architecture –Decoupling External Systems
Line 473: 164
Line 474:     void addReview(GeographicLocation location,
Line 475:                    Review review);
Line 476: }
Line 477: We have an interface representing MappingService as a whole. We’ve added a method to 
Line 478: add a review of a particular location on whichever service provider we end up using. We’re using 
Line 479: GeographicLocation to represent a place, defined in our terms. It may well have a latitude and 
Line 480: longitude pair in it or it may be based on postal code. That’s another design decision. Again, we see 
Line 481: no sign of the underlying map service or its API details. That code lives in the adapter, which would 
Line 482: connect to the real external mapping web service.
Line 483: This abstraction offers us benefits in being able to use a test double for that external service and being 
Line 484: able to change service providers in the future. You never know when an external service might shut 
Line 485: down or become too costly to use. It’s nice to keep our options open by using the hexagonal architecture.
Line 486: This section has presented some ideas for the most common tasks in working with external systems 
Line 487: in a hexagonal architecture. In the next section, we’ll discuss general approaches to writing code in 
Line 488: the domain model.
Line 489: Writing the domain code
Line 490: In this section, we will look at some of the things we need to think about as we write the code for 
Line 491: our domain model. We’ll cover what kinds of libraries we should and should not use in the domain 
Line 492: model, how we deal with application configuration and initialization, and we’ll also think about what 
Line 493: impact popular frameworks have.
Line 494: Deciding what should be in our domain model
Line 495: Our domain model is the very core of our application and the hexagonal architecture puts it up front 
Line 496: and center. A good domain model is written using the language of our users’ problem domain; that’s 
Line 497: where the name comes from. We should see the names of program elements that our users would 
Line 498: recognize. We should recognize the problem being solved over and above the mechanisms we are 
Line 499: using to solve it. Ideally, we will see terms from our user stories being used in our domain model.
Line 500: Applying the hexagonal architecture, we choose our domain model to be independent of those things 
Line 501: that are not essential to solving the problem. That’s why external systems are isolated. We may initially 
Line 502: think that creating a sales report means that we must read a file and we must create an HTML document. 
Line 503: But that’s not the essential heart of the problem. We simply need to get sales data from somewhere, 
Line 504: perform some calculations to get totals for our report, then format it somehow. The somewhere and 
Line 505: somehow can change, without affecting the essence of our solution.
Line 506: 
Line 507: --- 페이지 188 ---
Line 508: Writing the domain code
Line 509: 165
Line 510: Bearing this constraint in mind, we can take any standard analysis and design approach. We are free 
Line 511: to choose objects or decompose them into functions as we normally do. We only have to preserve that 
Line 512: distinction between the essence of the problem and the implementation details.
Line 513: We need to exercise judgment in these decisions. In our sales report example, the source of the sales 
Line 514: data is of no consequence. As a counter-example, suppose we are making a linter for our Java program 
Line 515: files – it’s quite reasonable to have the concept of files represented directly in our domain model. 
Line 516: This problem domain is all about working with Java files, so we should make that clear. We may still 
Line 517: decouple the domain model of a file from the OS-specific details of reading and writing it, but the 
Line 518: concept would be in the domain model.
Line 519: Using libraries and frameworks in the domain model
Line 520: The domain model can use any pre-written library or framework to help do its job. Popular libraries 
Line 521: such as Apache Commons or the Java Standard Runtime library generally present no problems 
Line 522: here. However, we need to be aware of frameworks that bind us to the world of external systems and 
Line 523: our adapter layer. We need to invert dependencies on those frameworks, leaving them to be just an 
Line 524: implementation detail of the adapter layer.
Line 525: An example might be the @RestController annotation of Spring Boot. It looks like pure domain 
Line 526: code at first sight, but it ties the class tightly to generated code that is specific to the web adapter.
Line 527: Deciding on a programming approach
Line 528: The domain model can be written using any programming paradigm. This flexibility means that we 
Line 529: will need to decide on which approach to use. This is never a purely technical decision, like with so 
Line 530: many things in software. We should consider the following:
Line 531: •	 Existing team skills and preferences: What paradigm does the team know best? Which 
Line 532: paradigm would they like to use, given the chance?
Line 533: •	 Existing libraries, frameworks, and code bases: If we are going to be using pre-written code 
Line 534: – and let’s face it, we almost certainly will – then what paradigm would best suit that code?
Line 535: •	 Style guides and other code mandates: Are we working with an existing style guide or paradigm? 
Line 536: If we are being paid for our work – or we are contributing to an existing open source project 
Line 537: – we will need to adopt the paradigm set out for us.
Line 538: The good news is that whatever paradigm we choose, we will be able to write our domain model 
Line 539: successfully. While the code may look different, equivalent functionality can be written using any of 
Line 540: the paradigms.
Line 541: 
Line 542: --- 페이지 189 ---
Line 543: Hexagonal Architecture –Decoupling External Systems
Line 544: 166
Line 545: Substituting test doubles for external systems
Line 546: In this section, we’ll discuss one of the biggest advantages that the hexagonal architecture brings to 
Line 547: TDD: high testability. It also brings some workflow advantages.
Line 548: Replacing the adapters with test doubles
Line 549: The key advantage the hexagonal architecture brings to TDD is that it is trivially easy to replace all the 
Line 550: adapters with test doubles, giving us the ability to test the entire domain model with FIRST unit tests. 
Line 551: We can test the entire application core logic without test environments, test databases, or HTTP tools 
Line 552: such as Postman or curl – just fast, repeatable unit tests. Our testing setup looks like this:
Line 553: Figure 9.7 – Testing the domain model
Line 554: We can see that all the adapters have been replaced by test doubles, completely freeing us from our 
Line 555: environment of external systems. Unit tests can now cover the whole domain model, reducing the 
Line 556: need for integration tests.
Line 557: We gain several benefits by doing this:
Line 558: •	 We can write TDD tests first with ease: There’s no friction in writing a simple test double that 
Line 559: lives entirely in memory and has no dependencies on the test environment.
Line 560: •	 We gain FIRST unit test benefits: Our tests run very fast indeed and are repeatable. Typically, 
Line 561: testing an entire domain model takes the order of seconds, not hours. The tests will repeatably 
Line 562: pass or fail, meaning we are never wondering whether a build failure was due to a flaky 
Line 563: integration test failure.
Line 564: •	 It unlocks our team: We can do useful work building the core logic of our system, without 
Line 565: having to wait for test environments to be designed and built.
Line 566: 
Line 567: --- 페이지 190 ---
Line 568: Unit testing bigger units
Line 569: 167
Line 570: The techniques for creating the test doubles were outlined in Chapter 8, Test Doubles – Stubs and 
Line 571: Mocks. There is nothing new required in terms of implementing these doubles.
Line 572: One consequence of being able to test the whole domain model is that we can apply TDD and FIRST 
Line 573: unit tests to much larger program units. The next section discusses what that means for us.
Line 574: Unit testing bigger units
Line 575: The previous section introduced the idea of surrounding our domain model with test doubles for 
Line 576: every port. This gives us some interesting opportunities to discuss in this section. We can test units 
Line 577: that are as large as a user story.
Line 578: We’re familiar with unit tests as being things that test in the small. There’s a good chance you’ll have 
Line 579: heard somebody say that a unit test should only ever apply to a single function, or that every class 
Line 580: should have one unit test for every method. We’ve already seen how that’s not the best way to use 
Line 581: unit tests. Tests like those miss out on some advantages. We are better served by thinking of tests as 
Line 582: covering behavior instead.
Line 583: The combined approach of designing with the hexagonal architecture and testing behaviors instead of 
Line 584: implementation details leads to an interesting system layering. Instead of having traditional layers, as 
Line 585: we might do in a three-tier architecture, we have circles of increasingly higher-level behavior. Inside 
Line 586: our domain model, we will find those tests-in-the-small. But as we move outward, toward the adapter 
Line 587: layer, we will find bigger units of behavior.
Line 588: Unit testing entire user stories
Line 589: The ports in the domain model form a natural high-level boundary of the domain model. If we review 
Line 590: what we’ve learned in this chapter, we’ll see that this boundary consists of the following:
Line 591: •	 The essence of requests from users
Line 592: •	 The essence of a response from our application
Line 593: •	 The essence of how data needs storing and accessing
Line 594: •	 All using technology-free code
Line 595: This layer is the essence of what our application does, free from the details of how it does it. It is nothing 
Line 596: less than the original user stories themselves. The most significant thing about this domain model is 
Line 597: that we can write FIRST unit tests against it. We have all we need to replace difficult-to-test external 
Line 598: systems with simple test doubles. We can write unit tests that cover entire user stories, confirming 
Line 599: that our core logic is correct.
Line 600: 
Line 601: --- 페이지 191 ---
Line 602: Hexagonal Architecture –Decoupling External Systems
Line 603: 168
Line 604: Faster, more reliable testing
Line 605: Traditionally, testing user stories involved slower integration tests in a test environment. The 
Line 606: hexagonal architecture enables unit tests to replace some of these integration tests, speeding 
Line 607: up our builds and providing greater repeatability of our testing.
Line 608: We can now test-drive at three granularities against our domain model:
Line 609: •	 Against a single method or function
Line 610: •	 Against the public behaviors of a class and any collaborators it has
Line 611: •	 Against the core logic of an entire user story
Line 612: This is a big benefit of the hexagonal architecture. The isolation from external services has the effect 
Line 613: of pushing the essential logic of a user story into the domain model, where it interacts with ports. As 
Line 614: we’ve seen, those ports – by design – are trivially easy to write test doubles for. It’s worth restating the 
Line 615: key benefits of FIRST unit tests:
Line 616: •	 They are very fast, so testing our user stories will be very fast
Line 617: •	 They are highly repeatable, so we can trust test passes and failures
Line 618: As we cover wide areas of functionality with unit tests, we blur the line between integration and unit 
Line 619: testing. We remove friction from developers testing more of the user stories by making that testing 
Line 620: easier. Using more unit tests improves build times, as the tests run quickly and give reliable pass/
Line 621: fail results. Fewer integration tests are needed, which is good as they run more slowly and are more 
Line 622: prone to incorrect results.
Line 623: In the next section, we’ll apply what we’ve learned to our Wordz application. We will write a port that 
Line 624: abstracts out the details of fetching a word for our users to guess.
Line 625: Wordz – abstracting the database
Line 626: In this section, we will apply what we’ve learned to our Wordz application and create a port suitable for 
Line 627: fetching the words to present to a user. We will write the adapters and integration tests in Chapter 14, 
Line 628: Driving the Database Layer.
Line 629: Designing the repository interface
Line 630: The first job in designing our port is to decide what it should be doing. For a database port, we need 
Line 631: to think about the split between what we want our domain model to be responsible for and what we 
Line 632: will push out to the database. The ports we use for a database are generally called repository interfaces.
Line 633: 
Line 634: --- 페이지 192 ---
Line 635: Wordz – abstracting the database
Line 636: 169
Line 637: Three broad principles should guide us:
Line 638: •	 Think about what the domain model needs – why do we need this data? What will it be used for?
Line 639: •	 Don’t simply echo an assumed database implementation – don’t think in terms of tables and 
Line 640: foreign keys at this stage. That comes later when we decide how to implement the storage. 
Line 641: Sometimes, database performance considerations mean we have to revisit the abstraction we 
Line 642: create here. We would then trade off leaking some database implementation details here if it 
Line 643: allowed the database to function better. We should defer such decisions as late as we can.
Line 644: •	 Consider when we should leverage the database engine more. Perhaps we intend to use complex 
Line 645: stored procedures in the database engine. Reflect this split of behavior in the repository interface. 
Line 646: It may suggest a higher-level abstraction in the repository interface.
Line 647: For our running example application, let’s consider the task of fetching a word at random for the user to 
Line 648: guess. How should we divide the work between the domain and database? There are two broad options:
Line 649: •	 Let the database choose a word at random
Line 650: •	 Let the domain model generate a random number and let the database supply a numbered word
Line 651: In general, letting the database do more work results in faster data handling; the database code is 
Line 652: closer to the data and isn’t dragging it over a network connection into our domain model. But how 
Line 653: do we persuade a database to choose something at random? We know that for relational databases, 
Line 654: we can issue a query that will return results in no guaranteed order. That’s sort of random. But would 
Line 655: it be random enough? Across all possible implementations? Seems unlikely.
Line 656: The alternative is to let the domain model code decide which word to pick by generating a random 
Line 657: number. We can then issue a query to fetch the word associated with that number. This also suggests 
Line 658: that each word has an associated number with it – something we can provide when we design the 
Line 659: database schema later.
Line 660: This approach implies we need the domain model to pick a random number from all the numbers 
Line 661: associated with the words. That implies the domain model needs to know the full set of numbers to 
Line 662: choose from. We can make another design decision here. The numbers used to identify a word will 
Line 663: start at 1 and increase by one for each word. We can provide a method on our port that returns the 
Line 664: upper bound of these numbers. Then, we are all set to define that repository interface – with a test.
Line 665: The test class starts with the package declaration and library imports we need:
Line 666: package com.wordz.domain;
Line 667: import org.junit.jupiter.api.BeforeEach;
Line 668: import org.junit.jupiter.api.Test;
Line 669: import org.junit.jupiter.api.extension.ExtendWith;
Line 670: 
Line 671: --- 페이지 193 ---
Line 672: Hexagonal Architecture –Decoupling External Systems
Line 673: 170
Line 674: import org.mockito.Mock;
Line 675: import org.mockito.MockitoAnnotations;
Line 676: import static org.assertj.core.api.Assertions.*;
Line 677: import static org.mockito.Mockito.when;
Line 678: We enable Mockito integration with an annotation provided by the junit-jupiter library. We 
Line 679: add the annotation at the class level:
Line 680: @ExtendWith(MockitoExtension.class)
Line 681: public class WordSelectionTest {
Line 682: This will ensure that Mockito is initialized on each test run. The next part of the test defines some 
Line 683: integer constants for readability:
Line 684:     private static final int HIGHEST_WORD_NUMBER = 3;
Line 685:     private static final int WORD_NUMBER_SHINE = 2;
Line 686: We need two test doubles, which we want Mockito to generate. We need a stub for the word repository 
Line 687: and a stub for a random number generator. We must add fields for these stubs. We will mark the fields 
Line 688: with the Mockito @Mock annotation so that Mockito will generate the doubles for us:
Line 689:     @Mock
Line 690:     private WordRepository repository;
Line 691:     @Mock
Line 692:     private RandomNumbers random;
Line 693: Mockito sees no difference between a mock or stub when we use the @Mock annotation. It simply 
Line 694: creates a test double that can be configured for use either as a mock or a stub. This is done later in 
Line 695: the test code.
Line 696: We will name the test method selectsWordAtRandom(). We want to drive out a class that we will call 
Line 697: WordSelection and make it responsible for choosing one word at random from WordRepository:
Line 698:     @Test
Line 699:     void selectsWordAtRandom() {
Line 700:         when(repository.highestWordNumber())
Line 701:             .thenReturn(HIGHEST_WORD_NUMBER);
Line 702: 
Line 703: --- 페이지 194 ---
Line 704: Wordz – abstracting the database
Line 705: 171
Line 706:         when(repository.fetchWordByNumber(WORD_NUMBER_SHINE))
Line 707:             .thenReturn("SHINE");
Line 708:         when(random.next(HIGHEST_WORD_NUMBER))
Line 709:             .thenReturn(WORD_NUMBER_SHINE);
Line 710:         var selector = new WordSelection(repository,
Line 711:                                          random);
Line 712:         String actual = selector.chooseRandomWord();
Line 713:         assertThat(actual).isEqualTo("SHINE");
Line 714:     }
Line 715: }
Line 716: The preceding test was written in the normal way, adding lines to capture each design decision:
Line 717: •	 The WordSelection class encapsulates the algorithm, which selects a word to guess
Line 718: •	 The WordSelection constructor takes two dependencies:
Line 719: 	 WordRepository is the port for stored words
Line 720: 	 RandomNumbers is the port for random number generation
Line 721: •	 The chooseRandomWord() method will return a randomly chosen word as a String
Line 722: •	 The arrange section is moved out to the beforeEachTest() method:
Line 723: @BeforeEach
Line 724: void beforeEachTest() {
Line 725:     when(repository.highestWordNumber())
Line 726:                   .thenReturn(HIGHEST_WORD_NUMBER);
Line 727:     when(repository.fetchWordByNumber(WORD_NUMBER_SHINE))
Line 728:                   .thenReturn("SHINE");
Line 729: }
Line 730: This will set up the test data in the stub for our WordRepository at the start of each test. 
Line 731: The word identified by number 2 is defined as SHINE, so we can check that in the assert.
Line 732: 
Line 733: --- 페이지 195 ---
Line 734: Hexagonal Architecture –Decoupling External Systems
Line 735: 172
Line 736: •	 Out of that test code flows the following definition of two interface methods:
Line 737: package com.wordz.domain;
Line 738: public interface WordRepository {
Line 739:     String fetchWordByNumber(int number);
Line 740:     int highestWordNumber();
Line 741: }
Line 742: The WordRepository interface defines our application’s view of the database. We only need two 
Line 743: facilities for our current needs:
Line 744: •	 A fetchWordByNumber() method to fetch a word, given its identifying number
Line 745: •	 A highestWordNumber() method to say what the highest word number will be
Line 746: The test has also driven out the interface needed for our random number generator:
Line 747: package com.wordz.domain;
Line 748: public interface RandomNumbers {
Line 749:     int next(int upperBoundInclusive);
Line 750: }
Line 751: The single next() method returns int in the range of 1 to the upperBoundInclusive number.
Line 752: With both the test and port interfaces defined, we can write the domain model code:
Line 753: package com.wordz.domain;
Line 754: public class WordSelection {
Line 755:     private final WordRepository repository;
Line 756:     private final RandomNumbers random;
Line 757:     public WordSelection(WordRepository repository,
Line 758:                          RandomNumbers random) {
Line 759:         this.repository = repository;
Line 760:         this.random = random;
Line 761:     }
Line 762:     public String chooseRandomWord() {
Line 763: 
Line 764: --- 페이지 196 ---
Line 765: Summary
Line 766: 173
Line 767:         int wordNumber =
Line 768:            random.next(repository.highestWordNumber());
Line 769:         return repository.fetchWordByNumber(wordNumber);
Line 770:     }
Line 771: }
Line 772: Notice how this code does not import anything from outside the com.wordz.domain package. 
Line 773: It is pure application logic, relying only on the port interfaces to access stored words and random 
Line 774: numbers. With this, our production code for the domain model of WordSelection is complete.
Line 775: Designing the database and random numbers adapters
Line 776: The next job is to implement the RandomNumbers port and database access code that implements 
Line 777: our WordRepository interface. In outline, we’ll choose a database product, research how to 
Line 778: connect to it and run database queries, then test-drive that code using an integration test. We will defer 
Line 779: doing these tasks to part three of this book, in Chapter 13, Driving the Domain Layer, and Chapter 14, 
Line 780: Driving the Database Layer.
Line 781: Summary
Line 782: In this chapter, we learned how to apply the SOLID principles to decouple external systems completely, 
Line 783: leading to an application architecture known as the hexagonal architecture. We saw how this allows 
Line 784: us to use test doubles in place of external systems, making our tests simpler to write, with repeatable 
Line 785: results. This, in turn, allows us to test entire user stories with a FIRST unit test. As a bonus, we isolate 
Line 786: ourselves from future changes in those external systems, limiting the amount of rework that would 
Line 787: be required to support new technologies. We’ve seen how the hexagonal architecture combined with 
Line 788: dependency injection allows us to support several different external systems choices and select the 
Line 789: one we want at runtime via configuration.
Line 790: The next chapter will look at the different styles of automated testing that apply to the different sections 
Line 791: of a hexagonal architecture application. This approach is summarized as the Test Pyramid, and we 
Line 792: shall learn more about it there.
Line 793: 
Line 794: --- 페이지 197 ---
Line 795: Hexagonal Architecture –Decoupling External Systems
Line 796: 174
Line 797: Questions and answers
Line 798: Take a look at the following questions and answers regarding this chapter’s content:
Line 799: 1.	
Line 800: Can we add the hexagonal architecture later?
Line 801: Not always. We can refactor it. The challenge can be too much code that directly depends on 
Line 802: details of external systems. If that’s the starting point, this refactoring will be challenging. There 
Line 803: will be a lot of rework to do. This implies that some degree of up-front design and architectural 
Line 804: discussion is required before we start work.
Line 805: 2.	
Line 806: Is the hexagonal architecture specific to OOP?
Line 807: No. It is a way of organizing dependencies in our code. It can be applied to OOP, FP, procedural 
Line 808: programming, or anything else – so long as those dependencies are managed correctly.
Line 809: 3.	
Line 810: When should we not use the hexagonal architecture?
Line 811: When we have no real logic in our domain model. This is common for very small CRUD 
Line 812: microservices that typically frontend a database table. With no logic to isolate, putting in all 
Line 813: this code has no benefit. We may as well do TDD with integration tests only and accept that 
Line 814: we won’t be able to use FIRST unit tests.
Line 815: 4.	
Line 816: Can we only have one port for an external system?
Line 817: No. It is often better if we have more ports. Suppose we have a single Postgres database connected 
Line 818: to our application, holding data on users, sales, and product inventory. We could simply have a 
Line 819: single repository interface, with methods to work with those three datasets. But it will be better 
Line 820: to split that interface up (following ISP) and have UserRepository, SalesRepository, 
Line 821: and InventoryRepository. The ports provide a view of what our domain model wants 
Line 822: from external systems. Ports are not a one-to-one mapping to hardware.
Line 823: Further reading
Line 824: To learn more about the topics that were covered in this chapter, take a look at the following resources:
Line 825: •	 Hexagonal architecture, Alastair Cockburn: https://alistair.cockburn.us/
Line 826: hexagonal-architecture/
Line 827: The original description of the hexagonal architecture in terms of ports and adapters.
Line 828: •	 https://medium.com/pragmatic-programmers/unit-tests-are-first-
Line 829: fast-isolated-repeatable-self-verifying-and-timely-a83e8070698e
Line 830: Credits the original inventors of the term FIRST, Tim Ottinger and Brett Schuchert.
Line 831: •	 https://launchdarkly.com/blog/testing-in-production-for-safety-
Line 832: and-sanity/
Line 833: Guide to testing code deployed on production systems, without accidentally triggering 
Line 834: unintended consequences.