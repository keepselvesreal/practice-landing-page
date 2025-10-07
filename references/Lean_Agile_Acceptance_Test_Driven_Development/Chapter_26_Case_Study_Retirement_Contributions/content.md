Line 1: 
Line 2: --- 페이지 242 ---
Line 3: Chapter 26 
Line 4: Case Study: Retirement 
Line 5: Contributions
Line 6: “First thing that I ask a new client is, ‘Have you been saving up for a rainy 
Line 7: day? Guess what? It’s raining.’”
Line 8: Marty, Primal Fear
Line 9: This case study presents testing a batch process with lots of exceptions and 
Line 10: states.
Line 11: Context
Line 12: You probably have a company retirement account administered by a ﬁnancial 
Line 13: institution that receives money from your company each month and purchases 
Line 14: the mutual funds or other investments that you speciﬁed for your account. The 
Line 15: ﬁnancial institution receives a contribution ﬁle from your company that has a 
Line 16: list of retirement plan participants and the amount that should be added to each 
Line 17: participant’s account. When the institution receives a statement from its bank 
Line 18: that your company has sent a deposit that matches the total in the contribution 
Line 19: ﬁle, it purchases the funds for each participant. 
Line 20: Figure 26.1 presents the overall ﬂow of the process. The matching process 
Line 21: checks the participant identiﬁers in the contribution ﬁle against the correspond-
Line 22: ing retirement plan. If each identiﬁer matches and the bank deposit is correct, 
Line 23: the funding data is produced. 
Line 24: 219
Line 25: 
Line 26: --- 페이지 243 ---
Line 27: Chapter 26 Case Study: Retirement Contributions
Line 28: 220
Line 29: Matching
Line 30: Process
Line 31: Contribution File
Line 32: Funding
Line 33: Bank Deposit 
Line 34: Retirement Plan
Line 35: Figure 26.1 Matching Process 
Line 36: Many retirement administrators have dedicated staffs (such as Customer 
Line 37: Service Representatives) that match each contribution ﬁle with the bank depos-
Line 38: its. When a match is found, the customer service representative initiates the 
Line 39: fund purchases. Several administrators have initiated projects to automatically 
Line 40: perform the matching operation. The business case for these projects is to cut 
Line 41: down on the time spent by the customer service representatives. 
Line 42: Many issues can occur with the matching process. The amount of the deposit 
Line 43: may not exactly match the total in the contribution ﬁle. Or perhaps the deposit 
Line 44: notiﬁcation will not arrive for several days after the contribution ﬁle is received. 
Line 45: Or multiple contribution ﬁles may be matched by a single deposit. Following 
Line 46: are some of the acceptance tests for an application which performs the matching 
Line 47: process.
Line 48: The Main Course Test 
Line 49: The main course test assumes that the deposit amount exactly matches the total 
Line 50: on the amounts in the contribution ﬁle and that all identiﬁers listed in the con-
Line 51: tribution ﬁle correspond to participants in the plan. 
Line 52: Setup
Line 53: Each retirement plan has a set of participants who have decided how to invest 
Line 54: their contributions. Each plan is associated with a bank account from which 
Line 55: transfers are made to pay for purchasing of the funds. 
Line 56: Retirement Plan 
Line 57: Plan ID = XYZ 
Line 58: Name 
Line 59: Participant ID 
Line 60: Fund
Line 61: George 
Line 62: 111111111 
Line 63: Wild Eyed Stocks 
Line 64: Sam 
Line 65: 222222222 
Line 66: Government Bonds 
Line 67: Bill 
Line 68: 333333333 
Line 69: Under the Mattress 
Line 70: 
Line 71: --- 페이지 244 ---
Line 72: The Main Course Test 
Line 73: 221
Line 74: Event
Line 75: The event consists of two parts, which can occur in either order. One is the ar-
Line 76: rival of the contribution ﬁle, and the other is the arrival of the deposit notiﬁca-
Line 77: tion. The Date Time Set makes the example repeatable. 
Line 78: Banking Relationship 
Line 79: Plan ID 
Line 80: Bank Routing Number 
Line 81: Account Number 
Line 82: XYZ 
Line 83: 555555555 
Line 84: 12345678
Line 85: Date Time Set 
Line 86: January 30, 2011 08:18 a.m. 
Line 87: Here is the contribution ﬁle where all participant IDs match those in the 
Line 88: plan.
Line 89: Contribution File 
Line 90: Plan ID = XYZ, File ID = 7777 
Line 91: Participant ID 
Line 92: Amount
Line 93: 111111111 
Line 94: $5,000
Line 95: 222222222 
Line 96: $1,000
Line 97: 333333333 
Line 98: $500
Line 99: Here is the bank deposit whose amount matches the total of the amounts 
Line 100: in the contribution ﬁle. 
Line 101: Bank Deposit 
Line 102: Routing Number 
Line 103: Account Number 
Line 104: Amount 
Line 105: Deposit ID 
Line 106: 555555555 
Line 107: 12345678 
Line 108: $6,500 
Line 109: 8888
Line 110: Expected
Line 111: Because the conditions for matching have been met, the expected output is fund-
Line 112: ing instructions. 
Line 113: 
Line 114: --- 페이지 245 ---
Line 115: Chapter 26 Case Study: Retirement Contributions
Line 116: 222
Line 117: Funding 
Line 118: Plan ID = XYZ, File ID = 9999 
Line 119: Participant ID 
Line 120: Fund 
Line 121: Amount
Line 122: 111111111 
Line 123: Wild Eyed Stocks 
Line 124: $5,000
Line 125: 222222222 
Line 126: Government Bonds 
Line 127: $1,000
Line 128: 333333333 
Line 129: Under the Mattress 
Line 130: $500
Line 131: Matches
Line 132: Deposit ID 
Line 133: Contribution File ID 
Line 134: Funding File ID 
Line 135: Matched on Date Time 
Line 136: 8888 
Line 137: 7777 
Line 138: 9999 
Line 139: January 30, 2011
Line 140: 08:18 a.m. 
Line 141: Implementation Issues 
Line 142: The way the setup works depends on your particular testing environment. The 
Line 143: setup tables, Retirement Plan and Banking Relationship, can either check that 
Line 144: the corresponding entries exist in the appropriate databases or insert them into 
Line 145: the databases if they do not exist. If they do not exist and they cannot be in-
Line 146: serted, the test fails at setup. 
Line 147: The contribution table and the bank deposit table can be converted by the 
Line 148: ﬁxture into data ﬁles that match the format of the data the system receives from 
Line 149: the companies and the bank. The matching program can then process these data 
Line 150: ﬁles as if they were actual ﬁles. 
Line 151: The matching program produces a funding ﬁle that another system proc-
Line 152: esses. This funding ﬁle can be parsed and matched against the expected funding 
Line 153: output.
Line 154: Separation of Concerns 
Line 155: Many other problems can occur during the operation of the system. The re-
Line 156: ceived contribution ﬁle may not be in a readable format. This may occur the 
Line 157: ﬁrst time the ﬁle is received from a company due to setup issues, or it may occur 
Line 158: repeatedly because of ongoing issues at the sending company. The ﬁles may be 
Line 159: in different formats because of each company’s human resource system. Those 
Line 160: problems can be dealt with by using another set of tests that read samples of 
Line 161: actual input ﬁles and check that either the ﬁle can be translated into a common 
Line 162: format or a conversion error must be dealt with manually. 
Line 163: 
Line 164: --- 페이지 246 ---
Line 165: One Exception 
Line 166: 223
Line 167: Business Value Tracking 
Line 168: Manual matching of deposits and contribution ﬁles takes an extensive amount 
Line 169: of time for a customer service representative. In a majority of the instances, the 
Line 170: match could be processed automatically. If the conditions did not hold (exact 
Line 171: match of amounts and all participants already enrolled in the plan), the match-
Line 172: ing process could be performed with the current manual process. So there is high 
Line 173: business value in creating a program that handles the main course as quickly as 
Line 174: possible. The user story that encompasses doing the main course is given a large 
Line 175: business value. 
Line 176: There can be a number of exceptions during the process. The deposit and 
Line 177: contribution total may be off by a small amount (a few cents) or a large amount. 
Line 178: A participant who is not entered as a participant on the plan may be listed in the 
Line 179: contribution ﬁle. In that case, the matching program does not know what fund 
Line 180: should be purchased for that participant. 
Line 181: The exceptions can be dealt with by ranking them by business value. The 
Line 182: value represents some combination of the frequency of the exception and the 
Line 183: cost for a customer service representative to process it. For example, one excep-
Line 184: tion is for a match that is off by a few cents. This event might occur frequently, 
Line 185: but the cost of the time involved to ﬁx it exceeds the beneﬁt. 
Line 186: One Exception 
Line 187:  
Line 188: Each exception should have its own test to show that the exception is handled 
Line 189: properly. The tests might use a common setup. The only difference may be in 
Line 190: the event. 
Line 191: Here is an exception: The deposit is off by one cent. The customer unit decided 
Line 192: that any discrepancy less than a dollar should be handled using the equivalent 
Line 193: of “take a penny, give a penny.” The discrepancies will be kept on some form of 
Line 194: persistent storage, such as a database table or a log ﬁle. At some point, they can 
Line 195: be analyzed to determine if there is a systemic issue such as one company always 
Line 196: being two cents short. For the time being, the total of the discrepancies will be 
Line 197: reportable to the appropriate ﬁnancial ofﬁcer so that the books can be balanced. 
Line 198: Event
Line 199: The setup is as for the main course. The event is different. 
Line 200: 
Line 201: --- 페이지 247 ---
Line 202: Chapter 26 Case Study: Retirement Contributions
Line 203: 224
Line 204: Expected
Line 205: Because the conditions for matching have been met, the expected output is fund-
Line 206: ing instructions. 
Line 207: Date Time Set 
Line 208: January 30, 2011 08:18 a.m. 
Line 209: Contribution File 
Line 210: Plan ID = XYZ, File ID = 7778 
Line 211: Participant ID 
Line 212: Amount
Line 213: 111111111 
Line 214: $5,000
Line 215: 222222222 
Line 216: $1,000
Line 217: 333333333 
Line 218: $500
Line 219: Bank Deposit 
Line 220: Routing Number 
Line 221: Account Number 
Line 222: Amount 
Line 223: Deposit ID 
Line 224: 555555555 
Line 225: 12345678 
Line 226: $6499.99 
Line 227: 8889
Line 228: Funding 
Line 229: Plan ID = XYZ, File ID = 10000 
Line 230: Participant ID 
Line 231: Fund 
Line 232: Amount
Line 233: 111111111 
Line 234: Wild Eyed Stocks 
Line 235: $5,000
Line 236: 222222222 
Line 237: Government Bonds 
Line 238: $1,000
Line 239: 333333333 
Line 240: Under the Mattress 
Line 241: $500
Line 242: Matches
Line 243: Deposit ID 
Line 244: Contribution File ID 
Line 245: Funding File ID 
Line 246: Matched on Date Time 
Line 247: 8889 
Line 248: 7779 
Line 249: 10000 
Line 250: January 30, 2011 
Line 251: 08:18 a.m. 
Line 252: Now the issue is whether to show this as a separate table or as part of the 
Line 253: Matches table. Because the purpose is for balancing nonmatching funding, it is 
Line 254: shown as a separate table. 
Line 255: 
Line 256: --- 페이지 248 ---
Line 257: Another Exception 
Line 258: 225
Line 259: Another Exception 
Line 260: In this exception, a participant ID that is listed in the contribution ﬁle does not 
Line 261: have a corresponding entry in the retirement plan. 
Line 262: Event
Line 263: Once again, you could use a common setup. The difference in the event is that 
Line 264: the contribution ﬁle contains an additional contributor who does not appear in 
Line 265: the funding data. The total matches the deposit. 
Line 266: Discrepancy
Line 267: Deposit ID 
Line 268: Contribution
Line 269: File ID 
Line 270: Matched on Date Time 
Line 271: Discrepancy Amount 
Line 272: 88889 
Line 273: 7779 
Line 274: January 30, 2011
Line 275: 08:18 a.m. 
Line 276: $–.01
Line 277: Date Time Set 
Line 278: January 30, 2011 08:18 a.m. 
Line 279: Contribution File 
Line 280: Plan ID = XYZ, File ID = 7779 
Line 281: Participant ID 
Line 282: Amount
Line 283: 111111111 
Line 284: $5,000
Line 285: 444444444 
Line 286: $100
Line 287: Bank Deposit 
Line 288: Routing Number 
Line 289: Account Number 
Line 290: Amount 
Line 291: Deposit ID 
Line 292: 555555555 
Line 293: 12345678 
Line 294: $5,100 
Line 295: 8892
Line 296: Expected
Line 297: Because the conditions for matching have been met, the expected output is fund-
Line 298: ing instructions. 
Line 299: 
Line 300: --- 페이지 249 ---
Line 301: Chapter 26 Case Study: Retirement Contributions
Line 302: 226
Line 303: The missing participant needs to be reported somehow. A separate table 
Line 304: shows the information that is attributed to the participant. A separate user story 
Line 305: and set of tests will show how to handle this output. 
Line 306: Funding 
Line 307: Plan ID = XYZ, File ID = 10001 
Line 308: Participant ID 
Line 309: Fund 
Line 310: Amount
Line 311: 111111111 
Line 312: Wild Eyed Stocks 
Line 313: $5,000
Line 314: Matches
Line 315: Deposit ID 
Line 316: Contribution File ID 
Line 317: Funding File ID 
Line 318: Matched on Date Time 
Line 319: 8892 
Line 320: 7779 
Line 321: 10001 
Line 322: January 30, 2011
Line 323: 08:18 a.m. 
Line 324: Missing Participant 
Line 325: Plan ID 
Line 326: Participant ID 
Line 327: Matched on Date Time 
Line 328: Participant Amount 
Line 329: XYZ 
Line 330: 444444444 
Line 331: January 30, 2011
Line 332: 08:18 a.m. 
Line 333: $100
Line 334: Two Simultaneous Exceptions 
Line 335: So what if two exceptions occur in the same processing? Should there be a test 
Line 336: for that? Often it is difﬁcult to form an automatic response to the occurrence of 
Line 337: two exceptions for the same transaction, so the transaction is handled manually. 
Line 338: However, it would be useful to know that there are two exceptions so that input 
Line 339: doesn’t have to be manually processed twice—once for each exception. The test 
Line 340: then shows that two exceptions occurred. If the two exceptions are decoupled 
Line 341: (the response to one does not depend on the response to the other), the tests for 
Line 342: the individual exceptions may be sufﬁcient, depending on the risk tolerance of 
Line 343: the project. 
Line 344: Event
Line 345: Once again, the setup matches what it was for the main course. But both a miss-
Line 346: ing participant and a nonmatching deposit are involved. 
Line 347: 
Line 348: --- 페이지 250 ---
Line 349: The Big Picture 
Line 350: 227
Line 351: Expected
Line 352: No funding is produced. The output describes the exceptions that occurred 
Line 353: during the matching process. These exceptions can be tracked to determine 
Line 354: which combinations of multiple exceptions occur frequently. At some point, 
Line 355: the frequent combinations could be handled in code, rather than left for manual 
Line 356: processing.
Line 357: Date Time Set 
Line 358: January 30, 2011 08:18 a.m. 
Line 359: Contribution File 
Line 360: Plan ID = XYZ, File ID = 7780 
Line 361: Participant ID 
Line 362: Amount
Line 363: 111111111 
Line 364: $5,000
Line 365: 444444444 
Line 366: $100
Line 367: Bank Deposit 
Line 368: Routing Number 
Line 369: Account Number 
Line 370: Amount 
Line 371: Deposit ID 
Line 372: 555555555 
Line 373: 12345678 
Line 374: $5,099 
Line 375: 8893
Line 376: Exception
Line 377: Contribution
Line 378: File ID 
Line 379: Deposit ID 
Line 380: Exceptions
Line 381: 7780
Line 382: 8893
Line 383: Deposit_does_not_match_contribution_total
Line 384: Participant_in_contribution_ﬁle_not_in_plan 
Line 385: The Big Picture 
Line 386: These tests have been focused on the context of the system. In the big picture, 
Line 387: not only do you have to create a funding ﬁle, you must actually purchase the 
Line 388: funds and record the transactions in each participant’s account. You need to 
Line 389: develop a larger test for this entire workﬂow. It may not necessarily be run as 
Line 390: an automated test. It may still require some test double. You would not want to 
Line 391: keep purchasing mutual funds and adding them to a participant’s account every 
Line 392: 
Line 393: --- 페이지 251 ---
Line 394: Chapter 26 Case Study: Retirement Contributions
Line 395: 228
Line 396: time you run this large test. So a test double for the actual purchasing interface 
Line 397: is required. 
Line 398: The big picture test may be beyond the developer unit’s scope. Their job is 
Line 399: to ensure that the funding instructions are correct based on the input. But the 
Line 400: project is not complete until the full test is run by the testing unit. 
Line 401: Event Table 
Line 402: The matching process is a batch process. It is not driven by user input, but by 
Line 403: events that occur. Therefore, an event table is appropriate for this case. Here’s 
Line 404: an example of some of these events. 
Line 405: Matching Events 
Line 406: Event 
Line 407: Response 
Line 408: Notes
Line 409: Contribution ﬁle received 
Line 410: Check for matching deposit 
Line 411: If so, perform match 
Line 412: Else store ﬁle 
Line 413: Bank deposit received 
Line 414: Check for matching 
Line 415: contribution ﬁle 
Line 416: If so, perform match 
Line 417: Else store deposit 
Line 418: One week after contribution 
Line 419: ﬁle received 
Line 420: If no bank deposit received, 
Line 421: notify client 
Line 422: One week after bank deposit 
Line 423: received
Line 424: If no contribution ﬁle received, 
Line 425: notify client 
Line 426: One minute prior to market 
Line 427: close
Line 428: Disallow matching until after 
Line 429: market close 
Line 430: Prevents funding 
Line 431: issues
Line 432: State Transition Table 
Line 433: The contribution ﬁle goes through several states that track its progress through 
Line 434: the matching process. These are some of the states that a ﬁle cvan be in. 
Line 435: 
Line 436: --- 페이지 252 ---
Line 437: State Transition Table 
Line 438: 229
Line 439: Contribution File 
Line 440: State 
Line 441: Meaning
Line 442: Received 
Line 443: Contribution ﬁle received 
Line 444: Data Checked 
Line 445: File has been examined for format errors 
Line 446: Awaiting Match 
Line 447: Waiting for bank deposit 
Line 448: Edit Processing 
Line 449: Contribution ﬁle has bad format 
Line 450: External events and internal events cause the state of the contribution ﬁle to 
Line 451: change or some processing to occur. This table describes some of the state tran-
Line 452: sitions for the contribution ﬁle. 
Line 453: Contribution File State/Event Transitions 
Line 454: State 
Line 455: Event 
Line 456: Response 
Line 457: New State 
Line 458: Notes
Line 459: Initial 
Line 460: Received contri-
Line 461: bution ﬁle 
Line 462: Record contri-
Line 463: bution ﬁle 
Line 464: Received
Line 465: Received
Line 466: Perform data 
Line 467: check
Line 468: Data
Line 469: checked
Line 470: Examine ﬁle 
Line 471: for format 
Line 472: errors
Line 473: Data checked 
Line 474: Data check is 
Line 475: bad
Line 476: Edit
Line 477: processing
Line 478: Need to cor-
Line 479: rect errors 
Line 480: Data checked 
Line 481: Data check is 
Line 482: good
Line 483: Awaiting
Line 484: match
Line 485: A test can be associated with each state transition that is not already being 
Line 486: checked by another test. For example, for the ﬁrst transition, you might have 
Line 487: the following. 
Line 488: Transition to State Received 
Line 489: Given a retirement plan: 
Line 490: Retirement Plan 
Line 491: Plan ID = XYZ 
Line 492: Name 
Line 493: Participant ID 
Line 494: Fund
Line 495: George 
Line 496: 111111111 
Line 497: Wild Eyed Stocks 
Line 498: Sam 
Line 499: 222222222 
Line 500: Government Bonds 
Line 501: Bill 
Line 502: 333333333 
Line 503: Under the Mattress 
Line 504: 
Line 505: --- 페이지 253 ---
Line 506: Chapter 26 Case Study: Retirement Contributions
Line 507: 230
Line 508: Summary
Line 509: • Separate concerns to make testing easier. 
Line 510: • Give each exception its own test. 
Line 511: • Test every state transition. 
Line 512: When a contribution ﬁle is received: 
Line 513: Date Time Set 
Line 514: January 30, 2011 08:18 a.m. 
Line 515: Contribution File 
Line 516: Plan ID = XYZ, File ID = 7777 
Line 517: Participant ID 
Line 518: Amount
Line 519: 111111111 
Line 520: $5,000
Line 521: 222222222 
Line 522: $1,000
Line 523: 333333333 
Line 524: $500
Line 525: Then record it as received. 
Line 526: Contribution File States 
Line 527: Plan ID 
Line 528: File ID 
Line 529: Status
Line 530: XYZ 
Line 531: 7777 
Line 532: Received