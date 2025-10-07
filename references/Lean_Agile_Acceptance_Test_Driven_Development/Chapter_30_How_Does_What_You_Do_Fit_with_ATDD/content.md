Line 1: 
Line 2: --- 페이지 274 ---
Line 3: Chapter 30 
Line 4: How Does What You Do Fit 
Line 5: with ATDD? 
Line 6: “Then the part comes to me and it ﬁts like a glove because it’s actually 
Line 7: written about me... All I had to do was show up and learn the lines.”
Line 8: David Carradine 
Line 9: This chapter presents topics that are aimed at developers and testers, rather than 
Line 10: customers. It examines testing and designing. 
Line 11: Test Platforms 
Line 12: Depending on how long it takes to run the tests, you can run them at different 
Line 13: times. Tests on a developer’s machine should run pretty quickly. When the code 
Line 14: is transferred to the integration platform, you can run a series of longer tests. 
Line 15: There is a limit, however, to the number of tests that can be run in a short time, 
Line 16: say 15 minutes. So a smoke test 1 is used that consists of the most risky or the 
Line 17: most relevant. 
Line 18: You can run longer-running tests on a separate platform (see Figure 30.1).
Line 19: There can be a set that is run at least a few times during the day, a set run at 
Line 20: night, another set over the weekend, or still another for a week at a time. If the 
Line 21: tests are successful on one platform, you start running the longer set on the next 
Line 22: 251
Line 23:   1 . The term derives from electrical engineers who used to design and build a circuit. If 
Line 24: the circuit smoked when they turned it on, they knew immediately that something 
Line 25: was wrong [Wiki04]. 
Line 26: 
Line 27: --- 페이지 275 ---
Line 28: Chapter 30 How Does What You Do Fit with ATDD?
Line 29: 252
Line 30: platform. You probably can’t imagine tests that last a week, but a number of 
Line 31: complex systems require that long (and even longer). 2
Line 32: Quick
Line 33: Tests
Line 34: (Developer’s
Line 35: Platform)
Line 36: 15-Minute Test
Line 37: Suite
Line 38: Part of Build
Line 39: (Integration
Line 40: Platform)
Line 41: Longer Test
Line 42: Suite
Line 43: Started by
Line 44: Successful
Line 45: Build
Line 46: (Test Platform)
Line 47: 12-Hour Test
Line 48: Suite
Line 49: Nightly
Line 50: (Test Platform)
Line 51: 48-Hour Test
Line 52: Suite
Line 53: Weekend
Line 54: (Test Platform)
Line 55: 168-Hour Test
Line 56: Suite
Line 57: Weekly
Line 58: (Test Platform)
Line 59: Figure 30.1 Test Timing 
Line 60: 2. Tests of compilers can take a long time. 
Line 61: A Little More Testing 
Line 62: In March 2007, a large airline migrated seven million reservations from 
Line 63: the Sabre reservation system to SHARES, another reservation system. 
Line 64: About one and a half million reservations did not transfer correctly. Pas-
Line 65: sengers could not check-in for their ﬂights. Kiosks in many cities stopped 
Line 66: working. The conversion took place over a weekend. On Sunday, many 
Line 67: passengers were stranded outside the security line because they could not 
Line 68: obtain a boarding pass. Many millions of dollars in revenue were lost, not 
Line 69: to mention customer dissatisfaction. 
Line 70: A little more testing might have gone a long way toward preventing the 
Line 71: problem [Fast01]. 
Line 72: Internal Design from Tests 
Line 73: There has been little discussion on the internal design of an application. The one 
Line 74: suggestion was to make the module implementing a business rule easily avail-
Line 75: able to testing, such as shown in Figure 30.2.
Line 76: The Model-View-Controller pattern states that the model should be sepa-
Line 77: rated from the view and controller. In this case, the model is the business rule 
Line 78: for determining whether a customer can reserve a CD. The view is how the user 
Line 79: 
Line 80: --- 페이지 276 ---
Line 81: Internal Design from Tests 
Line 82: 253
Line 83: sees the result of this business rule—button or dialog box. The controller is how 
Line 84: the user can make a reservation—the reservation dialog box. The view and the 
Line 85: controller should be coded separated from the model. 
Line 86: Reservation
Line 87: Allowed
Line 88: Module
Line 89: Reservation Test
Line 90: User
Line 91: Interface
Line 92: Test
Line 93: Figure 30.2 User Interface and Logic Tests 
Line 94: The tests in Chapter 14, “Separate View from Model,” showed how the sepa-
Line 95: ration of the model from the view made the tests simpler. The simpler tests show 
Line 96: up as simpler code. For example, suppose that the method used to determine 
Line 97: whether a customer is allowed to reserve is called: 
Line 98: Boolean Customer.allowedToReserve() 
Line 99: What this method does is obvious from its name. It returns whether a cus-
Line 100: tomer is allowed to reserve by calculating the result according to Sam’s busi-
Line 101: ness rule. The tests in Chapter 13, “Simpliﬁcation by Separation,” apply to this 
Line 102: method.
Line 103: The tests in Chapter 14 apply to the display. Because the calculation has 
Line 104: already been tested, the display need only be tested to see if it displays appropri-
Line 105: ately. Simple tests usually correspond to simple underlying code. For example, 
Line 106: the way the display code would look if the button was to be enabled or disabled 
Line 107: might be this: 
Line 108: if (customer.allowedToReserve())
Line 109:     enableReserveButton()
Line 110:  else
Line 111:     disableReserveButton() 
Line 112: If the button were to be shown or hidden, it might look like this: 
Line 113: if (customer.allowedToReserve()
Line 114:    showReserveButton()
Line 115: else
Line 116:    hideReserveButton() 
Line 117: 
Line 118: --- 페이지 277 ---
Line 119: Chapter 30 How Does What You Do Fit with ATDD?
Line 120: 254
Line 121: If there were different dialog boxes, it could be this: 
Line 122: OnReserveButtonClick() {
Line 123:     if (customer.allowedToReserve())
Line 124:        displayReservationDialog();
Line 125:     else
Line 126:        displayNotAllowedToReserveDialog();
Line 127:     } 
Line 128: In any case, the two tests to run for a customer who is allowed to reserve and 
Line 129: one who is not allowed to reserve will execute all the paths in this code. You 
Line 130: don’t have to run all the tests as shown in Chapter 13.
Line 131: Device Testing 
Line 132: Every external device should have its own set of tests. For example, Debbie is 
Line 133: investigating use a bar code scanner to read the CD ID and the customer ID. 
Line 134: She needs to create developer tests for the bar code scanner to ensure that the 
Line 135: scanner can properly read the bar code. These are going to be manual tests un-
Line 136: less Debbie can get a robot that will move the scanner. Here are some tests she 
Line 137: might come up with: 
Line 138: • Check that scanning a vendor-supplied bar code produces the correct out-
Line 139: put.
Line 140: • Create a bar code image with the printer, scan it, and check that the output 
Line 141: matches.
Line 142: • Try scanning at different speeds, and check the output. 
Line 143: • Scan in both directions, and check the output. 
Line 144: Tom might come up with these ideas: 
Line 145: • Try a dirty bar code to see if it is readable. 
Line 146: • Try a ripped bar code to see if it is readable or produces an error. 
Line 147: • Try scanning a bar code in an off-axis direction. 
Line 148: You need to do all these tests with the device itself. These are developer accept-
Line 149: ance tests. The change in input devices from the keyboard does not require new 
Line 150: acceptance tests from the customer. Debbie will have at least one acceptance test 
Line 151: that goes through the user interface to ensure that the connection to the scan-
Line 152: ner is properly made. But she does not have to test all the previous conditions 
Line 153: 
Line 154: --- 페이지 278 ---
Line 155: Black Box Testing 
Line 156: 255
Line 157: through the user interface unless she identiﬁes some risk in the integration of the 
Line 158: scanner with the system. 
Line 159: Starting with User Interfaces 
Line 160:  
Line 161: Some customers want to see user interface prototypes as part of the requirement 
Line 162: process. You can use these prototypes as the basis for acceptance tests through 
Line 163: the user interface or through the middle tier. 
Line 164: Once the user interface prototype is approved, you can employ it as the basis 
Line 165: for tests. For each display screen, assign every entry ﬁeld a label. For each screen, 
Line 166: make up an action table with those labels. The tests can execute the action table 
Line 167: either through the user interface or through the middle tier. Add “given” and 
Line 168: “then” parts to the tests that give the conditions—the data required—and the 
Line 169: expected results. Then create tables that show the business rules that apply to 
Line 170: combinations of inputs, such as the ones presented in this book. The tables will 
Line 171: clarify the cases that you may have missed by just looking at the user interface. 
Line 172: Black Box Testing 
Line 173: Acceptance test-driven development (ATDD) is closely related to black box test-
Line 174: ing. Both are independent of the implementation underneath, so common black 
Line 175: box techniques apply. These include 3 the following: 
Line 176: • Equivalence partitioning, which divides inputs into groups that should ex-
Line 177: hibit similar behavior. (See the tests in Chapter 10, “User Story Breakup,” 
Line 178: section “Business Rule Tests.”) 
Line 179: • Boundary value analysis, which tests values at the edge of each equivalence 
Line 180: partition. (See the example discount percentage tests in Chapter 4, “An 
Line 181: Introductory Acceptance Test,” section “An Example Business Rule.”) 
Line 182: • State transition testing checks the response from a system that depends on 
Line 183: its state. (See Chapter 15, “Events, Responses, and States,” section “States 
Line 184: and State Transitions.”) 
Line 185: • Use case testing to check all paths through a use case. (See the Check-Out 
Line 186: Use Case in Chapter 7, “Collaborating on Scenarios.”) 
Line 187:   3.  See [Myers01] or [Kaner01] for details on these techniques. 
Line 188: 
Line 189: --- 페이지 279 ---
Line 190: Chapter 30 How Does What You Do Fit with ATDD?
Line 191: 256
Line 192: • Decision table testing for complex business rules. (See “The Simpliﬁed 
Line 193: Rule” in Chapter 13.) Often, the decision table is presented in the opposite 
Line 194: format, where rows and columns are interchanged from the format used 
Line 195: in this book. This book’s format follows that of many of the automated 
Line 196: testing tools. 
Line 197: Unit Testing 
Line 198: Unit tests help with the design and quality of the implementation. You get more 
Line 199: immediate feedback with unit tests, because only a small chunk of code is being 
Line 200: tested. It may take a while to implement enough code to pass an acceptance test. 
Line 201: You don’t want to duplicate testing between unit tests and acceptance tests. 
Line 202: In many cases, business rule tests can be written in a unit test framework, as 
Line 203: shown in Chapter 4. The purpose of acceptance tests is communication. Keeping 
Line 204: customer-provided tests in a form that customers can understand helps in this 
Line 205: communication.
Line 206: If the terminology in an acceptance test changes, you may want to propagate 
Line 207: the changes to the classes and methods in an implementation to keep things in 
Line 208: sync.4
Line 209: Summary
Line 210: • Run acceptance tests as often as possible. 
Line 211: • Test devices separately from their connection to the system. 
Line 212: • Use black box testing techniques to develop acceptance tests. 
Line 213:   4.  See [Adjic01] for more tester and developer issues. 