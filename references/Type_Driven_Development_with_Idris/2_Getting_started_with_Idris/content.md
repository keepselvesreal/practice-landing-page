Line 1: 
Line 2: --- 페이지 51 ---
Line 3: 25
Line 4: Getting started with Idris
Line 5: When learning any new language, it’s important to have a solid grasp of the funda-
Line 6: mentals before moving on to the more distinctive features of the language. With
Line 7: this in mind, before we begin exploring dependent types and type-driven develop-
Line 8: ment itself, we’ll look at some types and values that will be familiar to you from
Line 9: other languages, and you’ll see how they work in Idris. You’ll also see how to define
Line 10: functions and put these together to build a complete, if simple, Idris program.
Line 11:  If you’re already familiar with a pure functional language, particularly Haskell,
Line 12: much of this chapter will seem very familiar. Listing 2.1 shows a simple, but self-
Line 13: contained, Idris program that repeatedly prompts for input from the console and
Line 14: then displays the average length of the words in the input. If you’re already comfort-
Line 15: able reading this program with the help of the annotations, you can safely skip this
Line 16: chapter, as it deliberately avoids introducing any language features specific to Idris.1
Line 17: This chapter covers
Line 18: Using built-in types and functions
Line 19: Defining functions
Line 20: Structuring Idris programs
Line 21: 1 Comparing Idris to Haskell, the most important difference is that Idris doesn’t use lazy evaluation by
Line 22: default.
Line 23: 
Line 24: --- 페이지 52 ---
Line 25: 26
Line 26: CHAPTER 2
Line 27: Getting started with Idris
Line 28: Even so, I still suggest you browse through this chapter’s tips and notes and read the
Line 29: summary at the end to make sure there aren’t any small details you’ve missed.
Line 30:  Otherwise, don’t worry. By the end of this chapter we’ll have covered all of the nec-
Line 31: essary features for you to be able to implement similar programs yourself.
Line 32: module Main
Line 33: average : (str : String) -> Double
Line 34: average str = let numWords = wordCount str
Line 35: totalLength = sum (allLengths (words str)) in
Line 36: cast totalLength / cast numWords
Line 37: where
Line 38: wordCount : String -> Nat
Line 39: wordCount str = length (words str)
Line 40: allLengths : List String -> List Nat
Line 41: allLengths strs = map length strs
Line 42: showAverage : String -> String
Line 43: showAverage str = "The average word length is: " ++
Line 44: show (average str) ++ "\n"
Line 45: main : IO ()
Line 46: main = repl "Enter a string: " showAverage
Line 47: 2.1
Line 48: Basic types
Line 49: Idris provides some standard basic types and functions for working with various forms,
Line 50: characters, and strings. In this section, I’ll give you an overview of these, along with
Line 51: some examples. These basic types are defined in the Prelude, which is a collection of
Line 52: standard types and functions automatically imported by every Idris program.
Line 53:  I’ll show you several example expressions in this section, and it may seem fairly
Line 54: clear what they should do. Nevertheless, instead of simply reading them and nodding,
Line 55: I strongly recommending you type the examples at the Idris REPL. You’ll learn the syn-
Line 56: tax much more easily by using it than you will by merely reading it.
Line 57:  Along the way, we’ll also encounter a couple of useful REPL features that will allow
Line 58: us to store the results of calculations at the REPL.
Line 59: Listing 2.1
Line 60: A complete Idris program to calculate average word length (Average.idr)
Line 61: All top-level functions must have a type declaration. 
Line 62: Argument types may optionally be given names as 
Line 63: part of the type declaration. Here, there’s one 
Line 64: argument with type String and name str.
Line 65: The cast function explicitly converts
Line 66: between types. Here, the division operator
Line 67: requires a Double, but the totalLength and
Line 68: numWords variables are Nats.
Line 69: The where keyword introduces local 
Line 70: function definitions. Here, they’re 
Line 71: only visible inside the scope of the 
Line 72: average function.
Line 73: String is a primitive type, 
Line 74: unlike some other languages 
Line 75: (notably Haskell, where a 
Line 76: string is represented as a list 
Line 77: of characters).
Line 78: The function main, in a module 
Line 79: called Main, is the entry point to 
Line 80: an Idris program.
Line 81: repl is a function that repeatedly 
Line 82: displays a prompt, reads a String 
Line 83: from the console, and then 
Line 84: displays the result of running a 
Line 85: function on that String.
Line 86: 
Line 87: --- 페이지 53 ---
Line 88: 27
Line 89: Basic types
Line 90: THE PRELUDE
Line 91: The types and functions I’ll discuss are defined in the Prelude.
Line 92: The Prelude is Idris’s standard library, always available at the REPL and auto-
Line 93: matically imported by every Idris program. With the exception of some primi-
Line 94: tive types and operations, everything in the Prelude is written in Idris itself.
Line 95: 2.1.1
Line 96: Numeric types and values
Line 97: Idris provides several basic numeric types, including the following:
Line 98: 
Line 99: Int—A fixed-width signed integer type. It’s guaranteed to be at least 31 bits wide,
Line 100: but the exact width is system dependent.
Line 101: 
Line 102: Integer—An unbounded signed integer type. Unlike Int, there’s no limit to the
Line 103: size of the numbers that can be represented, other than your machine’s mem-
Line 104: ory, but this type is more expensive in terms of performance and memory
Line 105: usage.
Line 106: 
Line 107: Nat—An unbounded unsigned integer type. This is very often used for sizes and
Line 108: indexing of data structures, because they can never be negative. You’ll see
Line 109: much more of Nat later.
Line 110: 
Line 111: Double—A double-precision floating-point type.
Line 112: SUBTRACTION WITH NATS
Line 113: Because Nats can never be negative, a Nat can only
Line 114: be subtracted from a larger Nat.
Line 115: We can use standard numeric literals as values for each of these types. For example,
Line 116: the literal 333 can be of type Int, Integer, Nat, or Double. The literal 333.0 can be
Line 117: only of type Double, due to the explicit decimal point.
Line 118:  You can try some simple calculations
Line 119: at the REPL:
Line 120: Idris> 6 + 3 * 12
Line 121: 42 : Integer
Line 122: Idris> 6.0 + 3 * 12
Line 123: 42.0 : Double
Line 124: Note that Idris will treat a number as an
Line 125: Integer by default, unless there’s some
Line 126: context, and both operands must be the
Line 127: same type. Therefore, in the second of
Line 128: the two preceding expressions, the literal
Line 129: 6.0 can be only a Double, so the whole
Line 130: expression is a Double, and 3 and 12 are
Line 131: also treated as Doubles.
Line 132:  When an expression, such as 6 + 3 * 12,
Line 133: can be one of several types, you can make
Line 134: the type explicit with the notation the
Line 135: <type><expression>, to say that type is
Line 136: the required type of expression:
Line 137: REPL results
Line 138: The most recent result at the REPL
Line 139: can always be retrieved and used in
Line 140: further calculations by using the spe-
Line 141: cial value it: 
Line 142: Idris> 6 + 3 * 12
Line 143: 42 : Integer
Line 144: Idris> it * 2
Line 145: 84 : Integer
Line 146: It’s also possible to bind expressions
Line 147: to names at the REPL using the :let
Line 148: command: 
Line 149: Idris> :let x = 100
Line 150: Idris> x
Line 151: 100 : Integer
Line 152: Idris> :let y = 200.0
Line 153: Idris> y
Line 154: 200.0 : Double
Line 155: 
Line 156: --- 페이지 54 ---
Line 157: 28
Line 158: CHAPTER 2
Line 159: Getting started with Idris
Line 160: Idris> 6 + 3 * 12
Line 161: 42 : Integer
Line 162: Idris> the Int (6 + 3 * 12)
Line 163: 42 : Int
Line 164: Idris> the Double (6 + 3 * 12)
Line 165: 42.0 : Double
Line 166: “THE” EXPRESSIONS
Line 167: the is not built-in syntax but an ordinary Idris function,
Line 168: defined in the Prelude, which takes advantage of first-class types. 
Line 169: 2.1.2
Line 170: Type conversions using cast
Line 171: Arithmetic operators work on any numeric types, but both inputs and the output must
Line 172: have the same type. Sometimes, therefore, you’ll need to convert between types.
Line 173:  Let’s say you’ve defined an Integer and a Double at the REPL: 
Line 174: Idris> :let integerval = 6 * 6
Line 175: Idris> :let doubleval = 0.1
Line 176: Idris> integerval
Line 177: 36 : Integer
Line 178: Idris> doubleval
Line 179: 0.1 : Double
Line 180: If you try to add integerval and doubleval, Idris will complain that they aren’t the
Line 181: same type:
Line 182: Idris> integerval + doubleval
Line 183: (input):1:8-9:When checking an application of function Prelude.Classes.+:
Line 184: Type mismatch between
Line 185: Double (Type of doubleval)
Line 186: and
Line 187: Integer (Expected type)
Line 188: To fix this, you can use the cast function, which converts its input to the required
Line 189: type, as long as that conversion is valid. Here, you can cast the Integer to a Double:
Line 190: Idris> cast integerval + doubleval
Line 191: 36.1 : Double
Line 192: Idris supports casting between all the primitive types, and it’s possible to add user-
Line 193: defined casts, as you’ll see in chapter 7. Note that some casts may lose information,
Line 194: such as casting a Double to an Integer.
Line 195: Specifying the target of a cast
Line 196: You can also use the to specify which type you want to cast to, as in these examples: 
Line 197: Idris> the Integer (cast 9.9)
Line 198: 9 : Integer
Line 199: Idris> the Double (cast (4 + 4))
Line 200: 8.0 : Double
Line 201: 
Line 202: --- 페이지 55 ---
Line 203: 29
Line 204: Basic types
Line 205: 2.1.3
Line 206: Characters and strings
Line 207: Idris also provides Unicode characters and strings as primitive types, along with some
Line 208: useful primitive functions for manipulating them. 
Line 209: Character literals (of type Char) are enclosed in single quotation marks, such as
Line 210: 'a'.
Line 211: String literals (of type String) are enclosed in double quotation marks, such as
Line 212: "Hello world!"
Line 213: Like many other languages, Idris supports special characters in character and string
Line 214: literals by using escape sequences, beginning with a backslash. For example, a newline
Line 215: character is indicated using \n: 
Line 216: Idris> :t '\n'
Line 217: '\n' : Char
Line 218: Idris> :t "Hello world!\n"
Line 219: "Hello world!\n" : String
Line 220: These are the most common escape sequences: 
Line 221: 
Line 222: \' for a literal single quote
Line 223: 
Line 224: \" for a literal double quote
Line 225: 
Line 226: \\ for a literal backslash
Line 227: 
Line 228: \n for a newline character
Line 229: 
Line 230: \t for a tab character
Line 231: The Prelude defines several useful functions for manipulating Strings. You can see
Line 232: some of these in action at the REPL: 
Line 233: Idris> length "Hello!"
Line 234: 6 : Nat
Line 235: Idris> reverse "drawer"
Line 236: "reward" : String
Line 237: Idris> substr 6 5 "Hello world"
Line 238: "world" : String
Line 239: Idris> "Hello" ++ " " ++ "World"
Line 240: "Hello World" : String
Line 241: Here’s a brief explanation of these functions: 
Line 242: 
Line 243: length—Gives the length of its argument as a Nat because a String can’t have a
Line 244: negative length
Line 245: 
Line 246: reverse—Returns a reversed version of its input
Line 247: 
Line 248: substr—Returns a substring of an input string, given a position to start at and
Line 249: the desired length of the substring
Line 250: 
Line 251: ++—An operator that concatenates two Strings
Line 252: 
Line 253: --- 페이지 56 ---
Line 254: 30
Line 255: CHAPTER 2
Line 256: Getting started with Idris
Line 257: Notice the syntax of the function calls. In Idris, functions are separated from their
Line 258: arguments by whitespace. If the argument is a complex expression, it must be brack-
Line 259: eted, as follows: 
Line 260: Idris> length ("Hello" ++ " " ++ "World")
Line 261: 11 : Nat
Line 262: FUNCTION SYNTAX
Line 263: Calling functions by separating the arguments with spaces
Line 264: may seem strange at first. There’s a good reason for it, though, as you’ll dis-
Line 265: cover when we look at function types later in this chapter. In short, it makes
Line 266: manipulating functions much more flexible. 
Line 267: 2.1.4
Line 268: Booleans
Line 269: Idris provides a Bool type for representing truth values. A Bool can take the value
Line 270: True or False. The operators && and || represent logical and and or, respectively:
Line 271: Idris> True && False
Line 272: False : Bool
Line 273: Idris> True || False
Line 274: True : Bool
Line 275: The usual comparison operators (<, <=, ==, /=, >, >=) are available:
Line 276: Idris> 3 > 2
Line 277: True : Bool
Line 278: Idris> 100 == 99
Line 279: False : Bool
Line 280: Idris> 100 /= 99
Line 281: True : Bool
Line 282: INEQUALITY
Line 283: The inequality operator in Idris is /=, which follows Haskell syn-
Line 284: tax, rather than !=, which would follow the syntax of languages like C and Java.
Line 285: There is also an if...then...else construct. This is an expression, so it must always
Line 286: include both a then branch and an else branch. For example, you can write an
Line 287: expression that evaluates to a different message as a String, depending on the length
Line 288: of a word:
Line 289: Idris> :let word = "programming"
Line 290: Idris> if length word > 10 then "What a long word!" else "Short word"
Line 291: "What a long word!" : String
Line 292: 2.2
Line 293: Functions: the building blocks of Idris programs
Line 294: Now that you’ve seen some basic types and a simple control structure, you can begin
Line 295: defining functions. In this section, you’ll write some Idris functions using the basic
Line 296: types you’ve seen so far, load them into the Idris system, and test them at the REPL.
Line 297: You’ll also see how the functional programming style allows you to write more generic
Line 298: programs in two ways: 
Line 299: 
Line 300: --- 페이지 57 ---
Line 301: 31
Line 302: Functions: the building blocks of Idris programs
Line 303: Using variables in function types, so that functions can be written to work with
Line 304: several different types
Line 305: Using higher-order functions to capture common programming patterns
Line 306: 2.2.1
Line 307: Function types and definitions
Line 308: Function types are composed of one or more input types and an output type. For exam-
Line 309: ple, a function that takes an Int as input and returns another Int would be written as
Line 310: Int -> Int. The following listing shows a simple function definition with this type, the
Line 311: double function.
Line 312: double : Int -> Int
Line 313: double x = x + x
Line 314: You can try this function by typing it into a file, Double.idr; loading it into the Idris
Line 315: REPL by typing idris Double.idr at the shell prompt; and then trying some exam-
Line 316: ples at the REPL:
Line 317: *Double> double 47
Line 318: 94 : Int
Line 319: *Double> double (double 15)
Line 320: 60 : Int
Line 321: Figure 2.1 shows the components of this function definition. All functions in Idris,
Line 322: like double, are introduced with a type declaration and then defined by equations with a
Line 323: left side and a right side.
Line 324: An expression is evaluated by rewriting the expression according to these equations
Line 325: until no further rewriting can be done. Functions, therefore, define rules by which
Line 326: expressions can be rewritten. For example, consider the definition of double:
Line 327: double x = x + x
Line 328: Listing 2.2
Line 329: A function to double an Int (Double.idr)
Line 330: The function type states that it takes an 
Line 331: Int as input and returns an Int as output.
Line 332: The function definition gives an equation that 
Line 333: defines what it means to double an input.
Line 334: double : Int -> Int
Line 335: double x = x + x
Line 336: Function
Line 337: name
Line 338: Type declaration
Line 339: Function definition
Line 340: Function
Line 341: type
Line 342: Left
Line 343: side
Line 344: Right
Line 345: side
Line 346: Figure 2.1
Line 347: The components 
Line 348: of a function definition
Line 349: 
Line 350: --- 페이지 58 ---
Line 351: 32
Line 352: CHAPTER 2
Line 353: Getting started with Idris
Line 354: This means that whenever the Idris evaluator encounters an expression of the form
Line 355: double x, with some expression standing for x, it should be rewritten as x + x.
Line 356:  So, in the example double (double 15),
Line 357: First, the inner double 15 is rewritten as 15 + 15.
Line 358: 
Line 359: 15 + 15 is rewritten as 30.
Line 360: 
Line 361: double 30 is rewritten as 30 + 30.
Line 362: 
Line 363: 30 + 30 is rewritten as 60.
Line 364: Optionally, you can give explicit names in the input types of a function. For example,
Line 365: you could write the type of double as follows:
Line 366: double : (value : Int) -> Int
Line 367: This has exactly the same meaning as the previous declaration (double : Int ->
Line 368: Int). There are two reasons why you might make the names of the arguments explicit: 
Line 369: Naming the argument in the type can give the reader some information about
Line 370: the purpose of the argument.
Line 371: Naming the argument means you can refer to it later.
Line 372: You’ll see more of this in chapter 4 when we begin to explore dependent types in
Line 373: depth. For now, remember the example of first-class types from chapter 1, where I
Line 374: gave the following Idris type for getStringOrInt:
Line 375: getStringOrInt : (x : Bool) -> StringOrInt x
Line 376: The first argument, of type Bool, was given the name x, which then appears in the
Line 377: return type.
Line 378: TYPE DECLARATIONS ARE REQUIRED!
Line 379: Functions in Idris must have an explicit
Line 380: type declaration, like double : Int -> Int here. Some other functional lan-
Line 381: guages, most notably Haskell and ML, allow programmers to omit type decla-
Line 382: rations and have the compiler infer the type. In a language with first-class
Line 383: types, however, this generally turns out to be impossible. In any case, it’s
Line 384: Evaluation order
Line 385: You might have noticed that instead of choosing to evaluate the inner double 15
Line 386: first, you could have chosen the outer double (double 15), which would have
Line 387: reduced to double 15 + double 15. Either order is possible, and each would lead to
Line 388: the same result. Idris, by default, will evaluate the innermost expression first. In other
Line 389: words, it will evaluate function arguments before function definitions.
Line 390: There are merits and drawbacks to both choices, and as a result this topic has been
Line 391: debated at length! Now is not the time to revisit this debate, but if you’re interested,
Line 392: you can investigate lazy evaluation. Idris supports lazy evaluation using explicit types,
Line 393: as you’ll see in chapter 11.
Line 394: 
Line 395: --- 페이지 59 ---
Line 396: 33
Line 397: Functions: the building blocks of Idris programs
Line 398: undesirable to omit type declarations in type-driven development. Our phi-
Line 399: losophy is to use types to help us write programs, rather than to use programs
Line 400: to help us infer types!
Line 401: 2.2.2
Line 402: Partially applying functions
Line 403: When a function has more than one argument, you can create a specialized version of
Line 404: the function by omitting the later arguments. This is called partial application.
Line 405:  For example, assume you have an add function that adds two integers, defined as
Line 406: follows in the Partial.idr file:
Line 407: add : Int -> Int -> Int
Line 408: add x y = x + y
Line 409: If you apply the function to two arguments, it will evaluate to an Int:
Line 410: *Partial> add 2 3
Line 411: 5 : Int
Line 412: If, on the other hand, you only apply the function to one argument, omitting the sec-
Line 413: ond, Idris will return a function of type Int -> Int:
Line 414: *Partial> add 2
Line 415: add 2 : Int -> Int
Line 416: By applying add to only one argument, you’ve created a new specialized function, add
Line 417: 2, that adds 2 to its argument. You can see this more explicitly by creating a new func-
Line 418: tion with :let:
Line 419: *Partial> :let addTwo = add 2
Line 420: *Partial> :t addTwo
Line 421: addTwo : Int -> Int
Line 422: *Partial> addTwo 3
Line 423: 5 : Int
Line 424: The function application syntax, applying functions to arguments simply by separat-
Line 425: ing the function from the argument with whitespace, gives a particularly concise syn-
Line 426: tax for partial application. Partial application is common in Idris programs, and you’ll
Line 427: see some examples of it in action shortly, in section 2.2.5. 
Line 428: 2.2.3
Line 429: Writing generic functions: variables in types
Line 430: As well as concrete types, such as Int, String, and Bool, function types can contain vari-
Line 431: ables. Variables in a function type can be instantiated with different values, just like
Line 432: variables in functions themselves.
Line 433:  For example, let’s consider the identity function, which returns its input,
Line 434: unchanged. The identity function on Ints is written as follows:
Line 435: identityInt : Int -> Int
Line 436: identityInt x = x
Line 437: 
Line 438: --- 페이지 60 ---
Line 439: 34
Line 440: CHAPTER 2
Line 441: Getting started with Idris
Line 442: Similarly, the identity function on Strings is written like this:
Line 443: identityString : String -> String
Line 444: identityString x = x
Line 445: And here’s the identity function on Bools:
Line 446: identityBool : Bool -> Bool
Line 447: identityBool x = x
Line 448: You may have noticed a pattern here. In each case the definition is the same! You
Line 449: don’t need to know anything about x because you’re returning it unchanged in each
Line 450: case. So, instead of writing an identity function for every type separately, you can write
Line 451: one identity function using a variable, ty, at the type level, in place of a concrete type:
Line 452: identity : ty -> ty
Line 453: identity x = x
Line 454: THE ID FUNCTION
Line 455: In fact, there is an identity function in the Prelude called
Line 456: id, defined in exactly the same way as identity here.
Line 457: The ty in the type of identity is a variable, standing for any type. Therefore,
Line 458: identity can be called with any input type, and will return an output with the same
Line 459: type as the input.
Line 460: VARIABLE NAMES IN TYPES
Line 461: Any name that appears in a type declaration,
Line 462: begins with a lowercase letter, and is otherwise undefined is assumed to be a
Line 463: variable. Note that I’m careful to call these variables, rather than type variables.
Line 464: This is because, with dependent types, variables in types don’t necessarily
Line 465: stand for only types, as you’ll see in chapter 3.
Line 466: You’ve already seen a form of the identity function when working with numeric types:
Line 467: the is an identity function. It’s defined in the Prelude as follows:
Line 468: the : (ty : Type) -> ty -> ty
Line 469: the ty x = x
Line 470: It takes an explicit type as its first argument, which is explicitly named ty. The type of
Line 471: the second argument is given by the input value of the first argument. This is a simple
Line 472: example of dependent types in action, in that the value of an earlier argument gives
Line 473: the type of a later argument. You can see this explicitly at the REPL, by partially apply-
Line 474: ing the to only one argument:
Line 475: Idris> :t the Int
Line 476: the Int : Int -> Int
Line 477: Idris> :t the String
Line 478: the String : String -> String
Line 479: Idris> :t the Bool
Line 480: the Bool : Bool -> Bool
Line 481: 
Line 482: --- 페이지 61 ---
Line 483: 35
Line 484: Functions: the building blocks of Idris programs
Line 485: 2.2.4
Line 486: Writing generic functions with constrained types
Line 487: The first function you saw in section 2.2.1, double, doubles the Int given as input:
Line 488: double : Int -> Int
Line 489: double x = x + x
Line 490: But what about other numeric types? For example, you could also write a function to
Line 491: double a Nat, or an Integer:
Line 492: doubleNat : Nat -> Nat
Line 493: doubleNat x = x + x
Line 494: doubleInteger : Integer -> Integer
Line 495: doubleInteger x = x + x
Line 496: As with identity, you’re probably starting to see a pattern here, so let’s see what hap-
Line 497: pens if we try to replace the input and output types with a variable. Put the following
Line 498: in a file called Generic.idr and load it into Idris:
Line 499: double : ty -> ty
Line 500: double x = x + x
Line 501: You’ll find that Idris rejects this definition, with the following error message:
Line 502: Generic.idr:2:8:
Line 503: When checking right hand side of double with expected type
Line 504: ty
Line 505: ty is not a numeric type
Line 506: The problem is that, unlike identity, double needs to know something about its
Line 507: input x, specifically that it’s numeric. You can only use arithmetic operators on
Line 508: numeric types, so you need to constrain ty so that it only stands for numeric types. The
Line 509: following listing shows how you can do this.
Line 510: double : Num ty => ty -> ty
Line 511: double x = x + x
Line 512: The type Num ty => ty -> ty can be read as, “A function with input type ty and out-
Line 513: put type ty under the constraint that ty is a numeric type.”
Line 514: TYPE CONSTRAINTS
Line 515: Constraints on generic types can be user-defined using
Line 516: interfaces, which we’ll cover in depth in chapter 7. Here, Num is an interface
Line 517: provided by Idris. Interfaces can be given implementations for specific types,
Line 518: and the Num interface has implementations for numeric types.
Line 519: Perhaps surprisingly, arithmetic and comparison operators aren’t primitive operators
Line 520: in Idris, but rather functions with constrained generic types. Infix operators such as +,
Line 521: Listing 2.3
Line 522: A generic type, constrained to numeric types (Generic.idr)
Line 523: The Num ty before the main part of 
Line 524: the function type indicates that ty 
Line 525: can only stand for numeric types.
Line 526: 
Line 527: --- 페이지 62 ---
Line 528: 36
Line 529: CHAPTER 2
Line 530: Getting started with Idris
Line 531: ==, and <= are really functions with two inputs, as you can see by checking their types
Line 532: at the REPL:
Line 533: Idris> :t (+)
Line 534: (+) : Num ty => ty -> ty -> ty
Line 535: Idris> :t (==)
Line 536: (==) : Eq ty => ty -> ty -> Bool
Line 537: Idris> :t (<=)
Line 538: (<=) : Ord ty => ty -> ty -> Bool
Line 539: As well as Num for numeric types, here you can see two other constraints provided by
Line 540: Idris: 
Line 541: 
Line 542: Eq states that the type must support the equality and inequality operators, ==
Line 543: and /=.
Line 544: 
Line 545: Ord states that the type must support the comparison operators <, <=, >, and >=.
Line 546: 2.2.5
Line 547: Higher-order function types
Line 548: There are no restrictions on what the argument or return types of a function can be.
Line 549: You’ve already seen how functions of multiple arguments are really functions that
Line 550: return something with a function type. Similarly, functions can take functions as argu-
Line 551: ments. Such functions are called higher-order functions.
Line 552:  Higher-order functions can be used to create abstractions for repeated program-
Line 553: ming patterns. For example, say you’ve defined a quadruple function that quadruples
Line 554: its input for any number, using double:
Line 555: quadruple : Num a => a -> a
Line 556: quadruple x = double (double x)
Line 557: Infix operators and operator sections
Line 558: Infix operators in Idris aren’t a primitive part of the syntax, but are defined by func-
Line 559: tions. Putting operators in brackets, as with (+), (==), and (<=) in the REPL exam-
Line 560: ple, means that they’ll be treated as ordinary function syntax. For example, you can
Line 561: apply (+) to one argument:
Line 562: Idris> :t (+) 2
Line 563: (+) 2 : Integer -> Integer
Line 564: Infix operators can also be partially applied using operator sections: 
Line 565: 
Line 566: (< 3) gives a function that returns whether its input is less than 3.
Line 567: 
Line 568: (3 <) gives a function that returns whether 3 is less than its input.
Line 569: An operator in brackets with only one argument is therefore considered to be a func-
Line 570: tion that expects the other missing argument. 
Line 571: 
Line 572: --- 페이지 63 ---
Line 573: 37
Line 574: Functions: the building blocks of Idris programs
Line 575: Or say you have a Shape type that represents any geometric shape, and a function
Line 576: rotate : Shape -> Shape that rotates a shape through 90 degrees. You could define
Line 577: a turn_around function that rotates a shape through 180 degrees as follows:
Line 578: turn_around : Shape -> Shape
Line 579: turn_around x = rotate (rotate x)
Line 580: Each of these functions has exactly the same pattern, but they work on different input
Line 581: types. You can capture this pattern using a higher-order function to apply a function
Line 582: to an argument twice. The next listing gives a definition of a twice function, along
Line 583: with new definitions of quadruple and rotate.
Line 584: twice : (a -> a) -> a -> a
Line 585: twice f x = f (f x)
Line 586: Shape : Type
Line 587: rotate : Shape -> Shape
Line 588: quadruple : Num a => a -> a
Line 589: quadruple = twice double
Line 590: turn_around : Shape -> Shape
Line 591: turn_around = twice rotate
Line 592: In chapter 1, I introduced the concept of “holes,” which are incomplete function defi-
Line 593: nitions. The type declarations with no definitions in listing 2.4, Shape and rotate, are
Line 594: treated as holes. They allow you to try an idea (such as how to implement
Line 595: turn_around in terms of rotate) without fully defining the types and functions.
Line 596: Listing 2.4
Line 597: Defining quadruple and rotate using a higher-order function (HOF.idr)
Line 598: twice takes a function as its first 
Line 599: argument, and the argument to apply 
Line 600: that function to as its second.
Line 601: The definition follows exactly the 
Line 602: same pattern as the initial definitions 
Line 603: of quadruple and turn_around but 
Line 604: with a generic function f.
Line 605: These are type declarations 
Line 606: with no definitions.
Line 607: This implements quadruple by directly 
Line 608: instantiating “twice” with “double”.
Line 609: This implements turn_around by directly 
Line 610: instantiating twice with “rotate”.
Line 611: Partial application in definitions
Line 612: In listing 2.4, quadruple and turn_around have function types, Num a => a -> a and
Line 613: Shape -> Shape, respectively, but in their definitions neither has an argument.
Line 614: The only requirement when checking a definition is that both sides of the definition
Line 615: must have the same type. You can check that this is the case here by looking at the
Line 616: types of the left and right sides of the definition at the REPL. You have the following
Line 617: definition:
Line 618: turn_around = twice rotate
Line 619: 
Line 620: --- 페이지 64 ---
Line 621: 38
Line 622: CHAPTER 2
Line 623: Getting started with Idris
Line 624: The definitions of quadruple and turn_around both use partial application, as
Line 625: described in section 2.2.2.
Line 626:  Another common use of partial application is in constructing arguments for
Line 627: higher-order functions. Consider this example, using HOF.idr and adding the defini-
Line 628: tion of add from section 2.2.2: 
Line 629: *HOF> twice (add 5) 10
Line 630: 20 : Int
Line 631: This uses a partial application of the add function to add 5 to an Int, twice. Because
Line 632: twice requires a function of one argument, and add takes two arguments, you can
Line 633: apply add to one argument so that it’s usable in an application of twice.
Line 634:  You could also use an operator section, as described at the end of section 2.2.4: 
Line 635: *HOF> twice (5 +) 10
Line 636: 20 : Integer
Line 637: Note that, in the absence of any other type information, Idris has defaulted to Integer,
Line 638: as described in section 2.1.1. 
Line 639: 2.2.6
Line 640: Anonymous functions
Line 641: When using higher-order functions, it’s often useful to pass an anonymous function as
Line 642: an argument. An anonymous function is generally a small function that you only
Line 643: expect to use once, so there’s no need to create a top-level definition for it.
Line 644:  For example, you could pass an anonymous function that squares its input to
Line 645: twice:
Line 646: *HOF> twice (\x => x * x) 2
Line 647: 16 : Integer
Line 648: Anonymous functions are introduced with a backslash \ followed by a list of argu-
Line 649: ments. If you check the type of the preceding anonymous function, you’ll see that it
Line 650: has a function type:
Line 651: *HOF> :t \x => x * x
Line 652: \x => x * x : Integer -> Integer
Line 653: Anonymous functions can take more than one argument, and arguments can option-
Line 654: ally be given explicit types:
Line 655: (continued)
Line 656: By checking the types at the REPL, you can see that both turn_around and twice
Line 657: rotate have the same type:
Line 658: Idris> :t turn_around
Line 659: turn_around : Shape -> Shape
Line 660: Idris> :t twice rotate
Line 661: twice rotate : Shape -> Shape
Line 662: 
Line 663: --- 페이지 65 ---
Line 664: 39
Line 665: Functions: the building blocks of Idris programs
Line 666: *HOF> :t \x : Int, y : Int => x + y
Line 667: \x, y => x + y : Int -> Int -> Int
Line 668: Note that the output doesn’t show the types explicitly. 
Line 669: 2.2.7
Line 670: Local definitions: let and where
Line 671: As functions get larger, it’s usually a good idea to break
Line 672: them down into smaller definitions. Idris provides two
Line 673: constructs for locally defining variables and functions: let
Line 674: and where.
Line 675:  Figure 2.2 illustrates the syntax for let bindings, which
Line 676: define local variables.
Line 677:  If you evaluate this expression at the REPL, you’ll see
Line 678: the following:
Line 679: Idris> let x = 50 in x + x
Line 680: 100 : Integer
Line 681: The next listing shows a larger example of let in action. It
Line 682: defines a function, longer, that takes two Strings and
Line 683: returns the length of the longer one. It uses let to record
Line 684: the length of each input.
Line 685: longer : String -> String -> Nat
Line 686: longer word1 word2
Line 687: = let len1 = length word1
Line 688: len2 = length word2 in
Line 689: if len1 > len2 then len1 else len2
Line 690: MULTIPLE LETS
Line 691: There can be several definitions in a let block. In listing 2.5,
Line 692: for example, there are two local variables defined in the let block in longer.
Line 693: Whereas let blocks contain local variable definitions, where blocks contain local func-
Line 694: tion definitions. Listing 2.6 shows where in action. It defines a function to calculate
Line 695: the length of the hypotenuse of a triangle, using the Pythagorean Theorem and a
Line 696: local square function.
Line 697: pythagoras : Double -> Double -> Double
Line 698: pythagoras x y = sqrt (square x + square y)
Line 699: where
Line 700: square : Double -> Double
Line 701: square x = x * x
Line 702: Listing 2.5
Line 703: Local variables with let (Let_Where.idr)
Line 704: Listing 2.6
Line 705: Local function definitions with where (Let_Where.idr)
Line 706: Records the length of the first word
Line 707: Records the length of the second word
Line 708: Returns whichever of 
Line 709: the lengths is longest.
Line 710: sqrt is defined in the Prelude.
Line 711: This definition is only visible 
Line 712: within the scope of pythagoras.
Line 713: let x = 50 in x + x
Line 714: Local variable
Line 715: definition
Line 716: Scope of
Line 717: definition
Line 718: Figure 2.2
Line 719: A local variable 
Line 720: definition: in the expression 
Line 721: after the in keyword, x has 
Line 722: the value 50.
Line 723: 
Line 724: --- 페이지 66 ---
Line 725: 40
Line 726: CHAPTER 2
Line 727: Getting started with Idris
Line 728: Generally, let is useful for breaking a complex expression into smaller subexpres-
Line 729: sions, and where is useful for defining more-complex functions that are only relevant
Line 730: in the local context. 
Line 731: 2.3
Line 732: Composite types
Line 733: Composite types are composed of other types. In this section, we’ll look at two of the
Line 734: most common composite types provided by Idris: tuples and lists.
Line 735: 2.3.1
Line 736: Tuples
Line 737: A tuple is a fixed-size collection, where each value in the collection can have a different
Line 738: type. For example, a pair of an Integer and a String can be written as follows:
Line 739: Idris> (94, "Pages")
Line 740: (94, "Pages") : (Integer, String)
Line 741: Tuples are written as a bracketed, comma-separated list of values. Notice that the type
Line 742: of the pair (94, "Pages") is (Integer, String). Tuple types are written using the
Line 743: same syntax as tuple values.
Line 744:  The fst and snd functions extract the first and second items, respectively, from a
Line 745: pair:
Line 746: Idris> :let mypair = (94, "Pages")
Line 747: Idris> fst mypair
Line 748: 94 : Integer
Line 749: Idris> snd mypair
Line 750: "Pages" : String
Line 751: Both fst and snd have generic types, because pairs can contain any types. You can
Line 752: check the type of each at the REPL:
Line 753: Idris> :t fst
Line 754: fst : (a, b) -> a
Line 755: Idris> :t snd
Line 756: snd : (a, b) -> b
Line 757: You can read the type of fst, for example, as “Given a pair of an a and a b, return the
Line 758: value that has type a.” In these types, you know that both a and b are variables because
Line 759: they begin with lowercase letters.
Line 760:  Tuples can have any number of components, including zero:
Line 761: Idris> ('x', 8, String)
Line 762: ('x', 8, String) : (Char, Integer, Type)
Line 763: Idris> ()
Line 764: () : ()
Line 765: The empty tuple, (), is often referred to as “unit” and its type as “the unit type.”
Line 766: Notice that the syntax is overloaded, and Idris will decide whether () means unit or
Line 767: the unit type from the context.
Line 768: 
Line 769: --- 페이지 67 ---
Line 770: 41
Line 771: Composite types
Line 772:  
Line 773: Tuples can also be arbitrarily deeply nested:
Line 774: Idris> (('x', 8), (String, 'y', 100), "Hello")
Line 775: (('x', 8), (String, 'y', 100), "Hello")
Line 776: : ((Char, Integer), (Type, Char, Integer), String)
Line 777: 2.3.2
Line 778: Lists
Line 779: Lists, like tuples, are collections of values. Unlike tuples, lists can be any size, but every
Line 780: element must have the same type. Lists are written as comma-separated lists of values
Line 781: in square brackets, as follows.
Line 782: Idris> [1, 2, 3, 4]
Line 783: [1, 2, 3, 4] : List Integer
Line 784: Idris> ["One", "Two", "Three", "Four"]
Line 785: ["One", "Two", "Three", "Four"] : List String
Line 786: The type of each of these expressions, List Integer and List String, indicates the
Line 787: element type that Idris has inferred for the list. In type-driven development, we typically
Line 788: give types first, and then write a corresponding value or function that satisfies this
Line 789: type. At the REPL, it would be inconvenient to do this for every value, so Idris will try
Line 790: Colors in the REPL
Line 791: You may have noticed that some values and types in the REPL are colored differently,
Line 792: particularly when evaluating the empty tuple (). This is semantic highlighting, and it
Line 793: indicates whether a subexpression is a type, value, function, or variable. By default,
Line 794: the REPL displays each as follows: 
Line 795: Types are blue.
Line 796: Values (more precisely, data constructors, as I’ll explain in chapter 3) are red.
Line 797: Functions are green.
Line 798: Variables are magenta.
Line 799: If these colors aren’t to your liking or are hard to distinguish (for example, if you’re
Line 800: color blind), you can change the settings with the :colour command.
Line 801: Tuples and pairs
Line 802: Internally, all tuples other than the empty tuple are stored as nested pairs. That is,
Line 803: if you write (1, 2, 3, 4), Idris will treat this in the same way as (1, (2, (3, 4))).
Line 804: The REPL will always display a tuple in the non-nested form: 
Line 805: Idris> (1, (2, (3, 4)))
Line 806: (1, 2, 3, 4) : (Integer, Integer, Integer, Integer)
Line 807: 
Line 808: --- 페이지 68 ---
Line 809: 42
Line 810: CHAPTER 2
Line 811: Getting started with Idris
Line 812: to infer a type for the given value. Unfortunately, it’s not always possible. For example,
Line 813: if you give it an empty list, Idris doesn’t know what the element type should be:
Line 814: Idris> []
Line 815: (input):Can't infer argument elem to []
Line 816: This error message means that Idris can’t work out the element type (which happens
Line 817: to be named elem) for the empty list []. The problem can be resolved in this case by
Line 818: giving an explicit type, using the:
Line 819: Idris> the (List Int) []
Line 820: [] : List Int
Line 821: Like strings, lists can be concatenated with the ++ operator, provided that both oper-
Line 822: ands have the same element type:
Line 823: Idris> [1, 2, 3] ++ [4, 5, 6, 7]
Line 824: [1, 2, 3, 4, 5, 6, 7] : List Integer
Line 825: You can add an element to the front of a list using the :: (pronounced “cons”) operator: 
Line 826: Idris> 1 :: [2, 3, 4]
Line 827: [1, 2, 3, 4] : List Integer
Line 828: Idris> 1 :: 2 :: 3 :: 4 :: []
Line 829: [1, 2, 3, 4] : List Integer
Line 830: Syntactic sugar for lists
Line 831: The :: operator is the primitive operator for constructing lists from a head element
Line 832: and a tail, and Nil is a primitive name for the empty list. A list can therefore take one
Line 833: of the following two canonical forms: 
Line 834: 
Line 835: Nil, the empty list
Line 836: 
Line 837: x :: xs, where x is an element, and xs is another list
Line 838: Because this can get quite verbose, Idris provides syntactic sugar for lists. List literals
Line 839: consisting of comma-separated elements inside square brackets are desugared to
Line 840: these primitive forms. For example, [] is desugared directly to Nil, and [1, 2, 3]
Line 841: is desugared to 1 :: (2 :: (3 :: Nil)).
Line 842: There’s also a more concise notation for ranges of numbers. Here are a few examples: 
Line 843: 
Line 844: [1..5] expands to the list [1, 2, 3, 4, 5].
Line 845: 
Line 846: [1,3..9] expands to the list [1, 3, 5, 7, 9].
Line 847: 
Line 848: [5,4..1] expands to the list [5, 4, 3, 2, 1].
Line 849: More generally, [n..m] gives an increasing list of numbers between n and m, and
Line 850: [n,m..p] gives a list of numbers between n and p with the step given by the differ-
Line 851: ence between n and m. 
Line 852: 
Line 853: --- 페이지 69 ---
Line 854: 43
Line 855: Composite types
Line 856: 2.3.3
Line 857: Functions with lists
Line 858: We’ll discuss lists in more depth in the next chapter, including how to define func-
Line 859: tions over lists, but there are several useful functions defined in the Prelude. Let’s take
Line 860: a look at some of these.
Line 861:  The words function, of type String -> List String, converts a string into a list of
Line 862: the whitespace-separated components of the string:2
Line 863: Idris> words "'Twas brillig, and the slithy toves"
Line 864: ["'Twas", "brillig,", "and", "the", "slithy", "toves"] : List String
Line 865: The unwords function, of type List String -> String, does the opposite, converting
Line 866: a list of words into a string where the words are separated by a space:
Line 867: Idris> unwords ["One", "two", "three", "four!"]
Line 868: "One two three four!" : String
Line 869: You’ve already seen a length function for calculating the lengths of strings. There’s
Line 870: also an overloaded length function, of type List a -> Nat, that gives the length of a
Line 871: list:
Line 872: Idris> length ["One", "two", "three", "four!"]
Line 873: 4 : Nat
Line 874: You can use length and words to write a word-count function for strings:
Line 875: wordCount : String -> Nat
Line 876: wordCount str = length (words str)
Line 877: The map function is a higher-order function that applies a function to every element
Line 878: in a list. It has the type (a -> b) -> List a -> List b. This example finds the lengths of
Line 879: every word in a list:
Line 880: Idris> map length (words "How long are these words?")
Line 881: [3, 4, 3, 5, 6] : List Nat
Line 882: You can use map and length to write a function that gets the length of every element
Line 883: in a list of Strings:
Line 884: allLengths : List String -> List Nat
Line 885: allLengths strs = map length strs
Line 886: 2 The words name comes from a similar function in the Haskell libraries. Many Idris function names follow
Line 887: Haskell terminology.
Line 888: Type of map
Line 889: If you check the type of map at the REPL, you’ll see something slightly different: 
Line 890: Idris> :t map
Line 891: map : Functor f => (a -> b) -> f a -> f b
Line 892: 
Line 893: --- 페이지 70 ---
Line 894: 44
Line 895: CHAPTER 2
Line 896: Getting started with Idris
Line 897: The filter function is another higher-order function that filters a list according to a
Line 898: Boolean function. It has type (a -> Bool) -> List a -> List a and returns a new list of
Line 899: everything in the input list for which the function returns True. For example, here’s
Line 900: how you find all the numbers larger than 10 in a list:
Line 901: Idris> filter (> 10) [1,11,2,12,3,13,4,14]
Line 902: [11, 12, 13, 14] : List Integer
Line 903: The sum function, of type Num a => List a -> a, calculates the sum of a list of numbers:
Line 904: Idris> sum [1..100]
Line 905: 5050 : Integer
Line 906: The type of sum states that every element of the input List must have the same type, a,
Line 907: and that type is constrained by Num.
Line 908:  You now know enough to be able to define a function named average that com-
Line 909: putes the average length of the words in a string. This function is defined in the next
Line 910: listing, which shows the complete Idris file Average.idr. 
Line 911: module Average
Line 912: export
Line 913: average : String -> Double
Line 914: average str = let numWords = wordCount str
Line 915: totalLength = sum (allLengths (words str)) in
Line 916: Listing 2.7
Line 917: Calculating the average word length in a string (Average.idr)
Line 918: (continued)
Line 919: The reason for this is that map can work on a variety of structures, not just lists, so
Line 920: it has a constrained generic type. You’ll learn about Functor in chapter 7, but for the
Line 921: moment it’s fine to read f as List in this type.
Line 922: Overloading functions
Line 923: You’ve seen the length function on both strings and lists. This works because Idris
Line 924: allows function names to be overloaded to work on multiple types. You can see
Line 925: what’s happening by checking the type of length at the REPL:
Line 926: *lists> :t length
Line 927: Prelude.List.length : List a -> Nat
Line 928: Prelude.Strings.length : String -> Nat
Line 929: In fact, there are two functions called length. The prefixes Prelude.List and
Line 930: Prelude.Strings are the namespaces these functions are defined in. Idris decides
Line 931: which length function is required from the context in which it’s used.
Line 932: This is a
Line 933: module
Line 934: declaration.
Line 935: The export keyword means 
Line 936: that the definition of average 
Line 937: is exported from the module.
Line 938: 
Line 939: --- 페이지 71 ---
Line 940: 45
Line 941: Composite types
Line 942: cast totalLength / cast numWords
Line 943: where
Line 944: wordCount : String -> Nat
Line 945: wordCount str = length (words str)
Line 946: allLengths : List String -> List Nat
Line 947: allLengths strs = map length strs
Line 948: Listing 2.7 also introduces the module and export keywords. A module declaration can
Line 949: optionally be put at the top of a file. This declares a namespace in which every func-
Line 950: tion is defined. Conventionally, module names are the same as the filename (without
Line 951: the .idr extension). The export keyword allows the average function to be used by
Line 952: other modules that import Average.idr.
Line 953:  As usual, you can try this at the REPL by loading Average.idr into Idris, and evaluat-
Line 954: ing as follows:
Line 955: *Average> average "How long are these words?"
Line 956: 4.2 : Double
Line 957: The casts are needed to 
Line 958: convert Nat to Double.
Line 959: You only need these definitions in 
Line 960: the scope of average, so you put 
Line 961: them in a where block.
Line 962: A function to calculate the 
Line 963: number of words in a string.
Line 964: A function to get the lengths 
Line 965: of each word in a list.
Line 966: Modules and namespaces
Line 967: By adding a module declaration to the top of Average.idr, you declare a namespace
Line 968: for the definitions in the module. Here, it means that the fully qualified name of the
Line 969: average function is Average.average. A module declaration must be the first thing
Line 970: in the file. If there’s no declaration, Idris calls the module Main.
Line 971: Modules allow you to divide larger Idris programs logically into several source files,
Line 972: each with their own purpose. They can be imported with an import statement. For
Line 973: example:
Line 974: 
Line 975: import Average will import the definitions from Average.idr, provided that
Line 976: Average.idr is either in the current directory or in some other path that Idris
Line 977: can find.
Line 978: 
Line 979: import Utils.Average will import the definitions from Average.idr in a sub-
Line 980: directory called Utils, provided that the file and subdirectory exist.
Line 981: Modules themselves can be combined into packages and distributed separately.
Line 982: Technically, the Prelude is defined in a module called Prelude, which itself imports
Line 983: several other modules, and which is part of a package called prelude. You can learn
Line 984: more about packages and how to create your own from the Idris package documen-
Line 985: tation at http://idris-lang.org/documentation/packages. 
Line 986: 
Line 987: --- 페이지 72 ---
Line 988: 46
Line 989: CHAPTER 2
Line 990: Getting started with Idris
Line 991: 2.4
Line 992: A complete Idris program
Line 993: So far, you’ve seen how to write functions with built-in types and some basic opera-
Line 994: tions on those types. Functions are the basic building blocks of Idris programs, so now
Line 995: that you’ve written some simple functions, it’s time to see how to put these together to
Line 996: build a complete program.
Line 997: 2.4.1
Line 998: Whitespace significance: the layout rule
Line 999: Whitespace, specifically indentation, is significant in Idris programs. Unlike some
Line 1000: other languages, there are no braces or semicolons to indicate where expressions,
Line 1001: type declarations, and definitions begin and end. Instead, in any list of definitions and
Line 1002: declarations, all must begin in precisely the same column. Listing 2.8 illustrates where
Line 1003: definitions and declarations begin and end according to this rule in a file containing
Line 1004: the previous definition of average.
Line 1005: SPACES AND TABS
Line 1006: One complication with whitespace significance is that tab
Line 1007: sizes can be set differently in different editors, and Idris expects tabs and
Line 1008: spaces to be used consistently. To avoid any confusion with tab sizes, I
Line 1009: strongly recommend you set your editor to replace tabs with spaces!
Line 1010: average : String -> Double
Line 1011: average str = let numWords = wordCount str
Line 1012: totalLength = sum (allLengths (words str)) in
Line 1013: cast totalLength / cast numWords
Line 1014: where
Line 1015: wordCount : String -> Nat
Line 1016: wordCount str = length (words str)
Line 1017: allLengths : List String -> List Nat
Line 1018: allLengths strs = map length strs
Line 1019: If, for example, allLengths was indented one extra space, as in listing 2.9, it would be
Line 1020: considered a continuation of the previous definition of wordCount, and would there-
Line 1021: fore be invalid.
Line 1022: Listing 2.8
Line 1023: The layout rule applied to average (Average.idr)
Line 1024: Type declaration 
Line 1025: begins in column 0
Line 1026: Type declaration ends, and a new definition
Line 1027: begins in column 0. The definition of
Line 1028: numWords begins in column 18.
Line 1029: The type declaration of 
Line 1030: wordCount begins in column 4.
Line 1031: The type declaration ends, and the 
Line 1032: definition of wordCount begins in column 4.
Line 1033: The definition ends, and the 
Line 1034: type declaration of allLengths 
Line 1035: begins in column 4.
Line 1036: The definition of numWords
Line 1037: ends, and a new definition
Line 1038: of totalLength begins in
Line 1039: column 18. The definition
Line 1040: of totalLength ends at the
Line 1041: keyword “in”.
Line 1042: 
Line 1043: --- 페이지 73 ---
Line 1044: 47
Line 1045: A complete Idris program
Line 1046:  
Line 1047: wordCount : String -> Nat
Line 1048: wordCount str = length (words str)
Line 1049: allLengths : List String -> List Nat
Line 1050: allLengths strs = map length strs
Line 1051: 2.4.2
Line 1052: Documentation comments
Line 1053: As with any other language, it’s good form to comment definitions to give the reader
Line 1054: of the code an idea of the purposes of functions and document how they work. Idris
Line 1055: provides three kinds of comments: 
Line 1056: Single-line comments, introduced with -- (two minus signs). These comments
Line 1057: continue to the end of the line.
Line 1058: Multiline nested comments, introduced with {- and ending with -}.
Line 1059: Documentation comments, which are used to provide documentation for func-
Line 1060: tions and types at the REPL.
Line 1061: The first two types of comments are conventional, and merely cause the commented
Line 1062: section to be ignored (the syntax is identical to the syntax of comments in Haskell).
Line 1063:  Documentation comments, on the other hand, make documentation available at
Line 1064: the REPL, accessible with the :doc command. You can look at the documentation for
Line 1065: some of the types and functions we’ve encountered so far. For example, :doc fst pro-
Line 1066: duces the following output:
Line 1067: Idris> :doc fst
Line 1068: Prelude.Basics.fst : (a, b) -> a
Line 1069: Return the first element of a pair.
Line 1070: The function is Total
Line 1071: This output includes the fully qualified name of fst, showing that it is defined in the
Line 1072: module Prelude.Basics, and states that the function is total, meaning that it’s guar-
Line 1073: anteed to produce a result for all inputs.
Line 1074:  You can also get documentation for types. For example, :doc List gives the fol-
Line 1075: lowing output: 
Line 1076: Idris> :doc List
Line 1077: Data type Prelude.List.List : Type -> Type
Line 1078: Generic lists
Line 1079: Constructors:
Line 1080: Nil : List elem
Line 1081: The empty list
Line 1082: (::) : elem -> List elem -> List elem
Line 1083: A non-empty list, consisting of a head element and the rest of
Line 1084: the list.
Line 1085: infixr 7
Line 1086: Listing 2.9
Line 1087: The layout rule, applied incorrectly
Line 1088: allLengths is indented one space too far, 
Line 1089: so this line is considered a continuation 
Line 1090: of the definition of wordCount.
Line 1091: 
Line 1092: --- 페이지 74 ---
Line 1093: 48
Line 1094: CHAPTER 2
Line 1095: Getting started with Idris
Line 1096: Again, this gives the fully qualified name of the type Prelude.List.List. It also gives
Line 1097: the constructors, which are the primitive ways of constructing lists. Finally, for the ::
Line 1098: operator, it gives the fixity, which states the operator is right associative (infixr) and
Line 1099: has precedence level 7. I’ll describe precedence and the associativity of operators in
Line 1100: more detail in chapter 3.
Line 1101:  Documentation comments, which produce this documentation, are introduced
Line 1102: with three vertical bars, |||. For example, you could document average as follows:
Line 1103: ||| Calculate the average length of words in a string.
Line 1104: average : String -> Double
Line 1105: Then, :doc average would produce the following output:
Line 1106: *Average> :doc average
Line 1107: Average.average : (str : String) -> Double
Line 1108: Calculate the average length of words in a string.
Line 1109: The function is Total
Line 1110: You can refer to the argument of average by giving it a name, str, and referring to
Line 1111: that name in the comment with @str:
Line 1112: ||| Calculate the average length of words in a string.
Line 1113: ||| @str a string containing words separated by whitespace.
Line 1114: average : (str : String) -> Double
Line 1115: average str = let numWords = wordCount str
Line 1116: totalLength = sum (allLengths (words str)) in
Line 1117: cast totalLength / cast numWords
Line 1118: This makes :doc average produce some more informative output:
Line 1119: *Average> :doc average
Line 1120: Main.average : (str : String) -> Double
Line 1121: Calculate the average length of words in a string.
Line 1122: Arguments:
Line 1123: str : String
Line 1124: -- a string containing words separated by whitespace.
Line 1125: The function is Total
Line 1126: TOTALITY CHECKING
Line 1127: Notice that :doc average reports that average is total.
Line 1128: Idris checks every definition for totality. The result of totality checking has
Line 1129: several interesting implications in type-driven development, which we’ll dis-
Line 1130: cuss throughout the book, and particularly in chapters 10 and 11. 
Line 1131: 2.4.3
Line 1132: Interactive programs
Line 1133: The entry point to a compiled Idris program is the main function, defined in a Main
Line 1134: module. That is, it’s the function with the fully qualified name Main.main. It must have
Line 1135: the type IO (), meaning that it returns an IO action that produces an empty tuple.
Line 1136:  You’ve already seen the “Hello, Idris World!” program:
Line 1137: main : IO ()
Line 1138: main = putStrLn "Hello Idris World!"
Line 1139: 
Line 1140: --- 페이지 75 ---
Line 1141: 49
Line 1142: A complete Idris program
Line 1143: Here, putStrLn is a function of type String -> IO () that takes a string as an argu-
Line 1144: ment and returns an IO action that outputs that string. We’ll discuss IO actions in
Line 1145: some depth in chapter 5, but even before then you’ll be able to write complete inter-
Line 1146: active Idris programs using the repl function (and some variants on it, as you’ll see in
Line 1147: chapter 4) provided by the Prelude:
Line 1148: Idris> :doc repl
Line 1149: Prelude.Interactive.repl : (prompt : String) ->
Line 1150: A basic read-eval-print loop
Line 1151: Arguments:
Line 1152: prompt : String
Line 1153: -- the prompt to show
Line 1154: onInput : String -> String
Line 1155: -- the function to run on reading
Line 1156: input, returning a String to output
Line 1157: This allows you to write programs that repeatedly display a prompt, read some input,
Line 1158: and produce some output by running a function of type String -> String on it. For
Line 1159: example, the next listing is a program that repeatedly reads a string and then prints
Line 1160: the string in reverse.
Line 1161: module Main
Line 1162: main : IO ()
Line 1163: main = repl "> " reverse
Line 1164: You can compile and run this program at the REPL with the :exec command. Note
Line 1165: that the program will loop indefinitely, but you can quit by interrupting the program
Line 1166: with Ctrl-C: 
Line 1167: *reverse> :exec
Line 1168: > hello!
Line 1169: !olleh> goodbye
Line 1170: eybdoog>
Line 1171: To conclude this chapter, you’ll write a program that imports the Average module,
Line 1172: reads a string from the console, and displays the average number of letters in each
Line 1173: word in the string. One difficulty is that the average function returns a Double, but
Line 1174: repl requires a function of type String -> String, so you can’t use average directly.
Line 1175: In general, though, values can be converted to String using the show function. Let’s
Line 1176: take a look at it using :doc:
Line 1177: Idris> :doc show
Line 1178: Prelude.Show.show : Show ty => (x : ty) -> String
Line 1179: Convert a value to its String representation.
Line 1180: Note that this is a constrained generic type, meaning that the type ty must support the
Line 1181: Show interface, which is true of all the types in the Prelude.
Line 1182: Listing 2.10
Line 1183: Reversing strings interactively (Reverse.idr)
Line 1184: 
Line 1185: --- 페이지 76 ---
Line 1186: 50
Line 1187: CHAPTER 2
Line 1188: Getting started with Idris
Line 1189:  Using this, you can write a showAverage function that uses average to get the aver-
Line 1190: age word length and displays it in a nicely formatted string. The complete program is
Line 1191: given in the following listing.
Line 1192: module Main
Line 1193: import Average
Line 1194: showAverage : String -> String
Line 1195: showAverage str = "The average word length is: " ++
Line 1196: show (average str) ++ "\n"
Line 1197: main : IO ()
Line 1198: main = repl "Enter a string: "
Line 1199: showAverage
Line 1200: Again, you can use :exec to compile and run this at the REPL, and then try some
Line 1201: inputs:
Line 1202: *AveMain> :exec
Line 1203: Enter a string: The quick brown fox jumped over the lazy dog
Line 1204: The average word length is: 4
Line 1205: Enter a string: The quick brown fox jumped over the lazy frog
Line 1206: The average word length is: 4.11111
Line 1207: Enter a string:
Line 1208: Exercises
Line 1209:  1
Line 1210: What are the types of the following values? 
Line 1211: ("A", "B", "C")
Line 1212: ["A", "B", "C"]
Line 1213: (('A', "B"), 'C')
Line 1214: You can check your answers with :t at the REPL, but try to work them out yourself
Line 1215: first.
Line 1216:  2
Line 1217: Write a palindrome function, of type String -> Bool, that returns whether the
Line 1218: input reads the same backwards as forwards. 
Line 1219: Hint: You may find the function reverse : String -> String useful.
Line 1220: You can test your answer at the REPL as follows: 
Line 1221: *ex_2> palindrome "racecar"
Line 1222: True : Bool
Line 1223: *ex_2> palindrome "race car"
Line 1224: False : Bool
Line 1225: Listing 2.11
Line 1226: Displaying average word lengths interactively (AveMain.idr)
Line 1227: Imports the definitions 
Line 1228: from Average.idr
Line 1229: The function that calculates 
Line 1230: the string to output from 
Line 1231: some input. It uses show 
Line 1232: to convert the result of 
Line 1233: average to a String.
Line 1234: The prompt
Line 1235: to display
Line 1236: The function to call to calculate the output
Line 1237: 
Line 1238: --- 페이지 77 ---
Line 1239: 51
Line 1240: A complete Idris program
Line 1241:  3
Line 1242: Modify the palindrome function so that it’s not case sensitive. 
Line 1243: Hint: You may find toLower : String -> String useful. 
Line 1244: You can test your answer at the REPL as follows: 
Line 1245: *ex_2> palindrome "Racecar"
Line 1246: True : Bool
Line 1247:  4
Line 1248: Modify the palindrome function so that it only returns True for strings longer than
Line 1249: 10 characters.
Line 1250: You can test your answer at the REPL as follows: 
Line 1251: *ex_2> palindrome "racecar"
Line 1252: False : Bool
Line 1253: *ex_2> palindrome "able was i ere i saw elba"
Line 1254: True : Bool
Line 1255:  5
Line 1256: Modify the palindrome function so that it only returns True for strings longer than
Line 1257: some length given as an argument. 
Line 1258: Hint: Your new function should have type Nat -> String -> Bool.
Line 1259: You can test your answer at the REPL as follows: 
Line 1260: *ex_2> palindrome 10 "racecar"
Line 1261: False : Bool
Line 1262: *ex_2> palindrome 5 "racecar"
Line 1263: True : Bool
Line 1264:  6
Line 1265: Write a counts function of type String -> (Nat, Nat) that returns a pair of the
Line 1266: number of words in the input and the number of characters in the input.
Line 1267: You can test your answer at the REPL as follows: 
Line 1268: *ex_2> counts "Hello, Idris world!"
Line 1269: (3, 19) : (Nat, Nat)
Line 1270:  7
Line 1271: Write a top_ten function of type Ord a => List a -> List a that returns the ten larg-
Line 1272: est values in a list. You may find the following Prelude functions useful: 
Line 1273: 
Line 1274: take : Nat -> List a -> List a
Line 1275: 
Line 1276: sort : Ord a => List a -> List a
Line 1277: Use :doc for further information about these functions if you need it.
Line 1278: You can test your answer at the REPL as follows: 
Line 1279: *ex_2> top_ten [1..100]
Line 1280: [100, 99, 98, 97, 96, 95, 94, 93, 92, 91] : List Integer
Line 1281:  8
Line 1282: Write an over_length function of type Nat -> List String -> Nat that returns the
Line 1283: number of strings in the list longer than the given number of characters.
Line 1284: You can test your answer at the REPL as follows: 
Line 1285: *ex_2> over_length 3 ["One", "Two", "Three", "Four"]
Line 1286: 2 : Nat
Line 1287: 
Line 1288: --- 페이지 78 ---
Line 1289: 52
Line 1290: CHAPTER 2
Line 1291: Getting started with Idris
Line 1292:  9
Line 1293: For each of palindrome and counts, write a complete program that prompts for an
Line 1294: input, calls the function, and prints its output.
Line 1295: You can test your answer using :exec at the REPL: 
Line 1296: *ex_2_palindrome> :exec
Line 1297: Enter a string: Able was I ere I saw Elba
Line 1298: True
Line 1299: Enter a string: Madam, I'm Adam
Line 1300: False
Line 1301: Enter a string:
Line 1302: 2.5
Line 1303: Summary
Line 1304: The Prelude defines a number of basic types and functions and is imported
Line 1305: automatically by all Idris programs.
Line 1306: Idris provides basic numeric types, Int, Integer, Nat, and Double, as well as a
Line 1307: Boolean type, Bool, a character type, Char, and a string type, String.
Line 1308: Values can be converted between compatible types using the cast function, and
Line 1309: can be given explicit types with the the function.
Line 1310: Tuples are fixed-size collections where each element can be a different type.
Line 1311: Lists are variable size collections where each element has the same type.
Line 1312: Function types have one or more input types and one output type.
Line 1313: Function types can be generic, meaning that they can contain variables. These
Line 1314: variables can be constrained to allow a smaller set of types.
Line 1315: Higher-order functions are functions in which one of the arguments is itself a
Line 1316: function.
Line 1317: Functions consist of a required type declaration and a definition. Function defi-
Line 1318: nitions are equations defining rewrite rules to be used during evaluation.
Line 1319: Whitespace is significant in Idris programs. Each definition in a block must
Line 1320: begin in exactly the same column.
Line 1321: Function documentation can be accessed at the REPL with the :doc command.
Line 1322: Idris programs can be divided into separate source files called modules.
Line 1323: The entry point to an Idris program is the main function, which must have type
Line 1324: IO (), and be defined in the module Main. Simple interactive programs can be
Line 1325: written by applying the repl function from main.