Line 1: 
Line 2: --- 페이지 200 ---
Line 3: Chapter 20 
Line 4: Business Capabilities, Rules, 
Line 5: and Value 
Line 6: “Price is what you pay. Value is what you get.”
Line 7: Warren Buffett 
Line 8: The triad discusses delivering value to the business in other ways. 
Line 9: Business Capabilities 
Line 10: Cathy would like to provide customers with discounts for repeat business to 
Line 11: keep them loyal to Sam’s store. She’s heard rumors about a competitive CD 
Line 12: rental store that Salvatore Bonpensiero is opening in town the end of the week. 
Line 13: Cathy has a vague idea for new things she can do for her customers, such as giv-
Line 14: ing discounts for renting a lot of CDs. 
Line 15: Debbie notes that the system currently does not keep track of the number of 
Line 16: rentals for each customer. She roughly estimates that it would take at least an 
Line 17: iteration to start keeping track of this information and then applying it to the 
Line 18: invoices that are sent out. 
Line 19: After hearing Debbie’s estimate, Tom asked Cathy if she’d really like it by 
Line 20: the end of the week. Cathy replies with a deﬁnite yes. Debbie then suggests that 
Line 21: Cathy should print up some discount cards, as some other retail stores use. The 
Line 22: counter clerk can mark off the number of rentals on the card. When the card is 
Line 23: ﬁlled in, the customer gets a free rental. 
Line 24: Cathy loves the idea. It could be in place by the afternoon without software 
Line 25: changes. She and Tom start discussing ways to avoid a customer misusing the 
Line 26: system, such as faking the marks. Debbie suggests putting the customer ID on 
Line 27: the card. Cathy can record in a spreadsheet each day the customer IDs of the 
Line 28: discount cards that have been turned in for a free rental. If a customer has used 
Line 29: 177
Line 30: 
Line 31: --- 페이지 201 ---
Line 32: Chapter 20 Business Capabilities, Rules, and Value
Line 33: 178
Line 34: an abnormal number of cards, Cathy can investigate whether an issue needs to 
Line 35: be dealt with. Also, Cathy can get a good idea of how many CDs each customer 
Line 36: rents to see whether it makes business sense to spend the money on automating 
Line 37: the discounts. 
Line 38: Morale of the story: Not all capabilities need to be met by software. The triad 
Line 39: should consider any means that implements the requested capability. 
Line 40: Scenario Handling 
Line 41: Sam is reviewing the demo that Debbie and Tom are presenting. Sam asks a 
Line 42: question, “So what happens if something goes wrong with the hardware? Or we 
Line 43: have a hurricane that knocks out the power. Or...” 
Line 44: Debbie interjects, “Then we go back to a manual system. You won’t have 
Line 45: index cards anymore, but we’ll have blank contracts that Cary can ﬁll out. 
Line 46: He’ll record the CD ID, the customer ID, the date rented, the date due, and the 
Line 47: amount. We’ll keep a printout of all CDs, with their categories, the number of 
Line 48: days in the base rental period, and the amount. We’ll see how long it takes Cary 
Line 49: to ﬁnd information on a CD. If it’s really long, you might have a power outage 
Line 50: special in which all CDs can be rented for the lowest amount and the longest 
Line 51: time.”
Line 52: “When the hardware comes back up, Cary, Mary, or Harry can enter the 
Line 53: information into the system. We’ll create a special screen for input of all 
Line 54: the information, rather than have the system calculate the return date and the 
Line 55: amount. In fact, because of the way we’ve designed the system for testing, we 
Line 56: already have a way to do this in the code. We just have to add a user interface 
Line 57: to the program.” 
Line 58: Morale of the story: Don’t try to deal with every possible scenario in software. 
Line 59: Every Exception Need Not Be Handled 
Line 60: My wife and I travel frequently. When we’re on the road, we like to pick 
Line 61: up a quick breakfast at a fast food place. We’re vegetarians, so that makes 
Line 62: it a little more difﬁcult. Usually we stop at McDonald’s and order Egg 
Line 63: McMufﬁns, hold the meat. That item usually stops the order taker in her 
Line 64: tracks. She looks down at the keyboard and then back up. There’s no key 
Line 65: for Egg McMufﬁn without meat. Many times, the cashier has to call the 
Line 66: manager over to help her. There is a combination of keys that allows her 
Line 67: to enter such a weird order, but sometimes it takes three or four minutes 
Line 68: to enter our food order. 
Line 69: 
Line 70: --- 페이지 202 ---
Line 71: A Different Business Value 
Line 72: 179
Line 73: Business Rules Exposed 
Line 74: A business rule is something that is true regardless of the technology that is 
Line 75: employed. Whether rentals are kept on paper or in the computer, Sam wants to 
Line 76: limit the number of simultaneous rentals by a customer. 
Line 77: Sam has the business rule that a customer cannot rent more than three CDs 
Line 78: at any one time. He created this rule because he had a limited stock of CDs, and 
Line 79: he wanted to ensure there was sufﬁcient choice in CDs for other customers. As 
Line 80: Sam’s inventory grows, the reason for the business rule may change. He may 
Line 81: want to increase the limit so that good customers who rent numerous CDs are 
Line 82: not disappointed. He might add a rule so that a customer is informed that they 
Line 83: had already rented a particular CD. In this case, the business rule could help a 
Line 84: long term customer save money on rentals by avoiding duplicates. 
Line 85: One of the primary purposes of a system is to make transactions comply with 
Line 86: the business rules. Business rules should be exposed so that they are easy to test 
Line 87: and easy to change. 
Line 88: A Different Business Value 
Line 89: The check-out workﬂow was modeled from what Sam had noticed in a regular 
Line 90: video store. The ﬂow looked like this. 
Line 91: One time, we stopped at a Burger King. We ordered two Breakfast 
Line 92: Croissants, hold the meat. The order taker responded almost instantly with 
Line 93: the total. I couldn’t ﬁgure out whether the employee was better trained, 
Line 94: more experienced, or had a better keyboard layout. I looked at the receipt. 
Line 95: It said “2 Breakfast Croissants—Ask Cashier.” In the event of any off-
Line 96: menu requests, the procedure was to ask the order taker for the details. It 
Line 97: sped up taking the order, which was a great beneﬁt to the customer. 
Line 98: Not handling every exception in software not only saved development 
Line 99: time, but increased customer satisfaction. It was a win-win. 
Line 100: P.S. Someone ﬁnally ﬁxed the issue of off-menu requests at McDonald’s. 
Line 101: Ordering goes a lot faster now. 
Line 102: 
Line 103: --- 페이지 203 ---
Line 104: Chapter 20 Business Capabilities, Rules, and Value
Line 105: 180
Line 106:  
Line 107: The triad created a value-stream map from the renter’s point of view. The 
Line 108: renter wants to rent a particular CD, so that is the starting point. The end point 
Line 109: is the renter heading out the door with the CD. The renter wants to get in and 
Line 110: out as quickly as possible. So the triad ﬁgured that instead of the customer walk-
Line 111: ing around looking at CD cases, he could just look on a computer screen and 
Line 112: select the CD. No more looking for the physical case. So the workﬂow would 
Line 113: be as follows: 
Line 114: As-Is Workﬂow 
Line 115: • The customer looks at CD cases that contain the title sheet. 
Line 116: • The customer picks the CD he wants. 
Line 117: • The customer brings the CD to the counter. 
Line 118: • The clerk retrieves the corresponding CD in its case from shelves behind 
Line 119: the counter and puts the title sheet case in its place. 
Line 120: • The clerk returns to the counter with the CD. 
Line 121: • The clerk scans the CD ID and customer ID. 
Line 122: • The contract is printed, and the customer signs it. 
Line 123: • The customer heads out the door with the CD he picked out. 
Line 124: Possible To-Be Workﬂow 
Line 125: • The customer selects the CD on the system. 
Line 126: • The customer enters his customer ID. 
Line 127: • The system notiﬁes the clerk that a CD had been requested by the
Line 128: customer and prints a contract. 
Line 129: • The clerk gets the CD and places it in a check-out box with the contract. 
Line 130: • The customer walks up with his customer card. 
Line 131: • The clerk retrieves the CD and contract and gives it to the customer. 
Line 132: • The customer signs the contract. 
Line 133: • The customer heads out the door with the CD. 
Line 134:  
Line 135: This workﬂow is quicker and faster for both the clerk and the customer. Sam 
Line 136: also ﬁgured he could save a large chunk of store rental by eliminating the display 
Line 137: shelves with all the CDs. The clerks wouldn’t have to replace the CD cases when 
Line 138: the CD was returned. However, customers may prefer to browse titles being dis-
Line 139: played on the shelves to ﬁnd something new. Before implementing the change, 
Line 140: Sam needs to investigate how his customers would react to this change. That’s 
Line 141: 
Line 142: --- 페이지 204 ---
Line 143: Summary 
Line 144: 181
Line 145: in accordance with the principles of the charter (see Chapter 5, “The Example 
Line 146: Project”).
Line 147: By looking at a larger value stream, the triad found a possible win-win situ-
Line 148: ation for everyone. Software teams that consider the larger context may ﬁnd 
Line 149: non-software improvements. 
Line 150: Summary
Line 151:  
Line 152: • Not all capabilities need to be met by software solutions. 
Line 153: • Software does not need to be able to handle every scenario. 
Line 154: • Software teams should examine workﬂows in which their software partici-
Line 155: pates for bigger-picture improvements. 
Line 156: 
Line 157: --- 페이지 205 ---
Line 158: This page intentionally left blank 