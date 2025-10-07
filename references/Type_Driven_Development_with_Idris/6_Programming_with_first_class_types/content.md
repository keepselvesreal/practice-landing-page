Line 1: 
Line 2: --- 페이지 173 ---
Line 3: 147
Line 4: Programming with
Line 5: first-class types
Line 6: In Idris, as you’ve seen several times now, types can be manipulated just like any
Line 7: other language construct. For example, they can be stored in variables, passed to
Line 8: functions, or constructed by functions. Furthermore, because they’re truly first-class,
Line 9: expressions can compute types, and types can also take any expression as an argu-
Line 10: ment. You’ve seen several uses of this concept in practice, in particular the ability to
Line 11: store additional information about data in its type, such as the length of a vector.
Line 12:  In this chapter, we’ll explore more ways of taking advantage of the first-class
Line 13: nature of types. You’ll see how type-level functions can be used to give alternative
Line 14: names to types and also to calculate the type of a function from some other data. In
Line 15: This chapter covers
Line 16: Programming with type-level functions
Line 17: Writing functions with varying numbers of 
Line 18: arguments
Line 19: Using type-level functions to calculate the 
Line 20: structure of data
Line 21: Refining larger interactive programs
Line 22: 
Line 23: --- 페이지 174 ---
Line 24: 148
Line 25: CHAPTER 6
Line 26: Programming with first-class types
Line 27: particular, you’ll see how you can write a type-safe formatted output function, printf.
Line 28: For printf, the type (and even number) of arguments to the function are calculated
Line 29: from a format string provided as its first argument. This technique, calculating the type
Line 30: of some data (in this case, the arguments to printf) based on some other data (in this
Line 31: case, the format string) is often useful. Here are a couple of examples:
Line 32: Given an HTML form on a web page, you can calculate the type of a function to
Line 33: process inputs in the form.
Line 34: Given a database schema, you can calculate types for queries on that database.
Line 35: As an example of this concept, you’ll see how to use type-level functions to refine the
Line 36: data store we implemented at the end of chapter 4. Previously, you could only store
Line 37: data as Strings, but for more flexibility you might want the form of the data to be
Line 38: described by a user rather than hardcoded into the program. Using type-level func-
Line 39: tions, you’ll extend the data store with a schema that describes the form of the data,
Line 40: and you’ll use that schema to calculate appropriate types for functions to parse and
Line 41: display user data. In doing so, you’ll learn more about using holes to help correct
Line 42: errors when refining larger programs.
Line 43:  To begin, we’ll look at how to use functions at the type level to calculate types.
Line 44: 6.1
Line 45: Type-level functions: calculating types
Line 46: One of the most fundamental features of Idris is that types and expressions are part of
Line 47: the same language—you use the same syntax for both. You’ve already seen in chapter 4
Line 48: that expressions can appear in types. For example, in the type of append on Vect, we
Line 49: have n and m (both Nats), and the resulting length is n + m:
Line 50: append : Vect n elem -> Vect m elem -> Vect (n + m) elem
Line 51: Here, n, m, and n + m all have type Nat, which can also be used in ordinary expressions.
Line 52: Similarly, you can use types in expressions and therefore write functions that calculate
Line 53: types. There are two common situations where you might want to do this: 
Line 54: To give more meaningful names to composite types—For example, if you have a type
Line 55: (Double, Double) representing a position as a 2D coordinate, you might prefer
Line 56: to call the type Position to make the code more readable and self-documenting.
Line 57: To allow a function’s type to vary according to some contextual information—For exam-
Line 58: ple, the type of a value returned by a database query will vary depending on the
Line 59: database schema and the query itself.
Line 60: In the first case, you can define type synonyms, which give alternative names to types. In
Line 61: the second case, you can define type-level functions (of which type synonyms are a special
Line 62: case) that calculate types from some input. In this section, we’ll take a look at both.
Line 63: 
Line 64: --- 페이지 175 ---
Line 65: 149
Line 66: Type-level functions: calculating types
Line 67: 6.1.1
Line 68: Type synonyms: giving informative names to complex types
Line 69: Let’s say you’re writing an application that deals with complex polygons, such as a
Line 70: drawing application. You might represent a polygon as a vector of the coordinates of
Line 71: each corner. A triangle, for example, might be initialized as follows:
Line 72: tri : Vect 3 (Double, Double)
Line 73: tri = [(0.0, 0.0), (3.0, 0.0), (0.0, 4.0)]
Line 74: The type, Vect 3 (Double, Double) says exactly what the form of the data will be,
Line 75: which is useful to the machine, but it doesn’t give any indication to the reader what
Line 76: the purpose of the data is. Instead, you can refine the type using a type synonym for a
Line 77: position represented as a 2D coordinate:
Line 78: Position : Type
Line 79: Position = (Double, Double)
Line 80: Here, you have a function called Position that takes no arguments and returns a
Line 81: Type. This is an ordinary function; there’s nothing special about the way it’s declared
Line 82: or implemented. Now, anywhere you can use a Type, you can use Position to calcu-
Line 83: late that type. For example, the triangle can be defined with a refined type as follows:
Line 84: tri : Vect 3 Position
Line 85: tri = [(0.0, 0.0), (3.0, 0.0), (0.0, 4.0)]
Line 86: This kind of function is a type synonym because it provides an alternative name for
Line 87: some other type.
Line 88: NAMING CONVENTION
Line 89: By convention, we usually use an initial capital letter for
Line 90: functions that are intended to compute types.
Line 91: Because they’re ordinary functions, they can also take arguments. For example, the
Line 92: following listing shows how you can use type synonyms to express more clearly that the
Line 93: Vect is intended to represent a polygon.
Line 94: import Data.Vect
Line 95: Position : Type
Line 96: Position = (Double, Double)
Line 97: Polygon : Nat -> Type
Line 98: Polygon n = Vect n Position
Line 99: tri : Polygon 3
Line 100: tri = [(0.0, 0.0), (3.0, 0.0), (0.0, 4.0)]
Line 101: Because Polygon is an ordinary function, you can evaluate it at the REPL:
Line 102: *TypeSynonyms> Polygon 3
Line 103: Vect 3 (Double, Double) : Type
Line 104: Listing 6.1
Line 105: Defining a polygon using type synonyms (TypeSynonym.idr)
Line 106: A type synonym for describing 
Line 107: positions as (x, y) coordinates
Line 108: A type synonym for describing 
Line 109: polygons with n corners
Line 110: 
Line 111: --- 페이지 176 ---
Line 112: 150
Line 113: CHAPTER 6
Line 114: Programming with first-class types
Line 115: Also, notice that if you evaluate tri at the REPL, Idris will display tri’s type in the eval-
Line 116: uated form. In other words, evaluation at the REPL evaluates both the expression and
Line 117: the type:
Line 118: *TypeSynonyms> tri
Line 119: [(0.0, 0.0), (3.0, 0.0), (0.0, 4.0)] : Vect 3 (Double, Double)
Line 120: Using :t, on the other hand, displays tri’s type:
Line 121: *TypeSynonyms> :t tri
Line 122: Polygon 3
Line 123: Finally, you can see what happens when you try to define tri interactively using
Line 124: expression search in Atom. Enter the following into an Atom buffer, along with the
Line 125: previous definition of Polygon:
Line 126: tri : Polygon 3
Line 127: tri = ?tri_rhs
Line 128: The interactive editing tools in general, and expression search in particular, are aware
Line 129: of how type synonyms are defined, so if you try an expression search on tri_rhs, you’ll
Line 130: get the same result as if the type were written directly as Vect 3 (Double, Double):
Line 131: tri : Polygon 3
Line 132: tri = [(?tri_rhs1, ?tri_rhs2), (?tri_rhs3, ?tri_rhs4),
Line 133:        (?tri_rhs5, ?tri_rhs6)]
Line 134: The type synonyms defined in this section, Position and Polygon, are really just ordi-
Line 135: nary functions that happen to be used to compute types. This gives you a lot of flexi-
Line 136: bility in how you describe types, as you’ll see in the rest of this chapter. 
Line 137: 6.1.2
Line 138: Type-level functions with pattern matching
Line 139: Type synonyms are a special case of type-level functions, which are functions that can be
Line 140: used anywhere Idris is expecting a Type. There isn’t anything special about type-level
Line 141: functions as far as Idris is concerned; they’re ordinary functions that happen to return
Line 142: a Type, and they can use all of the language constructs available elsewhere. Neverthe-
Line 143: less, it’s useful to consider them separately, to see how they work in practice.
Line 144:  Because type-level functions are ordinary functions that return a type, you can
Line 145: write them by case splitting. For example, the following listing shows a function that
Line 146: calculates a type from a Boolean input. You saw this function in chapter 1, although in
Line 147: a slightly different form.
Line 148: StringOrInt : Bool -> Type
Line 149: StringOrInt False = String
Line 150: StringOrInt True = Int
Line 151: Listing 6.2
Line 152: A function that calculates a type from a Bool (TypeFuns.idr)
Line 153: 
Line 154: --- 페이지 177 ---
Line 155: 151
Line 156: Type-level functions: calculating types
Line 157: Using this, you can write a function where the return type is calculated from or depends
Line 158: on an input. Using StringOrInt, you can write functions that return either type,
Line 159: depending on a Boolean flag.
Line 160:  As a small example, you can write a function that takes a Boolean input and
Line 161: returns the string "Ninety four" if it’s False, or the integer 94 if it’s True. Begin with
Line 162: the type:
Line 163: 1
Line 164: Type—Begin by giving a type declaration, using StringOrInt: 
Line 165: getStringOrInt : (isInt : Bool) -> StringOrInt isInt
Line 166: getStringOrInt isInt = ?getStringOrInt_rhs
Line 167: If you look at the type of getStringOrInt_rhs now, you’ll see this: 
Line 168: isInt : Bool
Line 169: --------------------------------------
Line 170: getStringOrInt_rhs : StringOrInt isInt
Line 171:  2
Line 172: Define—Because isInt appears in the required type for getStringOrInt_rhs,
Line 173: case splitting on isInt will cause the expected return type to change according
Line 174: to the specific value of isInt for each case. Case splitting on isInt leads to this: 
Line 175: getStringOrInt : (isInt : Bool) -> StringOrInt isInt
Line 176: getStringOrInt False = ?getStringOrInt_rhs_1
Line 177: getStringOrInt True = ?getStringOrInt_rhs_2
Line 178:  3
Line 179: Type—Looking at the types of the newly created holes, you can see how the
Line 180: expected type is changed in each case: 
Line 181: --------------------------------------
Line 182: getStringOrInt_rhs_1 : String
Line 183: --------------------------------------
Line 184: getStringOrInt_rhs_2 : Int
Line 185: In getStringOrInt_rhs_1, the type is refined to StringOrInt False because
Line 186: the pattern for isInt is False, which evaluates to String. Then, in getString-
Line 187: OrInt_rhs_2, the type is refined to StringOrInt True, which evaluates to Int.
Line 188: 4
Line 189: Refine—To complete the definition, you need to provide values of different
Line 190: types in each case: 
Line 191: getStringOrInt : (isInt : Bool) -> StringOrInt isInt
Line 192: getStringOrInt False = "Ninety four"
Line 193: getStringOrInt True = 94
Line 194: DEPENDENT PATTERN MATCHING
Line 195: The getStringOrInt example illustrates a
Line 196: technique that’s often useful when programming with dependent types:
Line 197: dependent pattern matching. This refers to a situation where the type of one
Line 198: argument to a function can be determined by inspecting the value of (that is,
Line 199: by case splitting) another. You’ve already seen an example of this when defin-
Line 200: ing zip in chapter 4, where the form of one vector restricted the valid forms
Line 201: of the other, and you’ll see a lot more.
Line 202: 
Line 203: --- 페이지 178 ---
Line 204: 152
Line 205: CHAPTER 6
Line 206: Programming with first-class types
Line 207: Type-level functions can be used anywhere a Type is expected, meaning that they can
Line 208: be used in place of argument types too. For example, you can write a function that
Line 209: converts either a String or an Int to a canonical String representation, according to
Line 210: a Boolean flag. This function will behave as follows: 
Line 211: If the input is a String, it returns the String with leading and trailing space
Line 212: removed using trim.
Line 213: If the input is an Int, it converts the input to a String using cast.
Line 214: DOCUMENTATION
Line 215: Remember that you can use :t and :doc to check the
Line 216: types of functions that are unfamiliar (such as trim) at the REPL.
Line 217: You can define this function with the following steps: 
Line 218: 1
Line 219: Type—Begin by writing a type for valToString, again using StringOrInt, but
Line 220: this time to calculate the input type: 
Line 221: valToString : (isInt : Bool) -> StringOrInt isInt -> String
Line 222: valToString isInt y = ?valToString_rhs
Line 223: Inspecting the type of valToString_rhs, you’ll see the following: 
Line 224: isInt : Bool
Line 225: y : StringOrInt isInt
Line 226: --------------------------------------
Line 227: valToString_rhs : String
Line 228:  2
Line 229: Define—You can define this by case splitting on isInt. The type of y is calcu-
Line 230: lated from isInt, so if you case-split on isInt, you should see refined types for
Line 231: y in each resulting case: 
Line 232: valToString : (isInt : Bool) -> StringOrInt isInt -> String
Line 233: valToString False y = ?valToString_rhs_1
Line 234: valToString True y = ?valToString_rhs_2
Line 235:  3
Line 236: Type—Inspecting the types of valToString_rhs_1 and valToString_rhs_2
Line 237: shows how the type of y is refined in each case: 
Line 238: y : String
Line 239: --------------------------------------
Line 240: valToString_rhs_1 : String
Line 241: y : Int
Line 242: --------------------------------------
Line 243: valToString_rhs_2 : String
Line 244: 4
Line 245: Refine—To complete the definition, fill in the right side to convert y to a
Line 246: trimmed String if it was a String, or a string representation of the number if it
Line 247: was an Int: 
Line 248: valToString : (isInt : Bool) -> StringOrInt isInt -> String
Line 249: valToString False y = trim y
Line 250: valToString True y = cast y
Line 251: 
Line 252: --- 페이지 179 ---
Line 253: 153
Line 254: Type-level functions: calculating types
Line 255: The simple examples in this section, getStringOrInt and valToString, illustrate a
Line 256: technique that can be used more widely in practice. You’ll see some more practical
Line 257: examples later in this chapter: using a format string to calculate a type for formatted
Line 258: output, and a larger example allowing users to calculate a schema, extending the data
Line 259: store you saw in chapter 4.
Line 260:  There’s more that you can achieve with type-level expressions, however. The fact
Line 261: that types are first-class means not only that types can be computed like any other
Line 262: value, but also that any expression form can appear in types. 
Line 263: 6.1.3
Line 264: Using case expressions in types
Line 265: Any expression that can be used in a function can also be used at the type level, and
Line 266: vice versa. For example, you can leave holes in types while your understanding of a
Line 267: function’s requirements develops, or you can use more-complex expression forms
Line 268: such as case. Let’s briefly take a look at how this can work by using a case expression
Line 269: in the type of valToString instead of a separate StringOrInt function:
Line 270: 1
Line 271: Type—Start by giving a type for valToString, but because you don’t immedi-
Line 272: ately know the input type, you can leave a hole: 
Line 273: valToString : (isInt : Bool) -> ?argType -> String
Line 274:  2
Line 275: Define—Even though you have an incomplete type, you can still proceed with
Line 276: the definition by case splitting on isInt, because you at least know that isInt is
Line 277: a Bool: 
Line 278: valToString : (isInt : Bool) -> ?argType -> String
Line 279: valToString False y = ?valToString_rhs_1
Line 280: valToString True y = ?valToString_rhs_2
Line 281:  3
Line 282: Type—Inspecting the types of valToString_rhs_1 and valToString_rhs_2 will,
Line 283: however, reveal that you don’t know the type of y yet: 
Line 284: y : ?argType
Line 285: --------------------------------------
Line 286: valToString_rhs_1 : String
Line 287:  4
Line 288: Refine—At this stage, you need to refine the type with more details of ?argType.
Line 289: You can fill in ?argType with a case expression: 
Line 290: valToString : (isInt : Bool) -> (case _ of
Line 291: case_val => ?argType) -> String
Line 292: valToString False y = ?valToString_rhs_1
Line 293: valToString True y = ?valToString_rhs_2
Line 294:  5
Line 295: Refine—Remember that when Idris generates a case expression, it leaves an
Line 296: underscore in place of the value the case expression will branch on. You’ll
Line 297: need to fill this in before the program will compile. You can compute the argu-
Line 298: ment type from the input isInt: 
Line 299: valToString : (isInt : Bool) -> (case isInt of
Line 300: case_val => ?argType) -> String
Line 301: 
Line 302: --- 페이지 180 ---
Line 303: 154
Line 304: CHAPTER 6
Line 305: Programming with first-class types
Line 306: valToString False y = ?valToString_rhs_1
Line 307: valToString True y = ?valToString_rhs_2
Line 308:  6
Line 309: Refine—Case splitting on case_val gives you the two possible values isInt can
Line 310: take: 
Line 311: valToString : (isInt : Bool) -> (case isInt of
Line 312: False => ?argType_1
Line 313: True => ?argType_2) -> String
Line 314: valToString False y = ?valToString_rhs_1
Line 315: valToString True y = ?valToString_rhs_2
Line 316: You can then complete the type in the same way as your implementation of
Line 317: StringOrInt, refining ?argType_1 with String and ?argType_2 with Int: 
Line 318: valToString : (isInt : Bool) -> (case isInt of
Line 319: False => String
Line 320: True => Int) -> String
Line 321: valToString False y = ?valToString_rhs_1
Line 322: valToString True y = ?valToString_rhs_2
Line 323:  7
Line 324: Type—Inspecting ?valToString_rhs_1 and ?valToString_rhs2 now will show
Line 325: you the new types for the input y, calculated from the first argument: 
Line 326: y : String
Line 327: --------------------------------------
Line 328: valToString_rhs_1 : String
Line 329: y : Int
Line 330: --------------------------------------
Line 331: valToString_rhs_2 : String
Line 332: 8
Line 333: Refine—Finally, now that you know the type of the input y in each case, you can
Line 334: complete the definition as before: 
Line 335: valToString : (isInt : Bool) -> (case isInt of
Line 336: False => String
Line 337: True => Int) -> String
Line 338: valToString False y = trim y
Line 339: valToString True y = cast y
Line 340: Totality and type-level functions
Line 341: In general, it’s best to consider type-level functions in exactly the same way as ordi-
Line 342: nary functions, as we’ve done so far. This isn’t always the case, though. There are a
Line 343: couple of technical differences that are useful to know about: 
Line 344: Type-level functions exist at compile time only. There’s no runtime representa-
Line 345: tion of Type, and no way to inspect a Type directly, such as pattern matching. 
Line 346: Only functions that are total will be evaluated at the type level. A function that
Line 347: isn’t total may not terminate, or may not cover all possible inputs. Therefore,
Line 348: to ensure that type-checking itself terminates, functions that are not total are
Line 349: treated as constants at the type level, and don’t evaluate further.  
Line 350: 
Line 351: --- 페이지 181 ---
Line 352: 155
Line 353: Defining functions with variable numbers of arguments
Line 354: 6.2
Line 355: Defining functions with variable numbers of arguments
Line 356: You can use type-level functions to calculate types based on some other known input.
Line 357: Given that function types are themselves types, this means that you can write functions
Line 358: with a different number of arguments depending on some other input. This is similar
Line 359: to some other languages that support variable-length argument lists, but with addi-
Line 360: tional precision in the type because you use the value of one argument to compute the
Line 361: types of the others.
Line 362:  In this section, we’ll see a couple of examples of how this can work: 
Line 363: As an introductory example, we’ll write a function that adds a sequence of num-
Line 364: bers, where the first argument is a number used to calculate the type of a func-
Line 365: tion that takes that many inputs.
Line 366: We’ll use the same technique to write a variant of the printf function that pro-
Line 367: duces a formatted output String using a format specifier in its first argument to
Line 368: describe the form of later arguments.
Line 369: 6.2.1
Line 370: An addition function
Line 371: First, we’ll define an addition function that adds
Line 372: together a sequence of numbers given directly as
Line 373: function arguments. Its behavior is characterized by
Line 374: the three examples shown in figure 6.1. An expres-
Line 375: sion of the form adder numargs val calculates a
Line 376: function that takes numargs additional arguments,
Line 377: which are added to an initial value val.
Line 378:  As usual in type-driven development, you’ll
Line 379: begin writing adder by writing its type, but in this
Line 380: case the type is not something you can construct
Line 381: directly; the type of adder is different depending on
Line 382: the value of the first argument. For the examples
Line 383: shown in figure 6.1, you’re looking for the following
Line 384: types:
Line 385: adder 0 : Int -> Int
Line 386: adder 1 : Int -> Int -> Int
Line 387: adder 2 : Int -> Int -> Int -> Int
Line 388: ...
Line 389: Because types are first-class, and this type differs depending on some value, you’ll be
Line 390: able to compute it using a type-level function. You can write an AdderType function
Line 391: with the required behavior. The name AdderType follows the convention that type-
Line 392: level functions are given names with an initial capital letter, and it indicates that it’s
Line 393: used to compute the type of adder.
Line 394: Additional
Line 395: arguments
Line 396: Number of additional
Line 397: arguments
Line 398: 0 10       = 10
Line 399: 1 10 15    = 25
Line 400: 2 10 15 20 = 45
Line 401: adder
Line 402: adder
Line 403: adder
Line 404: Initial value
Line 405: Figure 6.1
Line 406: Behavior of an addition 
Line 407: function with a variable number of 
Line 408: arguments
Line 409: 
Line 410: --- 페이지 182 ---
Line 411: 156
Line 412: CHAPTER 6
Line 413: Programming with first-class types
Line 414:  You can use a Nat to give the length of the argument list, both because you can
Line 415: case-split on it conveniently, and because it would be meaningless to have a negative
Line 416: length argument list. The following listing gives the definition of AdderType.
Line 417: AdderType : (numargs : Nat) -> Type
Line 418: AdderType Z = Int
Line 419: AdderType (S k) = (next : Int) -> AdderType k
Line 420: The type of adder can now be computed by passing its first argument to AdderType.
Line 421: The second argument is the initial value, which we’ll call acc as an abbreviation for
Line 422: “accumulator”:
Line 423: adder : (numargs : Nat) -> (acc : Int) -> AdderType numargs
Line 424: Because you calculate the type by case splitting on numargs in AdderType, you can
Line 425: write the definition of adder with a corresponding structure by case splitting on
Line 426: numargs, so that AdderType will be refined for each case. You can implement it with
Line 427: the following steps:
Line 428: 1
Line 429: Define—Add a skeleton definition, and then case-split on the first argument: 
Line 430: adder : (numargs : Nat) -> (acc : Int) -> AdderType numargs
Line 431: adder Z acc = ?adder_rhs_1
Line 432: adder (S k) acc = ?adder_rhs_2
Line 433:  2
Line 434: Refine—Where the number of additional arguments, numargs, is Z, return the
Line 435: accumulator directly: 
Line 436: adder : (numargs : Nat) -> (acc : Int) -> AdderType numargs
Line 437: adder Z acc = acc
Line 438: adder (S k) acc = ?adder_rhs_2
Line 439:  3
Line 440: Type—For adder_rhs_2, inspecting the type of the hole shows that you need to
Line 441: provide a function: 
Line 442: k : Nat
Line 443: acc : Int
Line 444: --------------------------------------
Line 445: adder_rhs_2 : Int -> AdderType k
Line 446: This is a function type because in AdderType when numargs matches a nonzero
Line 447: Nat, the expected type is a function type.
Line 448: 4
Line 449: Refine—The only way you have of producing something of type AdderType k in
Line 450: general is by calling adder with k as the first argument, so this type hints that
Line 451: you need to make a recursive call to adder. This is the complete definition: 
Line 452: Listing 6.3
Line 453: A function to calculate a type for adder n (Adder.idr)
Line 454: No further 
Line 455: function arguments
Line 456: Returns a function that takes a single integer
Line 457: and constructs the rest of the adder type,
Line 458: which takes k further arguments
Line 459: 
Line 460: --- 페이지 183 ---
Line 461: 157
Line 462: Defining functions with variable numbers of arguments
Line 463: adder : (numargs : Nat) -> (acc : Int) -> AdderType numargs
Line 464: adder Z acc = acc
Line 465: adder (S k) acc = \next => adder k (next + acc)
Line 466: Now that you have a complete and working definition, it’s a good idea to think about
Line 467: how you might refine either the type or the definition itself. For example, adder could
Line 468: be made generic in the type of numbers it adds.
Line 469:  Listing 6.4 shows a slightly refined version of the adder function that works with
Line 470: any numeric type, not just Int. It does this by passing an additional Type argument to
Line 471: AdderType, and then constraining that to numeric types in the type of adder.
Line 472: AdderType : (numargs : Nat) -> Type -> Type
Line 473: AdderType Z numType = numType
Line 474: AdderType (S k) numType = (next : numType) -> AdderType k numType
Line 475: adder : Num numType =>
Line 476: (numargs : Nat) -> numType -> AdderType numargs numType
Line 477: adder Z acc = acc
Line 478: adder (S k) acc = \next => adder k (next + acc)
Line 479: The adder function illustrates the basic pattern for defining functions with variable
Line 480: numbers of arguments: you’ve written an AdderType function to calculate the desired
Line 481: type of adder, given one of adder’s inputs. The pattern can also be applied for larger
Line 482: definitions, as you’ll now see when we define a function for formatting output. 
Line 483: 6.2.2
Line 484: Formatted output: a type-safe printf function
Line 485: A larger example of a function with a variable number of arguments is printf, found
Line 486: in C and some other languages. It produces formatted output given a format string
Line 487: and a variable number of arguments, as determined by the format string. The format
Line 488: string essentially gives a template string to be output, populated by the remaining
Line 489: arguments. In essence, printf has the same overall structure as adder, using the for-
Line 490: mat string to calculate the types of the later arguments.
Line 491:  Figure 6.2 shows some examples that characterize the printf behavior. Note that
Line 492: rather than producing output to the console, our version of printf returns a String.
Line 493: Listing 6.4
Line 494: A generic adder that works for any numeric type (Adder.idr)
Line 495: The Type here is the type of 
Line 496: arguments you’ll be adding together.
Line 497: Constrains the types you can add to
Line 498: numeric types, using Num numType and
Line 499: then passing numType to AdderType
Line 500: Additional
Line 501: arguments
Line 502: Format string describing
Line 503: additional arguments
Line 504: "Hello!"                 = "Hello!"
Line 505: "Answer : %d"  42        = "Answer : 42"
Line 506: "%s number %d" "Page" 94 = "Page number 94"
Line 507: printf
Line 508: printf
Line 509: printf
Line 510: Figure 6.2
Line 511: Behavior of a printf 
Line 512: function with different format strings
Line 513: 
Line 514: --- 페이지 184 ---
Line 515: 158
Line 516: CHAPTER 6
Line 517: Programming with first-class types
Line 518: In these format strings, the directive %d stands for an Int; %s stands for a String; and
Line 519: anything else is printed literally.
Line 520:  Following our usual process of type, define, refine, we’ll begin by thinking about a
Line 521: type for printf. As with adder, we’ll start with the types of the characteristic examples
Line 522: and then work out how to write a function that computes these types. These are the
Line 523: types of the examples in figure 6.2:
Line 524: printf "Hello!" : String
Line 525: printf "Answer: %d" : Int -> String
Line 526: printf "%s number %d" : String -> Int -> String
Line 527: FORMAT STRINGS
Line 528: In a full implementation of printf as provided by C,
Line 529: there are far more directives available than %d and %s. Furthermore, the
Line 530: directives can be modified in various ways to indicate further how the output
Line 531: should be formatted (such as leading zeroes in a number). Such details
Line 532: don’t add anything to this discussion of type-level functions, however, so we’ll
Line 533: omit them here.
Line 534: To get the type of printf, you’ll need to use the format string to build the expected
Line 535: types of the arguments. Instead of processing the string directly, you can write a data
Line 536: type describing the possible formats, as follows.
Line 537: data Format = Number Format
Line 538: | Str Format
Line 539: | Lit String Format
Line 540: | End
Line 541: This gives a clean separation between the parsing of the format string and the process-
Line 542: ing, much as we did when parsing the commands to the data store in chapter 4. For
Line 543: example, Str (Lit " = " (Number End)) would represent the format string "%s = %d",
Line 544: as illustrated in figure 6.3.
Line 545: Listing 6.5
Line 546: Representing format strings as a data type (Printf.idr)
Line 547: This represents %d, followed by the 
Line 548: rest of the format specifier.
Line 549: This represents %s, followed by 
Line 550: the rest of the format specifier.
Line 551: A literal string,
Line 552: followed by the rest of
Line 553: the format specifier
Line 554: An empty format specifier
Line 555: Marks the
Line 556: end of string
Line 557: "%s = %d"
Line 558: Str (Lit " = " (Number End))
Line 559: Figure 6.3
Line 560: Translating a format string 
Line 561: to a Format description
Line 562: 
Line 563: --- 페이지 185 ---
Line 564: 159
Line 565: Defining functions with variable numbers of arguments
Line 566:  
Line 567: For the moment, we’ll work directly with Format; we’ll define a conversion from
Line 568: String to Format later. The following listing shows how you can compute the type of
Line 569: printf from a Format specifier.
Line 570: PrintfType : Format -> Type
Line 571: PrintfType (Number fmt) = (i : Int) -> PrintfType fmt
Line 572: PrintfType (Str fmt) = (str : String) -> PrintfType fmt
Line 573: PrintfType (Lit str fmt) = PrintfType fmt
Line 574: PrintfType End = String
Line 575: Listing 6.7 defines a helper function for building a String from a Format, along with
Line 576: any necessary additional arguments as calculated by PrintfType. This works like
Line 577: adder, using an accumulator to build the result.
Line 578: printfFmt : (fmt : Format) -> (acc : String) -> PrintfType fmt
Line 579: printfFmt (Number fmt) acc = \i => printfFmt fmt (acc ++ show i)
Line 580: printfFmt (Str fmt) acc = \str => printfFmt fmt (acc ++ str)
Line 581: printfFmt (Lit lit fmt) acc = printfFmt fmt (acc ++ lit)
Line 582: printfFmt End acc = acc
Line 583: Listing 6.6
Line 584: Calculating the type of printf from a Format specifier 
Line 585: (extending Printf.idr)
Line 586: Listing 6.7
Line 587: Helper function for printf, building a String from a Format specifier
Line 588: (Printf.idr)
Line 589: Intermediate types
Line 590: In the type-driven development process, we often think about functions in terms of
Line 591: transformations between data types. As such, we often define intermediate types,
Line 592: such as Format in this section, to describe intermediate stages of a computation.
Line 593: There are two main reasons for doing this: 
Line 594: The meaning of String is not obvious from the type alone. The function type
Line 595: Format -> Type has a more precise meaning than the function type String
Line 596: -> Type because it’s clear that the input must be a format specification
Line 597: rather than any String.
Line 598: Defining an intermediate data type gives us access to more interactive edit-
Line 599: ing features, particularly case splitting.
Line 600: The Number directive means that your printf 
Line 601: function will need another Int argument.
Line 602: The Str directive means that your printf
Line 603: function will need another String argument.
Line 604: No additional argument is needed here 
Line 605: because you have a literal string. You can 
Line 606: calculate the type from the rest of the Format.
Line 607: This gives the return type of printf.
Line 608: The String is an
Line 609: accumulator, in
Line 610: which you build
Line 611: the String to be
Line 612: returned.
Line 613: At the end, there are no further 
Line 614: arguments to read and no further literal 
Line 615: inputs, so return the accumulator.
Line 616: PrintfType calculates a function 
Line 617: type from Number fmt, so you 
Line 618: need to build a function here.
Line 619: 
Line 620: --- 페이지 186 ---
Line 621: 160
Line 622: CHAPTER 6
Line 623: Programming with first-class types
Line 624: REMEMBER INTERACTIVE EDITING!
Line 625: For examples such as those in listings 6.6
Line 626: and 6.7, don’t just type them in directly. Instead, use the interactive editing
Line 627: tools in Atom to try to reconstruct them yourself. While doing so, make sure
Line 628: you take a look at the types of any holes, and see how far expression search
Line 629: can take you.
Line 630: Finally, to implement a printf that takes a String as a format specifier rather than a
Line 631: Format structure, you’ll need to be able to convert a String into a Format. The follow-
Line 632: ing listing defines the top-level printf function that does this conversion.
Line 633: toFormat : (xs : List Char) -> Format
Line 634: toFormat [] = End
Line 635: toFormat ('%' :: 'd' :: chars) = Number (toFormat chars)
Line 636: toFormat ('%' :: 's' :: chars) = Str (toFormat chars)
Line 637: toFormat ('%' :: chars) = Lit "%" (toFormat chars)
Line 638: toFormat (c :: chars) = case toFormat chars of
Line 639: Lit lit chars' => Lit (strCons c lit) chars'
Line 640: fmt => Lit (strCons c "") fmt
Line 641: printf : (fmt : String) -> PrintfType (toFormat (unpack fmt))
Line 642: printf fmt = printfFmt _ ""
Line 643: Exercises
Line 644: 1
Line 645: An n x m matrix can be represented by nested vectors of Double. Define a type syn-
Line 646: onym: Matrix : Nat -> Nat -> Type.
Line 647: You should be able to use it to define the following matrix: 
Line 648: testMatrix : Matrix 2 3
Line 649: testMatrix = [[0, 0, 0], [0, 0, 0]]
Line 650:  2
Line 651: Extend printf to support formatting directives for Char and Double.
Line 652: You can test your answer at the REPL as follows: 
Line 653: *ex_6_2> :t printf "%c %f"
Line 654: printf "%c %f" : Char -> Double -> String
Line 655: *ex_6_2> printf "%c %f" 'X' 24
Line 656: "'X' 24.0" : String
Line 657:  3
Line 658: You could implement a vector as nested pairs, with the nesting calculated from the
Line 659: length, as in this example: 
Line 660: TupleVect 0 ty = ()
Line 661: TupleVect 1 ty = (ty, ())
Line 662: TupleVect 2 ty = (ty, (ty, ()))
Line 663: ...
Line 664: Listing 6.8
Line 665: Top-level definition of printf, with a conversion from String to Format
Line 666: (Printf.idr)
Line 667: Use List Char rather than String here so that 
Line 668: you can easily match on individual characters.
Line 669: strCons builds a String from an initial
Line 670: character and the rest of the string.
Line 671: Use an underscore (_) for the format, 
Line 672: because Idris can infer from the type 
Line 673: that it must be toFormat (unpack fmt).
Line 674: 
Line 675: --- 페이지 187 ---
Line 676: 161
Line 677: Enhancing the interactive data store with schemas
Line 678: Define a type-level function, TupleVect, that implements this behavior. Remember
Line 679: to start with the type of TupleVect.
Line 680: When you have the correct answer, the following definition will be valid: 
Line 681: test : TupleVect 4 Nat
Line 682: test = (1,2,3,4,())
Line 683: 6.3
Line 684: Enhancing the interactive data store with schemas
Line 685: In the interactive data store we developed in chapter 4, you were able to add Strings
Line 686: to an in-memory store and retrieve them by index. But what if you want to store more-
Line 687: complex data? And what if you’d like the form of the data to be determined by the
Line 688: user before entering any data, rather than by hardcoding it in the program itself?
Line 689:  In the rest of this chapter, we’ll extend the data store by adding schemas to describe
Line 690: the form of the data. We’ll determine the schema by user input, and we’ll use type-level
Line 691: functions to compute the correct type for the data. Figure 6.4 shows two different data
Line 692: stores, with different schemas, that we’ll be able to represent with our extended system.
Line 693: Schema 1, at the top, shows a store that requires the data to be of type (Int, String),
Line 694: and schema 2, below, shows a store that requires the data to be of type (String,
Line 695: String, Int). In contrast, in the data store developed in chapter 4, the schema was
Line 696: effectively always String.
Line 697: A typical interaction with the extended system might proceed as follows. Note that
Line 698: we’re describing the schema before entering any data.
Line 699: Command: schema String String Int
Line 700: OK
Line 701: Command: add "Rain Dogs" "Tom Waits" 1985
Line 702: ID 0
Line 703: Command: add "Fog on the Tyne" "Lindisfarne" 1971
Line 704: ID 1
Line 705: Command: get 1
Line 706: "Fog on the Tyne", "Lindisfarne", 1971
Line 707: Command: quit
Line 708: Schema 1: (Int, String)
Line 709: 0
Line 710: (11, "Armstrong, Aldrin and Collins")
Line 711: 1
Line 712: (17, "Cernan, Evans and Schmitt")
Line 713: 2
Line 714: (8, "Borman, Lovell and Anders")
Line 715: Schema 2: (String, String, Int)
Line 716: 0
Line 717: ("Rain Dogs", "Tom Waits", 1985)
Line 718: 1
Line 719: ("Fog on the Tyne", "Lindisfarne", 1971)
Line 720: 2
Line 721: ("Flood", "They Might Be Giants", 1990)
Line 722: Figure 6.4
Line 723: Two different data 
Line 724: stores, with different schemas. 
Line 725: Schema 1 requires the data to be 
Line 726: of type (Int, String), and 
Line 727: schema 2 requires the data to be 
Line 728: of type (String, String, Int)
Line 729: 
Line 730: --- 페이지 188 ---
Line 731: 162
Line 732: CHAPTER 6
Line 733: Programming with first-class types
Line 734: Rather than starting from scratch, we’ll begin with the existing data store we imple-
Line 735: mented in chapter 4 and refine the overall system as necessary. We’ll take this
Line 736: approach: 
Line 737: 1
Line 738: Refine the representation of DataStore to include schema descriptions. This
Line 739: refinement will inevitably mean that our program no longer type-checks.
Line 740:  2
Line 741: Correct any errors, introducing holes for any more-complex errors.
Line 742: 3
Line 743: Fill in the holes to complete the implementation, and add any further features
Line 744: that are now supported as a result of refining the type.
Line 745: 6.3.1
Line 746: Refining the DataStore type
Line 747: At the moment, the DataStore only supports storing Strings. We implemented it in
Line 748: chapter 4 using the following type:
Line 749: data DataStore : Type where
Line 750: MkData : (size : Nat) -> (items : Vect size String) -> DataStore
Line 751: Instead of using a Vect size String for the items in the store, we’d like to be flexible
Line 752: in the types of these items. One natural way to do this might be to refine this to a
Line 753: generic version of DataStore, parameterizing it over a schema that gives the type of
Line 754: data in the store:
Line 755: data DataStore : Type -> Type where
Line 756: MkData : (size : Nat) -> (items : Vect size schema) -> DataStore schema
Line 757: COMMENTING OUT CODE SECTIONS
Line 758: While you’re working on the refined
Line 759: DataStore, you’ll inevitably break the rest of the program, which will no lon-
Line 760: ger type-check. Therefore, I’d suggest commenting out the rest of the code
Line 761: (placing it between {- and -}) until you’ve finished the new DataStore type
Line 762: and you’re ready to move on.
Line 763: We want the user to be able to describe and possibly even update the schema, but if we
Line 764: parameterize over a schema type, the schema will be fixed in the type. Instead, we’ll
Line 765: create a data type for describing schemas, and a type-level function for translating
Line 766: schema descriptions (possibly given by a user at runtime) into concrete types. The fol-
Line 767: lowing listing shows an outline of a refined DataStore type.
Line 768: data Schema
Line 769: SchemaType : Schema -> Type
Line 770: data DataStore : Type where
Line 771: MkData : (schema : Schema) ->
Line 772: Listing 6.9
Line 773: Outline of the refined DataStore type, with the Schema description and
Line 774: the translation of Schema to concrete types left undefined (DataStore.idr)
Line 775: A data declaration without a body stands for a type 
Line 776: that hasn’t been defined yet, much like a hole 
Line 777: stands for a function that hasn’t been defined yet.
Line 778: Once you’ve defined Schema, you’ll 
Line 779: be able to fill in this hole to convert 
Line 780: a Schema to a concrete type.
Line 781: Store the schema description 
Line 782: itself in the data store.
Line 783: 
Line 784: --- 페이지 189 ---
Line 785: 163
Line 786: Enhancing the interactive data store with schemas
Line 787: (size : Nat) ->
Line 788: (items : Vect size (SchemaType schema)) ->
Line 789: DataStore
Line 790: We’ll define Schemas as being some combination of Strings and Ints, according to a
Line 791: definition given by the user. The user will provide a Schema, and we’ll translate the
Line 792: Schema to some concrete type using a type-level function, SchemaType.
Line 793:  The next listing shows how you can describe Schemas and convert them into Idris
Line 794: Types using a type-level function, SchemaType.
Line 795: infixr 5 .+.
Line 796: data Schema = SString
Line 797: | SInt
Line 798: | (.+.) Schema Schema
Line 799: SchemaType : Schema -> Type
Line 800: SchemaType SString = String
Line 801: SchemaType SInt = Int
Line 802: SchemaType (x .+. y) = (SchemaType x, SchemaType y)
Line 803: You can try this for defining schemas for the two example stores shown in figure 6.4
Line 804: earlier:
Line 805: *DataStore> SchemaType (SInt .+. SString)
Line 806: (Int, String) : Type
Line 807: *DataStore> SchemaType (SString .+. SString .+. SInt)
Line 808: (String, String, Int) : Type
Line 809: Listing 6.10
Line 810: Defining Schema, and converting a Schema to a concrete type
Line 811: Calculate the required 
Line 812: type of the items in the 
Line 813: store from the schema.
Line 814: Idris allows us to introduce new operators 
Line 815: (see the sidebar, “Declaring operators”).
Line 816: A schema
Line 817: containing
Line 818: a single
Line 819: String
Line 820: A schema containing a single Int
Line 821: A schema combining two smaller schemas
Line 822: A type-level function for converting 
Line 823: a Schema to a concrete type
Line 824: Declaring operators
Line 825: You can define new operators by giving their fixity and precedence. In listing 6.10 you
Line 826: had this:
Line 827: infixr 5 .+.
Line 828: This introduces a new right-associative infix operator (infixr) with precedence level
Line 829: 5. In general, operators are introduced with the keyword infixl (for left-associative
Line 830: operators), infixr (for right-associative operators) or infix (for non-associative
Line 831: operators), followed by a precedence level and a list of operators.
Line 832: Even the arithmetic and comparison operators are defined this way, rather than being
Line 833: built-in syntax. They’re introduced as follows in the Prelude:
Line 834: infixl 5 ==, /=
Line 835: infixl 6 <, <=, >, >=
Line 836: infixl 7 <<, >>
Line 837: 
Line 838: --- 페이지 190 ---
Line 839: 164
Line 840: CHAPTER 6
Line 841: Programming with first-class types
Line 842: The new DataStore type allows you to store not only the size and the contents of the
Line 843: store, but also a description of the structure of the contents of the store, as a schema.
Line 844: Previously, each entry was always a String, but now the form is determined by the user.
Line 845:  Now, because you’ve changed the definition of DataStore, you’ll also need to
Line 846: change the functions that access it. 
Line 847: 6.3.2
Line 848: Using a record for the DataStore
Line 849: In order to be able to use the updated DataStore type, you’ll need to redefine the
Line 850: functions size and items to project the relevant fields out of the structure.
Line 851:  The definition of size is similar to the previous definition:
Line 852: size : DataStore -> Nat
Line 853: size (MkData schema' size' items') = size'
Line 854: To define items, however, you’ll also need to write a function to project a schema out
Line 855: of the store, because you need to know the schema description in order to know the
Line 856: type of the items in the store.
Line 857: schema : DataStore -> Schema
Line 858: schema (MkData schema' size' items') = schema'
Line 859: items : (store : DataStore) -> Vect (size store) (SchemaType (schema store))
Line 860: items (MkData schema' size' items') = items'
Line 861: Writing projection functions like these, which essentially extract fields from records,
Line 862: can get tedious very quickly. Instead, Idris provides a notation for defining records,
Line 863: which leads to automatically generated functions for projecting fields from a record.
Line 864: You can define DataStore as follows.
Line 865: record DataStore where
Line 866: constructor MkData
Line 867: schema : Schema
Line 868: size : Nat
Line 869: items : Vect size (SchemaType schema)
Line 870: Listing 6.11
Line 871: Implementing DataStore as a record, with automatically generated 
Line 872: projection functions
Line 873: (continued)
Line 874: infixl 8 +, -
Line 875: infixl 9 *, /
Line 876: The :: and ++ operators on lists are also defined in the Prelude and are declared as
Line 877: follows:
Line 878: infixr 7 ::, ++
Line 879: Names the data constructor for DataStore
Line 880: Declares fields, which automatically 
Line 881: generate projection functions with 
Line 882: the same name
Line 883: 
Line 884: --- 페이지 191 ---
Line 885: 165
Line 886: Enhancing the interactive data store with schemas
Line 887: A record declaration introduces a new data type, much like a data declaration, but
Line 888: with two differences: 
Line 889: There can be only one constructor.
Line 890: The fields give rise to projection functions, automatically generated from the
Line 891: types of the fields.
Line 892: In the case of DataStore, you can see the types of the MkData data constructor and the
Line 893: projection functions generated from the fields by using :doc:
Line 894: *DataStore> :doc DataStore
Line 895: Record DataStore
Line 896: Constructor:
Line 897: MkData : (schema : Schema) ->
Line 898: (size : Nat) ->
Line 899: (items : Vect size (SchemaType schema)) -> DataStore
Line 900: Projections:
Line 901: schema : (rec : DataStore) -> Schema
Line 902: size : (rec : DataStore) -> Nat
Line 903: items : (rec : DataStore) ->
Line 904: Vect (size rec) (SchemaType (schema rec))
Line 905: You can try this by creating a simple test record at the REPL:
Line 906: *DataStore> :let teststore = (MkData (SString .+. SInt) 1 [("Answer", 42)])
Line 907: *DataStore> :t teststore
Line 908: teststore : DataStore
Line 909: Next, you can project the schema, the size, and the list of items from this test record:
Line 910: *DataStore> schema teststore
Line 911: SString .+. SInt : Schema
Line 912: *DataStore> size teststore
Line 913: 1 : Nat
Line 914: *DataStore> items teststore
Line 915: [("Answer", 42)] : Vect 1 (String, Int)
Line 916: Records are actually much more flexible than can be seen in this small example. As
Line 917: well as projecting out the values of fields, Idris provides a syntax for setting fields and
Line 918: updating records. You’ll learn more about records when we discuss working with state
Line 919: in chapter 12. 
Line 920: 6.3.3
Line 921: Correcting compilation errors using holes
Line 922: Now that you have a new definition of DataStore, your old program that uses it will no
Line 923: longer type-check because it relies on the old definition. The next step in refining
Line 924: your data store program, then, is to update the definitions so that the whole program
Line 925: 
Line 926: --- 페이지 192 ---
Line 927: 166
Line 928: CHAPTER 6
Line 929: Programming with first-class types
Line 930: type-checks again. This doesn’t necessarily mean completing the program; at this
Line 931: stage, it’s fine to resolve type errors by inserting holes that you’ll fill in later.
Line 932:  Earlier, I suggested temporarily commenting out the code after the definition of
Line 933: DataStore so that you could work on the refined definition without worrying about
Line 934: compilation errors. Now, we’ll work through the remainder of the program, uncom-
Line 935: menting definitions bit by bit and repairing them, guided by the type errors Idris
Line 936: gives us.
Line 937:  First, let’s uncomment addToStore, defined previously as follows:
Line 938: addToStore : DataStore -> String -> DataStore
Line 939: addToStore (MkData size store) newitem = MkData _ (addToData store)
Line 940: where
Line 941: addToData : Vect oldsize String -> Vect (S oldsize) String
Line 942: addToData [] = [newitem]
Line 943: addToData (item :: items) = item :: addToData items
Line 944: On reloading, either by using Ctrl-Alt-R in Atom or the :r command at the REPL, Idris
Line 945: reports as follows:
Line 946: DataStore.idr:21:1-11:
Line 947: When checking left hand side of addToStore:
Line 948: When checking an application of Main.addToStore:
Line 949: Type mismatch between
Line 950: Vect size (SchemaType schema) ->
Line 951: DataStore (Type of MkData schema size)
Line 952: and
Line 953: DataStore (Expected type)
Line 954: The first problem here is that you’ve added an argument to MkData; it now requires a
Line 955: schema as well as a size and a vector of items. You can correct this by adding a schema
Line 956: argument to MkData:
Line 957: addToStore : DataStore -> String -> DataStore
Line 958: addToStore (MkData schema size store) newitem
Line 959: = MkData schema _ (addToData store)
Line 960: where
Line 961: addToData : Vect oldsize String -> Vect (S oldsize) String
Line 962: addToData [] = [newitem]
Line 963: addToData (item :: items) = item :: addToData items
Line 964: Idris now reports
Line 965: Type mismatch between
Line 966: Vect size (SchemaType schema) (Type of store)
Line 967: and
Line 968: Vect size String (Expected type)
Line 969: The problem is that the data store no longer stores merely Strings, but stores a type
Line 970: described by the schema. You can correct this by changing the types of addToStore
Line 971: and addToData so that they work with the correct type. A type-correct definition of
Line 972: addToStore is shown in the following listing.
Line 973: 
Line 974: --- 페이지 193 ---
Line 975: 167
Line 976: Enhancing the interactive data store with schemas
Line 977:  
Line 978: addToStore : (store : DataStore) -> SchemaType (schema store) -> DataStore
Line 979: addToStore (MkData schema size store) newitem
Line 980: = MkData schema _ (addToData store)
Line 981: where
Line 982: addToData : Vect oldsize (SchemaType schema) ->
Line 983: Vect (S oldsize) (SchemaType schema)
Line 984: addToData [] = [newitem]
Line 985: addToData (item :: items) = item :: addToData items
Line 986: If you continue uncommenting definitions one at a time, the next error you’ll
Line 987: encounter is in getEntry. It’s currently defined as follows, with the erroneous line
Line 988: marked.
Line 989: getEntry : (pos : Integer) -> (store : DataStore) ->
Line 990: Maybe (String, DataStore)
Line 991: getEntry pos store
Line 992: = let store_items = items store in
Line 993: case integerToFin pos (size store) of
Line 994: Nothing => Just ("Out of range\n", store)
Line 995: Just id => Just (index id (items store)
Line 996:                              ++ "\n", store)
Line 997: The problem is in the last line, where you extract an item from the store, because
Line 998: you’re treating the store as a Vect containing Strings. Here’s what Idris reports: 
Line 999: When checking an application of function Data.Vect.index:
Line 1000: Type mismatch between
Line 1001: Vect (size store)
Line 1002: (SchemaType (schema store)) (Type of items store)
Line 1003: and
Line 1004: Vect (size store) String (Expected type)
Line 1005: The problem is in the application of index, which no longer returns a String. You
Line 1006: can correct this error, temporarily, by inserting a hole to convert the result of index
Line 1007: into a String, as follows.
Line 1008: getEntry : (pos : Integer) -> (store : DataStore) ->
Line 1009: Maybe (String, DataStore)
Line 1010: getEntry pos store
Line 1011: = let store_items = items store in
Line 1012: case integerToFin pos (size store) of
Line 1013: Nothing => Just ("Out of range\n", store)
Line 1014: Just id => Just (?display (index id (items store)) ++ "\n",
Line 1015: store)
Line 1016: Listing 6.12
Line 1017: A corrected definition of addToStore using the refined DataStore type
Line 1018: Listing 6.13
Line 1019: Old version of getEntry, with an error in the application of index
Line 1020: Listing 6.14
Line 1021: Correcting getEntry by inserting a hole to convert the contents of the
Line 1022: store to a displayable String
Line 1023: Calculates the type of the item you’re
Line 1024: adding using SchemaType, from the
Line 1025: schema defined in the store
Line 1026: The name schema here 
Line 1027: refers to the name bound 
Line 1028: in the preceding clause
Line 1029: There’s an error in the 
Line 1030: application of index 
Line 1031: because the store no 
Line 1032: longer represents items as 
Line 1033: a Vect containing Strings.
Line 1034: The ?display hole, when filled in,
Line 1035: will be a function that converts
Line 1036: the result of index, which is a
Line 1037: SchemaType (schema store), into
Line 1038: a String that can be displayed.
Line 1039: 
Line 1040: --- 페이지 194 ---
Line 1041: 168
Line 1042: CHAPTER 6
Line 1043: Programming with first-class types
Line 1044: If you check the type of display, you’ll see the type of the function you need to fill in
Line 1045: the hole, converting a SchemaType (schema store) into a String:
Line 1046: store : DataStore
Line 1047: id : Fin (size store)
Line 1048: pos : Integer
Line 1049: store_items : Vect (size store) (SchemaType (schema store))
Line 1050: --------------------------------------
Line 1051: display : SchemaType (schema store) -> String
Line 1052: We’ll return to ?display shortly. For the moment, getEntry type-checks again. The
Line 1053: next error is in processInput. Here’s the current definition.
Line 1054: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1055: processInput store input
Line 1056: = case parse input of
Line 1057: Nothing => Just ("Invalid command\n", store)
Line 1058: Just (Add item) =>
Line 1059: Just ("ID " ++ show (size store) ++ "\n", addToStore store item)
Line 1060: Just (Get pos) => getEntry pos store
Line 1061: Just Quit => Nothing
Line 1062: This definition has an error similar to getEntry, showing that you have a String but
Line 1063: Idris expected a SchemaType (schema store):
Line 1064: When checking an application of function Main.addToStore:
Line 1065: Type mismatch between
Line 1066: String (Type of item)
Line 1067: and
Line 1068: SchemaType (schema store) (Expected type)
Line 1069: One possible fix is, as with getEntry, to add a hole for converting the String to an
Line 1070: appropriate SchemaType (schema store) in processInput:
Line 1071: Just ("ID " ++ show (size store) ++ "\n", addToStore store (?convert item))
Line 1072: Alternatively, you could refine the definition of Command so that it only represents valid
Line 1073: commands, meaning that any user input that’s invalid would lead to a parse error.
Line 1074: We’ll take this approach, because it involves defining a more precise intermediate
Line 1075: type, so you’ll check the validity of the input as early as possible.
Line 1076:  To achieve this, parameterize Command by the schema description, and change the
Line 1077: Add command so that it takes a SchemaType rather than the String input directly.
Line 1078: Here’s the refined definition of Command.
Line 1079: Listing 6.15
Line 1080: Old version of processInput, with an error in the application of 
Line 1081: addToStore
Line 1082: There’s an error in the application of addToStore 
Line 1083: here, because you’re passing it a String and it now 
Line 1084: expects an entry as described by the schema type.
Line 1085: 
Line 1086: --- 페이지 195 ---
Line 1087: 169
Line 1088: Enhancing the interactive data store with schemas
Line 1089:  
Line 1090: data Command : Schema -> Type where
Line 1091: Add : SchemaType schema -> Command schema
Line 1092: Get : Integer -> Command schema
Line 1093: Quit : Command schema
Line 1094: You can now change parse to take an explicit schema description, and add a hole
Line 1095: where necessary to convert String input to SchemaType schema. A new definition of
Line 1096: parse that type-checks is shown here.
Line 1097: parseCommand : (schema : Schema) -> String -> String -> Maybe (Command schema)
Line 1098: parseCommand schema "add" rest = Just (Add (?parseBySchema rest))
Line 1099: parseCommand schema "get" val = case all isDigit (unpack val) of
Line 1100: False => Nothing
Line 1101: True => Just (Get (cast val))
Line 1102: parseCommand schema "quit" "" = Just Quit
Line 1103: parseCommand _ _ _ = Nothing
Line 1104: parse : (schema : Schema) ->
Line 1105: (input : String) -> Maybe (Command schema)
Line 1106: parse schema input = case span (/= ' ') input of
Line 1107: (cmd, args) => parseCommand schema cmd (ltrim args)
Line 1108: The resulting hole has a type that explains that it converts a String to an appropriate
Line 1109: instance of the SchemaType schema:
Line 1110: schema : Schema
Line 1111: rest : String
Line 1112: --------------------------------------
Line 1113: parseBySchema : String -> SchemaType schema
Line 1114: There’s still a problem here, however! This function can’t be total because not every
Line 1115: String is going to be parsable as a valid instance of the schema. Nevertheless, your
Line 1116: goal at the moment is merely to make the overall program type-check again. We’ll
Line 1117: return to this problem shortly.
Line 1118:  You’ve refined the type of Command, added the schema argument to parse, and
Line 1119: inserted holes for displaying entries (?display) and converting user input into
Line 1120: entries (?parseBySchema). All that remains is to update processInput and main to
Line 1121: use the new definitions. These are minor changes, shown in the next listing. In
Line 1122: processInput, you pass the current schema to parse, and in main you set the initial
Line 1123: schema to simply accept Strings.
Line 1124: Listing 6.16
Line 1125: Command, refined to be parameterized by the schema in the data store
Line 1126: Listing 6.17
Line 1127: Updating parseCommand so that it parses inputs that conform to the
Line 1128: schema
Line 1129: Command is parameterized by the Schema 
Line 1130: description, which gives the form of 
Line 1131: entries that can be added to the store.
Line 1132: The type of Add now 
Line 1133: makes it explicit that only 
Line 1134: inputs that conform to 
Line 1135: the schema can be added.
Line 1136: Adds a hole for converting the
Line 1137: String input to the required
Line 1138: SchemaType schema
Line 1139: Adds an explicit schema argument that can be passed 
Line 1140: to parseCommand to tell it the form of valid inputs
Line 1141: 
Line 1142: --- 페이지 196 ---
Line 1143: 170
Line 1144: CHAPTER 6
Line 1145: Programming with first-class types
Line 1146:  
Line 1147: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1148: processInput store input
Line 1149: = case parse (schema store) input of
Line 1150: Nothing => Just ("Invalid command\n", store)
Line 1151: Just (Add item) =>
Line 1152: Just ("ID " ++ show (size store) ++ "\n", addToStore store item)
Line 1153: Just (Get pos) => getEntry pos store
Line 1154: Just Quit => Nothing
Line 1155: main : IO ()
Line 1156: main = replWith (MkData SString _ [])
Line 1157: "Command: " processInput
Line 1158: To recap, you’ve updated the DataStore type to allow user-defined schemas, defining
Line 1159: it using a record to get field access functions for free, and you’ve updated the remain-
Line 1160: der of the program so that it now type-checks, inserting holes temporarily for the parts
Line 1161: that are more difficult to correct immediately. 
Line 1162: 6.3.4
Line 1163: Displaying entries in the store
Line 1164: You now have two holes to fill in before you can execute this program. The first is
Line 1165: ?display, which converts an entry in the store into a String, where the schema in the
Line 1166: store gives the form of the data:
Line 1167: store : DataStore
Line 1168: id : Fin (size store)
Line 1169: pos : Integer
Line 1170: store_items : Vect (size store) (SchemaType (schema store))
Line 1171: --------------------------------------
Line 1172: display : SchemaType (schema store) -> String
Line 1173: In this case, using Ctrl-Alt-L to lift the hole to a top-level function gives you a lot of
Line 1174: information that you don’t need to implement display. All you really need is a
Line 1175: schema description and the data.
Line 1176:  Instead, you can implement display by hand as follows: 
Line 1177: 1
Line 1178: Type—First, you can write a more generic type than Idris suggested. Rather than
Line 1179: specifically using a schema extracted from a store, you can display data accord-
Line 1180: ing to any schema: 
Line 1181: display : SchemaType schema -> String
Line 1182:  2
Line 1183: Define—In order to define this function, you need to know about the schema
Line 1184: itself. Otherwise, you won’t know what form the data is in. Add a skeleton defi-
Line 1185: nition, and then bring the implicit argument schema into scope: 
Line 1186: display : SchemaType schema -> String
Line 1187: display {schema} item = ?display_rhs
Line 1188: Listing 6.18
Line 1189: Updated processInput and main, with a default schema
Line 1190: Adds an extra argument to parse so that it 
Line 1191: knows which schema to use to parse the data
Line 1192: Because item has type SchemaType (schema store)
Line 1193: here, it’s fine to call addToStore as before.
Line 1194: Sets the initial schema as SString, 
Line 1195: representing only Strings. We’ll 
Line 1196: add a way for users to set the 
Line 1197: schema shortly.
Line 1198: 
Line 1199: --- 페이지 197 ---
Line 1200: 171
Line 1201: Enhancing the interactive data store with schemas
Line 1202:  3
Line 1203: Define—You can define the function by case splitting on schema. Because the
Line 1204: type of item is SchemaType schema, case splitting on schema will give you more
Line 1205: information about the expected type of item: 
Line 1206: display : SchemaType schema -> String
Line 1207: display {schema = SString} item = ?display_rhs_1
Line 1208: display {schema = SInt} item = ?display_rhs_2
Line 1209: display {schema = (x .+. y)} item = ?display_rhs_3
Line 1210:  4
Line 1211: Type—Inspecting each of the resulting holes (?display_rhs_1, ?display_
Line 1212: rhs_2 and ?display_rhs_3) tells you what item must be in each case: 
Line 1213: item : String
Line 1214: --------------------------------------
Line 1215: display_rhs_1 : String
Line 1216: item : Int
Line 1217: --------------------------------------
Line 1218: display_rhs_2 : String
Line 1219: x : Schema
Line 1220: y : Schema
Line 1221: item : (SchemaType x, SchemaType y)
Line 1222: --------------------------------------
Line 1223: display_rhs_3 : String
Line 1224: 5
Line 1225: Refine—For ?display_rhs_1 and ?display_rhs_2 you can complete the defini-
Line 1226: tion by directly converting item to a String. For ?display_rhs_3, you can case-
Line 1227: split on item and recursively display each entry: 
Line 1228: display : SchemaType schema -> String
Line 1229: display {schema = SString} item = show item
Line 1230: display {schema = SInt} item = show item
Line 1231: display {schema = (x .+. y)} (iteml, itemr)
Line 1232: = display iteml ++ ", " ++ display itemr
Line 1233: Once this definition is complete and the file is reloaded into the Idris REPL, there
Line 1234: should be one remaining hole, ?parseBySchema. 
Line 1235: 6.3.5
Line 1236: Parsing entries according to the schema
Line 1237: The remaining hole, ?parseBySchema, is intended to convert the String the user
Line 1238: entered into an appropriate type for the schema. You can see what’s expected by look-
Line 1239: ing at its type:
Line 1240: rest : String
Line 1241: schema : Schema
Line 1242: --------------------------------------
Line 1243: parseBySchema : String -> SchemaType schema
Line 1244: As you saw earlier, not every String will lead to a valid SchemaType schema, so you can
Line 1245: refine this type slightly and create a top-level function that returns a Maybe (Schema-
Line 1246: Type schema) to reflect the fact that parsing the input might fail, additionally making
Line 1247: schema explicit:
Line 1248: parseBySchema : (schema : Schema) -> String -> Maybe (SchemaType schema)
Line 1249: 
Line 1250: --- 페이지 198 ---
Line 1251: 172
Line 1252: CHAPTER 6
Line 1253: Programming with first-class types
Line 1254: Then, you can edit parseCommand to use this new function. If parseBySchema fails
Line 1255: (that is, returns Nothing), parseCommand should also return Nothing:
Line 1256: parseCommand schema "add" rest = case parseBySchema schema rest of
Line 1257: Nothing => Nothing
Line 1258: Just restok => Just (Add restok)
Line 1259: To parse complete inputs as described by schemas, you’ll need to be able to parse por-
Line 1260: tions of the input according to a subset of the schema. For example, given a schema
Line 1261: (SInt .+. SString) and an input 100 "Antelopes", you’ll need to be able to parse the
Line 1262: prefix 100 as SInt, followed by the remainder, "Antelopes", as SString.
Line 1263:  You can therefore define your parser with the following two components: 
Line 1264: 
Line 1265: parsePrefix reads a prefix of the input according to the schema and returns
Line 1266: the parsed input, if successful, paired with the remainder of the text.
Line 1267: 
Line 1268: parseBySchema calls parsePrefix with some input and ensures that once it has
Line 1269: parsed the input according to the schema, there’s no input remaining.
Line 1270: The next listing shows the top-level implementation of parseBySchema and the type of
Line 1271: the parsePrefix helper function.
Line 1272: parsePrefix : (schema : Schema) -> String -> Maybe (SchemaType schema, String)
Line 1273: parseBySchema : (schema : Schema) -> String -> Maybe (SchemaType schema)
Line 1274: parseBySchema schema input = case parsePrefix schema input of
Line 1275: Just (res, "") => Just res
Line 1276: Just _ => Nothing
Line 1277: Nothing => Nothing
Line 1278: Let’s take a look at the outline of parsePrefix, following the type-define-refine
Line 1279: approach and see how the structure of the schema gives us hints about how to proceed
Line 1280: with each part of the implementation:
Line 1281: 1
Line 1282: Define—You already have the type, so begin by providing a skeleton definition: 
Line 1283: parsePrefix : (schema : Schema) -> String ->
Line 1284:         Maybe (SchemaType schema, String)
Line 1285: parsePrefix schema item = ?parsePrefix_rhs
Line 1286:  2
Line 1287: Define—If you case-split on schema, Idris will generate cases for each possible
Line 1288: form of the schema: 
Line 1289: parsePrefix : (schema : Schema) -> String ->
Line 1290:         Maybe (SchemaType schema, String)
Line 1291: parsePrefix SString input = ?parsePrefix_rhs_1
Line 1292: Listing 6.19
Line 1293: Outline implementation of parseBySchema, using an undefined
Line 1294: parsePrefix function to parse a prefix of an input according to a schema
Line 1295: Parsing succeeds when
Line 1296: parsePrefix succeeds and the
Line 1297: remainder of the input is empty.
Line 1298: If parsePrefix succeeds but there’s input 
Line 1299: remaining, parsing overall should fail because 
Line 1300: there’s more input than required by the schema.
Line 1301: parsePrefix failed, 
Line 1302: so parsing overall 
Line 1303: should fail.
Line 1304: 
Line 1305: --- 페이지 199 ---
Line 1306: 173
Line 1307: Enhancing the interactive data store with schemas
Line 1308: parsePrefix SInt input = ?parsePrefix_rhs_2
Line 1309: parsePrefix (x .+. y) input = ?parsePrefix_rhs_3
Line 1310:  3
Line 1311: Type—Looking at the types of the holes tells you what the return types must be
Line 1312: for each form of the schema. For example, in ?parsePrefix_rhs_2 you need to
Line 1313: convert the input into a Int, if possible, paired with the rest of the input: 
Line 1314: input : String
Line 1315: --------------------------------------
Line 1316: parsePrefix_rhs_2 : Maybe (Int, String)
Line 1317:  4
Line 1318: Refine—For ?parsePrefix_rhs_2, if the prefix of the input contains digits, you
Line 1319: can convert them to an Int and return the resulting Int and the remainder of
Line 1320: the String. You can refine it to the following: 
Line 1321: parsePrefix SInt input = case span isDigit input of
Line 1322: ("", rest) => Nothing
Line 1323: (num, rest) => Just (cast num, ltrim rest)
Line 1324: If the prefix of the input that contains digits is empty, then it’s not a valid Int,
Line 1325: so return Nothing. Otherwise, you can convert the prefix to an Int and return
Line 1326: the rest of the input, with leading spaces trimmed using ltrim.
Line 1327:  5
Line 1328: Refine—You can refine ?parsePrefix_rhs_1 similarly, looking for an opening
Line 1329: quotation mark and then reading the string until you reach the closing quota-
Line 1330: tion mark. You’ll see the complete definition shortly in listing 6.20.
Line 1331: 6
Line 1332: Refine—The type of ?parsePrefix_rhs_3 shows that you need to parse two sub-
Line 1333: schemas and combine the results: 
Line 1334: x : Schema
Line 1335: y : Schema
Line 1336: input : String
Line 1337: --------------------------------------
Line 1338: parsePrefix_rhs_3 : Maybe ((SchemaType x, SchemaType y), String)
Line 1339: It’s a good idea to give x and y more-meaningful names before proceeding:
Line 1340: parsePrefix (schemal .+. schemar) input = ?parsePrefix_rhs_3
Line 1341: To refine parsePrefix_rhs_3, you can recursively parse the first portion of the
Line 1342: input according to schemal, and if that succeeds, parse the rest of the input
Line 1343: according to schemar. Parse the first portion: 
Line 1344: parsePrefix (schemal .+. schemar) input
Line 1345: = case parsePrefix schemal input of
Line 1346: Nothing => Nothing
Line 1347: Just (l_val, input') => ?parsePrefix_rhs_2
Line 1348: If parsePrefix on the first part of the schema fails, the whole thing will fail.
Line 1349: Otherwise, you have a new hole: 
Line 1350: schemal : Schema
Line 1351: l_val : SchemaType schemal
Line 1352: input' : String
Line 1353: 
Line 1354: --- 페이지 200 ---
Line 1355: 174
Line 1356: CHAPTER 6
Line 1357: Programming with first-class types
Line 1358: schemar : Schema
Line 1359: input : String
Line 1360: --------------------------------------
Line 1361: parsePrefix_rhs_2 : Maybe ((SchemaType schemal, SchemaType schemar), String)
Line 1362: KEEP RELOADING!
Line 1363: While following this type-driven approach, you always have
Line 1364: a file that type-checks as far as possible. Here, rather than filling the hole
Line 1365: completely, you’ve written a small part of it with a new hole, and checked that
Line 1366: what you have type-checks before proceeding.
Line 1367:  7
Line 1368: Refine—Finally, you can complete this case by parsing the remaining input
Line 1369: according to schemar: 
Line 1370: parsePrefix (schemal .+. schemar) input
Line 1371: = case parsePrefix schemal input of
Line 1372: Nothing => Nothing
Line 1373: Just (l_val, input') =>
Line 1374: case parsePrefix schemar input' of
Line 1375: Nothing => Nothing
Line 1376: Just (r_val, input'') =>
Line 1377:                            Just ((l_val, r_val), input'')
Line 1378: NESTED CASE BLOCKS
Line 1379: These nested case blocks we’ve used may seem a little
Line 1380: verbose. In section 6.3.7 you’ll see one way of writing these more concisely.
Line 1381: The following listing shows the complete implementation of parsePrefix, filling in
Line 1382: the remaining details, including parsing quoted strings. You now have a complete
Line 1383: implementation that can compile and run.
Line 1384: parsePrefix : (schema : Schema) -> String -> Maybe (SchemaType schema, String)
Line 1385: parsePrefix SString input = getQuoted (unpack input)
Line 1386: where
Line 1387: getQuoted : List Char -> Maybe (String, String)
Line 1388: getQuoted ('"' :: xs)
Line 1389: = case span (/= '"') xs of
Line 1390: (quoted, '"' :: rest) => Just (pack quoted, ltrim (pack rest))
Line 1391: _ => Nothing
Line 1392: getQuoted _ = Nothing
Line 1393: parsePrefix SInt input = case span isDigit input of
Line 1394: ("", rest) => Nothing
Line 1395: (num, rest) => Just (cast num, ltrim rest)
Line 1396: Listing 6.20
Line 1397: Parsing a prefix of an input according to a specific schema
Line 1398: Parses a prefix of the input as a quoted 
Line 1399: string. If the input doesn’t begin with a 
Line 1400: quote character, parsing should fail.
Line 1401: getQuoted returns a quoted prefix
Line 1402: of a String, with the input broken
Line 1403: down into characters as a List Char.
Line 1404: Uses ltrim to remove any 
Line 1405: leading whitespace from the 
Line 1406: remainder of the input.
Line 1407: Parses a prefix of the input as an
Line 1408: integer: it takes the prefix of the string
Line 1409: that consists entirely of digits. If there
Line 1410: are no digits, parsing should fail.
Line 1411: 
Line 1412: --- 페이지 201 ---
Line 1413: 175
Line 1414: Enhancing the interactive data store with schemas
Line 1415: parsePrefix (schemal .+. schemar) input
Line 1416: = case parsePrefix schemal input of
Line 1417: Nothing => Nothing
Line 1418: Just (l_val, input') =>
Line 1419: case parsePrefix schemar input' of
Line 1420: Nothing => Nothing
Line 1421: Just (r_val, input'') => Just ((l_val, r_val), input'')
Line 1422: 6.3.6
Line 1423: Updating the schema
Line 1424: Although you now have a complete implementation, it still has no more functionality
Line 1425: than the previous version, because the schema is initialized as SString in main, and
Line 1426: you haven’t yet implemented any way to update this:
Line 1427: main : IO ()
Line 1428: main = replWith (MkData SString _ []) "Command: " processInput
Line 1429: You can, at least, try out different schemas by updating main and recompiling. For
Line 1430: example, you could try a schema that accepts two Strings and an Int:
Line 1431: main : IO ()
Line 1432: main = replWith (MkData (SString .+. SString .+. SInt) _ [])
Line 1433: "Command: " processInput
Line 1434: You can compile and run this using :exec at the REPL, and try a couple of example
Line 1435: entries:
Line 1436: *DataStore> :exec
Line 1437: Command: add "Bob Dylan" "Blonde on Blonde" 1965
Line 1438: ID 0
Line 1439: Command: add "Prefab Sprout" "From Langley Park to Memphis" 1988
Line 1440: ID 1
Line 1441: Command: get 0
Line 1442: "Bob Dylan", "Blonde on Blonde", 1965
Line 1443: It would be preferable, however, to allow users to define their own schemas, rather
Line 1444: than hardcoding them into main. To achieve this, you can add a new command for set-
Line 1445: ting a new schema, updating the Command data type. 
Line 1446: data Command : Schema -> Type where
Line 1447: SetSchema : (newschema : Schema) -> Command schema
Line 1448: Add : SchemaType schema -> Command schema
Line 1449: Get : Integer -> Command schema
Line 1450: Quit : Command schema
Line 1451: You’ll also need functions to do the following: 
Line 1452: Update the DataStore type to hold the new schema. This should only work
Line 1453: when the store is empty, because when you change the schema type, it invali-
Line 1454: dates the current contents of the store.
Line 1455: Parse a schema description from user input.
Line 1456: Listing 6.21
Line 1457: The Command data structure with a new command for updating the schema
Line 1458: Parses a prefix of the string according 
Line 1459: to schemal, and then the rest of the 
Line 1460: string according to schemar. If either 
Line 1461: part fails, parsing overall should fail. 
Line 1462: New command to set a new 
Line 1463: schema. Note that the type 
Line 1464: expresses no relationship 
Line 1465: between newschema and 
Line 1466: the existing schema.
Line 1467: 
Line 1468: --- 페이지 202 ---
Line 1469: 176
Line 1470: CHAPTER 6
Line 1471: Programming with first-class types
Line 1472: You’ll also need to update parseCommand and processInput to deal with parsing and
Line 1473: processing the new command. These new functions are implemented using the same
Line 1474: process you followed so far in implementing the extended data store. Listing 6.22
Line 1475: shows how parsing the new command works. It adds a user command, schema, fol-
Line 1476: lowed by a list of String and Int, and translates this into the SetSchema command.
Line 1477: parseSchema : List String -> Maybe Schema
Line 1478: parseSchema ("String" :: xs)
Line 1479: = case xs of
Line 1480: [] => Just SString
Line 1481: _ => case parseSchema xs of
Line 1482: Nothing => Nothing
Line 1483: Just xs_sch => Just (SString .+. xs_sch)
Line 1484: parseSchema ("Int" :: xs)
Line 1485: = case xs of
Line 1486: [] => Just SInt
Line 1487: _ => case parseSchema xs of
Line 1488: Nothing => Nothing
Line 1489: Just xs_sch => Just (SInt .+. xs_sch)
Line 1490: parseSchema _ = Nothing
Line 1491: parseCommand : (schema : Schema) -> String -> String -> Maybe (Command schema)
Line 1492: {- ... rest of definition as before ... -}
Line 1493: parseCommand schema "schema" rest
Line 1494: = case parseSchema (words rest) of
Line 1495: Nothing => Nothing
Line 1496: Just schemaok => Just (SetSchema schemaok)
Line 1497: parseCommand _ _ _ = Nothing
Line 1498: Listing 6.23 shows how updating the schema works once the new command has been
Line 1499: parsed. As a design choice, it will only allow the schema to be updated when the store
Line 1500: is empty, because there is no general way of updating the contents of the data store
Line 1501: with an arbitrarily updated schema (an alternative would be to empty the store when
Line 1502: the user changes the schema).
Line 1503: setSchema : (store : DataStore) -> Schema -> Maybe DataStore
Line 1504: setSchema store schema = case size store of
Line 1505: Z => Just (MkData schema _ [])
Line 1506: S k => Nothing
Line 1507: processInput : DataStore -> String -> Maybe (String, DataStore)
Line 1508: processInput store input
Line 1509: = case parse (schema store) input of
Line 1510: Nothing => Just ("Invalid command\n", store)
Line 1511: Just (Add item) =>
Line 1512: Listing 6.22
Line 1513: Parsing a Schema description, and extending the parser for Command to
Line 1514: support setting a new schema
Line 1515: Listing 6.23
Line 1516: Processing the SetSchema command, updating the schema description
Line 1517: in the DataStore
Line 1518: Parsing a schema description 
Line 1519: may fail if the arguments are 
Line 1520: invalid, so return something of 
Line 1521: type Maybe Schema.
Line 1522: Parses an
Line 1523: input where
Line 1524: the first
Line 1525: word is
Line 1526: “String”.
Line 1527: Parses an input where 
Line 1528: the first word is “Int”.
Line 1529: Parses the schema 
Line 1530: description by separating 
Line 1531: the rest of the input into a 
Line 1532: list of words.
Line 1533: Setting a new schema may fail
Line 1534: if there are entries in the
Line 1535: store, so return Maybe
Line 1536: DataStore to capture the
Line 1537: possibility of failure.
Line 1538: 
Line 1539: --- 페이지 203 ---
Line 1540: 177
Line 1541: Enhancing the interactive data store with schemas
Line 1542: Just ("ID " ++ show (size store) ++ "\n", addToStore store item)
Line 1543: Just (SetSchema schema') =>
Line 1544: case setSchema store schema' of
Line 1545: Nothing => Just ("Can't update schema\n", store)
Line 1546: Just store' => Just ("OK\n", store')
Line 1547: Just (Get pos) => getEntry pos store
Line 1548: Just Quit => Nothing
Line 1549: Finally, you can compile and run this program and try setting a new schema from user
Line 1550: input:
Line 1551: *DataStore> :exec
Line 1552: Command: schema Int String
Line 1553: OK
Line 1554: Command: add 99 "Red balloons"
Line 1555: ID 0
Line 1556: Command: add 76 "Trombones"
Line 1557: ID 1
Line 1558: Command: schema String String Int
Line 1559: Can't update schema when entries in store
Line 1560: Command: get 1
Line 1561: 76, "Trombones"
Line 1562: In the end, using a data type to describe the schema and using that schema to calcu-
Line 1563: late the types of the operations on the data store has a few consequences: 
Line 1564: On reading user input, you can’t add the input to the store if it’s not valid
Line 1565: according to the schema.
Line 1566: If you change the schema type, you can’t invalidate the contents of the store
Line 1567: because the type of the store’s contents prevents it. Changing the schema type
Line 1568: requires you to have an empty store.
Line 1569: When writing the parser for user input, you can use the description of the
Line 1570: schema to guide the implementation of the parser and to build the correct type
Line 1571: for the input.
Line 1572: 6.3.7
Line 1573: Sequencing expressions with Maybe using do notation
Line 1574: In the data store program, there are several places where we’ve used a case block to
Line 1575: check the result of a function that returns something with a Maybe type, and passed
Line 1576: that result on. For example:
Line 1577: parseCommand schema "schema" rest
Line 1578: = case parseSchema (words rest) of
Line 1579: Nothing => Nothing
Line 1580: Just schemaok => Just (SetSchema schemaok)
Line 1581: Here, parseCommand, which returns something of type Maybe (Command schema), has
Line 1582: called parseSchema, which returns something of type Maybe Schema, and has used a
Line 1583: case expression to check the result of the call to parseSchema.
Line 1584: Updating the
Line 1585: schema failed,
Line 1586: so report an
Line 1587: error and keep
Line 1588: the old store.
Line 1589: Updating the schema 
Line 1590: succeeded, so report 
Line 1591: success and update 
Line 1592: to the new store.
Line 1593: 
Line 1594: --- 페이지 204 ---
Line 1595: 178
Line 1596: CHAPTER 6
Line 1597: Programming with first-class types
Line 1598:  If parseSchema fails, parseCommand also fails. Similarly, if parseSchema succeeds,
Line 1599: then parseCommand also succeeds.
Line 1600:  You can see a similar pattern in the maybeAdd function in the following listing,
Line 1601: which adds two values of type Maybe Int, returning Nothing if either input is Nothing.
Line 1602: maybeAdd : Maybe Int -> Maybe Int -> Maybe Int
Line 1603: maybeAdd x y = case x of
Line 1604: Nothing => Nothing
Line 1605: Just x_val => case y of
Line 1606: Nothing => Nothing
Line 1607: Just y_val => Just (x_val + y_val)
Line 1608: You can try maybeAdd on a few examples, and you’ll see that it adds its inputs if both
Line 1609: are of the form Just val for some concrete value val, and that it returns Nothing if
Line 1610: either of the inputs is Nothing:
Line 1611: *Maybe> maybeAdd (Just 3) (Just 4)
Line 1612: Just 7 : Maybe Int
Line 1613: *Maybe> maybeAdd (Just 3) Nothing
Line 1614: Nothing : Maybe Int
Line 1615: *Maybe> maybeAdd Nothing (Just 4)
Line 1616: Nothing : Maybe Int
Line 1617: A common pattern is found here, in parseCommand, and in several other places
Line 1618: throughout the data store implementation: 
Line 1619: 1
Line 1620: Evaluate an expression of type Maybe ty. The result is either Nothing or Just x,
Line 1621: where x has type ty.
Line 1622:  2
Line 1623: If the result is Nothing, the result of the entire computation is Nothing.
Line 1624: 3
Line 1625: If the result is Just x, pass x to the rest of the computation.
Line 1626: When you see a common pattern, it’s a good idea to try to capture that pattern in a
Line 1627: higher-order function. In fact, you’ve already seen an operator that implements a sim-
Line 1628: ilar pattern in chapter 5, when sequencing IO operations: 
Line 1629: (>>=) : IO a -> (a -> IO b) -> IO b
Line 1630: The same operator works for sequencing Maybe computations, when defined as follows: 
Line 1631: (>>=) : Maybe a -> (a -> Maybe b) -> Maybe b
Line 1632: (>>=) Nothing next
Line 1633: = Nothing
Line 1634: (>>=) (Just x) next = next x
Line 1635: Listing 6.24
Line 1636: Adding two Maybe Ints (Maybe.idr)
Line 1637: First input was Nothing, so entire 
Line 1638: computation returns Nothing
Line 1639: Second input was Nothing,
Line 1640: so entire computation
Line 1641: returns Nothing
Line 1642: Both inputs of form Just val, so
Line 1643: add x_val and y_val and return
Line 1644: their sum, wrapped in a Just
Line 1645: 
Line 1646: --- 페이지 205 ---
Line 1647: 179
Line 1648: Enhancing the interactive data store with schemas
Line 1649:  Effectively, it takes the output of the first computation, if successful (that is, return-
Line 1650: ing a Just), and passes it on as input to the second. It captures a common pattern of
Line 1651: evaluating an expression with a Maybe type.
Line 1652: Using (>>=) as an infix operator, you can rewrite maybeAdd more concisely, if some-
Line 1653: what cryptically, as in the following listing.
Line 1654: maybeAdd : Maybe Int -> Maybe Int -> Maybe Int
Line 1655: maybeAdd x y = x >>= \x_val =>
Line 1656: y >>= \y_val =>
Line 1657: Just (x_val + y_val)
Line 1658: In chapter 5, you saw that Idris provides a special notation for sequencing computa-
Line 1659: tions using (>>=), introduced by the keyword do. You can use the same notation here,
Line 1660: and write maybeAdd as follows.
Line 1661: maybeAdd : Maybe Int -> Maybe Int -> Maybe Int
Line 1662: maybeAdd x y = do x_val <- x
Line 1663: y_val <- y
Line 1664: Just (x_val + y_val)
Line 1665: Figure 6.5 shows how an expression using do notation is translated into an expression
Line 1666: using (>>=). This works exactly the same way as the translation of IO programs written
Line 1667: using do notation. Just like the translation of list syntax into Nil and (::), this transla-
Line 1668: tion is purely syntactic. As a result, if you define the (>>=) operator in some other con-
Line 1669: text, Idris will allow you to use do notation in that context.
Line 1670: Listing 6.25
Line 1671: Adding two Maybe Ints using (>>=) rather than direct case analysis
Line 1672: Listing 6.26
Line 1673: Adding two Maybe Ints using do notation rather than using (>>=)
Line 1674: directly
Line 1675: Type of (>>=)
Line 1676: Remember from chapter 5 that if you check the type of (>>=) at the REPL, you’ll see
Line 1677: a constrained generic type: 
Line 1678: Idris> :t (>>=)
Line 1679: (>>=) : Monad m => m a -> (a -> m b) -> m b
Line 1680: In general, the >>= operator can be used to sequence computations. You’ll see how
Line 1681: this works in chapter 7 when we discuss interfaces.
Line 1682: If Idris evaluates the second operand of 
Line 1683: >>= here, the definition of >>= means 
Line 1684: that x must have the value Just x_val.
Line 1685: If Idris evaluates the
Line 1686: second operand of >>=
Line 1687: here, y must have the
Line 1688: value Just y_val.
Line 1689: If x has the form Just x_val, 
Line 1690: computation continues; 
Line 1691: otherwise, it returns Nothing.
Line 1692: If y has the form Just y_val, 
Line 1693: computation continues; 
Line 1694: otherwise, it returns Nothing.
Line 1695: 
Line 1696: --- 페이지 206 ---
Line 1697: 180
Line 1698: CHAPTER 6
Line 1699: Programming with first-class types
Line 1700: With do notation, you could have written the "schema" case for parseCommand as fol-
Line 1701: lows, letting the do notation, via (>>=), take care of the handling of Nothing so that
Line 1702: you could focus on the successful case of Just schemaok: 
Line 1703: parseCommand schema "schema" rest
Line 1704: = do schemaok <- parseSchema (words rest)
Line 1705: Just (SetSchema schemaok)
Line 1706: Exercises
Line 1707: 1
Line 1708: Update the data store program to support Chars in the schema.
Line 1709: You can test your solution at the REPL as follows: 
Line 1710: *ex_6_3> :exec
Line 1711: Command: schema Char Int
Line 1712: OK
Line 1713: Command: add x 24
Line 1714: ID 0
Line 1715: Command: add y 17
Line 1716: ID 1
Line 1717: Command: get 0
Line 1718: 'x', 24
Line 1719:  2
Line 1720: Modify the get command so that, if given no arguments, it prints the entire con-
Line 1721: tents of the data store.
Line 1722: For example:
Line 1723: *ex_6_3> :exec
Line 1724: Command: schema Char Int
Line 1725: OK
Line 1726: Command: add x 24
Line 1727: ID 0
Line 1728: Command: add y 17
Line 1729: ID 1
Line 1730: Command: get
Line 1731: 0: 'x', 24
Line 1732: 1: 'y', 17
Line 1733:  3
Line 1734: Update the data store program so that it uses do notation rather than nested case
Line 1735: blocks, where appropriate.
Line 1736: do x <- expr
Line 1737:    result
Line 1738: expr >>= \x => result
Line 1739: If expr has the form
Line 1740: Just val : Maybe ty
Line 1741: then x : ty = val
Line 1742: Expression to
Line 1743: be tested, of
Line 1744: type Maybe ty
Line 1745: Result of the computation,
Line 1746: which may use x : ty
Line 1747: Transformed expression
Line 1748: Figure 6.5
Line 1749: Transforming do 
Line 1750: notation to an expression using 
Line 1751: the (>>=) operator
Line 1752: 
Line 1753: --- 페이지 207 ---
Line 1754: 181
Line 1755: Summary
Line 1756: 6.4
Line 1757: Summary
Line 1758: Type synonyms are alternative names for existing types, which allow you to give
Line 1759: more-descriptive names to types.
Line 1760: Type-level functions are functions that can be used anywhere that Idris is
Line 1761: expecting a Type. Type synonyms are a special case of type-level functions.
Line 1762: Type-level functions can be used to compute types, and they allow you to write
Line 1763: functions with varying numbers of arguments, such as printf.
Line 1764: You can represent a schema for a data store as a type, and then use type-level
Line 1765: functions to calculate the types of operations, such as parsing and displaying
Line 1766: entries in the data store from the schema description.
Line 1767: A record is a data type with only one constructor, and with automatically gener-
Line 1768: ated functions for projecting fields from the record.
Line 1769: After refining a data type, you can use holes to correct compilation errors tem-
Line 1770: porarily.
Line 1771: Using do notation, you can sequence computations that use Maybe to capture
Line 1772: the possibility of errors.