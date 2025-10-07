Line 1: 
Line 2: --- 페이지 280 ---
Line 3: Chapter 31 
Line 4: Test Setup 
Line 5: “It’s not what I do, but the way I do it. It’s not what I say, but the way I 
Line 6: say it.”
Line 7: Mae West 
Line 8: This chapter discusses the trade-offs between using an individual setup for tests 
Line 9: and using a common setup. It also explores concerns about test order and per-
Line 10: sistent storage. 
Line 11: A Common Setup 
Line 12: You may have noticed that the setup for several of the triad’s tests started to be 
Line 13: repetitious. All the tests need customers and CDs to rent or return. It is tempting 
Line 14: to place the repetitive setup into a common setup. There is a classic trade-off 
Line 15: between decreasing duplication by the common setup and increasing the possi-
Line 16: bility that altering the common setup causes failing tests. 1 A common setup for 
Line 17: all tests might be as follows. 
Line 18: 257
Line 19:   1.  This is an example in the test world of the “Splitters versus Lumpers” prefactoring 
Line 20: guideline for design [Pugh02]. 
Line 21: Customer Data 
Line 22: Name 
Line 23: ID 
Line 24: Credit-Card Number 
Line 25: James 
Line 26: 007 
Line 27: 4005550000000019
Line 28: Maxwell 
Line 29: 88 
Line 30: 372700997251009
Line 31: 
Line 32: --- 페이지 281 ---
Line 33: Chapter 31 Test Setup
Line 34: 258
Line 35: This data forms a “test bed” for the other tests. If you make any changes 
Line 36: to this setup, such as to James’s ID or credit-card number, tests that depend 
Line 37: on those values will fail. They will fail not because the behavior of the system 
Line 38: changed, but because the test may now be specifying an invalid behavior. For 
Line 39: example, the Card Charge test would have James’s original credit-card number 
Line 40: on it, but James’s number has changed. A shared setup should remain constant. 
Line 41: On the other hand, the Rental table has more potential transactions than the 
Line 42: CD Data and the Album Data tables. Many tests require different values in this 
Line 43: table. For example, the data in this table are used for the tests of Check-In story 
Line 44: and the Customer Limit on Simultaneous Rentals business rule. 
Line 45: Rentals
Line 46: CD ID 
Line 47: Customer ID 
Line 48: Due Date 
Line 49: CD12 
Line 50: 007 
Line 51: 1/21/2011
Line 52: CD6 
Line 53: 88 
Line 54: 1/22/2011
Line 55: CD20 
Line 56: 88 
Line 57: 1/23/2011
Line 58: CD 21 
Line 59: 88 
Line 60: 1/24/2011
Line 61: Customer ID 007 could be used for a regular check-in test. Customer ID 
Line 62: 88 could not be used for a regular test, because ID 88 already has three CDs 
Line 63: rented. Keeping track of which customers are suitable for which tests requires 
Line 64: discipline. Without this discipline, using a separate setup in each test for the 
Line 65: appropriate data is far easier to maintain. 
Line 66: The common setup could be run for each test to get a clean start—“a Fresh 
Line 67: Fixture” as Gerard Meszaros terms it [Meszaros01]—or it could be run just 
Line 68: Album Data 
Line 69: UPC Code 
Line 70: Title 
Line 71: CD Category 
Line 72: UPC123456 
Line 73: Janet Jackson Number Ones 
Line 74: Regular
Line 75: UPC000001 
Line 76: Beatles Greatest Hits 
Line 77: Golden Oldie 
Line 78: CD Data 
Line 79: ID 
Line 80: UPC Code 
Line 81: CD2 
Line 82: UPC000001
Line 83: CD3 
Line 84: UPC123456
Line 85: CD7 
Line 86: UPC123456
Line 87: 
Line 88: --- 페이지 282 ---
Line 89: Some Amelioration 
Line 90: 259
Line 91: once before a series of tests that do not affect the setup [Koskela02]. In this par-
Line 92: ticular case, if the tests that are run add more rentals to ID 007 and this setup is 
Line 93: not rerun, ID 007 may reach the rental limit. Subsequent tests that assume he is 
Line 94: not at the limit will fail. 2
Line 95: Some Amelioration 
Line 96: You can do some things to ameliorate potential problems. First, never change 
Line 97: existing data in the setup. Add to the setup if you need a different entity. For 
Line 98: example, if you need a customer with different characteristics, add another cus-
Line 99: tomer. Some teams give names to the entities; customers who represent the kind 
Line 100: of entity they are dealing with might be Big Spender, Prompt Returner, and so 
Line 101: forth. For example, instead of Customer ID 88 being named Maxwell, he might 
Line 102: be named Customer Who Reached Limit if the previous Rental table was used. 
Line 103: Another way of handling the issue is not to have a common setup that is used 
Line 104: for every test, but ones that are common to a group of tests. The number of tests 
Line 105: that a change in the setup can affect is limited. 
Line 106: Still another way is to create variables in the common setup. For example, 
Line 107: you might deﬁne a variable (as shown in  Chapter 17, “Decouple with Inter-
Line 108: faces”) to contain James’s credit card, such as 
Line 109: 4005550000000019 → JAMES_CREDIT_CARD
Line 110: In each of the tests, you would reference JAMES_CREDIT_CARD rather 
Line 111: than the number. 3 For example, in the setup for the credit-card charges ( Chapter
Line 112: 11, “System Boundary”), you might use the following. 
Line 113: Credit-Card Charges from Rental System 
Line 114: Day = 1/21/2011 
Line 115: Card Number 
Line 116: Customer Name 
Line 117: Amount 
Line 118: Time
Line 119: ←JAMES_CREDIT_CARD 
Line 120: James 
Line 121: $2 
Line 122: 10:53 a.m. 
Line 123:   2.  The approach taken starts to deﬁne a test architecture [Rup01], which should be 
Line 124: designed with the same care as the application. 
Line 125:   3 . This is an example of the DRY—Don’t Repeat Yourself—Principle from the Prag-
Line 126: matic Programmers [Hunt01]. It is also known as the Once and Only Once Princi-
Line 127: ple. A corollary of this principle is Shalloway’s Law. If there are N places where a 
Line 128: change has to be made, Shalloway will ﬁnd N–1 of them. 
Line 129: 
Line 130: --- 페이지 283 ---
Line 131:  
Line 132: Chapter 31 Test Setup
Line 133: 260
Line 134: Still another way of making tests less dependent on the setup is to use rela-
Line 135: tive results. For example, you might be testing the ability to add a customer, 
Line 136: say Napolean Solo. Using this setup and an absolute result, the test would ﬁrst 
Line 137: check that there is one customer in the customer data, perform the add, and 
Line 138: check the result to see that there are two customers. Using a relative result, the 
Line 139: test would ﬁrst determine the current number of customers and then check to see 
Line 140: that the number of customers after the addition of Napolean Solo was the previ-
Line 141: ous number plus one. 4 In both cases, the test would also check that Napolean 
Line 142: Solo was a customer. 
Line 143: Test Order 
Line 144: In many acceptance test frameworks, you have control over the sequence in which 
Line 145: tests are run. 5 If a test has no side effects, the order in which it is run relative to 
Line 146: other tests is unimportant. A side effect is a change to the state of the system or 
Line 147: an output to an external repository, as shown in Chapter 8, “Test Anatomy.” If 
Line 148: a test does have a side effect on the shared setup, such as deleting a customer, you 
Line 149: may need to run the tests in an order such that the deletion comes last. 
Line 150: You may be able to take advantage of complementary side effects. Suppose 
Line 151: one test adds a customer and another test deletes a customer. If you run these 
Line 152: tests one right after the other, the side effects should cancel out. 6
Line 153: Running tests in a particular order, just like dependence on a common setup, 
Line 154: requires discipline. It can decrease the amount of testing code, because a test 
Line 155: assumes that the previous test has successfully executed. But maintenance of 
Line 156: the tests may accidentally change the order and cause tests to break, or it could 
Line 157: change the results of tests that later tests in the order depend upon. If tests are 
Line 158: tied together to run in a particular order, reproducing a test that fails requires 
Line 159: running all the preceding tests. 
Line 160: Persistent Storage Issues 
Line 161: Often, tests include altering entries in persistence storage, such as a database. 
Line 162: Even if the tests do not use the same entities, such as customers, they may leave 
Line 163:   4.  A relative result is also referred to as a delta. A test that uses a relative result is called 
Line 164: a delta test.
Line 165:   5 . This is not the case for unit test frameworks. 
Line 166:   6 . A log of operations can include entries on both of these operations. So the side effect 
Line 167: of logging is not cancelled out. 
Line 168: 
Line 169: --- 페이지 284 ---
Line 170: Summary 
Line 171: 261
Line 172: the database in a state in which it is not ready for the tests to be run again. In 
Line 173: that case, you need to restore the database to its original state. 
Line 174: Depending on your test environment, you may have a couple of technical 
Line 175: solutions to this problem. One solution is to simply restore the database from 
Line 176: a backup copy. Although this takes some time, it may be small relative to the 
Line 177: amount of time for all the tests. Alternatively, you could execute the tests within 
Line 178: a virtual machine. The virtual machine is closed upon test completion, and a 
Line 179: new clone of the virtual machine is used for the next test [Devx01]. 
Line 180: A database on a test platform may consist of many records, so it may take 
Line 181: considerable time to restore the entire database. You could create a procedure 
Line 182: that backs up and then restores just the entities that have been affected by the 
Line 183: test. Alternatively, you could have a process that eliminates all traces of an entity 
Line 184: such as a customer. Then the tests could create that entity and use it for further 
Line 185: tests.7 Another approach to restoring persistent data to its original state, partic-
Line 186: ularly for tests that add to the data, rather than modify it, is to time-stamp every 
Line 187: record. When the test is over, you would delete all records whose timestamps 
Line 188: are equal to or after the time at the beginning of the test. You could also create 
Line 189: a log of records that have been modiﬁed during the tests and restore the original 
Line 190: record once the tests have completed. 
Line 191: If you don’t have control of the database, what you can do is document 
Line 192: what the state of the system should be in the “Given” part of the tests. Then 
Line 193: if the state is not as expected, the test will fail not in the “When” part, but in 
Line 194: the “Given” part. That clariﬁes it is not the action that caused the failure. For 
Line 195: example, suppose you are testing adding a customer and the customer you want 
Line 196: to add is ID 99. You need to ensure that the customer does not already exist. So 
Line 197: you place this in the “Given” section. If you have a lot of these conditions, you 
Line 198: might separate them from the “Given” into an “Assume” section. 
Line 199: Customer Data 
Line 200: Name 
Line 201: ID 
Line 202: Exists?
Line 203: Agent 
Line 204: 99 
Line 205: No
Line 206: Summary
Line 207: •  There is a trade-off in eliminating redundancy and causing dependencies 
Line 208: between a common test setup and individual test setups. 
Line 209:   7.  This is like what happened to George Bailey in It’s a Wonderful Life.
Line 210: 
Line 211: --- 페이지 285 ---
Line 212: Chapter 31 Test Setup
Line 213: 262
Line 214: • Use a common setup to create a test bed for further tests. 
Line 215: • Be cautious of tests that have side effects that alter conditions for other 
Line 216: tests.
Line 217: • If using shared resources, document assumptions as to their condition. 