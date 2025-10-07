Line 1: 
Line 2: --- 페이지 317 ---
Line 3: 291
Line 4: Streams and processes:
Line 5: working with infinite data
Line 6: The functions we’ve written in this book so far have worked in batch mode, process-
Line 7: ing all of their inputs and then returning an output. In the previous chapter, we
Line 8: also spent some time discussing why termination is important, and you learned how
Line 9: to use views to help you write programs that are guaranteed to terminate.
Line 10:  But input data doesn’t always arrive in a batch, and you’ll often want to write
Line 11: programs that don’t terminate, running indefinitely. For example, it can be conve-
Line 12: nient to think of input data to an interactive program (such as keypresses, mouse
Line 13: movements, and so on) as a continuous stream of data, processed one element at a
Line 14: time, leading to a stream of output data. In reality, many programs are, in effect,
Line 15: stream processors:
Line 16: This chapter covers
Line 17: Generating and processing streams of data
Line 18: Distinguishing terminating from productive total 
Line 19: functions
Line 20: Defining total interactive processes using infinite 
Line 21: streams
Line 22: 
Line 23: --- 페이지 318 ---
Line 24: 292
Line 25: CHAPTER 11
Line 26: Streams and processes: working with infinite data
Line 27: A read-eval-print loop, such as the Idris environment, processes a potentially
Line 28: infinite stream of user commands, giving an output stream of responses.
Line 29: A web server processes a potentially infinite stream of HTTP requests, giving an
Line 30: output stream of responses to be sent over the network.
Line 31: A real-time game processes a potentially infinite stream of commands from a
Line 32: controller, giving an output stream of audiovisual actions.
Line 33: Furthermore, even when you’re writing pure functions that don’t interact with exter-
Line 34: nal data sources or devices, streams allow you to write reusable program components
Line 35: by separating the production of data from the consumption of data. For example, sup-
Line 36: pose you’re writing a function to determine the square root of a number. You can do
Line 37: this by producing an infinite list of successively closer approximations to a solution,
Line 38: and then writing a separate function to consume that list, finding the first approxima-
Line 39: tion within the desired bounds.
Line 40: PRODUCING AND CONSUMING DATA
Line 41: A common theme in this chapter is the dis-
Line 42: tinction between programs that consume (or process) data, and programs that
Line 43: produce data. All the functions you’ve seen in this book so far have been con-
Line 44: sumers of data, and in the last chapter we looked at using views to help us
Line 45: write functions that are guaranteed to terminate when consuming data.
Line 46: When you’re writing terminating functions, however, consuming data is only
Line 47: part of the story: a function that generates an infinite stream is never going to
Line 48: terminate, after all. As you’ll see, Idris checks that functions that generate
Line 49: streams are guaranteed to be productive, so that any function that consumes
Line 50: the output of a stream generator will always have data to process.
Line 51: The kinds of programs we write in practice often have a terminating component, pro-
Line 52: cessing and responding to user input, and a nonterminating component, which is an
Line 53: infinite loop that repeatedly invokes the terminating component. In this chapter,
Line 54: you’ll see how to write programs that manage this distinction, both producing and
Line 55: consuming potentially infinite data. We’ll start with one of the most common infinite
Line 56: structures, streams, and later look at how to define total functions describing interac-
Line 57: tive functions that execute indefinitely.
Line 58: 11.1
Line 59: Streams: generating and processing infinite lists
Line 60: Streams are infinite sequences of values, and you can process one value at a time. In
Line 61: this section, you’ll see how to write functions that produce an infinite sequence of data,
Line 62: as required, and how to write functions that consume finite portions of data produced
Line 63: as a stream.
Line 64:  As a first example, to illustrate the ideas behind streams, we’ll look at how to gen-
Line 65: erate an infinite sequence of numbers, 0, 1, 2, 3, 4, ..., and how to process them as
Line 66: needed to label elements in a list, as illustrated in figure 11.1.
Line 67:  
Line 68: 
Line 69: --- 페이지 319 ---
Line 70: 293
Line 71: Streams: generating and processing infinite lists
Line 72: You might use such a function after sorting some data, for example, to attach an
Line 73: explicit index to the data. As you’ll see, you can use streams to cleanly separate the
Line 74: production of an infinite list of labels from the consumption of the labels you need
Line 75: for a specific input list.
Line 76:  As well as showing you how to define potentially infinite data types, I’ll also intro-
Line 77: duce the Stream data type, provided by the Prelude, and we’ll briefly look at some
Line 78: functions on Streams. Finally, we’ll look at a larger example using a stream of random
Line 79: numbers to implement an arithmetic game.
Line 80: 11.1.1 Labeling elements in a List
Line 81: Suppose you want to write a function that labels every element of a List with an inte-
Line 82: ger indicating its position in the list, as in figure 11.1. That is, something like this:
Line 83: label : List a -> List (Integer, a)
Line 84: Running this function on some examples should give the following results:
Line 85: *Streams> label ['a', 'b', 'c']
Line 86: [(0, 'a'), (1, 'b'), (2, 'c')] : List (Integer, Char)
Line 87: *Streams> label ["Anderson", "Botham", "Willis", "Trueman"]
Line 88: [(0, "Anderson"),
Line 89: (1, "Botham"),
Line 90: (2, "Willis"),
Line 91: (3, "Trueman")] : List (Integer, String)
Line 92: The following listing shows one way to write label by writing a helper function,
Line 93: labelFrom that takes the label for the first element of the list, and then labels the
Line 94: remainder of the list, incrementing the label.
Line 95: 0, 1, 2, 3, 4, ...
Line 96: [Anderson, Botham, Willis, Trueman]
Line 97: [(0, Anderson), (1, Botham), (2, Willis), (3, Trueman)]
Line 98: Initial portion
Line 99: of stream
Line 100: Unused remainder
Line 101: of stream
Line 102: Labeled list
Line 103: Initial list
Line 104: Figure 11.1
Line 105: Labeling the elements of a List by taking elements from an infinite 
Line 106: stream of numbers. The stream contains an infinite number of elements, but you only 
Line 107: take as many as you need to label the elements in the finite list.
Line 108: 
Line 109: --- 페이지 320 ---
Line 110: 294
Line 111: CHAPTER 11
Line 112: Streams and processes: working with infinite data
Line 113:  
Line 114: labelFrom : Integer -> List a -> List (Integer, a)
Line 115: labelFrom lbl [] = []
Line 116: labelFrom lbl (val :: vals) = (lbl, val) :: labelFrom (lbl + 1) vals
Line 117: label : List a -> List (Integer a)
Line 118: label = labelFrom 0
Line 119: This works as required, but the definition of labelFrom combines two components:
Line 120: labeling each element, and generating the label itself. An alternative way of writing
Line 121: label would allow you to reuse these two components separately—you could write
Line 122: two functions:
Line 123: 
Line 124: countFrom—Generates an infinite stream of numbers, counting upwards from a
Line 125: given starting point.
Line 126: 
Line 127: labelWith—Takes an infinite stream of labels, and pairs each label with a corre-
Line 128: sponding element in a finite list. It therefore only consumes as much of the
Line 129: infinite stream as necessary to label the elements in the list.
Line 130: A natural way to try to write countFrom might be to generate a List of Integer from a
Line 131: given starting point:
Line 132: countFrom : Integer -> List Integer
Line 133: countFrom n = n :: countFrom (n + 1)
Line 134: When Idris runs a compiled program, however, it fully evaluates the arguments to a
Line 135: function before it evaluates the function itself. So, unfortunately, if you try to pass the
Line 136: result of countFrom to a function that expects a List, that function will never run
Line 137: because the result of countFrom will never be fully evaluated. If you ask Idris whether
Line 138: this definition of countFrom is total, it will tell you that there’s a problem: 
Line 139: *StreamFail> :total countFrom
Line 140: Main.countFrom is possibly not total due to recursive path:
Line 141: Main.countFrom, Main.countFrom
Line 142: You can see that countFrom will never terminate, because it makes a recursive call for
Line 143: every input, but to write labelWith you’ll only need a finite portion of the result of
Line 144: countFrom. What you really need to know about countFrom, therefore, is not that it
Line 145: always terminates, but rather that it will always produce as many numbers as you need.
Line 146: That is, you need to know that it’s productive and is guaranteed to generate an indefi-
Line 147: nitely long sequence of numbers.
Line 148:  As you’ll see in the next section, you can use types to distinguish between those
Line 149: expressions for which evaluation is guaranteed to terminate and those expressions for
Line 150: which evaluation is guaranteed to keep producing new values, marking arguments to
Line 151: a data structure as potentially infinite. 
Line 152: Listing 11.1
Line 153: Labeling each element of a list with an integer (Label.idr)
Line 154: Labels the first element of
Line 155: the list, and then
Line 156: recursively labels the tail
Line 157: Initializes
Line 158: the label
Line 159: at 0
Line 160: 
Line 161: --- 페이지 321 ---
Line 162: 295
Line 163: Streams: generating and processing infinite lists
Line 164: 11.1.2 Producing an infinite list of numbers
Line 165: To generate an infinite list of numbers and consume only the finite portion of the list
Line 166: that you need, you can use a new data type, Inf, for marking the potentially infinite
Line 167: parts of the structure.
Line 168:  You’ll see more details of how Inf works shortly. First, though, let’s take a look at a
Line 169: data type of infinite lists that uses Inf.
Line 170: data InfList : Type -> Type where
Line 171: (::) : (value : elem) -> Inf (InfList elem) -> InfList elem
Line 172: %name InfList xs, ys, zs
Line 173: InfList is similar to the List generic type, with two significant differences:
Line 174: There’s no Nil constructor, only a (::) constructor, so there’s no way to end
Line 175: the list. 
Line 176: The recursive argument is wrapped in a new data type, Inf, that marks the argu-
Line 177: ment as potentially infinite.
Line 178: To manipulate potentially infinite computations, you can use the Delay and Force
Line 179: functions. Listing 11.3 gives the types of Delay and Force. The idea is that you can use
Line 180: Delay and Force to control exactly when a subexpression is evaluated, so that you only
Line 181: calculate the finite portion of an infinite list that’s required for a specific function.
Line 182: Inf : Type -> Type
Line 183: Delay : (value : ty) -> Inf ty
Line 184: Force : (computation : Inf ty) -> ty
Line 185: The following listing shows how you can define countFrom, generating an infinite list
Line 186: of Integers from a given starting value.
Line 187: countFrom : Integer -> InfList Integer
Line 188: countFrom x = x :: Delay (countFrom (x + 1))
Line 189: Listing 11.2
Line 190: A data type of infinite lists (InfList.idr)
Line 191: Listing 11.3
Line 192: The Inf abstract data type, for delaying potentially infinite computations
Line 193: Listing 11.4
Line 194: Defining countFrom as an infinite list (InfList.idr)
Line 195: There’s no Nil constructor, 
Line 196: so no end to the list.
Line 197: The Inf generic type marks
Line 198: the InfList elem argument
Line 199: as potentially infinite.
Line 200: Name hints for interactive editing.
Line 201: Inf is a generic type of potentially 
Line 202: infinite computations.
Line 203: Delay is a function that states that 
Line 204: its argument should only be 
Line 205: evaluated when its result is forced.
Line 206: Force is a function that returns the 
Line 207: result from a delayed computation.
Line 208: The Delay means that the 
Line 209: remainder of the list will only 
Line 210: be calculated when explicitly 
Line 211: requested using Force.
Line 212: 
Line 213: --- 페이지 322 ---
Line 214: 296
Line 215: CHAPTER 11
Line 216: Streams and processes: working with infinite data
Line 217: If you try evaluating countFrom 0 at the REPL to generate an infinite list counting
Line 218: upwards from 0, you’ll see the effect of the Delay:
Line 219: *InfList> countFrom 0
Line 220: 0 :: Delay (countFrom 1) : InfList Integer
Line 221: You can see that the Idris evaluator has left the argument to Delay unevaluated. The
Line 222: evaluator treats Force and Delay specially: it will only evaluate an argument to Delay
Line 223: when explicitly requested to by a Force. As a result, despite there being a recursive call
Line 224: to countFrom on every input, evaluation at the REPL still terminates. Idris even agrees
Line 225: that it’s total:
Line 226: *InfList> :total countFrom
Line 227: Main.countFrom is Total
Line 228: TERMINOLOGY: RECURSION AND CORECURSION, DATA AND CODATA
Line 229: You may hear
Line 230: Idris programmers referring to functions such as countFrom as corecursive
Line 231: rather than recursive, and infinite lists as codata rather than data. The distinc-
Line 232: tion between data and codata is that data is finite and is intended to be con-
Line 233: sumed, whereas codata is potentially infinite and is intended to be produced.
Line 234: Whereas recursion operates by taking data and breaking it down toward a base
Line 235: case, corecursion operates by starting at a base case and building up codata.
Line 236: It may seem surprising that Idris considers countFrom to be total, given that it pro-
Line 237: duces an infinite structure. Before we continue discussing how to work with infinite
Line 238: lists, therefore, it’s worth investigating in more detail what it means for a function to
Line 239: be total. 
Line 240: 11.1.3 Digression: what does it mean for a function to be total?
Line 241: If a function is total, it will never crash due to a missing case (that is, all well-typed
Line 242: inputs are covered), and it will always return a well-typed result within a finite time.
Line 243: The functions you’ve written in previous chapters have all taken finite data as inputs,
Line 244: so they’re total as long as they terminate for all inputs. But now that you’ve seen the
Line 245: Inf type, you’re able to write functions that produce infinite data, and these functions
Line 246: don’t terminate! We’ll therefore need to refine our understanding of what it means
Line 247: for a function to be total.
Line 248:  Functions that produce infinite data can be used as components of terminating
Line 249: functions, provided they’ll always produce a new piece of data on request. In the case
Line 250: of countFrom, it will always produce a new Integer before making a delayed recursive
Line 251: call. 
Line 252:  Figure 11.2 illustrates the structure of countFrom. The delayed recursive call to
Line 253: countFrom is an argument to (::), meaning that countFrom will always produce at
Line 254: least one element of an infinite list before making a recursive call. Therefore, any
Line 255: function that consumes the result of countFrom will always have data to work with.
Line 256: 
Line 257: --- 페이지 323 ---
Line 258: 297
Line 259: Streams: generating and processing infinite lists
Line 260:  
Line 261: Idris considers a function to be total if there are patterns that cover all well-typed
Line 262: inputs, and it can determine that one of the following conditions holds:
Line 263: When there’s a recursive call (or a sequence of mutually recursive calls), there’s
Line 264: a decreasing argument that converges toward a base case.
Line 265: When there’s a recursive call as an argument to Delay, the delayed call will
Line 266: always be an argument to a data constructor (or sequence of nested data con-
Line 267: structors) after evaluation, for all inputs.
Line 268: We discussed the first of these conditions in the previous chapter. The second condi-
Line 269: tion allows us to use functions like countFrom in a terminating function. To illustrate
Line 270: this further, it’s helpful to see how the resulting infinite list is used. As an example,
Line 271: let’s write a function that consumes a finitely long prefix of an InfList. 
Line 272: 11.1.4 Processing infinite lists
Line 273: A function that generates an InfList is total provided that it’s guaranteed to keep
Line 274: producing data whenever data is required. You can see how this works by writing a
Line 275: program that calculates a finite list from the prefix of an infinite list:
Line 276: getPrefix : (count : Nat) -> InfList ty -> List ty
Line 277: countFrom n = n :: Delay (countFrom (n + 1))
Line 278: Produced value
Line 279: Delayed
Line 280: recursive call
Line 281: Figure 11.2
Line 282: Producing values of an infinite 
Line 283: structure. The Delay means that Idris will only 
Line 284: make the recursive call to countFrom when 
Line 285: it’s required by Force.
Line 286: Total functions defined
Line 287: A total function is a function that, for all well-typed inputs, does one of the following: 
Line 288: Terminates with a well-typed result
Line 289: Produces a non-empty finite prefix of a well-typed infinite result in finite time
Line 290: We can describe total functions as either terminating or productive. The halting prob-
Line 291: lem is the difficulty of determining whether a specific program terminates or not, and,
Line 292: thanks to Alan Turing, we know that it’s impossible in general to write a program that
Line 293: solves the halting problem. In other words, Idris can’t determine whether one of these
Line 294: conditions holds for all total functions. Instead, it makes a conservative approxima-
Line 295: tion by analyzing a function’s syntax.
Line 296: 
Line 297: --- 페이지 324 ---
Line 298: 298
Line 299: CHAPTER 11
Line 300: Streams and processes: working with infinite data
Line 301: getPrefix returns a List consisting of the first count items from an infinite list. It
Line 302: works by recursively taking the next element from the infinite list as long as it needs
Line 303: more elements. You can define it with the following steps:
Line 304: 1
Line 305: Define—First, case-split on the count argument: 
Line 306: getPrefix : (count : Nat) -> InfList a -> List a
Line 307: getPrefix Z xs = ?getPrefix_rhs_1
Line 308: getPrefix (S k) xs = ?getPrefix_rhs_2
Line 309:  2
Line 310: Refine—If you’re taking zero elements from the infinite list, return an empty
Line 311: list: 
Line 312: getPrefix : (count : Nat) -> InfList a -> List a
Line 313: getPrefix Z xs = []
Line 314: getPrefix (S k) xs = ?getPrefix_rhs_2
Line 315:  3
Line 316: Define—If you’re taking more than one element, you’ll case-split on the infinite
Line 317: list and then add the first value in the infinite list as the first element of the
Line 318: result. 
Line 319: getPrefix : (count : Nat) -> InfList a -> List a
Line 320: getPrefix Z xs = []
Line 321: getPrefix (S k) (value :: xs) = value :: ?getPrefix_rhs_1
Line 322: 4
Line 323: Type, refine—If you look at the type of the hole, ?getPrefix_rhs_1, you’ll see
Line 324: the following: 
Line 325: a : Type
Line 326: k : Nat
Line 327: value : a
Line 328: xs : Inf (InfList a)
Line 329: --------------------------------------
Line 330: getPrefix_rhs_1 : List a
Line 331: You can see from the type of xs that it’s an infinite list that has not yet been
Line 332: computed, because it’s an infinite list wrapped in an Inf. To complete the defi-
Line 333: nition, you can Force the computation of xs and recursively get its prefix: 
Line 334: getPrefix : (count : Nat) -> InfList a -> List a
Line 335: getPrefix Z xs = []
Line 336: getPrefix (S k) (value :: xs) = value :: getPrefix k (Force xs)
Line 337: The resulting definition is total, according to Idris:
Line 338: *InfList> :total getPrefix
Line 339: Main.getPrefix is Total
Line 340: Even though one of the inputs is potentially infinite, getPrefix will only evaluate as
Line 341: much as is necessary to retrieve count elements from the infinite list. Because count is
Line 342: a finite number, getPrefix will always terminate as long as the InfList is guaranteed
Line 343: to continue producing new elements. 
Line 344:  In practice, you can omit calls to Delay and Force and let Idris insert them where
Line 345: required. If, during type checking, Idris encounters a value of type Inf ty when it
Line 346: 
Line 347: --- 페이지 325 ---
Line 348: 299
Line 349: Streams: generating and processing infinite lists
Line 350: requires a value of type ty, it will add an implicit call to Force. Similarly, if it encounters
Line 351: a ty when it requires an Inf ty, it will add an implicit call to Delay. The following listing
Line 352: shows how you can define countFrom and getPrefix using implicit Force and Delay.
Line 353: countFrom : Integer -> InfList Integer
Line 354: countFrom x = x :: countFrom (x + 1)
Line 355: getPrefix : Nat -> InfList a -> List a
Line 356: getPrefix Z x = []
Line 357: getPrefix (S k) (x :: xs) = x :: getPrefix k xs
Line 358: You can therefore treat Inf as an annotation on a type, mark the parts of a data struc-
Line 359: ture that may be infinite, and let the Idris type checker manage the details of when
Line 360: computations must be delayed or forced.
Line 361:  Now that you’ve seen how to separate the production of data, using countFrom to
Line 362: generate an infinite list of numbers, from the consumption of data, using a function
Line 363: like getPrefix, we can revisit the definition of label. Rather than using our own
Line 364: InfList data type and countFrom, we’ll use a data type defined in the Prelude for this
Line 365: purpose: Stream. 
Line 366: 11.1.5 The Stream data type
Line 367: Listing 11.6 shows the definition of Stream in the Prelude. It has the same structure as
Line 368: the definition of InfList you saw in the previous section. Additionally, the Prelude
Line 369: provides several useful functions for building and manipulating Streams, some of
Line 370: which this listing also shows.
Line 371: data Stream : Type -> Type where
Line 372: (::) : (value : elem) -> Inf (Stream elem) -> Stream elem
Line 373: repeat : elem -> Stream elem
Line 374: take : (n : Nat) -> (xs : Stream elem) -> List elem
Line 375: iterate : (f : elem -> elem) -> (x : elem) -> Stream elem
Line 376: You can see the functions repeat, take, and iterate in action at the REPL. For exam-
Line 377: ple, repeat generates an infinite sequence of an element, delayed until specifically
Line 378: requested:
Line 379: Idris> repeat 94
Line 380: 94 :: Delay (repeat 94) : Stream Integer
Line 381: Listing 11.5
Line 382: Taking a finite portion of an infinite list, with implicit Force and Delay
Line 383: (InfList.idr)
Line 384: Listing 11.6
Line 385: The Stream data type and some functions, defined in the Prelude
Line 386: The Idris type checker implicitly inserts 
Line 387: the Delay required for the recursive call.
Line 388: The Idris type checker implicitly 
Line 389: inserts the Force required for xs.
Line 390: Generates an 
Line 391: infinite list of a 
Line 392: specific element
Line 393: Takes a specific number of elements 
Line 394: from the start of a stream
Line 395: Generates a stream by
Line 396: repeatedly applying a function
Line 397: 
Line 398: --- 페이지 326 ---
Line 399: 300
Line 400: CHAPTER 11
Line 401: Streams and processes: working with infinite data
Line 402: Like getPrefix on InfList, take takes a prefix of a Stream of a specific length:
Line 403: Idris> take 10 (repeat 94)
Line 404: [94, 94, 94, 94, 94, 94, 94, 94, 94, 94] : List Integer
Line 405: iterate applies a function repeatedly, generating a stream of the results. For exam-
Line 406: ple, starting at 0 and repeatedly applying (+1) leads to a sequence of increasing inte-
Line 407: gers, like countFrom:
Line 408: Idris> take 10 (iterate (+1) 0)
Line 409: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] : List Integer
Line 410: Putting all of this together, the following listing shows how to define label using
Line 411: iterate to generate an infinite sequence of integer labels, and a labelWith function
Line 412: that consumes enough of an infinite sequence of labels to attach a label to each ele-
Line 413: ment of a List.
Line 414: labelWith : Stream labelType -> List a -> List (labelType, a)
Line 415: labelWith lbs [] = []
Line 416: labelWith (lbl :: lbls) (val :: vals) = (lbl, val) :: labelWith lbls vals
Line 417: label : List a -> List (Integer, a)
Line 418: label = labelWith (iterate (+1) 0)
Line 419: Listing 11.7
Line 420: Labeling each element of a List using a Stream (Streams.idr)
Line 421: Syntactic sugar for stream generation
Line 422: Idris provides a concise syntax for generating streams of numbers, similar to the syn-
Line 423: tax for lists:
Line 424: Idris> take 10 [1..]
Line 425: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] : List Integer
Line 426: The syntax [1..] generates a Stream counting upwards from 1. This works for any
Line 427: countable numeric type, as in the following example:
Line 428: Idris> the (List Int) take 10 [1..]
Line 429: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] : List Int
Line 430: You can also change the increment:
Line 431: Idris> the (List Int) (take 10 [1,3..])
Line 432: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19] : List Int
Line 433: Uses a generic type variable, labelType, because 
Line 434: labelWith never inspects the label itself
Line 435: Nothing left to label, so 
Line 436: returns an empty list
Line 437: Labels the first element of the
Line 438: list with the first element in
Line 439: the stream of labels
Line 440: 
Line 441: --- 페이지 327 ---
Line 442: 301
Line 443: Streams: generating and processing infinite lists
Line 444: In this definition, you separate the two components of generating the labels and
Line 445: assigning labels to each element of the list.
Line 446:  You can even give a more generic type to labelWith, taking a Stream labelType
Line 447: rather than a Stream Integer, and allow labeling by any type for which you can gener-
Line 448: ate a Stream. For example, the cycle function generates a Stream that repeats a given
Line 449: sequence:
Line 450: *Streams> take 10 $ cycle ["a", "b", "c"]
Line 451: ["a", "b", "c", "a", "b", "c", "a", "b", "c", "a"] : List String
Line 452: Using cycle to generate a Stream, you could label each element of a List with a
Line 453: cycling sequence of labels, repeated as many times as necessary to label the entire list:
Line 454: *Streams> labelWith (cycle ["a", "b", "c"]) [1..5]
Line 455: [("a", 1), ("b", 2), ("c", 3), ("a", 4), ("b", 5)] : List (String, Integer)
Line 456: 11.1.6 An arithmetic quiz using streams of random numbers
Line 457: You can use a Stream in any situation where you need a source of data but don’t know
Line 458: in advance how much data you’ll need to generate. For example, you could write an
Line 459: interactive arithmetic quiz that takes a source of numbers for the questions. The fol-
Line 460: lowing listing shows how you might do this.
Line 461: quiz : Stream Int -> (score : Nat) -> IO ()
Line 462: quiz (num1 :: num2 :: nums) score
Line 463: = do putStrLn ("Score so far: " ++ show score)
Line 464: putStr (show num1 ++ " * " ++ show num2 ++ "? ")
Line 465: answer <- getLine
Line 466: if cast answer == num1 * num2
Line 467: then do putStrLn "Correct!"
Line 468: quiz nums (score + 1)
Line 469: else do putStrLn ("Wrong, the answer is " ++ show (num1 * num2))
Line 470: quiz nums score
Line 471: The quiz function takes an infinite source of Ints and the score so far, and then
Line 472: returns an IO action that displays the score and a question, reads an answer from the
Line 473: user, and repeats. The questions arise directly from the input stream, so you could try
Line 474: with a sequence of increasing numbers:
Line 475: *Arith> :exec quiz (iterate (+1) 0) 0
Line 476: Score so far: 0
Line 477: 0 * 1? 0
Line 478: Correct!
Line 479: Score so far: 1
Line 480: 2 * 3? 6
Line 481: Correct!
Line 482: Listing 11.8
Line 483: An arithmetic quiz, taking a Stream of numbers for the questions
Line 484:  (Arith.idr)
Line 485: Takes two numbers from 
Line 486: an infinite source of Ints
Line 487: Correct answer; continues 
Line 488: with an increased score
Line 489: Wrong answer; displays the correct 
Line 490: answer and continues with the same score
Line 491: 
Line 492: --- 페이지 328 ---
Line 493: 302
Line 494: CHAPTER 11
Line 495: Streams and processes: working with infinite data
Line 496: Score so far: 2
Line 497: 4 * 5? 20
Line 498: Correct!
Line 499: Score so far: 3
Line 500: ABORTING EXECUTION
Line 501: Execution of a repeatedly looping program will con-
Line 502: tinue until some external event causes the program to exit. You can abort exe-
Line 503: cution at the REPL by pressing Ctrl-C.
Line 504: So far, this isn’t especially interesting because you know in advance what the questions
Line 505: will be. Instead, you could write a function that generates a stream of pseudo-random
Line 506: Ints generated from an initial seed. The following listing shows one way to generate a
Line 507: random-looking stream of numbers using a linear congruential generator.
Line 508: randoms : Int -> Stream Int
Line 509: randoms seed = let seed' = 1664525 * seed + 1013904223 in
Line 510: (seed' `shiftR` 2) :: randoms seed'
Line 511: PSEUDO-RANDOM NUMBER GENERATION
Line 512: The randoms function in listing 11.9
Line 513: generates a random-looking, but predictable, stream of numbers from an ini-
Line 514: tial seed, using a linear congruential generator. This is one of the oldest tech-
Line 515: niques for pseudo-random number generation. It suits our purposes for this
Line 516: example, but it’s not suitable for situations where high-quality randomness is
Line 517: required, such as cryptographic applications, due to the distribution and pre-
Line 518: dictability of the generated numbers.
Line 519: You could try running quiz with a stream of numbers generated by randoms:
Line 520: *Arith> :exec quiz (randoms 12345) 0
Line 521: Score so far: 0
Line 522: 1095649041 * -2129715532? no idea
Line 523: Wrong, the answer is -765659660
Line 524: Score so far: 0
Line 525: Earlier, the questions were too predictable, but now they’re perhaps a little too hard
Line 526: for most of us! Furthermore, in the preceding example, the result has even over-
Line 527: flowed the bounds of an Int, so the reported answer is incorrect. Instead, the next list-
Line 528: ing shows one way to process the results of randoms so that they’re within reasonable
Line 529: bounds for an arithmetic quiz.
Line 530: import Data.Primitives.Views
Line 531: arithInputs : Int -> Stream Int
Line 532: arithInputs seed = map bound (randoms seed)
Line 533: Listing 11.9
Line 534: Generating a stream of pseudo-random numbers from a seed (Arith.idr)
Line 535: Listing 11.10
Line 536: Generating suitable inputs for quiz (Arith.idr)
Line 537: Multiplies the current seed by one 
Line 538: constant, and adds another
Line 539: shiftR bitwise-shifts an integer
Line 540: right by a given number of places
Line 541: You need to import this 
Line 542: for the Divides view
Line 543: 
Line 544: --- 페이지 329 ---
Line 545: 303
Line 546: Streams: generating and processing infinite lists
Line 547: where
Line 548: bound : Int -> Int
Line 549: bound num with (divides num 12)
Line 550: bound ((12 * div) + rem) | (DivBy prf) = rem + 1
Line 551: You can use arithInputs as a source of random inputs for quiz and be sure that all
Line 552: the questions will use numbers between 1 and 12. Here’s an example:
Line 553: *Arith> :exec quiz (arithInputs 12345) 0
Line 554: Score so far: 0
Line 555: 2 * 1? 2
Line 556: Correct!
Line 557: Score so far: 1
Line 558: 6 * 2? 18
Line 559: Wrong, the answer is 12
Line 560: Score so far: 1
Line 561: 11 * 10? 110
Line 562: Correct!
Line 563: Score so far: 2
Line 564: You’ve successfully used a source of random Ints as inputs to the quiz, and because
Line 565: randoms (and hence arithInputs) produces an infinite sequence of numbers, you’ll
Line 566: be able to generate new numbers as long as you need to.
Line 567:  There is, however, one remaining problem, which is that quiz itself is not total:
Line 568: *Arith> :total quiz
Line 569: Main.quiz is possibly not total due to recursive path:
Line 570: Main.quiz, Main.quiz
Line 571: This shouldn’t really surprise you, because there’s nothing in the definition of quiz
Line 572: that allows it to terminate. Instead, like countFrom, randoms, and arithInputs, it’s
Line 573: reading user input and continually producing an infinite sequence of IO actions.
Line 574: Matches on num by describing it 
Line 575: in terms of a dividend and 
Line 576: remainder when divided by 12
Line 577: Safe division with the Divides view
Line 578: You can reduce an arbitrary Int to a value between 1 and 12 by dividing by 12 and
Line 579: checking the remainder. Dividing isn’t necessarily safe, since division by 0 is unde-
Line 580: fined on Int, so instead you can use a view of Int that explains that a number is
Line 581: either 0 or composed of a multiplication plus a remainder: 
Line 582: data Divides : Int -> (d : Int) -> Type where
Line 583: DivByZero : Int.Divides x 0
Line 584: DivBy : (prf : rem >= 0 && rem < d = True) ->
Line 585: Int.Divides ((d * div) + rem) d
Line 586: divides : (val : Int) -> (d : Int) -> Divides val d
Line 587: Note that in the DivBy case, you also have a proof that the remainder is guaranteed
Line 588: to have a value between 0 and the divisor by using the equality type = introduced in
Line 589: chapter 8.
Line 590: 
Line 591: --- 페이지 330 ---
Line 592: 304
Line 593: CHAPTER 11
Line 594: Streams and processes: working with infinite data
Line 595:  In practice, interactive programs often have an outer loop, which you can run
Line 596: indefinitely, invoking specific commands, each of which you’d like to terminate so
Line 597: that you can issue the next command. The way to write interactive programs that run
Line 598: indefinitely, therefore, is to distinguish the types of interactive programs that describe
Line 599: terminating sequences of actions (commands in our main loop) from the types of inter-
Line 600: active programs that describe possibly infinite sequences of actions (the main loop
Line 601: itself). We’ll explore this further in the next section. 
Line 602: Exercises
Line 603: 1
Line 604: Write an every_other function that produces a new Stream from every second ele-
Line 605: ment of an input Stream.
Line 606: If you’ve implemented this correctly, you should see the following: 
Line 607: *ex_11_1> take 10 (every_other [1..])
Line 608: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20] : List Integer
Line 609:  2
Line 610: Write an implementation of Functor (as described in section 7.3.1) for InfList.
Line 611: If you’ve implemented this correctly, you should see the following, using count-
Line 612: From and getPrefix as defined in section 11.1.4:
Line 613: *ex_11_1> getPrefix 10 (map (*2) (countFrom 1))
Line 614: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20] : List Integer
Line 615:  3
Line 616: Define a Face data type that represents the faces of a coin: heads or tails. Then,
Line 617: define this: 
Line 618: coinFlips : (count : Nat) -> Stream Int -> List Face
Line 619: This should return a sequence of count coin flips using the stream as a source of
Line 620: randomness. If you’ve implemented this correctly, you should see something like
Line 621: the following: 
Line 622: *ex_11_1> coinFlips 6 (randoms 12345)
Line 623: [Tails, Heads, Tails, Tails, Heads, Tails] : List Face
Line 624: Hint: It will help to define a function, getFace : Int -> Face.
Line 625:  4
Line 626: You can define a function to calculate the square root of a Double as follows: 
Line 627: 1
Line 628: Generate a sequence of closer approximations to the square root.
Line 629: 2
Line 630: Take the first approximation that, when squared, is within a desired bound from
Line 631: the original number.
Line 632: Write a function that generates a sequence of approximations: 
Line 633: square_root_approx : (number : Double) -> (approx : Double) -> Stream Double
Line 634: Here, you’re looking for the square root of number, starting from an approximation,
Line 635: approx. You can generate the next approximation using this formula: 
Line 636: next = (approx + (number / approx)) / 2
Line 637: 
Line 638: --- 페이지 331 ---
Line 639: 305
Line 640: Infinite processes: writing interactive total programs
Line 641: If you’ve implemented this correctly, you should see the following: 
Line 642: *ex_11_1> take 3 (square_root_approx 10 10)
Line 643: [10.0, 5.5, 3.659090909090909] : List Double
Line 644: *ex_11_1> take 3 (square_root_approx 100 25)
Line 645: [25.0, 14.5, 10.698275862068964] : List Double
Line 646: 3
Line 647: Write a function that finds the first approximation of a square root that’s within a
Line 648: desired bound, or within a maximum number of iterations: 
Line 649: square_root_bound : (max : Nat) -> (number : Double) -> (bound : Double) ->
Line 650: (approxs : Stream Double) -> Double
Line 651: This should return the first element of approxs if max is zero. Otherwise, it should
Line 652: return the first element (let’s call it val) for which the difference between val x val
Line 653: and number is smaller than bound.
Line 654: If you’ve implemented this correctly, you should be able to define square_root
Line 655: as follows, and it should be total: 
Line 656: square_root : (number : Double) -> Double
Line 657: square_root number = square_root_bound 100 number 0.00000000001
Line 658: (square_root_approx number number)
Line 659: You can test it with the following values: 
Line 660: *ex_11_1> square_root 6
Line 661: 2.449489742783178 : Double
Line 662: *ex_11_1> square_root 2500
Line 663: 50.0 : Double
Line 664: *ex_11_1> square_root 2501
Line 665: 50.009999000199954 : Double
Line 666: 11.2
Line 667: Infinite processes: writing interactive total programs
Line 668: When you write a function to generate a Stream, you give a prefix of the Stream and
Line 669: generate the remainder recursively. This is similar to quiz in that you give the initial
Line 670: IO actions to run and then generate the remainder of the IO actions recursively. So,
Line 671: you can think of an interactive program as being a program that produces a potentially
Line 672: infinite sequence of interactive actions.
Line 673:  In chapter 5, you wrote interactive programs using the IO generic type, where IO
Line 674: ty is the type of terminating interactive actions giving a result of type ty. In this sec-
Line 675: tion, you’ll see how to write nonterminating, but productive (and therefore total),
Line 676: interactive programs by defining an InfIO type for representing infinite sequences of
Line 677: IO actions.
Line 678:  Because InfIO describes infinite sequences of actions, the functions must be pro-
Line 679: ductive, so you can be certain that the resulting programs continue to produce new IO
Line 680: actions for execution while continuing to run forever. But InfIO merely describes
Line 681: sequences of interactive actions, so you’ll also need to write a function to execute those
Line 682: actions.
Line 683: 
Line 684: --- 페이지 332 ---
Line 685: 306
Line 686: CHAPTER 11
Line 687: Streams and processes: working with infinite data
Line 688:  Overall, we’ll take the following approach to writing interactive total programs:
Line 689: 1
Line 690: Define a type InfIO that describes infinite sequences of interactive actions.
Line 691:  2
Line 692: Write nonterminating but productive functions using InfIO.
Line 693: 3
Line 694: Define a run function that converts InfIO programs to IO actions.
Line 695: Your first implementation of run will not, itself, be total. You’ll then see how to refine
Line 696: the definition so that even run is total, using a data type to describe how long execu-
Line 697: tion should continue. First, though, you’ll need to see how to describe infinite pro-
Line 698: cesses by defining InfIO.
Line 699: 11.2.1 Describing infinite processes
Line 700: The following listing shows how to define the InfIO type. It’s similar to Stream, except
Line 701: that, in an interactive program, you may want the value produced by the first action to
Line 702: influence the rest of a computation.
Line 703: data InfIO : Type where
Line 704: Do : IO a
Line 705: -> (a -> Inf InfIO)
Line 706: -> InfIO
Line 707: There are two arguments to Do: 
Line 708: A description of an IO action to execute
Line 709: The remainder of the infinite sequence of actions. Because its type is a -> Inf
Line 710: InfIO, it can use the result produced by the first action to compute the remain-
Line 711: ing actions.
Line 712: By using Inf to mark the remainder of the sequence as infinite, you’re telling Idris
Line 713: that you expect functions that return a value of type InfIO to be productive. In other
Line 714: words, as with functions on Stream, delayed recursive calls that produce an InfIO
Line 715: must be arguments to a constructor. The following listing shows how this works in a
Line 716: recursive program that repeatedly displays a message. 
Line 717: loopPrint : String -> InfIO
Line 718: loopPrint msg = Do (putStrLn msg)
Line 719: (\_ => loopPrint msg)
Line 720: The recursive call to loopPrint is an argument to the constructor Do, and loopPrint
Line 721: is guaranteed to produce a constructor (Do) as a finite prefix of its result. This satisfies
Line 722: the definition of a productive total function from section 11.1.3, so Idris is happy that
Line 723: loopPrint is total:
Line 724: Listing 11.11
Line 725: Infinite interactive processes (InfIO.idr)
Line 726: Listing 11.12
Line 727: An infinite process that repeatedly displays a message (InfIO.idr)
Line 728: An IO action that produces 
Line 729: a value of type a
Line 730: Given a value of type a, calculates 
Line 731: an infinite sequence of IO actions
Line 732: Displays a message 
Line 733: using an IO action
Line 734: Continues producing an infinitely 
Line 735: long sequence of actions
Line 736: 
Line 737: --- 페이지 333 ---
Line 738: 307
Line 739: Infinite processes: writing interactive total programs
Line 740: *InfIO> :total loopPrint
Line 741: Main.loopPrint is Total
Line 742: Recall from chapter 5 that IO is a generic type describing interactive actions and that
Line 743: it will be executed by the runtime system. If you try evaluating loopPrint at the REPL,
Line 744: you’ll see a description of the first IO action that will be executed and the delayed
Line 745: remainder of the infinite sequence of actions:
Line 746: *InfIO> loopPrint "Hello"
Line 747: Do (io_bind (prim_write "Hello!\n") (\__bindx => io_return ()))
Line 748: (\underscore => Delay (loopPrint "Hello")) : InfIO
Line 749: Just as with IO, for this to be useful in practice, you’ll also need to be able to execute
Line 750: infinite sequences of actions. 
Line 751: 11.2.2 Executing infinite processes
Line 752: In chapter 5, you learned how the Idris runtime system will execute programs of type
Line 753: IO ty, where ty is the type of value produced by an interactive computation. So, in
Line 754: order to execute a value of type InfIO, you’ll need to start by converting it to an IO ().
Line 755: Here’s one way to do this.
Line 756: run : InfIO -> IO ()
Line 757: run (Do action cont) = do res <- action
Line 758: run (cont res)
Line 759: Using run, you can convert your function that repeatedly prints a message to an IO
Line 760: action, and execute it using :exec:
Line 761: *InfIO> :exec run (loopPrint "on and on and on...")
Line 762: on and on and on...
Line 763: on and on and on...
Line 764: on and on and on...
Line 765: Because this runs indefinitely, at least until you abort it by pressing Ctrl-C, you should
Line 766: perhaps not be surprised to find that Idris doesn’t consider run to be total:
Line 767: *InfIO> :total run
Line 768: Main.run is possibly not total due to recursive path:
Line 769: Main.run, Main.run
Line 770: You know that loopPrint will continue to produce new IO actions to execute, because
Line 771: it’s total. This is valuable because a program that continues to execute IO actions is
Line 772: going to continue to make visible progress (at least assuming those actions produce
Line 773: some output, which we’ll consider further in section 11.3.2). It would be nice if run
Line 774: were also total, so that you’d at least know that all possible IO actions are processed and
Line 775: Listing 11.13
Line 776: Converting an expression of type InfIO to an executable IO action
Line 777: (InfIO.idr)
Line 778: The first action to execute 
Line 779: is the first argument to Do.
Line 780: Continues execution by passing 
Line 781: the result of the action, res, to 
Line 782: the rest of the computation, cont
Line 783: Continues indefinitely
Line 784: 
Line 785: --- 페이지 334 ---
Line 786: 308
Line 787: CHAPTER 11
Line 788: Streams and processes: working with infinite data
Line 789: that there isn’t any unexpected nontermination caused by the implementation of run
Line 790: itself.
Line 791:  This would seem to be impossible: the only way to have a total, nonterminating
Line 792: function is to use the Inf type, and IO is a type of terminating action that doesn’t use
Line 793: Inf. And, indeed, if you want functions to execute indefinitely at runtime, you’ll need
Line 794: at least some way to escape from total functions. You can, however, try to make the
Line 795: escape as quietly as possible.
Line 796:  To achieve this, we’ll begin by making a terminating version of run that takes as an
Line 797: argument an upper bound on the number of actions it’s willing to execute. 
Line 798: 11.2.3 Executing infinite processes as total functions
Line 799: Earlier, in section 11.1.4, you wrote a getPrefix function that retrieved a finite por-
Line 800: tion of an infinite list:
Line 801: getPrefix : (count : Nat) -> InfList a -> List a
Line 802: You can think of the count argument as being the “fuel” that allows you to continue
Line 803: processing the infinite list. Once you run out of fuel, you can’t process any more of
Line 804: the list. You can do something similar for run, giving it an additional argument stand-
Line 805: ing for the number of iterations it will run.
Line 806:  The following listing defines a Fuel data type and gives a new, total, definition of
Line 807: run that will execute actions as long as fuel remains.
Line 808: data Fuel = Dry | More Fuel
Line 809: tank : Nat -> Fuel
Line 810: tank Z = Dry
Line 811: tank (S k) = More (tank k)
Line 812: run : Fuel -> InfIO -> IO ()
Line 813: run (More fuel) (Do c f) = do res <- c
Line 814: run fuel (f res)
Line 815: run Dry p = putStrLn "Out of fuel"
Line 816: Now, run is total:
Line 817: *InfIO> :total run
Line 818: Main.run is Total
Line 819: Unfortunately, you still have a problem because you now need to specify an explicit
Line 820: maximum number of actions a program is allowed to execute, so you don’t really have
Line 821: indefinitely running processes anymore! For example:
Line 822: *InfIO> :exec run (tank 5) (loopPrint "vroom")
Line 823: vroom
Line 824: vroom
Line 825: Listing 11.14
Line 826: Converting an expression of type InfIO to an executable IO action 
Line 827: running for a finite time (InfIO.idr)
Line 828: Fuel
Line 829: defines the
Line 830: length of
Line 831: time a
Line 832: process
Line 833: can run.
Line 834: Generates an amount of fuel. Defines 
Line 835: a new type for Fuel instead of using 
Line 836: Nat—you’ll see why shortly.
Line 837: Consumes one drop of fuel 
Line 838: and continues execution
Line 839: No more fuel; 
Line 840: abandons execution
Line 841: 
Line 842: --- 페이지 335 ---
Line 843: 309
Line 844: Infinite processes: writing interactive total programs
Line 845: vroom
Line 846: vroom
Line 847: vroom
Line 848: Out of fuel
Line 849: It’s valuable to ensure that run is total, because it guarantees that the implementation
Line 850: of run itself won’t be the cause of any unexpected nontermination. If you still want
Line 851: programs to run indefinitely, though, you’ll need to find a way to generate fuel indefi-
Line 852: nitely. You can achieve this by using the Lazy data type. 
Line 853: 11.2.4 Generating infinite structures using Lazy types
Line 854: If you have a means of generating infinite Fuel, you can run interactive programs
Line 855: indefinitely. Listing 11.15 shows how you can do this using a single nontotal function,
Line 856: forever. You also need to change the definition of Fuel so that it’s explicit in the type
Line 857: that you only generate Fuel when it’s required.
Line 858: data Fuel = Dry | More (Lazy Fuel)
Line 859: forever : Fuel
Line 860: forever = More forever
Line 861: FOREVER AND NONTERMINATION
Line 862: It’s necessary for forever to be nontotal
Line 863: because it (deliberately) introduces nontermination. Fortunately, this is
Line 864: the only nontotal function you need in order to be able to execute programs
Line 865: forever.
Line 866: The purpose of Lazy is to control when Idris evaluates an expression. As the name
Line 867: Lazy implies, Idris won’t evaluate an expression of type Lazy ty until it’s explicitly
Line 868: requested by Force, which returns a value of type ty. The Prelude defines Lazy simi-
Line 869: larly to Inf, which you defined in section 11.1.2:
Line 870: Lazy : Type -> Type
Line 871: Delay : (value : ty) -> Lazy ty
Line 872: Force : (computation : Lazy ty) -> ty
Line 873: Also, like Inf, Idris inserts calls to Delay and Force implicitly. In fact, Inf and Lazy are
Line 874: sufficiently similar that they’re implemented internally using the same underlying
Line 875: type, as the next listing shows. The only difference in practice between Inf and Lazy is
Line 876: the way the totality checker treats them, as explained in the sidebar.
Line 877: data DelayReason = Infinite | LazyValue
Line 878: data Delayed : DelayReason -> Type -> Type where
Line 879: Delay : (val : ty) -> Delayed reason ty
Line 880: Listing 11.15
Line 881: Generating infinite fuel (InfIO.idr)
Line 882: Listing 11.16
Line 883: Internal definition of Inf and Lazy
Line 884: Lazy, explained shortly, means that 
Line 885: the value of the argument will only 
Line 886: be calculated when needed.
Line 887: Generates fuel as needed
Line 888: A computation is delayed either 
Line 889: because it may be infinite, or 
Line 890: because it’s to be evaluated later.
Line 891: 
Line 892: --- 페이지 336 ---
Line 893: 310
Line 894: CHAPTER 11
Line 895: Streams and processes: working with infinite data
Line 896: Inf : Type -> Type
Line 897: Inf ty = Delayed Infinite ty
Line 898: Lazy : Type -> Type
Line 899: Lazy ty = Delayed LazyValue ty
Line 900: Force : Delayed reason ty -> ty
Line 901: You’ve implemented three functions: loopPrint, which is the interactive program;
Line 902: run, which executes interactive programs given fuel; and forever, which provides an
Line 903: indefinite quantity of fuel. To summarize:
Line 904: 
Line 905: loopPrint is a total function because it continues to produce IO actions indefi-
Line 906: nitely.
Line 907: 
Line 908: run is a total function because it will consume IO actions, executing them as
Line 909: long as there is Fuel available.
Line 910: 
Line 911: forever is a nontotal (or partial) function because it will never terminate and
Line 912: doesn’t produce any data inside an Inf type.
Line 913: By writing a version of run that will process data as long as fuel is available, Idris can
Line 914: guarantee that run is total, consuming fuel as it goes. You still have an “escape hatch”
Line 915: that allows you to run interactive programs indefinitely, in the form of the forever
Line 916: function. Nevertheless, forever is the only function that’s not total.
Line 917:  You can still improve the definition of loopPrint itself. When we wrote interactive
Line 918: programs in chapter 5, we used do notation to help make interactive programs more
Line 919: readable, but we haven’t been able to do so using InfIO. You can, however, extend do
Line 920: notation to support your own data types, like InfIO. 
Line 921: Inf is a type synonym for a 
Line 922: delayed infinite value.
Line 923: Lazy is a type synonym for 
Line 924: a delayed lazy value.
Line 925: Force causes a delayed 
Line 926: value to be evaluated.
Line 927: Totality checking with Inf and Lazy
Line 928: At runtime, Inf and Lazy behave the same way. The key difference between them is
Line 929: the way the totality checker treats them. Idris detects termination by looking for argu-
Line 930: ments that converge toward a base case, so it needs to know whether an argument
Line 931: to a constructor is smaller (that is, closer to a base case) than the overall constructor
Line 932: expression:
Line 933: If the argument has type Lazy ty, for some type ty, it’s considered smaller
Line 934: than the constructor expression.
Line 935: If the argument has type Inf ty, for some type ty, it’s not considered smaller
Line 936: than the constructor expression, because it may continue expanding indefi-
Line 937: nitely. Instead, Idris will check that the overall expression is productive, as
Line 938: discussed in section 11.1.3. 
Line 939: If you used Inf for Fuel, rather than Lazy, run would no longer be total because the
Line 940: argument, fuel, wouldn’t be considered smaller than the expression More fuel.
Line 941: 
Line 942: --- 페이지 337 ---
Line 943: 311
Line 944: Infinite processes: writing interactive total programs
Line 945: 11.2.5 Extending do notation for InfIO
Line 946: As you saw in chapter 5, do notation translates to applications of the (>>=) operator,
Line 947: as illustrated again in figure 11.3.
Line 948: You’ve seen this transformation for IO in chapter 5, for Maybe in chapter 6, and in gen-
Line 949: eral for implementations of the Monad interface in chapter 7. In fact, the transforma-
Line 950: tion is purely syntactic, so you can define your own implementations of (>>=) to use
Line 951: do notation for your own types. The following listing shows how you can define do
Line 952: notation for InfIO.
Line 953: (>>=) : IO a -> (a -> Inf InfIO) -> InfIO
Line 954: (>>=) = Do
Line 955: loopPrint : String -> InfIO
Line 956: loopPrint msg = do putStrLn msg
Line 957: loopPrint msg
Line 958: Idris translates the do block to applications of (>>=) and decides which version of
Line 959: (>>=) to use by looking at the required type. Here, because the required type of the
Line 960: overall expression is InfIO, it uses the version of (>>=) that produces a value of type
Line 961: InfIO.
Line 962:  The InfIO type allows you to describe infinitely running interactive programs, and
Line 963: by defining a (>>=) operator, you can write those programs in much the same way as
Line 964: programs with IO, provided that the final action is to call a function of type InfIO.
Line 965:  Now that you've seen that you can write productive interactive programs using do
Line 966: notation, we can revisit the arithmetic quiz from section 11.1.6. 
Line 967: 11.2.6 A total arithmetic quiz
Line 968: To conclude this section, we’ll update the arithmetic quiz so that it’s a total function,
Line 969: and you’ll see how you can incorporate this in a complete Idris program. Listing 11.18
Line 970: shows our starting point, setting up the InfIO type and run function, as you’ve seen
Line 971: earlier in this section. You’ll need Data.Primitives.Views for generating the stream
Line 972: of random numbers. You’ll also import the System module for the time function,
Line 973: which you’ll use to help initialize the stream of random numbers.
Line 974: import Data.Primitives.Views
Line 975: import System
Line 976: Listing 11.17
Line 977: Defining do notation for infinite sequences of actions
Line 978: Listing 11.18
Line 979: Setting up InfIO (ArithTotal.idr)
Line 980: do x <- action
Line 981:    result
Line 982: action >>= \x => result
Line 983: Figure 11.3
Line 984: Transforming do notation 
Line 985: to an expression using the >>= 
Line 986: operator when sequencing actions
Line 987: Defines the (>>=) operator by 
Line 988: using Do from InfIO directly
Line 989: Idris translates this do block to 
Line 990: applications of the (>>=) operator.
Line 991: You’ll need this for the time function, which 
Line 992: you’ll use to seed the random stream.
Line 993: 
Line 994: --- 페이지 338 ---
Line 995: 312
Line 996: CHAPTER 11
Line 997: Streams and processes: working with infinite data
Line 998: %default total
Line 999: data InfIO : Type where
Line 1000: Do : IO a -> (a -> Inf InfIO) -> InfIO
Line 1001: (>>=) : IO a -> (a -> Inf InfIO) -> InfIO
Line 1002: (>>=) = Do
Line 1003: data Fuel = Dry | More (Lazy Fuel)
Line 1004: run : Fuel -> InfIO -> IO ()
Line 1005: run (More fuel) (Do c f) = do res <- c
Line 1006: run fuel (f res)
Line 1007: run Dry p = putStrLn "Out of fuel"
Line 1008: Listing 11.19 shows the next step, implementing quiz using InfIO. Because InfIO is
Line 1009: an infinite sequence of IO actions, you can write quiz as before, with the final step
Line 1010: being a recursive call. In fact, the definition is identical to the earlier definition; only
Line 1011: the type has changed. 
Line 1012: quiz : Stream Int -> (score : Nat) -> InfIO
Line 1013: quiz (num1 :: num2 :: nums) score
Line 1014: = do putStrLn ("Score so far: " ++ show score)
Line 1015: putStr (show num1 ++ " * " ++ show num2 ++ "? ")
Line 1016: answer <- getLine
Line 1017: if (cast answer == num1 * num2)
Line 1018: then do putStrLn "Correct!"
Line 1019: quiz nums (score + 1)
Line 1020: else do putStrLn ("Wrong, the answer is " ++ show (num1 * num2))
Line 1021: quiz nums score
Line 1022: Listing 11.19
Line 1023: Defining a total quiz function (ArithTotal.idr)
Line 1024: This compiler directive means that 
Line 1025: all functions are, unless otherwise 
Line 1026: stated, expected to be total.
Line 1027: The %default total directive
Line 1028: Idris supports a number of compiler directives that change certain details about the
Line 1029: language. In listing 11.18, the %default total directive means that Idris will report
Line 1030: an error if there are any functions that it can’t guarantee to be total.
Line 1031: You can override this for individual functions with the partial keyword. For example,
Line 1032: forever is not total:
Line 1033: partial
Line 1034: forever : Fuel
Line 1035: forever = More forever
Line 1036: It’s a good idea to use %default total in your programs, because if Idris can’t deter-
Line 1037: mine that a function is either terminating or productive, this can be a sign that there’s
Line 1038: a problem with the function’s definition. Furthermore, explicitly marking which func-
Line 1039: tions are partial means that if there’s a problem with nontermination, or a program
Line 1040: that crashes due to missing input, you’ve minimized the number of functions that
Line 1041: could cause the problem.
Line 1042: The last step is a
Line 1043: recursive call to quiz.
Line 1044: These calls are
Line 1045: productive, because
Line 1046: they each follow a
Line 1047: sequence of IO actions.
Line 1048: 
Line 1049: --- 페이지 339 ---
Line 1050: 313
Line 1051: Infinite processes: writing interactive total programs
Line 1052: Because you’re using the %default total annotation, you can be sure that quiz is
Line 1053: total. There are two recursive calls to quiz, and Idris can determine that each one is
Line 1054: guaranteed to be prefixed by a sequence of IO actions, so quiz is guaranteed to keep
Line 1055: producing IO actions indefinitely.
Line 1056:  The final step is to write a main function that calls run to execute quiz with a
Line 1057: stream of Ints. Here are the remaining parts of the implementation.
Line 1058: randoms : Int -> Stream Int
Line 1059: randoms seed = let seed' = 1664525 * seed + 1013904223 in
Line 1060: (seed' `shiftR` 2) :: randoms seed'
Line 1061: arithInputs : Int -> Stream Int
Line 1062: arithInputs seed = map bound (randoms seed)
Line 1063: where
Line 1064: bound : Int -> Int
Line 1065: bound x with (divides x 12)
Line 1066: bound ((12 * div) + rem) | (DivBy prf) = abs rem + 1
Line 1067: partial
Line 1068: forever : Fuel
Line 1069: forever = More forever
Line 1070: partial
Line 1071: main : IO ()
Line 1072: main = do seed <- time
Line 1073: run forever (quiz (arithInputs (fromInteger seed)) 0)
Line 1074: You’ve used randoms and arithInputs, as defined in section 11.1.6, to generate the
Line 1075: stream of Ints. By using the system time to initialize the stream, you’ll get different
Line 1076: questions every time you run the program.
Line 1077:  In the whole implementation, the only functions that aren’t total are forever and
Line 1078: main, the latter only because it needs to use forever to generate an indefinite amount
Line 1079: of fuel for run. Because you used the %default total annotation, you needed to mark
Line 1080: these as partial explicitly. That means you can be sure that the only possible cause of
Line 1081: nontermination in the program is the fact that you’ve deliberately said that the pro-
Line 1082: gram should run forever.
Line 1083:  Other than forever, you know that the individual components will be one of the
Line 1084: following:
Line 1085: Productive—Such as quiz continuing to produce IO actions for interpretation
Line 1086: and randoms continuing to produce new random numbers when required
Line 1087: Terminating—Such as the individual IO commands and the generation of the
Line 1088: next random number from a seed
Line 1089: This distinction is useful for writing realistic programs such as servers and REPLs, which
Line 1090: you want to run indefinitely while being sure that each individual action the program
Line 1091: executes terminates. Often, though, you’ll want more flexibility. At the moment, for
Line 1092: example, you have no way to quit the quiz cleanly. We’ll return to this in the next section. 
Line 1093: Listing 11.20
Line 1094: Completing the implementation with main (ArithTotal.idr)
Line 1095: forever needs to be
Line 1096: marked partial explicitly
Line 1097: because it doesn’t
Line 1098: terminate and doesn’t
Line 1099: use Inf, and you used
Line 1100: %default total.
Line 1101: main needs to be 
Line 1102: marked partial 
Line 1103: because it uses forever.
Line 1104: You can use the system time 
Line 1105: to initialize the stream of 
Line 1106: random numbers.
Line 1107: 
Line 1108: --- 페이지 340 ---
Line 1109: 314
Line 1110: CHAPTER 11
Line 1111: Streams and processes: working with infinite data
Line 1112: Exercise
Line 1113: The repl function defined in the Prelude isn’t total because it’s an IO action that
Line 1114: loops indefinitely. Implement a new version of repl using InfIO: 
Line 1115: totalREPL : (prompt : String) -> (action : String -> String) -> InfIO
Line 1116: If you’ve implemented this correctly, totalREPL should be total, and you should be
Line 1117: able to test it as follows: 
Line 1118: *ex_11_2> :total totalREPL
Line 1119: Main.totalREPL is Total
Line 1120: *ex_11_2> :exec run forever (totalREPL "\n: " toUpper)
Line 1121: : Hello [user input]
Line 1122: HELLO
Line 1123: : World [user input]
Line 1124: WORLD
Line 1125: 11.3
Line 1126: Interactive programs with termination
Line 1127: Using Inf, you can explicitly control when you want data to be produced, or when you
Line 1128: want it to be consumed. As a result, you have a choice between programs that always
Line 1129: terminate and programs that continue running forever. To write complete applica-
Line 1130: tions, though, you’ll need more control. After all, although you want a server to run
Line 1131: indefinitely, you’d like to be able to shut it down cleanly when you want to.
Line 1132:  So far, the types you’ve defined using Inf have had only one constructor, so they’ve
Line 1133: required you to produce infinite sequences. Instead, you can mix infinite and finite
Line 1134: components in a single data type, which means you can describe processes that can
Line 1135: run indefinitely, but which are also allowed to terminate. In this section, you’ll see
Line 1136: how to refine the InfIO type to support processes that terminate cleanly. Moreover,
Line 1137: you’ll see how to introduce more precision into the type, and define a type of pro-
Line 1138: cesses specifically for console I/O.
Line 1139: 11.3.1 Refining InfIO: introducing termination
Line 1140: Using InfIO, you can write total interactive programs that are guaranteed to keep pro-
Line 1141: ducing IO actions, running indefinitely. The following listing shows a small example of
Line 1142: the form you saw in the previous section. This program repeatedly asks for the user’s
Line 1143: name and displays a greeting.
Line 1144: greet : InfIO
Line 1145: greet = do putStr "Enter your name: "
Line 1146: name <- getLine
Line 1147: putStrLn ("Hello " ++ name)
Line 1148: greet
Line 1149: Listing 11.21
Line 1150: Repeatedly greeting a user, running forever (Greet.idr)
Line 1151: 
Line 1152: --- 페이지 341 ---
Line 1153: 315
Line 1154: Interactive programs with termination
Line 1155: Typically, when you write interactive programs, you’ll want to provide a means for the
Line 1156: user to quit. Unfortunately, the only way a user can quit greet is by pressing Ctrl-C.
Line 1157: There’s no way to write a function in InfIO that quits any other way!
Line 1158:  Fortunately, you can solve this with a small variation on InfIO. The Inf type marks
Line 1159: a value as potentially infinite, rather than guaranteeing that the value is infinite, and
Line 1160: you can introduce extra data constructors for potentially infinite types. You can define
Line 1161: a new RunIO type, shown in the next listing, that adds a Quit constructor to describe
Line 1162: programs that exit, producing a value.
Line 1163: data RunIO : Type -> Type where
Line 1164: Quit : a -> RunIO a
Line 1165: Do : IO a -> (a -> Inf (RunIO b)) -> RunIO b
Line 1166: (>>=) : IO a -> (a -> Inf (RunIO b)) -> RunIO b
Line 1167: (>>=) = Do
Line 1168: Using RunIO, you can write a version of greet, shown in the following listing, that
Line 1169: quits when the user gives an empty input.
Line 1170: greet : RunIO ()
Line 1171: greet = do putStr "Enter your name: "
Line 1172: name <- getLine
Line 1173: if name == ""
Line 1174: then do putStrLn "Bye bye!"
Line 1175: Quit ()
Line 1176: else do putStrLn ("Hello " ++ name)
Line 1177: greet
Line 1178: Depending on the input, greet is either terminating or productive. The totality
Line 1179: checker accepts greet as total, because it satisfies the definition from section 11.1.3
Line 1180: that a total function either terminates or is productive for all well-typed inputs.
Line 1181:  Before you can execute greet, you’ll need to write a new version of run that trans-
Line 1182: lates a program in RunIO to a sequence of IO actions for the runtime system to exe-
Line 1183: cute. Previously, run would only terminate on running out of Fuel, but now there are
Line 1184: two possible reasons for termination:
Line 1185: Running out of Fuel, as before
Line 1186: Exiting cleanly, with a result, if the process being executed invokes Quit
Line 1187: Listing 11.22
Line 1188: The RunIO type, describing potentially infinite processes with an 
Line 1189: additional Quit command (RunIO.idr)
Line 1190: Listing 11.23
Line 1191: Repeatedly greets a user, exiting on empty input (RunIO.idr)
Line 1192: RunIO is parameterized by the type 
Line 1193: of value produced by an interactive 
Line 1194: process, if it terminates.
Line 1195: Quits, producing 
Line 1196: a value
Line 1197: A process consisting of a 
Line 1198: single IO action, followed 
Line 1199: by a potentially infinite 
Line 1200: process
Line 1201: Implements (>>=) to support 
Line 1202: do notation for RunIO programs
Line 1203: The input was empty, so 
Line 1204: displays a message and exits. 
Line 1205: Here, greet is terminating.
Line 1206: There was input, so greets the user and 
Line 1207: continues. The recursive call follows IO 
Line 1208: actions, so greet is productive.
Line 1209: 
Line 1210: --- 페이지 342 ---
Line 1211: 316
Line 1212: CHAPTER 11
Line 1213: Streams and processes: working with infinite data
Line 1214: You can distinguish these results in the type:
Line 1215: run : Fuel -> RunIO a -> IO (Maybe a)
Line 1216: The possible results of run correspond to the two possible reasons for termination:
Line 1217: If run runs out of Fuel, it returns Nothing.
Line 1218: If run executes an action of the form Quit value, it returns Just value.
Line 1219: The following listing gives the new definition of run for RunIO.
Line 1220: run : Fuel -> RunIO a -> IO (Maybe a)
Line 1221: run fuel (Quit value) = pure (Just value)
Line 1222: run (More fuel) (Do c f) = do res <- c
Line 1223: run fuel (f res)
Line 1224: run Dry p = pure Nothing
Line 1225: Finally, you can write a main program that executes greet and discards the result:
Line 1226: partial
Line 1227: main : IO ()
Line 1228: main = do run forever greet
Line 1229: pure ()
Line 1230: Because run now creates an IO action that produces a value of type Maybe () when
Line 1231: invoked with greet, and main is expected to create an action that produces a value of
Line 1232: type (), you need to finish by calling pure (). When you execute main at the REPL, you
Line 1233: can now exit cleanly by entering an empty string:
Line 1234: *RunIO> :exec main
Line 1235: Enter your name: Edwin
Line 1236: Hello Edwin
Line 1237: Enter your name:
Line 1238: Bye bye!
Line 1239: With RunIO, you’ve refined InfIO with the ability to terminate a process cleanly when
Line 1240: required. This gives you more freedom to write interactive programs, but there’s
Line 1241: Listing 11.24
Line 1242: Converting an expression of type RunIO ty to an executable action of
Line 1243: type IO ty (RunIO.idr)
Line 1244: Interactive programs and infinite types
Line 1245: Using a potentially infinite data type like RunIO is not unique to Idris. A similar idea
Line 1246: was described by Peter Hancock and Anton Setzer in their 2004 paper “Interactive
Line 1247: programs and weakly final coalgebras in dependent type theory,” following on from
Line 1248: their earlier work in describing interactive programs with dependent types.
Line 1249: The generic type Inf that you use in the type of potentially infinite structures follows
Line 1250: a similar idea used in the Agda programming language, described by Nils Anders Dan-
Line 1251: ielsson in his 2010 paper “Total Parser Combinators.”
Line 1252: Terminates due to invoking the Quit 
Line 1253: command, so it returns Just value
Line 1254: Terminates due to running out 
Line 1255: of fuel, so it returns Nothing
Line 1256: Empty string
Line 1257: 
Line 1258: --- 페이지 343 ---
Line 1259: 317
Line 1260: Interactive programs with termination
Line 1261: another way in which RunIO arguably gives you too much freedom. Specifically, a pro-
Line 1262: cess described by RunIO is a sequence of arbitrary IO actions, giving you several possi-
Line 1263: bilities, including these: 
Line 1264: Reading from and writing to the console
Line 1265: Opening and closing files
Line 1266: Opening network connections
Line 1267: Deleting files
Line 1268: For the programs you’ve written in this chapter, you’re only interested in the first of
Line 1269: these. The others are not only unnecessary, but lead to the possibility of remote secu-
Line 1270: rity vulnerabilities in the third case, and potentially destructive errors in the fourth.
Line 1271:  One of the principles of type-driven development, which we discussed in chapter 1,
Line 1272: is that we should aim to write types that describe as precisely as possible the values that
Line 1273: inhabit that type. To conclude this chapter, therefore, we’ll look at how we can refine
Line 1274: the RunIO type to describe only the actions that are necessary to implement the arith-
Line 1275: metic quiz.
Line 1276: 11.3.2 Domain-specific commands
Line 1277: You only need two IO actions when implementing the arithmetic quiz: reading from
Line 1278: and writing to the console. Instead of allowing interactive programs in RunIO to exe-
Line 1279: cute arbitrary actions, therefore, you can restrict them to only the actions you need.
Line 1280: That is, you can prevent your program from executing any interactive action that’s
Line 1281: outside the problem domain in which you’re working.
Line 1282:  The next listing shows a refined ConsoleIO type that describes interactive pro-
Line 1283: grams that support only reading from and writing to the console.
Line 1284: data Command : Type -> Type where
Line 1285: PutStr : String -> Command ()
Line 1286: GetLine : Command String
Line 1287: data ConsoleIO : Type -> Type where
Line 1288: Quit : a -> ConsoleIO a
Line 1289: Do : Command a -> (a -> Inf (ConsoleIO b)) -> ConsoleIO b
Line 1290: (>>=) : Command a -> (a -> Inf (ConsoleIO b)) -> ConsoleIO b
Line 1291: (>>=) = Do
Line 1292: Effectively, Command defines an interactive interface that ConsoleIO programs can use.
Line 1293: You can think of it as defining the capabilities or permissions of interactive programs,
Line 1294: eliminating any unnecessary actions.
Line 1295:  You now need to refine the implementation of run to be able to execute ConsoleIO
Line 1296: programs.
Line 1297: Listing 11.25
Line 1298: Interactive programs supporting only console I/O (ArithCmd.idr)
Line 1299: Defines the IO commands that 
Line 1300: are available, parameterized by 
Line 1301: the commands’ return types.
Line 1302: Only IO operations defined in Command
Line 1303: are allowed in ConsoleIO programs.
Line 1304: 
Line 1305: --- 페이지 344 ---
Line 1306: 318
Line 1307: CHAPTER 11
Line 1308: Streams and processes: working with infinite data
Line 1309:  
Line 1310: runCommand : Command a -> IO a
Line 1311: runCommand (PutStr x) = putStr x
Line 1312: runCommand GetLine = getLine
Line 1313: run : Fuel -> ConsoleIO a -> IO (Maybe a)
Line 1314: run fuel (Quit val) = do pure (Just val)
Line 1315: run (More fuel) (Do c f) = do res <- runCommand c
Line 1316: run fuel (f res)
Line 1317: run Dry p = pure Nothing
Line 1318: DOMAIN-SPECIFIC LANGUAGES
Line 1319: A domain-specific language (DSL) is a language
Line 1320: that’s specialized for a particular class of problems. DSLs typically aim to pro-
Line 1321: vide only the operations that are needed when working in a specific problem
Line 1322: domain in a notation that’s accessible to experts in that domain, while elimi-
Line 1323: nating any redundant operations.
Line 1324: In a sense, ConsoleIO defines a DSL for writing interactive console pro-
Line 1325: grams, in that it restricts the programmer to only the interactive actions that
Line 1326: are needed and eliminates unnecessary actions such as file processing or net-
Line 1327: work communication. 
Line 1328: Listing 11.27 shows how you can modify quiz to run as a ConsoleIO program. By look-
Line 1329: ing at the type of quiz and the definitions of ConsoleIO and run, you have a guaran-
Line 1330: tee that quiz will only execute console I/O actions. There’s no way it can open or
Line 1331: close files, communicate over a network, or perform any other kind of interactive
Line 1332: operation.
Line 1333: quiz : Stream Int -> (score : Nat) -> ConsoleIO Nat
Line 1334: quiz (num1 :: num2 :: nums) score
Line 1335: = do PutStr ("Score so far: " ++ show score ++ "\n")
Line 1336: PutStr (show num1 ++ " * " ++ show num2 ++ "? ")
Line 1337: answer <- GetLine
Line 1338: if toLower answer == "quit" then Quit score else
Line 1339: if (cast answer == num1 * num2)
Line 1340: then do PutStr "Correct!\n"
Line 1341: quiz nums (score + 1)
Line 1342: else do PutStr ("Wrong, the answer is " ++
Line 1343: show (num1 * num2) ++ "\n")
Line 1344: quiz nums score
Line 1345: To complete the implementation, you’ll need to implement a main function. The fol-
Line 1346: lowing listing shows a new implementation of main that executes the quiz and then
Line 1347: displays the player’s final score after they enter quit.
Line 1348: Listing 11.26
Line 1349: Executing a ConsoleIO program (ArithCmd.idr)
Line 1350: Listing 11.27
Line 1351: The arithmetic quiz, written as a ConsoleIO program (ArithCmd.idr)
Line 1352: Runs a console I/O command by 
Line 1353: using the corresponding IO action
Line 1354: Uses runCommand to 
Line 1355: execute the IO action 
Line 1356: given by the command c
Line 1357: You’ll allow the player to quit, so quiz 
Line 1358: returns the player’s score on exit.
Line 1359: PutStr and GetLine are valid
Line 1360: Commands in ConsoleIO.
Line 1361: Entering “quit” 
Line 1362: will exit the quiz.
Line 1363: 
Line 1364: --- 페이지 345 ---
Line 1365: 319
Line 1366: Interactive programs with termination
Line 1367:  
Line 1368: partial
Line 1369: main : IO ()
Line 1370: main = do seed <- time
Line 1371: Just score <- run forever (quiz (arithInputs (fromInteger seed)) 0)
Line 1372: | Nothing => putStrLn "Ran out of fuel"
Line 1373: putStrLn ("Final score: " ++ show score)
Line 1374: You can still refine the definition of quiz slightly. As functions get larger, it’s good
Line 1375: practice to break them down into smaller functions, each with clearly defined roles.
Line 1376: Here, for example, you can lift out functions for reporting whether an answer is cor-
Line 1377: rect or wrong, as in the following listing. These functions must themselves be either
Line 1378: productive (finishing by calling quiz, as they do here) or terminating if quiz is to
Line 1379: remain total.
Line 1380: mutual
Line 1381: correct : Stream Int -> (score : Nat) -> ConsoleIO Nat
Line 1382: correct nums score
Line 1383: = do PutStr "Correct!\n"
Line 1384: quiz nums (score + 1)
Line 1385: wrong : Stream Int -> Int -> (score : Nat) -> ConsoleIO Nat
Line 1386: wrong nums ans score
Line 1387: = do PutStr ("Wrong, the answer is " ++ show ans ++ "\n")
Line 1388: quiz nums score
Line 1389: quiz : Stream Int -> (score : Nat) -> ConsoleIO Nat
Line 1390: quiz (num1 :: num2 :: nums) score
Line 1391: = do PutStr ("Score so far: " ++ show score ++ "\n")
Line 1392: PutStr (show num1 ++ " * " ++ show num2 ++ "? ")
Line 1393: answer <- GetLine
Line 1394: if toLower answer == "quit" then Quit score else
Line 1395: if (cast answer == num1 * num2)
Line 1396: then correct nums score
Line 1397: else wrong nums (num1 * num2) score
Line 1398: After quiz type-checks successfully, you can make several guarantees about its behav-
Line 1399: ior by looking at the types and checking for totality:
Line 1400: It will execute no interactive action other then putStr and getLine.
Line 1401: It will either exit immediately or execute at least one interactive action, because
Line 1402: it is productive.
Line 1403: Every action executed will return a result in finite time, because it is total.
Line 1404: Listing 11.28
Line 1405: A main function that executes the quiz and displays the final score
Line 1406: (ArithCmd.idr)
Line 1407: Listing 11.29
Line 1408: Lifting out components of quiz into separate functions (ArithCmd.idr)
Line 1409: This won’t happen because you used 
Line 1410: forever, but it’s good practice to cover 
Line 1411: all possible results of run, nevertheless.
Line 1412: Displays the score 
Line 1413: produced from the 
Line 1414: result of quiz
Line 1415: In a mutual block (see 
Line 1416: chapter 3), definitions 
Line 1417: can refer to each other. 
Line 1418: You need mutual 
Line 1419: because correct and 
Line 1420: wrong both call quiz, 
Line 1421: and vice versa.
Line 1422: 
Line 1423: --- 페이지 346 ---
Line 1424: 320
Line 1425: CHAPTER 11
Line 1426: Streams and processes: working with infinite data
Line 1427: 11.3.3 Sequencing Commands with do notation
Line 1428: In implementing quiz, you used two types to construct the function: Command and
Line 1429: ConsoleIO:
Line 1430: 
Line 1431: Command describes single commands, which terminate.
Line 1432: 
Line 1433: ConsoleIO describes sequences of terminating commands, which might be
Line 1434: infinite.
Line 1435: So, you can have single, finite commands, or sequences of infinite commands. But it would
Line 1436: also be useful to be able to construct composite commands; that is, sequences of com-
Line 1437: mands that are guaranteed to terminate. For example, you might like to write a com-
Line 1438: posite command that displays a prompt, and then reads and parses user input. The
Line 1439: next listing shows a type that represents possible user inputs, and a skeleton definition
Line 1440: of a function to read and parse input.
Line 1441: data Input = Answer Int
Line 1442: | QuitCmd
Line 1443: readInput : (prompt : String) -> Command Input
Line 1444: readInput prompt = ?readInput_rhs
Line 1445: To write this function, you need to do the following:
Line 1446: 1
Line 1447: Display the prompt.
Line 1448:  2
Line 1449: Read an input from the console.
Line 1450: 3
Line 1451: Convert the input string to Input and return it.
Line 1452: Because Command currently supports only single commands, you’ll need to extend it to
Line 1453: support sequences of commands. The next listing shows the extended definition,
Line 1454: including two new data constructors, Pure and Bind, and a correspondingly updated
Line 1455: definition of runCommand.
Line 1456: data Command : Type -> Type where
Line 1457: PutStr : String -> Command ()
Line 1458: GetLine : Command String
Line 1459: Pure : ty -> Command ty
Line 1460: Bind : Command a -> (a -> Command b) -> Command b
Line 1461: runCommand : Command a -> IO a
Line 1462: runCommand (PutStr x) = putStr x
Line 1463: runCommand GetLine = getLine
Line 1464: runCommand (Pure val) = pure val
Line 1465: runCommand (Bind c f) = do res <- runCommand c
Line 1466: runCommand (f res)
Line 1467: Listing 11.30
Line 1468: Defining a type for representing user input, and a composite command
Line 1469: for reading and parsing input (ArithCmdDo.idr)
Line 1470: Listing 11.31
Line 1471: Extending Command to allow sequences of commands (ArithCmdDo.idr)
Line 1472: An input is either a number that answers 
Line 1473: the question or a quit command.
Line 1474: The return type, Command 
Line 1475: Input, means that readInput 
Line 1476: will not loop indefinitely.
Line 1477: A command
Line 1478: that does
Line 1479: nothing,
Line 1480: returning a
Line 1481: value
Line 1482: A sequence of two commands,
Line 1483: taking the output of the first
Line 1484: and passing it to the second
Line 1485: Runs the first command, 
Line 1486: then runs the second with 
Line 1487: the output of the first
Line 1488: 
Line 1489: --- 페이지 347 ---
Line 1490: 321
Line 1491: Interactive programs with termination
Line 1492: You might also want to define (>>=) to support do notation for sequencing com-
Line 1493: mands, but the following definition doesn’t work as you might expect: 
Line 1494: (>>=) : Command a -> (a -> Command b) -> Command b
Line 1495: (>>=) = Bind
Line 1496: If you try this, Idris will complain that (>>=) is already defined, because you’ve
Line 1497: defined do notation for ConsoleIO:
Line 1498: ArithCmdDo.idr:22:7:Main.>>= already defined
Line 1499: Idris allows multiple definitions of the same function name, as long as they’re in sepa-
Line 1500: rate namespaces. You’ve already seen this with List and Vect, for example, where each
Line 1501: has constructors called Nil and (::) that Idris disambiguates according to the con-
Line 1502: text in which you use them.
Line 1503:  The namespace is given by the module where you define functions. Namespaces
Line 1504: are also hierarchical, so you can introduce further namespaces inside a module. You
Line 1505: can have multiple definitions of functions called (>>=) in one module by introducing
Line 1506: new namespaces for each. The following listing shows how you can define new name-
Line 1507: spaces for each (>>=).
Line 1508: namespace CommandDo
Line 1509: (>>=) : Command a -> (a -> Command b) -> Command b
Line 1510: (>>=) = Bind
Line 1511: namespace ConsoleDo
Line 1512: (>>=) : Command a -> (a -> Inf (ConsoleIO b)) -> ConsoleIO b
Line 1513: (>>=) = Do
Line 1514: If you check the type of (>>=) at the REPL, you’ll see all the definitions of (>>=) in
Line 1515: their respective namespaces, with their types:
Line 1516: *ArithCmdDo> :t (>>=)
Line 1517: Main.CommandDo.(>>=) : Command a ->
Line 1518: (a -> Command b) -> Command b
Line 1519: Main.ConsoleDo.(>>=) : Command a ->
Line 1520: (a -> Inf (ConsoleIO b)) -> ConsoleIO b
Line 1521: Prelude.Monad.(>>=) : Monad m => m a -> (a -> m b) -> m b
Line 1522: Listing 11.32
Line 1523: Creating two definitions of (>>=) in separate namespaces 
Line 1524: (ArithCmdDo.idr)
Line 1525: Introduces a new, 
Line 1526: nested namespace
Line 1527: Defining a Monad implementation for Command
Line 1528: You could also define an implementation of the Monad interface for Command, as
Line 1529: described in chapter 7. When possible, this is often preferable because the Prelude
Line 1530: and base libraries define several functions that work generically with Monad imple-
Line 1531: mentations. To do this, you’d also need to define implementations of Functor and
Line 1532: Applicative. You’ll see an example of how to do this for a similar type in the next
Line 1533: chapter.
Line 1534: 
Line 1535: --- 페이지 348 ---
Line 1536: 322
Line 1537: CHAPTER 11
Line 1538: Streams and processes: working with infinite data
Line 1539: Using CommandDo.(>>=) to provide do notation, you can complete the definition of
Line 1540: readInput.
Line 1541: readInput : (prompt : String) -> Command Input
Line 1542: readInput prompt = do PutStr prompt
Line 1543: answer <- GetLine
Line 1544: if toLower answer == "quit"
Line 1545: then Pure QuitCmd
Line 1546: else Pure (Answer (cast answer))
Line 1547: Finally, you can use readInput in the main quiz function to encapsulate the details of
Line 1548: displaying a prompt and parsing the user’s input, shown in the final definition.
Line 1549: quiz : Stream Int -> (score : Nat) -> ConsoleIO Nat
Line 1550: quiz (num1 :: num2 :: nums) score
Line 1551: = do PutStr ("Score so far: " ++ show score ++ "\n")
Line 1552: input <- readInput (show num1 ++ " * " ++ show num2 ++ "? ")
Line 1553: case input of
Line 1554: Answer answer => if answer == num1 * num2
Line 1555: then correct nums score
Line 1556: else wrong nums (num1 * num2) score
Line 1557: QuitCmd => Quit score
Line 1558: In this final definition, you distinguish between terminating sequences of commands
Line 1559: (using Command), and potentially nonterminating console I/O programs (using
Line 1560: ConsoleIO). Syntactically, you write functions the same way in each, but the type tells
Line 1561: you whether the function is allowed to run indefinitely, or whether it must eventually
Line 1562: terminate. 
Line 1563: Exercises
Line 1564: 1
Line 1565: Update quiz so that it keeps track of the total number of questions and then returns
Line 1566: the number of correct answers and the number of questions attempted. A sample
Line 1567: run might look something like this: 
Line 1568: Listing 11.33
Line 1569: Implementing readInput by sequence Command (ArithCmdDo.idr)
Line 1570: Listing 11.34
Line 1571: Defining quiz using readInput as a composite command to display a
Line 1572: prompt and read user input (ArithCmdDo.idr)
Line 1573: (continued)
Line 1574: You can’t, however, define an implementation of Monad for ConsoleIO, because the
Line 1575: type of ConsoleDo.(>>=) doesn’t fit the type of the (>>=) method in the Monad
Line 1576: interface. 
Line 1577: You can case-split on input because 
Line 1578: readInput has parsed it as a more 
Line 1579: informative type than simply a String.
Line 1580: 
Line 1581: --- 페이지 349 ---
Line 1582: 323
Line 1583: Summary
Line 1584: *ex_11_3> :exec
Line 1585: Score so far: 0 / 0
Line 1586: 9 * 11? 99
Line 1587: Correct!
Line 1588: Score so far: 1 / 1
Line 1589: 6 * 9? 42
Line 1590: Wrong, the answer is 54
Line 1591: Score so far: 1 / 2
Line 1592: 10 * 2? 20
Line 1593: Correct!
Line 1594: Score so far: 2 / 3
Line 1595: 7 * 2? quit
Line 1596: Final score: 2 / 3
Line 1597:  2
Line 1598: Extend the Command type from section 11.3.2 so that it also supports reading and
Line 1599: writing files.
Line 1600: Hint: Look at the types of readFile and writeFile in the Prelude to decide what
Line 1601: types your data constructors should have.
Line 1602:  3
Line 1603: Use your extended Command type to implement an interactive “shell” that supports
Line 1604: the following commands: 
Line 1605: 
Line 1606: cat [filename], which reads a file and displays its contents
Line 1607: 
Line 1608: copy [source] [destination], which reads a source file and writes its contents
Line 1609: to a destination file
Line 1610: 
Line 1611: exit, which exits the shell
Line 1612: 11.4
Line 1613: Summary
Line 1614: You can generate infinite data using Inf to state which parts of a structure are
Line 1615: potentially infinite.
Line 1616: A total function either terminates with a well-typed input or produces a prefix
Line 1617: of a well-typed infinite result in finite time.
Line 1618: You can process infinite structures by using finite data to determine how much
Line 1619: of the infinite structure to use.
Line 1620: The Prelude defines a Stream data type for constructing infinite lists.
Line 1621: You can define processes as infinite sequences of IO actions.
Line 1622: To execute an infinite process, you define a function that takes an argument
Line 1623: stating how long the process should run.
Line 1624: The partial function forever allows processes to run indefinitely by generating
Line 1625: an infinite amount of Fuel, using the Lazy type.
Line 1626: By implementing (>>=), you can extend do notation for your own data types to
Line 1627: make programs easier to read and write.
Line 1628: You can mix finite and infinite structures within the same data type to define
Line 1629: potentially infinite processes that may also terminate.