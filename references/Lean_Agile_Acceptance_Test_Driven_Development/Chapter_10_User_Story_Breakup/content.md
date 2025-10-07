Line 1: 
Line 2: --- 페이지 118 ---
Line 3: Chapter 10 
Line 4: User Story Breakup 
Line 5: “Life affords no higher pleasure than that of surmounting difﬁculties, 
Line 6: passing from one step of success to another, forming new wishes and see-
Line 7: ing them gratiﬁed.”
Line 8: Samuel Johnson 
Line 9: The triad meets to discuss another story. Cathy discovers how stories can emerge 
Line 10: from the details. Tom shows some boundary tests. 
Line 11: Acceptance Tests Help Break Up Stories 
Line 12: Cathy begins, “I tried out the Check-Out story on Tom’s computer. Obviously, 
Line 13: you need to add more customers and CDs, but at this point, it looks okay to me. 
Line 14: So what’s next?” 
Line 15: Debbie replies, “I worked with Cary on the user interface screen. Mary and 
Line 16: Larry need to try it to see if it’s usable for them. We could do the Check-In story 
Line 17: next, but it’s along the same lines as Check-Out. To save your time, Tom and I 
Line 18: created some tests, and we’ll review them with you. The Charge Rentals story is 
Line 19: related to Check-In, so let’s do that now. The story is”: 
Line 20: Charge Rentals—As the ﬁnance manager, I want to submit a credit card 
Line 21: charge every time a CD is rented so that the store does not have to handle 
Line 22: cash.
Line 23: Debbie states, “When we initially discussed the story, we thought about 
Line 24: breaking it into two stories with these acceptance criteria.” 
Line 25: 95
Line 26: 
Line 27: --- 페이지 119 ---
Line 28: Chapter 10 User Story Breakup
Line 29: 96
Line 30: 96
Line 31: Acceptance Criteria 
Line 32: Compute Rental Fee 
Line 33: • Check-in the CD. See if the rental charge is correct. See if the credit 
Line 34: charge matches the rental charge. 
Line 35: Submit Charge 
Line 36: • See if a charge is made to the credit card company. Check that the bank 
Line 37: account receives money from the charge. 
Line 38: “I’d keep these as two separate stories, based on the tests. The tests for the 
Line 39: ﬁrst one relate to computing the correct charge. The tests for the second one 
Line 40: revolve around transactions and interfaces with third parties. 
Line 41: Business Rule Tests 
Line 42: Debbie continues, “Cathy, could you explain the details for the computer rental 
Line 43: fee?”
Line 44: Cathy answers, “Sure. Sam and I created three categories of CDs: Regular, 
Line 45: Hot Stuff, and Golden Oldie. We have different rental rates for each category. 
Line 46: They are as follows.” 
Line 47: CD Rental Rates 
Line 48: Regular: $2/2 days plus $1/each extra day 
Line 49: Golden Oldie: $1/3 days plus $.50/each extra day 
Line 50: Hot Stuff: $4/1 day plus $6/each extra day 
Line 51: Debbie requests, “To make it clearer, I’d like to put the values for these rates 
Line 52: in a table.” Cathy replies, “Sounds ﬁne to me.” 
Line 53: Debbie asks, “We need some names for the column headers for those values 
Line 54: like $2 and 2 days. What do you call them?” 
Line 55: Cathy replies, “Sam and I just talk about rates. But I can understand that you 
Line 56: need more clarity. So I’ll call the rates Rental Rate, which is the base rate for 
Line 57: the Rental Period Days, and Extra Day Rate, which is for days over the Rental 
Line 58: Period Days.” 
Line 59: Debbie shows the following. 
Line 60: 
Line 61: --- 페이지 120 ---
Line 62: Business Rule Tests 
Line 63: 97
Line 64: Rental Rates 
Line 65: CD Category 
Line 66: Rental Rate 
Line 67: Rental Period Days 
Line 68: Extra Day Rate 
Line 69: Regular 
Line 70: $2 
Line 71: 2 
Line 72: $1
Line 73: Golden Oldie 
Line 74: $1 
Line 75: 3 
Line 76: $.50
Line 77: Hot Stuff 
Line 78: $4 
Line 79: 1 
Line 80: $6
Line 81: Cathy replies, “This is the way it works now. I know we discussed a late fee 
Line 82: in our original talks. Sam and I agreed we should just make a single charge when 
Line 83: the CD is returned, rather than two separate charges.” 
Line 84: Debbie asks, “Do these rates ever change?” 
Line 85: Cathy answers, “Not too often. But I obviously would like the ability to 
Line 86: change these rates.” 
Line 87: Debbie comments, “Let’s make up another story for that. As you can see, 
Line 88: there are often new stories that emerge when we get to the details. The story 
Line 89: could be this one.” 
Line 90: As the ﬁnance manager, I need to modify the rental rates. 
Line 91: Debbie continues, “We’ll get everything done for this current set of rates. I 
Line 92: have the big-picture idea that the rates will change. When I program this story, 
Line 93: I’ll code it so that the effort to add modiﬁability won’t be a big deal. If it would 
Line 94: take a lot of work to make the code easy to change, I’d code what I needed now 
Line 95: and make the alterations later. When I eventually add modiﬁability, I’ll know 
Line 96: that my alterations did not affect the original story, because there will be all the 
Line 97: acceptance tests we are going to develop around this story.” 
Line 98: Tom says, “So let’s make up some tests.” He writes the following on the 
Line 99: whiteboard.
Line 100: Rental Fees 
Line 101: CD Category 
Line 102: Rental Days 
Line 103: Rental Fee? 
Line 104: Notes
Line 105: Regular 
Line 106: 2 
Line 107: $2
Line 108: Regular 
Line 109: 3 
Line 110: $3 
Line 111: 1 extra day 
Line 112: Hot Stuff 
Line 113: 2 
Line 114: $10 
Line 115: 1 extra day 
Line 116: Cathy replies, “That doesn’t seem like enough. You don’t have an example 
Line 117: for Golden Oldie.” 
Line 118: “We can add one,” Tom responds. “We’re going to have a test for the rate 
Line 119: table you proposed. So we’ll have already made sure that the Rental Period Days 
Line 120: 
Line 121: --- 페이지 121 ---
Line 122: Chapter 10 User Story Breakup
Line 123: 98
Line 124: and so forth are correct for Hot Stuff. The test cases in the table show that we 
Line 125: can compute the Rental Fee correctly for a normal and an extra day rental. If 
Line 126: we had 50 different CD categories, repeating the same calculation for each one 
Line 127: would be redundant. We don’t want to over-test a low-risk situation, such as a 
Line 128: simple calculation. If we had all 50 calculations in this table and you changed 
Line 129: the formula, we’d have to change all 50 results.” 
Line 130: “There could be a reason for adding Golden Oldie. The test case would show 
Line 131: that our calculation worked for cents. So the new row looks like this.” 
Line 132: Rental Fees 
Line 133: CD Category 
Line 134: Rental Days 
Line 135: Rental Fee? 
Line 136: Notes
Line 137: Golden Oldie 
Line 138: 4 
Line 139: $1.50 
Line 140: Shows cents in the rental fee 
Line 141: calculation
Line 142: Tom continues, “If the values for Rental Rates are ﬁxed, we need a test that 
Line 143: checks that the values are correct in the application. In essence, it would make 
Line 144: sure they matched the values in the Rental Fees table. If values are modiﬁable, 
Line 145: we need a test to ensure that when you change a value, the new value is stored 
Line 146: correctly.”
Line 147: “The application can check when you change rates that the new values are in 
Line 148: a reasonable range, such as a Rental Rate greater than $.99 and less than $10. 
Line 149: However, if you entered an incorrect Rental Rate, for example $1 for Hot Stuff 
Line 150: instead of $4, that rate would seem reasonable to the application and it would 
Line 151: be stored. Trying to prevent an input error like that can be difﬁcult and often is 
Line 152: practically impossible.” 
Line 153: “I’d like to ask about some more test cases. I always think about the bound-
Line 154: ary conditions, so let me see if I’ve interpreted your rule correctly.” 
Line 155: Rental Fees 
Line 156: CD Category 
Line 157: Rental Days 
Line 158: Rental Fee? 
Line 159: Notes
Line 160: Regular 
Line 161: 1 
Line 162: $2 
Line 163: Short rental
Line 164: Regular 
Line 165: 100 
Line 166: $100 
Line 167: Long rental
Line 168: Regular 
Line 169: 0 
Line 170: $2 
Line 171: Really short rental
Line 172: “Wow!” exclaims Cathy. “You really do have an active mind. I never even 
Line 173: thought about those last two test cases. That one charging someone $100 for a 
Line 174: rental seems right according to your calculations. But that doesn’t seem right for 
Line 175: the business. I think we need to cap the amount of the Rental Fee to the price of 
Line 176: the CD. It will take a little bit of time for Sam and I to get together to determine 
Line 177: how that should work—whether a rental that goes on for a number of days is 
Line 178: 
Line 179: --- 페이지 122 ---
Line 180: Business Rule Tests 
Line 181: 99
Line 182: automatically terminated and the CD is sold to the customer or whether we give 
Line 183: the renter a call or so forth. I think there may be a couple of new stories:” 
Line 184: As the ﬁnance manager, I want to limit the fee for a rental. 
Line 185: As the inventory maintainer, I want to be able to handle a rental that goes 
Line 186: on for a long time. 
Line 187: Cathy continues, “So what do you mean by that test for 0 Rental Days? We 
Line 188: never rent anything for 0 days. We wouldn’t make any money doing that.” 
Line 189: Tom replies, “It’s unclear to me how you determine rental days. Is it a 24-hour 
Line 190: period? What if someone checks out the CD and then immediately returns it? 
Line 191: How long is that?” 
Line 192: Cathy smiles, “You are really being picky. I guess I need to be more precise 
Line 193: so that you can give me exactly what I want. If a rental is returned by 11:59:59 
Line 194: p.m. on a particular day, we count that as being returned on that day. We charge 
Line 195: the Rental Rate for anything that is returned on or before the Rental Due Date. 
Line 196: So it doesn’t matter if a customer returns it on the same day. It’s still charged 
Line 197: the full Rental Rate.” 
Line 198: Tom answers, “I might make up a table that gives examples of what you just 
Line 199: said. But I can’t see ambiguity, like when I worked on an application for one 
Line 200: place where they were using time periods based on minutes.” 
Line 201: Cathy asks, “How did that create a problem?” 
Line 202: Tom answers, “This was a case of where they needed to calculate days, hours, 
Line 203: and minutes. I came up with the following table.” 
Line 204: Calculate Time Period 
Line 205: Start
Line 206: Date
Line 207: Start
Line 208: Time
Line 209: End
Line 210: Date
Line 211: End
Line 212: Time 
Line 213: Days? 
Line 214: Hours? 
Line 215: Minutes? 
Line 216: Notes
Line 217: 1/21/2008 
Line 218: 12:01 AM 
Line 219: 1/22/2008 2:04 AM 1 
Line 220: 2 
Line 221: 3
Line 222: 2/28/2008 
Line 223: 12:01 AM 
Line 224: 3/1/2008 
Line 225: 3:05 AM 2 
Line 226: 3 
Line 227: 4 
Line 228: Leap
Line 229: year
Line 230: 11/2/2008
Line 231: 1:59 AM 
Line 232: 11/2/2008
Line 233: 1:01 AM 0
Line 234: 0
Line 235: –58
Line 236: Do you 
Line 237: know
Line 238: why?
Line 239: “What’s that last one?” Cathy inquires. “You can’t have an end time that is 
Line 240: before the start time.” 
Line 241: Tom answers, “It’s when daylight savings time ends. There is a small window 
Line 242: between 1 a.m. and 2 a.m. If the start falls within this window and the stop 
Line 243: occurs within one hour of setting the clock back, it’s possible to get negative 
Line 244: 
Line 245: --- 페이지 123 ---
Line 246: Chapter 10 User Story Breakup
Line 247: 100
Line 248: time. Even if you have a start before this window and a stop after this window, 
Line 249: you get one less hour than exists in reality.” 
Line 250: “Okay, so what did you do?” Cathy asks. 
Line 251: Tom responds, “The customer said he didn’t want us to spend the time ﬁgur-
Line 252: ing out how to handle it. The situation would occur so rarely that it’s not worth 
Line 253: trying to solve it. So we just limited the number of minutes not to be less than 
Line 254: zero.”
Line 255: Debbie says, “Testers tend to think of edge conditions, like what Tom 
Line 256: showed. Often, these edge conditions relate to decisions that businesses have to 
Line 257: make. So it makes sense to bring up these conditions as part of a requirements 
Line 258: discussion.”
Line 259: A Story with a Business Rule 
Line 260: Debbie starts off, “Let’s see how the business rule calculations ﬁt into a check-in 
Line 261: scenario. I had a preliminary acceptance test for Check-In. Let’s add the Rental 
Line 262: Fee calculation to it.” 
Line 263: The triad works together to create this test. 
Line 264: Check-In CD 
Line 265: Given that a CD is rented to a customer: 
Line 266: Customer Data 
Line 267: Name 
Line 268: ID
Line 269: James 
Line 270: 007
Line 271: CD Data 
Line 272: ID 
Line 273: Title 
Line 274: Rented
Line 275: CD
Line 276: Category
Line 277: Customer
Line 278: ID 
Line 279: Rental Due 
Line 280: CD3
Line 281: Janet Jackson 
Line 282: Number Ones 
Line 283: Yes
Line 284: Regular
Line 285: 007
Line 286: 1/23/2011
Line 287: When the clerk checks in the CD: 
Line 288: Test Date 
Line 289: Date
Line 290: 1/24/2011
Line 291: 
Line 292: --- 페이지 124 ---
Line 293: Summary 
Line 294: 101
Line 295: Check-in CD 
Line 296: Enter 
Line 297: CD ID 
Line 298: CD3
Line 299: Press 
Line 300: Submit
Line 301: Then the  CD is recorded as not rented, and the correct rental fee is com-
Line 302: puted.
Line 303: CD Data 
Line 304: ID 
Line 305: Title 
Line 306: Rented
Line 307: CD
Line 308: Category
Line 309: Customer
Line 310: ID
Line 311: Rental
Line 312: Due
Line 313: CD3
Line 314: Janet Jackson 
Line 315: Number Ones 
Line 316: No
Line 317: Regular
Line 318: Rental Fee 
Line 319: Customer ID 
Line 320: Name 
Line 321: Title 
Line 322: Returned 
Line 323: Rental Fee? 
Line 324: 007 
Line 325: James 
Line 326: Janet Jackson 
Line 327: Number Ones 
Line 328: 1/24/2011 
Line 329: $3
Line 330: Debbie continues, “We don’t have to run through all the combinations that 
Line 331: we tested in the rental fee computation. One will do. We could do a second one 
Line 332: to ensure that the check-in ﬂow is correctly tied to the rental fee computation 
Line 333: and it wasn’t just luck that we happened to get the right rental free. If Cathy 
Line 334: wanted a different outcome between an on-time check-in and a late check-in, 
Line 335: such as sending an e-mail for every late check-in, we would come up with two 
Line 336: test cases. We should also create test cases for exceptions, such as trying to 
Line 337: check-in a CD that hasn’t been rented or an ID that does not exist in the CD 
Line 338: data. These cases essentially follow the same form as the Check-Out test cases.” 
Line 339: Summary
Line 340: •  Creating acceptance tests can yield additional ideas. 
Line 341: •  Break acceptance tests into ones for business rules and ones for scenarios. 
Line 342: • Business rule tests verify all combinations. 
Line 343: • Scenario tests each instance where a business rule produces a different 
Line 344: outcome.
Line 345: •  Determine the edge cases and how the system should respond. 
Line 346: 
Line 347: --- 페이지 125 ---
Line 348: This page intentionally left blank 