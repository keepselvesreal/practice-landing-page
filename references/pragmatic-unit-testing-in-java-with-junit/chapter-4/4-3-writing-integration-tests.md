# 4.3 Writing Integration Tests (pp.84-90)

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


