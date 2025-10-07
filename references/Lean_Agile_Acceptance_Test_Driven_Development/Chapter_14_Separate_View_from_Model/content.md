Line 1: 
Line 2: --- 페이지 154 ---
Line 3: Chapter 14 
Line 4: Separate View from Model 
Line 5: “To each his own. (Suum Cuique)”
Line 6: Cicero
Line 7: Tests can be made more maintainable by separating what appears to the user 
Line 8: from the logic in the underlying business model. 
Line 9: Decouple the User Interface 
Line 10: For the CD Reservation story in the previous chapter, the business rule (the 
Line 11: model) for determining whether a customer is allowed to reserve CDs was docu-
Line 12: mented, and tests were written for it. This reservation tests go to some module 
Line 13: inside the system, as shown in Figure 14.1. The triad did not talk about how the 
Line 14: reservation-allowed condition is displayed (the view), and they did not make up 
Line 15: tests for the user interface. 
Line 16: Reservation
Line 17: Allowed
Line 18: Module
Line 19: Reservation Test
Line 20: User
Line 21: Interface
Line 22: Test
Line 23: Figure 14.1 User Interface and Logic Tests 
Line 24: 131
Line 25: 
Line 26: --- 페이지 155 ---
Line 27: Chapter 14 Separate View from Model
Line 28: 132
Line 29: There are at least three ways that the application could show how a customer 
Line 30: was not allowed to reserve a CD: 
Line 31: • The application could hide the Reserve option. 
Line 32: • It could disable the Reserve option. 
Line 33: • It could have the Reserve option go to a dialog box that informs the cus-
Line 34: tomer that he is not allowed to reserve. 
Line 35: Here are the three ways displayed in tables. 
Line 36: Display for Reservation Allowed 
Line 37: Allowed 
Line 38: Reserve Button Displayed? 
Line 39: Yes 
Line 40: Yes
Line 41: No 
Line 42: No
Line 43: Or
Line 44: Display for Reservation Allowed 
Line 45: Allowed 
Line 46: Reserve Button Enabled? 
Line 47: Yes 
Line 48: Yes
Line 49: No 
Line 50: No
Line 51: Or
Line 52: Display for Reservation Allowed 
Line 53: Allowed 
Line 54: Reserve Button Goes To? 
Line 55: Yes 
Line 56: Make Reservation dialog box 
Line 57: No 
Line 58: Sorry No Reservation dialog box 
Line 59: Each variation can be described with a speciﬁc test, as shown here. 
Line 60: Display for Reserve Allowed or Disallowed 
Line 61: Given that these customers are either allowed or disallowed to reserve: 
Line 62: Reservation Allowed 
Line 63: Customer ID 
Line 64: Allowed 
Line 65: Name
Line 66: 007 
Line 67: Yes 
Line 68: James
Line 69: 86 
Line 70: No 
Line 71: Maxwell
Line 72: 
Line 73: --- 페이지 156 ---
Line 74: Decouple the User Interface 
Line 75: 133
Line 76: Display the Reserve button if the customer is allowed to reserve (see
Line 77: Figure 14.2).
Line 78: Customer
Line 79: Customer
Line 80: Cancel
Line 81: Maxwell
Line 82: Customer
Line 83: Customer
Line 84: Cancel
Line 85: Reserve
Line 86: James
Line 87: Figure 14.2 Reserve Button Displayed or Not Displayed 
Line 88: Or
Line 89: Enable the Reserve button if the customer is allowed to reserve (see
Line 90: Figure 14.3).
Line 91: 
Line 92: --- 페이지 157 ---
Line 93: Chapter 14 Separate View from Model
Line 94: 134
Line 95: Customer
Line 96: Customer
Line 97: Cancel
Line 98: Reserve
Line 99: Maxwell
Line 100: Customer
Line 101: Customer
Line 102: Cancel
Line 103: Reserve
Line 104: James
Line 105: Figure 14.3 Reserve Button Enabled or Disabled 
Line 106: Or
Line 107: Display the Customer Allowed to Reserve option and put up a different dia-
Line 108: log box. If the customer is not allowed to reserve, display a No Reserve 
Line 109: dialog box. If the customer is allowed to reserve, display a Reservation 
Line 110: dialog box (see Figure 14.4).
Line 111: 
Line 112: --- 페이지 158 ---
Line 113: Decouple the User Interface 
Line 114: 135
Line 115: Customer
Line 116: Customer
Line 117: Cancel
Line 118: Reserve
Line 119: Maxwell
Line 120: Customer
Line 121: Sorry, Maxwell, you cannot reserve CDs.
Line 122: OK
Line 123: Customer
Line 124: Customer
Line 125: Cancel
Line 126: Reserve
Line 127: James
Line 128: Customer
Line 129: James, what CD would you like to reserve?
Line 130: CD Title
Line 131: Cancel
Line 132: Reserve
Line 133: Beatles Greatest Hits
Line 134: Figure 14.4 Different Dialog Boxes 
Line 135: 
Line 136: --- 페이지 159 ---
Line 137: Chapter 14 Separate View from Model
Line 138: 136
Line 139: Decoupling Simpliﬁes Testing 
Line 140: When Sam and Cathy change their minds about how the ability to reserve 
Line 141: should be displayed, all Debbie and Tom have to do is change the test to one of 
Line 142: these. These tests do not have to be automatic. Tom can manually run this test. 
Line 143: If there gets to be too many of these manual tests, Tom could use a user inter-
Line 144: face test automation tool. The tool could be used when the application is being 
Line 145: built to automatically verify the user interface, as shown in Chapter 3, “Testing 
Line 146: Strategy.”
Line 147: If the business logic had not been separated from the display logic, the test for 
Line 148: the button Enabled/Disabled option might be as follows. 
Line 149: Show Reserve Button 
Line 150: Monthly Rentals 
Line 151: Cumulative
Line 152: Rentals
Line 153: Sam’s Favorite 
Line 154: Customer
Line 155: Show Allowed 
Line 156: to Reserve? 
Line 157: MRLevelA 
Line 158: CRLevelA 
Line 159: Does Not Apply 
Line 160: Reserve Button 
Line 161: Enabled
Line 162: Does Not Apply 
Line 163: Does Not Apply 
Line 164: Yes 
Line 165: Reserve Button 
Line 166: Enabled
Line 167: MRLevelB 
Line 168: CRLevelB 
Line 169: Unknown 
Line 170: Reserve Button 
Line 171: Enabled
Line 172: MRLevelC 
Line 173: CRLevelC 
Line 174: No 
Line 175: Reserve Button 
Line 176: Enabled
Line 177: Does Not Apply 
Line 178: CRLevelD 
Line 179: Does Not Apply 
Line 180: Reserve Button 
Line 181: Disabled
Line 182: Whenever a change is made in how to display the allowable reservation, this 
Line 183: bigger table has to be changed. Mistakes might be made at some point. This 
Line 184: separation of state from display translates both into easier to test and simpler 
Line 185: code. From a testing standpoint, Tom just has to conﬁrm that the user interface 
Line 186: displays the correct result in two cases—for 007 and 86. With this table, he has 
Line 187: to see that the user interface displays the correct result in ﬁve cases—one for 
Line 188: each row in the table. 
Line 189: Summary
Line 190: •  Decouple the user interface from the business logic (separate view from 
Line 191: model) to simplify testing. 