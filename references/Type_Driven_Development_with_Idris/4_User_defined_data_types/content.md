Line 1: 
Line 2: --- 페이지 113 ---
Line 3: 87
Line 4: User-defined data types
Line 5: Type-driven development involves not only giving precise types to functions, as
Line 6: you’ve seen so far, but also thinking about exactly how data is structured. In a sense,
Line 7: programming (pure functional programming, in particular) is about transforming
Line 8: data from one form to another. Types allow us to describe the form of that data,
Line 9: and the more precise we make these descriptions, the more guidance the language
Line 10: can give in implementing transformations on that data.
Line 11:  Several useful data types are distributed as part of the Idris libraries, many of
Line 12: which we’ve used so far, such as List, Bool, and Vect. Other than being defined
Line 13: directly in Idris, there’s nothing special about these data types. In any realistic pro-
Line 14: gram, you’ll need to define your own data types to capture the specific require-
Line 15: ments of the problem you’re solving and the specific forms of data you’re working
Line 16: with. Not only that, but there’s a significant payoff to thinking carefully about the
Line 17: design of data types: the more precisely types capture the requirements of a prob-
Line 18: lem, the more benefit you’ll get from interactive type-directed editing.
Line 19: This chapter covers
Line 20: Defining your own data types
Line 21: Understanding different forms of data types
Line 22: Writing larger interactive programs in the type-
Line 23: driven style
Line 24: 
Line 25: --- 페이지 114 ---
Line 26: 88
Line 27: CHAPTER 4
Line 28: User-defined data types
Line 29:  In this chapter, therefore, we’ll look at how to define new data types. You’ll see the
Line 30: various forms of data types in a number of small example functions. We’ll also start to
Line 31: work on a larger example, an interactive data store, that we’ll extend in the coming
Line 32: chapters. At first, we’ll store only strings, accessing them by an integer index, but even
Line 33: in this small example you’ll see how user-defined types and dependent types can help
Line 34: build an interactive interface, dealing safely with possible runtime errors.
Line 35: 4.1
Line 36: Defining data types
Line 37: Data types are defined by a type constructor and one or more data constructors. In fact,
Line 38: you’ve already seen these when you used :doc to see the details of a data type. For
Line 39: example, the following listing shows the output of :doc List, annotated to highlight
Line 40: the type and data constructors.
Line 41: Data type Prelude.List.List : (elem : Type) -> Type
Line 42: Generic lists
Line 43: Constructors:
Line 44: Nil : List elem
Line 45: Empty list
Line 46: (::) : elem -> List elem -> List elem
Line 47: A non-empty list, consisting of a head element and the rest of
Line 48: the list.
Line 49: Using data constructors is the canonical way of building the types given by the type
Line 50: constructor. In the case of List, this means that every value with a type of the form
Line 51: List elem is either Nil or takes the form x :: xs for some element x and the remain-
Line 52: der of the list, xs.
Line 53:  We’ll classify types into five basic groups, although they’re all defined with the
Line 54: same syntax: 
Line 55: Enumerated types—Types defined by giving the possible values directly
Line 56: Union types—Enumerated types that carry additional data with each value
Line 57: Recursive types—Union types that are defined in terms of themselves
Line 58: Generic types—Types that are parameterized over some other types
Line 59: Dependent types—Types that are computed from some other value
Line 60:  In this section, you’ll see how to define enumerated types, union types, recursive
Line 61: types, and generic types; we’ll discuss dependent types in the next section. If you’ve
Line 62: programmed in a functional language before, or in any language that allows you to
Line 63: define generic types, the types we discuss in this section should be familiar, even if the
Line 64: notation is new.
Line 65: Listing 4.1
Line 66: Type and data constructors from :doc
Line 67: The type constructor for 
Line 68: List has a function type, 
Line 69: which takes a Type as an 
Line 70: input and returns a Type.
Line 71: The data constructor (::) takes two
Line 72: arguments and returns a list.
Line 73: The data constructor Nil takes no 
Line 74: arguments and returns an empty list.
Line 75: 
Line 76: --- 페이지 115 ---
Line 77: 89
Line 78: Defining data types
Line 79: NAMING CONVENTIONS
Line 80: By convention, I’ll use an initial capital letter for both
Line 81: type constructors and data constructors, and an initial lowercase letter for
Line 82: functions. There’s no requirement to do so, but it gives a useful visual indica-
Line 83: tion to the reader of the code.
Line 84: 4.1.1
Line 85: Enumerations
Line 86: An enumerated type is directly defined by giving the valid values for that type. The sim-
Line 87: plest example is Bool, which is defined as follows in the Prelude: 
Line 88: data Bool = False | True
Line 89: To define an enumerated data type, you give the data keyword to introduce the decla-
Line 90: ration, and then give the name of the type constructor (in this case, Bool) and list the
Line 91: names of the data constructors (in this case True and False).
Line 92:  Figure 4.1 shows another example, defining an enumerated type for representing
Line 93: the four cardinal points on a compass.
Line 94: Data constructor names are separated by a vertical bar, |, and there’s no restriction
Line 95: on how the declaration is laid out (other than the usual layout rule that all declara-
Line 96: tions begin in precisely the same column). For example, they could each be on a dif-
Line 97: ferent line: 
Line 98: data Direction = North
Line 99: | East
Line 100: | South
Line 101: | West
Line 102: Once you’ve defined a data type, you can use it to define functions interactively. For
Line 103: example, you could define a turnClockwise function as follows, with the usual pro-
Line 104: cess of type, define, refine: 
Line 105: 1
Line 106: Type—Write a function type with Direction as the input and output, and then
Line 107: create a skeleton definition: 
Line 108: turnClockwise : Direction -> Direction
Line 109: turnClockwise x = ?turnClockwise_rhs
Line 110:  2
Line 111: Define —Define the function by case splitting on x: 
Line 112: turnClockwise : Direction -> Direction
Line 113: turnClockwise North = ?turnClockwise_rhs_1
Line 114: data Direction = North | East | South | West
Line 115: Name of the
Line 116: type constructor
Line 117: List of data constructor
Line 118: names, separated by a |
Line 119: Introduces a
Line 120: new data type
Line 121: Figure 4.1
Line 122: Defining a Direction 
Line 123: data type (Direction.idr)
Line 124: 
Line 125: --- 페이지 116 ---
Line 126: 90
Line 127: CHAPTER 4
Line 128: User-defined data types
Line 129: turnClockwise East = ?turnClockwise_rhs_2
Line 130: turnClockwise South = ?turnClockwise_rhs_3
Line 131: turnClockwise West = ?turnClockwise_rhs_4
Line 132: 3
Line 133: Refine —Fill in the holes on the right sides: 
Line 134: turnClockwise : Direction -> Direction
Line 135: turnClockwise North = East
Line 136: turnClockwise East = South
Line 137: turnClockwise South = West
Line 138: turnClockwise West = North
Line 139: 4.1.2
Line 140: Union types
Line 141: A union type is an extension of an enumerated type in which the constructors of the
Line 142: type can themselves carry data. For example, you could create an enumeration type
Line 143: for shapes: 
Line 144: data Shape = Triangle | Rectangle | Circle
Line 145: You may want to store more information with a shape, so that you can draw it, for
Line 146: example, or calculate its area. This information will differ depending on the shape: 
Line 147: For a triangle, you might want to know the length of its base and its height.
Line 148: For a rectangle, you might want to know its length and height.
Line 149: For a circle, you might want to know its radius.
Line 150: To represent this information, each of the data constructors, Triangle, Rectangle,
Line 151: and Circle, can be given argument types that carry this data using Doubles to repre-
Line 152: sent dimensions. Figure 4.2 shows some example shapes and their representations.
Line 153: You can represent shapes in this form as an Idris data type: 
Line 154: data Shape = Triangle Double Double
Line 155: | Rectangle Double Double
Line 156: | Circle Double
Line 157: Triangle 4.0 2.5
Line 158: 2.5
Line 159: 4.0
Line 160: Rectangle 4.0 2.5
Line 161: Circle 2.0
Line 162: 2.5
Line 163: 4.0
Line 164: 2.0
Line 165: Figure 4.2
Line 166: Example shapes represented as 
Line 167: a union type. Triangle takes two 
Line 168: Doubles, for base and height; Rectangle 
Line 169: takes two Doubles, for width and height; 
Line 170: Circle takes a Double for radius.
Line 171: 
Line 172: --- 페이지 117 ---
Line 173: 91
Line 174: Defining data types
Line 175: Listing 4.2 shows how you might define an area function that calculates the area of a
Line 176: shape for each of these possibilities. As an exercise, rather than typing in this function
Line 177: directly, try to construct it using the interactive editing tools in Atom.
Line 178: data Shape = Triangle Double Double
Line 179: | Rectangle Double Double
Line 180: | Circle Double
Line 181: area : Shape -> Double
Line 182: area (Triangle base height) = 0.5 * base * height
Line 183: area (Rectangle length height) = length * height
Line 184: area (Circle radius) = pi * radius * radius
Line 185: If you check the documentation for Shape using :doc, you can see how this data decla-
Line 186: ration translates into type and data constructors: 
Line 187: *Shape> :doc Shape
Line 188: Data type Main.Shape : Type
Line 189: Constructors:
Line 190: Triangle : Double -> Double -> Shape
Line 191: Rectangle : Double -> Double -> Shape
Line 192: Circle : Double -> Shape
Line 193: When you define new data types, it’s also a good idea to provide documentation that
Line 194: will be displayed with :doc, using documentation comments. In this case, it helps indi-
Line 195: cate what each Double is for. Documentation comments are laid out in data declara-
Line 196: tions by giving the comment before each constructor: 
Line 197: ||| Represents shapes
Line 198: data Shape = ||| A triangle, with its base length and height
Line 199: Triangle Double Double
Line 200: | ||| A rectangle, with its length and height
Line 201:    Rectangle Double Double
Line 202: | ||| A circle, with its radius
Line 203: Circle Double
Line 204: This is rendered as follows with :doc: 
Line 205: *Shape> :doc Shape
Line 206: Data type Main.Shape : Type
Line 207: Represents shapes
Line 208: Constructors:
Line 209: Triangle : Double -> Double -> Shape
Line 210: A triangle, with its base length and height
Line 211: Rectangle : Double -> Double -> Shape
Line 212: A rectangle, with its length and height
Line 213: Circle : Double -> Shape
Line 214: A circle, with its radius
Line 215: Listing 4.2
Line 216: Defining a Shape type and calculating its area (Shape.idr)
Line 217: pi is defined in the 
Line 218: Prelude as a constant.
Line 219: 
Line 220: --- 페이지 118 ---
Line 221: 92
Line 222: CHAPTER 4
Line 223: User-defined data types
Line 224: 4.1.3
Line 225: Recursive types
Line 226: Types can also be recursive, that is, defined in terms of themselves. For example, Nat is
Line 227: defined recursively in the Prelude as follows: 
Line 228: data Nat = Z | S Nat
Line 229: The Prelude also defines functions and notation to allow Nat to be used like any other
Line 230: numeric type, so rather than writing S (S (S (S Z))), you can simply write 4. Never-
Line 231: theless, in its primitive form it’s defined using data constructors.
Line 232: Data type syntax
Line 233: There are two forms of data declaration. In one, as you’ve already seen, you list the
Line 234: data constructors and the types of their arguments:
Line 235: data Shape = Triangle Double Double
Line 236:         | Rectangle Double Double
Line 237:         | Circle Double
Line 238: It’s also possible to define data types by giving their type and data constructors
Line 239: directly, in the form shown by :doc. You could define Shape as follows: 
Line 240: data Shape : Type where
Line 241: Triangle : Double -> Double -> Shape
Line 242: Rectangle : Double -> Double -> Shape
Line 243: Circle : Double -> Shape
Line 244: This is identical to the previous declaration. In this case, it’s a little more verbose,
Line 245: but this syntax is more general and flexible. You’ll see more of this shortly when we
Line 246: define dependent types.
Line 247: I’ll use both syntaxes throughout the book. Generally, I’ll use the concise form,
Line 248: unless I need the additional flexibility. 
Line 249: Nat and efficiency
Line 250: It would be reasonable to be concerned about the efficiency of Nat given that it’s
Line 251: defined in terms of constructors. There’s no need to worry, though, for three reasons: 
Line 252: In practice, Nat is primarily used structurally, to describe the size of a data
Line 253: structure such as Vect in its type, so the size of a Nat corresponds to the
Line 254: size of the data structure itself.
Line 255: When a program is compiled, types are erased, so a Nat that appears at the
Line 256: type level, such as in the length of a Vect, is erased.
Line 257: Internally, the compiler optimizes the representation of Nat so that it’s really
Line 258: stored as a machine integer.
Line 259: 
Line 260: --- 페이지 119 ---
Line 261: 93
Line 262: Defining data types
Line 263: You can use a recursive type to extend the Shape example from the previous section to
Line 264: represent larger pictures. We’ll define a picture as being one of the following: 
Line 265: A primitive shape
Line 266: A combination of two other pictures
Line 267: A picture rotated through an angle
Line 268: A picture translated to a different location
Line 269: Note that three of these are defined in terms of pictures themselves. You could define
Line 270: a picture type following the preceding informal description, as shown next.
Line 271: data Picture = Primitive Shape
Line 272: | Combine Picture Picture
Line 273: | Rotate Double Picture
Line 274: | Translate Double Double Picture
Line 275: Figure 4.3 shows an example of the sort of picture you could represent with this data
Line 276: type. For each of the primitive shapes, we’ll consider its location to be the top left of
Line 277: an imaginary box that bounds the shape.
Line 278: We know that there are three subpictures, so to represent this in code, you can begin
Line 279: (define) by using Combine to put three subpictures together:
Line 280: testPicture : Picture
Line 281: testPicture = Combine ?pic1 (Combine ?pic2 ?pic3)
Line 282: To continue, you know that each subpicture is translated to a specific position, so you
Line 283: can fill in those details (refine), leaving holes for the primitive shapes themselves:
Line 284: Listing 4.3
Line 285: Defining a Picture type recursively, consisting of Shapes and smaller
Line 286: Pictures (Picture.idr)
Line 287: Uses the Shape type defined 
Line 288: earlier as the primitive
Line 289: Builds a picture by combining 
Line 290: two smaller pictures
Line 291: Builds a picture by rotating 
Line 292: another picture through an angle
Line 293: Builds a picture by 
Line 294: moving a picture to 
Line 295: another location
Line 296: Circle: radius 5,
Line 297: at 35, 5
Line 298: Triangle: base 10,
Line 299: height 10, at 15, 25
Line 300: Rectangle: base 20,
Line 301: height 10, at 5, 5
Line 302: Figure 4.3
Line 303: An example picture 
Line 304: combining three shapes translated 
Line 305: to different positions
Line 306: 
Line 307: --- 페이지 120 ---
Line 308: 94
Line 309: CHAPTER 4
Line 310: User-defined data types
Line 311: testPicture : Picture
Line 312: testPicture = Combine (Translate 5 5 ?rectangle)
Line 313: (Combine (Translate 35 5 ?circle)
Line 314: (Translate 15 25 ?triangle))
Line 315: Finally, you can fill in (refine) the details of the individual primitive shapes. One way
Line 316: to do this is to use Ctrl-Alt-L in Atom to lift the holes to the top level (type), and then
Line 317: fill in the definition, resulting in the following final definition.
Line 318: rectangle : Picture
Line 319: rectangle = Primitive (Rectangle 20 10)
Line 320: circle : Picture
Line 321: circle = Primitive (Circle 5)
Line 322: triangle : Picture
Line 323: triangle = Primitive (Triangle 10 10)
Line 324: testPicture : Picture
Line 325: testPicture = Combine (Translate 5 5 rectangle)
Line 326: (Combine (Translate 35 5 circle)
Line 327: (Translate 15 25 triangle))
Line 328: As usual, you write functions over the Picture data type by case splitting. To write a
Line 329: function that calculates the area of every primitive shape in a picture, you can begin
Line 330: by writing a type: 
Line 331: pictureArea : Picture -> Double
Line 332: Then, create a skeleton definition and case-split on its argument. You should reach
Line 333: the following: 
Line 334: pictureArea : Picture -> Double
Line 335: pictureArea (Primitive x) = ?pictureArea_rhs_1
Line 336: pictureArea (Combine x y) = ?pictureArea_rhs_2
Line 337: pictureArea (Rotate x y) = ?pictureArea_rhs_3
Line 338: pictureArea (Translate x y z) = ?pictureArea_rhs_4
Line 339: This has given you an outline definition, showing you the forms the input can take
Line 340: and giving holes on the right side.
Line 341:  The names of the variables x, y, and z, chosen by Idris when creating the patterns
Line 342: for pictureArea, are not particularly informative. You can tell Idris how to choose bet-
Line 343: ter default names using the %name directive: 
Line 344: %name Shape shape, shape1, shape2
Line 345: %name Picture pic, pic1, pic2
Line 346: Now, when Idris needs to choose a variable name for a variable of type Shape, it will
Line 347: choose shape by default, followed by shape1 if shape is already in scope, followed by
Line 348: shape2. Similarly, it will choose pic, pic1, or pic2 for variables of type Picture.
Line 349: Listing 4.4
Line 350:  The picture from figure 4.3 represented in code (Picture.idr) 
Line 351: Because Rectangle is a data 
Line 352: constructor of Shape rather 
Line 353: than Picture, you need to build 
Line 354: the picture with a Primitive.
Line 355: 
Line 356: --- 페이지 121 ---
Line 357: 95
Line 358: Defining data types
Line 359:  After adding %name directives, case splitting on the argument will lead to patterns
Line 360: with more-informative variable names: 
Line 361: pictureArea : Picture -> Double
Line 362: pictureArea (Primitive shape) = ?pictureArea_rhs_1
Line 363: pictureArea (Combine pic pic1) = ?pictureArea_rhs_2
Line 364: pictureArea (Rotate x pic) = ?pictureArea_rhs_3
Line 365: pictureArea (Translate x y pic) = ?pictureArea_rhs_4
Line 366: The completed definition is given in listing 4.5. For every Picture you encounter in
Line 367: the structure, you recursively call pictureArea, and when you encounter a Shape, you
Line 368: call the area function defined previously.
Line 369: pictureArea : Picture -> Double
Line 370: pictureArea (Primitive shape) = area shape
Line 371: pictureArea (Combine pic pic1) = pictureArea pic + pictureArea pic1
Line 372: pictureArea (Rotate x pic) = pictureArea pic
Line 373: pictureArea (Translate x y pic) = pictureArea pic
Line 374: It’s always a good idea to test the resulting definition at the REPL: 
Line 375: *Picture> pictureArea testPicture
Line 376: 328.5398163397473 : Double
Line 377: 4.1.4
Line 378: Generic data types
Line 379: A generic data type is a type that’s parameterized over some other type. Just like generic
Line 380: function types, which you saw in chapter 2, generic data types allow you to capture
Line 381: common patterns of data.
Line 382: Listing 4.5
Line 383: Calculating the total area of all shapes in a Picture (Picture.idr)
Line 384: Uses the area function defined earlier to 
Line 385: calculate the area of a primitive shape
Line 386: When two pictures are combined, the area
Line 387: is the sum of the areas of those pictures.
Line 388: When a picture is rotated, the area 
Line 389: is the area of the rotated picture.
Line 390: When a picture is translated, the area
Line 391: is the area of the translated picture.
Line 392: Infinitely recursive types
Line 393: Recursive data types, just like recursive functions, need at least one non-recursive
Line 394: case in order to be useful, so at least one of the constructors needs to have a non-
Line 395: recursive argument. If you don’t do this, you’ll never be able to construct an element
Line 396: of that type. For example:
Line 397: data Infinite = Forever Infinite
Line 398: It is, however, possible to work with infinite streams of data using a generic Inf type,
Line 399: which we’ll explore in chapter 11. 
Line 400: 
Line 401: --- 페이지 122 ---
Line 402: 96
Line 403: CHAPTER 4
Line 404: User-defined data types
Line 405:  To illustrate the need for generic data types, consider a function that returns the
Line 406: area of the largest triangle in a Picture, as defined in the previous section. At first,
Line 407: you might write the following type: 
Line 408: biggestTriangle : Picture -> Double
Line 409: But what should it return if there are no triangles in the picture? You could return
Line 410: some kind of sentinel value, like a negative size, but this would be against the spirit of
Line 411: type-driven development because you’d be using Double to represent something that
Line 412: isn’t really a number. Idris also doesn’t have a null value. Instead, you could refine
Line 413: the type of biggestTriangle, introducing a new union type for capturing the possibil-
Line 414: ity that there are no triangles: 
Line 415: data Biggest = NoTriangle | Size Double
Line 416: biggestTriangle : Picture -> Biggest
Line 417: I’ll leave the definition of biggestTriangle as an exercise.
Line 418:  You might also want to write a type that represents the possibility of failure. For
Line 419: example, you could write a safe division function for Double that returns an error if
Line 420: dividing by zero: 
Line 421: data DivResult = DivByZero | Result Double
Line 422: safeDivide : Double -> Double -> DivResult
Line 423: safeDivide x y = if y == 0 then DivByZero
Line 424: else Result (x / y)
Line 425: Both Biggest and DivResult have the same structure! Instead of defining multiple
Line 426: types of this form, you can define one single generic type. In fact, such a generic type
Line 427: exists in the Prelude, called Maybe. The following listing shows the definition of Maybe.
Line 428: data Maybe valtype =
Line 429: Nothing
Line 430: | Just valtype
Line 431: In a generic type, we use type variables such as valtype here to stand for concrete
Line 432: types. You can now define safeDivide using Maybe Double instead of DivResult,
Line 433: instantiating valtype with Double: 
Line 434: safeDivide : Double -> Double -> Maybe Double
Line 435: safeDivide x y = if y == 0 then Nothing
Line 436: else Just (x / y)
Line 437: Listing 4.6
Line 438: A generic type, Maybe, that captures the possibility of failure
Line 439: The name valtype here is a type-level variable 
Line 440: standing for any type you wish to use Maybe with.
Line 441: Nothing indicates
Line 442: that no value is
Line 443: stored.
Line 444: Just is a constructor that takes one argument 
Line 445: and indicates that a single value is stored.
Line 446: 
Line 447: --- 페이지 123 ---
Line 448: 97
Line 449: Defining data types
Line 450: Generic data types can have more than one parameter, as illustrated in figure 4.4 for
Line 451: Either, which is defined in the Prelude and represents a choice between two alterna-
Line 452: tive types.
Line 453:  
Line 454: One useful example of a generic type is a binary tree structure. The following listing
Line 455: shows the definition of binary trees, using a %name directive to give naming hints for
Line 456: building definitions interactively.
Line 457: data Tree elem = Empty
Line 458: | Node (Tree elem) elem (Tree elem)
Line 459: %name Tree tree, tree1
Line 460: Listing 4.7
Line 461: Defining binary trees (Tree.idr)
Line 462: Definition of List
Line 463: We’ve already written several functions with a generic type, List, which is defined
Line 464: in the Prelude as follows: 
Line 465: data List elem = Nil | (::) elem (List elem)
Line 466: data Either a b = Left a | Right b
Line 467: Parameters
Line 468: List of data constructor
Line 469: names and their arguments
Line 470: Name of the type
Line 471: constructor
Line 472: Figure 4.4
Line 473: Defining 
Line 474: the Either data type
Line 475: Generic types and terminology
Line 476: You might hear people informally referring to “the List type” or “the Maybe type.”
Line 477: It’s not strictly accurate to do this, however. List on its own is not a type, as you
Line 478: can confirm at the REPL: 
Line 479: Idris> :t List
Line 480: List : Type -> Type
Line 481: Technically, List has a function type that takes a Type as a parameter and returns
Line 482: a Type. Although List Int is a type because it has been applied to a concrete argu-
Line 483: ment, List itself is not. Instead, we’ll informally refer to List as a generic type.
Line 484: A tree with no data
Line 485: A node with a left 
Line 486: subtree, a value, 
Line 487: and a right subtree
Line 488: 
Line 489: --- 페이지 124 ---
Line 490: 98
Line 491: CHAPTER 4
Line 492: User-defined data types
Line 493: Binary trees are commonly used to store ordered information, where everything in a
Line 494: node’s left subtree is smaller than the value at the node, and everything in a node’s
Line 495: right subtree is larger than the value at the node.
Line 496:  Such trees are called binary search trees, and you can write a function to insert a
Line 497: value into such a tree, provided that you can order those values:
Line 498: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 499: insert x tree = ?insert_rhs
Line 500: To write this function, create a Tree.idr file containing the definition in listing 4.7,
Line 501: and do the following: 
Line 502: 1
Line 503: Define—Case-split on the tree, giving the cases where the tree is Empty and
Line 504: where the tree is a Node: 
Line 505: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 506: insert x Empty = ?insert_rhs_1
Line 507: insert x (Node tree y tree1) = ?insert_rhs_2
Line 508: Even with the %name directive, the names tree, y, and tree1 aren’t especially
Line 509: informative, so let’s rename them to indicate that they’re the left subtree, the
Line 510: value at the node, and the right subtree, respectively: 
Line 511: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 512: insert x Empty = ?insert_rhs_1
Line 513: insert x (Node left val right) = ?insert_rhs_2
Line 514:  2
Line 515: Refine—For ?insert_rhs_1, you create a new tree node with empty subtrees: 
Line 516: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 517: insert x Empty = Node Empty x Empty
Line 518: insert x (Node left val right) = ?insert_rhs_2
Line 519:  3
Line 520: Define —For ?insert_rhs_2, you need to compare the value you’re inserting, x,
Line 521: with the value at the node, val. If x is smaller than val, you insert it into the left
Line 522: subtree. If it’s equal, it’s already in the tree, so you return the tree unchanged.
Line 523: If it’s greater than val, you insert it into the right subtree. To do this, you can
Line 524: use the compare function from the Prelude, which returns an element of an
Line 525: Ordering enumeration: 
Line 526: data Ordering = LT | EQ | GT
Line 527: compare : Ord a => a -> a -> Ordering
Line 528: You’ll perform a match on the intermediate result of compare x val. Press Ctrl-
Line 529: Alt-M over insert_rhs_2: 
Line 530: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 531: insert x Empty = Node Empty x Empty
Line 532: insert x (Node left val right) = case _ of
Line 533: case_val => ?insert_rhs_2
Line 534:  4
Line 535: Define —The case expression won’t type-check until the _ is replaced with an
Line 536: expression to test, so replace it with compare x val: 
Line 537: 
Line 538: --- 페이지 125 ---
Line 539: 99
Line 540: Defining data types
Line 541: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 542: insert x Empty = Node Empty x Empty
Line 543: insert x (Node left val right) = case compare x val of
Line 544: case_val => ?insert_rhs_2
Line 545: 5
Line 546: Define—If you now case-split on case_val, you’ll get the patterns for LT, EQ, and
Line 547: GT:
Line 548: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 549: insert x Empty = Node Empty x Empty
Line 550: insert x (Node left val right) = case compare x val of
Line 551: LT => ?insert_rhs_1
Line 552: EQ => ?insert_rhs_3
Line 553: GT => ?insert_rhs_4
Line 554: The following listing shows the complete definition of this function, after refining the
Line 555: remaining holes.
Line 556: insert : Ord elem => elem -> Tree elem -> Tree elem
Line 557: insert x Empty = Node Empty x Empty
Line 558: insert x (Node left val right)
Line 559: = case compare x val of
Line 560: LT => Node (insert x left) val right
Line 561: EQ => Node left val right
Line 562: GT => Node left val (insert x right)
Line 563:  
Line 564: There needs to be an Ord constraint on the generic variable elem in the type of
Line 565: insert, because otherwise you wouldn’t be able to use compare. An alternative
Line 566: Listing 4.8
Line 567: Inserting a value into a binary search tree (Tree.idr)
Line 568: x is less than the val at the 
Line 569: node, so return a new tree 
Line 570: with x inserted into the 
Line 571: left subtree.
Line 572: x is already in the tree, because 
Line 573: it’s equal to val, so return the 
Line 574: original tree.
Line 575: x is greater than the val at the node,
Line 576: so return a new tree with x inserted
Line 577: into the right subtree.
Line 578: @ patterns
Line 579: In insert, you might have noticed that in the EQ branch, the value you returned was
Line 580: exactly the same as the pattern on the left side. As a notational convenience, you
Line 581: can also name patterns:
Line 582: insert x orig@(Node left val right)
Line 583: = case compare x val of
Line 584: LT => Node (insert x left) val right
Line 585: EQ => orig
Line 586: GT => Node left val (insert x right)
Line 587: The notation orig@(Node left val right) gives the name orig to the pattern
Line 588: Node left val right. It doesn’t change the meaning of the pattern match, but
Line 589: it does mean that you can use the name orig on the right side rather than repeating
Line 590: the pattern.
Line 591: 
Line 592: --- 페이지 126 ---
Line 593: 100
Line 594: CHAPTER 4
Line 595: User-defined data types
Line 596: approach would be to capture the Ord constraint in the tree type itself, refining the
Line 597: type to include this extra precision. The following listing shows how to do this by giv-
Line 598: ing the type and data constructors directly.
Line 599: data BSTree : Type -> Type where
Line 600: Empty : Ord elem => BSTree elem
Line 601: Node : Ord elem => (left : BSTree elem) -> (val : elem) ->
Line 602: (right : BSTree elem) -> BSTree elem
Line 603: insert : elem -> BSTree elem -> BSTree elem
Line 604: insert x Empty = Node Empty x Empty
Line 605: insert x orig@(Node left val right)
Line 606: = case compare x val of
Line 607: LT => Node (insert x left) val right
Line 608: EQ => orig
Line 609: GT => Node left val (insert x right)
Line 610: PRECISION AND REUSE
Line 611: Putting a constraint in the tree structure itself makes
Line 612: the type more precise, in that it can now only store values that can be com-
Line 613: pared at the nodes, but at the cost of making it less reusable. This is a trade-
Line 614: off you’ll often have to consider when defining new data types. There are var-
Line 615: ious ways of managing this trade-off, such as pairing data with predicates that
Line 616: describe the form of that data, as you’ll see in chapter 9. 
Line 617: Exercises
Line 618: 1
Line 619: Write a function, listToTree : Ord a => List a -> Tree a, that inserts every ele-
Line 620: ment of a list into a binary search tree.
Line 621: You can test this at the REPL as follows: 
Line 622: *ex_4_1> listToTree [1,4,3,5,2]
Line 623: Node (Node Empty 1 Empty)
Line 624: 2
Line 625: (Node (Node Empty 3 (Node Empty 4 Empty))
Line 626: 5
Line 627: Empty) : Tree Integer
Line 628:  2
Line 629: Write a corresponding function, treeToList : Tree a -> List a, that flattens a tree
Line 630: into a list using in-order traversal (that is, all the values in the left subtree of a node
Line 631: should be added to the list before the value at the node, which should be added
Line 632: before the values in the right subtree).
Line 633: If you have the correct answers to exercises 1 and 2, you should be able to run
Line 634: this: 
Line 635: *ex_4_1> treeToList (listToTree [4,1,8,7,2,3,9,5,6])
Line 636: Listing 4.9
Line 637: A binary search tree with the ordering constraint in the type (BSTree.idr)
Line 638: Name this type BSTree rather than 
Line 639: Tree because the type is explicitly for 
Line 640: representing binary search trees.
Line 641: Put an Ord constraint on the data
Line 642: constructors so you can’t have a search tree
Line 643: containing values that aren’t ordered.
Line 644: There’s no need for an Ord 
Line 645: constraint on insert because 
Line 646: there are already Ord 
Line 647: constraints on elem in 
Line 648: BSTree itself.
Line 649: 
Line 650: --- 페이지 127 ---
Line 651: 101
Line 652: Defining data types
Line 653: [1, 2, 3, 4, 5, 6, 7, 8, 9] : List Integer
Line 654:  3
Line 655: An integer arithmetic expression can take one of the following forms: 
Line 656: A single integer
Line 657: Addition of an expression to an expression
Line 658: Subtraction of an expression from an expression
Line 659: Multiplication of an expression with an expression
Line 660: Define a recursive data type, Expr, that can be used to represent such expressions. 
Line 661: Hint: Look at the Picture data type and see how the informal description
Line 662: mapped to the data declaration.
Line 663:  4
Line 664: Write a function, evaluate : Expr -> Int, that evaluates an integer arithmetic
Line 665: expression.
Line 666: If you have correct answers to 3 and 4, you should be able to try something like
Line 667: the following at the REPL: 
Line 668: *ex_4_1> evaluate (Mult (Val 10) (Add (Val 6) (Val 3)))
Line 669: 90 : Int
Line 670:  5
Line 671: Write a function, maxMaybe : Ord a => Maybe a -> Maybe a -> Maybe a, that
Line 672: returns the larger of the two inputs, or Nothing if both inputs are Nothing. For
Line 673: example:
Line 674: *ex_4_1> maxMaybe (Just 4) (Just 5)
Line 675: Just 5 : Maybe Integer
Line 676: *ex_4_1> maxMaybe (Just 4) Nothing
Line 677: Just 4 : Maybe Integer
Line 678:  6
Line 679: Write a function, biggestTriangle : Picture -> Maybe Double, that returns the
Line 680: area of the biggest triangle in a picture, or Nothing if there are no triangles.
Line 681: For example, you can define the following pictures: 
Line 682: testPic1 : Picture
Line 683: testPic1 = Combine (Primitive (Triangle 2 3))
Line 684: (Primitive (Triangle 2 4))
Line 685: testPic2 : Picture
Line 686: testPic2 = Combine (Primitive (Rectangle 1 3))
Line 687: (Primitive (Circle 4))
Line 688: Then, test biggestTriangle at the REPL as follows: 
Line 689: *ex_4_1> biggestTriangle testPic1
Line 690: Just 4.0 : Maybe Double
Line 691: *ex_4_1> biggestTriangle testPic2
Line 692: Nothing : Maybe Double
Line 693: 
Line 694: --- 페이지 128 ---
Line 695: 102
Line 696: CHAPTER 4
Line 697: User-defined data types
Line 698: 4.2
Line 699: Defining dependent data types
Line 700: A dependent data type is a type that’s computed from some other value. You’ve already
Line 701: seen a dependent type, Vect, where the exact type is calculated from the vector’s
Line 702: length:
Line 703: Vect : Nat -> Type -> Type
Line 704: In other words, the type of a Vect depends on its length. This gives us additional pre-
Line 705: cision in the type, which we used to help direct our programming via the process of
Line 706: type, define, refine. In this section, you’ll see how to define dependent types such as
Line 707: Vect. The core of the idea is that, because there’s no syntactic distinction between
Line 708: types and expressions, types can be computed from any expression.
Line 709:  We’ll begin with a simple example to illustrate how this works, defining a type for
Line 710: representing vehicles and their properties, depending on their power source, and
Line 711: you’ll see how you can use this to constrain the valid inputs to a function to those that
Line 712: make sense. You’ll then see how Vect itself is defined, along with some useful opera-
Line 713: tions on it.
Line 714: 4.2.1
Line 715: A first example: classifying vehicles by power source
Line 716: Dependent types allow you to give more precise information about the data construc-
Line 717: tors of a type, by adding more arguments to the type constructor. For example, you
Line 718: might have a data type to represent vehicles (for example, bicycles, cars, and buses),
Line 719: but some operations don’t make sense on all values in the type (for example, refueling
Line 720: a bicycle wouldn’t work because there’s no fuel tank). We’ll therefore classify vehicles
Line 721: into those powered by pedal and those powered by petrol, and express this in the type.
Line 722:  The following listing shows how you could express this in Idris.
Line 723: data PowerSource = Petrol | Pedal
Line 724: data Vehicle : PowerSource -> Type where
Line 725: Bicycle : Vehicle Pedal
Line 726: Car : (fuel : Nat) -> Vehicle Petrol
Line 727: Bus : (fuel : Nat) -> Vehicle Petrol
Line 728: You can write functions that will work on all vehicles by using a type variable to stand
Line 729: for the power source. For example, all vehicles have a number of wheels. On the other
Line 730: hand, not all vehicles carry fuel, so it only makes sense to refuel a vehicle whose type
Line 731: indicates it’s powered by Petrol. Both of these concepts are illustrated in the follow-
Line 732: ing listing.
Line 733: Listing 4.10 Defining a dependent type for vehicles, with their power source in the type
Line 734: (vehicle.idr)
Line 735: An enumeration type describing 
Line 736: possible power sources for a vehicle
Line 737: A Vehicle’s type is annotated 
Line 738: with its power source.
Line 739: A vehicle
Line 740: powered
Line 741: by pedal
Line 742: A vehicle powered by petrol, with 
Line 743: a field for current fuel stocks
Line 744: 
Line 745: --- 페이지 129 ---
Line 746: 103
Line 747: Defining dependent data types
Line 748:  
Line 749: wheels : Vehicle power -> Nat
Line 750: wheels Bicycle = 2
Line 751: wheels (Car fuel) = 4
Line 752: wheels (Bus fuel) = 4
Line 753: refuel : Vehicle Petrol -> Vehicle Petrol
Line 754: refuel (Car fuel) = Car 100
Line 755: refuel (Bus fuel) = Bus 200
Line 756: In general, you should define dependent types by giving the type constructor and the
Line 757: data constructors directly. This gives you a lot of flexibility in the form that the con-
Line 758: structors can take. Here, it has allowed you to define types where the data constructors
Line 759: can each take different arguments. You can either write functions that work on all vehi-
Line 760: cles (like wheels) or functions that only work on some subset of vehicles (like refuel).
Line 761: DEFINING FAMILIES OF TYPES
Line 762: For Vehicle, you’ve actually defined two types
Line 763: in one declaration (specifically, Vehicle Pedal and Vehicle Petrol).
Line 764: Dependent data types like Vehicle are therefore sometimes referred to as
Line 765: families of types, because you’re defining multiple related types at the same
Line 766: time. The power source is an index of the Vehicle family. The index tells
Line 767: you exactly which Vehicle type you mean. 
Line 768: Listing 4.11
Line 769: Reading and updating properties of Vehicle
Line 770: Use a type variable, power, 
Line 771: because this function works 
Line 772: for all possible vehicle types.
Line 773: Refueling only makes sense for vehicles 
Line 774: that carry fuel, so restrict the input and 
Line 775: output type to Vehicle Petrol.
Line 776: Asserting that inputs are impossible
Line 777: If you try adding a case for refueling a Bicycle, Idris will report a type error, because
Line 778: the input type is restricted to vehicles powered by petrol. If you use the interactive
Line 779: tools, Idris won’t even give a case for Bicycle after a case split with Ctrl-Alt-C. Nev-
Line 780: ertheless, it can sometimes aid readability to make it explicit that you know the
Line 781: Bicycle case is impossible. You can write this: 
Line 782: refuel : Vehicle Petrol -> Vehicle Petrol
Line 783: refuel (Car fuel) = Car 100
Line 784: refuel (Bus fuel) = Bus 200
Line 785: refuel Bicycle impossible
Line 786: If you do this, Idris will check that the case you have marked as impossible would
Line 787: produce a type error.
Line 788: Similarly, if you assert a case is impossible but Idris believes it’s valid, it will report
Line 789: an error:
Line 790: refuel : Vehicle Petrol -> Vehicle Petrol
Line 791: refuel (Car fuel) = Car 100
Line 792: refuel (Bus fuel) impossible
Line 793: Here, Idris will report the following:
Line 794: vehicle.idr:15:8:refuel (Bus fuel) is a valid case
Line 795: 
Line 796: --- 페이지 130 ---
Line 797: 104
Line 798: CHAPTER 4
Line 799: User-defined data types
Line 800: 4.2.2
Line 801: Defining vectors
Line 802: In chapter 3, we looked at the ways we could use the length information in the type to
Line 803: help drive development of functions on vectors. In this section, we’ll look at how Vect
Line 804: is defined, along with some of the operations on it.
Line 805:  It’s defined in the Data.Vect module, as shown in listing 4.12. The type construc-
Line 806: tor, Vect, takes a length and an element type as arguments, so when you define the
Line 807: data constructors, you state explicitly in their types what their lengths are.
Line 808: data Vect : Nat -> Type -> Type where
Line 809: Nil
Line 810: : Vect Z a
Line 811: (::) : (x : a) -> (xs : Vect k a) -> Vect (S k) a
Line 812: %name Vect xs, ys, zs
Line 813: The Data.Vect library includes several utility functions on Vect, including concatena-
Line 814: tion, looking up values by their position in the vector, and various higher-order func-
Line 815: tions, such as map. Instead of importing this, though, we’ll use our own definition of
Line 816: Vect and try writing some functions by hand. To begin, create a Vect.idr file contain-
Line 817: ing only the definition of Vect in listing 4.12.
Line 818:  Because Vect includes the length explicitly in its type, any function that uses some
Line 819: instance of Vect will describe its length properties explicitly in its type. For example, if
Line 820: you define an append function on Vect, its type will express how the lengths of the
Line 821: inputs and output are related:
Line 822: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 823: TYPE-LEVEL EXPRESSIONS
Line 824: The expression n + m in the return type here is an
Line 825: ordinary expression with type Nat, using the ordinary + operator. Because
Line 826: Vect’s first argument is of type Nat, you should expect to be able to use any
Line 827: expression of type Nat. Remember, types are first-class, so types and expres-
Line 828: sions are all part of the same language.
Line 829: Having written the type first, as always, you can define append by case splitting on the
Line 830: first argument. You do this interactively as follows: 
Line 831: 1
Line 832: Define —Begin by creating a skeleton definition and then case splitting on the
Line 833: first argument xs: 
Line 834: Listing 4.12
Line 835: Defining vectors (Vect.idr)
Line 836: The type constructor Vect states that a vector 
Line 837: constructor takes two arguments: a Nat, which is 
Line 838: its length, and a Type, which is its element type.
Line 839: The data constructor Nil 
Line 840: explicitly states that an empty 
Line 841: vector has length Z.
Line 842: The data constructor (::) explicitly states that 
Line 843: adding an element x to a vector of length k 
Line 844: results in a vector of length S k (that is, 1 + k).
Line 845: Gives some default names to 
Line 846: use in case splits
Line 847: 
Line 848: --- 페이지 131 ---
Line 849: 105
Line 850: Defining dependent data types
Line 851: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 852: append [] ys = ?append_rhs_1
Line 853: append (x :: xs) ys = ?append_rhs_2
Line 854: 2
Line 855: Refine —Idris has enough information in the type to complete this definition by
Line 856: an expression search on each of the holes, resulting in this: 
Line 857: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 858: append [] ys = ys
Line 859: append (x :: xs) ys = x :: append xs ys
Line 860: Another common operation on vectors is zip, which pairs corresponding elements in
Line 861: two vectors, as illustrated in figure 4.5.
Line 862: Terminology: parameters and indices
Line 863: Vect defines a family of types, and we say that a Vect is indexed by its length and
Line 864: parameterized by an element type. The distinction between parameters and indices
Line 865: is as follows:
Line 866: A parameter is unchanged across the entire structure. In this case, every ele-
Line 867: ment of the vector has the same type.
Line 868: An index may change across a structure. In this case, every subvector has a
Line 869: different length.
Line 870: The distinction is most useful when looking at a function’s type: you can be certain
Line 871: that the specific value of a parameter can play no part in a function’s definition. The
Line 872: index, however, might, as you’ve already seen in chapter 3 when defining length for
Line 873: vectors by looking at the length index, and when defining createEmpties for build-
Line 874: ing a vector of empty vectors.
Line 875: "one"
Line 876: 1
Line 877: Vect 4 String
Line 878: Vect 4 Nat
Line 879: "two"
Line 880: 2
Line 881: "three"
Line 882: 3
Line 883: "four"
Line 884: (1, "one")
Line 885: Vect 4 (Nat, String)
Line 886: zip [1, 2, 3, 4] ["one", "two", "three", "four"]
Line 887: (2, "two")
Line 888: (3, "three")
Line 889: (4, "four")
Line 890: 4
Line 891: Figure 4.5
Line 892: Pairing corresponding elements of [1,2,3,4] 
Line 893: and ["one","two","three","four"] using zip
Line 894: 
Line 895: --- 페이지 132 ---
Line 896: 106
Line 897: CHAPTER 4
Line 898: User-defined data types
Line 899: The name zip is intended to suggest the workings of a zip fastener, bringing two sides
Line 900: of a bag or jacket together. Because the length of each input Vect is in the type, you
Line 901: need to think about how the lengths of the inputs and output will correspond. A rea-
Line 902: sonable choice for this would be to require the lengths of both inputs to be the same:
Line 903: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 904: Having a more precise type for Vect, capturing the length in the type, means that you
Line 905: need to decide in advance how the lengths of the inputs to zip relate and express this
Line 906: decision in the type. Also, it means you can safely assume that zip will only ever be
Line 907: called with equal length lists, because if this assumption is violated, Idris will report a
Line 908: type error.
Line 909:  You can define zip, as usual, step by step:
Line 910: 1
Line 911: Define —Again, you can begin to define this by a case split on the first argument: 
Line 912: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 913: zip [] ys = ?zip_rhs_1
Line 914: zip (x :: xs) ys = ?zip_rhs_2
Line 915:  2
Line 916: Refine —You can fill in ?zip_rhs_1 with an expression search, because the only
Line 917: well-typed result is an empty vector: 
Line 918: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 919: zip [] ys = []
Line 920: zip (x :: xs) ys = ?zip_rhs_2
Line 921: 3
Line 922: Refine —For the second case, ?zip_rhs_2, take a look at the type of the hole
Line 923: and see if that gives you further information about what to do:
Line 924: b : Type
Line 925: a : Type
Line 926: x : a
Line 927: k : Nat
Line 928: xs : Vect k a
Line 929: ys : Vect (S k) b
Line 930: --------------------------------------
Line 931: zip_rhs_2 : Vect (S k) (a, b)
Line 932: Notice that ys has length S k, meaning that there must be at least one element.
Line 933: If you case-split on ys, Idris won’t give you a pattern for the empty list, because
Line 934: it wouldn’t be a well-typed value: 
Line 935: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 936: zip [] ys = []
Line 937: zip (x :: xs) (y :: ys) = ?zip_rhs_1
Line 938: After the case split, Idris has created a new hole, so let’s take a look at the types
Line 939: of the local variables:
Line 940: b : Type
Line 941: a : Type
Line 942: x : a
Line 943: k : Nat
Line 944: 
Line 945: --- 페이지 133 ---
Line 946: 107
Line 947: Defining dependent data types
Line 948: xs : Vect k a
Line 949: y : b
Line 950: ys : Vect k b
Line 951: --------------------------------------
Line 952: zip_rhs_1 : Vect (S k) (a, b)
Line 953: Again, there’s enough information to complete the definition with an expres-
Line 954: sion search: 
Line 955: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 956: zip [] ys = []
Line 957: zip (x :: xs) (y :: ys) = (x, y) :: zip xs ys
Line 958: Idris has noticed that it needs to build a vector of length S k, that it can create
Line 959: the appropriate vector of length k with a recursive call, and that it can create
Line 960: the appropriate first element by pairing x and y.
Line 961: 4.2.3
Line 962: Indexing vectors with bounded numbers using Fin
Line 963: Because Vects carry their length as part of their type, the type checker has additional
Line 964: knowledge that it can use to check that operations are implemented and used cor-
Line 965: rectly. One example is that if you wish to look up an element in a Vect by its location
Line 966: in the vector, you can know at compile time that the location can’t be out of bounds
Line 967: when the program is run.
Line 968: Deconstructing expression searches
Line 969: To understand what expression search has done, it can be instructive to remove
Line 970: some part of the result and replace it with a hole, to see what type expression search
Line 971: was working with at that point. For example, you can remove the (x, y): 
Line 972: zip : Vect n a -> Vect n b -> Vect n (a, b)
Line 973: zip [] ys = []
Line 974: zip (x :: xs) (y :: ys) = ?element :: zip xs ys
Line 975: Then, checking the type of the ?element hole, you’ll see that at this point, Idris was
Line 976: looking for a pair of a and b:
Line 977: b : Type
Line 978: a : Type
Line 979: x : a
Line 980: k : Nat
Line 981: xs : Vect k a
Line 982: y : b
Line 983: ys : Vect k b
Line 984: --------------------------------------
Line 985: element : (a, b)
Line 986: The only way to make a pair of a and b at this point is to use x and y, so this is what
Line 987: Idris used to construct the pair. 
Line 988: 
Line 989: --- 페이지 134 ---
Line 990: 108
Line 991: CHAPTER 4
Line 992: User-defined data types
Line 993:  The index function, defined in Data.Vect, is a bounds-safe lookup function whose
Line 994: type guarantees that it will never access a location that’s outside the bounds of a vector:
Line 995: index : Fin n -> Vect n a -> a
Line 996: The first argument, of type Fin n, is an unsigned number that has a non-inclusive
Line 997: upper bound of n. The name Fin suggests that the number is finitely bounded. So, for
Line 998: example, when you look up an element by location, you can use a number within the
Line 999: bounds of the vector:
Line 1000: Idris> :module Data.Vect
Line 1001: *Data/Vect> Vect.index 3 [1,2,3,4,5]
Line 1002: IMPORTING MODULES AT THE REPL
Line 1003: In the element lookup example, you
Line 1004: import Data.Vect at the REPL using the :module command, to get access to
Line 1005: the index function. There are several functions in the Prelude called index
Line 1006: for indexing different list-like structures, so you have to disambiguate explic-
Line 1007: itly with Vect.index here.
Line 1008: But if you try to use a number outside the bounds, you’ll get a type error:
Line 1009: *Data/Vect> Vect.index 7 [1,2,3,4,5]
Line 1010: (input):1:14:When checking argument prf to function Data.Fin.fromInteger:
Line 1011: When using 7 as a literal for a Fin 5
Line 1012: 7 is not strictly less than 5
Line 1013: INTEGER LITERAL NOTATION
Line 1014: As with Nat, you can use integer literals for Fin,
Line 1015: provided that the compiler can be sure that the literal is within the bounds
Line 1016: stated in the type.
Line 1017: If you’re reading a number as user input that will be used to index a Vect, the num-
Line 1018: ber won’t always be within the bounds of the Vect. In practice, you’ll often need to
Line 1019: convert from an arbitrarily sized Integer to a bounded Fin.
Line 1020:  Importing Data.Vect gives you access to the integerToFin function, which con-
Line 1021: verts an Integer to a Fin with some bounds, provided the Integer is within bounds. It
Line 1022: has the following type: 
Line 1023: integerToFin : Integer -> (n : Nat) -> Maybe (Fin n)
Line 1024: The first argument is the integer to be converted, and the second is the upper bound
Line 1025: on the Fin. Remember that a type Fin upper, for some value of upper, represents
Line 1026: numbers up to but not including upper, so 5 is not a valid Fin 5, but 4 is. Here are a
Line 1027: couple of examples: 
Line 1028: *Data/Vect> integerToFin 2 5
Line 1029: Just (FS (FS FZ)) : Maybe (Fin 5)
Line 1030: *Data/Vect> integerToFin 6 5
Line 1031: Nothing : Maybe (Fin 5)
Line 1032: FIN CONSTRUCTORS
Line 1033: FZ and FS are constructors of Fin, corresponding to Z and
Line 1034: S as constructors of Nat. Typically, you can use numeric literals, as with Nat.
Line 1035: 
Line 1036: --- 페이지 135 ---
Line 1037: 109
Line 1038: Defining dependent data types
Line 1039: Using integerToFin, you can write a tryIndex function that looks up a value in a
Line 1040: Vect by Integer index, using Maybe in the type to capture the possibility that the
Line 1041: result may be out of range. Begin by creating a TryIndex.idr file that imports
Line 1042: Data.Vect. Then, follow these steps:
Line 1043: 1
Line 1044: Type —As ever, start by giving a type: 
Line 1045: tryIndex : Integer -> Vect n a -> Maybe a
Line 1046: Note that this type gives no relationship between the input Integer and the
Line 1047: length of the Vect.
Line 1048:  2
Line 1049: Define —You can write the definition by using integerToFin to check whether
Line 1050: the input is within range: 
Line 1051: tryIndex : Integer -> Vect n a -> Maybe a
Line 1052: tryIndex {n} i xs = case integerToFin i n of
Line 1053: case_val => ?tryIndex_rhs
Line 1054: Note that you need to bring n into scope so that you can pass it to integerTo-
Line 1055: Fin as the desired bound of the Fin.
Line 1056:  3
Line 1057: Define —Now, define the function by case splitting on case_val. If integerTo-
Line 1058: Fin returns Nothing, the input was out of bounds, so you return Nothing: 
Line 1059: tryIndex : Integer -> Vect n a -> Maybe a
Line 1060: tryIndex {n} i xs = case integerToFin i n of
Line 1061: Nothing => Nothing
Line 1062: Just idx => ?tryIndex_rhs_2
Line 1063: 4
Line 1064: Type —If you inspect the type of tryIndex_rhs_2, you’ll see that you now have a
Line 1065: Fin n and a Vect n a, so you can safely use index: 
Line 1066: n : Nat
Line 1067: idx : Fin n
Line 1068: a : Type
Line 1069: i : Integer
Line 1070: xs : Vect n a
Line 1071: --------------------------------------
Line 1072: tryIndex_rhs_2 : Maybe a
Line 1073: The end result is as follows:
Line 1074: tryIndex : Integer -> Vect n a -> Maybe a
Line 1075: tryIndex {n} i xs = case integerToFin i n of
Line 1076: Nothing => Nothing
Line 1077: Just idx => Just (index idx xs)
Line 1078: This is a common pattern in dependently typed programming, which you’ll see more
Line 1079: often in the coming chapters. The type of index tells you when it’s safe to call it, so if
Line 1080: you have an input that’s potentially unsafe, you need to check. Once you’ve converted
Line 1081: the Integer to a Fin n, you know that number must be within bounds, so you don’t
Line 1082: need to check again. 
Line 1083: 
Line 1084: --- 페이지 136 ---
Line 1085: 110
Line 1086: CHAPTER 4
Line 1087: User-defined data types
Line 1088: Exercises
Line 1089: 1
Line 1090: Extend the Vehicle data type so that it supports unicycles and motorcycles, and
Line 1091: update wheels and refuel accordingly.
Line 1092:  2
Line 1093: Extend the PowerSource and Vehicle data types to support electric vehicles (such
Line 1094: as trams or electric cars).
Line 1095:  3
Line 1096: The take function, on List, has type Nat -> List a -> List a. What’s an appropri-
Line 1097: ate type for the corresponding vectTake function on Vect?
Line 1098: Hint: How do the lengths of the input and output relate? It shouldn’t be valid to
Line 1099: take more elements than there are in the Vect. Also, remember that you can have
Line 1100: any expression in a type.
Line 1101:  4
Line 1102: Implement vectTake. If you’ve implemented it correctly, with the correct type, you
Line 1103: can test your answer at the REPL as follows: 
Line 1104: *ex_4_2> vectTake 3 [1,2,3,4,5,6,7]
Line 1105: [1, 2, 3] : Vect 3 Integer
Line 1106: You should also get a type error if you try to take too many elements: 
Line 1107: *ex_4_2> vectTake 8 [1,2,3,4,5,6,7]
Line 1108: (input):1:14:When checking argument xs to constructor Main.:::
Line 1109: Type mismatch between
Line 1110: Vect 0 a1 (Type of [])
Line 1111: and
Line 1112: Vect (S m) a (Expected type)
Line 1113:  5
Line 1114: Write a sumEntries function with the following type: 
Line 1115: sumEntries : Num a => (pos : Integer) -> Vect n a -> Vect n a -> Maybe a
Line 1116: It should return the sum of the entries at position pos in each of the inputs if pos is
Line 1117: within bounds, or Nothing otherwise. For example:
Line 1118: *ex_4_2> sumEntries 2 [1,2,3,4] [5,6,7,8]
Line 1119: Just 10 : Maybe Integer
Line 1120: *ex_4_2> sumEntries 4 [1,2,3,4] [5,6,7,8]
Line 1121: Nothing : Maybe Integer
Line 1122: Hint:
Line 1123: You’ll need to call integerToFin, but you’ll only need to do it once.
Line 1124: 4.3
Line 1125: Type-driven implementation of 
Line 1126: an interactive data store
Line 1127: To into practice put the ideas you’ve learned so far, let’s now take a look at a larger
Line 1128: example program, an interactive data store. In this section, we’ll set up the basic infra-
Line 1129: structure. We’ll revise this program in chapter 6, as you learn more about Idris, to sup-
Line 1130: port key-value pairs, with schemas for describing the form of the data.
Line 1131:  In our initial implementation, we’ll only support storing data as Strings, in mem-
Line 1132: ory, accessed by a numeric identifier. It will have a command prompt and support the
Line 1133: following commands: 
Line 1134: 
Line 1135: --- 페이지 137 ---
Line 1136: 111
Line 1137: Type-driven implementation of an interactive data store
Line 1138: 
Line 1139: add [String] adds a string to the document store and responds by printing an
Line 1140: identifier by which you can refer to the string.
Line 1141: 
Line 1142: get [Identifier] retrieves and prints the string with the given identifier,
Line 1143: assuming the identifier exists, or an error message otherwise.
Line 1144: 
Line 1145: quit exits the program.
Line 1146: A brief session might go as follows: 
Line 1147: $ ./datastore
Line 1148: Command: add Even Old New York
Line 1149: ID 0
Line 1150: Command: add Was Once New Amsterdam
Line 1151: ID 1
Line 1152: Command: get 1
Line 1153: Was Once New Amsterdam
Line 1154: Command: get 2
Line 1155: Out of range
Line 1156: Command: add Why They Changed It I Can't Say
Line 1157: ID 2
Line 1158: Command: get 2
Line 1159: Why They Changed It I Can't Say
Line 1160: Command: quit
Line 1161: We’ll use the type system to guarantee that all accesses to the data store use valid iden-
Line 1162: tifiers, and all of our functions will be total so we’re sure that the program won’t abort
Line 1163: due to unexpected input.
Line 1164:  The overall approach we’ll take, at a high level, again follows the process of type,
Line 1165: define, refine: 
Line 1166: Type—Design a new data type for the representation of the data store. In type-
Line 1167: driven development, even at the highest level, types come first. Before we can
Line 1168: implement any part of a data store program, we need to know how we’re repre-
Line 1169: senting and working with the data.
Line 1170: Define —Implement as much of a main program as we can, leaving holes for
Line 1171: parts we can’t write immediately, lifting these holes to top-level functions.
Line 1172: Refine—As we go deeper into the implementation and improve our understand-
Line 1173: ing of the problem, we’ll refine the implementation and types as necessary.
Line 1174: To begin, create an outline of a DataStore.idr file that contains a module header, an
Line 1175: import statement for Data.Vect, and an empty main function, as follows.
Line 1176: module Main
Line 1177: import Data.Vect
Line 1178: main : IO ()
Line 1179: main = ?main_rhs
Line 1180: Listing 4.13
Line 1181: Outline implementation of the data store (DataStore.idr)
Line 1182: Use Vect to store the data so you can keep 
Line 1183: track of the size of the store in types
Line 1184: Initial implementation 
Line 1185: of main is empty
Line 1186: 
Line 1187: --- 페이지 138 ---
Line 1188: 112
Line 1189: CHAPTER 4
Line 1190: User-defined data types
Line 1191: We’ll start by defining a type to represent the store, and then we’ll write a main func-
Line 1192: tion that reads user input and updates the store according to user commands. As we
Line 1193: progress through the implementation, we’ll add new types and functions as necessary,
Line 1194: always guided by the Idris type checker.
Line 1195: 4.3.1
Line 1196: Representing the store
Line 1197: The data store itself is, initially, a collection of strings. We’ll begin by defining a type
Line 1198: for the store, including the size of the store (that is, the number of stored items),
Line 1199: explicitly and using a Vect for the items, as shown in the following listing. You can add
Line 1200: this to DataStore.idr, above the initial empty definition of main.
Line 1201: data DataStore : Type where
Line 1202: MkData : (size : Nat) ->
Line 1203: (items : Vect size String) ->
Line 1204: DataStore
Line 1205: You can access the size and content of a data store by writing functions that pattern
Line 1206: match on the data store and extract the appropriate fields. These are shown in the fol-
Line 1207: lowing listing.
Line 1208: size : DataStore -> Nat
Line 1209: size (MkData size' items') = size'
Line 1210: items : (store : DataStore) -> Vect (size store) String
Line 1211: items (MkData size' items') = items'
Line 1212: In this listing, the length of the Vect in the type of items is calculated by a function,
Line 1213: size.
Line 1214: RECORDS
Line 1215: A data type with one constructor, like DataStore, is essentially a
Line 1216: record with fields for its data. In chapter 6, you’ll see a more concise syntax
Line 1217: for records that avoids the need to write explicit projection functions such as
Line 1218: size and items.
Line 1219: You’ll also need to add new data items to the store, as in listing 4.16. This adds items
Line 1220: to the end of the store, rather than at the beginning using :: directly. The reason for
Line 1221: this is that we plan to access items by their integer index; if you add items at the begin-
Line 1222: ning, new items will always have an index of zero, and everything else will be shifted
Line 1223: along one place.
Line 1224: Listing 4.14
Line 1225: A data type for representing the data store (DataStore.idr)
Line 1226: Listing 4.15
Line 1227: Projecting out the size and content of a data store (DataStore.idr)
Line 1228: DataStore is the type constructor.
Line 1229: MkData is the data constructor, which gives the canonical 
Line 1230: way of constructing a data store. You can think of its 
Line 1231: arguments, size, and items as the fields of a record.
Line 1232: The type explicitly states that 
Line 1233: the length of this Vect is the size 
Line 1234: of the store.
Line 1235: The length in the 
Line 1236: type of the Vect 
Line 1237: projected out of the 
Line 1238: store is given by the 
Line 1239: size projected out of 
Line 1240: the store.
Line 1241: 
Line 1242: --- 페이지 139 ---
Line 1243: 113
Line 1244: Type-driven implementation of an interactive data store
Line 1245:  
Line 1246: addToStore : DataStore -> String -> DataStore
Line 1247: addToStore (MkData size items) newitem = MkData _ (addToData items)
Line 1248: where
Line 1249: addToData : Vect old String -> Vect (S old) String
Line 1250: addToData [] = [newitem]
Line 1251: addToData (item :: items) = item :: addToData items
Line 1252: 4.3.2
Line 1253: Interactively maintaining state in main
Line 1254: When you implement the main function for your data store, you’ll need to read input
Line 1255: from the user, maintain the state of the store itself, and allow the user to exit. In the
Line 1256: last chapter, we used the Prelude function repl to write a simple interactive program
Line 1257: that repeatedly read input, ran a function on it, and displayed the output: 
Line 1258: repl : String -> (String -> String) -> IO ()
Line 1259: Unfortunately, this only allows simple interactions that repeat forever.
Line 1260:  For more-complex programs that maintain state, the Prelude provides another
Line 1261: function, replWith, which implements a read-eval-print loop that carries some state.
Line 1262: :doc describes it as follows: 
Line 1263: Idris> :doc replWith
Line 1264: Prelude.Interactive.replWith : (state : a) ->
Line 1265: (prompt : String) ->
Line 1266: (onInput : a -> String -> Maybe (String, a)) -> IO ()
Line 1267: Listing 4.16
Line 1268: Adding a new entry to the data store (DataStore.idr)
Line 1269: You can use _ here, rather than giving the size 
Line 1270: explicitly, because Idris can work out the new size at 
Line 1271: compile time from the type of addToData.
Line 1272: This type states that addToData 
Line 1273: always increases the length of 
Line 1274: the store by 1.
Line 1275: In a where block, functions have access
Line 1276: to the pattern variables of the outer
Line 1277: function, so you can use newitem here.
Line 1278: Interactive editing in where blocks
Line 1279: The interactive editing tools work just as effectively in where blocks as they do at
Line 1280: the top level. For example, try implementing addToStore beginning at this point: 
Line 1281: addToStore : DataStore -> String -> DataStore
Line 1282: addToStore (MkData size items) newitem
Line 1283: = MkData _ (addToData items)
Line 1284: where
Line 1285: addToData : Vect old String -> Vect (S old) String
Line 1286: You can use Ctrl-Alt-A to add a definition for addToData, and expression search with
Line 1287: Ctrl-Alt-S is aware that newitem is in scope.
Line 1288: 
Line 1289: --- 페이지 140 ---
Line 1290: 114
Line 1291: CHAPTER 4
Line 1292: User-defined data types
Line 1293: A basic read-eval-print loop, maintaining a state
Line 1294: Arguments:
Line 1295: state : a
Line 1296: -- the input state
Line 1297: prompt : String
Line 1298: -- the prompt to show
Line 1299: onInput : a -> String -> Maybe (String, a)
Line 1300: -- the function to
Line 1301: run on reading input, returning a String to output and a new
Line 1302: state. Returns Nothing if the repl should exit
Line 1303: On each iteration through the loop, it calls the onInput argument, which itself takes
Line 1304: two arguments: 
Line 1305: The current state, of some generic type a
Line 1306: The String entered at the prompt
Line 1307: The value the onInput function should return is of type Maybe (String, a), meaning
Line 1308: that it can be in one of the following forms: 
Line 1309: 
Line 1310: Nothing, if it wants the loop to exit
Line 1311: 
Line 1312: Just (output, newState), if it wants to print some output and update the
Line 1313: state to newState for the next iteration 
Line 1314: The next listing shows a simple example of this in action: an interactive program that
Line 1315: reads an integer from the console and displays a running total of the sum of the
Line 1316: inputs. If it reads a negative value, it will exit.
Line 1317: sumInputs : Integer -> String -> Maybe (String, Integer)
Line 1318: sumInputs tot inp
Line 1319: = let val = cast inp in
Line 1320: if val < 0
Line 1321: then Nothing
Line 1322: else let newVal = tot + val in
Line 1323: Just ("Subtotal: " ++ show newVal ++ "\n", newVal)
Line 1324: main : IO ()
Line 1325: main = replWith 0 "Value: " sumInputs
Line 1326: You can use replWith to refine the main function in the data store. At this stage you have 
Line 1327: A type for the data store (DataStore)
Line 1328: A way of accessing the items in the store (items)
Line 1329: A way of updating the store with new items (addToStore)
Line 1330: Listing 4.17 Interactive program to sum input values until a negative value is read 
Line 1331: (SumInputs.idr)
Line 1332: Casts the input String to an Integer. Default value is 0 
Line 1333: if the input is not a valid number. Idris knows that val 
Line 1334: must be an Integer because it’s used later in a context 
Line 1335: where only Integer is well typed.
Line 1336: Negative input 
Line 1337: received, so returns 
Line 1338: Nothing, which 
Line 1339: exits the loop
Line 1340: Calculates a new state
Line 1341: (newVal) and continues the
Line 1342: loop, giving the subtotal as an
Line 1343: output, and the new state
Line 1344: Initializes
Line 1345: the loop
Line 1346: with 0 as
Line 1347: the initial
Line 1348: state
Line 1349: 
Line 1350: --- 페이지 141 ---
Line 1351: 115
Line 1352: Type-driven implementation of an interactive data store
Line 1353: When you call replWith, you need to pass the initial data, a prompt, and a function to
Line 1354: process inputs as arguments. You can pass an initialized empty data store and a
Line 1355: prompt string, but you don’t yet have a function to process user input. Nevertheless,
Line 1356: you can refine your definition of main to the following, leaving a hole for the input-
Line 1357: processing function: 
Line 1358: main : IO ()
Line 1359: main = replWith (MkData _ []) "Command: " ?processInput
Line 1360: Lifting processInput shows the type you have to work with:
Line 1361: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1362: main : IO ()
Line 1363: main = replWith (MkData _ []) "Command: " processInput
Line 1364: Following the type-driven approach, when you refined the definition of main with an
Line 1365: application of replWith, Idris was able to work out the necessary specialized type for
Line 1366: processInput. 
Line 1367: 4.3.3
Line 1368: Commands: parsing user input
Line 1369: To process the String input, you somehow have to work out which one of the com-
Line 1370: mands add, get, or quit has been entered. Rather than processing the input string
Line 1371: directly, it’s usually much cleaner to define a new data type that represents the possible
Line 1372: commands. This way, you can cleanly separate the parsing of commands from the
Line 1373: processing.
Line 1374:  You’ll therefore define a Command data type, which is a union type representing the
Line 1375: possible commands and their arguments. Put the following definition in DataStore.idr
Line 1376: above processInput:
Line 1377: data Command = Add String
Line 1378: | Get Integer
Line 1379: | Quit
Line 1380: AVOID USING STRINGS FOR DATA REPRESENTATION
Line 1381: The user enters a String,
Line 1382: but only a certain number of Strings are valid input commands. Introduc-
Line 1383: ing the Command type makes the representation of commands more precise
Line 1384: in that only valid commands can be represented. If the user enters a String
Line 1385: that can’t be converted to a Command, the types force you to think about how
Line 1386: to handle the error. At first, you can leave a hole in the program for error
Line 1387: handling, but, ultimately, making a precise type leads to a more robust
Line 1388: implementation.
Line 1389: You need to convert the string input by the user into a Command. The input may be
Line 1390: invalid, however, so the type of the function to parse the command captures this possi-
Line 1391: bility in its type:
Line 1392: parse : (input : String) -> Maybe Command
Line 1393: 
Line 1394: --- 페이지 142 ---
Line 1395: 116
Line 1396: CHAPTER 4
Line 1397: User-defined data types
Line 1398: You can write a simple parser for input commands by searching for the first space in
Line 1399: the input using the span function to establish which part of the input is the command
Line 1400: and which is the argument. The span function works as follows:
Line 1401: Idris> :t Strings.span
Line 1402: span : (Char -> Bool) -> String -> (String, String)
Line 1403: Idris> span (/= ' ') "Hello world, here is a string"
Line 1404: ("Hello", " world, here is a string") : (String, String)
Line 1405: The first argument, (/= ' '), is a test that returns a Bool. This test returns True for
Line 1406: any character that’s not equal to a space. The second argument is an input string, and
Line 1407: span will split the string into two parts: 
Line 1408: The first part is the prefix of the input string, where all characters satisfy the
Line 1409: test.
Line 1410: The second part is the remainder of the string. If all characters in the string sat-
Line 1411: isfy the test, this will be empty.
Line 1412: You can define parse with Ctrl-Alt-A and then refine its definition to the following:
Line 1413: parse : (input : String) -> Maybe Command
Line 1414: parse input = case span (/= ' ') input of
Line 1415: (cmd, args) => ?parseCommand
Line 1416: You can then lift parseCommand to a top-level function with the appropriate type, using
Line 1417: Ctrl-Alt-L:
Line 1418: parseCommand : (cmd : String) -> (args : String) -> (input : String) ->
Line 1419: Maybe Command
Line 1420: parse : (input : String) -> Maybe Command
Line 1421: parse input = case span (/= ' ') input of
Line 1422: (cmd, args) => parseCommand cmd args input
Line 1423: You won’t need the input argument because you’ll be parsing the input from cmd and
Line 1424: args alone, although Idris has added it because input is in scope. You can therefore
Line 1425: edit the type:
Line 1426: parseCommand : (cmd : String) -> (args : String) -> Maybe Command
Line 1427: parse : (input : String) -> Maybe Command
Line 1428: parse input = case span (/= ' ') input of
Line 1429: (cmd, args) => parseCommand cmd args
Line 1430: Also, you can see that args, if it’s not empty, will have a leading space, because the first
Line 1431: character that span encounters that doesn’t satisfy the test will be a space. You can
Line 1432: remove leading spaces with the ltrim : String -> String function, which returns its
Line 1433: input with leading whitespace characters removed:
Line 1434: parseCommand : (cmd : String) -> (args : String) -> Maybe Command
Line 1435: parse : (input : String) -> Maybe Command
Line 1436: parse input = case span (/= ' ') input of
Line 1437: (cmd, args) => parseCommand cmd (ltrim args)
Line 1438: 
Line 1439: --- 페이지 143 ---
Line 1440: 117
Line 1441: Type-driven implementation of an interactive data store
Line 1442: You can now write parseCommand by examining the cmd and args arguments. You’ll
Line 1443: need some Prelude functions to complete the definition of parseCommand: 
Line 1444: 
Line 1445: unpack : String -> List Char converts a String into a list of characters.
Line 1446: 
Line 1447: isDigit : Char -> Bool returns whether a Char is one of the digits 0–9.
Line 1448: 
Line 1449: all : (a -> Bool) -> List a -> Bool returns whether every entry in a list
Line 1450: satisfies a test.
Line 1451: Thus, the expression all isDigit (unpack val) returns whether the string val con-
Line 1452: sists entirely of digits.
Line 1453: DOCUMENTATION AND PRELUDE FUNCTIONS
Line 1454: In general, remember that you can
Line 1455: use :doc at the REPL, or Ctrl-Alt-D in Atom, to check the documentation for
Line 1456: any names, no matter whether they are type constructors, data constructors,
Line 1457: or functions.
Line 1458: Listing 4.18 shows how parsing the input works. In particular, notice that pattern
Line 1459: matching is very general; as long as patterns are composed of primitive ways of con-
Line 1460: structing a type (data constructors and primitive values), they are valid. An under-
Line 1461: score is a match-anything pattern.
Line 1462: parseCommand : String -> String -> Maybe Command
Line 1463: parseCommand "add" str = Just (Add str)
Line 1464: parseCommand "get" val = case all isDigit (unpack val) of
Line 1465: False => Nothing
Line 1466: True => Just (Get (cast val))
Line 1467: parseCommand "quit" "" = Just Quit
Line 1468: parseCommand _ _ = Nothing
Line 1469: Now that you can parse a string into a Command, you can make more progress with
Line 1470: processInput, calling parse. If it fails, you display an error message and leave the
Line 1471: store as it is. Otherwise, you add a hole for processing the Command:
Line 1472: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1473: processInput store inp
Line 1474: = case parse inp of
Line 1475: Nothing => Just ("Invalid command\n", store)
Line 1476: Just cmd => ?processCommand
Line 1477: Listing 4.18
Line 1478: Parsing a command and argument string into a Command (DataStore.idr)
Line 1479: This pattern matches an 
Line 1480: application where the first 
Line 1481: argument is "add". The string 
Line 1482: you add to the store will be 
Line 1483: composed of the entire 
Line 1484: second argument, str.
Line 1485: This pattern matches an
Line 1486: application where the first
Line 1487: argument is "get". The parse is
Line 1488: valid if the second argument
Line 1489: consists entirely of digits.
Line 1490: This matches any input. Pattern
Line 1491: matching works top to bottom;
Line 1492: if none of the previous patterns
Line 1493: have matched, then the input is
Line 1494: invalid, so there’s no Command.
Line 1495: 
Line 1496: --- 페이지 144 ---
Line 1497: 118
Line 1498: CHAPTER 4
Line 1499: User-defined data types
Line 1500: 4.3.4
Line 1501: Processing commands
Line 1502: One way to proceed with your implementation of processInput would be to case-split
Line 1503: on cmd and process the commands directly:
Line 1504: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1505: processInput store inp
Line 1506: = case parse inp of
Line 1507: Nothing => Just ("Invalid command\n", store)
Line 1508: Just (Add item) => ?processCommand_1
Line 1509: Just (Get pos) => ?processCommand_2
Line 1510: Just Quit => ?processCommand_3
Line 1511: You can refine the implementation by filling in the easier holes, in the cases for Add
Line 1512: item and Quit. The next listing shows how these holes are refined, leaving process-
Line 1513: Command_2 for the moment.
Line 1514: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1515: processInput store inp
Line 1516: = case parse inp of
Line 1517: Nothing => Just ("Invalid command\n", store)
Line 1518: Just (Add item) =>
Line 1519: Just ("ID " ++ show (size store) ++ "\n", addToStore store item)
Line 1520: Just (Get pos) => ?processCommand_2
Line 1521: Just Quit => Nothing
Line 1522: It’s always a good idea to inspect the types of holes Idris has generated to see what vari-
Line 1523: ables you have available, what their types are, and what type you need to build. For
Line 1524: ?processCommand_2, you have this:
Line 1525: pos : Integer
Line 1526: store : DataStore
Line 1527: input : String
Line 1528: --------------------------------------
Line 1529: processCommand_2 : Maybe (String, DataStore)
Line 1530: This will be slightly more involved than the other cases. You need to do the following:
Line 1531: Get the items from the store.
Line 1532: Ensure that the position, pos, is in range.
Line 1533: If it is, extract the item from the specified pos and return it along with the store
Line 1534: itself.
Line 1535: The type-define-refine process encourages you to write parts of definitions, step by
Line 1536: step, constantly type-checking as you go, and constantly inspecting the types of the
Line 1537: holes.
Line 1538: Listing 4.19
Line 1539: Processing the inputs Add item and Quit (DataStore.idr)
Line 1540: Returns a String that gives the position at which this 
Line 1541: item was added and an updated store using addToStore
Line 1542: Quit command exits, 
Line 1543: so return Nothing
Line 1544: 
Line 1545: --- 페이지 145 ---
Line 1546: 119
Line 1547: Type-driven implementation of an interactive data store
Line 1548:  Because there are a few details involved in filling the ?processCommand_2 hole,
Line 1549: we’ll rename it ?getEntry and lift it to a top-level function before implementing it
Line 1550: step by step:
Line 1551: 1
Line 1552: Type —Lift getEntry to a new top-level function: 
Line 1553: getEntry : (pos : Integer) -> (store : DataStore) -> (input : String) ->
Line 1554: Maybe (String, DataStore)
Line 1555:  2
Line 1556: Define —Create a new skeleton definition: 
Line 1557: getEntry pos store input = ?getEntry_rhs
Line 1558:  3
Line 1559: Define —You’ll need the items in the store, so define a new local variable for
Line 1560: these: 
Line 1561: getEntry pos store input = let store_items = items store in
Line 1562: ?getEntry_rhs
Line 1563: Inspecting the type of getEntry_rhs tells you the type of store_items: 
Line 1564: pos : Integer
Line 1565: store : DataStore
Line 1566: input : String
Line 1567: store_items : Vect (size store) String
Line 1568: --------------------------------------
Line 1569: getEntry_rhs : Maybe (String, DataStore)
Line 1570:  4
Line 1571: Refine —To retrieve an entry from a Vect, you can use index as you’ve previ-
Line 1572: ously seen: 
Line 1573: index : Fin n -> Vect n a -> a
Line 1574: To extract an entry from store_items, which has type Vect (size store),
Line 1575: you’ll need a Fin (size store). Unfortunately, all you have available at the
Line 1576: moment is an Integer. Using integerToFin, as described in section 4.2.34.2.3,
Line 1577: you can refine the definition. If integerToFin returns Nothing, the input was
Line 1578: out of bounds. 
Line 1579: getEntry : (pos : Integer) -> (store : DataStore) -> (input : String) ->
Line 1580: Maybe (String, DataStore)
Line 1581: getEntry pos store input
Line 1582: = let store_items = items store in
Line 1583: case integerToFin pos (size store) of
Line 1584: Nothing => Just ("Out of range\n", store)
Line 1585: Just id => ?getEntry_rhs_2
Line 1586:  5
Line 1587: Refine —If you inspect the type of getEntry_rhs_2 now, you’ll see that you have
Line 1588: the Fin (size store) you need: 
Line 1589: store : DataStore
Line 1590: id : Fin (size store)
Line 1591: pos : Integer
Line 1592: input : String
Line 1593: store_items : Vect (size store) String
Line 1594: --------------------------------------
Line 1595: 
Line 1596: --- 페이지 146 ---
Line 1597: 120
Line 1598: CHAPTER 4
Line 1599: User-defined data types
Line 1600: getEntry_rhs_2 : Maybe (String, DataStore)
Line 1601: You can now refine to a complete definition: 
Line 1602: getEntry : (pos : Integer) -> (store : DataStore) -> (input : String)
Line 1603: Maybe (String, DataStore)
Line 1604: getEntry pos store input
Line 1605: = let store_items = items store in
Line 1606: case integerToFin pos (size store) of
Line 1607: Nothing => Just ("Out of range\n", store)
Line 1608: Just id => Just (index id store_items ++ "\n", store)
Line 1609: 6
Line 1610: Refine —As a final refinement, observe that input is never used, so you can
Line 1611: remove this argument. Don’t forget to remove it from the application of get-
Line 1612: Entry in processInput too. 
Line 1613: getEntry : (pos : Integer) -> (store : DataStore) ->
Line 1614:                  Maybe (String, DataStore)
Line 1615: getEntry pos store
Line 1616: = let store_items = items store in
Line 1617: case integerToFin pos (size store) of
Line 1618: Nothing => Just ("Out of range\n", store)
Line 1619: Just id => Just (index id store_items ++ "\n", store)
Line 1620: By using a Vect for the store, with its size as part of the type, the type system can
Line 1621: ensure that any access of the store by index will be within bounds, because you have to
Line 1622: show that the index has the same upper bound as the length of the Vect.
Line 1623:  For reference, the complete implementation of the data store is given in the fol-
Line 1624: lowing listing, with all the functions we just worked through. 
Line 1625: module Main
Line 1626: import Data.Vect
Line 1627: data DataStore : Type where
Line 1628: MkData : (size : Nat) -> (items : Vect size String) -> DataStore
Line 1629: size : DataStore -> Nat
Line 1630: size (MkData size' items') = size'
Line 1631: items : (store : DataStore) -> Vect (size store) String
Line 1632: items (MkData size' items') = items'
Line 1633: addToStore : DataStore -> String -> DataStore
Line 1634: addToStore (MkData size store) newitem = MkData _ (addToData store)
Line 1635: where
Line 1636: addToData : Vect oldsize String -> Vect (S oldsize) String
Line 1637: addToData [] = [newitem]
Line 1638: addToData (x :: xs) = x :: addToData xs
Line 1639: data Command = Add String
Line 1640: | Get Integer
Line 1641: | Quit
Line 1642: Listing 4.20
Line 1643: Complete implementation of a simple data store (DataStore.idr)
Line 1644: 
Line 1645: --- 페이지 147 ---
Line 1646: 121
Line 1647: Type-driven implementation of an interactive data store
Line 1648: parseCommand : String -> String -> Maybe Command
Line 1649: parseCommand "add" str = Just (Add str)
Line 1650: parseCommand "get" val = case all isDigit (unpack val) of
Line 1651: False => Nothing
Line 1652: True => Just (Get (cast val))
Line 1653: parseCommand "quit" "" = Just Quit
Line 1654: parseCommand _ _ = Nothing
Line 1655: parse : (input : String) -> Maybe Command
Line 1656: parse input = case span (/= ' ') input of
Line 1657: (cmd, args) => parseCommand cmd (ltrim args)
Line 1658: getEntry : (pos : Integer) -> (store : DataStore) ->
Line 1659: Maybe (String, DataStore)
Line 1660: getEntry pos store
Line 1661: = let store_items = items store in
Line 1662: case integerToFin pos (size store) of
Line 1663: Nothing => Just ("Out of range\n", store)
Line 1664: Just id => Just (index id (items store) ++ "\n", store)
Line 1665: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1666: processInput store input
Line 1667: = case parse input of
Line 1668: Nothing => Just ("Invalid command\n", store)
Line 1669: Just (Add item) =>
Line 1670: Just ("ID " ++ show (size store) ++ "\n", addToStore store item)
Line 1671: Just (Get pos) => getEntry pos store
Line 1672: Just Quit => Nothing
Line 1673: main : IO ()
Line 1674: main = replWith (MkData _ []) "Command: " processInput
Line 1675: Exercises
Line 1676: 1
Line 1677: Add a size command that displays the number of entries in the store.
Line 1678:  2
Line 1679: Add a search command that displays all the entries in the store containing a given
Line 1680: substring.
Line 1681: Hint: Use Strings.isInfixOf.
Line 1682:  3
Line 1683: Extend search to print the location of each result, as well as the string.
Line 1684: You can test your solution at the REPL as follows:
Line 1685: *ex_4_3> :exec
Line 1686: Command: add Shearer
Line 1687: ID 0
Line 1688: Command: add Milburn
Line 1689: ID 1
Line 1690: Command: add White
Line 1691: ID 2
Line 1692: Command: size
Line 1693: 3
Line 1694: Command: search Mil
Line 1695: 1: Milburn
Line 1696: 
Line 1697: --- 페이지 148 ---
Line 1698: 122
Line 1699: CHAPTER 4
Line 1700: User-defined data types
Line 1701: 4.4
Line 1702: Summary
Line 1703: Data types are defined in terms of a type constructor and data constructors.
Line 1704: Enumeration types are defined by listing the data constructors of the type.
Line 1705: Union types are defined by listing the data constructors of the type, each of
Line 1706: which may carry additional information.
Line 1707: Generic types are parameterized over some other type. In a generic type defini-
Line 1708: tion, variables stand in place of concrete types.
Line 1709: Dependent types can be indexed over any other value.
Line 1710: Using dependent types, you can classify a larger family of types (such as vehi-
Line 1711: cles) into smaller subgroups (such as vehicles powered by petrol and those pow-
Line 1712: ered by pedal) in the same declaration.
Line 1713: Dependent types allow safety checks to be guaranteed at compile time, such as
Line 1714: guaranteeing that all vector accesses are within the bounds of the vector.
Line 1715: You can write larger programs in the type-driven style, creating new data types
Line 1716: where appropriate to help describe components of the system.
Line 1717: Interactive programs that involve state can be written using the replWith function.