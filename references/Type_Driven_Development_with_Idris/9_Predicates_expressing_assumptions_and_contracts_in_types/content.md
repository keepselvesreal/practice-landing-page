Line 1: 
Line 2: --- 페이지 262 ---
Line 3: 236
Line 4: Predicates: expressing
Line 5: assumptions and
Line 6: contracts in types
Line 7: Dependent types like EqNat and =, which you saw in the previous chapter, are used
Line 8: entirely for describing relationships between data. These types are often referred to
Line 9: as predicates, which are data types that exist entirely to describe a property of some
Line 10: data. If you can construct a value for a predicate, then you know the property
Line 11: described by that predicate must be true.
Line 12:  In this chapter, you’ll see how to express more-complex relationships between
Line 13: data using predicates. By expressing relationships between data in types, you can be
Line 14: explicit about the assumptions you’re making about the inputs to a function, and
Line 15: have those assumptions checked by the type checker when those functions are
Line 16: This chapter covers
Line 17: Describing and checking membership of a vector 
Line 18: using a predicate
Line 19: Using predicates to describe contracts for 
Line 20: function inputs and outputs
Line 21: Reasoning about system state in types
Line 22: 
Line 23: --- 페이지 263 ---
Line 24: 237
Line 25: Membership tests: the Elem predicate
Line 26: called. You can even think of these assumptions as expressing compile time contracts
Line 27: that other arguments must satisfy before anything can call the function.
Line 28:  In practice, you’ll often write functions that make assumptions about the form of
Line 29: some other data, having (hopefully!) checked those assumptions beforehand. Here
Line 30: are a few examples:
Line 31: A function that reads from a file assumes that the file handle describes an open
Line 32: file.
Line 33: A function that processes data it has received from a network assumes that the
Line 34: data follows the appropriate protocol.
Line 35: A function that retrieves user data (say, for a customer on a website) assumes
Line 36: that the user has successfully authenticated.
Line 37: You need to ensure that you check any necessary assumptions before you call these
Line 38: functions, particularly when security or user privacy is at stake. In Idris, you can make
Line 39: this kind of assumption explicit in a type, and have the type checker ensure that you’ve
Line 40: properly checked the assumption in advance. An advantage of expressing assumptions
Line 41: in types is that they are guaranteed to hold, even as a system evolves over time.
Line 42:  In this chapter, we’ll take an in-depth look at a specific small example: removing a
Line 43: value from a vector if that value is contained within the vector. We’ll look at how to
Line 44: express in a type that a vector contains a specific element, how to test this property at
Line 45: runtime, and how to use such properties in practice to write a larger program with
Line 46: some aspects of its behavior expressed in its types.
Line 47: 9.1
Line 48: Membership tests: the Elem predicate
Line 49: Using =, Void, and Dec, you can describe properties that your programs satisfy in their
Line 50: types, making the types precise as a result. Typically, you’ll use =, Void, and Dec as
Line 51: building blocks for describing and checking relationships between pieces of data.
Line 52: Describing relationships in types allows you to state assumptions that functions make
Line 53: and, more importantly, it allows Idris to check whether those assumptions are satisfied
Line 54: or violated.
Line 55:  For example, you might want to
Line 56: Remove an element from a vector only under the assumption that the element
Line 57: is present in the vector
Line 58: Search for a value in a list only under the assumption that the list is ordered
Line 59: Run a database query only under the assumption that the inputs have been
Line 60: validated
Line 61: Send a message to a machine on the network only under the assumption that
Line 62: you have an open connection
Line 63: In this section, we’ll examine the first of these in more detail. We’ll begin by trying to
Line 64: write a function that removes an element from a vector, and then we’ll see how we can
Line 65: refine the type to state and check any necessary assumptions that make the type more
Line 66: precise. Finally, we’ll use the function in a simple interactive program.
Line 67: 
Line 68: --- 페이지 264 ---
Line 69: 238
Line 70: CHAPTER 9
Line 71: Predicates: expressing assumptions and contracts in types
Line 72: 9.1.1
Line 73: Removing an element from a Vect
Line 74: If you have a Vect containing a number of elements, you’d expect the following of a
Line 75: removeElem function that removes a specific element from that vector: 
Line 76: The input vector should have at least one element.
Line 77: The output vector’s length should be one less than the input vector’s length.
Line 78: Because Vect is parameterized by the element type contained in the vector and is
Line 79: indexed by the length of the vector, you can (indeed, you must) express these length
Line 80: properties in the type of removeElem. Your first attempt might look like this:
Line 81: removeElem : (value : a) -> (xs : Vect (S n) a) -> Vect n a
Line 82: Let’s see what happens if you try to write this function:
Line 83: 1
Line 84: Define—If you add a skeleton definition and case-split on xs, Idris will give you
Line 85: only one pattern, because xs can’t be an empty vector: 
Line 86: removeElem : (value : a) -> (xs : Vect (S n) a) -> Vect n a
Line 87: removeElem value (x :: xs) = ?removeElem_rhs_1
Line 88:  2
Line 89: Refine—If the value you’re looking for is equal to x, you can remove it from the
Line 90: list, returning xs. You’ll need to refine the type before you can compare value
Line 91: and x; you can use decidable equality so that you can be certain that the equal-
Line 92: ity test is accurate. This is the refined type: 
Line 93: removeElem : DecEq a => (value : a) -> (xs : Vect (S n) a) -> Vect n a
Line 94:  3
Line 95: Refine—You can now use decEq to compare value and x, and discard x if they’re
Line 96: equal: 
Line 97: removeElem : DecEq a => (value : a) -> (xs : Vect (S n) a) -> Vect n a
Line 98: removeElem value (x :: xs) = case decEq value x of
Line 99: Yes prf => xs
Line 100: No contra => ?removeElem_rhs_3
Line 101: 4
Line 102: Refine failure—For ?removeElem_rhs_3, you might hope to be able to remove
Line 103: value from xs recursively, but if you try this, you’ll get an error: 
Line 104: removeElem : DecEq a => (value : a) -> (xs : Vect (S n) a) -> Vect n a
Line 105: removeElem value (x :: xs) = case decEq value x of
Line 106: Yes prf => xs
Line 107: No contra => x :: removeElem value xs
Line 108: Idris reports the following: 
Line 109: When checking right hand side of Main.case block in removeElem
Line 110: at removeelem.idr:4:35 with expected type
Line 111: Vect n a
Line 112: When checking argument xs to Main.removeElem:
Line 113: Type mismatch between
Line 114: Vect n a (Type of xs)
Line 115: and
Line 116: Vect (S k) a (Expected type)
Line 117: 
Line 118: --- 페이지 265 ---
Line 119: 239
Line 120: Membership tests: the Elem predicate
Line 121: The problem is that removeElem requires a vector that’s guaranteed to be non-
Line 122: empty, but xs may be empty! You can see this from its type, Vect n a: the n could
Line 123: stand for any natural number, including zero.
Line 124: This problem arises because there’s no guarantee that value will appear in
Line 125: the vector, so it’s possible to reach the end of the vector without encountering
Line 126: it. If this happens, there’s no value to remove, so you can’t satisfy the type.
Line 127: You’ll need to refine the type further in order to be able to write this function. You
Line 128: can try one of the following:
Line 129: Rewrite the type so that removeElem returns Maybe (Vect n a), returning Nothing
Line 130: if the value doesn’t appear in the input.
Line 131: Rewrite the type so that removeElem returns a dependent pair, (newLength **
Line 132: Vect newLength a).
Line 133: Express a precondition on removeElem that the value is guaranteed to be in the
Line 134: vector.
Line 135: You’ve already seen how to express possible failure with Maybe (in chapter 4), and how
Line 136: to express an unknown length using dependent pairs (in chapter 5). The third
Line 137: option, however, would express the purpose of removeElem precisely. To achieve this,
Line 138: you’ll need to write a type that describes the relationship between a value and a vector
Line 139: that contains that value. 
Line 140:  If you can describe in a type that a vector contains a specific element, you’ll be able
Line 141: to use that type to express a contract on removeElem expressing that you can only use it
Line 142: if you know the element is in the vector. In the rest of this section, you’ll implement
Line 143: this type, Elem, use it to make the type of removeElem more precise, and learn more
Line 144: about how to use Elem in practice. 
Line 145: 9.1.2
Line 146: The Elem type: guaranteeing a value is in a vector
Line 147: In the previous chapter, you saw how to express that two values are guaranteed to be
Line 148: equal by using either a specific EqNat type or the generic = type. The existence of a
Line 149: value in one of these types is, essentially, a proof that two values are equal. You can do
Line 150: something similar to guarantee that a value is in a vector.
Line 151:  Our goal is to define a type, Elem, with the following type constructor: 
Line 152: Elem : (value : a) -> (xs : Vect k a) -> Type
Line 153: If we have a value, and a vector, xs, that contains that value, we should be able to construct
Line 154: an element of the type Elem value xs. For example, we should be able to construct the
Line 155: following: 
Line 156: oneInVector : Elem 1 [1,2,3]
Line 157: maryInVector : Elem "Mary" ["Peter", "Paul", "Mary"]
Line 158: We should also be able to construct functions of the following types, which show that a
Line 159: specific value is not contained in a vector: 
Line 160: 
Line 161: --- 페이지 266 ---
Line 162: 240
Line 163: CHAPTER 9
Line 164: Predicates: expressing assumptions and contracts in types
Line 165: fourNotInVector : Elem 4 [1,2,3] -> Void
Line 166: peteNotInVector : Elem "Pete" ["John", "Paul", "George", "Ringo"] -> Void
Line 167: The following listing shows how the Elem dependent type is defined in Data.Vect.
Line 168: data Elem : a -> Vect k a -> Type where
Line 169: Here : Elem x (x :: xs)
Line 170: There : (later : Elem x xs) -> Elem x (y :: xs)
Line 171: The value Here can be read as a proof that a value is the first value in a vector, as in this
Line 172: example: 
Line 173: oneInVector : Elem 1 [1,2,3]
Line 174: oneInVector = Here
Line 175: The constructor There, given an argument that shows a value x is in the vector xs, can
Line 176: be read as a proof that x must also be in the vector y :: xs for any value y.
Line 177:  To illustrate this, let’s try to write maryInVector: 
Line 178: maryInVector : Elem "Mary" ["Peter", "Paul", "Mary"]
Line 179: 1
Line 180: Define—Create a skeleton definition with a hole for the right side: 
Line 181: maryInVector : Elem "Mary" ["Peter", "Paul", "Mary"]
Line 182: maryInVector = ?maryInVector_rhs
Line 183:  2
Line 184: Refine, type—You can’t use Here, because "Mary" isn’t the first element of the
Line 185: vector, so try using There and leaving a hole for its argument: 
Line 186: maryInVector : Elem "Mary" ["Peter", "Paul", "Mary"]
Line 187: maryInVector = There ?maryInVector_rhs
Line 188: If you check the type of ?maryInVector_rhs, you’ll see that you now have a
Line 189: smaller problem: 
Line 190: --------------------------------------
Line 191: maryInVector_rhs : Elem "Mary" ["Paul", "Mary"]
Line 192:  3
Line 193: Refine, type—If you do the same again, applying There and leaving a hole for its
Line 194: argument, you get the following program: 
Line 195: maryInVector : Elem "Mary" ["Peter", "Paul", "Mary"]
Line 196: maryInVector = There (There ?maryInVector_rhs)
Line 197: You also now have a simpler type for ?maryInVector_rhs: 
Line 198: --------------------------------------
Line 199: maryInVector_rhs : Elem "Mary" ["Mary"]
Line 200: Listing 9.1
Line 201: The Elem dependent type, expressing that a value is guaranteed to be 
Line 202: contained in a vector (defined in Data.Vect)
Line 203: Here states that x is the first value 
Line 204: in a vector of the form x :: xs.
Line 205: There states that if you 
Line 206: know that x occurs in a 
Line 207: vector xs, then x must also 
Line 208: occur in a vector y :: xs.
Line 209: 
Line 210: --- 페이지 267 ---
Line 211: 241
Line 212: Membership tests: the Elem predicate
Line 213: 4
Line 214: Refine—"Mary" is now the first element in the vector, so you can refine ?mary-
Line 215: InVector_rhs using Here: 
Line 216: maryInVector : Elem "Mary" ["Peter", "Paul", "Mary"]
Line 217: maryInVector = There (There Here)
Line 218: EXPRESSION SEARCH
Line 219: An expression search with Ctrl-Alt-S will successfully
Line 220: find the definition of maryInVector, and it’s often useful for constructing
Line 221: values of dependent types like Elem and =.
Line 222: You can use Elem and types like it that describe relationships between data to express
Line 223: contracts on the form of data expected as input to a function. These contracts, being
Line 224: expressed as types, can be verified by Idris using type checking; if a function call vio-
Line 225: lates a contract, the program will not compile.
Line 226:  More constructively, if you express the types of your functions precisely enough,
Line 227: with contracts expressed using types like Elem, you know that once your program com-
Line 228: piles, every contract must be satisfied. You can use Elem to express a contract on
Line 229: removeElem that specifies when the inputs are valid. 
Line 230: 9.1.3
Line 231: Removing an element from a Vect: types as contracts
Line 232: The difficulty we had when writing removeElem was that we couldn’t make a recursive
Line 233: call on the tail of the vector because we couldn’t guarantee that the element we were
Line 234: trying to remove was in the vector. We’ll therefore refine the type of removeElem, add-
Line 235: ing an argument that expresses the contract that the element to be removed must be
Line 236: in the vector. The following listing shows our starting point.
Line 237: removeElem : (value : a) ->
Line 238: (xs : Vect (S n) a) ->
Line 239: (prf : Elem value xs) ->
Line 240: Vect n a
Line 241: removeElem value xs prf = ?removeElem_rhs
Line 242: In type-driven development, we aim to use more-precise types to help direct the
Line 243: implementation of functions. Here, the input prf gives more precision to the input
Line 244: type of removeElem, and you can even case-split on it to see what you learn about the
Line 245: inputs value and xs from the relationship specified between them by prf.
Line 246:  You can write the function as follows:
Line 247: 1
Line 248: Define—Begin with the case split on prf: 
Line 249: removeElem : (value : a) -> (xs : Vect (S n) a) ->
Line 250:              (prf : Elem value xs) ->
Line 251: Vect n a
Line 252: removeElem value (value :: ys) Here = ?removeElem_rhs_1
Line 253: removeElem value (y :: ys) (There later) = ?removeElem_rhs_2
Line 254: Listing 9.2
Line 255: Removing an element from a vector, with a contract specified in the type
Line 256: using Elem (RemoveElem.idr)
Line 257: The value to be removed
Line 258: The vector to remove the value from
Line 259: A proof that the value is present 
Line 260: in the vector, expressing a 
Line 261: contract for the caller to satisfy
Line 262: 
Line 263: --- 페이지 268 ---
Line 264: 242
Line 265: CHAPTER 9
Line 266: Predicates: expressing assumptions and contracts in types
Line 267:  2
Line 268: Refine—For the first case, ?removeElem_rhs_1, you can see from the patterns
Line 269: that Idris has generated that value must be the first element in the vector if the
Line 270: proof has the form Here. You can therefore refine this case to remove value: 
Line 271: removeElem : (value : a) -> (xs : Vect (S n) a) ->
Line 272:              (prf : Elem value xs) ->
Line 273: Vect n a
Line 274: removeElem value (value :: ys) Here = ys
Line 275: removeElem value (y :: ys) (There later) = ?removeElem_rhs_2
Line 276:  3
Line 277: Type—If you look at the type of ?removeElem_rhs_2, you’ll see that it appears
Line 278: you have the same problem as before, in that ys has length n, and removeElem
Line 279: requires a vector of length S n for the recursive call: 
Line 280: a : Type
Line 281: value : a
Line 282: y : a
Line 283: n : Nat
Line 284: ys : Vect n a
Line 285: later : Elem value ys
Line 286: --------------------------------------
Line 287: removeElem_rhs_2 : Vect n a
Line 288: But you have some further information that you didn’t have available earlier:
Line 289: you know from the variable later that value must occur in ys, and this means
Line 290: that ys must have a nonzero length. But how can you use this knowledge?
Line 291:  4
Line 292: Define—Given that the length n must be nonzero, the trick is to case-split on n
Line 293: (by bringing it into scope using braces on the left side of the definition) and
Line 294: show that it’s impossible for it to be zero: 
Line 295: removeElem : (value : a) -> (xs : Vect (S n) a) ->
Line 296:              (prf : Elem value xs) ->
Line 297: Vect n a
Line 298: removeElem value (value :: ys) Here = ys
Line 299: removeElem {n = Z} value (y :: ys) (There later) = ?removeElem_rhs_1
Line 300: removeElem {n = (S k)} value (y :: ys) (There later) = ?removeElem_rhs_3
Line 301:  5
Line 302: Refine—Now, you can complete ?removeElem_rhs_3. You now know the length
Line 303: of ys is nonzero, so you can make a recursive call: 
Line 304: removeElem : (value : a) -> (xs : Vect (S n) a) -> (prf : Elem value xs) ->
Line 305: Vect n a
Line 306: removeElem value (value :: ys) Here = ys
Line 307: removeElem {n = Z} value (y :: ys) (There later) = ?removeElem_rhs_1
Line 308: removeElem {n = (S k)} value (y :: ys) (There later)
Line 309: = y :: removeElem value ys later
Line 310: Note that you need to pass later to the recursive call, as evidence that value is
Line 311: contained within ys.
Line 312:  6
Line 313: Type, define—For the remaining hole, ?removeElem_rhs_1, take a look at its type
Line 314: and what variables are available: 
Line 315: 
Line 316: --- 페이지 269 ---
Line 317: 243
Line 318: Membership tests: the Elem predicate
Line 319: a : Type
Line 320: value : a
Line 321: y : a
Line 322: ys : Vect 0 a
Line 323: later : Elem value ys
Line 324: --------------------------------------
Line 325: removeElem_rhs_2 : Vect 0 a
Line 326: You’re looking for an empty vector. That empty vector, if you look at the vari-
Line 327: ables on the left side, should be a vector resulting from removing value from
Line 328: ys. This doesn’t make sense, because ys is an empty vector!
Line 329: You can make this more clear by case splitting on ys. Idris produces only one
Line 330: case: 
Line 331: removeElem : (value : a) -> (xs : Vect (S n) a) -> (prf : Elem value xs) ->
Line 332: Vect n a
Line 333: removeElem value (value :: ys) Here = ys
Line 334: removeElem {n = Z} value (y :: []) (There later) = ?removeElem_rhs_1
Line 335: removeElem {n = (S k)} value (y :: ys) (There later)
Line 336: = y :: removeElem value ys later
Line 337: Looking at the type of the new hole, ?removeElem_rhs_1, shows the following: 
Line 338: a : Type
Line 339: value : a
Line 340: y : a
Line 341: later : Elem value []
Line 342: --------------------------------------
Line 343: removeElem_rhs_1 : Vect 0 a
Line 344: Previously, you’ve used the impossible keyword to rule out a case that doesn’t
Line 345: type-check. This case does type-check, so you can’t use impossible. But there’s
Line 346: no way you’ll ever have a value of type Elem value [] as an input, because
Line 347: there’s no way to construct an element of this type.
Line 348: 7
Line 349: Refine—You can complete the definition using a function, absurd, defined in
Line 350: the Prelude. It has the following type: 
Line 351: absurd : Uninhabited t => t -> a
Line 352: The Uninhabited interface, described in the sidebar, can be implemented for
Line 353: any type that has no values (as you saw with twoplustwo_not_five in chapter 8).
Line 354: So, you can refine ?remove_Elem_rhs_1 as follows: 
Line 355: removeElem : (value : a) -> (xs : Vect (S n) a) -> (prf : Elem value xs) ->
Line 356: Vect n a
Line 357: removeElem value (value :: ys) Here = ys
Line 358: removeElem {n = Z} value (y :: []) (There later) = absurd later
Line 359: removeElem {n = (S k)} value (y :: ys) (There later)
Line 360: = y :: removeElem value ys later
Line 361: 
Line 362: --- 페이지 270 ---
Line 363: 244
Line 364: CHAPTER 9
Line 365: Predicates: expressing assumptions and contracts in types
Line 366: The additional argument to removeElem, of type Elem value xs, means that
Line 367: removeElem can work under the assumption that value is in the vector xs. It also
Line 368: means that you must provide a proof that value is in xs when calling the function. 
Line 369: 9.1.4
Line 370: auto-implicit arguments: automatically constructing proofs
Line 371: If you try running removeElem with some specific values for the element and the vec-
Line 372: tor, you’ll find you need to provide an additional argument for the proof. Sometimes
Line 373: it might be a proof that’s possible to construct:
Line 374: *RemoveElem> removeElem 2 [1,2,3,4,5]
Line 375: removeElem 2 [1, 2, 3, 4, 5] : Elem 2 [1, 2, 3, 4, 5] -> Vect 4 Integer
Line 376: Sometimes it might not:
Line 377: *RemoveElem> removeElem 7 [1,2,3,4,5]
Line 378: removeElem 7 [1, 2, 3, 4, 5] : Elem 7 [1, 2, 3, 4, 5] -> Vect 4 Integer
Line 379: In the first case, you can call removeElem by explicitly providing a proof of Elem 2
Line 380: [1,2,3,4,5]:
Line 381: *RemoveElem> removeElem 2 [1,2,3,4,5] (There Here)
Line 382: [1, 3, 4, 5] : Vect 4 Integer
Line 383: The need to provide proofs explicitly like this can add a lot of noise to programs and
Line 384: can harm readability. Idris provides a special kind of implicit argument, marked with
Line 385: the keyword auto, to reduce this noise.
Line 386:  You can define a removeElem_auto function:
Line 387: removeElem_auto : (value : a) -> (xs : Vect (S n) a) ->
Line 388: {auto prf : Elem value xs} -> Vect n a
Line 389: removeElem_auto value xs {prf} = removeElem value xs prf
Line 390: The Uninhabited interface
Line 391: If a type has no values, like 2 + 2 = 5 or Elem x [], you can provide an imple-
Line 392: mentation of the Uninhabited interface for it. Uninhabited is defined in the Pre-
Line 393: lude as follows: 
Line 394: interface Uninhabited t where
Line 395: uninhabited : t -> Void
Line 396: There’s one method, which returns an element of the empty type. For example, you
Line 397: can provide an implementation of Uninhabited for 2 + 2 = 5: 
Line 398: Uninhabited (2 + 2 = 5) where
Line 399: uninhabited Refl impossible
Line 400: Using uninhabited, the Prelude defines absurd as follows, using void: 
Line 401: absurd : Uninhabited t => (h : t) -> a
Line 402: absurd h = void (uninhabited h)
Line 403: 
Line 404: --- 페이지 271 ---
Line 405: 245
Line 406: Membership tests: the Elem predicate
Line 407: The third argument, named prf, is an auto-implicit argument. Like the implicit argu-
Line 408: ments you’ve already seen, an auto-implicit argument can be brought into scope by
Line 409: writing it in braces, and Idris will attempt to find a value automatically. Unlike ordi-
Line 410: nary implicits, Idris will search for a value for an auto implicit using the same machin-
Line 411: ery it uses for expression search with Ctrl-Alt-S in Atom.
Line 412:  When you run removeElem_auto with arguments for value and xs, Idris will try to
Line 413: construct a proof for the argument marked auto:
Line 414: *RemoveElem> removeElem_auto 2 [1,2,3,4,5]
Line 415: [1, 3, 4, 5] : Vect 4 Integer
Line 416: If it can’t find a proof, it will report an error:
Line 417: *RemoveElem> removeElem_auto 7 [1,2,3,4,5]
Line 418: (input):1:17:When checking argument prf to function Main.removeElem_auto:
Line 419: Can't find a value of type
Line 420: Elem 7 [1, 2, 3, 4, 5]
Line 421: Alternatively, the following listing shows how you could define removeElem using an
Line 422: auto implicit directly.
Line 423: removeElem : (value : a) -> (xs : Vect (S n) a) ->
Line 424: {auto prf : Elem value xs} ->
Line 425: Vect n a
Line 426: removeElem value (value :: ys) {prf = Here} = ys
Line 427: removeElem {n = Z} value (y :: []) {prf = There later} = absurd later
Line 428: removeElem {n = (S k)} value (y :: ys) {prf = There later}
Line 429: = y :: removeElem value ys
Line 430: In general, though, you won’t know the specific values you’re passing to removeElem.
Line 431: They could be values read from a user or constructed by another part of the program.
Line 432: We’ll therefore need to consider how you can use removeElem when the inputs are
Line 433: unknown until runtime.
Line 434:  Just as you wrote a checkEqNat function to decide whether two numbers are equal,
Line 435: and later generalized it to decEq using an interface, you’ll need a function to decide
Line 436: whether a value is contained in a vector. 
Line 437: 9.1.5
Line 438: Decidable predicates: deciding membership of a vector
Line 439: As you saw in the last chapter, a property is decidable if you can always say whether the
Line 440: property holds for some specific values. Using the following function, you can see that
Line 441: Elem value xs is a decidable property for specific values of value and xs, so Elem is a
Line 442: decidable predicate:
Line 443: isElem : DecEq ty => (value : ty) -> (xs : Vect n ty) -> Dec (Elem value xs)
Line 444: Listing 9.3
Line 445: Defining removeElem using an auto-implicit argument (RemoveElem.idr)
Line 446: prf is an auto-implicit argument. Idris will try 
Line 447: to find a value automatically for each call, 
Line 448: using expression search.
Line 449: Matches on prf by bringing 
Line 450: it into scope using braces
Line 451: Idris will find the value (later) for
Line 452: the proof in this call automatically.
Line 453: 
Line 454: --- 페이지 272 ---
Line 455: 246
Line 456: CHAPTER 9
Line 457: Predicates: expressing assumptions and contracts in types
Line 458: The type of isElem states that as long as you can decide equality of values in some type
Line 459: ty, you can decide whether a value with type ty is contained in a vector of types ty.
Line 460: Remember that Dec has the following constructors:
Line 461: 
Line 462: Yes, which takes as its argument a proof that the predicate holds. In this case,
Line 463: that’s a value of type Elem value xs for whichever value and xs are passed as
Line 464: inputs to isElem.
Line 465: 
Line 466: No, which takes as its argument a proof that the predicate doesn’t hold. In this
Line 467: case, that’s a value of type Elem value xs -> Void.
Line 468: isElem is defined in Data.Vect, but it’s instructive to see how to write it yourself. The
Line 469: following listing shows our starting point, defining Elem by hand in a file named Elem-
Line 470: Type.idr.
Line 471: data Elem : a -> Vect k a -> Type where
Line 472: Here : Elem x (x :: xs)
Line 473: There : (later : Elem x xs) -> Elem x (y :: xs)
Line 474: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 475: 1
Line 476: Define, refine—Define the function by case splitting on the input vector xs: 
Line 477: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 478: isElem value [] = ?isElem_rhs_1
Line 479: isElem value (x :: xs) = ?isElem_rhs_2
Line 480:  2
Line 481: Refine—For ?isElem_rhs_1, value is clearly not in the empty vector, so you can
Line 482: return No. Remember that No takes as an argument a proof that you can’t con-
Line 483: struct the predicate. You can leave a hole for this argument for the moment: 
Line 484: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 485: isElem value [] = No ?notInNil
Line 486: isElem value (x :: xs) = ?isElem_rhs_2
Line 487: If you check the type of ?notInNil, you’ll see that to fill in this hole, you need
Line 488: to provide a proof that there can’t be an element of the empty vector: 
Line 489: a : Type
Line 490: value : a
Line 491: constraint : DecEq a
Line 492: --------------------------------------
Line 493: notInNil : Elem value [] -> Void
Line 494: We’ll return to this hole shortly.
Line 495:  3
Line 496: Refine—For ?isElem_rhs_2, if value and x are equal, you’ve found the value
Line 497: you’re looking for. You can use decEq, case-split on the result, and if the result is
Line 498: of the form Yes prf, return Yes with a hole for the proof that the value is the
Line 499: first in the vector: 
Line 500: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 501: Listing 9.4
Line 502: Defining Elem and isElem by hand (ElemType.idr)
Line 503: 
Line 504: --- 페이지 273 ---
Line 505: 247
Line 506: Membership tests: the Elem predicate
Line 507: isElem value [] = No ?notInNil
Line 508: isElem value (x :: xs) = case decEq value x of
Line 509: Yes prf => Yes ?isElem_rhs_1
Line 510: No notHere => ?isElem_rhs_3
Line 511:  4
Line 512: Type, refine—You might like to fill the ?isElem_rhs_1 hole with Here, but if you
Line 513: check its type, you’ll see that you can’t quite use Here yet: 
Line 514: a : Type
Line 515: value : a
Line 516: x : a
Line 517: prf : value = x
Line 518: k : Nat
Line 519: xs : Vect k a
Line 520: constraint : DecEq a
Line 521: --------------------------------------
Line 522: isElem_rhs_1 : Elem value (x :: xs)
Line 523: You can’t use Here because the type you’re looking for isn’t of the form Elem
Line 524: value (value :: xs). But prf tells you that value and x must be the same, so if
Line 525: you case-split on prf, you’ll get this: 
Line 526: isElem value (x :: xs) = case decEq value x of
Line 527: Yes Refl => Yes ?isElem_rhs_2
Line 528: No notHere => ?isElem_rhs_3
Line 529: The type of the newly created hole, ?isElem_rhs_2, is now in the form you
Line 530: need: 
Line 531: a : Type
Line 532: value : a
Line 533: k : Nat
Line 534: xs : Vect k a
Line 535: constraint : DecEq a
Line 536: --------------------------------------
Line 537: isElem_rhs_2 : Elem value (value :: xs)
Line 538: You can fill in the ?isElem_rhs_2 using expression search in Atom: 
Line 539: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 540: isElem value [] = No ?notInNil
Line 541: isElem value (x :: xs) = case decEq value x of
Line 542: Yes Refl => Yes Here
Line 543: No notHere => ?isElem_rhs_3
Line 544:  5
Line 545: Refine—For ?isElem_rhs_3, value and x aren’t equal (you know this because
Line 546: decEq value x has returned a proof), so you can search recursively in xs: 
Line 547: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 548: isElem value [] = No ?notInNil
Line 549: isElem value (x :: xs) = case decEq value x of
Line 550: Yes Refl => Yes Here
Line 551: No notHere => case isElem value xs of
Line 552: Yes prf => Yes ?isElem_rhs_1
Line 553: No notThere => No ?isElem_rhs_2
Line 554: 
Line 555: --- 페이지 274 ---
Line 556: 248
Line 557: CHAPTER 9
Line 558: Predicates: expressing assumptions and contracts in types
Line 559: Expression search will find the necessary proof for ?isElem_rhs_1. You can
Line 560: leave a hole for the No case for now: 
Line 561: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 562: isElem value [] = No ?notInNil
Line 563: isElem value (x :: xs) = case decEq value x of
Line 564: Yes Refl => Yes Here
Line 565: No notHere => case isElem value xs of
Line 566: Yes prf => Yes (There prf)
Line 567: No notThere => No ?notInTail
Line 568: At this stage, you can test the definition at the REPL. If a value is in a vector,
Line 569: you’ll see Yes and a proof: 
Line 570: *ElemType> isElem 3 [1,2,3,4,5]
Line 571: Yes (There (There Here)) : Dec (Elem 3 [1, 2, 3, 4, 5])
Line 572: If not, you’ll see No, with a hole for the proof that the element is missing: 
Line 573: *ElemType> isElem 7 [1,2,3,4,5]
Line 574: No ?notInTail : Dec (Elem 7 [1, 2, 3, 4, 5])
Line 575: To complete the definition, you’ll need to complete notInNil and notInTail.
Line 576:  6
Line 577: Define, refine—You can complete ?notInNil by lifting it to a top-level function
Line 578: with Ctrl-Alt-L and then case splitting on its argument. Idris notices that neither
Line 579: input is possible: 
Line 580: notInNil : Elem value [] -> Void
Line 581: notInNil Here impossible
Line 582: notInNil (There _) impossible
Line 583:  7
Line 584: Define—You can complete ?notInTail similarly, but you’ll need to work a bit
Line 585: harder to show that each case is impossible. Lifting to a top-level definition and
Line 586: then case splitting on the argument leads to the following: 
Line 587: notInTail : (notThere : Elem value xs -> Void) ->
Line 588: (notHere : (value = x) -> Void) ->
Line 589:             Elem value (x :: xs) -> Void
Line 590: notInTail notThere notHere Here = ?notInTail_rhs_1
Line 591: notInTail notThere notHere (There later) = ?notInTail_rhs_2
Line 592: For each hole, remember to check its type and the type of its local variables,
Line 593: because these will often give a strong hint as to how to proceed.
Line 594: 8
Line 595: Refine—For each case, you can use either notHere or notThere to produce the
Line 596: value of type Void that you need: 
Line 597: notInTail : (notThere : Elem value xs -> Void) ->
Line 598:             (notHere : (value = x) -> Void) ->
Line 599:             Elem value (x :: xs) -> Void
Line 600: notInTail notThere notHere Here = notHere Refl
Line 601: notInTail notThere notHere (There later) = notThere later
Line 602: 
Line 603: --- 페이지 275 ---
Line 604: 249
Line 605: Membership tests: the Elem predicate
Line 606: Here’s the completed definition, for reference.
Line 607: notInNil : Elem value [] -> Void
Line 608: notInNil Here impossible
Line 609: notInNil (There _) impossible
Line 610: notInTail : (notThere : Elem value xs -> Void) ->
Line 611: (notHere : (value = x) -> Void) -> Elem value (x :: xs) -> Void
Line 612: notInTail notThere notHere Here = notHere Refl
Line 613: notInTail notThere notHere (There later) = notThere later
Line 614: isElem : DecEq a => (value : a) -> (xs : Vect n a) -> Dec (Elem value xs)
Line 615: isElem value [] = No notInNil
Line 616: isElem value (x :: xs)
Line 617: = case decEq value x of
Line 618: Yes Refl => Yes Here
Line 619: No notHere => case isElem value xs of
Line 620: Yes prf => Yes (There prf)
Line 621: No notThere => No (notInTail notThere notHere)
Line 622: For comparison, listing 9.6 shows how you could define a Boolean test for checking
Line 623: vector membership. Here, I’ve used the Eq interface, so we don’t have any guarantees
Line 624: from the type about how the equality test behaves. Nevertheless, elem follows a struc-
Line 625: ture similar to decElem.
Line 626: elem : Eq ty => (value : ty) -> (xs : Vect n ty) -> Bool
Line 627: elem value [] = False
Line 628: elem value (x :: xs) = case value == x of
Line 629: False => elem value xs
Line 630: True => True
Line 631: Both definitions have a similar structure, but more work is required in isElem to show
Line 632: that the impossible cases are really impossible. As a trade-off, there’s no need for any
Line 633: tests for isElem, because the type is sufficiently precise that the implementation must
Line 634: be correct. 
Line 635: Exercises
Line 636: 1
Line 637: Data.List includes a version of Elem for List that works similarly to Elem for Vect.
Line 638: How would you define it?
Line 639: 2
Line 640: The following predicate states that a specific value is the last value in a List: 
Line 641: data Last : List a -> a -> Type where
Line 642: LastOne : Last [value] value
Line 643: LastCons : (prf : Last xs value) -> Last (x :: xs) value
Line 644: So, for example, you can construct a proof of Last [1,2,3] 3: 
Line 645: last123 : Last [1,2,3] 3
Line 646: Listing 9.5
Line 647: Complete definition of isElem (ElemType.idr)
Line 648: Listing 9.6
Line 649: A Boolean test for whether a value is in a vector (ElemBool.idr)
Line 650: 
Line 651: --- 페이지 276 ---
Line 652: 250
Line 653: CHAPTER 9
Line 654: Predicates: expressing assumptions and contracts in types
Line 655: last123 = LastCons (LastCons LastOne)
Line 656: Write an isLast function that decides whether a value is the last element in a List.
Line 657: It should have the following type: 
Line 658: isLast : DecEq a => (xs : List a) -> (value : a) -> Dec (Last xs value)
Line 659: You can test your answer at the REPL as follows: 
Line 660: *ex_9_1> isLast [1,2,3] 3
Line 661: Yes (LastCons (LastCons LastOne)) : Dec (Last [1, 2, 3] 3)
Line 662: 9.2
Line 663: Expressing program state in types: a guessing game
Line 664: In practice, the need for predicates like Elem and functions like removeElem arises nat-
Line 665: urally when we write functions that express characteristics of system state, such as vec-
Line 666: tor length, in their types. To conclude this chapter, we’ll look at a small example of
Line 667: where this happens: using the type system to encode simple properties of a word-
Line 668: guessing game, Hangman.
Line 669:  In Hangman, a player tries to guess a word by guessing one letter at a time. If they
Line 670: guess all the letters in the word, they win. Otherwise, they’re allowed a limited num-
Line 671: ber of incorrect guesses, after which they lose.
Line 672: 9.2.1
Line 673: Representing the game’s state
Line 674: Listing 9.7 shows how we can represent the current state of a word game as a data
Line 675: type, WordState, in Idris. There are two important parts of the state that capture the
Line 676: features of the game, and they’re written as parts of the type:
Line 677: The number of guesses the player has remaining
Line 678: The number of letters the player still has to guess
Line 679: data WordState : (guesses_remaining : Nat) -> (letters : Nat) -> Type where
Line 680: MkWordState : (word : String) ->
Line 681: (missing : Vect letters Char) ->
Line 682: WordState guesses_remaining letters
Line 683: A game is finished if either the number of guesses remaining is zero (in which case
Line 684: the player has lost) or the number of letters remaining is zero (in which case the
Line 685: player has won). Listing 9.8 shows how we can represent this in a data type. We can be
Line 686: certain that this captures only games that are won or lost, because we’re including the
Line 687: number of guesses and the number of letters remaining as arguments to WordState.
Line 688: Listing 9.7
Line 689: The game state (Hangman.idr)
Line 690: The word the player 
Line 691: is trying to guess
Line 692: Letters in the word that 
Line 693: have not yet been 
Line 694: guessed correctly
Line 695: guesses_remaining is an implicit
Line 696: argument of MkWordState, which
Line 697: we’ll keep track of in the type.
Line 698: 
Line 699: --- 페이지 277 ---
Line 700: 251
Line 701: Expressing program state in types: a guessing game
Line 702:  
Line 703: data Finished : Type where
Line 704: Lost : (game : WordState 0 (S letters)) -> Finished
Line 705: Won
Line 706: : (game : WordState (S guesses) 0) -> Finished
Line 707: The WordState dependent type stores the core data required by the game. By includ-
Line 708: ing the core components of the rules—the number of guesses and number of let-
Line 709: ters—as arguments to WordState, we’ll be able to see exactly how any function that
Line 710: uses a WordState implements the rules of the game. 
Line 711: 9.2.2
Line 712: A top-level game function
Line 713: We’ll take a top-down approach, defining a top-level function that implements a com-
Line 714: plete game. The following listing gives the starting point.
Line 715: game : WordState (S guesses) (S letters) -> IO Finished
Line 716: game st = ?game_rhs
Line 717: The type of game states that a game can proceed if there’s at least one guess remaining
Line 718: (S guesses) and at least one letter still to guess (S letters). It returns IO Finished,
Line 719: meaning that it performs interactive actions that produce game data in a Finished
Line 720: state. 
Line 721:  To implement the game, you’ll need to read a single letter from the user (any
Line 722: other input is invalid), check whether the letter input by the user is in the target word
Line 723: in the game state, update the game state, and loop if the game isn’t complete. You can
Line 724: update the state in one of the following ways:
Line 725: The letter is in the word, in which case you continue the game with the same
Line 726: number of guesses and one fewer letter.
Line 727: The letter isn’t in the word, in which case you continue the game with one
Line 728: fewer guess and the same number of letters.
Line 729: The numbers of guesses and letters used and remaining are explicitly recorded in the
Line 730: game state’s type. The next step, therefore, is to write a function that captures these
Line 731: state updates in its type. 
Line 732: 9.2.3
Line 733: A predicate for validating user input: ValidInput
Line 734: You can read user input using the IO action getLine: 
Line 735: getLine : IO String
Line 736: Listing 9.8
Line 737: Defining precisely when a game is in a finished state (Hangman.idr)
Line 738: Listing 9.9
Line 739: Top-level game function (Hangman.idr)
Line 740: A game is lost if zero 
Line 741: guesses remain.
Line 742: A game is won if zero letters
Line 743: remain to be guessed.
Line 744: ?game_rhs needs to read a letter and updates 
Line 745: the game state according to the guess.
Line 746: 
Line 747: --- 페이지 278 ---
Line 748: 252
Line 749: CHAPTER 9
Line 750: Predicates: expressing assumptions and contracts in types
Line 751: But because the user is guessing a letter, the only inputs that are valid are those that
Line 752: consist of exactly one character. For precision, you can make the notion of a valid
Line 753: input explicit in a predicate. Because String is a primitive, it’s difficult to reason
Line 754: about its individual components in a type, so you can use a List Char to represent the
Line 755: input in the predicate and convert as necessary:
Line 756: data ValidInput : List Char -> Type where
Line 757: Letter : (c : Char) -> ValidInput [c]
Line 758: To check whether a String is a valid input, you can write the following function,
Line 759: which returns either a proof that the input is valid, or a proof that it can never be
Line 760: valid, using Dec:
Line 761: isValidString : (s : String) -> Dec (ValidInput (unpack s))
Line 762: You’ll see the definition of isValidString shortly, in section 9.2.5. As an exercise, you
Line 763: can try writing it yourself, beginning with the following helper function: 
Line 764: isValidInput : (cs : List Char) -> Dec (ValidInput cs)
Line 765: Then, instead of using getLine, write a readGuess function that returns the user’s
Line 766: guess, along with an instance of a predicate that guarantees the user’s guess is a valid
Line 767: input:
Line 768: readGuess : IO (x ** ValidInput x)
Line 769: readGuess returns a dependent pair, where the first element is the input read from
Line 770: the console, and the second is a predicate that the input must satisfy.
Line 771: CONTRACTS ON RETURN VALUES
Line 772: By returning a value paired with a predicate
Line 773: on that value, the type of readGuess is expressing a contract that the return
Line 774: value must satisfy.
Line 775: The following listing gives the definition of readGuess.
Line 776: readGuess : IO (x ** ValidInput x)
Line 777: readGuess = do putStr "Guess:"
Line 778: x <- getLine
Line 779: case isValidString (toUpper x) of
Line 780: Yes prf => pure (_ ** prf)
Line 781: No contra => do putStrLn "Invalid guess"
Line 782: readGuess
Line 783: By using readGuess, you can be certain that any valid string read from the console is
Line 784: guaranteed to contain exactly one character. 
Line 785: Listing 9.10
Line 786: Read a guess from the console, which is guaranteed to be valid 
Line 787: (Hangman.idr)
Line 788: Reads a
Line 789: string from
Line 790: the console
Line 791: Converts the input to 
Line 792: uppercase so that you can treat 
Line 793: inputs as non-case-sensitive
Line 794: If it’s a valid input,
Line 795: returns the input
Line 796: and the proof
Line 797: If it’s not a valid input, 
Line 798: tries again
Line 799: 
Line 800: --- 페이지 279 ---
Line 801: 253
Line 802: Expressing program state in types: a guessing game
Line 803: 9.2.4
Line 804: Processing a guess
Line 805: Processing a guess will return a game state with one type if the guess is correct, and a
Line 806: different type if the guess is incorrect. You can use the Either generic type to repre-
Line 807: sent this. Remember that Either is a generic type defined in the Prelude that carries a
Line 808: value of two possible types:
Line 809: data Either a b = Left a | Right b
Line 810: Either is often used to represent the result of a computation that might fail, carrying
Line 811: information about the error if it does fail. By convention, we use Left for the error
Line 812: case and Right for the success case.1 You can think of an incorrect guess as being the
Line 813: error case, so the next listing shows the type you’ll use for a function that processes a
Line 814: guess.
Line 815: processGuess : (letter : Char) ->
Line 816: WordState (S guesses) (S letters) ->
Line 817: Either (WordState guesses (S letters))
Line 818: (WordState (S guesses) letters)
Line 819: This type states that, given a letter and an input game state, it will either produce a
Line 820: new game state where the number of guesses remaining has decreased (the guess was
Line 821: incorrect), or where the number of letters remaining has decreased (the guess was
Line 822: correct.)
Line 823: TYPES AS ABSTRACT STATE
Line 824: A value of type WordState guesses letters
Line 825: holds concrete information about system state, including the exact word to be
Line 826: guessed and exactly which letters are still missing. The type itself expresses
Line 827: abstract information about the game state (guesses remaining and number of
Line 828: missing letters), which allows you to express the rules in function types like
Line 829: processGuess.
Line 830: You can implement processGuess as follows:
Line 831: 1
Line 832: Define—You need to inspect the input game state, so you can case-split on the
Line 833: input state: 
Line 834: processGuess : (letter : Char) ->
Line 835: WordState (S guesses) (S letters) ->
Line 836: Either (WordState guesses (S letters))
Line 837: (WordState (S guesses) letters)
Line 838: processGuess letter (MkWordState word missing) = ?guess_rhs_1
Line 839: 1 “Right” also being a synonym of “correct.”
Line 840: Listing 9.11
Line 841: Type of a function that processes a user’s guess (Hangman.idr)
Line 842: Input game state, with at least 
Line 843: one guess remaining and at 
Line 844: least one letter to guess
Line 845: Correct guess (Right
Line 846: case), so remove a
Line 847: letter to guess
Line 848: Incorrect guess 
Line 849: (Left case), so remove
Line 850: an available guess
Line 851: 
Line 852: --- 페이지 280 ---
Line 853: 254
Line 854: CHAPTER 9
Line 855: Predicates: expressing assumptions and contracts in types
Line 856:  2
Line 857: Define—If the guessed letter is correct, it’ll be in the missing vector, and you’ll
Line 858: need to remove it. You can use isElem to find whether it’s there and define the
Line 859: function by case splitting on the result of isElem: 
Line 860: processGuess letter (MkWordState word missing)
Line 861: = case isElem letter missing of
Line 862: Yes prf => ?guess_rhs_2
Line 863: No contra => ?guess_rhs_3
Line 864:  3
Line 865: Refine—If the letter is in the vector of missing letters, you’ll return a new state
Line 866: with one fewer letters to guess. Otherwise, you’ll return a new state with one
Line 867: fewer guess available: 
Line 868: processGuess letter (MkWordState word missing)
Line 869: = case isElem letter missing of
Line 870: Yes prf => Right (MkWordState word ?nextVect)
Line 871: No contra => Left (MkWordState word missing)
Line 872: You have a hole, ?nextVect, for the updated vector of missing letters.
Line 873: 4
Line 874: Type, refine—The type of ?nextVect shows that you need to remove an element
Line 875: from the vector: 
Line 876: word : String
Line 877: letter : Char
Line 878: letters : Nat
Line 879: missing : Vect (S letters) Char
Line 880: prf : Elem letter missing
Line 881: guesses : Nat
Line 882: --------------------------------------
Line 883: nextVect : Vect letters Char
Line 884: You can complete the definition by using removeElem to remove letter from
Line 885: missing, and Idris will find the necessary proof, prf, as an auto implicit. This
Line 886: completes the definition: 
Line 887: processGuess : (letter : Char) ->
Line 888: WordState (S guesses) (S letters) ->
Line 889: Either (WordState guesses (S letters))
Line 890: (WordState (S guesses) letters)
Line 891: processGuess letter (MkWordState word missing)
Line 892: = case isElem letter missing of
Line 893: Yes prf => Right (MkWordState word (removeElem letter missing))
Line 894: No contra => Left (MkWordState word missing)
Line 895: EXPLICIT ASSUMPTIONS
Line 896: In the game state, you assume that the number of let-
Line 897: ters still to guess is the same as the length of the vector of missing letters. By
Line 898: putting this in the type of WordState and the type of processGuess, you
Line 899: can be sure that if you ever violate this assumption, your program will no lon-
Line 900: ger compile.
Line 901: You can complete the definition of game using processGuess to update the game state
Line 902: as necessary. 
Line 903: 
Line 904: --- 페이지 281 ---
Line 905: 255
Line 906: Expressing program state in types: a guessing game
Line 907: 9.2.5
Line 908: Deciding input validity: checking ValidInput
Line 909: Before completing the implementation of game, you’ll need to complete your imple-
Line 910: mentation of isValidString, which decides whether a string entered by the user is a
Line 911: valid input or not.
Line 912: data ValidInput : List Char -> Type where
Line 913: Letter : (c : Char) -> ValidInput [c]
Line 914: isValidNil : ValidInput [] -> Void
Line 915: isValidNil (Letter _) impossible
Line 916: isValidTwo : ValidInput (x :: y :: xs) -> Void
Line 917: isValidTwo (Letter _) impossible
Line 918: isValidInput : (cs : List Char) -> Dec (ValidInput cs)
Line 919: isValidInput [] = No isValidNil
Line 920: isValidInput (x :: []) = Yes (Letter x)
Line 921: isValidInput (x :: (y :: xs)) = No isValidTwo
Line 922: isValidString : (s : String) -> Dec (ValidInput (unpack s))
Line 923: isValidString s = isValidInput (unpack s)
Line 924: You can test this definition at the REPL by using >>= to take the output of readGuess,
Line 925: matching on the first component of the dependent pair, and passing it on to printLn:
Line 926: *Hangman> :exec readGuess >>= \(x ** _) => printLn x
Line 927: Guess: badguess
Line 928: Invalid guess
Line 929: Guess:
Line 930: Invalid guess
Line 931: Guess: f
Line 932: ['F']
Line 933: Now that you have the ability to read input that’s guaranteed to be in a valid form, and
Line 934: the ability to process guesses to update the game state, you can complete the top-level
Line 935: game implementation. 
Line 936: 9.2.6
Line 937: Completing the top-level game implementation
Line 938: The next listing shows one possible (if basic) way to complete the implementation of
Line 939: game. It uses processGuess to check the user’s input and reports whether a guess is
Line 940: correct or incorrect until the player has won or lost.
Line 941: Listing 9.12
Line 942: Showing that an input string must be either a valid or invalid input 
Line 943: (Hangman.idr)
Line 944: An input with one character is valid. 
Line 945: Remember that [c] desugars to c :: [].
Line 946: None of the constructors of ValidInput 
Line 947: have the type ValidInput [].
Line 948: None of the constructors of 
Line 949: ValidInput have a type of the 
Line 950: form ValidInput (x :: y :: xs).
Line 951: The only valid case, 
Line 952: because a constructor 
Line 953: of ValidInput has a 
Line 954: type of the form 
Line 955: ValidInput (x :: []).
Line 956: Entered by the user
Line 957: Putput by readGuess
Line 958: Entered by the user
Line 959: Output by readGuess
Line 960: Entered by the user
Line 961: Output by readGuess
Line 962: 
Line 963: --- 페이지 282 ---
Line 964: 256
Line 965: CHAPTER 9
Line 966: Predicates: expressing assumptions and contracts in types
Line 967:  
Line 968: game : WordState (S guesses) (S letters) -> IO Finished
Line 969: game {guesses} {letters} st
Line 970: = do (_ ** Letter letter) <- readGuess
Line 971: case processGuess letter st of
Line 972: Left l => do putStrLn "Wrong!"
Line 973: case guesses of
Line 974: Z => pure (Lost l)
Line 975: S k => game l
Line 976: Right r => do putStrLn "Right!"
Line 977: case letters of
Line 978: Z => pure (Won r)
Line 979: S k => game r
Line 980: By including the number of guesses and number of letters remaining in the type,
Line 981: you’ve essentially written an important rule of the game in the type of the guess func-
Line 982: tion. As a result, certain kinds of errors in the implementation can’t happen. For
Line 983: example, as long as you always use the guess function to update the game state, you
Line 984: avoid the following potential problems: 
Line 985: It’s impossible to test the wrong variable (guesses or letters) before continu-
Line 986: ing the game.2 Doing so would cause a type error.
Line 987: It’s impossible to continue a completed game, because there must be at least
Line 988: one guess remaining and at least one letter to guess.
Line 989: It’s impossible to finish a game prematurely, when there are both missing letters
Line 990: and guesses still available.
Line 991: The following listing shows a possible implementation of main that sets up a game
Line 992: with a target word, "Test", so requiring a player to guess the letters 'T', 'E', and 'S'.
Line 993: main : IO ()
Line 994: main = do result <- game {guesses=2}
Line 995:                  (MkWordState "Test" ['T', 'E', 'S'])
Line 996: case result of
Line 997: Lost (MkWordState word missing) =>
Line 998: putStrLn ("You lose. The word was " ++ word)
Line 999: Won game =>
Line 1000: putStrLn "You win!"
Line 1001: Listing 9.13
Line 1002: Top-level game function (Hangman.idr)
Line 1003: 2 I really did make this mistake when writing this example!
Line 1004: Listing 9.14
Line 1005: A main program to set up a game (Hangman.idr)
Line 1006: You’ll need to check guesses and 
Line 1007: letters to find out if the player has 
Line 1008: won or lost, so bring them into scope.
Line 1009: Extract the letter by 
Line 1010: pattern-matching on the 
Line 1011: ValidInput predicate.
Line 1012: The guess was wrong; 
Line 1013: check whether there 
Line 1014: are any guesses left, 
Line 1015: and continue if so.
Line 1016: The guess was correct; 
Line 1017: check whether there 
Line 1018: are any letters left, and 
Line 1019: continue if so.
Line 1020: Sets up a 
Line 1021: new game 
Line 1022: with 2 wrong 
Line 1023: guesses 
Line 1024: allowed and 
Line 1025: a target 
Line 1026: word, “Test”
Line 1027: 
Line 1028: --- 페이지 283 ---
Line 1029: 257
Line 1030: Summary
Line 1031: 9.3
Line 1032: Summary
Line 1033: You can write types that express assumptions about how values relate.
Line 1034: The Elem dependent type is a predicate that expresses that a value must be con-
Line 1035: tained in a vector.
Line 1036: By passing a predicate as an argument to a function, you can express a contract
Line 1037: that the inputs to the function must follow.
Line 1038: You can write a function to show that a predicate is decidable, using Dec.
Line 1039: Idris will attempt to find values for arguments marked auto by expression
Line 1040: search. 
Line 1041: You can capture properties of a system’s state (such as the rules of a game) in a
Line 1042: type.
Line 1043: Predicates can describe the validity of user input and ensure that the user input
Line 1044: is validated when necessary.