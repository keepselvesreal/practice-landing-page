Line 1: 
Line 2: --- 페이지 58 ---
Line 3: 30
Line 4: Specification-based
Line 5: testing
Line 6: Software requirements are undoubtedly the most valuable artifact of software test-
Line 7: ing. By requirements, I mean any textual document that describes what a functional-
Line 8: ity should do. Requirements tell us precisely what the software needs to do and
Line 9: what it should not do. They describe the intricacies of the business rules that the
Line 10: software has to implement and we need to validate. Therefore, requirements
Line 11: should be the first artifact you go for when it comes to testing!
Line 12:  In this chapter, we explore specification-based testing. These techniques use the
Line 13: program requirements—such as agile user stories or UML use cases—as testing
Line 14: input. We will discuss how to use all the information available in a requirement to
Line 15: systematically derive a set of tests that exercise that requirement extensively.
Line 16:  Where does specification-based testing fit into the entire testing process? Imag-
Line 17: ine that a software developer receives a new feature to implement. The developer
Line 18: writes the implementation code, guided by test-driven development (TDD)
Line 19: This chapter covers
Line 20: Creating test cases using specification-based 
Line 21: testing
Line 22: Identifying and creating test cases for program 
Line 23: boundaries
Line 24: 
Line 25: --- 페이지 59 ---
Line 26: 31
Line 27: The requirements say it all
Line 28: cycles, and always ensures that the code is testable. With all the classes ready, the
Line 29: developer switches to “testing mode.” It is time to systematically look for bugs. This is
Line 30: where specification testing fits in: it is the first testing technique I recommend using
Line 31: once you’re in testing mode.
Line 32:  As I mentioned, the idea of specification-based testing is to derive tests from the
Line 33: requirements themselves. The specific implementation is less important. Of course,
Line 34: we use source code to test, too—this structural testing is the next technique in the work-
Line 35: flow. Once you have a complete picture of all the techniques, you will be able to use
Line 36: them iteratively and go back and forth between them.
Line 37: 2.1
Line 38: The requirements say it all
Line 39: Let’s start with an example. A new set of requirements comes in for you to develop. As
Line 40: soon as you begin to analyze the requirements, you identify a particular method you
Line 41: need to implement: a method that searches for substrings between two tags in a given
Line 42: string and returns all the matching substrings. Let’s call this method substrings-
Line 43: Between(), inspired by the Apache Commons Lang library (http://mng.bz/nYR5).
Line 44: You are about to test a real-world open source method.
Line 45:  After some thinking, you end up with the following requirements for the sub-
Line 46: stringsBetween() method:
Line 47: Method: substringsBetween()
Line 48: Searches a string for substrings delimited by a start and end tag, returning all
Line 49: matching substrings in an array.
Line 50: 
Line 51: str—The string containing the substrings. Null returns null; an empty
Line 52: string returns another empty string.
Line 53: 
Line 54: open—The string identifying the start of the substring. An empty string
Line 55: returns null.
Line 56: 
Line 57: close—The string identifying the end of the substring. An empty string
Line 58: returns null.
Line 59: The program returns a string array of substrings, or null if there is no match.
Line 60: Example: if str = “axcaycazc”, open = “a”, and close = “c”, the output will be
Line 61: an array containing [“x”, “y”, “z”]. This is the case because the “a<something>c”
Line 62: substring appears three times in the original string: the first contains “x” in
Line 63: the middle, the second “y,” and the last “z.”
Line 64: With these requirements in mind, you write the implementation shown in listing 2.1.
Line 65: You may or may not use TDD (discussed in chapter 8) to help you develop this feature.
Line 66: You are somewhat confident that the program works. Slightly, but not completely.
Line 67:  
Line 68:  
Line 69:  
Line 70: 
Line 71: --- 페이지 60 ---
Line 72: 32
Line 73: CHAPTER 2
Line 74: Specification-based testing
Line 75: public static String[] substringsBetween(final String str,
Line 76:  final String open, final String close) {
Line 77:   if (str == null || isEmpty(open) || isEmpty(close)) {   
Line 78:     return null;
Line 79:   }
Line 80:   int strLen = str.length();
Line 81:   if (strLen == 0) {    
Line 82:     return EMPTY_STRING_ARRAY;
Line 83:   }
Line 84:   int closeLen = close.length();
Line 85:   int openLen = open.length();
Line 86:   List<String> list = new ArrayList<>();
Line 87:   int pos = 0;               
Line 88:   while (pos < strLen - closeLen) {
Line 89:     int start = str.indexOf(open, pos);   
Line 90:     if (start < 0) {  
Line 91:       break;
Line 92:     }
Line 93:     start += openLen;
Line 94:     int end = str.indexOf(close, start);   
Line 95:     if (end < 0) {      
Line 96:       break;
Line 97:     }
Line 98:     list.add(str.substring(start, end));    
Line 99:     pos = end + closeLen;     
Line 100:   }
Line 101:   if (list.isEmpty()) {   
Line 102:     return null;
Line 103:   }
Line 104:   return list.toArray(EMPTY_STRING_ARRAY);
Line 105: }
Line 106: Let’s walk through an example. Consider the inputs str = “axcaycazc”, open = “a”, and
Line 107: close = “c”. None of the three strings are empty, so the method goes straight to the
Line 108: openLen and closeLen variables. These two variables store the length of the open and
Line 109: close strings, respectively. In this case, both are equal to 1, as “a” and “c” are strings
Line 110: with a single character.
Line 111:  The program then goes into its main loop. This loop runs while there still may be
Line 112: substrings in the string to check. In the first iteration, pos equals zero (the beginning
Line 113: of the string). We call indexOf, looking for a possible occurrence of the open tag. We
Line 114: Listing 2.1
Line 115: Implementing the substringsBetween() method
Line 116: If the pre-
Line 117: conditions do not 
Line 118: hold, returns null 
Line 119: right away
Line 120: If the string is empty, 
Line 121: returns an empty 
Line 122: array immediately
Line 123: A pointer that indicates 
Line 124: the position of the string 
Line 125: we are looking at
Line 126: Looks for the next 
Line 127: occurrence of the 
Line 128: open tag
Line 129: Breaks the loop if the 
Line 130: open tag does not appear 
Line 131: again in the string
Line 132: Looks for
Line 133: the close
Line 134: tag
Line 135: Breaks the loop if the 
Line 136: close tag does not appear 
Line 137: again in the string
Line 138: Gets the substring 
Line 139: between the open 
Line 140: and close tags
Line 141: Moves the pointer to 
Line 142: after the close tag we 
Line 143: just found
Line 144: Returns
Line 145: null if we
Line 146: do not
Line 147: find any
Line 148: substrings
Line 149: 
Line 150: --- 페이지 61 ---
Line 151: 33
Line 152: The requirements say it all
Line 153: pass the open tag and the position to start the search, which at this point is 0. indexOf
Line 154: returns 0, which means we found an open tag. (The first element of the string is
Line 155: already the open tag.)
Line 156:  The program then looks for the end of the substring by calling the indexOf
Line 157: method again, this time on the close tag. Note that we increase the start position by
Line 158: the length of the open tag because we want to look for the close tag after the end of
Line 159: the entire open tag. Remember that the open tag has a length of one but can have any
Line 160: length. If we find a close tag, this means there is a substring to return to the user. We
Line 161: get this substring by calling the substring method with the start and end positions as
Line 162: parameters. We then reposition our pos pointer, and the loop iterates again. Figure 2.1
Line 163: shows the three iterations of the loop as well as the locations to which the main point-
Line 164: ers (start, end, and pos) are pointing.
Line 165: Now that you have finished the first implementation, you flip your mind to testing
Line 166: mode. It is time for specification and boundary testing. As an exercise, before we work
Line 167: on this problem together, look at the requirements one more time and write down all
Line 168: the test cases you can come up with. The format does not matter—it can be something
Line 169: like “all parameters null.” When you are finished with this chapter, compare your ini-
Line 170: tial test suite with the one we are about to derive together.
Line 171:  The best way to ensure that this method works properly would be to test all the pos-
Line 172: sible combinations of inputs and outputs. Given that substringsBetween() receives
Line 173: three string parameters as an input, we would need to pass all possible valid strings to
Line 174: the three parameters, combined in all imaginable ways. As we discussed in chapter 1,
Line 175: exhaustive testing is rarely possible. We have to be pragmatic.
Line 176: 2.1.1
Line 177: Step 1: Understanding the requirements, inputs, and outputs
Line 178: Regardless of how your requirements are written (or even if they are only in your
Line 179: mind), they include three parts. First is what the program/method must do: its busi-
Line 180: ness rules. Second, the program receives data as inputs. Inputs are a fundamental part
Line 181: of our reasoning, as it is through them that we can test the different cases. Third, rea-
Line 182: soning about the output will help us better understand what the program does and
Line 183: how the inputs are converted to the expected output.
Line 184: 1st iteration: axcaycazc
Line 185: pos
Line 186: open
Line 187: close
Line 188: pos (in the end of the loop)
Line 189: 2nd iteration: axcaycazc
Line 190: pos
Line 191: open
Line 192: close
Line 193: pos
Line 194: 3rd iteration: axcaycazc
Line 195: pos
Line 196: open
Line 197: close
Line 198: pos
Line 199: Figure 2.1
Line 200: The three iterations of 
Line 201: the substringsBetween method 
Line 202: for our example
Line 203: 
Line 204: --- 페이지 62 ---
Line 205: 34
Line 206: CHAPTER 2
Line 207: Specification-based testing
Line 208:  For the substringsBetween() method, my reasoning would be
Line 209: 1
Line 210: The goal of this method is to collect all substrings in a string that are delimited
Line 211: by an open tag and a close tag (the user provides these).
Line 212: 2
Line 213: The program receives three parameters:
Line 214: a
Line 215: str, which represents the string from which the program will extract sub-
Line 216: strings
Line 217: b
Line 218: The open tag, which indicates the start of a substring
Line 219: c
Line 220: The close tag, which indicates the end of the substring
Line 221: 3
Line 222: The program returns an array composed of all the substrings found by the
Line 223: program.
Line 224: Such reflection is useful to think about what you want from the method. 
Line 225: 2.1.2
Line 226: Step 2: Explore what the program does for various inputs
Line 227: An ad hoc exploration of what the method does may increase your understanding of
Line 228: it. I have noticed this when observing professional software developers writing test
Line 229: cases for methods they have never seen before (Aniche, Treude, and Zaidman, 2021).
Line 230: This step is more relevant when you did not write the code—if you wrote it, this explo-
Line 231: ration phase may not be needed.
Line 232:  To illustrate this step, suppose you did not write this code (which, in this case, is
Line 233: true). My process would be as follows (see the JUnit code in listing 2.2):
Line 234:  Let’s see the program working on a happy case. I will pass the string “abcd” with
Line 235: the open tag “a” and the close tag “d”. I expect it to return an array with a single ele-
Line 236: ment: ["bc"]. I try that (in a unit test), and the program returns what I expect.
Line 237:  Next, let’s see what happens if there are multiple substrings in the main string. I
Line 238: will pass the string “abcdabcdab” with the same open and close tags. I expect it to
Line 239: return an array with two strings: ["bc", "bc"]. The program returns what I expect.
Line 240:  I expect the program to behave the same with open and close tags larger than a
Line 241: single character. I will repeat the second test, doubling the “a”s and the “d”s in all the
Line 242: parameters. I will also change one of the “bc”s to “bf”, so it is easier to check that the
Line 243: method returns two different substrings: ["bc", "bf"]. The program returns what I
Line 244: expect.
Line 245: @Test
Line 246: void simpleCase() {   
Line 247:   assertThat(
Line 248:     StringUtils.substringsBetween("abcd", "a", "d")
Line 249:   ).isEqualTo(new String[] { "bc" });
Line 250: }
Line 251: @Test
Line 252: void manySubstrings() {   
Line 253:   assertThat(
Line 254: Listing 2.2
Line 255: Exploratory tests for substringsBetween()
Line 256: We write these test cases based on our feelings. 
Line 257: What do we want to explore next?
Line 258: I don’t care if they are good 
Line 259: tests, as long as they teach me 
Line 260: something about the code.
Line 261: 
Line 262: --- 페이지 63 ---
Line 263: 35
Line 264: The requirements say it all
Line 265:     StringUtils.substringsBetween("abcdabcdab", "a", "d")
Line 266:   ).isEqualTo(new String[] { "bc", "bc" });
Line 267: }
Line 268: @Test
Line 269: void openAndCloseTagsThatAreLongerThan1Char() {    
Line 270:   assertThat(
Line 271:     StringUtils.substringsBetween("aabcddaabfddaab", "aa", "dd")
Line 272:   ).isEqualTo(new String[] { "bc", "bf" });
Line 273: }
Line 274: I stop this exploration phase when I have a clear mental model of how the program
Line 275: should work. Note that I do not expect you to perform the same exploration I did—it
Line 276: is personal and guided by my hypothesis about the program. Also note that I did not
Line 277: explore any corner cases; that comes later. At this moment, I am only interested in
Line 278: better understanding the program. 
Line 279: 2.1.3
Line 280: Step 3: Explore possible inputs and outputs, and identify partitions
Line 281: We should find a way to prioritize and select a subset of inputs and outputs that will
Line 282: give us sufficient certainty about the correctness of the program. Although the num-
Line 283: ber of possible program inputs and outputs is nearly infinite, some sets of inputs make
Line 284: the program behave the same way, regardless of the precise input value.
Line 285:  In the case of our example, for testing purposes, the input “abcd” with open tag “a”
Line 286: and close tag “d”, which makes the program return “bc”, is the same as the input
Line 287: “xyzw” with open tag “x” and close tag “w”. You change the letters, but you expect the
Line 288: program to do the same thing for both inputs. Given your resource constraints, you
Line 289: will test just one of these inputs (it does not matter which), and you will trust that this
Line 290: single case represents that entire class of inputs. In testing terminology, we say that
Line 291: these two inputs are equivalent.
Line 292:  Once you have identified this class (or partition), you repeat the process and look
Line 293: for another class that will make the program behave in a different way that you have
Line 294: not yet tested. If you keep dividing the domain, you will eventually identify all the dif-
Line 295: ferent possible classes (or partitions) of inputs.
Line 296:  A systematic way to do such an exploration is to think of the following:
Line 297: 1
Line 298: Each input individually: “What are the possible classes of inputs I can provide?”
Line 299: 2
Line 300: Each input in combination with other inputs: “What combinations can I try
Line 301: between the open and close tags?”
Line 302: 3
Line 303: The different classes of output expected from this program: “Does it return
Line 304: arrays? Can it return an empty array? Can it return nulls?”
Line 305: I find it easiest to start with individual inputs. Follow me:
Line 306: 
Line 307: str parameter—The string can be any string. The specification mentions the
Line 308: null and empty cases; I would have tested those anyway, because they are always
Line 309: I wrote all the test code in 
Line 310: a single line, although you 
Line 311: cannot see that in the 
Line 312: printed book. Feel free to 
Line 313: write it any way you prefer.
Line 314: 
Line 315: --- 페이지 64 ---
Line 316: 36
Line 317: CHAPTER 2
Line 318: Specification-based testing
Line 319: good exceptional test cases. Given that this is a string (which is basically a list of
Line 320: characters), I will also test what happens if the string has length 1.
Line 321: a
Line 322: Null string
Line 323: b
Line 324: Empty string
Line 325: c
Line 326: String of length 1
Line 327: d
Line 328: String of length > 1 (any string)
Line 329: 
Line 330: open parameter—This can also be anything. I will try it with null and empty, as I
Line 331: learned from the str parameter that those cases are special in this program. I
Line 332: will also try strings with length 1 and greater than 1:
Line 333: a
Line 334: Null string
Line 335: b
Line 336: Empty string
Line 337: c
Line 338: String of length 1
Line 339: d
Line 340: String of length > 1
Line 341: 
Line 342: close parameter—This parameter is like the previous one:
Line 343: a
Line 344: Null string
Line 345: b
Line 346: Empty string
Line 347: c
Line 348: String of length 1
Line 349: d
Line 350: String of length > 1
Line 351: Once the input variables are analyzed in detail, we explore possible combinations of
Line 352: variables. A program’s input variables may be related to each other. In the example, it
Line 353: is clear that the three variables have a dependency relationship. Follow me again:
Line 354: 
Line 355: (str, open, close)parameters—open and close may or may not be in the string.
Line 356: Also, open may be there, but not close (and vice versa).
Line 357: a
Line 358: str contains neither the open nor the close tag.
Line 359: b
Line 360: str contains the open tag but not the close tag.
Line 361: c
Line 362: str contains the close tag but not the open tag.
Line 363: d
Line 364: str contains both the open and close tags.
Line 365: e
Line 366: str contains both the open and close tags multiple times.
Line 367: Note that this thought process depended on my experience as a tester. The documen-
Line 368: tation does not explicitly mention tags not being in the string, nor does it mention the
Line 369: open tag being present but the close tag not. I saw this case because of my experience
Line 370: as a tester.
Line 371:  Finally, we reflect on the possible outputs. The method returns an array of sub-
Line 372: strings. I can see a set of possible different outputs, both for the array itself and for the
Line 373: strings within the array:
Line 374: Array of strings (output)
Line 375: a
Line 376: Null array
Line 377: b
Line 378: Empty array
Line 379: 
Line 380: --- 페이지 65 ---
Line 381: 37
Line 382: The requirements say it all
Line 383: c
Line 384: Single item
Line 385: d
Line 386: Multiple items
Line 387: Each individual string (output)
Line 388: a
Line 389: Empty
Line 390: b
Line 391: Single character
Line 392: c
Line 393: Multiple characters
Line 394: You may think that reflecting on the outputs is not necessary. After all, if you reasoned
Line 395: correctly about the inputs, you are probably exercising all the possible kinds of out-
Line 396: puts. This is a valid argument. Nevertheless, for more complex programs, reflecting
Line 397: on the outputs may help you see an input case that you did not identify before. 
Line 398: 2.1.4
Line 399: Step 4: Analyze the boundaries
Line 400: Bugs in the boundaries of the input domain are common in software systems. As
Line 401: developers, we have all made mistakes such as using a “greater than” operator (>)
Line 402: where it should have been a “greater than or equal to” operator (>=). Programs with
Line 403: such bugs tend to work well for most provided inputs, but they fail when the input is
Line 404: near the boundary. Boundaries are everywhere, and our goal in this section is to learn
Line 405: how to identify them.
Line 406:  When we devise partitions, they have close boundaries with the other partitions. Imag-
Line 407: ine a simple program that prints “hiphip” if the given input is a number smaller than 10
Line 408: or “hooray” if the given input is greater than or equal to 10. A tester can divide the input
Line 409: domain into two partitions: (1) the set of inputs that make the program print “hiphip”
Line 410: and (2) the set of inputs that make the program print “hooray”. Figure 2.2 illustrates
Line 411: this program’s inputs and partitions. Note that the input value 9 belongs to the “hiphip”
Line 412: partition, while the input value 10 belongs to the “hooray” partition.
Line 413: The odds of a programmer writing a bug near the boundary (in this case, near the
Line 414: input values 9 and 10) are greater than for other input values. This is what boundary
Line 415: testing is about: making the program behave correctly when inputs are near a bound-
Line 416: ary. And this is what this fourth step is about: boundary testing.
Line 417: hooray
Line 418: hiphip
Line 419: 1
Line 420: 1
Line 421: 2 3 4 5 6 7 8 9 10 11 12
Line 422: 3 14 15 …
Line 423: Boundary
Line 424: When we cross this boundary, the program
Line 425: suddenly changes its behavior completely.
Line 426: We want to make sure this works perfectly!
Line 427: Figure 2.2
Line 428: The boundary between the 
Line 429: “hiphip” and “hooray” partitions. Numbers 
Line 430: up to 9 belong to the “hiphip” partition, 
Line 431: and numbers greater than 9 belong to the 
Line 432: “hooray” partition.
Line 433: 
Line 434: --- 페이지 66 ---
Line 435: 38
Line 436: CHAPTER 2
Line 437: Specification-based testing
Line 438:  Whenever a boundary is identified, I suggest that you test what happens to the pro-
Line 439: gram when inputs go from one boundary to the other. In the previous example, this
Line 440: would mean having a test with 9 as input and another test with 10 as input. This idea is
Line 441: similar to what Jeng and Weyuker proposed in their 1994 paper: testing two points
Line 442: whenever there is a boundary. One test is for the on point, which is the point that is on
Line 443: the boundary; and the other test is for the off point, which is the point closest to the
Line 444: boundary that belongs to the partition the on point does not belong to (that is, the
Line 445: other partition).
Line 446:  In the hiphip-hooray example, the on point is 10. Note that 10 is the number that
Line 447: appears in the specification of the program (input >= 10) and is likely to also be the
Line 448: number the developer uses in the if statement. The value 10 makes the program
Line 449: print “hooray”. The off point is the point closest to the boundary that belongs to the
Line 450: other partition. In this case, the off point is 9. The number 9 is the closest number to
Line 451: 10, and it belongs to the “hiphip” partition.
Line 452:  Let’s discuss two more common terms: in point and out point. In points are points
Line 453: that make the condition true. You may have an infinite number of them. In the
Line 454: hiphip-hooray example, 11, 12, 25, and 42 are all examples of in points. Out points,
Line 455: on the other hand, are points that make the condition false. 8, 7, 2, and –42 are all
Line 456: examples of out points. In equalities, the in point is the one in the condition, and all
Line 457: others are out points. For example, in a == 10, 10 is the (only) in point and the on
Line 458: point; 12 is an out point and an off point; and 56 is an out point. Whenever you find a
Line 459: boundary, two tests (for the on and off points) are usually enough, although, as I will
Line 460: discuss later, I do not mind throwing in some interesting in and out points to have a
Line 461: more complete test suite.
Line 462:  Another common situation in boundary testing is finding boundaries that deal
Line 463: with equalities. In the previous example, suppose that instead of input >= 10, the spec-
Line 464: ification says that the program prints “hooray” whenever the input is 10 or “hiphip”
Line 465: otherwise. Given that this is an equality, we now have one on point (10) but two off
Line 466: points (9 and 11), because the boundary applies to both sides. In this case, as a tester,
Line 467: you would write three test cases.
Line 468:  My trick to explore boundaries is to look at all the partitions and think of inputs
Line 469: between them. Whenever you find one that is worth testing, you test it.
Line 470:  In our example, a straightforward boundary happens when the string passes from
Line 471: empty to non-empty, as you know that the program stops returning empty and will
Line 472: (possibly) start to return something. You already covered this boundary, as you have
Line 473: partitions for both cases. As you examine each partition and how it makes boundaries
Line 474: with others, you analyze the partitions in the (str, open, close) category. The pro-
Line 475: gram can have no substrings, one substring, or multiple substrings. And the open and
Line 476: close tags may not be in the string; or, more importantly, they may be in the string,
Line 477: but with no substring between them. This is a boundary you should exercise! See fig-
Line 478: ure 2.3.
Line 479: 
Line 480: --- 페이지 67 ---
Line 481: 39
Line 482: The requirements say it all
Line 483: Whenever we identify a boundary, we devise two tests for it, one for each side of the
Line 484: boundary. For the “no substring”/“one substring” boundary, the two tests are as follows:
Line 485: 
Line 486: str contains both open and close tags, with no characters between them.
Line 487: 
Line 488: str contains both open and close tags, with characters between them.
Line 489: The second test is not necessary in this case, as other tests already exercise this situa-
Line 490: tion. Therefore, we can discard it. 
Line 491: 2.1.5
Line 492: Step 5: Devise test cases
Line 493: With the inputs, outputs, and boundaries properly dissected, we can generate con-
Line 494: crete test cases. Ideally, we would combine all the partitions we’ve devised for each of
Line 495: the inputs. The example has four categories, each with four or five partitions: the str
Line 496: category with four partitions (null string, empty string, string of length 1, and string of
Line 497: length > 1), the open category with four partitions (the same as str), the close cate-
Line 498: gory with four partitions (also the same as str), and the (str, open, close) category
Line 499: with five partitions (string does not contain either the open or close tags, string contains the
Line 500: open tag but does not contain the close tag, string contains the close tag but does not contain
Line 501: the open tag, string contains both the open and close tags, string contains both the open and
Line 502: close tags multiple times). This means you would start with the str null partition and
Line 503: combine it with the partitions of the open, close, and (str, open, close) categories.
Line 504: You would end up with 4 × 4 × 4 × 5 = 320 tests. Writing 320 tests may be an effort that
Line 505: will not pay off.
Line 506:  In such situations, we pragmatically decide which partitions should be combined
Line 507: with others and which should not. A first idea to reduce the number of tests is to test
Line 508: exceptional cases only once and not combine them. For example, the null string parti-
Line 509: tion may be tested only once and not more than that. What would we gain from com-
Line 510: bining null string with open being null, empty, length = 1, and length > 1 as well as
Line 511: with close being null, empty, length = 1, length > 1, and so on? It would not be
Line 512: worth the effort. The same goes for empty string: one test may be good enough. If we
Line 513: When the input contains both the “open” and “close” tags, and the length
Line 514: of the substring changes from 0 to greater than 0, the program starts to
Line 515: return this substring. It’s a boundary, and we should exercise it!
Line 516: One substring
Line 517: len(substring)
Line 518: len = 0
Line 519: len > 0
Line 520: No
Line 521: substring
Line 522: Figure 2.3
Line 523: Some of the boundaries in the substringsBetween() problem.
Line 524: 
Line 525: --- 페이지 68 ---
Line 526: 40
Line 527: CHAPTER 2
Line 528: Specification-based testing
Line 529: apply the same logic to the other two parameters and test them as null and empty just
Line 530: once, we already drastically reduce the number of test cases.
Line 531:  There may be other partitions that do not need to be combined fully. In this prob-
Line 532: lem, I see two:
Line 533: For the string of length 1 case, given that the string has length 1, two tests may be
Line 534: enough: one where the single character in the string matches open and close,
Line 535: and one where it does not.
Line 536: Unless we have a good reason to believe that the program handles open and
Line 537: close tags of different lengths in different ways, we do not need the four combi-
Line 538: nations of (open length = 1, close length = 1), (open length > 1, close length = 1), (open
Line 539: length = 1, close length > 1), and (open length > 1, close length > 1). Just (open length = 1,
Line 540: close length = 1) and (open length > 1, close length > 1) are enough.
Line 541: In other words, do not blindly combine partitions, as doing so may lead to less rele-
Line 542: vant test cases. Looking at the implementation can also help you reduce the number
Line 543: of combinations. We discuss using the source code to design test cases in chapter 3.
Line 544:  In the following list, I’ve marked with an [x] partitions we will not test multiple
Line 545: times:
Line 546: 
Line 547: str—Null string [x], empty string [x], length = 1 [x], length > 1
Line 548: 
Line 549: open—Null string [x], empty string [x], length = 1, length > 1
Line 550: 
Line 551: close—Null string [x], empty string [x], length = 1, length > 1
Line 552: 
Line 553: str—Null string [x], empty string [x], length = 1, length > 1
Line 554: (str, open, close)—String does not contain either the open or the close tag,
Line 555: string contains the open tag but does not contain the close tag, string contains
Line 556: the close tag but does not contain the open tag, string contains both the open
Line 557: and close tags, string contains both the open and close tags multiple times
Line 558: With a clear understanding of which partitions need to be extensively tested and
Line 559: which ones do not, we can derive the test cases by performing the combination. First,
Line 560: the exceptional cases:
Line 561: T1: str is null.
Line 562: T2: str is empty.
Line 563: T3: open is null.
Line 564: T4: open is empty.
Line 565: T5: close is null.
Line 566: T6: close is empty.
Line 567: Then, str length = 1:
Line 568: T7: The single character in str matches the open tag.
Line 569: T8: The single character in str matches the close tag.
Line 570: T9: The single character in str does not match either the open or the close tag.
Line 571: T10: The single character in str matches both the open and close tags.
Line 572: 
Line 573: --- 페이지 69 ---
Line 574: 41
Line 575: The requirements say it all
Line 576: Now, str length > 1, open length = 1, close = 1:
Line 577: T11: str does not contain either the open or the close tag.
Line 578: T12: str contains the open tag but does not contain the close tag.
Line 579: T13: str contains the close tag but does not contain the open tag.
Line 580: T14: str contains both the open and close tags.
Line 581: T15: str contains both the open and close tags multiple times.
Line 582: Next, str length > 1, open length > 1, close > 1:
Line 583: T16: str does not contain either the open or the close tag.
Line 584: T17: str contains the open tag but does not contain the close tag.
Line 585: T18: str contains the close tag but does not contain the open tag.
Line 586: T19: str contains both the open and close tags.
Line 587: T20: str contains both the open and close tags multiple times.
Line 588: Finally, here is the test for the boundary:
Line 589: T21: str contains both the open and close tags with no characters between
Line 590: them.
Line 591: We end up with 21 tests. Note that deriving them did not require much creativity: the
Line 592: process we followed was systematic. This is the idea!
Line 593: 2.1.6
Line 594: Step 6: Automate the test cases
Line 595: It is now time to transform the test cases into automated JUnit tests. Writing those tests
Line 596: is mostly a mechanical task. The creative part is coming up with inputs to exercise the
Line 597: specific partition and understanding the correct program output for that partition.
Line 598:  The automated test suite is shown in listings 2.3 through 2.7. They are long but
Line 599: easy to understand. Each call to the substringsBetween method is one of our test
Line 600: cases. The 21 calls to it are spread over the test methods, each matching the test cases
Line 601: we devised earlier.
Line 602:  First are the tests related to the string being null or empty.
Line 603: import org.junit.jupiter.api.Test;
Line 604: import static ch2.StringUtils.substringsBetween;
Line 605: import static org.assertj.core.api.Assertions.assertThat;
Line 606: public class StringUtilsTest {
Line 607:   @Test
Line 608:   void strIsNullOrEmpty() {
Line 609:     assertThat(substringsBetween(null, "a", "b"))     
Line 610:       .isEqualTo(null);
Line 611: Listing 2.3
Line 612: Tests for substringsBetween, part 1
Line 613: This first call to 
Line 614: substringsBetween 
Line 615: is our test T1.
Line 616: 
Line 617: --- 페이지 70 ---
Line 618: 42
Line 619: CHAPTER 2
Line 620: Specification-based testing
Line 621:     assertThat(substringsBetween("", "a", "b"))  
Line 622:       .isEqualTo(new String[]{});
Line 623:   }
Line 624: }
Line 625: Next are all the tests related to open or close being null or empty.
Line 626:   @Test
Line 627:   void openIsNullOrEmpty() {
Line 628:     assertThat(substringsBetween("abc", null, "b")).isEqualTo(null);
Line 629:     assertThat(substringsBetween("abc", "", "b")).isEqualTo(null);
Line 630:   }
Line 631:   @Test
Line 632:   void closeIsNullOrEmpty() {
Line 633:     assertThat(substringsBetween("abc", "a", null)).isEqualTo(null);
Line 634:     assertThat(substringsBetween("abc", "a", "")).isEqualTo(null);
Line 635:   }
Line 636: Now come all the tests related to string and open and close tags with length 1.
Line 637:   @Test
Line 638:   void strOfLength1() {
Line 639:     assertThat(substringsBetween("a", "a", "b")).isEqualTo(null);
Line 640:     assertThat(substringsBetween("a", "b", "a")).isEqualTo(null);
Line 641:     assertThat(substringsBetween("a", "b", "b")).isEqualTo(null);
Line 642:     assertThat(substringsBetween("a", "a", "a")).isEqualTo(null);
Line 643:   }
Line 644:   @Test
Line 645:   void openAndCloseOfLength1() {
Line 646:     assertThat(substringsBetween("abc", "x", "y")).isEqualTo(null);
Line 647:     assertThat(substringsBetween("abc", "a", "y")).isEqualTo(null);
Line 648:     assertThat(substringsBetween("abc", "x", "c")).isEqualTo(null);
Line 649:     assertThat(substringsBetween("abc", "a", "c"))
Line 650:       .isEqualTo(new String[] {"b"});
Line 651:     assertThat(substringsBetween("abcabc", "a", "c"))
Line 652:       .isEqualTo(new String[] {"b", "b"});
Line 653:   }
Line 654: Then we have the tests for the open and close tags of varying sizes.
Line 655:   @Test
Line 656:   void openAndCloseTagsOfDifferentSizes() {
Line 657:     assertThat(substringsBetween("aabcc", "xx", "yy")).isEqualTo(null);  
Line 658:     assertThat(substringsBetween("aabcc", "aa", "yy")).isEqualTo(null);
Line 659: Listing 2.4
Line 660: Tests for substringsBetween, part 2
Line 661: Listing 2.5
Line 662: Tests for substringsBetween, part 3
Line 663: Listing 2.6
Line 664: Tests for substringsBetween, part 4
Line 665: Test T2
Line 666: 
Line 667: --- 페이지 71 ---
Line 668: 43
Line 669: The requirements say it all
Line 670:     assertThat(substringsBetween("aabcc", "xx", "cc")).isEqualTo(null);
Line 671:     assertThat(substringsBetween("aabbcc", "aa", "cc"))
Line 672:       .isEqualTo(new String[] {"bb"});
Line 673:     assertThat(substringsBetween("aabbccaaeecc", "aa", "cc"))
Line 674:       .isEqualTo(new String[] {"bb", "ee"});
Line 675:   }
Line 676: Finally, here is the test for when there is no substring between the open and close tags.
Line 677: @Test
Line 678: void noSubstringBetweenOpenAndCloseTags() {
Line 679:   assertThat(substringsBetween("aabb", "aa", "bb"))
Line 680:     .isEqualTo(new String[] {""});
Line 681:   }
Line 682: }
Line 683: I decided to group the assertions in five different methods. They almost match my
Line 684: groups when engineering the test cases in step 5. The only difference is that I broke
Line 685: the exceptional cases into three test methods: strIsNullOrEmpty, openIsNullOr-
Line 686: Empty, and closeIsNullOrEmpty.
Line 687:  Some developers would vouch for a single method per test case, which would
Line 688: mean 21 test methods, each containing one method call and one assertion. The
Line 689: advantage would be that the test method’s name would clearly describe the test case.
Line 690: JUnit also offers the ParameterizedTest feature (http://mng.bz/voKp), which could
Line 691: be used in this case.
Line 692:  I prefer simple test methods that focus on one test case, especially when imple-
Line 693: menting complex business rules in enterprise systems. But in this case, there are lots
Line 694: of inputs to test, and many of them are variants of a larger partition, so it made more
Line 695: sense to me to code the way I did.
Line 696:  Deciding whether to put all tests in a single method or in multiple methods is
Line 697: highly subjective. We discuss test code quality and how to write tests that are easy to
Line 698: understand and debug in chapter 10.
Line 699:  Also note that sometimes there are values we do not care about. For example, con-
Line 700: sider test case 1: str is null. We do not care about the values we pass to the open and
Line 701: close tags here. My usual approach is to select reasonable values for the inputs I do
Line 702: not care about—that is, values that will not interfere with the test. 
Line 703: 2.1.7
Line 704: Step 7: Augment the test suite with creativity and experience
Line 705: Being systematic is good, but we should never discard our experience. In this step, we
Line 706: look at the partitions we’ve devised and see if we can develop interesting variations.
Line 707: Variation is always a good thing to have in testing.
Line 708:  In the example, when revisiting the tests, I noticed that we never tried strings with
Line 709: spaces. I decided to engineer two extra tests based on T15 and T20, both about “str
Line 710: contains both open and close tags multiple times”: one for open and close tags with
Line 711: Listing 2.7
Line 712: Tests for substringsBetween, part 5
Line 713: 
Line 714: --- 페이지 72 ---
Line 715: 44
Line 716: CHAPTER 2
Line 717: Specification-based testing
Line 718: lengths 1, another for open and close tags with larger lengths. These check whether
Line 719: the implementation works if there are whitespaces in the string. You see them in list-
Line 720: ing 2.8.
Line 721: NOTE
Line 722: It’s possible we don’t need to test for this extra case. Maybe the imple-
Line 723: mentation handles strings in a generic way. For now, we are only looking at
Line 724: the requirements, and testing special characters is always a good idea. If you
Line 725: have access to the implementation (as we discuss in the next chapter), the
Line 726: code can help you decide whether a test is relevant.
Line 727: @Test
Line 728: void openAndCloseOfLength1() {
Line 729:   // ... previous assertions here
Line 730:   assertThat(substringsBetween("abcabyt byrc", "a", "c"))
Line 731:     .isEqualTo(new String[] {"b", "byt byr"});
Line 732: }
Line 733: @Test
Line 734: void openAndCloseTagsOfDifferentSizes() {
Line 735:   // ... previous assertions here
Line 736:   assertThat(substringsBetween("a abb ddc ca abbcc", "a a", "c c")).
Line 737:   ➥ isEqualTo(new String[] {"bb dd"});
Line 738: }
Line 739: We end up with 23 test cases. Take time to revisit all the steps we have worked through,
Line 740: and then consider this question: are we finished?
Line 741:  We are finished with specification testing. However, we are not done testing. After
Line 742: specification testing, the next step is to bring the implementation into play and aug-
Line 743: ment our test suite with what we see in the code. That is the topic of chapter 3.
Line 744: Listing 2.8
Line 745: Tests for substringsBetween using parameterized tests, part 6
Line 746: Four eyes are better than two
Line 747: A reviewer of this book had an interesting question: what about a test case where the
Line 748: input is aabcddaabeddaab, open is aa, and close is d? “bc” and “be” are the sub-
Line 749: strings between the provided open and the close tags (aa<bc>ddaa<be>ddaab), but
Line 750: “bcddaabed” could also be considered a substring (aa<bcddaabed>daab).
Line 751: At first, I thought I had missed this test case. But in fact, it is the same as T15 and T20.
Line 752: Different people approach problems in different ways. My thought process was,
Line 753: “Let’s see if the program breaks if we have multiple open and close tags in the
Line 754: string.” The reviewer may have thought, “Let’s see if the program will incorrectly go
Line 755: for the longer substring.”
Line 756: We want to make testing as systematic as possible, but a lot depends on how the
Line 757: developer models the problem. Sometimes you will not see all the test cases. When
Line 758: you do come up with a new test, add it to the test suite!
Line 759: 
Line 760: --- 페이지 73 ---
Line 761: 45
Line 762: Specification-based testing in a nutshell
Line 763: 2.2
Line 764: Specification-based testing in a nutshell
Line 765: I propose a seven-step approach to derive systematic tests based on a specification.
Line 766: This approach is a mix of the category-partition method proposed by Ostrand and Balcer
Line 767: in their seminal 1988 work, and Kaner et al.’s Domain Testing Workbook (2013), with my
Line 768: own twist: see figure 2.4.
Line 769: The steps are as follows:
Line 770: 1
Line 771: Understand the requirement, inputs, and outputs. We need an overall idea of what
Line 772: we are about to test. Read the requirements carefully. What should the program
Line 773: do? What should it not do? Does it handle specific corner cases? Identify the
Line 774: input and output variables in play, their types (integers, strings, and so on),
Line 775: and their input domain (for example, is the variable a number that must be
Line 776: between 5 and 10?). Some of these characteristics can be found in the pro-
Line 777: gram’s specification; others may not be stated explicitly. Try to understand the
Line 778: nitty-gritty details of the requirements.
Line 779: 2
Line 780: Explore the program. If you did not write the program yourself, a very good way to
Line 781: determine what it does (besides reading the documentation) is to play with it.
Line 782: Call the program under test with different inputs and see what it produces as
Line 783: output. Continue until you are sure your mental model matches what the pro-
Line 784: gram does. This exploration does not have to be (and should not be) system-
Line 785: atic. Rather, focus on increasing your understanding. Remember that you are
Line 786: still not testing the program.
Line 787: 3
Line 788: Judiciously explore the possible inputs and outputs, and identify the partitions. Identify-
Line 789: ing the correct partitions is the hardest part of testing. If you miss one, you may
Line 790: let a bug slip through. I propose three steps to identify the partitions:
Line 791: a
Line 792: Look at each input variable individually. Explore its type (is it an integer? is it
Line 793: a string?) and the range of values it can receive (can it be null? is it a number
Line 794: ranging from 0 to 100? does it allow negative numbers?).
Line 795: b
Line 796: Look at how each variable may interact with another. Variables often have
Line 797: dependencies or put constraints on each other, and those should be tested.
Line 798: Understand the
Line 799: requirement.
Line 800: Explore the
Line 801: program.
Line 802: Identify the
Line 803: partitions.
Line 804: Analyze the
Line 805: boundaries.
Line 806: Devise test
Line 807: cases.
Line 808: Automate test
Line 809: cases.
Line 810: Augment
Line 811: (creativity and
Line 812: experience).
Line 813: Figure 2.4
Line 814: The seven steps I propose to derive test cases based on specifications. The solid 
Line 815: arrows indicate the standard path to follow. The dashed arrows indicate that, as always, the 
Line 816: process should be iterative, so in practice you’ll go back and forth until you are confident about the 
Line 817: test suite you’ve created.
Line 818: 
Line 819: --- 페이지 74 ---
Line 820: 46
Line 821: CHAPTER 2
Line 822: Specification-based testing
Line 823: c
Line 824: Explore the possible types of outputs, and make sure you are testing them
Line 825: all. While exploring the inputs and outputs, pay attention to any implicit
Line 826: (business) rules, logic, or expected behavior.
Line 827: 4
Line 828: Identify the boundaries. Bugs love boundaries, so be extra thorough here. Analyze
Line 829: the boundaries of all the partitions you devised in the previous step. Identify
Line 830: the relevant ones, and add them to the list.
Line 831: 5
Line 832: Devise test cases based on the partitions and boundaries. The basic idea is to combine
Line 833: all the partitions in the different categories to test all possible combinations of
Line 834: inputs. However, combining them all may be too expensive, so part of the task is
Line 835: to reduce the number of combinations. The common strategy is to test excep-
Line 836: tional behavior only once and not combine it with the other partitions.
Line 837: 6
Line 838: Automate the test cases. A test is only a test when it is automated. Therefore, the
Line 839: goal is to write (JUnit) automated tests for all the test cases you just devised.
Line 840: This means identifying concrete input values for them and having a clear
Line 841: expectation of what the program should do (the output). Remember that test
Line 842: code is code, so reduce duplication and ensure that the code is easy to read and
Line 843: that the different test cases are easily identifiable in case one fails.
Line 844: 7
Line 845: Augment the test suite with creativity and experience. Perform some final checks.
Line 846: Revisit all the tests you created, using your experience and creativity. Did you
Line 847: miss something? Does your gut feeling tell you that the program may fail in a
Line 848: specific case? If so, add a new test case. 
Line 849: 2.3
Line 850: Finding bugs with specification testing
Line 851: The developers of the Apache Commons Lang framework (the framework where I
Line 852: extracted the implementation of the substringsBetween method) are just too good.
Line 853: We did not find any bugs there. Let’s look at another example: one implemented by
Line 854: me, an average developer who makes mistakes from time to time. This example will
Line 855: show you the value of specification testing. Try to spot the bug before I reveal it!
Line 856:  Some friends and I have participated in many coding challenges, primarily for fun.
Line 857: A couple of years ago we worked on the following problem inspired by LeetCode
Line 858: (https://leetcode.com/problems/add-two-numbers):
Line 859: The method receives two numbers, left and right (each represented as a list
Line 860: of digits), adds them, and returns the result as a list of digits.
Line 861: Each element in the left and right lists of digits should be a number from
Line 862: [0–9]. An IllegalArgumentException is thrown if this pre-condition does
Line 863: not hold.
Line 864: 
Line 865: left—A list containing the left number. Null returns null; empty means 0.
Line 866: 
Line 867: right—A list containing the right number. Null returns null; empty
Line 868: means 0.
Line 869: The program returns the sum of left and right as a list of digits.
Line 870: 
Line 871: --- 페이지 75 ---
Line 872: 47
Line 873: Finding bugs with specification testing
Line 874: For example, adding the numbers 23 and 42 means a (left) list with two elements
Line 875: [2,3], a (right) list with two elements [4,2] and, as an output, a list with two elements
Line 876: [6,5] (since 23 + 42 = 65).
Line 877:  My initial implementation was as follows.
Line 878: public List<Integer> add(List<Integer> left, List<Integer> right) {
Line 879:   if (left == null || right == null)   
Line 880:     return null;
Line 881:   Collections.reverse(left);   
Line 882:   Collections.reverse(right);
Line 883:   LinkedList<Integer> result = new LinkedList<>();
Line 884:   int carry = 0;
Line 885:   for (int i = 0; i < max(left.size(), right.size()); i++) {  
Line 886:     int leftDigit = left.size() > i ? left.get(i) : 0;
Line 887:     int rightDigit = right.size() > i ? right.get(i) : 0;
Line 888:     if (leftDigit < 0 || leftDigit > 9 ||
Line 889:      rightDigit < 0 || rightDigit > 9)    
Line 890:       throw new IllegalArgumentException();
Line 891:     int sum = leftDigit + rightDigit + carry;   
Line 892:     result.addFirst(sum % 10);   
Line 893:     carry = sum / 10;   
Line 894:   }
Line 895:   return result;
Line 896: }
Line 897: The algorithm works as follows. First it reverses both lists of digits, so the least signifi-
Line 898: cant digit is on the left. This makes it easier for us to loop through the list. Then, for
Line 899: each digit in both the left and right numbers, the algorithm gets the next relevant
Line 900: digits and sums them. If the resulting sum is greater than 10, +1 needs to be carried to
Line 901: the next most significant digit. In the end, the algorithm returns the list.
Line 902:  I was just having fun with coding, so I did not write systematic tests. I tried a couple
Line 903: of inputs and observed that the output was correct. If you already understand the con-
Line 904: cept of code coverage, these four tests achieve 100% branch coverage if we discard the
Line 905: ifs related to checking null and pre-conditions (if you are not familiar with code cov-
Line 906: erage, don’t worry; we discuss it in the next chapter):
Line 907: T1 = [1] + [1] = [2]
Line 908: T2 = [1,5] + [1,0] = [2,5]
Line 909: Listing 2.9
Line 910: Initial implementation of the add() method
Line 911: Returns null if left 
Line 912: or right is null
Line 913: Reverses the numbers so the least 
Line 914: significant digit is on the left
Line 915: While there 
Line 916: is a digit, keeps 
Line 917: summing, taking 
Line 918: carries into 
Line 919: consideration
Line 920: Throws an exception 
Line 921: if the pre-condition 
Line 922: does not hold
Line 923: Sums the left digit with 
Line 924: the right digit with the 
Line 925: possible carry
Line 926: The digit should be a number between 0 and 
Line 927: 9. We calculate it by taking the rest of the 
Line 928: division (the % operator) of the sum by 10.
Line 929: If the sum is greater than 10, carries the 
Line 930: rest of the division to the next digit
Line 931: 
Line 932: --- 페이지 76 ---
Line 933: 48
Line 934: CHAPTER 2
Line 935: Specification-based testing
Line 936: T3 = [1,5] + [1,5] = [3,0]
Line 937: T4 = [5,0,0] + [2,5,0] = [7,5,0]
Line 938: The program worked fine for these inputs. I submitted it to the coding challenge plat-
Line 939: form, and, to my surprise, the implementation was rejected! There was a bug in my code.
Line 940: Before I show you where it is, here is how specification testing would have caught it.
Line 941:  First we analyze each parameter in isolation:
Line 942: 
Line 943: left parameter—It is a list, so we should first exercise basic inputs such as null,
Line 944: empty, a single digit, and multiple digits. Given that this list represents a num-
Line 945: ber, we should also try a number with many zeroes on the left. Such zeroes are
Line 946: useless, but it is good to see whether the implementation can handle them.
Line 947: Thus we have the following partitions:
Line 948: – Empty
Line 949: – Null
Line 950: – Single digit
Line 951: – Multiple digits
Line 952: – Zeroes on the left
Line 953: 
Line 954: right parameter—We have the same list of partitions as for the left parameter:
Line 955: – Empty
Line 956: – Null
Line 957: – Single digit
Line 958: – Multiple digits
Line 959: – Zeroes on the left
Line 960: left and right have a relationship. Let’s explore that:
Line 961: (left, right) parameters—They can be different sizes, and the program should
Line 962: be able to handle it:
Line 963: – length(left list) > length(right list)
Line 964: – length(left list) < length(right list)
Line 965: – length(left list) = length(right list)
Line 966: While not explicit in the documentation, we know that the sum of two numbers
Line 967: should be the same regardless of whether the highest number is on the left or right
Line 968: side of the equation. We also know that some sums require carrying. For example,
Line 969: suppose we’re summing 18 + 15: 8 + 5 = 13, which means we have a 3, and we carry +1
Line 970: to the next digit. We then add 1 + 1 + 1: the first 1 from the left number, the second
Line 971: 1 from the right number, and the third 1 carried from the previous sum. The final
Line 972: result is 33. Figure 2.5 illustrates this process.
Line 973: +1
Line 974: 1
Line 975: 1
Line 976: +
Line 977: + carry = 3
Line 978: 8 + 5 = 3
Line 979: 1
Line 980: 3
Line 981: 3 3
Line 982: 1 8
Line 983: 1 5
Line 984: +
Line 985: Figure 2.5
Line 986: Illustrating the carry 
Line 987: when summing 18 + 15
Line 988: 
Line 989: --- 페이지 77 ---
Line 990: 49
Line 991: Finding bugs with specification testing
Line 992: The carry is such an important concept in this program that it deserves testing. This is
Line 993: what I meant in listing 2.9 when I said to pay extra attention to specific (business)
Line 994: rules and logic:
Line 995: Carry—Let’s try sums that require carrying in many different ways. These are
Line 996: good places to start:
Line 997: – Sum without a carry
Line 998: – Sum with a carry: one carry at the beginning
Line 999: – Sum with a carry: one carry in the middle
Line 1000: – Sum with a carry: many carries
Line 1001: – Sum with a carry: many carries, not in a row
Line 1002: – Sum with a carry: carry propagated to a new (most significant) digit
Line 1003: The only boundary worth testing is the following: ensuring that cases such as 99 + 1
Line 1004: (where the final number is carried to a new, most significant digit) are covered. This
Line 1005: comes from the last partition derived when analyzing the carry: “Sum with a carry:
Line 1006: carry propagated to a new (most significant) digit.”
Line 1007:  With all the inputs and outputs analyzed, it is time to derive concrete test cases.
Line 1008: Let’s apply the following strategy:
Line 1009: 1
Line 1010: Test nulls and empties just once.
Line 1011: 2
Line 1012: Test numbers with single digits just once.
Line 1013: 3
Line 1014: Test numbers with multiple digits, with left and right having the same and
Line 1015: different lengths. We will be thorough and have the same set of tests for both
Line 1016: equal and different lengths, and we will duplicate the test suite to ensure that
Line 1017: everything works if left is longer than right or vice versa.
Line 1018: 4
Line 1019: We will exercise the zeroes on the left, but a few test cases are enough.
Line 1020: 5
Line 1021: Test the boundary.
Line 1022: Domain knowledge is still fundamental to engineer good test cases
Line 1023: Up to this point, this chapter may have given you the impression that if you analyze
Line 1024: every parameter of the method, you can derive all the test cases you need. Life would
Line 1025: be much easier if that were true!
Line 1026: Analyzing parameters, even without much domain knowledge, will help you uncover
Line 1027: many bugs. However, having a deep understanding of the requirements is still key in
Line 1028: devising good test cases. In the current example, the requirements do not discuss
Line 1029: the carry. We devised many tests around the carry because we have a deep knowl-
Line 1030: edge of the problem. We build up knowledge over time; so although the systematic
Line 1031: approaches I discuss will help you uncover many common bugs, it is your job to learn
Line 1032: about the domain of the software system you’re working on. (And if you wrote the
Line 1033: code, you have an advantage: you know it deeply!)
Line 1034: 
Line 1035: --- 페이지 78 ---
Line 1036: 50
Line 1037: CHAPTER 2
Line 1038: Specification-based testing
Line 1039: Let’s look at the specific test cases:
Line 1040: Nulls and empties
Line 1041: – T1: left null
Line 1042: – T2: left empty
Line 1043: – T3: right null
Line 1044: – T4: right empty
Line 1045: Single digits
Line 1046: – T5: single digit, no carry
Line 1047: – T6: single digit, carry
Line 1048: Multiple digits
Line 1049: – T7: no carry
Line 1050: – T8: carry in the least significant digit
Line 1051: – T9: carry in the middle
Line 1052: – T10: many carries
Line 1053: – T11: many carries, not in a row
Line 1054: – T12: carry propagated to a new (now most significant) digit
Line 1055: Multiple digits with different lengths (one for left longer than right, and one
Line 1056: for right longer than left)
Line 1057: – T13: no carry
Line 1058: – T14: carry in the least significant digit
Line 1059: – T15: carry in the middle
Line 1060: – T16: many carries
Line 1061: – T17: many carries, not in a row
Line 1062: – T18: carry propagated to a new (now most significant) digit
Line 1063: Zeroes on the left
Line 1064: – T19: no carry
Line 1065: – T20: carry
Line 1066: Boundaries
Line 1067: – T21: carry to a new most significant digit, by one (such as 99 +1 ).
Line 1068: Now we transform them into automated test cases, as shown in listing 2.10. A few
Line 1069: remarks about this listing:
Line 1070: This test uses the ParameterizedTest feature from JUnit. The idea is that we
Line 1071: write a single generic test method that works like a skeleton. Instead of having
Line 1072: hard-coded values, it uses variables. The concrete values are passed to the test
Line 1073: method later. The testCases() method provides inputs to the shouldReturn-
Line 1074: CorrectResult test method. The link between the test method and the method
Line 1075: source is done through the @MethodSource annotation. JUnit offers other ways
Line 1076: to provide inputs to methods, such as inline comma-separated values (see the
Line 1077: @CsvSource annotation in the documentation).
Line 1078: 
Line 1079: --- 페이지 79 ---
Line 1080: 51
Line 1081: Finding bugs with specification testing
Line 1082: The numbers() helper method receives a list of integers and converts it to a
Line 1083: List<Integer>, which the method under test receives. This helper method
Line 1084: increases the legibility of the test methods. (For the Java experts, the Arrays
Line 1085: .asList() native method would have yielded the same result.)
Line 1086: import org.junit.jupiter.params.ParameterizedTest;
Line 1087: import org.junit.jupiter.params.provider.Arguments;
Line 1088: import org.junit.jupiter.params.provider.MethodSource;
Line 1089: import java.util.ArrayList;
Line 1090: import java.util.List;
Line 1091: import java.util.stream.Stream;
Line 1092: import static org.assertj.core.api.Assertions.assertThat;
Line 1093: import static org.assertj.core.api.Assertions.assertThatThrownBy;
Line 1094: import static org.junit.jupiter.params.provider.Arguments.of;
Line 1095: public class NumberUtilsTest {
Line 1096:  @ParameterizedTest          
Line 1097:  @MethodSource("testCases")                          
Line 1098:  void shouldReturnCorrectResult(List<Integer> left,
Line 1099:   List<Integer> right, List<Integer> expected) {
Line 1100:    assertThat(new NumberUtils().add(left, right))   
Line 1101:        .isEqualTo(expected);
Line 1102:  }
Line 1103:  static Stream<Arguments> testCases() {     
Line 1104:    return Stream.of(
Line 1105:      of(null, numbers(7,2), null), // T1                
Line 1106:      of(numbers(), numbers(7,2), numbers(7,2)), // T2   
Line 1107:      of(numbers(9,8), null, null), // T3                
Line 1108:      of(numbers(9,8), numbers(), numbers(9,8 )), // T4  
Line 1109:      of(numbers(1), numbers(2), numbers(3)), // T5     
Line 1110:      of(numbers(9), numbers(2), numbers(1,1)), // T6   
Line 1111:      of(numbers(2,2), numbers(3,3), numbers(5,5)), // T7          
Line 1112:      of(numbers(2,9), numbers(2,3), numbers(5,2)), // T8          
Line 1113:      of(numbers(2,9,3), numbers(1,8,3), numbers(4,7,6)), // T9    
Line 1114:      of(numbers(1,7,9), numbers(2,6,8), numbers(4,4,7)), // T10   
Line 1115:      of(numbers(1,9,1,7,1), numbers(1,8,1,6,1),
Line 1116:        numbers(3,7,3,3,2)), // T11                                
Line 1117:      of(numbers(9,9,8), numbers(1,7,2), numbers(1,1,7,0)), // T12 
Line 1118:      of(numbers(2,2), numbers(3), numbers(2,5)), // T13.1          
Line 1119:      of(numbers(3), numbers(2,2), numbers(2,5)), // T13.2          
Line 1120:      of(numbers(2,2), numbers(9), numbers(3,1)), // T14.1          
Line 1121:      of(numbers(9), numbers(2,2), numbers(3,1)), // T14.2          
Line 1122:      of(numbers(1,7,3), numbers(9,2), numbers(2,6,5)), // T15.1    
Line 1123:      of(numbers(9,2), numbers(1,7,3), numbers(2,6,5)), // T15.2    
Line 1124: Listing 2.10
Line 1125: Tests for the add method
Line 1126: A parameterized test is 
Line 1127: a perfect fit for these 
Line 1128: kinds of tests!
Line 1129: Indicates the name of 
Line 1130: the method that will 
Line 1131: provide the inputs
Line 1132: Calls the
Line 1133: method under
Line 1134: test, using the
Line 1135: parameterized
Line 1136: values
Line 1137: One argument 
Line 1138: per test case
Line 1139: Tests with nulls 
Line 1140: and empties
Line 1141: Tests with 
Line 1142: single digits
Line 1143: Tests with 
Line 1144: multiple 
Line 1145: digits
Line 1146: Tests with multiple
Line 1147: digits, different
Line 1148: length, with and
Line 1149: without carry
Line 1150: (from both sides)
Line 1151: 
Line 1152: --- 페이지 80 ---
Line 1153: 52
Line 1154: CHAPTER 2
Line 1155: Specification-based testing
Line 1156:      of(numbers(3,1,7,9), numbers(2,6,8), numbers(3,4,4,7)), // T16.1    
Line 1157:      of(numbers(2,6,8), numbers(3,1,7,9), numbers(3,4,4,7)), // T16.2    
Line 1158:      of(numbers(1,9,1,7,1), numbers(2,1,8,1,6,1),
Line 1159:        numbers(2,3,7,3,3,2)), // T17.1                                   
Line 1160:      of(numbers(2,1,8,1,6,1), numbers(1,9,1,7,1),
Line 1161:        numbers(2,3,7,3,3,2)), // T17.2                                   
Line 1162:      of(numbers(9,9,8), numbers(9,1,7,2), numbers(1,0,1,7,0)), // T18.1  
Line 1163:      of(numbers(9,1,7,2), numbers(9,9,8), numbers(1,0,1,7,0)), // T18.2  
Line 1164:      of(numbers(0,0,0,1,2), numbers(0,2,3), numbers(3,5)), // T19   
Line 1165:      of(numbers(0,0,0,1,2), numbers(0,2,9), numbers(4,1)), // T20   
Line 1166:      of(numbers(9,9), numbers(1), numbers(1,0,0)) // T21   
Line 1167:    );
Line 1168:  }
Line 1169:  private static List<Integer> numbers(int... nums) {   
Line 1170:    List<Integer> list = new ArrayList<>();
Line 1171:    for(int n : nums)
Line 1172:      list.add(n);
Line 1173:    return list;
Line 1174:  }
Line 1175: }
Line 1176: Interestingly, a lot of these test cases break! See the JUnit report in figure 2.6. For
Line 1177: example, take the first failing test, T6 (single digit with a carry). Given left = [9] and
Line 1178: right = [2], we expect the output to be [1,1]. But the program outputs [1]! T12
Line 1179: (“carry propagated to a new (now most significant) digit”) also fails: given left =
Line 1180: [9,9,8] and right = [1,7,2], we expect the output to be [1,1,7,0], but it is
Line 1181: [1,7,0]. The program cannot handle the carry when the carry needs to become a
Line 1182: new leftmost digit.
Line 1183:  What a tricky bug! Did you see it when we wrote the method implementation?
Line 1184:  There is a simple fix: all we need to do is add the carry at the end, if necessary.
Line 1185: Here’s the implementation.
Line 1186: // ... all the code here ...
Line 1187: if (carry > 0)
Line 1188:     result.addFirst(carry);
Line 1189: return result;
Line 1190: With these tests passing, we see that the program does not handle zeroes to the left.
Line 1191: When left = [0,0,0,1,2] and right = [0,2,3], we expect the output to be [3,5],
Line 1192: but the program returns [0,0,0,3,5]. The fix is also straightforward: remove the
Line 1193: zeroes on the left before returning the result (listing 2.12).
Line 1194:  
Line 1195: Listing 2.11
Line 1196: First bug fix in the add program
Line 1197: Tests with multiple
Line 1198: digits, different
Line 1199: length, with and
Line 1200: without carry
Line 1201: (from both sides)
Line 1202: Tests with zeroes
Line 1203: on the left
Line 1204: The boundary 
Line 1205: test
Line 1206: Auxiliary method
Line 1207: that produces a list of
Line 1208: integers. Auxiliary methods
Line 1209: are common in test suites to
Line 1210: help developers write more
Line 1211: maintainable test code.
Line 1212: 
Line 1213: --- 페이지 81 ---
Line 1214: 53
Line 1215: Finding bugs with specification testing
Line 1216:  
Line 1217: // ... previous code here...
Line 1218: if (carry > 0)
Line 1219:     result.addFirst(carry);
Line 1220: while (result.size() > 1 && result.get(0) == 0)   
Line 1221:   result.remove(0);
Line 1222: return result;
Line 1223: Listing 2.12
Line 1224: Second bug fix in the add program
Line 1225: Left
Line 1226: Right
Line 1227: Expected
Line 1228: output
Line 1229: These tests are all
Line 1230: failing! This means
Line 1231: our implementation
Line 1232: has a bug.
Line 1233: Figure 2.6
Line 1234: The results of the test cases we just created. A lot of them fail, indicating 
Line 1235: that the program has a bug!
Line 1236: Removes leading 
Line 1237: zeroes from the 
Line 1238: result
Line 1239: 
Line 1240: --- 페이지 82 ---
Line 1241: 54
Line 1242: CHAPTER 2
Line 1243: Specification-based testing
Line 1244: We’re only missing test cases to ensure that the pre-condition holds that each digit is a
Line 1245: number between 0 and 9. All we need to do is pass various invalid digits. Let’s do it
Line 1246: directly in the JUnit test as follows.
Line 1247: @ParameterizedTest       
Line 1248: @MethodSource("digitsOutOfRange")
Line 1249: void shouldThrowExceptionWhenDigitsAreOutOfRange(List<Integer> left,
Line 1250:   ➥ List<Integer> right) {
Line 1251:   assertThatThrownBy(() -> new NumberUtils().add(left, right))
Line 1252:       .isInstanceOf(IllegalArgumentException.class);   
Line 1253: }
Line 1254: static Stream<Arguments> digitsOutOfRange() {  
Line 1255:   return Stream.of(
Line 1256:       of(numbers(1,-1,1), numbers(1)),
Line 1257:       of(numbers(1), numbers(1,-1,1)),
Line 1258:       of(numbers(1,10,1), numbers(1)),
Line 1259:       of(numbers(1), numbers(1,11,1))
Line 1260:   );
Line 1261: }
Line 1262: All tests are now passing. Given the thoroughness of our test suite, I feel confident
Line 1263: enough to move on.
Line 1264: NOTE
Line 1265: Interestingly, the bugs we found in this example were caused not by
Line 1266: buggy code but by a lack of code. This is a common type of bug, and it can be
Line 1267: caught by specification testing. When in doubt, write a test! Writing auto-
Line 1268: mated (unit) test cases is so quick that they let you easily see what happens.
Line 1269: Having too many useless tests is a problem, but a couple will not hurt. 
Line 1270: 2.4
Line 1271: Specification-based testing in the real world
Line 1272: Now that you have a clear understanding of how to systematically devise test cases
Line 1273: based on specifications, here are a few pragmatic tips I have learned over the years.
Line 1274: 2.4.1
Line 1275: The process should be iterative, not sequential
Line 1276: Describing iterative processes in writing is challenging. My explanation may have
Line 1277: given you the impression that this process is fully sequential and that you move to the
Line 1278: next step only when you have completed the previous one. However, the entire pro-
Line 1279: cess is meant to be iterative. In practice, I go back and forth between the different
Line 1280: steps. Often, when I’m writing test cases, I notice that I missed a partition or bound-
Line 1281: ary, and I go back and improve my test suite. 
Line 1282: Listing 2.13
Line 1283: Tests for a pre-condition of the add program
Line 1284: A parameterized test 
Line 1285: also fits well here.
Line 1286: Asserts that 
Line 1287: an exception 
Line 1288: happens
Line 1289: Passes invalid 
Line 1290: arguments
Line 1291: 
Line 1292: --- 페이지 83 ---
Line 1293: 55
Line 1294: Specification-based testing in the real world
Line 1295: 2.4.2
Line 1296: How far should specification testing go?
Line 1297: The pragmatic answer to this question is to understand the risks of a failure. What
Line 1298: would be the cost of a failure in that part of the program? If the cost is high, it may be
Line 1299: wise to invest more in testing, explore more corner cases, and try different techniques
Line 1300: to ensure quality. But if the cost is low, being less thorough may be good enough. Per-
Line 1301: sonally, I stop testing when I have been through all the steps a couple of times and
Line 1302: cannot see a case I am not testing. 
Line 1303: 2.4.3
Line 1304: Partition or boundary? It does not matter!
Line 1305: When you are exploring inputs and outputs, identifying partitions, and devising test
Line 1306: cases, you may end up considering a boundary to be an exclusive partition and not a
Line 1307: boundary between two partitions. It does not matter if a specific case emerges when
Line 1308: you are identifying partitions or in the boundaries step. Each developer may interpret
Line 1309: the specification differently, and minor variations may result. The important thing is
Line 1310: that the test case emerges and the bug will not slip into the program. 
Line 1311: 2.4.4
Line 1312: On and off points are enough, but feel free to add in 
Line 1313: and out points
Line 1314: On and off points belong to specific partitions, so they also serve as concrete test cases
Line 1315: for the partitions. This means testing all the boundaries of your input domain is
Line 1316: enough. Nevertheless, I often try some in and out points in my tests. They are redun-
Line 1317: dant, because the on and off points exercise the same partition as the in and out
Line 1318: points; but these extra points give me a better understanding of the program and may
Line 1319: better represent real-life inputs. Striving for the leanest test suite is always a good idea,
Line 1320: but a few extra points are fine. 
Line 1321: 2.4.5
Line 1322: Use variations of the same input to facilitate understanding
Line 1323: You can simplify your understanding of the different test cases by using the same
Line 1324: input seed for all of them, as we noticed in an observational study with professional
Line 1325: developers described in my paper with Treude and Zaidman (2021). For each parti-
Line 1326: tion, you then make small modifications to the input seed: just enough to meet the
Line 1327: criteria of that partition. In the chapter example, all the test cases are based on the
Line 1328: string “abc”; as soon as one test case fails, it is easy to compare it to similar inputs from
Line 1329: other test cases that pass.
Line 1330:  Note that this trick goes against the common testing idea of varying inputs as
Line 1331: much as possible. Varying inputs is essential, as it allows us to explore the input space
Line 1332: and identify corner cases. However, when doing specification-based testing, I prefer to
Line 1333: focus on rigorously identifying and testing partitions. Later in the book, we will write
Line 1334: test cases that explore the input domain in an automated fashion via property-based
Line 1335: testing in chapter 5. 
Line 1336: 
Line 1337: --- 페이지 84 ---
Line 1338: 56
Line 1339: CHAPTER 2
Line 1340: Specification-based testing
Line 1341: 2.4.6
Line 1342: When the number of combinations explodes, be pragmatic
Line 1343: If we had combined all the partitions we derived from the substringsBetween pro-
Line 1344: gram, we would have ended up with 320 tests. This number is even larger for more
Line 1345: complex problems. Combinatorial testing is an entire area of research in software test-
Line 1346: ing; I will not dive into the techniques that have been proposed for such situations,
Line 1347: but I will provide you with two pragmatic suggestions.
Line 1348:  First, reduce the number of combinations as much as possible. Testing exceptional
Line 1349: behavior isolated from other behaviors (as we did in the example) is one way to do so.
Line 1350: You may also be able to leverage your domain knowledge to further reduce the num-
Line 1351: ber of combinations.
Line 1352:  Second, if you are facing many combinations at the method level, consider breaking
Line 1353: the method in two. Two smaller methods have fewer things to test and, therefore, fewer
Line 1354: combinations to test. Such a solution works well if you carefully craft the method con-
Line 1355: tracts and the way they should pass information. You also reduce the chances of bugs
Line 1356: when the two simple methods are combined into a larger, more complex one. 
Line 1357: 2.4.7
Line 1358: When in doubt, go for the simplest input
Line 1359: Picking concrete input for test cases is tricky. You want to choose a value that is realis-
Line 1360: tic but, at the same time, simple enough to facilitate debugging if the test fails.
Line 1361:  I recommend that you avoid choosing complex inputs unless you have a good rea-
Line 1362: son to use them. Do not pick a large integer value if you can choose a small integer
Line 1363: value. Do not pick a 100-character string if you can select a 5-character string. Simplic-
Line 1364: ity matters. 
Line 1365: 2.4.8
Line 1366: Pick reasonable values for inputs you do not care about
Line 1367: Sometimes, your goal is to exercise a specific part of the functionality, and that part does
Line 1368: not use one of the input values. You can pass any value to that “useless” input variable. In
Line 1369: such scenarios, my recommendation is to pass realistic values for these inputs. 
Line 1370: 2.4.9
Line 1371: Test for nulls and exceptional cases, but only when 
Line 1372: it makes sense
Line 1373: Testing nulls and exceptional cases is always important because developers often for-
Line 1374: get to handle such cases in their code. But remember that you do not want to write
Line 1375: tests that never catch a bug. Before writing such tests, you should understand the over-
Line 1376: all picture of the software system (and its architecture). The architecture may ensure
Line 1377: that the pre-conditions of the method are satisfied before calling it.
Line 1378:  If the piece of code you are testing is very close to the UI, exercise more corner
Line 1379: cases such as null, empty strings, uncommon integer values, and so on. If the code is
Line 1380: far from the UI and you are sure the data is sanitized before it reaches the component
Line 1381: under test, you may be able to skip such tests. Context is king. Only write tests that will
Line 1382: eventually catch a bug. 
Line 1383: 
Line 1384: --- 페이지 85 ---
Line 1385: 57
Line 1386: Specification-based testing in the real world
Line 1387: 2.4.10 Go for parameterized tests when tests have the same skeleton
Line 1388: A little duplication is never a problem, but a lot of duplication is. We created 21 differ-
Line 1389: ent tests for the substringsBetween program. The test code was lean because we
Line 1390: grouped some of the test cases into single test methods. Imagine writing 21 almost-
Line 1391: identical test cases. If each method took 5 lines of code, we would have a test class with
Line 1392: 21 methods and 105 lines. This is much longer than the test suite with the parameter-
Line 1393: ized test that we wrote.
Line 1394:  Some developers argue that parameterized tests are confusing. Deciding whether
Line 1395: to use JUnit test cases or parameterized tests is, most of all, a matter of taste. I use
Line 1396: parameterized tests when the amount of duplication in my test suite is too large. In
Line 1397: this chapter, I leaned more toward JUnit test cases: lots of test cases logically grouped
Line 1398: in a small set of test methods. We discuss test code quality further in chapter 10. 
Line 1399: 2.4.11 Requirements can be of any granularity
Line 1400: The seven-step approach I propose in this chapter works for requirements of any
Line 1401: granularity. Here, we applied it in a specification that could be implemented by a sin-
Line 1402: gle method. However, nothing prevents you from using it with larger requirements
Line 1403: that involve many classes. Traditionally, specification-based testing techniques focus
Line 1404: on black-box testing: that is, testing an entire program or feature, rather than unit-
Line 1405: testing specific components. I argue that these ideas also make sense at the unit level.
Line 1406:  When we discuss larger tests (integration testing), we will also look at how to devise
Line 1407: test cases for sets of classes or components. The approach is the same: reflect on the
Line 1408: inputs and their expected outputs, divide the domain space, and create test cases. You
Line 1409: can generalize the technique discussed here to tests at any level. 
Line 1410: 2.4.12 How does this work with classes and state?
Line 1411: The two methods we tested in this chapter have no state, so all we had to do was think
Line 1412: of inputs and outputs. In object-oriented systems, classes have state. Imagine a Shop-
Line 1413: pingCart class and a behavior totalPrice() that requires some CartItems to be
Line 1414: inserted before the method can do its job. How do we apply specification-based test-
Line 1415: ing in this case? See the following listing.
Line 1416: public class ShoppingCart {
Line 1417:   private List<CartItem> items = new ArrayList<CartItem>();
Line 1418:   public void add(CartItem item) {   
Line 1419:     this.items.add(item);
Line 1420:   }
Line 1421:   public double totalPrice() {   
Line 1422:     double totalPrice = 0;
Line 1423:     for (CartItem item : items) {
Line 1424: Listing 2.14
Line 1425: ShoppingCart and CartItem classes
Line 1426: Adds items 
Line 1427: to the cart
Line 1428: Loops through all the items 
Line 1429: and sums up the final price
Line 1430: 
Line 1431: --- 페이지 86 ---
Line 1432: 58
Line 1433: CHAPTER 2
Line 1434: Specification-based testing
Line 1435:       totalPrice += item.getUnitPrice() * item.getQuantity();
Line 1436:     }
Line 1437:     return totalPrice;
Line 1438:   }
Line 1439: }
Line 1440: public class CartItem {   
Line 1441:   private final String product;
Line 1442:   private final int quantity;
Line 1443:   private final double unitPrice;
Line 1444:   public CartItem(String product, int quantity,
Line 1445:    double unitPrice) {
Line 1446:     this.product = product;
Line 1447:     this.quantity = quantity;
Line 1448:     this.unitPrice = unitPrice;
Line 1449:   }
Line 1450:   // getters
Line 1451: }
Line 1452: Nothing changes in the way we approach specification-based testing. The only differ-
Line 1453: ence is that when we reflect about the method under test, we must consider not only
Line 1454: the possible input parameters, but also the state the class should be in. For this spe-
Line 1455: cific example, looking at the expected behavior of the totalPrice method, I can
Line 1456: imagine tests exercising the behavior of the method when the cart has zero items, a
Line 1457: single item, multiple items, and various quantities (plus corner cases such as nulls).
Line 1458: All we do differently is to set up the class’s state (by adding multiple items to the cart)
Line 1459: before calling the method we want to test, as in the following listing.
Line 1460: import org.junit.jupiter.api.Test;
Line 1461: import static org.assertj.core.api.Assertions.assertThat;
Line 1462: public class ShoppingCartTest {
Line 1463:   private final ShoppingCart cart = new ShoppingCart();   
Line 1464:   @Test
Line 1465:   void noItems() {
Line 1466:     assertThat(cart.totalPrice())   
Line 1467:       .isEqualTo(0);
Line 1468:   }
Line 1469:   @Test
Line 1470:   void itemsInTheCart() {
Line 1471:     cart.add(new CartItem("TV", 1, 120));
Line 1472:     assertThat(cart.totalPrice())   
Line 1473:       .isEqualTo(120);
Line 1474: Listing 2.15
Line 1475: Tests for the ShoppingCart class
Line 1476: A simple class that 
Line 1477: represents an item 
Line 1478: in the cart
Line 1479: Having the cart as a 
Line 1480: field means we don’t 
Line 1481: have to instantiate it 
Line 1482: for every test. This is 
Line 1483: a common technique 
Line 1484: to improve legibility.
Line 1485: Asserts that 
Line 1486: an empty cart 
Line 1487: returns 0
Line 1488: Asserts that it 
Line 1489: works for a single 
Line 1490: item in the cart …
Line 1491: 
Line 1492: --- 페이지 87 ---
Line 1493: 59
Line 1494: Exercises
Line 1495:     cart.add(new CartItem("Chocolate", 2, 2.5));
Line 1496:     assertThat(cart.totalPrice())   
Line 1497:       .isEqualTo(120 + 2.5*2);
Line 1498:   }
Line 1499: }
Line 1500: Again, the mechanics are the same. We just have to take more into consideration when
Line 1501: engineering the test cases. 
Line 1502: 2.4.13 The role of experience and creativity
Line 1503: If two testers performed the specification-based testing technique I described earlier
Line 1504: in the same program, would they develop the same set of tests? Ideally, but possibly
Line 1505: not. In the substringsBetween() example, I would expect most developers to come
Line 1506: up with similar test cases. But it is not uncommon for developers to approach a prob-
Line 1507: lem from completely different yet correct angles.
Line 1508:  I am trying to reduce the role of experience and creativity by giving developers a
Line 1509: process that everybody can follow, but in practice, experience and creativity make a
Line 1510: difference in testing. We observed that in a small controlled experiment (Yu, Treude,
Line 1511: and Aniche, 2019).
Line 1512:  In the substringsBetween() example, experienced testers may see more compli-
Line 1513: cated test cases, but a novice tester may have difficulty spotting those. A more experi-
Line 1514: enced tester may realize that spaces in the string play no role and skip this test,
Line 1515: whereas a novice developer may be in doubt and write an extra “useless” test. This is
Line 1516: why I like the specification-based testing systematic approach I described in this
Line 1517: chapter: it will help you remember what to think about. But it is still up to you to do
Line 1518: the thinking!
Line 1519: Exercises
Line 1520: 2.1
Line 1521: Which statement is false about applying the specification-based testing method
Line 1522: on the following Java method?
Line 1523: /**
Line 1524:  * Puts the supplied value into the Map,
Line 1525:  * mapped by the supplied key.
Line 1526:  * If the key is already in the map, its
Line 1527:  * value will be replaced by the new value.
Line 1528:  *
Line 1529:  * NOTE: Nulls are not accepted as keys;
Line 1530:  *  a RuntimeException is thrown when key is null.
Line 1531:  *
Line 1532:  * @param key the key used to locate the value
Line 1533:  * @param value the value to be stored in the HashMap
Line 1534:  * @return the prior mapping of the key,
Line 1535:  *  or null if there was none.
Line 1536: */
Line 1537: public V put(K key, V value) {
Line 1538:   // implementation here
Line 1539: }
Line 1540: … as well as for 
Line 1541: many items in 
Line 1542: the cart.
Line 1543: 
Line 1544: --- 페이지 88 ---
Line 1545: 60
Line 1546: CHAPTER 2
Line 1547: Specification-based testing
Line 1548: A The specification does not specify any details about the value input
Line 1549: parameter, and thus, experience should be used to partition it (for exam-
Line 1550: ple, value being null or not null).
Line 1551: B The number of tests generated by the category/partition method can
Line 1552: grow quickly, as the chosen partitions for each category are later com-
Line 1553: bined one by one. This is not a practical problem for the put() method
Line 1554: because the number of categories and partitions is small.
Line 1555: C In an object-oriented language, in addition to using the method’s input
Line 1556: parameters to explore partitions, we should also consider the object’s
Line 1557: internal state (the class’s attributes), as it can also affect the method’s
Line 1558: behavior.
Line 1559: D With the available information, it is not possible to perform the category/
Line 1560: partition method, as the source code is required for the last step (adding
Line 1561: constraints).
Line 1562: 2.2
Line 1563: Consider a find program that finds occurrences of a pattern in a file. The pro-
Line 1564: gram has the following syntax:
Line 1565: find <pattern> <file>
Line 1566: After reading the specification and following specification-based testing, a tes-
Line 1567: ter devised the following partitions:
Line 1568: A Pattern size: empty, single character, many characters, longer than any
Line 1569: line in the file
Line 1570: B Quoting: pattern is quoted, pattern is not quoted, pattern is improperly
Line 1571: quoted
Line 1572: C Filename: good filename, no filename with this name, omitted
Line 1573: D Occurrences in the file: none, exactly one, more than one
Line 1574: E Occurrences in a single line, assuming the line contains the pattern: one,
Line 1575: more than one
Line 1576: Now the number of combinations is too high. What actions could we take to
Line 1577: reduce the number of combinations?
Line 1578: 2.3
Line 1579: Postal codes in some imaginary country are always composed of four numbers
Line 1580: and two letters: for example, 2628CD. Numbers are in the range [1000, 4000].
Line 1581: Letters are in the range [C, M].
Line 1582: Consider a program that receives two inputs—an integer (for the four num-
Line 1583: bers) and a string (for the two letters)—and returns true (valid postal code) or
Line 1584: false (invalid postal code). The boundaries for this program appear to be
Line 1585: straightforward:
Line 1586: A Anything below 1000: invalid
Line 1587: B
Line 1588: [1000, 4000]: valid
Line 1589: C Anything above 4000: invalid
Line 1590: 
Line 1591: --- 페이지 89 ---
Line 1592: 61
Line 1593: Summary
Line 1594: D
Line 1595: [A, B]: invalid
Line 1596: E
Line 1597: [C, M]: valid
Line 1598: F
Line 1599: [N, Z]: invalid
Line 1600: Based on what you as a tester assume about the program, what other corner or
Line 1601: boundary cases can you come up with? Describe these invalid cases and how
Line 1602: they may exercise the program based on your assumptions.
Line 1603: 2.4
Line 1604: A program called FizzBuzz does the following: given an integer n, return the
Line 1605: string formed from the number followed by “!”. If the number is divisible by 3,
Line 1606: use “Fizz” instead of the number; and if the number is divisible by 5, use “Buzz”
Line 1607: instead of the number, and if the number is divisible by both 3 and 5, use “Fizz-
Line 1608: Buzz” instead of the number.
Line 1609: Examples:
Line 1610: A The integer 3 yields “Fizz!”
Line 1611: B The integer 4 yields “4!”
Line 1612: C The integer 5 yields “Buzz!”
Line 1613: D The integer 15 yields “FizzBuzz!”
Line 1614: A novice tester is trying to devise as many tests as possible for the FizzBuzz
Line 1615: method and comes up with the following:
Line 1616: A T1 = 15
Line 1617: B T2 = 30
Line 1618: C T3 = 8
Line 1619: D T4 = 6
Line 1620: E T5 = 25
Line 1621: Which of these tests can be removed while maintaining a good test suite? Which
Line 1622: concept can we use to determine the test(s) that can be removed?
Line 1623: 2.5
Line 1624: A game has the following condition: numberOfPoints <= 570. Perform bound-
Line 1625: ary analysis on the condition. What are the on and off points?
Line 1626: A On point = 570, off point = 571
Line 1627: B On point = 571, off point = 570
Line 1628: C On point = 570, off point = 569
Line 1629: D On point = 569, off point = 570
Line 1630: 2.6
Line 1631: Perform boundary analysis on the following equality: x == 10. What are the on
Line 1632: and off points?
Line 1633: Summary
Line 1634: Requirements are the most important artifact we can use to generate tests.
Line 1635: Specification-based testing techniques help us explore the requirements in a
Line 1636: systematic way. For example, they help us examine the domain space of the dif-
Line 1637: ferent input variables and how they interact with each other.
Line 1638: 
Line 1639: --- 페이지 90 ---
Line 1640: 62
Line 1641: CHAPTER 2
Line 1642: Specification-based testing
Line 1643: I propose a seven-step approach for specification testing: (1) understand the
Line 1644: requirements, (2) explore the program if you do not know much about it, (3)
Line 1645: judiciously analyze the properties of the inputs and outputs and identify the
Line 1646: partitions, (4) analyze the boundaries, (5) devise concrete test cases, (6) imple-
Line 1647: ment the concrete test cases as automated (JUnit) tests, and (7) use creativity
Line 1648: and experience to augment the test suite.
Line 1649: Bugs love boundaries. However, identifying the boundaries may be the most
Line 1650: challenging part of specification testing.
Line 1651: The number of test cases may be too large, even in simpler programs. This
Line 1652: means you must decide what should be tested and what should not be tested.