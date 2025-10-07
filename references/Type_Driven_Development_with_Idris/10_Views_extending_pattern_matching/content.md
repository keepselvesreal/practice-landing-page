Line 1: 
Line 2: --- 페이지 284 ---
Line 3: 258
Line 4: Views: extending
Line 5: pattern matching
Line 6: In type-driven development, our approach to implementing functions is to write a
Line 7: type, define the structure of the function by case splits on its arguments, and refine
Line 8: the function by filling in holes. In the define step in particular, we use the structure
Line 9: of the input types to drive the structure of the function as a whole.
Line 10:  As you learned in chapter 3, when you case-split on a variable, the patterns arise
Line 11: from the variable’s type. Specifically, the patterns arise from the data constructors
Line 12: that can be used to build values of that type. For example, if you case-split on an
Line 13: items variable of type List elem, the following patterns will arise:
Line 14: 
Line 15: []—Represents the empty list
Line 16: 
Line 17: (x :: xs)—Represents a non-empty list with x as the first element and xs as
Line 18: the list of the remaining elements
Line 19: This chapter covers
Line 20: Defining views, which describe alternative forms of 
Line 21: pattern matching
Line 22: Introducing the with construct for working with views
Line 23: Describing efficient traversals of data structures
Line 24: Hiding the representation of data behind views
Line 25: 
Line 26: --- 페이지 285 ---
Line 27: 259
Line 28: Defining and using views
Line 29: Pattern matching, therefore, deconstructs variables into their components. Often,
Line 30: though, you’ll want to deconstruct variables in different ways. For example, you might
Line 31: want to deconstruct an input list into one of the following forms: 
Line 32: A list of all but the last element, and then the last element
Line 33: Two sublists—the first half and the second half of the input
Line 34: In this chapter, you’ll see how to extend the forms of patterns you can use by defining
Line 35: informative data types, called views. Views are dependent types that are parameterized
Line 36: by the data you’d like to match, and they give you new ways of observing that data. For
Line 37: example, views can do the following:
Line 38: Describe new forms of patterns, such as allowing you to match against the last
Line 39: element of a list rather than the first
Line 40: Define alternative ways of traversing data structures, such as traversing a list in
Line 41: reverse, or by repeatedly splitting the list into halves
Line 42: Hide complex data representations behind an abstract interface while still sup-
Line 43: porting pattern-matching on that data
Line 44: We’ll start by looking at how, using views, we can define alternative ways of matching
Line 45: on lists, such as processing the last element first. We’ll then look at defining efficient
Line 46: traversals of lists and guaranteeing that they terminate, and we’ll look at some traversals
Line 47: provided by the Idris library. Finally, we’ll use views to help with data abstraction by
Line 48: hiding the structure of data in a separate module and matching and traversing the
Line 49: data using a view.
Line 50: 10.1
Line 51: Defining and using views
Line 52: When you write a (x :: xs) pattern for matching a list, x will take the value of the
Line 53: first element of the list and xs will take the value of the tail of the list. You saw the fol-
Line 54: lowing function in chapter 3 to describe how a list was constructed, illustrated again
Line 55: in figure 10.1:
Line 56: describeList : List Int -> String
Line 57: describeList [] = "Empty"
Line 58: describeList (x :: xs) = "Non-empty, tail = " ++ show xs
Line 59: x = 1
Line 60: x = 2
Line 61: xs = []
Line 62: 1 :: []
Line 63: "Non-empty, tail = []"
Line 64: 2 :: 3 :: 4 :: 5 :: []
Line 65: "Non-empty, tail = [3,4,5]"
Line 66: xs = 3 :: 4 :: 5 :: []
Line 67: Figure 10.1
Line 68: Matching the pattern (x :: xs) for inputs [1] and [2,3,4,5]
Line 69: 
Line 70: --- 페이지 286 ---
Line 71: 260
Line 72: CHAPTER 10
Line 73: Views: extending pattern matching
Line 74: As a result, matching lists using the pattern (x :: xs) means that you’ll always traverse
Line 75: the list forwards, processing x first, and then processing the tail, xs. But sometimes it’s
Line 76: convenient to be able to traverse the list backwards, processing the last element first.
Line 77:  You can add a single element to the end of a list using the ++ operator:
Line 78: Idris> [2,3,4] ++ [5]
Line 79: [2, 3, 4, 5] : List Integer
Line 80: It would be nice to be able to match patterns of the form (xs ++ [x]), where x takes
Line 81: the value of the last element of the list and xs takes the value of the initial segment of
Line 82: the list. That is, you might like to be able to write a function of the following form, as
Line 83: illustrated in figure 10.2: 
Line 84: describeListEnd : List Int -> String
Line 85: describeListEnd [] = "Empty"
Line 86: describeListEnd (xs ++ [x]) = "Non-empty, initial portion = " ++ show xs
Line 87: Unfortunately, if you try to implement describeListEnd, it will fail with the following
Line 88: error:
Line 89: DLFail.idr:3:19:
Line 90: When checking left hand side of describeListEnd:
Line 91: Can't match on describeListEnd (xs ++ [x])
Line 92: The problem is that you’re trying to pattern-match on the result of a function, ++, and
Line 93: in general there’s no way for Idris to automatically deduce the inputs to an arbitrary
Line 94: function from its output. You can, however, extend the forms of the patterns you can
Line 95: use by defining informative data types called views. In this section, you’ll see how to
Line 96: define views, and I’ll introduce the with construct, which provides a concise notation
Line 97: for defining functions that use views.
Line 98: 10.1.1 Matching the last item in a list
Line 99: You can’t write describeListEnd directly because you can’t match a pattern of the
Line 100: form (xs ++ [x]) directly. You can, however, take advantage of dependent pattern
Line 101: matching to deduce that a particular input must have the form (xs ++ [x]). You saw
Line 102: This line does not type check
Line 103: xs = []
Line 104: xs = 2 :: 3 :: 4 :: []
Line 105: x = 1
Line 106: 1 :: []
Line 107: "Non-empty, initial portion = []"
Line 108: 2 :: 3 :: 4 :: 5 :: []
Line 109: "Non-empty, initial portion = [2,3,4]"
Line 110: x = 5
Line 111: Figure 10.2
Line 112: Matching the pattern (xs ++ [x]) for inputs [1] and [2,3,4,5]
Line 113: 
Line 114: --- 페이지 287 ---
Line 115: 261
Line 116: Defining and using views
Line 117: dependent pattern matching in chapter 6, where inspecting the value of one argument
Line 118: (that is, case-splitting on that argument) can tell you about the form of another. Using
Line 119: dependent pattern matching, you can describe alternative patterns for lists.
Line 120:  The following listing shows the ListLast dependent type, which describes two pos-
Line 121: sible forms a List can take. A list is either empty, [], or constructed from the initial
Line 122: portion of a list and its final element.
Line 123: data ListLast : List a -> Type where
Line 124: Empty : ListLast []
Line 125: NonEmpty : (xs : List a) -> (x : a) -> ListLast (xs ++ [x])
Line 126: Using ListLast, along with dependent pattern matching, you can define describe-
Line 127: ListEnd. You’ll start by defining a helper function that takes an input list, input, and
Line 128: an extra argument, form, that says whether the list is empty or non-empty:
Line 129: 1
Line 130: Type—Begin with the type. You’ll use ListLast to describe the possible forms
Line 131: that input can take: 
Line 132: describeHelper : (input : List Int) -> (form : ListLast input) -> String
Line 133: describeHelper input form = ?describeHelper_rhs
Line 134:  2
Line 135: Define—You want to describe input, so you’ll need to inspect its form somehow.
Line 136: Previously, when defining a function to inspect the form of an input, you’ve
Line 137: case-split on that input. Here, the intention of the form argument is to tell you
Line 138: more about input, so case-split on that instead: 
Line 139: describeHelper : (input : List Int) -> (form : ListLast input) -> String
Line 140: describeHelper [] Empty = ?describeHelper_rhs_1
Line 141: describeHelper (xs ++ [x]) (NonEmpty xs x) = ?describeHelper_rhs_2
Line 142: Notice that the case split on form has told you more about the form of input. In
Line 143: particular, the type of NonEmpty means that if form has the value NonEmpty xs x,
Line 144: then input must have the value (xs ++ [x]).
Line 145: 3
Line 146: Refine—Complete the definition by describing the patterns as in our initial
Line 147: attempt at describeListEnd: 
Line 148: describeHelper : (input : List Int) -> ListLast input -> String
Line 149: describeHelper [] Empty = "Empty"
Line 150: describeHelper (xs ++ [x]) (NonEmpty xs x)
Line 151: = "Non-empty, initial portion = " ++ show xs
Line 152: ListLast is a view of lists because it provides an alternative means of viewing the data.
Line 153: It’s an ordinary data type, though, and in order to use ListLast in practice, you’ll
Line 154: need to be able to convert an input list, xs, into a value of type ListLast xs. 
Line 155: Listing 10.1
Line 156: The ListLast dependent type, which gives alternative patterns for a list
Line 157: (DescribeList.idr)
Line 158: An empty list has 
Line 159: the form [].
Line 160: A non-empty list has an initial
Line 161: portion, xs, and a last item, x.
Line 162: 
Line 163: --- 페이지 288 ---
Line 164: 262
Line 165: CHAPTER 10
Line 166: Views: extending pattern matching
Line 167: 10.1.2 Building views: covering functions
Line 168: The next listing shows listLast, which converts an input list, xs, into an instance of a
Line 169: view, ListLast xs, which gives access to the last element of xs.
Line 170: total
Line 171: listLast : (xs : List a) -> ListLast xs
Line 172: listLast [] = Empty
Line 173: listLast (x :: xs) = case listLast xs of
Line 174: Empty => NonEmpty [] x
Line 175: NonEmpty ys y => NonEmpty (x :: ys) y
Line 176: listLast is the covering function of the ListLast view. A covering function of a view
Line 177: describes how to convert a value (in this case the input list) into a view of that value
Line 178: (in this case, an xs list and a value x, where xs ++ [x] = input).
Line 179: NAMING CONVENTION FOR COVERING FUNCTIONS
Line 180: By convention, covering func-
Line 181: tions are given the same name as the view type, but with an initial lowercase
Line 182: letter.
Line 183: Now that you can describe any List in the form ListLast, you can complete the defi-
Line 184: nition of describeListEnd: 
Line 185: describeHelper : (input : List Int) -> ListLast input -> String
Line 186: describeHelper [] Empty = "Empty"
Line 187: describeHelper (xs ++ [x]) (NonEmpty xs x)
Line 188: = "Non-empty, initial portion = " ++ show xs
Line 189: describeListEnd : List Int -> String
Line 190: describeListEnd xs = describeHelper xs (listLast xs)
Line 191: This works as we intended in our initial attempt at describeListEnd, with the original
Line 192: patterns in describeHelper. Given that you’re using a different notion of pattern
Line 193: matching than the default, you should expect to have to use some additional notation
Line 194: to explain how to match the pattern (xs ++ [x]), but the overall definition still feels
Line 195: quite verbose.
Line 196:  Because dependent pattern matching in this way is a common programming
Line 197: idiom in Idris, there’s a construct for expressing extended pattern matching more
Line 198: concisely: the with construct. 
Line 199: 10.1.3 with blocks: syntax for extended pattern matching
Line 200: Using views to generate informative patterns like (xs ++ [x]) can help the readability
Line 201: of functions and increase your confidence in their correctness because the types tell
Line 202: you exactly what form the inputs must take. But these functions can be a little more
Line 203: verbose because you need to create an extra helper function (like describeHelper) to
Line 204: Listing 10.2
Line 205: Describing a List in the form ListLast (DescribeList.idr)
Line 206: The total flag means Idris will 
Line 207: report an error if listLast is not 
Line 208: fully defined, ensuring that 
Line 209: listLast will work for every list.
Line 210: You need to traverse the entire 
Line 211: list to find the last element, so 
Line 212: make a recursive call.
Line 213: 
Line 214: --- 페이지 289 ---
Line 215: 263
Line 216: Defining and using views
Line 217: do the necessary pattern matching. The with construct provides a notation for using
Line 218: views more concisely.
Line 219:  Using with blocks, you can add extra arguments to the left side of a definition, giv-
Line 220: ing you more arguments to case-split. The easiest way to see how this works is by exam-
Line 221: ple, so let’s take a look at how you can use a with block to define describeListEnd:
Line 222: 1
Line 223: Type—Begin with a top-level type that takes a List Int and returns a String: 
Line 224: describeListEnd : List Int -> String
Line 225: describeListEnd input = ?describeListEnd_rhs
Line 226:  2
Line 227: Define—Press Ctrl-Alt-W with the cursor on the line with the hole ?describe-
Line 228: ListEnd_rhs. This adds a new pattern clause as follows (it won’t yet type-
Line 229: check): 
Line 230: describeListEnd : List Int -> String
Line 231: describeListEnd input with (_)
Line 232: describeListEnd input | with_pat = ?describeListEnd_rhs
Line 233:  3
Line 234: Define—The with syntax adds a new argument to the left side of the definition.
Line 235: The brackets after with give the value of that argument, and the (indented)
Line 236: clause beneath contains the extra argument, after a vertical bar. Here, you’ll
Line 237: match on the result of listLast input, so replace the _ with listLast input: 
Line 238: describeListEnd : List Int -> String
Line 239: describeListEnd input with (listLast input)
Line 240: describeListEnd input | with_pat = ?describeListEnd_rhs
Line 241:  4
Line 242: Type—If you check the type of ?describeListEnd_rhs, you can see more detail
Line 243: about how with works, looking specifically at the type of with_pat: 
Line 244: input : List Int
Line 245: with_pat : ListLast input
Line 246: --------------------------------------
Line 247: describeListEnd_rhs : String
Line 248: The value of with_pat is the result of listLast input. Figure 10.3 shows the
Line 249: components of the syntax for the with construct. Note that the scope of the
Line 250: with block is managed by indentation.
Line 251: describe_list_end input with (listLast input)
Line 252:   describe_list_end input | with_pat = ?describe_list_end_rhs
Line 253: Value to match
Line 254: Additional
Line 255: argument with
Line 256: value of listLast
Line 257: input
Line 258: Vertical bar
Line 259: appears before
Line 260: additional
Line 261: argument
Line 262: Extra
Line 263: indentation
Line 264: Figure 10.3
Line 265: Syntax for 
Line 266: the with construct
Line 267: 
Line 268: --- 페이지 290 ---
Line 269: 264
Line 270: CHAPTER 10
Line 271: Views: extending pattern matching
Line 272:  5
Line 273: Define—Notice that the types of input and with_pat are exactly the same as the
Line 274: types of the inputs to describeHelper earlier. And as in the definition of
Line 275: describeHelper, if you case-split on with_pat, you’ll learn more about the
Line 276: form of input: 
Line 277: describeListEnd : List Int -> String
Line 278: describeListEnd input with (listLast input)
Line 279: describeListEnd [] | Empty = ?describeListEnd_rhs_1
Line 280: describeListEnd (xs ++ [x]) | (NonEmpty xs x)
Line 281: = ?describeListEnd_rhs_2
Line 282: 6
Line 283: Refine—Complete the definition as before, with the description of the patterns: 
Line 284: describeListEnd : List Int -> String
Line 285: describeListEnd input with (listLast input)
Line 286: describeListEnd [] | Empty = "Empty"
Line 287: describeListEnd (xs ++ [x]) | (NonEmpty xs x)
Line 288: = "Non-empty, initial portion = " ++ show xs
Line 289: Effectively, the with construct has allowed you to use an intermediate pattern match,
Line 290: on the result of listLast input, without needing to define a separate function like
Line 291: describeHelper. In turn, matching on the result of listLast input gives you more-
Line 292: informative patterns for input.
Line 293: THE DIFFERENCE BETWEEN WITH AND CASE
Line 294: The purpose of the with construct
Line 295: is similar to that of a case block in that it allows matching on intermediate
Line 296: results. There’s one important difference, however: with introduces a new
Line 297: pattern to match on the left side of a definition. As a result, you can use depen-
Line 298: dent pattern matching directly. In describeListEnd, for example, matching
Line 299: on the result of listLast input told you about the form input must take.
Line 300: You can’t use just any expression in a pattern because it isn’t possible, in general, to
Line 301: decide what the inputs to a function must be, given only its result. Idris therefore
Line 302: allows patterns only when it can deduce those inputs, which is in the following cases: 
Line 303: The pattern consists of a data constructor applied to some arguments. The
Line 304: arguments must also be valid patterns.
Line 305: The value of the pattern is forced by some other valid pattern. In the case of
Line 306: describeListEnd, the value of the pattern (xs ++ [x]) is forced by the valid
Line 307: pattern NonEmpty xs x.
Line 308: 10.1.4 Example: reversing a list using a view
Line 309: Once you have the ability to pattern-match in different ways using views, you can tra-
Line 310: verse data structures in new ways. Rather than always traversing a list from left to right,
Line 311: for example, you can use listLast to traverse a list from right to left, inspecting the
Line 312: last element first.
Line 313:  You can reverse a list in this way:
Line 314: To reverse an empty list [], return [].
Line 315: To reverse a list in the form xs ++ [x], reverse xs and then add x to the front of
Line 316: the list.
Line 317: 
Line 318: --- 페이지 291 ---
Line 319: 265
Line 320: Defining and using views
Line 321: You can implement this algorithm fairly directly using the ListLast view: 
Line 322: 1
Line 323: Type—Call the function myReverse because there’s already a reverse function
Line 324: in the Prelude: 
Line 325: myReverse : List a -> List a
Line 326: myReverse input = ?myReverse_rhs
Line 327:  2
Line 328: Define—You’ll define the function by inspecting the last element of the input
Line 329: first, so you can use listLast to match on a value of type ListLast input. Press
Line 330: Ctrl-Alt-W to insert a with block, and add listLast input as the value to
Line 331: inspect: 
Line 332: myReverse : List a -> List a
Line 333: myReverse input with (listLast input)
Line 334: myReverse input | with_pat = ?myReverse_rhs
Line 335:  3
Line 336: Define—Next, case-split on with_pat to give the relevant patterns for input: 
Line 337: myReverse : List a -> List a
Line 338: myReverse input with (listLast input)
Line 339: myReverse [] | Empty = ?myReverse_rhs_1
Line 340: myReverse (xs ++ [x]) | (NonEmpty xs x) = ?myReverse_rhs_2
Line 341: 4
Line 342: Refine—Finally, you can complete the definition as follows: 
Line 343: myReverse : List a -> List a
Line 344: myReverse input with (listLast input)
Line 345: myReverse [] | Empty = []
Line 346: myReverse (xs ++ [x]) | (NonEmpty xs x) = x :: myReverse xs
Line 347: This is a fairly direct implementation of the algorithm, traversing the list in reverse
Line 348: and constructing a new list by adding the last item of the input as the first item of the
Line 349: result. There are, nevertheless, two problems:
Line 350: The definition is inefficient because it constructs ListLast input on every
Line 351: recursive call, and constructing ListLast input requires traversing input.
Line 352: Idris can’t decide whether the definition is total or not: 
Line 353: *Reverse> :total myReverse
Line 354: Main.myReverse is possibly not total due to:
Line 355: possibly not total due to recursive path:
Line 356: with block in Main.myReverse, with block in Main.myReverse
Line 357: See the sidebar for a brief discussion on totality checking in Idris.
Line 358: The first problem is important to address, because it’s possible to write myReverse in
Line 359: linear time, traversing the input list only once. The second problem is important from
Line 360: the type-driven development perspective: as I discussed in chapter 1, if Idris can deter-
Line 361: mine that a function is total, you have a strong guarantee that the type accurately
Line 362: describes what the function will do. If not, you only have a guarantee that the function
Line 363: will produce a value of the given type if it terminates without crashing. Furthermore, if
Line 364: Idris can’t determine that a function is total, it can’t determine that any functions that
Line 365: call it are total, either.
Line 366: 
Line 367: --- 페이지 292 ---
Line 368: 266
Line 369: CHAPTER 10
Line 370: Views: extending pattern matching
Line 371:  We’ll look at how to address each of these problems, with only minor alterations to
Line 372: myReverse itself, in section 10.2.
Line 373: 10.1.5 Example: merge sort
Line 374: Views allow you to describe matching on data structures any way you like, with as many
Line 375: patterns as you like, provided you can implement a covering function for the view. As
Line 376: a second example of a view, we’ll implement the merge sort algorithm on Lists.
Line 377:  Merge sort, at a high level, works as follows:
Line 378: If the input is an empty list, return an empty list.
Line 379: If the input has one element, it’s already sorted, so return the input.
Line 380: In all other cases, split the list into two halves (differing in size by at most one),
Line 381: recursively sort those halves, and then merge the two sorted halves into a sorted
Line 382: list (see figure 10.4).
Line 383: Totality checking
Line 384: Idris tries to decide whether a function is always terminating by checking two things: 
Line 385: There must be patterns for all possible well-typed inputs.
Line 386: When there is a recursive call (or a sequence of mutually recursive calls),
Line 387: there must be a decreasing argument that converges toward a base case.
Line 388: To determine which arguments are decreasing, Idris looks at the patterns for the
Line 389: inputs in a definition. If a pattern is in the form of a data constructor, Idris considers
Line 390: the arguments in that pattern to be smaller than the input. In myReverse, for exam-
Line 391: ple, Idris doesn’t consider xs to be smaller than (xs ++ [x]), because (xs ++
Line 392: [x]) is not in the form of a data constructor.
Line 393: This restriction keeps the concept of decreasing argument simple for Idris to check.
Line 394: In general, Idris can’t tell whether the inputs to a function will always be smaller than
Line 395: the result.
Line 396: As you’ll see in section 10.2, you can work around this restriction by defining recur-
Line 397: sive views. 
Line 398: 3
Line 399: 5
Line 400: 1
Line 401: 2
Line 402: 6
Line 403: 4
Line 404: 3
Line 405: 5
Line 406: 1
Line 407: 2
Line 408: 6
Line 409: 4
Line 410: 1
Line 411: 3
Line 412: 5
Line 413: 2
Line 414: 4
Line 415: 6
Line 416: 1
Line 417: 2
Line 418: 3
Line 419: 4
Line 420: 5
Line 421: 6
Line 422: Original list
Line 423: Split into halves
Line 424: Sort each half
Line 425: Merge sorted halves
Line 426: Figure 10.4
Line 427: Sorting a list using merge 
Line 428: sort: split the list into two halves, sort 
Line 429: the halves, and then merge the sorted 
Line 430: halves back together
Line 431: 
Line 432: --- 페이지 293 ---
Line 433: 267
Line 434: Defining and using views
Line 435: If you have two sorted lists, you can merge them together using the merge function
Line 436: defined in the Prelude:
Line 437: Idris> :doc merge
Line 438: Prelude.List.merge : Ord a => List a -> List a -> List a
Line 439: Merge two sorted lists using the default ordering for the type
Line 440: of their elements.
Line 441: Note that it has a generic type and requires the Ord interface to be implemented for
Line 442: the element type of the list.
Line 443:  Assuming that the two input lists are sorted, merge will produce a sorted list of the
Line 444: elements in the input lists. For example, the lists in figure 10.4 would be merged as
Line 445: follows:
Line 446: Idris> merge [1,3,5] [2,4,6]
Line 447: [1, 2, 3, 4, 5, 6] : List Integer
Line 448: Listing 10.3 shows how you might ideally like to write a mergeSort function that sorts a
Line 449: list using the merge sort algorithm. Unfortunately, as it stands, this won’t work
Line 450: because (lefts ++ rights) isn’t a valid pattern.
Line 451: mergeSort : Ord a => List a -> List a
Line 452: mergeSort [] = []
Line 453: mergeSort [x] = [x]
Line 454: mergeSort (lefts ++ rights)
Line 455: = merge (mergeSort lefts) (mergeSort rights)
Line 456: Given an input list matched against a pattern, (lefts ++ rights), Idris can’t in gen-
Line 457: eral deduce what lefts and rights must be; indeed, there could be several reason-
Line 458: able possibilities if the input list has one or more elements. Here are a couple of
Line 459: examples:
Line 460: 
Line 461: [1] could match against (lefts ++ rights) with lefts as [1] and rights as [],
Line 462: or lefts as [] and rights as [1].
Line 463: 
Line 464: [1,2,3] could match against (lefts ++ rights) with lefts as [1] and rights
Line 465: as [2,3], or lefts as [1,2] and rights as [3], among many other possibilities.
Line 466: To match the patterns we want, as shown in listing 10.3, you’ll need to create a view of
Line 467: lists, SplitList, that gives the patterns you want. The following listing shows the defi-
Line 468: nition of SplitList and gives the type for its covering function, splitList.
Line 469: Listing 10.3
Line 470: Initial attempt at mergeSort with an invalid pattern (MergeSort.idr)
Line 471: An empty list is already sorted.
Line 472: A singleton list is already sorted.
Line 473: This pattern isn’t valid because ++ isn’t a 
Line 474: data constructor, but you’d like to extract 
Line 475: the left and right halves of the input.
Line 476: Recursively sorts the left and 
Line 477: right halves of the list, and 
Line 478: then merges the results into a 
Line 479: complete sorted list
Line 480: 
Line 481: --- 페이지 294 ---
Line 482: 268
Line 483: CHAPTER 10
Line 484: Views: extending pattern matching
Line 485:  
Line 486: data SplitList : List a -> Type where
Line 487: SplitNil : SplitList []
Line 488: SplitOne : SplitList [x]
Line 489: SplitPair : (lefts : List a) -> (rights : List a) ->
Line 490: SplitList (lefts ++ rights)
Line 491: splitList : (input : List a) ->
Line 492: SplitList input
Line 493: I’ll give a definition of the covering function, splitList, shortly. For now, note that as
Line 494: long as the implementation of splitList is total, you can be sure from its type that it
Line 495: gives valid patterns for empty lists, singleton lists, or concatenations of two lists. You
Line 496: don’t, however, have any guarantees in the type about how a list is split into pairs; in
Line 497: this case, you need to rely on the implementation to ensure that lefts and rights dif-
Line 498: fer in size by at most one.
Line 499: PRECISION OF SPLITPAIR
Line 500: In principle, you could make the type of SplitPair
Line 501: more precise and carry a proof that lefts and rights differ in size by at
Line 502: most one. In fact, the Idris library module Data.List.Views exports such a
Line 503: view, called SplitBalanced.
Line 504: You can implement mergeSort using the SplitList view as follows: 
Line 505: 1
Line 506: Type—Begin with the type and a skeleton definition: 
Line 507: mergeSort : Ord a => List a -> List a
Line 508: mergeSort input = ?mergeSort_rhs
Line 509:  2
Line 510: Define—To get the patterns you want, you’ll need to use the SplitList view
Line 511: you’ve just created. Add a with block and use the splitList covering function: 
Line 512: mergeSort : Ord a => List a -> List a
Line 513: mergeSort input with (splitList input)
Line 514: mergeSort input | with_pat = ?mergeSort_rhs
Line 515:  3
Line 516: Define—If you case-split on with_pat, you’ll get appropriate patterns for input
Line 517: arising from the types of the constructors to SplitList: 
Line 518: mergeSort : Ord a => List a -> List a
Line 519: mergeSort input with (splitList input)
Line 520: mergeSort [] | SplitNil = ?mergeSort_rhs_1
Line 521: mergeSort [x] | SplitOne = ?mergeSort_rhs_2
Line 522: mergeSort (lefts ++ rights) | (SplitPair lefts rights) = ?mergeSort_rhs_3
Line 523: 4
Line 524: Refine—You can complete the definition by filling in the right sides for each
Line 525: pattern, directly following the high-level description of the merge sort algo-
Line 526: rithm I gave at the start of this section: 
Line 527: mergeSort : Ord a => List a -> List a
Line 528: mergeSort input with (splitList input)
Line 529: mergeSort [] | SplitNil = []
Line 530: mergeSort [x] | SplitOne = [x]
Line 531: Listing 10.4
Line 532: A view of lists that gives patterns for empty lists, singleton lists, and 
Line 533: concatenating lists (MergeSort.idr)
Line 534: 
Line 535: --- 페이지 295 ---
Line 536: 269
Line 537: Defining and using views
Line 538: mergeSort (lefts ++ rights) | (SplitPair lefts rights)
Line 539: = merge (mergeSort lefts) (mergeSort rights)
Line 540: Before you can test mergeSort, you’ll need to implement the covering function
Line 541: splitList. The next listing gives a definition of splitList that returns a description
Line 542: of the empty list pattern, a singleton list pattern, or a pattern consisting of the concat-
Line 543: enation of two lists, where those lists differ in length by at most one.
Line 544: total
Line 545: splitList : (input : List a) -> SplitList input
Line 546: splitList input = splitListHelp input input
Line 547: where
Line 548: splitListHelp : List a -> (input : List a) -> SplitList input
Line 549: splitListHelp _ [] = SplitNil
Line 550: splitListHelp _ [x] = SplitOne
Line 551: splitListHelp (_ :: _ :: counter) (item :: items)
Line 552: = case splitListHelp counter items of
Line 553: SplitNil => SplitOne
Line 554: SplitOne {x} => SplitPair [item] [x]
Line 555: SplitPair lefts rights => SplitPair (item :: lefts) rights
Line 556: splitListHelp _ items = SplitPair [] items
Line 557: You build two (approximately) equally sized lists by using a second reference to the
Line 558: input list as a counter in a helper function, splitListHelp, as follows: 
Line 559: On each recursive call, the counter steps through two elements of the list. The
Line 560: pattern (_ :: _ :: counter) matches any list with at least two elements, where
Line 561: counter is a list containing all but the first two elements.
Line 562: When the counter reaches the end of the list (that is, fewer than two elements
Line 563: remain), you must have traversed half of the input.
Line 564: You can now try splitList and mergeSort at the REPL: 
Line 565: *MergeSort> splitList [1]
Line 566: SplitOne : SplitList [1]
Line 567: *MergeSort> splitList [1,2,3,4,5]
Line 568: SplitPair [1, 2] [3, 4, 5] : SplitList [1, 2, 3, 4, 5]
Line 569: *MergeSort> mergeSort [3,2,1]
Line 570: [1, 2, 3] : List Integer
Line 571: *MergeSort> mergeSort [5,1,4,3,2,6,8,7,9]
Line 572: [1, 2, 3, 4, 5, 6, 7, 8, 9] : List Integer
Line 573: Listing 10.5
Line 574: Defining a covering function for SplitList (MergeSort.idr)
Line 575: Adds the “total” flag so Idris 
Line 576: checks that the definition is total
Line 577: Uses a second reference to the list
Line 578: as a counter, which steps through
Line 579: the list two elements at a time
Line 580: The input is empty, so return
Line 581: SplitNil, which gives a
Line 582: pattern for the empty list.
Line 583: The input has one element, so 
Line 584: return SplitOne, which gives a 
Line 585: pattern for the singleton list.
Line 586: Recursively splits the list,
Line 587: moving the counter along
Line 588: two places in the list, and
Line 589: then adds the first element,
Line 590: item, to the first half
Line 591: There are fewer than two elements
Line 592: in the counter list, so put the
Line 593: remaining items in the second list.
Line 594: 
Line 595: --- 페이지 296 ---
Line 596: 270
Line 597: CHAPTER 10
Line 598: Views: extending pattern matching
Line 599: By defining a view that gives possible cases for the input list in terms of how it can be
Line 600: split in half, you can write a definition of mergeSort that directly implements the high-
Line 601: level description of the algorithm.
Line 602:  Like myReverse, however, Idris can’t tell whether mergeSort is total:
Line 603: *MergeSort> :total mergeSort
Line 604: Main.mergeSort is possibly not total due to:
Line 605: possibly not total due to recursive path:
Line 606: with block in Main.mergeSort, with block in Main.mergeSort
Line 607: Again, the problem is that Idris can’t tell that the recursive calls are guaranteed to be
Line 608: on smaller lists than the original input. In the next section, you’ll see how to address
Line 609: this problem by defining recursive views that describe the recursive structure of a
Line 610: function, as well as the patterns that define a function. 
Line 611: Exercises
Line 612: 1
Line 613: The TakeN view allows traversal of a list several elements at a time: 
Line 614: data TakeN : List a -> Type where
Line 615: Fewer : TakeN xs
Line 616: Exact : (n_xs : List a) -> TakeN (n_xs ++ rest)
Line 617: takeN : (n : Nat) -> (xs : List a) -> TakeN xs
Line 618: The Fewer constructor covers the case where there are fewer than n elements.
Line 619: Define the covering function takeN.
Line 620: To check that your definition works, you should be able to run the following
Line 621: function, which groups lists into sublists with n elements each:
Line 622: groupByN : (n : Nat) -> (xs : List a) -> List (List a)
Line 623: groupByN n xs with (takeN n xs)
Line 624: groupByN n xs | Fewer = [xs]
Line 625: groupByN n (n_xs ++ rest) | (Exact n_xs) = n_xs :: groupByN n rest
Line 626: Here’s an example: 
Line 627: *ex_10_1> groupByN 3 [1..10]
Line 628: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]] : List (List Integer)
Line 629: 2
Line 630: Use TakeN to define a function that splits a list into two halves by calculating its
Line 631: length: 
Line 632: halves : List a -> (List a, List a)
Line 633: If you have implemented this correctly, you should see the following: 
Line 634: *ex_10_1> halves [1..10]
Line 635: ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) : (List Integer, List Integer)
Line 636: *ex_10_1> halves [1]
Line 637: ([], [1]) : (List Integer, List Integer)
Line 638: Hint: Use div for dividing a Nat.
Line 639: 
Line 640: --- 페이지 297 ---
Line 641: 271
Line 642: Recursive views: termination and efficiency
Line 643: 10.2
Line 644: Recursive views: termination and efficiency
Line 645: The purpose of views is to give us new ways to match on data, using the with construct
Line 646: for a more concise syntax. When you write a function with a view, you use the follow-
Line 647: ing components:
Line 648: The original input data
Line 649: A view of the input data, where the view data type is parameterized by the input
Line 650: data
Line 651: A covering function for the view, which constructs an instance of the view for the
Line 652: input data
Line 653: Then, using the with construct, you can pattern-match on the view. Dependent pat-
Line 654: tern matching gives you informative patterns for the original data. You’ve seen two
Line 655: examples of this in the previous section: reversing a list, and splitting a list in half for
Line 656: merge sort. In both cases, however, Idris couldn’t tell that the resulting function was
Line 657: total. Moreover, when you reverse a list, the resulting function is inefficient because it
Line 658: has to reconstruct the view on every recursive call.
Line 659:  In this section, we’ll look at how to solve both these problems by defining recursive
Line 660: views for describing traversals of data structures. Furthermore, once we’ve defined a
Line 661: view, we can reuse it for any function that uses the same recursion pattern. The Idris
Line 662: library provides a number of useful views for traversals of data structures, and we’ll
Line 663: look at some example functions with some of these. First, though, we’ll improve the
Line 664: definition of myReverse.
Line 665: 10.2.1 “Snoc” lists: traversing a list in reverse
Line 666: A snoc list is a list where elements are added to the end of the list, rather than the
Line 667: beginning. We can define them as follows, as a generic data type:
Line 668: data SnocList ty = Empty | Snoc (SnocList ty) ty
Line 669: SNOC LIST TERMINOLOGY
Line 670: The name snoc list arises because the traditional
Line 671: name (originating with Lisp) for the operator that adds an element to the
Line 672: beginning of a list is cons. Therefore, the name for the operator that adds an
Line 673: element to the end of a list is snoc.
Line 674: Using SnocList, you traverse the elements in reverse order, because the element (of
Line 675: type ty) appears after the list (of type SnocList ty). You can easily produce a List
Line 676: from a SnocList where the elements are in reverse order:
Line 677: reverseSnoc : SnocList ty -> List ty
Line 678: reverseSnoc Empty = []
Line 679: reverseSnoc (Snoc xs x) = x :: reverseSnoc xs
Line 680: You can show the relationship between SnocList and List more precisely by parame-
Line 681: terizing SnocList over the equivalent List. The following listing shows how to define
Line 682: SnocList in this way.
Line 683: 
Line 684: --- 페이지 298 ---
Line 685: 272
Line 686: CHAPTER 10
Line 687: Views: extending pattern matching
Line 688:  
Line 689: data SnocList : List a -> Type where
Line 690: Empty : SnocList []
Line 691: Snoc : (rec : SnocList xs) -> SnocList (xs ++ [x])
Line 692: snocList : (xs : List a) -> SnocList xs
Line 693: This is very similar in structure to ListLast, which you defined in the previous sec-
Line 694: tion. The difference is that Snoc takes a recursive argument of type SnocList xs.
Line 695:  Here, SnocList is a recursive view, and snocList is its covering function. We’ll come
Line 696: to the definition of snocList shortly; first, let’s see how you can use this to implement
Line 697: myReverse:
Line 698: 1
Line 699: Type—Begin by defining a helper function that takes a list, input, and its equiv-
Line 700: alent SnocList: 
Line 701: myReverseHelper : (input : List a) -> SnocList input -> List a
Line 702: myReverseHelper input snoc = ?myReverseHelper_rhs
Line 703:  2
Line 704: Define—If you case-split on snoc, you’ll get corresponding patterns for input: 
Line 705: myReverseHelper : (input : List a) -> SnocList input -> List a
Line 706: myReverseHelper [] Empty = ?myReverseHelper_rhs_1
Line 707: myReverseHelper (xs ++ [x]) (Snoc rec) = ?myReverseHelper_rhs_2
Line 708:  3
Line 709: Refine—If the input is empty, you’ll return the empty list: 
Line 710: myReverseHelper : (input : List a) -> SnocList input -> List a
Line 711: myReverseHelper [] Empty = []
Line 712: myReverseHelper (xs ++ [x]) (Snoc rec) = ?myReverseHelper_rhs_2
Line 713:  4
Line 714: Refine, type—Otherwise, you’ll recursively reverse xs and add the item x to the
Line 715: front: 
Line 716: myReverseHelper : (input : List a) -> SnocList input -> List a
Line 717: myReverseHelper [] Empty = []
Line 718: myReverseHelper (xs ++ [x]) (Snoc rec) = x :: myReverseHelper xs ?snocrec
Line 719: There’s still a hole, ?snocrec, for the second argument in the recursive call. If
Line 720: you inspect it, you’ll see that you need the SnocList that represents xs: 
Line 721: a : Type
Line 722: xs : List a
Line 723: rec : SnocList xs
Line 724: x : a
Line 725: --------------------------------------
Line 726: snocrec : SnocList xs
Line 727: Listing 10.6
Line 728: The SnocList type, parameterized over the equivalent List 
Line 729: (SnocList.idr)
Line 730: Empty is equivalent to 
Line 731: the list represented by [].
Line 732: Given a SnocList equivalent to a
Line 733: list, xs, and an implicit value, x,
Line 734: Snoc builds a SnocList
Line 735: equivalent to xs ++ [x].
Line 736: Given a list, xs, snocList
Line 737: builds a SnocList that is
Line 738: equivalent to xs.
Line 739: 
Line 740: --- 페이지 299 ---
Line 741: 273
Line 742: Recursive views: termination and efficiency
Line 743:  5
Line 744: Refine—Fortunately, you already have a value, rec, of type SnocList xs, so you
Line 745: can use it directly to complete the definition: 
Line 746: myReverseHelper : (input : List a) -> SnocList input -> List a
Line 747: myReverseHelper [] Empty = []
Line 748: myReverseHelper (xs ++ [x]) (Snoc rec) = x :: myReverseHelper xs rec
Line 749: 6
Line 750: Define—Finally, you can define myReverse by building a SnocList and calling
Line 751: myReverseHelper: 
Line 752: myReverse : List a -> List a
Line 753: myReverse input = myReverseHelper input (snocList input)
Line 754: You can’t test this yet because you haven’t implemented snocList, but for now notice
Line 755: how this contrasts with the implementation of myReverse in section 10.1.4, using
Line 756: ListLast. The similarity is that you find the patterns for the input list by matching on
Line 757: a view of input. The difference is that the view is recursive, meaning that you don’t
Line 758: have to rebuild the view on each recursive call; you already have access to it.
Line 759:  The definition of myReverseHelper is total, because the SnocList argument is
Line 760: decreasing on each recursive call:
Line 761: *SnocList> :total myReverseHelper
Line 762: Main.myReverseHelper is Total
Line 763: It now remains to implement snocList. As long as you can implement snocList by
Line 764: traversing the list only once, you’ll have an implementation of myReverse that runs in
Line 765: linear time. The following listing shows an implementation of snocList that traverses
Line 766: the list only once, using a helper function with an accumulator to build the SnocList
Line 767: by adding one element at a time.
Line 768: snocListHelp : (snoc : SnocList input) -> (rest : List a) ->
Line 769: SnocList (input ++ rest)
Line 770: snocListHelp {input} snoc [] = rewrite appendNilRightNeutral input in snoc
Line 771: snocListHelp {input} snoc (x :: xs)
Line 772: = rewrite appendAssociative input [x] xs in
Line 773: snocListHelp (Snoc snoc {x}) xs
Line 774: snocList : (xs : List a) -> SnocList xs
Line 775: snocList xs = snocListHelp Empty xs
Line 776: The definition of snocList is slightly tricky, involving the rewrite construct (which
Line 777: you saw in chapter 8) to get the types in the correct form for building the SnocList.
Line 778: You’ll rewrite with the following functions from the Prelude:
Line 779: Listing 10.7
Line 780: Implementing the covering function snocList
Line 781: Appends an empty list to a 
Line 782: SnocList representing input
Line 783: Appends an element, x, to a
Line 784: SnocList representing input,
Line 785: and then appends the
Line 786: remaining elements, xs
Line 787: Initializes the SnocList as Empty
Line 788: and then calls snocListHelp to
Line 789: add xs an element at a time
Line 790: 
Line 791: --- 페이지 300 ---
Line 792: 274
Line 793: CHAPTER 10
Line 794: Views: extending pattern matching
Line 795: appendNilRightNeutral : (l : List a) -> l ++ [] = l
Line 796: appendAssociative : (l : List a) -> (c : List a) -> (r : List a) ->
Line 797: l ++ (c ++ r) = (l ++ c) ++ r
Line 798: As with any complex definition, it’s a good idea to try to understand it by replacing
Line 799: subexpressions of the definition with holes, and seeing what the types of those holes
Line 800: are. In this case, it’s also useful to remove the rewrite constructs and replace them
Line 801: with holes, to see how the types need rewriting: 
Line 802: snocListHelp : SnocList input -> (xs : List a) -> SnocList (input ++ xs)
Line 803: snocListHelp {input} snoc [] = ?rewriteNil snoc
Line 804: snocListHelp {input} snoc (x :: xs)
Line 805: = ?rewriteCons (snocListHelp (Snoc snoc {x}) xs)
Line 806: You should see the following types for rewriteNil and rewriteCons:
Line 807: rewriteNil : SnocList input -> SnocList (input ++ [])
Line 808: rewriteCons : SnocList ((input ++ [x]) ++ xs) -> SnocList (input ++ x :: xs)
Line 809: The good news is that once you’ve defined snocList, you can reuse it for any function
Line 810: that needs to traverse a list in reverse. Furthermore, as you’ll see shortly, a SnocList
Line 811: view is also defined in the Idris library, along with several others. 
Line 812: 10.2.2 Recursive views and the with construct
Line 813: You now have an implementation of myReverse that runs in linear time, because it tra-
Line 814: verses the list once to build the SnocList view and then traverses the SnocList view
Line 815: once to build the reversed list. You can also confirm that Idris believes it’s total:
Line 816: *SnocList> :total myReverse
Line 817: Main.myReverse is Total
Line 818: The resulting definition isn’t quite as concise as the previous definition of myReverse,
Line 819: however, because it doesn’t use the with construct: 
Line 820: myReverseHelper : (input : List a) -> SnocList input -> List a
Line 821: myReverseHelper [] Empty = []
Line 822: myReverseHelper (xs ++ [x]) (Snoc rec) = x :: myReverseHelper xs rec
Line 823: myReverse : List a -> List a
Line 824: myReverse input = myReverseHelper input (snocList input)
Line 825: Let’s see what happens if you try to do so:
Line 826: 1
Line 827: Type, define—Begin with the following skeleton definition: 
Line 828: myReverse : List a -> List a
Line 829: myReverse input with (snocList input)
Line 830: myReverse input | with_pat = ?myReverse_rhs
Line 831:  2
Line 832: Define—You can write the function by case splitting on with_pat to get the pos-
Line 833: sible patterns for input: 
Line 834: myReverse : List a -> List a
Line 835: myReverse input with (snocList input)
Line 836: 
Line 837: --- 페이지 301 ---
Line 838: 275
Line 839: Recursive views: termination and efficiency
Line 840: myReverse [] | Empty = ?myReverse_rhs_1
Line 841: myReverse (xs ++ [x]) | (Snoc rec) = ?myReverse_rhs_2
Line 842:  3
Line 843: Refine—Fill in the right side as before: 
Line 844: myReverse : List a -> List a
Line 845: myReverse input with (snocList input)
Line 846: myReverse [] | Empty = []
Line 847: myReverse (xs ++ [x]) | (Snoc rec) = x :: myReverse xs
Line 848: Unfortunately, this calls the top-level reverse function, which rebuilds the view
Line 849: using snocList input, so you have the same problem as before: 
Line 850: *SnocList> :total myReverse
Line 851: Main.myReverse is possibly not total due to:
Line 852: possibly not total due to recursive path:
Line 853: with block in Main.myReverse, with block in Main.myReverse
Line 854: 4
Line 855: Refine—Instead, when you make the recursive call, you can make the call
Line 856: directly to the with block, using the | notation on the right side: 
Line 857: myReverse : List a -> List a
Line 858: myReverse input with (snocList input)
Line 859: myReverse [] | Empty = []
Line 860: myReverse (xs ++ [x]) | (Snoc rec) = x :: myReverse xs | rec
Line 861: The call to myReverse xs | rec recursively calls myReverse, but bypasses the
Line 862: construction of snocList input and uses rec directly. The resulting definition
Line 863: is total, building the SnocList representation of input, and traversing that: 
Line 864: *SnocList> :total myReverse
Line 865: Main.myReverse is Total
Line 866: This also has the effect of making myReverse run in linear time.
Line 867: In practice, when you use the with construct, Idris introduces a new function defini-
Line 868: tion for the body of the with block, like the definition of myReverseHelper that you
Line 869: implemented manually earlier.
Line 870:  When you write myReverse xs | rec, this is equivalent to writing myReverseHelper
Line 871: xs rec in the earlier definition. But by using the with construct instead, Idris gener-
Line 872: ates an appropriate type for the helper function.
Line 873:  By using the with construct, you can pattern-match and traverse data structures in
Line 874: different ways, with the structure of the matching and traversal given by the type of a
Line 875: view. Moreover, because the views themselves are data structures, Idris can be sure that
Line 876: functions that traverse views are total. 
Line 877: 10.2.3 Traversing multiple arguments: nested with blocks
Line 878: When you write pattern-matching definitions, you often want to match on several
Line 879: inputs at once. So far, using the with construct, you’ve only been matching one value.
Line 880: But like any language construct, with blocks can be nested.
Line 881: 
Line 882: --- 페이지 302 ---
Line 883: 276
Line 884: CHAPTER 10
Line 885: Views: extending pattern matching
Line 886:  To see how this works, let’s define an isSuffix function:
Line 887: isSuffix : Eq a => List a -> List a -> Bool
Line 888: The result of isSuffix should be True if the list in the first argument is a suffix of the
Line 889: second argument. For example:
Line 890: *IsSuffix> isSuffix [7,8,9,10] [1..10]
Line 891: True : Bool
Line 892: *IsSuffix> isSuffix [7,8,9] [1..10]
Line 893: False : Bool
Line 894: You can define this function by traversing both lists in reverse, taking the following
Line 895: steps:
Line 896: 1
Line 897: Define—Start with the skeleton definition: 
Line 898: isSuffix : Eq a => List a -> List a -> Bool
Line 899: isSuffix input1 input2 = ?isSuffix_rhs
Line 900:  2
Line 901: Define, refine—Next, match on the first input, using snocList so that you pro-
Line 902: cess the last element first: 
Line 903: isSuffix : Eq a => List a -> List a -> Bool
Line 904: isSuffix input1 input2 with (snocList input1)
Line 905: isSuffix [] input2 | Empty = ?isSuffix_rhs_1
Line 906: isSuffix (xs ++ [x]) input2 | (Snoc rec) = ?isSuffix_rhs_2
Line 907: You can rename rec to xsrec, to indicate that it’s a recursive view of xs when
Line 908: reversed. Then, if the first list is empty, it’s trivially a suffix of the second list: 
Line 909: isSuffix : Eq a => List a -> List a -> Bool
Line 910: isSuffix input1 input2 with (snocList input1)
Line 911: isSuffix [] input2 | Empty = True
Line 912: isSuffix (xs ++ [x]) input2 | (Snoc xsrec) = ?isSuffix_rhs_2
Line 913:  3
Line 914: Define—Next, match on the second input, again using snocList to process the
Line 915: last element first. With the cursor over ?isSuffix_rhs_2, press Ctrl-Alt-W to
Line 916: add a nested with block: 
Line 917: isSuffix : Eq a => List a -> List a -> Bool
Line 918: isSuffix input1 input2 with (snocList input1)
Line 919: isSuffix [] input2 | Empty = True
Line 920: isSuffix (xs ++ [x]) input2 | (Snoc xsrec) with (snocList input2)
Line 921: isSuffix (xs ++ [x]) [] | (Snoc xsrec) | Empty = ?isSuffix_rhs_2
Line 922: isSuffix (xs ++ [x]) (ys ++ [y]) | (Snoc xsrec) | (Snoc ysrec)
Line 923: = ?isSuffix_rhs_3
Line 924: 4
Line 925: Refine—A non-empty list can’t be a suffix of an empty list, and if the last two ele-
Line 926: ments of a list are equal, you’ll recursively check the rest of the list: 
Line 927: isSuffix : Eq a => List a -> List a -> Bool
Line 928: isSuffix input1 input2 with (snocList input1)
Line 929: isSuffix [] input2 | Empty = True
Line 930: isSuffix (xs ++ [x]) input2 | (Snoc rec) with (snocList input2)
Line 931: 
Line 932: --- 페이지 303 ---
Line 933: 277
Line 934: Recursive views: termination and efficiency
Line 935: isSuffix (xs ++ [x]) [] | (Snoc rec) | Empty = False
Line 936: isSuffix (xs ++ [x]) (ys ++ [y]) | (Snoc rec) | (Snoc z)
Line 937: = if x == y then isSuffix xs ys | xsrec | ysrec
Line 938: else False
Line 939: Note that when you call isSuffix recursively, you pass both of the recursive view
Line 940: arguments, xsrec and ysrec, to save recomputing them unnecessarily.
Line 941: You can confirm that this definition is total by asking Idris at the REPL: 
Line 942: *IsSuffix> :total isSuffix
Line 943: Main.isSuffix is Total
Line 944: 10.2.4 More traversals: Data.List.Views
Line 945: In order to help you write total functions, the Idris library provides a number of views
Line 946: for traversing data structures. The Data.List.Views module provides several, includ-
Line 947: ing the SnocList view you’ve just seen.
Line 948:  For example, listing 10.8 shows the SplitRec view, which allows you to recursively
Line 949: traverse a list, processing one half at a time. This is similar to the SplitList view you
Line 950: saw in section 10.1.5, but with recursive traversals on the halves of the list.
Line 951: data SplitRec : List a -> Type where
Line 952: SplitRecNil : SplitRec []
Line 953: SplitRecOne : SplitRec [x]
Line 954: SplitRecPair : (lrec : Lazy (SplitRec lefts)) ->
Line 955: (rrec : Lazy (SplitRec rights)) ->
Line 956: SplitRec (lefts ++ rights)
Line 957: total splitRec : (xs : List a) -> SplitRec xs
Line 958: Listing 10.8
Line 959: The SplitRec view from Data.List.Views
Line 960: The Lazy annotation 
Line 961: means that the recursive 
Line 962: argument will only be 
Line 963: constructed when needed.
Line 964: SplitRecPair constructs 
Line 965: two halves of the input 
Line 966: list, recursively.
Line 967: The covering function is total, so you can
Line 968: use the view to write total functions.
Line 969: The Lazy generic type
Line 970: The Lazy type allows you to postpone a computation until the result is needed. For
Line 971: example, a variable of type Lazy Int is a computation that, when evaluated, will
Line 972: produce a value of type Int. Idris has the following two functions built-in: 
Line 973: Delay : a -> Lazy a
Line 974: Force : Lazy a -> a
Line 975: When type-checking, Idris will insert applications of Delay and Force implicitly, as
Line 976: required. Therefore, in practice, you can treat Lazy as an annotation that states that
Line 977: a variable will only be evaluated when its result is required. You’ll see the definition
Line 978: of Lazy in more detail in chapter 11.
Line 979: 
Line 980: --- 페이지 304 ---
Line 981: 278
Line 982: CHAPTER 10
Line 983: Views: extending pattern matching
Line 984: You can use SplitRec to reimplement mergeSort from section 10.1.5 as a total func-
Line 985: tion. The following listing shows our starting point.
Line 986: import Data.List.Views
Line 987: mergeSort : Ord a => List a -> List a
Line 988: mergeSort input = ?mergeSort_rhs
Line 989: You can implement mergeSort using the SplitRec view by taking the following steps:
Line 990: 1
Line 991: Define—Begin by adding a with block, to say you’d like to write the function by
Line 992: using the SplitRec view: 
Line 993: mergeSort : Ord a => List a -> List a
Line 994: mergeSort input with (splitRec input)
Line 995: mergeSort [] | SplitRecNil = ?mergeSort_rhs_1
Line 996: mergeSort [x] | SplitRecOne = ?mergeSort_rhs_2
Line 997: mergeSort (lefts ++ rights) | (SplitRecPair lrec rrec)
Line 998: = ?mergeSort_rhs_3
Line 999:  2
Line 1000: Refine—The inputs [] and [x] are already sorted: 
Line 1001: mergeSort : Ord a => List a -> List a
Line 1002: mergeSort input with (splitRec input)
Line 1003: mergeSort [] | SplitRecNil = []
Line 1004: mergeSort [x] | SplitRecOne = [x]
Line 1005: mergeSort (lefts ++ rights) | (SplitRecPair lrec rrec)
Line 1006: = ?mergeSort_rhs_3
Line 1007: 3
Line 1008: Refine—For the (lefts ++ rights) case, you can sort lefts and rights recur-
Line 1009: sively, and then merge the results: 
Line 1010: mergeSort : Ord a => List a -> List a
Line 1011: mergeSort input with (splitRec input)
Line 1012: mergeSort [] | SplitRecNil = []
Line 1013: mergeSort [x] | SplitRecOne = [x]
Line 1014: mergeSort (lefts ++ rights) | (SplitRecPair lrec rrec)
Line 1015: = merge (mergeSort lefts | lrec)
Line 1016: (mergeSort rights | rrec)
Line 1017: The | says that, in the recursive calls, you want to bypass constructing the view,
Line 1018: because you already have appropriate views for lefts and rights.
Line 1019: You can confirm that the new definition of mergeSort is total, and test it on some
Line 1020: examples:
Line 1021: *MergeSortView> :total mergeSort
Line 1022: Main.mergeSort is Total
Line 1023: *MergeSortView> mergeSort [3,2,1]
Line 1024: [1, 2, 3] : List Integer
Line 1025: *MergeSortView> mergeSort [5,1,4,3,2,6,8,7,9]
Line 1026: [1, 2, 3, 4, 5, 6, 7, 8, 9] : List Integer
Line 1027: Listing 10.9
Line 1028: Starting point for a total implementation of mergeSort, using SplitRec
Line 1029: (MergeSortView.idr)
Line 1030: Imports Data.List.Views 
Line 1031: to get access to SplitRec
Line 1032: 
Line 1033: --- 페이지 305 ---
Line 1034: 279
Line 1035: Recursive views: termination and efficiency
Line 1036: Exercises
Line 1037: These exercises use views defined in the Idris library in the modules
Line 1038: Data.List.Views, Data.Vect.Views, and Data.Nat.Views. For each view mentioned
Line 1039: in the exercises, use :doc to find out about the view and its covering function.
Line 1040:  For each of these exercises, make sure Idris considers your solution to be total.
Line 1041: 1
Line 1042: Implement an equalSuffix function using the SnocList view defined in
Line 1043: Data.List.Views. It should have the following type: 
Line 1044: equalSuffix : Eq a => List a -> List a -> List a
Line 1045: Its behavior should be to return the maximum equal suffix of the two input
Line 1046: lists. Here’s an example: 
Line 1047: *ex_10_2> equalSuffix [1,2,4,5] [1..5]
Line 1048: [4, 5] : List Integer
Line 1049: *ex_10_2> equalSuffix [1,2,4,5,6] [1..5]
Line 1050: [] : List Integer
Line 1051: *ex_10_2> equalSuffix [1,2,4,5,6] [1..6]
Line 1052: [4, 5, 6] : List Integer
Line 1053:  2
Line 1054: Implement mergeSort for vectors, using the SplitRec view defined in
Line 1055: Data.Vect.Views.
Line 1056:  3
Line 1057: Write a toBinary function that converts a Nat to a String containing a binary
Line 1058: representation of the Nat. You should use the HalfRec view defined in
Line 1059: Data.Nat.Views.
Line 1060: If you have a correct implementation, you should see this: 
Line 1061: *ex_10_2> toBinary 42
Line 1062: "101010" : String
Line 1063: *ex_10_2> toBinary 94
Line 1064: "1011110" : String
Line 1065: Hint: It’s okay to return an empty string if the input is Z.
Line 1066: 4
Line 1067: Write a palindrome function that returns whether a list is the same when tra-
Line 1068: versed forwards and backwards, using the VList view defined in Data
Line 1069: .List.Views.
Line 1070: If you have a correct implementation, you should see the following: 
Line 1071: *ex_10_2> palindrome (unpack "abccba")
Line 1072: True : Bool
Line 1073: *ex_10_2> palindrome (unpack "abcba")
Line 1074: True : Bool
Line 1075: *ex_10_2> palindrome (unpack "abcb")
Line 1076: False : Bool
Line 1077: Hint: The VList view allows you to traverse a list in linear time, processing the
Line 1078: first and last elements simultaneously and recursing on the middle of the list.
Line 1079: 
Line 1080: --- 페이지 306 ---
Line 1081: 280
Line 1082: CHAPTER 10
Line 1083: Views: extending pattern matching
Line 1084: 10.3
Line 1085: Data abstraction: hiding the structure 
Line 1086: of data using views
Line 1087: The views you’ve seen so far in this chapter allow you to inspect and traverse data
Line 1088: structures in ways beyond the default pattern matching, focusing in particular on
Line 1089: List. In a sense, views allow you to describe alternative interfaces for building pattern-
Line 1090: matching definitions:
Line 1091: Using SnocList, you can see how a list is constructed using [] and by adding a
Line 1092: single element with ++, rather than using [] and ::.
Line 1093: Using SplitRec, you can see how a list is constructed as an empty list, a single-
Line 1094: ton list, or a concatenation of a pair of lists.
Line 1095: That is, you can find out how a value was constructed by looking at the view, rather
Line 1096: than by looking directly at the constructors of that value. In fact, you often won’t need
Line 1097: to know what the data constructors of a value are to be able to use a view of a value.
Line 1098:  With this in mind, one use of views in practice is to hide the representation of data in
Line 1099: a module, while still allowing interactive type-driven development of functions that
Line 1100: use that data, by case splitting on a view of that data.
Line 1101: THE ORIGIN OF VIEWS
Line 1102: The idea of views was proposed by Philip Wadler for
Line 1103: Haskell in 1987, in his paper “Views: a way for pattern matching to cohabit
Line 1104: with data abstraction.” The example in this section is in the spirit of Wadler’s
Line 1105: paper, which contains several other examples of using views in practice. Views
Line 1106: as a programming idiom, using dependent types and a notation similar to
Line 1107: the with notation in Idris, was later proposed by Conor McBride and James
Line 1108: McKinna in their 2004 paper, “The view from the left.”
Line 1109: To conclude this chapter, we’ll look at this idea in action. We’ll revisit the data store
Line 1110: example that we implemented in chapters 4 and 6, hide the representation of the data
Line 1111: in an Idris module, and export only the following:
Line 1112: Schema descriptions, explaining the form of data in the store
Line 1113: A function for initializing a data store, empty
Line 1114: A function for adding an entry to the store, addToStore
Line 1115: A view for traversing the contents of the store, StoreView, along with its cover-
Line 1116: ing function, storeView
Line 1117: None of these require users of the module to know anything about the structure of
Line 1118: the store itself or the structure of the data contained within it.
Line 1119:  Before you implement a module and export the relevant definitions, though, we’ll
Line 1120: need to discuss briefly how Idris supports data abstraction in modules.
Line 1121: 10.3.1 Digression: modules in Idris
Line 1122: With the exception of a small example in chapter 2, the programs you’ve written in this
Line 1123: book have been self-contained in a single main module. As you write larger applications,
Line 1124: 
Line 1125: --- 페이지 307 ---
Line 1126: 281
Line 1127: Data abstraction: hiding the structure of data using views
Line 1128: however, you’ll need a way to organize code into smaller compilation units, and to con-
Line 1129: trol which definitions are exported from those units.
Line 1130:  The following listing shows a small Idris module that defines a Shape type and
Line 1131: exports it, along with its data constructors and a function to calculate the area of a
Line 1132: shape. 
Line 1133: module Shape
Line 1134: public export
Line 1135: data Shape = Triangle Double Double
Line 1136: | Rectangle Double Double
Line 1137: | Circle Double
Line 1138: private
Line 1139: rectangle_area : Double -> Double -> Double
Line 1140: rectangle_area width height = width * height
Line 1141: export
Line 1142: area : Shape -> Double
Line 1143: area (Triangle base height) = 0.5 * rectangle_area base height
Line 1144: area (Rectangle length height) = rectangle_area length height
Line 1145: area (Circle radius) = pi * radius * radius
Line 1146: Each name defined in this module has an export modifier that explains whether that
Line 1147: name is visible to other modules. An export modifier can be one of the following:
Line 1148: 
Line 1149: private—The name is not exported at all.
Line 1150: 
Line 1151: export—The name and type are exported, but not the definition. In the case of
Line 1152: a data type, this means the type constructor is exported, but the data construc-
Line 1153: tors are private.
Line 1154: 
Line 1155: public export—The name, type, and complete definition are exported. For
Line 1156: data types, this means the data constructors are exported. For functions, this
Line 1157: means the functions’ definitions are exported.
Line 1158: If there’s no export modifier on a function or data type definition, Idris treats it as
Line 1159: private. In the preceding example, this means that a module that imports Shape can
Line 1160: use the names Shape, Triangle, Rectangle, Circle, and area, but not rectangle_
Line 1161: area.
Line 1162: EXPORTING FUNCTION DEFINITIONS
Line 1163: Exporting a function’s definition as well as
Line 1164: its type (via public export) is important if you want to use the function’s
Line 1165: behavior in a type. In particular, this is important for type synonyms and type-
Line 1166: level functions, which we first used in chapter 6.
Line 1167: The next listing shows an alternative version of the Shape module that keeps the
Line 1168: details of the Shape data type abstract, exporting the type but not its constructors.
Line 1169: Listing 10.10
Line 1170: A module defining shapes and area calculations (Shape.idr)
Line 1171: Exports modifiers, 
Line 1172: saying whether the 
Line 1173: names are visible 
Line 1174: outside this module
Line 1175: 
Line 1176: --- 페이지 308 ---
Line 1177: 282
Line 1178: CHAPTER 10
Line 1179: Views: extending pattern matching
Line 1180:  
Line 1181: module Shape_abs
Line 1182: export
Line 1183: data Shape = Triangle Double Double
Line 1184: | Rectangle Double Double
Line 1185: | Circle Double
Line 1186: export
Line 1187: triangle : Double -> Double -> Shape
Line 1188: triangle = Triangle
Line 1189: export
Line 1190: rectangle : Double -> Double -> Shape
Line 1191: rectangle = Rectangle
Line 1192: export
Line 1193: circle : Double -> Shape
Line 1194: circle = Circle
Line 1195: Here, we’ve exported the functions triangle, rectangle, and circle for building
Line 1196: Shape. Rather than using the data constructors directly, other modules will need to
Line 1197: use these functions and won’t be able to pattern-match on the Shape type, because the
Line 1198: constructors aren’t exported.
Line 1199:  Using export modifiers, you can implement a module that implements the fea-
Line 1200: tures of a data store but only exports functions for creating a store, adding items, and
Line 1201: traversing the store, without exporting any details about the structure of the store. 
Line 1202: 10.3.2 The data store, revisited
Line 1203: To illustrate the role of views in data abstraction, we’ll create a module that implements
Line 1204: a data store, exporting functions for constructing the store. We’ll also implement a view
Line 1205: for inspecting and traversing the contents of the store.
Line 1206:  The following listing shows the DataStore.idr module. This is a slight variation
Line 1207: on the DataStore record you implemented in chapter 6.
Line 1208: module DataStore
Line 1209: import Data.Vect
Line 1210: infixr 5 .+.
Line 1211: public export
Line 1212: data Schema = SString | SInt | (.+.) Schema Schema
Line 1213: public export
Line 1214: SchemaType : Schema -> Type
Line 1215: SchemaType SString = String
Line 1216: SchemaType SInt = Int
Line 1217: SchemaType (x .+. y) = (SchemaType x, SchemaType y)
Line 1218: Listing 10.11
Line 1219: Exporting Shape as an abstract data type (Shape_abs.idr)
Line 1220: Listing 10.12
Line 1221: Data store, with a schema (DataStore.idr)
Line 1222: Exports the Shape data type, 
Line 1223: but not its constructors
Line 1224: Exports functions for 
Line 1225: building shapes, rather 
Line 1226: than their constructors
Line 1227: Exports Schema and all 
Line 1228: of its data constructors
Line 1229: The Schema type was defined 
Line 1230: for the data store 
Line 1231: implementation in chapter 6, 
Line 1232: along with SchemaType, 
Line 1233: which translates a Schema 
Line 1234: into an Idris type.
Line 1235: Exports SchemaType 
Line 1236: and its definition
Line 1237: 
Line 1238: --- 페이지 309 ---
Line 1239: 283
Line 1240: Data abstraction: hiding the structure of data using views
Line 1241: export
Line 1242: record DataStore (schema : Schema) where
Line 1243: constructor MkData
Line 1244: size : Nat
Line 1245: items : Vect size (SchemaType schema)
Line 1246: Rather than storing the schema as a field in the record, here you parameterize the
Line 1247: record by the data’s schema because you don’t intend to allow the schema to be
Line 1248: updated:
Line 1249: export
Line 1250: record DataStore (schema : Schema) where
Line 1251: constructor MkData
Line 1252: size : Nat
Line 1253: items : Vect size (SchemaType schema)
Line 1254: The syntax for a parameterized record declaration is similar to the syntax for an inter-
Line 1255: face declaration, with the parameters and their types listed after the record name.
Line 1256: This declaration gives rise to a DataStore type constructor with the following type:
Line 1257: DataStore : Schema -> Type
Line 1258: It also gives rise to functions for projecting the size of the store (size) and the entries
Line 1259: in the store (items) out of the record. The functions have the following types:
Line 1260: size : DataStore schema -> Nat
Line 1261: items : (rec : DataStore schema) -> Vect (size rec) (SchemaType schema)
Line 1262: Because the record has the export modifier export, the DataStore data type is visible
Line 1263: to other modules, but the size and items projection functions aren’t.
Line 1264:  Listing 10.13 shows three functions that other modules can use to create a new,
Line 1265: empty store with a specific schema (empty), or add a new entry to a store (addTo-
Line 1266: Store). Each of these functions has the export modifier export, meaning that other
Line 1267: modules can see their names and types but have no access to their definitions.
Line 1268: export
Line 1269: empty : DataStore schema
Line 1270: empty = MkData 0 []
Line 1271: export
Line 1272: addToStore : (value : SchemaType schema) -> (store : DataStore schema) ->
Line 1273: DataStore schema
Line 1274: addToStore value (MkData _ items) = MkData _ (value :: items)
Line 1275: To be able to use this module effectively, you’ll also need to traverse the entries in the
Line 1276: store. You can build the contents of a store using empty to create a new store and
Line 1277: addToStore to add a new entry. It would therefore be convenient to be able to use
Line 1278: Listing 10.13
Line 1279: Functions for accessing the store (DataStore.idr)
Line 1280: Exports DataStore, but not its 
Line 1281: constructor or any of its fields
Line 1282: The DataStore record is parameterized 
Line 1283: by the data schema.
Line 1284: 
Line 1285: --- 페이지 310 ---
Line 1286: 284
Line 1287: CHAPTER 10
Line 1288: Views: extending pattern matching
Line 1289: these as patterns to match the contents of a store. When you match on a store, you’ll
Line 1290: need to deal with the following two cases:
Line 1291: An empty case that matches a store with no contents
Line 1292: An addToStore value store case that matches a store where the first entry is
Line 1293: given by value, and the remaining items in the store are given by store
Line 1294: To match these cases, you can write a view of DataStore. 
Line 1295: 10.3.3 Traversing the store’s contents with a view
Line 1296: Listing 10.14 shows a StoreView view and its covering function, storeView. They allow
Line 1297: you to traverse the contents of a store by seeing how the store was constructed, either
Line 1298: with empty or addToStore.
Line 1299: public export
Line 1300: data StoreView : DataStore schema -> Type where
Line 1301: SNil : StoreView empty
Line 1302: SAdd : (rec : StoreView store) -> StoreView (addToStore value store)
Line 1303: storeViewHelp : (items : Vect size (SchemaType schema)) ->
Line 1304: StoreView (MkData size items)
Line 1305: storeViewHelp [] = SNil
Line 1306: storeViewHelp (val :: xs) = SAdd (storeViewHelp xs)
Line 1307: export
Line 1308: storeView : (store : DataStore schema) -> StoreView store
Line 1309: storeView (MkData size items) = storeViewHelp items
Line 1310: The StoreView view gives you access to the contents of the store by pattern matching
Line 1311: but hides its internal representation. To use the store, and to traverse its contents, you
Line 1312: don’t need to know anything about the internal representation.
Line 1313:  To illustrate this, let’s set up some test data and write some functions to inspect it.
Line 1314: The next listing defines a store and populates it with some test data, mapping planet
Line 1315: names to the name of the space probe that first visited the planet and the year of the
Line 1316: visit.1
Line 1317: import DataStore
Line 1318: testStore : DataStore (SString .+. SString .+. SInt)
Line 1319: testStore = addToStore ("Mercury", "Mariner 10", 1974)
Line 1320: (addToStore ("Venus", "Venera", 1961)
Line 1321: Listing 10.14
Line 1322: A view for traversing the entries in a store (DataStore.idr)
Line 1323: Listing 10.15
Line 1324: A datastore populated with some test data (TestStore.idr)
Line 1325: 1 We won’t, however, get into any debates about whether Pluto is a planet here.
Line 1326: You want to match on the constructors 
Line 1327: of StoreView when using the view, so 
Line 1328: export the data constructors.
Line 1329: There’s no export annotation, 
Line 1330: so Idris considers 
Line 1331: storeViewHelp to be private.
Line 1332: Exports the covering 
Line 1333: function so that 
Line 1334: other modules can 
Line 1335: build the view
Line 1336: 
Line 1337: --- 페이지 311 ---
Line 1338: 285
Line 1339: Data abstraction: hiding the structure of data using views
Line 1340: (addToStore ("Uranus", "Voyager 2", 1986)
Line 1341: (addToStore ("Pluto", "New Horizons", 2015)
Line 1342: empty)))
Line 1343: The following listing shows a basic traversal of the data store, returning a list of entries
Line 1344: in the store.
Line 1345: listItems : DataStore schema -> List (SchemaType schema)
Line 1346: listItems input with (storeView input)
Line 1347: listItems empty | SNil = []
Line 1348: listItems (addToStore value store) | (SAdd rec)
Line 1349: = value :: listItems store | rec
Line 1350: If you call showItems with the test data, you’ll see the following result:
Line 1351: *TestStore> listItems testStore
Line 1352: [("Mercury", "Mariner 10", 1974),
Line 1353: ("Venus", "Venera", 1961),
Line 1354: ("Uranus", "Voyager 2", 1986),
Line 1355: ("Pluto", "New Horizons", 2015)] : List (String, String, Int)
Line 1356: More interestingly, you might want to write functions that traverse the data store and
Line 1357: filter out certain entries. For example, suppose you want to get a list of the planets
Line 1358: that were first visited by a space probe during the twentieth century. You could do this
Line 1359: by writing the following function:
Line 1360: filterKeys : (test : SchemaType val_schema -> Bool) ->
Line 1361: DataStore (SString .+. val_schema) -> List String
Line 1362: You can think of a schema of the form (SString .+. val_schema) as giving a key-value
Line 1363: pair, where the key is a String and val_schema describes the form of the values.
Line 1364: Listing 10.16
Line 1365: A function to convert the store’s contents to a list of entries 
Line 1366: (TestStore.idr)
Line 1367: The application operator $
Line 1368: When expressions get deeply nested, as in the testStore definition, it can be dif-
Line 1369: ficult to keep track of the bracketing. The $ operator is an infix operator that applies
Line 1370: a function to an argument, and you can use it to reduce the need for bracketing.
Line 1371: Using it, you can write the following:
Line 1372: testStore = addToStore ("Mercury", "Mariner 10", 1974) $
Line 1373: addToStore ("Venus", "Venera", 1961) $
Line 1374: addToStore ("Uranus", "Voyager 2", 1986) $
Line 1375: addToStore ("Pluto", "New Horizons", 2015) $
Line 1376: empty
Line 1377: Writing $ is therefore equivalent to putting the rest of the expression in brackets. For
Line 1378: example, writing f x $ y z is exactly equivalent to writing f x (y z).
Line 1379: The | rec bypasses the building 
Line 1380: of the view on the recursive 
Line 1381: call, because rec is already a 
Line 1382: view of the rest of the store.
Line 1383: 
Line 1384: --- 페이지 312 ---
Line 1385: 286
Line 1386: CHAPTER 10
Line 1387: Views: extending pattern matching
Line 1388: Then, filterKeys will apply a function to the value in the pair, and if it returns True,
Line 1389: it will add the key to a list of String. This can find the planets that a probe visited
Line 1390: before the year 2000:
Line 1391: *TestStore> filterKeys (\x => snd x < 2000) testStore
Line 1392: ["Mercury", "Venus", "Uranus"] : List String
Line 1393: You can implement filterKeys using StoreView by taking the following steps:
Line 1394: 1
Line 1395: Type, define—Begin with a type and a skeleton definition: 
Line 1396: filterKeys : (test : SchemaType val_schema -> Bool) ->
Line 1397: DataStore (SString .+. val_schema) -> List String
Line 1398: filterKeys test input = ?filterKeys_rhs
Line 1399:  2
Line 1400: Define—You’ll define the function by traversing the store using StoreView, so
Line 1401: you can use the with construct to build the view, and case-split on it: 
Line 1402: filterKeys : (test : SchemaType val_schema -> Bool) ->
Line 1403: DataStore (SString .+. val_schema) -> List String
Line 1404: filterKeys test input with (storeView input)
Line 1405: filterKeys test empty | SNil = ?filterKeys_rhs_1
Line 1406: filterKeys test (addToStore value store) | (SAdd rec)
Line 1407: = ?filterKeys_rhs_2
Line 1408:  3
Line 1409: Refine—If the store is empty, there’s no value to apply the test to, so return an
Line 1410: empty list: 
Line 1411: filterKeys : (test : SchemaType val_schema -> Bool) ->
Line 1412: DataStore (SString .+. val_schema) -> List String
Line 1413: filterKeys test input with (storeView input)
Line 1414: filterKeys test empty | SNil = []
Line 1415: filterKeys test (addToStore value store) | (SAdd rec)
Line 1416: = ?filterKeys_rhs_2
Line 1417: 4
Line 1418: Refine—Otherwise, because of the schema of the data store, entry must itself be
Line 1419: a key-value pair: 
Line 1420: filterKeys : (test : SchemaType val_schema -> Bool) ->
Line 1421: DataStore (SString .+. val_schema) -> List String
Line 1422: filterKeys test input with (storeView input)
Line 1423: filterKeys test empty | SNil = []
Line 1424: filterKeys test (addToStore (key, value) store) | (SAdd rec)
Line 1425: = ?filterKeys_rhs_2
Line 1426: You’ll apply test to the value. If the result is True, you’ll keep the key and
Line 1427: recursively build the rest of the list. If the result is False, you’ll omit the key and
Line 1428: build the rest of the list:
Line 1429: filterKeys : (test : SchemaType val_schema -> Bool) ->
Line 1430: DataStore (SString .+. val_schema) -> List String
Line 1431: filterKeys test input with (storeView input)
Line 1432: filterKeys test empty | SNil = []
Line 1433: filterKeys test (addToStore (key, value) store) | (SAdd rec)
Line 1434: = if test value
Line 1435: 
Line 1436: --- 페이지 313 ---
Line 1437: 287
Line 1438: Data abstraction: hiding the structure of data using views
Line 1439: then key :: filterKeys test store | rec
Line 1440: else filterKeys test store | rec
Line 1441: You can try this function with some test filters:
Line 1442: *TestStore> filterKeys (\x => fst x == "Voyager 2") testStore
Line 1443: ["Uranus"] : List String
Line 1444: *TestStore> filterKeys (\x => snd x > 2000) testStore
Line 1445: ["Pluto"] : List String
Line 1446: *TestStore> filterKeys (\x => snd x < 2000) testStore
Line 1447: ["Mercury", "Venus", "Uranus"] : List String
Line 1448: For both showItems and filterKeys, you’ve written a function that traverses the con-
Line 1449: tents of the data store without knowing anything about the internal representation of
Line 1450: the store. In each case, you’ve used a view to deconstruct the data, rather than decon-
Line 1451: structing the data directly. If you were to change the internal representation in the
Line 1452: DataStore module, and correspondingly the implementation of storeView, the
Line 1453: implementations of showItems and filterKeys would remain unchanged. 
Line 1454: Exercises
Line 1455: 1
Line 1456: Write a getValues function that returns a list of all values in a DataStore. It should
Line 1457: have the following type: 
Line 1458: getValues : DataStore (SString .+. val_schema) ->
Line 1459: List (SchemaType val_schema)
Line 1460: You can test your definition by writing a function to set up a data store: 
Line 1461: testStore : DataStore (SString .+. SInt)
Line 1462: testStore = addToStore ("First", 1) $
Line 1463: addToStore ("Second", 2) $
Line 1464: empty
Line 1465: If you’ve implemented getValues correctly, you should see the following: 
Line 1466: *ex_10_3> getValues testStore
Line 1467: [1, 2] : List Int
Line 1468: 2
Line 1469: Define a view that allows other modules to inspect the abstract Shape data type in
Line 1470: listing 10.11. You should be able to use it to complete the following definition: 
Line 1471: area : Shape -> Double
Line 1472: area s with (shapeView s)
Line 1473: area (triangle base height) | STriangle = ?area_rhs_1
Line 1474: area (rectangle width height) | SRectangle = ?area_rhs_2
Line 1475: area (circle radius) | SCircle = ?area_rhs_3
Line 1476: If you have implemented this correctly, you should see the following: 
Line 1477: *ex_10_3> area (triangle 3 4)
Line 1478: 6.0 : Double
Line 1479: *ex_10_3> area (circle 10)
Line 1480: 314.1592653589793 : Double
Line 1481: 
Line 1482: --- 페이지 314 ---
Line 1483: 288
Line 1484: CHAPTER 10
Line 1485: Views: extending pattern matching
Line 1486: 10.4
Line 1487: Summary
Line 1488: A view is a dependent type that describes the possible forms of another data
Line 1489: type. Views take advantage of dependent pattern matching to allow you to
Line 1490: extend the forms of patterns you can use.
Line 1491: A covering function builds a view of a value. By convention, its name is the
Line 1492: name of the view with an initial lowercase letter.
Line 1493: The with construct allows you to use views directly, without defining an inter-
Line 1494: mediate function.
Line 1495: You can use views to define alternative traversals of data structures, such as
Line 1496: extracting the last element of a list instead of the first.
Line 1497: Recursive views help you write functions that are guaranteed to terminate, by
Line 1498: writing recursive functions that pattern-match on the view.
Line 1499: Idris provides several views for alternative traversals of List in the
Line 1500: Data.List.Views library. Similar libraries exist for Vect, Nat, and String.
Line 1501: You can hide the structure of data in a module, while still supporting interactive
Line 1502: type-driven programming with that data, by exporting views for traversing data
Line 1503: structures.