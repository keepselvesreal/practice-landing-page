Line 1: 
Line 2: --- 페이지 399 ---
Line 3: 373
Line 4: Dependent state machines:
Line 5: handling feedback and errors
Line 6: As you saw in the previous chapter, you can describe the valid state transitions of a
Line 7: state machine in a dependent type, indexed by the required input state of an oper-
Line 8: ation (its precondition) and the output state (its postcondition). By defining valid
Line 9: state transitions in the type, you can be sure that a program that type-checks is guar-
Line 10: anteed to describe a valid sequence of state transitions.
Line 11:  You saw two examples, a description of a door and a simulation of a vending
Line 12: machine, and in each case we gave precise types to the operations to describe how
Line 13: they affected the state. But we didn’t consider the possibility that any of the opera-
Line 14: tions could fail:
Line 15: What if, when you try to open the door, it’s jammed? What if, even though
Line 16: you’ve run the Open operation, it’s still in the DoorClosed state?
Line 17: This chapter covers
Line 18: Handling errors in state transitions
Line 19: Developing protocol implementations interactively
Line 20: Guaranteeing security properties in types
Line 21: 
Line 22: --- 페이지 400 ---
Line 23: 374
Line 24: CHAPTER 14
Line 25: Dependent state machines: handling feedback and errors
Line 26: What if, when you insert a coin in the vending machine, the machine rejects the
Line 27: coin?
Line 28: In almost any realistic setting, when you try to give precise types to describe a state
Line 29: machine, you’ll need to consider the possibility of the operation failing, or of an unex-
Line 30: pected response:
Line 31: Like the DoorState, you might represent the state of a file handle (open or
Line 32: closed) in a type, but if you try to open a file, the file might not exist or you
Line 33: might not have permission to open it.
Line 34: You might represent a secure communication protocol in a state machine, but
Line 35: whether you can progress in the protocol depends on receiving valid responses
Line 36: from the network to any request you send.
Line 37: You might represent the state of a bank’s automated teller machine (ATM) in a
Line 38: type (waiting for a card, waiting for PIN entry, and so on), but you can only
Line 39: move to a state where the machine can dispense cash if checking the user’s PIN
Line 40: is successful.
Line 41: In these cases, you’re not in complete control of how the system state changes. You
Line 42: can request a change in the state (opening a file, sending a message, and so on) but
Line 43: whether and how the state changes in practice depends on the response you receive
Line 44: from the environment. In this chapter, you’ll see how to deal with the possibility of an
Line 45: operation failing by allowing a state transition to depend on the result of an operation.
Line 46:  You’ll also see how to deal with state changes that might depend on user input—
Line 47: we’ll look at the state transitions involved in modeling an ATM, where user input
Line 48: determines whether the machine can dispense cash. We’ll begin by revisiting the
Line 49: model of the door from chapter 13 and see how to deal with the possibility that the
Line 50: door might jam, so the Open operation fails.
Line 51: 14.1
Line 52: Dealing with errors in state transitions
Line 53: In the previous chapter, you defined a DoorCmd data type for modeling state transi-
Line 54: tions on a door, as illustrated by the state transition diagram in figure 14.1.
Line 55:  Listing 14.1 recaps the definition of DoorCmd, which models the state transition sys-
Line 56: tem in figure 14.1.
Line 57: DoorOpen
Line 58: DoorClosed
Line 59: Open
Line 60: RingBell
Line 61: Close
Line 62: Figure 14.1
Line 63: A state transition 
Line 64: diagram showing the states and 
Line 65: operations on a door
Line 66: 
Line 67: --- 페이지 401 ---
Line 68: 375
Line 69: Dealing with errors in state transitions
Line 70:  
Line 71: data DoorState = DoorClosed | DoorOpen
Line 72: data DoorCmd : Type -> DoorState -> DoorState -> Type where
Line 73: Open : DoorCmd
Line 74: () DoorClosed DoorOpen
Line 75: Close : DoorCmd
Line 76: () DoorOpen
Line 77: DoorClosed
Line 78: RingBell : DoorCmd () DoorClosed DoorClosed
Line 79: Pure : ty -> DoorCmd ty state state
Line 80: (>>=) : DoorCmd a state1 state2 ->
Line 81: (a -> DoorCmd b state2 state3) ->
Line 82: DoorCmd b state1 state3
Line 83: In this model, you’re in complete control of how each operation moves from one state
Line 84: to another. For example, the type of Open states that it always starts with a door in the
Line 85: DoorClosed state, and it always ends with a door in the DoorOpen state:
Line 86: Open : DoorCmd () DoorClosed DoorOpen
Line 87: Reality is not always so accommodating, however! If you were to implement this with
Line 88: some real hardware, such as a sliding door operated by pressing a button, you’d need
Line 89: to consider the possibility of hardware problems such as the door jamming. In this sec-
Line 90: tion, we’ll refine the door model to capture this possibility of failure, and see how this
Line 91: affects the implementation of programs that follow the protocol.
Line 92: 14.1.1 Refining the door model: representing failure
Line 93: Open could fail due to the door being jammed, so we need a way to represent whether
Line 94: it was successful. We could define an enumeration type to describe the possible results
Line 95: of opening the door:
Line 96: data DoorResult = OK | Jammed
Line 97: Then, instead of producing the unit value, Open could return a DoorResult. We might
Line 98: try the following type for Open:
Line 99: Open : DoorCmd DoorResult DoorClosed DoorOpen
Line 100: Unfortunately, this isn’t quite right because it still says that opening the door causes
Line 101: the door to be in the DoorOpen state, whatever happens. Somehow, we need to express
Line 102: that Open causes the door to be in either the DoorClosed or DoorOpen state, depend-
Line 103: ing on the value of the DoorResult it produces. Figure 14.2 illustrates the state
Line 104: machine we’d like to implement.
Line 105: Listing 14.1
Line 106: Modeling the door state machine in a type
Line 107: 
Line 108: --- 페이지 402 ---
Line 109: 376
Line 110: CHAPTER 14
Line 111: Dependent state machines: handling feedback and errors
Line 112:  
Line 113: You can achieve this by changing the type of DoorCmd to allow the output state to be
Line 114: calculated from the return value. Figure 14.3 illustrates how you can refine the type of
Line 115: DoorCmd to achieve this.
Line 116: Here, you’ve given a name to the return type of the operation, ty, and said that the
Line 117: output state is computed by a function that takes a ty as an input. Now, when you
Line 118: define the type of Open (and indeed all of the DoorCmd operations), you give an expres-
Line 119: sion for the output state, explaining how the output state is computed from the return
Line 120: value, of type DoorResult:
Line 121: Open : DoorCmd DoorResult DoorClosed
Line 122: (\res => case res of
Line 123: OK => DoorOpen
Line 124: Jammed => DoorClosed)
Line 125: This encodes exactly what the state transition diagram in figure 14.2 illustrates. That
Line 126: is, the output state of Open can be one of the following: 
Line 127: 
Line 128: DoorOpen—If Open returns OK
Line 129: 
Line 130: DoorClosed—If Open returns Jammed
Line 131: Although you won’t know the value of res until you run the operation, you can at least
Line 132: use the type to explain the possible states the door will be in given the result of Open.
Line 133: Listing 14.2 shows the complete DoorCmd type declaration after this refinement. It also
Line 134: adds Display, so you can display logging messages if necessary.
Line 135: DoorOpen
Line 136: DoorClosed
Line 137: Open(OK)
Line 138: RingBell
Line 139: Open(Jammed)
Line 140: Close
Line 141: Figure 14.2
Line 142: A state transition diagram 
Line 143: showing the states and operations on a 
Line 144: door, where opening the door might fail
Line 145: data DoorCmd : (ty : Type) -> DoorState -> (ty -> DoorState)
Line 146: Result of the
Line 147: operation
Line 148: Input state
Line 149: Output state calculated from
Line 150: the result of the operation
Line 151: Figure 14.3
Line 152: New type for DoorCmd, where the output state of an operation 
Line 153: is computed from the return value of the operation
Line 154: 
Line 155: --- 페이지 403 ---
Line 156: 377
Line 157: Dealing with errors in state transitions
Line 158:  
Line 159: data DoorCmd : (ty : Type) -> DoorState -> (ty -> DoorState) -> Type where
Line 160: Open : DoorCmd DoorResult DoorClosed
Line 161: (\res => case res of
Line 162: OK => DoorOpen
Line 163: Jammed => DoorClosed)
Line 164: Close : DoorCmd () DoorOpen (const DoorClosed)
Line 165: RingBell : DoorCmd () DoorClosed (const DoorClosed)
Line 166: Display : String -> DoorCmd () state (const state)
Line 167: Pure : (res : ty) -> DoorCmd ty (state_fn res) state_fn
Line 168: (>>=) : DoorCmd a state1 state2_fn ->
Line 169: ((res : a) -> DoorCmd b (state2_fn res) state3_fn) ->
Line 170: DoorCmd b state1 state3_fn
Line 171: In the previous definition of DoorCmd, in listing 14.1, you used the (>>=) operator to
Line 172: explain that the output state of the first operation should be the input state of the
Line 173: second:
Line 174: (>>=) : DoorCmd a state1 state2 -> (a -> DoorCmd b state2 state3) ->
Line 175: DoorCmd b state1 state3
Line 176: It’s now slightly more complicated, because the return value of the first operation
Line 177: affects the input state of the second:
Line 178: (>>=) : DoorCmd a state1 state2_fn ->
Line 179: ((res : a) -> DoorCmd b (state2_fn res) state3_fn) ->
Line 180: DoorCmd b state1 state3_fn
Line 181: Listing 14.2
Line 182: The refined DoorCmd type, allowing the output state of each operation to
Line 183: be computed from the return value of the operation (DoorJam.idr)
Line 184: Calculates the output state from 
Line 185: the return value of Open
Line 186: You use const to say that the output state
Line 187: is not dependent on the return value.
Line 188: This type for Pure means that the value 
Line 189: res can be used to compute the output 
Line 190: state of a sequence of operations.
Line 191: The (>>=) operator needs 
Line 192: to compute the intermediate 
Line 193: state from the output of the 
Line 194: first operation.
Line 195: Calculating output state with const
Line 196: This is the type of const, defined in the Prelude:
Line 197: *DoorJam> :t const
Line 198: const : a -> b -> a
Line 199: It ignores its second argument and returns its first. So, if you say const Door-
Line 200: Closed for the output state of an operation, that gives you a function that ignores
Line 201: the result of the function and always returns DoorClosed.
Line 202: 
Line 203: --- 페이지 404 ---
Line 204: 378
Line 205: CHAPTER 14
Line 206: Dependent state machines: handling feedback and errors
Line 207: This works as follows: 
Line 208: 1
Line 209: The first operation returns a value of type a, and the output state is computed
Line 210: from a state2_fn function once you know the result of the operation.
Line 211:  2
Line 212: When you come to the second operation, you’ll know the result of the first
Line 213: operation, named res, so it has an input state of state2_fn res.
Line 214: 3
Line 215: The combined operation has an input state of state1 (the input state of the
Line 216: first operation) and an output state computed from the result of the second
Line 217: operation, using state3_fn.
Line 218: Defining DoorCmd this way gives you more precision in defining the state transitions,
Line 219: and it means that when you define functions using DoorCmd, the types of the opera-
Line 220: tions require you to execute any necessary checks before continuing. For example,
Line 221: after you try to Open a door, you can’t execute any further door operations until you’ve
Line 222: checked the result. We’ll look at how this works by revisiting our earlier example,
Line 223: doorProg. 
Line 224: 14.1.2 A verified, error-checking, door-protocol description
Line 225: In chapter 13, you implemented a function using DoorCmd as a sequence of actions to
Line 226: ring the bell, and open and then close the door, and you used the types to verify that
Line 227: the sequence of actions was valid. You wrote doorProg as follows:
Line 228: doorProg : DoorCmd () DoorClosed DoorClosed
Line 229: doorProg = do RingBell
Line 230: Open
Line 231: Close
Line 232: Now that you’ve refined the type of DoorCmd so that the output state is computed from
Line 233: the result of the operation, you’ll need to write the type differently:
Line 234: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 235: That is, the output state isn’t affected by the result, so you use const, which ignores its
Line 236: second argument and returns its first unchanged. But if you try implementing door-
Line 237: Prog as before, without checking the result of Open, you’ll get an error:
Line 238: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 239: doorProg = do RingBell
Line 240: Open
Line 241: Close
Line 242: The error happens when you try to use Close. Its type requires that the input state is
Line 243: DoorOpen, but in fact its input state is computed from the result of Open:
Line 244: When checking an application of constructor Main.>>=:
Line 245: Type mismatch between
Line 246: DoorCmd () DoorOpen (const DoorClosed) (Type of Close)
Line 247: and
Line 248: DoorCmd ()
Line 249: ((\res =>
Line 250: 
Line 251: --- 페이지 405 ---
Line 252: 379
Line 253: Dealing with errors in state transitions
Line 254: case res of
Line 255: OK => DoorOpen
Line 256: Jammed => DoorClosed) _)
Line 257: (\value => DoorClosed) (Expected type)
Line 258: To see how to avoid this problem, you can develop doorProg interactively, beginning
Line 259: from the following point: 
Line 260: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 261: doorProg = do RingBell
Line 262: Open
Line 263: ?doorProg_rhs
Line 264: DEBUGGING TYPE ERRORS USING HOLES
Line 265: If you get a type error that’s hard to
Line 266: understand on its own, it’s often a good idea to replace the offending part of
Line 267: the program with a hole (as we did by replacing Close with ?door-
Line 268: Prog_rhs), to see what the expected type is, along with any local variables in
Line 269: scope.
Line 270: 1
Line 271: Type, refine—If you check the type of ?doorProg_rhs, you’ll see this: 
Line 272: --------------------------------------
Line 273: doorProg_rhs : DoorCmd ()
Line 274: (case _ of
Line 275: OK => DoorOpen
Line 276: Jammed => DoorClosed)
Line 277: (\value => DoorClosed)
Line 278: The output state you see here arises from the definition of const in the Pre-
Line 279: lude, and it’s a function that ignores its argument value and returns Door-
Line 280: Closed. The input state you’re looking for is calculated from some value, _.
Line 281: This value is the result of Open, which you haven’t named. Let’s call it jam: 
Line 282: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 283: doorProg = do RingBell
Line 284: jam <- Open
Line 285: ?doorProg_rhs
Line 286:  2
Line 287: Type—You’ll now see that the input state of the next operation is calculated
Line 288: from the value of jam: 
Line 289: jam : DoorResult
Line 290: --------------------------------------
Line 291: doorProg_rhs : DoorCmd ()
Line 292: (case jam of
Line 293: OK => DoorOpen
Line 294: Jammed => DoorClosed)
Line 295: (\value => DoorClosed)
Line 296:  3
Line 297: Define, type—Because the input state depends on the value of jam, you can make
Line 298: progress by inspecting the value of jam: 
Line 299: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 300: doorProg = do RingBell
Line 301: jam <- Open
Line 302: 
Line 303: --- 페이지 406 ---
Line 304: 380
Line 305: CHAPTER 14
Line 306: Dependent state machines: handling feedback and errors
Line 307: case jam of
Line 308: case_val => ?doorProg_rhs
Line 309: You’ll now see that the input state depends on the value of case_val: 
Line 310: case_val : DoorResult
Line 311: jam : DoorResult
Line 312: --------------------------------------
Line 313: doorProg_rhs : DoorCmd ()
Line 314: (case case_val of
Line 315: OK => DoorOpen
Line 316: Jammed => DoorClosed)
Line 317: (\value => DoorClosed)
Line 318:  4
Line 319: Define, type—If you case-split on case_val, you should see that each branch of
Line 320: the case has a different type, calculated from the specific value of case_val: 
Line 321: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 322: doorProg = do RingBell
Line 323: jam <- Open
Line 324: case jam of
Line 325: OK => ?doorProg_rhs_1
Line 326: Jammed => ?doorProg_rhs_2
Line 327: In ?doorProg_rhs_1, for example, jam has the value OK, so the door must have
Line 328: successfully opened: 
Line 329: jam : DoorResult
Line 330: --------------------------------------
Line 331: doorProg_rhs_1 : DoorCmd () DoorOpen (\value => DoorClosed)
Line 332: In ?doorProg_rhs_2, on the other hand, the door is jammed, so it’s still in the
Line 333: DoorClosed state: 
Line 334: jam : DoorResult
Line 335: --------------------------------------
Line 336: doorProg_rhs_2 : DoorCmd () DoorClosed (\value => DoorClosed)
Line 337: 5
Line 338: Refine—To complete the definition, you can display a log message in each case,
Line 339: and if the door is open, close it again: 
Line 340: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 341: doorProg = do RingBell
Line 342: jam <- Open
Line 343: case jam of
Line 344: OK => do Display "Glad To Be Of Service"
Line 345: Close
Line 346: Jammed => Display "Door Jammed"
Line 347: The type of Open means that you need to check the state of the door before you exe-
Line 348: cute any further operations that need to know the door’s state. In particular, you can’t
Line 349: Close the door unless you’ve successfully opened it. You don’t have to check immedi-
Line 350: ately, though. For example, you can display a message between opening the door and
Line 351: checking the result:
Line 352: 
Line 353: --- 페이지 407 ---
Line 354: 381
Line 355: Dealing with errors in state transitions
Line 356: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 357: doorProg = do RingBell
Line 358: jam <- Open
Line 359: Display "Trying to open the door"
Line 360: case jam of
Line 361: OK => do Display "Glad To Be Of Service"
Line 362: Close
Line 363: Jammed => Display "Door Jammed"
Line 364: This is valid, because the precondition on Display doesn’t require the door to be in a
Line 365: specific state; any will do, and Display won’t change the state.
Line 366:  Using pattern-matching bindings, which you first saw in chapter 5, you can also
Line 367: define doorProg more concisely, as follows:
Line 368: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 369: doorProg = do RingBell
Line 370: OK <- Open | Jammed => Display "Door Jammed"
Line 371: Display "Glad To Be Of Service"
Line 372: Close
Line 373: This gives a default path through the sequence of actions, when Open returns OK, and
Line 374: an alternative action when Open returns Jammed. Using pattern-matching bindings
Line 375: makes it easier to write longer sequences of actions, where some of the actions might
Line 376: fail. For example, you can open and close the door twice and abandon the sequence if
Line 377: either fails:
Line 378: doorProg : DoorCmd () DoorClosed (const DoorClosed)
Line 379: doorProg = do RingBell
Line 380: OK <- Open | Jammed => Display "Door Jammed"
Line 381: Display "Glad To Be Of Service"
Line 382: Close
Line 383: OK <- Open | Jammed => Display "Door Jammed"
Line 384: Display "Glad To Be Of Service"
Line 385: Close
Line 386: This example describes a protocol in the type, and it explicitly says where an operation
Line 387: might fail. In doorProg, the type of Open means that you need to check its result
Line 388: before you can proceed with any further operations that change the state.
Line 389: The type of Pure
Line 390: The type of Pure in DoorCmd allows you to define functions like the following, where
Line 391: the call to Pure changes the state:
Line 392: logOpen : DoorCmd DoorResult DoorClosed
Line 393: (\res => case res of
Line 394: OK => DoorOpen
Line 395: Jammed => DoorClosed)
Line 396: logOpen = do Display "Trying to open the door"
Line 397: OK <- Open | Jammed => do Display "Jammed"
Line 398: Pure Jammed
Line 399: Display "Success"
Line 400: Pure OK
Line 401: 
Line 402: --- 페이지 408 ---
Line 403: 382
Line 404: CHAPTER 14
Line 405: Dependent state machines: handling feedback and errors
Line 406: You now have a definition of DoorCmd that precisely describes the protocol for open-
Line 407: ing and closing doors, capturing the possibility of failure. But you haven’t yet seen
Line 408: how the corresponding run function works, which is where the result of an Open oper-
Line 409: ation would be produced in practice. We’ll look at this next, in the context of a larger
Line 410: example: an ATM. We’ll also look at how state can change according to user input. 
Line 411: 14.2
Line 412: Security properties in types: modeling an ATM
Line 413: You can use explicit states in the types of operations to guarantee, by type checking,
Line 414: that a system will only execute security-critical operations when it’s in a valid state to
Line 415: do so. For example, an ATM should only dispense cash when a user has inserted their
Line 416: card and entered a correct PIN. This is a typical sequence of operations on an ATM:
Line 417: 1
Line 418: A user inserts their bank card.
Line 419:  2
Line 420: The machine prompts the user for their PIN, to check that the user is entitled to
Line 421: use the card.
Line 422: 3
Line 423: If PIN entry is successful, the machine prompts the user for an amount of
Line 424: money, and then dispenses cash.
Line 425: If the user enters the correct PIN, the machine will be in a state to dispense cash; oth-
Line 426: erwise, it won’t be. In this section, we’ll define a model for an ATM and see how to
Line 427: change the state of the machine, in its type, based on user input.
Line 428: SECURITY PROPERTY OF THE ATM
Line 429: In this model, we’ll omit some of the finer
Line 430: details of banking, such as accessing and updating the user’s bank account, and
Line 431: checking the PIN securely, which would be done with separate state machines.
Line 432: We’ll focus on one important security property we want to maintain: the
Line 433: machine must only dispense cash when there is a validated card in the machine.
Line 434: As with the door model, we’ll begin by defining the possible states of the ATM and
Line 435: the operations that can change the ATM’s state. Once we know how the operations
Line 436: (continued)
Line 437: If you replace the last line, Pure OK, with a hole, ?pure_ok, you’ll see that it has
Line 438: an input state of DoorOpen, and the output state (of the entire logOpen function)
Line 439: needs to be a function that computes its output state:
Line 440: pure_ok : DoorCmd DoorResult DoorOpen
Line 441: (\res => case res of
Line 442: OK => DoorOpen
Line 443: Jammed => DoorClosed)
Line 444: The type of Pure is designed to work in this situation:
Line 445: Pure : (res : ty) -> DoorCmd ty (state_fn res) state_fn
Line 446: Here, state_fn is the function containing the case block, and Pure must take OK
Line 447: as an argument to have the correct input state for ?pure_ok.
Line 448: 
Line 449: --- 페이지 409 ---
Line 450: 383
Line 451: Security properties in types: modeling an ATM
Line 452: affect the state, we can define a data type for representing the operations on the
Line 453: machine.
Line 454: 14.2.1 Defining states for the ATM
Line 455: An ATM is either waiting for a user to begin an interaction, waiting for the user to
Line 456: enter their PIN, or ready to dispense cash after validating a PIN. So an ATM, in our
Line 457: model, can be in one of the following states:
Line 458: 
Line 459: Ready—The ATM is ready and waiting for a card to be inserted.
Line 460: 
Line 461: CardInserted—There is a card inside the ATM, but the system has not yet
Line 462: checked a PIN entry against the card.
Line 463: 
Line 464: Session—There is a card inside the ATM and the user has entered a valid PIN
Line 465: for the card, so a validated session is in progress.
Line 466: We’ll validate the card by checking that the user inputs a correct PIN. In the vending
Line 467: machine in chapter 13, you also had to check that an input was valid, but in that case
Line 468: you could check the command locally. Here, we’ll assume that there’s an external ser-
Line 469: vice to check the PIN, so we won’t know until runtime which inputs will result in
Line 470: which states.
Line 471:  The machine supports the following basic operations, each of which may have pre-
Line 472: conditions and postconditions on the state of the machine:
Line 473: 
Line 474: InsertCard—Waits for a user to insert a card
Line 475: 
Line 476: EjectCard—Ejects a card from the machine, as long as there’s a card in the
Line 477: machine
Line 478: 
Line 479: GetPIN—Reads a user’s PIN, as long as there’s a card in the machine
Line 480: 
Line 481: CheckPIN—Checks whether an entered PIN is valid
Line 482: 
Line 483: Dispense—Dispenses cash as long as there’s a validated card in the machine
Line 484: 
Line 485: GetAmount—Reads from the user an amount to dispense
Line 486: 
Line 487: Message—Displays a message to the user
Line 488: Figure 14.4 illustrates how these operations affect the state of the machine.
Line 489: CardInserted
Line 490: Session
Line 491: Ready
Line 492: EjectCard
Line 493: Dispense
Line 494: GetPIN,
Line 495: CheckPIN (Incorrect)
Line 496: InsertCard
Line 497: EjectCard
Line 498: CheckPIN (Correct)
Line 499: Figure 14.4
Line 500: A state machine describing the states and operations on an ATM. This omits 
Line 501: operations (such as GetAmount) that are valid in all states.
Line 502: 
Line 503: --- 페이지 410 ---
Line 504: 384
Line 505: CHAPTER 14
Line 506: Dependent state machines: handling feedback and errors
Line 507: Having defined the states and seen how the high-level operations that the machine
Line 508: performs can affect the states, we’re now in a position to define a type for the ATM
Line 509: that describes the state transitions illustrated in figure 14.4. 
Line 510: 14.2.2 Defining a type for the ATM
Line 511: Listing 14.3 defines an ATMCmd type that represents the state transitions of operations
Line 512: on an ATM in Idris code. It also includes GetAmount and Message, which are valid in all
Line 513: states and don’t affect the state, and the usual operations Pure and (>>=). The type of
Line 514: EjectCard is slightly simplified; we’ll refine this in section 14.2.4.
Line 515: import Data.Vect
Line 516: PIN : Type
Line 517: PIN = Vect 4 Char
Line 518: data ATMState = Ready | CardInserted | Session
Line 519: data PINCheck = CorrectPIN | IncorrectPIN
Line 520: data ATMCmd : (ty : Type) -> ATMState -> (ty -> ATMState) -> Type where
Line 521: InsertCard : ATMCmd ()
Line 522: Ready
Line 523: (const CardInserted)
Line 524: EjectCard
Line 525: : ATMCmd ()
Line 526: state
Line 527: (const Ready)
Line 528: GetPIN
Line 529: : ATMCmd PIN
Line 530: CardInserted (const CardInserted)
Line 531: CheckPIN
Line 532: : PIN -> ATMCmd PINCheck CardInserted
Line 533: (\check => case check of
Line 534: CorrectPIN => Session
Line 535: IncorrectPIN => CardInserted)
Line 536: GetAmount : ATMCmd Nat state (const state)
Line 537: Dispense : (amount : Nat) -> ATMCmd () Session (const Session)
Line 538: Message : String -> ATMCmd () state (const state)
Line 539: Pure
Line 540: : (res : ty) -> ATMCmd ty (state_fn res) state_fn
Line 541: (>>=) : ATMCmd a state1 state2_fn ->
Line 542: ((res : a) -> ATMCmd b (state2_fn res) state3_fn) ->
Line 543: ATMCmd b state1 state3_fn
Line 544: Using ATMCmd, you can write a function that describes a session on an ATM, from the
Line 545: user inserting a card to the machine dispensing cash. Listing 14.4 shows the begin-
Line 546: ning of an atm function that waits for a user to insert a card, prompts for a PIN, and
Line 547: then checks the result. I’ve left a hole for the rest of the sequence, in which we’ll
Line 548: check the PIN and dispense cash if the PIN is valid.
Line 549: Listing 14.3
Line 550: A type for representing the commands of an ATM, and how they affect the
Line 551: ATM’s state (ATM.idr)
Line 552: A PIN is
Line 553: exactly four
Line 554: characters.
Line 555: The possible
Line 556: states of the ATM
Line 557: The possible results 
Line 558: of checking a PIN: 
Line 559: valid or invalid
Line 560: This isn’t quite right, because it allows the 
Line 561: card to be ejected even if there’s no card 
Line 562: in the machine. We’ll refine it shortly.
Line 563: The machine will only
Line 564: dispense money if there’s a
Line 565: validated card in the machine.
Line 566: Only moves to the Session state
Line 567: if the PIN check succeeds
Line 568: 
Line 569: --- 페이지 411 ---
Line 570: 385
Line 571: Security properties in types: modeling an ATM
Line 572:   
Line 573: atm : ATMCmd () Ready (const Ready)
Line 574: atm = do InsertCard
Line 575: pin <- GetPIN
Line 576: pinOK <- CheckPIN pin
Line 577: ?atm_rhs
Line 578: You can complete atm as follows:
Line 579: 1
Line 580: Type, define —If you check the type of the ?atm_rhs hole, you’ll see that you
Line 581: begin in a state that depends on the value of pinOK, and you need to end in the
Line 582: Ready state: 
Line 583: pin : Vect 4 Char
Line 584: pinOK : PINCheck
Line 585: --------------------------------------
Line 586: atm_rhs : ATMCmd ()
Line 587: (case pinOK of
Line 588: CorrectPIN => Session
Line 589: IncorrectPIN => CardInserted)
Line 590: (\value => Ready)
Line 591: The type here suggests you can proceed by checking the value of pinOK: 
Line 592: atm : ATMCmd () Ready (const Ready)
Line 593: atm = do InsertCard
Line 594: pin <- GetPIN
Line 595: pinOK <- CheckPIN pin
Line 596: case pinOK of
Line 597: CorrectPIN => ?atm_rhs_1
Line 598: IncorrectPIN => ?atm_rhs_2
Line 599:  2
Line 600: Type—If you check ?atm_rhs_1 and ?atm_rhs_2, you’ll see that the state is dif-
Line 601: ferent in each case. In ?atm_rhs_1, the PIN was found to be valid, so you have a
Line 602: validated session: 
Line 603: pinOK : PINCheck
Line 604: pin : Vect 4 Char
Line 605: --------------------------------------
Line 606: atm_rhs_1 : ATMCmd () Session (\value => Ready)
Line 607: In ?atm_rhs_2, on the other hand, the PIN was found to be invalid, so you’re
Line 608: still in the CardInserted state: 
Line 609: pinOK : PINCheck
Line 610: pin : Vect 4 Char
Line 611: --------------------------------------
Line 612: atm_rhs_2 : ATMCmd () CardInserted (\value => Ready)
Line 613:  3
Line 614: Refine—In ?atm_rhs_1, you can now dispense cash, so you can prompt for an
Line 615: amount and dispense that: 
Line 616: case pinOK of
Line 617: CorrectPIN => do cash <- GetAmount
Line 618: Dispense cash
Line 619: Listing 14.4
Line 620: An atm function describing a sequence of operations on an ATM (ATM.idr)
Line 621: Checks whether the PIN is valid. 
Line 622: The next state of the machine 
Line 623: depends on the value of pinOK.
Line 624: 
Line 625: --- 페이지 412 ---
Line 626: 386
Line 627: CHAPTER 14
Line 628: Dependent state machines: handling feedback and errors
Line 629: ?atm_rhs_1
Line 630: IncorrectPIN => ?atm_rhs_2
Line 631:  4
Line 632: Type, refine—The input state of ?atm_rhs_1 is still Session, so before you finish
Line 633: you need to get back to the Ready state: 
Line 634: pin : Vect 4 Char
Line 635: pinOK : PINCheck
Line 636: cash : Nat
Line 637: --------------------------------------
Line 638: atm_rhs_1 : ATMCmd () Session (\value => Ready)
Line 639: You can achieve this by ejecting the card: 
Line 640: case pinOK of
Line 641: CorrectPIN => do cash <- GetAmount
Line 642: Dispense cash
Line 643: EjectCard
Line 644: IncorrectPIN => ?atm_rhs_2
Line 645: 5
Line 646: Refine—For ?atm_rhs_2, the PIN was invalid, so the simplest thing to do is eject
Line 647: the card, leading to the following completed definition: 
Line 648: atm : ATMCmd () Ready (const Ready)
Line 649: atm = do InsertCard
Line 650: pin <- GetPIN
Line 651: pinOK <- CheckPIN pin
Line 652: case pinOK of
Line 653: CorrectPIN => do cash <- GetAmount
Line 654: Dispense cash
Line 655: EjectCard
Line 656: IncorrectPIN => EjectCard
Line 657: There are other ways you could define atm. For example, it would be helpful to dis-
Line 658: play messages to the user. Also, in practice, ATMs typically don’t check the PIN until
Line 659: just before dispensing cash. The next listing shows this alternative way of implement-
Line 660: ing atm.
Line 661: atm : ATMCmd () Ready (const Ready)
Line 662: atm = do InsertCard
Line 663: pin <- GetPIN
Line 664: cash <- GetAmount
Line 665: pinOK <- CheckPIN pin
Line 666: Message "Checking Card"
Line 667: case pinOK of
Line 668: CorrectPIN => do Dispense cash
Line 669: EjectCard
Line 670: Message "Please remove your card and cash"
Line 671: IncorrectPIN => do Message "Incorrect PIN"
Line 672: EjectCard
Line 673: Listing 14.5
Line 674: An alternative implementation of atm, including messages to the user and
Line 675: checking the PIN later (ATM.idr)
Line 676: You haven’t checked the PIN yet, or the 
Line 677: state of pinOK, but these commands are 
Line 678: valid because they don’t require the 
Line 679: machine to be in a specific state.
Line 680: 
Line 681: --- 페이지 413 ---
Line 682: 387
Line 683: Security properties in types: modeling an ATM
Line 684: As long as you only execute actions when the machine is in the appropriate state, and as
Line 685: long as you make sure that every path through the actions in atm ends in the Ready state,
Line 686: you can implement the details however you like. If atm type-checks, you can be certain
Line 687: that you’ve maintained the important security property: the machine will only dispense
Line 688: cash when there’s a card in the machine and the PIN has been entered correctly. 
Line 689: 14.2.3 Simulating an ATM at the console: executing ATMCmd
Line 690: To try the atm function, you can write a console simulation of an ATM that produces
Line 691: IO actions for an ATMCmd description:
Line 692: runATM : ATMCmd res inState outState_fn -> IO res
Line 693: Given a sequence of ATMCmd that produces a result of type res, begins in state inState,
Line 694: and computes the result state with outState_fn, runATM gives a sequence of IO actions
Line 695: that produces a result, res. Let’s hardcode a single valid PIN for this simulation:
Line 696: testPIN : Vect 4 Char
Line 697: testPIN = ['1', '2', '3', '4']
Line 698: The following listing shows a console simulation of an ATM that uses this hardcoded
Line 699: PIN. In this simulation, many of the commands prompt for an input on the console
Line 700: and return the value read.
Line 701: readVect : (n : Nat) -> IO (Vect n Char)
Line 702: readVect Z = do discard <- getLine
Line 703: pure []
Line 704: readVect (S k) = do ch <- getChar
Line 705: chs <- readVect k
Line 706: pure (ch :: chs)
Line 707: runATM : ATMCmd res inState outState_fn -> IO res
Line 708: runATM InsertCard = do putStrLn "Please insert your card (press enter)"
Line 709: x <- getLine
Line 710: pure ()
Line 711: runATM EjectCard = putStrLn "Card ejected"
Line 712: runATM GetPIN = do putStr "Enter PIN: "
Line 713: readVect 4
Line 714: runATM (CheckPIN pin) = if pin == testPIN
Line 715: then pure CorrectPIN
Line 716: else pure IncorrectPIN
Line 717: runATM GetAmount = do putStr "How much would you like? "
Line 718: x <- getLine
Line 719: pure (cast x)
Line 720: runATM (Dispense amount) = putStrLn ("Here is " ++ show amount)
Line 721: runATM (Message msg) = putStrLn msg
Line 722: runATM (Pure res) = pure res
Line 723: runATM (x >>= f) = do x' <- runATM x
Line 724: runATM (f x')
Line 725: Listing 14.6
Line 726: A console simulation of an ATM (ATM.idr)
Line 727: readVect reads a line, keeping 
Line 728: the prefix of a specific length 
Line 729: and discarding the rest.
Line 730: Simulates waiting for a card to be 
Line 731: inserted by waiting for any input
Line 732: Checks the given pin 
Line 733: against the hardcoded 
Line 734: PIN. The value returned 
Line 735: here determines the new 
Line 736: state of the machine.
Line 737: 
Line 738: --- 페이지 414 ---
Line 739: 388
Line 740: CHAPTER 14
Line 741: Dependent state machines: handling feedback and errors
Line 742: You’ve now defined the ATM as a type, with commands describing each of the state
Line 743: transitions on the ATM, and a separate runATM function that interprets those com-
Line 744: mands in the IO context. By separating the description from the implementation, you
Line 745: can write different interpreters for different contexts, as required. In particular, you
Line 746: wouldn’t want to hardcode a PIN on a real device! 
Line 747: 14.2.4 Refining preconditions using auto-implicits
Line 748: One feature of the state machine in figure 14.4 that ATMCmd type doesn’t quite capture
Line 749: is that ejecting the card should only be allowed when there’s a card in the machine.
Line 750: Instead, you have the following type:
Line 751: EjectCard : ATMCmd () state (const Ready)
Line 752: That is, you can try to eject a card in any input state, even when there’s no card in the
Line 753: machine. But there are only two states when it’s okay to eject a card: CardInserted
Line 754: and Session. You shouldn’t be able to write the following function, because the
Line 755: machine is ejecting a card in the Ready state:
Line 756: badATM : ATMCmd () Ready (const Ready)
Line 757: badATM = EjectCard
Line 758: Somehow, you need both of the following types to work for EjectCard:
Line 759: EjectCard : ATMCmd () CardInserted (const Ready)
Line 760: EjectCard : ATMCmd () Session
Line 761: (const Ready)
Line 762: A data constructor like EjectCard can’t have two different types. You can, however,
Line 763: define a predicate on ATMState that will allow you to restrict the possible input states of
Line 764: EjectCard to those that are valid. We discussed predicates in chapter 9, and you can
Line 765: define a HasCard predicate that describes the states in which a machine contains a card:
Line 766: data HasCard : ATMState -> Type where
Line 767: HasCI
Line 768: : HasCard CardInserted
Line 769: HasSession : HasCard Session
Line 770: You can only construct a value of type HasCard state when state is one of Card-
Line 771: Inserted or Session, so you can refine the type of EjectCard as follows:
Line 772: EjectCard
Line 773: : HasCard state -> ATMCmd () state (const Ready)
Line 774: If you do this, you’ll need to give values of type HasCard explicitly when using Eject-
Line 775: Card. For example:
Line 776: insertEject : ATMCmd () Ready (const Ready)
Line 777: insertEject = do InsertCard
Line 778: EjectCard HasCI
Line 779: Having to write explicit values for the predicate will get tedious very quickly. Instead,
Line 780: you can use an auto implicit for the predicate, which you also saw in chapter 9:
Line 781: EjectCard
Line 782: : {auto prf : HasCard state} -> ATMCmd () state (const Ready)
Line 783: 
Line 784: --- 페이지 415 ---
Line 785: 389
Line 786: Security properties in types: modeling an ATM
Line 787: Now, you can use EjectCard as before, and let Idris find the correct value for the
Line 788: predicate by searching through the possible data constructors for HasCard to see if
Line 789: any of them are valid:
Line 790: insertEject : ATMCmd () Ready (const Ready)
Line 791: insertEject = do InsertCard
Line 792: EjectCard
Line 793: For badATM, Idris shouldn’t be able to find a suitable value:
Line 794: badATM : ATMCmd () Ready (const Ready)
Line 795: badATM = EjectCard
Line 796: In this case, Idris will report an error, saying that it needs to find a value of type HasCard
Line 797: Ready for the predicate to EjectCard, but it can’t find one:
Line 798: When checking argument prf to constructor Main.EjectCard:
Line 799: Can't find a value of type
Line 800: HasCard Ready
Line 801: All of your other previous definitions, including the two versions of atm and the exe-
Line 802: cution function runATM, will work without any alteration using this refined version of
Line 803: EjectCard. 
Line 804: Exercises
Line 805: 1
Line 806: The following type outlines a security system in which a user can log in with a pass-
Line 807: word and then read a secret message, although there are some gaps: 
Line 808: data Access = LoggedOut | LoggedIn
Line 809: data PwdCheck = Correct | Incorrect
Line 810: data ShellCmd : (ty : Type) -> Access -> (ty -> Access) -> Type where
Line 811: Password : String -> ShellCmd PwdCheck ?password_in ?password_out
Line 812: Logout : ShellCmd () ?logout_in ?logout_out
Line 813: GetSecret : ShellCmd String ?getsecret_in ?getsecret_out
Line 814: PutStr : String -> ShellCmd () state (const state)
Line 815: Pure : (res : ty) -> ShellCmd ty (state_fn res) state_fn
Line 816: (>>=) : ShellCmd a state1 state2_fn ->
Line 817: ((res : a) -> ShellCmd b (state2_fn res) state3_fn) ->
Line 818: ShellCmd b state1 state3_fn
Line 819: Fill in the holes in the following types: 
Line 820: 
Line 821: Password—Reads a password and changes the state to LoggedIn or LoggedOut,
Line 822: depending on whether the password was correct
Line 823: 
Line 824: Logout—Changes the state from LoggedIn to LoggedOut
Line 825: 
Line 826: GetSecret—Reads a secret message as long as the state is LoggedIn
Line 827: The following function should type-check if you have the correct answer: 
Line 828: session : ShellCmd () LoggedOut (const LoggedOut)
Line 829: session = do Correct <- Password "wurzel"
Line 830: 
Line 831: --- 페이지 416 ---
Line 832: 390
Line 833: CHAPTER 14
Line 834: Dependent state machines: handling feedback and errors
Line 835: | Incorrect => PutStr "Wrong password"
Line 836: msg <- GetSecret
Line 837: PutStr ("Secret code: " ++ show msg ++ "\n")
Line 838: Logout
Line 839: The following functions should not type-check: 
Line 840: sessionBad : ShellCmd () LoggedOut (const LoggedOut)
Line 841: sessionBad = do Password "wurzel"
Line 842: msg <- GetSecret
Line 843: PutStr ("Secret code: " ++ show msg ++ "\n")
Line 844: Logout
Line 845: noLogout : ShellCmd () LoggedOut (const LoggedOut)
Line 846: noLogout = do Correct <- Password "wurzel"
Line 847: | Incorrect => PutStr "Wrong password"
Line 848: msg <- GetSecret
Line 849: PutStr ("Secret code: " ++ show msg ++ "\n")
Line 850:  2
Line 851: When inserting a coin into the vending machine defined in chapter 13, the
Line 852: machine could reject the coin. You can represent this by changing the types of
Line 853: MachineCmd and InsertCoin. An operation in MachineCmd can change the state
Line 854: based on its result: 
Line 855: data MachineCmd : (ty : Type) -> VendState -> (ty -> VendState) -> Type
Line 856: Then, InsertCoin can return whether or not the coin insertion was successful and
Line 857: change the state accordingly: 
Line 858: InsertCoin : MachineCmd CoinResult (pounds, chocs)
Line 859: (\res => case res of
Line 860: Inserted => (S pounds, chocs)
Line 861: Rejected => (pounds, chocs))
Line 862: Define the CoinResult type, and then make this change to MachineCmd in Vending
Line 863: .idr. Also, refine the types of the other commands and the implementation of
Line 864: machineLoop as necessary.
Line 865: 14.3
Line 866: A verified guessing game: describing rules in types
Line 867: As a concluding example in this chapter, we’ll look at how you can use a type to repre-
Line 868: sent the rules of a game precisely, and be sure that any implementation of the game
Line 869: follows the rules correctly. We’ll revisit an example from chapter 9, the word-guessing
Line 870: game Hangman.
Line 871:  To recap how this worked, you defined a WordState type to represent the state of
Line 872: the game. WordState was defined as follows, including the number of guesses and let-
Line 873: ters remaining as arguments:
Line 874: data WordState : (guesses : Nat) -> (letters : Nat) -> Type where
Line 875: MkWordState : (word : String)
Line 876: -> (missing : Vect letters Char)
Line 877: -> WordState guesses_remaining letters
Line 878: Target word, to be 
Line 879: guessed by the player
Line 880: Letters still to 
Line 881: be guessed by 
Line 882: the player
Line 883: 
Line 884: --- 페이지 417 ---
Line 885: 391
Line 886: A verified guessing game: describing rules in types
Line 887: You also defined a Finished type to express when a game was complete, either
Line 888: because there were no letters left to guess in the word (so the player won), or there
Line 889: were no guesses remaining (so the player lost):
Line 890: data Finished : Type where
Line 891: Lost : (game : WordState 0 (S letters)) -> Finished
Line 892: Won
Line 893: : (game : WordState (S guesses) 0) -> Finished
Line 894: Given these, you defined a main loop called game, which took a WordState with both
Line 895: guesses and letters remaining, and looped until the game was complete:
Line 896: game : WordState (S guesses) (S letters) -> IO Finished
Line 897: In the implementation, you used the type to help direct you to a working implementa-
Line 898: tion. But you could also have written an incorrect implementation of the game using
Line 899: this type. For example, the following implementation of game would also be well
Line 900: typed, but wrong, because it returns a losing game state in all cases:
Line 901: game : WordState (S guesses) (S letters) -> IO Finished
Line 902: game state = pure (Lost (MkWordState "ANYTHING" ['A']))
Line 903: Although the type allows you to express the game state precisely and helps you give
Line 904: types to intermediate operations (such as processing a guess), it doesn’t guarantee
Line 905: that the implementation follows the rules of the game correctly. In the preceding
Line 906: implementation, it’s impossible for the player to win!
Line 907:  In this section, instead of defining a WordState type and then trusting that game
Line 908: will follow the rules of the game correctly, we’ll define the rules of the game precisely
Line 909: in a state type. Just as DoorCmd expresses when we can execute operations on a door,
Line 910: and ATMCmd expresses when we can execute operations on an ATM, we can define a
Line 911: dependent GameCmd type that expresses when it’s valid to execute particular opera-
Line 912: tions in a game, and what the effect on those operations will be. As with the door and
Line 913: ATM examples, we’ll begin by defining the states and the operations that can be exe-
Line 914: cuted on those states.
Line 915: 14.3.1 Defining an abstract game state and operations
Line 916: First, we’ll think about how we can define the rules of the game in abstract terms,
Line 917: without worrying about the details of the implementation. A game can be in one of
Line 918: the following states:
Line 919: 
Line 920: NotRunning—There is no game currently in progress. Either the game hasn’t
Line 921: started and there’s no word yet to guess, or the game is complete.
Line 922: 
Line 923: Running—There is a game in progress, and the player has a number of guesses
Line 924: remaining and letters still to guess.
Line 925: In the case of Running, we’ll annotate the state with the number of guesses and letters
Line 926: remaining, just as we did with WordState earlier, because this means we’ll be able to
Line 927: No guesses left, so
Line 928: player has lost
Line 929: No letters left to guess, 
Line 930: so player has won
Line 931: 
Line 932: --- 페이지 418 ---
Line 933: 392
Line 934: CHAPTER 14
Line 935: Dependent state machines: handling feedback and errors
Line 936: describe precisely when a game has been won (no letters to guess) or lost (no guesses
Line 937: remaining). We can express the possible states in the following data type:
Line 938: data GameState : Type where
Line 939: NotRunning : GameState
Line 940: Running : (guesses : Nat) -> (letters : Nat) -> GameState
Line 941: Then, we’ll support some basic operations for manipulating the game state:
Line 942: 
Line 943: NewGame—Initializes a game with a word for the player to guess
Line 944: 
Line 945: Guess—Allows the player to guess a letter
Line 946: 
Line 947: Won—Declares that the player has won the game
Line 948: 
Line 949: Lost—Declares that the player has lost the game
Line 950: Figure 14.5 illustrates how these basic operations affect the game state. There are
Line 951: additional preconditions on Won and Lost: we can only declare that the player has
Line 952: won the game if there are no letters left to guess, and we can only declare that the
Line 953: player has lost if there are no guesses remaining.
Line 954: The next step is to represent these state transitions precisely in a dependent type,
Line 955: including the specific rules about the number of guesses and letters required for each
Line 956: operation to be valid. 
Line 957: 14.3.2 Defining a type for the game state
Line 958: We’ll define a GameCmd type that describes the possible operations you can run that
Line 959: affect GameState.
Line 960:  The next listing shows the types of NewGame, Won, and Lost from figure 14.5. As
Line 961: usual, Pure and (>>=) are included so that you can introduce pure values and
Line 962: sequence operations.
Line 963: import Data.Vect
Line 964: %default total
Line 965: data GameCmd : (ty : Type) -> GameState -> (ty -> GameState) -> Type where
Line 966: Listing 14.7
Line 967: Beginning to define GameCmd (Hangman.idr)
Line 968: Running
Line 969: NotRunning
Line 970: NewGame
Line 971: Guess
Line 972: Lost(guesses = 0)
Line 973: Won(letters = 0)
Line 974: Figure 14.5
Line 975: State transition diagram for Hangman. The Running state also 
Line 976: holds the number of letters and guesses remaining. Won requires the number of 
Line 977: letters to be zero, and Lost requires the number of guesses to be zero.
Line 978: You’ll use Vect later to 
Line 979: represent missing letters.
Line 980: Reports an
Line 981: error if any
Line 982: definitions
Line 983: are not total
Line 984: 
Line 985: --- 페이지 419 ---
Line 986: 393
Line 987: A verified guessing game: describing rules in types
Line 988: NewGame : (word : String) ->
Line 989: GameCmd () NotRunning
Line 990:   (const (Running 6 (length (letters word))))
Line 991: Won
Line 992: : GameCmd () (Running (S guesses) 0)
Line 993: (const NotRunning)
Line 994: Lost : GameCmd () (Running 0 (S guesses))
Line 995: (const NotRunning)
Line 996: Pure : (res : ty) -> GameCmd ty (state_fn res) state_fn
Line 997: (>>=) : GameCmd a state1 state2_fn ->
Line 998: ((res : a) -> GameCmd b (state2_fn res) state3_fn) ->
Line 999: GameCmd b state1 state3_fn
Line 1000: You can get the different letters in a word using letters, which converts the word to
Line 1001: uppercase, then converts it to a List Char, and finally removes any duplicate elements:
Line 1002: letters : String -> List Char
Line 1003: letters str = nub (map toUpper (unpack str))
Line 1004: Listing 14.8 adds a Guess operation to GameCmd. The type of Guess has a precondition
Line 1005: and a postcondition that explain how the guess affects the game:
Line 1006: As a precondition, there must be at least one guess available (S guesses) and at
Line 1007: least one letter still to guess (S letters), or attempting to guess a letter won’t
Line 1008: type-check.
Line 1009: As a postcondition, the number of guesses will reduce if the guess was incorrect,
Line 1010: and the number of letters will reduce if the guess was correct.
Line 1011: data GuessResult = Correct | Incorrect
Line 1012: data GameCmd : (ty : Type) -> GameState -> (ty -> GameState) -> Type where
Line 1013: NewGame : (word : String) ->
Line 1014: GameCmd () NotRunning
Line 1015:    (const (Running 6 (length (letters word))))
Line 1016: Won
Line 1017: : GameCmd () (Running (S guesses) 0)
Line 1018:  (const NotRunning)
Line 1019: Lost : GameCmd () (Running 0 (S guesses))
Line 1020: (const NotRunning)
Line 1021: Guess : (c : Char) ->
Line 1022: GameCmd GuessResult
Line 1023: (Running (S guesses) (S letters))
Line 1024: Listing 14.8
Line 1025: Adding a Guess operation (Hangman.idr)
Line 1026: You can only start a new game if 
Line 1027: you’re not currently playing a game.
Line 1028: Allows six guesses and
Line 1029: counts the number of
Line 1030: letters to guess
Line 1031: You can assert that the player has won, as 
Line 1032: long as there are no letters to guess, and 
Line 1033: move into the NotRunning state.
Line 1034: You can assert that the player has
Line 1035: lost, as long as there are no
Line 1036: guesses remaining.
Line 1037: nub is defined in the Prelude; 
Line 1038: it removes duplicate elements 
Line 1039: from a list.
Line 1040: The result of a Guess is either Correct or Incorrect.
Line 1041: You can only guess if 
Line 1042: there are guesses and 
Line 1043: letters remaining.
Line 1044: 
Line 1045: --- 페이지 420 ---
Line 1046: 394
Line 1047: CHAPTER 14
Line 1048: Dependent state machines: handling feedback and errors
Line 1049: (\res => case res of
Line 1050: Correct => Running (S guesses) letters
Line 1051: Incorrect => Running guesses (S letters))
Line 1052: Pure : (res : ty) -> GameCmd ty (state_fn res) state_fn
Line 1053: (>>=) : GameCmd a state1 state2_fn ->
Line 1054: ((res : a) -> GameCmd b (state2_fn res) state3_fn) ->
Line 1055: GameCmd b state1 state3_fn
Line 1056: Finally, in order to be able to implement the game with a user interface, you’ll need to
Line 1057: add commands for displaying the current game state, displaying any messages, and
Line 1058: reading a guess from the user:
Line 1059: data GameCmd : (ty : Type) -> GameState -> (ty -> GameState) -> Type where
Line 1060: {- Continued from Listing 14.8 -}
Line 1061: ShowState : GameCmd () state (const state)
Line 1062: Message : String -> GameCmd () state (const state)
Line 1063: ReadGuess : GameCmd Char state (const state)
Line 1064: Displaying the game state should display the known letters in the target word and the
Line 1065: number of guesses remaining. For example, if the target word is TESTING and you’ve
Line 1066: already guessed T, with six guesses remaining, ShowState should display the following:
Line 1067: T--T---
Line 1068: 6 guesses left
Line 1069: When you actually implement the game, it’s useful to support indefinitely long game
Line 1070: loops. For example, once you finish a game, a player might want to start a new game.
Line 1071: The next listing defines a GameLoop type, using Inf to note that execution might con-
Line 1072: tinue indefinitely. 
Line 1073: namespace Loop
Line 1074: data GameLoop : (ty : Type) -> GameState -> (ty -> GameState) -> Type where
Line 1075: (>>=) : GameCmd a state1 state2_fn ->
Line 1076: ((res : a) -> Inf (GameLoop b (state2_fn res) state3_fn)) ->
Line 1077: GameLoop b state1 state3_fn
Line 1078: Exit : GameLoop () NotRunning (const NotRunning)
Line 1079: You can use the operations in GameLoop and GameCmd to define the following function,
Line 1080: which implements a game loop:
Line 1081: gameLoop : GameLoop () (Running (S guesses) (S letters)) (const NotRunning)
Line 1082: Once you have a well-typed, total implementation of gameLoop, you’ll know that it’s a
Line 1083: valid implementation of the rules. Neither the game nor the player will be able to
Line 1084: Listing 14.9
Line 1085: A type for describing potentially infinite game loops (Hangman.idr)
Line 1086: Correct, so there’s one 
Line 1087: fewer letter to guess
Line 1088: Incorrect, so there’s one 
Line 1089: fewer guess remaining
Line 1090: You can’t Exit a game
Line 1091: that’s still running.
Line 1092: Introduces a new namespace, 
Line 1093: because you’re overloading (>>=)
Line 1094: 
Line 1095: --- 페이지 421 ---
Line 1096: 395
Line 1097: A verified guessing game: describing rules in types
Line 1098: cheat by breaking the rules as they’re defined in GameCmd. You can only call gameLoop
Line 1099: on a properly initialized game, with a word to guess, and any implementation must be
Line 1100: a complete implementation of the game because the only way to finish a GameLoop is
Line 1101: by calling Exit, which requires a game to be in the NotRunning state. 
Line 1102: 14.3.3 Implementing the game
Line 1103: We’ll implement gameLoop interactively and see how the state of the game progresses
Line 1104: by checking types as we go.
Line 1105:  To begin, you can create a skeleton definition, bringing guesses and letters
Line 1106: from the type into scope, because you’ll need to inspect them to check the player’s
Line 1107: progress later:
Line 1108: gameLoop : GameLoop () (Running (S guesses) (S letters)) (const NotRunning)
Line 1109: gameLoop {guesses} {letters} = ?gameLoop_rhs
Line 1110: To implement gameLoop, take the following steps:
Line 1111: 1
Line 1112: Refine—At the start of each iteration of gameLoop, you’ll display the current
Line 1113: state of the game using ShowState, read a guess from the user, and then check
Line 1114: whether it was correct: 
Line 1115: gameLoop : GameLoop () (Running (S guesses) (S letters)) (const NotRunning)
Line 1116: gameLoop {guesses} {letters} = do
Line 1117: ShowState
Line 1118: g <- ReadGuess
Line 1119: ok <- Guess g
Line 1120: ?gameLoop_rhs
Line 1121:  2
Line 1122: Type, define—If you check the type of ?gameLoop_rhs now, you’ll see that the
Line 1123: current state of the game depends on whether the guess was correct or not:
Line 1124: letters : Nat
Line 1125: guesses : Nat
Line 1126: g : Char
Line 1127: ok : GuessResult
Line 1128: --------------------------------------
Line 1129: gameLoop_rhs : GameLoop ()
Line 1130: (case ok of
Line 1131: Correct => Running (S guesses) letters
Line 1132: Incorrect => Running guesses (S letters))
Line 1133: (\value => NotRunning)
Line 1134: To make progress, you’ll need to inspect ok to establish which state the game is in:
Line 1135: gameLoop : GameLoop () (Running (S guesses) (S letters)) (const NotRunning)
Line 1136: gameLoop {guesses} {letters} = do
Line 1137: ShowState
Line 1138: g <- ReadGuess
Line 1139: ok <- Guess g
Line 1140: case ok of
Line 1141: Correct => ?gameLoop_rhs_1
Line 1142: Incorrect => ?gameLoop_rhs_2
Line 1143: 
Line 1144: --- 페이지 422 ---
Line 1145: 396
Line 1146: CHAPTER 14
Line 1147: Dependent state machines: handling feedback and errors
Line 1148:  3
Line 1149: Type, define—In ?gameLoop_rhs_1, the guess was correct, so the number of let-
Line 1150: ters remaining is reduced, as you can see by checking its type: 
Line 1151: ok : GuessResult
Line 1152: letters : Nat
Line 1153: guesses : Nat
Line 1154: g : Char
Line 1155: --------------------------------------
Line 1156: gameLoop_rhs_1 : GameLoop ()
Line 1157: (Running (S guesses) letters)
Line 1158: (\value => NotRunning)
Line 1159: You can only continue with gameLoop if there are both letters and guesses
Line 1160: remaining, because its input state is Running (S guesses) (S letters). To
Line 1161: decide how to continue, you’ll need to check the current value of letters:
Line 1162: case ok of
Line 1163: Correct => case letters of
Line 1164: Z => ?gameLoop_rhs_3
Line 1165: S k => ?gameLoop_rhs_4
Line 1166: Incorrect => ?gameLoop_rhs_2
Line 1167:  4
Line 1168: Refine—In ?gameLoop_rhs_3, there are no letters left to guess, so the player has
Line 1169: won. You can declare that the player has won with Won, moving to the Not-
Line 1170: Running state. Then display the final state and exit: 
Line 1171: case ok of
Line 1172: Correct => case letters of
Line 1173: Z => do Won
Line 1174: ShowState
Line 1175: Exit
Line 1176: S k => ?gameLoop_rhs_4
Line 1177: Incorrect => ?gameLoop_rhs_2
Line 1178: You need to Exit explicitly, because Exit is the only way to break out of a
Line 1179: GameLoop. You can only Exit a game in the NotRunning state.
Line 1180: 5
Line 1181: Refine—In ?gameLoop_rhs_4, there are still letters to guess, so you can display a
Line 1182: message and continue with gameLoop: 
Line 1183: case ok of
Line 1184: Correct => case letters of
Line 1185: Z => do Won
Line 1186: ShowState
Line 1187: Exit
Line 1188: S k => do Message "Correct"
Line 1189: gameLoop
Line 1190: Incorrect => ?gameLoop_rhs_2
Line 1191: The Incorrect case works similarly, checking whether guesses are still available and
Line 1192: declaring that the player has lost if not. The following listing gives the complete defi-
Line 1193: nition, for reference.
Line 1194: 
Line 1195: --- 페이지 423 ---
Line 1196: 397
Line 1197: A verified guessing game: describing rules in types
Line 1198:  
Line 1199: gameLoop : GameLoop () (Running (S guesses) (S letters)) (const NotRunning)
Line 1200: gameLoop {guesses} {letters} = do
Line 1201: ShowState
Line 1202: g <- ReadGuess
Line 1203: ok <- Guess g
Line 1204: case ok of
Line 1205: Correct => case letters of
Line 1206: Z => do Won
Line 1207: ShowState
Line 1208: Exit
Line 1209: S k => do Message "Correct"
Line 1210: gameLoop
Line 1211: Incorrect => case guesses of
Line 1212: Z => do Lost
Line 1213: ShowState
Line 1214: Exit
Line 1215: (S k) => do Message "Incorrect"
Line 1216: gameLoop
Line 1217: You’ll also need to initialize the game. For example, you could write a function to set
Line 1218: up a new game, and then initiate the gameLoop:
Line 1219: hangman : GameLoop () NotRunning (const NotRunning)
Line 1220: hangman = do NewGame "testing"
Line 1221: gameLoop
Line 1222: So far, you’ve only defined a data type that describes the actions in the game. The
Line 1223: gameLoop function describes sequences of actions in a valid game of Hangman that fol-
Line 1224: lows the rules. In order to run the game, you’ll need to define a concrete representation
Line 1225: of the game state and a function that translates a GameLoop to a sequence of IO actions. 
Line 1226: 14.3.4 Defining a concrete game state
Line 1227: In the stack example in chapter 13, we had an abstract state of the stack (the number
Line 1228: of items on the stack), and a concrete state represented by a Vect of an appropriate
Line 1229: length. Similarly, GameState is the abstract state of a game, describing only whether a
Line 1230: game is running, and if so, how many guesses and letters are remaining.
Line 1231:  In order to run a game, you’ll need to define a corresponding concrete game state
Line 1232: that includes the specific target word and which specific letters are still to be guessed.
Line 1233: The following listing defines a Game type with a GameState argument, representing the
Line 1234: concrete data associated with an abstract game state.
Line 1235: data Game : GameState -> Type where
Line 1236: GameStart
Line 1237: : Game NotRunning
Line 1238: GameWon
Line 1239: : (word : String) -> Game NotRunning
Line 1240: Listing 14.10
Line 1241: A complete implementation of gameLoop (Hangman.idr)
Line 1242: Listing 14.11
Line 1243: Representing the concrete game state (Hangman.idr)
Line 1244: Game is NotRunning because 
Line 1245: it hasn’t started yet
Line 1246: Game is NotRunning because 
Line 1247: the player has won
Line 1248: 
Line 1249: --- 페이지 424 ---
Line 1250: 398
Line 1251: CHAPTER 14
Line 1252: Dependent state machines: handling feedback and errors
Line 1253: GameLost
Line 1254: : (word : String) -> Game NotRunning
Line 1255: InProgress : (word : String) -> (guesses : Nat)
Line 1256: -> (missing : Vect letters Char)
Line 1257: -> Game (Running guesses letters)
Line 1258: It’s convenient to define a Show implementation for Game so that you can easily display
Line 1259: a string representation of a game’s progress. 
Line 1260: Show (Game g) where
Line 1261: show GameStart = "Starting"
Line 1262: show (GameWon word) = "Game won: word was " ++ word
Line 1263: show (GameLost word) = "Game lost: word was " ++ word
Line 1264: show (InProgress word guesses missing)
Line 1265: = "\n" ++ pack (map hideMissing (unpack word))
Line 1266: ++ "\n" ++ show guesses ++ " guesses left"
Line 1267: where hideMissing : Char -> Char
Line 1268: hideMissing c = if c `elem` missing then '-' else c
Line 1269: You can use Game to keep track of the concrete game state. When you execute a
Line 1270: GameLoop, you’ll take a concrete game state as input, and return a result along with
Line 1271: the updated game state:
Line 1272: data Fuel = Dry | More (Lazy Fuel)
Line 1273: run : Fuel ->
Line 1274: Game instate ->
Line 1275: GameLoop ty instate outstate_fn ->
Line 1276: IO (GameResult ty outstate_fn)
Line 1277: You use Fuel, because run potentially loops. In particular, when you read a Guess
Line 1278: from the player, the only valid input is a single alphabetical character, so you’ll need
Line 1279: to keep asking for input until it’s valid.
Line 1280:  If you run out of fuel, the GameResult needs to say that execution failed. Other-
Line 1281: wise, it needs to store the result of the operation and the new state. Crucially, the type
Line 1282: of the new state might depend on the result; for example, the number of guesses avail-
Line 1283: able is different depending on whether Guess returns Correct or Incorrect. A
Line 1284: GameResult, therefore, is one of the following:
Line 1285: A pair of the result produced by executing the game and the output state, with
Line 1286: a type calculated from the result
Line 1287: An error, if run ran out of fuel
Line 1288: You can define GameResult as follows:
Line 1289: data GameResult : (ty : Type) -> (ty -> GameState) -> Type where
Line 1290: OK : (res : ty) -> Game (outstate_fn res) ->
Line 1291: GameResult ty outstate_fn
Line 1292: OutOfFuel : GameResult ty outstate_fn
Line 1293: Listing 14.12
Line 1294: A Show implementation for Game (Hangman.idr)
Line 1295: Game is NotRunning 
Line 1296: because the player has lost
Line 1297: Game is in progress, 
Line 1298: with guesses and 
Line 1299: letters remaining
Line 1300: Only displays the 
Line 1301: characters that the 
Line 1302: player has successfully 
Line 1303: guessed
Line 1304: The input
Line 1305: game state
Line 1306: A command to 
Line 1307: update the 
Line 1308: game state
Line 1309: GameResult, defined 
Line 1310: shortly, pairs the result 
Line 1311: value and the output state.
Line 1312: As in the definition of 
Line 1313: GameCmd, the argument 
Line 1314: to Game is calculated 
Line 1315: from the result, res.
Line 1316: 
Line 1317: --- 페이지 425 ---
Line 1318: 399
Line 1319: A verified guessing game: describing rules in types
Line 1320: outstate_fn is included in the type of GameResult because then you’re explicit in the
Line 1321: type about how you’re calculating the output state of Game.
Line 1322:  Now that you have a data type to represent the concrete state of a game—which
Line 1323: takes the abstract state as an argument—along with a representation of the result,
Line 1324: you’re ready to implement run. 
Line 1325: 14.3.5 Running the game: executing GameLoop
Line 1326: The next listing outlines the definition of run for GameLoop. This uses another function,
Line 1327: runCmd, to execute GameCmd. There’s a hole for the definition of runCmd for the moment.
Line 1328: runCmd : Fuel ->
Line 1329: Game instate -> GameCmd ty instate outstate_fn ->
Line 1330: IO (GameResult ty outstate_fn)
Line 1331: runCmd fuel state cmd = ?runCmd_rhs
Line 1332: run : Fuel -> Game instate -> GameLoop ty instate outstate_fn ->
Line 1333: IO (GameResult ty outstate_fn)
Line 1334: run Dry _ _ = pure OutOfFuel
Line 1335: run (More fuel) st (cmd >>= next)
Line 1336: = do OK cmdRes newSt <- runCmd fuel st cmd
Line 1337: | OutOfFuel => pure OutOfFuel
Line 1338: run fuel newSt (next cmdRes)
Line 1339: run (More fuel) st Exit = pure (OK () st)
Line 1340: In run, when it’s successful, you use pure to return a pair of the result and the new
Line 1341: state. Because you’ll often return a result in this form when executing a command,
Line 1342: you can define a helper function, ok, to make this more concise:
Line 1343: ok : (res : ty) -> Game (outstate_fn res) ->
Line 1344: IO (GameResult ty outstate_fn)
Line 1345: ok res st = pure (OK res st)
Line 1346: Using ok, you can refine the last clause of run to the following:
Line 1347: run (More fuel) st Exit = ok () st
Line 1348: Listing 14.14 gives an outline definition of runCmd, leaving holes for the Guess and
Line 1349: ReadGuess cases. In the other cases, you use ok to update the state as required by the
Line 1350: type and execute IO actions as necessary.
Line 1351: runCmd : Fuel -> Game instate -> GameCmd ty instate outstate_fn ->
Line 1352: IO (GameResult ty outstate_fn)
Line 1353: runCmd fuel state (NewGame word)
Line 1354: = ok () (InProgress (toUpper word) _ (fromList (letters word)))
Line 1355: Listing 14.13
Line 1356: Running the game loop (Hangman.idr)
Line 1357: Listing 14.14
Line 1358: Outline definition of runCmd (Hangman.idr)
Line 1359: Runs a command. We’ll leave a 
Line 1360: hole for this, and define in shortly.
Line 1361: When successful, 
Line 1362: run returns the 
Line 1363: result of the 
Line 1364: operation 
Line 1365: (cmdRes here) 
Line 1366: and an updated 
Line 1367: state (newSt here).
Line 1368: First command 
Line 1369: ran out of fuel
Line 1370: Creates a new in-progress game, using letters
Line 1371: to extract unique letters from the word
Line 1372: 
Line 1373: --- 페이지 426 ---
Line 1374: 400
Line 1375: CHAPTER 14
Line 1376: Dependent state machines: handling feedback and errors
Line 1377: runCmd fuel (InProgress word _ missing) Won
Line 1378: = ok () (GameWon word)
Line 1379: runCmd fuel (InProgress word _ missing) Lost
Line 1380: = ok () (GameLost word)
Line 1381: runCmd fuel state (Guess c) = ?runCmd_rhs_4
Line 1382: runCmd fuel state ShowState = do printLn state
Line 1383: ok () state
Line 1384: runCmd fuel state (Message str) = do putStrLn str
Line 1385: ok () state
Line 1386: runCmd fuel state ReadGuess = ?runCmd_rhs_7
Line 1387: runCmd fuel state (Pure res) = ok res state
Line 1388: runCmd fuel st (cmd >>= next)
Line 1389: = do OK cmdRes newSt <- runCmd fuel st cmd
Line 1390: | OutOfFuel => pure OutOfFuel
Line 1391: runCmd fuel newSt (next cmdRes)
Line 1392: When a game is in progress, the game state uses the InProgress constructor of Game,
Line 1393: which has the following type:
Line 1394: *Hangman> :t InProgress
Line 1395: InProgress : String ->
Line 1396: (guesses : Nat) ->
Line 1397: Vect letters Char -> Game (Running guesses letters)
Line 1398: The third argument is a vector of the letters that are still to be guessed. So, in the
Line 1399: Guess case, you check whether the guessed character is in the vector of missing letters:
Line 1400: runCmd fuel (InProgress word _ missing) (Guess c)
Line 1401: = case isElem c missing of
Line 1402: Yes prf => ok Correct (InProgress word _ (removeElem c missing))
Line 1403: No contra => ok Incorrect (InProgress word _ missing)
Line 1404: You defined removeElem interactively in chapter 9 in the earlier implementation of
Line 1405: Hangman. For convenience, I’ll repeat it here:
Line 1406: removeElem : (value : a) -> (xs : Vect (S n) a) ->
Line 1407: {auto prf : Elem value xs} ->
Line 1408: Vect n a
Line 1409: removeElem value (value :: ys) {prf = Here} = ys
Line 1410: removeElem {n = Z} value (y :: []) {prf = There later} = absurd later
Line 1411: removeElem {n = (S k)} value (y :: ys) {prf = There later}
Line 1412: = y :: removeElem value ys
Line 1413: Updates to the 
Line 1414: NonRunning game state
Line 1415: Prints a message 
Line 1416: and continues with 
Line 1417: current state
Line 1418: As with run, you execute the first 
Line 1419: command and continue with the 
Line 1420: result and state it produces.
Line 1421: Correct, so remove the letter from 
Line 1422: the vector of missing letters
Line 1423: Returns a proof of whether c is 
Line 1424: in the vector of missing letters
Line 1425: Incorrect. The guesses argument
Line 1426: to InProgress is inferred from
Line 1427: the type, and decreases.
Line 1428: 
Line 1429: --- 페이지 427 ---
Line 1430: 401
Line 1431: A verified guessing game: describing rules in types
Line 1432: Finally, you need to define the ReadGuess case, which reads a character from the
Line 1433: player. The input is only valid if it’s an alphabetical character, so you loop until the
Line 1434: player enters a valid input:
Line 1435: runCmd (More fuel) st ReadGuess = do
Line 1436: putStr "Guess: "
Line 1437: input <- getLine
Line 1438: case unpack input of
Line 1439: [x] => if isAlpha x
Line 1440: then ok (toUpper x) st
Line 1441: else do putStrLn "Invalid input"
Line 1442: runCmd fuel st ReadGuess
Line 1443: _ => do putStrLn "Invalid input"
Line 1444: runCmd fuel st ReadGuess
Line 1445: runCmd Dry _ _ = pure OutOfFuel
Line 1446: This case might loop indefinitely if the user continues to enter invalid input, so
Line 1447: runCmd takes Fuel as an argument and consumes fuel whenever there’s an invalid
Line 1448: input. As a result, runCmd itself remains total because it either consumes fuel or pro-
Line 1449: cesses a command on each recursive call. It’s important for runCmd to be total, because
Line 1450: it means you know that executing a GameCmd will continue to make progress as long as
Line 1451: there are commands to execute.
Line 1452:  You’re now in a position to write the main program, using forever to ensure that,
Line 1453: in practice, run never runs out of fuel. Add the following to the end of Hangman.idr:
Line 1454: %default partial
Line 1455: forever : Fuel
Line 1456: forever = More forever
Line 1457: main : IO ()
Line 1458: main = do run forever GameStart hangman
Line 1459: pure ()
Line 1460: You should now be able to execute the game at the REPL. Here’s an example:
Line 1461: *Hangman> :exec
Line 1462: -------
Line 1463: 6 guesses left
Line 1464: Guess: t
Line 1465: Correct
Line 1466: T--T---
Line 1467: 6 guesses left
Line 1468: Guess: x
Line 1469: Incorrect
Line 1470: T--T---
Line 1471: 5 guesses left
Line 1472: Guess: g
Line 1473: Correct
Line 1474: Reads a single alphabetical 
Line 1475: character, so input is valid
Line 1476: Invalid input, so 
Line 1477: prompt again but 
Line 1478: with reduced fuel
Line 1479: Needed to catch the case where 
Line 1480: ReadGuess runs out of fuel
Line 1481: Analogous to %default total, this 
Line 1482: means that all following definitions 
Line 1483: are allowed to be partial.
Line 1484: Initializes with the GameStart state, 
Line 1485: meaning that no game is running
Line 1486: 
Line 1487: --- 페이지 428 ---
Line 1488: 402
Line 1489: CHAPTER 14
Line 1490: Dependent state machines: handling feedback and errors
Line 1491: T--T--G
Line 1492: 5 guesses left
Line 1493: Guess: bad
Line 1494: Invalid input
Line 1495: Guess:
Line 1496: In this example, we’ve separated the description of the rules, in GameCmd and GameLoop,
Line 1497: from the execution of the rules, in runCmd and run. Essentially, GameCmd and GameLoop
Line 1498: define an interface for constructing a valid game of Hangman, correctly following the
Line 1499: rules. Any well-typed total function using these types must be a correct implementa-
Line 1500: tion of the rules, or it wouldn’t have type-checked!
Line 1501: 14.4
Line 1502: Summary
Line 1503: You can get feedback from the environment by using the result of an operation
Line 1504: to compute the output state of a command.
Line 1505: A system might be in a different state after running a command, depending on
Line 1506: whether the command was successful.
Line 1507: Defining preconditions on operations allows you to express security properties
Line 1508: in types, such as when it’s valid for an ATM to dispense cash.
Line 1509: A system might change state according to whether a user’s input is valid in the
Line 1510: current environment, such as whether a PIN or password is correct.
Line 1511: Predicates and auto implicits help you describe valid input states of operations
Line 1512: precisely.
Line 1513: You can describe the rules of a game precisely in a type, so that a function that
Line 1514: type-checks must be a valid implementation of the rules.
Line 1515: You use an abstract state type to describe what operations do, and a concrete
Line 1516: state, depending on the abstract state, to describe their corresponding imple-
Line 1517: mentations.