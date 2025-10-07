Line 1: 
Line 2: --- 페이지 208 ---
Line 3: 182
Line 4: Interfaces: using
Line 5: constrained generic types
Line 6: In chapter 2, you saw that generic function types with type variables could be con-
Line 7: strained so that the variables stood for a more limited set of types. For example, you
Line 8: saw the following function for doubling a number in any numeric type: 
Line 9: double : Num a => a -> a
Line 10: double x = x + x
Line 11: The type of double includes a constraint, Num a, which states that a can only stand
Line 12: for numeric types. Therefore, you can use double with Int, Nat, Integer, or any
Line 13: other numeric type, but if you try to use it with a non-numeric type, such as Bool,
Line 14: Idris will report an error.
Line 15:  You’ve seen a few such constraints, such as Eq for types that support equality
Line 16: tests and Ord for types that support comparisons. You’ve also seen functions that
Line 17: This chapter covers
Line 18: Constraining generic types using interfaces
Line 19: Implementing interfaces for specific contexts
Line 20: Using interfaces defined in the Prelude
Line 21: 
Line 22: --- 페이지 209 ---
Line 23: 183
Line 24: Generic comparisons with Eq and Ord
Line 25: rely on other constraints that we haven’t discussed in detail, such as map and >>=,
Line 26: which rely on Functor and Monad, respectively. We haven’t yet discussed how these
Line 27: constraints are defined or introduced.
Line 28:  In this chapter, we’ll discuss how to define and use constrained generic types using
Line 29: interfaces. In the type declaration for double, for example, the constraint Num a is
Line 30: implemented by an interface, Num, which describes arithmetic operations that will be
Line 31: implemented in different ways for different numeric types.
Line 32: TYPE CLASSES IN HASKELL
Line 33: If you know Haskell, you’ll be familiar with Has-
Line 34: kell’s concept of type classes. Interfaces in Idris are similar to type classes in
Line 35: Haskell and are often used in the same way, though there are some differ-
Line 36: ences. The most important are, first, that interfaces in Idris can be parameter-
Line 37: ized by values of any type, and are not limited to types or type constructors,
Line 38: and, second, interfaces in Idris can have multiple implementations, though
Line 39: we won’t go into the details in this chapter.
Line 40: From the perspective of type-driven development, interfaces allow us to give the nec-
Line 41: essary level of precision to generic types. In general, an interface in Idris describes a
Line 42: collection of generic operations that can be implemented in different ways for differ-
Line 43: ent concrete types. For example:
Line 44: You could define an interface for operations that serialize and load generic
Line 45: data to and from JSON.
Line 46: A graphics library could provide an interface for operations that draw represen-
Line 47: tations of data.
Line 48: The Prelude includes a wide range of interfaces, and we’ll concentrate on these in this
Line 49: chapter. We’ll begin by looking in detail at two of the most important.
Line 50: 7.1
Line 51: Generic comparisons with Eq and Ord
Line 52: To begin, we’ll look at two interfaces that define generic comparisons, both of which
Line 53: are defined in the Prelude: 
Line 54: 
Line 55: Eq, which supports comparing values for equality or inequality.
Line 56: 
Line 57: Ord, which supports comparing values to determine which is larger.
Line 58: In doing so, you’ll learn how to declare interfaces, how to implement those interfaces
Line 59: in specific contexts, and how different interfaces can relate to each other.
Line 60: 7.1.1
Line 61: Testing for equality with Eq
Line 62: As you saw in chapter 2, Idris provides an operator for testing values for equality, ==,
Line 63: with a constrained generic type: 
Line 64: Idris> :t (==)
Line 65: (==) : Eq ty => ty -> ty -> Bool
Line 66: 
Line 67: --- 페이지 210 ---
Line 68: 184
Line 69: CHAPTER 7
Line 70: Interfaces: using constrained generic types
Line 71:  In other words, you can compare two values of some generic type ty for equality,
Line 72: returning a result as a Bool, provided that ty satisfies the Eq constraint. Similarly,
Line 73: there’s an operator for testing for inequality: 
Line 74: Idris> :t (/=)
Line 75: (/=) : Eq ty => ty -> ty -> Bool
Line 76: Any time you use either of these operators, you must know that its operands are of a
Line 77: type that can be compared for equality. Let’s say, for example, you want to write a
Line 78: function that counts the number of occurrences of a specific value, of some generic
Line 79: type ty, in a list. We’ll create a function called occurrences in a file, Eq.idr: 
Line 80: 1
Line 81: Type—As always, begin by giving a type for the function and creating a skeleton
Line 82: definition: 
Line 83: occurrences : (item : ty) -> (values : List ty) -> Nat
Line 84: occurrences item xs = ?occurrences_rhs
Line 85:  2
Line 86: Define, refine—You can define the function by case splitting on the input list, xs,
Line 87: and refining the hole generated in each case. If it’s an empty list, there can be
Line 88: no occurrences of item, so return 0: 
Line 89: occurrences : (item : ty) -> (values : List ty) -> Nat
Line 90: occurrences item [] = 0
Line 91: occurrences item (value :: values) = ?occurrences_rhs_2
Line 92:  3
Line 93: Refine—If the input is a non-empty list, try testing the value at the start of the
Line 94: list and item for equality: 
Line 95: occurrences : (item : ty) -> (values : List ty) -> Nat
Line 96: occurrences item [] = 0
Line 97: occurrences item (value :: values) = case value == item of
Line 98: case_val => ?occurrences_rhs_2
Line 99: Unfortunately, Idris reports an error: 
Line 100: Eq.idr:3:13:
Line 101: When checking right hand side of occurrences with expected type
Line 102: Nat
Line 103: Can't find implementation for Eq ty
Line 104: Specifying multiple constraints
Line 105: In the example in this section, I’ve specified exactly one constraint, Eq ty. You can
Line 106: also list multiple constraints as a comma-separated list. For example, the following
Line 107: function type specifies that ty needs to satisfy the Num and Show constraints: 
Line 108: addAndShow : (Num ty, Show ty) => ty -> ty -> String
Line 109: You’ll see more examples later, in section 7.2.2.
Line 110: 
Line 111: --- 페이지 211 ---
Line 112: 185
Line 113: Generic comparisons with Eq and Ord
Line 114: This problem is similar to the one we encountered in chapter 3 when defining
Line 115: ins_sort. In this case, value and item have type ty, but there’s no constraint
Line 116: that values of type ty are comparable for equality.
Line 117: 4
Line 118: Refine—The solution, as with ins_sort, is to refine the type by adding a constraint: 
Line 119: occurrences : Eq ty => (item : ty) -> (values : List ty) -> Nat
Line 120: The constraint Eq ty means that you can now use the == operator and complete
Line 121: the definition as follows: 
Line 122: occurrences : Eq ty => (item : ty) -> (values : List ty) -> Nat
Line 123: occurrences item [] = 0
Line 124: occurrences item (value :: values) = case value == item of
Line 125: False => occurrences item values
Line 126: True => 1 + occurrences item values
Line 127: The final type of occurrences says that it takes a ty and a List ty as inputs, provided
Line 128: that the type variable ty stands for a type that can be compared for equality.
Line 129:  This works fine for built-in types such as Char and Integer: 
Line 130: *Eq> occurrences 'b' ['a','a','b','b','b','c']
Line 131: 3 : Nat
Line 132: *Eq> occurrences 100 [50,100,100,150]
Line 133: 2 : Nat
Line 134: But what if you have user-defined types? Let’s say you have a user-defined type named
Line 135: Matter, also defined in Eq.idr: 
Line 136: data Matter = Solid | Liquid | Gas
Line 137: You’d hope to be able to count the number of occurrences of Liquid in a list. Unfor-
Line 138: tunately, if you try this, Idris reports an error: 
Line 139: *Eq> occurrences Liquid [Solid, Liquid, Liquid, Gas]
Line 140: Can't find implementation for Eq Matter
Line 141: This error message means that Idris doesn’t know how to compare values in the user-
Line 142: defined Matter type for equality. To correct this, we’ll need to take a look at how the
Line 143: Eq constraint is defined, and how to explain to Idris how user-defined types such as
Line 144: Matter can satisfy it. 
Line 145: 7.1.2
Line 146: Defining the Eq constraint using interfaces and implementations
Line 147: Constraints such as Eq are defined in Idris using interfaces. An interface definition
Line 148: contains a collection of related functions (called methods of the interface) that can be
Line 149: given different implementations for specific contexts. The Eq interface is defined in the
Line 150: Prelude, containing the methods (==) and (/=).
Line 151: 
Line 152: --- 페이지 212 ---
Line 153: 186
Line 154: CHAPTER 7
Line 155: Interfaces: using constrained generic types
Line 156:  
Line 157: interface Eq ty where
Line 158: (==) : ty -> ty -> Bool
Line 159: (/=) : ty -> ty -> Bool
Line 160: Defining an interface introduces new top-level functions
Line 161: for each method of the interface. The interface declara-
Line 162: tion in listing 7.1 introduces the top-level functions (==)
Line 163: and (/=). If you check the types of these functions,
Line 164: you’ll see the Eq ty constraint explicit in their types: 
Line 165: (==) : Eq ty => ty -> ty -> Bool
Line 166: (/=) : Eq ty => ty -> ty -> Bool
Line 167: Figure 7.1 shows the components of the interface decla-
Line 168: ration. The parameter, ty in this case, is assumed to have
Line 169: type Type by default, and stands for the generic argu-
Line 170: ment that’s to be constrained. The parameter must
Line 171: appear in each of the method declarations.
Line 172: PARAMETER NAMING CONVENTIONS
Line 173: The parameters of an interface (ty here)
Line 174: are typically generic type variables, so I typically give them short, generic,
Line 175: names. The name ty indicates that the parameter could be any type. When
Line 176: there are more parameters, or where the interface has a more specific pur-
Line 177: pose, I give more-specific names.
Line 178: An interface declaration, then, provides the types for related functions with a parame-
Line 179: ter standing for a generic argument. To define these functions for specific cases, you
Line 180: need to provide implementations.
Line 181:  To write an implementation, you give the interface and a parameter, along with
Line 182: definitions for each of the methods. The following listing shows an implementation
Line 183: for the Eq interface, which explains how the Matter type satisfies the constraint.
Line 184: Eq Matter where
Line 185: (==) Solid Solid = True
Line 186: (==) Liquid Liquid = True
Line 187: (==) Gas Gas = True
Line 188: (==) _ _ = False
Line 189: (/=) x y = not (x == y)
Line 190: Listing 7.1
Line 191: The Eq interface (defined in the Prelude)
Line 192: Listing 7.2
Line 193: Implementation of Eq for Matter (Eq.idr)
Line 194: An interface declaration introduces 
Line 195: a new interface that can be used to 
Line 196: constrain generic functions.
Line 197: Method declarations introduce 
Line 198: functions that must be defined by 
Line 199: implementations of the interface.
Line 200: An implementation declaration, here explaining how 
Line 201: to satisfy the Eq constraint for the Matter type
Line 202: Implementation of the (==) 
Line 203: method for Matter
Line 204: Implementation of the (/=) 
Line 205: method for Matter
Line 206: interface Eq ty where
Line 207: Interface name
Line 208: Interface parameter,
Line 209: of type Type
Line 210: Figure 7.1
Line 211: The Eq interface 
Line 212: declaration
Line 213: 
Line 214: --- 페이지 213 ---
Line 215: 187
Line 216: Generic comparisons with Eq and Ord
Line 217: INTERACTIVE DEVELOPMENT OF IMPLEMENTATIONS
Line 218: As you’ll see shortly, you can
Line 219: use Ctrl-Alt-A to provide a skeleton implementation of Eq Matter, as with
Line 220: function definitions.
Line 221: If you add this implementation to the file in which you defined occurrences and
Line 222: Matter, you’ll now be able to use occurrences with a List Matter: 
Line 223: *Eq> occurrences Liquid [Solid, Liquid, Liquid, Gas]
Line 224: 2 : Nat
Line 225: This provides implementations of the two methods, (==) and (/=), which are
Line 226: required to be implemented in order to be able to compare elements of type Matter
Line 227: for equality and inequality. Note that the implementation doesn’t contain any type
Line 228: declarations, because these are given in the interface declaration.
Line 229: You can build the implementation interactively in Atom as follows:
Line 230: 1
Line 231: Type—Start by giving the implementation header on its own: 
Line 232: Eq Matter where
Line 233: Interface documentation
Line 234: If you use :doc on an interface at the REPL, or Ctrl-Alt-D over an interface name in
Line 235: Atom, Idris will show documentation for the interface including its parameters, meth-
Line 236: ods, and a list of the known implementations. For example, here’s what it looks like
Line 237: for Eq:
Line 238: Idris> :doc Eq
Line 239: Interface Eq
Line 240: The Eq interface defines inequality and equality.
Line 241: Parameters:
Line 242: ty
Line 243: Methods:
Line 244: (==) : Eq ty => ty -> ty -> Bool
Line 245: infixl 5
Line 246: The function is Total
Line 247: (/=) : Eq ty => ty -> ty -> Bool
Line 248: infixl 5
Line 249: The function is Total
Line 250: Implementations:
Line 251: Eq ()
Line 252: Eq Int
Line 253: Eq Integer
Line 254: Eq Double
Line 255: [...]
Line 256: 
Line 257: --- 페이지 214 ---
Line 258: 188
Line 259: CHAPTER 7
Line 260: Interfaces: using constrained generic types
Line 261: This a Type step because it instantiates the types of (==) and (/=), with Matter
Line 262: standing for the parameter a.
Line 263:  2
Line 264: Define—You can also use the interactive editing tools in Atom to build imple-
Line 265: mentations of interfaces. With the cursor over Eq, press Ctrl-Alt-A, and Idris
Line 266: will add skeleton definitions for (==) and (/=) with generic names for the
Line 267: arguments: 
Line 268: Eq Matter where
Line 269: (==) x y = ?Eq_rhs_1
Line 270: (/=) x y = ?Eq_rhs_2
Line 271:  3
Line 272: Type—If you check the type of ?Eq_rhs_1, you’ll see confirmation that x and y
Line 273: are of type Matter: 
Line 274: x : Matter
Line 275: y : Matter
Line 276: --------------------------------------
Line 277: Eq_rhs_1 : Bool
Line 278:  4
Line 279: Define—You can begin by defining (==) by case splitting on x: 
Line 280: Eq Matter where
Line 281: (==) Solid y = ?Eq_rhs_3
Line 282: (==) Liquid y = ?Eq_rhs_4
Line 283: (==) Gas y = ?Eq_rhs_5
Line 284: (/=) x y = ?Eq_rhs_2
Line 285:  5
Line 286: Refine—Each value of type Matter is only equal to itself, so you can refine the
Line 287: definition as follows, with a catchall case to handle when the inputs aren’t
Line 288: equal: 
Line 289: Eq Matter where
Line 290: (==) Solid Solid = True
Line 291: (==) Liquid Liquid = True
Line 292: (==) Gas Gas = True
Line 293: (==) _ _ = False
Line 294: (/=) x y = ?Eq_rhs_2
Line 295: Remember that the order of cases is important, and Idris will try to match the
Line 296: clauses in order, so the catchall case must be at the end.
Line 297: 6
Line 298: Refine—To complete the implementation, you need to define (/=). The sim-
Line 299: plest definition is to use (==) and then invert the result: 
Line 300: Eq Matter where
Line 301: (==) Solid Solid = True
Line 302: (==) Liquid Liquid = True
Line 303: (==) Gas Gas = True
Line 304: (==) _ _ = False
Line 305: (/=) x y = not (x == y)
Line 306: 
Line 307: --- 페이지 215 ---
Line 308: 189
Line 309: Generic comparisons with Eq and Ord
Line 310: When you declare an interface, you introduce a collection of related new generic
Line 311: functions, known as methods, that can be overloaded for specific situations. When you
Line 312: define an implementation of the interface, you must provide definitions for all its
Line 313: methods. So, when you defined the Eq instance for Matter, you had to provide defini-
Line 314: tions for both (==) and (/=). 
Line 315: 7.1.3
Line 316: Default method definitions
Line 317: Interfaces define a collection of related methods, such as (==) and (/=). In some
Line 318: cases, methods are so closely related that you can define them in terms of other meth-
Line 319: ods in the interface. For example, you’d always expect the result of x /= y to be the
Line 320: opposite of the result of x == y, no matter what the values or even types of x and y.
Line 321:  For this situation, Idris allows you to provide a default definition for a method. If an
Line 322: implementation doesn’t provide a definition for a method that has a default defini-
Line 323: tion, Idris uses that default. For example, the Eq interface provides defaults for both
Line 324: (==) and (/=), each defined in terms of the other, as follows.
Line 325: interface Eq a where
Line 326: (==) : a -> a -> Bool
Line 327: (/=) : a -> a -> Bool
Line 328: (==) x y = not (x /= y)
Line 329: (/=) x y = not (x == y)
Line 330: You can therefore provide an implementation of Eq for Matter by providing only a
Line 331: definition of (==), and using the default method implementation for (/=):
Line 332: Eq Matter where
Line 333: (==) Solid Solid = True
Line 334: (==) Liquid Liquid = True
Line 335: (==) Gas Gas = True
Line 336: (==) _ _ = False
Line 337: The default method definitions mean that when you’re defining an implementation
Line 338: of Eq, you can provide definitions for either or both of (==) and (/=). 
Line 339: 7.1.4
Line 340: Constrained implementations
Line 341: When writing implementations for generic types, you may discover the need for addi-
Line 342: tional constraints on the parameters of the generic types. For example, to check
Line 343: whether two lists are equal, you’ll need to know how to compare the element types for
Line 344: equality.
Line 345:  In chapter 4, you saw the generic type of binary trees, defined as follows in tree.idr: 
Line 346: data Tree elem = Empty
Line 347: | Node (Tree elem) elem (Tree elem)
Line 348: Listing 7.3
Line 349: Eq interface with default method definitions
Line 350: Default method instance, used if the 
Line 351: method isn’t present in a specific 
Line 352: implementation of an interface
Line 353: 
Line 354: --- 페이지 216 ---
Line 355: 190
Line 356: CHAPTER 7
Line 357: Interfaces: using constrained generic types
Line 358: To check whether two trees are equal, you’ll also need to be able to compare the ele-
Line 359: ment types. Let’s see what happens if you try to define an implementation of Eq for
Line 360: Trees with a generic element type:
Line 361: 1
Line 362: Type—Begin by writing the implementation header, stating the interface you
Line 363: wish to implement and the type for which you’re implementing it: 
Line 364: Eq (Tree elem) where
Line 365:  2
Line 366: Define—Add a skeleton definition that gives template definitions for all the
Line 367: methods of the interface: 
Line 368: Eq (Tree elem) where
Line 369: (==) x y = ?Eq_rhs_1
Line 370: (/=) x y = ?Eq_rhs_2
Line 371: You can use the default definition for (/=), so you can delete the second
Line 372: method: 
Line 373: Eq (Tree elem) where
Line 374: (==) x y = ?Eq_rhs_1
Line 375:  3
Line 376: Define—As with the Eq implementation for Matter, you can define (==) by case
Line 377: splitting on each argument and using a catchall case for cases where the inputs
Line 378: are unequal. You know that Empty equals itself, Nodes are equal if all their argu-
Line 379: ments are equal, and everything else is not equal: 
Line 380: Eq (Tree elem) where
Line 381: (==) Empty Empty = True
Line 382: (==) (Node left e right) (Node left' e' right') = ?Eq_rhs_3
Line 383: (==) _ _ = False
Line 384: For the moment, you’ve left a hole, ?Eq_rhs_3, for the details of comparing
Line 385: Nodes.
Line 386:  4
Line 387: Refine—You’d expect to be able to complete the definition by refining the
Line 388: ?Eq_rhs_3 hole to say that you can compare each corresponding argument: 
Line 389: Eq (Tree elem) where
Line 390: (==) Empty Empty = True
Line 391: (==) (Node left e right) (Node left' e' right')
Line 392: = left == left' && e == e' && right == right'
Line 393: (==) _ _ = False
Line 394: But, unfortunately, Idris reports a problem: 
Line 395: Can't find implementation for Eq elem
Line 396: You can compare left and left' for equality, and correspondingly right and
Line 397: right', because they’re of type Tree elem, and the implementation can be
Line 398: recursive; you’re currently defining equality for Tree elem. But e and e' are of
Line 399: type elem, a generic type, and you don’t necessarily know how to compare elem
Line 400: for equality.
Line 401: 
Line 402: --- 페이지 217 ---
Line 403: 191
Line 404: Generic comparisons with Eq and Ord
Line 405: 5
Line 406: Refine—The solution is to refine the implementation declaration by constraining
Line 407: it to require that elem also has an implementation of Eq available: 
Line 408: Eq elem => Eq (Tree elem) where
Line 409: (==) Empty Empty = True
Line 410: (==) (Node left e right) (Node left' e' right')
Line 411: = left == left' && e == e' && right == right'
Line 412: (==) _ _ = False
Line 413: The constraint appears to the left of the arrow,
Line 414: =>, the same way as constraints appear in type
Line 415: declarations. Figure 7.2 shows the compo-
Line 416: nents of this interface header.
Line 417:  You can read this header as stating that
Line 418: generic trees can be compared for equal-
Line 419: ity, provided that their element type can
Line 420: also be compared for equality. You can
Line 421: introduce interface constraints like this
Line 422: anywhere you introduce a type variable, if
Line 423: you need to constrain that type variable
Line 424: further.
Line 425: LIMITATIONS ON IMPLEMENTATION PARAMETERS
Line 426: You’ve now seen implementa-
Line 427: tions of Eq parameterized by Matter and by Tree elem, both of which are of
Line 428: type Type. But you can’t parameterize implementations by everything of type
Line 429: Type. You’re limited to names introduced by either a data or record decla-
Line 430: ration, or primitive types. In particular, this means you can’t parameterize
Line 431: implementations by type synonyms or functions that compute types.
Line 432: You’ve already seen constraints on type declarations, and here you’ve seen one in an
Line 433: implementation definition. In the same way, you can place constraints on interface
Line 434: definitions themselves. 
Line 435: 7.1.5
Line 436: Constrained interfaces: defining orderings with Ord
Line 437: If you place a constraint on an interface definition, you’re effectively extending an
Line 438: existing interface. In the Prelude, for example, there’s an Ord interface, shown in the
Line 439: next listing, that extends Eq to support ordering of values.
Line 440: interface Eq ty => Ord ty where
Line 441: compare : ty -> ty -> Ordering
Line 442: (<) : ty -> ty -> Bool
Line 443: (>) : ty -> ty -> Bool
Line 444: (<=) : ty -> ty -> Bool
Line 445: (>=) : ty -> ty -> Bool
Line 446: max : ty -> ty -> ty
Line 447: min : ty -> ty -> ty
Line 448: Listing 7.4
Line 449: The Ord Interface, which extends Eq (defined in the Prelude)
Line 450: Declares the Ord interface and states 
Line 451: that an implementation of Ord ty 
Line 452: requires an implementation of Eq ty
Line 453: Ordering is defined in the 
Line 454: Prelude as either LT, EQ, or GT.
Line 455: Returns
Line 456: the larger
Line 457: of the two
Line 458: inputs
Line 459: Returns the smaller of the two inputs
Line 460: Eq elem => Eq (Tree elem) where
Line 461: Implementation
Line 462: constraint
Line 463: Implementation
Line 464: being defined
Line 465: Figure 7.2
Line 466: Constrained implementation header
Line 467: 
Line 468: --- 페이지 218 ---
Line 469: 192
Line 470: CHAPTER 7
Line 471: Interfaces: using constrained generic types
Line 472: All methods, except compare, have default definitions, some of which are written
Line 473: in terms of compare, and some of which use the (==) method provided by the Eq
Line 474: interface.
Line 475:  If you have an implementation of Ord for some data type, you can sort lists contain-
Line 476: ing that type: 
Line 477: sort : Ord ty => List ty -> List ty
Line 478: For example, you might have a data type representing a music collection, with records
Line 479: containing a title, artist, and year of release, and you may wish to sort them first by art-
Line 480: ist name, then by year of release, and then by title. The following listing gives a defini-
Line 481: tion of this data type with some examples.
Line 482: record Album where
Line 483: constructor MkAlbum
Line 484: artist : String
Line 485: title : String
Line 486: year : Integer
Line 487: help : Album
Line 488: help = MkAlbum "The Beatles" "Help" 1965
Line 489: rubbersoul : Album
Line 490: rubbersoul = MkAlbum "The Beatles" "Rubber Soul" 1965
Line 491: clouds : Album
Line 492: clouds = MkAlbum "Joni Mitchell" "Clouds" 1969
Line 493: hunkydory : Album
Line 494: hunkydory = MkAlbum "David Bowie" "Hunky Dory" 1971
Line 495: heroes : Album
Line 496: heroes = MkAlbum "David Bowie" "Heroes" 1977
Line 497: collection : List Album
Line 498: collection = [help, rubbersoul, clouds, hunkydory, heroes]
Line 499: If you try sorting the collection as it stands, Idris will report that it doesn’t know how
Line 500: to order values of type Album: 
Line 501: *Ord> sort collection
Line 502: Can't find implementation for Ord Album
Line 503: Listing 7.6 shows how you can explain to Idris how to order Albums. First, you need to
Line 504: give an Eq implementation, because the constraint on the Ord interface requires that
Line 505: implementations of Ord are also implementations of Eq. The Eq implementation
Line 506: checks that each field has the same value; the Ord implementation compares by artist
Line 507: name, and then by year, and then by title if the first two are equal.
Line 508: Listing 7.5
Line 509: A record data type and a collection to be sorted (Ord.idr)
Line 510: A record declaration (see chapter 6, section 6.3.2)
Line 511: Record fields, which give rise to the 
Line 512: artist, title and year projection functions
Line 513: 
Line 514: --- 페이지 219 ---
Line 515: 193
Line 516: Generic comparisons with Eq and Ord
Line 517:  
Line 518: Eq Album where
Line 519: (==) (MkAlbum artist title year) (MkAlbum artist' title' year')
Line 520: = artist == artist' && title == title' && year == year'
Line 521: Ord Album where
Line 522: compare (MkAlbum artist title year) (MkAlbum artist' title' year')
Line 523: = case compare artist artist' of
Line 524: EQ => case compare year year' of
Line 525: EQ => compare title title'
Line 526: diff_year => diff_year
Line 527: diff_artist => diff_artist
Line 528: Implementing Ord for Album means that you can use the usual comparison operators
Line 529: on values of type Album: 
Line 530: *Ord> heroes > clouds
Line 531: False : Bool
Line 532: *Ord> help <= rubbersoul
Line 533: True : Bool
Line 534: It also means that you can use any function with an Ord constraint, such as sort. For
Line 535: example, you can sort the collection and list the titles in sorted order: 
Line 536: *Ord> map title (sort collection)
Line 537: ["Hunky Dory", "Heroes", "Clouds", "Help", "Rubber Soul"] : List String
Line 538: Giving constraints on interfaces, like the Eq constraint on Ord, allows you to define
Line 539: hierarchies of interfaces. So, for example, if there’s an implementation of Ord for some
Line 540: type, you know it’s safe to assume that there’s also an implementation of Eq for that
Line 541: type. The Prelude defines several interfaces, some arranged into hierarchies, and we’ll
Line 542: look at some of the most important in the next section. 
Line 543: Exercises
Line 544: For these exercises, you’ll use the Shape type defined in chapter 4: 
Line 545: data Shape = Triangle Double Double
Line 546: | Rectangle Double Double
Line 547: | Circle Double
Line 548: Listing 7.6
Line 549: Implementations of Eq and Ord for Album
Line 550: The Eq implementation is necessary beca
Line 551: of the Eq constraint on the Ord interface
Line 552: Compares artists, which are 
Line 553: represented as Strings, so it uses 
Line 554: the String implementation of Ord
Line 555: If the artists are the same, 
Line 556: compares by year
Line 557: If the years are the same,
Line 558: compares by title
Line 559: The years are different, so return the
Line 560: result of comparing them directly.
Line 561: The artists are different, so return
Line 562: the result of comparing them directly.
Line 563: 
Line 564: --- 페이지 220 ---
Line 565: 194
Line 566: CHAPTER 7
Line 567: Interfaces: using constrained generic types
Line 568: 1
Line 569: Implement Eq for Shape.
Line 570: You can test your answer at the REPL as follows: 
Line 571: *ex_7_1> Circle 4 == Circle 4
Line 572: True : Bool
Line 573: *ex_7_1> Circle 4 == Circle 5
Line 574: False : Bool
Line 575: *ex_7_1> Circle 4 == Triangle 3 2
Line 576: False : Bool
Line 577: 2
Line 578: Implement Ord for Shape. Shapes should be ordered by area, so that shapes
Line 579: with a larger area are considered greater than shapes with a smaller area.
Line 580: You can test this by trying to sort the following list of Shapes: 
Line 581: testShapes : List Shape
Line 582: testShapes = [Circle 3, Triangle 3 9, Rectangle 2 6, Circle 4,
Line 583: Rectangle 2 7]
Line 584: You should see the following when sorting the list at the REPL: 
Line 585: *ex_7_1> sort testShapes
Line 586: [Rectangle 2.0 6.0,
Line 587: Triangle 3.0 9.0,
Line 588: Rectangle 2.0 7.0,
Line 589: Circle 3.0,
Line 590: Circle 4.0] : List Shape
Line 591: 7.2
Line 592: Interfaces defined in the Prelude
Line 593: The Idris Prelude provides several commonly used interfaces, in addition to Eq
Line 594: and Ord, as you’ve just seen. In this section and the next, I’ll briefly describe some of
Line 595: the most important. We’ve encountered several in passing already: Show, Num, Cast,
Line 596: Functor, and Monad. Here, you’ll see how these interfaces are defined, where they
Line 597: might be used, and some examples of how you can write implementations of them for
Line 598: your own types.
Line 599:  The parameters of an interface (in other words, the variables given in the interface
Line 600: header) can have any type. If there’s no explicit type given in the interface header for
Line 601: a parameter, it’s assumed to be of type Type. In this section, we’ll look at some inter-
Line 602: faces that are parameterized by Types.
Line 603: 7.2.1
Line 604: Converting to String with Show
Line 605: In chapter 2, you saw the show function, which converts a value to a String. This is a
Line 606: method of the Show interface, defined in the Prelude and shown in the following list-
Line 607: ing. Both the show and showPrec methods have default implementations, each
Line 608: defined in terms of the other. Here, we’ll only consider show.
Line 609: 
Line 610: --- 페이지 221 ---
Line 611: 195
Line 612: Interfaces defined in the Prelude
Line 613:  
Line 614: interface Show ty where
Line 615: show : (x : ty) -> String
Line 616: showPrec : (d : Prec) -> (x : ty) -> String
Line 617: PRECEDENCE CONTEXTS
Line 618: The purpose of showPrec is to be able to display
Line 619: complex expressions in parentheses if necessary. This might be useful if, say,
Line 620: you have a representation of arithmetic formulae, where precedence rules say
Line 621: that some subexpressions need to be parenthesized. By default, showPrec
Line 622: calls show directly, and for most display purposes this is entirely adequate. If
Line 623: you wish to investigate further, take a look at the documentation using :doc.
Line 624: The Prelude provides two functions that use show to convert a value to a String and
Line 625: then output it to the console, with or without a trailing newline character: 
Line 626: printLn : Show ty => ty -> IO ()
Line 627: print : Show ty => ty -> IO ()
Line 628: You can define a simple Show implementation for the Album type: 
Line 629: Show Album where
Line 630: show (MkAlbum artist title year)
Line 631: = title ++ " by " ++ artist ++ " (released " ++ show year ++ ")"
Line 632: Then, you can print an Album to the console using printLn. For example:
Line 633: *Ord> :exec printLn hunkydory
Line 634: Hunky Dory by David Bowie (released 1971)
Line 635: The Show interface is primarily used for debugging output, to display values of com-
Line 636: plex data types in a human-readable form. 
Line 637: 7.2.2
Line 638: Defining numeric types
Line 639: The Prelude provides a hierarchy of interfaces with methods for numeric operations.
Line 640: These interfaces divide operators into several groups: 
Line 641: The Num interface—Contains operations that work on all numeric types, includ-
Line 642: ing addition, multiplication, and conversion from integer literals
Line 643: The Neg interface—Contains operations that work on numeric types that can be
Line 644: negative, including negation, subtraction, and absolute value
Line 645: The Integral interface—Contains operations that work on integer types
Line 646: The Fractional interface—Contains operations that work on numeric types that
Line 647: can be divided into fractions
Line 648: The following listing shows how these interfaces are defined.
Line 649: Listing 7.7
Line 650: The Show interface (defined in the Prelude)
Line 651: Direct conversion of a value to a String
Line 652: ty is the parameter of the interface 
Line 653: and is a variable of type Type.
Line 654: Conversion of a 
Line 655: value to a String in a 
Line 656: precedence context
Line 657: 
Line 658: --- 페이지 222 ---
Line 659: 196
Line 660: CHAPTER 7
Line 661: Interfaces: using constrained generic types
Line 662:  
Line 663: interface Num ty where
Line 664: (+) : ty -> ty -> ty
Line 665: (*) : ty -> ty -> ty
Line 666: fromInteger : Integer -> ty
Line 667: interface Num ty => Neg ty where
Line 668: negate : ty -> ty
Line 669: (-) : ty -> ty -> ty
Line 670: abs : ty -> ty
Line 671: interface Num ty => Integral ty where
Line 672: div : ty -> ty -> ty
Line 673: mod : ty -> ty -> ty
Line 674: interface Num ty => Fractional ty where
Line 675: (/) : ty -> ty -> ty
Line 676: recip : ty -> ty
Line 677: recip x = 1 / x
Line 678: It’s useful to know which operations are available on which types. Table 7.1 summarizes
Line 679: the numeric interfaces and the implementations that exist for each in the Prelude.
Line 680: One method that’s particularly worth noting is fromInteger. All integer literals in
Line 681: Idris are implicitly converted to the appropriate numeric type using fromInteger. As a
Line 682: result, as long as there’s an implementation of Num for a numeric type, you can use
Line 683: integer literals for that type.
Line 684:  By making new implementations of Num and related interfaces, you can use standard
Line 685: arithmetic notation and integer literals for your own types. For example, listing 7.9 shows
Line 686: an Expr data type that represents arithmetic expressions, including an “absolute value”
Line 687: operation and an eval function that calculates the result of evaluating an expression.
Line 688: data Expr num = Val num
Line 689: | Add (Expr num) (Expr num)
Line 690: | Sub (Expr num) (Expr num)
Line 691: | Mul (Expr num) (Expr num)
Line 692: Listing 7.8
Line 693: The numeric interface hierarchy (defined in the Prelude)
Line 694: Table 7.1
Line 695: Summary of numeric interfaces and their implementations
Line 696: Interface
Line 697: Description
Line 698: Implementations
Line 699: Num
Line 700: All numeric types
Line 701: Integer, Int, Nat, Double
Line 702: Neg
Line 703: Numeric types that can be negative
Line 704: Integer, Int, Double
Line 705: Integral
Line 706: Integer types
Line 707: Integer, Int, Nat
Line 708: Fractional
Line 709: Numeric types that can be divided into 
Line 710: fractions
Line 711: Double
Line 712: Listing 7.9
Line 713: An arithmetic expression data type and an evaluator (Expr.idr)
Line 714: Values of all numeric types can 
Line 715: be added and multiplied.
Line 716: Converts from an integer literal 
Line 717: to the numeric type
Line 718: Numeric types that can have negative 
Line 719: values additionally support subtraction, 
Line 720: negation, and absolute value.
Line 721: Numeric types that are integers 
Line 722: additionally support integer 
Line 723: division and modulus (remainder).
Line 724: Numeric types that can be divided 
Line 725: into fractions additionally support 
Line 726: division and taking a reciprocal.
Line 727: Expressions are parameterized 
Line 728: by the type of numeric literals.
Line 729: 
Line 730: --- 페이지 223 ---
Line 731: 197
Line 732: Interfaces defined in the Prelude
Line 733: | Div (Expr num) (Expr num)
Line 734: | Abs (Expr num)
Line 735: eval : (Neg num, Integral num) => Expr num -> num
Line 736: eval (Val x) = x
Line 737: eval (Add x y) = eval x + eval y
Line 738: eval (Sub x y) = eval x - eval y
Line 739: eval (Mul x y) = eval x * eval y
Line 740: eval (Div x y) = eval x `div` eval y
Line 741: eval (Abs x) = abs (eval x)
Line 742: To construct an expression, you need to apply the constructors of Expr directly. For
Line 743: example, to represent the expression 6 + 3 * 12, and to evaluate it, you’ll need to write
Line 744: it as follows: 
Line 745: *Expr> Add (Val 6) (Mul (Val 3) (Val 12))
Line 746: Add (Val 6) (Mul (Val 3) (Val 12)) : Expr Integer
Line 747: *Expr> eval (Add (Val 6) (Mul (Val 3) (Val 12)))
Line 748: 42 : Integer
Line 749: If, on the other hand, you make a Num implementation for Expr, you’ll be able to use
Line 750: standard arithmetic notation (with +, *, and integer literals) to build values of type
Line 751: Expr. If, furthermore, you make a Neg implementation, you’ll be able to use negative
Line 752: numbers and subtraction. The following listing shows how you can do this.
Line 753: Num ty => Num (Expr ty) where
Line 754: (+) = Add
Line 755: (*) = Mul
Line 756: fromInteger = Val . fromInteger
Line 757: Neg ty => Neg (Expr ty) where
Line 758: negate x = 0 - x
Line 759: (-) = Sub
Line 760: abs = Abs
Line 761: Listing 7.10
Line 762: Implementations of Num and Neg for Expr (Expr.idr)
Line 763: You need num to be 
Line 764: negatable, because the 
Line 765: evaluator subtracts, 
Line 766: and also to support 
Line 767: integer division.
Line 768: You need the constraint Num ty 
Line 769: because you’re using the ty 
Line 770: implementation of fromInteger.
Line 771: The (.) function allows you 
Line 772: to compose functions.
Line 773: Function composition
Line 774: The (.) function gives you a concise notation for composing two functions. It has
Line 775: the following type and definition: 
Line 776: (.) : (b -> c) -> (a -> b) -> a -> c
Line 777: (.) func_bc func_ab x = func_bc (func_ab x)
Line 778: In the example in listing 7.10, you could have written this: 
Line 779: fromInteger x = Val (fromInteger x)
Line 780: The (.) function allows you instead to write this: 
Line 781: fromInteger x = (Val . fromInteger) x
Line 782: 
Line 783: --- 페이지 224 ---
Line 784: 198
Line 785: CHAPTER 7
Line 786: Interfaces: using constrained generic types
Line 787: To construct an expression and evaluate it, you can use standard notation:
Line 788: *Expr> the (Expr _) (6 + 3 * 12)
Line 789: Add (Val 6) (Mul (Val 3) (Val 12)) : Expr Integer
Line 790: *Expr> eval (6 + 3 * 12)
Line 791: 42 : Integer
Line 792: In the first case, you need to use the to make it clear that the numeric expression should
Line 793: be interpreted as an Expr, rather than the default, which would be an Integer. In the
Line 794: second case, Idris infers from the type of eval that the argument must be an Expr. 
Line 795: 7.2.3
Line 796: Converting between types with Cast
Line 797: In chapter 2, you saw the cast function, which is used to convert values between dif-
Line 798: ferent, compatible types. If you look at the type of cast, you’ll see that it has a con-
Line 799: strained generic type that uses a Cast interface: 
Line 800: Idris> :t cast
Line 801: cast : Cast from to => from -> to
Line 802: Unlike the interfaces we’ve seen so far, Cast has two parameters rather than one. The
Line 803: next listing gives its definition. Interfaces in Idris can have any number of parameters
Line 804: (even zero!).
Line 805: interface Cast from to where
Line 806: cast : (orig : from) -> to
Line 807: As we observed in chapter 2, conversions using cast may be lossy. Idris defines casts
Line 808: between Double and Integer, for example, which may lose precision. The purpose of
Line 809: cast is to provide a convenient generic function, with an easy-to-remember name, for
Line 810: conversions.
Line 811:  To define an implementation of an interface with more than one parameter, you
Line 812: need to give both concrete parameters. For example, you could define a cast from
Line 813: Maybe elem to List elem, because you can think of Maybe elem as being a list of either
Line 814: zero or one elems:
Line 815: Cast (Maybe elem) (List elem) where
Line 816: cast Nothing = []
Line 817: cast (Just x) = [x]
Line 818: Listing 7.11
Line 819: The Cast interface (defined in the Prelude)
Line 820: (continued)
Line 821: Finally, rather than have the x as an argument on both sides, you can use partial
Line 822: application: 
Line 823: fromInteger = Val . fromInteger
Line 824: Cast has two parameters, from and to, 
Line 825: both of which are of type Type.
Line 826: 
Line 827: --- 페이지 225 ---
Line 828: 199
Line 829: Interfaces parameterized by Type -> Type
Line 830: You could also define a cast in the other direction, from List elem to Maybe elem, but
Line 831: this would potentially lose information, because you’d need to decide which element
Line 832: to take if the list had more than one element. 
Line 833: Exercises
Line 834: 1
Line 835: Implement Show for the Expr type defined in section 7.2.2.
Line 836: Hint: To keep this simple and avoid concerns about precedence, assume all sub-
Line 837: expressions can be written in parentheses.
Line 838: You can test your answer at the REPL as follows: 
Line 839: *ex_7_2> show (the (Expr _) (6 + 3 * 12))
Line 840: "(6 + (3 * 12))" : String
Line 841: *ex_7_2> show (the (Expr _) (6 * 3 + 12))
Line 842: "((6 * 3) + 12)" : String
Line 843:  2
Line 844: Implement Eq for the Expr type. Expressions should be considered equal if their
Line 845: evaluation is equal. So, for example, you should see the following: 
Line 846: *Expr> the (Expr _) (2 + 4) == 3 + 3
Line 847: True : Bool
Line 848: *Expr> the (Expr _) (2 + 4) == 3 + 4
Line 849: False : Bool
Line 850: Hint: Start with the implementation header Eq (Expr ty) where, and add constraints
Line 851: as you discover you need them.
Line 852: 3
Line 853: Implement Cast to allow conversions from Expr num to any appropriately con-
Line 854: strained type num.
Line 855: Hint: You’ll need to evaluate the expression, which should tell you how num needs
Line 856: to be constrained.
Line 857: You can test your answer at the REPL as follows: 
Line 858: *ex_7_2> let x : Expr Integer = 6 * 3 + 12 in the Integer (cast x)
Line 859: 30 : Integer
Line 860: 7.3
Line 861: Interfaces parameterized by Type -> Type
Line 862: In all the interfaces we’ve seen so far, the parameters have been Types. There is, how-
Line 863: ever, no restriction on what the types of the parameters can be. In particular, it’s com-
Line 864: mon for interfaces to have parameters of Type -> Type. For example, you’ve already
Line 865: seen the following functions with constrained types: 
Line 866: map : Functor f => (a -> b) -> f a -> f b
Line 867: pure : Applicative f => a -> f a
Line 868: (>>=) : Monad m => m a -> (a -> m b) -> m b
Line 869: In each case, the parameter f or m stands for a parameterized type, such as List or IO.
Line 870: You’ve seen map in the context of List, and pure and (>>=) in the context of IO.
Line 871: 
Line 872: --- 페이지 226 ---
Line 873: 200
Line 874: CHAPTER 7
Line 875: Interfaces: using constrained generic types
Line 876:  In this section, we’ll look at how these and other operations are defined generi-
Line 877: cally in the Prelude using interfaces, along with some examples of how to apply them
Line 878: to your own types.
Line 879: 7.3.1
Line 880: Applying a function across a structure with Functor
Line 881: In chapter 2 you saw the map function, which applies a function to every element in a
Line 882: list: 
Line 883: Idris> map (*2) [1,2,3,4]
Line 884: [2, 4, 6, 8] : List Integer
Line 885: I noted, however, that map isn’t limited to lists, but rather has a constrained generic
Line 886: type using the Functor interface. Functors allow you to apply a function uniformly
Line 887: across a generic type. The preceding example applied the “multiply by two” function
Line 888: uniformly across a list of Integers.
Line 889:  The following listing shows the definition of the Functor interface, which contains
Line 890: map as its only method, and its implementation for List, as defined in the Prelude.
Line 891: interface Functor (f : Type -> Type) where
Line 892: map : (func : a -> b) -> f a -> f b
Line 893: Functor List where
Line 894: map func []
Line 895: = []
Line 896: map func (x::xs) = func x :: map func xs
Line 897: So far, the interfaces we’ve seen have been parameterized by a variable with type
Line 898: Type. But the parameter of Functor is itself a parameterized type (such as List).
Line 899: When the parameter has any type other than Type, you need to give the parameter’s
Line 900: type explicitly.
Line 901:  It’s often useful to provide an implementation of Functor for collection data struc-
Line 902: tures. For example, the following listing shows how to define a Functor implementa-
Line 903: tion for binary trees, uniformly applying a function across every element that appears
Line 904: at a Node.
Line 905: data Tree elem = Empty
Line 906: | Node (Tree elem) elem (Tree elem)
Line 907: Functor Tree where
Line 908: map func Empty = Empty
Line 909: map func (Node left e right)
Line 910: = Node (map func left)
Line 911: (func e)
Line 912: (map func right)
Line 913: Listing 7.12 The Functor interface and an implementation for List 
Line 914: (defined in the Prelude)
Line 915: Listing 7.13
Line 916: Implementation of Functor for Tree (Tree.idr)
Line 917: Gives the type of f explicitly, 
Line 918: because it’s not Type
Line 919: Applies func uniformly 
Line 920: across the left subtree
Line 921: Applies func to the element at the Node
Line 922: Applies func uniformly across 
Line 923: the right subtree
Line 924: 
Line 925: --- 페이지 227 ---
Line 926: 201
Line 927: Interfaces parameterized by Type -> Type
Line 928: The Prelude provides Functor implementations for all types with a single type param-
Line 929: eter, where possible, including List, Maybe, and IO. If you import Data.Vect, there’s
Line 930: also a Functor implementation for Vect n, as follows.
Line 931: Functor (Vect n) where
Line 932: map func []
Line 933:   = []
Line 934: map func (x :: xs) = func x :: map func xs
Line 935: The parameter in the implementation’s header, Vect n, means that you’re defining an
Line 936: implementation of Functor for vectors of any length. The usual rules for implicit
Line 937: arguments apply, as described in chapter 3: any name beginning with a lowercase let-
Line 938: ter in a function argument position is treated as an implicit argument. Therefore, n is
Line 939: treated as an implicit argument here. 
Line 940: 7.3.2
Line 941: Reducing a structure using Foldable
Line 942: If you write down a list of numbers in the form 1 :: 2 :: 3 :: 4 :: [], you can compute
Line 943: the sum of the numbers by applying the following rules:
Line 944: 1
Line 945: Replace each :: with a + (giving 1 + 2 + 3 + 4 + []).
Line 946:  2
Line 947: Replace the [] with a 0 (giving 1 + 2 + 3 + 4 + 0).
Line 948: 3
Line 949: Calculate the value of the resulting expression (giving 10).
Line 950:  Or you can compute the product of the numbers by applying the following rules:
Line 951: 1
Line 952: Replace each :: with a * (giving 1 * 2 * 3 * 4 * []).
Line 953:  2
Line 954: Replace the [] with a 1 (giving 1 * 2 * 3 * 4 * 1).
Line 955: 3
Line 956: Calculate the value of the resulting expression (giving 24).
Line 957: In general, we’re reducing the contents of the list to a single value by replacing the []
Line 958: with a default, or initial, value, and replacing :: with a function of two arguments,
Line 959: which combines each value with the result of reducing the rest of the list. Idris pro-
Line 960: vides two higher-order functions, called folds to suggest folding the structure into a sin-
Line 961: gle value, to do exactly this:
Line 962: foldr : (elem -> acc -> acc) -> acc -> List elem -> acc
Line 963: foldl : (acc -> elem -> acc) -> acc -> List elem -> acc
Line 964: The distinction between foldr and foldl is in how the resulting expression is bracketed.
Line 965: In our first example, foldr would calculate the result as 1 + (2 + (3 + (4 + 0))), whereas
Line 966: foldl would calculate the result as (((0 + 1) + 2) + 3) + 4. In other words, foldr pro-
Line 967: cesses the elements left to right, and foldl processes the elements right to left.
Line 968: TYPE VARIABLES IN FOLDL AND FOLDR
Line 969: The names of the variables in the types
Line 970: of foldl and foldr suggest their purpose: elem is the element type of the
Line 971: list and acc is the type of the result. The name acc suggests the type of an
Line 972: accumulating parameter, in which the eventual result is computed.
Line 973: Listing 7.14
Line 974: Implementation of Functor for vectors (defined in Data.Vect)
Line 975: The n here is an implicit argument and 
Line 976: means that this implementation works 
Line 977: for vectors of any length.
Line 978: 
Line 979: --- 페이지 228 ---
Line 980: 202
Line 981: CHAPTER 7
Line 982: Interfaces: using constrained generic types
Line 983: In each case, the first argument is the function (or operator) to apply, and the second
Line 984: argument is the initial value. So, you can calculate the two previous examples as follows:
Line 985: Idris> foldr (+) 0 [1,2,3,4]
Line 986: 10 : Integer
Line 987: Idris> foldr (*) 1 [1,2,3,4]
Line 988: 24 : Integer
Line 989: Or you could use a fold to calculate the total length of the Strings in a List String.
Line 990: For example, the total length of ["One", "Two", "Three"] should be 11.
Line 991:  Let’s write this interactively, using foldr, in a file named Fold.idr:
Line 992: 1
Line 993: Type, define—You can begin with a type and a candidate definition, and apply
Line 994: foldr to the input list, xs, but leave holes for the function and initial value so
Line 995: their types can give you hints as to how to proceed: 
Line 996: totalLen : List String -> Nat
Line 997: totalLen xs = foldr ?sumLength ?initial xs
Line 998:  2
Line 999: Type, refine—The type of ?initial tells you that the initial value must be a Nat: 
Line 1000: xs : List String
Line 1001: t : Type -> Type
Line 1002: elem : Type
Line 1003: --------------------------------------
Line 1004: initial : Nat
Line 1005: You can initialize it with 0, because the total length of an empty list of strings is 0:
Line 1006: totalLen : List String -> Nat
Line 1007: totalLen xs = foldr ?sumLength 0 xs
Line 1008: 3
Line 1009: Type, refine—The type and context of ?sumLength tells you that you need to pro-
Line 1010: vide a function: 
Line 1011: xs : List String
Line 1012: t : Type -> Type
Line 1013: elem : Type
Line 1014: --------------------------------------
Line 1015: sumLength : String -> Nat -> Nat
Line 1016: The function you need to provide takes a String (standing for the string at a
Line 1017: given position in the list) and a Nat (standing for the result of folding the rest
Line 1018: of the list), and returns a Nat (standing for the total length). You can complete
Line 1019: the definition as follows: 
Line 1020: totalLen : List String -> Nat
Line 1021: totalLen xs = foldr (\str, len => length str + len) 0 xs
Line 1022: You can test the resulting function at the REPL: 
Line 1023: *Fold> totalLen ["One", "Two", "Three"]
Line 1024: 11 : Nat
Line 1025: 
Line 1026: --- 페이지 229 ---
Line 1027: 203
Line 1028: Interfaces parameterized by Type -> Type
Line 1029: In the preceding example, I gave a type for foldr that was specific to List. But if you look
Line 1030: at the type at the REPL, you’ll see a constrained generic type using a Foldable interface: 
Line 1031: foldr : Foldable t => (elem -> acc -> acc) -> acc -> t elem -> acc
Line 1032: An implementation of Foldable for a structure explains how to reduce that structure
Line 1033: to a single value using an initial value and a function to combine each element with
Line 1034: an overall folded structure. The following listing gives the interface definition.
Line 1035: There’s a default definition for foldl, written in terms of foldr, so only foldr need
Line 1036: be implemented.
Line 1037: interface Foldable (t : Type -> Type) where
Line 1038: foldr : (elem -> acc -> acc) -> acc -> t elem -> acc
Line 1039: foldl : (acc -> elem -> acc) -> acc -> t elem -> acc
Line 1040: The next listing shows how Foldable is implemented in the Prelude for List. Note in
Line 1041: particular the distinction between the implementations of foldr and foldl.
Line 1042: Foldable List where
Line 1043: foldr func acc [] = acc
Line 1044: foldr func acc (x :: xs) = func x (foldr func acc xs)
Line 1045: foldl func acc [] = acc
Line 1046: foldl func acc (x :: xs) = foldl func (func acc x) xs
Line 1047: Because our Tree data type is a generic type containing a collection of values, you
Line 1048: should be able to provide a Foldable implementation:
Line 1049: 1
Line 1050: Type—Begin by providing an implementation header and a skeleton definition
Line 1051: of foldr. You can use the default definition for foldl: 
Line 1052: Foldable Tree where
Line 1053: foldr func acc tree = ?Foldable_rhs_1
Line 1054:  2
Line 1055: Define, refine—Case-split on the tree. If the tree is Empty, you return the initial
Line 1056: value: 
Line 1057: Foldable Tree where
Line 1058: foldr func acc Empty = acc
Line 1059: foldr func acc (Node left e right) = ?Foldable_rhs_3
Line 1060: 3
Line 1061: Refine—In the Node case, because foldr works left to right, you begin by folding
Line 1062: the left subtree recursively. Figure 7.3 illustrates this with an example, assuming
Line 1063: an initial accumulator of 0.
Line 1064: Listing 7.15
Line 1065: The Foldable interface (defined in the Prelude)
Line 1066: Listing 7.16
Line 1067: Implementation of Foldable for List (defined in the Prelude)
Line 1068: Folds a structure, working 
Line 1069: from left to right
Line 1070: Folds a structure, working from right
Line 1071: to left. Implementing foldl is optional.
Line 1072: Applies the function to the 
Line 1073: first element and the result 
Line 1074: of folding the tail of the list
Line 1075: Recursively folds the tail, 
Line 1076: updating the initial value 
Line 1077: by applying the function 
Line 1078: to it and the first element
Line 1079: 
Line 1080: --- 페이지 230 ---
Line 1081: 204
Line 1082: CHAPTER 7
Line 1083: Interfaces: using constrained generic types
Line 1084: In code, it looks like this: 
Line 1085: Foldable Tree where
Line 1086: foldr func acc Empty = acc
Line 1087: foldr func acc (Node left e right)
Line 1088: = let leftfold = foldr func acc left in
Line 1089: ?Foldable_rhs_3
Line 1090:  4
Line 1091: Refine—Next, take the result of folding the left subtree (leftfold) and use it as
Line 1092: the initial value when folding the right subtree. Figure 7.4 illustrates this on the
Line 1093: same example.
Line 1094: In code, it looks like this: 
Line 1095: Foldable Tree where
Line 1096: foldr func acc Empty = acc
Line 1097: foldr func acc (Node left e right)
Line 1098: = let leftfold = foldr func acc left
Line 1099: rightfold = foldr func leftfold right in
Line 1100: ?Foldable_rhs_3
Line 1101: 5
Line 1102: Refine—Finally, apply func to the value at the node e and the result of folding
Line 1103: the right subtree: 
Line 1104: Foldable Tree where
Line 1105: foldr func acc Empty = acc
Line 1106: foldr func acc (Node left e right)
Line 1107: = let leftfold = foldr func acc left
Line 1108: rightfold = foldr func leftfold right in
Line 1109: func e rightfold
Line 1110: In the example, this gives you the result 4 + 24 = 28.
Line 1111: 2
Line 1112: 1
Line 1113: 3
Line 1114: 6
Line 1115: 5
Line 1116: 7
Line 1117: 4
Line 1118: 6
Line 1119: 6
Line 1120: 5
Line 1121: 7
Line 1122: 4
Line 1123: Figure 7.3
Line 1124: Fold the left 
Line 1125: subtree with the initial 
Line 1126: accumulator. This gives you 0 
Line 1127: + 1 + 2 + 3 = 6.
Line 1128: 6
Line 1129: 5
Line 1130: 7
Line 1131: 4
Line 1132: 24
Line 1133: 4
Line 1134: 6
Line 1135: 6
Line 1136: 5
Line 1137: 7
Line 1138: 4
Line 1139: Figure 7.4
Line 1140: Fold the right 
Line 1141: subtree, initialized with the result 
Line 1142: of folding the left subtree. This 
Line 1143: gives you 6 + 5 + 6 + 7 = 24.
Line 1144: 
Line 1145: --- 페이지 231 ---
Line 1146: 205
Line 1147: Interfaces parameterized by Type -> Type
Line 1148: 7.3.3
Line 1149: Generic do notation using Monad and Applicative
Line 1150: There are two other interfaces that are useful to know about, and which you’ve
Line 1151: already seen in practice: Monad and Applicative. In most cases, you’re unlikely to
Line 1152: need to provide your own implementations, but they do appear throughout the Pre-
Line 1153: lude and base libraries, so it’s useful to know their capabilities, and particularly which
Line 1154: functions they provide.
Line 1155:  In chapter 5, you saw how the (>>=) function was used to sequence IO operations: 
Line 1156: (>>=) : IO a -> (a -> IO b) -> IO b
Line 1157: Then, in chapter 6, you saw how the (>>=) function was used to sequence Maybe com-
Line 1158: putations, abandoning the sequence if any computation returned Nothing: 
Line 1159: (>>=) : Maybe a -> (a -> Maybe b) -> Maybe b
Line 1160: Given that these two functions have similar types (directly replacing IO with Maybe)
Line 1161: and similar purposes (sequencing either interactive actions or computations that
Line 1162: might fail), you might expect them to be defined in a common interface. The follow-
Line 1163: ing listing shows the Monad interface that provides (>>=), along with a join method
Line 1164: that combines nested monadic structures.1
Line 1165: interface Applicative m => Monad (m : Type -> Type) where
Line 1166: (>>=) : m a -> (a -> m b) -> m b
Line 1167: join : m (m a) -> m a
Line 1168: Both (>>=) and join have default definitions, so you can define a Monad implementa-
Line 1169: tion in terms of either. Here, we’ll concentrate on (>>=).
Line 1170:  In chapter 6, you saw a definition of (>>=) for Maybe. In practice, it’s defined in the
Line 1171: Prelude as follows:
Line 1172: Monad Maybe where
Line 1173: (>>=) Nothing
Line 1174: next = Nothing
Line 1175: (>>=) (Just x) next = next x
Line 1176: You’ve also seen the pure function, particularly in the context of IO programs to pro-
Line 1177: duce a value in an IO computation without describing any actions: 
Line 1178: pure : a -> IO a
Line 1179: As with (>>=), pure also works in the context of Maybe, applying Just to its argument: 
Line 1180: Idris> the (Maybe _) (pure "driven snow")
Line 1181: Just "driven snow" : Maybe String
Line 1182: Listing 7.17
Line 1183: The Monad interface (defined in the Prelude)
Line 1184: 1 We won’t go into detail on join here, but it allows you to define a Monad implementation for List by con-
Line 1185: catenating lists of lists, among other things.
Line 1186: The Applicative interface supports function
Line 1187: application inside a generic type.
Line 1188: 
Line 1189: --- 페이지 232 ---
Line 1190: 206
Line 1191: CHAPTER 7
Line 1192: Interfaces: using constrained generic types
Line 1193: Again, given that pure works in several contexts, you might expect it to be defined in
Line 1194: an interface. The following listing shows the definition of the Applicative interface,
Line 1195: which provides pure and a (<*>) function that applies a function inside a structure.
Line 1196: You’ll see an example of Applicative in chapter 12.
Line 1197: interface Functor f => Applicative (f : Type -> Type) where
Line 1198: pure
Line 1199: : a -> f a
Line 1200: (<*>) : f (a -> b) -> f a -> f b
Line 1201: There are several practical uses of Monad and Applicative, although as a user of a
Line 1202: library, you’ll usually just need to know whether there are Monad and Applicative
Line 1203: instances for the provided types, and particularly what the effect of the (>>=) operator is.
Line 1204:  One interesting implementation of Monad in the Prelude is for List. The (>>=)
Line 1205: function for List passes every value in the input list to the next function in sequence,
Line 1206: and combines the results into a new list. I won’t go into this in detail in this book, but
Line 1207: you can use it to write nondeterministic programs.
Line 1208:  There’s much more to be said on the subject of interfaces, particularly the hierar-
Line 1209: chy we’ve looked at briefly in this section covering Functor, Foldable, Applicative,
Line 1210: and Monad. A deep discussion is beyond the scope of this book, but the interfaces
Line 1211: we’ve discussed in this chapter are the ones you’ll encounter most often at first. 
Line 1212: Exercises
Line 1213: 1
Line 1214: Implement Functor for Expr (defined in section 7.2.2).
Line 1215: You can test your answer at the REPL as follows: 
Line 1216: *Expr> map (*2) (the (Expr _) (1 + 2 * 3))
Line 1217: Add (Val 2) (Mul (Val 4) (Val 6)) : Expr Integer
Line 1218: *Expr> map show (the (Expr _) (1 + 2 * 3))
Line 1219: Add (Val "1") (Mul (Val "2") (Val "3")) : Expr String
Line 1220: 2
Line 1221: Implement Eq and Foldable for Vect.
Line 1222: Hint: If you import Data.Vect, these implementations already exist, so you’ll
Line 1223: need to define Vect by hand to try this exercise.
Line 1224: You can test your answers at the REPL as follows: 
Line 1225: *ex_7_3> foldr (+) 0 (the (Vect _ _) [1,2,3,4,5])
Line 1226: 15 : Integer
Line 1227: *ex_7_3> the (Vect _ _) [1,2,3,4] == [1,2,3,4]
Line 1228: True : Bool
Line 1229: *ex_7_3> the (Vect _ _) [1,2,3,4] == [5,6,7,8]
Line 1230: False : Bool
Line 1231: Listing 7.18
Line 1232: The Applicative interface (defined in the Prelude)
Line 1233: 
Line 1234: --- 페이지 233 ---
Line 1235: 207
Line 1236: Summary
Line 1237: 7.4
Line 1238: Summary
Line 1239: Generic types can be constrained using interfaces, which describe groups of
Line 1240: functions that can be applied in a specific context.
Line 1241: The Eq interface provides functions for comparing values for equality and
Line 1242: inequality.
Line 1243: The Ord interface provides functions for comparing two values to see which is
Line 1244: smaller or larger.
Line 1245: Implementations of interfaces describe how interfaces can be evaluated in spe-
Line 1246: cific contexts.
Line 1247: Interfaces and implementations can themselves have constraints. Constraints
Line 1248: say which interfaces must be implemented for a definition to be valid.
Line 1249: The Prelude provides several standard interfaces, including Show for converting
Line 1250: values to a String, Num for arithmetic operations and numeric literals, and Cast
Line 1251: for converting between types.
Line 1252: Interfaces can be parameterized by values of any type. Several in the Prelude
Line 1253: are parameterized by values of type Type -> Type.
Line 1254: An implementation of Functor for a structure allows a uniform action to be
Line 1255: applied to each element in the structure.
Line 1256: An implementation of Foldable allows a structure to be reduced to a single
Line 1257: value.
Line 1258: An implementation of Monad allows you to use do notation to sequence compu-
Line 1259: tations on a structure. 