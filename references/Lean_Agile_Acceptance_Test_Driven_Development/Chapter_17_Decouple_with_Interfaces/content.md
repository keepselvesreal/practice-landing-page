Line 1: 
Line 2: --- 페이지 176 ---
Line 3: Chapter 17 
Line 4: Decouple with Interfaces 
Line 5: Wizard of Oz: “Pay no attention to that man behind the curtain.”
Line 6: The Wizard of Oz 
Line 7: Developers can create acceptance tests for service implementations. The tests 
Line 8: can be both for accuracy and for performance. 
Line 9: Tests for a Service Provider 
Line 10: Cathy wants the ZIP code to be checked for customer contact addresses. Debbie 
Line 11: needs a service for the veriﬁcation of a ZIP code for an address; she is not going 
Line 12: to code the service herself, but obtain it from another group. Dave is another 
Line 13: developer who is going to provide that service. As a backup plan in case Dave 
Line 14: cannot implement the service, Debbie may purchase it from an external vendor. 
Line 15: As the requester, Debbie needs to create acceptance tests for the service that 
Line 16: Dave will use to test his implementation. The tests should be independent of the 
Line 17: service provider. Ideally, she should not have to rewrite any of her production 
Line 18: code if the service provider is changed, so she creates an application program-
Line 19: ming interface (API) that Dave should implement [Pugh01]. If she uses another 
Line 20: service provider, she will adapt its interface to this API. The tests that she writes 
Line 21: as well as her production application are coded to the API. 
Line 22: The Interface 
Line 23: Debbie creates an API that describes what she wants the ZIP code veriﬁcation 
Line 24: interface to look like: 
Line 25: interface ZipCodeLookup {
Line 26:    ZipCode lookupZipCode( String streetAddress,
Line 27:        String City, StateID state ) throws ZipCodeNotFound
Line 28:    } 
Line 29: 153
Line 30: 
Line 31: --- 페이지 177 ---
Line 32: Chapter 17 Decouple with Interfaces
Line 33: 154
Line 34: “ZipCode” is a data class that contains the ZIP code. The lookupZipCode()
Line 35: method needs to indicate an error if the ZIP code cannot be found. From a 
Line 36: programmer’s point of view, if the ZIP code was not ﬁndable, the method could 
Line 37: return the value of null or throw an exception that contained further informa-
Line 38: tion. The “StateID” is a data class that contains a reference to a valid U.S. state 
Line 39: or territory. 
Line 40: There are other things that Debbie may need, such as the ability to get the 
Line 41: city and state that correspond to a ZIP code. If so, she would add that to the 
Line 42: interface.
Line 43: Debbie provides the following table as an example of the tests she is going to 
Line 44: run against the interface. 
Line 45: ZIP Code Lookup 
Line 46: Street Address 
Line 47: City 
Line 48: State 
Line 49: ZIP Code? 
Line 50: 1 East Oak Street 
Line 51: Chicago 
Line 52: IL 
Line 53: 60611
Line 54: 101 Penny Lane 
Line 55: Danville 
Line 56: VT 
Line 57: 05828
Line 58: 1 No Place 
Line 59: Nowhere 
Line 60: OK 
Line 61: NotFound
Line 62: Dave may create an implementation that uses a subscription to the United 
Line 63: States Postal Service (USPS) web-service, a corporately-owned address valida-
Line 64: tion program, or some other system. If Debbie needs a quick way to do an end-
Line 65: to-end test, she might create a browser-simulator version that interacts with the 
Line 66: usps.com website and provides the answers found on that site. If she needs a 
Line 67: way to have a quick unit test for her code that uses this service, she might create 
Line 68: a “test double” (see Chapter 11 “System Boundary”) for ZipCodeLookup. The 
Line 69: test double might only return a small set of ZIP codes, such as the set listed in 
Line 70: this table. 
Line 71: The “StateID” data class listed in the interface speciﬁcation needs to be 
Line 72: deﬁned. Debbie can use a table to do that. She could include just the states or all 
Line 73: USPS recognized abbreviations. 
Line 74: StateID
Line 75: Full Name 
Line 76: Abbreviation
Line 77: North Carolina 
Line 78: NC
Line 79: Massachusetts 
Line 80: MA
Line 81: ... and more 
Line 82: The ZIP Code Lookup tests do not have to include states that are not in this 
Line 83: table.
Line 84: 
Line 85: --- 페이지 178 ---
Line 86: Tests for a Service Provider 
Line 87: 155
Line 88: Quality Attribute Tests 
Line 89: Debbie can provide quality attribute tests for an interface implementation. The 
Line 90: initial test checks that the interface is working properly. She may also be con-
Line 91: cerned with the performance of the implementation. If it takes a long time to 
Line 92: look up a ZIP code, then the user experience will suffer. So she can specify the 
Line 93: amount of time in a test. The time limits may differ based on the type of result 
Line 94: (success or failure) and the particulars of the data being passed to the service. 
Line 95: ZIP Code Lookup 
Line 96: Street Address 
Line 97: City 
Line 98: State 
Line 99: ZIP Code? 
Line 100: Time?
Line 101: 1 East Oak Street 
Line 102: Chicago 
Line 103: IL 
Line 104: 60611 
Line 105: .01
Line 106: 101 Penny Lane 
Line 107: Danville 
Line 108: VT 
Line 109: 05828 
Line 110: .01
Line 111: 1 No Place 
Line 112: Nowhere 
Line 113: OK 
Line 114: NotFound 
Line 115: .2
Line 116: For a data-lookup style service, such as the ZIP code, Debbie could also make 
Line 117: up acceptance criteria for the completeness and accuracy of the data. The crite-
Line 118: ria can be speciﬁed in a table such as: 
Line 119: ZIP Code Lookup Qualities 
Line 120: Completeness 
Line 121: Accuracy of What Is Available 
Line 122: 99.999% 
Line 123: 99.9999%
Line 124: Determining whether an implementation meets these criteria is a difﬁcult task 
Line 125: and beyond the scope of this book. However if you have two implementations 
Line 126: of a service, you can at least cross-check them. 
Line 127: Comparing Implementations 
Line 128: In the case of ZIP Code Lookup, Debbie may be able to obtain two implemen-
Line 129: tations of the interface. She may not know in advance what the correct results 
Line 130: are. All she knows is that the results of the two implementations need to match. 
Line 131: This is often the case when you have an existing system and you are rewriting 
Line 132: the system to use another technology. The external behavior of the new system 
Line 133: must match the existing system. So you ﬁrst run one implementation and store 
Line 134: the results. This forms the acceptable values (the oracle [Bach01]) for the new 
Line 135: system. Then you run the second implementation and compare the results to 
Line 136: those found in the ﬁrst implementation. 
Line 137: There are at least two ways to do this. The ﬁrst way involves using variables. 
Line 138: It’s introduced here to show how a test can reuse results from earlier in a test. 
Line 139: The second way eliminates some redundancy. 
Line 140: 
Line 141: --- 페이지 179 ---
Line 142: Chapter 17 Decouple with Interfaces
Line 143: 156
Line 144: Using tables to represent this comparison involves creating some type of vari-
Line 145: able. A variable is used to store the results of one action for use in a later action. 
Line 146: You need to be able have a way to show when a value is stored in the variable 
Line 147: and when it is retrieved. For the purposes of demonstration, we’ll use a → sym-
Line 148: bol to show a value is stored into a variable and a → symbol to show the value 
Line 149: is retrieved from the variable. 1 Debbie creates the following table for the ﬁrst 
Line 150: implementation of the interface. 
Line 151: ZIP Code Lookup 
Line 152: Implementation = Dave’s 
Line 153: Street Address 
Line 154: City 
Line 155: State 
Line 156: ZIP Code? 
Line 157: 1 East Oak Street 
Line 158: Chicago 
Line 159: IL 
Line 160: →eastoakzip
Line 161: 101 Penny Lane 
Line 162: Danville 
Line 163: VT 
Line 164: →pennylanezip
Line 165: 1 No Place 
Line 166: Nowhere 
Line 167: OK 
Line 168: →noplacezip
Line 169: The ZIP codes are stored in variables named eastoakzip, pennylanezip, and 
Line 170: noplacezip. Debbie then makes the next table for the second implementation. 
Line 171: ZIP Code Lookup 
Line 172: Implementation = USPS 
Line 173: Street Address 
Line 174: City 
Line 175: State 
Line 176: ZIP Code? 
Line 177: 1 East Oak Street 
Line 178: Chicago 
Line 179: IL 
Line 180: ←eastoakzip
Line 181: 101 Penny Lane 
Line 182: Danville 
Line 183: VT 
Line 184: ←pennylanezip
Line 185: 1 No Place 
Line 186: Nowhere 
Line 187: OK 
Line 188: ←noplacezip
Line 189: The ZIP codes returned by this implementation are compared to values stored 
Line 190: in eastoakzip, pennylanezip, and noplacezip. If a value does not match, an error 
Line 191: is indicated. If an error appears, Debbie cannot be sure which implementation 
Line 192: was wrong without further investigation. 
Line 193: If the number of comparisons was large, Debbie might use a second way to 
Line 194: compare the ZIP codes that eliminates some redundancy. Rather than use a 
Line 195: table to list the individual data items, she might create a module that does the 
Line 196: comparison internally. So all she would list are the input values. If a mismatch 
Line 197: occurs between the two implementations, the two answers can be shown in the 
Line 198: ZIP Code column as follows: 
Line 199:   1.  The methodology and symbols used for storing and retrieving values vary in each 
Line 200: test framework. 
Line 201: 
Line 202: --- 페이지 180 ---
Line 203: Separating User Interface from Service 
Line 204: 157
Line 205: ZIP Code Lookup Comparison 
Line 206: Implementation = Dave’s 
Line 207: Implementation = USPS 
Line 208: Street Address 
Line 209: City 
Line 210: State 
Line 211: Dave’s ZIP Code? 
Line 212: USPS ZIP Code? 
Line 213: 1 East Oak Street 
Line 214: Chicago 
Line 215: IL
Line 216: 60611
Line 217: 60612
Line 218: 101 Penny Lane 
Line 219: Danville 
Line 220: VT
Line 221: 1 No Place 
Line 222: Nowhere 
Line 223: OK
Line 224: Comparing Implementations 
Line 225: Using and comparing two or more implementations is a common design 
Line 226: solution, particularly in critical systems. For example, in space ﬂight, three 
Line 227: computers calculate the required ﬂight operations, such as when to turn 
Line 228: on the rocket booster. The results of the three are compared. If all three 
Line 229: computers report the same results, the operation commences. If two agree 
Line 230: and one doesn’t, the majority usually wins and the report is, “Houston, 
Line 231: we have a problem that we can deal with for the moment.” If all of them 
Line 232: disagree, the ﬂight reports, “Houston, we have a big problem.” 
Line 233: Separating User Interface from Service 
Line 234: Debbie has not speciﬁed how the state in the address is going to appear in the 
Line 235: user interface. She knows that separating the business rules from the display 
Line 236: makes for easier testing, as shown in Chapter 14, “Separate View from Model.” 
Line 237: There are at least four ways the state could appear on the user interface: 
Line 238: • A text box that accepts two-character abbreviations for the state 
Line 239: • A text box that accepts the full name for the state 
Line 240: • A drop-down list that contains the two-character abbreviations for each 
Line 241: state
Line 242: • A drop-down list that contains the full name for each state 2
Line 243: These are four display manifestations of the same requirement; they are not 
Line 244: four different requirements. They differ in the user experience. In the drop-down 
Line 245:   2.  As a resident of North Carolina, I highly prefer the two-character drop-down list. 
Line 246: Can you ﬁgure out why? 
Line 247: 
Line 248: --- 페이지 181 ---
Line 249: Chapter 17 Decouple with Interfaces
Line 250: 158
Line 251: version, users cannot enter an incorrect state, but they may have to type more. 3
Line 252: The selection of one is based on user quality feedback. 
Line 253: In any event, the ﬁeld for the ZIP code should only allow either ﬁve or nine 
Line 254: digits to be entered. These are the two valid lengths for U.S. ZIP codes. Allow-
Line 255: ing other characters or lengths would cause unnecessary calls to the ZIP Code 
Line 256: Lookup.
Line 257: If Debbie had a ﬁeld that allowed the user to enter a ZIP code, she would 
Line 258: check that ZIP code against the one returned by ZIP Code Lookup. How she 
Line 259: displays a mismatch is based on the desired user experience. The mismatch 
Line 260: might show up in a dialog box, as a line at the top of the dialog box, as a mes-
Line 261: sage next to the ZIP code, or as a different colored ZIP code. 
Line 262: Separation of Concerns 
Line 263: The preceding example is being pretty U.S centric. Debbie might need to do 
Line 264: postal code matching for all the countries in the world. To keep things simple, 
Line 265: she could have a master table of all the countries that breaks out to tables of 
Line 266: tests for each country. 
Line 267: Country Breakout 
Line 268: Country 
Line 269: ISO Code 
Line 270: Input With 
Line 271: Validate With 
Line 272: U.S.A. 
Line 273: US 
Line 274: US Address Form 
Line 275: ZIPCodeLookup
Line 276: Canada 
Line 277: CA 
Line 278: CA Address Form 
Line 279: CAAddressValidator
Line 280: ...and many more 
Line 281: Reusable Business Rules 
Line 282: A business rule is something that is true regardless of the technology employed 
Line 283: (paper, computer, and so on). The rule that a ZIP code be valid for an address is 
Line 284: true regardless of whether the envelope is printed on a laser printer or handwrit-
Line 285: ten. Implementations of business rules should be exposed so that they can be 
Line 286: used in multiple places, not just the middle tier. 
Line 287: For example, the user interface may require business rule checking to allow 
Line 288: errors to be identiﬁed in a more user-friendly manner. The ZIP code for cus-
Line 289: tomer address may be veriﬁed as part of the input process. To avoid duplication 
Line 290:   3. Try to enter North Carolina in a drop-down that has full state names. How many 
Line 291: keystrokes does it take? 
Line 292: 
Line 293: --- 페이지 182 ---
Line 294: Summary 
Line 295: 159
Line 296: of functionality that would require duplication of testing, the user interface 
Line 297: should use the same module as the middle tier. The means for doing so depend 
Line 298: on the technology involved and are beyond the scope of this book. 4
Line 299: Reuse extends beyond a single application. If a function, such as ZIP Code 
Line 300: Lookup, is used by multiple applications, Debbie would put the component into 
Line 301: an infrastructure or core system library. That would eliminate needing to have 
Line 302: tests applied to each application. 
Line 303: Summary
Line 304: • Developer acceptance tests should be created for every service. 
Line 305: • A common API should be created for services that have multiple imple-
Line 306: mentations.
Line 307: • Create performance tests for service implementations. 
Line 308: • Create completeness and accuracy criteria for service implementation, 
Line 309: when appropriate. 
Line 310: • Create comparative tests for checking old versus new implementations. 
Line 311: • Keep tests for services separate from tests for user interfaces. 
Line 312: • Consider whether services are application services or core services. 
Line 313:   4. For example, you might use Ajax [Riordan01]. 
Line 314: 
Line 315: --- 페이지 183 ---
Line 316: This page intentionally left blank 