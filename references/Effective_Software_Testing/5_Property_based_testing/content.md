Line 1: 
Line 2: --- 페이지 145 ---
Line 3: 117
Line 4: Property-based testing
Line 5: So far, we have been doing example-based testing. We judiciously divide the input
Line 6: space of a program (into partitions), pick one concrete example from all the possi-
Line 7: ble ones, and write the test case. What if we did not have to pick one concrete
Line 8: example out of many? What if we could express the property we are trying to exercise
Line 9: and let the test framework choose several concrete examples for us? Our tests
Line 10: would be less dependent on a concrete example, and the test framework would be
Line 11: able to call the method under test multiple times with different input parameters—
Line 12: usually with zero effort from us.
Line 13:  This is what property-based testing is about. We do not pick a concrete example;
Line 14: rather, we define a property (or a set of properties) that the program should
Line 15: adhere to, and the test framework tries to find a counterexample that causes the
Line 16: program to break with these properties.
Line 17:  I have learned that the best way to teach how to write property-based tests is with
Line 18: multiple examples. So, this chapter presents five different examples with varying
Line 19: levels of complexity. I want you to focus on my way of thinking and notice how
Line 20: much creativity is required to write such tests.
Line 21: This chapter covers
Line 22: Writing property-based tests
Line 23: Understanding when to write property-based tests 
Line 24: or example-based tests
Line 25: 
Line 26: --- 페이지 146 ---
Line 27: 118
Line 28: CHAPTER 5
Line 29: Property-based testing
Line 30: 5.1
Line 31: Example 1: The passing grade program
Line 32: Consider the following requirement, inspired by a similar problem in Kaner et al.’s
Line 33: book (2013):
Line 34: A student passes an exam if they get a grade >= 5.0. Grades below that are a
Line 35: fail. Grades fall in the range [1.0, 10.0].
Line 36: A simple implementation for this program is shown in the following listing.
Line 37: public class PassingGrade {
Line 38:   public boolean passed(float grade) {
Line 39:     if (grade < 1.0 || grade > 10.0) 
Line 40:       throw new IllegalArgumentException();
Line 41:     return grade >= 5.0;
Line 42:   }
Line 43: }
Line 44: If we were to apply specification-based testing to this program, we would probably
Line 45: devise partitions such as “passing grade,” “failing grade,” and “grades outside the
Line 46: range.” We would then devise a single test case per partition. With property-based test-
Line 47: ing, we want to formulate properties that the program should have. I see the following
Line 48: properties for this requirement:
Line 49: 
Line 50: fail—For all numbers ranging from 1.0 (inclusive) to 5.0 (exclusive), the pro-
Line 51: gram should return false.
Line 52: 
Line 53: pass—For all numbers ranging from 5.0 (inclusive) to 10.0 (inclusive), the pro-
Line 54: gram should return true.
Line 55: 
Line 56: invalid—For all invalid grades (which we define as any number below 1.0 or
Line 57: greater than 10.0), the program must throw an exception.
Line 58: Can you see the difference between what we do in specification-based testing and
Line 59: what we aim to do in property-based testing? Let’s write a suite test by test, starting
Line 60: with the fail property. For that, we will use jqwik (https://jqwik.net), a popular prop-
Line 61: erty-based testing framework for Java.
Line 62: NOTE
Line 63: Property-based testing frameworks are available in many different lan-
Line 64: guages, although their APIs vary significantly (unlike unit testing frameworks
Line 65: like JUnit, which all look similar). If you are applying this knowledge to
Line 66: another language, your task is to study the framework that is available in your
Line 67: programming language. The way to think and reason is the same across dif-
Line 68: ferent languages.
Line 69: Before I show the concrete implementation, let me break down property-based testing
Line 70: step by step, using jqwik’s lingo:
Line 71: Listing 5.1
Line 72: Implementation of the PassingGrade program
Line 73: Note the pre-condition 
Line 74: check here.
Line 75: 
Line 76: --- 페이지 147 ---
Line 77: 119
Line 78: Example 1: The passing grade program
Line 79: 1
Line 80: For each property we want to express, we create a method and annotate it with
Line 81: @Property. These methods look like JUnit tests, but instead of containing a sin-
Line 82: gle example, they contain an overall property.
Line 83: 2
Line 84: Properties use randomly generated data. Jqwik includes several generators for
Line 85: various types (including Strings, Integers, Lists, Dates, and so on.). Jqwik
Line 86: allows you to define different sets of constraints and restrictions to these param-
Line 87: eters: for example, to generate only positive Integers or only Strings with a
Line 88: length between 5 and 10 characters. The property method receives all the
Line 89: required data for that test as parameters.
Line 90: 3
Line 91: The property method calls the method under test and asserts that the method’s
Line 92: behavior is correct.
Line 93: 4
Line 94: When the test runs, jqwik generates a large amount of random data (following
Line 95: the characteristics you defined) and calls the test for it, looking for an input
Line 96: that would break the property. If jqwik finds an input that makes your test fail,
Line 97: the tool reports this input back to the developer. The developer then has an
Line 98: example of an input that breaks their program.
Line 99: The following listing shows the code for the fail property.
Line 100: public class PassingGradesPBTest {
Line 101:   private final PassingGrade pg = new PassingGrade();
Line 102:   @Property
Line 103:   void fail( 
Line 104:    @ForAll 
Line 105:    @FloatRange(min = 1f, max = 5f, maxIncluded = false) 
Line 106:    float grade) { 
Line 107:     assertThat(pg.passed(grade)).isFalse();
Line 108:   }
Line 109: }
Line 110: We annotate the test method with @Property instead of @Test. The test method
Line 111: receives a grade parameter that jqwik will set, following the rules we give it. We then
Line 112: annotate the grade parameter with two properties. First, we say that this property
Line 113: should hold for all (@ForAll) grades. This is jqwik’s terminology. If we left only the
Line 114: @ForAll annotation, jqwik would try any possible float as input. However, for this fail
Line 115: property, we want numbers varying from 1.0 to 5.0, which we specify using the @Float-
Line 116: Range annotation. The test then asserts that the program returns false for all the pro-
Line 117: vided grades.
Line 118: Listing 5.2
Line 119: A property-based test for the fail property
Line 120: Defines the characteristics of the values 
Line 121: we want to generate via annotations
Line 122: Any parameter to be 
Line 123: generated by jqwik 
Line 124: must be annotated 
Line 125: with ForAll.
Line 126: We want random floats 
Line 127: in a [1.0, 5.0] interval 
Line 128: (max value excluded), 
Line 129: which we define in the 
Line 130: FloatRange annotation.
Line 131: The grade parameter will be
Line 132: generated according to the rules
Line 133: specified in the annotations.
Line 134: 
Line 135: --- 페이지 148 ---
Line 136: 120
Line 137: CHAPTER 5
Line 138: Property-based testing
Line 139:  When we run the test, jqwik randomly provides values for the grade parameter, fol-
Line 140: lowing the ranges we specified. With its default configuration, jqwik randomly gener-
Line 141: ates 1,000 different inputs for this method. If this is your first time with property-based
Line 142: testing, I suggest that you write some print statements in the body of the test method
Line 143: to see the values generated by the framework. Note how random they are and how
Line 144: much they vary.
Line 145:  Correspondingly, we can test the pass property using a similar strategy, as shown next.
Line 146: @Property
Line 147: void pass(
Line 148:   @ForAll
Line 149:   @FloatRange(min = 5f, max = 10f, maxIncluded = true) 
Line 150:   float grade) {
Line 151:   assertThat(pg.passed(grade)).isTrue();
Line 152: }
Line 153: Finally, to make jqwik generate numbers that are outside of the valid range of grades,
Line 154: we need to use a smarter generator (as FloatRange does not allow us to express things
Line 155: like “grade < 1.0 or grade > 10.0”). See the invalidGrades() provider method in the
Line 156: following listing: methods annotated with @Provide are used to express more com-
Line 157: plex inputs that need to be generated.
Line 158: @Property
Line 159: void invalid(
Line 160:  @ForAll("invalidGrades") 
Line 161:  float grade) {
Line 162:   assertThatThrownBy(() -> {
Line 163:     pg.passed(grade);
Line 164:   }).isInstanceOf(IllegalArgumentException.class); 
Line 165: }
Line 166: @Provide 
Line 167: private Arbitrary<Float> invalidGrades() {
Line 168:   return Arbitraries.oneOf( 
Line 169:       Arbitraries.floats().lessThan(1f), 
Line 170:       Arbitraries.floats().greaterThan(10f) 
Line 171:   );
Line 172: }
Line 173: The @Property test method is straightforward: for all grades generated, we assert that
Line 174: an exception is thrown. The challenge is generating random grades. We express this
Line 175: in the invalidGrades provider method, which should return either a grade smaller
Line 176: than 1 or a grade greater than 10. Also, note that the method returns an Arbitrary.
Line 177: Listing 5.3
Line 178: A property-based test for the pass property
Line 179: Listing 5.4
Line 180: A property-based test for the invalidGrades property
Line 181: We want random 
Line 182: floats in the range 
Line 183: of [5.0, 10.0], max 
Line 184: value included.
Line 185: The @ForAll annotation receives 
Line 186: the name of a Provider method 
Line 187: that will generate the data.
Line 188: Asserts that an 
Line 189: exception is thrown 
Line 190: for any value outside 
Line 191: the boundary
Line 192: A provider method needs to be 
Line 193: annotated with @Provide.
Line 194: Makes the method 
Line 195: randomly return …
Line 196: … a float that is 
Line 197: less than 1.0 …
Line 198: … or greater than 10.0.
Line 199: 
Line 200: --- 페이지 149 ---
Line 201: 121
Line 202: Example 1: The passing grade program
Line 203: An Arbitrary is how jqwik handles arbitrary values that need to be generated. If you
Line 204: need, say, arbitrary floats, your provider method should return an Arbitrary<Float>.
Line 205:  To give the two options to jqwik, we use the Arbitraries.oneOf() method. The
Line 206: Arbitraries class contains dozens of methods that help build arbitrary data. The
Line 207: oneOf() method receives a list of arbitrary values it may return. Behind the scenes,
Line 208: this method ensures that the distribution of data points generated is fairly distributed:
Line 209: for example, it generates as many “smaller than 1” inputs as “greater than 10” inputs.
Line 210: Then, we use another helper, the Arbitraries.floats() method, to generate ran-
Line 211: dom floats. Finally, we use the lessThan() and greaterThan() methods to generate
Line 212: numbers less than 1 and greater than 10, respectively.
Line 213: NOTE
Line 214: I suggest exploring the methods that the Arbitraries class provides!
Line 215: Jqwik is a very extensive framework and contains lots of methods to help you
Line 216: build any property you need. I will not discuss every feature of the framework, as
Line 217: that would be an entire book by itself. Instead, I recommend that you dive into
Line 218: jqwik’s excellent user guide: https://jqwik.net/docs/current/user-guide.html.
Line 219: When we run the tests, all of them pass, since our implementation is correct. Now,
Line 220: let’s introduce a bug in the code to see the jqwik output. For example, let’s change
Line 221: return grade >= 5.0 to return grade > 5.0, a simple off-by-one mistake. When we run
Line 222: our test suite again, the pass property test fails as expected! Jqwik also produces nice
Line 223: output to help us debug the problem.
Line 224: |-------------------jqwik-------------------
Line 225: tries = 11                    | \# of calls to property
Line 226: checks = 11                   | \# of not rejected calls
Line 227: generation = RANDOMIZED       | parameters are randomly generated
Line 228: after-failure = PREVIOUS_SEED | use the previous seed
Line 229: when-fixed-seed = ALLOW       | fixing the random seed is allowed
Line 230: edge-cases\#mode = MIXIN      | edge cases are mixed in
Line 231: edge-cases\#total = 2         | \# of all combined edge cases
Line 232: edge-cases\#tried = 1         | \# of edge cases tried in current run
Line 233: seed = 7015333710778187630    | random seed to reproduce generated values
Line 234: Sample
Line 235: ------
Line 236:   arg0: 5.0
Line 237: The output shows that jqwik found a counterexample in attempt number 11. Only 11
Line 238: trials were enough to find the bug! Jqwik then shows a set of configuration parameters
Line 239: that may be useful when reproducing and debugging more complex cases. In particu-
Line 240: lar, note the seed information: you can reuse that seed later to force jqwik to come up
Line 241: with the same sequence of inputs. Below the configuration, we see the sample that
Line 242: caused the bug: the value 5.0, as expected.
Line 243: Listing 5.5
Line 244: An example of a jqwik test failure
Line 245: 
Line 246: --- 페이지 150 ---
Line 247: 122
Line 248: CHAPTER 5
Line 249: Property-based testing
Line 250: NOTE
Line 251: If you are connecting the dots with previous chapters, you may be won-
Line 252: dering about boundary testing. Jqwik is smart enough to also generate
Line 253: boundary values! If we ask jqwik to generate, say, floats smaller than 1.0,
Line 254: jqwik will generate 1.0 as a test. If we ask jqwik to generate any integer, jqwik
Line 255: will try the maximum and minimum possible integers as well as 0 and nega-
Line 256: tive numbers. 
Line 257: 5.2
Line 258: Example 2: Testing the unique method
Line 259: The Apache Commons Lang offers the unique method (http://mng.bz/XWGM). Fol-
Line 260: lowing is its adapted Javadoc:
Line 261: Returns an array consisting of the unique values in data. The return array is
Line 262: sorted in descending order. Empty arrays are allowed, but null arrays result in
Line 263: a NullPointerException. Infinities are allowed.
Line 264: Parameters:
Line 265: 
Line 266: data: Array to scan
Line 267: The method returns a descending list of values included in the input array. It
Line 268: throws a NullPointerException if data is null.
Line 269: You can see its implementation next.
Line 270: public static int[] unique(int[] data) {
Line 271:   TreeSet<Integer> values = new TreeSet<Integer>(); 
Line 272:   for (int i = 0; i < data.length; i++) {
Line 273:      values.add(data[i]);
Line 274:   }
Line 275:   final int count = values.size();
Line 276:   final int[] out = new int[count]; 
Line 277:   Iterator<Integer> iterator = values.iterator();
Line 278:   int i = 0;
Line 279:   while (iterator.hasNext()) { 
Line 280:      out[count - ++i] = iterator.next();
Line 281:   }
Line 282:   return out;
Line 283: }
Line 284: Let’s go straight to property-based testing. Here, we focus on the main property of the
Line 285: method: given an array of integers, the method returns a new array containing only
Line 286: the unique values of the original array, sorted in descending order. This is the prop-
Line 287: erty we will embed in a jqwik test.
Line 288:  Our test works as follows. First we create a random list of integers. To ensure that
Line 289: the list has repeated numbers, we create a list of size 100 and limit the range of integers
Line 290: Listing 5.6
Line 291: Implementation of the unique method
Line 292: Uses a treeset to 
Line 293: filter out repeated 
Line 294: elements
Line 295: Creates the new array 
Line 296: using the size of the tree
Line 297: Visits the treeset and 
Line 298: adds the elements to 
Line 299: the new array
Line 300: 
Line 301: --- 페이지 151 ---
Line 302: 123
Line 303: Example 2: Testing the unique method
Line 304: to [0,20]. We then call the unique method and assert that the array contains all the
Line 305: elements of the original array, does not have duplicates, and is sorted in descending
Line 306: order. Let’s write that down in jqwik.
Line 307: public class MathArraysPBTest {
Line 308:   @Property
Line 309:   void unique(
Line 310:    @ForAll
Line 311:    @Size(value = 100) 
Line 312:    List<@IntRange(min = 1, max = 20) Integer> 
Line 313:    numbers) {
Line 314:     int[] doubles = convertListToArray(numbers);
Line 315:     int[] result = MathArrays.unique(doubles);
Line 316:     assertThat(result)
Line 317:         .contains(doubles) 
Line 318:         .doesNotHaveDuplicates() 
Line 319:         .isSortedAccordingTo(reverseOrder()); 
Line 320:   }
Line 321:   private int[] convertListToArray(List<Integer> numbers) { 
Line 322:     int[] array = numbers
Line 323:       .stream()
Line 324:       .mapToInt(x -> x)
Line 325:       .toArray();
Line 326:     return array;
Line 327:   }
Line 328: }
Line 329: TIP
Line 330: Note how AssertJ simplifies our lives with its many ready-to-use asser-
Line 331: tions. Without it, the developer would have to write lots of extra code. When
Line 332: writing complex assertions, check the documentation to see whether some-
Line 333: thing is available out of the box!
Line 334: NOTE
Line 335: One of my students noticed that even if we do not restrict the integer
Line 336: list to numbers in [0, 20], jqwik will produce lists with duplicated elements. In
Line 337: his exploration, he noticed that 11% of the produced arrays had a duplicated
Line 338: element. As a tester, you may want to consider whether 11% is a good rate. To
Line 339: measure this, my student used jqwik’s statistics feature (http://mng.bz/y4gE),
Line 340: which enables you to measure the distribution of the input values.
Line 341: Jqwik did not find any inputs that would break the program. So, our implementation
Line 342: seems to work. Let’s move to the next example. 
Line 343: Listing 5.7
Line 344: Property-based test for the unique method
Line 345: An array of 
Line 346: size 100
Line 347: With values in [0, 20]. Given 
Line 348: the size of the array (100), 
Line 349: we know it will contain 
Line 350: repeated elements.
Line 351: Contains all the elements
Line 352: No duplicates
Line 353: In descending order
Line 354: Utility method
Line 355: that converts a list of
Line 356: integers to an array
Line 357: 
Line 358: --- 페이지 152 ---
Line 359: 124
Line 360: CHAPTER 5
Line 361: Property-based testing
Line 362: 5.3
Line 363: Example 3: Testing the indexOf method
Line 364: The Apache Commons Lang has an interesting method called indexOf() (http://mng
Line 365: .bz/M24m) with the following documentation, adapted from its Javadoc:
Line 366: Finds the index of the given value in the array starting at the given index. This
Line 367: method returns –1 for a null input array. A negative startIndex is treated as
Line 368: zero. A startIndex larger than the array length will return –1.
Line 369: Input parameters:
Line 370: 
Line 371: array: Array to search for the object. May be null.
Line 372: 
Line 373: valueToFind: Value to find.
Line 374: 
Line 375: startIndex: Index at which to start searching.
Line 376: The method returns the index of the value within the array, or –1 if not found
Line 377: or null.
Line 378: Following is the implementation of this method.
Line 379: class ArrayUtils {
Line 380:   public static int indexOf(final int[] array, final int valueToFind,
Line 381:     ➥ int startIndex) {
Line 382:     if (array == null) { 
Line 383:       return -1;
Line 384:     }
Line 385:     if (startIndex < 0) { 
Line 386:       startIndex = 0;
Line 387:     }
Line 388:     for (int i = startIndex; i < array.length; i++) {
Line 389:       if (valueToFind == array[i]) {
Line 390:         return i; 
Line 391:       }
Line 392:     }
Line 393:     return -1; 
Line 394:   }
Line 395: }
Line 396: In this example, let’s first apply the techniques we already know. Start by exploring the
Line 397: input variables and how they interact with each other:
Line 398: 
Line 399: array of integers:
Line 400: – Null
Line 401: – Single element
Line 402: – Multiple elements
Line 403: 
Line 404: valueToFind:
Line 405: – Any integer
Line 406: Listing 5.8
Line 407: Implementation of the indexOf method
Line 408: The method accepts a null array and returns -1 in such a 
Line 409: case. Another option could be to throw an exception, but 
Line 410: the developer decided to use a weaker pre-condition.
Line 411: The same goes for startIndex: 
Line 412: if the index is negative, the 
Line 413: method assumes it is 0.
Line 414: If the value is found, 
Line 415: return the index.
Line 416: If the value is not in 
Line 417: the array, return -1.
Line 418: 
Line 419: --- 페이지 153 ---
Line 420: 125
Line 421: Example 3: Testing the indexOf method
Line 422: 
Line 423: startIndex:
Line 424: – Negative number
Line 425: – 0 [boundary]
Line 426: – Positive number
Line 427: 
Line 428: (array, startIndex):
Line 429: – startIndex in array
Line 430: – startIndex outside the boundaries of array
Line 431: 
Line 432: (array, valueToFind):
Line 433: – valueToFind not in array
Line 434: – valueToFind in array
Line 435: – valueToFind many times in array
Line 436: 
Line 437: (array, valueToFind, startIndex):
Line 438: – valueToFind in array, but before startIndex
Line 439: – valueToFind in array, but after startIndex
Line 440: – valueToFind in array, precisely in startIndex [boundary]
Line 441: – valueToFind in array multiple times after startIndex
Line 442: – valueToFind in array multiple times, one before and another after startIndex
Line 443: We now create the test cases by combining the different partitions:
Line 444: 1
Line 445: array is null
Line 446: 2
Line 447: array with a single element, valueToFind in array
Line 448: 3
Line 449: array with a single element, valueToFind not in array
Line 450: 4
Line 451: startIndex negative, value in array
Line 452: 5
Line 453: startIndex outside the boundaries of array
Line 454: 6
Line 455: array with multiple elements, valueToFind in array, startIndex after value-
Line 456: ToFind
Line 457: 7
Line 458: array with multiple elements, valueToFind in array, startIndex before
Line 459: valueToFind
Line 460: 8
Line 461: array with multiple elements, valueToFind in array, startIndex precisely at
Line 462: valueToFind
Line 463: 9
Line 464: array with multiple elements, valueToFind in array multiple times, start-
Line 465: Index before valueToFind
Line 466: 10
Line 467: array with multiple elements, valueToFind in array multiple times, one before
Line 468: startIndex
Line 469: 11
Line 470: array with multiple elements, valueToFind not in array
Line 471: In JUnit, the test suite looks like the following listing.
Line 472: import static org.junit.jupiter.params.provider.Arguments.of;
Line 473: public class ArrayUtilsTest {
Line 474: Listing 5.9
Line 475: First tests for the indexOf() method
Line 476: 
Line 477: --- 페이지 154 ---
Line 478: 126
Line 479: CHAPTER 5
Line 480: Property-based testing
Line 481:   @ParameterizedTest
Line 482:   @MethodSource("testCases")
Line 483:   void testIndexOf(int[] array, int valueToFind, int startIndex,
Line 484:     ➥ int expectedResult) {
Line 485:     int result = ArrayUtils.indexOf(array, valueToFind, startIndex);
Line 486:     assertThat(result).isEqualTo(expectedResult);
Line 487:   }
Line 488:   static Stream<Arguments> testCases() { 
Line 489:     int[] array = new int[] { 1, 2, 3, 4, 5, 4, 6, 7 };
Line 490:     return Stream.of(
Line 491:       of(null, 1, 1, -1), 
Line 492:       of(new int[] { 1 }, 1, 0, 0), 
Line 493:       of(new int[] { 1 }, 2, 0, -1), 
Line 494:       of(array, 1, 10, -1), 
Line 495:       of(array, 2, -1, 1), 
Line 496:       of(array, 4, 6, -1), 
Line 497:       of(array, 4, 1, 3), 
Line 498:       of(array, 4, 3, 3), 
Line 499:       of(array, 4, 1, 3), 
Line 500:       of(array, 4, 4, 5), 
Line 501:       of(array, 8, 0, -1) 
Line 502:     );
Line 503:   }
Line 504: }
Line 505: Listing 5.10 shows the test suite developed for the library method itself (http://mng
Line 506: .bz/aDAY). I added some comments, so you can see how their tests related to our
Line 507: tests. This test suite contains our test cases T1, T4, T5, T6, T7, T8, T10, and T11. Inter-
Line 508: estingly, it is not testing the behavior of the array with a single element or the case in
Line 509: which the element appears again after the first time it is found.
Line 510: @Test
Line 511: public void testIndexOfIntWithStartIndex() {
Line 512:   int[] array = null;
Line 513:   assertEquals(-1, ArrayUtils.indexOf(array, 0, 2)); 
Line 514:   array = new int[]{0, 1, 2, 3, 0};
Line 515:   assertEquals(4, ArrayUtils.indexOf(array, 0, 2)); 
Line 516:   assertEquals(-1, ArrayUtils.indexOf(array, 1, 2)); 
Line 517:   assertEquals(2, ArrayUtils.indexOf(array, 2, 2)); 
Line 518:   assertEquals(3, ArrayUtils.indexOf(array, 3, 2)); 
Line 519:   assertEquals(3, ArrayUtils.indexOf(array, 3, -1)); 
Line 520:   assertEquals(-1, ArrayUtils.indexOf(array, 99, 0)); 
Line 521: Listing 5.10
Line 522: Original test suite of the indexOf() method
Line 523: All the test cases we engineered 
Line 524: are implemented here.
Line 525: T1
Line 526: T2
Line 527: T3
Line 528: T4
Line 529: T5
Line 530: T6
Line 531: T7
Line 532: T8
Line 533: T9
Line 534: T10
Line 535: T11
Line 536: Similar to test case T1
Line 537: Similar to test case T10
Line 538: Similar to test case T6
Line 539: Similar to test case T8
Line 540: Similar to test case T7
Line 541: Similar to test case T4
Line 542: Similar to test case T11
Line 543: 
Line 544: --- 페이지 155 ---
Line 545: 127
Line 546: Example 3: Testing the indexOf method
Line 547:   assertEquals(-1, ArrayUtils.indexOf(array, 0, 6)); 
Line 548: }
Line 549: NOTE
Line 550: Parameterized tests seem to be less popular in open source systems.
Line 551: For methods with simple signatures, inputs, and outputs, like indexOf, we
Line 552: could argue that parameterized tests are overkill. When creating this exam-
Line 553: ple, I considered writing two different traditional JUnit test cases: one con-
Line 554: taining only the exceptional behavior and another containing the remaining
Line 555: test cases. In the end, organizing test cases is a matter of personal taste—talk
Line 556: to your team and see what approach they prefer. We talk more about test
Line 557: code quality and readability in chapter 10.
Line 558: Both test suites look good and are quite strong. But now, let’s express the main behav-
Line 559: ior of the method via property-based testing.
Line 560:  The overall idea of the test is to insert a random value in a random position of a
Line 561: random array. The indexOf() method will look for this random value. Finally, the test
Line 562: will assert that the method returns an index that matches the random position where
Line 563: we inserted the element.
Line 564:  The tricky part of writing such a test is ensuring that the random value we add in the
Line 565: array does not already exist in the random array. If the value is already there, this may
Line 566: break our test. Consider a randomly generated array containing [1, 2, 3, 4]: if we
Line 567: insert a random element 4 (which already exists in the array) on index 1 of the array,
Line 568: we will get a different response depending on whether startIndex is 0 or 3. To avoid
Line 569: such confusion, we generate random values that do not exist in the randomly gener-
Line 570: ated array. This is easily achievable in jqwik. The property-based test needs at least four
Line 571: parameters:
Line 572: 
Line 573: numbers—A list of random integers (we generate a list, as it is much easier to
Line 574: add an element at a random position in a list than in an array). This list will
Line 575: have a size of 100 and will contain values between –1000 and 1000.
Line 576: 
Line 577: value—A random integer that is the value to be inserted into the list. We gener-
Line 578: ate values ranging from 1001 to 2000, ensuring that whatever value is generated
Line 579: will not exist in the list.
Line 580: 
Line 581: indexToAddElement—A random integer that represents a random index for
Line 582: where to add this element. The index ranges from 0 to 99 (the list has size 100).
Line 583: 
Line 584: startIndex—A random integer that represents the index where we ask the
Line 585: method to start the search. This is also a random number ranging from 0 to 99.
Line 586: With all the random values ready, the method adds the random value at the random
Line 587: position and calls indexOf with the random array, the random value to search, and the
Line 588: random index at which to start the search. We then assert that the method returns
Line 589: indexToAddElement if indexToAddElement >= startIndex (that is, the element was
Line 590: inserted after the start index) or –1 if the element was inserted before the start index.
Line 591: Figure 5.1 illustrates this process.
Line 592:  The concrete implementation of the jqwik test can be found in listing 5.11.
Line 593: Similar to test case T5
Line 594: 
Line 595: --- 페이지 156 ---
Line 596: 128
Line 597: CHAPTER 5
Line 598: Property-based testing
Line 599: @Property
Line 600: void indexOf(
Line 601:   @ForAll
Line 602:   @Size(value = 100) List<@IntRange(min = -1000, max = 1000)
Line 603:   ➥ Integer> numbers, 
Line 604:   @ForAll
Line 605:   @IntRange(min = 1001, max = 2000) int value, 
Line 606:   @ForAll
Line 607:   @IntRange(max = 99) int indexToAddElement, 
Line 608:   @ForAll
Line 609:   @IntRange(max = 99) int startIndex) { 
Line 610:  numbers.add(indexToAddElement, value); 
Line 611:  int[] array = convertListToArray(numbers); 
Line 612:  int expectedIndex = indexToAddElement >= startIndex ?
Line 613:    indexToAddElement : -1;  
Line 614:  assertThat(ArrayUtils.indexOf(array, value, startIndex))
Line 615:    .isEqualTo(expectedIndex); 
Line 616: }
Line 617: private int[] convertListToArray(List<Integer> numbers) { 
Line 618:   int[] array = numbers.stream().mapToInt(x -> x).toArray();
Line 619:   return array;
Line 620: }
Line 621: Listing 5.11
Line 622: Property-based test for the indexOf() method
Line 623: 5
Line 624: 6
Line 625: …
Line 626: 31
Line 627: –1
Line 628: …
Line 629: 89
Line 630: 87
Line 631: numbers =
Line 632: 0
Line 633: 1
Line 634: 2
Line 635: 56
Line 636: 57
Line 637: 100
Line 638: 1500
Line 639: value =
Line 640: Lots of random unique
Line 641: integers. This list has a
Line 642: size of 00 (after the
Line 643: 1
Line 644: element is inserted,
Line 645: size = 0 ).
Line 646: 1 1
Line 647: This value is not
Line 648: in the original list.
Line 649: 58
Line 650: indexToAdd
Line 651: Element =
Line 652: 1
Line 653: startIndex =
Line 654: 1500
Line 655: 58
Line 656: Where to start looking. It may
Line 657: be before or after the position
Line 658: at which we inserted the element.
Line 659: The index at which to insert
Line 660: the element we will search for
Line 661: Figure 5.1
Line 662: The data generation of the property-based test for the indexOf method
Line 663: Generates a list with 100 numbers 
Line 664: ranging from -1000 to 1000
Line 665: Generates a random number that we
Line 666: insert into the array. This number is
Line 667: outside the range of the list so we
Line 668: can find it easily.
Line 669: Randomly picks a 
Line 670: place to put the 
Line 671: element in the list
Line 672: Randomly picks a 
Line 673: number to start the 
Line 674: search in the array
Line 675: Adds the number to 
Line 676: the list at the randomly 
Line 677: chosen position
Line 678: Converts the list to an array, since 
Line 679: this is what the method expects
Line 680: If we added the element after the start index, 
Line 681: we expect the method to return the position 
Line 682: where we inserted the element. Otherwise we 
Line 683: expect the method to return -1.
Line 684: Asserts that the 
Line 685: search for the value 
Line 686: returns the index 
Line 687: we expect
Line 688: Utility method that
Line 689: converts a list of
Line 690: integers to an array
Line 691: 
Line 692: --- 페이지 157 ---
Line 693: 129
Line 694: Example 4: Testing the Basket class
Line 695: Jqwik will generate a large number of random inputs for this method, ensuring that
Line 696: regardless of where the value to find is, and regardless of the chosen start index, the
Line 697: method will always return the expected index. Notice how this property-based test bet-
Line 698: ter exercises the properties of the method than the testing method we used earlier.
Line 699:  I hope this example shows you that writing property-based tests requires creativity.
Line 700: Here, we had to come up with the idea of generating a random value that is never in
Line 701: the list so that the indexOf method could find it without ambiguity. We also had to be
Line 702: creative when doing the assertion, given that the randomly generated indexToAdd-
Line 703: Element could be larger or smaller than the startIndex (which would drastically
Line 704: change the output). Pay attention to these two points:
Line 705: 1
Line 706: Ask yourself, “Am I exercising the property as closely as possible to the real
Line 707: world?” If you come up with input data that will be wildly different from what
Line 708: you expect in the real world, it may not be a good test.
Line 709: 2
Line 710: Do all the partitions have the same likelihood of being exercised by your test?
Line 711: In the example, the element to be found is sometimes before and sometimes
Line 712: after the start index. If you write a test in which, say, 95% of the inputs have the
Line 713: element before the start index, you may be biasing your test too much. You
Line 714: want all the partitions to have the same likelihood of being exercised.
Line 715: In the example code, given that both indexToAddElement and startIndex
Line 716: are random numbers between 0 and 99, we expect about a 50-50 split between
Line 717: the partitions. When you are unsure about the distribution, add some debug-
Line 718: ging instructions and see what inputs or partitions your test generates or
Line 719: exercises. 
Line 720: 5.4
Line 721: Example 4: Testing the Basket class
Line 722: Let’s explore one last example that revisits the Basket class from chapter 4. The class
Line 723: offers two methods: an add() method that receives a product and adds it a quantity
Line 724: of times to the basket, and a remove() method that removes a product completely
Line 725: from the cart. Let’s start with the add method.
Line 726: import static java.math.BigDecimal.valueOf;
Line 727: public class Basket {
Line 728:   private BigDecimal totalValue = BigDecimal.ZERO;
Line 729:   private Map<Product, Integer> basket = new HashMap<>();
Line 730:   public void add(Product product, int qtyToAdd) {
Line 731:     assert product != null : "Product is required";               
Line 732:     assert qtyToAdd > 0 : "Quantity has to be greater than zero"; 
Line 733:     BigDecimal oldTotalValue = totalValue; 
Line 734: Listing 5.12
Line 735: Implementation of Baskets add method
Line 736: Checks all the
Line 737: pre-conditions
Line 738: Stores the old value so we can check 
Line 739: the post-condition later
Line 740: 
Line 741: --- 페이지 158 ---
Line 742: 130
Line 743: CHAPTER 5
Line 744: Property-based testing
Line 745:     int existingQuantity = basket.getOrDefault(product, 0); 
Line 746:     int newQuantity = existingQuantity + qtyToAdd;
Line 747:     basket.put(product, newQuantity);
Line 748:     BigDecimal valueAlreadyInTheCart = product.getPrice()
Line 749:       .multiply(valueOf(existingQuantity)); 
Line 750:     BigDecimal newFinalValueForTheProduct = product.getPrice()
Line 751:       .multiply(valueOf(newQuantity));      
Line 752:     totalValue = totalValue
Line 753:       .subtract(valueAlreadyInTheCart)
Line 754:       .add(newFinalValueForTheProduct); 
Line 755:     assert basket.containsKey(product) : "Product was not inserted in     
Line 756:     ➥ the basket";                                                       
Line 757:     assert totalValue.compareTo(oldTotalValue) == 1 : "Total value should 
Line 758:     ➥ be greater than previous total value";                             
Line 759:     assert invariant() : "Invariant does not hold";                       
Line 760:   }
Line 761: }
Line 762: The implementation is straightforward. First it does the pre-condition checks we dis-
Line 763: cussed in chapter 4. The product cannot be null, and the quantity of the product to
Line 764: be added to the cart has to be larger than zero. Then the method checks whether the
Line 765: basket already contains the product. If so, it adds the quantity on top of the quantity
Line 766: already in the cart. It then calculates the value to add to the total value of the basket.
Line 767: To do so, it calculates the value of that product based on the previous amount in the
Line 768: basket, subtracts that from the total value, and then adds the new total value for that
Line 769: product. Finally, it ensures that the invariant (the total value of the basket must be
Line 770: positive) still holds.
Line 771:  The remove method is simpler than the add method. It looks for the product in
Line 772: the basket, calculates the amount it needs to remove from the total value of the bas-
Line 773: ket, subtracts it, and removes the product (listing 5.13). The method also ensures
Line 774: the same two pre-conditions we discussed before: the product cannot be null, and
Line 775: the product has to be in the basket.
Line 776: public void remove(Product product) {
Line 777:     assert product != null : "product can't be null";                 
Line 778:     assert basket.containsKey(product) : "Product must already be in  
Line 779:     ➥ the basket";                                                   
Line 780:     int qty = basket.get(product);
Line 781:     BigDecimal productPrice = product.getPrice();             
Line 782:     BigDecimal productTimesQuantity = productPrice.multiply(  
Line 783:       ➥ valueOf(qty));                                       
Line 784:     totalValue = totalValue.subtract(productTimesQuantity);   
Line 785: Listing 5.13
Line 786: Implementation of Baskets remove method
Line 787: If the product 
Line 788: is already in the 
Line 789: cart, add to it.
Line 790: Calculates the
Line 791: previous and the
Line 792: new value of the
Line 793: product for the
Line 794: relevant quantities
Line 795: Subtracts the previous value of the 
Line 796: product from the total value of the 
Line 797: basket and adds the new final value 
Line 798: of the product to it
Line 799: Post-conditions and 
Line 800: invariant checks
Line 801: Pre-
Line 802: conditions
Line 803: check
Line 804: Calculates the 
Line 805: amount that 
Line 806: should be removed 
Line 807: from the basket
Line 808: 
Line 809: --- 페이지 159 ---
Line 810: 131
Line 811: Example 4: Testing the Basket class
Line 812:     basket.remove(product); 
Line 813:     assert !basket.containsKey(product) : "Product is still  
Line 814:     ➥ in the basket";                                       
Line 815:     assert invariant() : "Invariant does not hold";          
Line 816:   }
Line 817: A developer who did not read the chapters on specification-based testing and struc-
Line 818: tural testing would come up with at least three tests: one to ensure that add() adds the
Line 819: product to the cart, another to ensure that the method behaves correctly when
Line 820: the same product is added twice, and one to ensure that remove() indeed removes
Line 821: the product from the basket. Then they would probably add a few tests for the excep-
Line 822: tional cases (which in this class are clearly specified in the contracts). Here are the
Line 823: automated test cases.
Line 824: import static java.math.BigDecimal.valueOf;
Line 825: public class BasketTest {
Line 826:   private Basket basket = new Basket();
Line 827:   @Test
Line 828:   void addProducts() { 
Line 829:     basket.add(new Product("TV", valueOf(10)), 2);
Line 830:     basket.add(new Product("Playstation", valueOf(100)), 1);
Line 831:     assertThat(basket.getTotalValue())
Line 832:         .isEqualByComparingTo(valueOf(10*2 + 100*1));
Line 833:   }
Line 834:   @Test
Line 835:   void addSameProductTwice() { 
Line 836:     Product p = new Product("TV", valueOf(10));
Line 837:     basket.add(p, 2);
Line 838:     basket.add(p, 3);
Line 839:     assertThat(basket.getTotalValue())
Line 840:         .isEqualByComparingTo(valueOf(10*5));
Line 841:   }
Line 842:   @Test
Line 843:   void removeProducts() { 
Line 844:     basket.add(new Product("TV", valueOf(100)), 1);
Line 845:     Product p = new Product("PlayStation", valueOf(10));
Line 846:     basket.add(p, 2);
Line 847:     basket.remove(p);
Line 848:     assertThat(basket.getTotalValue())
Line 849:         .isEqualByComparingTo(valueOf(100)); 
Line 850:   }
Line 851: Listing 5.14
Line 852: Non-systematic tests for the Basket class
Line 853: Removes the product 
Line 854: from the hashmap
Line 855: Post-conditions 
Line 856: and invariant 
Line 857: check
Line 858: Ensures that 
Line 859: products are added 
Line 860: to the basket
Line 861: If the same product is 
Line 862: added twice, the basket 
Line 863: sums up the quantities.
Line 864: Ensures that products are 
Line 865: removed from the basket
Line 866: Food for thought: is this 
Line 867: assertion enough? You 
Line 868: might also want to verify 
Line 869: that PlayStation is not in 
Line 870: the basket.
Line 871: 
Line 872: --- 페이지 160 ---
Line 873: 132
Line 874: CHAPTER 5
Line 875: Property-based testing
Line 876:   // tests for exceptional cases...
Line 877: }
Line 878: NOTE
Line 879: I used the isEqualByComparingTo assert instruction. Remember that
Line 880: BigDecimals are instances of a strange class, and the correct way to compare
Line 881: one BigDecimal to another is with the compareTo() method. That is what the
Line 882: isEqualByComparingTo assertion does. Again, the BigDecimal class is not
Line 883: easy to handle.
Line 884: The problem with these tests is that they do not exercise the feature extensively. If
Line 885: there is a bug in our implementation, it is probably hidden and will only appear after
Line 886: a long and unexpected sequence of adds and removes to and from the basket. Finding
Line 887: this specific sequence might be hard to see, even after proper domain and structural
Line 888: testing. However, we can express it as a property: given any arbitrary sequence of addi-
Line 889: tions and removals, the basket still calculates the correct final amount. We have to cus-
Line 890: tomize jqwik so that it understands how to randomly call a sequence of add()s and
Line 891: remove()s, as shown in figure 5.2.
Line 892: Fasten your seatbelt, because this takes a lot of code. The first step is to create a bunch
Line 893: of jqwik Actions to represent the different actions that can happen with the basket.
Line 894: Actions are a way to explain to the framework how to execute a more complex action.
Line 895: In our case, two things can happen: we can add a product to the basket, or we can
Line 896: remove a product from the basket. We define how these two actions work so that later,
Line 897: jqwik can generate a random sequence of actions.
Line 898:  Let’s start with the add action. It will receive a Product and a quantity and insert
Line 899: the Product into the Basket. The action will then ensure that the Basket behaved as
Line 900: expected by comparing its current total value against the expected value. Note that
Line 901: everything happens in the run() method: this method is defined by jqwik’s Action
Line 902: interface, which our action implements. In practice, jqwik will call this method when-
Line 903: ever it generates an add action and passes the current basket to the run method. The
Line 904: following listing shows the implementation of the AddAction class.
Line 905:  
Line 906: Add
Line 907: Remove
Line 908: Add
Line 909: Add
Line 910: Remove
Line 911: Add
Line 912: Add
Line 913: Add
Line 914: Remove
Line 915: Add
Line 916: Add
Line 917: Add
Line 918: Add
Line 919: Remove
Line 920: Add
Line 921: Remove Remove
Line 922: T1 =
Line 923: T2 =
Line 924: T3 =
Line 925: We want to call arbitrary sequences
Line 926: of adds and removes and assert that
Line 927: the basket is still in a correct state.
Line 928: T4 =
Line 929: ….
Line 930: Figure 5.2
Line 931: We want our test to call arbitrary sequences of add and remove 
Line 932: actions.
Line 933: 
Line 934: --- 페이지 161 ---
Line 935: 133
Line 936: Example 4: Testing the Basket class
Line 937: class AddAction
Line 938:   implements Action<Basket> { 
Line 939:   private final Product product;
Line 940:   private final int qty;
Line 941:   public AddAction(Product product, int qty) { 
Line 942:     this.product = product;
Line 943:     this.qty = qty;
Line 944:   }
Line 945:   @Override
Line 946:   public Basket run(Basket basket) { 
Line 947:     BigDecimal currentValue = basket.getTotalValue(); 
Line 948:     basket.add(product, qty); 
Line 949:     BigDecimal newProductValue = product.getPrice()
Line 950:       .multiply(valueOf(qty));
Line 951:     BigDecimal newValue = currentValue.add(newProductValue);
Line 952:     assertThat(basket.getTotalValue())
Line 953:       .isEqualByComparingTo(newValue); 
Line 954:     return basket; 
Line 955:   }
Line 956: }
Line 957: Now let’s implement the remove action. This is tricky: we need a way to get the set of
Line 958: products that are already in the basket and their quantities. Note that we do not
Line 959: have such a method in the Basket class. The simplest thing to do is add such a
Line 960: method to the class.
Line 961:  You might be thinking that adding more methods for the tests is a bad idea. It’s a
Line 962: trade-off. I often favor anything that eases testing. An extra method will not hurt and
Line 963: will help our testing, so I’d do it, as shown next.
Line 964: class Basket {
Line 965:   // ... the code of the class here ...
Line 966:   public int quantityOf(Product product) { 
Line 967:     assert basket.containsKey(product);
Line 968:     return basket.get(product);
Line 969:   }
Line 970:   public Set<Product> products() { 
Line 971:     return Collections.unmodifiableSet(basket.keySet());
Line 972:   }
Line 973: }
Line 974: Listing 5.15
Line 975: The AddAction action
Line 976: Listing 5.16
Line 977: Basket class modified to support the test
Line 978: Actions have to implement the 
Line 979: jqwik Action interface.
Line 980: The constructor receives 
Line 981: a product and a quantity. 
Line 982: These values will be randomly 
Line 983: generated later by jqwik.
Line 984: The run method receives a 
Line 985: Basket and, in this case, adds 
Line 986: a new random product to it.
Line 987: Gets the current total 
Line 988: value of the basket, 
Line 989: so we can make the 
Line 990: assertion later
Line 991: Adds the
Line 992: product to
Line 993: the basket
Line 994: Asserts that the value of the basket 
Line 995: is correct after the addition
Line 996: Returns the current basket so 
Line 997: the next action starts from it
Line 998: We only return the quantity if 
Line 999: the product is in the cart. Note 
Line 1000: that here, we could have gone 
Line 1001: for a weaker pre-condition: for 
Line 1002: example, if the product is not 
Line 1003: in the basket, return 0.
Line 1004: Returns a copy of 
Line 1005: the set, not the 
Line 1006: original one!
Line 1007: 
Line 1008: --- 페이지 162 ---
Line 1009: 134
Line 1010: CHAPTER 5
Line 1011: Property-based testing
Line 1012: The remove action picks a random product from the basket, removes it, and then
Line 1013: ensures that the current total value is the total value minus the value of the product
Line 1014: that was just removed. The pickRandom() method chooses a random product from
Line 1015: the set of products; I do not show the code here, to save space, but you can find it in
Line 1016: the book’s code repository.
Line 1017: class RemoveAction implements Action<Basket> {
Line 1018:   @Override
Line 1019:   public Basket run(Basket basket) {
Line 1020:     BigDecimal currentValue = basket.getTotalValue(); 
Line 1021:     Set<Product> productsInBasket = basket.products(); 
Line 1022:     if(productsInBasket.isEmpty()) {
Line 1023:       return basket;
Line 1024:     }
Line 1025:     Product randomProduct = pickRandom(productsInBasket); 
Line 1026:     double currentProductQty = basket.quantityOf(randomProduct);
Line 1027:     basket.remove(randomProduct);
Line 1028:     BigDecimal basketValueWithoutRandomProduct = currentValue
Line 1029:       .subtract(randomProduct.getPrice()
Line 1030:       .multiply(valueOf(currentProductQty))); 
Line 1031:     assertThat(basket.getTotalValue())
Line 1032:       .isEqualByComparingTo(basketValueWithoutRandomProduct); 
Line 1033:     return basket; 
Line 1034:   }
Line 1035:   // ...
Line 1036: }
Line 1037: Jqwik now knows how to call add() (via AddAction) and remove() (via RemoveAction).
Line 1038: The next step is to explain how to instantiate random products and sequences of
Line 1039: actions. Let’s start by explaining to jqwik how to instantiate an arbitrary AddAction.
Line 1040: First we randomly pick a product from a predefined list of products. Then we gener-
Line 1041: ate a random quantity value. Finally, we add the random product in the random quan-
Line 1042: tity to the basket.
Line 1043: class BasketTest {
Line 1044:   // ...
Line 1045:   private Arbitrary<AddAction> addAction() {
Line 1046:     Arbitrary<Product> products = Arbitraries.oneOf( 
Line 1047:       randomProducts
Line 1048:         .stream()
Line 1049:         .map(product -> Arbitraries.of(product))
Line 1050:         .collect(Collectors.toList()));
Line 1051: Listing 5.17
Line 1052: The RemoveAction class
Line 1053: Listing 5.18
Line 1054: Instantiating add actions
Line 1055: Gets the current
Line 1056: value of the
Line 1057: basket for the
Line 1058: assertion later
Line 1059: If the basket is 
Line 1060: empty, we skip this 
Line 1061: action. This may 
Line 1062: happen, as we do not 
Line 1063: control the sequence 
Line 1064: jqwik generates.
Line 1065: Picks a
Line 1066: random
Line 1067: element in
Line 1068: the basket
Line 1069: to be
Line 1070: removed
Line 1071: Calculates the new 
Line 1072: value of the basket
Line 1073: Asserts the value of the
Line 1074: basket without the random
Line 1075: product we removed
Line 1076: Returns the current 
Line 1077: basket so the next action 
Line 1078: can continue from here
Line 1079: Creates an arbitrary 
Line 1080: product out of the 
Line 1081: list of predefined 
Line 1082: products
Line 1083: 
Line 1084: --- 페이지 163 ---
Line 1085: 135
Line 1086: Example 4: Testing the Basket class
Line 1087:     Arbitrary<Integer> qtys =
Line 1088:       Arbitraries.integers().between(1, 100); 
Line 1089:     return Combinators
Line 1090:         .combine(products, qtys)
Line 1091:         .as((product, qty) -> new AddAction(product, qty)); 
Line 1092:   }
Line 1093:   static List<Product> randomProducts = new ArrayList<>() {{   
Line 1094:     add(new Product("TV", new BigDecimal("100")));
Line 1095:     add(new Product("PlayStation", new BigDecimal("150.3")));
Line 1096:     add(new Product("Refrigerator", new BigDecimal("180.27")));
Line 1097:     add(new Product("Soda", new BigDecimal("2.69")));
Line 1098:   }};
Line 1099: }
Line 1100: This is a complex piece of code, and it involves a lot of details about how jqwik works.
Line 1101: Let’s digest it step by step:
Line 1102: 1
Line 1103: Our first goal is to randomly select an arbitrary Product from the list of products.
Line 1104: To do so, we use jqwik’s Arbitraries.oneOf() method, which randomly picks an
Line 1105: arbitrary element of a given set of options. Given that the oneOf method needs a
Line 1106: List<Arbitrary<Product>>, we have to convert our randomProducts (which
Line 1107: is a List<Product>). This is easily done using Java’s Stream API.
Line 1108: 2
Line 1109: We generate a random integer that will serve as the quantity to pass to the add()
Line 1110: method. We define an Arbitrary<Integer> with numbers between 1 and 100
Line 1111: (random choices that I made after exploring the method’s source code).
Line 1112: 3
Line 1113: We return an AddAction that is instantiated using a combination of arbitrary
Line 1114: products and quantities.
Line 1115: We can now create our test. The property test should receive an ActionSequence, which
Line 1116: we define as an arbitrary sequence of AddActions and RemoveActions. We do so with the
Line 1117: Arbitraries.sequences() method. Let’s define this in an addsAndRemoves method.
Line 1118:  We also need arbitrary remove actions, as we did for add actions, but this is much
Line 1119: simpler since the RemoveAction class does not receive anything in its constructor. So,
Line 1120: we use Arbitraries.of().
Line 1121: private Arbitrary<RemoveAction> removeAction() {
Line 1122:   return Arbitraries.of(new RemoveAction()); 
Line 1123: }
Line 1124: @Provide
Line 1125: Arbitrary<ActionSequence<Basket>> addsAndRemoves() {
Line 1126:   return Arbitraries.sequences(Arbitraries.oneOf( 
Line 1127:       addAction(),
Line 1128:       removeAction()));
Line 1129: }
Line 1130: Listing 5.19
Line 1131: Adding remove actions to the test
Line 1132: Creates arbitrary 
Line 1133: quantities
Line 1134: Combines products 
Line 1135: and quantities, and 
Line 1136: generates AddActions
Line 1137: A static list of 
Line 1138: hard-coded 
Line 1139: products
Line 1140: Returns an arbitrary 
Line 1141: remove action
Line 1142: This is where the magic 
Line 1143: happens: jqwik generates 
Line 1144: random sequences of add 
Line 1145: and remove actions.
Line 1146: 
Line 1147: --- 페이지 164 ---
Line 1148: 136
Line 1149: CHAPTER 5
Line 1150: Property-based testing
Line 1151: We now only need a @Property test method that runs the different sequences of
Line 1152: actions generated by the addsAndRemoves method.
Line 1153: @Property
Line 1154: void sequenceOfAddsAndRemoves(
Line 1155:   @ForAll("addsAndRemoves") 
Line 1156:   ActionSequence<Basket> actions) {
Line 1157:     actions.run(new Basket());
Line 1158: }
Line 1159: And we are finished. As soon as we run the test, jqwik randomly invokes sequences of
Line 1160: adds and removes, passing random Products and quantities and ensuring that the
Line 1161: value of the basket is always correct.
Line 1162:  This was a long, complex property-based test, and you may be wondering if it is
Line 1163: worth the effort. For this specific Basket implementation, I would probably write thor-
Line 1164: ough example-based tests. But I hope this example illustrates the power of property-
Line 1165: based testing. Although they tend to be more complicated than traditional example-
Line 1166: based tests, you will get used to it, and you will soon be writing them quickly. 
Line 1167: 5.5
Line 1168: Example 5: Creating complex domain objects
Line 1169: Building more complex objects may come in handy when testing business systems.
Line 1170: This can be done using jqwik’s Combinators feature, which we’ll use in the following
Line 1171: listing. Imagine that we have the following Book class, and we need to generate differ-
Line 1172: ent books for a property-based test.
Line 1173: public class Book {
Line 1174:   private final String title;
Line 1175:   private final String author;
Line 1176:   private final int qtyOfPages;
Line 1177:   public Book(String title, String author, int qtyOfPages) {
Line 1178:     this.title = title;
Line 1179:     this.author = author;
Line 1180:     this.qtyOfPages = qtyOfPages;
Line 1181:   }
Line 1182:   // getters...
Line 1183: }
Line 1184: One way to do this would be to have a property test that receives three parameters: a
Line 1185: String for title, a String for author, and an Integer for quantity of pages. Inside
Line 1186: the property test, we would instantiate the Book class. Jqwik offers a better way to do
Line 1187: that, as shown in the next listing.
Line 1188: Listing 5.20
Line 1189: Property-based test that generates adds and removes
Line 1190: Listing 5.21
Line 1191: A simple Book class
Line 1192: The property receives 
Line 1193: a sequence of Basket 
Line 1194: actions defined by the 
Line 1195: addsAndRemoves method.
Line 1196: 
Line 1197: --- 페이지 165 ---
Line 1198: 137
Line 1199: Property-based testing in the real world
Line 1200: public class BookTest {
Line 1201:   @Property
Line 1202:   void differentBooks(@ForAll("books") Book book) {
Line 1203:     // different books!
Line 1204:     System.out.println(book);
Line 1205:     // write your test here!
Line 1206:   }
Line 1207:   @Provide
Line 1208:   Arbitrary<Book> books() {
Line 1209:     Arbitrary<String> titles = Arbitraries.strings().withCharRange(
Line 1210:       ➥ 'a', 'z')
Line 1211:         .ofMinLength(10).ofMaxLength(100); 
Line 1212:     Arbitrary<String> authors = Arbitraries.strings().withCharRange(
Line 1213:       ➥ 'a', 'z')
Line 1214:         .ofMinLength(5).ofMaxLength(21);   
Line 1215:     Arbitrary<Integer> qtyOfPages = Arbitraries.integers().between(
Line 1216:       ➥ 0, 450); 
Line 1217:     return Combinators.combine(titles, authors, qtyOfPages)
Line 1218:         .as((title, author, pages) -> new Book(title, author, pages)); 
Line 1219:   }
Line 1220: }
Line 1221: The Combinators API lets us combine different generators to build a more complex
Line 1222: object. All we have to do is to build specific Arbitrarys for each of the attributes of the
Line 1223: complex class we want to build: in this case, one Arbitrary<String> for the title,
Line 1224: another Arbitrary<String> for the author, and one Arbitrary<Integer> for the num-
Line 1225: ber of pages. After that, we use the Combinators.combine() method, which receives a
Line 1226: series of Arbitrarys and returns an Arbitrary of the complex object. The magic hap-
Line 1227: pens in the as() method, which gives us the values we use to instantiate the object.
Line 1228:  Note how flexible jqwik is. You can build virtually any object you want. Moreover,
Line 1229: nothing prevents you from building even more realistic input values: for example,
Line 1230: instead of building random author names, we could develop something that returns
Line 1231: real people’s names. Try implementing such an arbitrary yourself. 
Line 1232: 5.6
Line 1233: Property-based testing in the real world
Line 1234: Let me give you some tips on writing property-based tests.
Line 1235: 5.6.1
Line 1236: Example-based testing vs. property-based testing
Line 1237: Property-based testing seems much fancier than example-based testing. It also explores
Line 1238: the input domain much better. Should we only use property-based testing from now on?
Line 1239:  In practice, I mix example-based testing and property-based testing. In the testing
Line 1240: workflow I propose, I use example-based testing when doing specification-based and
Line 1241: structural testing. Example-based tests are naturally simpler than property-based tests,
Line 1242: Listing 5.22
Line 1243: Using the Combinators API to generate complex objects
Line 1244: Instantiates
Line 1245: one arbitrary
Line 1246: for each of the
Line 1247: Book’s fields
Line 1248: Combines them
Line 1249: to generate an
Line 1250: instance of Book
Line 1251: 
Line 1252: --- 페이지 166 ---
Line 1253: 138
Line 1254: CHAPTER 5
Line 1255: Property-based testing
Line 1256: and they require less creativity to automate. I like that: their simplicity allows me to
Line 1257: focus on understanding the requirements and engineer better test cases. When I am
Line 1258: done with both testing techniques and have a much better grasp of the program
Line 1259: under test, I evaluate which test cases would be better as property-based tests.
Line 1260:  Do I always write property-based tests for my programs? Honestly, no. In many of the
Line 1261: problems I work on, I feel pretty confident with example-based testing. I use property-
Line 1262: based testing when I do not feel entirely secure that my example-based tests were
Line 1263: enough. 
Line 1264: 5.6.2
Line 1265: Common issues in property-based tests
Line 1266: I see three common issues in the property-based tests my students write when they
Line 1267: learn this technique. The first is requiring jqwik to generate data that is very expensive
Line 1268: or even impossible. If you ask jqwik to, say, generate an array of 100 elements in which
Line 1269: the numbers have to be unique and multiples of 2, 3, 5, and 15, such an array can be
Line 1270: difficult to find, given jqwik’s random approach. Or if you want an array with 10
Line 1271: unique elements, but you give jqwik a range of 2 to 8, the array is impossible to gener-
Line 1272: ate. In general, if jqwik is taking too long to generate the data for you, maybe you can
Line 1273: find a better way to generate the data or write the test.
Line 1274:  Second, we saw in previous chapters that boundaries are a perfect place for bugs.
Line 1275: So, we want to exercise those boundaries when writing property-based tests. Ensure
Line 1276: that you are expressing the boundaries of the property correctly. When we wrote the
Line 1277: tests for the passing-grade problem (section 5.1), we wrote arbitraries like Arbitraries
Line 1278: .floats().lessThan(1f) and Arbitraries.floats().greaterThan(10f). Jqwik will
Line 1279: do its best to generate boundary values: for example, the closest possible number to
Line 1280: 1f or the smallest possible float. The default configuration for jqwik is to mix edge
Line 1281: cases with random data points. Again, all of this will work well only if you express the
Line 1282: properties and boundaries correctly.
Line 1283:  The third caveat is ensuring that the input data you pass to the method under test
Line 1284: is fairly distributed among all the possible options. Jqwik does its best to generate well-
Line 1285: distributed inputs. For example, if you ask for an integer between 0 and 10, all the
Line 1286: numbers in the interval will have the same probability of being generated. But I have
Line 1287: seen tests that manipulate the generated data and then harm this property. For exam-
Line 1288: ple, imagine testing a method that receives three integers, a, b, and c, and returns a
Line 1289: boolean indicating whether these three sides can form a triangle. The implementa-
Line 1290: tion of this method is simple, as shown in the following listing.
Line 1291: public class Triangle {
Line 1292:   public static boolean isTriangle(int a, int b, int c) {
Line 1293:     boolean hasABadSide = a >= (b + c) || c >= (b + a) || b >= (a + c);
Line 1294:     return !hasABadSide;
Line 1295:   }
Line 1296: }
Line 1297: Listing 5.23
Line 1298: Implementation of the isTriangle method
Line 1299: 
Line 1300: --- 페이지 167 ---
Line 1301: 139
Line 1302: Summary
Line 1303: To write a property-based test for this method, we need to express two properties:
Line 1304: valid triangles and invalid triangles. If the developer generates three random integer
Line 1305: values as shown next, there is a very low chance of them forming a valid triangle.
Line 1306: @Property
Line 1307: void triangleBadTest( 
Line 1308:   @ForAll @IntRange(max = 100) int a,
Line 1309:   @ForAll @IntRange(max = 100) int b,
Line 1310:   @ForAll @IntRange(max = 100) int c) {
Line 1311:    // ... test here ...
Line 1312: }
Line 1313: The test exercises the invalid triangle property more than the valid triangle property.
Line 1314: A good property-based test for this problem would ensure that jqwik generates the
Line 1315: same number of valid and invalid triangles. The easiest way to do that would be to split
Line 1316: it into two tests: one for valid triangles and one for invalid triangles. (The solution is
Line 1317: available in the code repository.) 
Line 1318: 5.6.3
Line 1319: Creativity is key
Line 1320: Writing property-based tests requires a lot of creativity from the developer. Finding
Line 1321: ways to express the property, generating random data, and being able to assert the
Line 1322: expected behavior without knowing the concrete input is not easy. Property-based
Line 1323: testing requires more practice than traditional example-based testing: get your hands
Line 1324: dirty as soon as possible. I hope the examples have given you some ideas!
Line 1325: Exercises
Line 1326: 5.1
Line 1327: What is the main difference between example-based testing and property-based
Line 1328: testing?
Line 1329: 5.2
Line 1330: Suppose we have a method that returns true if the passed string is a palin-
Line 1331: drome or false otherwise. (A palindrome is a word or sentence that reads the
Line 1332: same backward and forward.) What properties do you see that could be tested
Line 1333: via property-based tests? Also describe how you would implement such tests.
Line 1334: 5.3
Line 1335: Find out what fuzz testing or fuzzing is. What is the difference between property-
Line 1336: based testing and fuzzing?
Line 1337: Summary
Line 1338: In property-based testing, instead of coming up with concrete examples, we
Line 1339: express the property that should hold for that method. The framework then
Line 1340: randomly generates hundreds of different inputs.
Line 1341: Listing 5.24
Line 1342: A bad property-based test for isTriangle
Line 1343: Generates three different integers. The 
Line 1344: odds are that these a, b, and c will be 
Line 1345: an invalid triangle. We therefore do not 
Line 1346: exercise the valid triangle property as 
Line 1347: much as we wanted to.
Line 1348: 
Line 1349: --- 페이지 168 ---
Line 1350: 140
Line 1351: CHAPTER 5
Line 1352: Property-based testing
Line 1353: Property-based testing does not replace specification-based testing and struc-
Line 1354: tural testing. It is one more tool to have in your belt. Sometimes traditional
Line 1355: example-based testing is enough.
Line 1356: Writing property-based tests is a tad more challenging than example-based test-
Line 1357: ing. You have to be creative to express the properties. Practice is key.