Line 1: 
Line 2: --- 페이지 286 ---
Line 3: Chapter 32 
Line 4: Case Study: E-Mail Addresses 
Line 5: “Beware of bugs in the above code; I have only proved it correct, 
Line 6: not tried it.”
Line 7: Donald Knuth 
Line 8: This study involves breaking down a complex test, which represents a complex 
Line 9: business rule, into simpler tests. The simpler tests can decrease time in under-
Line 10: standing and implementing the rule. 
Line 11: Context
Line 12: Almost every application that involves communication requires an e-mail ad-
Line 13: dress. When you enter an e-mail address, you should parse it to ensure that it 
Line 14: is in a valid format. The process of verifying that an e-mail address is actually 
Line 15: valid requires an exterior action, such as sending an e-mail to the address and 
Line 16: checking that it was not rejected. 
Line 17: The testers for one company had a set of e-mail address examples they uses to 
Line 18: test every application that had an e-mail address entry. The examples included 
Line 19: both correct and incorrect formatted addresses. The company also had a busi-
Line 20: ness rule that e-mail addresses from some domains were not acceptable. These 
Line 21: domains included mail servers that allowed completely anonymous e-mail. A 
Line 22: portion of the tests is shown here. 
Line 23: E-Mail Tests 
Line 24: E-Mail 
Line 25: Valid? 
Line 26: Reason
Line 27: George@sam.com 
Line 28: Yes
Line 29: George@george@same.com 
Line 30: No 
Line 31: Two @s 
Line 32: .George@sam.com 
Line 33: No 
Line 34: Invalid name 
Line 35: 263
Line 36: 
Line 37: --- 페이지 287 ---
Line 38: Chapter 32 Case Study: E-Mail Addresses
Line 39: 264
Line 40: E-Mail Tests 
Line 41: E-Mail 
Line 42: Valid? 
Line 43: Reason
Line 44: George@samcom 
Line 45: No 
Line 46: Invalid domain 
Line 47: George+Bill@sam.com 
Line 48: Yes 
Line 49: + is allowed in name 
Line 50: George@hotmail.com 
Line 51: No 
Line 52: Banned domain 
Line 53: George@iamoutogetyou.com 
Line 54: No 
Line 55: Banned domain 
Line 56: ...and many more 
Line 57: Every time an e-mail address was entered on an input screen, this entire set 
Line 58: of tests was run. 
Line 59: An E-Mail Trick 
Line 60: You may notice that George+Bill@sam.com is a valid e-mail address. The 
Line 61: + is allowed in the part prior to the @ sign. It has a special meaning in most 
Line 62: e-mail systems. The e-mail is delivered to the part before the + (George 
Line 63: in this case). The full address (George+Bill) is used in the To part of the 
Line 64: e-mail. Your e-mail client (Eudora, Thunderbird, Outlook, and so on.) can 
Line 65: ﬁlter based on the part after the + (Bill) to put the message in a particular 
Line 66: folder or perform another action. Some e-mail systems or internal servers 
Line 67: may discard the + so that the mail instead goes to a user named GeorgeBill. 
Line 68: That represents a different user than George. If you try this trick, test this 
Line 69: on your system to ensure that it works before using the trick. 
Line 70: Breaking Down Tests 
Line 71:  
Line 72: This acceptance test is pretty clear. When I ask developers how much time they 
Line 73: think it will take to program an e-mail validation routine that will pass this test, 
Line 74: they suggest a couple of days. I then suggest breaking down this test into smaller 
Line 75: ones may decrease the time. 
Line 76: We saw in Chapter 13, “Simpliﬁcation by Separation,” that breaking down a 
Line 77: business rule into simpler business rules makes things easier to understand and 
Line 78: test. Each smaller table represents either a requirement or a test. Sometimes it’s 
Line 79: hard to distinguish between the two. The tables presented here represent either 
Line 80: details of an e-mail address from the business point of view or unit tests for a 
Line 81: module that implements e-mail format veriﬁcation. 
Line 82: In the e-mail situation, we can use the rules that the Internet standards pro-
Line 83: vide in RFC 2822 [IEFF01]. The ﬁrst rule for a valid e-mail address is that it con-
Line 84: tain one and only one @ symbol. The @ separates the name part of the address 
Line 85: 
Line 86: --- 페이지 288 ---
Line 87: Breaking Down Tests 
Line 88: 265
Line 89: from the domain part. For example, with ken.pugh@netobjectives.com, ken.
Line 90: pugh is the name part and netobjectives.com is the domain. The ofﬁcial term for 
Line 91: the name part is local-part. So we will use that in our tables. 
Line 92: E-Mail Split into Local-Part and Domain 
Line 93: E-Mail 
Line 94: Valid? 
Line 95: Local-Part? 
Line 96: Domain?
Line 97: X@Y 
Line 98: Yes 
Line 99: X 
Line 100: Y
Line 101: XY 
Line 102: No 
Line 103: DNC 
Line 104: DNC
Line 105: XY@XY@XY 
Line 106: No 
Line 107: DNC 
Line 108: DNC
Line 109:  
Line 110: DNC means “Do Not Care” because the e-mail is invalid. Usually, a devel-
Line 111: oper says that it will take less than 15 minutes to implement code that per-
Line 112: forms this check. It all depends on how familiar the developer is with the regular 
Line 113: expression library. 
Line 114: Local-Part Validation 
Line 115: According to the rules, the local-part must only contain the following characters: 
Line 116: • Uppercase and lowercase English letters (a through z, A through Z) 
Line 117: • Digits 0 through 9 
Line 118: • Period (.), provided that it is not the ﬁrst or the last character and it doesn’t 
Line 119: appear two or more times consecutively 
Line 120: • ! # $ % & ’ * + – / = ? ^ _ ` { | } ~ 
Line 121: The maximum size of the local-part is 64 characters. 1 We can put this free 
Line 122: text business rule into a table. 
Line 123: Local-Part Allowable Characters 
Line 124: Characters 
Line 125: Allowed? 
Line 126: Notes
Line 127: a through z 
Line 128: Yes
Line 129: A through Z 
Line 130: Yes
Line 131: 0 through 9 
Line 132: Yes
Line 133: ! # $ % & ’ * + – / = ? ^ _ ` { | } ~ 
Line 134: Yes
Line 135: . 
Line 136: Yes 
Line 137: If not ﬁrst, last, or two consecutive 
Line 138: Anything else 
Line 139: No
Line 140:   1 . If you are actually following this case study to perform your own validation, you 
Line 141: may also want to eliminate characters that can inject SQL [Security01]. You would 
Line 142: not allow a single quote or a forward slash. 
Line 143: 
Line 144: --- 페이지 289 ---
Line 145: Chapter 32 Case Study: E-Mail Addresses
Line 146: 266
Line 147: We could have a test of the allowed characters for the local-part. Of course, 
Line 148: we need some test cases to see that the character rules are applied properly. 
Line 149: Local-Part Character Combination Tests 
Line 150: Local-Part 
Line 151: Valid? 
Line 152: Notes
Line 153: George 
Line 154: Yes
Line 155: George\ 
Line 156: No 
Line 157: Character not allowed 
Line 158: George..a 
Line 159: No 
Line 160: Period appears twice in a row 
Line 161: .George 
Line 162: No 
Line 163: Period ﬁrst 
Line 164: George. 
Line 165: No 
Line 166: Period last 
Line 167: And, of course, we should have some rules for length. 
Line 168: Local-Part Length Tests 
Line 169: Local-Part 
Line 170: Valid? 
Line 171: Notes
Line 172: No 
Line 173: Zero length 
Line 174: a 
Line 175: Yes 
Line 176: Minimum length 
Line 177: 123456789012345678901234567890123456789012
Line 178: 3456789012345678901234
Line 179: Yes 
Line 180: Maximum length 
Line 181: 123456789012345678901234567890123456789012
Line 182: 34567890123456789012345
Line 183: No 
Line 184: Exceeds maxi-
Line 185: mum length 
Line 186: Now when I ask a developer how long it will take to implement just the local-
Line 187: part rules, he usually says no more than an hour. 
Line 188: Domain Tests 
Line 189: The rules for domains are different than for the local part. The allowed charac-
Line 190: ters are as follows. 
Line 191: Domain-Allowable Characters 
Line 192: Character 
Line 193: Allowed? 
Line 194: Notes
Line 195: a through z 
Line 196: Yes
Line 197: .
Line 198: Yes
Line 199: Must have at least one 
Line 200: Cannot be ﬁrst or last character 
Line 201: – 
Line 202: Yes
Line 203: 0 through 9 
Line 204: Yes
Line 205: Anything else 
Line 206: No
Line 207: 
Line 208: --- 페이지 290 ---
Line 209: Breaking Down Tests 
Line 210: 267
Line 211: A domain has a maximum of 255 characters, and periods separate the parts. 
Line 212: The top level is the rightmost part of the domain, the second level is the next-
Line 213: most right part, and so forth. So for a domain with two periods, the levels are 
Line 214: as follows: 
Line 215: third-level.second-level.top-level
Line 216: For example, the domain “www.netobjectives.com” has three levels. The 
Line 217: third level is “www”; the second level is “netobjectives”; and the top level is 
Line 218: “com”. Most e-mail addresses use a two level domain, such as “netobjectives.
Line 219: com”.
Line 220: There must be at least a top-level domain and a second-level domain. Most 
Line 221: e-mail addresses use just two levels, but there is no limit to the levels within the 
Line 222: conﬁnes of the maximum of 255 characters. Top-level domains are standard, 
Line 223: such as “com”, “org”, “net”, “us”, “ca”, “mx”, “tv”, and so on. 
Line 224: We have a few alternatives for the top-level domain part. We could have a 
Line 225: table that lists all valid top levels, such as this: 
Line 226: Top-Level Domain List 
Line 227: Top Level 
Line 228: Valid?
Line 229: com 
Line 230: Yes
Line 231: net 
Line 232: Yes
Line 233: us 
Line 234: Yes
Line 235: ...and so forth for all possibilities 
Line 236: Yes
Line 237: Anything not listed 
Line 238: No
Line 239: But it might be work to keep this table up to date. As an alternative, we 
Line 240: could accept top-level parts that are at least two characters and at most four 
Line 241: characters. However, some top-level domains that might not be valid would be 
Line 242: accepted since they passed the simple rule. For example: 
Line 243: Top-Level Domain Parts 
Line 244: Top Level 
Line 245: Valid? 
Line 246: Notes
Line 247: c 
Line 248: No 
Line 249: Too short 
Line 250: co 
Line 251: Yes 
Line 252: Minimum length 
Line 253: come 
Line 254: Yes 
Line 255: Maximum length 
Line 256: comet 
Line 257: No 
Line 258: Too long 
Line 259: The issue with having something that lists all domains is that when a new 
Line 260: top-level domain is created, the domain list table has to be updated. However, 
Line 261: 
Line 262: --- 페이지 291 ---
Line 263: Chapter 32 Case Study: E-Mail Addresses
Line 264: 268
Line 265: you can ensure that there is validation for all the ones that are currently in the 
Line 266: table. There is a generic aspect to this trade-off. The more speciﬁc you are, 
Line 267: the less possibility there is that something invalid will sneak through. However, 
Line 268: the less speciﬁc you are, the less often you’ll have to update anything if some-
Line 269: thing new that ﬁts into the model passes through. It’s your choice, based on 
Line 270: customer input. 
Line 271: Here are the tests for the domain structure. 
Line 272: Domain Breakdown Tests 
Line 273: Domain
Line 274: Top-Level
Line 275: Domain?
Line 276: Second-Level
Line 277: Domain?
Line 278: Third-Level
Line 279: Domain? 
Line 280: Valid? 
Line 281: Notes
Line 282: A.B.COM 
Line 283: COM 
Line 284: B 
Line 285: A 
Line 286: Yes
Line 287: COM
Line 288: No
Line 289: Must have 
Line 290: at least one 
Line 291: period
Line 292: B.COM 
Line 293: COM 
Line 294: B 
Line 295: Yes 
Line 296: Could require 
Line 297: two
Line 298: A.B.C.COM 
Line 299: COM 
Line 300: C 
Line 301: B 
Line 302: Yes 
Line 303: Fourth level 
Line 304: is A 
Line 305: A.B.COM. 
Line 306: No 
Line 307: Cannot end in 
Line 308: period
Line 309: .A.B.COM 
Line 310: No 
Line 311: Cannot begin 
Line 312: with period 
Line 313: And, of course, we can have a test for the maximum length of the domain. 
Line 314: That is left to an exercise for the readers. 
Line 315: Developers, when asked, usually suggest that it would take an hour or so to 
Line 316: code the method that this table could be tested against. 
Line 317: Disallowed Domain Tests 
Line 318: Finally, there is a list of disallowed domains, or domains that customers cannot 
Line 319: use. These domains permit people to send anonymous e-mails. Whether a par-
Line 320: ticular application wants to disallow these domains is up to it. The following list 
Line 321: is static. If we wanted to be able to update the list, we would create tests to verify 
Line 322: that the list is updated correctly. This table represents the list. We could use it as 
Line 323: an input to the program or as a test to see that every domain on it is recognized 
Line 324: to be a disallowed domain. 
Line 325: 
Line 326: --- 페이지 292 ---
Line 327: Breaking Down Tests 
Line 328: 269
Line 329: Disallowed Domains 
Line 330: Domain 
Line 331: Reason
Line 332: Hotmail.com 
Line 333: Anonymous mail 
Line 334: Imouttogetyou.com 
Line 335: Spam source 
Line 336: Anymore ??? 
Line 337: When developers are asked how long coding will take (without worrying 
Line 338: about updating the list), they usually answer around an hour. 
Line 339: The total time estimates from the individual pieces is usually around four 
Line 340: hours. The original time estimate from the combined test is often two days. By 
Line 341: breaking down the tests into smaller parts, the estimated time decreases because 
Line 342: each part appears simpler. In addition, the smaller parts are easier to program. 
Line 343: Test to Ensure Connection 
Line 344: You can run the same tests as presented at the beginning of this chapter against 
Line 345: a module that passes all these tests. That would ensure that all the validation 
Line 346: functions have been tied together properly. It’s possible that the test cases in this 
Line 347: table will fail because the results in these tables differ from the actual result. In 
Line 348: that case, you get to decide whether you should alter the underlying implemen-
Line 349: tation to agree with these tests or alter these tests, because they actually do not 
Line 350: represent e-mail address validation correctly. 
Line 351: Veriﬁcation Test 
Line 352: There are two parts to the validation process. The ﬁrst is to make sure that the 
Line 353: e-mail address is properly formatted. The second is to ensure that a properly 
Line 354: formatted e-mail address actually represents a real e-mail address. Usually, you 
Line 355: send an e-mail to the address. If it bounces, it is invalid. The e-mail often con-
Line 356: tains either a note to reply to the message or a link to a web page that can record 
Line 357: that the message was received. The table might look like this. 
Line 358: Actual E-Mail Address Check 
Line 359: Sent Message 
Line 360: Bounced 
Line 361: Received Reply 
Line 362: Valid?
Line 363: Yes 
Line 364: No 
Line 365: Yes 
Line 366: Yes
Line 367: Yes 
Line 368: Yes 
Line 369: Do not care 
Line 370: No
Line 371: Yes 
Line 372: No 
Line 373: No 
Line 374: Unknown
Line 375: No 
Line 376: Do not care 
Line 377: Do not care 
Line 378: Unknown
Line 379: 
Line 380: --- 페이지 293 ---
Line 381: Chapter 32 Case Study: E-Mail Addresses
Line 382: 270
Line 383: Summary
Line 384: • Break up complicated conditions into smaller conditions. 
Line 385: • Smaller conditions are easier to test and code. 
Line 386: • Validation of correct format is only part of validation. 
Line 387: • Validate whether a correctly formatted value represents a real value (such 
Line 388: as e-mail address, customer ID, or CD ID). 