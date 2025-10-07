Line 1: 
Line 2: --- 페이지 160 ---
Line 3: Chapter 15 
Line 4: Events, Responses, and States 
Line 5: “I just dropped in to see what condition my condition is in.”
Line 6: Mickey Newbury, “Just Dropped In” 
Line 7: This chapter explains the event-response way of capturing requirements and 
Line 8: testing the state transitions caused by events. 
Line 9: Events and an Event Table 
Line 10: The CD rental process is driven mostly by user actions. So employing use cases 
Line 11: was a natural ﬁt for eliciting requirements. There are other ways to discover 
Line 12: requirements. A popular technique is the event table. It deﬁnes events that occur 
Line 13: and determines how the system should respond. An event could be something 
Line 14: that a user initiated or something that a piece of hardware signaled. It could also 
Line 15: be a particular time, such as the ﬁrst of the month, or a time interval, such as 
Line 16: every hour. The response of the system could be a visible output or a change in 
Line 17: the internal state. 
Line 18: The triad brainstorms to come up with events to see if any issues have been 
Line 19: missed. They come up with the following: 
Line 20: Events for CD Rental 
Line 21: Event 
Line 22: Notes
Line 23: Customer rents CD 
Line 24: Human initiated 
Line 25: Customer returns CD 
Line 26: Human initiated 
Line 27: First of the month 
Line 28: Speciﬁc time 
Line 29: Base rental period ends 
Line 30: Period of time 
Line 31: Bank statement arrives 
Line 32: External event 
Line 33: 137
Line 34: continues
Line 35: 
Line 36: --- 페이지 161 ---
Line 37: Chapter 15 Events, Responses, and States
Line 38: 138
Line 39: Events for CD Rental 
Line 40: Event 
Line 41: Notes
Line 42: Customer enters store 
Line 43: Human initiated 
Line 44: Chicken Little announces the sky is falling 
Line 45: External event 
Line 46: Customer reports CD is lost 
Line 47: Human initiated 
Line 48: Inventory Maintainer cannot ﬁnd CD 
Line 49: External event 
Line 50: Counter Clerk drops CD, and it breaks 
Line 51: External event 
Line 52: Counter Clerk sees CD is dirty 
Line 53: External event 
Line 54: The triad now needs to come up with how the system should respond to all 
Line 55: these events. Cathy decides on the business response to events. Other events 
Line 56: may trigger internal actions. After a certain period, the triad winds up with the 
Line 57: following:
Line 58: Events and Responses for CD Rental 
Line 59: Event 
Line 60: Response 
Line 61: Notes
Line 62: Customer rents CD 
Line 63: Record CD as rented 
Line 64: Print rental contract 
Line 65: Human initiated 
Line 66: Customer returns CD 
Line 67: Record CD as returned 
Line 68: Charge for rental 
Line 69: Human initiated 
Line 70: First of the month 
Line 71: Print inventory report 
Line 72: Speciﬁc time 
Line 73: Rental period ends 
Line 74: Notify customer of end of 
Line 75: rental
Line 76: Period of time 
Line 77: Bank statement arrives 
Line 78: Nothing 
Line 79: External event 
Line 80: Customer enters store 
Line 81: Nothing 
Line 82: Human initiated 
Line 83: Chicken Little announces the
Line 84: sky is falling 
Line 85: Nothing 
Line 86: External event 
Line 87: Customer reports CD is lost 
Line 88: Record as lost 
Line 89: Charge for CD 
Line 90: Human initiated 
Line 91: Inventory Maintainer cannot
Line 92: ﬁnd CD 
Line 93: Record as lost 
Line 94: External event 
Line 95: Counter Clerk drops CD, and 
Line 96: it breaks 
Line 97: Record as broken 
Line 98: External event 
Line 99: Counter Clerk sees CD is dirty 
Line 100: Set aside to clean 
Line 101: External event 
Line 102: Anything that does not require a response from the system is out of scope. 
Line 103: For example, the bank statement arriving does not have a response from the sys-
Line 104: tem, although Cathy will have a response. Many of the human-initiated events 
Line 105: , Continued
Line 106: 
Line 107: --- 페이지 162 ---
Line 108: States and State Transitions 
Line 109: 139
Line 110: are turned into use cases. Some of the external events, such as dropping a CD, 
Line 111: are also turned into a simple story. Making up a use case might be overkill, 
Line 112: because there are not many details associated with them. 
Line 113: A test should be created for every one of the events, even the simple ones. The 
Line 114: tests clarify exactly what the system response should be. For example, dropping 
Line 115: a CD might have a test something like this: 
Line 116: Dropping a CD 
Line 117: Given a CD in the inventory: 
Line 118: CD
Line 119: ID 
Line 120: Status 
Line 121: Rented
Line 122: CD5 
Line 123: Okay 
Line 124: No
Line 125: When it is broken by the Counter Clerk or Inventory Maintainer, record 
Line 126: the event: 
Line 127: Record Broken CD 
Line 128: Enter 
Line 129: CD ID 
Line 130: CD5
Line 131: Press 
Line 132: Submit
Line 133: Then the CD status should change: 
Line 134: CD
Line 135: ID 
Line 136: Status 
Line 137: Rented
Line 138: CD5 
Line 139: Broken 
Line 140: No
Line 141: The number of tests might suggest a different approach for the conditions. 
Line 142: For example, all losses could be grouped into a small number of categories, 
Line 143: such as things that are irreversible, such as a broken CD, and things that 
Line 144: are possibly reversible, such as a dirty CD or a missing one. (A missing one 
Line 145: might be found sometime.) 
Line 146: States and State Transitions 
Line 147: Entities such as CDs take on different states or conditions. The CD transitions 
Line 148: from one state to another due to an event, such as the ones shown in the event-
Line 149: response table. Documenting the states and the transitions is a collaborative 
Line 150: 
Line 151: --- 페이지 163 ---
Line 152: Chapter 15 Events, Responses, and States
Line 153: 140
Line 154: effort, just as for the event-response table. The outcome of the effort is a list of 
Line 155: the states and a map of the transitions. 
Line 156: Based on the events, more discussion, and some simpliﬁcation, the triad 
Line 157: agrees on the following states: 
Line 158: CD States 
Line 159: State 
Line 160: Meaning
Line 161: Ready to Rent 
Line 162: In inventory, ready for renting 
Line 163: Rented 
Line 164: Customer has it on rental 
Line 165: Irreversible Loss 
Line 166: For example, broken or badly scratched 
Line 167: Reversible Issue 
Line 168: For example, dirty, cracked case 
Line 169: Missing 
Line 170: Not rented, but not found in inventory 
Line 171: Lost 
Line 172: Customer reports CD is lost 
Line 173: The transitions can be documented in two ways. The ﬁrst is a state diagram. 
Line 174: In Figure 15.1, the states are shown in circles, and transitions are shown as lines 
Line 175: with labels. Each state may have associated data. For example, the rented state 
Line 176: can have the date the CD was rented and the customer it was rented to. The 
Line 177: large black circle on the left is called the initial state. It points to which state is 
Line 178: the ﬁrst one. The small black circle on the right is the ﬁnal terminal state. There 
Line 179: are no transitions from the ﬁnal state. 
Line 180: Inventory
Line 181: maintainer
Line 182: cannot find
Line 183: CD.
Line 184: Ready to
Line 185: Rent
Line 186: Irreversible
Line 187: Loss
Line 188: Reversible issue
Line 189: Rented
Line 190: Missing
Line 191: Customer
Line 192: returns CD.
Line 193: Clerk sees
Line 194: CD is dirty.
Line 195: Lost
Line 196: Customer
Line 197: rents CD.
Line 198: Customer
Line 199: reports CD
Line 200: is lost.
Line 201: Clerk drops
Line 202: CD and it
Line 203: breaks.
Line 204: Figure 15.1 State Diagram 
Line 205: Alternatively, the states and events can be speciﬁed in a table. Initially this 
Line 206: may display the same information as parts of the event/response table, such as 
Line 207: these:
Line 208: 
Line 209: --- 페이지 164 ---
Line 210: States and State Transitions 
Line 211: 141
Line 212: CD States and Events 
Line 213: States/Events
Line 214: Customer
Line 215: Rents
Line 216: CD
Line 217: Customer
Line 218: Returns
Line 219: CD
Line 220: Inventory
Line 221: Maintainer
Line 222: Cannot
Line 223: Find CD
Line 224: Counter
Line 225: Clerk
Line 226: Drops
Line 227: CD, and It 
Line 228: Breaks
Line 229: Customer
Line 230: Reports
Line 231: CD Is 
Line 232: Lost
Line 233: Counter
Line 234: Clerk Sees
Line 235: CD Is 
Line 236: Dirty
Line 237: Ready to Rent 
Line 238: Rented 
Line 239: Missing 
Line 240: Irrevers-
Line 241: ible Loss 
Line 242: Reversible
Line 243: Issue
Line 244: Rented 
Line 245: Ready to 
Line 246: Rent
Line 247: Lost
Line 248: Irreversible Loss
Line 249: Reversible Issue
Line 250: Missing
Line 251: Lost
Line 252: The state diagram does not show an event that causes an Irreversible Loss 
Line 253: for the terminal state. No events are shown that cause the CD to transition out 
Line 254: of states such as Missing or Reversible Issue. After some discussion, the triad 
Line 255: comes with these additional events. The entire table is not repeated, because it 
Line 256: would exceed the width of the page. 
Line 257: CD States and Events 
Line 258: States/Events
Line 259: Customer
Line 260: Reports CD
Line 261: Is Found 
Line 262: CD Prepared
Line 263: for Rental 
Line 264: (Cleaned)
Line 265: Monthly
Line 266: Inventory Report 
Line 267: Created
Line 268: CD Is 
Line 269: Found by 
Line 270: Clerk
Line 271: Irreversible Loss
Line 272: Remove CD from 
Line 273: system
Line 274: Terminal
Line 275: Reversible Issue 
Line 276: Ready to Rent 
Line 277: Missing 
Line 278: Ready to 
Line 279: Rent
Line 280: Lost 
Line 281: Rented
Line 282: With the state-event table, blank cells are easily identiﬁed. A blank cell repre-
Line 283: sents that an event should not occur for a particular state or, if it does, it should 
Line 284: not cause the state to change. Examine all blank cells to ensure that all the bases 
Line 285: are covered—that is, all possible state transitions due to events are identiﬁed. A 
Line 286: blank cell can be ﬁlled in once it’s examined with some indicator, such as N/A 
Line 287: for not applicable to show that the state/event combination has been considered 
Line 288: and that the event should cause no response when the CD is in that state. 
Line 289: 
Line 290: --- 페이지 165 ---
Line 291: Chapter 15 Events, Responses, and States
Line 292: 142
Line 293: The primary purpose of the state table is to show transitions. Other responses 
Line 294: and state data such as the date rented can be put into this state table. For exam-
Line 295: ple, the action of Remove CD from System is shown in the state/event combina-
Line 296: tion of Irreversible Loss/Monthly Inventory Report Created. 
Line 297: There should be a test for every state transition. Some of the transitions are 
Line 298: already covered by other tests. The ones for check-out and check-in already 
Line 299: cover the transitions between Ready to Rent and Rented. Other transitions may 
Line 300: show additional user stories that need to be implemented, such as a Prepare CD 
Line 301: for Rental. The tests for these stories would show the transition from Reversible 
Line 302: Issue to Ready to Rent. 
Line 303: Internal State or External Response 
Line 304: Here is another example of event, state, and response. Every external event caus-
Line 305: es a system to produce an externally visible response, change its internal state 
Line 306: (such as persistent data), or both. An internal state change alters an externally 
Line 307: visible response in the future. For example, suppose the system keeps the ad-
Line 308: dresses of customers. The address of a customer can be changed, as shown in 
Line 309: Figure 15.2.
Line 310: Internal
Line 311: Persistence
Line 312: of Address
Line 313: (State)
Line 314: Send Mail
Line 315: Change Address
Line 316: Figure 15.2 Internal State 
Line 317: Event/Response
Line 318: Event 
Line 319: Address changed 
Line 320: Response 
Line 321: Address change conﬁrmation 
Line 322: Internal State Change 
Line 323: Address updated 
Line 324: 
Line 325: --- 페이지 166 ---
Line 326: Internal State or External Response 
Line 327: 143
Line 328: In the future, when the system sends mail, the new address will be used: 
Line 329: Event/Response
Line 330: Event 
Line 331: Send mail 
Line 332: Response 
Line 333: Send to current address of customer 
Line 334: An acceptance test for an internal state change could conﬁrm that the state 
Line 335: has been changed. Or it could be combined with another test that shows the 
Line 336: result of that changed state. So the Change Address—Send Mail test would ﬂow 
Line 337: together.
Line 338: Alternatively, if the address is kept in a repository that is external to the sys-
Line 339: tem (see Figure 15.3), the update is part of the response. 
Line 340: Send Mail
Line 341: Change Address
Line 342: External
Line 343: Repository
Line 344: for Address
Line 345: Output Is
Line 346: Response to
Line 347: Change Address
Line 348: Input for
Line 349: Send Mail
Line 350: Figure 15.3 External State 
Line 351: Event/Response
Line 352: Event 
Line 353: Address changed 
Line 354: Response 
Line 355: Address change conﬁrmation 
Line 356: Output 
Line 357: New address output to external repository 
Line 358: Internal State Change 
Line 359: None
Line 360: In this case, an output is expected. The acceptance test can verify this output 
Line 361: to another system, just as was done with the credit charge in Chapter 11, “Sys-
Line 362: tem Boundary.” In creating a response to an event, a system may use data that 
Line 363: comes from the external world. That data may affect the response. In this case, 
Line 364: the input data in the repository changes the response. For testing, developers 
Line 365: may create a test double to simulate the input data from the external repository. 
Line 366: With the external data, the response to send mail is as follows: 
Line 367: 
Line 368: --- 페이지 167 ---
Line 369: Chapter 15 Events, Responses, and States
Line 370: 144
Line 371: Event/Response
Line 372: Event 
Line 373: Send mail 
Line 374: Response
Line 375: Input address from external repository
Line 376: Send mail to that address 
Line 377: Transient or Persistent States 
Line 378: A state change may be transient or persistent. A transient state change exists 
Line 379: for a short period. For example, an address could be changed just for a single 
Line 380: order or for all the orders made during a web session. A persistent change would 
Line 381: change the address permanently, or at least until it was changed again. 
Line 382: A Zen Question 
Line 383: If the internal state changes, but it never affects anything directly or indirectly 
Line 384: seen in the outside world, is that state change necessary? Does a tree make a 
Line 385: sound when it falls with no one around? 
Line 386: Summary
Line 387: • Event/response tables are a complementary way of eliciting requirements. 
Line 388: • Every event/response combination should be covered by an acceptance 
Line 389: test.
Line 390: • A state table documents the events that cause the state of an entity to 
Line 391: change.
Line 392: • Every state/event combination should be covered by an acceptance test. 
Line 393: • State tables and event/response tables may show the same information, but 
Line 394: they are organized with a different emphasis. 