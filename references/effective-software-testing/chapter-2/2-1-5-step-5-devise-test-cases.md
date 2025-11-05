# 2.1.5 Step 5: Devise test cases (pp.39-41)

---
**Page 39**

39
The requirements say it all
Whenever we identify a boundary, we devise two tests for it, one for each side of the
boundary. For the “no substring”/“one substring” boundary, the two tests are as follows:

str contains both open and close tags, with no characters between them.

str contains both open and close tags, with characters between them.
The second test is not necessary in this case, as other tests already exercise this situa-
tion. Therefore, we can discard it. 
2.1.5
Step 5: Devise test cases
With the inputs, outputs, and boundaries properly dissected, we can generate con-
crete test cases. Ideally, we would combine all the partitions we’ve devised for each of
the inputs. The example has four categories, each with four or five partitions: the str
category with four partitions (null string, empty string, string of length 1, and string of
length > 1), the open category with four partitions (the same as str), the close cate-
gory with four partitions (also the same as str), and the (str, open, close) category
with five partitions (string does not contain either the open or close tags, string contains the
open tag but does not contain the close tag, string contains the close tag but does not contain
the open tag, string contains both the open and close tags, string contains both the open and
close tags multiple times). This means you would start with the str null partition and
combine it with the partitions of the open, close, and (str, open, close) categories.
You would end up with 4 × 4 × 4 × 5 = 320 tests. Writing 320 tests may be an effort that
will not pay off.
 In such situations, we pragmatically decide which partitions should be combined
with others and which should not. A first idea to reduce the number of tests is to test
exceptional cases only once and not combine them. For example, the null string parti-
tion may be tested only once and not more than that. What would we gain from com-
bining null string with open being null, empty, length = 1, and length > 1 as well as
with close being null, empty, length = 1, length > 1, and so on? It would not be
worth the effort. The same goes for empty string: one test may be good enough. If we
When the input contains both the “open” and “close” tags, and the length
of the substring changes from 0 to greater than 0, the program starts to
return this substring. It’s a boundary, and we should exercise it!
One substring
len(substring)
len = 0
len > 0
No
substring
Figure 2.3
Some of the boundaries in the substringsBetween() problem.


---
**Page 40**

40
CHAPTER 2
Specification-based testing
apply the same logic to the other two parameters and test them as null and empty just
once, we already drastically reduce the number of test cases.
 There may be other partitions that do not need to be combined fully. In this prob-
lem, I see two:
For the string of length 1 case, given that the string has length 1, two tests may be
enough: one where the single character in the string matches open and close,
and one where it does not.
Unless we have a good reason to believe that the program handles open and
close tags of different lengths in different ways, we do not need the four combi-
nations of (open length = 1, close length = 1), (open length > 1, close length = 1), (open
length = 1, close length > 1), and (open length > 1, close length > 1). Just (open length = 1,
close length = 1) and (open length > 1, close length > 1) are enough.
In other words, do not blindly combine partitions, as doing so may lead to less rele-
vant test cases. Looking at the implementation can also help you reduce the number
of combinations. We discuss using the source code to design test cases in chapter 3.
 In the following list, I’ve marked with an [x] partitions we will not test multiple
times:

str—Null string [x], empty string [x], length = 1 [x], length > 1

open—Null string [x], empty string [x], length = 1, length > 1

close—Null string [x], empty string [x], length = 1, length > 1

str—Null string [x], empty string [x], length = 1, length > 1
(str, open, close)—String does not contain either the open or the close tag,
string contains the open tag but does not contain the close tag, string contains
the close tag but does not contain the open tag, string contains both the open
and close tags, string contains both the open and close tags multiple times
With a clear understanding of which partitions need to be extensively tested and
which ones do not, we can derive the test cases by performing the combination. First,
the exceptional cases:
T1: str is null.
T2: str is empty.
T3: open is null.
T4: open is empty.
T5: close is null.
T6: close is empty.
Then, str length = 1:
T7: The single character in str matches the open tag.
T8: The single character in str matches the close tag.
T9: The single character in str does not match either the open or the close tag.
T10: The single character in str matches both the open and close tags.


---
**Page 41**

41
The requirements say it all
Now, str length > 1, open length = 1, close = 1:
T11: str does not contain either the open or the close tag.
T12: str contains the open tag but does not contain the close tag.
T13: str contains the close tag but does not contain the open tag.
T14: str contains both the open and close tags.
T15: str contains both the open and close tags multiple times.
Next, str length > 1, open length > 1, close > 1:
T16: str does not contain either the open or the close tag.
T17: str contains the open tag but does not contain the close tag.
T18: str contains the close tag but does not contain the open tag.
T19: str contains both the open and close tags.
T20: str contains both the open and close tags multiple times.
Finally, here is the test for the boundary:
T21: str contains both the open and close tags with no characters between
them.
We end up with 21 tests. Note that deriving them did not require much creativity: the
process we followed was systematic. This is the idea!
2.1.6
Step 6: Automate the test cases
It is now time to transform the test cases into automated JUnit tests. Writing those tests
is mostly a mechanical task. The creative part is coming up with inputs to exercise the
specific partition and understanding the correct program output for that partition.
 The automated test suite is shown in listings 2.3 through 2.7. They are long but
easy to understand. Each call to the substringsBetween method is one of our test
cases. The 21 calls to it are spread over the test methods, each matching the test cases
we devised earlier.
 First are the tests related to the string being null or empty.
import org.junit.jupiter.api.Test;
import static ch2.StringUtils.substringsBetween;
import static org.assertj.core.api.Assertions.assertThat;
public class StringUtilsTest {
  @Test
  void strIsNullOrEmpty() {
    assertThat(substringsBetween(null, "a", "b"))     
      .isEqualTo(null);
Listing 2.3
Tests for substringsBetween, part 1
This first call to 
substringsBetween 
is our test T1.


