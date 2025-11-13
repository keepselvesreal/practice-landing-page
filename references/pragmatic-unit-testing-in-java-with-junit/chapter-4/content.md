# Expanding Your Testing Horizons (pp.71-99)

---
**Page 71**

CHAPTER 4
Expanding Your Testing Horizons
At this point, you’ve worked through the core topics in unit testing, including
JUnit and unit testing fundamentals, how to test various scenarios, and how
to use test doubles to deal with dependencies.
In this chapter, you’ll review a few topics that begin to move outside the sphere
of “doing unit testing”:
• Code coverage and how it can help (or hurt)
• Challenges with writing tests for multithreaded code
• Writing integration tests
Improving Unit Testing Skills Using Code Coverage
Code coverage metrics measure the percentage of code that your unit tests
execute (exercise) when run. Ostensibly, code that is covered is working, and
code that is not covered represents the risk of breakage.
From a high level, tests that exhaust all relevant pieces of code provide 100
percent coverage. Code with no tests whatsoever has 0 percent coverage. Most
code lies somewhere in between.
Many tools exist that will calculate coverage metrics for Java code, including
JaCoCo, OpenClover, SonarQube, and Cobertura. IntelliJ IDEA ships with a
coverage tool built into the IDE.
Numerous coverage metrics exist to measure various code aspects. Function
coverage, for example, measures the percentage of functions (methods) exer-
cised by tests. Some of the other metrics include line, statement, branch,
condition, and path coverage.
report erratum  •  discuss


---
**Page 72**

Line and statement coverage metrics are similar. Line coverage measures
source lines exercised. Since a line can consist of multiple statements, some
tools measure statement coverage.
Branch, condition, and path coverage metrics are similarly related. Branch
coverage measures whether all branches of a conditional statement (for
example, both true and false branches of an if statement) are executed. Condition
coverage measures whether all conditionals (including each in a complex
conditional) have evaluated to both true and false. Path coverage measures
whether every possible route through the code has been executed.
Most of the popular Java coverage tools support calculating line and branch
coverage. You’ll learn about these in this section.
Understanding Statement Coverage
Consider a Batter class that tracks a baseball batter’s strike count. A batter is
out after three strikes. A swing-and-a-miss with the bat—a strike—increments
the strike count. A foul ball (a ball hit out of play) also increments the strike
count unless the batter already has two strikes.
utj3-coverage/01/src/main/java/util/Batter.java
public class Batter {
private int strikeCount = 0;
public void foul() {
if (strikeCount < 2)
strikeCount++;
}
public void strike() {
strikeCount++;
}
public int strikeCount() {
return strikeCount;
}
}
Note the strike method. If none of your tests trigger its execution, its coverage
is 0 percent. If your tests do result in a call to strike, its whopping one line of
code gets exercised, and thus the recorded coverage is 100 percent.
The foul method contains a conditional. It increments strikeCount only if there
are fewer than two strikes. A conditional, implemented in Java with an if
statement, demands at least two tests—one that forces the conditional block
to execute (because the conditional expression resolved to true) and one that
bypasses the if block code.
Chapter 4. Expanding Your Testing Horizons • 72
report erratum  •  discuss


---
**Page 73**

The following test covers the special case—when two strikes already exist.
utj3-coverage/01/src/test/java/util/ABatter.java
@Test
void doesNotIncrementStrikesWhenAtTwo() {
batter.strike();
batter.strike();
batter.foul();
assertEquals(2, batter.strikeCount());
}
If you run this test “with coverage” (that’s the actual text on an IDEA menu
item), the if statement conditional evaluates to false because strikeCount is not
less than two. As a result, the if-statement body doesn’t execute, and strikeCount
is not incremented.
Here’s a tool window showing the summary coverage metrics:
Method coverage shows that three of three possible methods defined on the
Batter class were exercised. That’s not terribly interesting or useful.
Line coverage shows that three of four lines were exercised across those three
methods—one of the lines didn’t get covered when the test ran. In this case,
it’s because you only ran one test in ABatter. Run them all to attain 100 percent
line coverage.
The real value of a coverage tool is that it shows exactly what lines are exer-
cised and what lines are not. IDEA’s coverage tool window shows colored
markers in the gutter (the gray strip left of the source code) to the immediate
right of the line numbers. It marks executed lines as green, lines not executed
as red, and lines partially covered (read on) as yellow as shown in the figure
on page 74.
The increment operation (strikeCount++) is marked red because it is never
executed.
Uncovered code is one of two things: dead or risky.
It can be near-impossible to determine whether code is ever needed or used.
“All dead” code (as opposed to mostly dead code, which might have some
report erratum  •  discuss
Improving Unit Testing Skills Using Code Coverage • 73


---
**Page 74**

future resurrected purpose) can waste time in many ways. Like a vampire,
dead code sucks time: when you read it, when it shows up in search results,
and when you mistakenly start making changes (true stories here) to it.
When you encounter uncovered, mostly dead code, bring it into the sunlight
of your whole team. If it doesn’t shrivel away under their scrutiny, cover the
code with tests. Otherwise, delete it.
Unit tests declare intent. If you test every intent, you can safely
delete untested code.
Add a second test involving only a single strike to get 100 percent coverage
in foul:
utj3-coverage/01/src/test/java/util/ABatter.java
@Test
void incrementsStrikesWhenLessThan2() {
batter.strike();
batter.foul();
assertEquals(2, batter.strikeCount());
}
Conditionals and Code Coverage
Line coverage is an unsophisticated metric that tells you only whether a line
of code was executed or not. It doesn’t tell you if you’ve explored different
Chapter 4. Expanding Your Testing Horizons • 74
report erratum  •  discuss


---
**Page 75**

data cases. For example, if a method accepts an int, did you test it with 0?
With negative numbers and very large numbers? A coverage tool doesn’t even
tell you if the tests contain any assertions. (Yes, some clever developers do
that to make their coverage numbers look better.)
Complex conditionals often represent insufficiently covered paths through
your code. You create complex conditionals when you produce Boolean
expressions involving the logical operators OR (||) and AND (&&).
Suppose you write one test that exercises a complex conditional using only
the OR operator. The line coverage metric will credit your tests for the entire
line containing the complex conditional as long as any one of its Boolean
expressions resolves to true. But you won’t have ensured that all the other
Boolean expressions behave as expected.
Conditional coverage tools can help you pinpoint deficiencies in your coverage
of conditionals.
Take a look at the next intended increment of the Batter code, which supports
tracking balls and walks. It introduces the notion of whether or not a batter’s
turn at home plate is “done,” meaning that they either struck out or walked
(hits and fielding outs would come later). The method isDone implements that
complex conditional.
utj3-coverage/02/src/main/java/util/Batter.java
public class Batter {
private int strikeCount = 0;
private int ballCount = 0;
public void foul() {
if (strikeCount < 2)
strikeCount++;
}
public void ball() {
ballCount++;
}
public void strike() {
strikeCount++;
}
public int strikeCount() {
return strikeCount;
}
public boolean isDone() {
➤
return struckOut() || walked();
➤
}
➤
report erratum  •  discuss
Improving Unit Testing Skills Using Code Coverage • 75


---
**Page 76**

private boolean walked() {
return ballCount == 4;
}
private boolean struckOut() {
return strikeCount == 3;
}
}
A new test is added to the test class to cover a strikeout case:
utj3-coverage/02/src/test/java/util/ABatter.java
@Test
void whenStruckOut() {
batter.strike();
batter.strike();
batter.strike();
assertTrue(batter.isDone());
}
IDEA supports the branch coverage metric, but it is turned off by default.
Turn it on and run all the tests in ABatter. Your code coverage summary now
includes a column for Branch Coverage %:
The summary pane shows that you have a branch coverage deficiency; cur-
rently, it measures only 50 percent. Again, the more revealing aspect is how
the coverage tool marks code within the editor for Batter. The isDone method is
marked with yellow to indicate that not all branches of the complex conditional
are covered. A call to struckOut occurs, but not to walked.
Chapter 4. Expanding Your Testing Horizons • 76
report erratum  •  discuss


---
**Page 77**

The struckOut method is also marked as partially covered. If you click on the
yellow marker, IDEA reveals the coverage data:
Hits: 1
Covered 1/2 branches
In other words, the method was invoked (“hit”) one time. Full branch coverage
of a simple Boolean conditional would require getting hit twice—once where
it evaluates to true and once where it gets evaluated to false.
To garner full coverage for ABatter, you’ll need to add a couple of tests to not
only exercise the walked method but to also ensure that you have a test in
which the entire expression in isDone returns false.
utj3-coverage/03/src/test/java/util/ABatter.java
@Test
void isDoneWithWalk() {
for (var i = 0; i < 4; i++)
batter.ball();
assertTrue(batter.isDone());
}
@Test
void isNotDoneWhenNeitherWalkNorStrikeout() {
assertFalse(batter.isDone());
}
How Much Coverage Is Enough?
Any one of your unit tests will exercise only a very small percentage of code—a
unit’s worth. If you want 100 percent coverage, write unit tests for every unit
you add to your system. Emphasize testing the behaviors, not the methods.
Use tools like ZOM to help you think through the different cases and their
outcomes.
On the surface, it would seem that higher code coverage is good and lower
coverage is not so good. But your manager craves a single number that says,
“Yup, we’re doing well on our unit testing practice,” or “No, we’re not writing
enough unit tests.”
To satisfy your manager, you’d unfortunately need to first determine what
enough means. Obviously, 0 percent is not enough. And 100 percent would
be great, but is it realistic? The use of certain frameworks can make it nearly
impossible to hit 100 percent without some trickery.
Most folks out there (the purveyors of Emma included) suggest that coverage
under 70 percent is insufficient. I agree.
report erratum  •  discuss
Improving Unit Testing Skills Using Code Coverage • 77


---
**Page 78**

Many developers also claim that attempts to increase coverage represent
diminishing returns on value. I disagree. Teams that habitually write unit tests
after they write code achieve coverage levels of 70 percent with relative ease.
Unfortunately, that means the remaining 30 percent of their code remains
untested, often because it’s difficult, hard-to-test code. Difficult code hides more
defects, so at least a third of your defects will probably lie in this untested code.
Jeff’s Theory of Code Coverage: the amount of costly code
increases in the areas of least coverage.
The better your design, the easier it is to write tests. Revisit Chapter 8, Refactor-
ing to Cleaner Code, on page 147 and Chapter 9, Refactoring Your Code’s
Structure, on page 169 to understand how to better structure your code. A
good design coupled with the will to increase coverage will move you in the
direction of 100 percent, which should lead to fewer defects. You might not
reach 100 percent, and that’s okay.
Developers practicing TDD (see Chapter 11, Advancing with Test-Driven Devel-
opment (TDD), on page 211) achieve percentages well over 90 percent, largely by
definition. They write a test for each new behavior they’re about to code. Those
who do TDD, myself included, rarely look at the coverage numbers. TDD makes
coverage a self-fulfilling prophecy.
Coverage percentages can mislead. You can easily write a few tests that blast
through a large percentage of code yet assert little of use. Most tools don’t
even care if your tests have no assertions (which means they’re not really
tests). The tools certainly don’t care if your tests are cryptic or prolix or if they
assert nothing useful. Too many teams spend a fortune writing unit tests
with decent coverage numbers but little value.
Unfortunately, managers always want a single number they can use to mea-
sure success. The code-coverage number is but a surface-level metric that
means little if the tests stink. And if someone tells the team that the metric
goal matters most, the tests will stink.
A downward code coverage trend is probably useful information, however.
Your coverage percentage should either increase or become stable over time
as you add behavior.
The Value in Code Coverage
If you write your tests after you write the corresponding code, you’ll miss
numerous test cases until you improve your skills and habits. Even if you
Chapter 4. Expanding Your Testing Horizons • 78
report erratum  •  discuss


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


---
**Page 85**

Here’s the code for the class:
utj3-iloveyouboss2/01/src/main/java/iloveyouboss/persistence/QuestionRepository.java
import iloveyouboss.domain.BooleanQuestion;
import iloveyouboss.domain.PercentileQuestion;
import iloveyouboss.domain.Persistable;
import iloveyouboss.domain.Question;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import java.time.Clock;
import java.util.List;
import java.util.function.Consumer;
public class QuestionRepository {
private Clock clock = Clock.systemUTC();
private static EntityManagerFactory getEntityManagerFactory() {
return Persistence.createEntityManagerFactory("h2-ds");
}
public Question find(Long id) {
try (var em = em()) {
return em.find(Question.class, id);
}
}
public List<Question> getAll() {
try (var em = em()) {
return em.createQuery("select q from Question q",
Question.class).getResultList();
}
}
public List<Question> findWithMatchingText(String text) {
try (var em = em()) {
var queryString =
"select q from Question q where q.text like :searchText";
var query = em.createQuery(queryString, Question.class);
query.setParameter("searchText", "%" + text + "%");
return query.getResultList();
}
}
public long addPercentileQuestion(String text, String... answerChoices) {
return persist(new PercentileQuestion(text, answerChoices));
}
public long addBooleanQuestion(String text) {
return persist(new BooleanQuestion(text));
}
report erratum  •  discuss
Writing Integration Tests • 85


---
**Page 86**

void setClock(Clock clock) {
this.clock = clock;
}
void deleteAll() {
executeInTransaction(em ->
em.createNativeQuery("delete from Question").executeUpdate());
}
private EntityManager em() {
return getEntityManagerFactory().createEntityManager();
}
private void executeInTransaction(Consumer<EntityManager> func) {
try (var em = em()) {
var transaction = em.getTransaction();
try {
transaction.begin();
func.accept(em);
transaction.commit();
} catch (Exception t) {
if (transaction.isActive()) transaction.rollback();
}
}
}
private long persist(Persistable object) {
object.setCreateTimestamp(clock.instant());
executeInTransaction(em -> em.persist(object));
return object.getId();
}
}
Most of the code in QuestionRepository is simple delegation to the JPA. The class
contains little in the way of interesting logic. That’s good design. QuestionRepository
isolates the dependency on JPA from the rest of the system.
From a testing stance, does it make sense to write a unit test against Question-
Repository? You could write unit tests in which you stub all of the relevant
interfaces, but it would take a good amount of effort, the tests would be diffi-
cult, and in the end, you wouldn’t have proven much. Particularly, unit testing
QuestionRepository won’t prove that you’re using JPA correctly. Defects are fairly
common in dealings with JPA because three different pieces of detail must
all work correctly in concert: the Java code, the mapping configuration
(located in src/META-INF/persistence.xml in your codebase), and the database itself.
The only real way to know if QuestionRepository works is to have it interact with
a real database. You can write tests to do so, but they’ll be integration tests,
not unit tests. They’ll also be one to two orders of magnitude slower than unit
tests.
Chapter 4. Expanding Your Testing Horizons • 86
report erratum  •  discuss


---
**Page 87**

The world of integration testing is huge, and this section is tiny, but hopefully,
it provides a few ideas on when you’ll want integration tests and how you
might approach crafting them.
The Data Problem
You want the vast majority of your JUnit tests to be fast. No worries—if you
isolate all of your persistence interaction to one place in the system, you’ll
have a reasonably small amount of code that must be integration tested.
When you write integration tests for code that interacts with the real database,
the data in the database and how it gets there are important considerations.
To verify that database query operations return expected results, for example,
you must either insert appropriate data or assume it already exists.
Assuming that data is already in the database will create problems. Over
time, the data will change without your knowledge, breaking tests. Also,
divorcing the data from the test code makes it a lot harder to understand why
a particular test passes or not. The meaning of the data with respect to the
tests is lost by dumping it all into the database.
As much as possible, integration tests should create and manage
their own data.
If your tests will be running against your database on your own machine, the
simplest route might be for each test to start with a clean database (or one pre-
populated with necessary reference data). Each test then becomes responsible
for adding and working with its own data. This minimizes intertest dependency
issues, where one test breaks because of data that another test left lying
around. (Those can be a headache to debug!)
If you can only interact with a shared database for your testing, then you’ll
need a less intrusive solution. One option: if your database supports it, you
can initiate a transaction in the context of each test and then roll it back.
(The transaction handling is usually relegated to @BeforeEach and @AfterEach
methods.)
You’ll also want your integration tests to execute as part of your build process.
Whatever solution you derive for the tests must work both on your machine
as well as in the build server’s environment.
Ultimately, integration tests are harder to write, execute, and maintain. They
tend to break more often, and when they do break, debugging the problem
report erratum  •  discuss
Writing Integration Tests • 87


---
**Page 88**

can take considerably longer. But a dependable testing strategy demands you
include some.
If you find yourself adding interesting logic either before or after interaction
with the live interactions (to the database in this example), find a way to
extract that logic to another class. Write unit tests against it there.
Integration tests are essential but challenging to design and
maintain. Minimize their number and complexity by maximizing
the logic you verify in unit tests.
Clean-Room Database Tests
Your tests for the repository empty the database both before and after each
test method’s execution:
utj3-iloveyouboss2/01/src/test/java/iloveyouboss/persistence/AQuestionRepository.java
import iloveyouboss.domain.Question;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.time.ZoneId;
import java.util.Date;
import java.util.List;
import static java.time.Clock.fixed;
import static java.util.Arrays.asList;
import static org.junit.jupiter.api.Assertions.assertEquals;
class AQuestionRepository {
QuestionRepository repository = new QuestionRepository();
@BeforeEach
void setUp() {
repository.deleteAll();
}
@AfterEach
void tearDown() {
repository.deleteAll();
}
@Test
void findsPersistedQuestionById() {
var id = repository.addBooleanQuestion("question text");
var question = repository.find(id);
assertEquals("question text", question.getText());
}
Chapter 4. Expanding Your Testing Horizons • 88
report erratum  •  discuss


---
**Page 89**

@Test
void storesDateAddedForPersistedQuestion() {
var now = new Date().toInstant();
repository.setClock(fixed(now, ZoneId.systemDefault()));
var id = repository.addBooleanQuestion("text");
var question = repository.find(id);
assertEquals(now, question.getCreateTimestamp());
}
@Test
void answersMultiplePersistedQuestions() {
repository.addBooleanQuestion("q1");
repository.addBooleanQuestion("q2");
repository.addPercentileQuestion("q3", "a1", "a2");
var questions = repository.getAll();
assertEquals(asList("q1", "q2", "q3"), extractText(questions));
}
@Test
void findsMatchingEntries() {
repository.addBooleanQuestion("alpha 1");
repository.addBooleanQuestion("alpha 2");
repository.addBooleanQuestion("beta 1");
var questions = repository.findWithMatchingText("alpha");
assertEquals(asList("alpha 1", "alpha 2"), extractText(questions));
}
private List<String> extractText(List<Question> questions) {
return questions.stream().map(Question::getText).toList();
}
}
Clearing the data before gives your tests the advantage of working with a clean
slate.
Clearing the data after each test runs is just being nice, not leaving data
around cluttering shared databases.
When trying to figure out a problem, you might want to take a look at the
data after a test completes. To do so, comment out the call to clearData call in
the @AfterEach method.
Your tests aren’t focused on individual methods; instead, they’re verifying
behaviors that are inextricably linked. To verify that you can retrieve or find
elements, you must first insert them. To verify that you’ve inserted elements,
you retrieve them.
report erratum  •  discuss
Writing Integration Tests • 89


---
**Page 90**

Ensure you run coverage tools to verify that all the code is getting tested. The
tests for QuestionRepository show that it’s completely covered with tests. Also, if
you use integration tests to cover some small portions of code rather than
unit tests, your system-wide unit test code coverage numbers will suffer a
little. If that concerns you, you might be able to merge the numbers properly
(the tool jacoco:merge
1 works for JaCoCo).
Exploratory Unit Testing
The unit tests you’ve learned to build capture your best understanding of the
intents in the code. They cover known edge cases and typical use cases.
Some code may demand further exploration. For example, complex code, code
that seems to keep breaking as you uncover more nuances about the input
data, or code that incurs a high cost if it were to fail. Systems requiring high
reliability or security might incur significant costs from unit-level failures.
Numerous kinds of developer-focused tests exist to help you with such
exploratory testing. Many of them verify at the integration level—load tests,
failover tests, performance tests, and contract tests, to name a few. You can
learn about some of these in Alexander Tarlinder’s book Developer Testing.
2
Following is an overview of two unit-level testing tactics: fuzz testing and
property testing, which can be considered forms of what’s known as generative
testing. These sorts of tests require additional tooling above and beyond JUnit,
and thus, you’re only getting an introduction to them in this book. (That’s
one excuse among a few, and I’m sticking with it.)
Not covered at all: mutation testing, which involves tools that make small
changes to your production code to see if such changes break your tests. If
your tests don’t break, the mutation tests suggest you might have insufficient
test coverage.
Fuzz Testing
With fuzz testing, you use a tool to provide a wide range of random, unexpected,
or invalid inputs to your code. It can help you identify edge cases in your
code that you’re otherwise unlikely to think of when doing traditional unit
testing.
1.
https://www.jacoco.org/jacoco/trunk/doc/merge-mojo.html
2.
https://www.informit.com/store/developer-testing-building-quality-into-software-9780134431802
Chapter 4. Expanding Your Testing Horizons • 90
report erratum  •  discuss


---
**Page 91**

This URL creator code combines server and document strings into a valid
URL string:
utj3-iloveyouboss2/03/src/main/java/util/URLCreator.java
import java.net.MalformedURLException;
import java.net.URL;
import static java.lang.String.format;
public class URLCreator {
public String create(String server, String document)
throws MalformedURLException {
if (isEmpty(document))
return new URL(format("https://%s", server)).toString();
return new URL(
format("https://%s/%s", server, clean(document))).toString();
}
private boolean isEmpty(String document) {
return document == null || document.trim().equals("");
}
private String clean(String document) {
return document.charAt(0) == '/'
? document.substring(1)
: document;
}
}
Here are the tests:
utj3-iloveyouboss2/03/src/test/java/util/AURLCreator.java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;
import java.net.MalformedURLException;
import static org.junit.jupiter.api.Assertions.assertEquals;
class AURLCreator {
URLCreator urlCreator = new URLCreator();
@Test
void returnsCombinedURLStringGivenServerAndDocument()
throws MalformedURLException {
assertEquals(
"https://example.com/customer?id=123",
urlCreator.create("example.com", "customer?id=123"));
}
@ParameterizedTest
@NullSource
report erratum  •  discuss
Exploratory Unit Testing • 91


---
**Page 92**

@ValueSource(strings = { "", " \n\t\r " })
void buildsURLGivenServerOnly(String document)
throws MalformedURLException {
assertEquals(
"https://example.com",
urlCreator.create("example.com", document));
}
@Test
void eliminatesRedundantLeadingSlash() throws MalformedURLException {
assertEquals(
"https://example.com/customer?id=123",
urlCreator.create("example.com", "/customer?id=123"));
}
}
Code like this tends to grow over time as you think of additional protections
to add. The third test deals with the case where the caller of the create method
prepends the document with a forward slash—"/employee?id=42", for example.
Someone likely wasn’t sure if the slash needed to be provided or not. The
developer, as a result, updated the code to allow either circumstance.
With fuzz testing, you’ll likely add more protections and corresponding tests
as the fuzzing effort uncovers additional problems.
You can write fuzz tests using the tool Jazzer:
3
utj3-iloveyouboss2/03/src/test/java/util/AURLCreatorFuzzer.java
import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;
import java.net.MalformedURLException;
public class AURLCreatorFuzzer {
@FuzzTest
public void fuzzTestIsValidURL(FuzzedDataProvider data)
throws MalformedURLException {
var server = data.consumeString(32);
var document = data.consumeRemainingAsString();
new URLCreator().create(server, document);
}
}
Fuzz test methods are annotated with @FuzzTest, and passed a data provider.
From this data provider (a wrapper around some random stream of data),
you can extract the data you need. The test fuzzTestIsValidUrl first extracts a 32-
character string to be passed as the server, then uses the remaining incoming
data as the document.
3.
https://github.com/CodeIntelligenceTesting/jazzer
Chapter 4. Expanding Your Testing Horizons • 92
report erratum  •  discuss


---
**Page 93**

To run fuzzing with Jazzer, first create a directory in your project’s test
resources. Derive its name from your fuzzer class’s package plus the fuzzer
class name plus the word Inputs:
utj3-iloveyouboss2/src/test/resources/util/AURLCreatorFuzzerInputs
Then run your tests with the environment variable setting JAZZER_FUZZ=1. The
fuzzing tool will display failures and add the inputs causing the failures to
files within the resource directory you created.
The fuzzer should report that an input containing an LF (line feed character;
ASCII value 10) represents an invalid character for a URL. You, as the devel-
oper, get to decide how you want the code to deal with that, if at all.
You can also collect a number of inputs in the test resources directory. With
the JAZZER_FUZZ environment variable turned off, Jazzer will use these inputs
to run what effectively become regression test inputs.
Property Testing
Another form of unit testing is property testing, where your tests describe
invariants and postconditions, or properties, about the expected behavior of
code. Property testing tools, such as jqwik,
4 will test these invariants using
a wide range of automatically generated inputs.
Your primary reason for using property tests is to uncover edge cases and
unexpected behaviors by virtue of exploring a broader range of inputs.
Here’s an implementation for the insertion sort algorithm, which performs
terribly but is a reasonable choice if your input array is small (or if your inputs
are generally almost sorted already):
utj3-iloveyouboss2/03/src/main/java/util/ArraySorter.java
public class ArraySorter {
public void inPlaceInsertionSort(int[] arr) {
for (var i = 1; i < arr.length - 1; i++) {
var key = arr[i];
var j = i - 1;
while (j >= 0 && arr[j] > key) {
arr[j + 1] = arr[j];
j = j - 1;
}
arr[j + 1] = key;
}
}
}
4.
https://jqwik.net
report erratum  •  discuss
Exploratory Unit Testing • 93


---
**Page 94**

Using jqwik, you define @Property methods that get executed by the JUnit test
runner. The following set of properties for ArraySorter describes three properties:
an already-sorted array should remain sorted, an array with all the same
elements should remain unchanged, and a random array should be sorted
in ascending order:
utj3-iloveyouboss2/03/src/test/java/util/ArraySorterProperties.java
import static java.util.Arrays.fill;
import static java.util.Arrays.sort;
import net.jqwik.api.*;
import java.util.Arrays;
public class ArraySorterProperties {
ArraySorter arraySorter = new ArraySorter();
@Property
boolean returnsSameArrayWhenAlreadySorted(@ForAll int[] array) {
sort(array);
var expected = array.clone();
arraySorter.inPlaceInsertionSort(array);
return Arrays.equals(expected, array);
}
@Property
boolean returnsSameArrayWhenAllSameElements(@ForAll int element) {
var array = new int[12];
fill(array, element);
var expected = array.clone();
arraySorter.inPlaceInsertionSort(array);
return Arrays.equals(expected, array);
}
@Property
boolean sortsAscendingWhenRandomUnsortedArray(@ForAll int[] array) {
var expected = array.clone();
sort(expected);
arraySorter.inPlaceInsertionSort(array);
return Arrays.equals(expected, array);
}
}
Taking the last method as an example: sortsAscendingForRandomUnsortedArray rep-
resents a postcondition that should hold true for all (@ForAll) input arrays (array).
The property implementation clones the incoming array and sorts it using
Java’s built-in sort, capturing the result as expected. It sorts the incoming
array, then returns the result of comparing that sort to expected.
Chapter 4. Expanding Your Testing Horizons • 94
report erratum  •  discuss


---
**Page 95**

Jqwik, a sophisticated and highly flexible tool, calls the property one thousand
times by default. And, beauty! The last property fails, and consistently so,
given those thousand inputs.
The array sort code represents a good fit for property testing. You might think
to write a handful of test cases (ZOM, certainly). But there are some cases
that can be hard to think of. Property testing can help uncover those cases.
Yes, there’s a defect in the insertion sort. The jqwik tool should identify the
problem. See if you can figure out and fix the defective code.
Summary
In this chapter, you rounded out your knowledge of core unit testing concepts
with a few (mostly unrelated) topics that look at bigger concerns surrounding
unit testing:
• Code coverage, a concept that can help you learn where your unit testing
is deficient
• Testing multithreaded code, a tricky and sophisticated challenge
• Integration tests, which verify code and its interaction with external
dependencies that might be out of your control
Now that you’ve worked through foundational concepts regarding unit testing,
you’ll take a deeper look into the preferred tool for Java unit testing, JUnit.
The next three chapters will explore JUnit in-depth, providing useful insights
and nuggets on how to best take advantage of its wealth of features.
report erratum  •  discuss
Summary • 95


---
**Page 97**

Part II
Mastering JUnit with “E”s
You can accomplish most of your unit testing needs
with a small fraction of JUnit’s robust capabilities.
In this part, you’ll learn to streamline your day-to-
day unit testing activities by delving into the three
"E"s of JUnit: Examining outcomes with assertions,
Establishing organization in your tests, and Execut-
ing your tests.


---
**Page 99**

CHAPTER 5
Examining Outcomes with Assertions
You’ve learned the most important features of JUnit in the prior four chapters
of this book, enough to survive but not thrive. Truly succeeding with your
unit testing journey will involve gaining proficiency with your primary tool,
JUnit. In this and the next couple of chapters, you’ll explore JUnit in signifi-
cant detail. First, you’ll focus on JUnit’s means of verification—its assertion
library.
Assertions (or asserts) in JUnit are static method calls that you drop into
your tests. Each assertion is an opportunity to verify that some condition
holds true. If an asserted condition does not hold true, the test stops executing
right there and JUnit reports a test failure.
To abort the test, JUnit throws an exception object of type AssertionFailedError.
If JUnit catches AssertionFailedError, it marks the test as failed. In fact, JUnit
marks any test as failed that throws an exception not caught in the test body.
In order to use the most appropriate assertion for your verification need, you’ll
want to learn about JUnit’s numerous assertion variants.
In examples to this point, you’ve used the two most prevalent assertion forms,
assertTrue and assertEquals. Since you’ll use them for the bulk of your tests, you’ll
first examine these assertion workhorses more deeply. You’ll then move on
to exploring the numerous alternative assertion choices that JUnit provides.
In some cases, the easiest way to assert something won’t be to compare to
an actual result but to instead verify an operation by inverting it. You’ll see
a brief example of how.
You’ll also get an overview of AssertJ, a third-party assertion library that
allows you to write “fluent” assertions. Such assertions can make your tests
considerably easier to read. They can also provide more precise explanations
about why a test is failing.
report erratum  •  discuss


