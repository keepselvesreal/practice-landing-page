Line 1: 
Line 2: --- 페이지 52 ---
Line 3: Chapter 4 
Line 4: An Introductory 
Line 5: Acceptance Test 
Line 6: “If you don’t know where you’re going, you will wind up somewhere 
Line 7: else.”
Line 8: Yogi Berra 
Line 9: An example of an acceptance test is presented, along with four ways that you 
Line 10: can execute an acceptance test. 
Line 11: A Sample Business Rule 
Line 12: Here is an example from a previous project where Debbie and Tom created tests 
Line 13: in collaboration with the customer. The business representative, Betty, presented 
Line 14: the two of them with a business rule for giving discounts that she had obtained 
Line 15: from one of the stakeholders. The stakeholder wanted to give discounts to the 
Line 16: ﬁrm’s customers based on what type of customer they were. Debbie had already 
Line 17: completed implementing a previous requirement that determined the customer 
Line 18: type. Here’s the rule that Betty gave them: 
Line 19: If Customer Type is Good and Item Total is less than or equal to $10.00, 
Line 20: Then do not give a discount, 
Line 21: Otherwise, give a 1% discount. 
Line 22: If Customer Type is Excellent, 
Line 23: Then give a discount of 1% for any order. 
Line 24: If Item Total is greater than $50.00, 
Line 25: Then give a discount of 5%. 
Line 26: 29
Line 27: 
Line 28: --- 페이지 53 ---
Line 29: Chapter 4 An Introductory Acceptance Test 
Line 30: 30
Line 31: This rule may seem clear. It uses consistent terms, such as Customer Type
Line 32: and Item Total. Debbie and Tom had previously gotten from Betty the deﬁni-
Line 33: tions of those terms [Evans01]. For example, Item Total did not include taxes or 
Line 34: shipping. But even with that consistency, there was an issue. Tom and Debbie 
Line 35: looked at the rule and tried to ﬁgure out what the discount percentage should 
Line 36: be if a customer who is good had an order total greater than $50.00. So Betty, 
Line 37: Debbie, and Tom made up a table of examples. 1
Line 38: Discount Calculation 
Line 39: Item Total 
Line 40: Customer Rating 
Line 41: Discount Percentage? 
Line 42: $10.00 
Line 43: Good 
Line 44: 0%
Line 45: $10.01 
Line 46: Good 
Line 47: 1%
Line 48: $50.01 
Line 49: Good 
Line 50: 1% ?? 
Line 51: $.01 
Line 52: Excellent 
Line 53: 1%
Line 54: $50.00 
Line 55: Excellent 
Line 56: 1%
Line 57: $50.01 
Line 58: Excellent 
Line 59: 5%
Line 60: The answers in this table of examples are going to be used to test the imple-
Line 61: mentation. The ﬁrst two rows show that the limit between giving a good cus-
Line 62: tomer no discount or a 1% discount is $10.00. The “less than or equal to” in 
Line 63: the business rule is pretty clear. The tests just ensure that the implementation 
Line 64: produced that result. The ?? was put after the 1 in the third example because it 
Line 65: was unclear to the triad whether that was the right value. To what type of cus-
Line 66: tomer did the last statement in the rule apply? 
Line 67: The fourth row indicates that the discount for an excellent customer starts at 
Line 68: the smallest possible Item Total. The ﬁfth and sixth entries show that the dis-
Line 69: count increases just after the $50.00 point. 2
Line 70: Betty took this table back to the stakeholder. He looked it over and said that 
Line 71: the interpretation was correct. He did not want to give a 5% discount to good 
Line 72: customers. So ?? from that result was removed from that cell. There was now a 
Line 73: set of tests that could be applied to the system. The correct discount amount test 
Line 74: is not just a single case but includes cases for all possible combinations. 
Line 75: Tom suggested other possibilities. For example, what if Item Total was less 
Line 76: than $0.00? Tom asked Betty whether this would ever happen. She said it might 
Line 77:   1 . See  Appendix D, “Tables Everywhere,” for an example of putting the rule into a 
Line 78: table.
Line 79:   2 . There could be even more interpretations of this business rule, as reviewers pointed 
Line 80: out. For example, if Customer Rating is any other type than Good or Excellent, 
Line 81: what should the discount be? 
Line 82: 
Line 83: --- 페이지 54 ---
Line 84: Implementing the Acceptance Tests 
Line 85: 31
Line 86: be possible, because Item Total could include a rebate coupon that was greater 
Line 87: than the total of the items. So Tom added the following possibilities. 
Line 88: Discount Calculation 
Line 89: Item Total 
Line 90: Customer Rating 
Line 91: Discount Percentage? 
Line 92: $–.01 
Line 93: Good 
Line 94: 0%
Line 95: $–.01 
Line 96: Excellent 
Line 97: 1% ?? 
Line 98: Tom explained that it didn’t seem right to apply a discount percentage that 
Line 99: would actually increase the amount that the customer owed. Based on this 
Line 100: example, Betty went back to the stakeholder and conﬁrmed that the percentage 
Line 101: should be 0% if Item Total is less than 0 for any customer. So the table became 
Line 102: as follows. 
Line 103: Discount Calculation 
Line 104: Item Total 
Line 105: Customer Rating 
Line 106: Discount Percentage? 
Line 107: $–.01 
Line 108: Good 
Line 109: 0%
Line 110: $–.01 
Line 111: Excellent 
Line 112: 0%
Line 113: These examples were the acceptance tests for the system. If Debbie imple-
Line 114: mented these correctly, Betty would be satisﬁed. Now it was a matter of how 
Line 115: Debbie and Tom were going to use these tests to test the system. 
Line 116: Implementing the Acceptance Tests 
Line 117: Tom and Debbie needed to apply these tests to the implementation they were 
Line 118: developing. There were at least four possible ways to do this. First, Tom could 
Line 119: create a test script that operates manually at the user interface level. Second, 
Line 120: Debbie could create a test user interface that allows her or Tom to check the 
Line 121: appropriate discount percentages. Third, Debbie could perform the tests using 
Line 122: a unit testing framework. Fourth, Tom and Debbie could implement the tests 
Line 123: with an acceptance test framework. Following are examples of how they could 
Line 124: use each of these possibilities. 
Line 125:  
Line 126: Test Script 
Line 127: In this case, the program has a user interface that allows a customer to enter an 
Line 128: order. The user interface ﬂow is much like Amazon or other order sites. The user 
Line 129: enters an order and a summary screen appears, such as the one in Figure 4.1.
Line 130: 
Line 131: --- 페이지 55 ---
Line 132: Chapter 4 An Introductory Acceptance Test 
Line 133: 32
Line 134: Order Summary
Line 135: Count 
Line 136: Item 
Line 137: Item Price 
Line 138: Total
Line 139: 10 
Line 140: Little Widget
Line 141: Big Widget
Line 142: $.10 
Line 143: $1.00
Line 144: 1 
Line 145: $9.00 
Line 146: $9.00
Line 147: Item Total 
Line 148: $10.00
Line 149: Discount 
Line 150: $0.00
Line 151: Taxes 
Line 152: $.55
Line 153: Shipping 
Line 154: $2.00
Line 155: Order Total 
Line 156: $12.55
Line 157: Order Summary
Line 158: Place Order 
Line 159: Cancel
Line 160: Figure 4.1 Order Interface 
Line 161: What Tom would have to do is to create a script that either he or Debbie 
Line 162: would follow to test each of the six cases in the Discount Calculation table. He 
Line 163: might start by computing what the actual discount amount should be for each 
Line 164: case. Unless the Order Summary screen shows this percentage, this value is the 
Line 165: only output Tom can check to ensure the calculation is correct. Here is an addi-
Line 166: tion to the table that shows the amounts he needs to look for. 
Line 167: Discount Calculation 
Line 168: Item Total 
Line 169: Customer
Line 170: Rating
Line 171: Discount
Line 172: Percentage?
Line 173: Discount
Line 174: Amount? 
Line 175: Notes
Line 176: $10.00 
Line 177: Good 
Line 178: 0% 
Line 179: $0.00
Line 180: $10.01 
Line 181: Good 
Line 182: 1% 
Line 183: $0.10 
Line 184: Discount rounded down 
Line 185: $50.01 
Line 186: Good 
Line 187: 1% 
Line 188: $0.50 
Line 189: Discount rounded down 
Line 190: $.01 
Line 191: Excellent 
Line 192: 1% 
Line 193: $0.00 
Line 194: Discount rounded down 
Line 195: $50.00 
Line 196: Excellent 
Line 197: 1% 
Line 198: $0.50
Line 199: $50.01 
Line 200: Excellent 
Line 201: 5% 
Line 202: $2.50 
Line 203: Discount rounded down 
Line 204: 
Line 205: --- 페이지 56 ---
Line 206: Implementing the Acceptance Tests 
Line 207: 33
Line 208: The script would go something like this: 
Line 209: 1. Log on as a customer who has the rating listed in the table. 
Line 210: 2. Start an order, and put items in it until the total is the speciﬁed amount in 
Line 211: the Item Total column on the test. 
Line 212: 3. Check that the discount on the Order Summary screen matches Discount 
Line 213: Amount in the table. 
Line 214: Then the test would be repeated ﬁve more times to cover all six cases. Either 
Line 215: Tom or Debbie would do this once the discount feature and order features are 
Line 216: implemented. This test should be run for all possible combinations. That would 
Line 217: have been more difﬁcult if there were more discount percentages for more cus-
Line 218: tomer types. There’s another possible way to run these tests. 
Line 219: Test User Interface 
Line 220: To simplify executing the tests, Debbie could set up a user interface that con-
Line 221: nects to the discount calculation module in her code. This interface would be 
Line 222: used only during testing. But having it would cut down on the work involved in 
Line 223: showing that the percentage was correctly determined. The interface might be a 
Line 224: command-line interface (CLI) or a graphical user interface (GUI). For example, 
Line 225: a CLI might be this: 
Line 226: RunDiscountCalculatorTest  <item_total> <customer_type> 
Line 227: And when it is run for each case, such as 
Line 228: RunDiscountCalculatorTest 10,00 Good 
Line 229: It would output the result 
Line 230: 0
Line 231: A GUI, such as what’s shown in Figure 4.2, might be connected to the CLI. 
Line 232: Regardless of whether it is a GUI or CLI, the user interface has penetrated 
Line 233: into the system. It exposes a test point within the system that allows easier test-
Line 234: ing. Here’s an analogy showing the differences between this method and Tom’s 
Line 235: original test script. Suppose you want to build a car that accelerates quickly. 
Line 236: You know you need an engine that can increase its speed rapidly. If you could 
Line 237: only check the engine operation as part of the car, you would need to put the 
Line 238: engine in the car and then take the car on a test drive. If you had a test point 
Line 239: for the engine speed inside the car, you could check how fast the engine sped up 
Line 240: without driving the car. You could measure it in the garage. You’d save a lot of 
Line 241: 
Line 242: --- 페이지 57 ---
Line 243: Chapter 4 An Introductory Acceptance Test 
Line 244: 34
Line 245: time in on-the-road testing if the engine wasn’t working properly. That doesn’t 
Line 246: mean you don’t need to test the engine on the road. But if the engine isn’t work-
Line 247: ing by itself, you don’t run the road test until the engine passes its own tests. 
Line 248: If you’re not into cars, Figure 4.3 shows a context diagram. The Order Sum-
Line 249: mary screen connects to the system through the standard user interface layer. 
Line 250: The Discount Percentage user interface connects to some module inside the sys-
Line 251: tem. Let’s call that module the Discount Calculator. By having a connection to 
Line 252: the inside, a tester can check whether the internal behavior by itself is correct. 
Line 253: Order
Line 254: Summary
Line 255: Screen
Line 256: User Interface
Line 257: Discount Percentage
Line 258: User Interface
Line 259: Interior of
Line 260: Application,
Line 261: Discount
Line 262: Calculator
Line 263: Figure 4.3 Context Diagram 
Line 264: xUnit Test 
Line 265: The next way to perform the testing is to write the tests for the Discount Cal-
Line 266: culator in a unit testing framework. The framework used is usually in the lan-
Line 267: guage that the program is written in. There is a generic framework called xUnit 
Line 268: Customer Type 
Line 269: Good
Line 270: Item Total 
Line 271: 10.01
Line 272: Percentage 
Line 273: 1%
Line 274: Discount Percentage Test
Line 275: Figure 4.2 User Interface for Testing 
Line 276: 
Line 277: --- 페이지 58 ---
Line 278: Implementing the Acceptance Tests 
Line 279: 35
Line 280: that has versions for many programming languages. Here’s a sample of what 
Line 281: these tests look like in Java using Junit [Beck01]. The test would look similar in 
Line 282: TestNG [Beust01], but the order of the parameters would be reversed: 
Line 283: class DiscountCalculatorTest  {
Line 284:    @Test
Line 285:    public void shouldCalculateDiscountPercentageForCustomer() {
Line 286:       DiscountCalculator dc = new DiscountCalculator();
Line 287:       assertEquals(0, dc.computeDiscountPercentage(10.0,
Line 288:          Customer.Good));
Line 289:       assertEquals(1, dc.computeDiscountPercentage (10.01,
Line 290:          Customer.Good));
Line 291:       assertEquals(1, dc.computeDiscountPercentage (50.01,
Line 292:          Customer.Good));
Line 293:       assertEquals(1, dc.computeDiscountPercentage(.01,
Line 294:          Customer.Excellent));
Line 295:       assertEquals(1, dc.computeDiscountPercentage(50.0,
Line 296:          Customer.Excellent));
Line 297:       assertEquals(5, dc.computeDiscountPercentage(50.01,
Line 298:          Customer.Excellent));
Line 299:    }
Line 300: }
Line 301: Any time there is a change in the examples that Betty and the stakeholder 
Line 302: use to explain the business rule, Debbie may want these tests to conform to the 
Line 303: changed examples. That’s a bit of waste. The next testing framework can elimi-
Line 304: nate that waste. 
Line 305: Automated Acceptance Test 
Line 306: Betty, Debbie, and Tom agreed that the examples in the table accurately re-
Line 307: ﬂected the requirements and there would be less waste if the table did not have 
Line 308: to be converted into another form for testing. Several available acceptance test 
Line 309: frameworks use tables. Some examples are in Appendix C, “Test Framework 
Line 310: Examples.” With these frameworks, you describe the tests with a table similar 
Line 311: to the one for the example. 
Line 312: The following test table works in table-based frameworks, such as the Fit-
Line 313: Nesse and Fit frameworks. A similar style table can be used in narrative-form 
Line 314: frameworks, such as Cucumber. 3 The table looks practically like the one that 
Line 315: Betty presented to the stakeholder. 
Line 316:   3 . Fit is the Framework for Integrated Tests, developed by Ward Cunningham [Cun-
Line 317: ningham01], [Cunningham02]. Fit was incorporated into FitNesse by Bob Martin 
Line 318: [Martin01]. Cucumber can be found in [Chelimsky01]. 
Line 319: 
Line 320: --- 페이지 59 ---
Line 321: Chapter 4 An Introductory Acceptance Test 
Line 322: 36
Line 323: Discount Calculation 
Line 324: Item Total 
Line 325: Customer Rating 
Line 326: Discount Percentage() 
Line 327: $10.00 
Line 328: Good 
Line 329: 0%
Line 330: $10.01 
Line 331: Good 
Line 332: 1%
Line 333: $50.01 
Line 334: Good 
Line 335: 1%
Line 336: $.01 
Line 337: Excellent 
Line 338: 1%
Line 339: $50.00 
Line 340: Excellent 
Line 341: 1%
Line 342: $50.01 
Line 343: Excellent 
Line 344: 5%
Line 345: Now when the table is used as a test, the Fit/FitNesse framework executes 
Line 346: code that connects to the Discount Calculator. It gives the Discount Calculator 
Line 347: the values in Item Total and Customer Rating. The Discount Calculator returns 
Line 348: the Discount Percentage. The framework compares the returned value to the 
Line 349: value in the table. If it agrees, the column shows up in green. If it does not, it 
Line 350: shows up in red. The colors cannot be seen in this black-and-white book. So 
Line 351: light gray represents green and dark gray represents red. The ﬁrst time the test 
Line 352: was run, the following table was output. 
Line 353: Discount Calculation 
Line 354: Item Total 
Line 355: Customer Rating 
Line 356: Discount Percentage() 
Line 357: $10.00 
Line 358: Good
Line 359: 0%
Line 360: $10.01 
Line 361: Good
Line 362: 1%
Line 363: $50.01 
Line 364: Good
Line 365: Expected 1% Actual 5% 
Line 366: $.01 
Line 367: Excellent
Line 368: 1%
Line 369: $50.00 
Line 370: Excellent
Line 371: 1%
Line 372: $50.01 
Line 373: Excellent
Line 374: 5%
Line 375: With the results shown in the table, it was apparent there was an error in the 
Line 376: Discount Calculator. Once it was ﬁxed, Betty saw the passing tests as conﬁrma-
Line 377: tion that the calculation was working as desired. 
Line 378: An Overall Test 
Line 379: If the discount test is applied using one of the last three forms, there still needs 
Line 380: to be a test using the order interface. This ensures that processing an order is 
Line 381: correctly connected to the Discount Calculator. The script for an order would be 
Line 382: run for a couple of instances. But unless there was a large risk factor involved, 
Line 383: the script might just be executed for a few cases, such as the following. 
Line 384: 
Line 385: --- 페이지 60 ---
Line 386: Summary 
Line 387: 37
Line 388: Discount Calculation 
Line 389: Item Total 
Line 390: Customer Rating 
Line 391: Discount Percentage? 
Line 392: Discount Amount? 
Line 393: $10.01 
Line 394: Good 
Line 395: 1% 
Line 396: $0.10
Line 397: $50.01 
Line 398: Excellent 
Line 399: 5% 
Line 400: $2.50
Line 401: Testing Process 
Line 402: The acceptance test is the original table that Betty, Tom, and Debbie developed 
Line 403: to clarify the business rule. This acceptance test can be used at four different 
Line 404: levels, as described earlier in this chapter. Because the acceptance test was cus-
Line 405: tomer supplied, all four levels are considered acceptance tests in this book. The 
Line 406: last two forms are automated by their nature. The second form—an interface to 
Line 407: the Discount Calculator—can be automated. The test for an order could also be 
Line 408: automated with a little more effort. However, you should still check it manually 
Line 409: as well. 
Line 410: Passing the acceptance tests is necessary but insufﬁcient to ensure that the 
Line 411: system meets the customer needs. Other tests, such as those for quality attributes 
Line 412: and usability (described in Chapter 3, “Testing Strategy”), also need to be 
Line 413: passed. See [Meszaros02] for more information. 
Line 414: Summary
Line 415: •  Examples of requirements clarify the requirements. 
Line 416: •  The examples can be used as tests for the implementation of the require-
Line 417: ments.
Line 418: •  Tests for business rules can be executed in at least these four ways: 
Line 419: • Creation through the user interface of a transaction that invokes the 
Line 420: business rule 
Line 421: • Development of a user interface that directly invokes the business rule 
Line 422: • A unit test implemented in a language’s unit testing framework 
Line 423: • An automated test that communicates with the business rule module 
Line 424: 
Line 425: --- 페이지 61 ---
Line 426: This page intentionally left blank 