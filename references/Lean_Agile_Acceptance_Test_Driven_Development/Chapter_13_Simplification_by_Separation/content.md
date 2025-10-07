Line 1: 
Line 2: --- 페이지 148 ---
Line 3: Chapter 13 
Line 4: Simpliﬁcation by Separation 
Line 5: “Life is like an onion: You peel it off one layer at a time, and sometimes 
Line 6: you weep.”
Line 7: Carl Sandburg 
Line 8: The triad discusses a new story from their sponsor, Sam, to let people reserve 
Line 9: CDs online. The story illustrates how separation of issues allows the creation of 
Line 10: simpler tests. 
Line 11: Complex Business Rules 
Line 12: Cathy starts off, “Sam has an idea for a website. The website connects back to 
Line 13: the charter, because we want to give our customers the ability to reserve a CD. 
Line 14: Sam has come up with two ideas. He wants to allow customers to reserve CDs 
Line 15: on the web, and he wants them to be able to search CDs. We haven’t worked 
Line 16: out the details on the second story. But Sam has already decided on the ﬁrst.” 
Line 17: “He has worked out a pretty elaborate business rule for whether a customer 
Line 18: should be allowed to reserve a CD. He created a table, because he’s been fol-
Line 19: lowing along with our discussions. The table looks like the one that follows.” 
Line 20: Debbie interrupts, “That table looks complicated, but I’ve seen some business 
Line 21: rules that look like it.” 
Line 22: Cathy replies, “I think Sam can be a little complex sometimes. He wants 
Line 23: the decision for allowing someone to reserve to be based on a number of crite-
Line 24: ria. The criteria includes the number of times the customer rented in the past 
Line 25: month and the cumulative number of rentals since becoming a customer and the 
Line 26: number of late returns for the past month and beginning rentals. Sam also has a 
Line 27: few people who are his favorites; he wants them to be allowed to reserve unless 
Line 28: they have a really bad rental history.” 
Line 29: 125
Line 30: 
Line 31: --- 페이지 149 ---
Line 32:  
Line 33: Chapter 13 Simpliﬁcation by Separation
Line 34: 126
Line 35: Allowed to Reserve Business Rule 
Line 36: Monthly Rentals 
Line 37: Cumulative Rentals 
Line 38: Sam’s Favorite
Line 39: Customer
Line 40: Allowed to
Line 41: Reserve?
Line 42: If Rentals Past Month 
Line 43: > 30 and Late Rentals 
Line 44: Past Month <= 1 
Line 45: If Cumulative Rentals > 
Line 46: 100 and Late Cumulative 
Line 47: Rentals <= 2 
Line 48: Does Not
Line 49: Apply
Line 50: Yes
Line 51: Does Not Apply 
Line 52: Does Not Apply 
Line 53: Yes 
Line 54: Yes
Line 55: If Rentals Past Month 
Line 56: > 30 and Late Rentals 
Line 57: Past Month <= 3 
Line 58: If Cumulative Rentals > 
Line 59: 300 and Late Cumulative 
Line 60: Rentals < 10 
Line 61: Unknown
Line 62: Yes
Line 63: If Rentals Past Month 
Line 64: > 20 and Late Rentals 
Line 65: Past Month <= 3 
Line 66: If Cumulative Rentals > 
Line 67: 200 and Late Cumulative 
Line 68: Rentals < 5 
Line 69: No
Line 70: No
Line 71: Does Not Apply 
Line 72: Anything Else 
Line 73: Does Not Apply 
Line 74: No
Line 75: Simplify by Separating 
Line 76: Cathy asks, “So what do we do with this?” 
Line 77: Tom replies, “With all these comparisons and complex conditions, this is a 
Line 78: hard table to understand. We can break it into smaller tables, if Sam lets us or 
Line 79: you let us, in lieu of Sam being here. As David Parnas states [Parnas01], tables 
Line 80: can clarify the requirements. And smaller tables can add more clariﬁcation.” 
Line 81: Cathy responds, “It’s as clear as mud to me. So let’s break it up.” 
Line 82: Tom says, “Let’s start with the Monthly Rentals column. We can separate the 
Line 83: values into separate ﬁelds and put the comparisons in single cells. I like to make 
Line 84: up names for the result of each comparison. My suggestion is to call the results 
Line 85: Monthly Rental Levels, or MRLevels to keep it short. If there were meaning-
Line 86: ful names we could assign to each result, we might name them MRExcellent, 
Line 87: MRGood, and so forth. But in this case, let’s just label them with letters. The 
Line 88: table for Monthly Rental Levels looks like this.” 
Line 89: Monthly Rentals Level Calculation 
Line 90: Rentals in Past Month 
Line 91: Late Rentals in Past Month 
Line 92: Monthly Rental Level 
Line 93: >30 
Line 94: <= 1 
Line 95: MRLevelA
Line 96: >30 
Line 97: <= 3 
Line 98: MRLevelB
Line 99: >20 
Line 100: <= 3 
Line 101: MRLevelC
Line 102: Cathy says, “I know we’ll need some tests for these Monthly Rental Levels.” 
Line 103: The triad works together and creates the following. 
Line 104: 
Line 105: --- 페이지 150 ---
Line 106: Complex Business Rules 
Line 107: 127
Line 108: Monthly Rental Level Tests 
Line 109: Rentals in Past Month 
Line 110: Late Rentals in Past Month 
Line 111: Monthly Rental Level 
Line 112: 30 
Line 113: 1 
Line 114: MRLevelA
Line 115: 30 
Line 116: 2 
Line 117: MRLevelB
Line 118: 31 
Line 119: 1 
Line 120: MRLevelA
Line 121: 31 
Line 122: 2 
Line 123: MRLevelB
Line 124: 31 
Line 125: 3 
Line 126: MRLevelB
Line 127: 32 
Line 128: 4 
Line 129: ??
Line 130: 20 
Line 131: 3 
Line 132: ??
Line 133: 21 
Line 134: 3 
Line 135: MRLevelC
Line 136: Cathy says, “I’m not sure what the results should be for those two rows with 
Line 137: the ??.” 
Line 138: Tom replies, “By breaking the original table into smaller tables, we can see 
Line 139: whether we have left out anything. Creating some tests for just the Monthly 
Line 140: Rental rule shows that some possibilities have not been covered. Perhaps these 
Line 141: possibilities may never occur during production. But at least we’ve identiﬁed 
Line 142: them and Debbie can be sure to make allowance for them in the implementa-
Line 143: tion. She could at least record that they occurred, put up a dialog box, or do 
Line 144: whatever is appropriate.” 
Line 145: Debbie interjects, “It seems like there should be a MRLevelD as the default 
Line 146: level if none of the conditions are met. That would make it easier to keep track 
Line 147: of those possibilities when they occur.” 
Line 148: Tom resumes, “We can do the same thing for the Cumulative Rentals. To 
Line 149: save time, here’s a quick outline.” 1
Line 150: Cumulative Rentals Level Rule 
Line 151: Condition 
Line 152: Level
Line 153: If Cumulative Rentals > 100 and Late Cumulative Rentals <= 2 
Line 154: CRLevelA
Line 155: If Cumulative Rentals > 300 and Late Cumulative Rentals < 10 
Line 156: CRLevelB
Line 157: If Cumulative Rentals > 200 and Late Cumulative Rentals < 5 
Line 158: CRLevelC
Line 159: Anything Else 
Line 160: CRLevelD
Line 161: 1. Creating the tests for the Cumulative Rentals Level is left as an exercise for the reader. 
Line 162: 
Line 163: --- 페이지 151 ---
Line 164:  
Line 165: Chapter 13 Simpliﬁcation by Separation
Line 166: 128
Line 167: The Simpliﬁed Rule 
Line 168: Tom continues, “With these individual tables taking care of the details for 
Line 169: Monthly Rentals and Cumulative Rentals, our revised table now looks like this.” 
Line 170: Allowed To Reserve Business Rule (Revised) 
Line 171: Monthly Rentals Level 
Line 172: Cumulative Rentals 
Line 173: Level
Line 174: Sam’s Favorite 
Line 175: Customer
Line 176: Allowed to 
Line 177: Reserve?
Line 178: MRLevelA 
Line 179: CRLevelA 
Line 180: Does Not Apply 
Line 181: Yes
Line 182: Does Not Apply 
Line 183: Does Not Apply 
Line 184: Yes 
Line 185: Yes
Line 186: MRLevelB 
Line 187: CRLevelB 
Line 188: Unknown 
Line 189: Yes
Line 190: MRLevelC 
Line 191: CRLevelC 
Line 192: No 
Line 193: No
Line 194: Does Not Apply 
Line 195: CRLevelD 
Line 196: Does Not Apply 
Line 197: No
Line 198: Cathy asks, “Have we covered all the cases? It seems like there are some miss-
Line 199: ing ones.” 
Line 200: Tom replies, “You’re right. It’s clearer now what all the cases are. There 
Line 201: are several combinations of MRLevels, CRLevels, and Sam’s Favorite Customer 
Line 202: that do not appear in the table. Here are a few.” 
Line 203: Allowed to Reserve Business Rule—Missing Cases 
Line 204: Monthly Rentals Level 
Line 205: Cumulative
Line 206: Rentals Level 
Line 207: Sam’s Favorite 
Line 208: Customer
Line 209: Allowed to 
Line 210: Reserve?
Line 211: MRLevelA 
Line 212: CRLevelB 
Line 213: No 
Line 214: No??
Line 215: MRLevelA 
Line 216: CRLevelB 
Line 217: Unknown 
Line 218: No?
Line 219: “We need to ask Sam whether the answer is yes or no in these cases. He could 
Line 220: simply say that the answer is no in all other cases. That would make Debbie’s 
Line 221: life easier, as well as mine. In any event, you and he need to approve these new 
Line 222: tables as being the way to represent the business rule. As you can see, separating 
Line 223: rentals into separate tables decreases the amount of information that needs to be 
Line 224: absorbed for each table and makes the tests cleaner.” 
Line 225: Rental History 
Line 226: To allow reservations based on Sam’s business rule, the system needs to keep 
Line 227: track of the rentals for each customer. The system could keep separate informa-
Line 228: tion on each rental. At this point, Cathy does not need the history. All she needs 
Line 229: is a count of rentals for the month and the total number of rentals. So for each 
Line 230: customer, there might be the following.” 
Line 231: 
Line 232: --- 페이지 152 ---
Line 233: Rental History 
Line 234: 129
Line 235: When Tom tests the overall system including the user interface, he’ll look up 
Line 236: both 007 and 86 and see whether the reservation is allowed. 2 There also should 
Line 237: be a test ensuring that the system calculates rental history correctly, such as this. 
Line 238: Reservation Allowed Based on Rental History 
Line 239: Given this rental history: 
Line 240: Customer Data 
Line 241: Customer
Line 242: ID
Line 243: Name
Line 244: Rentals
Line 245: in Past 
Line 246: Month
Line 247: Late
Line 248: Rentals in 
Line 249: Past Month 
Line 250: Cumulative
Line 251: Rentals
Line 252: Late
Line 253: Cumulative
Line 254: Rentals
Line 255: Sam’s
Line 256: Favorite
Line 257: 007 
Line 258: James 
Line 259: 100 
Line 260: 3 
Line 261: 300 
Line 262: 30 
Line 263: Yes
Line 264: 86 
Line 265: Maxwell 
Line 266: 200 
Line 267: 1 
Line 268: 400 
Line 269: 30 
Line 270: No
Line 271: Determine if a reservation is allowed. 
Line 272: Reservation Allowed 
Line 273: Customer ID 
Line 274: Allowed?
Line 275: 007 
Line 276: Yes
Line 277: 86 
Line 278: No
Line 279:   2. If there was already a system in production with real data, Tom might try to ﬁnd two 
Line 280: customers: one who is allowed to reserve according to the rule, and one who is not. 
Line 281: This could expose any data-dependent issues. 
Line 282: Compute Rental Counts 
Line 283: Given this rental history: 
Line 284: Rental History Data 
Line 285: Customer ID = 86 
Line 286: CD ID 
Line 287: Rental Due 
Line 288: Rental Returned 
Line 289: CD3 
Line 290: 1/21/2011 
Line 291: 1/21/2011
Line 292: CD5 
Line 293: 1/23/2011 
Line 294: 1/23/2011
Line 295: CD7 
Line 296: 1/23/2011 
Line 297: 1/24/2011
Line 298: CD2 
Line 299: 2/11/2011 
Line 300: 2/12/2011
Line 301: CD4 
Line 302: 2/13/2011 
Line 303: 2/13/2011
Line 304: CD6 
Line 305: 2/13/2011 
Line 306: 2/14/2011
Line 307: CD7 
Line 308: 2/14/2011 
Line 309: 2/14/2011
Line 310: 
Line 311: --- 페이지 153 ---
Line 312:  
Line 313: Chapter 13 Simpliﬁcation by Separation
Line 314: 130
Line 315: The test does not imply whether a rental history is kept. If it is, the history 
Line 316: could be used for other features that are scheduled to be developed soon. All 
Line 317: that is needed now is to change the numbers whenever a check-in occurs. When 
Line 318: the check-in happens, the number of rentals is incremented by one. If the rental 
Line 319: is late, the number of late rentals is incremented by one. Once a month, the sys-
Line 320: tem clears out the rental count for the past month. 3
Line 321: It might be easier to keep a history. The check-in process would add the data 
Line 322: for a rental to the history. The Rental Summary calculation would ﬁnd all the 
Line 323: rentals for a customer and calculate the counts. In either case, the test is inde-
Line 324: pendent of the way the calculation is performed. 
Line 325: Summary
Line 326: • Simplify business rules by separating them in component parts. 
Line 327: • Create tests for the component parts. 
Line 328: • Use the simpler components to determine missing logic. 
Line 329: And a day in the next month: 
Line 330: Test
Line 331: Date
Line 332: Date
Line 333: 3/1/2011
Line 334: The monthly and cumulative rental counts should be as follows. 
Line 335: Rental Summary 
Line 336: Customer
Line 337: ID
Line 338: Name
Line 339: Rentals
Line 340: in Past 
Line 341: Month?
Line 342: Late
Line 343: Rentals in
Line 344: Past Month? 
Line 345: Cumulative
Line 346: Rentals?
Line 347: Late
Line 348: Cumulative
Line 349: Rentals?
Line 350: 86 
Line 351: Maxwell 
Line 352: 4 
Line 353: 2 
Line 354: 7 
Line 355: 3
Line 356:   3. Alternatively, the system could increment the Late Rentals count when a CD was not 
Line 357: returned by the Rental Due date. This would be a time-base event, as described in 
Line 358: Chapter 15, “Events, Responses, and States.” 