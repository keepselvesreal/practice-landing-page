Line 1: 
Line 2: --- 페이지 149 ---
Line 3: 123
Line 4: Interactive programs:
Line 5: input and output processing
Line 6: Idris is a pure language, meaning that functions don’t have side effects, such as
Line 7: updating global variables, throwing exceptions, or performing console input or
Line 8: output. Realistically, though, when we put functions together to make complete
Line 9: programs, we’ll need to interact with users somehow.
Line 10:  In the preceding chapters, we used the repl and replWith functions to write
Line 11: simple, looping interactive programs that we can compile and execute without wor-
Line 12: rying too much about how they work. For all but the simplest programs, however,
Line 13: this approach is very limiting. In this chapter, you’ll see how interactive programs
Line 14: work in Idris more generally. You’ll see how to process and validate user input, and
Line 15: how you can write interactive programs that work with dependent types. 
Line 16: This chapter covers
Line 17: Writing interactive console programs
Line 18: Distinguishing evaluation and execution
Line 19: Validating user inputs to dependently typed 
Line 20: functions
Line 21: 
Line 22: --- 페이지 150 ---
Line 23: 124
Line 24: CHAPTER 5
Line 25: Interactive programs: input and output processing
Line 26:  The key idea that allows us to write interactive programs in Idris, despite it being a
Line 27: pure language, is that we distinguish between evaluation and execution. We write inter-
Line 28: active programs using a generic type IO, which describes sequences of actions that are
Line 29: then executed by the Idris runtime system.
Line 30: 5.1
Line 31: Interactive programming with IO
Line 32: Although you can’t write functions that interact with a user directly, you can write
Line 33: functions that describe sequences of interactions. Once you have a description of a
Line 34: sequence of interactions, you can pass it to the Idris runtime environment, which will
Line 35: execute those actions.
Line 36:  The Prelude provides a generic type, IO, that allows you to describe interactive pro-
Line 37: grams that return a value: 
Line 38: Idris> :doc IO
Line 39: IO : (res : Type) -> Type
Line 40: Interactive programs, describing I/O actions and returning a
Line 41: value.
Line 42: Arguments:
Line 43: res : Type
Line 44: -- The result type of the program
Line 45: Thus, you distinguish in the type between functions that describe interactions with a
Line 46: user, and functions that return a value directly. 
Line 47:  For example, consider the difference between the function types String -> Int
Line 48: and String -> IO Int: 
Line 49: 
Line 50: String -> Int is the type of a function that takes a String as an input and
Line 51: returns an Int without any user interaction or side effects.
Line 52: 
Line 53: String -> IO Int is the type of a function that takes a String as an input and
Line 54: returns a description of an interactive program that produces an Int.
Line 55: These are a couple of examples of functions with these types:
Line 56: 
Line 57: length : String -> Int, which is defined in the Prelude, returns the length
Line 58: of the input String.
Line 59: 
Line 60: readAndGetLength : String -> IO Int returns a description of interactive
Line 61: actions that display the input String as a prompt, reads another String from
Line 62: the console, and then returns the length of that String.
Line 63: As you’ve seen in earlier chapters, the entry point to an Idris application is main : IO
Line 64: (), and we’ve used this to write simple interactive loops using the repl and replWith
Line 65: functions without worrying too much about the details of how these functions work.
Line 66: It’s now time to look at IO in more detail, and to learn how to write more-complex
Line 67: interactive programs.
Line 68:  Listing 5.1 shows an example of an interactive program that returns a description
Line 69: of the actions to display a prompt, read a user’s name, and then display a greeting.
Line 70: We’ll cover the details of the syntax throughout this section, but for now, notice the
Line 71: type of main : IO (). This type states that main takes no input and returns a descrip-
Line 72: tion of interactive actions that produce an empty tuple.
Line 73: 
Line 74: --- 페이지 151 ---
Line 75: 125
Line 76: Interactive programming with IO
Line 77:  
Line 78: module Main
Line 79: main : IO ()
Line 80: main = do
Line 81: putStr "Enter your name: "
Line 82: x <- getLine
Line 83: putStrLn ("Hello " ++ x ++ "!")
Line 84: IO IN HASKELL AND IDRIS
Line 85: If you’re already familiar with Haskell, you’ll find
Line 86: that programming with IO in Idris is very similar to writing interactive pro-
Line 87: grams in Haskell. If you understand listing 5.1, you can safely move on to sec-
Line 88: tion 5.3, where you’ll see how to validate user input and deal with errors in
Line 89: interactive Idris programs. You may also want to look at section 5.2.2, which
Line 90: discusses pattern-matching bindings.
Line 91: In this section, you’ll learn how to write interactive programs like this using IO in Idris
Line 92: and explore the distinction between evaluating expressions and executing programs,
Line 93: which allows us to write interactive programs without compromising on purity.
Line 94: 5.1.1
Line 95: Evaluating and executing interactive programs
Line 96: Functions that return an IO type are still considered pure, because they merely describe
Line 97: interactive actions. For example, the putStrLn function is defined in the Prelude and
Line 98: returns the actions that output a given String, plus a newline character, to the console:
Line 99: Idris> :t putStrLn
Line 100: putStrLn : String -> IO ()
Line 101: When you enter an expression at the REPL, Idris evaluates that expression. If that
Line 102: expression is a description of interactive actions, then to perform those actions
Line 103: requires an additional step, execution.
Line 104:  Figure 5.1 illustrates what happens when the expression putStrLn (show (47 * 2))
Line 105: is executed. First, Idris calculates that the interactive action is to display "94\n" on the
Line 106: console (that is, the evaluator calculates the exact string that is to be displayed), and
Line 107: then it passes that action to the runtime environment.
Line 108:  You can see what happens by evaluating the expression putStrLn (show (47 * 2))
Line 109: at the REPL. This merely shows a description of the actions that a runtime environ-
Line 110: ment can execute. There’s no need to look closely at the exact form of the result here,
Line 111: but you can at least see that the evaluation produces an expression with type IO ():
Line 112: Idris> putStrLn (show (47 * 2))
Line 113: io_bind (prim_write "94\n") (\__bindx => io_return ()) : IO ()
Line 114: Listing 5.1
Line 115: A simple interactive program, reading a user’s name and displaying a greet-
Line 116: ing (Hello.idr)
Line 117: The keyword do introduces a 
Line 118: sequence of interactive actions.
Line 119: putStr displays a String 
Line 120: on the console.
Line 121: getLine reads a String 
Line 122: from the console.
Line 123: putStrLn displays a String on the 
Line 124: console with a trailing newline.
Line 125: 
Line 126: --- 페이지 152 ---
Line 127: 126
Line 128: CHAPTER 5
Line 129: Interactive programs: input and output processing
Line 130: If you want to execute the resulting actions, you’ll need to pass this description to the
Line 131: Idris runtime environment. You achieve this with the :exec command at the REPL:
Line 132: Idris> :exec putStrLn (show (47 * 2))
Line 133: 94
Line 134: In general, the :exec command, given an expression of type IO (), can be under-
Line 135: stood to do the following:
Line 136: 1
Line 137: Evaluate the expression, producing a description of the interactive actions to
Line 138: execute. In figure 5.1, evaluating the expression produces a description of an
Line 139: action: Write the string "94\n" to the console.
Line 140: 2
Line 141: Pass the resulting actions to the runtime environment, which executes them. In
Line 142: figure 5.1, executing the actions writes the string "94\n" to the console.
Line 143: It’s also possible to compile to a standalone executable using the :c command at the
Line 144: REPL, which takes the executable name as an argument and generates a program that
Line 145: executes the actions described in main. For example, let’s go back to listing 5.1,
Line 146: repeated here: 
Line 147: module Main
Line 148: main : IO ()
Line 149: main = do
Line 150: putStr "Enter your name: "
Line 151: x <- getLine
Line 152: putStrLn ("Hello " ++ x ++ "!")
Line 153: If you save this in a file, Hello.idr, and load it at the REPL, you can produce an execut-
Line 154: able as follows:
Line 155: *Hello> :c hello
Line 156: This results in an executable file called hello (or, on Windows systems, hello.exe)
Line 157: that can be run directly from the shell. For example:
Line 158: $ ./hello
Line 159: Enter your name: Edwin
Line 160: Hello Edwin!
Line 161: Evaluator
Line 162: putStrLn (show (47 * 2))
Line 163: Runtime environment
Line 164: Write "94\n"
Line 165: to console
Line 166: Original expression
Line 167: Description of interactions
Line 168: Figure 5.1
Line 169: Evaluating the expression 
Line 170: putStrLn (show (47 * 2)) and then 
Line 171: executing the resulting actions
Line 172: 
Line 173: --- 페이지 153 ---
Line 174: 127
Line 175: Interactive programming with IO
Line 176: Here, main describes not just one action but a sequence of actions. In general, in
Line 177: interactive programs you need to be able to sequence actions and have commands
Line 178: react to user input. Therefore, Idris provides facilities for combining smaller interac-
Line 179: tive programs into larger ones. We’ll begin by seeing how to do this using a Prelude
Line 180: function, (>>=), and then we’ll look at the higher-level syntax we used earlier in listing
Line 181: 5.1, the do notation. 
Line 182: 5.1.2
Line 183: Actions and sequencing: the >>= operator
Line 184: In the brief example in listing 5.1, we used three IO actions: 
Line 185: 
Line 186: putStr : String -> IO (), which is an action to display a String on the console
Line 187: 
Line 188: putStrLn : String -> IO (), which is an action to display a String followed by a
Line 189: newline on the console
Line 190: 
Line 191: getLine : IO String, which is an action to read a String from the console
Line 192: In order to write realistic programs, you’ll need to do more than just execute actions.
Line 193: You’ll need to be able to sequence actions, and you’ll need to be able to process the
Line 194: results of those actions.
Line 195:  Let’s say, for example, you want to read a string from the console and then output
Line 196: its length. There’s a length function in the Prelude, of type String -> Int, that you
Line 197: can use to calculate the length of a string, but getLine returns a value of type IO
Line 198: String, not String. The type IO String is a description of an action that produces a
Line 199: String, not the String itself.
Line 200:  In other words, you can get access to the string read from the console when the
Line 201: actions resulting from the function are executed, but you don’t yet have access to it
Line 202: when the function is evaluated. There’s no function of type IO String -> String. If
Line 203: such a function existed, it would mean that it was possible to know which string was
Line 204: read from the console without actually reading any string from the console!
Line 205:  The Prelude provides a function called >>= (intended to be used as an infix opera-
Line 206: tor) that allows the sequencing of IO actions, feeding the result of one action as input
Line 207: into the next. It has the following type:
Line 208: (>>=) : IO a -> (a -> IO b) -> IO b
Line 209: Figure 5.2 shows an example application of >>=
Line 210: to sequence two actions, feeding the output of
Line 211: the first, getLine, as the input into the second,
Line 212: putStrLn. Because getLine returns a value of
Line 213: type IO String, Idris expects that putStrLn
Line 214: takes a String as its argument.
Line 215:  You can execute any sequence of actions
Line 216: with type IO () at the REPL using the :exec
Line 217: command, so you can execute the operations
Line 218: in figure 5.2 as follows: 
Line 219: getLine >>= putStrLn
Line 220: Has type
Line 221: IO String
Line 222: Has type
Line 223: String -> IO ()
Line 224: Has type IO ()
Line 225: Figure 5.2
Line 226: An interactive operation to 
Line 227: read a String and then echo its contents 
Line 228: using the >>= operator. The types of each 
Line 229: subexpression are indicated.
Line 230: 
Line 231: --- 페이지 154 ---
Line 232: 128
Line 233: CHAPTER 5
Line 234: Interactive programs: input and output processing
Line 235: Idris> :exec getLine >>= putStrLn
Line 236: Hello
Line 237: Hello
Line 238: To illustrate further, let’s try using >>= to write a printLength function that reads a
Line 239: string from the console and then outputs its length. To do this, take the following
Line 240: steps: 
Line 241: 1
Line 242: Type—Our printLength function takes no input and returns a description of IO
Line 243: actions, so give it the following type: 
Line 244: printLength : IO ()
Line 245:  2
Line 246: Define—The function has a skeleton definition that takes no arguments: 
Line 247: printLength : IO ()
Line 248: printLength = ?printLength_rhs
Line 249:  3
Line 250: Refine—Refine the printLength_rhs hole to call getLine for a description of
Line 251: an action that reads from the console, and use >>= to pass the value produced
Line 252: by getLine when it’s executed to the next action. Leave a hole in place of the
Line 253: next action for the moment: 
Line 254: printLength : IO ()
Line 255: printLength = getLine >>= ?printLength_rhs
Line 256:  4
Line 257: Type—If you inspect the type of ?printLength_rhs, you’ll see that it has a func-
Line 258: tion type: 
Line 259: --------------------------------------
Line 260: printLength_rhs : String -> IO ()
Line 261: The String in the function type here is the value that will be produced by exe-
Line 262: cuting getLine. This string will be available when the action is executed, and
Line 263: you can use it to compute the remaining IO actions.
Line 264:  5
Line 265: Refine—An expression search on ?printLength_rhs will give you an anony-
Line 266: mous function: 
Line 267: printLength : IO ()
Line 268: printLength = getLine >>= \result => ?printLength_rhs1
Line 269: The variable result is the String produced by the getLine action. Rename
Line 270: this to something more informative, like input: 
Line 271: printLength : IO ()
Line 272: printLength = getLine >>= \input => ?printLength_rhs1
Line 273:  6
Line 274: Refine—Because input is a String, you can use length to calculate its length as
Line 275: a Nat. Use a let binding to store this in a local variable: 
Line 276: printLength : IO ()
Line 277: printLength = getLine >>= \input => let len = length input in
Line 278: ?printLength_rhs1
Line 279: Entered by the user
Line 280: Output by the Idris runtime environment
Line 281: 
Line 282: --- 페이지 155 ---
Line 283: 129
Line 284: Interactive programming with IO
Line 285: 7
Line 286: Refine—Finally, complete the definition using show to convert len to a String,
Line 287: and putStrLn to give an action that displays the result: 
Line 288: printLength : IO ()
Line 289: printLength = getLine >>= \input => let len = length input in
Line 290: putStrLn (show len)
Line 291: You can try this definition at the REPL with :exec printLength, telling Idris that
Line 292: you’d like to execute the resulting actions rather than merely evaluate the expression: 
Line 293: *PrintLength> :exec printLength
Line 294: test input
Line 295: 10
Line 296: Listing 5.2 shows the complete definition, further refined by displaying a prompt. The
Line 297: layout has also been adjusted in this definition to highlight the sequence of actions.
Line 298: printLength : IO ()
Line 299: printLength = putStr "Input string: " >>= \_ =>
Line 300: getLine >>= \input =>
Line 301: let len = length input in
Line 302: putStrLn (show len)
Line 303: In principle, you can always use >>= to sequence IO actions, feeding the output of one
Line 304: action as the input to the next. However, the resulting definitions are somewhat ugly,
Line 305: and sequencing actions is particularly common. That’s why Idris provides an alterna-
Line 306: tive syntax for sequencing IO actions, the do notation. 
Line 307: 5.1.3
Line 308: Syntactic sugar for sequencing with do notation
Line 309: Interactive programs are, by their nature, typically imperative in style, with a sequence
Line 310: of commands, each of which produces a value that can be used later. The >>= function
Line 311: captures this idea, but the resulting definitions can be difficult to read.
Line 312: Listing 5.2
Line 313: A function to display a prompt, read a string, and then display its length,
Line 314: using >>= to sequence IO actions (PrintLength.idr)
Line 315: Entered by the user
Line 316: Output by the Idris runtime environment
Line 317: putStr returns IO (), so the 
Line 318: second argument of >>= 
Line 319: expects a value of type () as 
Line 320: its input. The underscore 
Line 321: indicates that this value is 
Line 322: ignored.
Line 323: getLine returns an IO String, so in 
Line 324: the rest of the definition, input 
Line 325: will have type String.
Line 326: The type of >>=
Line 327: If you check the type of >>= at the REPL, you’ll see a constrained generic type: 
Line 328: Idris> :t (>>=)
Line 329: (>>=) : Monad m => m a -> (a -> m b) -> m b
Line 330: In practice, this means that the pattern applies more generally than for IO, and you’ll
Line 331: see more of this later. For now, just read the type variable m here as IO.
Line 332: 
Line 333: --- 페이지 156 ---
Line 334: 130
Line 335: CHAPTER 5
Line 336: Interactive programs: input and output processing
Line 337:  Instead, you can sequence IO actions inside do blocks, which allow you list the
Line 338: actions that will be run when a block is executed. For example, to print two things in
Line 339: succession you’d do something like this:
Line 340: printTwoThings : IO ()
Line 341: printTwoThings = do putStrLn "Hello"
Line 342: putStrLn "World"
Line 343: Idris translates the do notation into applications of >>=. Figure 5.3 shows how this
Line 344: works in the simplest case, where an action is to be executed, followed by more
Line 345: actions.
Line 346: The result of an action can be assigned to a variable. For example, to assign the result
Line 347: of reading from the console with getLine to a variable x and then print the result, you
Line 348: can write this:
Line 349: printInput : IO ()
Line 350: printInput = do x <- getLine
Line 351: putStrLn x
Line 352: The notation x <- getLine states that the result of the getLine action (that is, the
Line 353: String produced by the action of type IO String) will be stored in the variable x,
Line 354: which you can use in the rest of the do block. Sequencing actions and binding a vari-
Line 355: able like this with do notation directly translates to applications of >>=, as illustrated in
Line 356: figure 5.4.
Line 357: do action
Line 358:  more
Line 359: action >>= \_ => more
Line 360: Action to be executed,
Line 361: of type IO ty
Line 362: More IO actions
Line 363: Transformed expression
Line 364: Figure 5.3
Line 365: Transforming do notation to 
Line 366: an expression using the >>= operator 
Line 367: when sequencing actions. The value 
Line 368: produced by the action, of type ty, is 
Line 369: ignored, as indicated by the underscore.
Line 370: do x <- action
Line 371:    more
Line 372: action >>= \x => more
Line 373: If action : IO ty
Line 374: then x : ty
Line 375: Action to be
Line 376: executed, of
Line 377: type IO ty
Line 378: More IO actions, which
Line 379: may use x : ty
Line 380: Transformed expression
Line 381: Figure 5.4
Line 382: Transforming do 
Line 383: notation to an expression using the 
Line 384: >>= operator, when binding a 
Line 385: variable and sequencing actions
Line 386: 
Line 387: --- 페이지 157 ---
Line 388: 131
Line 389: Interactive programming with IO
Line 390: You can also use let inside do blocks to assign a pure expression to a variable. The fol-
Line 391: lowing listing shows how printLength could be written using do notation instead of
Line 392: using >>= directly. 
Line 393: printLength : IO ()
Line 394: printLength = do putStr "Input string: "
Line 395: input <- getLine
Line 396: let len = length input
Line 397: putStrLn (show len)
Line 398: Most interactive definitions in Idris are written using do notation to control sequenc-
Line 399: ing. In larger programs, you’ll also need to respond to user input and direct program
Line 400: flow. In the next section, we’ll look at various methods of reading and responding to
Line 401: user input, and at how to implement loops and other forms of control flow in interac-
Line 402: tive programs. 
Line 403: Exercises
Line 404: 1
Line 405: Using do notation, write a printLonger program that reads two strings and then dis-
Line 406: plays the length of the longer string.
Line 407: 2
Line 408: Write the same program using >>= instead of do notation. 
Line 409: You can test your answers at the REPL as follows:
Line 410: *ex_5_1> :exec printLonger
Line 411: First string: short
Line 412: Second string: longer
Line 413: 6
Line 414: Listing 5.3
Line 415: A function to display a prompt, read a string, and then display its length
Line 416: using do notation to sequence IO actions (PrintLength.idr)
Line 417: getLine has type IO String, 
Line 418: so input has type String.
Line 419: “length input” has type Nat, so len 
Line 420: has type Nat; it was assigned using 
Line 421: let. Note that in do blocks, there’s no 
Line 422: “in” keyword after the assignment.
Line 423: let and <- in do blocks
Line 424: The printLength function in listing 5.3 uses two different forms for assigning to vari-
Line 425: ables: using let and using <-. There’s an important difference between these two,
Line 426: which again relies on the distinction between evaluation and execution: 
Line 427: Use let x = expression to assign the result of the evaluation of an expression
Line 428: to a variable.
Line 429: Use x <- action to assign the result of the execution of an action to a
Line 430: variable.
Line 431: In listing 5.3, getLine describes an action, so it needs to be executed and the result
Line 432: assigned using <-, but length input doesn’t, so it’s assigned using let.
Line 433: 
Line 434: --- 페이지 158 ---
Line 435: 132
Line 436: CHAPTER 5
Line 437: Interactive programs: input and output processing
Line 438: 5.2
Line 439: Interactive programs and control flow
Line 440: You’ve seen how to write basic interactive programs by sequencing existing actions,
Line 441: such as getLine to read input from the console and putStrLn to display text at the
Line 442: console. But as programs get larger, you’ll need more control: you’ll need to be able
Line 443: to validate and respond to user input, and you’ll need to express loops and other
Line 444: forms of control.
Line 445:  In general, control flow in functions describing interactive actions works exactly
Line 446: the same way as control flow in pure functions, by pattern matching and recursion.
Line 447: Functions that describe interactive actions are pure functions themselves, after all,
Line 448: merely describing the actions that are to be executed later.
Line 449:  In this section, we’ll look at some common patterns that are encountered in inter-
Line 450: active programs: producing pure values by combining the results of interactive
Line 451: actions, pattern matching on the results of interactive actions, and, finally, putting
Line 452: everything together in an interactive program with loops.
Line 453: 5.2.1
Line 454: Producing pure values in interactive definitions
Line 455: As well as describing actions for execution by the runtime system, you’ll often want to
Line 456: produce results from interactive programs. You’ve already seen getLine, for example: 
Line 457: getLine : IO String
Line 458: The type IO String says that this is a function describing actions that produce a
Line 459: String as a result.
Line 460:  Often, you’ll want to write a function that uses an IO action such as getLine and
Line 461: then manipulates its result further before returning it. For example, you might want
Line 462: to write a readNumber function that reads a String from the console and converts it to
Line 463: a Nat if the input consists entirely of digits. It produces a value of type Maybe Nat: 
Line 464: If the input consists entirely of digits representing the number i, it produces
Line 465: Just i. For example, on reading the string "1234", it produces Just 1234.
Line 466: Otherwise, it produces Nothing.
Line 467: Listing 5.4 shows how to define readNumber. After reading an input using getLine, it
Line 468: checks whether every character in the input is a digit. If so, it converts the input to a
Line 469: Nat, producing a result using Just; otherwise, it produces Nothing.
Line 470: readNumber : IO (Maybe Nat)
Line 471: readNumber = do
Line 472: input <- getLine
Line 473: if all isDigit (unpack input)
Line 474: then pure (Just (cast input))
Line 475: else pure Nothing
Line 476: Listing 5.4
Line 477: Reading and validating a number (ReadNum.idr)
Line 478: getLine has type IO String, 
Line 479: so input has type String.
Line 480: Uses unpack to convert the input to 
Line 481: List Char, to check that each input 
Line 482: character is a digit
Line 483: The pure function constructs an IO 
Line 484: action that produces a value, with no 
Line 485: other input or output effects.
Line 486: 
Line 487: --- 페이지 159 ---
Line 488: 133
Line 489: Interactive programs and control flow
Line 490: The pure function is used to produce a value in an interactive program without hav-
Line 491: ing any other input or output effects when it’s executed. Its purpose is to allow pure
Line 492: values to be constructed by interactive programs, as shown by its type:
Line 493: pure : a -> IO a
Line 494: To understand the need for pure in readNumber, you can replace the then and else
Line 495: branches of the if with holes, and inspect their types: 
Line 496: readNumber : IO (Maybe Nat)
Line 497: readNumber = do
Line 498: input <- getLine
Line 499: if all isDigit (unpack input)
Line 500: then ?numberOK
Line 501: else ?numberBad
Line 502: If you look at the type of ?numberOK, you’ll see that you need a value of type IO
Line 503: (Maybe Nat): 
Line 504: input : String
Line 505: --------------------------------------
Line 506: numberOK : IO (Maybe Nat)
Line 507: You can then refine the ?numberOK and ?numberBad holes using pure:
Line 508: readNumber : IO (Maybe Nat)
Line 509: readNumber = do
Line 510: input <- getLine
Line 511: if all isDigit (unpack input)
Line 512: then pure ?numberOK
Line 513: else pure ?numberBad
Line 514: Now, if you look at the type of ?numberOK, you’ll see that you need a value of type
Line 515: Maybe Nat instead, without the IO wrapper: 
Line 516: input : String
Line 517: --------------------------------------
Line 518: numberOK : Maybe Nat
Line 519: Type of pure
Line 520: As with >>=, if you check the type of pure at the REPL, you’ll see a constrained
Line 521: generic type, rather than a type that uses IO specifically: 
Line 522: Idris> :t pure
Line 523: pure : Applicative f => a -> f a
Line 524: You can read the f here as IO. We’ll get to the exact meaning of Applicative and
Line 525: Monad in chapter 7; you don’t need to understand the details to write interactive
Line 526: programs.
Line 527: 
Line 528: --- 페이지 160 ---
Line 529: 134
Line 530: CHAPTER 5
Line 531: Interactive programs: input and output processing
Line 532: You can try readNumber at the REPL by executing it and passing the result on to
Line 533: printLn (described in the sidebar, “Displaying values with printLn”): 
Line 534: *ReadNum> :exec readNumber >>= printLn
Line 535: 100
Line 536: Just 100
Line 537: *ReadNum> :exec readNumber >>= printLn
Line 538: bad
Line 539: Nothing
Line 540: In the first case, the input is valid, so Idris produces the result Just 100. In the second
Line 541: case, the input has nondigit characters, so Idris produces Nothing.
Line 542: 5.2.2
Line 543: Pattern-matching bindings
Line 544: When an interactive action produces a value of some complex data type, such as
Line 545: readNumber, which produces a value of type Maybe Nat, you’ll often want to pattern-
Line 546: match on the intermediate result. You can do this using a case expression, but this
Line 547: can lead to deeply nested definitions. The following listing, for example, shows a func-
Line 548: tion that reads two numbers from the console using readNumber, and produces a pair
Line 549: of those numbers if both are valid inputs, or Nothing otherwise.
Line 550: readNumbers : IO (Maybe (Nat, Nat))
Line 551: readNumbers =
Line 552: do num1 <- readNumber
Line 553: case num1 of
Line 554: Nothing => pure Nothing
Line 555: Just num1_ok =>
Line 556: do num2 <- readNumber
Line 557: case num2 of
Line 558: Nothing => pure Nothing
Line 559: Just num2_ok => pure (Just (num1_ok, num2_ok))
Line 560: This will only get worse as functions get longer and there are more error conditions to
Line 561: deal with. To help with this, Idris provides some concise syntax for matching on inter-
Line 562: mediate values in do notation. First, we’ll take a look at a simple example, reading a
Line 563: pair of Strings from the console, and then we’ll revisit readNumbers and see how it
Line 564: can be made more concise.
Line 565: Listing 5.5
Line 566: Reading and validating a pair of numbers from the console (ReadNum.idr)
Line 567: Entered by the user
Line 568: Output by Idris
Line 569: Entered by the user
Line 570: Output by Idris
Line 571: Displaying values with printLn
Line 572: printLn is a combination of putStrLn and show, and it’s convenient for displaying
Line 573: values at the console directly. It’s defined in the Prelude: 
Line 574: printLn : Show a => a -> IO ()
Line 575: printLn x = putStrLn (show x) 
Line 576: Reads first
Line 577: input; num1
Line 578: has type
Line 579: Maybe Nat
Line 580: num1 is an invalid input, 
Line 581: so produces Nothing
Line 582: Reads second input; num2 
Line 583: has type Maybe Nat
Line 584: num2 is an invalid input, 
Line 585: so produces Nothing
Line 586: Both inputs are valid,
Line 587: so produces a pair of
Line 588: the inputs read
Line 589: 
Line 590: --- 페이지 161 ---
Line 591: 135
Line 592: Interactive programs and control flow
Line 593:  You can write a function that reads two Strings and produces a pair as follows,
Line 594: using pure to combine the two inputs:
Line 595: readPair : IO (String, String)
Line 596: readPair = do str1 <- getLine
Line 597: str2 <- getLine
Line 598: pure (str1, str2)
Line 599: When you use the result produced by readPair, you’ll need to pattern-match on it to
Line 600: extract the first and second inputs. For example, to read a pair of Strings using read-
Line 601: Pair and then display both, you’d do this:
Line 602: usePair : IO ()
Line 603: usePair = do pair <- readPair
Line 604: case pair of
Line 605: (str1, str2) => putStrLn ("You entered " ++
Line 606: str1 ++ " and " ++ str2)
Line 607: To make these programs more concise, Idris allows the pattern match and the assign-
Line 608: ment to be combined on one line, in a pattern-matching binding. The following pro-
Line 609: gram has exactly the same behavior as the preceding one:
Line 610: usePair : IO ()
Line 611: usePair = do (str1, str2) <- readPair
Line 612: putStrLn ("You entered " ++ str1 ++ " and " ++ str2)
Line 613: A similar idea works for readNumbers. You can pattern-match directly on the result of
Line 614: readNumber to check the validity of its result:
Line 615: readNumbers : IO (Maybe (Nat, Nat))
Line 616: readNumbers =
Line 617: do Just num1_ok <- readNumber
Line 618: Just num2_ok <- readNumber
Line 619: pure (Just (num1_ok, num2_ok))
Line 620: This works as you’d like when the user enters valid numbers:
Line 621: *ReadNum> :exec readNumbers >>= printLn
Line 622: 10
Line 623: 20
Line 624: Just (10, 20)
Line 625: But, unfortunately, it doesn’t deal with the case where readNumber produces Nothing,
Line 626: and therefore crashes on execution:
Line 627: *ReadNum> :exec readNumbers >>= printLn
Line 628: bad
Line 629: *** ReadNum.idr:26:22:unmatched case in Main.case block in readNumbers
Line 630: at ReadNum.idr:26:22 ***
Line 631: Idris has noticed this when checking readNumbers for totality:
Line 632: *ReadNum> :total readNumbers_v2
Line 633: Main.readNumbers is possibly not total due to:
Line 634: Main.case block in readNumbers at ReadNum.idr:26:22, which is
Line 635: not total as there are missing cases
Line 636: Entered by the user
Line 637: Entered by the user
Line 638: Output by Idris
Line 639: Entered by the user
Line 640: 
Line 641: --- 페이지 162 ---
Line 642: 136
Line 643: CHAPTER 5
Line 644: Interactive programs: input and output processing
Line 645: REMEMBER TO CHECK TOTALITY!
Line 646: This incomplete definition of readNumbers
Line 647: illustrates why it’s important to check that functions are total. Even though
Line 648: readNumbers type-checks successfully, it could still fail at runtime due to the
Line 649: missing cases.
Line 650: Listing 5.6 shows how you can deal with the other possibilities in a pattern-matching
Line 651: binding. As well as the binding itself, you provide alternative matches after a vertical
Line 652: bar, showing how the rest of the function should proceed if the default match on Just
Line 653: num1_ok or Just num2_ok fails. This function has exactly the same behavior as the ear-
Line 654: lier function in listing 5.5.
Line 655: readNumbers : IO (Maybe (Nat, Nat))
Line 656: readNumbers =
Line 657: do Just num1_ok <- readNumber | Nothing => pure Nothing
Line 658: Just num2_ok <- readNumber | Nothing => pure Nothing
Line 659: pure (Just (num1_ok, num2_ok))
Line 660: Pattern-matching bindings of this form allow you to express the expected valid behav-
Line 661: ior of a function in the default matches (Just num1_ok and Just num2_ok in listing 5.6),
Line 662: dealing with the error cases in the alternative matches. 
Line 663: 5.2.3
Line 664: Writing interactive definitions with loops
Line 665: Now that you can read, validate, and respond to user input, let’s put everything
Line 666: together and write interactive definitions with loops.
Line 667:  You can write loops by writing recursive definitions. The next listing, for example,
Line 668: shows a countdown function that calculates a sequence of actions to display a count-
Line 669: down, with a one-second pause between displaying each number.
Line 670: module Main
Line 671: import System
Line 672: countdown : (secs : Nat) -> IO ()
Line 673: countdown Z = putStrLn "Lift off!"
Line 674: countdown (S secs) = do putStrLn (show (S secs))
Line 675: usleep 1000000
Line 676: countdown secs
Line 677: Listing 5.6
Line 678: Reading and validating a pair of numbers from the console, concisely
Line 679:  (ReadNum.idr)
Line 680: Listing 5.7
Line 681: Display a countdown, pausing one second between each iteration (Loops.idr)
Line 682: Reads first input. If it’s
Line 683: invalid, produces Nothing as
Line 684: a result of the computation.
Line 685: Reads second input. If it’s invalid, 
Line 686: produces Nothing as a result of 
Line 687: the computation.
Line 688: Both inputs are valid, so produces a 
Line 689: pair of the inputs read
Line 690: The System module contains several 
Line 691: definitions for interacting with the 
Line 692: operating system and environment. 
Line 693: You import it here for usleep.
Line 694: countdown is implemented by pattern 
Line 695: matching on Nat, so there are cases 
Line 696: for each constructor of Nat.
Line 697: usleep describes an action that sleeps 
Line 698: for the given number of microseconds.
Line 699: Continues
Line 700: the
Line 701: countdown
Line 702: 
Line 703: --- 페이지 163 ---
Line 704: 137
Line 705: Interactive programs and control flow
Line 706: If you try executing this at the REPL using :exec, you’ll see a countdown displayed:
Line 707: *Loops> :exec countdown 5
Line 708: 5
Line 709: 4
Line 710: 3
Line 711: 2
Line 712: 1
Line 713: Lift off!
Line 714: You can also check whether this function is total, that is, guaranteed to produce a
Line 715: result in finite time for all possible inputs:
Line 716: *Loops> :total countdown
Line 717: Main.countdown is Total
Line 718: In general, you can write an interactive function that describes a loop by making a
Line 719: recursive call to the function with its last action. In countdown, as long as the input
Line 720: argument isn’t Z, the program when executed will print the argument and wait a sec-
Line 721: ond before making a recursive call on the next smaller number. The number of itera-
Line 722: tions of the loop is therefore determined by the initial input. Because this is finite,
Line 723: countdown must terminate eventually, so Idris reports that it is total.
Line 724: TOTALITY AND INTERACTIVE PROGRAMS
Line 725: Totality checking is based on evalua-
Line 726: tion, not execution. The result of totality checking an IO program, therefore,
Line 727: tells you whether Idris will produce a finite sequence of actions, but nothing
Line 728: about the runtime behavior of those actions.
Line 729: Sometimes, however, the number of iterations is determined by user input. For exam-
Line 730: ple, you can write a function to keep executing countdown until the user wants to stop,
Line 731: as shown next.
Line 732: countdowns : IO ()
Line 733: countdowns = do putStr "Enter starting number: "
Line 734: Just startNum <- readNumber
Line 735: | Nothing => do putStrLn "Invalid input"
Line 736: countdowns
Line 737: countdown startNum
Line 738: putStr "Another (y/n)? "
Line 739: yn <- getLine
Line 740: if yn == "y" then countdowns
Line 741: else pure ()
Line 742: This function is not total, because there’s no guarantee that a user will ever enter any-
Line 743: thing other than y, or even provide any valid input.
Line 744: *Loops> :total countdowns
Line 745: Main.countdowns is possibly not total due to recursive path:
Line 746: Main.countdowns
Line 747: Listing 5.8
Line 748: Keep running countdown until the user doesn’t want to run it any more
Line 749: (Loops.idr)
Line 750: Uses readNumber to get
Line 751: a valid input, or restart if
Line 752: the input is not valid
Line 753: Calls countdown with
Line 754: the user’s input
Line 755: Makes a recursive call 
Line 756: if the user enters “y”
Line 757: 
Line 758: --- 페이지 164 ---
Line 759: 138
Line 760: CHAPTER 5
Line 761: Interactive programs: input and output processing
Line 762: Interactive programs that might loop forever, such as countdowns (or, more realisti-
Line 763: cally, servers or operating systems) are not total, at least if we limit the definition to ter-
Line 764: minating programs. More precisely, a total function must either terminate or be
Line 765: guaranteed to produce a finite prefix of some infinite input, within finite time. We’ll
Line 766: discuss this further in chapter 11. 
Line 767: Exercises
Line 768: 1
Line 769: Write a function that implements a simple “guess the number” game. It should have
Line 770: the following type: 
Line 771: guess : (target : Nat) -> IO ()
Line 772: Here, target is the number to be guessed, and guess should behave as follows: 
Line 773: Repeatedly ask the user to guess a number, and display whether the guess is too
Line 774: high, too low, or correct.
Line 775: When the guess is correct, exit.
Line 776: Ideally, guess will also report an error message if the input is invalid (for example, if
Line 777: it contains characters that are not digits or are out of range).
Line 778:  2
Line 779: Implement a main function that chooses a random number between 1 and 100 and
Line 780: then calls guess.
Line 781: Hint: As a source of random numbers, you could use time : IO Integer, defined
Line 782: in the System module.
Line 783:  3
Line 784: Extend guess so that it counts the number of guesses the user has taken and dis-
Line 785: plays that number before the input is read.
Line 786: Hint: Refine the type of guess to the following: 
Line 787: guess : (target : Nat) -> (guesses : Nat) -> IO ()
Line 788:  4
Line 789: Implement your own versions of repl and replWith. Remember that you’ll need to
Line 790: use different names to avoid clashing with the names defined in the Prelude.
Line 791: 5.3
Line 792: Reading and validating dependent types
Line 793: In previous chapters, you’ve seen several functions with dependent types, particularly
Line 794: using Vect to express lengths of vectors in their types. This allows you to state assump-
Line 795: tions about the form of inputs to a function in its type and guarantees about the form
Line 796: of its output. For example, you’ve seen zip, which pairs corresponding elements of
Line 797: vectors:
Line 798: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 799: The type expresses the following: 
Line 800: Assumption—Both input vectors have the same length, n.
Line 801: Guarantee—The output vector will have the same length as the input vectors.
Line 802: 
Line 803: --- 페이지 165 ---
Line 804: 139
Line 805: Reading and validating dependent types
Line 806: Guarantee—The output vector will consist of pairs of the element type of the
Line 807: first input vector and the element type of the second input vector.
Line 808: Idris checks that whenever the function is called, the arguments satisfy the assumption
Line 809: and the definition of the function satisfies the guarantee.
Line 810:  So far, we’ve been testing functions such as zip at the REPL. Realistically, though,
Line 811: inputs to functions don’t come from such a carefully controlled environment where
Line 812: the Idris type checker is available. In practice, when a complete program is compiled
Line 813: and executed, inputs to functions will originate from some external source: perhaps a
Line 814: field on a web page, or user input at the console.
Line 815:  When a program reads data from some external source, it can’t make any assump-
Line 816: tions about the form of that data. Rather, the program has to check that the data is of
Line 817: the necessary form. The type of a function tells you exactly what you need to check in
Line 818: order to evaluate it safely.
Line 819:  In this section, we’ll write a program that reads two vectors from the console, uses
Line 820: zip to pair corresponding elements if the vectors are the same length, and then dis-
Line 821: plays the result. Although this is a simple goal, it demonstrates several important
Line 822: aspects of working with dependent types in interactive programs, and you’ll see many
Line 823: more examples of this form later in this book. You’ll see, briefly, how the types of the
Line 824: pure parts of programs tell you what you need to check in the interactive parts, and
Line 825: how the type system guides you toward the parts where error checking is necessary.
Line 826: 5.3.1
Line 827: Reading a Vect from the console
Line 828: As a first step, you’ll need to be able to read a vector from the console. Because vectors
Line 829: express their length in the type, you’ll need some way of describing the length of the
Line 830: vector you intend to read. One way is to take the length as an input, such as in the fol-
Line 831: lowing type:
Line 832: readVectLen : (len : Nat) -> IO (Vect len String)
Line 833: This type states that readVectLen takes an intended length as input, and returns the
Line 834: sequence of actions that reads a vector of Strings of that length. The following listing
Line 835: shows one way you could implement this function.
Line 836: readVectLen : (len : Nat) -> IO (Vect len String)
Line 837: readVectLen Z = pure []
Line 838: readVectLen (S k) = do x <- getLine
Line 839: xs <- readVectLen k
Line 840: pure (x :: xs)
Line 841: Listing 5.9
Line 842: Reading a Vect of known length from the console (ReadVect.idr)
Line 843: Nothing to read; 
Line 844: returns an empty vector
Line 845: Reads
Line 846: one
Line 847: String
Line 848: Reads the rest of the vector
Line 849: Combines the string and 
Line 850: the rest of the vector
Line 851: 
Line 852: --- 페이지 166 ---
Line 853: 140
Line 854: CHAPTER 5
Line 855: Interactive programs: input and output processing
Line 856:  You can try readVectLen at the REPL by executing it with a specific length, and
Line 857: then printing the result with printLn:
Line 858: *ReadVect> :exec readVectLen 4 >>= printLn
Line 859: John
Line 860: Paul
Line 861: George
Line 862: Ringo
Line 863: ["John", "Paul", "George", "Ringo"]
Line 864: A problem with this approach is that you need to know in advance how long the vec-
Line 865: tor should be, because the length is given as an input. What if, instead, you want to
Line 866: read strings until the user enters a blank line? You can’t know in advance how many
Line 867: strings the user will enter, so instead, you’ll need to return the length along with a vec-
Line 868: tor of that length. 
Line 869: 5.3.2
Line 870: Reading a Vect of unknown length
Line 871: If you read a vector from the console, terminated by a blank line, you can’t know how
Line 872: many elements will be in the resulting vector. In this situation, you can define a new
Line 873: data type that wraps not only the vector but also its length:
Line 874: data VectUnknown : Type -> Type where
Line 875: MkVect : (len : Nat) -> Vect len a -> VectUnknown a
Line 876: In type-driven development, we aim to express what we know about data in its type; if
Line 877: we can’t know something about data, we need to express this somehow too. This is the
Line 878: purpose of VectUnknown; it contains both the vector and its length, meaning that the
Line 879: length doesn’t have to be known in the type.
Line 880:  You can construct an example at the REPL: 
Line 881: *ReadVect> MkVect 4 ["John", "Paul", "George", "Ringo"]
Line 882: MkVect 4 ["John", "Paul", "George", "Ringo"] : VectUnknown String
Line 883: In fact, you could leave an underscore in the expression instead of giving the length,
Line 884: 4, explicitly, because Idris can infer this from the length of the given vector: 
Line 885: *ReadVect> MkVect _ ["John", "Paul", "George", "Ringo"]
Line 886: MkVect 4 ["John", "Paul", "George", "Ringo"] : VectUnknown String
Line 887: Having defined VectUnknown, instead of writing a function that returns IO (Vect len
Line 888: String), you can write a function that returns IO (VectUnknown String). That is, it
Line 889: returns not only the vector, but also its length:
Line 890: readVect : IO (VectUnknown String)
Line 891: This type states that readVect is a sequence of interactive actions that produce a vec-
Line 892: tor of some unknown length, which will be determined at runtime. The following list-
Line 893: ing shows one possible implementation.
Line 894: Entered by the user
Line 895: Output by Idris
Line 896: 
Line 897: --- 페이지 167 ---
Line 898: 141
Line 899: Reading and validating dependent types
Line 900:  
Line 901: readVect : IO (VectUnknown String)
Line 902: readVect = do x <- getLine
Line 903: if (x == "")
Line 904: then pure (MkVect _ [])
Line 905: else do MkVect _ xs <- readVect
Line 906: pure (MkVect _ (x :: xs))
Line 907: To try this, you can define a convenience function, printVect, that displays the con-
Line 908: tents and length of a VectUnknown at the console:
Line 909: printVect : Show a => VectUnknown a -> IO ()
Line 910: printVect (MkVect len xs)
Line 911: = putStrLn (show xs ++ " (length " ++ show len ++ ")")
Line 912: Then, you can try reading some input at the REPL:
Line 913: *ReadVect> :exec readVect >>= printVect
Line 914: John
Line 915: Paul
Line 916: George
Line 917: Ringo
Line 918: ["John", "Paul", "George", "Ringo"] (length 4)
Line 919: When dealing with user input, there’ll often be some properties of the data that you
Line 920: can’t know until runtime. The length of a vector is one example: once you’ve read the
Line 921: vector, you know its length, and from there you can check it and reason about how it
Line 922: relates to other data. But you could have a similar problem with any dependent data
Line 923: type that’s read from user input, and it would be better not to define a new type (like
Line 924: VectUnknown) every time this happens. Instead, Idris provides a more generic solu-
Line 925: tion, dependent pairs. 
Line 926: 5.3.3
Line 927: Dependent pairs
Line 928: You’ve already seen tuples, introduced in chapter 2, which allow you to combine val-
Line 929: ues of different types, as in this example:
Line 930: mypair : (Int, String)
Line 931: mypair = (94, "Pages")
Line 932: A dependent pair is a more expressive form of this construct, where the type of the second
Line 933: element in a pair can be computed from the value of the first element. For example:
Line 934: anyVect : (n : Nat ** Vect n String)
Line 935: anyVect = (3 ** ["Rod", "Jane", "Freddy"])
Line 936: Listing 5.10
Line 937: Reading a Vect of unknown length from the console (ReadVect.idr)
Line 938: Reads the first line
Line 939: If the line read is blank,
Line 940: returns an empty vector
Line 941: wrapped in MkVect. Idris
Line 942: will infer its length.
Line 943: Combines xs with 
Line 944: the first line (x) and 
Line 945: wraps it in MkVect
Line 946: Reads the rest of the vector 
Line 947: and pattern-matches on the 
Line 948: result to extract xs
Line 949: Entered by the user
Line 950: Blank line entered by user
Line 951: Output by Idris
Line 952: 
Line 953: --- 페이지 168 ---
Line 954: 142
Line 955: CHAPTER 5
Line 956: Interactive programs: input and output processing
Line 957: Dependent pairs are written with the elements separated by **. Their types are written
Line 958: using the same syntax as their values, except that the first element is given an explicit
Line 959: name (n in the preceding example). Figure 5.5 illustrates the syntax for dependent
Line 960: pair types.
Line 961: You can also often omit the type of the first element, if Idris can infer it from the type
Line 962: of the second element. For example:
Line 963: anyVect : (n ** Vect n String)
Line 964: anyVect = (3 ** ["Rod", "Jane", "Freddy"])
Line 965: If you replace the value ["Rod", "Jane", "Freddy"] with a hole, you can see how the
Line 966: first value, 3, affects its type:
Line 967: anyVect : (n ** Vect n String)
Line 968: anyVect = (3 ** ?anyVect_rhs)
Line 969: Inspecting the type of ?anyVect_rhs reveals that the second element must specifically
Line 970: be a vector of length 3, as specified by the first element:
Line 971: --------------------------------------
Line 972: anyVect_rhs : Vect 3 String
Line 973: TYPES OF SUBEXPRESSIONS
Line 974: Remember that when trying to understand larger
Line 975: program listings, you can replace subexpressions with a hole, like ?any-
Line 976: Vect_rhs in the type-inference example, to find out their expected types
Line 977: and the types of any local variables that are in scope.
Line 978: Instead of defining VectUnknown as in the section 5.3.2, you can define a function that
Line 979: reads vectors of unknown length by returning a dependent pair of the length, and a
Line 980: vector of that length. The following listing shows how readVect could be defined
Line 981: using dependent pairs.
Line 982: readVect : IO (len ** Vect len String)
Line 983: readVect = do x <- getLine
Line 984: if (x == "")
Line 985: Listing 5.11
Line 986: Reading a Vect of unknown length from the console, returning a depen-
Line 987: dent pair (DepPairs.idr)
Line 988: anyVect : (n : Nat ** Vect n String)
Line 989: Name of first element
Line 990: defined here
Line 991: Name of first element
Line 992: used here
Line 993: Type of first
Line 994: element
Line 995: Type of second
Line 996: element, which may
Line 997: refer to name of
Line 998: first element
Line 999: Figure 5.5
Line 1000: Dependent pair syntax. Notice that 
Line 1001: the first element is given a name that can be 
Line 1002: used in the type of the second element.
Line 1003: Returns actions that build a 
Line 1004: dependent pair of some length, 
Line 1005: and a vector of that length
Line 1006: 
Line 1007: --- 페이지 169 ---
Line 1008: 143
Line 1009: Reading and validating dependent types
Line 1010: then pure (_ ** [])
Line 1011: else do (_ ** xs) <- readVect
Line 1012: pure (_ ** x :: xs)
Line 1013: Again, you can try this at the REPL. You can use printLn to display the contents of the
Line 1014: dependent pair:
Line 1015: *DepPairs> :exec readVect >>= printLn
Line 1016: Rod
Line 1017: Jane
Line 1018: Freddy
Line 1019: (3 ** ["Rod", "Jane", "Freddy"])
Line 1020: Now that you have the ability to read vectors of arbitrary and user-defined lengths
Line 1021: from the console, we can complete our original goal of writing a program that reads
Line 1022: two vectors and zips them together if their lengths match. 
Line 1023: 5.3.4
Line 1024: Validating Vect lengths
Line 1025: Our goal, as stated at the beginning of this section, is to write a program that does the
Line 1026: following: 
Line 1027: 1
Line 1028: Read two input vectors, using readVect.
Line 1029:  2
Line 1030: If they have different lengths, display an error.
Line 1031: 3
Line 1032: If they have the same lengths, display the result of zipping the vectors together.
Line 1033: The program will take its inputs from the user at the console and display its result on
Line 1034: the console. We’ll implement it as a zipInputs function, as follows: 
Line 1035: 1
Line 1036: Type—Because the input and output are entirely at the console, the type states
Line 1037: that zipInputs takes no arguments and returns interactive actions: 
Line 1038: zipInputs : IO ()
Line 1039:  2
Line 1040: Define—The first step in defining the function is to read two inputs using read-
Line 1041: Vect. Leave a hole, ?zipInputs_rhs, for the rest of the definition: 
Line 1042: zipInputs : IO ()
Line 1043: zipInputs = do putStrLn "Enter first vector (blank line to end):"
Line 1044: (len1 ** vec1) <- readVect
Line 1045: putStrLn "Enter second vector (blank line to end):"
Line 1046: (len2 ** vec2) <- readVect
Line 1047: ?zipInputs_rhs
Line 1048:  3
Line 1049: Type—Looking at the type of ?zipInputs_rhs, you can see the types (and
Line 1050: hence the lengths) of the vectors that have been read: 
Line 1051: len2 : Nat
Line 1052: vec2 : Vect len2 String
Line 1053: len1 : Nat
Line 1054: vec1 : Vect len1 String
Line 1055: --------------------------------------
Line 1056: zipInputs_rhs : IO ()
Line 1057: Returns a dependent
Line 1058: pair of zero (inferred by
Line 1059: Idris) and a Vect of
Line 1060: length zero
Line 1061: Returns a dependent pair of a 
Line 1062: length inferred by Idris, and a 
Line 1063: Vect combining x and xs
Line 1064: Entered by the user
Line 1065: Blank line entered by user
Line 1066: Output by Idris
Line 1067: 
Line 1068: --- 페이지 170 ---
Line 1069: 144
Line 1070: CHAPTER 5
Line 1071: Interactive programs: input and output processing
Line 1072: vec1 has length len1, and vec2 has length len2; there’s no explicit relationship
Line 1073: between these lengths. Indeed, there shouldn’t be, because they were read
Line 1074: independently. But if you look at the type of zip, you’ll see that the lengths
Line 1075: must be the same before you can use it: 
Line 1076: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 1077:  4
Line 1078: Refine—Before you can make progress, you’ll need to check that the length of
Line 1079: the second vector is the same as the length of the first. As a first attempt, you
Line 1080: might try the following: 
Line 1081: if len1 == len2
Line 1082: then ?zipInputs_rhs1
Line 1083: else ?zipInputs_rhs2
Line 1084: Unfortunately, this doesn’t help. If you look at the type of ?zipInputs_rhs1,
Line 1085: you’ll see that nothing has changed: 
Line 1086: len1 : Nat
Line 1087: len2 : Nat
Line 1088: vec2 : Vect len2 String
Line 1089: vec1 : Vect len1 String
Line 1090: --------------------------------------
Line 1091: zipInputs_rhs1 : IO ()
Line 1092: The problem is that the type of len1 == len2, Bool, tells you nothing about the
Line 1093: meaning of the operation itself. As far as Idris is concerned, the == operation
Line 1094: could be implemented in any way (you’ll see in chapter 7 how == can be
Line 1095: defined) and doesn’t necessarily guarantee that len1 and len2 really are equal. 
Line 1096: Instead, you can use the following function defined in Data.Vect: 
Line 1097: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 1098: This function takes a length, len, and a vector, input, of any length. If the
Line 1099: length of the input vector turns out to be len, it returns Just input, with its
Line 1100: type updated to Vect len a. Otherwise, it returns Nothing.
Line 1101: IMPLEMENTING EXACTLENGTH
Line 1102: To implement exactLength, you need a more
Line 1103: expressive type than Bool for representing the result of an equality test.
Line 1104: You’ll see how to do this in chapter 8, and we’ll discuss the limitations of Bool
Line 1105: in general.
Line 1106: Using exactLength, you can refine the definition as follows: 
Line 1107: zipInputs : IO ()
Line 1108: zipInputs = do putStrLn "Enter first vector (blank line to end):"
Line 1109: (len1 ** vec1) <- readVect
Line 1110: putStrLn "Enter second vector (blank line to end):"
Line 1111: (len2 ** vec2) <- readVect
Line 1112: case exactLength len1 vec2 of
Line 1113: Nothing => ?zipInputs_rhs_1
Line 1114: Just vec2' => ?zipInputs_rhs_2
Line 1115: 
Line 1116: --- 페이지 171 ---
Line 1117: 145
Line 1118: Reading and validating dependent types
Line 1119:  5
Line 1120: Refine—For zipInputs_rhs_1, the inputs are different lengths, so you display
Line 1121: an error: 
Line 1122: case exactLength len1 vec2 of
Line 1123: Nothing => putStrLn "Vectors are different lengths"
Line 1124: Just vec2' => ?zipInputs_rhs_2
Line 1125: 6
Line 1126: Refine—For zipInputs_rhs_2, you have a new vector, vec2', which is the same
Line 1127: as vec2 but with its length now guaranteed to be the same as the length of vec1,
Line 1128: as you can confirm by looking at the type: 
Line 1129: len1 : Nat
Line 1130: vec2' : Vect len1 String
Line 1131: len2 : Nat
Line 1132: vec2 : Vect len2 String
Line 1133: vec1 : Vect len1 String
Line 1134: --------------------------------------
Line 1135: zipInputs_rhs_2 : IO ()
Line 1136: You can therefore complete the definition by calling zip with vec1 and vec2',
Line 1137: and then printing the result: 
Line 1138: case exactLength len1 vec2 of
Line 1139: Nothing => putStrLn "Vectors are different lengths"
Line 1140: Just vec2' => printLn (zip vec1 vec2')
Line 1141: For reference, the complete definition is given in the following listing.  
Line 1142: zipInputs : IO ()
Line 1143: zipInputs = do putStrLn "Enter first vector (blank line to end):"
Line 1144: (len1 ** vec1) <- readVect
Line 1145: putStrLn "Enter second vector (blank line to end):"
Line 1146: (len2 ** vec2) <- readVect
Line 1147: case exactLength len1 vec2 of
Line 1148: Nothing => putStrLn "Vectors are different lengths"
Line 1149: Just vec2' => printLn (zip vec1 vec2')
Line 1150: Exercises
Line 1151: In these exercises, you’ll find the following Prelude functions useful, in addition to
Line 1152: the functions discussed earlier in the chapter: openFile, closeFile, fEOF, fGetLine,
Line 1153: and writeFile. Use :doc to find out what each of these do. Also, see the sidebar,
Line 1154: “Handling I/O errors.”
Line 1155: 1
Line 1156: Write a function, readToBlank : IO (List String), that reads input from the
Line 1157: console until the user enters a blank line.
Line 1158:  2
Line 1159: Write a function, readAndSave : IO (), that reads input from the console until
Line 1160: the user enters a blank line, and then reads a filename from the console and
Line 1161: writes the input to that file.
Line 1162: Listing 5.12
Line 1163: Complete definition of zipInputs (DepPairs.idr)
Line 1164: 
Line 1165: --- 페이지 172 ---
Line 1166: 146
Line 1167: CHAPTER 5
Line 1168: Interactive programs: input and output processing
Line 1169: 3
Line 1170: Write a function, readVectFile : (filename : String) -> IO (n ** Vect n
Line 1171: String), that reads the contents of a file into a dependent pair containing a
Line 1172: length and a Vect of that length. If there are any errors, it should return an
Line 1173: empty vector.
Line 1174: 5.4
Line 1175: Summary
Line 1176: Idris provides a generic IO type for describing interactive actions.
Line 1177: Idris distinguishes between evaluation of pure functions and execution of inter-
Line 1178: active actions. The :exec command at the REPL executes interactive actions.
Line 1179: You can sequence interactive actions using do notation, which translates to
Line 1180: applications of the >>= operator.
Line 1181: You can produce pure values from interactive definitions by using the pure
Line 1182: function.
Line 1183: Idris provides a concise notation for pattern-matching on the result of an inter-
Line 1184: active action.
Line 1185: Dependent types express assumptions about inputs to functions, so you need to
Line 1186: validate user inputs to check that they satisfy those assumptions.
Line 1187: Dependent pairs allow you to pair two values, where the type of the second
Line 1188: value is computed from the first value.
Line 1189: You can use dependent pairs to express that a type’s argument, such as the
Line 1190: length of a vector, will not be known until the user enters some input.
Line 1191: Handling I/O errors
Line 1192: Many of the functions in the Exercises may return errors using Either. At first, you
Line 1193: can assume the result is successful using a pattern-matching binding, as described
Line 1194: in section 5.2.2: 
Line 1195: do Right h <- openFile filename Read
Line 1196: Right line <- fGetLine h
Line 1197: {- rest of code -}
Line 1198: Then, to make the function total, handle errors using the notation described in the
Line 1199: same section:
Line 1200: do Right h <- openFile filename Read
Line 1201: | Left err => putStrLn (show err)
Line 1202: Right line <- fGetLine h
Line 1203: | Left err => putStrLn (show err)
Line 1204: {- rest of code -} 