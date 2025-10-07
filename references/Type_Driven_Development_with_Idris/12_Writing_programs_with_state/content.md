Line 1: 
Line 2: --- 페이지 350 ---
Line 3: 324
Line 4: Writing programs with state
Line 5: Idris is a pure language, so variables are immutable. Once a variable is defined with
Line 6: a value, nothing can update it. This might suggest that writing programs that
Line 7: manipulate state is difficult, or even impossible, or that Idris programmers in gen-
Line 8: eral aren’t interested in state. In practice, the opposite is true.
Line 9:  In type-driven development, a function’s type tells you exactly what a function
Line 10: can do in terms of its allowed inputs and outputs. So, if you want to write a function
Line 11: that manipulates state, you can do that, but you need to be explicit about it in the
Line 12: function’s type. In fact, we’ve already done this in earlier chapters:
Line 13: In chapter 4, we implemented an interactive data store using global state.
Line 14: In chapter 9, we implemented a word-guessing game using global state to
Line 15: hold the target word, the letters guessed, and the number of guesses still
Line 16: available.
Line 17: In chapter 11, we implemented an arithmetic game using global state to hold
Line 18: the user’s current score.
Line 19: This chapter covers
Line 20: Using the State type to describe mutable state
Line 21: Implementing custom types for state management
Line 22: Defining and using records for global system state
Line 23: 
Line 24: --- 페이지 351 ---
Line 25: 325
Line 26: Working with mutable state
Line 27:  In each case, we implemented state by writing a recursive function that took the
Line 28: current state of the overall program as an argument.
Line 29:  Almost all real-world applications need to manipulate state to some extent. Some-
Line 30: times, as in the previous examples, state is global and is used throughout an applica-
Line 31: tion. Sometimes, state is local to an algorithm; for example, a graph-traversal
Line 32: algorithm will hold the nodes it has visited in local state to avoid visiting nodes more
Line 33: than once. In this chapter, we’ll look at how we can manage mutable state in Idris,
Line 34: both for state that’s local to an algorithm, and for representing overall system state.
Line 35: STATE MANAGEMENT AND DEPENDENT TYPES
Line 36: We won’t use many dependent
Line 37: types in this chapter; using dependent types in state introduces some compli-
Line 38: cations, as well as opportunities for precision in describing state transition sys-
Line 39: tems and protocols. We’ll consider these opportunities in the next two chapters,
Line 40: but we’ll begin here by looking at how state works in general.
Line 41: Previously, we’ve used types to describe interactive programs in terms of sequences of
Line 42: commands, using IO in chapter 5 and ConsoleIO in chapter 11. Stateful programs can
Line 43: work in the same way, using types to describe the operations a stateful program can
Line 44: perform. We’ll begin by looking at the generic State type defined in the Idris library
Line 45: and then at how we can define types like State ourselves. Finally, we’ll look at how we
Line 46: can structure a complete application with state, refining the arithmetic quiz from
Line 47: chapter 11. 
Line 48: 12.1
Line 49: Working with mutable state
Line 50: Even though Idris is a pure language, it’s often useful to work with state. It’s particu-
Line 51: larly useful, when writing functions with a complex data structure, such as a tree or a
Line 52: graph, to be able to read and write local state as you’re traversing the structure. In this
Line 53: section, you’ll see how to manage mutable state.
Line 54: COMPARING STATE IN IDRIS AND HASKELL
Line 55: This section describes the State
Line 56: type for capturing local mutable state in Idris. If you’re familiar with Haskell,
Line 57: you’ll find that you can use State in Idris in the same way as Haskell, by
Line 58: importing Control.Monad.State. If you’re familiar with the State type in
Line 59: Haskell, you can safely move ahead to section 12.2, where I’ll describe a cus-
Line 60: tom implementation of State.
Line 61: In the previous chapter, you wrote a function to attach labels to elements of a list, tak-
Line 62: ing the labels from a Stream. It’s repeated for reference here.
Line 63: labelWith : Stream labelType -> List a -> List (labelType, a)
Line 64: labelWith lbs [] = []
Line 65: labelWith (lbl :: lbls) (val :: vals) = (lbl, val) :: labelWith lbls vals
Line 66: Listing 12.1
Line 67: Labeling each element of a List using a Stream (Streams.idr)
Line 68: For every label in the stream, pair it with
Line 69: the corresponding element of the list.
Line 70: 
Line 71: --- 페이지 352 ---
Line 72: 326
Line 73: CHAPTER 12
Line 74: Writing programs with state
Line 75: In this section, you’ll implement a function similar to label a binary tree. First, you’ll
Line 76: see how to implement mutable state by hand, with each function returning a pair that
Line 77: stores an updated state along with the result of a computation. You’ll then see how to
Line 78: encapsulate the state using a State type defined in the Idris base library. First, though,
Line 79: I’ll describe the example of tree traversal in more detail.
Line 80: 12.1.1 The tree-traversal example
Line 81: Figure 12.1 shows the result of a function that labels a binary tree, and we’ll use this as
Line 82: a running example throughout this section. This function labels the nodes depth first,
Line 83: left to right, so the deepest, leftmost node takes the first label, and the deepest, right-
Line 84: most node takes the last label.
Line 85: The following listing gives the definition of binary trees that we’ll use for labeling,
Line 86: along with testTree, a representation of the specific tree we’ll label (from the exam-
Line 87: ple in figure 12.1).
Line 88: data Tree a = Empty
Line 89: | Node (Tree a) a (Tree a)
Line 90: testTree : Tree String
Line 91: testTree = Node (Node (Node Empty "Jim" Empty) "Fred"
Line 92: (Node Empty "Sheila" Empty)) "Alice"
Line 93: (Node Empty "Bob" (Node Empty "Eve" Empty))
Line 94: flatten : Tree a -> List a
Line 95: flatten Empty = []
Line 96: flatten (Node left val right) = flatten left ++ val :: flatten right
Line 97: It’s convenient to define flatten so that you can easily see the ordering in which the
Line 98: labels should be applied:
Line 99: *TreeLabel> flatten testTree
Line 100: ["Jim", "Fred", "Sheila", "Alice", "Bob", "Eve"] : List String
Line 101: Listing 12.2
Line 102: Definition of binary trees, and an example (TreeLabel.idr)
Line 103: 1, Jim
Line 104: 3, Sheila
Line 105: 2, Fred
Line 106: 4, Alice
Line 107: 6, Eve
Line 108: 5, Bob
Line 109: Jim
Line 110: Sheila
Line 111: Fred
Line 112: Alice
Line 113: Eve
Line 114: Bob
Line 115: Figure 12.1
Line 116: Labeling a tree, depth first. Each node is labeled with an integer.
Line 117: A tree node
Line 118: with a value,
Line 119: a left subtree,
Line 120: and a right
Line 121: subtree
Line 122: An empty binary tree
Line 123: A representation of the example tree
Line 124: Converts the tree to a list by traversing 
Line 125: the tree, depth first, left to right
Line 126: 
Line 127: --- 페이지 353 ---
Line 128: 327
Line 129: Working with mutable state
Line 130: Once you’ve written a treeLabel function that labels the nodes in the tree according
Line 131: to the elements in a stream, you should be able to run it as follows:
Line 132: *TreeLabel> flatten (treeLabel testTree)
Line 133: [(1, "Jim"),
Line 134: (2, "Fred"),
Line 135: (3, "Sheila"),
Line 136: (4, "Alice"),
Line 137: (5, "Bob"),
Line 138: (6, "Eve")] : List (Integer, String)
Line 139: When you wrote the function to label lists, in listing 12.1, you had a direct correspon-
Line 140: dence between the structure of the stream of labels and the list you were labeling.
Line 141: That is, for every (::) in the List, you could take the first element of the stream as
Line 142: the label, and then recursively label the rest of the list. With Tree, it’s a bit more com-
Line 143: plicated, because when you label the left subtree, you don’t know in advance how
Line 144: many elements you’ll need to take from the stream. Figure 12.2 illustrates labeling the
Line 145: subtrees in this example.
Line 146: Before labeling the right subtree, you need to know how many elements you took
Line 147: from the stream when labeling the left subtree. Not only does the labeling function
Line 148: need to return the labeled tree, it also needs to return some information about where
Line 149: to start labeling the rest of the tree.
Line 150:  A natural way to do this might be for the labeling function to take the stream of
Line 151: labels as an input, as before, and to return a pair, containing
Line 152: The labeled tree
Line 153: A new stream of labels that you can use to label the rest of the tree
Line 154: We’ll begin by implementing tree labeling this way, using a pair to represent the result
Line 155: of the operation and the state of the labels. Then, you’ll see how the State type
Line 156: defined in the Idris library encapsulates the state management details in this kind of
Line 157: algorithm. 
Line 158: 1, Jim
Line 159: 3, Sheila
Line 160: 2, Fred
Line 161: 4, Alice
Line 162: 6, Eve
Line 163: 5, Bob
Line 164: Figure 12.2
Line 165: Labeling subtrees. The left 
Line 166: subtree is labeled from 1 to 3, and the right 
Line 167: subtree is labeled from 5 to 6.
Line 168: 
Line 169: --- 페이지 354 ---
Line 170: 328
Line 171: CHAPTER 12
Line 172: Writing programs with state
Line 173: 12.1.2 Representing mutable state using a pair
Line 174: Listing 12.3 defines a helper function to label a tree with a stream of labels, and uses a
Line 175: pair to represent the state of the stream after each subtree is labeled. The helper func-
Line 176: tion returns the unused part of the stream of labels, so that when you’ve labeled one
Line 177: subtree, you know where to start labeling the next subtree.
Line 178: treeLabelWith : Stream labelType -> Tree a ->
Line 179: (Stream labelType, Tree (labelType, a))
Line 180: treeLabelWith lbls Empty = (lbls, Empty)
Line 181: treeLabelWith lbls (Node left val right)
Line 182: = let (lblThis :: lblsLeft, left_labelled) = treeLabelWith lbls left
Line 183: (lblsRight, right_labelled) = treeLabelWith lblsLeft right
Line 184: in
Line 185: (lblsRight, Node left_labelled (lblThis, val) right_labelled)
Line 186: treeLabel : Tree a -> Tree (Integer, a)
Line 187: treeLabel tree = snd (treeLabelWith [1..] tree)
Line 188: If you try labeling the example tree, you’ll see that the labels are applied in the order
Line 189: you expect:
Line 190: *TreeLabel> flatten (treeLabel testTree)
Line 191: [(1, "Jim"),
Line 192: (2, "Fred"),
Line 193: (3, "Sheila"),
Line 194: (4, "Alice"),
Line 195: (5, "Bob"),
Line 196: (6, "Eve")] : List (Integer, String)
Line 197: You can check that labeling also preserves the structure of the tree by omitting the call
Line 198: to flatten:
Line 199: *TreeLabel> treeLabel testTree
Line 200: Node (Node (Node Empty (1, "Jim") Empty)
Line 201: (2, "Fred")
Line 202: (Node Empty (3, "Sheila") Empty))
Line 203: (4, "Alice")
Line 204: (Node Empty
Line 205: (5, "Bob")
Line 206: (Node Empty (6, "Eve") Empty)) : Tree (Integer, String)
Line 207: In the current definition of treeLabelWith, you need to keep track of the state of the
Line 208: stream of labels. Labeling a subtree not only gives you a tree with labels attached to
Line 209: the nodes, it also gives you a new stream of labels for labeling the next part of the tree.
Line 210: Listing 12.3
Line 211: Labeling a Tree with a stream of labels (TreeLabel.idr)
Line 212: Returns the unused portion of the 
Line 213: stream, as well as the labeled tree
Line 214: Labels the left subtree,
Line 215: which gives you a new
Line 216: subtree and a new
Line 217: stream. Uses the first
Line 218: element, lblThis, to label
Line 219: the current node.
Line 220: Labels the right subtree, 
Line 221: using the stream returned 
Line 222: after labeling the left subtree
Line 223: Returns the stream
Line 224: given by labeling the
Line 225: right subtree, and a
Line 226: labeled node
Line 227: Initializes with a stream of
Line 228: integers, and returns only
Line 229: the labeled tree using snd
Line 230: 
Line 231: --- 페이지 355 ---
Line 232: 329
Line 233: Working with mutable state
Line 234:  As you traverse the tree, you keep track of the state of the stream by passing it as an
Line 235: argument, and returning the updated state. Essentially, the function uses local mutable
Line 236: state, with the state explicitly threaded through the definition. Although this works,
Line 237: there are two problems with this approach:
Line 238: It’s error-prone because you need to ensure that the correct state is propagated
Line 239: correctly to the recursive calls. Notice that left_labelled and right_labelled
Line 240: have the same type, for example, so it’s easy to use the wrong one!
Line 241: It’s hard to read because the details of the algorithm are hidden behind the
Line 242: details of state management.
Line 243: It’s often useful to have local mutable state, and like any concept you use regularly, it’s
Line 244: a good idea to create an abstraction that captures the concept. You can improve the
Line 245: definition of treeLabel, making it less error-prone and more readable, by using a
Line 246: type that captures the concept of state explicitly. 
Line 247: 12.1.3 State, a type for describing stateful operations
Line 248: The only reason you’re passing the stream of labels around in the definition of tree-
Line 249: LabelWith is that when you encounter a value at a node, you need to associate it with
Line 250: a label value. In an imperative language, you might pass a mutable variable to tree-
Line 251: LabelWith and update it as you encounter each node. Because Idris is a purely func-
Line 252: tional language, you don’t have mutable variables, but the base library does provide a
Line 253: type for describing sequences of stateful operations, in the Control.Monad.State
Line 254: module. Control.Monad.State exports the following relevant definitions.
Line 255: State : (stateType : Type) -> (ty : Type) -> Type
Line 256: runState : State stateType a -> stateType -> (a, stateType)
Line 257: get : State stateType stateType
Line 258: put : stateType -> State stateType ()
Line 259: (>>=) : State stateType a -> (a -> State stateType b) -> State stateType b
Line 260: Just as a value of IO ty describes a sequence of interactive operations that produce a
Line 261: value of type ty, a value of type State Nat ty describes a sequence of operations that
Line 262: read and write a mutable state of type Nat. Listing 12.5 gives a small example of a func-
Line 263: tion that works with mutable state. It reads the state using get and then updates it
Line 264: using put, increasing the Nat state by the given value.
Line 265: Listing 12.4
Line 266: State and associated functions, defined in Control.Monad.State
Line 267: A type describing sequences of stateful 
Line 268: operations with a state of type stateType, 
Line 269: producing a result of type ty
Line 270: Runs a sequence of stateful
Line 271: operations, producing a pair of
Line 272: the result and the final state
Line 273: Reads the current state, producing 
Line 274: a result of type stateType
Line 275: Writes a new state, 
Line 276: producing a result of type ()
Line 277: Sequences get and put with do notation.
Line 278: There’s a Monad implementation for
Line 279: State that defines (>>=).
Line 280: 
Line 281: --- 페이지 356 ---
Line 282: 330
Line 283: CHAPTER 12
Line 284: Writing programs with state
Line 285:  
Line 286: import Control.Monad.State
Line 287: increase : Nat -> State Nat ()
Line 288: increase inc = do current <- get
Line 289: put (current + inc)
Line 290: A value of type State Nat () is a description of stateful operations using a state of type
Line 291: Nat. You can execute it using runState by passing it the operations and an initial state.
Line 292: For example, you can execute increase 5 with an initial state of 89:
Line 293: *State> runState (increase 5) 89
Line 294: ((), 94) : ((), Nat)
Line 295: The result is a pair of the value produced by the stateful operations, in this case the unit
Line 296: value (), and the final state, in this case 94. There are also two variants of runState:
Line 297: 
Line 298: evalState—Returns only the value produced by the sequence of operations: 
Line 299: *State> :t evalState
Line 300: evalState : State stateType a -> stateType -> a
Line 301: *State> evalState (increase 5) 89
Line 302: () : ()
Line 303: 
Line 304: execState—Returns only the final state after the sequence of operations: 
Line 305: *State> :t execState
Line 306: execState : State stateType a -> stateType -> stateType
Line 307: *State> execState (increase 5) 89
Line 308: 94 : Nat
Line 309: Listing 12.5
Line 310: A stateful function that increases a state by a given value (State.idr)
Line 311: Needed for the State type
Line 312: Assigns the value of the state to current
Line 313: Updates the value of the state
Line 314: Generic types of State
Line 315: If you check the types of get and put, you’ll see that they use constrained generic
Line 316: types:
Line 317: *TreeLabelState> :t get
Line 318: get : MonadState stateType m => m stateType
Line 319: *TreeLabelState> :t put
Line 320: put : MonadState stateType m => stateType -> m ()
Line 321: This gives library authors more flexibility in defining stateful programs. The details of
Line 322: the MonadState interface are beyond the scope of this book, but you can read more
Line 323: in the Idris library documentation (http://idris-lang.org/documentation). In this exam-
Line 324: ple, you can read m as State stateType.
Line 325: Although State encapsulates sequences of stateful operations, internally it’s
Line 326: defined using pure functions. Essentially, it encapsulates the implementation pattern
Line 327: you used to pass the state around in treeLabelWith.
Line 328: 
Line 329: --- 페이지 357 ---
Line 330: 331
Line 331: Working with mutable state
Line 332: Using State, you can reimplement treeLabelWith, hiding the internal details of state
Line 333: management and only reading and updating the stream of labels when necessary. 
Line 334: 12.1.4 Tree traversal with State
Line 335: The next listing shows how you can define treeLabelWith by keeping the stream of
Line 336: labels as state, reading it to get the next label for a node.
Line 337: treeLabelWith : Tree a -> State (Stream labelType) (Tree (labelType, a))
Line 338: treeLabelWith Empty = pure Empty
Line 339: treeLabelWith (Node left val right)
Line 340: = do left_labelled <- treeLabelWith left
Line 341: (this :: rest) <- get
Line 342: put rest
Line 343: right_labelled <- treeLabelWith right
Line 344: pure (Node left_labelled (this, val) right_labelled)
Line 345: In this definition, you can see the details of the labeling algorithm more clearly than
Line 346: in the previous definition. Here, you leave the internal details of state management to
Line 347: the implementation of State.
Line 348:  In order to run this function and actually carry out the tree labeling, you’ll need to
Line 349: provide an initial state. The following listing defines a treeLabel function that initial-
Line 350: izes the state with an infinite stream of integers, counting upwards from 1.
Line 351: treeLabel : Tree a -> Tree (Integer, a)
Line 352: treeLabel tree = evalState (treeLabelWith tree) [1..]
Line 353: As before, you can test this at the REPL. It behaves the same way as the previous imple-
Line 354: mentation of treeLabel on the test input:
Line 355: *TreeLabelState> flatten (treeLabel testTree)
Line 356: [(1, "Jim"),
Line 357: (2, "Fred"),
Line 358: (3, "Sheila"),
Line 359: (4, "Alice"),
Line 360: (5, "Bob"),
Line 361: (6, "Eve")] : List (Integer, String)
Line 362: Like IO, which you first encountered in chapter 5, State gives you a way of writing
Line 363: functions with side effects (here, modifying mutable state) by describing sequences of
Line 364: operations and executing them separately:
Line 365: Listing 12.6
Line 366: Defining treeLabelWith as a sequence of stateful operations 
Line 367: (TreeLabelState.idr)
Line 368: Listing 12.7
Line 369: Top-level function to label tree nodes, depth first, left to right 
Line 370: (TreeLabelState.idr)
Line 371: Gets the current stream of labels. You’ll use 
Line 372: the first label, this, to label the current node.
Line 373: Sets the new stream of labels to be
Line 374: the tail of the current stream, rest
Line 375: evalState discards the 
Line 376: final state, so it returns 
Line 377: only the labeled tree.
Line 378: 
Line 379: --- 페이지 358 ---
Line 380: 332
Line 381: CHAPTER 12
Line 382: Writing programs with state
Line 383: A value of type IO ty is a description of a sequence of interactive actions pro-
Line 384: ducing a result of type ty. It’s executed by the runtime system by compilation,
Line 385: or by :exec at the REPL. 
Line 386: A value of type State stateType ty is a description of a sequence of actions that
Line 387: read and write a state of type stateType, producing a result of type ty. It’s exe-
Line 388: cuted by using one of runState, execState, or evalState.
Line 389: Many interesting programs follow this pattern, defining a type for describing
Line 390: sequences of commands and a separate function for executing those commands.
Line 391: Indeed, you’ve already seen one in chapter 11, when you defined the ConsoleIO type
Line 392: for describing indefinitely running interactive programs. You’ll see more examples in
Line 393: the remaining chapters, so in the rest of this chapter we’ll look at how to implement
Line 394: custom types for representing state and interaction. 
Line 395: Exercises
Line 396: 1
Line 397: Write a function that updates a state by applying a function to the current state: 
Line 398: update : (stateType -> stateType) -> State stateType ()
Line 399: You should be able to use update to reimplement increase: 
Line 400: increase : Nat -> State Nat ()
Line 401: increase x = update (+x)
Line 402: You can test your answer at the REPL as follows: 
Line 403: *ex_12_1> runState (increase 5) 89
Line 404: ((), 94) : ((), Nat)
Line 405:  2
Line 406: Write a function that uses State to count the number of occurrences of Empty in a
Line 407: tree. It should have the following type: 
Line 408: countEmpty : Tree a -> State Nat ()
Line 409: You can test your answer at the REPL with testTree as follows: 
Line 410: *ex_12_1> execState (countEmpty testTree) 0
Line 411: 7 : Nat
Line 412:  3
Line 413: Write a function that counts the number of occurrences of both Empty and Node in a
Line 414: tree, using State to store the count of each in a pair. It should have the following
Line 415: type: 
Line 416: countEmptyNode : Tree a -> State (Nat, Nat) ()
Line 417: You can test your answer at the REPL with testTree as follows: 
Line 418: *ex_12_1> execState (countEmptyNode testTree) (0, 0)
Line 419: (7, 6) : (Nat, Nat)
Line 420: 
Line 421: --- 페이지 359 ---
Line 422: 333
Line 423: A custom implementation of State
Line 424: 12.2
Line 425: A custom implementation of State
Line 426: In the previous section, you saw that the State type gives you a generic way of imple-
Line 427: menting algorithms that use state. You used it to maintain a stream of labels as local
Line 428: mutable state, which you could access by reading (using get) and writing (using put)
Line 429: as necessary. Like IO, which separates the description of an interactive program from its
Line 430: execution at runtime, State separates the description of a stateful program from its
Line 431: execution with a concrete state.
Line 432:  We’ll look at more examples of the same pattern, separating the description of a
Line 433: program from its execution, in the remaining chapters, so before we go any further,
Line 434: let’s explore how we can define the State type ourselves, along with runState for exe-
Line 435: cuting stateful operations. In this section, you’ll see one way of defining State, and
Line 436: how to provide implementations of some interfaces for State: Functor, Applicative,
Line 437: and Monad. By implementing these interfaces, you’ll be able to use some generic
Line 438: library functions with State.
Line 439: 12.2.1 Defining State and runState
Line 440: The following listing shows one way you could define State by hand, with a Get data
Line 441: constructor for describing the operation that reads state, and a Put data constructor
Line 442: for describing the operation that writes state.
Line 443: data State : (stateType : Type) -> Type -> Type where
Line 444: Get : State stateType stateType
Line 445: Put : stateType -> State stateType ()
Line 446: Pure : ty -> State stateType ty
Line 447: Bind : State stateType a -> (a -> State stateType b) -> State stateType b
Line 448: Listing 12.8
Line 449: A type for describing stateful operations (TreeLabelType.idr)
Line 450: Describes the operation 
Line 451: that gets the current state
Line 452: Describes the operation 
Line 453: that puts a new state
Line 454: An operation that 
Line 455: produces a value
Line 456: Sequences stateful operations, passing the 
Line 457: result of the first as the input to the next
Line 458: Naming conventions reminder
Line 459: Remember that, by convention, type and data constructor names in Idris begin with
Line 460: a capital letter. I won’t deviate from this convention here, so if you want the same
Line 461: names as those exported by Control.Monad.State, you’ll need to define the fol-
Line 462: lowing functions:
Line 463: get : State stateType stateType
Line 464: get = Get
Line 465: put : stateType -> State stateType ()
Line 466: put = Put
Line 467: pure : ty -> State stateType ty
Line 468: pure = Pure
Line 469: 
Line 470: --- 페이지 360 ---
Line 471: 334
Line 472: CHAPTER 12
Line 473: Writing programs with state
Line 474: You can support do notation for State by defining (>>=). You can do this either by
Line 475: implementing the Monad interface for (>>=), or by defining (>>=) directly:
Line 476: (>>=) : State stateType a -> (a -> State stateType b) -> State stateType b
Line 477: (>>=) = Bind
Line 478: Using this version of State, and defining the functions get, put, and pure, which
Line 479: directly use the data constructors, listing 12.9 shows how you can define treeLabel-
Line 480: With. This version is exactly the same as the previous one, as you’d expect, because it
Line 481: uses the same names for the functions that manipulate the state.
Line 482: treeLabelWith : Tree a -> State (Stream labelType) (Tree (labelType, a))
Line 483: treeLabelWith Empty = Pure Empty
Line 484: treeLabelWith (Node left val right)
Line 485: = do left_labelled <- treeLabelWith left
Line 486: (this :: rest) <- get
Line 487: put rest
Line 488: right_labelled <- treeLabelWith right
Line 489: pure (Node left_labelled (this, val) right_labelled)
Line 490: In order to run it, you’ll need to define a function that converts the description of the
Line 491: stateful operations into the tree-labeling function. The following listing shows the
Line 492: definition of runState, which takes a description of a stateful program and an initial
Line 493: state, and returns the value produced by the stateful program and a final state.
Line 494: runState : State stateType a -> (st : stateType) -> (a, stateType)
Line 495: runState Get st = (st, st)
Line 496: runState (Put newState) st = ((), newState)
Line 497: Listing 12.9
Line 498: Defining treeLabelWith as a sequence of stateful operations 
Line 499: (TreeLabelType.idr)
Line 500: Listing 12.10
Line 501: Running a labeling operation (TreeLabelType.idr)
Line 502: Implementing interfaces for State
Line 503: Defining (>>=) means that you can use do notation for programs in State. As you
Line 504: saw in chapter 7, (>>=) is also a method of the Monad interface, which also
Line 505: requires implementations of the Functor and Applicative interfaces. It’s
Line 506: defined here as a standalone function to avoid the need to implement Functor and
Line 507: Applicative first for this example.
Line 508: Where possible, it’s a very good idea to implement the Monad interface instead,
Line 509: because that gives you access to several constrained generic functions defined by
Line 510: the Idris library. For example, you’d be able to use the when function, which executes
Line 511: an operation when a condition is met, and traverse, which applies a computation
Line 512: across a structure. You’ll see how to do this for State in section 12.2.2.
Line 513: Labels
Line 514: the left
Line 515: subtree
Line 516: Gets the next label for labeling 
Line 517: the node from the stream
Line 518: Labels the
Line 519: right subtree
Line 520: Returns a pair of the value produced by the 
Line 521: stateful operations, and the final state
Line 522: Put produces the unit value and
Line 523: updates the state to the new value.
Line 524: Get produces the
Line 525: current state and
Line 526: leaves the state
Line 527: unchanged.
Line 528: 
Line 529: --- 페이지 361 ---
Line 530: 335
Line 531: A custom implementation of State
Line 532: runState (Pure x) st = (x, st)
Line 533: runState (Bind cmd prog) st = let (val, nextState) = runState cmd st in
Line 534: runState (prog val) nextState
Line 535: When you run sequences of stateful operations, defined using Bind, you need to take
Line 536: the nextState state returned by running cmd, and pass it to runState when executing
Line 537: the rest of the operations. You calculate the rest of the operations by taking the val
Line 538: returned by running cmd and passing it to prog. This encapsulates the state manage-
Line 539: ment that you had to implement by hand (three times!) in your first implementation
Line 540: of treeLabelWith, and it’s similar to the way the Control.Monad.State module
Line 541: implements State itself.
Line 542:  The following listing shows a definition of treeLabel that uses the new implemen-
Line 543: tation of treeLabelWith, initializing the stream with [1..].
Line 544: treeLabel : Tree a -> Tree (Integer, a)
Line 545: treeLabel tree = fst (runState (treeLabelWith tree) [1..])
Line 546: 12.2.2 Defining Functor, Applicative, 
Line 547: and Monad implementations for State
Line 548: Implementing (>>=) for State means that you can use do notation, which gives a
Line 549: clear, readable notation for writing functions that describe sequences of operations.
Line 550: But do notation is all it gives us.
Line 551:  Rather than defining (>>=) as a standalone function, it’s a good idea to implement
Line 552: the Functor, Applicative, and Monad interfaces for State. In addition to providing
Line 553: do notation via the Monad interface, this will give you access to generic functions
Line 554: defined in the library. For example, when and traverse are generic functions. In the
Line 555: context of IO, they behave as follows:
Line 556: 
Line 557: when evaluates a computation if a condition is True. It could be used to run
Line 558: some IO actions only on a specific user input. 
Line 559: 
Line 560: traverse is similar to map and applies a computation across a structure. For
Line 561: example, you could print every element of a List to the console.
Line 562: You can find out more about these functions, especially their types, with :doc. The fol-
Line 563: lowing listing shows them in action in the context of an IO computation.
Line 564: crew : List String
Line 565: crew = ["Lister", "Rimmer", "Kryten", "Cat"]
Line 566: Listing 12.11 The tree-labeling function, which calls run with an initial stream of labels
Line 567: (TreeLabelType.idr)
Line 568: Listing 12.12
Line 569: Using when and traverse (Traverse.idr)
Line 570: Runs the first stateful command and then runs
Line 571: the rest of the program with the updated state
Line 572: and the output of the first command
Line 573: Uses fst to extract the 
Line 574: labeled tree and 
Line 575: discard the final state
Line 576: 
Line 577: --- 페이지 362 ---
Line 578: 336
Line 579: CHAPTER 12
Line 580: Writing programs with state
Line 581: main : IO ()
Line 582: main = do putStr "Display Crew? "
Line 583: x <- getLine
Line 584: when (x == "yes") $
Line 585: do traverse putStrLn crew
Line 586: pure ()
Line 587: putStrLn "Done"
Line 588: If you implement Functor, Applicative, and Monad for State, you’ll be able to use
Line 589: these and other similar functions in functions that use State. The next listing shows an
Line 590: example of what you can do, giving a function that adds Integers from a list to a run-
Line 591: ning total, provided the Integer is positive. At the moment, this will fail to type-check.
Line 592: addIfPositive : Integer -> State Integer Bool
Line 593: addIfPositive val = do when (val > 0) $
Line 594: do current <- get
Line 595: put (current + val)
Line 596: pure (val > 0)
Line 597: addPositives : List Integer -> State Integer Nat
Line 598: addPositives vals = do added <- traverse addIfPositive vals
Line 599: pure (length (filter id added))
Line 600: This will fail because you don’t have implementations of Functor or Applicative for
Line 601: State:
Line 602: StateMonad.idr:42:15:
Line 603: When checking right hand side of addIfPositive with expected type
Line 604: State Integer Bool
Line 605: When checking an application of function Main.>>=:
Line 606: Can't find implementation for Applicative (State Integer)
Line 607: Listing 12.13
Line 608: Adding positive integers from a list to a state (StateMonad.idr)
Line 609: Evaluates the computation after 
Line 610: $ only if this condition is true. $ 
Line 611: is the application operator.
Line 612: For everything in the crew 
Line 613: list, evaluates putStrLn
Line 614: The application operator $
Line 615: Remember from chapter 10 that the $ operator is an infix operator that applies a
Line 616: function to an argument. Its primary purpose is to reduce the need for bracketing. In
Line 617: listing 12.12, you could also have written the application of when with explicit brack-
Line 618: ets, as follows:
Line 619: when (x == "yes")
Line 620: (do traverse putStrLn crew
Line 621: pure ())
Line 622: Increments the state with the 
Line 623: given value, if it’s positive
Line 624: Returns
Line 625: whether the
Line 626: integer was
Line 627: successfully
Line 628: added
Line 629: For every integer in vals, the value in 
Line 630: added corresponds to whether that 
Line 631: integer was added to the state.
Line 632: filter id added gives the elements of added
Line 633: that are True, so this returns the number of
Line 634: successfully added Integers.
Line 635: 
Line 636: --- 페이지 363 ---
Line 637: 337
Line 638: A custom implementation of State
Line 639: Your ultimate goal here is to implement Monad for State, which also requires imple-
Line 640: mentations of Functor and Applicative. The next listing shows the Monad interface,
Line 641: as defined in the Prelude. 
Line 642: interface Applicative m => Monad (m : Type -> Type) where
Line 643: (>>=) : m a -> (a -> m b) -> m b
Line 644: join : m (m a) -> m a
Line 645: Both methods, (>>=) and join, have default definitions, so you can implement Monad
Line 646: by defining one or both of these. Here, we’ll only use (>>=).
Line 647:  If you want to provide an implementation for Monad, you also need to implement
Line 648: Applicative, because it’s a parent interface of Monad. Similarly, Applicative has a
Line 649: parent interface, Functor. The following listing shows both interfaces as defined in
Line 650: the Prelude.
Line 651: interface Functor (f : Type -> Type) where
Line 652: map : (func : a -> b) -> f a -> f b
Line 653: interface Functor f => Applicative (f : Type -> Type) where
Line 654: pure
Line 655: : a -> f a
Line 656: (<*>) : f (a -> b) -> f a -> f b
Line 657: Listing 12.14
Line 658: The Monad interface
Line 659: Listing 12.15
Line 660: The Functor and Applicative interfaces
Line 661: Passes the output of the first 
Line 662: operation as the input to the second
Line 663: “Flattens” a nested 
Line 664: structure. See the sidebar.
Line 665: The join method
Line 666: We haven’t looked at join in detail, but you can use it to flatten nested structures
Line 667: into a single structure. For example, there are implementations of Monad for List
Line 668: and Maybe, so you can try join on examples of each:
Line 669: Idris> join [[1,2,3], [4,5,6]]
Line 670: [1, 2, 3, 4, 5, 6] : List Integer
Line 671: Idris> join (Just (Just "One"))
Line 672: Just "One" : Maybe String
Line 673: Idris> join (Just (Nothing {a=String}))
Line 674: Nothing : Maybe String
Line 675: For List, join will concatenate the nested lists. For Maybe, join will find the sin-
Line 676: gle value nested in the structure, if any.
Line 677: Applies a function to an 
Line 678: argument, where the function and 
Line 679: argument are inside a structure
Line 680: 
Line 681: --- 페이지 364 ---
Line 682: 338
Line 683: CHAPTER 12
Line 684: Writing programs with state
Line 685: The (<*>) method allows you to, for example, have a stateful function that returns a
Line 686: function (of type a -> b), have another stateful function that returns an argument (of
Line 687: type a), and apply the function to the argument.
Line 688:  You can begin by implementing Functor as follows:
Line 689: 1
Line 690: Type, define—Write the implementation header and create a skeleton definition
Line 691: of map. Remember that you can create skeleton definitions for interface meth-
Line 692: ods by pressing Ctrl-Alt-A with the cursor over the interface name: 
Line 693: Functor (State stateType) where
Line 694: map func x = ?Functor_rhs_1
Line 695:  2
Line 696: Type, refine—The type of the ?Functor_rhs_1 hole tells you that x is a stateful
Line 697: computation: 
Line 698: stateType : Type
Line 699: b : Type
Line 700: a : Type
Line 701: func : a -> b
Line 702: x : State stateType a
Line 703: --------------------------------------
Line 704: Functor_rhs_1 : State stateType b
Line 705: You can continue the definition by extracting the value from the computation x
Line 706: using Bind: 
Line 707: Functor (State stateType) where
Line 708: map func x = Bind x (\val => ?Functor_rhs_1)
Line 709: 3
Line 710: Refine—To complete the definition, pass val to func, and use Pure to convert
Line 711: the result to a stateful computation: 
Line 712: Functor (State stateType) where
Line 713: map func x = Bind x (\val => Pure (func val))
Line 714: Listing 12.16 shows the definitions of Applicative and Monad for State. You imple-
Line 715: ment Applicative in a way similar to Functor, using Bind to extract the values you
Line 716: need from stateful computations.
Line 717: Applicative (State stateType) where
Line 718: pure = Pure
Line 719: (<*>) f a = Bind f (\f' =>
Line 720: Bind a (\a' =>
Line 721: Pure (f' a')))
Line 722: Monad (State stateType) where
Line 723: (>>=) = Bind
Line 724: You’ve used Bind in the implementations of Functor and Applicative because you
Line 725: don’t have do notation available yet. You need a Monad implementation to provide it,
Line 726: Listing 12.16
Line 727: Implementing Applicative and Monad for State (StateMonad.idr)
Line 728: Gets the function 
Line 729: to apply from f
Line 730: Gets the argument to pass 
Line 731: to the function from a
Line 732: Applies the function to the 
Line 733: argument and creates a stateful 
Line 734: computation containing the result
Line 735: Applies
Line 736: Bind
Line 737: directly
Line 738: 
Line 739: --- 페이지 365 ---
Line 740: 339
Line 741: A custom implementation of State
Line 742: and you need to have Functor and Applicative implementations to have a Monad
Line 743: implementation.
Line 744:  But you could use do notation by defining all the implementations together, in a
Line 745: mutual block, as listing 12.17 shows. In a mutual block, definitions can refer to each
Line 746: other, so the implementations of Functor and Applicative can rely on the imple-
Line 747: mentation of Monad.
Line 748: mutual
Line 749: Functor (State stateType) where
Line 750: map func x = do val <- x
Line 751: pure (func val)
Line 752: Applicative (State stateType) where
Line 753: pure = Pure
Line 754: (<*>) f a = do f' <- f
Line 755: a' <- a
Line 756: pure (f' a')
Line 757: Monad (State stateType) where
Line 758: (>>=) = Bind
Line 759: Now that you’ve implemented these interfaces, you can try the earlier definition of
Line 760: addPositives from listing 12.13:
Line 761: *StateMonad> runState (addPositives [-4, 3, -8, 9, 8]) 0
Line 762: (3, 20) : (Nat, Integer)
Line 763: You’ve now seen how to encapsulate the details of state manipulation by describing
Line 764: sequences of stateful operations as State, and executing them using runState. You’ve
Line 765: also seen how to implement Functor, Applicative, and Monad for State.
Line 766: Listing 12.17 Defining Functor, Applicative, and Monad implementations together
Line 767: (StateMonad.idr)
Line 768: do notation implementation 
Line 769: given by (>>=) from Monad.
Line 770: pure given
Line 771: by
Line 772: definition
Line 773: from
Line 774: Applicative.
Line 775: Each implementation needs to begin in the same 
Line 776: column to be within the scope of the mutual block.
Line 777: The Effects library: combining State, IO, and other side effects
Line 778: Given that you have Monad implementations for State and IO, sequencing stateful
Line 779: computations and interactive computations respectively, it’s reasonable to wonder
Line 780: whether you can sequence both at once, in the same function—what about interac-
Line 781: tive programs that also manipulate state?
Line 782: You’ll see one way to do this in the next section. As a more general solution, though,
Line 783: Idris provides a library called Effects that supports combining different kinds of
Line 784: side effects like State and IO in types, as well as other effects such as exceptions
Line 785: and nondeterminism. You can find more details in the Effects library tutorial
Line 786: (http://idris-lang.org/documentation/effects).
Line 787: 
Line 788: --- 페이지 366 ---
Line 789: 340
Line 790: CHAPTER 12
Line 791: Writing programs with state
Line 792:  The states you’ve used in the examples so far have been fairly small: a single stream
Line 793: of labels, or a single Integer. More generally, state can get fairly complex:
Line 794: State may consist of several complex components, stored as a record. We’ll dis-
Line 795: cuss this in the rest of this chapter, where you’ll see how to write a complete
Line 796: interactive program with state.
Line 797: You might want to use a dependent type in your State, in which case updating
Line 798: the state will also update its type! For example, if you add an element to a Vect
Line 799: 8 Int, it would become a Vect 9 Int. We’ll discuss this in the next chapter.
Line 800: An advantage of writing a type that expresses sequences of commands, along with a
Line 801: function for running those commands, is that you can make the command type as
Line 802: precise as you need. As you’ll see in the next section, you can describe precisely the set
Line 803: of commands you need for a specific application, including commands for interaction
Line 804: at the console and commands for reading and writing components of the applica-
Line 805: tion’s state. In the next chapter, you’ll see how you can precisely describe in its type the
Line 806: effect each command has on a system’s state. 
Line 807: 12.3
Line 808: A complete program with state: working with records
Line 809: In the previous chapter, you implemented an arithmetic quiz that presented multipli-
Line 810: cation problems to the user and kept track of the numbers of correct answers and
Line 811: questions asked. In this section, we’ll write a refined version, with the following
Line 812: improvements:
Line 813: We’ll add a difficulty setting, which specifies the largest number allowed when
Line 814: generating questions.
Line 815: Instead of passing the current score as an argument to the quiz function, main-
Line 816: taining the state by hand, we’ll extend the Command type with commands for giv-
Line 817: ing access to the current score and the difficulty setting.
Line 818: To write this refined version, we’ll need to rethink how to represent the game’s state.
Line 819: We’ll do this using record types. You’ve already seen some the use of records to repre-
Line 820: sent the data store in chapter 6, with similar examples in chapters 7 and 10. As an
Line 821: application’s state grows, though, it can make sense to divide its state into several hier-
Line 822: archical records.
Line 823:  You’ll see how to define and use nested records, how to update records with a con-
Line 824: cise syntax, and how to use a record to store the state of the interactive quiz program.
Line 825: First, though, we’ll revisit the Command type from chapter 11 and see how you can
Line 826: extend it to support reading and writing system state, in a way similar to the custom
Line 827: State type defined in the previous section.
Line 828: 12.3.1 Interactive programs with state: the arithmetic quiz revisited
Line 829: In chapter 11, you defined a Command data type, representing the commands you could
Line 830: use in console I/O programs, and a ConsoleIO type, representing possibly infinite
Line 831: interactive processes. You used this to implement an arithmetic quiz, presenting
Line 832: 
Line 833: --- 페이지 367 ---
Line 834: 341
Line 835: A complete program with state: working with records
Line 836: multiplication problems for a user to answer. Like State, which describes the opera-
Line 837: tions Get and Put for reading and writing state, Command describes the operations Get-
Line 838: Line and PutStr for reading from and writing to the console. The following listing
Line 839: recaps the definitions of Command and ConsoleIO.
Line 840: data Command : Type -> Type where
Line 841: PutStr : String -> Command ()
Line 842: GetLine : Command String
Line 843: Pure : ty -> Command ty
Line 844: Bind : Command a -> (a -> Command b) -> Command b
Line 845: data ConsoleIO : Type -> Type where
Line 846: Quit : a -> ConsoleIO a
Line 847: Do : Command a -> (a -> Inf (ConsoleIO b)) -> ConsoleIO b
Line 848: namespace CommandDo
Line 849: (>>=) : Command a -> (a -> Command b) -> Command b
Line 850: (>>=) = Bind
Line 851: namespace ConsoleDo
Line 852: (>>=) : Command a -> (a -> Inf (ConsoleIO b)) -> ConsoleIO b
Line 853: (>>=) = Do
Line 854: IMPLEMENTING MONAD FOR COMMAND
Line 855: As with State, you could implement
Line 856: Functor, Applicative, and Monad for Command instead of implementing
Line 857: (>>=) directly. As an exercise, try providing implementations of each. As I
Line 858: noted in the last chapter, however, you can’t provide a Monad implementa-
Line 859: tion for ConsoleIO because the type of ConsoleDo.(>>=) doesn’t fit.
Line 860: Like runState, which takes a description of stateful operations and returns the result
Line 861: of executing those operations with an initial state, run takes a description of interac-
Line 862: tive operations and executes them in IO. Listing 12.19 recaps the run function.
Line 863: Remember that you limit how long interactive programs can run by using the Fuel
Line 864: type, and you add a nontotal function, forever, that allows a total interactive program
Line 865: to run indefinitely, while only introducing a single nontotal function. 
Line 866: data Fuel = Dry | More (Lazy Fuel)
Line 867: forever : Fuel
Line 868: forever = More forever
Line 869: runCommand : Command a -> IO a
Line 870: runCommand (PutStr x) = putStr x
Line 871: runCommand GetLine = getLine
Line 872: runCommand (Pure val) = pure val
Line 873: runCommand (Bind c f) = do res <- runCommand c
Line 874: runCommand (f res)
Line 875: Listing 12.18
Line 876: Interactive programs supporting only console I/O (ArithState.idr)
Line 877: Listing 12.19
Line 878: Running interactive programs (ArithState.idr)
Line 879: Defines the valid commands 
Line 880: for an interactive program
Line 881: Interactive programs 
Line 882: that either produce a 
Line 883: result with Quit, or loop 
Line 884: indefinitely
Line 885: Defines (>>=) 
Line 886: to support do 
Line 887: notation for 
Line 888: Command and 
Line 889: ConsoleIO
Line 890: Executes an 
Line 891: interactive command
Line 892: 
Line 893: --- 페이지 368 ---
Line 894: 342
Line 895: CHAPTER 12
Line 896: Writing programs with state
Line 897: run : Fuel -> ConsoleIO a -> IO (Maybe a)
Line 898: run fuel (Quit val) = do pure (Just val)
Line 899: run (More fuel) (Do c f) = do res <- runCommand c
Line 900: run fuel (f res)
Line 901: run Dry p = pure Nothing
Line 902: If you want your interactive programs to be able to read and write state, in addition to
Line 903: reading from and writing to the console, you can extend the Command type with addi-
Line 904: tional commands for manipulating state, and process those commands just as you did
Line 905: with State. For the arithmetic game, we’ll need to do the following:
Line 906: Get random numbers for the questions, given the game’s difficulty setting.
Line 907: Read the current game state so that you can display the score.
Line 908: Update the game state so that you can update the score according to the user’s
Line 909: answers.
Line 910: The next listing shows how you can extend the Command data type to include these com-
Line 911: mands. There’s no need to update ConsoleIO, because it merely sequences Commands.
Line 912: GameState : Type
Line 913: data Command : Type -> Type where
Line 914: PutStr : String -> Command ()
Line 915: GetLine : Command String
Line 916: GetRandom : Command Int
Line 917: GetGameState : Command GameState
Line 918: PutGameState : GameState -> Command ()
Line 919: Pure : ty -> Command ty
Line 920: Bind : Command a -> (a -> Command b) -> Command b
Line 921: GameState is undefined for the moment, so you can’t yet complete run or runCommand.
Line 922: You can, however, add pattern clauses with holes for the extra commands so that the
Line 923: totality checker is satisfied:
Line 924: runCommand : Command a -> IO a
Line 925: runCommand (PutStr x) = putStr x
Line 926: runCommand GetLine = getLine
Line 927: runCommand (Pure val) = pure val
Line 928: runCommand (Bind c f) = do res <- runCommand c
Line 929: runCommand (f res)
Line 930: runCommand (PutGameState x) = ?runCommand_rhs_1
Line 931: runCommand GetGameState = ?runCommand_rhs_2
Line 932: runCommand GetRandom = ?runCommand_rhs_3
Line 933: ADDING MISSING CASES
Line 934: After you’ve added constructors to Command, you can
Line 935: use Ctrl-Alt-A with the cursor over runCommand in the type declaration to add
Line 936: the new pattern clauses for runCommand.
Line 937: Listing 12.20
Line 938: Extending the Command type to support game state (ArithState.idr)
Line 939: Executes an interactive 
Line 940: program as long as 
Line 941: fuel remains
Line 942: This is a placeholder. You’ll 
Line 943: define GameState shortly.
Line 944: Returns a random number based on 
Line 945: the game’s current difficulty level
Line 946: Returns the current game state
Line 947: Sets the game state
Line 948: 
Line 949: --- 페이지 369 ---
Line 950: 343
Line 951: A complete program with state: working with records
Line 952: You’ll use the GameState type to store the game’s state. Before you implement the
Line 953: refined quiz, therefore, you’ll need to consider how to define GameState.
Line 954: 12.3.2 Complex state: defining nested records
Line 955: In the refined quiz implementation, you’ll use GameState to store the following:
Line 956: The current score, consisting of the number of questions answered correctly
Line 957: and the number attempted
Line 958: The difficulty setting
Line 959: When there are several components to a program’s state like this, it often makes sense
Line 960: to use a record type. Records are convenient because they give rise to projection func-
Line 961: tions, which allow you to inspect the fields of the record. You can also nest records;
Line 962: the following listing shows how you can represent the current score as a record, and
Line 963: the overall game state as a record, including the nested score record as a field.
Line 964: record Score where
Line 965: constructor MkScore
Line 966: correct : Nat
Line 967: attempted : Nat
Line 968: record GameState where
Line 969: constructor MkGameState
Line 970: score : Score
Line 971: difficulty : Int
Line 972: initState : GameState
Line 973: initState = MkGameState (MkScore 0 0) 12
Line 974: Defining Score and GameState as records automatically generates projection func-
Line 975: tions for each field: correct, attempted, score, and difficulty. For example, you
Line 976: can get the difficulty level like this:
Line 977: *ArithState> difficulty initState
Line 978: 12 : Int
Line 979: Or you can get the number of correct answers so far:
Line 980: *ArithState> correct (score initState)
Line 981: 0 : Nat
Line 982: Listing 12.21
Line 983: Representing a game state as nested records (ArithState.idr)
Line 984: Current score has fields for the 
Line 985: number of correct answers and 
Line 986: attempted questions
Line 987: The game state record includes the 
Line 988: score record as a field in that record.
Line 989: The initial game state is a score of 0 
Line 990: out of 0, with a difficulty of 12.
Line 991: Records and namespaces
Line 992: When you define a record, the projection functions are defined in their own name-
Line 993: space, given by the name of the record. For example, the score function is defined
Line 994: in a new GameState namespace, as you can see with :doc at the REPL:
Line 995: *ArithState> :doc score
Line 996: Main.GameState.score : (rec : GameState) -> Score
Line 997: 
Line 998: --- 페이지 370 ---
Line 999: 344
Line 1000: CHAPTER 12
Line 1001: Writing programs with state
Line 1002: The following listing shows how you can use projection functions to define an imple-
Line 1003: mentation of Show for GameState.
Line 1004: Show GameState where
Line 1005: show st = show (correct (score st)) ++ "/" ++
Line 1006: show (attempted (score st)) ++ "\n" ++
Line 1007: "Difficulty: " ++ show (difficulty st)
Line 1008: You can try this at the REPL, using printLn to display the initial game state:
Line 1009: *ArithState> :exec printLn initState
Line 1010: 0/0
Line 1011: Difficulty: 12
Line 1012: Records, therefore, give you a convenient notation for inspecting field values, but when
Line 1013: you write programs that use records to hold state, you’ll also need to update fields. In
Line 1014: the quiz, for example, you’ll need to increment the score and the number of ques-
Line 1015: tions attempted. 
Line 1016: 12.3.3 Updating record field values
Line 1017: Idris is a pure functional language, so you won’t update record fields in-place. Instead,
Line 1018: when we say we’re updating a record, we really mean that we’re constructing a new
Line 1019: record containing the contents of the old record with a single field changed. For
Line 1020: example, the following listing shows one way to return a new record with the difficulty
Line 1021: field updated, using pattern matching.
Line 1022: Listing 12.22
Line 1023: Show implementation for GameState (ArithState.idr)
Line 1024: (continued)
Line 1025: This allows the same field name to be used multiple times within the same module.
Line 1026: For example, you can use a field called title in two different records in the same
Line 1027: file, Record.idr:
Line 1028: record Book where
Line 1029: constructor MkBook
Line 1030: title : String
Line 1031: author : String
Line 1032: record Album where
Line 1033: constructor MkAlbum
Line 1034: title : String
Line 1035: tracks : List String
Line 1036: Idris will decide which version of title to use, according to context:
Line 1037: *Record> title (MkBook "Breakfast of Champions" "Kurt Vonnegut")
Line 1038: "Breakfast of Champions" : String
Line 1039: 
Line 1040: --- 페이지 371 ---
Line 1041: 345
Line 1042: A complete program with state: working with records
Line 1043:  
Line 1044: setDifficulty : Nat -> GameState -> GameState
Line 1045: setDifficulty newDiff (MkGameState score _) = MkGameState score newDiff
Line 1046: If the record has a lot of fields, this can get unwieldy very quickly, because you’d need to
Line 1047: write update functions for every field. Not only that, if you were to add a field to a record,
Line 1048: you’d need to modify all of the update functions. Idris therefore provides a built-in syn-
Line 1049: tax for updating fields in records. Here’s an implementation of setDifficulty using
Line 1050: record-update syntax.
Line 1051: setDifficulty : Nat -> GameState -> GameState
Line 1052: setDifficulty newDiff state = record { difficulty = newDiff } state
Line 1053: Figure 12.3 shows the components of the record-update syntax. Note in particular
Line 1054: that the record-update syntax itself is first-class, where record is a keyword that begins
Line 1055: a record update, so the record update has a type. Here, the update has a function
Line 1056: type, GameState -> GameState, so you can also implement setDifficulty as follows: 
Line 1057: setDifficulty : Nat -> GameState -> GameState
Line 1058: setDifficulty newDiff = record { difficulty = newDiff }
Line 1059: You can update nested record fields in a similar way, by giving the path to the field
Line 1060: you’d like to update. The following listing shows how you can write the correct and
Line 1061: wrong functions, which update the score.
Line 1062: addWrong : GameState -> GameState
Line 1063: addWrong state
Line 1064: = record { score->attempted = attempted (score state) + 1 } state
Line 1065: addCorrect : GameState -> GameState
Line 1066: addCorrect state
Line 1067: Listing 12.23
Line 1068: Setting a record field by pattern matching (ArithState.idr)
Line 1069: Listing 12.24
Line 1070: Setting a record field using record-update syntax (ArithState.idr)
Line 1071: Listing 12.25
Line 1072: Setting nested record fields using record-update syntax (ArithState.idr)
Line 1073: record { difficulty = newDiff } state
Line 1074: Field to
Line 1075: update
Line 1076: New
Line 1077: value
Line 1078: Record
Line 1079: to update
Line 1080: Function to update
Line 1081: a record field, of type
Line 1082: GameState -> GameState
Line 1083: Figure 12.3
Line 1084: Syntax for returning a 
Line 1085: new record with a field updated
Line 1086: Updates the number of attempted
Line 1087: questions by adding 1 to the current value
Line 1088: 
Line 1089: --- 페이지 372 ---
Line 1090: 346
Line 1091: CHAPTER 12
Line 1092: Writing programs with state
Line 1093: = record { score->correct = correct (score state) + 1,
Line 1094: score->attempted = attempted (score state) + 1 } state
Line 1095: The score->attempted notation gives the path to the field you’d like to update, with
Line 1096: the outermost field name first. So, in this example, you’d like to update the attempted
Line 1097: field of the score field of the state record. 
Line 1098: 12.3.4 Updating record fields by applying functions
Line 1099: The record-update syntax offers a concise notation for specifying a path to a particu-
Line 1100: lar record field. It’s still a little inconvenient, though, because you’ve needed to
Line 1101: explicitly write the path to each field twice, in different notations:
Line 1102: First, to find the field to update, using the score->correct path notation
Line 1103: Second, to find the old value, using a function application, correct (score state)
Line 1104: Idris therefore provides a notation for updating record fields by directly applying a
Line 1105: function to the current value of the field. The next listing shows a concise way of
Line 1106: updating the nested record fields in GameState.
Line 1107: addWrong : GameState -> GameState
Line 1108: addWrong = record { score->attempted $= (+1) }
Line 1109: addCorrect : GameState -> GameState
Line 1110: addCorrect = record { score->correct $= (+1),
Line 1111: score->attempted $= (+1) }
Line 1112: UPDATING RECORDS WITH $=
Line 1113: You saw the $ operator, which applies a function
Line 1114: to an argument, in chapter 10. The $= syntax arises from a combination of
Line 1115: the function application operator $ and the record-update syntax.
Line 1116: This syntax gives you a concise and convenient way of writing functions that update
Line 1117: nested record fields, which makes it easier to write programs that manipulate state.
Line 1118: Moreover, because it doesn’t use pattern matching, it’s independent of any other
Line 1119: fields in a record, so even if you add fields to the GameState record, addWrong and
Line 1120: addCorrect will work without modifications. 
Line 1121: 12.3.5 Implementing the quiz
Line 1122: Using your new Command type and the GameState record, you can implement the arith-
Line 1123: metic quiz by reading and updating the state as necessary. The next listing shows an
Line 1124: outline of the quiz implementation, leaving holes for correct and wrong, which,
Line 1125: respectively, process a correct answer and a wrong answer.
Line 1126: Listing 12.26
Line 1127: Updating nested record fields by directly applying functions to the 
Line 1128: current value of the field (ArithState.idr)
Line 1129: You can update multiple fields in one go,
Line 1130: separating the updates with a comma.
Line 1131: Updates the number of correct answers 
Line 1132: by adding 1 to the current value
Line 1133: The $= operator in the field 
Line 1134: update means that the new 
Line 1135: field value is calculated by 
Line 1136: applying the function (+1) to 
Line 1137: the current value.
Line 1138: 
Line 1139: --- 페이지 373 ---
Line 1140: 347
Line 1141: A complete program with state: working with records
Line 1142:  
Line 1143: mutual
Line 1144: correct : ConsoleIO GameState
Line 1145: correct = ?correct_rhs
Line 1146: wrong : Int -> ConsoleIO GameState
Line 1147: wrong ans = ?wrong_rhs
Line 1148: readInput : (prompt : String) -> Command Input
Line 1149: quiz : ConsoleIO GameState
Line 1150: quiz = do num1 <- GetRandom
Line 1151: num2 <- GetRandom
Line 1152: st <- GetGameState
Line 1153: PutStr (show st ++ "\n")
Line 1154: input <- readInput (show num1 ++ " * " ++ show num2 ++ "? ")
Line 1155: case input of
Line 1156: Answer answer => if answer == num1 * num2
Line 1157: then correct
Line 1158: else wrong (num1 * num2)
Line 1159: QuitCmd => Quit st
Line 1160: This is similar to the implementation of quiz at the end of chapter 11, but instead of
Line 1161: passing the stream of random numbers and the score as arguments, you treat each of
Line 1162: them as state that you read and write as required. This simplifies the definition of
Line 1163: quiz, at the cost of making the definition of ConsoleIO more complex.
Line 1164:  The next listing shows how you can implement correct and wrong, each modify-
Line 1165: ing the state using addCorrect and addWrong, respectively, as defined in the previous
Line 1166: section.
Line 1167: correct : ConsoleIO GameState
Line 1168: correct = do PutStr "Correct!\n"
Line 1169: st <- GetGameState
Line 1170: PutGameState (addCorrect st)
Line 1171: quiz
Line 1172: wrong : Int -> ConsoleIO GameState
Line 1173: wrong ans = do PutStr ("Wrong, the answer is " ++ show ans ++ "\n")
Line 1174: st <- GetGameState
Line 1175: PutGameState (addWrong st)
Line 1176: quiz
Line 1177: At this stage, you have a complete description of an interactive arithmetic quiz that
Line 1178: retrieves random numbers and the current score from the state. It’s also total:
Line 1179: *ArithState> :total quiz
Line 1180: Main.quiz is Total
Line 1181: Listing 12.27
Line 1182: Implementing the arithmetic quiz (ArithState.idr)
Line 1183: Listing 12.28
Line 1184: Processing correct and wrong answers by updating the game state
Line 1185: (ArithState.idr)
Line 1186: readInput was defined at 
Line 1187: the end of chapter 11. It 
Line 1188: displays a prompt and reads 
Line 1189: and parses user input.
Line 1190: Gets the next random 
Line 1191: number from the state
Line 1192: Gets the game
Line 1193: state so you
Line 1194: can display the
Line 1195: current score
Line 1196: and difficulty
Line 1197: Processes a 
Line 1198: correct answer
Line 1199: Processes a 
Line 1200: wrong answer
Line 1201: Sets a new game state with 
Line 1202: an updated record
Line 1203: Continues
Line 1204: with
Line 1205: the quiz
Line 1206: Sets a new game state with 
Line 1207: an updated record
Line 1208: 
Line 1209: --- 페이지 374 ---
Line 1210: 348
Line 1211: CHAPTER 12
Line 1212: Writing programs with state
Line 1213: But to run quiz, you’ll need to extend runCommand to support your new commands. 
Line 1214: 12.3.6 Running interactive and stateful programs: executing the quiz
Line 1215: As with the runState function you wrote for processing operations in the custom
Line 1216: State type in section 12.2, the updated run function will need to process the current
Line 1217: game state. It will also need to read from a stream of random numbers (for Get-
Line 1218: Random) and perform console I/O. The following listing shows how these are all cap-
Line 1219: tured in a new type for runCommand.
Line 1220: runCommand : Stream Int ->
Line 1221: GameState ->
Line 1222: Command a ->
Line 1223: IO (a, Stream Int, GameState)
Line 1224: runCommand = ?runCommand_rhs
Line 1225: Listing 12.30 gives the complete definition of runCommand. Note that, in each case, you
Line 1226: need to return the result of the command as well as show how each command affects
Line 1227: the random number stream and the game state.
Line 1228: runCommand : Stream Int -> GameState -> Command a ->
Line 1229: IO (a, Stream Int, GameState)
Line 1230: runCommand rnds state (PutStr x) = do putStr x
Line 1231: pure ((), rnds, state)
Line 1232: runCommand rnds state GetLine = do str <- getLine
Line 1233: pure (str, rnds, state)
Line 1234: runCommand (val :: rnds) state GetRandom
Line 1235: = pure (getRandom val (difficulty state), rnds, state)
Line 1236: where
Line 1237: getRandom : Int -> Int -> Int
Line 1238: getRandom val max with (divides val max)
Line 1239: getRandom val 0 | DivByZero = 1
Line 1240: getRandom ((max * div) + rem) max | (DivBy prf) = abs rem + 1
Line 1241: runCommand rnds state GetGameState
Line 1242: = pure (state, rnds, state)
Line 1243: runCommand rnds state (PutGameState newState)
Line 1244: = pure ((), rnds, newState)
Line 1245: Listing 12.29
Line 1246: A new type and skeleton definition for runCommand (ArithState.idr)
Line 1247: Listing 12.30
Line 1248: The complete definition of runCommand (ArithState.idr)
Line 1249: The stream of available random 
Line 1250: numbers, before running the command
Line 1251: The game state, 
Line 1252: before running 
Line 1253: the command
Line 1254: The command to run
Line 1255: Returns the result of the 
Line 1256: command and an updated 
Line 1257: stream of random numbers 
Line 1258: and game state
Line 1259: No change to 
Line 1260: the random 
Line 1261: number 
Line 1262: stream or 
Line 1263: game state
Line 1264: Takes the
Line 1265: first random
Line 1266: number from
Line 1267: the stream and
Line 1268: converts it
Line 1269: to a number
Line 1270: between 1 and
Line 1271: the difficulty
Line 1272: level
Line 1273: Remember to import 
Line 1274: Data.Primitives.Views 
Line 1275: to be able to use 
Line 1276: divides.
Line 1277: The result of the command 
Line 1278: is the current game state.
Line 1279: The argument to PutGameState 
Line 1280: becomes the new game state.
Line 1281: 
Line 1282: --- 페이지 375 ---
Line 1283: 349
Line 1284: A complete program with state: working with records
Line 1285: runCommand rnds state (Pure val)
Line 1286: = pure (val, rnds, state)
Line 1287: runCommand rnds state (Bind c f)
Line 1288: = do (res, newRnds, newState) <- runCommand rnds state c
Line 1289: runCommand newRnds newState (f res)
Line 1290: Similarly, you need to update run to take a stream of random integers and an initial
Line 1291: game state. Like runCommand, run also returns the result of running the program,
Line 1292: along with the updated stream and game state. Here’s the new implementation of
Line 1293: run, which supports the game state.
Line 1294: run : Fuel -> Stream Int -> GameState -> ConsoleIO a ->
Line 1295: IO (Maybe a, Stream Int, GameState)
Line 1296: run fuel rnds state (Quit val) = do pure (Just val, rnds, state)
Line 1297: run (More fuel) rnds state (Do c f)
Line 1298: = do (res, newRnds, newState) <- runCommand rnds state c
Line 1299: run fuel newRnds newState (f res)
Line 1300: run Dry rnds state p = pure (Nothing, rnds, state)
Line 1301: As in chapter 11, you use Fuel to say how long you’re willing to allow a potentially
Line 1302: infinite interactive program to run, so the portion of the return type that represents
Line 1303: the result of running the program, of type ConsoleIO a, has type Maybe a, to capture
Line 1304: the possibility of running out of Fuel.
Line 1305:  Finally, the next listing shows how you update the main program to initialize the
Line 1306: stream of random numbers and the game state.
Line 1307: randoms : Int -> Stream Int
Line 1308: randoms seed = let seed' = 1664525 * seed + 1013904223 in
Line 1309: (seed' `shiftR` 2) :: randoms seed'
Line 1310: partial
Line 1311: main : IO ()
Line 1312: main = do seed <- time
Line 1313: (Just score, _, state) <-
Line 1314: run forever (randoms (fromInteger seed)) initState quiz
Line 1315: | _ => putStrLn "Ran out of fuel"
Line 1316: putStrLn ("Final score: " ++ show state)
Line 1317: As with the implementation of quiz at the end of chapter 11, you separate terminat-
Line 1318: ing sequences of commands (using the Command type) from possible nonterminating
Line 1319: sequences of console I/O operations (using the ConsoleIO type). In addition, you
Line 1320: extend the Command type to allow reading and writing of the game’s state much like
Line 1321: Listing 12.31
Line 1322: Running a ConsoleIO program consisting of a potentially infinite
Line 1323: stream of Command (ArithState.idr)
Line 1324: Listing 12.32
Line 1325: A main program that initializes the arithmetic quiz with a random number
Line 1326: stream and an initial state (ArithState.idr)
Line 1327: No change to the random 
Line 1328: number stream or game state
Line 1329: Takes the states from running 
Line 1330: the first command and passes 
Line 1331: them on to the next command
Line 1332: Generates an infinite stream of random numbers
Line 1333: Needed because you use forever
Line 1334: Remember to import System to be able to use time.
Line 1335: 
Line 1336: --- 페이지 376 ---
Line 1337: 350
Line 1338: CHAPTER 12
Line 1339: Writing programs with state
Line 1340: the implementation of State. If you define a specific type for the commands that an
Line 1341: application can execute, you can make that type as precise as you need, possibly
Line 1342: describing the effect of each operation on an abstraction of a system’s state. You’ll see
Line 1343: more of what you can achieve by following this pattern and the guarantees you can
Line 1344: make about stateful, interactive programs in the next chapter. 
Line 1345: Exercises
Line 1346: 1
Line 1347: Write an updateGameState function with the following type: 
Line 1348: updateGameState : (GameState -> GameState) -> Command ()
Line 1349: You can test it by using it in the definitions of correct and wrong instead of Get-
Line 1350: GameState and PutGameState. For example:
Line 1351: correct : ConsoleIO GameState
Line 1352: correct = do PutStr "Correct!\n"
Line 1353: updateGameState addCorrect
Line 1354: quiz
Line 1355:  2
Line 1356: Implement the Functor, Applicative, and Monad interfaces for Command.
Line 1357:  3
Line 1358: You could define records for representing an article on a social news website as fol-
Line 1359: lows, along with the number of times the article has been upvoted or downvoted: 
Line 1360: record Votes where
Line 1361: constructor MkVotes
Line 1362: upvotes : Integer
Line 1363: downvotes : Integer
Line 1364: record Article where
Line 1365: constructor MkArticle
Line 1366: title : String
Line 1367: url : String
Line 1368: score : Votes
Line 1369: initPage : (title : String) -> (url : String) -> Article
Line 1370: initPage title url = MkArticle title url (MkVotes 0 0)
Line 1371: Write a function to calculate the overall score of a given article, where the score is
Line 1372: calculated from the number of downvotes subtracted from the number of upvotes.
Line 1373: It should have the following type: 
Line 1374: getScore : Article -> Integer
Line 1375: You can test it with the following example articles: 
Line 1376: badSite : Article
Line 1377: badSite = MkArticle "Bad Page" "http://example.com/bad" (MkVotes 5 47)
Line 1378: goodSite : Article
Line 1379: goodSite = MkArticle "Good Page" "http://example.com/good" (MkVotes 101 7)
Line 1380: At the REPL, you should see the following: 
Line 1381: *ex_12_3> getScore goodSite
Line 1382: 94 : Integer
Line 1383: 
Line 1384: --- 페이지 377 ---
Line 1385: 351
Line 1386: Summary
Line 1387: *ex_12_3> getScore badSite
Line 1388: -42 : Integer
Line 1389:  4
Line 1390: Write addUpvote and addDownvote functions that modify an article’s score up or
Line 1391: down. They should have the following types: 
Line 1392: addUpvote : Article -> Article
Line 1393: addDownvote : Article -> Article
Line 1394: You can test these at the REPL as follows: 
Line 1395: *ex_12_3> addUpvote goodSite
Line 1396: MkArticle "Good Page"
Line 1397: "http://example.com/good"
Line 1398: (MkVotes 102 7) : Article
Line 1399: *ex_12_3> addDownvote badSite
Line 1400: MkArticle "Bad Page"
Line 1401: "http://example.com/bad"
Line 1402: (MkVotes 5 48) : Article
Line 1403: *ex_12_3> getScore (addUpvote goodSite)
Line 1404: 95 : Integer
Line 1405: 12.4
Line 1406: Summary
Line 1407: Many algorithms read and write state. For example, when labeling the nodes of
Line 1408: a tree in depth-first order, you can keep track of the state of the labels while tra-
Line 1409: versing the tree.
Line 1410: You can manage state by using the generic State type to describe operations on
Line 1411: the state along with a runState function to execute those operations.
Line 1412: You can define your own State type as a sequence of Get and Put operations.
Line 1413: Defining Functor, Applicative, and Monad for the State type gives you access
Line 1414: to several generic functions from the Idris library.
Line 1415: When writing interactive programs with state, you can define a Command type to
Line 1416: describe an interface consisting of console I/O and state management operations.
Line 1417: Record types can represent more complex nested state.
Line 1418: Idris provides a concise syntax for assigning new values to fields in nested
Line 1419: records.
Line 1420: Idris also provides a syntax (using $=) for updating a field in a nested record by
Line 1421: applying a function to the value in that field.