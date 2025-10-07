Line 1: 
Line 2: --- 페이지 80 ---
Line 3: Chapter 7 
Line 4: Collaborating on Scenarios 
Line 5: “What we’ve got here is a failure to communicate.”
Line 6: Captain, Road Prison 36, Cool Hand Luke
Line 7: Debbie explains to Cathy how to create scenarios with use cases (see Figure 7.1).
Line 8: The triad constructs a use case for the user story about checking out a CD. Issues 
Line 9: in collaboration are discussed. 
Line 10: Charter 
Line 11: Scenario 
Line 12: Test
Line 13: Story
Line 14: Feature
Line 15: Focus
Line 16: Figure 7.1 Scenarios
Line 17: Use Cases from User Stories 
Line 18: Debbie explains to Cathy one way to discover the details of a user story. “We 
Line 19: use a common technique called a use case. 1 The use case describes a sequence 
Line 20: of actions and reactions between the user and the software. There are several 
Line 21: 57
Line 22: 1. Another way is to use Event/Response, as shown in  Chapter 15, “Events, Responses, 
Line 23: and States.” 
Line 24: 
Line 25: --- 페이지 81 ---
Line 26: Chapter 7 Collaborating on Scenarios
Line 27: 58
Line 28: formal templates for a use case, but Tom and I prefer a lightweight one. It’s 
Line 29: adapted from Alistair Coburn’s book on use cases [Cockburn02]. Because the 
Line 30: ﬁrst story we’re working on is Check Out CD, we’ll create a use case for it. We 
Line 31: do not create use cases for other stories until we need them. Otherwise, we could 
Line 32: get stuck in what is called analysis paralysis.”
Line 33: Check Out CD 
Line 34: As the clerk, I want to check out a CD for a customer so that I can keep 
Line 35: track of who has rented it. 
Line 36: Debbie continues, “Often the use case is part of a workﬂow that either 
Line 37: involves other use cases or actions that occur outside of the software system. 
Line 38: Let’s track the steps that occur when one of your customers rents a CD with 
Line 39: the manual process. Cathy, can you describe the current ﬂow for checking out 
Line 40: a CD?” 
Line 41: “Sure,” Cathy replies. She writes the steps on a whiteboard. After a few addi-
Line 42: tions and corrections, the steps look like this: 
Line 43: The customer selects a CD from the cases on the shelves. (The case just has 
Line 44: the cover page). 
Line 45: The customer brings the CD case to the clerk. 
Line 46: The clerk gets the actual CD in another case from a shelf behind the 
Line 47: counter.
Line 48: The customer presents his driver’s license. 
Line 49: The clerk pulls out the rental card from the CD case. 
Line 50: The clerk writes down the customer’s name and the current date on the 
Line 51: rental card. 
Line 52: The customer signs the rental card. 
Line 53: The clerk ﬁles the rental card in a box on the counter and stores the CD 
Line 54: case with the cover page on a back shelf. 
Line 55: Debbie starts, “The software system will not replace all these steps. A big-
Line 56: ger system, like those red DVD rental kiosks, might, but not the system we’re 
Line 57: replacing. So we only need to concentrate on the steps involved with recording 
Line 58: the rental itself. Based on your current workﬂow, what do you want the soft-
Line 59: ware to do?” 
Line 60: 
Line 61: --- 페이지 82 ---
Line 62: Use Cases from User Stories 
Line 63: 59
Line 64: Cathy replies, “It seems like these are the steps:” 
Line 65: The clerk enters the customer identiﬁcation and CD identiﬁer into the 
Line 66: system.
Line 67: The system records the information. 
Line 68: System prints a form that the customer signs 
Line 69: Simple Use Case 
Line 70: Debbie says, “These steps form the main course or the main scenario of a use 
Line 71: case. Some people call this the happy path because it assumes that nothing goes 
Line 72: wrong. The template for a simple use case looks like this:” 
Line 73: Simple Use Case Template 
Line 74: Name—Identiﬁer to easily reference it by 
Line 75: Description—Brief note 
Line 76: Actor—Who initiates the use case 
Line 77: Pre-conditions—What must be true before the use case is initiated 
Line 78: Post-conditions—What is true if the use case successfully executes 
Line 79: Main course—Steps that show the sequence of interactions 
Line 80: “The actor almost always plays the role of the user in the user story. The 
Line 81: name of the use case can be the name of the user story. The brief description 
Line 82: can be the same as the description on the user story. The pre-conditions describe 
Line 83: the required state of the system prior to starting the main course. The post-
Line 84: conditions are how the state of the system has changed. They describe the results 
Line 85: to check to ensure that the implementation successfully performed the use case. 
Line 86: The pre-conditions represent the setup required to obtain those results. So, based 
Line 87: on the story and the steps, the basic use case looks like this:” 
Line 88: 
Line 89: --- 페이지 83 ---
Line 90: Chapter 7 Collaborating on Scenarios
Line 91: 60
Line 92: Exceptions and Alternatives 
Line 93: Debbie states, “Now that we’ve identiﬁed the main course, we can add addi-
Line 94: tional information to the use case. During the use case, conditions can occur that 
Line 95: do not allow it to reach its post-conditions. We call these conditions exceptions.
Line 96: Exceptions can happen in almost any use case. For example, you could have a 
Line 97: power failure or the computer could crash.” 
Line 98: “We could deal with those sorts of exceptions with an overall response 
Line 99: scheme, such as ﬁlling out the rental contract manually. Speciﬁc exceptions can 
Line 100: occur during the main course. For example, it’s possible that the customer iden-
Line 101: tiﬁcation is not recognized when the clerk enters it. Each exception forms a dif-
Line 102: ferent scenario, which sometimes called an exception scenario. We identify this 
Line 103: exception with an item that is numbered with the step in the main course where 
Line 104: it could occur. We add a letter to denote it as an exception, rather than a main 
Line 105: course step. So this might look like the following:” 
Line 106: Check Out Use Case 
Line 107:  
Line 108: Name—Check out the CD. 
Line 109: Description—Check out a CD for a customer. 
Line 110: Actor—Clerk.
Line 111: Pre-conditions—The customer has an identiﬁcation. The CD has an 
Line 112: identity.
Line 113: Post-conditions—The CD is recorded as rented. The rental contract is 
Line 114: printed.
Line 115: Main Course: 
Line 116: 1. The clerk enters the customer identiﬁcation and CD identiﬁer into 
Line 117: the system. 
Line 118: 2. The system records the information. 
Line 119: 3. The system prints a contract that the customer signs. 
Line 120: Exceptions:
Line 121: 1a. Customer identiﬁcation is not recognized. 
Line 122: 
Line 123: --- 페이지 84 ---
Line 124: Use Cases from User Stories 
Line 125: 61
Line 126: “For many exceptions, the customer needs to determine the response. What 
Line 127: should we have the clerk do?” 
Line 128: Cathy replies, “We could have the clerk enter the customer identiﬁcation 
Line 129: again. It could be that it was entered wrong.” 
Line 130: Debbie continues, “So we make note of that action with the exception. We 
Line 131: put that beneath the exception, like this:” 
Line 132: Exceptions:
Line 133: 1a. Customer identiﬁcation is not recognized. 
Line 134: Repeat step 1. 
Line 135: “But suppose that this step is repeated and the customer identiﬁcation is still 
Line 136: not recognized. It could be that the customer identiﬁcation is not very readable, 
Line 137: or it could be a fake customer identiﬁcation. It’s not up to the developer to 
Line 138: determine how to handle this exception. It’s the business’s responsibility. What 
Line 139: should the system do?” Debbie asked. 
Line 140: Cathy replies, “I suppose the clerk could take down additional information 
Line 141: from the customer and rent the CD anyway. We might lose a CD or two because 
Line 142: of fake IDs, but we would avoid making real customers unhappy. I’ll check with 
Line 143: Sam, but for now, let’s do that.” 
Line 144: Debbie says, “Okay, so let’s call these steps Record Customer ID and Check 
Line 145: Out Manually. You can come up with the exact details later. Because it is a 
Line 146: different exception, we give it a different letter. So the two exceptions that can 
Line 147: occur during step 1 are” 
Line 148: Exceptions:
Line 149: 1a. Customer identiﬁcation is not recognized on ﬁrst try.
Line 150: Repeat step 1. 
Line 151: 1b. Customer identiﬁcation is not recognized on second try. 
Line 152: The clerk performs Record Customer ID and Check Out Manually. 
Line 153: Use case exits. 
Line 154: Debbie asks, “Do you have business rules that apply to the rental process? 
Line 155: Our deﬁnition of a business rule is something that is true, regardless of the 
Line 156: technology.”
Line 157: “We do have one that is hard to enforce, given the way we do things now,” 
Line 158: Cathy replies. “Sam and I agreed that a customer should not be able to rent 
Line 159: more than three CDs at any time. The rule limits our losses in case the customer 
Line 160: skips out on us. It also keeps more CDs in stock for other customers.” 
Line 161: 
Line 162: --- 페이지 85 ---
Line 163: Chapter 7 Collaborating on Scenarios
Line 164: 62
Line 165: Debbie responds, “So you want the check out abandoned in that case. If a 
Line 166: use case is abandoned, the post-conditions are not met. Let’s get that one down. 
Line 167: Later on, you can change your mind, such as increasing the limit for a particu-
Line 168: larly responsible customer. But that would involve a little more coding.” 
Line 169: Exceptions:
Line 170: 1c. The customer violates the CD Rental Limit business rule.
Line 171: The clerk notiﬁes the customer of the violation.
Line 172: The use case is abandoned. 
Line 173: Business Rule: 
Line 174: •  CD Rental Limit 
Line 175: A customer can rent only three CDs at any one time. 
Line 176: “Each of these exceptions will be a scenario for which we create tests. One 
Line 177: other facet of use cases is the alternative, which is another scenario. An alterna-
Line 178: tive is a ﬂow that allows the use case to be successful even if some condition 
Line 179: occurs. For example, the printer might jam when printing the rental contract. In 
Line 180: this case, the clerk could ﬁll out the contract manually, if that’s what you want, 
Line 181: Cathy.”
Line 182: “I guess that’s about the only thing that could be done. I’ll have to make sure 
Line 183: we still have some of the paper contracts left around.” Cathy replied. 
Line 184: Debbie continues, “So we add an alternative to step 3:” 
Line 185: Alternatives
Line 186: 3a. The printer jams. 
Line 187: The clerk ﬁlls out the contract by hand.
Line 188: The use case exits. 
Line 189: “This use case is fairly straightforward. If there were several alternatives, 
Line 190: we’d make up separate use cases to keep each one simple. We know from experi-
Line 191: ence with testing that each alternative requires more tests. If the number of tests 
Line 192: for an alternative seemed large, we deﬁnitely would split up the use case. If it 
Line 193: took me a while to implement an exception or you could use the system without 
Line 194: the exception being handled, we’d make up separate stories for either an indi-
Line 195: vidual or a group of exceptions. Those stories would be related to the one for 
Line 196: the main use case.” 
Line 197: 
Line 198: --- 페이지 86 ---
Line 199: Story Map 
Line 200: 63
Line 201: Acceptance Tests 
Line 202: Debbie continues, “Now that we have the use case for this story, it’s time to 
Line 203: outline the tests to write against it. We need at least one test for the main course, 
Line 204: each exception, and each alternative. Later, we will make up speciﬁc examples 
Line 205: for each of these tests. The use case suggests these tests:” 
Line 206: Rent a CD—This is the main course. 
Line 207: One Bad Customer ID—Enter the customer ID wrong once. 
Line 208: Two Bad Customer IDs—Enter the customer ID wrong twice. 
Line 209: CD Rental Limit—A customer has three CDs and rents another one. 
Line 210: Printer Jam—Simulate a printer jam (maybe out of paper). 
Line 211: “As I mentioned before, the pre-conditions convert to the setup for these 
Line 212: tests, and the post-conditions are the expected results. If there is an exception 
Line 213: and the use case is abandoned, we should see something other than the post-
Line 214: condition, because the use case did not completely execute. Tom will be talking 
Line 215: about the tests more in little bit” [see Chapter 8, “Test Anatomy”]. 
Line 216: “If a business rule such as CD Rental Limit is complicated, you would have 
Line 217: tests that exercise just the business rule. The test scenarios for the use case would 
Line 218: exercise two conditions: when the business rule passes and when it fails. If there 
Line 219: was a particular risky aspect to the business rule, we might create more test cases 
Line 220: for the scenario.” 
Line 221: Documentation
Line 222: “In general, use cases,” Debbie states, “are more than just our joint understand-
Line 223: ing of how things should work. They also document the computer part of the 
Line 224: workﬂow. If you create a user’s manual for the clerks, you could just put the 
Line 225: use case into the manual. Or you could rephrase it so that it reads better for a 
Line 226: non-computer savvy person. Each use case captures all the issues for a particular 
Line 227: operation so it is a document that is worth making correct.” 
Line 228: Story Map 
Line 229: Another way to generate scenarios is with a story map [Patton01] [Hussman01]. 
Line 230: You can use this technique to break down features into stories. Or, in reverse, 
Line 231: the technique can take tasks that people perform and relate them to each other. 
Line 232: 
Line 233: --- 페이지 87 ---
Line 234: Chapter 7 Collaborating on Scenarios
Line 235: 64
Line 236: The tasks can be generated with a brainstorming session on high-level require-
Line 237: ments, as shown in Chapter 5, “The Example Project.” The tasks that are writ-
Line 238: ten on cards are then collaboratively formed into a map. 
Line 239: On the map, the sequence from left to right shows the time relationship 
Line 240: between activities (groups of related tasks). The columns show tasks related 
Line 241: to the activity. Some are essential tasks (such as the happy path in a use case). 
Line 242: Other tasks can be alternatives, exceptions, or details. 
Line 243: The map can display a workﬂow, where each activity is a step in that work-
Line 244: ﬂow, as shown in  Figure 7.2. Underneath each step are the stories associated 
Line 245: with that step. To get through the ﬂow, you need to have an implementation of 
Line 246: at least one story associated with each step. You can place the highest priority 
Line 247: story at the top in each column. When you have a tested implementation for 
Line 248: each of these, you then have an implementation for the entire activity you can 
Line 249: test.
Line 250: Other Stories for One
Line 251: Other Stories for 
Line 252: Another
Line 253: Other Stories for 
Line 254: Still Another
Line 255: Workflow
Line 256: Another Activity
Line 257: One Activity
Line 258: Story for Still Another
Line 259: Still Another Activity
Line 260: Story for One
Line 261: Story for Another
Line 262: Figure 7.2 Story Map Template 
Line 263: The Check Out story, along with the subsequent Check In story, could have 
Line 264: a map, as shown in Figure 7.3.
Line 265: 
Line 266: --- 페이지 88 ---
Line 267: Conceptual Flow 
Line 268: 65
Line 269: Check-Out with 
Line 270: Printer Not Working
Line 271: Check-In CD 
Line 272: Check-Out CD 
Line 273: Check-Out with CD
Line 274: Limit
Line 275: Time
Line 276: Rental Workflow
Line 277: Check-Out CD 
Line 278: Activity
Line 279: Check-In CD 
Line 280: Activity
Line 281: Check-Out with Bad
Line 282: Customer ID
Line 283: Check-In CD That Is
Line 284: Not Checked Out
Line 285: Figure 7.3 Rental Story Map 
Line 286: Conceptual Flow 
Line 287: Cathy, the customer who Tom and Debbie are working with, understands how 
Line 288: the system will work even without seeing a user interface. But if the interface 
Line 289: was unclear, prototype user interfaces and a conceptual ﬂow could be created to 
Line 290: visualize the steps. For example, the conceptual ﬂow for check-out might look 
Line 291: like Figure 7.4.
Line 292: The user interface prototype is a means for understanding the customer’s 
Line 293: requirements. If the customer needs to see the ﬂow in action, demonstrate it 
Line 294: with as few business rules as possible and no database storage. Use test doubles, 
Line 295: as shown in Chapter 11, “System Boundary,” to simulate any required actions 
Line 296: or data. 
Line 297: 
Line 298: --- 페이지 89 ---
Line 299: Chapter 7 Collaborating on Scenarios
Line 300: 66
Line 301: Communication
Line 302: In development, the triad communicates more through face-to-face interactions 
Line 303: than through written documentation. The user stories, use cases, and acceptance 
Line 304: tests are developed interactively. Face-to-face meetings with a whiteboard to 
Line 305: record and display ideas are the most effective form of communication [Cock-
Line 306: burn02]. If the triad members are separate, having a video meeting with a shared 
Line 307: desktop is an alternative. 2 Let’s take a bird’s-eye view of how Tom, Debbie, and 
Line 308: Cathy interact in these face-to-face meetings. 
Line 309: All three perform active listening [Mindtools01]. In active listening, they lis-
Line 310: ten to understand. If they understand, they acknowledge their understanding 
Line 311: with an “I follow you” gesture—a nod or a verbal afﬁrmation. They focus on 
Line 312: what the speaker is saying, not what they are going to say next. If they need 
Line 313: clariﬁcation, they ask for it, such as “Give me an example.” 
Line 314: When recording ideas on the whiteboard, Tom, Debbie, and Cathy practice 
Line 315: what is termed active writing. Recording on a whiteboard instead of on paper 
Line 316: provides instant feedback. When a person is recording ideas, the speaker waits 
Line 317: until each idea is recorded before proceeding to the next. That keeps the pace 
Line 318: reasonable. If an idea is not recorded clearly, the group can immediately sug-
Line 319: gest a correction. Ideas are clariﬁed in person and recorded with a common 
Line 320: understanding.
Line 321: 2. You can use video conferencing sites such as ooVoo.com or Skype.com. 
Line 322: Acknowledged
Line 323: Acknowledged
Line 324: Submitted
Line 325: Invalid
Line 326: ID Dialog
Line 327: Rental
Line 328: Denied
Line 329: Dialog
Line 330: Rental
Line 331: Confirmed
Line 332: Dialog
Line 333: Invalid
Line 334: Customer ID
Line 335: CD Rental
Line 336: Limit
Line 337: Exceeded
Line 338: Check-
Line 339: Out CD
Line 340: Dialog
Line 341: Rental
Line 342: Limit
Line 343: Dialog
Line 344: Figure 7.4 Conceptual Flow 
Line 345: 
Line 346: --- 페이지 90 ---
Line 347: Communication 
Line 348: 67
Line 349: When documenting ideas, the three recognize that each person may have a 
Line 350: preferred way of receiving information. Some like textual descriptions in either 
Line 351: prose format or outline form. Others would rather view diagrams and charts 
Line 352: than text. If necessary, information is recorded in both formats so that both 
Line 353: preferences can be honored. 
Line 354: When Tom, Debbie, and Cathy are brainstorming or describing ideas, they 
Line 355: realize that each person can have different responses. Some people get their 
Line 356: energy from verbal discussions with other people (extroverts), whereas others 
Line 357: process their ideas internally (introverts) [Wiki05]. So the triad has mechanisms 
Line 358: for allowing both to interact. They have times when people think individually 
Line 359: and write down thoughts as well as times when people discuss thoughts as a 
Line 360: group.
Line 361: They understand that some people like to see the big picture without getting 
Line 362: into details (intuition), whereas others want to see the details (sensing). So they 
Line 363: have both brief requirements (such as user stories) and detailed requirements 
Line 364: (such as use cases). They recognize that progress usually can be made without 
Line 365: ﬁrst gathering all the details. But they acknowledge sometimes that work needs 
Line 366: to stop if an important detail is unknown. 
Line 367: They realize that clarity is important, so they develop a common terminology. 
Line 368: The developers and testers accept that the terms and deﬁnitions come from the 
Line 369: business customer. The customer understands that the ambiguous terms they 
Line 370: use may have to be renamed to provide clarity. 
Line 371:  
Line 372: Communication Is More Than Words 
Line 373: Communication, even when you understand it, can be difﬁcult. We each 
Line 374: have our own preconceived notions as to what is clear and what is correct. 
Line 375: I was working with a colleague on developing a PowerPoint presentation 
Line 376: for a conference. We had gone through the slides together and had a good 
Line 377: working understanding of what we were going to present. 
Line 378: A little before the presentation, I got a printed copy of the slides from him. 
Line 379: They were printed four to a page: two rows and two columns. I looked at 
Line 380: the printout and exclaimed that he had rearranged the slides. He looked at 
Line 381: the printout and said that he had not. 
Line 382: Here’s a question for you: If the ﬁrst slide is in the upper-left portion of the 
Line 383: page and the fourth slide is in the bottom-right portion, where should the 
Line 384: second and third slides be located? 
Line 385: 
Line 386: --- 페이지 91 ---
Line 387: Chapter 7 Collaborating on Scenarios
Line 388: 68
Line 389: Summary
Line 390: • A use case describes the scenarios in a user story. 
Line 391: • A use case states the pre-conditions, post-conditions, and main course or 
Line 392: main scenario. 
Line 393: • A use case may have scenarios with exceptions that do not allow it to 
Line 394: successfully complete. 
Line 395: • A use case may have scenarios with alternative ways to achieve the
Line 396: post-condition.
Line 397: • If a use case is large, the exceptions and alternatives may become user 
Line 398: stories.
Line 399: • Use case scenarios suggest acceptance tests. 
Line 400: • Collaboration requires an understanding of the differences in how people 
Line 401: create and process information. 
Line 402: If you said the second should be upper-right and the third should be lower-
Line 403: left, then you would have been as surprised as I was. If you said the reverse, 
Line 404: you would have had no issue with the printout. 
Line 405: Communication is about more than just words. It’s about how you organ-
Line 406: ize those words. 