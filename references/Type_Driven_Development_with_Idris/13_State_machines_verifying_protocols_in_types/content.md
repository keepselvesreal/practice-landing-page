Line 1: 
Line 2: --- 페이지 378 ---
Line 3: 352
Line 4: State machines:
Line 5: verifying protocols in types
Line 6: In the previous chapter, you saw how to manage mutable state by defining a type
Line 7: for representing sequences of commands in a system, and a function for running
Line 8: those commands. This follows a common pattern: the data type describes a sequence
Line 9: of operations, and the function interprets that sequence in a particular context. For
Line 10: example, State describes sequences of stateful operations, and runState inter-
Line 11: prets those operations with a specific initial state.
Line 12:  In this chapter, we’ll look at one of the advantages of using a type for describing
Line 13: sequences of operations and keeping the execution function separate. It allows you
Line 14: to make the descriptions more precise, so that certain operations can only be run
Line 15: when the state has a specific form. For example, some operations require access to
Line 16: a resource, such as a file handle or database connection, before they’re executed:
Line 17: This chapter covers
Line 18: Specifying protocols in types
Line 19: Describing preconditions and postconditions of 
Line 20: operations
Line 21: Using dependent types in state
Line 22: 
Line 23: --- 페이지 379 ---
Line 24: 353
Line 25: State machines: tracking state in types
Line 26: You need an open file handle to read from a file successfully.
Line 27: You need a connection to a database before you can run a query on the data-
Line 28: base.
Line 29: When you write programs that work with resources like this, you’re really working with
Line 30: a state machine. A database client might have two states, such as Closed and Connected,
Line 31: referring to its connection status to a database. Some operations (such as querying the
Line 32: database) are only valid in the Connected state; some (such as connecting to the data-
Line 33: base) are only valid in the Closed state; and some (such as connecting and closing)
Line 34: also change the state of the system. Figure 13.1 illustrates this system.
Line 35: State machines like the one illustrated in figure 13.1 exist, implicitly, in lots of real-
Line 36: world systems. When you’re implementing communicating systems, for example,
Line 37: whether over a network or using concurrent processes, you need to make sure each
Line 38: party is following the same communication pattern, or the system could deadlock or
Line 39: behave in some other unexpected way. Each party follows a state machine where send-
Line 40: ing or receiving a message puts the overall system into a new state, so it’s important
Line 41: that each party follows a clearly defined protocol. In Idris, we have an expressive type
Line 42: system, so if there’s a model for a protocol, it’s a good idea to express that in a type, so
Line 43: that you can use the type to help implement the protocol accurately.
Line 44:  In this chapter, you’ll see how to make state machines like the one illustrated in fig-
Line 45: ure 13.1explicit in types. In this way, you can be sure that any function that correctly
Line 46: describes a sequence of actions follows the protocol defined by a state machine. Not
Line 47: only that, you can take a type-driven approach to defining sequences of actions using
Line 48: holes and interactive development. We’ll begin with some fairly abstract examples to
Line 49: illustrate how you can describe state machines in types, modeling the states and oper-
Line 50: ations on a door and a vending machine.
Line 51: 13.1
Line 52: State machines: tracking state in types
Line 53: You’ve previously implemented programs with state by defining a type that describes
Line 54: commands for reading and writing state. With dependent types, you can make the
Line 55: types of these commands more precise and include any relevant details about the state
Line 56: of the system in the type itself.
Line 57:  For example, let’s consider how to represent the state of a door with a doorbell. A
Line 58: door can be in one of two states, open (represented as DoorOpen) or closed (repre-
Line 59: sented as DoorClosed), and we’ll allow three operations:
Line 60: Connected
Line 61: Closed
Line 62: Connect
Line 63: Query
Line 64: Close
Line 65: Figure 13.1
Line 66: A state transition diagram showing the high-level operation of 
Line 67: a database. It has two possible states, Closed and Connected. Its three 
Line 68: operations, Connect, Query, and Close, are only valid in specific states.
Line 69: 
Line 70: --- 페이지 380 ---
Line 71: 354
Line 72: CHAPTER 13
Line 73: State machines: verifying protocols in types
Line 74: Opening the door, which moves the system from the DoorClosed state to the
Line 75: DoorOpen state
Line 76: Closing the door, which moves the system from the DoorOpen state to the Door-
Line 77: Closed state
Line 78: Ringing the doorbell, which we’ll only allow when the door is in the Door-
Line 79: Closed state
Line 80: Figure 13.2 is a state transition diagram that shows the states the system can be in and
Line 81: how each operation modifies the overall state.
Line 82: If you can define these state transitions in a type, then a well-typed description of a
Line 83: sequence of operations must correctly follow the rules shown in the state transition
Line 84: diagram. Furthermore, you’ll be able to use holes and interactive editing to find out
Line 85: which operations are valid at a particular point in a sequence.
Line 86:  In this section, you’ll see how to define state machines like the door in a depen-
Line 87: dent type. First, we’ll implement a model of the door, and then we’ll model more-
Line 88: complex states in a model of a simplified vending machine. In each case, we’ll focus
Line 89: on the model of the state transitions, rather than a concrete implementation of the
Line 90: machine.
Line 91: 13.1.1 Finite state machines: modeling a door as a type
Line 92: The state machine in figure 13.2 describes a protocol for correct use of a door by saying
Line 93: which operations are valid in which state, and how those operations affect the state.
Line 94: Listing 13.1 shows one way to represent the possible operations. This also includes a
Line 95: (>>=) constructor for sequencing and a Pure constructor for producing pure values.
Line 96: data DoorCmd : Type where
Line 97: Open : DoorCmd ()
Line 98: Close : DoorCmd ()
Line 99: RingBell : DoorCmd ()
Line 100: Pure : ty -> DoorCmd ty
Line 101: (>>=) : DoorCmd a -> (a -> DoorCmd b) -> DoorCmd b
Line 102: REMINDER: (>>=) AND DO NOTATION
Line 103: Remember that do notation translates
Line 104: into applications of (>>=).
Line 105: Listing 13.1
Line 106: Representing operations on a door as a command type (Door.idr)
Line 107: DoorOpen
Line 108: DoorClosed
Line 109: Open
Line 110: RingBell
Line 111: Close
Line 112: Figure 13.2
Line 113: A state transition 
Line 114: diagram showing the states and 
Line 115: operations on a door
Line 116: Changes the state of the door 
Line 117: from DoorClosed to DoorOpen
Line 118: Changes the state of the door 
Line 119: from DoorOpen to DoorClosed
Line 120: 
Line 121: --- 페이지 381 ---
Line 122: 355
Line 123: State machines: tracking state in types
Line 124: With DoorCmd, you can write functions like the following, which describes a sequence
Line 125: of operations for ringing a doorbell and opening and then closing the door, correctly
Line 126: following the door-usage protocol:
Line 127: doorProg : DoorCmd ()
Line 128: doorProg = do RingBell
Line 129: Open
Line 130: Close
Line 131: Unfortunately, you can also describe invalid sequences of operations that don’t follow
Line 132: the protocol, such as the following, where you attempt to open a door twice, and then
Line 133: ring the doorbell when the door is already open: 
Line 134: doorProgBad : DoorCmd ()
Line 135: doorProgBad = do Open
Line 136: Open
Line 137: RingBell
Line 138: You can avoid this, and limit functions with DoorCmd to valid sequences of operations
Line 139: that do follow the protocol, by keeping track of the door’s state in the type of the
Line 140: DoorCmd operations. The following listing shows how to do this, describing exactly the
Line 141: state transitions represented in figure 13.2 in the types of the commands.
Line 142: data DoorState = DoorClosed | DoorOpen
Line 143: data DoorCmd : Type ->
Line 144: DoorState ->
Line 145: DoorState ->
Line 146: Type where
Line 147: Open : DoorCmd
Line 148: () DoorClosed DoorOpen
Line 149: Close : DoorCmd
Line 150: () DoorOpen
Line 151: DoorClosed
Line 152: RingBell : DoorCmd () DoorClosed DoorClosed
Line 153: Pure : ty -> DoorCmd ty state state
Line 154: (>>=) : DoorCmd a state1 state2 ->
Line 155: (a -> DoorCmd b state2 state3) ->
Line 156: DoorCmd b state1 state3
Line 157: Each command’s type takes three arguments:
Line 158: The type of the value produced by the command
Line 159: The input state of the door; that is, the state the door must be in before you can
Line 160: execute the operation
Line 161: The output state of the door; that is, the state the door will be in after you exe-
Line 162: cute the operation
Line 163: Listing 13.2
Line 164: Modeling the door state machine in a type, describing state transitions in
Line 165: the types of the commands (Door.idr)
Line 166: Defines the two possible 
Line 167: states of a door
Line 168: The type of the result of the operation
Line 169: The state of the door before the operation
Line 170: The state of the door after the operation
Line 171: Produces a value without 
Line 172: affecting the state
Line 173: Sequences two operations. The 
Line 174: output state of the first gives 
Line 175: the input state of the second.
Line 176: Combined operation goes from the input 
Line 177: state of the first operation to the output 
Line 178: state of the second
Line 179: 
Line 180: --- 페이지 382 ---
Line 181: 356
Line 182: CHAPTER 13
Line 183: State machines: verifying protocols in types
Line 184: An implementation of the following function would therefore describe a sequence of
Line 185: actions that begins and ends with the door closed:
Line 186: doorProg : DoorCmd () DoorClosed DoorClosed
Line 187: ARGUMENT ORDER IN DOORCMD
Line 188: Notice that the type that a sequence of opera-
Line 189: tions produces is the first argument to DoorCmd, and it’s followed by the
Line 190: input and output states. This is a common convention when defining types
Line 191: for describing state transitions, and it will become important in chapter 14
Line 192: when we look at more-complex state machines that deal with errors and feed-
Line 193: back from the environment.
Line 194: In general, if you have a value of type DoorType ty beforeState afterState, it
Line 195: describes a sequence of door actions that produces a value of type ty; it begins with
Line 196: the door in the state beforeState; and it ends with the door in the state afterState. 
Line 197: 13.1.2 Interactive development of sequences of door operations
Line 198: To see how the types in DoorCmd can help you write sequences of operations correctly,
Line 199: let’s reimplement doorProg. We’ll write this in the same way as before: ring the door-
Line 200: bell, open the door, and close the door.
Line 201:  If you write it incrementally, you’ll see how the type shows the changes in the state
Line 202: of the door throughout the sequence of actions:
Line 203: 1
Line 204: Define—Begin with the skeleton definition: 
Line 205: doorProg : DoorCmd () DoorClosed DoorClosed
Line 206: doorProg = ?doorProg_rhs
Line 207:  2
Line 208: Refine, type—Add an action to ring the doorbell: 
Line 209: doorProg : DoorCmd () DoorClosed DoorClosed
Line 210: doorProg = do RingBell
Line 211: ?doorProg_rhs
Line 212: If you check the type of ?doorProg_rhs now, you’ll see that it should be a
Line 213: sequence of actions that begins and ends with the door in the DoorClosed state: 
Line 214: --------------------------------------
Line 215: doorProg_rhs : DoorCmd () DoorClosed DoorClosed
Line 216:  3
Line 217: Refine, type—Next, add an action to open the door: 
Line 218: doorProg : DoorCmd () DoorClosed DoorClosed
Line 219: doorProg = do RingBell
Line 220: Open
Line 221: ?doorProg_rhs
Line 222: If you check the type of ?doorProg_rhs now, you’ll see that it should begin with
Line 223: the door in the DoorOpen state instead: 
Line 224: --------------------------------------
Line 225: doorProg_rhs : DoorCmd () DoorOpen DoorClosed
Line 226: 
Line 227: --- 페이지 383 ---
Line 228: 357
Line 229: State machines: tracking state in types
Line 230:  4
Line 231: Refine failure—If you add an extra Open now, with the door already in the
Line 232: DoorOpen state, you’ll get a type error: 
Line 233: doorProg : DoorCmd () DoorClosed DoorClosed
Line 234: doorProg = do RingBell
Line 235: Open
Line 236: Open
Line 237: ?doorProg_rhs
Line 238: The error says that the type of Open is an operation that starts in the DoorClosed
Line 239: state, but the expected type starts in the DoorOpen state: 
Line 240: Door.idr:20:15:
Line 241: When checking right hand side of doorProg with expected type
Line 242: DoorCmd () DoorClosed DoorClosed
Line 243: When checking an application of constructor Main.>>=:
Line 244: Type mismatch between
Line 245: DoorCmd () DoorClosed DoorOpen (Type of Open)
Line 246: and
Line 247: DoorCmd a DoorOpen state2 (Expected type)
Line 248: Specifically:
Line 249: Type mismatch between
Line 250: DoorClosed
Line 251: and
Line 252: DoorOpen
Line 253: 5
Line 254: Refine—Instead, complete the definition by closing the door: 
Line 255: doorProg : DoorCmd () DoorClosed DoorClosed
Line 256: doorProg = do RingBell
Line 257: Open
Line 258: Close
Line 259: Defining preconditions and postconditions in types
Line 260: The type of doorProg includes input and output states that give preconditions and
Line 261: postconditions for the sequence (the door must be closed both before and after the
Line 262: sequence). If the definition violates either, you’ll get a type error.
Line 263: For example, you might forget to close the door:
Line 264: doorProg : DoorCmd () DoorClosed DoorClosed
Line 265: doorProg = do RingBell
Line 266: Open
Line 267: In this case, you’ll get a type error:
Line 268: Door.idr:18:15:
Line 269: When checking right hand side of doorProg with expected type
Line 270: DoorCmd () DoorClosed DoorClosed
Line 271: When checking an application of constructor Main.>>=:
Line 272: Type mismatch between
Line 273: DoorCmd () DoorClosed DoorOpen (Type of Open)
Line 274: 
Line 275: --- 페이지 384 ---
Line 276: 358
Line 277: CHAPTER 13
Line 278: State machines: verifying protocols in types
Line 279: By defining DoorCmd in this way, with the input and output states explicit in the type,
Line 280: you’ve defined what it means for a sequence of door operations to be valid. And by writ-
Line 281: ing doorProg incrementally, with a sequence of steps and a hole for the rest of the defi-
Line 282: nition, you can see the state of the door at each stage by looking at the type of the hole.
Line 283:  The door has exactly two states, DoorClosed and DoorOpen, and you can describe
Line 284: exactly when you change states from one to the other in the types of the door opera-
Line 285: tions. But not all systems have an exact number of states that you can determine in
Line 286: advance. Next, we’ll look at how you can model systems with an infinite number of
Line 287: possible states. 
Line 288: 13.1.3 Infinite states: modeling a vending machine
Line 289: In this section, we’ll model a vending machine using type-driven development, writing
Line 290: types that explicitly describe the input and output states of each operation. As a sim-
Line 291: plification, the machine accepts only one type of coin (a £1 coin) and dispenses one
Line 292: product (a chocolate bar). Even so, there could be an arbitrarily large number of
Line 293: coins or chocolate bars in the machine, so the number of possible states is not finite.
Line 294:  Table 13.1 describes the basic operations of a vending machine, along with the
Line 295: state of the machine before and after each operation.
Line 296: As with the door example, each operation has a precondition and a postcondition:
Line 297: Precondition—The number of coins and amount of chocolate that must be in
Line 298: the machine before the operation
Line 299: Table 13.1
Line 300: Vending machine operations, with input and output states represented as Nat
Line 301: Coins (before)
Line 302: Chocolate (before)
Line 303: Operation
Line 304: Coins (after)
Line 305: Chocolate (after)
Line 306: pounds
Line 307: chocs
Line 308: Insert coin
Line 309: S pounds
Line 310: chocs
Line 311: S pounds
Line 312: S chocs
Line 313: Vend chocolate
Line 314: pounds
Line 315: chocs
Line 316: pounds
Line 317: chocs
Line 318: Return coins
Line 319: Z
Line 320: chocs
Line 321: (continued)
Line 322: and
Line 323: DoorCmd () DoorClosed DoorClosed (Expected type)
Line 324: Specifically:
Line 325: Type mismatch between
Line 326: DoorOpen
Line 327: and
Line 328: DoorClosed
Line 329: The error refers to the final step and says that Open moves from DoorClosed to
Line 330: DoorOpen, but the expected type is to move from DoorClosed to DoorClosed.
Line 331: 
Line 332: --- 페이지 385 ---
Line 333: 359
Line 334: State machines: tracking state in types
Line 335: Postcondition—The number of coins and amount of chocolate in the machine
Line 336: after the operation.
Line 337: You can represent the state of the machine as a pair of two Nats, the first representing
Line 338: the number of coins in the machine and the second representing the number of
Line 339: chocolates:
Line 340: VendState : Type
Line 341: VendState = (Nat, Nat)
Line 342: The next listing shows a representation of the vending machine state as an Idris type,
Line 343: with the state transitions from table 13.1 explicitly written in the types of the
Line 344: MachineCmd operations.
Line 345: VendState : Type
Line 346: VendState = (Nat, Nat)
Line 347: data MachineCmd : Type ->
Line 348: VendState ->
Line 349: VendState ->
Line 350: Type where
Line 351: InsertCoin : MachineCmd () (pounds, chocs)
Line 352: (S pounds, chocs)
Line 353: Vend
Line 354: : MachineCmd () (S pounds, S chocs) (pounds, chocs)
Line 355: GetCoins
Line 356: : MachineCmd () (pounds, chocs)
Line 357: (Z, chocs)
Line 358: To complete the model, you’ll need to be able to sequence commands. You’ll also
Line 359: need to be able to read user input: the commands you’re defining describe what the
Line 360: machine does, but there’s also a user interface that consists of the following:
Line 361: A coin slot
Line 362: A vend button, for dispensing chocolate
Line 363: A change button, for returning any unused coins
Line 364: You can model these operations in a data type for describing possible user inputs. List-
Line 365: ing 13.4 shows the complete model of the vending machine, including additional
Line 366: operations for displaying a message (Display), refilling the machine (Refill), and
Line 367: reading user actions (GetInput).
Line 368: data Input = COIN
Line 369: | VEND
Line 370: | CHANGE
Line 371: | REFILL Nat
Line 372: Listing 13.3
Line 373: Modeling the vending machine in a type, describing state transitions in the
Line 374: types of commands (Vending.idr)
Line 375: Listing 13.4
Line 376: The complete model of vending machine state (Vending.idr)
Line 377: A type synonym for the machine state: 
Line 378: a pair of the number of £1 coins and 
Line 379: the number of chocolates
Line 380: Machine state before the 
Line 381: operation (precondition)
Line 382: Machine state after the 
Line 383: operation (postcondition)
Line 384: Defines the possible 
Line 385: user inputs
Line 386: 
Line 387: --- 페이지 386 ---
Line 388: 360
Line 389: CHAPTER 13
Line 390: State machines: verifying protocols in types
Line 391: data MachineCmd : Type -> VendState -> VendState -> Type where
Line 392: InsertCoin : MachineCmd () (pounds, chocs)
Line 393: (S pounds, chocs)
Line 394: Vend
Line 395: : MachineCmd () (S pounds, S chocs) (pounds, chocs)
Line 396: GetCoins
Line 397: : MachineCmd () (pounds, chocs)
Line 398: (Z, chocs)
Line 399:     Refill :(bars : Nat) ->
Line 400: MachineCmd () (Z, chocs)
Line 401: (Z, bars + chocs)
Line 402: Display : String -> MachineCmd () state state
Line 403: GetInput : MachineCmd (Maybe Input) state state
Line 404: Pure : ty -> MachineCmd ty state state
Line 405: (>>=) : MachineCmd a state1 state2 ->
Line 406:              (a -> MachineCmd b state2 state3) ->
Line 407: MachineCmd b state1 state3
Line 408: data MachineIO : VendState -> Type where
Line 409: Do : MachineCmd a state1 state2 ->
Line 410: (a -> Inf (MachineIO state2)) -> MachineIO state1
Line 411: namespace MachineDo
Line 412: (>>=) : MachineCmd a state1 state2 ->
Line 413: (a -> Inf (MachineIO state2)) -> MachineIO state1
Line 414: (>>=) = Do
Line 415: 13.1.4 A verified vending machine description
Line 416: Listing 13.5 shows the outline of a function that describes verified sequences of opera-
Line 417: tions for a vending machine using the state transitions defined by MachineCmd. As long
Line 418: as it type-checks, you know that you’ve correctly sequenced the operations, and you’ll
Line 419: never execute an operation without its precondition being satisfied.
Line 420: mutual
Line 421: vend : MachineIO (pounds, chocs)
Line 422: vend = ?vend_rhs
Line 423: refill : (num : Nat) -> MachineIO (pounds, chocs)
Line 424: refill = ?refill_rhs
Line 425: machineLoop : MachineIO (pounds, chocs)
Line 426: machineLoop =
Line 427: do Just x <- GetInput
Line 428: | Nothing => do Display "Invalid input"
Line 429: machineLoop
Line 430: case x of
Line 431: COIN => do InsertCoin
Line 432: machineLoop
Line 433: VEND => vend
Line 434: Listing 13.5
Line 435: A main loop that reads and processes user input to the vending machine
Line 436: (Vending.idr)
Line 437: Refilling the
Line 438: machine is only
Line 439: valid if there are
Line 440: no coins in the
Line 441: machine.
Line 442: Displaying a
Line 443: message
Line 444: doesn’t affect
Line 445: the state.
Line 446: Reading user input
Line 447: doesn’t affect the state.
Line 448: Returns Maybe Input to
Line 449: account for possible
Line 450: invalid inputs.
Line 451: An infinite sequence of machine 
Line 452: state transitions. The type gives the 
Line 453: starting state of the machine.
Line 454: Supports do notation for infinite
Line 455: sequences of machine state transitions
Line 456: vend and refill need to 
Line 457: check their preconditions 
Line 458: are satisfied.
Line 459: User input
Line 460: could be invalid,
Line 461: so check here.
Line 462: A pattern-matching 
Line 463: binding alternative (see 
Line 464: chapter 5). This branch 
Line 465: is executed if GetInput 
Line 466: returns Nothing.
Line 467: 
Line 468: --- 페이지 387 ---
Line 469: 361
Line 470: State machines: tracking state in types
Line 471: CHANGE => do GetCoins
Line 472: Display "Change returned"
Line 473: machineLoop
Line 474: REFILL num => refill num
Line 475: There are holes for vend and refill. In each case, you need to check that the num-
Line 476: ber of coins and chocolates satisfy their preconditions. If you try to Vend without
Line 477: checking the precondition, Idris will report an error:
Line 478: vend : MachineIO (pounds, chocs)
Line 479: vend = do Vend
Line 480: Display "Enjoy!"
Line 481: machineLoop
Line 482: Idris will report an error because you haven’t checked whether there’s a coin in the
Line 483: machine and a chocolate bar available, so the precondition might not be satisfied:
Line 484: Vending.idr:67:13:
Line 485: When checking right hand side of vend with expected type
Line 486: MachineIO (pounds, chocs)
Line 487: When checking an application of function Main.MachineDo.>>=:
Line 488: Type mismatch between
Line 489: MachineCmd ()
Line 490: (S pounds1, S chocs2)
Line 491: (pounds1, chocs2) (Type of Vend)
Line 492: and
Line 493: MachineCmd () (pounds, chocs) (pounds1, chocs2) (Expected type)
Line 494: Specifically:
Line 495: Type mismatch between
Line 496: S chocs1
Line 497: and
Line 498: chocs
Line 499: The error says that the input state must be of the form (S pounds1, S chocs2), but
Line 500: instead it’s of the form (pounds, chocs).
Line 501:  You can solve this problem by pattern matching on the implicit arguments, pounds
Line 502: and chocs, to ensure they’re in the right form, or display an error otherwise. The fol-
Line 503: lowing listing shows definitions of vend and refill that do this.
Line 504: vend : MachineIO (pounds, chocs)
Line 505: vend {pounds = S p} {chocs = S c}
Line 506: = do Vend
Line 507: Display "Enjoy!"
Line 508: machineLoop
Line 509: vend {pounds = Z}
Line 510: = do Display "Insert a coin"
Line 511: machineLoop
Line 512: vend {chocs = Z}
Line 513: = do Display "Out of stock"
Line 514: Listing 13.6
Line 515: Adding definitions of vend and refill that check that their precondi-
Line 516: tions are satisfied (Vending.idr)
Line 517: Doesn’t type-check because there may not 
Line 518: be coins or chocolate in the machine
Line 519: A coin and a chocolate are 
Line 520: available, so vend and continue.
Line 521: No money in the machine; can’t vend
Line 522: No chocolate in the machine; can’t vend
Line 523: 
Line 524: --- 페이지 388 ---
Line 525: 362
Line 526: CHAPTER 13
Line 527: State machines: verifying protocols in types
Line 528: machineLoop
Line 529: refill : (num : Nat) -> MachineIO (pounds, chocs)
Line 530: refill {pounds = Z} num
Line 531: = do Refill num
Line 532: machineLoop
Line 533: refill _ = do Display "Can't refill: Coins in machine"
Line 534: machineLoop
Line 535: With both the door and the vending machine, we’ve used types to model the states of a
Line 536: physical system. In each case, the type gives an abstraction of the state a system is in
Line 537: before and after each operation, and values in the type describe the valid sequences of
Line 538: operations. We haven’t implemented a run function to execute the state transitions
Line 539: for either DoorCmd or MachineCmd, but in the code accompanying this book, which is
Line 540: available online, you’ll find code that implements a console simulation of the vending
Line 541: machine.
Line 542:  In the next section, you’ll see a more concrete example of tracking state in the
Line 543: type, implementing a stack data structure. I’ll use this example to illustrate how you
Line 544: can execute commands in practice. 
Line 545: Exercises
Line 546: 1
Line 547: Change the RingBell operation so that it works in any state, rather than only when
Line 548: the door is closed. You can test your answer by seeing that the following function
Line 549: type-checks: 
Line 550: doorProg : DoorCmd () DoorClosed DoorClosed
Line 551: doorProg = do RingBell
Line 552: Open
Line 553: RingBell
Line 554: Close
Line 555:  2
Line 556: The following (incomplete) type defines a command for a guessing game, where
Line 557: the input and output states are the number of remaining guesses allowed: 
Line 558: data GuessCmd : Type -> Nat -> Nat -> Type where
Line 559: Try : Integer -> GuessCmd Ordering ?in_state ?out_state
Line 560: Pure : ty -> GuessCmd ty state state
Line 561: (>>=) : GuessCmd a state1 state2 ->
Line 562: (a -> GuessCmd b state2 state3) ->
Line 563: GuessCmd b state1 state3
Line 564: The Try command returns an Ordering that says whether the guess was too high,
Line 565: too low, or correct, and that changes the number of available guesses. Complete the
Line 566: type of Try so that you can only make a guess when there’s at least one guess
Line 567: allowed, and so that guessing reduces the number of guesses available.
Line 568: If you have a correct answer, the following definition should type-check: 
Line 569: threeGuesses: GuessCmd () 3 0
Line 570: threeGuesses = do Try 10
Line 571: Refill only allows 
Line 572: restocking with chocolate 
Line 573: when there are no coins 
Line 574: in the machine.
Line 575: 
Line 576: --- 페이지 389 ---
Line 577: 363
Line 578: Dependent types in state: implementing a stack
Line 579: Try 20
Line 580: Try 15
Line 581: Pure ()
Line 582: Also, the following definition shouldn’t type-check: 
Line 583: noGuesses : GuessCmd () 0 0
Line 584: noGuesses = do Try 10
Line 585: Pure ()
Line 586:  3
Line 587: The following type defines the possible states of matter: 
Line 588: data Matter = Solid | Liquid | Gas
Line 589: Define a MatterCmd type in such a way that the following definitions type-check: 
Line 590: iceSteam : MatterCmd () Solid Gas
Line 591: iceSteam = do Melt
Line 592: Boil
Line 593: steamIce : MatterCmd () Gas Solid
Line 594: steamIce = do Condense
Line 595: Freeze
Line 596: Additionally, the following definition should not type-check: 
Line 597: overMelt : MatterCmd () Solid Gas
Line 598: overMelt = do Melt
Line 599: Melt
Line 600: 13.2
Line 601: Dependent types in state: implementing a stack
Line 602: You’ve seen how to model state transitions in a type for two abstract examples: a door
Line 603: (representing whether it was open or closed in its type) and a vending machine (rep-
Line 604: resenting its contents in its type). Storing this abstract information in the type of the
Line 605: operations is particularly useful when you also have concrete data that relates to that
Line 606: abstract data. For example, if you’re describing data of a specific size, and the type of
Line 607: an operation tells you how it changes the size of the data, you can use a Vect as a con-
Line 608: crete representation. You’ll know the required length of the input and output Vect
Line 609: from the type of each operation.
Line 610:  In this section, you’ll see how this works by implementing operations on a stack
Line 611: data structure. A stack is a last-in, first-out data structure where you can add items to
Line 612: and remove them from the top of the stack, and only the top item is ever accessible. A
Line 613: stack supports three operations:
Line 614: 
Line 615: Push—Adds a new item to the top of the stack
Line 616: 
Line 617: Pop—Removes the top item from the stack, provided that the stack isn’t empty
Line 618: 
Line 619: Top—Inspects the top item on the stack, provided that the stack isn’t empty
Line 620: Like the operations on the vending machine, each of these operations has a precondi-
Line 621: tion that describes the necessary input state and a postcondition describing the out-
Line 622: put state. Table 13.2 describes these, giving the required stack size before each
Line 623: operation and the resulting stack size after the operation.
Line 624: 
Line 625: --- 페이지 390 ---
Line 626: 364
Line 627: CHAPTER 13
Line 628: State machines: verifying protocols in types
Line 629:  
Line 630: You’ll express the preconditions and postconditions in the types of each operation.
Line 631: Once you’ve defined the operations on a stack, you’ll implement a function to run
Line 632: sequences of stack operations using a concrete representation of a stack with its
Line 633: height in its type. Because you’re using the stack’s height in the state transitions, a
Line 634: good concrete representation of a stack is a Vect. You know, for example, that a stack
Line 635: of Integer of height 10, contains exactly 10 integers, so you can represent this as a
Line 636: value of type Vect 10 Integer.
Line 637:  Finally, you’ll see an example of a stack in action, implementing a stack-based
Line 638: interactive calculator.
Line 639: 13.2.1 Representing stack operations in a state machine
Line 640: As with DoorCmd and MachineCmd in section 13.1, we’ll describe operations on a stack
Line 641: in a dependent type and put the important properties of the input and output states
Line 642: explicitly in the type. Here, the property of the state that interests us is the height of
Line 643: the stack.
Line 644:  Listing 13.7 shows how you can express the operations in table 13.2 in code,
Line 645: describing how each operation affects the height of the stack. For this example, you’ll
Line 646: only store Integer values on the stack, but you could extend StackCmd to allow
Line 647: generic stacks by parameterizing over the element type in the stack.
Line 648: import Data.Vect
Line 649: data StackCmd : Type -> Nat -> Nat -> Type where
Line 650: Push : Integer -> StackCmd () height (S height)
Line 651: Pop : StackCmd Integer (S height) height
Line 652: Top : StackCmd Integer (S height) (S height)
Line 653: Pure : ty -> StackCmd ty height height
Line 654: (>>=) : StackCmd a height1 height2 ->
Line 655: (a -> StackCmd b height2 height3) ->
Line 656: StackCmd b height1 height3
Line 657: Table 13.2
Line 658: Stack operations, with input and output stack sizes represented as Nat
Line 659: Stack size (before)
Line 660: Operation
Line 661: Stack size (after)
Line 662: height
Line 663: Push element
Line 664: S height
Line 665: S height
Line 666: Pop element
Line 667: height
Line 668: S height
Line 669: Inspect top element
Line 670: S height
Line 671: Listing 13.7
Line 672: Representing operations on a stack data structure with the input and out-
Line 673: put heights of the stack in the type (Stack.idr)
Line 674: You’ll use a Vect to represent the 
Line 675: stack, so import Data.Vect here.
Line 676: Push increases the height 
Line 677: of the stack by 1.
Line 678: Pop requires there to be at least one 
Line 679: element on the stack, and it decreases the 
Line 680: height of the stack by 1.
Line 681: Top requires there to be at
Line 682: least one element on the
Line 683: stack, and it preserves the
Line 684: height of the stack.
Line 685: 
Line 686: --- 페이지 391 ---
Line 687: 365
Line 688: Dependent types in state: implementing a stack
Line 689: You’re using a Vect to represent the stack, so every time you add an element to the
Line 690: vector or remove an element, you’ll change the vector’s type. You’re therefore repre-
Line 691: senting dependently typed mutable state by putting the relevant arguments to the
Line 692: type (the length of the Vect) in the StateCmd type itself.
Line 693:  Using StackCmd, you can write sequences of stack operations where the input and
Line 694: output heights of the stack are explicit in the types. For example, the following func-
Line 695: tion pushes two integers, pops two integers, and then returns their sum:
Line 696: testAdd : StackCmd Integer 0 0
Line 697: testAdd = do Push 10
Line 698: Push 20
Line 699: val1 <- Pop
Line 700: val2 <- Pop
Line 701: Pure (val1 + val2)
Line 702: The types of the constructors in StackCmd ensure that there will always be an element
Line 703: on the stack when you try to Pop. For example, if you only push one integer in
Line 704: testAdd, Idris will report an error:
Line 705: testAdd : StackCmd Integer 0 0
Line 706: testAdd = do Push 10
Line 707: val1 <- Pop
Line 708: val2 <- Pop
Line 709: Pure (val1 + val2)
Line 710: When you try to define testAdd like this, Idris reports an error:
Line 711: Stack.idr:27:22:
Line 712: When checking right hand side of testAdd with expected type
Line 713: StackCmd Integer 0 0
Line 714: When checking an application of constructor Main.>>=:
Line 715: Type mismatch between
Line 716: StackCmd Integer (S height) height (Type of Pop)
Line 717: and
Line 718: StackCmd a 0 height2 (Expected type)
Line 719: Specifically:
Line 720: Type mismatch between
Line 721: S height
Line 722: and
Line 723: 0
Line 724: This error, and particularly the mismatch between S height and 0, means that you
Line 725: have a stack of height 0, but Pop needs a stack that contains at least one element.
Line 726:  This approach is similar to the stateful functions defined in chapter 12, here using
Line 727: Push and Pop to describe how you’re modifying and querying the state. As with the
Line 728: earlier descriptions of sequences of stateful operations, you’ll need to write a separate
Line 729: function to run those sequences. 
Line 730: There’s only one element on the 
Line 731: stack, so Pop doesn’t type-check.
Line 732: 
Line 733: --- 페이지 392 ---
Line 734: 366
Line 735: CHAPTER 13
Line 736: State machines: verifying protocols in types
Line 737: 13.2.2 Implementing the stack using Vect
Line 738: Listing 13.8 shows how to implement a function that executes stack operations. This is
Line 739: similar to runState, which you saw in chapter 12, but here you take an input Vect of
Line 740: the correct height as the contents of the stack.
Line 741: runStack : (stk : Vect inHeight Integer) ->
Line 742: StackCmd ty inHeight outHeight ->
Line 743: (ty, Vect outHeight Integer)
Line 744: runStack stk (Push val) = ((), val :: stk)
Line 745: runStack (val :: stk) Pop = (val, stk)
Line 746: runStack (val :: stk) Top = (val, val :: stk)
Line 747: runStack stk (Pure x) = (x, stk)
Line 748: runStack stk (cmd >>= next)
Line 749: = let (cmdRes, newStk) = runStack stk cmd in
Line 750: runStack newStk (next cmdRes)
Line 751: If you try runStack with testAdd, passing it an initial empty stack, you’ll see that it
Line 752: returns the sum of the two elements that you push, and that the final stack is empty:
Line 753: *Stack> runStack [] testAdd
Line 754: (30, []) : (Integer, Vect 0 Integer)
Line 755: You can also define functions like the following, which adds the top two elements on
Line 756: the stack, putting the result back onto the stack:
Line 757: doAdd : StackCmd () (S (S height)) (S height)
Line 758: doAdd = do val1 <- Pop
Line 759: val2 <- Pop
Line 760: Push (val1 + val2)
Line 761: The input state S (S height) means that the stack must have at least two elements on
Line 762: it, but, otherwise, it could be any height. If you try executing doAdd with an initial
Line 763: stack containing two elements, you’ll see that it results in a stack containing a single
Line 764: element that’s the sum of the two input elements:
Line 765: *Stack> runStack [2,3] doAdd
Line 766: ((), [5]) : ((), Vect 1 Integer)
Line 767: If the input state contains more than two elements, you’ll see that it results in a stack
Line 768: with a height one smaller than the input height. For example, an input stack of [2, 3,
Line 769: 4] results in an output stack with the value [2 + 3, 4]:
Line 770: *Stack> runStack [2,3,4] doAdd
Line 771: ((), [5, 4]) : ((), Vect 2 Integer)
Line 772: Listing 13.8
Line 773: Executing a sequence of actions on a stack, using a Vect to represent
Line 774: the stack’s contents
Line 775: The length of 
Line 776: the input 
Line 777: vector is the 
Line 778: input height 
Line 779: of the stack.
Line 780: The length of the 
Line 781: output vector is 
Line 782: the output height 
Line 783: of the stack.
Line 784: The length of the output 
Line 785: vector is the output 
Line 786: height of the stack.
Line 787: 
Line 788: --- 페이지 393 ---
Line 789: 367
Line 790: Dependent types in state: implementing a stack
Line 791: You can add the two elements on the resulting stack with another call to doAdd:
Line 792: *Stack> runStack [2,3,4] (do doAdd; doAdd)
Line 793: ((), [9]) : ((), Vect 1 Integer)
Line 794: But trying one more doAdd would result in a type error, because there’s only one ele-
Line 795: ment left on the stack:
Line 796: *Stack> runStack [2,3,4] (do doAdd; doAdd; doAdd)
Line 797: (input):1:34:When checking an application of constructor Main.>>=:
Line 798: Type mismatch between
Line 799: StackCmd () (S (S height)) (S height) (Type of doAdd)
Line 800: and
Line 801: StackCmd ty 1 outHeight (Expected type)
Line 802: Specifically:
Line 803: Type mismatch between
Line 804: S height
Line 805: and
Line 806: 0
Line 807: This error means that you needed S (S height) elements on the stack (that is, at least
Line 808: two elements) but you only had S height (that is, at least one, but not necessarily any
Line 809: more). By putting the height of the stack in the type, therefore, you’ve explicitly spec-
Line 810: ified the preconditions and postconditions on each operation, so you get a type error
Line 811: if you violate any of these. 
Line 812: 13.2.3 Using a stack interactively: a stack-based calculator
Line 813: If you add commands for reading from and writing to the console, you can write a
Line 814: console application for manipulating the stack and implement a stack-based calcula-
Line 815: tor. A user can either enter a number, which pushes the number onto the stack, or
Line 816: add, which adds the top two stack items, pushes the result onto the stack, and displays
Line 817: the result. A typical session might go as follows:
Line 818: *StackIO> :exec
Line 819: > 3
Line 820: > 4
Line 821: > 5
Line 822: > add
Line 823: 9
Line 824: > add
Line 825: 12
Line 826: > add
Line 827: Fewer than two items on the stack
Line 828: Figure 13.3 shows how each of the valid inputs in this session affects the contents of
Line 829: the stack. Every time the user enters an integer, the stack size grows by one, and every
Line 830: time the user enters add, the stack size decreases by one, as long as there are two items
Line 831: to add.
Line 832: User pushes three values 
Line 833: onto the stack: 3, 4 and 5
Line 834: Adds the top two stack items, 
Line 835: displays and pushes the result
Line 836: Error, because there’s only one item (12) on the 
Line 837: 
Line 838: --- 페이지 394 ---
Line 839: 368
Line 840: CHAPTER 13
Line 841: State machines: verifying protocols in types
Line 842: To implement this interactive stack program, you’ll need to extend StackCmd to sup-
Line 843: port reading from and writing to the console. The following listing shows StackCmd in
Line 844: a new file, StackIO.idr, extended with two commands: GetStr and PutStr.
Line 845: data StackCmd : Type -> Nat -> Nat -> Type where
Line 846: Push : Integer -> StackCmd () height (S height)
Line 847: Pop : StackCmd Integer (S height) height
Line 848: Top : StackCmd Integer (S height) (S height)
Line 849: GetStr : StackCmd String height height
Line 850: PutStr : String -> StackCmd () height height
Line 851: Pure : ty -> StackCmd ty height height
Line 852: (>>=) : StackCmd a height1 height2 ->
Line 853: (a -> StackCmd b height2 height3) ->
Line 854: StackCmd b height1 height3
Line 855: DEPENDENT STATES IN THE EFFECTS LIBRARY
Line 856: I mentioned the Effects library in
Line 857: chapter 12, which allows you to combine effects like state and console I/O
Line 858: without having to define a new type, like StackCmd here. The Effects library
Line 859: supports descriptions of state transitions and dependent state as in Stack-
Line 860: Cmd. I won’t describe the Effects library further in this book, but learning
Line 861: about the principles of dependent state here will mean that you’ll be able to
Line 862: learn how to use the more flexible Effects library more readily.
Line 863: You’ll also need to update runStack to support the two new commands. Because Get-
Line 864: Str and PutStr describe interactive actions, you’ll need to update the type of run-
Line 865: Stack to return IO actions. Here’s the updated runStack.
Line 866: runStack : (stk : Vect inHeight Integer) ->
Line 867: StackCmd ty inHeight outHeight ->
Line 868: IO (ty, Vect outHeight Integer)
Line 869: runStack stk (Push val) = pure ((), val :: stk)
Line 870: Listing 13.9
Line 871: Extending StackCmd to support console I/O with the commands GetStr
Line 872: and PutStr (StackIO.idr)
Line 873: Listing 13.10
Line 874: Updating runStack to support the interactive commands GetStr and
Line 875: PutStr (StackIO.idr)
Line 876: 3
Line 877: User input:
Line 878: 3
Line 879: Resulting stack:
Line 880: 4
Line 881: 4
Line 882: 3
Line 883: 5
Line 884: 5
Line 885: 4
Line 886: 3
Line 887: add
Line 888: 9
Line 889: 3
Line 890: add
Line 891: 12
Line 892: Figure 13.3
Line 893: How each user 
Line 894: input affects the contents of 
Line 895: the stack
Line 896: Neither GetStr nor PutStr use 
Line 897: the stack, so the height remains 
Line 898: the same.
Line 899: 
Line 900: --- 페이지 395 ---
Line 901: 369
Line 902: Dependent types in state: implementing a stack
Line 903: runStack (val :: stk) Pop = pure (val, stk)
Line 904: runStack (val :: stk) Top = pure (val, val :: stk)
Line 905: runStack stk GetStr = do x <- getLine
Line 906: pure (x, stk)
Line 907: runStack stk (PutStr x) = do putStr x
Line 908: pure ((), stk)
Line 909: runStack stk (Pure x) = pure (x, stk)
Line 910: runStack stk (x >>= f) = do (x', newStk) <- runStack stk x
Line 911: runStack newStk (f x')
Line 912: As with the vending machine, you’ll describe infinite sequences of StackCmd opera-
Line 913: tions in total functions by defining a separate StackIO type for describing infinite
Line 914: streams of stack operations. The following listing shows how you can define StackIO
Line 915: and how to run StackIO sequences, given an initial state for the stack.
Line 916: data StackIO : Nat -> Type where
Line 917: Do : StackCmd a height1 height2 ->
Line 918: (a -> Inf (StackIO height2)) -> StackIO height1
Line 919: namespace StackDo
Line 920: (>>=) : StackCmd a height1 height2 ->
Line 921: (a -> Inf (StackIO height2)) -> StackIO height1
Line 922: (>>=) = Do
Line 923: data Fuel = Dry | More (Lazy Fuel)
Line 924: partial
Line 925: forever : Fuel
Line 926: forever = More forever
Line 927: run : Fuel -> Vect height Integer -> StackIO height -> IO ()
Line 928: run (More fuel) stk (Do c f)
Line 929: = do (res, newStk) <- runStack stk c
Line 930: run fuel newStk (f res)
Line 931: run Dry stk p = pure ()
Line 932: The interactive calculator follows a similar pattern to the implementation of the vend-
Line 933: ing machine. The next listing shows an outline of the main loop, which reads an
Line 934: input, parses it into a command type, and processes the command if the input is valid.
Line 935: data StkInput = Number Integer
Line 936: | Add
Line 937: strToInput : String -> Maybe StkInput
Line 938: mutual
Line 939: tryAdd : StackIO height
Line 940: stackCalc : StackIO height
Line 941: stackCalc = do PutStr "> "
Line 942: input <- GetStr
Line 943: Listing 13.11
Line 944: Defining infinite sequences of interactive stack operations (StackIO.idr)
Line 945: Listing 13.12
Line 946: Outline of an interactive stack-based calculator (StackIO.idr)
Line 947: The Nat argument is 
Line 948: the initial height of 
Line 949: the stack for the 
Line 950: infinite sequence.
Line 951: Supports do 
Line 952: notation for 
Line 953: StackIO
Line 954: forever allows you to run a total program 
Line 955: indefinitely by giving an infinite supply of 
Line 956: Fuel. See chapter 11 for the full details.
Line 957: The input Vect must have a
Line 958: number of items given by
Line 959: the initial stack height.
Line 960: Describes possible user inputs: 
Line 961: entering a number or the add 
Line 962: Parses the input read from the console. 
Line 963: Returns Maybe because input could be invalid.
Line 964: Adds two numbers at the top of the 
Line 965: stack, if present, and then loops
Line 966: Main loop of the interactive calculator
Line 967: 
Line 968: --- 페이지 396 ---
Line 969: 370
Line 970: CHAPTER 13
Line 971: State machines: verifying protocols in types
Line 972: case strToInput input of
Line 973: Nothing => do PutStr "Invalid input\n"
Line 974: stackCalc
Line 975: Just (Number x) => do Push x
Line 976: stackCalc
Line 977: Just Add => tryAdd
Line 978: main : IO ()
Line 979: main = run forever [] stackCalc
Line 980: You still need to define strToInput, which parses user input, and tryAdd, which adds
Line 981: the two elements on the top of the stack, if possible. The following listing shows the
Line 982: definition of strToInput.
Line 983: strToInput : String -> Maybe RPNInput
Line 984: strToInput "" = Nothing
Line 985: strToInput "add" = Just Add
Line 986: strToInput x = if all isDigit (unpack x)
Line 987: then Just (Number (cast x))
Line 988: else Nothing
Line 989: Finally, the next listing shows the definition of tryAdd. Like vend and refill in the
Line 990: vending machine implementation, you need to match on the initial state to make sure
Line 991: that there are enough items on the stack to add.
Line 992: tryAdd : StackIO height
Line 993: tryAdd {height = (S (S h))}
Line 994: = do doAdd
Line 995: result <- Top
Line 996: PutStr (show result ++ "\n")
Line 997: stackCalc
Line 998: tryAdd
Line 999: = do PutStr "Fewer than two items on the stack\n"
Line 1000: stackCalc
Line 1001: You can check that stackCalc is total at the REPL:
Line 1002: *StackIO> :total stackCalc
Line 1003: Main.stackCalc is Total
Line 1004: By separating the looping component (StackIO) from the terminating component
Line 1005: (StackCmd), and by giving precise types to the operations, you can be sure that stack-
Line 1006: Calc has at least the following properties, as long as it’s total:
Line 1007: Listing 13.13
Line 1008: Reading user input for the stack-based calculator (StackIO.idr)
Line 1009: Listing 13.14
Line 1010: Adding the top two elements on the stack, if they’re present (StackIO.idr)
Line 1011: Empty input
Line 1012: is considered
Line 1013: invalid.
Line 1014: If the input is the string “add”, 
Line 1015: parse as the Add command.
Line 1016: If the input consists entirely of 
Line 1017: digits, parse as Number.
Line 1018: Adding is only valid if there are at 
Line 1019: least two elements on the stack.
Line 1020: doAdd, defined earlier, has a precondition in its 
Line 1021: type that there are two elements on the stack.
Line 1022: Inspects the top item on the stack so 
Line 1023: that you can display it as the result
Line 1024: Continues
Line 1025: with the
Line 1026: main loop
Line 1027: If the earlier case doesn’t match, there 
Line 1028: aren’t enough items on the stack to add.
Line 1029: 
Line 1030: --- 페이지 397 ---
Line 1031: 371
Line 1032: Summary
Line 1033: It will continue running indefinitely.
Line 1034: It will never crash due to user input that isn’t handled.
Line 1035: It will never crash due to a stack overflow.
Line 1036: Exercises
Line 1037: 1
Line 1038: Add user commands to the stack-based calculator for subtract and multiply. You
Line 1039: can test these as follows: 
Line 1040: *ex_13_2> :exec
Line 1041: > 5
Line 1042: > 3
Line 1043: > subtract
Line 1044: 2
Line 1045: > 8
Line 1046: > multiply
Line 1047: 16
Line 1048:  2
Line 1049: Add a negate user command to the stack-based calculator for negating the top item
Line 1050: on the stack. You can test this as follows: 
Line 1051: > 10
Line 1052: > negate
Line 1053: -10
Line 1054:  3
Line 1055: Add a discard user command that removes the top item from the stack. You can
Line 1056: test this as follows: 
Line 1057: > 3
Line 1058: > 4
Line 1059: > discard
Line 1060: Discarded 4
Line 1061: > add
Line 1062: Fewer than two items on the stack
Line 1063:  4
Line 1064: Add a duplicate user command that duplicates the top item on the stack. You can
Line 1065: test this as follows: 
Line 1066: > 2
Line 1067: > duplicate
Line 1068: Duplicated 2
Line 1069: > add
Line 1070: 4
Line 1071: 13.3
Line 1072: Summary
Line 1073: Data types can model state machines by using each data constructor to describe
Line 1074: a state transition.
Line 1075: You can describe how a command changes the state of a system by giving the
Line 1076: input and output states of the system as part of the command’s type.
Line 1077: Developing sequences of state transitions interactively, using holes, means you
Line 1078: can check the required input and output states of a sequence of commands.
Line 1079: 
Line 1080: --- 페이지 398 ---
Line 1081: 372
Line 1082: CHAPTER 13
Line 1083: State machines: verifying protocols in types
Line 1084: Types can model infinite state spaces as well as finite states.
Line 1085: Sequences of commands give verified sequences of state transitions because a
Line 1086: sequence of commands will only type-check if it describes a valid sequence of
Line 1087: state transitions.
Line 1088: You can represent mutable dependently typed state by putting the arguments to
Line 1089: the dependent type in the state transitions. For example, you can use the length
Line 1090: of a vector to represent the height of a stack.