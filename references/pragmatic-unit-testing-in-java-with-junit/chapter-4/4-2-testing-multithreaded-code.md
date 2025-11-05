# 4.2 Testing Multithreaded Code (pp.79-84)

---
**Page 79**

try TDD and write tests first for all unit behaviors, you’ll still find yourself
sneaking in untested logic over time.
As you’re learning, lean on the visual red-yellow-and-green annotations that
the tools produce.
Use code-coverage tools to help you understand where your code
lacks coverage or where your team is trending downward.
Do your best to avoid the code coverage metric debate and convince your
leadership that the metric is not for them. It will ultimately create problems
when used for anything but educational purposes.
Testing Multithreaded Code
It’s hard enough to write code that works as expected. That’s one reason to
write unit tests. It’s dramatically harder to write concurrent code that works
and even harder to verify that it’s safe enough to ship.
In one sense, testing application code that requires concurrent processing is
technically out of the realm of unit testing. It’s better classified as integration
testing. You’re verifying that you can integrate the notion of your application-
specific logic with the ability to execute portions of it concurrently.
Tests for threaded code tend to be slower because you must expand the scope
of execution time to ensure that you have no concurrency issues. Threading
defects sometimes sneakily lie in wait, surfacing long after you thought you’d
stomped them all out.
There are piles of ways to approach multithreading in Java and, similarly,
piles of ways for your implementation to go wrong: deadlock, race conditions,
livelock, starvation, and thread interference, to name a few. One could fill a
book (or at least several chapters) covering how to test for and correct all of
these policies. I’m not allowed to fill that much paper, so you’ll see only a
short example that highlights a couple of key thoughts.
Tips for Testing Multithreaded Code
Here’s a short list of techniques for designing and analyzing multithreaded
code that minimizes concurrency issues:
• Minimize the overlap between threading controls and application code.
Rework your design so that you can unit test the bulk of application
report erratum  •  discuss
Testing Multithreaded Code • 79


---
**Page 80**

code in the absence of threads. Write thread-focused tests for the small
remainder of the code.
• Trust the work of others. Java incorporates Doug Lea’s set of concurrency
utility classes in java.util.concurrent. Don’t code producer/consumer yourself
by hand, for example; it’s too easy to get wrong. Do take advantage of
Lea’s BlockingQueue implementations, and capitalize on his painstaking
efforts to get them right.
• Avoid and isolate concurrent updates, which cause most problems.
• Profile the codebase using static concurrency analysis tools, which can
identify potential problems (including deadlocks) based on coded interac-
tions between threads.
• Profile the runtime behavior of your system using dynamic analysis tooling
such as VisualVM or YourKit. These tools can monitor thread state, ana-
lyze thread dumps, detect deadlocks, and more.
• Write a test that demonstrates a potential concurrency problem, then
exacerbate it to the point where the test always fails. You might reduce
the number of threads, increase the number of requests being tested, or
temporarily introduce sleep to expose timing issues. Tools like Thread
Weaver can also help you force and test different thread interleavings.
– Add only the concurrency control that makes the test pass. Syn-
chronization blocks and locks may be necessary, but using them
inappropriately can degrade performance (while still not solving
the real concurrency problems).
– When your fix consistently passes, remove any artificialities like sleep.
• Don’t introduce concurrency controls like locks, synchronized blocks, or
atomic variables until you’ve actually demonstrated a concurrency problem
(hopefully with a failing test).
Let’s take a quick look at one example of fixing a concurrency issue.
Exacerbating a Threading Issue
You’ll work on a bit of code from iloveyouboss, a job-search website designed
to compete with sites like Indeed and Monster. It takes a different approach to
the typical job posting site: It attempts to match prospective employees with
potential employers and vice versa, much as a dating site would. Employers
and employees both create profiles by answering a series of multiple-choice or
yes-no questions. The site scores profiles based on criteria from the other party
Chapter 4. Expanding Your Testing Horizons • 80
report erratum  •  discuss


---
**Page 81**

and shows the best potential matches from the perspective of both the employee
and employer. (The author reserves the right to monetize the site, make a
fortune, retire, and do nothing but support the kind readers of this book.)
The ProfileMatcher class, a core piece of iloveyouboss, collects all of the relevant
profiles. Provided with a set of criteria (essentially the preferred answers to
relevant questions), the ProfileMatcher method scoreProfiles iterates all profiles
added. For each profile matching the criteria, ProfileMatcher collects both the
profile and its score—zero if the profile is not a match for the criteria and a
positive value otherwise.
utj3-iloveyouboss2/01/src/main/java/iloveyouboss/domain/ProfileMatcher.java
import java.util.*;
import java.util.concurrent.*;
public class ProfileMatcher {
private List<Profile> profiles = new ArrayList<>();
public void addProfile(Profile profile) {
profiles.add(profile);
}
ExecutorService executorService =
Executors.newFixedThreadPool(8);
public Map<Profile, Integer> scoreProfiles(Criteria criteria)
throws ExecutionException, InterruptedException {
var profiles = new HashMap<Profile, Integer>();
➤
var futures = new ArrayList<Future<Void>>();
for (var profile: this.profiles) {
futures.add(executorService.submit(() -> {
profiles.put(profile,
profile.matches(criteria) ? profile.score(criteria) : 0);
return null;
}));
}
for (var future: futures)
future.get();
executorService.shutdown();
return profiles;
}
}
To be responsive, scoreProfiles calculates matches in the context of separate
threads, implemented using futures. Each profile iterated gets managed by
a single future. That future is responsible for adding the profile and score to
the profiles variable, initialized to an empty HashMap. That concurrent update
is the source of the problem your test will uncover.
report erratum  •  discuss
Testing Multithreaded Code • 81


---
**Page 82**

utj3-iloveyouboss2/01/src/test/java/iloveyouboss/domain/AProfileMatcher.java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.List;
import java.util.function.Function;
import static iloveyouboss.domain.Weight.REQUIRED;
import static iloveyouboss.domain.Weight.WOULD_PREFER;
import static java.util.stream.IntStream.range;
import static org.junit.jupiter.api.Assertions.assertEquals;
@ExtendWith(MockitoExtension.class)
class AProfileMatcher {
ProfileMatcher matcher = new ProfileMatcher();
@Test
void returnsScoreForAllProfiles() throws Exception {
var questions = createQuestions(50);
int profileCount = 500;
var half = profileCount / 2;
range(0, half).forEach(id ->
matcher.addProfile(createProfile(
questions, id, i -> nonMatchingAnswer(questions.get(i)))));
range(half, profileCount).forEach(id ->
matcher.addProfile(createProfile(
questions, id, i -> matchingAnswer(questions.get(i)))));
var criteria = createCriteria(questions);
var results = matcher.scoreProfiles(criteria);
assertEquals(half,
results.values().stream().filter(score -> score == 0).count());
assertEquals(half,
results.values().stream().filter(score -> score > 0).count());
}
private Profile createProfile(
List<BooleanQuestion> questions,
int id,
Function<Integer, Answer> answerFunction) {
var profile = new Profile(String.valueOf(id));
range(0, questions.size()).forEach(i ->
profile.add(answerFunction.apply(i)));
return profile;
}
private Criteria createCriteria(List<BooleanQuestion> questions) {
var questionCount = questions.size();
var criteria = new Criteria();
range(0, 5).forEach(i ->
criteria.add(new Criterion(
matchingAnswer(questions.get(i)), REQUIRED)));
Chapter 4. Expanding Your Testing Horizons • 82
report erratum  •  discuss


---
**Page 83**

range(5, questionCount).forEach(i ->
criteria.add(new Criterion(
matchingAnswer(questions.get(i)), WOULD_PREFER)));
return criteria;
}
private List<BooleanQuestion> createQuestions(int questionCount) {
return range(0, questionCount)
.mapToObj(i -> new BooleanQuestion("question " + i))
.toList();
}
Answer matchingAnswer(Question question) {
return new Answer(question, Bool.TRUE);
}
Answer nonMatchingAnswer(Question question) {
return new Answer(question, Bool.FALSE);
}
}
The test returnsScoreForAllProfiles should fail most of the time and occasionally
pass. If you have difficulty getting it to fail, alter the size of the thread pool,
the number of questions (currently 50), and/or the number of profiles (500).
Try to get it to fail at least 9 out of 10 times. I got it to consistently fail with
200 questions and 2000 profiles.
A simple solution is to wrap the shared HashMap in a synchronized map, which
makes it a thread-safe Java construct:
utj3-iloveyouboss2/02/src/main/java/iloveyouboss/domain/ProfileMatcher.java
public class ProfileMatcher {
private List<Profile> profiles = new ArrayList<>();
public void addProfile(Profile profile) {
profiles.add(profile);
}
ExecutorService executorService =
Executors.newFixedThreadPool(8);
public Map<Profile, Integer> scoreProfiles(Criteria criteria)
throws ExecutionException, InterruptedException {
var profiles =
➤
Collections.synchronizedMap(new HashMap<Profile, Integer>());
➤
var futures = new ArrayList<Future<Void>>();
for (var profile: this.profiles) {
futures.add(executorService.submit(() -> {
profiles.put(profile,
profile.matches(criteria) ? profile.score(criteria) : 0);
report erratum  •  discuss
Testing Multithreaded Code • 83


---
**Page 84**

return null;
}));
}
for (var future: futures)
future.get();
executorService.shutdown();
return profiles;
}
Ensure that your test passes consistently—with the same numbers as it was
consistently failing with—after making this small change.
Perhaps the better approach, however, is to have each future return a map
with a single key-value pair of profile and score. This avoids the modification
to a shared data store. The individual-key maps can all be aggregated into a
single HashMap as part of a loop that blocks on future.get for all futures:
utj3-iloveyouboss2/03/src/main/java/iloveyouboss/domain/ProfileMatcher.java
public Map<Profile, Integer> scoreProfiles(Criteria criteria)
throws ExecutionException, InterruptedException {
var futures = new ArrayList<Future<Map<Profile, Integer>>>();
➤
for (var profile : profiles)
futures.add(executorService.submit(() ->
Map.of(profile,
➤
profile.matches(criteria) ? profile.score(criteria) : 0)));
➤
var finalScores = new HashMap<Profile, Integer>();
➤
for (var future: futures)
➤
finalScores.putAll(future.get());
➤
executorService.shutdown();
return finalScores;
}
Any exacerbation aside, the performance test will be slow due to the numerous
iterations and larger data volumes typically wanted for such a test. It takes
several hundred milliseconds on my machine, far too much for a single test.
Mark it as “slow,” and run it separately from your suite of fast unit tests. See
Creating Arbitrary Test Groups Using Tags, on page 137.
Writing Integration Tests
The QuestionRepository class talks to an H2 database using the Java Persistence
API (JPA). You might correctly guess that this data class is used in many
places throughout the application and that testing each of those places will
require the use of a test double.
Chapter 4. Expanding Your Testing Horizons • 84
report erratum  •  discuss


