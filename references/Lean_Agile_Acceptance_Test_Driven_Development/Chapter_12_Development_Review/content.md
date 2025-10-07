Line 1: 
Line 2: --- 페이지 138 ---
Line 3: Chapter 12 
Line 4: Development Review 
Line 5: “May you have the hindsight to know where you have been, the foresight 
Line 6: to know where you are going, and the insight to know when you have 
Line 7: gone too far.”
Line 8: Anonymous
Line 9: The triad demonstrates to Sam the current state of the system. Debbie and Tom 
Line 10: recount other stories that have been completed and tests that have been run. 
Line 11: The Rest of the Story 
Line 12: The triad meets with Sam. Cathy begins, “Sam, as sponsor, I’d like to update 
Line 13: you on the current status of the system. I’ve shown you some of the user inter-
Line 14: faces and tests as we’ve gone along. I’ve worked together with Debbie and Tom 
Line 15: on the acceptance tests for Check-Out, Check-In, and Credit-Card Charging. I 
Line 16: reviewed the other stories and acceptance tests they came up with. I’ll let Debbie 
Line 17: tell you more about them.” 
Line 18: Debbie begins, “Because the system deals with customers and CDs, we needed 
Line 19: a way to add, update, and delete customers and CDs. We had to add custom-
Line 20: ers and CDs to test check-in and check-out. But we didn’t go into the stories 
Line 21: themselves.”
Line 22: “Adding, deleting, and updating data is so common that Tom and I know it 
Line 23: needs to be done. We just create stories for those actions and let the customer 
Line 24: schedule them. If the customer has the time, we work through the details with 
Line 25: him. Otherwise, we just review the tests with him.” 
Line 26: “For adding a customer, we checked the business-related decisions with 
Line 27: Cathy. For example, you want to ensure that a customer isn’t accidentally 
Line 28: added twice. So we asked Cathy for a business rule to determine if you have 
Line 29: two customers who are duplicates. She said the rule should look for the same 
Line 30: 115
Line 31: 
Line 32: --- 페이지 139 ---
Line 33: Chapter 12 Development Review
Line 34: 116
Line 35: credit-card number. This duplicate rule is also used when updating a customer.” 
Line 36: “Another action was to a delete a customer. Cathy said not to completely 
Line 37: delete customers, but to deactivate them since they may still have outstanding 
Line 38: rentals. She said she wanted to keep a record of previous customers so it would 
Line 39: be possible to welcome them back or have on ﬁle that you don’t want them 
Line 40: back.1 We asked for similar rules for adding, editing, and deleting CDs.” 
Line 41: The acceptance tests Cathy approved were run through both the middle tier 
Line 42: and the user interface. Talking about the user brings up the usability issues that 
Line 43: Tom will talk about.” 
Line 44: Usability Testing 
Line 45: Tom starts, “Debbie described acceptance tests for functionality. There are also 
Line 46: usability tests; quality attribute tests, such as security and performance; and 
Line 47: exploratory tests [ Chapter 3, “Testing Strategy”].” 
Line 48: “Debbie and I worked with Cary, Harry, and Mary on the usability of the 
Line 49: check-out and check-in screens. Harry is color blind, so he couldn’t distinguish 
Line 50: that messages displayed in red and green had different meanings. So we added 
Line 51: textual indicators to the messages to clarify whether they meant “This is a prob-
Line 52: lem” or “This is okay.” Mary doesn’t want to use her glasses to read the screen, 
Line 53: so we increased the size of the font. These examples represent issues that we 
Line 54: often ﬁnd in usability testing.” 
Line 55: “We talked to a couple of your customers to see if the rental contract was 
Line 56: readable. The wording that your lawyer approved seemed a bit obfuscated.” 
Line 57: Sam interjects, “I think talking about lawyers and obfuscation is redundant.” 
Line 58: Tom replies, “Agreed. And so did the customers. So we worked on a simple 
Line 59: language contract, which is still undergoing review by the lawyer” [ABA01]. 
Line 60: Separating State from Display 
Line 61: Tom continues, “We’ll talk more about the concept of separating display from 
Line 62: state later [ Chapter 14, “Separate View from Model”], but because we’re talk-
Line 63: ing about what the user sees, I think it’s appropriate to introduce the idea now. 
Line 64: A while back [ Chapter 9, “Scenario Tests”], we presented to Cathy the idea 
Line 65: of separating the form of input from the internal logic. For example, whether 
Line 66: the input is from typing, the scan of a barcode, or the reading of an RFID tag, 
Line 67: the middle-tier tests should not be affected. This separation makes for less test 
Line 68: maintenance.”
Line 69:   1. A full deletion of a customer would require that all references to a customer (rent-
Line 70: als, card charge history, and so on) be deleted to maintain what is called referential
Line 71: integrity [IBM01]. 
Line 72: 
Line 73: --- 페이지 140 ---
Line 74: The Rest of the Story 
Line 75: 117
Line 76: “A similar issue applies to separating a state from the way it is displayed. As 
Line 77: you can see for tests for check-out, we listed the error messages as CD_Rental_ 
Line 78: Limit_Exceeded. For example:” 
Line 79: Check-Out CD 
Line 80: Enter 
Line 81: Customer ID 
Line 82: 007
Line 83: Enter 
Line 84: CD ID 
Line 85: CD5
Line 86: Press 
Line 87: Submit
Line 88: Check 
Line 89: Error Message 
Line 90: CD_Rental_Limit_Exceeded
Line 91: Tom resumes, “Debbie coded this test with a reference to an identiﬁer, such 
Line 92: as CD_Rental _Limit_Exceeded. When Cathy decided what should appear on 
Line 93: the screen, we put that into a separate table, as follows.” 
Line 94: Error Message 
Line 95: Identiﬁer 
Line 96: Text
Line 97: CD_Rental_Limit_Exceeded 
Line 98: The customer has exceeded the CD rental limit. 
Line 99: Sam has set the limit at 3. Please gently inform the 
Line 100: customer of the limit. 
Line 101: Tom continues, “These two tables allow for separation of testing. One test 
Line 102: veriﬁes that the system produces the right state. The other test conﬁrms that, 
Line 103: given the state, the output is as is desired. It also allows testing the system even 
Line 104: when the ﬁnal wording has not been approved.” 
Line 105: “Because the contract wording has not yet been agreed upon, the test for the 
Line 106: Rental Contract [ Chapter 8, “Test Anatomy”] just veriﬁes that the data on the 
Line 107: contract is correct. Now we have a separate test for the printed contract:” 
Line 108: Given data for a rental contract: 
Line 109: Rental Contract 
Line 110: Customer ID 
Line 111: Customer Name 
Line 112: CD ID 
Line 113: CD Title 
Line 114: Rental
Line 115: Due
Line 116: 007 
Line 117: James 
Line 118: CD2 
Line 119: Beatles Greatest Hits 
Line 120: 1/23/2011
Line 121: 
Line 122: --- 페이지 141 ---
Line 123: Chapter 12 Development Review
Line 124: 118
Line 125: And this template:
Line 126: Rental Contract Template 
Line 127: The customer named <Customer Name> with the ID <Customer ID>, hereaf-
Line 128: ter referred to as the Renter, ha rented the CD identiﬁed by <CD ID> with the 
Line 129: title “<CD Title>,” hereafter referred to as the Rented CD, from Sam’s Lawn 
Line 130: Mower Repair and CD Rental Store, hereafter referred to as the Rentee. The 
Line 131: Renter promises to return the Rented CD to the Rentee by <Rental due>. If 
Line 132: said Renter exceeds  ... blah...blah...blah. 
Line 133: When the contract is printed, it should appear as this: 
Line 134: Rental Contract Printout 
Line 135: The customer named James with the ID 007, hereafter referred to as the 
Line 136: Renter, has rented the CD identiﬁed by CD2 with the title “Beatle’s Great-
Line 137: est Hits,” hereafter referred to as the Rented CD, from Sam’s Lawn Mower 
Line 138: Repair and CD Rental Store, hereafter referred to as the Rentee. The Renter 
Line 139: promises to return the Rented CD to the Rentee by 1/23/2011. If said Renter 
Line 140: exceeds ... blah...blah...blah. 
Line 141: Debbie injects, “When the lawyer approves the wording, we need to change 
Line 142: this test.” 
Line 143: Quality Attribute Tests 
Line 144: Tom resumes, “I often do extensive performance testing on stories. Just as with 
Line 145: the other acceptance tests, I make up a table for the desired behavior. For exam-
Line 146: ple, if Sam is expecting to have many checkout people other than Cary, Harry, 
Line 147: and Mary on the system simultaneously, I would make up a table such as what 
Line 148: follows. As the stories are developed, they are checked to see if they meet the 
Line 149: performance measures.” 
Line 150: Check-Out Performance 
Line 151: Number of Simultaneous Check-Outs 
Line 152: Response Time Maximum (Seconds) 
Line 153: 1 
Line 154: .1
Line 155: 10 
Line 156: .2
Line 157: 100 
Line 158: .3
Line 159: Tom continues, “Security is an important area for testing. You need to ensure 
Line 160: both physical security of the system and software security. You don’t want a 
Line 161: customer to go behind the counter and check-in a CD that he really isn’t check-
Line 162: ing in. We have name/password security on the screens, but based on usage 
Line 163: 
Line 164: --- 페이지 142 ---
Line 165: The Rest of the Story 
Line 166: 119
Line 167: patterns, you may need to change the means and timing for that veriﬁcation. 
Line 168: You could have a logon at the beginning of the day or before every rental. You 
Line 169: could have software veriﬁcation, or you could have employee cards.” 
Line 170: “Because you are keeping credit-card information, Debbie discovered that 
Line 171: you need to abide by the PCI Data Security Standard. So we’ll need tests to 
Line 172: ensure that each of the requirements in that standard is met” [Security01]. 
Line 173: “Security is such a broad issue that I can’t really get into much more detail 
Line 174: in a limited amount of time. Sufﬁce it to say that I can test a system to see if 
Line 175: there are known security issues, but I can’t test to make sure that it is absolutely 
Line 176: secure. Security is not about letting people do things; it’s about making sure they 
Line 177: can’t do things. It’s easier to test the former than the latter.” 
Line 178: “The entire team can try exploratory testing [ Chapter 3] on the system. Each 
Line 179: member takes on the role of a different persona. Each performs the operations 
Line 180: related to that persona and sees how the system feels. Issues may be discovered 
Line 181: that do not come out in our predetermined tests. Because the system is in a run-
Line 182: nable state and we’ll keep it that way as we add features, exploratory testing can 
Line 183: continue throughout the project.” 
Line 184: Workﬂow Tests 
Line 185: Debbie starts, “Just because we have tests for each story does not mean that the 
Line 186: system is fully tested. We need to have a test for an entire workﬂow. The work-
Line 187: ﬂow can correspond to a story map [see  Chapter 11, “System Boundary”] or a 
Line 188: set of story maps. The workﬂow test veriﬁes that there are no issues between re-
Line 189: lated stories and that the entire ﬂow is usable. Here’s an example of a workﬂow 
Line 190: test (see Figure 12.1). If the workﬂow was really complicated, we might have 
Line 191: multiple workﬂow tests that go along alternative paths.” 
Line 192: Delay some days 
Line 193: Rental
Line 194: Contract
Line 195: Add CD
Line 196: Add Customer
Line 197: Check out CD
Line 198: Check in CD
Line 199: Bank
Line 200: Statement
Line 201: Card Charge
Line 202: Test these
Line 203: against expected
Line 204: outcomes
Line 205: Figure 12.1 Workﬂow Test 
Line 206: 
Line 207: --- 페이지 143 ---
Line 208: Chapter 12 Development Review
Line 209: 120
Line 210: Debbie resumes, “Because this test involves many facets of the check-in proc-
Line 211: ess, it can break for a variety of reasons and may have to be maintained fre-
Line 212: quently. For example, if the wording of the rental contract changed, the rental 
Line 213: rates changed, or other things changed, the test would have to be rewritten or it 
Line 214: would fail. So we only want the essential workﬂow tests.” 
Line 215: Deployment Plans 
Line 216: Sam speaks up, “Cathy has been keeping me in the loop about your discussions. 
Line 217: So let me ask the bottom-line question: How quickly can you get the system into 
Line 218: operation? Other than the stuff you’ve already outlined, what else do you need 
Line 219: to do?” 
Line 220: Debbie replies, “We already have a way to get customers and CDs into the 
Line 221: system. We don’t have all the data. If we had a spreadsheet with all the data, we 
Line 222: could input it into the system.” 
Line 223: Sam states, “I’ll have Cary, Harry, and Mary start inputting all that informa-
Line 224: tion. What else?” 
Line 225: Debbie answers, “You’ll need a transition plan to go from the old system to 
Line 226: the new one. You could start with doing rentals both ways for a little while, or 
Line 227: doing all new rentals in the new system, or doing rentals in the new system for 
Line 228: just a few customers.” 
Line 229: Sam says, “Let’s work on that in a little while. Is that it?” 
Line 230: Debbie replies, “Anything else you can think of, Tom?” Tom responds, “I 
Line 231: think that’s it.” 
Line 232: Sam states, “Then let’s go for it. The sooner this starts to happen, the quicker 
Line 233: we can start renting more CDs with the same number of people and thus make 
Line 234: the money to pay you for all your hard work.” 
Line 235: Cathy injects, “I think it’s time to look back at the objectives. The one we’re 
Line 236: dealing with right now is “Within two months, CD check-outs and returns will 
Line 237: be processed in 50% less time.” From what I’ve seen so far, it looks like that 
Line 238: will be met. The manual system measurement was 1 minute, 40 seconds for a 
Line 239: check-out and 55 seconds for a check-in. The preliminary measurements using 
Line 240: the user interface were 46 seconds and 26 seconds, respectively. But as you say, 
Line 241: the sooner we get it working, the sooner we’ll ﬁnd out.” 
Line 242: From Charter to Deliverable 
Line 243: The triad (Cathy, Debbie, and Tom); Sam the sponsor; and the users Cary, 
Line 244: Harry, and Mary have gone from the initial project charter through the ﬁrst 
Line 245: deliverable. Along the way, acceptance criteria have been created as objectives 
Line 246: 
Line 247: --- 페이지 144 ---
Line 248: Summary 
Line 249: 121
Line 250: in the charter through the high-level features and stories. The criteria have been 
Line 251: expressed as speciﬁc tests. Cathy now understands the importance of helping to 
Line 252: create acceptance tests. Debbie and Tom have learned about the business do-
Line 253: main. The more they comprehend the domain, the more effective the triad will 
Line 254: be in producing quality software. 
Line 255: Summary
Line 256: • It is insufﬁcient to have just acceptance tests that revolve around the func-
Line 257: tionality of a system. 
Line 258: • Acceptance criteria need to be established for usability, security, perform-
Line 259: ance, and other quality attributes. 
Line 260: • Workﬂow tests catch inter-story issues. 
Line 261: • Developing in deployable chunks allows for quicker cost recovery. 
Line 262: 
Line 263: --- 페이지 145 ---
Line 264: This page intentionally left blank 