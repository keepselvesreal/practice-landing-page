Line 1: 
Line 2: --- 페이지 258 ---
Line 3: Chapter 28 
Line 4: Case Study: A Library Print 
Line 5: Server
Line 6: “There’s no such thing as a free lunch.”
Line 7: Anonymous
Line 8: Here is a library print server system. Libraries use such a system to charge for 
Line 9: printouts of documents. The example shows how acceptance tests can cover a 
Line 10: workﬂow and not just a use case. 
Line 11: The Context 
Line 12: I have consulted for Rob Walsh, the cofounder of EnvisionWare, in exploring a 
Line 13: new object design for the print server system the company provides to libraries. 
Line 14: In my book Prefactoring, I showed the unit test strategy and underlying object 
Line 15: design for the system. 1 I described the work ﬂow with a concentration on how it 
Line 16: was implemented using the internal messaging system. The following workﬂow 
Line 17: concentrates on the acceptance tests. 
Line 18: A library patron, Joe, wants to print a document created on one of the 
Line 19: library’s computers. He submits the document for printing and then goes over 
Line 20: to a release station to print the job. There are two separate use cases that form 
Line 21: the work ﬂow—submitting the document for printing and actually printing the 
Line 22: document—. Internally, the personal computer and the release station commu-
Line 23: nicate with a central server (see Figure 28.1).
Line 24: 235
Line 25:   1.  See Chapter 15 in [Pugh01]. 
Line 26: 
Line 27: --- 페이지 259 ---
Line 28: Chapter 28 Case Study: A Library Print Server
Line 29: 236
Line 30: Library
Line 31: Computer
Line 32: Central
Line 33: Server
Line 34: Print Release
Line 35: Station
Line 36: Printed
Line 37: Documents
Line 38: #1 Prints Document
Line 39:  (File / Print)
Line 40: #2  Requests
Line 41: Printing
Line 42: Print Job
Line 43: Print Job
Line 44: Joe
Line 45: Figure 28.1 Workﬂow 
Line 46: There are a number of tests that ensure the individual steps work. For exam-
Line 47: ple, some tests ensure that the print cost is correctly computed for various users 
Line 48: and different modes of printing—black-and-white and color. Other tests check 
Line 49: that users can deposit money into their prepaid accounts. The following is the 
Line 50: test for the entire workﬂow. 
Line 51: A Workﬂow Test 
Line 52: In this workﬂow, Joe submits two documents for printing and then goes to the 
Line 53: release station. When Joe signs onto the release station, he sees a list of the two 
Line 54: print jobs. Joe selects each one to print. Each job is printed, and Joe’s account is 
Line 55: charged. Here’s the detailed test. 
Line 56: Workﬂow of Printing Two Documents to Print Queue 
Line 57: Given a user with an account on the system: 
Line 58: User
Line 59: Name 
Line 60: Balance 
Line 61: User ID 
Line 62: Joe 
Line 63: $1.00 
Line 64: 123
Line 65: And these print rates: 
Line 66: Print Rates 
Line 67: B&W Per-Page Rate 
Line 68: Color Per-Page Rate 
Line 69: $.03 
Line 70: $.10
Line 71: 
Line 72: --- 페이지 260 ---
Line 73: A Workﬂow Test 
Line 74: 237
Line 75: And two documents to be printed: 
Line 76: Document
Line 77: Name 
Line 78: Number of Pages 
Line 79: Contains
Line 80: Joestuff.doc 
Line 81: 1 
Line 82: The quick brown fox jumped over the 
Line 83: lazy dogs 
Line 84: Document
Line 85: Name 
Line 86: Number of Pages 
Line 87: Contains
Line 88: Morestuff.doc 
Line 89: 7 
Line 90: --Lots of stuff-- 
Line 91: And no print jobs currently on the print queue for that user: 
Line 92: Print Jobs 
Line 93: User ID = 123 
Line 94: User ID 
Line 95: Filename 
Line 96: Print Mode 
Line 97: Job Number
Line 98: And the next job number is set: 
Line 99: Next Job Number 
Line 100: Job Number 
Line 101: 99991
Line 102: When the user requests the ﬁrst document to be printed: 
Line 103: Request Printing 
Line 104: Enter 
Line 105: User ID 
Line 106: 123
Line 107: Enter 
Line 108: Filename 
Line 109: Joestuff.doc
Line 110: Enter 
Line 111: Printing Mode 
Line 112: Black & White 
Line 113: Press 
Line 114: Submit
Line 115: Then the system responds with: 
Line 116: Approve Print Charge 
Line 117: Display 
Line 118: Print Charge 
Line 119: $.03
Line 120: Press 
Line 121: Accept
Line 122: 
Line 123: --- 페이지 261 ---
Line 124: Chapter 28 Case Study: A Library Print Server
Line 125: 238
Line 126: Now two print jobs have been created. The next step in the ﬂow is for Joe to 
Line 127: go over to the release station and request each job to be printed. 
Line 128: If the user accepts, a print job is created. 
Line 129: Print Jobs 
Line 130: User ID 
Line 131: Filename 
Line 132: Print Mode 
Line 133: Job Number 
Line 134: 123 
Line 135: Joestuff.doc 
Line 136: Black & White 
Line 137: 99991
Line 138: When the user requests a second document to be printed: 
Line 139: Request Printing 
Line 140: Enter 
Line 141: User ID 
Line 142: 123
Line 143: Enter 
Line 144: Filename 
Line 145: Morestuff.doc
Line 146: Enter 
Line 147: Print mode 
Line 148: Color
Line 149: Press 
Line 150: Submit
Line 151: Then the system responds with: 
Line 152: Approve Print Charge 
Line 153: Display 
Line 154: Print Charge 
Line 155: $.70
Line 156: Press 
Line 157: Accept
Line 158: If the user accepts, a print job is created. 
Line 159: Print Jobs 
Line 160: User ID 
Line 161: Filename 
Line 162: Print Mode 
Line 163: Job Number 
Line 164: 123 
Line 165: Joestuff.doc 
Line 166: Black & White 
Line 167: 99991
Line 168: 123 
Line 169: Morestuff.doc 
Line 170: Color 
Line 171: 99992
Line 172: Workﬂow for Printing Jobs from Print Queue 
Line 173: Given that print jobs have been created for a user: 
Line 174: Print Jobs 
Line 175: User ID 
Line 176: Filename 
Line 177: Print Mode 
Line 178: Job Number 
Line 179: 123 
Line 180: Joestuff.doc 
Line 181: Black & White 
Line 182: 99991
Line 183: 123 
Line 184: Morestuff.doc 
Line 185: Color 
Line 186: 99992
Line 187: 
Line 188: --- 페이지 262 ---
Line 189: A Workﬂow Test 
Line 190: 239
Line 191: When the user enters his user ID: 
Line 192: User ID Entry 
Line 193: Enter 
Line 194: User ID 
Line 195: 123
Line 196: Press 
Line 197: Submit
Line 198: Then the list of print jobs is displayed. 
Line 199: Print Job List 
Line 200: Filename 
Line 201: Job Number 
Line 202: Joestuff.doc 
Line 203: 99991
Line 204: Morestuff.doc 
Line 205: 99992
Line 206: When the user selects one ﬁle: 
Line 207: Select File to Print 
Line 208: Filename 
Line 209: Joestuff.doc
Line 210: Press 
Line 211: Submit
Line 212: Then it is printed on the appropriate printer. 
Line 213: Printed Output 
Line 214: Selected File = Joestuff.doc 
Line 215: Output?
Line 216: The quick brown fox jumped over the lazy dogs 
Line 217: And the ﬁle is eliminated from the display list and the print queue. 
Line 218: Print Job List 
Line 219: Filename 
Line 220: Job Number 
Line 221: Morestuff.doc 
Line 222: 99992
Line 223: Print Jobs 
Line 224: User ID 
Line 225: Filename 
Line 226: Print Mode 
Line 227: Job Number 
Line 228: 123 
Line 229: Morestuff.doc 
Line 230: Color 
Line 231: 99992
Line 232: 
Line 233: --- 페이지 263 ---
Line 234: Chapter 28 Case Study: A Library Print Server
Line 235: 240
Line 236: And the user’s account is charged the print cost. 
Line 237: User
Line 238: Name 
Line 239: Balance 
Line 240: User ID 
Line 241: Joe 
Line 242: $.97 
Line 243: 123
Line 244: When the user selects another ﬁle: 
Line 245: Select File to Print 
Line 246: Filename 
Line 247: Morestuff.doc
Line 248: Press 
Line 249: Submit
Line 250: Then it is printed. 
Line 251: Print Output 
Line 252: Selected File = Morestuff.doc 
Line 253: Output?
Line 254: --Lots of stuff-- 
Line 255: Then it is eliminated from the display list and the print queue. 
Line 256: Print Job List 
Line 257: Filename 
Line 258: Job Number
Line 259: Print Jobs 
Line 260: User ID = 123 
Line 261: User IDh 
Line 262: Filename 
Line 263: Print Mode 
Line 264: Job Number
Line 265: And the user’s account is charged the print cost. 
Line 266: User
Line 267: Name 
Line 268: Balance 
Line 269: User ID 
Line 270: Joe 
Line 271: $.27 
Line 272: 123
Line 273: 
Line 274: --- 페이지 264 ---
Line 275: Summary 
Line 276: 241
Line 277: Additional tests could show the ﬂow if the user does not have sufﬁcient 
Line 278: money to print a document or the user decides to cancel the printing of a 
Line 279: document.
Line 280: Summary
Line 281: •  A workﬂow test consists of more than one use case. 
Line 282: 
Line 283: --- 페이지 265 ---
Line 284: This page intentionally left blank 