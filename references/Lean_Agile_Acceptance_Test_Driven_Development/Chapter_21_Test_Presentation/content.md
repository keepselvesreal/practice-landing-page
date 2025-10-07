Line 1: 
Line 2: --- 페이지 206 ---
Line 3: Chapter 21 
Line 4: Test Presentation 
Line 5: “Ring the bells that still can ring
Line 6: Forget your perfect offering.
Line 7: There is a crack in everything,
Line 8: That’s how the light gets in.”
Line 9: Leonard Cohen 
Line 10: There is no perfect way of writing a test or a table. Alternative ways are pre-
Line 11: sented here. 
Line 12: Customer Understood Tables 
Line 13: The key in selecting the form of a table is to pick the one that the customer unit 
Line 14: most easily understands. For example, here is the business rule table for rental 
Line 15: fees.
Line 16: CD Rental Fees 
Line 17: Category
Line 18: Standard
Line 19: Rental Days 
Line 20: Standard
Line 21: Rental Fee 
Line 22: Extra Day
Line 23: Rental Fee 
Line 24: Regular 
Line 25: 2 
Line 26: $2 
Line 27: $1
Line 28: Golden Oldie 
Line 29: 3 
Line 30: $1 
Line 31: $.50
Line 32: Hot Stuff 
Line 33: 1 
Line 34: $4 
Line 35: $2
Line 36: 183
Line 37: 
Line 38: --- 페이지 207 ---
Line 39: Chapter 21 Test Presentation
Line 40: 184
Line 41: There are various ways you can document the tests for this table. You can 
Line 42: have a standard calculation-style table, such as this. 
Line 43: Rental Charges 
Line 44: Category 
Line 45: Days 
Line 46: Cost?
Line 47: Regular 
Line 48: 3 
Line 49: $3
Line 50: Golden Oldie 
Line 51: 3 
Line 52: $1
Line 53: Hot Stuff 
Line 54: 3 
Line 55: $8
Line 56: Alternatively, you could have an individual table for each computation, as 
Line 57: here.
Line 58: Rental Charges 
Line 59: Category 
Line 60: Regular
Line 61: Days 
Line 62: 3
Line 63: Cost? 
Line 64: $3
Line 65: Rental Charges 
Line 66: Category 
Line 67: Golden Oldie 
Line 68: Days 
Line 69: 3
Line 70: Cost? 
Line 71: $1
Line 72: Rental Charges 
Line 73: Category 
Line 74: Hot Stuff 
Line 75: Days 
Line 76: 3
Line 77: Cost? 
Line 78: $8
Line 79: There are forms of tables with labels that make the test read almost like a 
Line 80: sentence.1
Line 81: 1. This is a DoFixture table from the Fit Library by Rick Mugridge [Cunningham01]. 
Line 82: Slim also has a version like this [Martin03]. 
Line 83: 
Line 84: --- 페이지 208 ---
Line 85: Specifying Multiple Actions 
Line 86: 185
Line 87: Rental Charges 
Line 88: When renting a CD 
Line 89: with category 
Line 90: Regular 
Line 91: for 
Line 92: 3 days 
Line 93: the charge 
Line 94: should be 
Line 95: $3
Line 96: When renting a CD 
Line 97: with category 
Line 98: Golden
Line 99: Oldie
Line 100: for 
Line 101: 3 days 
Line 102: the charge 
Line 103: should be 
Line 104: $1
Line 105: When renting a CD 
Line 106: with category 
Line 107: Hot Stuff 
Line 108: for 
Line 109: 3 days 
Line 110: the charge 
Line 111: should be 
Line 112: $8
Line 113: You do not need to use the same style table in all tests. The triad should select 
Line 114: the one most appropriate to the behavior being tested. In case of a disagreement, 
Line 115: the decision should be deferred to the customer unit. 
Line 116: Table Versus Text 
Line 117: The tests in this book have used tables to indicate the setups, actions, and 
Line 118: expected results. If the customer prefers, the tests can be expressed in pure text. 
Line 119: For example, the previous actions could be written as follows. 
Line 120: Rental Charges 
Line 121: Given a CD that is a Regular, when it is rented for 3 days, then the charge 
Line 122: should be $3. 
Line 123: Given a CD that is a Golden Oldie, when it is rented for 3 days, then the 
Line 124: charge should be $1. 
Line 125: Given a CD that is a Hot Stuff, when it is rented for 3 days, then the charge 
Line 126: should be $8. 
Line 127: Specifying Multiple Actions 
Line 128: Sam’s application has the business rule that a customer should not be allowed 
Line 129: to rent another CD after that customer exceeds the rental limit. You could show 
Line 130: this test as a sequence of action tables, such as this. 
Line 131: 
Line 132: --- 페이지 209 ---
Line 133: Chapter 21 Test Presentation
Line 134: 186
Line 135: Alternatively, you can specify all the actions in a calculation-style table. This 
Line 136: reduces the size of the test and can make it more understandable to all members 
Line 137: of the triad. 
Line 138: CD Rental Limit Reached 
Line 139: Given these rentals: 
Line 140: First rental: 
Line 141: Start 
Line 142: Check-Out
Line 143: Enter 
Line 144: CD ID 
Line 145: CD1
Line 146: Enter 
Line 147: Customer ID 
Line 148: 007
Line 149: Press 
Line 150: Check-Out 
Line 151: OK
Line 152: Second rental: 
Line 153: Start 
Line 154: Check-Out
Line 155: Enter 
Line 156: CD ID 
Line 157: CD3
Line 158: Enter 
Line 159: Customer ID 
Line 160: 007
Line 161: Press 
Line 162: Check-Out 
Line 163: OK
Line 164: Third rental: 
Line 165: Start 
Line 166: Check-Out
Line 167: Enter 
Line 168: CD ID 
Line 169: CD5
Line 170: Enter 
Line 171: Customer ID 
Line 172: 007
Line 173: Press 
Line 174: Check-Out 
Line 175: OK
Line 176: Then the next rental should fail: 
Line 177: Fourth rental: 
Line 178: Start 
Line 179: Check-Out
Line 180: Enter 
Line 181: CD ID 
Line 182: CD2
Line 183: Enter 
Line 184: Customer ID 
Line 185: 007
Line 186: Press 
Line 187: Check-Out 
Line 188: Rental_Limit_Exceeded
Line 189: 
Line 190: --- 페이지 210 ---
Line 191: Complex Data 
Line 192: 187
Line 193: In the ﬁrst version, the notes appear before each table. In this version, those 
Line 194: notes are included in the table to explain each step in the test. 
Line 195: Complex Data 
Line 196: An embedded table can show the individual parts of particular columns. For ex-
Line 197: ample, a customer with a name and an address that have individual parts could 
Line 198: be shown with embedded tables, as here. 
Line 199: Customer Data 
Line 200: Date Joined
Line 201: Address
Line 202: Name
Line 203: First 
Line 204: Last Prefix 
Line 205: John 
Line 206: Doe 
Line 207: Mr.  
Line 208: Street  
Line 209: City  
Line 210: State ZIP  
Line 211: 1 Doe Lane Somewhere NC 
Line 212: 99999 
Line 213: 03/04/2003 
Line 214: Another way of representing parts such as the address is to use a different 
Line 215: organization of the table. Each column represents a different level. As shown 
Line 216: below, the leftmost column is the topmost level. The next column breaks the 
Line 217: level into its parts. The rightmost column contains the values for each element. 
Line 218: Customer Data 
Line 219: Name
Line 220: First 
Line 221: John
Line 222: Last 
Line 223: Doe
Line 224: Preﬁ x 
Line 225: Mr.
Line 226: Address
Line 227: Street 
Line 228: 1 Doe Lane 
Line 229: City 
Line 230: Somewhere
Line 231: State 
Line 232: NC
Line 233: ZIP 
Line 234: 99999
Line 235: Date Joined 
Line 236: 03/04/2003
Line 237: CD Rental Limit Reached 
Line 238: CD ID 
Line 239: Customer ID 
Line 240: Check-Out Status? 
Line 241: Notes
Line 242: CD1 
Line 243: 007 
Line 244: OK 
Line 245: 1st rental 
Line 246: CD3 
Line 247: 007 
Line 248: OK 
Line 249: 2nd rental 
Line 250: CD5 
Line 251: 007 
Line 252: OK 
Line 253: 3rd rental 
Line 254: CD2 
Line 255: 007 
Line 256: Rental_Limit_Exceeded 
Line 257: 4th rental 
Line 258: 
Line 259: --- 페이지 211 ---
Line 260: Chapter 21 Test Presentation
Line 261: 188
Line 262: Custom Table Forms 
Line 263: The tables in the test can represent whatever is most appropriate for the ap-
Line 264: plication. If you were creating an acceptance test for an application that solves 
Line 265: Sudoku puzzles, you might have an input table that looked like this. 
Line 266: Sudoku Puzzle 
Line 267: 1 
Line 268: 4 
Line 269: 7
Line 270: 2 
Line 271: 5 
Line 272: 8
Line 273: 3 
Line 274: 6 
Line 275: 9
Line 276: 4 
Line 277: 7 
Line 278: 1
Line 279: 5 
Line 280: 8 
Line 281: 2
Line 282: 6 
Line 283: 9 
Line 284: 3
Line 285: 7 
Line 286: 1 
Line 287: 4
Line 288: 8 
Line 289: 2 
Line 290: 5
Line 291: 9 
Line 292: 3 
Line 293: 6
Line 294: The output table would look like the following. 
Line 295: Sudoku Solution 
Line 296: 1 
Line 297: 6 
Line 298: 5 
Line 299: 4 
Line 300: 9 
Line 301: 8 
Line 302: 7 
Line 303: 3 
Line 304: 2
Line 305: 9 
Line 306: 2 
Line 307: 4 
Line 308: 3 
Line 309: 5 
Line 310: 7 
Line 311: 6 
Line 312: 8 
Line 313: 1
Line 314: 8 
Line 315: 7 
Line 316: 3 
Line 317: 2 
Line 318: 1 
Line 319: 6 
Line 320: 5 
Line 321: 4 
Line 322: 9
Line 323: 4 
Line 324: 9 
Line 325: 8 
Line 326: 7 
Line 327: 3 
Line 328: 2 
Line 329: 1 
Line 330: 6 
Line 331: 5
Line 332: 3 
Line 333: 5 
Line 334: 7 
Line 335: 6 
Line 336: 8 
Line 337: 1 
Line 338: 9 
Line 339: 2 
Line 340: 4
Line 341: 2 
Line 342: 1 
Line 343: 6 
Line 344: 5 
Line 345: 4 
Line 346: 9 
Line 347: 8 
Line 348: 7 
Line 349: 3
Line 350: 7 
Line 351: 3 
Line 352: 2 
Line 353: 1 
Line 354: 6 
Line 355: 5 
Line 356: 4 
Line 357: 9 
Line 358: 8
Line 359: 6 
Line 360: 8 
Line 361: 1 
Line 362: 9 
Line 363: 2 
Line 364: 4 
Line 365: 3 
Line 366: 5 
Line 367: 7
Line 368: 5 
Line 369: 4 
Line 370: 9 
Line 371: 8 
Line 372: 7 
Line 373: 3 
Line 374: 2 
Line 375: 1 
Line 376: 6
Line 377: You might also have a test in which the puzzle has no solution or has multiple 
Line 378: possible solutions to see if the results match your expectation. A tester like Tom 
Line 379: might create a puzzle that has thousands of possible results or one that has only 
Line 380: a single digit in it to see how long it takes to get all the possible solutions. 
Line 381: In any event, the form of the test should be as compatible as possible with the 
Line 382: way the customer unit deals with the functionality. 
Line 383: 
Line 384: --- 페이지 212 ---
Line 385: Summary 
Line 386: 189
Line 387: Summary
Line 388: • Use the form of the table that is easiest for the customer unit to under-
Line 389: stand.
Line 390: • If a standard table form is unsuitable, create a table form that is more ap-
Line 391: propriate for the test. 
Line 392: 
Line 393: --- 페이지 213 ---
Line 394: This page intentionally left blank 