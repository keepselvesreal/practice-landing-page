# 2.1.6 Step 6: Automate the test cases (pp.41-43)

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


---
**Page 42**

42
CHAPTER 2
Specification-based testing
    assertThat(substringsBetween("", "a", "b"))  
      .isEqualTo(new String[]{});
  }
}
Next are all the tests related to open or close being null or empty.
  @Test
  void openIsNullOrEmpty() {
    assertThat(substringsBetween("abc", null, "b")).isEqualTo(null);
    assertThat(substringsBetween("abc", "", "b")).isEqualTo(null);
  }
  @Test
  void closeIsNullOrEmpty() {
    assertThat(substringsBetween("abc", "a", null)).isEqualTo(null);
    assertThat(substringsBetween("abc", "a", "")).isEqualTo(null);
  }
Now come all the tests related to string and open and close tags with length 1.
  @Test
  void strOfLength1() {
    assertThat(substringsBetween("a", "a", "b")).isEqualTo(null);
    assertThat(substringsBetween("a", "b", "a")).isEqualTo(null);
    assertThat(substringsBetween("a", "b", "b")).isEqualTo(null);
    assertThat(substringsBetween("a", "a", "a")).isEqualTo(null);
  }
  @Test
  void openAndCloseOfLength1() {
    assertThat(substringsBetween("abc", "x", "y")).isEqualTo(null);
    assertThat(substringsBetween("abc", "a", "y")).isEqualTo(null);
    assertThat(substringsBetween("abc", "x", "c")).isEqualTo(null);
    assertThat(substringsBetween("abc", "a", "c"))
      .isEqualTo(new String[] {"b"});
    assertThat(substringsBetween("abcabc", "a", "c"))
      .isEqualTo(new String[] {"b", "b"});
  }
Then we have the tests for the open and close tags of varying sizes.
  @Test
  void openAndCloseTagsOfDifferentSizes() {
    assertThat(substringsBetween("aabcc", "xx", "yy")).isEqualTo(null);  
    assertThat(substringsBetween("aabcc", "aa", "yy")).isEqualTo(null);
Listing 2.4
Tests for substringsBetween, part 2
Listing 2.5
Tests for substringsBetween, part 3
Listing 2.6
Tests for substringsBetween, part 4
Test T2


---
**Page 43**

43
The requirements say it all
    assertThat(substringsBetween("aabcc", "xx", "cc")).isEqualTo(null);
    assertThat(substringsBetween("aabbcc", "aa", "cc"))
      .isEqualTo(new String[] {"bb"});
    assertThat(substringsBetween("aabbccaaeecc", "aa", "cc"))
      .isEqualTo(new String[] {"bb", "ee"});
  }
Finally, here is the test for when there is no substring between the open and close tags.
@Test
void noSubstringBetweenOpenAndCloseTags() {
  assertThat(substringsBetween("aabb", "aa", "bb"))
    .isEqualTo(new String[] {""});
  }
}
I decided to group the assertions in five different methods. They almost match my
groups when engineering the test cases in step 5. The only difference is that I broke
the exceptional cases into three test methods: strIsNullOrEmpty, openIsNullOr-
Empty, and closeIsNullOrEmpty.
 Some developers would vouch for a single method per test case, which would
mean 21 test methods, each containing one method call and one assertion. The
advantage would be that the test method’s name would clearly describe the test case.
JUnit also offers the ParameterizedTest feature (http://mng.bz/voKp), which could
be used in this case.
 I prefer simple test methods that focus on one test case, especially when imple-
menting complex business rules in enterprise systems. But in this case, there are lots
of inputs to test, and many of them are variants of a larger partition, so it made more
sense to me to code the way I did.
 Deciding whether to put all tests in a single method or in multiple methods is
highly subjective. We discuss test code quality and how to write tests that are easy to
understand and debug in chapter 10.
 Also note that sometimes there are values we do not care about. For example, con-
sider test case 1: str is null. We do not care about the values we pass to the open and
close tags here. My usual approach is to select reasonable values for the inputs I do
not care about—that is, values that will not interfere with the test. 
2.1.7
Step 7: Augment the test suite with creativity and experience
Being systematic is good, but we should never discard our experience. In this step, we
look at the partitions we’ve devised and see if we can develop interesting variations.
Variation is always a good thing to have in testing.
 In the example, when revisiting the tests, I noticed that we never tried strings with
spaces. I decided to engineer two extra tests based on T15 and T20, both about “str
contains both open and close tags multiple times”: one for open and close tags with
Listing 2.7
Tests for substringsBetween, part 5


