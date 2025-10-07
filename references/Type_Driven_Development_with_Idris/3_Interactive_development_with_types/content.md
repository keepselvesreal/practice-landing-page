Line 1: 
Line 2: --- 페이지 81 ---
Line 3: 55
Line 4: Interactive development
Line 5: with types
Line 6: You’ve now seen how to define simple functions, and how to structure these into
Line 7: complete programs. In this chapter, we’ll start a deeper exploration into type-
Line 8: driven development. First, we’ll look at how to write more-complex functions with
Line 9: existing types from the Prelude, such as lists. Then, we’ll look at using the Idris type
Line 10: system to give functions more-precise types.
Line 11:  In type-driven development, we follow the process of “type, define, refine.”
Line 12: You’ll see this process in action throughout this chapter as you first write the types
Line 13: and, as far as possible, always have a type-correct, if perhaps incomplete, definition
Line 14: of a function and refine it step by step until it’s complete. Each step will be broadly
Line 15: characterized as one of these three:
Line 16: Type—Either write a type to begin the process, or inspect the type of a hole to
Line 17: decide how to continue the process.
Line 18: This chapter covers
Line 19: Defining functions by pattern matching
Line 20: Type-driven interactive editing in Atom
Line 21: Adding precision to function types
Line 22: Practical programming with vectors
Line 23: 
Line 24: --- 페이지 82 ---
Line 25: 56
Line 26: CHAPTER 3
Line 27: Interactive development with types
Line 28: Define—Create the structure of a function definition either by creating an out-
Line 29: line of a definition or breaking it down into smaller components.
Line 30: Refine—Improve an existing definition either by filling in a hole or making its
Line 31: type more precise.
Line 32: In this chapter, I’ll introduce interactive development in the Atom text editor, which
Line 33: assists with this process. Atom provides an interactive editing mode that communi-
Line 34: cates with a running Idris system and uses types to help direct function development.
Line 35: Atom also provides some structural editing features and contextual information about
Line 36: functions with holes, and, when the types are precise enough, even completes large
Line 37: parts of functions for you. I’ll begin this chapter, therefore, by introducing the interac-
Line 38: tive editing mode in Atom.
Line 39: EDITOR MODES
Line 40: Although we’ll use Atom to edit Idris programs, the interac-
Line 41: tive features we’ll use are provided by Idris itself. The Atom integration works
Line 42: by communicating with an Idris process running in the background. This pro-
Line 43: cess is run as a child of the editor, so it’s independent of any REPLs you may
Line 44: have running. As such, it’s reasonably straightforward to add Idris support to
Line 45: other text editors, and similar editing modes currently exist for Emacs and
Line 46: Vim. In this book, we’ll stick to Atom for consistency, but each of the com-
Line 47: mands directly maps to corresponding commands in other editors.
Line 48: 3.1
Line 49: Interactive editing in Atom
Line 50: You saw in chapter 1 that Idris programs can contain holes, which stand for parts of a
Line 51: function definition that haven’t yet been written. This is one way in which programs
Line 52: can be developed interactively: you write an incomplete definition containing holes,
Line 53: check the types of the holes to see what Idris expects in each, and then continue by
Line 54: filling in the holes with more code. There are several additional ways in which Idris
Line 55: can help you by integrating interactive development features with a text editor: 
Line 56: Add definitions—Given a type declaration, Idris can add a skeleton definition of
Line 57: a function that satisfies that type.
Line 58: Case analysis—Given a skeleton function definition with arguments, Idris can use
Line 59: the types of those arguments to help define the function by pattern matching.
Line 60: Expression search—Given a hole with a precise enough type, Idris can try to find
Line 61: an expression that satisfies the hole’s type, refining the definition.
Line 62: In this section, we’ll begin writing some more-complex Idris functions, using its inter-
Line 63: active editing features to develop those functions, step by step, in a type-directed way.
Line 64: We’ll use the Atom text editor, because there’s an extension available for editing Idris
Line 65: programs, which can be installed directly from the default Atom distribution. The rest
Line 66: of this chapter assumes that you have the interactive Idris mode up and running. If
Line 67: not, follow the instructions in appendix A for installing Atom and the Idris mode.
Line 68: 
Line 69: --- 페이지 83 ---
Line 70: 57
Line 71: Interactive editing in Atom
Line 72: 3.1.1
Line 73: Interactive command summary
Line 74: Interactive editing in Atom involves a number of keyboard commands in the editor,
Line 75: which are summarized in table 3.1.
Line 76: COMMAND MNEMONICS
Line 77: For each command, the shortcut in Atom is to press
Line 78: Ctrl, Alt, and the first letter of the command.
Line 79: 3.1.2
Line 80: Defining functions by pattern matching
Line 81: All of the function definitions we’ve looked at so far have involved a single equation to
Line 82: define that function’s behavior. For example, in the previous chapter you wrote a
Line 83: function to calculate the lengths of every word in a list: 
Line 84: allLengths : List String -> List Nat
Line 85: allLengths strs = map length strs
Line 86: Here, you used functions defined in the Prelude (map and length) to inspect the list.
Line 87: At some stage, though, you’re going to need a more direct way to inspect values. After
Line 88: all, functions like map and length need to be defined themselves somehow!
Line 89:  In general, you define functions by pattern matching on the possible values of
Line 90: inputs to a function. For example, you can define a function to invert a Bool as follows:
Line 91: invert : Bool -> Bool
Line 92: invert False = True
Line 93: invert True = False
Line 94: The possible inputs of type Bool are True and False, so here you implement invert
Line 95: by listing the possible inputs and giving the corresponding outputs. Patterns can also
Line 96: contain variables, as illustrated by the following function, which returns "Empty" if
Line 97: Table 3.1
Line 98: Interactive editing commands in Atom
Line 99: Shortcut
Line 100: Command
Line 101: Description
Line 102: Ctrl-Alt-A
Line 103: Add definition
Line 104: Adds a skeleton definition for the name under the cursor
Line 105: Ctrl-Alt-C
Line 106: Case split
Line 107: Splits a definition into pattern-matching clauses for the 
Line 108: name under the cursor
Line 109: Ctrl-Alt-D
Line 110: Documentation
Line 111: Displays documentation for the name under the cursor
Line 112: Ctrl-Alt-L
Line 113: Lift hole
Line 114: Lifts a hole to the top level as a new function declaration
Line 115: Ctrl-Alt-M
Line 116: Match
Line 117: Replaces a hole with a case expression that matches on 
Line 118: an intermediate result
Line 119: Ctrl-Alt-R
Line 120: Reload
Line 121: Reloads and type-checks the current buffer
Line 122: Ctrl-Alt-S
Line 123: Search
Line 124: Searches for an expression that satisfies the type of the 
Line 125: hole name under the cursor
Line 126: Ctrl-Alt-T
Line 127: Type-check name
Line 128: Displays the type of the name under the cursor
Line 129: 
Line 130: --- 페이지 84 ---
Line 131: 58
Line 132: CHAPTER 3
Line 133: Interactive development with types
Line 134: given an empty list or "Non-empty" followed by the value of the tail if given a non-
Line 135: empty list:
Line 136: describeList : List Int -> String
Line 137: describeList [] = "Empty"
Line 138: describeList (x :: xs) = "Non-empty, tail = " ++ show xs
Line 139: Figure 3.1 illustrates how the patterns are matched in describeList for the inputs
Line 140: [1] (which is syntactic sugar for 1 :: []) and [2,3,4,5] (which is syntactic sugar for
Line 141: 2 :: 3 :: 4 :: 5 :: []).
Line 142: NAMING CONVENTIONS FOR LISTS
Line 143: Conventionally, when working with lists and
Line 144: list-like structures, Idris programmers use a name ending in “s” (to suggest a
Line 145: plural), and then use its singular to refer to individual elements. So, if you
Line 146: have a list called things, you might refer to an element of the list as thing.
Line 147: A function definition consists of one or more equations matching the possible inputs
Line 148: to that function. You can see how this works for lists if you implement allLengths by
Line 149: inspecting the list directly, instead of using map.
Line 150: allLengths : List String -> List Nat
Line 151: allLengths [] = []
Line 152: allLengths (x :: xs) = length x :: allLengths xs
Line 153: To see in detail how this definition is constructed, you’ll build it interactively in Atom.
Line 154: Each step can be broadly characterized as Type (creating or inspecting a type), Define
Line 155: (making a definition or breaking it down into separate clauses), or Refine (improving
Line 156: a definition by filling in a hole or making its type more precise).
Line 157: 1
Line 158: Type—First, start up Atom and create a WordLength.idr file containing the type
Line 159: declaration for allLengths. That’s only the following: 
Line 160: allLengths : List String -> List Nat
Line 161: Listing 3.1
Line 162: Calculating word lengths by pattern matching on the list (WordLength.idr)
Line 163: x = 1
Line 164: x = 2
Line 165: xs = []
Line 166: 1 :: []
Line 167: "Non-empty, tail = []"
Line 168: 2 :: 3 :: 4 :: 5 :: []
Line 169: "Non-empty, tail = [3,4,5]"
Line 170: xs = 3 :: 4 :: 5 :: []
Line 171: Figure 3.1
Line 172: Matching the pattern (x :: xs) for inputs [1] and [2,3,4,5]
Line 173: If the input list is empty, the 
Line 174: output list will also be empty.
Line 175: If the input list has a head element x and a tail
Line 176: xs, the output list will have the length of x as
Line 177: the head and then, recursively, a list of the
Line 178: lengths of xs as the tail.
Line 179: 
Line 180: --- 페이지 85 ---
Line 181: 59
Line 182: Interactive editing in Atom
Line 183: You should also start up an Idris REPL in a separate terminal so that you can
Line 184: type-check and test your definition: 
Line 185: $ idris WordLength.idr
Line 186: ____
Line 187: __
Line 188: _
Line 189: /
Line 190: _/___/ /____(_)____
Line 191: / // __
Line 192: / ___/ / ___/
Line 193: Version 1.0
Line 194: _/ // /_/ / /
Line 195: / (__
Line 196: )
Line 197: http://www.idris-lang.org/
Line 198: /___/\__,_/_/
Line 199: /_/____/
Line 200: Type :? for help
Line 201: Idris is free software with ABSOLUTELY NO WARRANTY.
Line 202: For details type :warranty.
Line 203: Holes: Main.allLengths
Line 204: *WordLength>
Line 205:  2
Line 206: Define—In Atom, move the cursor over the name allLengths and press Ctrl-Alt-A.
Line 207: This will add a skeleton definition, and your editor buffer should now contain
Line 208: the following: 
Line 209: allLengths : List String -> List Nat
Line 210: allLengths xs = ?allLengths_rhs
Line 211: The skeleton definition is always a clause with the appropriate number of argu-
Line 212: ments listed on the left side of the =, and with a hole on the right side. Idris uses
Line 213: various heuristics to choose initial names for the arguments. By convention,
Line 214: Idris chooses default names of xs, ys, or zs for Lists.
Line 215:  3
Line 216: Type—You can check the types of holes in Atom by pressing Ctrl-Alt-T with
Line 217: the cursor over the hole you want to check. If you check the type of the
Line 218: allLengths_rhs hole, you should see this: 
Line 219: xs : List String
Line 220: --------------------------------------
Line 221: allLengths_rhs : List Nat
Line 222:  4
Line 223: Define—You’ll write this definition by inspecting the list argument, named xs,
Line 224: directly. This means that for every form the list can take, you need to explain
Line 225: how to measure word lengths when it’s in that form. To tell the editor that you
Line 226: want to inspect the first argument, press Ctrl-Alt-C in Atom with the cursor over
Line 227: the variable xs in the first argument position. This expands the definition to
Line 228: give the two forms that the argument xs could take: 
Line 229: allLengths : List String -> List Nat
Line 230: allLengths [] = ?allLengths_rhs_1
Line 231: allLengths (x :: xs) = ?allLengths_rhs_2
Line 232: These are the two canonical forms of a list. That is, every list must be in one of
Line 233: these two forms: it can either be empty (in the form []), or it can be non-empty,
Line 234: containing a head element and the rest of the list (in the form (x :: xs)). It’s
Line 235: a good idea at this point to rename x and xs to something more meaningful
Line 236: than these default names: 
Line 237: allLengths : List String -> List Nat
Line 238: allLengths [] = ?allLengths_rhs_1
Line 239: allLengths (word :: words) = ?allLengths_rhs_2
Line 240: 
Line 241: --- 페이지 86 ---
Line 242: 60
Line 243: CHAPTER 3
Line 244: Interactive development with types
Line 245: In each case, there’s a new hole on the right side to fill in. You can check the
Line 246: types of these holes; type checking gives the expected return type and the types
Line 247: of any local variables. For example, if you check the type of allLengths_rhs_2,
Line 248: you’ll see the types of the local variables word and words, as well as the expected
Line 249: return type: 
Line 250: word : String
Line 251: words : List String
Line 252: --------------------------------------
Line 253: allLengths_rhs_2 : List Nat
Line 254:  5
Line 255: Refine—Idris has now told you which patterns are needed. Your job is to com-
Line 256: plete the definition by filling in the holes on the right side. In the case where
Line 257: the input is the empty list, the output is also the empty list, because there are no
Line 258: words for which to measure the length: 
Line 259: allLengths [] = []
Line 260: 6
Line 261: Refine—In the case where the input is non-empty, there’s a word as the first ele-
Line 262: ment (word) followed by the remainder of the list (words). You need to return a
Line 263: list with the length of word as its first element. For the moment, you can add a
Line 264: new hole (?rest) for the remainder of the list: 
Line 265: allLengths : List String -> List Nat
Line 266: allLengths [] = []
Line 267: allLengths (word :: words) = length word :: ?rest
Line 268: You can even test this incomplete definition at the REPL. Note that the REPL
Line 269: doesn’t reload files automatically, because it runs independently of the interac-
Line 270: tive editing in Atom, so you’ll need to reload explicitly using the :r command: 
Line 271: *WordLength> :r
Line 272: Type Checking ./WordLength.idr
Line 273: Holes: Main.rest
Line 274: *WordLength> allLengths ["Hello", "Interactive", "Editors"]
Line 275: 5 :: ?rest : List Nat
Line 276: For the hole rest, you need to calculate the lengths of the words in words. You
Line 277: can do this with a recursive call to allLengths, to complete the definition: 
Line 278: allLengths : List String -> List Nat
Line 279: allLengths [] = []
Line 280: allLengths (word :: words) = length word :: allLengths words
Line 281: You now have a complete definition, which you can test at the REPL after reloading: 
Line 282: *WordLength> :r
Line 283: Type Checking ./WordLength.idr
Line 284: *WordLength> allLengths ["Hello", "Interactive", "Editors"]
Line 285: [5, 11, 7] : List Nat
Line 286: It’s also a good idea to check whether Idris believes the definition is total. 
Line 287: *WordLength> :total allLengths
Line 288: Main.allLengths is Total
Line 289: 
Line 290: --- 페이지 87 ---
Line 291: 61
Line 292: Interactive editing in Atom
Line 293: Idris believes that allLengths is total because there are clauses for all possible well-
Line 294: typed inputs, and the argument to the recursive call to allLengths is smaller (that is,
Line 295: closer to the base case) than the input. 
Line 296: 3.1.3
Line 297: Data types and patterns
Line 298: When you press Ctrl-Alt-C in Atom with the cursor over a variable on the left side of a
Line 299: definition, it performs a case split on that variable, giving the possible patterns the vari-
Line 300: able can match. But where do these patterns come from?
Line 301:  Each data type has one or more constructors, which are the primitive ways of build-
Line 302: ing values in that data type and give the patterns that can be matched for that data
Line 303: type. For List, there are two: 
Line 304: 
Line 305: Nil, which constructs an empty list
Line 306: 
Line 307: ::, an infix operator that constructs a list from a head element and a tail
Line 308: Additionally, as you saw in chapter 2, there’s syntactic sugar for lists that allows a list to
Line 309: be written as a comma-separated list of values in square brackets. Hence, Nil can also
Line 310: be written as [].
Line 311:  For any data type, you can find the constructors and thus the patterns to match
Line 312: using :doc at the REPL prompt: 
Line 313: Idris> :doc List
Line 314: Data type Prelude.List.List : (elem : Type) -> Type
Line 315: Generic lists
Line 316: Constructors:
Line 317: Nil : List elem
Line 318: Empty list
Line 319: (::) : (x : elem) -> (xs : List elem) -> List elem
Line 320: Totality checking
Line 321: When Idris has successfully type-checked a function, it also checks whether it
Line 322: believes the function is total. If a function is total, it’s guaranteed to produce a
Line 323: result for any well-typed input, in finite time. Thanks to the halting problem, which we
Line 324: discussed in chapter 1, Idris can’t decide in general whether a function is total, but
Line 325: by analyzing a function’s syntax, it can decide that a function is total in many spe-
Line 326: cific cases.
Line 327: We’ll discuss totality checking in much more detail in chapters 10 and 11. For the
Line 328: moment, it’s sufficient to know that Idris will consider a function total if
Line 329: It has clauses that cover all possible well-typed inputs
Line 330: All recursive calls converge on a base case
Line 331: As you’ll see in chapter 11 in particular, the definition of totality also allows interac-
Line 332: tive programs that run indefinitely, such as servers and interactive loops, provided
Line 333: they continue to produce intermediate results in finite time.
Line 334: 
Line 335: --- 페이지 88 ---
Line 336: 62
Line 337: CHAPTER 3
Line 338: Interactive development with types
Line 339: A non-empty list, consisting of a head element and the rest of
Line 340: the list.
Line 341: infixr 7
Line 342: DOCUMENTATION IN ATOM
Line 343: You can get documentation directly in Atom
Line 344: by pressing Ctrl-Alt-D, with the cursor over the name for which you want
Line 345: documentation.
Line 346: For Bool, for example, :doc reveals that the constructors are False and True:
Line 347: Idris> :doc Bool
Line 348: Data type Prelude.Bool.Bool : Type
Line 349: Boolean Data Type
Line 350: Constructors:
Line 351: False : Bool
Line 352: True : Bool
Line 353: Therefore, if you write a function that takes a Bool as an input, you can provide
Line 354: explicit cases for the inputs False and True.
Line 355:  For example, to write the exclusive OR operator, you could follow these steps: 
Line 356: 1
Line 357: Type—Start by giving a type: 
Line 358: xor : Bool -> Bool -> Bool
Line 359:  2
Line 360: Define—Press Ctrl-Alt-A with the cursor over xor to add a skeleton definition: 
Line 361: xor : Bool -> Bool -> Bool
Line 362: xor x y = ?xor_rhs
Line 363:  3
Line 364: Define—Press Ctrl-Alt-C over the x to give the two possible cases for x: 
Line 365: xor : Bool -> Bool -> Bool
Line 366: xor False y = ?xor_rhs_1
Line 367: xor True y = ?xor_rhs_2
Line 368: 4
Line 369: Refine—Complete the definition by filling in the right sides: 
Line 370: xor : Bool -> Bool -> Bool
Line 371: xor False y = y
Line 372: xor True y = not y
Line 373: TYPE CHECKING IN ATOM
Line 374: While developing a function, and particularly when
Line 375: writing clauses by hand rather than using interactive editing features, it can
Line 376: be a good idea to type-check what you have so far. The Ctrl-Alt-R command
Line 377: rechecks the current buffer using the running Idris process. If it loads suc-
Line 378: cessfully, the Atom status bar will report “File loaded successfully.”
Line 379: The Nat type, which represents unbounded unsigned integers, is also defined by prim-
Line 380: itive constructors. In Idris, a natural number is defined as being either zero, or one
Line 381: more than (that is, the successor of) another natural number. 
Line 382: Idris> :doc Nat
Line 383: Data type Prelude.Nat.Nat : Type
Line 384: Natural numbers: unbounded, unsigned integers which can be
Line 385: pattern matched.
Line 386: 
Line 387: --- 페이지 89 ---
Line 388: 63
Line 389: Interactive editing in Atom
Line 390: Constructors:
Line 391: Z : Nat
Line 392: Zero
Line 393: S : Nat -> Nat
Line 394: Successor
Line 395: DATA TYPES AND CONSTRUCTORS
Line 396: Data types are defined in terms of their con-
Line 397: structors, as you’ll see in detail in chapter 4. The constructors of a data type
Line 398: are the primitive ways of building that data type, so in the case of Nat, every
Line 399: value of type Nat must be either zero or the successor of another Nat. The
Line 400: number 3, for example, is written in primitive form as S (S (S Z)). That is, it’s
Line 401: the successor (S) of 2 (written as S (S Z)).
Line 402: Therefore, if you write a function that takes a Nat as an input, you can provide explicit
Line 403: cases for the number zero (Z) or a number greater than zero (S k, where k is any non-
Line 404: negative number). For example, to write an isEven function that returns True if a nat-
Line 405: ural number input is divisible by 2, and returns False otherwise, you could define it
Line 406: recursively (if inefficiently) as follows: 
Line 407: 1
Line 408: Type—Start by giving a type: 
Line 409: isEven : Nat -> Bool
Line 410:  2
Line 411: Define—Press Ctrl-Alt-A to add a skeleton definition: 
Line 412: isEven : Nat -> Bool
Line 413: isEven k = ?isEven_rhs
Line 414: NAMING CONVENTIONS
Line 415: As a naming convention, Idris chooses k by default for
Line 416: variables of type Nat. Naming conventions can be set by the programmer
Line 417: when defining data types, and you’ll see how to do this in chapter 4. In any
Line 418: case, it’s usually a good idea to rename these variables to something more
Line 419: informative.
Line 420:  3
Line 421: Define—Press Ctrl-Alt-C over the k to give the two possible cases for k: 
Line 422: isEven : Nat -> Bool
Line 423: isEven Z = ?isEven_rhs_1
Line 424: isEven (S k) = ?isEven_rhs_2
Line 425: To complete the definition, you have to explain what to return when the input
Line 426: is zero (Z) or when the input is non-zero (if the input takes the form S k, then k
Line 427: is a variable standing for a number that’s one smaller than the input).
Line 428: 4
Line 429: Refine—Complete the definition by filling in the right sides: 
Line 430: isEven : Nat -> Bool
Line 431: isEven Z = True
Line 432: isEven (S k) = not (isEven k)
Line 433: You’ve defined this recursively. Zero is an even number, so you return True for
Line 434: the input Z. If a number is even, its successor is odd, and vice versa, so you
Line 435: return not (isEven k) for the input S k.
Line 436: 
Line 437: --- 페이지 90 ---
Line 438: 64
Line 439: CHAPTER 3
Line 440: Interactive development with types
Line 441: 3.2
Line 442: Adding precision to types: working with vectors
Line 443: In chapter 1, we discussed how having types as a first-class language construct allows us
Line 444: to define more-precise types. As one example, you saw how lists could be given more-
Line 445: precise types by including the number of elements in a list in its type, as well as the
Line 446: type of the elements. In Idris, a list that includes both the number and the type of ele-
Line 447: ments in its type is called a vector, defined as the data type Vect. The following listing
Line 448: shows some example vectors.
Line 449: import Data.Vect
Line 450: fourInts : Vect 4 Int
Line 451: fourInts = [0, 1, 2, 3]
Line 452: sixInts : Vect 6 Int
Line 453: sixInts = [4, 5, 6, 7, 8, 9]
Line 454: tenInts : Vect 10 Int
Line 455: tenInts = fourInts ++ sixInts
Line 456: Vect isn’t defined in the Prelude, but it can be made available by importing the
Line 457: Data.Vect library module. Modules are imported with an import statement at the top
Line 458: of a source file: 
Line 459: import Data.Vect
Line 460: PACKAGES: PRELUDE AND BASE
Line 461: Idris modules can be combined into packages,
Line 462: from which individual modules can be imported. The Prelude is defined in a
Line 463: package called prelude, from which all modules are imported automatically.
Line 464: Idris programs also have access to a package called base, which defines
Line 465: Listing 3.2
Line 466: Vectors: lists with lengths encoded in the type (Vectors.idr)
Line 467: Mutually defined functions
Line 468: Idris processes input files from top to bottom and requires types and functions to be
Line 469: defined before use. This is necessary due to complications that arise with dependent
Line 470: types, where the definition of a function can affect a type.
Line 471: It’s nevertheless sometimes useful to define two or more functions in terms of each
Line 472: other. This can be achieved in a mutual block. For example, you could define isEven
Line 473: in terms of an isOdd function, and vice versa: 
Line 474: mutual
Line 475: isEven : Nat -> Bool
Line 476: isEven Z = True
Line 477: isEven (S k) = isOdd k
Line 478: isOdd : Nat -> Bool
Line 479: isOdd Z = False
Line 480: isOdd (S k) = isEven k
Line 481: Appending vectors using ++ 
Line 482: also adds their lengths in the 
Line 483: type of the result.
Line 484: 
Line 485: --- 페이지 91 ---
Line 486: 65
Line 487: Adding precision to types: working with vectors
Line 488: several commonly useful data structures and algorithms including Vect, but
Line 489: from which modules must be imported explicitly. Up-to-date documentation
Line 490: for the packages distributed with Idris is available at www.idris-lang.org/
Line 491: documentation.
Line 492: 3.2.1
Line 493: Refining the type of allLengths
Line 494: To see how Vect works, you can refine the type of the allLengths function from sec-
Line 495: tion 3.1.2 to use a Vect instead of a List, and redefine the function.
Line 496:  To do so, create a new source file called WordLength_vec.idr containing only the
Line 497: line import Data.Vect, and load it into the REPL. You can then check the documenta-
Line 498: tion for Vect: 
Line 499: *WordLength_vec> :doc Vect
Line 500: Data type Data.Vect.Vect : Nat -> Type -> Type
Line 501: Vectors: Generic lists with explicit length in the type
Line 502: Constructors:
Line 503: Nil : Vect 0 a
Line 504: Empty vector
Line 505: (::) : (x : a) -> (xs : Vect k a) -> Vect (S k) a
Line 506: A non-empty vector of length S k, consisting of a head element
Line 507: and the rest of the list, of length k.
Line 508: infixr 7
Line 509: Notice that it has the same constructors as List, but they have different types that give
Line 510: explicit lengths. Lengths are given as Nat, because they can’t be negative: 
Line 511: The type of Nil explicitly states that the length is Z (displayed as the numeric lit-
Line 512: eral 0 here). 
Line 513: The type of :: explicitly states that the length is S k, given an element and a tail
Line 514: of length k.
Line 515: The same syntactic sugar applies as for List, translating a bracketed list of values such
Line 516: as [1, 2, 3] to a sequence of :: and Nil: 1 :: 2 :: 3 :: Nil, in this case. In fact, this
Line 517: syntactic sugar applies to any data type with constructors called Nil and ::.
Line 518: Overloading names
Line 519: The constructor names for both List and Vect are the same, Nil and ::. Names
Line 520: can be overloaded, provided that different things with the same name are defined in
Line 521: separate namespaces, which in practice usually means separate modules. Idris will
Line 522: infer the appropriate namespace from the context in which the name is used.
Line 523: You can explicitly indicate which of List or Vect is required using the:
Line 524: Idris> the (List _) ["Hello", "There"]
Line 525: ["Hello", "There"] : List String
Line 526: Idris> the (Vect _ _) ["Hello", "There"]
Line 527: ["Hello", "There"] : Vect 2 String
Line 528: 
Line 529: --- 페이지 92 ---
Line 530: 66
Line 531: CHAPTER 3
Line 532: Interactive development with types
Line 533: To define allLengths using a Vect, you can follow a similar procedure as when defin-
Line 534: ing it using List. The difference is that you must consider how the lengths of the
Line 535: input and output are related.
Line 536:  Figure 3.2 shows how, in the output list, there’s always an entry corresponding to
Line 537: an entry in the input list. Therefore, you can make it explicit in the type that the out-
Line 538: put vector has the same length as the input vector:
Line 539: allLengths : Vect len String -> Vect len Nat
Line 540: The len that appears in the input is a variable at the type level, standing for the length
Line 541: of the input. Because the output uses the same variable at the type level, it’s explicit in
Line 542: the type that the output has the same length as the input. Here’s how you can write
Line 543: the function:
Line 544: 1
Line 545: Type—Create an Atom buffer with the following contents to import Data.Vect
Line 546: and give the type of allLengths: 
Line 547: import Data.Vect
Line 548: allLengths : Vect len String -> Vect len Nat
Line 549:  2
Line 550: Define—As before, create a skeleton definition with Ctrl-Alt-A: 
Line 551: allLengths : Vect len String -> Vect len Nat
Line 552: allLengths xs = ?allLengths_rhs
Line 553:  3
Line 554: Define—As before, press Ctrl-Alt-C over the xs to tell Idris that you’d like to
Line 555: define the function by pattern matching on xs: 
Line 556: allLengths : Vect len String -> Vect len Nat
Line 557: allLengths [] = ?allLengths_rhs_1
Line 558: allLengths (x :: xs) = ?allLengths_rhs_2
Line 559: As before, it’s a good idea at this point to rename the variables x and xs to
Line 560: something more meaningful: 
Line 561: allLengths : Vect len String -> Vect len Nat
Line 562: (continued)
Line 563: The underscore (_) in the preceding expressions indicates to Idris that you would like
Line 564: it to infer a value for that argument. You can use _ in an expression whenever there’s
Line 565: only one valid value that would stand for that expression. You’ll see more about this
Line 566: in section 3.4.
Line 567: "Hot"
Line 568: 3
Line 569: Vect 4 String
Line 570: Vect 4 Nat
Line 571: "Dog"
Line 572: 3
Line 573: "Jumping"
Line 574: 7
Line 575: "Frog"
Line 576: 4
Line 577: Figure 3.2
Line 578: Calculating the lengths of words in a 
Line 579: list. Notice that each input has a corresponding 
Line 580: output, so the length of the output vector is always 
Line 581: the same as the length of the input vector.
Line 582: 
Line 583: --- 페이지 93 ---
Line 584: 67
Line 585: Adding precision to types: working with vectors
Line 586: allLengths [] = ?allLengths_rhs_1
Line 587: allLengths (word :: words) = ?allLengths_rhs_2
Line 588:  4
Line 589: Type—If you now inspect the types of the holes allLengths_rhs_1 and
Line 590: allLengths_rhs_2, you’ll see more information than in the List version,
Line 591: because the types are more precise. For example, in allLengths_rhs_1 you can
Line 592: see that the only valid result is a vector with zero elements: 
Line 593: --------------------------------------
Line 594: allLengths_rhs_1 : Vect 0 Nat
Line 595: In allLengths_rhs_2 you can see how the lengths of the pattern variables and
Line 596: output relate to each other, given some natural number n: 
Line 597: word : String
Line 598: k : Nat
Line 599: words : Vect k String
Line 600: --------------------------------------
Line 601: allLengths_rhs_2 : Vect (S k) Nat
Line 602: That is, in the pattern (word :: words), word is a String, words is a vector of
Line 603: kStrings, and for the output you need to provide a vector of Nat of length 1 + k,
Line 604: represented as S k.
Line 605:  5
Line 606: Refine—For allLengths_rhs_1, there’s only one vector that has length zero,
Line 607: which is the empty vector, so there’s only one value you can use to refine the
Line 608: definition by filling in the hole: 
Line 609: allLengths : Vect len String -> Vect len Nat
Line 610: allLengths [] = []
Line 611: allLengths (word :: words) = ?allLengths_rhs_2
Line 612:  6
Line 613: Refine—For allLengths_rhs_2, the required type is Vect (S k) Nat, so the
Line 614: result must be a non-empty vector (using ::). Also, you can make a value of
Line 615: type Vect k Nat by calling allLengths recursively. You can leave a hole for the
Line 616: first element in the resulting list, refining the definition by hand as follows: 
Line 617: allLengths : Vect len String -> Vect len Nat
Line 618: allLengths [] = []
Line 619: allLengths (word :: words) = ?wordlen :: allLengths words
Line 620: You still have one hole in this result, ?wordlen, which will be the length of the
Line 621: first word: 
Line 622: word : String
Line 623: k : Nat
Line 624: words : Vect k String
Line 625: --------------------------------------
Line 626: wordlen : Nat
Line 627: 7
Line 628: Refine—To complete the definition, fill in the remaining hole by calculating the
Line 629: length of the word x: 
Line 630: allLengths : Vect len String -> Vect len Nat
Line 631: allLengths [] = []
Line 632: allLengths (word :: words) = length word :: allLengths words
Line 633: 
Line 634: --- 페이지 94 ---
Line 635: 68
Line 636: CHAPTER 3
Line 637: Interactive development with types
Line 638: The more precise type, describing how the lengths of the input and output relate,
Line 639: means that the interactive editing mode can tell you more about the expressions
Line 640: you’re looking for. You can also be more confident that the program behaves as
Line 641: intended by ruling out any program that doesn’t preserve length by type-checking.
Line 642: NAT AND DATA STRUCTURES
Line 643: You might notice a direct correspondence
Line 644: between the constructors of Vect and the constructors of Nat. When you add
Line 645: an element to a Vect with ::, you add an S constructor to its length. In prac-
Line 646: tice, capturing the size of data structures like this is a very common use of Nat.
Line 647: To illustrate how the more precise type rules out some incorrect programs, consider
Line 648: the following implementation of allLengths, using List instead of Vect: 
Line 649: allLengths : List String -> List Nat
Line 650: allLengths xs = []
Line 651: This is well typed and it will be accepted by Idris, but it won’t work as intended
Line 652: because there’s no guarantee that the output list has an entry corresponding to each
Line 653: entry in the input. On the other hand, the following program with the more precise
Line 654: type is not well typed and will not be accepted by Idris: 
Line 655: allLengths : Vect n String -> Vect n Nat
Line 656: allLengths xs = []
Line 657: This results in the following type error, which states that an empty vector was given
Line 658: when a vector of length n was needed: 
Line 659: WordLength_vec.idr:4:14:When checking right hand side of allLengths:
Line 660: Type mismatch between
Line 661: Vect 0 Nat (Type of [])
Line 662: and
Line 663: Vect n Nat (Expected type)
Line 664: As with the previous List-based version of allLengths, you can check that your new
Line 665: definition is total at the REPL:
Line 666: *WordLength_vec> :total allLengths
Line 667: Main.allLengths is Total
Line 668: If, for example, you remove the case for the empty list, you have a definition that is
Line 669: well typed but partial:
Line 670: allLengths : Vect len String -> Vect len Nat
Line 671: allLengths (word :: words) = length word :: allLengths words
Line 672: When you check this for totality, you’ll see this:
Line 673: *WordLength_vec> :total allLengths
Line 674: Main.allLengths is not total as there are missing cases
Line 675: 
Line 676: --- 페이지 95 ---
Line 677: 69
Line 678: Adding precision to types: working with vectors
Line 679: 3.2.2
Line 680: Type-directed search: automatic refining
Line 681: After step 3 in the previous section, you had the patterns for allLengths and holes for
Line 682: the right sides, which you provided by refining directly: 
Line 683: allLengths : Vect n String -> Vect n Nat
Line 684: allLengths [] = ?allLengths_rhs_1
Line 685: allLengths (word :: words) = ?allLengths_rhs_2
Line 686: Take another look at the types and the local variables for the allLengths_rhs_1 and
Line 687: allLengths_rhs_2 holes: 
Line 688: --------------------------------------
Line 689: allLengths_rhs_1 : Vect 0 Nat
Line 690: word : String
Line 691: k : Nat
Line 692: words : Vect k String
Line 693: --------------------------------------
Line 694: allLengths_rhs_2 : Vect (S k) Nat
Line 695: By looking carefully at the types, you could see how to construct values to fill these
Line 696: holes. But not only do you have more information here, so does Idris!
Line 697:  Given enough information in the type, Idris can search for a valid expression that
Line 698: satisfies the type. In Atom, press Ctrl-Alt-S over the allLengths_rhs_1 hole, and you
Line 699: should see that the definition has changed: 
Line 700: allLengths : Vect n String -> Vect n Nat
Line 701: allLengths [] = []
Line 702: allLengths (word :: words) = ?allLengths_rhs_2
Line 703: Because there’s only one possible value for a vector of length zero, Idris has refined
Line 704: this automatically.
Line 705:  You can also try an expression search on the allLengths_rhs_2 hole. Press Ctrl-
Line 706: Alt-S with the cursor over allLengths_rhs_2, and you should see this: 
Line 707: Totality annotations
Line 708: For added confidence in a function’s correctness, you can annotate in the source
Line 709: code that a function must be total. For example, you can write this:
Line 710: total allLengths : Vect len String -> Vect len Nat
Line 711: allLengths [] = []
Line 712: allLengths (word :: words) = length word :: allLengths words
Line 713: The total keyword before the type declaration means that Idris will report an error
Line 714: if the definition isn’t total. For example, if you remove the allLengths [] case, this
Line 715: is what Idris will report:
Line 716: WordLength_vec.idr:5:1:
Line 717: Main.allLengths is not total as there are missing cases
Line 718: 
Line 719: --- 페이지 96 ---
Line 720: 70
Line 721: CHAPTER 3
Line 722: Interactive development with types
Line 723: allLengths : Vect n String -> Vect n Nat
Line 724: allLengths [] = []
Line 725: allLengths (word :: words) = 0 :: allLengths words
Line 726: The required type was Vect (S k) Nat so, as before, Idris realized that the only possi-
Line 727: ble result would be a non-empty vector. It also realized that it could find a value of
Line 728: type Vect k Nat by calling allLengths recursively on words.
Line 729:  For the Nat at the head of the vector, Idris has found the first value that satisfies
Line 730: the type, 0, but this isn’t exactly what you want, so you can replace it with a hole—
Line 731: ?vecthead: 
Line 732: allLengths : Vect n String -> Vect n Nat
Line 733: allLengths [] = []
Line 734: allLengths (word :: words) = ?vecthead :: allLengths words
Line 735: Checking the type of ?vecthead confirms that you’re looking for a Nat: 
Line 736: word : String
Line 737: k : Nat
Line 738: words : Vect k String
Line 739: --------------------------------------
Line 740: vecthead : Nat
Line 741: As before, you can complete the definition by filling this hole with length word. So,
Line 742: not only does the more precise type give you more confidence in the correctness of
Line 743: the program and give you more information when writing the program, it also gives
Line 744: Idris some information, allowing it to write a good bit of the program for you. 
Line 745: 3.2.3
Line 746: Type, define, refine: sorting a vector
Line 747: For all the functions you’ve written so far in this chapter, you’ve followed this process: 
Line 748: 1
Line 749: Write a type.
Line 750:  2
Line 751: Create a skeleton definition.
Line 752:  3
Line 753: Pattern match on an argument.
Line 754: 4
Line 755: Fill in the holes on the right side with a combination of type-driven expression
Line 756: search and refining holes by hand.
Line 757: Usually, there’s a little more work to do, however. For example, you may find you need
Line 758: to create additional helper functions, inspect intermediate results, or refine the type
Line 759: you initially gave for a function.
Line 760:  You can see this in practice by creating a function that returns a sorted version of
Line 761: an input vector. You can use insertion sort, which is a simple sorting algorithm that’s
Line 762: easily implemented in a functional style, informally described as follows: 
Line 763: Given an empty vector, return an empty vector.
Line 764: Given the head and tail of a vector, sort the tail of the vector and then insert the
Line 765: head into the sorted tail such that the result remains sorted.
Line 766: 
Line 767: --- 페이지 97 ---
Line 768: 71
Line 769: Adding precision to types: working with vectors
Line 770: You can write this interactively, beginning with the skeleton definition shown in listing
Line 771: 3.3. Open an Atom buffer and put this code into a file called VecSort.idr. Remember
Line 772: that you can create the skeleton definition of insSort from the type with Ctrl-Alt-A.
Line 773: import Data.Vect
Line 774: insSort : Vect n elem -> Vect n elem
Line 775: insSort xs = ?insSort_rhs
Line 776: As you work through this process, I recommend that you inspect the types of each of
Line 777: the holes that arise using Ctrl-Alt-T, and ensure that you understand the types of the
Line 778: variables and the holes.
Line 779: DEVELOPMENT WORKFLOW
Line 780: It’s typically useful to have an Atom window open
Line 781: for interactively editing a file, as well as a terminal window with a REPL open
Line 782: for testing, evaluation, checking documentation, and so on.
Line 783: Having written the type for this function, implement it by doing the following: 
Line 784: 1
Line 785: Define—Case-split on xs with Ctrl-Alt-C, leading to this: 
Line 786: insSort : Vect n elem -> Vect n elem
Line 787: insSort [] = ?insSort_rhs_1
Line 788: insSort (x :: xs) = ?insSort_rhs_2
Line 789:  2
Line 790: Refine—Try an expression search on ?insSort_rhs_1, leading to this: 
Line 791: insSort : Vect n elem -> Vect n elem
Line 792: insSort [] = []
Line 793: insSort (x :: xs) = ?insSort_rhs_2
Line 794: A sorted empty vector is itself an empty vector, as expected.
Line 795:  3
Line 796: Refine—Trying an expression search on ?insSort_rhs_2 is, unfortunately, less
Line 797: effective: 
Line 798: insSort : Vect n elem -> Vect n elem
Line 799: insSort [] = []
Line 800: insSort (x :: xs) = x :: xs
Line 801: Although Idris knows how long the vector should be, and it has local variables
Line 802: of the correct types, the overall type of insSort isn’t precise enough for Idris to
Line 803: fill in the hole with the program you intend.
Line 804: EXPRESSION SEARCH
Line 805: As this example demonstrates, although expression
Line 806: search can often lead you to a valid function, it’s not a substitute for under-
Line 807: standing how the program works! You need to understand the algorithm, but
Line 808: you can use expression search to help fill in the details.
Line 809: Listing 3.3
Line 810: A skeleton definition of insSort on vectors with an initial type 
Line 811: (VecSort.idr)
Line 812: This type explicitly states that the 
Line 813: output must have the same length as 
Line 814: the input. The element type, elem, is 
Line 815: given by a type-level variable, so it 
Line 816: stands for any type.
Line 817: 
Line 818: --- 페이지 98 ---
Line 819: 72
Line 820: CHAPTER 3
Line 821: Interactive development with types
Line 822:  4
Line 823: Define—When you’re writing a function over a recursive data type, it’s often
Line 824: effective to make recursive calls to the recursive parts of the structure. Here,
Line 825: you can sort the tail with a recursive call to insSort xs and bind the result to a
Line 826: locally defined variable: 
Line 827: insSort : Vect n elem -> Vect n elem
Line 828: insSort [] = []
Line 829: insSort (x :: xs) = let xsSorted = insSort xs in
Line 830: ?insSort_rhs_2
Line 831:  5
Line 832: Type—In ?insSort_rhs_2 you’re going to insert the head x into the sorted tail,
Line 833: xsSorted. Because this is going to be a little more complex, you can lift the
Line 834: hole to a top-level definition by pressing Ctrl-Alt-L with the cursor over
Line 835: ?insSort_rhs_2, which leads to the following: 
Line 836: insSort_rhs_2 : (x : elem) -> (xs : Vect k elem) ->
Line 837: (xsSorted : Vect k elem) ->
Line 838: Vect (S k) elem
Line 839: insSort : Vect n elem -> Vect n elem
Line 840: insSort [] = []
Line 841: insSort (x :: xs) = let xsSorted = insSort xs in
Line 842: insSort_rhs_2 x xs xsSorted
Line 843: This has created a new top-level function with a new type but no implementa-
Line 844: tion, and it has replaced the hole with a call to the new function. The argu-
Line 845: ments to the new function are the local variables that were in scope in the hole
Line 846: ?insSort_rhs_2.
Line 847:  6
Line 848: Refine—Once you realize that the job of the new function is to insert x into the
Line 849: xsSorted vector, you can edit the name and type of insSort_rhs_2 to reflect
Line 850: this. You can remove the arguments that you aren’t going to need: 
Line 851: insert : (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 852: insSort : Vect n elem -> Vect n elem
Line 853: insSort [] = []
Line 854: insSort (x :: xs) = let xsSorted = insSort xs in
Line 855: insert x xsSorted
Line 856: LIFTING DEFINITIONS
Line 857: When lifting a definition with Ctrl-Alt-L, Idris will gener-
Line 858: ate a new definition with the same name as the hole, using all of the local vari-
Line 859: ables in the generated type. In this case, you know you aren’t going to need
Line 860: all of them, so you can edit out the unnecessary xs argument. 
Line 861:  7
Line 862: Define—You now have to define insert. Again, create a skeleton definition: 
Line 863: insert : (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 864: insert x xsSorted = ?insert_rhs
Line 865: Then case-split on xsSorted, leading to this: 
Line 866: insert : (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 867: insert x [] = ?insert_rhs_1
Line 868: insert x (y :: xs) = ?insert_rhs_2
Line 869: 
Line 870: --- 페이지 99 ---
Line 871: 73
Line 872: Adding precision to types: working with vectors
Line 873:  8
Line 874: Refine—An expression search on insert_rhs_1 leads to the following: 
Line 875: insert : (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 876: insert x [] = [x]
Line 877: insert x (y :: xs) = ?insert_rhs_2
Line 878: This works because Idris knows it’s looking for a vector with one element of
Line 879: type elem, and the only thing available with type elem is x.
Line 880:  9
Line 881: Refine—For the (y :: xs) case, with the hole ?insert_rhs_2, you have a prob-
Line 882: lem. There are two cases to consider: 
Line 883: If x < y, the result should be x :: y :: xs, because the result won’t be
Line 884: ordered if x is inserted after y.
Line 885: Otherwise, the result should begin with y, and then have x inserted into the
Line 886: tail xs.
Line 887: Your problem is that you know nothing about the element type elem. You need
Line 888: to constrain it so that you know you can compare elements of type elem. You
Line 889: can refine the type of insert (and correspondingly insSort) so that you can
Line 890: do the necessary comparison: 
Line 891: insert : Ord elem =>
Line 892: (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 893: insert x [] = [x]
Line 894: insert x (y :: xs) = ?insert_rhs_2
Line 895: insSort : Ord elem => Vect n elem -> Vect n elem
Line 896: insSort [] = []
Line 897: insSort (x :: xs) = let xsSorted = insSort xs in
Line 898: insert x xsSorted
Line 899: Remember from chapter 2 that you constrain generic types by placing con-
Line 900: straints such as Ord elem before => in the type. You’ll see more about this in
Line 901: chapter 7.
Line 902:  10
Line 903: Define—You now need to check x < y and act on the result. One way to do this
Line 904: is with an if...then...else construct: 
Line 905: insert : Ord elem =>
Line 906: (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 907: insert x [] = [x]
Line 908: insert x (y :: xs) = if x < y then x :: y :: xs
Line 909: else y :: insert x xs
Line 910: Alternatively, you can use interactive editing to give more structure to the defi-
Line 911: nition, and insert a case construct to match on an intermediate result. Press
Line 912: Ctrl-Alt-M with the cursor over ?insert_rhs_2. This introduces a new case
Line 913: expression with a placeholder for the value to be inspected (so the function
Line 914: won’t type-check yet): 
Line 915: insert : Ord elem =>
Line 916: (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 917: insert x [] = [x]
Line 918: 
Line 919: --- 페이지 100 ---
Line 920: 74
Line 921: CHAPTER 3
Line 922: Interactive development with types
Line 923: insert x (y :: xs) = case _ of
Line 924: case_val => ?insert_rhs_2
Line 925: The _ stands for an expression you need to provide in order for the function to
Line 926: type-check successfully. You’ll need to fill in the _ with the expression you want
Line 927: to match: 
Line 928: insert : Ord elem =>
Line 929: (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 930: insert x [] = [x]
Line 931: insert x (y :: xs) = case x < y of
Line 932: case_val => ?insert_rhs_2
Line 933:  11
Line 934: Define—You can now case-split on case_val in the usual way, with Ctrl-Alt-C,
Line 935: leading to this: 
Line 936: insert : Ord elem =>
Line 937: (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 938: insert x [] = [x]
Line 939: insert x (y :: xs) = case x < y of
Line 940: False => ?insert_rhs_1
Line 941: True => ?insert_rhs_3
Line 942: 12
Line 943: Refine—Finally, you complete the implementation by filling in the new holes
Line 944: insert_rhs_1 and insert_rhs_3. Unfortunately, expression search won’t help
Line 945: you much here because there’s not enough information in the type, so you
Line 946: need to fill these in by hand: 
Line 947: insert : Ord elem =>
Line 948: (x : elem) -> (xsSorted : Vect k elem) -> Vect (S k) elem
Line 949: insert x [] = [x]
Line 950: insert x (y :: xs) = case x < y of
Line 951: False => y :: insert x xs
Line 952: True => x :: y :: xs
Line 953: Once the definition is complete, you can test it at the REPL, like this: 
Line 954: *VecSort> insSort [1,3,2,9,7,6,4,5,8]
Line 955: [1, 2, 3, 4, 5, 6, 7, 8, 9] : Vect 9 Integer
Line 956: Remember totality checking!
Line 957: Don’t forget to check that insSort is total:
Line 958: *VecSort> :total insSort
Line 959: Main.insSort is Total
Line 960: It’s a good habit to check that the functions you define are total. If a function is type-
Line 961: correct, but not total, it might appear to work when you test it, but there might still
Line 962: be a subtle error on some unusual inputs, such as a missing pattern or possible non-
Line 963: termination.
Line 964: 
Line 965: --- 페이지 101 ---
Line 966: 75
Line 967: Example: type-driven development of matrix functions
Line 968: To summarize, following the type-define-refine process, you’ve done the following: 
Line 969: 1
Line 970: Written a type for insSort.
Line 971:  2
Line 972: Tried to define insSort until you encountered the need to insert, which you
Line 973: lifted to a new top-level definition with its own type.
Line 974:  3
Line 975: Tried to define insert until you encountered the need to compare, at which
Line 976: point you refined the types to support the ordering constraint on elem.
Line 977: 4
Line 978: Continued to define insert using the refined type, and hence completed the
Line 979: implementation of insSort.
Line 980: Exercises
Line 981: To conclude this section, here are some exercises to test your understanding of the
Line 982: interactive editing mode and pattern matching on List and Vect.
Line 983:  The following functions, or some variant on them, are defined in the Prelude or in
Line 984: Data.Vect: 
Line 985: 1
Line 986: length : List a -> Nat
Line 987:  2
Line 988: reverse : List a -> List a
Line 989:  3
Line 990: map : (a -> b) -> List a -> List b
Line 991: 4
Line 992: map : (a -> b) -> Vect n a -> Vect n b
Line 993: For each of them, define your own version using interactive editing in Atom. Note
Line 994: that you’ll need to use different names (such as my_length, my_reverse, my_map) to
Line 995: avoid clashing with the names in the Prelude. You can test your answers at the REPL as
Line 996: follows:
Line 997: *ex_3_2> my_length [1..10]
Line 998: 10 : Nat
Line 999: *ex_3_2> my_reverse [1..10]
Line 1000: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] : List Integer
Line 1001: *ex_3_2> my_map (* 2) [1..10]
Line 1002: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20] : List Integer
Line 1003: *ex_3_2> my_vect_map length ["Hot", "Dog", "Jumping", "Frog"]
Line 1004: [3, 3, 7, 4] : Vect 4 Nat
Line 1005: Don’t forget to check that your definitions are total!
Line 1006: 3.3
Line 1007: Example: type-driven development of matrix functions
Line 1008: The main reason you might use vectors, with the length explicit in the type, as opposed
Line 1009: to lists, is to have the lengths of the vectors help guide you to a working function more
Line 1010: quickly. This can be particularly helpful when you work with two-dimensional vectors.
Line 1011: These, in turn, can be helpful for implementing operations on matrices, which have
Line 1012: several applications in programming, such as 3D graphics.
Line 1013:  A matrix, in mathematics, is a rectangular array of numbers arranged in rows and
Line 1014: columns. Figure 3.3 shows an example 3 × 4 matrix in both mathematical notation,
Line 1015: 
Line 1016: --- 페이지 102 ---
Line 1017: 76
Line 1018: CHAPTER 3
Line 1019: Interactive development with types
Line 1020: and in Idris notation as a vector of vectors. Notice that when representing a matrix as
Line 1021: nested vectors, the dimensions of the matrix become explicit in the type.
Line 1022: 3.3.1
Line 1023: Matrix operations and their types
Line 1024: When implementing operations on matrices, such as addition and multiplication, it’s
Line 1025: important to check that the dimensions of the vectors you’re working with are appro-
Line 1026: priate for the operations. For example:
Line 1027: When adding matrices, each matrix must have exactly the same dimensions.
Line 1028: Addition works by adding corresponding elements in each matrix. For exam-
Line 1029: ple, you can add two 3 × 2 matrices as follows:
Line 1030: The following addition of a 2 × 2 matrix to a 3 × 2 matrix is invalid because
Line 1031: there are no corresponding elements in the third row: 
Line 1032: So, the type of matrix addition could be as follows: 
Line 1033: addMatrix : Num numType =>
Line 1034:       Vect rows (Vect cols numType) ->
Line 1035:                   Vect rows (Vect cols numType) ->
Line 1036:       
Line 1037: Vect rows (Vect cols numType)
Line 1038: In other words, for some numeric type numType, adding a rows × cols matrix to
Line 1039: a rows × cols matrix results in a rows × cols matrix.
Line 1040: When multiplying matrices, the number of columns in the left matrix must be
Line 1041: the same as the number of rows in the right matrix. Then, multiplication works
Line 1042: as follows:
Line 1043: 1
Line 1044: 2
Line 1045: 3
Line 1046: 4
Line 1047: 5
Line 1048: 6
Line 1049: 7
Line 1050: 8
Line 1051: 9 10 11 12
Line 1052: 
Line 1053: 
Line 1054: 
Line 1055: 
Line 1056: 
Line 1057: 
Line 1058: 
Line 1059: 
Line 1060: 
Line 1061: 
Line 1062: 3 x 4 matrix
Line 1063: Vect 3 (Vect 4 Int)
Line 1064: [1,
Line 1065: [5,
Line 1066: [9,
Line 1067: [
Line 1068: 2,
Line 1069: 6,
Line 1070: 10,
Line 1071: 3,
Line 1072: 7,
Line 1073: 11,
Line 1074:  4],
Line 1075:  8],
Line 1076: 12]]
Line 1077: Figure 3.3
Line 1078: Representation of a matrix as 
Line 1079: two-dimensional vectors. On the left, the 
Line 1080: matrix is in mathematical notation. The same 
Line 1081: matrix is represented in Idris on the right.
Line 1082: 1 2
Line 1083: 3 4
Line 1084: 5 6
Line 1085: 
Line 1086: 
Line 1087: 
Line 1088: 
Line 1089: 
Line 1090: 
Line 1091: 
Line 1092: 
Line 1093: 
Line 1094: 
Line 1095: 7
Line 1096: 8
Line 1097: 9 10
Line 1098: 11 12
Line 1099: 
Line 1100: 
Line 1101: 
Line 1102: 
Line 1103: 
Line 1104: 
Line 1105: 
Line 1106: 
Line 1107: 
Line 1108: 
Line 1109: +
Line 1110: 8 10
Line 1111: 12 14
Line 1112: 16 18
Line 1113: 
Line 1114: 
Line 1115: 
Line 1116: 
Line 1117: 
Line 1118: 
Line 1119: 
Line 1120: 
Line 1121: 
Line 1122: 
Line 1123: =
Line 1124: 1 2
Line 1125: 3 4
Line 1126: 5 6
Line 1127: 
Line 1128: 
Line 1129: 
Line 1130: 
Line 1131: 
Line 1132: 
Line 1133: 
Line 1134: 
Line 1135: 
Line 1136: 
Line 1137: 7 8
Line 1138: 9 10
Line 1139: 
Line 1140: 
Line 1141: 
Line 1142: 
Line 1143: 
Line 1144: 
Line 1145: +
Line 1146: ???
Line 1147: =
Line 1148: 
Line 1149: --- 페이지 103 ---
Line 1150: 77
Line 1151: Example: type-driven development of matrix functions
Line 1152:  
Line 1153: Here, multiplying a 3 × 2 matrix by a 2 × 4 matrix results in a 3 × 4 matrix. The
Line 1154: value in row x, column y in the result is the sum of the product of correspond-
Line 1155: ing elements in row x of the left input, and column y of the right input. So the
Line 1156: type of matrix multiplication could be as follows: 
Line 1157: multMatrix : Num numType =>
Line 1158: Vect n (Vect m numType) -> Vect m (Vect p numType) ->
Line 1159: Vect n (Vect p numType)
Line 1160: In other words, for some numeric type numType, multiplying an n × m matrix by
Line 1161: an m × p matrix results in an n × p matrix.
Line 1162: 3.3.2
Line 1163: Transposing a matrix
Line 1164: A useful operation when manipulating matrices is transposition, which converts rows
Line 1165: to columns and vice versa. For example, a 3 × 2 matrix becomes a 2 × 3 matrix: 
Line 1166: You can write a transposeMat function that, in general, converts an m × n matrix into
Line 1167: an n × m matrix, representing matrices as nested vectors. As usual, you can write the
Line 1168: function interactively, where each step is broadly characterized as one of type, define,
Line 1169: or refine. From this point, I’ll generally assume you’re comfortable with the interac-
Line 1170: tive commands in Atom, and I’ll describe the overall type-driven process rather than
Line 1171: the specifics of building the function.
Line 1172: 1
Line 1173: Type—Begin by giving a type for transposeMat: 
Line 1174: transposeMat : Vect m (Vect n elem) -> Vect n (Vect m elem)
Line 1175: For matrix arithmetic, in the types of addMatrix and multMatrix, you need to
Line 1176: constrain the element type to be numeric. Here, though, the element type of
Line 1177: the matrix, elem, could be anything. You’re not going to inspect it or use it at
Line 1178: any point in the implementation of transposeMat; you merely change the rows
Line 1179: to columns and columns to rows.
Line 1180: ×
Line 1181: =
Line 1182: 1
Line 1183: 3
Line 1184: 5
Line 1185: 2
Line 1186: 4
Line 1187: 6
Line 1188: 7
Line 1189: 11
Line 1190: 8
Line 1191: 12
Line 1192: 9
Line 1193: 13
Line 1194: 10
Line 1195: 14
Line 1196: Row 2 column 3 of result = 3 × 9 + 4 × 13 = 79
Line 1197: 29
Line 1198: 65
Line 1199: 101
Line 1200: 32
Line 1201: 72
Line 1202: 112
Line 1203: 35
Line 1204: 79
Line 1205: 123
Line 1206: 38
Line 1207: 86
Line 1208: 134
Line 1209: 1 2
Line 1210: 3 4
Line 1211: 5 6
Line 1212: 
Line 1213: 
Line 1214: 
Line 1215: 
Line 1216: 
Line 1217: 
Line 1218: 
Line 1219: 
Line 1220: 
Line 1221: 
Line 1222:  ... transposed to ... 1 3 5
Line 1223: 2 4 6
Line 1224: 
Line 1225: 
Line 1226: 
Line 1227: 
Line 1228: 
Line 1229: 
Line 1230: 
Line 1231: 
Line 1232: 
Line 1233: --- 페이지 104 ---
Line 1234: 78
Line 1235: CHAPTER 3
Line 1236: Interactive development with types
Line 1237:  2
Line 1238: Define—Create a skeleton definition, and then case-split on the input vector: 
Line 1239: transposeMat : Vect m (Vect n elem) -> Vect n (Vect m elem)
Line 1240: transposeMat [] = ?transposeMat_rhs_1
Line 1241: transposeMat (x :: xs) = ?transposeMat_rhs_2
Line 1242:  3
Line 1243: Type—When Idris creates new holes, either from a case split or an incomplete
Line 1244: result of an expression search, it’s always a good idea to inspect the types of
Line 1245: those holes to get some insight into how to proceed. First, take a look at the
Line 1246: type of ?transposeMat_rhs_1: 
Line 1247: elem : Type
Line 1248: n : Nat
Line 1249: --------------------------------------
Line 1250: transposeMat_rhs_1 : Vect n (Vect 0 elem)
Line 1251: Here, you’re trying to convert a 0 × n vector into an n × 0 vector, so you need to
Line 1252: create n copies of an empty vector. We’ll return to this case later; for now, you
Line 1253: can rename the hole to createEmpties and lift it to a top-level function with
Line 1254: Ctrl-Alt-L: 
Line 1255: createEmpties : Vect n (Vect 0 elem)
Line 1256: transposeMat : Vect m (Vect n elem) -> Vect n (Vect m elem)
Line 1257: transposeMat [] = createEmpties
Line 1258: transposeMat (x :: xs) = ?transposeMat_rhs_2
Line 1259:  4
Line 1260: Type—Look at the type of ?transposeMat_rhs_2: 
Line 1261: elem : Type
Line 1262: n : Nat
Line 1263: x : Vect n elem
Line 1264: k : Nat
Line 1265: xs : Vect k (Vect n elem)
Line 1266: --------------------------------------
Line 1267: transposeMat_rhs_2 : Vect n (Vect (S k) elem)
Line 1268: You have xs, which is a k × n matrix, and you need to make an n × (S k) matrix.
Line 1269:  5
Line 1270: Define—One insight you need here is that it’s likely easier to build an n × (S k)
Line 1271: matrix from an n × k matrix, because at least one of the dimensions is correct.
Line 1272: You can create such a matrix by transposing xs: 
Line 1273: transposeMat (x :: xs) = let xsTrans = transposeMat xs in
Line 1274: ?transposeMat_rhs_2
Line 1275:  6
Line 1276: Type—You can also lift ?transposeMat_rhs_2 to a top-level function, renaming
Line 1277: it transposeHelper. This results in the following: 
Line 1278: transposeHelper : (x : Vect n elem) -> (xs : Vect k (Vect n elem)) ->
Line 1279: (xsTrans : Vect n (Vect k elem)) -> Vect n (Vect (S k) elem)
Line 1280: The type for transposeHelper is generated from the types of the local variables
Line 1281: you have access to: x, xs, and xsTrans. It will take these variables as inputs, and
Line 1282: produce a Vect n (Vect (S k) elem) as output.
Line 1283: 
Line 1284: --- 페이지 105 ---
Line 1285: 79
Line 1286: Example: type-driven development of matrix functions
Line 1287:  7
Line 1288: Type—At this stage, it’s good to look more closely at the types of the variables x,
Line 1289: xs, and xsTrans and try to use these types to visualize what you need to do to
Line 1290: complete transposeMat.
Line 1291: For the sake of visualization, let’s take n = 4 and k = 2. Figure 3.4 shows an
Line 1292: original two-dimensional vector, of the form (x :: xs), where x is the first row
Line 1293: and xs is the rest of the rows, built with these dimensions. It identifies the com-
Line 1294: ponents x and xs, and it shows the result of transposing xs and the expected
Line 1295: result of the whole operation.
Line 1296: What you need to do, therefore, is add each element of x to the vector in the
Line 1297: corresponding element of xsTrans; you won’t need xs in transposeHelper. If
Line 1298: you delete this by hand in the type of transposeHelper and the application in
Line 1299: transposeMat, you get this:
Line 1300: transposeHelper : (x : Vect n elem) -> (xsTrans : Vect n (Vect k elem)) ->
Line 1301: Vect n (Vect (S k) elem)
Line 1302: transposeMat : Vect m (Vect n elem) -> Vect n (Vect m elem)
Line 1303: transposeMat [] = createEmpties
Line 1304: transposeMat (x :: xs) = let xsTrans = transposeMat xs in
Line 1305: transposeHelper x xsTrans
Line 1306:  8
Line 1307: Define—To implement transposeHelper, you can add a skeleton definition,
Line 1308: pattern match on x and xsTrans, and then use expression search to complete
Line 1309: the definition. There’s enough information for Idris to fill in the details itself: 
Line 1310: transposeHelper : (x : Vect n elem) -> (xsTrans : Vect n (Vect k elem)) ->
Line 1311: Vect n (Vect (S k) elem)
Line 1312: transposeHelper [] [] = []
Line 1313: transposeHelper (x :: xs) (y :: ys) = (x :: y) :: transposeHelper xs ys
Line 1314: Rather than typing this in directly, try to build it using the interactive com-
Line 1315: mands. It’s possible to write this function from the type using only Ctrl-Alt-A,
Line 1316: Ctrl-Alt-C, Ctrl-Alt-S, and cursor movements.
Line 1317: CASE SPLITTING ON VECTORS
Line 1318: If you case-split on x and then case-split on
Line 1319: xsTrans, notice that Idris only gives one possible pattern for xsTrans. This is
Line 1320: because the types of x and xsTrans state that both must have the same length.
Line 1321: x
Line 1322: xs
Line 1323: [5,
Line 1324: [6,
Line 1325: [7,
Line 1326: [8,
Line 1327: 9],
Line 1328: 10],
Line 1329: 11],
Line 1330: 12] 
Line 1331:  
Line 1332: ]
Line 1333: [
Line 1334: xs_trans
Line 1335: [1,
Line 1336: [5,
Line 1337: [9,
Line 1338: [
Line 1339: 2,
Line 1340: 6,
Line 1341: 10,
Line 1342: 3,
Line 1343: 7,
Line 1344: 11,
Line 1345:  4],
Line 1346:  8],
Line 1347: 12] ]
Line 1348: Result
Line 1349: [1,
Line 1350: [2,
Line 1351: [3,
Line 1352: [4,
Line 1353: [
Line 1354: 5,
Line 1355: 6,
Line 1356: 7,
Line 1357: 8,
Line 1358:   9],
Line 1359:  10],
Line 1360:  11],
Line 1361:  12] ]
Line 1362: Figure 3.4
Line 1363: The components of the vector you’re transposing (x and xs), along 
Line 1364: with the result of transposing xs, and the expected overall result
Line 1365: 
Line 1366: --- 페이지 106 ---
Line 1367: 80
Line 1368: CHAPTER 3
Line 1369: Interactive development with types
Line 1370: 9
Line 1371: Define—All that remains is to implement createEmpties. You can implement
Line 1372: this using a library function, replicate: 
Line 1373: *transpose> :doc Vect.replicate
Line 1374: Data.Vect.replicate : (n : Nat) -> (x : a) -> Vect n a
Line 1375: Repeat some value n times
Line 1376: Arguments:
Line 1377: n : Nat
Line 1378: -- the number of times to repeat it
Line 1379: x : a
Line 1380: -- the value to repeat
Line 1381: If you create a skeleton definition of createEmpties from its type, you’ll see the
Line 1382: following: 
Line 1383: createEmpties : Vect n (Vect 0 elem)
Line 1384: createEmpties = ?createEmpties_rhs
Line 1385: You need to call replicate to build a vector of n empty lists. Unfortunately,
Line 1386: because there are no local variables available from the patterns on the left side,
Line 1387: the natural definition results in an error message: 
Line 1388: createEmpties : Vect n (Vect 0 elem)
Line 1389: createEmpties = replicate n [] -- "No such variable n"
Line 1390: The problem is that n is a type-level variable, and not accessible to the defini-
Line 1391: tion of createEmpties. Shortly, in section 3.4, you’ll see how to handle type-
Line 1392: level variables in general, and how you might write createEmpties directly. For
Line 1393: the moment, because the type dictates that there’s only one valid value for the
Line 1394: length argument to replicate, you can use an underscore instead: 
Line 1395: createEmpties : Vect n (Vect 0 elem)
Line 1396: createEmpties = replicate _ []
Line 1397: The implementation of transposeMat is now complete. For reference, the complete
Line 1398: definition is given in listing 3.4. You can test it at the REPL: 
Line 1399: *transpose> transposeMat [[1,2], [3,4], [5,6]]
Line 1400: [[1, 3, 5], [2, 4, 6]] : Vect 2 (Vect 3 Integer)
Line 1401: createEmpties : Vect n (Vect 0 elem)
Line 1402: createEmpties = replicate _ []
Line 1403: transposeHelper : (x : Vect n elem) ->
Line 1404: (xsTrans : Vect n (Vect k elem)) ->
Line 1405: Vect n (Vect (S k) elem)
Line 1406: transposeHelper [] [] = []
Line 1407: transposeHelper (x :: xs) (y :: ys) = (x :: y) :: transposeHelper xs ys
Line 1408: transposeMat : Vect m (Vect n elem) -> Vect n (Vect m elem)
Line 1409: transposeMat [] = createEmpties
Line 1410: transposeMat (x :: xs) = let xsTrans = transposeMat xs in
Line 1411: transposeHelper x xsTrans
Line 1412: Listing 3.4
Line 1413: Complete definition of matrix transposition (Matrix.idr)
Line 1414: 
Line 1415: --- 페이지 107 ---
Line 1416: 81
Line 1417: Example: type-driven development of matrix functions
Line 1418: Exercises
Line 1419: 1
Line 1420: Reimplement transposeMat using zipWith instead of transposeHelper.
Line 1421: You can test your answer at the REPL as follows: 
Line 1422: *ex_3_3_3> transposeMat [[1,2], [3,4], [5,6]]
Line 1423: [[1, 3, 5], [2, 4, 6]] : Vect 2 (Vect 3 Integer)
Line 1424:  2
Line 1425: Implement addMatrix : Num a => Vect n (Vect m a) -> Vect n (Vect m a) -> Vect n
Line 1426: (Vect m a).
Line 1427: You can test your answer at the REPL as follows: 
Line 1428: *ex_3_3_3> addMatrix [[1,2], [3,4]] [[5,6], [7,8]]
Line 1429: [[6, 8], [10, 12]] : Vect 2 (Vect 2 Integer)
Line 1430:  3
Line 1431: Implement a function for multiplying matrices, following the description given in
Line 1432: section 3.3.1.
Line 1433: Hint: This definition is quite tricky and involves multiple steps. Consider the fol-
Line 1434: lowing: 
Line 1435: You have a left matrix of dimensions n × m, and a right matrix of dimensions m × p.
Line 1436: A good start is to use transposeMat on the right matrix.
Line 1437: Remember that you can use Ctrl-Alt-L to lift holes to top-level functions.
Line 1438: Remember to pay close attention to the types of the local variables and the types
Line 1439: of the holes.
Line 1440: Remember to use Ctrl-Alt-S to search for expressions, and pay close attention to
Line 1441: the types of any resulting holes.
Line 1442: You can test your answer at the REPL as follows: 
Line 1443: *ex_3_3_3> multMatrix [[1,2], [3,4], [5,6]] [[7,8,9,10], [11,12,13,14]]
Line 1444: [[29, 32, 35, 38],
Line 1445: [65, 72, 79, 86],
Line 1446: [101, 112, 123, 134]] : Vect 3 (Vect 4 Integer)
Line 1447: Code reuse
Line 1448: When building a definition interactively using the type-define-refine process, it’s good
Line 1449: to look out for parts of the definition that could be made more generic, or that could
Line 1450: instead be implemented using existing library functions.
Line 1451: For example, transposeHelper has a structure very similar to the library function
Line 1452: zipWith, which applies a function to corresponding elements in two vectors and is
Line 1453: defined as follows:
Line 1454: zipWith : (a -> b -> c) -> Vect n a -> Vect n b -> Vect n c
Line 1455: zipWith f []
Line 1456:   []
Line 1457:   
Line 1458: = []
Line 1459: zipWith f (x :: xs) (y :: ys) = f x y :: zipWith f xs ys
Line 1460: 
Line 1461: --- 페이지 108 ---
Line 1462: 82
Line 1463: CHAPTER 3
Line 1464: Interactive development with types
Line 1465: 3.4
Line 1466: Implicit arguments: type-level variables
Line 1467: You’ve now seen several definitions with variables at the type level that can stand
Line 1468: either for types or values. For example:
Line 1469: reverse : List elem -> List elem
Line 1470: Here, elem is a type-level variable standing for the element type of the list. It appears
Line 1471: twice, in the input type and the return type, so the element type of each must be the
Line 1472: same. 
Line 1473: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1474: Here, elem is again a type-level variable standing for the element type of the vectors. n
Line 1475: and m are type-level variables standing for the lengths of the input vectors, and they’re
Line 1476: used again in the output to describe how the length of the output relates to the length
Line 1477: of the inputs.
Line 1478:  These type-level variables aren’t declared anywhere else. Because types are first
Line 1479: class, type-level variables can also be brought into scope and used in definitions. These
Line 1480: type-level variables are referred to as implicit arguments to the functions reverse and
Line 1481: append. In this section, you’ll see how implicit arguments work, and how to use them
Line 1482: in definitions.
Line 1483: 3.4.1
Line 1484: The need for implicit arguments
Line 1485: To illustrate the need for implicit arguments, let’s take a look at how you might define
Line 1486: append without them. You could make the elem, n, and m arguments to append
Line 1487: explicit, resulting in the following definition:
Line 1488: append : (elem : Type) -> (n : Nat) -> (m : Nat) ->
Line 1489: Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1490: append elem Z m [] ys = ys
Line 1491: append elem (S k) m (x :: xs) ys = x :: append elem k m xs ys
Line 1492: But if you did so, you’d also have to be explicit about the element type and lengths
Line 1493: when calling append:
Line 1494: *Append_expl> append Char 2 2 ['a','b'] ['c','d']
Line 1495: ['a', 'b', 'c', 'd'] : Vect 4 Char
Line 1496: Given the types of the arguments ['a', 'b'] and ['c', 'd'], there’s only one possible
Line 1497: value for each of the arguments elem (which must be a Char), n (which must be 2,
Line 1498: from the length of ['a', 'b']), and m (which must also be 2, from the length of
Line 1499: ['c','d']). Any other value for any of these would not be well typed.
Line 1500:  Because there is enough information in the types of the vector arguments, Idris
Line 1501: can infer the values for the a, n, and m arguments. You can therefore write this: 
Line 1502: *Append> append _ _ _ ['a','b'] ['c','d']
Line 1503: ['a', 'b', 'c', 'd'] : Vect 4 Char
Line 1504: 
Line 1505: --- 페이지 109 ---
Line 1506: 83
Line 1507: Implicit arguments: type-level variables
Line 1508: Using implicit arguments avoids the need for writing details explicitly that can be
Line 1509: inferred by Idris. Making elem, n, and m implicit in the type of append means that you
Line 1510: can refer to them directly in the type where necessary, without needing to give explicit
Line 1511: values when calling the function. 
Line 1512: 3.4.2
Line 1513: Bound and unbound implicits
Line 1514: Let’s take another look at the types of reverse and append, with implicit arguments:
Line 1515: reverse : List elem -> List elem
Line 1516: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1517: The names elem, n, and m are called unbound implicits. This is because their names are
Line 1518: used directly, without being declared (or bound) anywhere else. You could also have
Line 1519: written these types as follows:
Line 1520: reverse : {elem : Type} -> List elem -> List elem
Line 1521: append : {elem : Type} -> {n : Nat} -> {m : Nat} ->
Line 1522: Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1523: Here, the implicit arguments have been explicitly bound in the type. The notation
Line 1524: {x : S} -> T denotes a function type where the argument is intended to be inferred by
Line 1525: Idris, rather than written directly by the programmer.
Line 1526:  When you write a type with unbound implicits, Idris will look for undefined names
Line 1527: in the type, and turn them internally into bound implicits. Consider this example:
Line 1528: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1529: First, Idris identifies that elem, n, and m are undefined, so it internally rewrites the type
Line 1530: as follows: 
Line 1531: append : {elem : _} -> {n : _} -> {m : _} ->
Line 1532: Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1533: Implicit values
Line 1534: An underscore (_) in a function call means that you want Idris to work out an implicit
Line 1535: value for the argument, given the information in the rest of the expression:
Line 1536: *Append> append _ _ _ ['a','b'] ['c','d']
Line 1537: ['a', 'b', 'c', 'd'] : Vect 4 Char
Line 1538: Idris will report an error if it can’t:
Line 1539: *Append> append _ _ _ _ ['c','d']
Line 1540: (input):Can't infer argument n to append,
Line 1541: Can't infer explicit argument to append
Line 1542: Here, Idris reports that it can’t work out the length of the first vector, or the first vector
Line 1543: itself. Unlike holes, which stand for parts of expressions that aren’t yet written, under-
Line 1544: scores stand for parts of expressions for which there’s only one valid value. It’s an
Line 1545: error if Idris can’t infer a unique value for an underscore.
Line 1546: 
Line 1547: --- 페이지 110 ---
Line 1548: 84
Line 1549: CHAPTER 3
Line 1550: Interactive development with types
Line 1551: Note that it has not attempted to fill in types for the new arguments, but instead has
Line 1552: given them as underscores in the hope that it will be able to infer them from some
Line 1553: other information in the rest of the type. Here, this results in the following:
Line 1554: append : {elem : Type} -> {n : Nat} -> {m : Nat} ->
Line 1555: Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 1556: Normally, for conciseness, you leave implicits unbound, but in some situations, it’s
Line 1557: useful to use bound implicits instead: 
Line 1558: For clarity and readability, it can be useful to give explicit types to implicit
Line 1559: arguments.
Line 1560: If there’s a dependency between an implicit argument and some other argu-
Line 1561: ment, you may need to use a bound implicit to make this clear to Idris.
Line 1562: 3.4.3
Line 1563: Using implicit arguments in functions
Line 1564: Internally, Idris treats implicit arguments like any other argument, but with the nota-
Line 1565: tional convenience that the programmer doesn’t need to provide them explicitly. As a
Line 1566: result, you can refer to implicit arguments inside function definitions, and even case-
Line 1567: split on them.
Line 1568:  For example, how can you find the length of a vector? You could do this by case
Line 1569: splitting on the vector itself:
Line 1570: length : Vect n elem -> Nat
Line 1571: length [] = Z
Line 1572: length (x :: xs) = 1 + length xs
Line 1573: Because the length is part of the type, you could also refer to it directly:
Line 1574: length : Vect n elem -> Nat
Line 1575: length {n} xs = n
Line 1576: The notation {n} in a pattern brings the implicit argument n into scope, allowing you
Line 1577: to use it directly.
Line 1578:  More generally, you can give explicit values for implicit arguments by using the
Line 1579: notation {n = value}, where n is the name of an implicit argument:
Line 1580: Unbound implicit names
Line 1581: In practice, Idris will not treat every undefined name as an unbound implicit—only
Line 1582: names that begin with a lowercase letter and that appear either on their own or in a
Line 1583: function argument position. Given the following,
Line 1584: test : f m a -> b -> a
Line 1585: m appears in an argument position, as does a. b appears on its own, and f only
Line 1586: appears in a function position. As a result, m, a, and b are treated as unbound implic-
Line 1587: its. f isn’t treated as an unbound implicit, meaning that it must be defined elsewhere
Line 1588: for this type to be valid.
Line 1589: 
Line 1590: --- 페이지 111 ---
Line 1591: 85
Line 1592: Implicit arguments: type-level variables
Line 1593: *Append> append {elem = Char} {n = 2} {m = 3}
Line 1594: append : Vect 2 Char -> Vect 3 Char -> Vect 5 Char
Line 1595: Here, you’ve partially applied append to its implicit arguments only, giving a specialized
Line 1596: function for appending a vector of two Chars to a vector of three Chars.
Line 1597:  This notation can also be used on the left side of a definition to case-split on an
Line 1598: implicit argument. For example, to implement createEmpties in section 3.3.2, you
Line 1599: could have written it directly by case splitting on the length n after bringing it into
Line 1600: scope:
Line 1601: createEmpties : Vect n (Vect 0 a)
Line 1602: createEmpties {n} = ?createEmpties_rhs
Line 1603: If you case-split on n in Atom, you’ll see this:
Line 1604: createEmpties : Vect n (Vect 0 a)
Line 1605: createEmpties {n = Z} = ?createEmpties_rhs_1
Line 1606: createEmpties {n = (S k)} = ?createEmpties_rhs_2
Line 1607: Finally, you can complete the definition with an expression search for both of the
Line 1608: remaining holes:
Line 1609: createEmpties : Vect n (Vect 0 a)
Line 1610: createEmpties {n = Z} = []
Line 1611: createEmpties {n = (S k)} = [] :: createEmpties
Line 1612: Note that in the recursive call, createEmpties is sufficient. There’s no need to pro-
Line 1613: vide an explicit value for the length because only one value (k) would type-check. On
Line 1614: the other hand, if you try at the REPL without a value for the length, Idris will report
Line 1615: an error:
Line 1616: *transpose> createEmpties
Line 1617: (input):Can't infer argument n to createEmpties,
Line 1618: Can't infer argument a to createEmpties
Line 1619: You can solve this either by giving explicit values for n and elem, or giving a target type
Line 1620: for the expression:
Line 1621: *transpose> createEmpties {a=Int} {n=4}
Line 1622: [[], [], [], []] : Vect 4 (Vect 0 Int)
Line 1623: *transpose> the (Vect 4 (Vect 0 Int)) createEmpties
Line 1624: [[], [], [], []] : Vect 4 (Vect 0 Int)
Line 1625: Type and argument erasure
Line 1626: Because implicit arguments are, internally, treated the same as any other argument,
Line 1627: you might wonder what happens at runtime. Generally, you use implicit arguments to
Line 1628: give precise types to programs, so does this mean that type information has to be
Line 1629: compiled and present at runtime?
Line 1630: Fortunately, the Idris compiler is aware of this problem. It will analyze a program
Line 1631: before compiling it so that any arguments that are only used for type checking won’t
Line 1632: be present at runtime. 
Line 1633: 
Line 1634: --- 페이지 112 ---
Line 1635: 86
Line 1636: CHAPTER 3
Line 1637: Interactive development with types
Line 1638: 3.5
Line 1639: Summary
Line 1640: Functions in Idris are defined by collections of pattern-matching equations.
Line 1641: Patterns arise from the constructors of a data type.
Line 1642: The Atom text editor provides an interactive editing mode that uses the type to
Line 1643: help direct function implementation. Similar modes are available for Emacs
Line 1644: and Vim.
Line 1645: Interactive editing commands provide natural tools for following the process of
Line 1646: type, define, refine.
Line 1647: Interactive editing provides a command for searching for a valid expression
Line 1648: that satisfies the type of a hole.
Line 1649: More-precise types, such as Vect, give more information to the compiler both
Line 1650: to help check that a function is correct, and to help constrain expression
Line 1651: searches.
Line 1652: Matrices are two-dimensional vectors, with the dimensions encoded in the type.
Line 1653: Operations on matrices such as addition and multiplication can be given types
Line 1654: that precisely describe how the operations affect the dimensions.
Line 1655: The type-define-refine process helps you to implement matrix operations with
Line 1656: precise types by using the type to direct the implementation of each subexpres-
Line 1657: sion and create appropriate helper functions.
Line 1658: Type-level variables are implicit arguments to functions, which can be brought
Line 1659: into scope and used like any other arguments by enclosing them in braces {}.