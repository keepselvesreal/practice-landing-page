Line 1: 
Line 2: --- 페이지 234 ---
Line 3: 208
Line 4: Equality: expressing
Line 5: relationships between data
Line 6: You’ve now seen several ways in which first-class types increase the expressivity of
Line 7: the type system, and the precision of the types we give to functions. You’ve seen
Line 8: how to use increased precision in types (along with holes) to help write functions,
Line 9: and how to write functions to calculate types. Another way you can use first-class
Line 10: types to increase the precision of your types, and to increase confidence in func-
Line 11: tions behaving correctly, is to write types specifically to express properties of data
Line 12: and the relationships between data.
Line 13:  In this chapter, we’ll look at a simple property, using types to express guarantees
Line 14: that values are equal. You’ll also see how to express guarantees that values are not
Line 15: equal. Properties such as equality and inequality are sometimes required when
Line 16: This chapter covers
Line 17: Expressing properties of functions and data
Line 18: Checking and guaranteeing equalities between 
Line 19: data
Line 20: Showing when cases are impossible with the 
Line 21: empty type Void
Line 22: 
Line 23: --- 페이지 235 ---
Line 24: 209
Line 25: Guaranteeing equivalence of data with equality types
Line 26: you’re defining more-complex functions with dependent types, where the relation-
Line 27: ship between values might not be immediately obvious to Idris. For example, as you’ll
Line 28: see when we define reverse on vectors, the input and output vector lengths must be
Line 29: the same, so we’ll need to explain to the compiler why the length is preserved.
Line 30:  We’ll start by looking at a function we’ve already used, exactLength, and see in
Line 31: some detail how to build it from first principles.
Line 32: 8.1
Line 33: Guaranteeing equivalence of data with equality types
Line 34: When you want to compare values for equality, you can use the == operator, which
Line 35: returns a value of type Bool, given two values in a type ty for which there’s an imple-
Line 36: mentation of the Eq interface: 
Line 37: (==) : Eq ty => ty -> ty -> Bool
Line 38: But if you look closely at this type, what does it tell you about the relationships
Line 39: between the inputs (of type ty) and the output (of type Bool)?
Line 40:  In fact, it tells you nothing at all! Without looking at the specific implementation,
Line 41: you don’t know exactly how == will behave. Any of the following would be reasonable
Line 42: behavior for an implementation of == in the Eq interface, at least as far as the type is
Line 43: concerned: 
Line 44: Always returning True
Line 45: Always returning False
Line 46: Returning whether the inputs are not equal
Line 47: It would be surprising to programmers if == behaved in any of these ways, but as far as
Line 48: the Idris type checker is concerned, it can make no assumptions other than those
Line 49: given explicitly in the type. If you want to compare values at the type level, therefore,
Line 50: you’ll need something more expressive.
Line 51:  In fact, you’ve already seen an example of a situation where you might want to do
Line 52: this: at the end of chapter 5 you used the exactLength function to check whether a
Line 53: Vect had a specific length: 
Line 54: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 55: You used this function to check whether two vectors entered by a user had exactly
Line 56: the same length. Given a specific length, len, and a vector of length, m, it returns the
Line 57: following: 
Line 58: 
Line 59: Nothing, if len is not the same as m
Line 60: 
Line 61: Just input, if len is the same as m
Line 62: In this section, we’ll look at how to implement exactLength by representing equality
Line 63: as a type, and you’ll see in more detail why == isn’t sufficient. We’ll start by trying to
Line 64: implement it using == and see where we run into limitations.
Line 65: 
Line 66: --- 페이지 236 ---
Line 67: 210
Line 68: CHAPTER 8
Line 69: Equality: expressing relationships between data
Line 70: 8.1.1
Line 71: Implementing exactLength, first attempt
Line 72: Rather than importing Data.Vect, which defines exactLength, we’ll begin by defin-
Line 73: ing Vect by hand and giving a type and a skeleton definition of exactLength. The fol-
Line 74: lowing listing shows our starting point, in a file named ExactLength.idr.
Line 75: data Vect : Nat -> Type -> Type where
Line 76: Nil
Line 77: : Vect Z a
Line 78: (::) : a -> Vect k a -> Vect (S k) a
Line 79: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 80: exactLength len input = ?exactLength_rhs
Line 81: You should expect to be able to implement exactLength by comparing the length of
Line 82: input with the desired length, len. If they’re equal, then input has length len, so its
Line 83: type should be considered equivalent to Vect len a, and you can return it directly.
Line 84: Otherwise, you return Nothing.
Line 85:  As a first attempt, you can try the following steps:
Line 86: 1
Line 87: Define—Because m doesn’t appear on the left side of the skeleton definition,
Line 88: you’ll need to bring it into scope explicitly in order to compare len and m. You
Line 89: can do this by updating the definition to the following: 
Line 90: exactLength {m} len input = ?exactLength_rhs
Line 91: Recall from chapter 3 that an implicit argument such as m can be used in the
Line 92: definition if it’s written inside braces on the left side.
Line 93:  2
Line 94: Define—You can now compare m and len for equality using == and inspect the
Line 95: result in a case statement: 
Line 96: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 97: exactLength {m} len input = case m == len of
Line 98: False => ?exactLength_rhs_1
Line 99: True => ?exactLength_rhs_2
Line 100:  3
Line 101: Refine—For ?exactLength_rhs_1, the lengths are different, so you return
Line 102: Nothing: 
Line 103: exactLength {m} len input = case m == len of
Line 104: False => Nothing
Line 105: True => ?exactLength_rhs_2
Line 106:  4
Line 107: Refine—For ?exactLength_rhs_2, you’d like to return Just input because the
Line 108: lengths are equal. You can start with Just: 
Line 109: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 110: exactLength {m} len input = case m == len of
Line 111: False => Nothing
Line 112: True => Just ?exactLength_rhs_2
Line 113: Listing 8.1
Line 114: A definition of Vect and the type and skeleton definition of exactLength
Line 115: (ExactLength.idr)
Line 116: 
Line 117: --- 페이지 237 ---
Line 118: 211
Line 119: Guaranteeing equivalence of data with equality types
Line 120: 5
Line 121: Type—Then, you can take a look at the types of the variables in scope, and the
Line 122: type required to fill in the ?exactLength_rhs_2 hole: 
Line 123: a : Type
Line 124: m : Nat
Line 125: len : Nat
Line 126: input : Vect m a
Line 127: --------------------------------------
Line 128: exactLength_rhs_2 : Vect len a
Line 129: Even though you’ve checked that m and len are equal using ==, you can’t fill in
Line 130: the hole with input because it has type Vect m a, and the required type is Vect
Line 131: len a. The problem, as when defining zipInputs at the end of chapter 5, is that
Line 132: the type of == isn’t informative enough to guarantee that m and len are equal,
Line 133: even if it returns True.
Line 134: You will, therefore, need to consider alternative approaches to implementing
Line 135: exactLength, using a more informative type when comparing m and len.
Line 136: A variable’s type tells Idris what possible values a variable can have, but it says nothing
Line 137: about where the value has come from. If a variable has type Bool, Idris knows that it
Line 138: can have either of the values True or False, but nothing about the computation that
Line 139: has produced the value. There are lots of possible computations that could produce a
Line 140: result of type Bool other than testing for equality. Furthermore, equality is defined by
Line 141: the Eq interface, and there are no guarantees in the type about how that interface
Line 142: might be implemented.
Line 143:  Instead, you’ll need to create a more precise type for the equality test, where the
Line 144: type guarantees that a comparison between two inputs can only be successful if the
Line 145: inputs really are identical. In the rest of this section, you’ll see how to do this from first
Line 146: principles, and how to use the new equality type to implement exactLength. 
Line 147: 8.1.2
Line 148: Expressing equality of Nats as a type
Line 149: Listing 8.2 shows a dependent type, EqNat. It has two numbers as arguments, num1 and
Line 150: num2. If you have a value of type EqNat num1 num2, you know that num1 and num2 must
Line 151: be the same number because the only constructor, Same, can only build something
Line 152: with a type of the form EqNat num num, where the two arguments are the same.
Line 153: data EqNat : (num1 : Nat) -> (num2 : Nat) -> Type where
Line 154:     Same : (num : Nat) -> EqNat num num
Line 155: With dependent types, you can use types such as EqNat to express additional informa-
Line 156: tion about other data, in this case expressing that two Nats are guaranteed to be equal.
Line 157: This is a powerful concept, as you’ll soon see, and can take some time to fully appreci-
Line 158: ate. We’ll therefore look at representing and checking equalities in some depth.
Line 159: Listing 8.2
Line 160: Representing equal Nats as a type (EqNat.idr)
Line 161: The only constructor, Same, 
Line 162: constructs evidence that num 
Line 163: is equal to itself.
Line 164: 
Line 165: --- 페이지 238 ---
Line 166: 212
Line 167: CHAPTER 8
Line 168: Equality: expressing relationships between data
Line 169:  First, to see how EqNat works, let’s try a few examples at the REPL: 
Line 170: *EqNat> Same 4
Line 171: Same 4 : EqNat 4 4
Line 172: *EqNat> Same 5
Line 173: Same 5 : EqNat 5 5
Line 174: *EqNat> the (EqNat 3 3) (Same _)
Line 175: Same 3 : EqNat 3 3
Line 176: *EqNat> Same (2 + 2)
Line 177: Same 4 : EqNat 4 4
Line 178: Whatever you try, the argument in the type is repeated. It is, nevertheless, perfectly
Line 179: valid to write a type with unequal arguments: 
Line 180: *EqNat> EqNat 3 4
Line 181: EqNat 3 4 : Type
Line 182: But if you try to construct a value with this type, you can’t succeed and will always get a
Line 183: type error: 
Line 184: *EqNat> the (EqNat 3 4) (Same _)
Line 185: (input):1:5:When checking argument value to function Prelude.Basics.the:
Line 186: Type mismatch between
Line 187: EqNat num num (Type of Same num)
Line 188: and
Line 189: EqNat 3 4 (Expected type)
Line 190: Specifically:
Line 191: Type mismatch between
Line 192: 0
Line 193: and
Line 194: 1
Line 195: This error message indicates that 3 and 4 need to be the same, because they both
Line 196: need to be instantiated for num in the type of Same. The type EqNat 3 4 is an empty type,
Line 197: meaning that there are no values of that type.
Line 198: SPECIFICITY IN ERROR MESSAGES
Line 199: You’ll notice that in error messages, Idris
Line 200: often reports the error in two ways. The first part gives an overall type mis-
Line 201: match. This can become quite large, however, so Idris also reports the specific
Line 202: part of the expression that didn’t match. Here, it reports a mismatch between
Line 203: 0 and 1 because of the way Nat is defined in terms of Z and S. The overall
Line 204: mismatch is between S (S (S Z)) and S (S (S (S Z))), for which the specific
Line 205: difference is between Z and S Z. 
Line 206: 8.1.3
Line 207: Testing for equality of Nats
Line 208: We’ll use EqNat to help implement exactLength. Because EqNat num1 num2 is essen-
Line 209: tially a proof that num1 must be equal to num2, we’ll write a function that checks
Line 210: whether the input lengths are equal, and, if they are, express that equality as an
Line 211: instance of EqNat.
Line 212: 
Line 213: --- 페이지 239 ---
Line 214: 213
Line 215: Guaranteeing equivalence of data with equality types
Line 216:  We’ll begin by writing a checkEqNat function that either returns a proof that its
Line 217: inputs are the same, in the form of EqNat, or Nothing if the inputs are different. It has
Line 218: the following type:
Line 219: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 220: Once implemented, it will behave as in the following examples:
Line 221: *EqNat> checkEqNat 5 5
Line 222: Just (Same 5) : Maybe (EqNat 5 5)
Line 223: *EqNat> checkEqNat 1 2
Line 224: Nothing : Maybe (EqNat 1 2)
Line 225: Because we can only have a value of type EqNat num1 num2 for a specific num1 and num2
Line 226: if num1 and num2 are identical, the type of checkEqNat guarantees that if it’s successful
Line 227: (that is, returns a value of the form Just p), then its inputs really must be equal.
Line 228:  You can implement the function as follows:
Line 229: 1
Line 230: Type—Begin with a type and a skeleton definition: 
Line 231: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 232: checkEqNat num1 num2 = ?checkEqNat_rhs
Line 233:  2
Line 234: Define—You can define the function by case splitting on both Nat inputs. First,
Line 235: case-split on num1: 
Line 236: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 237: checkEqNat Z num2 = ?checkEqNat_rhs_1
Line 238: checkEqNat (S k) num2 = ?checkEqNat_rhs_2
Line 239:  3
Line 240: Define—Then, case-split on num2 in both cases: 
Line 241: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 242: checkEqNat Z Z = ?checkEqNat_rhs_3
Line 243: checkEqNat Z (S k) = ?checkEqNat_rhs_4
Line 244: checkEqNat (S k) Z = ?checkEqNat_rhs_1
Line 245: checkEqNat (S k) (S j) = ?checkEqNat_rhs_5
Line 246:  4
Line 247: Refine—If you take a look at the type of the ?checkEqNat_rhs_3 hole, you’ll see
Line 248: that you need to provide evidence that 0 is the same as itself, so you can fill this
Line 249: in with Just (Same 0). For ?checkEqNat_rhs_4 and ?checkEqNat_rhs_1, you
Line 250: can’t provide any evidence that 0 is the same as a non-zero number, so return
Line 251: Nothing. You now have this: 
Line 252: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 253: checkEqNat Z Z = Just (Same 0)
Line 254: checkEqNat Z (S k) = Nothing
Line 255: checkEqNat (S k) Z = Nothing
Line 256: checkEqNat (S k) (S j) = ?checkEqNat_rhs_5
Line 257:  5
Line 258: Refine—The result for ?checkEqNat_rhs_5 depends on whether k is equal to j,
Line 259: which you can determine by making a recursive call and then case splitting on
Line 260: the result: 
Line 261: 
Line 262: --- 페이지 240 ---
Line 263: 214
Line 264: CHAPTER 8
Line 265: Equality: expressing relationships between data
Line 266: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 267: case_val => ?checkEqNat_rhs_5
Line 268:  6
Line 269: Define—Case splitting on case_val leads to cases for when k and j aren’t equal
Line 270: (Nothing) and when they are equal (Just x). You can rename the Just x pro-
Line 271: duced by the case split to something more informative, and fill in the case
Line 272: where the recursive call produces Nothing: 
Line 273: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 274: Nothing => Nothing
Line 275: Just eq => ?checkEqNat_rhs_2
Line 276:  7
Line 277: Type—Looking at the type of checkEqNat_rhs_2 gives you some information
Line 278: about how to proceed: 
Line 279: k : Nat
Line 280: j : Nat
Line 281: eq : EqNat k j
Line 282: --------------------------------------
Line 283: checkEqNat_rhs_2 : Maybe (EqNat (S k) (S j))
Line 284: The type of eq is EqNat k j, and you’re looking for something of type Maybe
Line 285: (EqNat (S k) (S j)).
Line 286:  8
Line 287: Refine—If k and j are equal, you know that S k and S j must be equal, so you
Line 288: can return a value constructed with Just: 
Line 289: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 290: Nothing => Nothing
Line 291: Just eq => Just ?checkEqNat_rhs_2
Line 292: 9
Line 293: Refine—To complete the definition, rename the remaining hole, and lift it to a
Line 294: top-level definition, which you’ll implement in the next section. 
Line 295: sameS : (eq : EqNat k j) -> EqNat (S k) (S j)
Line 296: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 297: checkEqNat Z Z = Just (Same Z)
Line 298: checkEqNat Z (S k) = Nothing
Line 299: checkEqNat (S k) Z = Nothing
Line 300: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 301: Nothing => Nothing
Line 302: Just eq => Just (sameS eq)
Line 303: You can see from the type of the lifted definition, sameS, that it’s a function that takes
Line 304: evidence that k and j are equal, and returns evidence that S k and S j are equal. By
Line 305: expressing equality between numbers as a dependent data type, EqNat, you’re able to
Line 306: write functions like sameS that take an instance of EqNat as an input and manipulate
Line 307: them, essentially deducing additional information about equalities. 
Line 308: 
Line 309: --- 페이지 241 ---
Line 310: 215
Line 311: Guaranteeing equivalence of data with equality types
Line 312: 8.1.4
Line 313: Functions as proofs: manipulating equalities
Line 314: It’s impossible to create an instance of EqNat k j when k and j are different, which
Line 315: means you can think of sameS as a proof that if k and j are equal, S k and S j are also
Line 316: equal.
Line 317:  Let’s now try implementing sameS. For clarity, we’ll make the Nat arguments
Line 318: explicit:
Line 319: sameS : (k : Nat) -> (j : Nat) -> (eq : EqNat k j) -> EqNat (S k) (S j)
Line 320: sameS k j eq = ?sameS_rhs
Line 321: You can implement sameS with the following steps: 
Line 322: 1
Line 323: Define—Begin by creating a skeleton definition: 
Line 324: sameS : (k : Nat) -> (j : Nat) -> (eq : EqNat k j) -> EqNat (S k) (S j)
Line 325: sameS k j eq = ?sameS_rhs
Line 326:  2
Line 327: Define—Next, in Atom, ask to case-split on eq:
Line 328: sameS : (k : Nat) -> (j : Nat) -> (eq : EqNat k j) -> EqNat (S k) (S j)
Line 329: sameS k k (Same k) = ?sameS_rhs_1
Line 330: Notice that k appears three times on the left side of this definition! Because
Line 331: you’ve expressed a relationship between k and j using eq in the type of sameS,
Line 332: and you’ve case-split on eq, Idris has noticed that both Nat inputs must be the
Line 333: same. Not only that, if you try to give a different value, it will report an error. If,
Line 334: instead, you write this, 
Line 335: sameS k j (Same k) = ?sameS_rhs_1
Line 336: then Idris will report the following: 
Line 337: EqNat.idr:15:7:When checking left hand side of sameS:
Line 338: Type mismatch between
Line 339: j (Inferred value)
Line 340: and
Line 341: k (Given value)
Line 342: In other words, because the type states that both Nat inputs must be the same,
Line 343: Idris isn’t happy that they’re different. So, revert to the left side that Idris gener-
Line 344: ated after the case split on eq: 
Line 345: sameS : (k : Nat) -> (j : Nat) -> (eq : EqNat k j) -> EqNat (S k) (S j)
Line 346: sameS k k (Same k) = ?sameS_rhs_1
Line 347:  3
Line 348: Type—If you check the type of ?sameS_rhs_1, you’ll see that you need to pro-
Line 349: vide evidence that S k is the same as itself: 
Line 350: k : Nat
Line 351: --------------------------------------
Line 352: sameS_rhs_1 : EqNat (S k) (S k)
Line 353: 4
Line 354: Refine—You can therefore complete the definition as follows: 
Line 355: sameS : (k : Nat) -> (j : Nat) -> (eq : EqNat k j) -> EqNat (S k) (S j)
Line 356: sameS k k (Same k) = Same (S k)
Line 357: 
Line 358: --- 페이지 242 ---
Line 359: 216
Line 360: CHAPTER 8
Line 361: Equality: expressing relationships between data
Line 362: PROOFS IN IDRIS
Line 363: In principle, you can state and try to prove complex proper-
Line 364: ties of any function in Idris. For example, you could write a function whose
Line 365: type states that reversing a list twice yields the original list. In practice, how-
Line 366: ever, you’ll rarely need to manipulate equalities much more complex than the
Line 367: implementation of sameS. Nevertheless, you’ll see a bit more about manipu-
Line 368: lating equalities, and where they arise when defining functions, in section 8.2.
Line 369: Listing 8.3 gives the complete definition of checkEqNat, using the version of sameS
Line 370: with explicit arguments. You could also write this function without using sameS,
Line 371: instead using a case split on eq. You could also use do notation, as described at the end
Line 372: of chapter 6, to make the definition more concise. As exercises, try reimplementing it
Line 373: in each of these ways. 
Line 374: sameS : (k : Nat) -> (j : Nat) -> (eq : EqNat k j) -> EqNat (S k) (S j)
Line 375: sameS k k (Same k) = Same (S k)
Line 376: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (EqNat num1 num2)
Line 377: checkEqNat Z Z = Just (Same 0)
Line 378: checkEqNat Z (S k) = Nothing
Line 379: checkEqNat (S k) Z = Nothing
Line 380: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 381: Nothing => Nothing
Line 382: Just eq => Just (sameS _ _ eq)
Line 383: Unlike ==, checkEqNat expresses the relationship between its inputs and its output
Line 384: precisely in its type. Using this, we can make another attempt to implement exact-
Line 385: Length. 
Line 386: 8.1.5
Line 387: Implementing exactLength, second attempt
Line 388: Earlier, we reached the following point in implementing exactLength, before estab-
Line 389: lishing that a Boolean comparison wasn’t sufficient: 
Line 390: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 391: exactLength {m} len input = case m == len of
Line 392: False => ?exactLength_rhs_1
Line 393: True => ?exactLength_rhs_2
Line 394: Instead of using the Boolean comparison operator == to compare m and len, you can
Line 395: try using checkEqNat m len. This will return a value of type Maybe (EqNat m len), so if
Line 396: m and len are equal, you’ll have some additional information in the type that states the
Line 397: meaning of the result of the comparison precisely. In this second attempt, you can
Line 398: implement the function as follows:
Line 399: 1
Line 400: Define—As before, begin with a type and a skeleton definition, bringing m into
Line 401: scope on the left side: 
Line 402: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 403: exactLength {m} len input = ?exactLength_rhs
Line 404: Listing 8.3
Line 405: Testing for equality of Nats with EqNat (EqNat.idr)
Line 406: Z and S are the canonical 
Line 407: constructors for Nat and 
Line 408: can never be equal.
Line 409: S k and S j are equal if k and j are equal. You 
Line 410: use sameS to provide evidence for this.
Line 411: 
Line 412: --- 페이지 243 ---
Line 413: 217
Line 414: Guaranteeing equivalence of data with equality types
Line 415:  2
Line 416: Define—Instead of defining the function by case splitting on the result of m ==
Line 417: len, case-split on the result of checkEqNat: 
Line 418: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 419: exactLength {m} len input = case checkEqNat m len of
Line 420: Nothing => ?exactLength_rhs_1
Line 421: Just eq_nat => ?exactLength_rhs_2
Line 422:  3
Line 423: Refine—If checkEqNat returns Nothing, the inputs were different, so the input
Line 424: vector is the wrong length: 
Line 425: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 426: exactLength {m} len input = case checkEqNat m len of
Line 427: Nothing => Nothing
Line 428: Just eq_nat => Just ?exactLength_rhs_2
Line 429:  4
Line 430: Type—If checkEqNat returns Just eq_nat, the lengths are equal, and eq_nat
Line 431: provides evidence that they’re equal. For ?exactLength_rhs_2, you have this: 
Line 432: m : Nat
Line 433: len : Nat
Line 434: eq_nat : EqNat m len
Line 435: a : Type
Line 436: input : Vect m a
Line 437: --------------------------------------
Line 438: exactLength_rhs_2 : Maybe (Vect len a)
Line 439:  5
Line 440: Define—As before, you still need to provide a result of type Maybe (Vect len a),
Line 441: and all you have available is input of type Vect m a. But you also have eq_nat,
Line 442: which provides evidence that m and len are equal. If you case-split on eq_nat,
Line 443: you’ll get the following: 
Line 444: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 445: exactLength {m} len input = case checkEqNat m len of
Line 446: Nothing => Nothing
Line 447: Just (Same len) => ?exactLength_rhs_1
Line 448: Then, when inspecting the type of the new hole, ?exactLength_rhs_1, you’ll
Line 449: see this: 
Line 450: m : Nat
Line 451: a : Type
Line 452: input : Vect len a
Line 453: --------------------------------------
Line 454: exactLength_rhs_1 : Maybe (Vect len a)
Line 455: Because eq_nat can only take the form Same len, and the type of Same len
Line 456: forces m to be identical to len, Idris has refined the required type to be Maybe
Line 457: (Vect len a).
Line 458: 6
Line 459: Refine—From here, it’s easy to complete the definition:
Line 460: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 461: exactLength {m} len input = case checkEqNat m len of
Line 462: Nothing => Nothing
Line 463: Just (Same len) => Just input
Line 464: 
Line 465: --- 페이지 244 ---
Line 466: 218
Line 467: CHAPTER 8
Line 468: Equality: expressing relationships between data
Line 469: This isn’t exactly the definition used in the Prelude, however. Instead, the Prelude
Line 470: uses a generic equality type, built into Idris. 
Line 471: 8.1.6
Line 472: Equality in general: the = type
Line 473: Rather than defining a specific equality type and function for every possible type
Line 474: you’ll need to compare, such as Nat with EqNat and checkEqNat here, Idris provides a
Line 475: generic equality type. This is built into Idris’s syntax, so you can’t define this yourself
Line 476: (because = is a reserved symbol), but conceptually it would be defined as follows. 
Line 477: data (=) : a -> b -> Type where
Line 478: Refl : x = x
Line 479: The name Refl is short for reflexive, a mathematical term that (informally) means that
Line 480: a value is equal to itself. As with EqNat, you can try some examples at the REPL: 
Line 481: Idris> the ("Hello" = "Hello") Refl
Line 482: Refl : "Hello" = "Hello"
Line 483: Idris> the (True = True) Refl
Line 484: Refl : True = True
Line 485: If you give more-complex expressions as part of the type, Idris will evaluate them. For
Line 486: example, if you give the expression 2 + 2 as part of a type, 2 + 2 = 4, Idris will evaluate
Line 487: it: 
Line 488: Idris> the (2 + 2 = 4) Refl
Line 489: Refl : 4 = 4
Line 490: As before, if you try to use Refl to build an instance of an equality type using two
Line 491: unequal values, you’ll get an error:
Line 492: Idris> the (True = False) Refl
Line 493: (input):1:5:When checking argument value to function Prelude.Basics.the:
Line 494: Type mismatch between
Line 495: x = x (Type of Refl)
Line 496: and
Line 497: True = False (Expected type)
Line 498: Specifically:
Line 499: Type mismatch between
Line 500: True
Line 501: and
Line 502: False
Line 503: Using the built-in equality type, rather than EqNat, you can define checkEqNat as
Line 504: follows.
Line 505: Listing 8.4
Line 506: Conceptual definition of a generic equality type
Line 507: = takes two arguments: one of 
Line 508: some generic type a, and the 
Line 509: other of some generic type b.
Line 510: Like Same, but x is an 
Line 511: implicit argument
Line 512: 
Line 513: --- 페이지 245 ---
Line 514: 219
Line 515: Guaranteeing equivalence of data with equality types
Line 516:  
Line 517: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (num1 = num2)
Line 518: checkEqNat Z Z = Just Refl
Line 519: checkEqNat Z (S k) = Nothing
Line 520: checkEqNat (S k) Z = Nothing
Line 521: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 522: Nothing => Nothing
Line 523: Just prf => Just (cong prf)
Line 524: Exercises
Line 525: 1
Line 526: Implement the following function, which states that if you add the same value onto
Line 527: the front of equal lists, the resulting lists are also equal: 
Line 528: same_cons : {xs : List a} -> {ys : List a} ->
Line 529: xs = ys -> x :: xs = x :: ys
Line 530: Because this function represents an equality proof, it’s sufficient to know that your
Line 531: definition type-checks and is total: 
Line 532: *ex_8_1> :total same_cons
Line 533: Main.same_cons is Total
Line 534:  2
Line 535: Implement the following function, which states that if two values, x and y, are equal,
Line 536: and two lists, xs and ys, are equal, then the two lists x :: xs and y :: ys must also be
Line 537: equal: 
Line 538: same_lists : {xs : List a} -> {ys : List a} ->
Line 539: x = y -> xs = ys -> x :: xs = y :: ys
Line 540: Again, it’s sufficient to know that your definition type-checks.
Line 541:  3
Line 542: Define a type, ThreeEq, that expresses that three values must be equal.
Line 543: Hint: ThreeEq should have the type a -> b -> c -> Type.
Line 544: 4
Line 545: Implement the following function, which uses ThreeEq: 
Line 546: allSameS : (x, y, z : Nat) -> ThreeEq x y z -> ThreeEq (S x) (S y) (S z)
Line 547: What does this type mean?
Line 548: Listing 8.5
Line 549: Checking equality between Nats using the generic equality type 
Line 550: (CheckEqMaybe.idr)
Line 551: cong is a generic 
Line 552: version of sameS.
Line 553: Congruence
Line 554: In listing 8.5, you used cong to convert a value of type k = j to a value of type S
Line 555: k = S j. It has the following type:
Line 556: cong : {func : a -> b} -> x = y -> func x = func y
Line 557: In other words, given some (implicit) function, func, if you have two values that are
Line 558: equal, then applying func to those values gives an equal result. This does the same
Line 559: job as sameS, using the generic equality type.  
Line 560: 
Line 561: --- 페이지 246 ---
Line 562: 220
Line 563: CHAPTER 8
Line 564: Equality: expressing relationships between data
Line 565: 8.2
Line 566: Equality in practice: types and reasoning
Line 567: Equality proofs, and functions that manipulate them, can be useful when defining
Line 568: functions with dependent types. You saw a small example of this when implementing
Line 569: checkEqNat, where you wrote a sameS function to show that adding one to equal num-
Line 570: bers results in equal numbers.
Line 571:  Reasoning about equality often becomes necessary when writing functions on
Line 572: types that are indexed by numbers. For example, when manipulating vectors, you
Line 573: might need to prove the equivalence between two expressions with natural numbers
Line 574: that appear in the types of the vectors. To see how this can happen and how to deal
Line 575: with it, we’ll look at how to implement a function that reverses a Vect.
Line 576: 8.2.1
Line 577: Reversing a vector
Line 578: If you import Data.Vect, you’ll get access to a function that reverses a vector, with the
Line 579: following type:
Line 580: reverse : Vect n elem -> Vect n elem
Line 581: The type states that reversing a vector preserves the length of the input vector. You’d
Line 582: expect it to be fairly straightforward to implement this function using the following
Line 583: rules: 
Line 584: If the input vector is empty, return an empty vector.
Line 585: If the input vector isn’t empty and has a head x and a tail xs, reverse xs and
Line 586: append x.
Line 587: Let’s see what happens if we try to implement our own version, myReverse, in the file
Line 588: ReverseVec.idr:
Line 589: 1
Line 590: Type, define—Begin with a type and a skeleton definition, and case-split on the
Line 591: input: 
Line 592: myReverse : Vect n elem -> Vect n elem
Line 593: myReverse [] = ?myReverse_rhs_1
Line 594: myReverse (x :: xs) = ?myReverse_rhs_2
Line 595:  2
Line 596: Refine—For ?myReverse_rhs_1, return an empty vector: 
Line 597: myReverse : Vect n elem -> Vect n elem
Line 598: myReverse [] = []
Line 599: myReverse (x :: xs) = ?myReverse_rhs_2
Line 600: 3
Line 601: Refine failure—For ?myReverse_rhs_2, you’d like to be able to reverse xs and
Line 602: append x, as follows, but unfortunately this fails: 
Line 603: myReverse : Vect n elem -> Vect n elem
Line 604: myReverse [] = []
Line 605: myReverse (x :: xs) = myReverse xs ++ [x]
Line 606: The error message tells you that Idris has found a mismatch between the type of
Line 607: the value you’ve given, Vect (k + 1), and the expected type, Vect (S k): 
Line 608: This line has 
Line 609: a type error
Line 610: 
Line 611: --- 페이지 247 ---
Line 612: 221
Line 613: Equality in practice: types and reasoning
Line 614: ReverseVec.idr:6:12:
Line 615: When checking right hand side of myReverse with expected type
Line 616: Vect (S k) elem
Line 617: Type mismatch between
Line 618: Vect (k + 1) elem (Type of myReverse xs ++ [x])
Line 619: and
Line 620: Vect (S k) elem (Expected type)
Line 621: This seems surprising, because our knowledge of the behavior of addition sug-
Line 622: gests that S k and k + 1 will always evaluate to the same result, whatever the value
Line 623: of k.
Line 624: We’ll postpone the completion of this definition and take a closer look at how type
Line 625: checking works in Idris in order to understand what has gone wrong and how we
Line 626: might correct it. 
Line 627: 8.2.2
Line 628: Type checking and evaluation
Line 629: When Idris type-checks an expression, it will look at the expected type of the expression,
Line 630: and check that the type of the given expression matches it, after evaluating both. The
Line 631: following code fragment will type-check:
Line 632: test1 : Vect 4 Int
Line 633: test1 = [1, 2, 3, 4]
Line 634: test2: Vect (2 + 2) Int
Line 635: test2 = test1
Line 636: Even though test1 and test2 have different expressions in their types, these expres-
Line 637: sions evaluate to the same result, so you can define test2 to return test1.
Line 638:  You can see at the REPL how the Idris type checker evaluates types containing type
Line 639: variables by using an anonymous function (explained in chapter 2) to introduce vari-
Line 640: ables with unknown values. Consider this example:
Line 641: *ReverseVec> \k, elem => Vect (1 + k) elem
Line 642: \k => \elem => Vect (S k) elem : Nat -> Type -> Type
Line 643: Here, Idris has evaluated 1 + k in the type to S k. But if you try swapping the argu-
Line 644: ments to +, you’ll get a different result:
Line 645: *ReverseVec> \k, elem => Vect (k + 1) elem
Line 646: \k => \elem => Vect (plus k 1) elem : Nat -> Type -> Type
Line 647: Here, Idris has evaluated k + 1 to plus k 1, where plus is the Prelude function that
Line 648: implements addition on Nat. To see the reason for the difference, you need to look at
Line 649: the definition of plus. You can do this using the REPL command :printdef, which
Line 650: prints the pattern-matching definition of the function given as its argument:
Line 651: *ReverseVec> :printdef plus
Line 652: plus : Nat -> Nat -> Nat
Line 653: plus 0 right = right
Line 654: plus (S left) right = S (plus left right)
Line 655: 
Line 656: --- 페이지 248 ---
Line 657: 222
Line 658: CHAPTER 8
Line 659: Equality: expressing relationships between data
Line 660: Because plus is defined by pattern-matching on its first argument, Idris can’t evaluate
Line 661: plus k 1 any further. To do so, it would need to know what form k takes, but at the
Line 662: moment, neither of the clauses for plus matches.
Line 663:  Returning to our problem with defining myReverse, let’s take a look at the current
Line 664: state: 
Line 665: myReverse : Vect n elem -> Vect n elem
Line 666: myReverse [] = []
Line 667: myReverse (x :: xs) = myReverse xs ++ [x]
Line 668: If you rewrite the definition using let to build each component of the result, and
Line 669: leave a hole for the return value, you can see in more detail what problem you have to
Line 670: solve: 
Line 671: myReverse : Vect n elem -> Vect n elem
Line 672: myReverse [] = []
Line 673: myReverse (x :: xs) = let rev_xs = myReverse xs
Line 674: result = rev_xs ++ [x] in
Line 675: ?myReverse_rhs_2
Line 676: Checking the type of ?myReverse_rhs_2 shows the type of each component and the
Line 677: required type of the result: 
Line 678: elem : Type
Line 679: x : elem
Line 680: k : Nat
Line 681: xs : Vect k elem
Line 682: rev_xs : Vect k elem
Line 683: result : Vect (plus k 1) elem
Line 684: --------------------------------------
Line 685: myReverse_rhs_2 : Vect (S k) elem
Line 686: For the intended result, you have an expression with type Vect (k + 1) elem, but you
Line 687: need an expression with type Vect (S k) elem.
Line 688:  You know, from trying the evaluation at the REPL previously, that Vect (1 + k) elem
Line 689: would evaluate to the type you need, so you need to be able to explain to Idris that 1 + k
Line 690: is equal to k + 1; or, when evaluated, that S k is equal to plus k 1. The Idris library pro-
Line 691: vides a function that can help you: 
Line 692: plusCommutative : (left : Nat) -> (right : Nat) -> left + right = right + left
Line 693: If you check the type of plusCommutative at the REPL with values 1 and k for left and
Line 694: right, respectively, you’ll see exactly the equality you need: 
Line 695: *ReverseVec> :t \k => plusCommutative 1 k
Line 696: \k => plusCommutative 1 k : (k : Nat) -> S k = plus k 1
Line 697: You can think of this expression’s type as a “rewrite rule” that allows you to replace
Line 698: one value with another. If you can find a way to apply this rule to rewrite the expected
Line 699: type to Vect (plus k 1) a, you’ll be able to complete the definition. 
Line 700: This line has 
Line 701: a type error
Line 702: 
Line 703: --- 페이지 249 ---
Line 704: 223
Line 705: Equality in practice: types and reasoning
Line 706: 8.2.3
Line 707: The rewrite construct: rewriting a type using equality
Line 708: We’ll resume our definition of myReverse at the following point, using let to name
Line 709: the result we’d like to return: 
Line 710: myReverse : Vect n elem -> Vect n elem
Line 711: myReverse [] = []
Line 712: myReverse (x :: xs) = let result = myReverse xs ++ [x] in
Line 713: ?myReverse_rhs_2
Line 714: At this stage, these are the types: 
Line 715: elem : Type
Line 716: x : elem
Line 717: k : Nat
Line 718: xs : Vect k elem
Line 719: result : Vect (plus k 1) elem
Line 720: --------------------------------------
Line 721: myReverse_rhs_2 : Vect (S k) elem
Line 722: In order to complete the definition, you can use the information given by plus-
Line 723: Commutative 1 k to rewrite the type of ?myReverse_rhs_2. You’ll want to replace any
Line 724: S k in the type of ?myReverse_rhs_2 with plus k 1, so that you can return result. Idris
Line 725: provides a syntax for using equality proofs to rewrite types, illustrated in figure 8.1.
Line 726: You can therefore implement myReverse using the rewrite construct to update the
Line 727: type of ?myReverse_rhs_2, taking the following steps: 
Line 728: 1
Line 729: Define—Before rewriting the type using plusCommutative 1 k, you’ll need to
Line 730: bring k into scope, and k arises from pattern matching on the length of the
Line 731: input vector: 
Line 732: myReverse : Vect n elem -> Vect n elem
Line 733: myReverse [] = []
Line 734: myReverse {n = S k} (x :: xs)
Line 735: = let result = myReverse xs ++ [x] in
Line 736: ?myReverse_rhs_2
Line 737:  2
Line 738: Refine, type—Now, you can apply the rewriting rule: 
Line 739: myReverse : Vect n elem -> Vect n elem
Line 740: myReverse [] = []
Line 741: myReverse {n = S k} (x :: xs)
Line 742: rewrite plusCommutative 1 k in ?my_reverse_rhs_2
Line 743: Rewrite rule replaces S k with
Line 744: plus k 1 in this hole's type
Line 745: Rewrite rule with
Line 746: type S k = plus k 1
Line 747: Figure 8.1
Line 748: Rewriting a type 
Line 749: using an equality proof
Line 750: 
Line 751: --- 페이지 250 ---
Line 752: 224
Line 753: CHAPTER 8
Line 754: Equality: expressing relationships between data
Line 755: = let result = myReverse xs ++ [x] in
Line 756: rewrite plusCommutative 1 k in ?myReverse_rhs_2
Line 757: If you look at the resulting type for ?myReverse_rhs_2, you can see the effect
Line 758: the rewrite has had: 
Line 759: elem : Type
Line 760: k : Nat
Line 761: x : elem
Line 762: xs : Vect k elem
Line 763: result : Vect (plus k 1) elem
Line 764: _rewrite_rule : plus k 1 = S k
Line 765: --------------------------------------
Line 766: myReverse_rhs_2 : Vect (plus k 1) elem
Line 767: 3
Line 768: Refine—Finally, you can complete the definition using expression search: 
Line 769: myReverse : Vect n elem -> Vect n elem
Line 770: myReverse [] = []
Line 771: myReverse {n = S k} (x :: xs)
Line 772: = let result = myReverse xs ++ [x] in
Line 773: rewrite plusCommutative 1 k in result
Line 774: Using rewrite, you’ve replaced an expression in the type (S k) with an equivalent
Line 775: expression (plus k 1), which allows you to use result. But although this has allowed
Line 776: you to write the function, this definition still leaves something to be desired: the part
Line 777: of the definition that computes the result (myReverse xs ++ [x]) has become rather
Line 778: lost in the details of the proof. You can improve this by delegating the details of the
Line 779: proof, using a hole. 
Line 780: 8.2.4
Line 781: Delegating proofs and rewriting to holes
Line 782: Instead of applying the rewrite inside the definition of myReverse, you can use a hole
Line 783: along with interactive editing to generate a helper function that contains the details of
Line 784: the proof. Let’s start again, with our initial (failing) definition of myReverse: 
Line 785: myReverse : Vect n elem -> Vect n elem
Line 786: myReverse [] = []
Line 787: myReverse (x :: xs) = myReverse xs ++ [x]
Line 788: You can correct this definition using the following steps: 
Line 789: 1
Line 790: Refine, type—Add a hole to the right side, which takes the initial attempt as an
Line 791: argument: 
Line 792: myReverse : Vect n elem -> Vect n elem
Line 793: myReverse [] = []
Line 794: myReverse (x :: xs) = ?reverseProof (myReverse xs ++ [x])
Line 795: If you check the type of ?reverseProof, you’ll see exactly how you need to
Line 796: rewrite the type for this definition to be accepted: 
Line 797: elem : Type
Line 798: x : elem
Line 799: k : Nat
Line 800: 
Line 801: --- 페이지 251 ---
Line 802: 225
Line 803: Equality in practice: types and reasoning
Line 804: xs : Vect k elem
Line 805: --------------------------------------
Line 806: reverseProof : Vect (plus k 1) elem -> Vect (S k) elem
Line 807:  2
Line 808: Type—Using Ctrl-Alt-L in Atom, lift ?reverseProof to a top-level function: 
Line 809: reverseProof : (x : elem) -> (xs : Vect k elem) ->
Line 810: Vect (k + 1) elem -> Vect (S k) elem
Line 811: myReverse : Vect n elem -> Vect n elem
Line 812: myReverse [] = []
Line 813: myReverse (x :: xs) = reverseProof x xs (myReverse xs ++ [x])
Line 814:  3
Line 815: Define—Define reverseProof as follows, using the same application of rewrite
Line 816: as in your previous definition of myReverse: 
Line 817: reverseProof : (x : elem) -> (xs : Vect k elem) ->
Line 818: Vect (k + 1) elem -> Vect (S k) elem
Line 819: reverseProof {k} x xs result = rewrite plusCommutative 1 k in result
Line 820: 4
Line 821: Refine—Finally, because you don’t use x or xs in reverseProof, and because
Line 822: reverseProof will only be used by myReverse, you can tidy up the definition as
Line 823: follows: 
Line 824: myReverse : Vect n elem -> Vect n elem
Line 825: myReverse [] = []
Line 826: myReverse (x :: xs) = reverseProof (myReverse xs ++ [x])
Line 827: where
Line 828: reverseProof : Vect (k + 1) elem -> Vect (S k) elem
Line 829: reverseProof {k} result = rewrite plusCommutative 1 k in result
Line 830: By introducing the hole ?reverseProof, you’ve been able to keep the relevant com-
Line 831: putation part of myReverse separate from the details of the proof. 
Line 832: 8.2.5
Line 833: Appending vectors, revisited
Line 834: You can often avoid the need for rewriting in types by taking care in how you write
Line 835: function types. For example, in chapter 4, you saw how to define a function that
Line 836: appends vectors with the following type: 
Line 837: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 838: The order of arguments to the + operator in the return type turns out to be important
Line 839: because of the definition of +. If you begin to implement this (in the file AppendVec
Line 840: .idr) by creating a skeleton definition and then case splitting on the first argument,
Line 841: you’ll reach the following state: 
Line 842: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 843: append [] ys = ?append_rhs_1
Line 844: append (x :: xs) ys = ?append_rhs_2
Line 845: Then, if you check the type of ?append_rhs_1, you’ll see the following: 
Line 846: elem : Type
Line 847: m : Nat
Line 848: ys : Vect m elem
Line 849: 
Line 850: --- 페이지 252 ---
Line 851: 226
Line 852: CHAPTER 8
Line 853: Equality: expressing relationships between data
Line 854: --------------------------------------
Line 855: append_rhs_1 : Vect m elem
Line 856: In this case, the first argument, [], has type Vect 0 elem, and the second argument, ys,
Line 857: has type Vect m elem. According to the return type of append, ?append_rhs_1 should
Line 858: have type Vect (0 + m) elem, which reduces to Vect m elem by the definition of +.
Line 859:  Take a look at what happens if you swap the arguments n and m, as follows: 
Line 860: append : Vect n elem -> Vect m elem -> Vect (m + n) elem
Line 861: append [] ys = ?append_rhs_1
Line 862: append (x :: xs) ys = ?append_rhs_2
Line 863: You now see a different type for ?append_rhs_1: 
Line 864: elem : Type
Line 865: m : Nat
Line 866: ys : Vect m elem
Line 867: --------------------------------------
Line 868: append_rhs_1 : Vect (plus m 0) elem
Line 869: As in the definition of myReverse, Idris can’t reduce plus m 0 any further, because plus
Line 870: is defined by pattern-matching on its first argument, and the form of m is unknown.
Line 871: Because of this, you can’t simply return ys for this case, and you’ll need to rewrite the
Line 872: type of append_rhs_1. You’ll have a similar problem for append_rhs_2; the following
Line 873: listing shows the definition of append, with holes in place of the necessary rewrites.
Line 874: append : Vect n elem -> Vect m elem -> Vect (m + n) elem
Line 875: append [] ys = ?append_nil ys
Line 876: append (x :: xs) ys = ?append_xs (x :: append xs ys)
Line 877: The next listing shows a completed definition of append, with definitions of
Line 878: append_nil and append_xs that rewrite the types for each case.
Line 879: append_nil : Vect m elem -> Vect (plus m 0) elem
Line 880: append_nil {m} xs = rewrite plusZeroRightNeutral m in xs
Line 881: append_xs : Vect (S (m + k)) elem -> Vect (plus m (S k)) elem
Line 882: append_xs {m} {k} xs = rewrite sym
Line 883:                       (plusSuccRightSucc m k) in xs
Line 884: append : Vect n elem -> Vect m elem -> Vect (m + n) elem
Line 885: append [] ys = append_nil ys
Line 886: append (x :: xs) ys = append_xs (x :: append xs ys)
Line 887: Listing 8.6
Line 888: Implementing append on vectors with the arguments to + swapped in the
Line 889: return type (AppendVec.idr)
Line 890: Listing 8.7
Line 891: Completing append on vectors by adding rewriting proofs for append_nil
Line 892: and append_xs (AppendVec.idr)
Line 893: ?append_nil stands for a proof 
Line 894: that it’s valid to return ys here.
Line 895: ?append_xs stands 
Line 896: for a proof that it’s 
Line 897: valid to return x :: 
Line 898: append xs ys here.
Line 899: sym is a function 
Line 900: that reverses the 
Line 901: direction of 
Line 902: a rewrite.
Line 903: 
Line 904: --- 페이지 253 ---
Line 905: 227
Line 906: The empty type and decidability
Line 907: These rewrites use several definitions from the Prelude. Two of them assist with rewrit-
Line 908: ing expressions using Nat: 
Line 909: plusZeroRightNeutral : (left : Nat) -> left + 0 = left
Line 910: plusSuccRightSucc : (left : Nat) -> (right : Nat) ->
Line 911: S (left + right) = left + S right
Line 912: The third, sym, allows you to apply a rewrite rule in reverse:
Line 913: sym : left = right -> right = left
Line 914: Essentially, plusZeroRightNeutral and plusSuccRightSucc together explain that the
Line 915: behavior of plus is identical if the arguments are given in the opposite order. 
Line 916: Exercises
Line 917: 1
Line 918: Using plusZeroRightNeutral and plusSuccRightSucc, write your own version of
Line 919: plusCommutes: 
Line 920: myPlusCommutes : (n : Nat) -> (m : Nat) -> n + m = m + n
Line 921: Hint: Write this by case splitting on n. In the case of S k, you can rewrite with a recur-
Line 922: sive call to myPlusCommutes k m, and rewrites can be nested.
Line 923: 2
Line 924: The implementation of myReverse you wrote earlier is inefficient because it needs
Line 925: to traverse the entire vector to append a single element on every iteration. You can
Line 926: write a better definition as follows, using a helper function, reverse', that takes an
Line 927: accumulating argument to build the reversed list: 
Line 928: myReverse : Vect n a -> Vect n a
Line 929: myReverse xs = reverse' [] xs
Line 930: where reverse' : Vect n a -> Vect m a -> Vect (n+m) a
Line 931: reverse' acc [] = ?reverseProof_nil acc
Line 932: reverse' acc (x :: xs)
Line 933: = ?reverseProof_xs (reverse' (x::acc) xs)
Line 934: Complete this definition by implementing the holes ?reverseProof_nil and
Line 935: ?reverseProof_xs.
Line 936: You can test your answer at the REPL as follows: 
Line 937: *ex_8_2> myReverse [1,2,3,4]
Line 938: [4, 3, 2, 1] : Vect 4 Integer
Line 939: 8.3
Line 940: The empty type and decidability
Line 941: You can use the equality type, =, to write functions with types that state that two values
Line 942: are guaranteed to be equal, and then use this guarantee elsewhere in the program.
Line 943: This works because the only way to construct a value with an equality type is to use
Line 944: Refl, and Refl will only construct a value with a type of the form x = x:
Line 945: Idris> :t Refl
Line 946: Refl : x = x
Line 947: 
Line 948: --- 페이지 254 ---
Line 949: 228
Line 950: CHAPTER 8
Line 951: Equality: expressing relationships between data
Line 952: Idris> Refl {x = 94}
Line 953: Refl : 94 = 94
Line 954: But what if you want to say the opposite, that two values are guaranteed not to be
Line 955: equal? When you construct a value in a type, you’re effectively giving evidence that an
Line 956: element of that type exists. To show that two values x and y are not equal, you need to
Line 957: be able to give evidence that an element of the type x = y can’t exist.
Line 958:  In this section, you’ll see how to use the empty type, Void, to express that something
Line 959: is impossible. If a function returns a value of type Void, that can only mean that it’s
Line 960: impossible to construct values of its inputs (or, logically, that the types of its inputs
Line 961: express a contradiction.) We’ll use Void to express guarantees in types that values can’t
Line 962: be equal, and then use it to write a more precise type for checkEqNat, which guaran-
Line 963: tees that
Line 964: If its inputs are equal, it will produce a proof that they are equal
Line 965: If its inputs are not equal, it will produce a proof that they are not equal
Line 966:  First, let’s take a look at how Void is defined and used in the simplest case.
Line 967: 8.3.1
Line 968: Void: a type with no values
Line 969: In order to express that something can’t happen, the Prelude provides a type with no
Line 970: values, Void. The complete definition of Void is as follows:
Line 971: data Void : Type where
Line 972: You can’t write values of type Void directly, because there aren’t any! As a result, if you
Line 973: have a function that returns something of type Void, it must be because one of its
Line 974: arguments is also impossible to construct.
Line 975:  Just as you can use = to write functions that express facts about how functions do
Line 976: behave, you can use Void to express facts about how functions don’t behave. For exam-
Line 977: ple, you can show that 2 + 2 doesn’t equal 5.
Line 978:  Let’s write a function in a file named Void.idr:
Line 979: 1
Line 980: Type—Begin by writing the appropriate type: 
Line 981: twoPlusTwoNotFive : 2 + 2 = 5 -> Void
Line 982: You can read this “if 2 + 2 = 5, then return an element of the empty type.”
Line 983:  2
Line 984: Define—Adding a skeleton definition gives you this: 
Line 985: twoPlusTwoNotFive : 2 + 2 = 5 -> Void
Line 986: twoPlusTwoNotFive prf = ?twoPlusTwoNotFive_rhs
Line 987: If you look at the type of prf, you’ll see that it’s a proof that 4 = 5: 
Line 988: prf : 4 = 5
Line 989: --------------------------------------
Line 990: twoPlusTwoNotFive_rhs : Void
Line 991: 
Line 992: --- 페이지 255 ---
Line 993: 229
Line 994: The empty type and decidability
Line 995: 3
Line 996: Define—You can try to define the function by a case split on prf. Idris produces
Line 997: this: 
Line 998: twoPlusTwoNotFive : 2 + 2 = 5 -> Void
Line 999: twoPlusTwoNotFive Refl impossible
Line 1000: This definition is now complete. Idris has produced one case, and noticed that the only
Line 1001: possible input, Refl, can never be valid. Recall from chapter 4 that the impossible key-
Line 1002: word means that the pattern clause must not type-check.
Line 1003: Similarly, you can write a function that shows that a number can never be equal to its
Line 1004: successor:
Line 1005: valueNotSuc : (x : Nat) -> x = S x -> Void
Line 1006: valueNotSuc _ Refl impossible
Line 1007: If you were able to provide a value of the empty type, you’d be able to produce a value
Line 1008: of any type. In other words, if you have a proof that an impossible value has happened,
Line 1009: you can do anything. The Prelude provides a function, void, that expresses this:
Line 1010: void : Void -> a
Line 1011: It may seem strange, and of little practical use, to be writing functions merely to show
Line 1012: that something can’t happen. But if you know that something can’t happen, you can
Line 1013: use this knowledge to express limitations about what can happen. In other words, you
Line 1014: can express more precisely what a function is intended to do. 
Line 1015: 8.3.2
Line 1016: Decidability: checking properties with precision
Line 1017: Previously, when you wrote checkEqNat, you used Maybe for the result: 
Line 1018: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (num1 = num2)
Line 1019: Void and total functions
Line 1020: It’s important to check that a function that returns Void is a total function, if you
Line 1021: really want to believe that it takes an impossible input:
Line 1022: *Void> :total twoPlusTwoNotFive
Line 1023: Main.twoPlusTwoNotFive is Total
Line 1024: Otherwise, you could write a function that claims to return Void by looping forever: 
Line 1025: loop : Void
Line 1026: loop = loop
Line 1027: This function isn’t total, so you can’t believe that it really does produce an element
Line 1028: of Void. Idris reports the following:
Line 1029: *Void> :total loop
Line 1030: Main.loop is possibly not total due to recursive path:
Line 1031: Main.loop
Line 1032: 
Line 1033: --- 페이지 256 ---
Line 1034: 230
Line 1035: CHAPTER 8
Line 1036: Equality: expressing relationships between data
Line 1037: So, if checkEqNat returns a value of the form Just p, you can be certain that num1 and
Line 1038: num2 are equal, and that p represents a proof that they’re equal. But you can’t say the
Line 1039: opposite: that if checkEqNat returns Nothing, then num1 and num2 are guaranteed not
Line 1040: to be equal.
Line 1041:  The following definition would, for example, be perfectly valid, though not very
Line 1042: useful:
Line 1043: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Maybe (num1 = num2)
Line 1044: checkEqNat num1 num2 = Nothing
Line 1045: Instead, to make this type more precise, you’d need a way of stating that for any pair
Line 1046: of numbers, num1 and num2, you’ll always be able to produce either a proof that
Line 1047: they’re equal (of type num1 = num2) or a proof that they’re not equal (of type num1 =
Line 1048: num2 -> Void). That is, you’d like to state that checking whether num1 = num2 is a decid-
Line 1049: able property.
Line 1050: DECIDABILITY
Line 1051: A property of some values is decidable if you can always say
Line 1052: whether the property holds or not for specific values. For example, checking
Line 1053: equality on Nat is decidable, because for any two natural numbers you can
Line 1054: always decide whether they are equal or not.
Line 1055: Listing 8.8 shows the Dec generic type, which is defined in the Prelude. Like Maybe,
Line 1056: Dec has a constructor (Yes) that carries a value. Unlike Maybe, it also has a constructor
Line 1057: (No) that carries a proof that no value of its argument type can exist.
Line 1058: data Dec : (prop : Type) -> Type where
Line 1059: Yes : (prf : prop) -> Dec prop
Line 1060: No
Line 1061: : (contra : prop -> Void) -> Dec prop
Line 1062: For example, you can construct a proof that 2 + 2 = 4, so you’d use Yes: 
Line 1063: *Void> the (Dec (2 + 2 = 4)) (Yes Refl)
Line 1064: Yes Refl : Dec (4 = 4)
Line 1065: But it’s impossible to construct a proof that 2 + 2 = 5, so you’d use No and provide your
Line 1066: evidence, twoPlusTwoNotFive, that it’s impossible: 
Line 1067: *Void> the (Dec (2 + 2 = 5)) (No twoPlusTwoNotFive)
Line 1068: No twoPlusTwoNotFive : Dec (4 = 5)
Line 1069: Let’s rewrite checkEqNat using Dec instead of Maybe for the result type. In doing so,
Line 1070: we’ll have two guarantees verified by the Idris type checker: 
Line 1071: Listing 8.8
Line 1072: Dec: precisely stating that a property is decidable
Line 1073: The type Dec prop states that you can 
Line 1074: decide whether prop is either 
Line 1075: guaranteed to hold, or guaranteed to 
Line 1076: be impossible.
Line 1077: contra is a proof that the property,
Line 1078: prop, doesn’t hold, because it’s a
Line 1079: function that returns a value of the
Line 1080: empty type Void, given a prop.
Line 1081: prf is a proof 
Line 1082: that the 
Line 1083: property, 
Line 1084: prop, holds.
Line 1085: 
Line 1086: --- 페이지 257 ---
Line 1087: 231
Line 1088: The empty type and decidability
Line 1089: If the inputs num1 and num2 are equal, checkEqNat is guaranteed to produce a
Line 1090: result of the form Yes prf, where prf has type num1 = num2.
Line 1091: If the inputs num1 and num2 are not equal, checkEqNat is guaranteed to produce
Line 1092: a result of the form No contra, where contra has type num1 = num2 -> Void.
Line 1093: These are guarantees because the type of checkEqNat gives a direct link between the
Line 1094: inputs and the output type:
Line 1095: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Dec (num1 = num2)
Line 1096: You can write this function interactively, in a new file called CheckEqDec.idr:
Line 1097: 1
Line 1098: Define, refine—You can mostly follow the same steps as earlier, when you defined
Line 1099: checkEqNat using Maybe. But instead of Just, use Yes, and instead of Nothing,
Line 1100: use No. No requires proofs that the inputs are unequal, so you can leave holes
Line 1101: for these for the moment: 
Line 1102: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Dec (num1 = num2)
Line 1103: checkEqNat Z Z = Yes Refl
Line 1104: checkEqNat Z (S k) = No ?zeroNotSuc
Line 1105: checkEqNat (S k) Z = No ?sucNotZero
Line 1106: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 1107: Yes prf => Yes (cong prf)
Line 1108: No contra => No ?noRec
Line 1109: You can test this at the REPL, even without the proofs, though you may see holes
Line 1110: in the results: 
Line 1111: *CheckEqDec> checkEqNat 3 3
Line 1112: Yes Refl : Dec (3 = 3)
Line 1113: *CheckEqDec> checkEqNat 3 4
Line 1114: No ?noRec : Dec (3 = 4)
Line 1115: *CheckEqDec> checkEqNat 3 0
Line 1116: No ?sucNotZero : Dec (3 = 0)
Line 1117:  2
Line 1118: Type—If you look at the types of the holes, you’ll see what you need to prove to
Line 1119: complete the definition, as in this example: 
Line 1120: k : Nat
Line 1121: --------------------------------------
Line 1122: zeroNotSuc : (0 = S k) -> Void
Line 1123:  3
Line 1124: Define, refine—You can lift ?zeroNotSuc and ?sucNotZero to top-level defini-
Line 1125: tions with Ctrl-Alt-L and implement them using case splitting and impossible,
Line 1126: as with twoPlusTwoNotFive in the previous section, because it’s never possible
Line 1127: for zero to be equal to a nonzero number: 
Line 1128: zeroNotSuc : (0 = S k) -> Void
Line 1129: zeroNotSuc Refl impossible
Line 1130: sucNotZero : (S k = 0) -> Void
Line 1131: sucNotZero Refl impossible
Line 1132: 
Line 1133: --- 페이지 258 ---
Line 1134: 232
Line 1135: CHAPTER 8
Line 1136: Equality: expressing relationships between data
Line 1137:  4
Line 1138: Type, define—For ?noRec, you can take a look at the type to see what you need to
Line 1139: show: 
Line 1140: k : Nat
Line 1141: j : Nat
Line 1142: contra : (k = j) -> Void
Line 1143: --------------------------------------
Line 1144: noRec : (S k = S j) -> Void
Line 1145: The type of contra tells you that k is guaranteed not to be equal to j. Given
Line 1146: that, you have to show that S k can’t equal S j. Again, you can lift this to a top-
Line 1147: level definition with Ctrl-Alt-L: 
Line 1148: noRec : (contra : (k = j) -> Void) -> (S k = S j) -> Void
Line 1149: noRec contra prf = ?noRec_rhs
Line 1150:  5
Line 1151: Define—The type of noRec says that if you have a proof that k = j is impossible,
Line 1152: and a proof that S k = S j, you can produce an element of the empty type. Logi-
Line 1153: cally, the two inputs contradict each other. You can write this function by case
Line 1154: splitting on prf: 
Line 1155: noRec : (contra : (k = j) -> Void) -> (S k = S j) -> Void
Line 1156: noRec contra Refl = ?noRec_rhs_1
Line 1157:  6
Line 1158: Type—The only possible value prf can take is Refl, and the only way it can take
Line 1159: the value Refl is if S k and S j are equal, and therefore k and j are equal. Rec-
Line 1160: ognizing this, Idris refines the type of contra, as you can see by inspecting the
Line 1161: type of noRec_rhs_1: 
Line 1162: j : Nat
Line 1163: contra : (j = j) -> Void
Line 1164: --------------------------------------
Line 1165: noRec_rhs_1 : Void
Line 1166: 7
Line 1167: Refine—To complete the definition, you can use contra to produce an element
Line 1168: of the empty type; an expression search will find this: 
Line 1169: noRec : (contra : (k = j) -> Void) -> (S k = S j) -> Void
Line 1170: noRec contra Refl = contra Refl
Line 1171: The following listing shows the complete definition of checkEqNat, including the
Line 1172: helper functions zeroNotSuc, sucNotZero, and noRec.
Line 1173: zeroNotSuc : (0 = S k) -> Void
Line 1174: zeroNotSuc Refl impossible
Line 1175: sucNotZero : (S k = 0) -> Void
Line 1176: sucNotZero Refl impossible
Line 1177: noRec : (contra : (k = j) -> Void) -> (S k = S j) -> Void
Line 1178: noRec contra Refl = contra Refl
Line 1179: Listing 8.9
Line 1180: Checking whether Nats are equal, with a precise type (CheckEqDec.idr)
Line 1181: Given a proof that zero equals a nonzero 
Line 1182: number, produce a value of the empty type.
Line 1183: Given a proof that a nonzero number equals 
Line 1184: zero, produce a value of the empty type.
Line 1185: Given a proof that two numbers aren’t equal,
Line 1186: and a proof that their successors are equal,
Line 1187: produce a value of the empty type.
Line 1188: 
Line 1189: --- 페이지 259 ---
Line 1190: 233
Line 1191: The empty type and decidability
Line 1192: checkEqNat : (num1 : Nat) -> (num2 : Nat) -> Dec (num1 = num2)
Line 1193: checkEqNat Z Z = Yes Refl
Line 1194: checkEqNat Z (S k) = No zeroNotSuc
Line 1195: checkEqNat (S k) Z = No sucNotZero
Line 1196: checkEqNat (S k) (S j) = case checkEqNat k j of
Line 1197: Yes prf => Yes (cong prf)
Line 1198: No contra => No (noRec contra)
Line 1199: PROVING INPUTS ARE IMPOSSIBLE WITH VOID
Line 1200: When you run checkEqNat, you
Line 1201: aren’t really going to produce a value of the empty type using zeroNotSuc,
Line 1202: sucNotZero, or noRec. Essentially, a function that produces a value of type
Line 1203: Void can be seen as a proof that its arguments can’t all be provided at the
Line 1204: same time. In the case of noRec, the type of the functions says that if you can
Line 1205: provide both a proof that k doesn’t equal j and a proof that S k = S j, then
Line 1206: there’s a contradiction, and you can therefore have a value of type Void.
Line 1207: By using Dec, you’ve been able to write explicitly in the type what checkEqNat is sup-
Line 1208: posed to do: return either a proof that the inputs are equal or a proof that they’re not.
Line 1209: The real benefit of this comes not in checkEqNat itself, however, but in the functions
Line 1210: that use it, because they not only have the result of the equality test, but also a proof
Line 1211: that the equality test has worked correctly.
Line 1212:  Being able to guarantee that two values are equal (or different) is commonly use-
Line 1213: ful in type-driven development, because showing relationships between larger struc-
Line 1214: tures depends on showing relationships between the individual components. Because
Line 1215: of this, the Idris Prelude provides an interface, DecEq, with a generic function, decEq,
Line 1216: for deciding equality. 
Line 1217: 8.3.3
Line 1218: DecEq: an interface for decidable equality
Line 1219: Rather than providing specific functions like checkEqNat for each type, the Idris Pre-
Line 1220: lude provides an interface, DecEq. The next listing shows how DecEq is defined. There
Line 1221: are implementations for all of the types defined in the Prelude.
Line 1222: interface DecEq ty where
Line 1223: decEq : (val1 : ty) -> (val2 : ty) -> Dec (val1 = val2)
Line 1224: Instead of defining and using a special-purpose function, checkEqNat, to define exact-
Line 1225: Length, you could use decEq. The following listing shows how to do this, and it’s the
Line 1226: definition of exactLength used in Data.Vect.
Line 1227: exactLength : (len : Nat) -> (input : Vect m a) -> Maybe (Vect len a)
Line 1228: exactLength {m} len input = case decEq m len of
Line 1229: Yes Refl => Just input
Line 1230: No contra => Nothing
Line 1231: Listing 8.10
Line 1232: The DecEq interface (defined in the Prelude)
Line 1233: Listing 8.11
Line 1234: Implementing exactLength using decEq (ExactLengthDec.idr)
Line 1235: Given two values, val1 and val2, return either a proof
Line 1236: that they are equal or a proof that they are different.
Line 1237: 
Line 1238: --- 페이지 260 ---
Line 1239: 234
Line 1240: CHAPTER 8
Line 1241: Equality: expressing relationships between data
Line 1242: Using decEq rather than the Boolean equality operator, ==, gives you a strong guaran-
Line 1243: tee about how the equality test works. You can be sure that if decEq returns a value of
Line 1244: the form Yes prf, then the inputs really are structurally equal.
Line 1245:  In the next chapter, you’ll see how to describe relationships between larger data
Line 1246: structures (such as showing that a value is an element of a list) and how to use decEq
Line 1247: to build proofs of these relationships. 
Line 1248: Exercises
Line 1249: 1
Line 1250: Implement the following functions: 
Line 1251: headUnequal : DecEq a => {xs : Vect n a} -> {ys : Vect n a} ->
Line 1252: (contra : (x = y) -> Void) -> ((x :: xs) = (y :: ys)) -> Void
Line 1253: tailUnequal : DecEq a => {xs : Vect n a} -> {ys : Vect n a} ->
Line 1254: (contra : (xs = ys) -> Void) -> ((x :: xs) = (y :: ys)) -> Void
Line 1255: The first states that if the first elements of two vectors are unequal, then the vectors
Line 1256: must be unequal. The second states that if there are differences in the tails of two
Line 1257: vectors, then the vectors must be unequal.
Line 1258: If you have a correct solution, both headUnequal and tailUnequal should type-
Line 1259: check and be total: 
Line 1260: *ex_8_3> :total headUnequal
Line 1261: Main.headUnequal is Total
Line 1262: *ex_8_3> :total tailUnequal
Line 1263: Main.tailUnequal is Total
Line 1264: 2
Line 1265: Implement DecEq for Vect. Begin with the following implementation header: 
Line 1266: DecEq a => DecEq (Vect n a) where
Line 1267: Hint: You’ll find headUnequal and tailUnequal useful here. Remember to check
Line 1268: the types of the holes as you write the definition. You should also use your own defi-
Line 1269: nition of Vect rather than importing Data.Vect, because the library provides a
Line 1270: DecEq implementation.
Line 1271: You can test your answer at the REPL as follows: 
Line 1272: *ex_8_3> decEq (the (Vect _ _) [1,2,3]) [1,2,3]
Line 1273: Yes Refl : Dec ([1, 2, 3] = [1, 2, 3])
Line 1274: 8.4
Line 1275: Summary
Line 1276: You can write a type to express a proof that two values must be equal.
Line 1277: You can write functions that take equality types as inputs to prove additional
Line 1278: properties of data.
Line 1279: Using Maybe, you can test for equality of values at runtime.
Line 1280: The generic = type allows you to describe equality between values of any type.
Line 1281: Proof requirements arise naturally when programming with dependent types,
Line 1282: such as to show that lengths are preserved when reversing a vector.
Line 1283: 
Line 1284: --- 페이지 261 ---
Line 1285: 235
Line 1286: Summary
Line 1287: The rewrite construct allows you to update a type using an equality proof.
Line 1288: Using holes and interactive editing, you can delegate the details of rewriting
Line 1289: types to a separate function.
Line 1290: 
Line 1291: Void is a type with no values, used to show that inputs to a function can’t all
Line 1292: occur at once.
Line 1293: A property is decidable if you can always say whether the property holds for
Line 1294: some specific values.
Line 1295: Using Dec, you can compute at runtime whether a property is guaranteed to
Line 1296: hold or guaranteed not to hold.