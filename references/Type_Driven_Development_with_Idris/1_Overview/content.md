Line 1: 
Line 2: --- 페이지 29 ---
Line 3: 3
Line 4: Overview
Line 5: This book teaches a new approach to building robust software, type-driven develop-
Line 6: ment, using the Idris programming language. Traditionally, types are seen as a tool
Line 7: for checking for errors, with the programmer writing a complete program first and
Line 8: using either the compiler or the runtime system to detect type errors. In type-
Line 9: driven development, we use types as a tool for constructing programs. We put the
Line 10: type first, treating it as a plan for a program, and use the compiler and type checker
Line 11: as our assistant, guiding us to a complete and working program that satisfies the
Line 12: type. The more expressive the type is that we give up front, the more confidence we
Line 13: can have that the resulting program will be correct.
Line 14: TYPES AND TESTS
Line 15: The name “type-driven development” suggests an anal-
Line 16: ogy to test-driven development. There’s a similarity, in that writing tests
Line 17: first helps establish a program’s purpose and whether it satisfies some basic
Line 18: requirements. The difference is that, unlike tests, which can usually only
Line 19: be used to show the presence of errors, types (used appropriately) can show
Line 20: the absence of errors. But although types reduce the need for tests, they
Line 21: rarely eliminate it entirely.
Line 22: This chapter covers
Line 23: Introducing type-driven development
Line 24: The essence of pure functional programming
Line 25: First steps with Idris
Line 26: 
Line 27: --- 페이지 30 ---
Line 28: 4
Line 29: CHAPTER 1
Line 30: Overview
Line 31: Idris is a relatively young programming language, designed from the beginning to
Line 32: support type-driven development. A prototype implementation first appeared in 2008,
Line 33: with development of the current implementation beginning in 2011. It builds on
Line 34: decades of research into the theoretical and practical foundations of programming
Line 35: languages and type systems.
Line 36:  In Idris, types are a first-class language construct. Types can be manipulated, used,
Line 37: passed as arguments to functions, and returned from functions just like any other
Line 38: value, such as numbers, strings, or lists. This is a simple but powerful idea: 
Line 39: It allows relationships to be expressed between values; for example, that two
Line 40: lists have the same length.
Line 41: It allows assumptions to be made explicit and checkable by the compiler. For
Line 42: example, if you assume that a list is non-empty, Idris can ensure this assumption
Line 43: always holds before the program is run.
Line 44: If desired, it allows program behavior to be formally stated and proven correct.
Line 45: In this chapter, I’ll introduce the Idris programming language and give a brief tour of
Line 46: its features and environment. I’ll also provide an overview of type-driven develop-
Line 47: ment, discussing why types matter in programming languages and how they can be
Line 48: used to guide software development. But first, it’s important to understand exactly
Line 49: what we mean when we talk about “types.”
Line 50: 1.1
Line 51: What is a type?
Line 52: We’re taught from an early age to recognize and distinguish types of objects. As a
Line 53: young child, you may have had a shape-sorter toy. This consists of a box with variously
Line 54: shaped holes in the top (see figure 1.1) and some shapes that fit through the holes.
Line 55: Sometimes they’re equipped with a small plastic hammer. The idea is to fit each shape
Line 56: (think of this as a “value”) into the appropriate hole (think of this as a “type”), possi-
Line 57: bly with coercion from the hammer.
Line 58:  In programming, types are a means of classifying values. For example, the values
Line 59: 94, "thing", and [1,2,3,4,5] could respec-
Line 60: tively be classified as an integer, a string, and a
Line 61: list of integers. Just as you can’t put a square
Line 62: shape in a round hole in the shape sorter, you
Line 63: can’t use a string like "thing" in a part of a pro-
Line 64: gram where you need an integer.
Line 65:  All modern programming languages classify
Line 66: values by type, although they differ enormously
Line 67: in when and how they do so (for example,
Line 68: whether they’re checked statically at compile
Line 69: time or dynamically at runtime, whether con-
Line 70: versions between types are automatic or not,
Line 71: and so on).
Line 72: Figure 1.1
Line 73: The top of a shape-sorter toy. 
Line 74: The shapes correspond to the types of 
Line 75: objects that will fit through the holes.
Line 76: 
Line 77: --- 페이지 31 ---
Line 78: 5
Line 79: Introducing type-driven development
Line 80:  Types serve several important roles:
Line 81: For a machine, types describe how bit patterns in memory are to be interpreted.
Line 82: For a compiler or interpreter, types help ensure that bit patterns are interpreted
Line 83: consistently when a program runs.
Line 84: For a programmer, types help name and organize concepts, aiding documenta-
Line 85: tion and supporting interactive editing environments.
Line 86: From our point of view in this book, the most important purpose of types is the third.
Line 87: Types help programmers in several ways:
Line 88: By allowing for the naming and organization of concepts (such as Square,
Line 89: Circle, Triangle, and Hexagon)
Line 90: By providing explicit documentation of the purposes of variables, functions,
Line 91: and programs
Line 92: By driving code completion in an interactive editing environment
Line 93: As you’ll see, type-driven development makes extensive use of code completion in par-
Line 94: ticular. Although all modern, statically typed languages support code completion to
Line 95: some extent, the expressivity of the Idris type system leads to powerful automatic code
Line 96: generation. 
Line 97: 1.2
Line 98: Introducing type-driven development
Line 99: Type-driven development is a style of pro-
Line 100: gramming in which we write types first and
Line 101: use those types to guide the definition of
Line 102: functions. The overall process is to write the
Line 103: necessary data types, and then, for each func-
Line 104: tion, do the following:
Line 105: 1
Line 106: Write the input and output types.
Line 107: 2
Line 108: Define the function, using the struc-
Line 109: ture of the input types to guide the
Line 110: implementation.
Line 111: 3
Line 112: Refine and edit the type and function
Line 113: definition as necessary.
Line 114: In type-driven development, instead of think-
Line 115: ing of types in terms of checking, with the type
Line 116: checker criticizing you when you make a mis-
Line 117: take, you can think of types as being a plan,
Line 118: with the type checker acting as your guide,
Line 119: leading you to a working, robust program.
Line 120: Starting with a type and an empty function
Line 121: body, you gradually add details to the defini-
Line 122: tion until it’s complete, regularly using the
Line 123: Types as models
Line 124: When you write a program, you’ll
Line 125: often have a conceptual model in
Line 126: your head (or, if you’re disci-
Line 127: plined, even on paper) of how it’s
Line 128: supposed to work, how the com-
Line 129: ponents interact, and how the
Line 130: data is organized. This model is
Line 131: likely to be quite vague at first
Line 132: and will become more precise as
Line 133: the program evolves and your
Line 134: understanding of the concept
Line 135: develops.
Line 136: Types allow you to make these
Line 137: models explicit in code and
Line 138: ensure that your implementation
Line 139: of a program matches the model
Line 140: in your head. Idris has an expres-
Line 141: sive type system that allows you
Line 142: to describe a model as precisely
Line 143: as you need, and to refine the
Line 144: model at the same time as devel-
Line 145: oping the implementation.
Line 146: 
Line 147: --- 페이지 32 ---
Line 148: 6
Line 149: CHAPTER 1
Line 150: Overview
Line 151: compiler to check that the program so far satisfies the type. Idris, as you’ll soon see,
Line 152: strongly encourages this style of programming by allowing incomplete function defini-
Line 153: tions to be checked, and by providing an expressive language for describing types.
Line 154:  To illustrate further, in this section I’ll show some examples of how you can use
Line 155: types to describe in detail what a program is intended to do: matrix arithmetic, model-
Line 156: ing an automated teller machine (ATM), and writing concurrent programs. Then, I’ll
Line 157: summarize the process of type-driven development and introduce the concept of
Line 158: dependent types, which will allow you to express detailed properties of your programs.
Line 159: 1.2.1
Line 160: Matrix arithmetic
Line 161: A matrix is a rectangular grid of numbers, arranged in rows and columns. They have
Line 162: several scientific applications, and in programming they have applications in cryptog-
Line 163: raphy, 3D graphics, machine learning, and data analytics. The following, for example,
Line 164: is a 3 × 4 matrix:
Line 165: You can implement various arithmetic operations on matrices, such as addition and
Line 166: multiplication. To add two matrices, you add the corresponding elements, as you see
Line 167: here:
Line 168: When programming with matrices, if you begin by defining a Matrix data type, then
Line 169: addition requires two inputs of type Matrix and gives an output of type Matrix. But
Line 170: because adding matrices involves adding corresponding elements of the inputs, what
Line 171: happens if the two inputs have different dimensions, as here?
Line 172: It’s likely that if you’re trying to add matrices of different dimensions, then you’ve
Line 173: made a mistake somewhere. So, instead of using a Matrix type, you could refine the
Line 174: 1
Line 175: 5
Line 176: 9
Line 177: 2
Line 178: 6
Line 179: 10
Line 180: 3
Line 181: 7
Line 182: 11
Line 183: 4
Line 184: 8
Line 185: 12
Line 186: 
Line 187: 
Line 188: 
Line 189: 
Line 190: 
Line 191: 
Line 192: 
Line 193: 
Line 194: 
Line 195: 
Line 196: 
Line 197: 
Line 198: 
Line 199: 
Line 200: 1 2
Line 201: 3 4
Line 202: 5 6
Line 203: 
Line 204: 
Line 205: 
Line 206: 
Line 207: 
Line 208: 
Line 209: 
Line 210: 
Line 211: 
Line 212: 
Line 213: 7
Line 214: 8
Line 215: 9 10
Line 216: 11 12
Line 217: 
Line 218: 
Line 219: 
Line 220: 
Line 221: 
Line 222: 
Line 223: 
Line 224: 
Line 225: 
Line 226: 
Line 227: +
Line 228: 8 10
Line 229: 12 14
Line 230: 16 18
Line 231: 
Line 232: 
Line 233: 
Line 234: 
Line 235: 
Line 236: 
Line 237: 
Line 238: 
Line 239: 
Line 240: 
Line 241: =
Line 242: 1 2
Line 243: 3 4
Line 244: 5 6
Line 245: 
Line 246: 
Line 247: 
Line 248: 
Line 249: 
Line 250: 
Line 251: 
Line 252: 
Line 253: 
Line 254: 
Line 255: 7 8
Line 256: 9 10
Line 257: 
Line 258: 
Line 259: 
Line 260: 
Line 261: 
Line 262: 
Line 263: +
Line 264: ???
Line 265: =
Line 266: 
Line 267: --- 페이지 33 ---
Line 268: 7
Line 269: Introducing type-driven development
Line 270: type so that it includes the dimensions of the matrix, and require that the two input
Line 271: matrices have the same dimensions:
Line 272: The first example of a 3 × 4 matrix now has type Matrix 3 4 .
Line 273: The first (correct) example of addition takes two inputs of type Matrix 3 2 and
Line 274: gives an output of type Matrix 3 2.
Line 275: By including the dimensions in the type of a matrix, you can describe the input and
Line 276: output types of addition in such a way that it’s a type error to try to add matrices of dif-
Line 277: ferent sizes. If you try to add a Matrix 3 2 and a Matrix 2 2, your program won’t
Line 278: compile, let alone run.
Line 279:  If you include the dimensions of a matrix in its type, then you need to think about
Line 280: the relationship between the dimensions of the input and output for every matrix
Line 281: operation. For example, transposing a matrix involves switching the rows to columns
Line 282: and vice versa, so if you transpose a 3 × 2 matrix, you’ll end up with a 2 × 3 matrix:
Line 283: The input type of this transposition is Matrix 3 2, and the output type is Matrix 2 3.
Line 284:  In general, rather than giving exact dimensions in the type, we’ll use variables to
Line 285: describe the relationship between the dimensions of the inputs and the dimensions of
Line 286: the outputs. Table 1.1 shows the relationships between the dimensions of inputs and
Line 287: outputs for three matrix operations: addition, multiplication, and transposition.
Line 288: We’ll look at matrices in depth in chapter 3, where we’ll work through an implemen-
Line 289: tation of matrix transposition in detail. 
Line 290: 1.2.2
Line 291: An automated teller machine
Line 292: As well as using types to describe the relationships between the inputs and outputs of
Line 293: functions, as with matrix operations, you can describe precisely when operations are
Line 294: valid. For example, if you’re implementing software to drive an ATM, you’ll want to
Line 295: guarantee that the machine will dispense cash only after a user has entered a card and
Line 296: validated their personal identification number (PIN).
Line 297: Table 1.1
Line 298: Input and output types for matrix operations. The names x, y, and z
Line 299: describe, in general, how the dimensions of the inputs and outputs are related.
Line 300: Operation
Line 301: Input types
Line 302: Output type
Line 303: Add
Line 304: Matrix x y, Matrix x y
Line 305: Matrix x y
Line 306: Multiply
Line 307: Matrix x y, Matrix y z
Line 308: Matrix x z
Line 309: Transpose
Line 310: Matrix x y
Line 311: Matrix y x
Line 312: 1 2
Line 313: 3 4
Line 314: 5 6
Line 315: 
Line 316: 
Line 317: 
Line 318: 
Line 319: 
Line 320: 
Line 321: 
Line 322: 
Line 323: 
Line 324: 
Line 325:  ... transposed to ... 1 3 5
Line 326: 2 4 6
Line 327: 
Line 328: 
Line 329: 
Line 330: 
Line 331: 
Line 332: 
Line 333: 
Line 334: 
Line 335: 
Line 336: --- 페이지 34 ---
Line 337: 8
Line 338: CHAPTER 1
Line 339: Overview
Line 340:  To see how this works, we’ll need to consider the possible states that an ATM can be in:
Line 341: 
Line 342: Ready—The ATM is ready and waiting for a user to insert a card.
Line 343: 
Line 344: CardInserted—The ATM is waiting for a user, having inserted a card, to enter
Line 345: their PIN.
Line 346: 
Line 347: Session—A validated session is in progress, with the ATM, having validated the
Line 348: user’s PIN, ready to dispense cash.
Line 349: An ATM supports several basic operations, each of which is valid only when the
Line 350: machine is in a specific state, and each of which might change the state of the
Line 351: machine, as illustrated in figure 1.2. These are the basic operations:
Line 352: 
Line 353: InsertCard—Waits for the user to insert a card
Line 354: 
Line 355: EjectCard—Ejects a card from the machine
Line 356: 
Line 357: GetPIN—Prompts the user to enter a PIN
Line 358: 
Line 359: CheckPIN—Checks whether an entered PIN is correct
Line 360: 
Line 361: Dispense—Dispenses cash
Line 362: Whether an operation is valid or not depends on the state of the machine. For exam-
Line 363: ple, InsertCard is valid only in the Ready state, because that’s the only state where
Line 364: there’s no card already in the machine. Also, Dispense is valid only in the Session
Line 365: state, because that’s the only state where there’s a validated card in the machine.
Line 366:  Furthermore, executing one of these operations can change the state of the
Line 367: machine. For example, InsertCard changes the state from Ready to CardInserted,
Line 368: and CheckPIN changes the state from CardInserted to Session, provided that the
Line 369: entered PIN is correct.
Line 370: STATE MACHINES AND TYPES
Line 371: Figure 1.2 illustrates a state machine, describing
Line 372: how operations affect the overall state of a system. State machines are often
Line 373: present, implicitly, in real-world systems. For example, when you open, read,
Line 374: CardInserted
Line 375: Session
Line 376: Ready
Line 377: EjectCard
Line 378: Dispense
Line 379: GetPIN,
Line 380: CheckPIN (Incorrect)
Line 381: InsertCard
Line 382: EjectCard
Line 383: CheckPIN (Correct)
Line 384: Figure 1.2
Line 385: The states and valid operations on an ATM. Each operation is valid only in specific 
Line 386: states and can change the state of the machine. CheckPIN changes the state only if the 
Line 387: entered PIN is correct.
Line 388: 
Line 389: --- 페이지 35 ---
Line 390: 9
Line 391: Introducing type-driven development
Line 392: and then close a file, you change the state of the file with the open and close
Line 393: operations. As you’ll see in chapter 13, types allow you to make these state
Line 394: changes explicit, guarantee that you’ll execute operations only when they’re
Line 395: valid, and help you use resources correctly.
Line 396: By defining precise types for each of the operations on the ATM, you can guarantee,
Line 397: by type checking, that the ATM will execute only valid operations. If, for example, you
Line 398: try to implement a program that dispenses cash without validating a PIN, the pro-
Line 399: gram won’t compile. By defining valid state transitions explicitly in types, you get
Line 400: strong and machine-checkable guarantees about the correctness of their implementa-
Line 401: tion. We’ll look at state machines in chapter 13, and then implement the ATM exam-
Line 402: ple in chapter 14. 
Line 403: 1.2.3
Line 404: Concurrent programming
Line 405: A concurrent program consists of multiple processes running at the same time and
Line 406: coordinating with each other. Concurrent programs can be responsive and continue
Line 407: to interact with a user while a large computation is running. For example, a user can
Line 408: continue browsing a web page while a large file is downloading. Moreover, by writing
Line 409: concurrent programs we can take full advantage of the processor power of modern
Line 410: CPUs, dividing work among multiple processes on separate CPU cores.
Line 411:  In Idris, processes coordinate with each other by sending and receiving messages.
Line 412: Figure 1.3 shows one way this can work, with two processes, main and adder. The adder
Line 413: process waits for a request to add numbers from other processes. After it receives a mes-
Line 414: sage from main asking it to add two numbers, it sends a response back with the result.
Line 415:  Despite its advantages, however, concurrent programming is notoriously error
Line 416: prone. The need for processes to interact with each other can greatly increase a sys-
Line 417: tem’s complexity. For each process, you need to ensure that the messages it sends and
Line 418: Concurrent processes
Line 419: in Idris coordinate
Line 420: through messages.
Line 421: main
Line 422: adder
Line 423: Add 2 3
Line 424: 5
Line 425: Time
Line 426: Figure 1.3
Line 427: Two interacting 
Line 428: concurrent processes, main and 
Line 429: adder. The main process sends a 
Line 430: request to adder, which then sends a 
Line 431: response back to main.
Line 432: 
Line 433: --- 페이지 36 ---
Line 434: 10
Line 435: CHAPTER 1
Line 436: Overview
Line 437: receives are properly coordinated with other processes. If, for example, main and
Line 438: adder aren’t properly coordinated and each is expecting to receive a message from
Line 439: the other at the same time, they’ll deadlock.
Line 440: TYPES VERSUS TESTING FOR CONCURRENT PROGRAMS
Line 441: Testing a concurrent
Line 442: program is difficult because, unlike a purely sequential program, there’s no
Line 443: guarantee about the order in which operations from different processes will
Line 444: execute. Even if two processes are correctly coordinated when you run a test
Line 445: once, there’s no guarantee they’ll be correctly coordinated when you next
Line 446: run the test. On the other hand, if you can express the coordination between
Line 447: processes in types, you can be sure that a concurrent program that type-checks
Line 448: has properly coordinated processes.
Line 449: When you write concurrent programs, you’ll ideally have a model of how processes
Line 450: should interact. Using types, you can make this model explicit in code. Then, if a con-
Line 451: current program type-checks, you’ll know that it correctly follows the model. In partic-
Line 452: ular, you can do two things:
Line 453: Define an interface for adder that describes the form of messages it will handle.
Line 454: Define a protocol that defines the order of message passing, ensuring that main
Line 455: will always send a message to adder and then receive a reply, and adder will
Line 456: always do the opposite.
Line 457: Concurrent programming is an extensive topic, and there are several ways you can use
Line 458: types to model coordination between processes. We’ll look at one example of how to
Line 459: do this in chapter 15. 
Line 460: 1.2.4
Line 461: Type, define, refine: the process of type-driven development
Line 462: In each of these introductory examples, we’ve discussed in general terms how we
Line 463: might model a system: by describing the valid forms of inputs and outputs for matrix
Line 464: operations, the valid states of an interactive system, or the order of transmission of
Line 465: messages between concurrent processes. In each case, to implement the system, you
Line 466: start by trying to find a type that captures the important details of the model, and then
Line 467: define functions to work with that type, refining the type as necessary.
Line 468:  To put it succinctly, you can characterize type-driven development as an iterative
Line 469: process of type, define, refine: writing a type, implementing a function to satisfy that
Line 470: type, and refining the type or definition as you learn more about the problem.
Line 471:  With matrix addition, for example, you do the following:
Line 472: Type—Write a Matrix data type, and use it as the input and output types for an
Line 473: addition function. 
Line 474: Define—Write an addition function that satisfies its input and output types.
Line 475: Refine—Notice that the input and output types for your addition function allow
Line 476: you to give invalid inputs with different dimensions, and then make the type
Line 477: more precise by including the dimensions of the matrices.
Line 478: 
Line 479: --- 페이지 37 ---
Line 480: 11
Line 481: Introducing type-driven development
Line 482: In general, you’ll write a type to represent the system you’re modeling, define func-
Line 483: tions using that type, and then refine the type and definition as necessary to capture
Line 484: any missing properties. You’ll see a lot more of this type-define-refine process
Line 485: throughout this book, both on a small scale when implementing individual functions,
Line 486: and on a larger scale when deciding how to write function and data types. 
Line 487: 1.2.5
Line 488: Dependent types
Line 489: In the matrix arithmetic example, we began with a Matrix type and then refined it to
Line 490: include the number of rows and columns. This means, for example, that Matrix 3 4
Line 491: is the type of 3 × 4 matrices. In this type, 3 and 4 are ordinary values. A dependent type,
Line 492: such as Matrix, is a type that’s calculated from some other values. In other words, it
Line 493: depends on other values.
Line 494:  By including values in a type like this, you can make types as precise as required. For
Line 495: example, some languages have a simple list type, describing lists of objects. You can
Line 496: make this more precise by parameterizing over the element type: a generic list of
Line 497: strings is more precise than a simple list and differs from a list of integers. You can be
Line 498: more precise still with a dependent type: a list of 4 strings differs from a list of 3 strings.
Line 499:  Table 1.2 illustrates how types in Idris can have differing levels of precision even
Line 500: for fundamental operations such as appending lists. Suppose you have two specific
Line 501: input lists of strings:
Line 502: ["a", "b", "c", "d"]
Line 503: ["e", "f", "g"]
Line 504: When you append them, you’ll expect the following output list:
Line 505: ["a", "b", "c", "d", "e", "f", "g"]
Line 506: Using a simple type, both input lists have type AnyList, as does the output list. Using a
Line 507: generic type, you can specify that the input lists are both lists of strings, as is the output
Line 508: list. The more-precise types mean that, for example, the output is clearly related to the
Line 509: input in that the element type is unchanged. Finally, using a dependent type, you can
Line 510: specify the sizes of the input and output lists. It’s clear from the type that the length of
Line 511: the output list is the sum of the lengths of the input lists. That is, a list of 3 strings
Line 512: appended to a list of 4 strings results in a list of 7 strings.
Line 513: Table 1.2
Line 514: Appending specific typed lists. Unlike simple types, where there’s no difference between the
Line 515: input and output list types, dependent types allow the length to be encoded in the type.
Line 516: Input 
Line 517: ["a", "b", "c", "d"]
Line 518: Input 
Line 519: ["e", "f", "g"]
Line 520: Output type
Line 521: Simple
Line 522: AnyList
Line 523: AnyList
Line 524: AnyList
Line 525: Generic
Line 526: List String
Line 527: List String
Line 528: List String
Line 529: Dependent
Line 530: Vect 4 String
Line 531: Vect 3 String
Line 532: Vect 7 String
Line 533: 
Line 534: --- 페이지 38 ---
Line 535: 12
Line 536: CHAPTER 1
Line 537: Overview
Line 538: LISTS AND VECTORS
Line 539: The syntax for the types in table 1.2 is valid Idris syntax.
Line 540: Idris provides several ways of building list types, with varying levels of preci-
Line 541: sion. In the table, you can see two of these, List and Vect. AnyList is
Line 542: included in the table purely for illustrative purposes and is not defined in
Line 543: Idris. List encodes generic lists with no explicit length, and Vect (short for
Line 544: “vector”) encodes lists with the length explicitly in the type. You’ll see much
Line 545: more of both these types throughout this book.
Line 546: Table 1.3 illustrates how the input and output types of an append function can be writ-
Line 547: ten with increasing levels of precision in Idris. Using simple types, you can write the
Line 548: input and output types as AnyList, suggesting that you have no interest in the types of
Line 549: the elements of the list. Using generic types, you can write the input and output types as
Line 550: List elem. Here, elem is a type variable standing for the element types. Because the
Line 551: type variable is the same for both inputs and the output, the types specify that both
Line 552: the input lists and the output list have a consistent element type. If you append two
Line 553: lists of integers, the types guarantee that the output will also be a list of integers.
Line 554: Finally, using dependent types, you can write the inputs as Vect n elem and Vect m
Line 555: elem, where n and m are variables representing the length of each list. The output type
Line 556: specifies that the resulting length will be the sum of the lengths of the inputs.
Line 557: TYPE VARIABLES
Line 558: Types often contain type variables, like n, m, and elem in
Line 559: table 1.3. These are very much like parameters to generic types in Java or C#,
Line 560: but they’re so common in Idris that they have a very lightweight syntax. In
Line 561: general, concrete type names begin with an uppercase letter, and type vari-
Line 562: able names begin with a lowercase letter.
Line 563: In the dependent type for the append function in table 1.3, the parameters n and m are
Line 564: ordinary numeric values, and the + operator is the normal addition operator. All of
Line 565: these could appear in programs just as they’ve appeared here in the types. 
Line 566: Introductory exercises
Line 567: Throughout this book, exercises will help reinforce the concepts you’ve learned. As a
Line 568: warm-up, take a look at the following selection of function specifications, given purely
Line 569: in the form of input and output types. For each of them, suggest possible operations
Line 570: Table 1.3
Line 571: Appending typed lists, in general. Type variables describe the relationships between
Line 572: the inputs and outputs, even though the exact inputs and outputs are unknown.
Line 573: Input 1 type
Line 574: Input 2 type
Line 575: Output type
Line 576: Simple
Line 577: AnyList
Line 578: AnyList
Line 579: AnyList
Line 580: Generic
Line 581: List elem
Line 582: List elem
Line 583: List elem
Line 584: Dependent
Line 585: Vect n elem
Line 586: Vect m elem
Line 587: Vect (n + m) elem
Line 588: 
Line 589: --- 페이지 39 ---
Line 590: 13
Line 591: Pure functional programming
Line 592: that would satisfy the given input and output types. Note that there could be more
Line 593: than one answer in each case.
Line 594: 1
Line 595: Input type:
Line 596: Vect n elem
Line 597: Output type: Vect n elem
Line 598: 2
Line 599: Input type:
Line 600: Vect n elem
Line 601: Output type: Vect (n * 2) elem
Line 602: 3
Line 603: Input type:
Line 604: Vect (1 + n) elem
Line 605: Output type: Vect n elem
Line 606: 4
Line 607: Assume that Bounded n represents a number between zero and n - 1.
Line 608: Input types:
Line 609: Bounded n, Vect n elem
Line 610: Output type: elem
Line 611: 1.3
Line 612: Pure functional programming
Line 613: Idris is a pure functional programming language, so before we begin exploring Idris in
Line 614: depth, we should look at what it means for a language to be functional, and what we
Line 615: mean by the concept of purity. Unfortunately, there’s no universally agreed-on defini-
Line 616: tion of exactly what it means for a programming language to be functional, but for our
Line 617: purposes we’ll take it to mean the following: 
Line 618: Programs are composed of functions.
Line 619: Program execution consists of the evaluation of functions.
Line 620: Functions are a first-class language construct.
Line 621: This differs from an imperative programming language primarily in that functional
Line 622: programming is concerned with the evaluation of functions, rather than the execu-
Line 623: tion of statements. 
Line 624:  In a pure functional language, the following are also true: 
Line 625: Functions don’t have side effects such as modifying global variables, throwing
Line 626: exceptions, or performing console input or output.
Line 627: As a result, for any specific inputs, a function will always give the same result.
Line 628: You may wonder, very reasonably, how it’s possible to write any useful software under
Line 629: these constraints. In fact, far from making it more difficult to write realistic programs,
Line 630: pure functional programming allows you to treat tricky concepts such as state and
Line 631: exceptions with the respect they deserve. Let’s explore further.
Line 632: 1.3.1
Line 633: Purity and referential transparency
Line 634: The key property of a pure function is that the same inputs always produce the same
Line 635: result. This property is known as referential transparency. An expression (such as a func-
Line 636: tion call) in a function is referentially transparent if it can be replaced with its result
Line 637: without changing the behavior of the function. If functions produce only results, with
Line 638: no side effects, this property is clearly true. Referential transparency is a very useful
Line 639: concept in type-driven development, because if a function has no side effects and is
Line 640: 
Line 641: --- 페이지 40 ---
Line 642: 14
Line 643: CHAPTER 1
Line 644: Overview
Line 645: defined entirely by its inputs and outputs, then you can look at its input and output
Line 646: types and have a clear idea of the limits of what the function can do.
Line 647:  Figure 1.4 shows example inputs and outputs for the append function. It takes two
Line 648: inputs and produces a result, but there’s no interaction with a user, such as reading
Line 649: from the keyboard, and no informative output, such as logging or progress bars.
Line 650:  Figure 1.5 shows pure functions in general. There can be no observable side
Line 651: effects when running these programs, other than perhaps making the computer
Line 652: slightly warmer or taking a different amount of time to run.
Line 653: Pure functions are very common in practice, particularly for constructing and manip-
Line 654: ulating data structures. It’s possible to reason about their behavior because the func-
Line 655: tion always gives the same result for the same inputs; these functions are important
Line 656: components of larger programs. The preceding append function is pure, and it’s a
Line 657: valuable component for any program that works with lists. It produces a list as a result,
Line 658: and because it’s pure, you know that it won’t require any input, output any logging, or
Line 659: do anything destructive like delete files. 
Line 660: 1.3.2
Line 661: Side-effecting programs
Line 662: Realistically, programs must have side effects in order to be useful, and you’re always
Line 663: going to have to deal with unexpected or erroneous inputs in practical software. At
Line 664: first, this would seem to be impossible in a pure language. There is a way, however:
Line 665: pure functions may not be able to perform side effects, but they can describe them.
Line 666:  Consider a function that reads two lists from a file, appends them, prints the result-
Line 667: ing list, and returns it. The following listing outlines this function in imperative-style
Line 668: pseudocode, using simple types.
Line 669: List appendFromFile(File h) {
Line 670: list1 = readListFrom(h)
Line 671: list2 = readListFrom(h)
Line 672: result = append(list1, list2)
Line 673: print(result)
Line 674: Listing 1.1
Line 675: Appending lists read from a file (pseudocode)
Line 676: ["a", "b", "c", "d"]
Line 677: ["a", "b", "c", "d", "e", "f", "g"]
Line 678: append
Line 679: ["e", "f", "g"]
Line 680: Figure 1.4
Line 681: A pure function, taking inputs and producing outputs with no observable side effects
Line 682: Result
Line 683: Inputs
Line 684: Pure function
Line 685: Figure 1.5
Line 686: Pure functions, in general, take 
Line 687: only inputs and have no observable side effects.
Line 688: 
Line 689: --- 페이지 41 ---
Line 690: 15
Line 691: Pure functional programming
Line 692: return result
Line 693: }
Line 694: This program takes a file handle as an input and returns a List with some side effects.
Line 695: It reads two lists from the given file and prints the list before returning. Figure 1.6
Line 696: illustrates this for the situation when the file contains the two lists ["a", "b", "c",
Line 697: "d"] and ["e", "f", "g"].
Line 698:  The appendFromFile function doesn’t satisfy the referential transparency prop-
Line 699: erty. Referential transparency requires that an expression can be replaced by its result
Line 700: without changing the program’s behavior. Here, however, replacing a call to append-
Line 701: FromFile with its result means that nothing will be read from the file, and nothing will
Line 702: be output to the screen. The function’s input and output types tell us that the input is a
Line 703: file and the output is a list, but nothing in the type describes the side effects the func-
Line 704: tion may execute.
Line 705:  In pure functional programming in general, and Idris in particular, you can solve
Line 706: this problem by writing functions that describe side effects, rather than functions that
Line 707: execute them, and defer the details of execution to the compiler and runtime system.
Line 708: We’ll explore this in greater detail in chapter 5; for now, it’s sufficient to recognize
Line 709: that a program with side effects has a type that makes this explicit. For example,
Line 710: there’s a distinction between the following: 
Line 711: 
Line 712: String is the type of a program that results in a String and is guaranteed to
Line 713: perform no input or output as side effects.
Line 714: 
Line 715: IO String is the type of a program that describes a sequence of input and out-
Line 716: put operations that result in a String.
Line 717: Type-driven development takes this idea much further. As you’ll see from chapter 12
Line 718: onward, you can define types that describe the specific side effects a program can
Line 719: have, such as console interaction, reading and writing global state, or spawning con-
Line 720: current processes and sending messages. 
Line 721: File handle
Line 722: appendFromFile
Line 723: ["a", "b", "c", "d", "e", "f", "g"]
Line 724: Read ["a", "b", "c", "d"]
Line 725: Print ["a", "b", "c", "d", "e", "f", "g"]
Line 726: Read ["e", "f", "g"]
Line 727: Figure 1.6
Line 728: A side-effecting program, reading inputs from a file, printing the result, and 
Line 729: returning the result
Line 730: 
Line 731: --- 페이지 42 ---
Line 732: 16
Line 733: CHAPTER 1
Line 734: Overview
Line 735: 1.3.3
Line 736: Partial and total functions
Line 737: Idris supports an even stronger property than purity for functions, making a distinc-
Line 738: tion between partial and total functions. A total function is guaranteed to produce a
Line 739: result, meaning that it will return a value in a finite time for every possible well-typed
Line 740: input, and it’s guaranteed not to throw any exceptions. A partial function, on the
Line 741: other hand, might not return a result for some inputs. Here are a couple of examples: 
Line 742: The append function is total for finite lists, because it will always return a new
Line 743: list.
Line 744: The function that returns the first element of a list is partial, because it’s not
Line 745: defined if the list is empty, and it will therefore crash.
Line 746: TOTAL FUNCTIONS AND LONG-RUNNING PROGRAMS
Line 747: A total function is guaran-
Line 748: teed to produce a finite prefix of a potentially infinite result. As you’ll see in
Line 749: chapter 11, you can write command shells or servers as total functions that
Line 750: guarantee a response for every user input, indefinitely.
Line 751: The distinction is important because knowing that a function is total allows you to
Line 752: make much stronger claims about its behavior based on its type. If you have a function
Line 753: with a return type of String, for example, you can make different claims depending
Line 754: on whether the function is partial or total.
Line 755: If it’s total—It will return a value of type String in finite time.
Line 756: If it’s partial—If it doesn’t crash or enter an infinite loop, the value it returns will
Line 757: be a String.
Line 758: In most modern languages, we must assume that functions are partial and can there-
Line 759: fore only make the latter, weaker, claim. Idris checks whether functions are total, so we
Line 760: can therefore often make the former, stronger, claim.
Line 761: A useful pattern in type-driven development is to write a type that precisely describes
Line 762: the valid states of a system (like the ATM in section 1.2.2) and that constrains the oper-
Line 763: Total functions and the halting problem
Line 764: The halting problem is the problem of determining whether a program terminates for
Line 765: some specific input. Thanks to Alan Turing, we know that it’s not possible to write a
Line 766: program that solves the halting problem in general. Given this, it’s reasonable to won-
Line 767: der how Idris can determine that a function is total, which is essentially checking that
Line 768: a function terminates for all inputs.
Line 769: Although it can’t solve the problem in general, Idris can identify a large class of func-
Line 770: tions that are definitely total. You’ll learn more about how it does so, along with some
Line 771: techniques for writing total functions, in chapters 10 and 11.
Line 772: 
Line 773: --- 페이지 43 ---
Line 774: 17
Line 775: A quick tour of Idris
Line 776: ations the system is allowed to perform. A total function with that type is then guaran-
Line 777: teed by the type checker to perform those operations as precisely as the type requires. 
Line 778: 1.4
Line 779: A quick tour of Idris
Line 780: The Idris system consists of an interactive environment and a batch mode compiler. In
Line 781: the interactive environment, you can load and type-check source files, evaluate
Line 782: expressions, search libraries, browse documentation, and compile and run complete
Line 783: programs. We’ll use these features extensively throughout this book.
Line 784:  In this section, I’ll briefly introduce the most important features of the environ-
Line 785: ment, which are evaluation and type checking, and describe how to compile and run
Line 786: Idris programs. I’ll also introduce the two most distinctive features of the Idris lan-
Line 787: guage itself: 
Line 788: Holes, which stand for incomplete programs
Line 789: The use of types as first-class language constructs
Line 790: As you’ll see, by using holes you can define functions incrementally, asking the type
Line 791: checker for contextual information to help complete definitions. Using first-class
Line 792: types, you can be very precise about what a function is intended to do, and even ask
Line 793: the type checker to fill in some of the details of functions for you.
Line 794: 1.4.1
Line 795: The interactive environment
Line 796: Much of your interaction with Idris will be through an interactive environment called
Line 797: the read-eval-print loop, typically abbreviated as REPL. As the name suggests, the REPL
Line 798: will read input from the user, usually in the form of an expression, evaluate the expres-
Line 799: sion, and then print the result.
Line 800:  Once Idris is installed, you can start the REPL by typing idris at a shell prompt.
Line 801: You should see something like the following:
Line 802: ____
Line 803: __
Line 804: _
Line 805: /
Line 806: _/___/ /____(_)____
Line 807: / // __
Line 808: / ___/ / ___/
Line 809: Version 1.0
Line 810: _/ // /_/ / /
Line 811: / (__
Line 812: )
Line 813: http://www.idris-lang.org/
Line 814: /___/\__,_/_/
Line 815: /_/____/
Line 816: Type :? for help
Line 817: Idris is free software with ABSOLUTELY NO WARRANTY.
Line 818: For details type :warranty.
Line 819: Idris>
Line 820: INSTALLING IDRIS
Line 821: You can find instructions on how to download and install
Line 822: Idris for Linux, OS X, or Windows in appendix A.
Line 823: You can enter expressions to be evaluated at the Idris> prompt. For example, arith-
Line 824: metic expressions work in the conventional way, with the usual precedence rules (that
Line 825: is, * and / have higher precedence than + and -):
Line 826: Idris> 2 + 2
Line 827: 4 : Integer
Line 828: 
Line 829: --- 페이지 44 ---
Line 830: 18
Line 831: CHAPTER 1
Line 832: Overview
Line 833: Idris> 2.1 * 20
Line 834: 42.0 : Double
Line 835: Idris> 6 + 8 * 11
Line 836: 94 : Integer
Line 837: You can also manipulate Strings. The ++ operator concatenates Strings, and the
Line 838: reverse function reverses a String:
Line 839: Idris> "Hello" ++ " " ++ "World!"
Line 840: "Hello World!" : String
Line 841: Idris> reverse "abcdefg"
Line 842: "gfedcba" : String
Line 843: Notice that Idris prints not only the result of evaluating the expression, but also its
Line 844: type. In general, if you see something of the form x : T—some expression x, a colon,
Line 845: and some other expression T—this can be read as “x has type T.” In the previous exam-
Line 846: ples, you have the following:
Line 847: 
Line 848: 4 has type Integer.
Line 849: 
Line 850: 42.0 has type Double.
Line 851: 
Line 852: "Hello World!" has type String.
Line 853: 1.4.2
Line 854: Checking types
Line 855: The REPL provides a number of commands, all prefixed by a colon. One of the most
Line 856: commonly useful is :t, which allows you to check the types of expressions without eval-
Line 857: uating them:
Line 858: Idris> :t 2 + 2
Line 859: 2 + 2 : Integer
Line 860: Idris> :t "Hello!"
Line 861: "Hello!" : String
Line 862: Types, such as Integer and String, can be manipulated just like any other value, so
Line 863: you can check their types too:
Line 864: Idris> :t Integer
Line 865: Integer : Type
Line 866: Idris> :t String
Line 867: String : Type
Line 868: It’s natural to wonder what the type of Type itself might be. In practice, you’ll never
Line 869: need to worry about this, but for the sake of completeness, let’s take a look:
Line 870: Idris> :t Type
Line 871: Type : Type 1
Line 872: 
Line 873: --- 페이지 45 ---
Line 874: 19
Line 875: A quick tour of Idris
Line 876: That is, Type has type Type 1, Type 1 has type Type 2, and so on forever, as far as
Line 877: we’re concerned. The good news is that Idris will take care of the details for you, and
Line 878: you can always write Type alone. 
Line 879: 1.4.3
Line 880: Compiling and running Idris programs
Line 881: As well as evaluating expressions and inspecting the types of functions, you’ll want to
Line 882: be able to compile and run complete programs. The following listing shows a minimal
Line 883: Idris program.
Line 884: module Main
Line 885: main : IO ()
Line 886: main = putStrLn "Hello, Idris World!"
Line 887: At this stage, there’s no need to worry too much about the syntax or how the program
Line 888: works. For now, you just need to know that Idris source files consist of a module
Line 889: header and a collection of function and data type definitions. They may also import
Line 890: other source files.
Line 891: WHITESPACE SIGNIFICANCE
Line 892: Whitespace is significant in Idris, so when you
Line 893: type listing 1.2, make sure there are no spaces at the beginning of each line.
Line 894: Here, the module is called Main, and there’s only one function definition, called main.
Line 895: The entry point to any Idris program is the main function in the Main module.
Line 896:  To run the program, follow these steps: 
Line 897: 1
Line 898: Create a file called Hello.idr in a text editor.1 Idris source files all have the
Line 899: extension .idr.
Line 900: 2
Line 901: Enter the code in listing 1.2.
Line 902: 3
Line 903: In the working directory where you saved Hello.idr, start up an Idris REPL with
Line 904: the command idris Hello.idr.
Line 905: 4
Line 906: At the Idris prompt, type :exec.
Line 907: If all is well, you should see something like the following:
Line 908: $ idris Hello.idr
Line 909: ____
Line 910: __
Line 911: _
Line 912: /
Line 913: _/___/ /____(_)____
Line 914: / // __
Line 915: / ___/ / ___/
Line 916: Version 1.0
Line 917: _/ // /_/ / /
Line 918: / (__
Line 919: )
Line 920: http://www.idris-lang.org/
Line 921: /___/\__,_/_/
Line 922: /_/____/
Line 923: Type :? for help
Line 924: Idris is free software with ABSOLUTELY NO WARRANTY.
Line 925: For details type :warranty.
Line 926: Type checking ./Hello.idr
Line 927: Listing 1.2
Line 928: Hello, Idris World! (Hello.idr)
Line 929: 1 I recommend Atom because it has a mode for interactive editing of Idris programs, which we’ll use in this
Line 930: book.
Line 931: Module header
Line 932: Function declaration
Line 933: Function definition
Line 934: 
Line 935: --- 페이지 46 ---
Line 936: 20
Line 937: CHAPTER 1
Line 938: Overview
Line 939: *Hello> :exec
Line 940: Hello, Idris World
Line 941: Here, $ stands for your shell prompt. Alternatively, you can create a standalone exe-
Line 942: cutable by invoking the idris command with the -o option, as follows:
Line 943: $ idris Hello.idr -o Hello
Line 944: $ ./Hello
Line 945: Hello, Idris World
Line 946: THE REPL PROMPT
Line 947: The REPL prompt, by default, tells you the name of the
Line 948: file that’s currently loaded. The Idris> prompt indicates that no file is
Line 949: loaded, whereas the prompt *Hello> indicates that the Hello.idr file is
Line 950: loaded. 
Line 951: 1.4.4
Line 952: Incomplete definitions: working with holes
Line 953: Earlier, I compared working with types and values to inserting shapes into a shape-
Line 954: sorter toy. Much as the square shape will only fit through a square hole, the argument
Line 955: "Hello, Idris World!" will only fit into a function in a place where a String type is
Line 956: expected.
Line 957:  Idris functions themselves can contain holes, and a function with a hole is incom-
Line 958: plete. Only a value of an appropriate type will fit into the hole, just as a square shape
Line 959: will only fit into a square hole in the shape sorter. Here’s an incomplete implementa-
Line 960: tion of the “Hello, Idris World!” program:
Line 961: module Main
Line 962: main : IO ()
Line 963: main = putStrLn ?greeting
Line 964: If you edit Hello.idr to replace the string "Hello, Idris World!" with ?greeting and
Line 965: load it into the Idris REPL, you should see something like the following:
Line 966: Type checking ./Hello.idr
Line 967: Holes: Main.greeting
Line 968: *Hello>
Line 969: The syntax ?greeting introduces a hole, which is a part of the program yet to be writ-
Line 970: ten. You can type-check programs with holes and evaluate them at the REPL.
Line 971:  Here, when Idris encounters the ?greeting hole, it creates a new name, greeting,
Line 972: that has a type but no definition. You can inspect the type using :t at the REPL:
Line 973: *Hello> :t greeting
Line 974: --------------------------------------
Line 975: greeting : String
Line 976: If you try to evaluate it, on the other hand, Idris will show you that it’s a hole:
Line 977: *Hello> greeting
Line 978: ?greeting : String
Line 979: ?greeting is a hole, standing 
Line 980: for a missing part of the 
Line 981: program.
Line 982: 
Line 983: --- 페이지 47 ---
Line 984: 21
Line 985: A quick tour of Idris
Line 986: Holes allow you to develop programs incrementally, writing the parts you know and ask-
Line 987: ing the machine to help you by identifying the types for the parts you don’t. For exam-
Line 988: ple, let’s say you’d like to print a character (with type Char) instead of a String. The
Line 989: putStrLn function requires a String argument, so you can’t simply pass a Char to it.
Line 990: module Main
Line 991: main : IO ()
Line 992: main = putStrLn 'x'
Line 993: If you try loading this program into the REPL, Idris will report an error:
Line 994: Hello.idr:4:17:When checking right hand side of main:
Line 995: When checking an application of function Prelude.putStrLn:
Line 996: Type mismatch between
Line 997: Char (Type of 'x')
Line 998: and
Line 999: String (Expected type)
Line 1000: You have to convert a Char to a String somehow. Even if you don’t know exactly how
Line 1001: to do this at first, you can start by adding a hole to stand in for a conversion.
Line 1002: module Main
Line 1003: main : IO ()
Line 1004: main = putStrLn (?convert 'x')
Line 1005: Then you can check the type of the convert hole:
Line 1006: *Hello> :t convert
Line 1007: --------------------------------------
Line 1008: convert : Char -> String
Line 1009: The type of the hole, Char -> String, is the type of a function that takes a Char as an
Line 1010: input and returns a String as an output. We’ll discuss type conversions in more detail
Line 1011: in chapter 2, but an appropriate function to complete this definition is cast:
Line 1012: main : IO ()
Line 1013: main = putStrLn (cast 'x')
Line 1014: Listing 1.3
Line 1015: A program with a type error
Line 1016: Reloading
Line 1017: Instead of exiting the REPL and restarting, you can also reload Hello.idr with the :r
Line 1018: REPL command as follows:
Line 1019: *Hello> :r
Line 1020: Type checking ./Hello.idr
Line 1021: Holes: Main.greeting
Line 1022: *Hello>
Line 1023: Type error, giving a 
Line 1024: character instead of a string
Line 1025: This is a function type, taking a Char 
Line 1026: as input and returning a String. 
Line 1027: 
Line 1028: --- 페이지 48 ---
Line 1029: 22
Line 1030: CHAPTER 1
Line 1031: Overview
Line 1032: 1.4.5
Line 1033: First-class types
Line 1034: A first-class language construct is one that’s treated as a value, with no syntactic restric-
Line 1035: tions on where it can be used. In other words, a first-class construct can be passed to
Line 1036: functions, returned from functions, stored in variables, and so on.
Line 1037:  In most statically typed languages, there are restrictions on where types can be
Line 1038: used, and there’s a strict syntactic separation between types and values. You can’t, for
Line 1039: example, say x = int in the body of a Java method or C function. In Idris, there are
Line 1040: no such restrictions, and types are first-class; not only can types be used in the same
Line 1041: way as any other language construct, but any construct can appear as part of a type.
Line 1042:  This means that you can write functions that compute types, and the return type of
Line 1043: a function can differ depending on the input value to a function. This idea comes up
Line 1044: regularly when programming in Idris, and there are several real-world situations
Line 1045: where it’s useful:
Line 1046: A database schema determines the allowed forms of queries on a database.
Line 1047: A form on a web page determines the number and type of inputs expected.
Line 1048: A network protocol description determines the types of values that can be sent
Line 1049: or received over a network.
Line 1050: In each of these cases, one piece of data tells you about the expected form of some
Line 1051: other data. If you’ve programmed in C, you’ll have seen a similar idea with the
Line 1052: printf function, where one argument is a format string that describes the number
Line 1053: and expected types of the remaining arguments. The C type system can’t check that
Line 1054: the format string is consistent with the arguments, so this check is often hardcoded
Line 1055: into C compilers. In Idris, however, you can write a function similar to printf
Line 1056: directly, by taking advantage of types as first-class constructs. You’ll see this specific
Line 1057: example in chapter 6.
Line 1058:  The following listing illustrates the concept of first-class types with a small exam-
Line 1059: ple: computing a type from a Boolean input.
Line 1060: StringOrInt : Bool -> Type
Line 1061: StringOrInt x = case x of
Line 1062: True => Int
Line 1063: False => String
Line 1064: getStringOrInt : (x : Bool) -> StringOrInt x
Line 1065: getStringOrInt x = case x of
Line 1066: True => 94
Line 1067: False => "Ninety four"
Line 1068: Listing 1.4
Line 1069: Calculating a type, given a Boolean value (FCTypes.idr)
Line 1070: This function calculates a type 
Line 1071: given a Boolean value as an input.
Line 1072: If the input is True,
Line 1073: return the type Int.
Line 1074: If the input is False, 
Line 1075: return the type String.
Line 1076: The return type is calculated 
Line 1077: from the value of the input.
Line 1078: The input x was True, so 
Line 1079: this needs to be an Int.
Line 1080: The input x was False, so 
Line 1081: this needs to be a String.
Line 1082: 
Line 1083: --- 페이지 49 ---
Line 1084: 23
Line 1085: A quick tour of Idris
Line 1086: valToString : (x : Bool) -> StringOrInt x -> String
Line 1087: valToString x val = case x of
Line 1088: True => cast val
Line 1089: False => val
Line 1090: Here, StringOrInt is a function that computes a type. Listing 1.4 uses it in two ways:
Line 1091: In getStringOrInt, StringOrInt calculates the return type. If the input is
Line 1092: True, getStringOrInt returns an Int; otherwise it returns a String.
Line 1093: In valToString, StringOrInt calculates an argument type. If the first input is
Line 1094: True, the second input must be an Int; otherwise it must be a String.
Line 1095: You can see in detail what’s going on by introducing holes in the definition of valTo-
Line 1096: String:
Line 1097: valToString : (x : Bool) -> StringOrInt x -> String
Line 1098: valToString x val = case x of
Line 1099: True => ?xtrueType
Line 1100: False => ?xfalseType
Line 1101: Inspecting the type of a hole with :t gives you not only the type of the hole itself, but
Line 1102: also the types of any local variables in scope. If you check the type of xtrueType, you’ll
Line 1103: see the type of val, which is computed when x is known to be True:
Line 1104: *FCTypes> :t xtrueType
Line 1105: x : Bool
Line 1106: val : Int
Line 1107: --------------------------------------
Line 1108: xtrueType : String
Line 1109: The argument type is 
Line 1110: calculated from the value 
Line 1111: of the input.
Line 1112: The input x was True, so the 
Line 1113: argument val must be an Int and 
Line 1114: needs to be converted to a String.
Line 1115: The input x was False, so the 
Line 1116: argument val must be a String 
Line 1117: and can be returned directly.
Line 1118: Function syntax
Line 1119: We’ll go into much more detail on Idris syntax in the coming chapters. For now, just
Line 1120: keep the following in mind: 
Line 1121: A function type takes the form a -> b -> ... -> t, where a, b, and so on,
Line 1122: are the input types, and t is the output type. Inputs may also be annotated
Line 1123: with names, taking the form (x : a) -> (y : b) -> ... -> t.
Line 1124: 
Line 1125: name : type declares a new function, name, of type type.
Line 1126: Functions are defined by equations: 
Line 1127: square x = x * x
Line 1128: This defines a function called square that multiplies its input by itself. 
Line 1129: 
Line 1130: --- 페이지 50 ---
Line 1131: 24
Line 1132: CHAPTER 1
Line 1133: Overview
Line 1134: So, if x is True, then val must be an Int, as computed by the StringOrInt function.
Line 1135: Similarly, you can check the type of xfalseType to see the type of val when x is known
Line 1136: to be False:
Line 1137: *FCTypes> :t xfalseType
Line 1138: x : Bool
Line 1139: val : String
Line 1140: --------------------------------------
Line 1141: xfalseType : String
Line 1142: This is a small example, but it illustrates a fundamental concept of type-driven devel-
Line 1143: opment and programming with dependent types: the idea that the type of a variable
Line 1144: can be computed from the value of another. In each case, Idris has used StringOrInt
Line 1145: to refine the type of val, given what it knows about the value of x. 
Line 1146: 1.5
Line 1147: Summary
Line 1148: Types are a means of classifying values. Programming languages use types to
Line 1149: decide how to lay out data in memory, and to ensure that data is interpreted
Line 1150: consistently.
Line 1151: A type can be viewed as a specification, so that a language implementation (spe-
Line 1152: cifically, its type checker) can check whether a program conforms to that speci-
Line 1153: fication.
Line 1154: Type-driven development is an iterative process of type, define, refine, creating
Line 1155: a type to model a system, then defining functions, and finally refining the types
Line 1156: as necessary.
Line 1157: In type-driven development, a type is viewed more like a plan, helping an inter-
Line 1158: active environment guide the programmer to a working program.
Line 1159: Dependent types allow you to give more-precise types to programs, and hence
Line 1160: more informative plans to the machine.
Line 1161: In a functional programming language, program execution consists of evaluat-
Line 1162: ing functions.
Line 1163: In a purely functional programming language, additionally, functions have no
Line 1164: side effects.
Line 1165: Instead of writing programs that perform side effects, you can write programs
Line 1166: that describe side effects, with the side effects stated explicitly in a program’s
Line 1167: type.
Line 1168: A total function is guaranteed to produce a result for any well-typed input in
Line 1169: finite time.
Line 1170: Idris is a programming language that’s specifically designed to support type-
Line 1171: driven development. It’s a purely functional programming language with first-
Line 1172: class dependent types.
Line 1173: Idris allows programs to contain holes that stand for incomplete programs.
Line 1174: In Idris, types are first-class, meaning that they can be stored in variables, passed
Line 1175: to functions, or returned from functions like any other value.