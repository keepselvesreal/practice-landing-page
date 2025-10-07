Line 1: 
Line 2: --- 페이지 32 ---
Line 3: Chapter 1 
Line 4: Prologue
Line 5: “Begin at the beginning,” the King said, very gravely, “and go on till you 
Line 6: come to the end; then stop.”
Line 7: Lewis Carroll, Alice’s Adventures in Wonderland
Line 8: Say hello to testable requirements. You are introduced to acceptance tests and 
Line 9: discover the beneﬁts of using them. You are also introduced to the team that 
Line 10: will create them. 
Line 11: Ways to Develop Software 
Line 12: Different teams have different ways to develop software. Here are examples of 
Line 13: two ways. 
Line 14:  
Line 15: One Way 
Line 16: It’s the last day of the iteration. Tom, the tester, is checking the implementa-
Line 17: tion that Debbie, the developer, handed over to him earlier that day. He goes 
Line 18: through the screens, entering the test case data he created. He discovers that 
Line 19: the results aren’t what he had assumed they should be. He’s unable to contact 
Line 20: Cathy, the customer, for clariﬁcation as to whether he made the correct assump-
Line 21: tions. There’s nothing left to do but write up a defect to be addressed during the 
Line 22: next iteration, leaving less time to develop new features. 
Line 23: Another Way 
Line 24: It’s the last day of the iteration. Debbie, the developer, has run through the ac-
Line 25: ceptance tests that Cathy, Debbie, and Tom created prior to Debbie starting 
Line 26: implementation. Tom quickly runs through the same acceptance tests and then 
Line 27: 9
Line 28: 
Line 29: --- 페이지 33 ---
Line 30:  
Line 31: Chapter 1 Prologue
Line 32: 10
Line 33: starts doing more testing to get a feeling for how the implementation ﬁts into 
Line 34: the entire workﬂow. At the review the next morning, Cathy agrees that the story 
Line 35: is complete. 
Line 36:  
Line 37: The Difference 
Line 38: What’s the difference between the ﬁrst way and the second way? In the ﬁrst case, 
Line 39: no tests were created upfront. The developer had nothing to test against, so she 
Line 40: relied on the tester to perform veriﬁcation. The tester needed more details from 
Line 41: the customer. Feedback as to success or failure of a requirement implementation 
Line 42: was delayed. Every requirement story in the second situation has one or more 
Line 43: tests associated with it, making each a testable requirement. The tests were de-
Line 44: veloped by the customer, tester, and developer prior to implementation. As we 
Line 45: will see in later chapters with detailed examples, these tests clarify the require-
Line 46: ments. They provide a measure of doneness to all the parties. 
Line 47: If a requirement does not have a test, it is not yet demonstrated to be a test-
Line 48: able requirement. If you cannot test that a requirement has been fulﬁlled, how 
Line 49: do you know when it has been met? This does not mean that the test is easy 
Line 50: to perform. Nor can tests be fully speciﬁed; there are always assumptions. But 
Line 51: there must be at least an objective test so that the customer, developer, and tester 
Line 52: have a common understanding of what meeting the requirement means. 
Line 53: The Importance of Acceptance Tests 
Line 54: In my classes, I often start with a dialogue to emphasize the importance of ac-
Line 55: ceptance tests. It usually goes something like this: 
Line 56: I ask, “Does anyone want a fast car?” 
Line 57: Someone always says, “Yes, I want one.” 
Line 58: “I’ll build you one,” I reply. I turn around and work furiously for 5 seconds. 
Line 59: I turn back around and show the student the results. “Here’s your car,” I state. 
Line 60: “Great,” the student answers. 
Line 61: “It’s really fast. It goes from 0 to 60 in less than 20 seconds,” I proudly 
Line 62: explain.
Line 63: “That’s not fast,” the student retorts. 
Line 64: “I thought it was fast. So give me a test for how fast you want the car to be,” 
Line 65: I reply. 
Line 66: “0 to 60 in less than 4.5 seconds,” the student states. 
Line 67: I turn back around, again work quickly, and then face the student again. 
Line 68: “Here it is: 0 to 60 in 4.5 seconds. Fast enough?” I ask. 
Line 69: “Yes,” the student answers. 
Line 70: “Oh, by the way: 60 is the top speed,” I state. 
Line 71: 
Line 72: --- 페이지 34 ---
Line 73: The Importance of Acceptance Tests 
Line 74: 11
Line 75: “That’s not fast,” the student retorts. 
Line 76: “So give me another test,” I ask. 
Line 77: “The top speed should be 150,” the student demands. 
Line 78: Again, I quickly create a new car. “Okay, here it is: 0 to 60 in 4.5 seconds. 
Line 79: Top speed of 150. Fast enough?” I again ask. 
Line 80: “That should be good,” the student retorts. 
Line 81: “Oh, by the way: It takes two minutes to get to 150,” I let slide. 
Line 82: By this time, my point has been made. Getting just a requirement for a “fast 
Line 83: car” is not sufﬁcient for knowing what to build. The customer needs to create 
Line 84: some tests for that requirement that clarify what exactly is meant by “fast.” 
Line 85: Without those tests, the engineers may go off and create something that they 
Line 86: think meets the requirement. When they deliver it to the customer, the customer 
Line 87: has a negative reaction to the creation. The item does not meet his needs, as he 
Line 88: thought he had clearly stated in saying, “the car must be fast.” 
Line 89: Having acceptance tests for a requirement gives developers a deﬁnitive stand-
Line 90: ard against which to measure their implementation. If the implementation does 
Line 91: not meet the tests, they do not have to bother the customer with something that 
Line 92: is noncompliant. If each acceptance test represents a similar effort in creating the 
Line 93: implementation, the number of passing tests can be used as a rough indication 
Line 94: of how much progress has been made on a project. 
Line 95: Absolute Tests Are Not Absolutely Fixed 
Line 96: Although the tests are absolute, such as “0 to 60 in less than 4.5 sec-
Line 97: onds,” they also form a point of discussion between the customer and 
Line 98: the engineers. If the engineers work for a while and the car accelerates in 
Line 99: 4.6 seconds, they can discuss with the customer whether this is sufﬁcient. 
Line 100: In particular, this would occur when the engineers discover that getting 
Line 101: the time down to 4.5 seconds might take considerably more development 
Line 102: time. In the end, the customer is the decision maker. If 4.5 seconds is an 
Line 103: absolute requirement to sell the car, the extra development cost is worth 
Line 104: it. If it is not, money will be saved. 1
Line 105: I’d like to clarify a couple of terms that are used throughout the book: accept-
Line 106: ance criteria and acceptance tests. Acceptance criteria are general conditions of 
Line 107: acceptance without giving speciﬁcs. For the car example, these might be “accel-
Line 108: eration from one speed to another,” “top speed,” and “must feel fast.” Accept-
Line 109: ance tests are speciﬁc conditions of acceptance, such as “0 to 60 in less than 
Line 110:   1 . If you can agree up front how much that extra 0.1 second is worth, developers can 
Line 111: make quick decisions. See Don Reinertsen [Reinertsen01] for lean economic models. 
Line 112: 
Line 113: --- 페이지 35 ---
Line 114:  
Line 115: Chapter 1 Prologue
Line 116: 12
Line 117: 4.5 seconds.” Each acceptance test has unstated conditions. For example, an 
Line 118: unstated condition could be that the acceleration is measured on a ﬂat area, with 
Line 119: little wind. You could be very speciﬁc about these conditions: an area that has 
Line 120: less than .1 degree of slope and wind less than 1 mile per hour. If necessary for 
Line 121: regulatory or other purposes, you could add these to the test. But you should 
Line 122: avoid making the test a complex document. 
Line 123: A few facets that differentiate acceptance tests from other types of tests, such 
Line 124: as unit tests, are 
Line 125: •  The customer understands and speciﬁes acceptance tests. 
Line 126: •  Acceptance tests do not change even if the implementation changes. 
Line 127: System and Team Introduction 
Line 128: The principles and practices of acceptance test-driven development (ATDD) are 
Line 129: introduced through the tale of the development of a software system. The story 
Line 130: originated in my book Prefactoring—Extreme Abstraction, Extreme Separa-
Line 131: tion, Extreme Readability [Pugh02]. That book emphasizes how developers can 
Line 132: create a high-quality solution for the system. This book highlights the customer-
Line 133: developer-tester interaction in creating and using acceptance tests in developing 
Line 134: the system. 
Line 135: The System 
Line 136: Sam, the owner of Sam’s Lawn Mower Repair and CD Rental Store, had a 
Line 137: lawn mower repair shop for a number of years. He noticed that people coming 
Line 138: into the shop had circular devices hanging on their bodies. It turned out they 
Line 139: were Sony Discmans. Being the inquisitive type, he discovered that his customers 
Line 140: liked to listen to music while they mowed the lawn. So he added CD rental to 
Line 141: the services his store offered. 
Line 142: Business has been booming, even though the Sony Discman is no longer being 
Line 143: used. People are now coming in with little rectangular boxes hanging around 
Line 144: their necks or sitting in their pockets. They are renting more CDs than ever and 
Line 145: returning them quickly—in as little as an hour. Sam’s paper system is having a 
Line 146: hard time keeping up, and it is becoming difﬁcult to produce the reports needed 
Line 147: to track the inventory. Sam is planning to open a second store. Before he does 
Line 148: that, he ﬁgures that he needs to obtain a software system, or his issues will just 
Line 149: double.
Line 150: 
Line 151: --- 페이지 36 ---
Line 152: System and Team Introduction 
Line 153: 13
Line 154: Sam got a recommendation and called Debbie. She works with Tom in an 
Line 155: agile development shop. Sam selected that shop to develop the system. 
Line 156: The People 
Line 157: Sam represents the project sponsor for the new system. His wife Cathy takes 
Line 158: care of the logistic side of the business. She does the bookkeeping, handles the 
Line 159: inventory, and places orders for new CDs. Cathy plays the role of customer—
Line 160: the one requesting the application. Along the way, as you’ll see, Cathy is intro-
Line 161: duced to software development and in particular to ATDD. Other interested 
Line 162: parties include Sam’s sister Mary and his brother-in-law Harry, who frequently 
Line 163: help out at the store. Their son Cary is a clerk at the store. He will be using the 
Line 164: new system. 
Line 165: Debbie is the developer and Tom is the tester. They work as a pair to under-
Line 166: stand and implement what Cathy needs. The terms developer and  tester are 
Line 167: often related to titles. In this book, these terms refer to what Debbie and Tom 
Line 168: focus on. The development focus is to create an implementation that does what 
Line 169: it is supposed to do. The testing focus is to check that the implementation does 
Line 170: precisely that and does not do what it should not. 
Line 171: Focus may not be correlated with the titles developer and tester. In many 
Line 172: agile processes, such as Scrum, there are no titles on teams [Larman01]. Any 
Line 173: two people may pair together, with one focusing on testing and one on imple-
Line 174: menting. It’s possible that a single person may focus both ways on a particular 
Line 175: requirement. The entire team is shown in Figure 1.1.
Line 176: Sam
Line 177: the
Line 178: Sponsor
Line 179: Cathy
Line 180: the
Line 181: Customer
Line 182: Tom
Line 183: the
Line 184: Tester
Line 185: Debbie
Line 186: the
Line 187: Developer
Line 188: Cary,
Line 189: Mary,
Line 190: Harry
Line 191: the
Line 192: Users
Line 193: Figure 1.1 The Team 
Line 194: 
Line 195: --- 페이지 37 ---
Line 196: Chapter 1 Prologue
Line 197: 14
Line 198: Summary
Line 199: • A testable requirement has one or more acceptance tests. 
Line 200: • An acceptance test is a standard to measure the correctness of the imple-
Line 201: mentation.
Line 202: • Acceptance tests are created in collaboration with the customer. 