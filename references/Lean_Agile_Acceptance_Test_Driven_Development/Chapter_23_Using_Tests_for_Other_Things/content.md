Line 1: 
Line 2: --- 페이지 222 ---
Line 3: Chapter 23 
Line 4: Using Tests for Other Things 
Line 5: “By ﬁghting, you never get enough, but by yielding, you get more than 
Line 6: you expected.”
Line 7: Lawrence G. Lovasik 
Line 8: Acceptance tests deﬁne the functionality of a program. But you can use them 
Line 9: for more than just that—measuring doneness, estimating, and breaking down 
Line 10: a story. 
Line 11: Uses of Acceptance Tests 
Line 12: Acceptance tests are a communication mechanism between the members of the 
Line 13: triad. They clarify the customer requirements and are a speciﬁcation of how the 
Line 14: system works. But you can also employ them for other purposes. They are a 
Line 15: measure of how complete an implementation is; a means of estimating the effort 
Line 16: to implement a story, and a method for story breakdown. 
Line 17: Degree of Doneness 
Line 18: If there are multiple acceptance tests for a business rule or a story, the ratio of 
Line 19: successful tests to the total number of tests can provide a rough guide to how 
Line 20: much of the story has been implemented. For example, if you have ten accept-
Line 21: ance tests and three are passing, the story is “about” 30% complete. 
Line 22: It is possible that the “worst” test case was saved for last. So the effort to 
Line 23: implement that story represents more than its fair share of the total effort. That 
Line 24: is why this is only a guide to doneness, rather than an exact measurement. 
Line 25: Make all the tests pass for a story before moving to another story. Otherwise, 
Line 26: you may wind up with lots of stories that are not done. 
Line 27: 199
Line 28: 
Line 29: --- 페이지 223 ---
Line 30: Chapter 23 Using Tests for Other Things
Line 31: 200
Line 32: Estimation Aid 
Line 33: An estimate may be required for implementing a story in many environments. 
Line 34: The number and complexity of the acceptance tests can be a rough guide to the 
Line 35: effort required to implement a story. The tests for a new story can be compared 
Line 36: to the tests run against completed stories. You can develop your own heuristics 
Line 37: as to how the number and complexity inﬂuence the effort. Large custom setups 
Line 38: (givens) and numerous state changes (thens) usually imply a much larger effort 
Line 39: than tests with small setups and few state changes. 
Line 40: Breaking Down Stories 
Line 41: You may need to break down a story into smaller stories for the purposes of 
Line 42: ﬁtting stories into iterations. Mike Cohn [Cohn01] offers some ways to break 
Line 43: down a story. For example, you can start with a basic user interface and then 
Line 44: add more bells and whistles, such as images. You can implement something 
Line 45: manually, such as calling users about overdue rentals, and later automate it with 
Line 46: robot calling. You can do something simple, such as a single check-out per CD, 
Line 47: and then have a story for checking out multiple CDs at once. 
Line 48: In addition, you can use acceptance tests as a breakdown mechanism. The 
Line 49: test for each scenario of a use case can become a separate story. A complex busi-
Line 50: ness rule can become a separate story. The test for a complicated business rule 
Line 51: calculation may be expressed in a table with lots of rows. You can break the 
Line 52: calculation into separate stories by assigning a set of rows to each story. 
Line 53: With the address example in Chapter 17, “Decouple with Interfaces,” the 
Line 54: tests themselves suggest a way to break down the story. The tests for a U.S. 
Line 55: address are separate from the tests for a Canadian address. Therefore, U.S. 
Line 56: address veriﬁcation can be a different story than Canadian address veriﬁcation. 
Line 57: Developer Stories 
Line 58: Another reason for breaking down a story is so that multiple teams can help 
Line 59: implement it. Chapter 16, “Developer Acceptance Tests,” showed how Debbie 
Line 60: made up acceptance tests for user interface components and functional modules 
Line 61: that are to be created by other developers. If a story has to be broken down, 
Line 62: you should create acceptance tests for each of the substories. The acceptance 
Line 63: tests help decouple the stories by clarifying the responsibilities of each of the 
Line 64: stories. They provide doneness criteria for each story. It is far more effective for 
Line 65: distributed teams to work on decoupled stories than to work on tasks for the 
Line 66: same story [Eckstein01]. 
Line 67: 
Line 68: --- 페이지 224 ---
Line 69: Tests as a Bug Report 
Line 70: 201
Line 71: Tests as a Bug Report 
Line 72:  
Line 73: For nontrivial bugs, you can write a test as documentation of the bug. The 
Line 74: deﬁnition of a nontrivial bug is something more than a misspelled word, a bad 
Line 75: color, or an unaligned dialog box. For each bug, the discoverer should create 
Line 76: an acceptance test that shows that the desired behavior has not been achieved. 
Line 77: With the bug, the acceptance test fails. When it passes, the bug has been ﬁxed. 1
Line 78: For example, suppose that you were coding the discount example in Chapter
Line 79: 4, “An Introductory Acceptance Test,” and you did not have an acceptance test. 
Line 80: If a bug was reported for a Good customer, you would create an acceptance test. 
Line 81: To ensure that the bug ﬁx does not affect other behavior, include related test 
Line 82: cases that are currently passing. For example, here are tests around other values 
Line 83: for a Good customer. You might also have tests for the Excellent customer as 
Line 84: well, depending on the situation - the cost involved if the bug ﬁx might alter that 
Line 85: Customer Rating as well. 
Line 86: Discount Acceptance Test 
Line 87: Item Total 
Line 88: Customer Rating 
Line 89: Discount Percentage? 
Line 90: $10.00 
Line 91: Good 
Line 92: 0%
Line 93: $10.01 
Line 94: Good 
Line 95: 1%
Line 96: $50.01 
Line 97: Good 
Line 98: 1%
Line 99: Root Cause Analysis 
Line 100: If a bug like the preceding appears, you have an opportunity to do root-cause 
Line 101: analysis.2 What you are looking for is why the bug appeared. Is it something in 
Line 102: the process itself, or was it a random event? Was the case in production not cov-
Line 103: ered by a test case, and if so, why not? Were the data values not expected? For 
Line 104: example, suppose a data value was supposed to be between 1 and 100, but the 
Line 105: value in production was found to be 101. In that case, you create an acceptance 
Line 106: test that demonstrates the correct behavior—limiting the value to 100. Because 
Line 107: an acceptance test represents a requirement, the need for this acceptance test 
Line 108: being created after implementation may represent a missed requirement An ac-
Line 109: ceptance test that has the wrong values is a misinterpreted requirement. 
Line 110:  
Line 111:   1.  In some complex situations, you can write an “unacceptance” test that passes with 
Line 112: the bug. The “unacceptance” test should fail when the bug is ﬁxed. If it does not, the 
Line 113: changes did not totally ﬁx the problem. 
Line 114:   2 . Other resources give detailed explanations of how to do this [Systems01] [Wiki07] 
Line 115: [Wiki09].
Line 116: 
Line 117: --- 페이지 225 ---
Line 118: Chapter 23 Using Tests for Other Things
Line 119: 202
Line 120: The missed or misinterpreted requirement may be traced to a random event, 
Line 121: such as, “We had to get this done in four hours before release.” Alternatively, 
Line 122: it may be traced to a common cause, such as, “The customer never collaborates 
Line 123: with us before we start implementing.” 3
Line 124: If you ﬁnd yourself getting buried in analysis, try something you think might 
Line 125: prevent the problem from reoccurring and see what happens. If it doesn’t work, 
Line 126: try something else. 
Line 127: Production Bugs 
Line 128: One of the most important measures for a team process is the number of bugs 
Line 129: that have escaped to production. You should examine the root cause or causes 
Line 130: of each escaped bug so you can discover how to prevent more of them from 
Line 131: escaping in the future. 
Line 132: Regression Testing 
Line 133: The primary purpose of acceptance tests is to translate the customer require-
Line 134: ments into code. If you have acceptance tests for all requirements, you can use 
Line 135: the set of acceptance tests as a regression test suite. Unless the requirement as-
Line 136: sociated with an acceptance test changes, all acceptance tests should pass. If a 
Line 137: change is made to the implementation to accommodate a new requirement, all 
Line 138: previous acceptance tests should still pass. If previous tests break when a new 
Line 139: requirement is introduced, you may have issues in the design of your code. 
Line 140: If the acceptance tests are automated, run them as often as possible. This 
Line 141: provides immediate feedback that a change in the application has caused some 
Line 142: previously implemented functionality to break. 
Line 143: Summary
Line 144: • You can use acceptance tests as any of the following: 
Line 145: • A rough guide to story completeness 
Line 146: • A rough way to estimate relative story effort 
Line 147: • A way to break up stories 
Line 148:   3.  If the “We had to get this done in four hours before release” occurs more than once, 
Line 149: it is a common cause rather than a random event. 
Line 150: 
Line 151: --- 페이지 226 ---
Line 152: Summary 
Line 153: 203
Line 154: • Distributed teams that break up a story should have acceptance tests for 
Line 155: their part of the story. 
Line 156: • Examine the root cause of why an acceptance test was missed or incorrect. 
Line 157: If possible, change the process to eliminate the cause. 
Line 158: 
Line 159: --- 페이지 227 ---
Line 160: This page intentionally left blank 