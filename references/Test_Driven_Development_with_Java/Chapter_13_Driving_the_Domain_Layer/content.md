Line 1: 
Line 2: --- 페이지 258 ---
Line 3: 13
Line 4: Driving the Domain Layer
Line 5: We laid a lot of groundwork in previous chapters, covering a mixture of TDD techniques and software 
Line 6: design approaches. Now we can apply those capabilities to build our Wordz game. We will be building 
Line 7: on top of the useful code we have written throughout the book and working toward a well-engineered, 
Line 8: well-tested design, written using the test-first approach.
Line 9: Our goal for this chapter is to create the domain layer of our system. We will adopt the hexagonal 
Line 10: architecture approach as described in Chapter 9, Hexagonal Architecture – Decoupling External Systems. 
Line 11: The domain model will contain all our core application logic. This code will not be tied to details of 
Line 12: any external system technologies such as SQL databases or web servers. We will create abstractions 
Line 13: for these external systems and use test doubles to enable us to test-drive the application logic.
Line 14: Using hexagonal architecture in this way allows us to write FIRST unit tests for complete user stories, 
Line 15: which is something often requiring integration or end-to-end testing in other design approaches. We 
Line 16: will write our domain model code by applying the ideas presented in the book so far.
Line 17: In this chapter, we’re going to cover the following main topics:
Line 18: •	 Starting a new game
Line 19: •	 Playing the game
Line 20: •	 Ending the game
Line 21: Technical requirements
Line 22: The final code for this chapter can be found at https://github.com/PacktPublishing/
Line 23: Test-Driven-Development-with-Java/tree/main/chapter13.
Line 24: Starting a new game
Line 25: In this section, we will make a start by coding our game. Like every project, starting is usually quite 
Line 26: difficult, with the first decision being simply where to begin. A reasonable approach is to find a user 
Line 27: story that will begin to flesh out the structure of the code. Once we have a reasonable structure for an 
Line 28: application, it becomes much easier to figure out where new code should be added.
Line 29: 
Line 30: --- 페이지 259 ---
Line 31: Driving the Domain Layer
Line 32: 236
Line 33: Given this, we can make a good start by considering what needs to happen when we start a new game. 
Line 34: This must set things up ready to play and so will force some critical decisions to be made.
Line 35: The first user story to work on is starting a new game:
Line 36: •	 As a player I want to start a new game so that I have a new word to guess
Line 37: When we start a new game, we must do the following:
Line 38: 1.	
Line 39: Select a word at random from the available words to guess
Line 40: 2.	
Line 41: Store the selected word so that scores for guesses can be calculated
Line 42: 3.	
Line 43: Record that the player may now make an initial guess
Line 44: We will assume the use of hexagonal architecture as we code this story, meaning that any external 
Line 45: system will be represented by a port in the domain model. With this in mind, we can create our first 
Line 46: test and take it from there.
Line 47: Test-driving starting a new game
Line 48: In terms of a general direction, using hexagonal architecture means we are free to use an outside-in 
Line 49: approach with TDD. Whatever design we come up with for our domain model, none of it is going 
Line 50: to involve difficult-to-test external systems. Our unit tests are assured to be FIRST – fast, isolated, 
Line 51: repeatable, self-checking, and timely.
Line 52: Importantly, we can write unit tests that cover the entire logic needed for a user story.  If we wrote 
Line 53: code that is bound to external systems – for example, it contained SQL statements and connected 
Line 54: to a database – we would need an integration test to cover a user story. Our choice of hexagonal 
Line 55: architecture frees us from that.
Line 56: On a tactical note, we will reuse classes that we have already test-driven, such as class 
Line 57: WordSelection, class Word, and class Score. We will reuse existing code and third-
Line 58: party libraries whenever an opportunity presents itself.
Line 59: Our starting point is to write a test to capture our design decisions related to starting a new game:
Line 60: 1.	
Line 61: We will start with a test called NewGameTest. This test will act across the domain model to 
Line 62: drive out our handling of everything we need to do to start a new game:
Line 63: package com.wordz.domain;
Line 64: public class NewGameTest {
Line 65: }
Line 66: 
Line 67: --- 페이지 260 ---
Line 68: Starting a new game
Line 69: 237
Line 70: 2.	
Line 71: For this test, we will start with the Act step first. We are assuming hexagonal architecture, so the 
Line 72: design goal of the Act step is to design the port that handles the request to start a new game. In 
Line 73: hexagonal architecture, a port is the piece of code that allows some external system to connect 
Line 74: with the domain model. We begin by creating a class for our port:
Line 75: package com.wordz.domain;
Line 76: public class NewGameTest {
Line 77:     void startsNewGame() {
Line 78:         var game = new Game();
Line 79:     }
Line 80: }
Line 81: The key design decision here is to create a controller class to handle the request to start 
Line 82: a game. It is a controller in the sense of the original Gang of Four’s Design Patterns book – a 
Line 83: domain model object that will orchestrate other domain model objects. We will let the IntelliJ 
Line 84: IDE create the empty Game class:
Line 85: package com.wordz.domain;
Line 86: public class Game {
Line 87: }
Line 88: That’s another advantage of TDD. When we write the test first, we give our IDE enough 
Line 89: information to be able to generate boilerplate code for us. We enable the IDE autocomplete 
Line 90: feature to really help us. If your IDE cannot autogenerate code after having written the test, 
Line 91: consider upgrading your IDE.
Line 92: 3.	
Line 93: The next step is to add a start() method on the controller class to start a new game. We 
Line 94: need to know which player we are starting a game for, so we pass in a Player object. We 
Line 95: write the Act step of our test:
Line 96: public class NewGameTest {
Line 97:     @Test
Line 98:     void startsNewGame() {
Line 99:         var game = new Game();
Line 100:         var player = new Player();
Line 101:         game.start(player);
Line 102:     }
Line 103: }
Line 104: 
Line 105: --- 페이지 261 ---
Line 106: Driving the Domain Layer
Line 107: 238
Line 108: We allow the IDE to generate the method in the controller:
Line 109: public class Game {
Line 110:     public void start(Player player) {
Line 111:     }
Line 112: }
Line 113: Tracking the progress of the game
Line 114: The next design decisions concern the expected outcome of starting a new game for a player. There 
Line 115: are two things that need to be recorded:
Line 116: •	 The selected word that the player attempts to guess
Line 117: •	 That we expect their first guess next
Line 118: The selected word and current attempt number will need to persist somewhere. We will use the 
Line 119: repository pattern to abstract that. Our repository will need to manage some domain objects. Those 
Line 120: objects will have the single responsibility of tracking our progress in a game.
Line 121: Already, we see a benefit of TDD in terms of rapid design feedback. We haven’t written too much 
Line 122: code yet, but already, it seems like the new class needed to track game progress would best be called 
Line 123: class Game. However, we already have a class Game, responsible for starting a new game. TDD 
Line 124: is providing feedback on our design – that our names and responsibilities are mismatched.
Line 125: We must choose one of the following options to proceed:
Line 126: •	 Keep our existing class Game as it is. Call this new class something such as Progress 
Line 127: or Attempt.
Line 128: •	 Change the start() method to a static method – a method that applies to all instances of 
Line 129: a class.
Line 130: •	 Rename class Game to something that better describes its responsibility. Then, we can 
Line 131: create a new class Game to hold current player progress.
Line 132: The static method option is unappealing. When using object-oriented programming in Java, static 
Line 133: methods rarely seem as good a fit as simply creating another object that manages all the relevant 
Line 134: instances. The static method becomes a normal method on this new object. Using class Game to 
Line 135: represent progress through a game seems to result in more descriptive code. Let’s go with that approach.
Line 136: 1.	
Line 137: Use the IntelliJ IDEA IDE to refactor/rename class Game class Wordz, which represents 
Line 138: the entry point into our domain model. We also rename the local variable game to match:
Line 139: public class NewGameTest {
Line 140:     @Test
Line 141: 
Line 142: --- 페이지 262 ---
Line 143: Starting a new game
Line 144: 239
Line 145:     void startsNewGame() {
Line 146:         var wordz = new Wordz();
Line 147:         var player = new Player();
Line 148:         wordz.start(player);
Line 149:     }
Line 150: }
Line 151: The name of the NewGameTest test is still good. It represents the user story we are testing and 
Line 152: is not related to any class names. The production code has been refactored by the IDE as well:
Line 153: public class Wordz {
Line 154:     public void start(Player player) {
Line 155:     }
Line 156: }
Line 157: 2.	
Line 158: Use the IDE to refactor/rename the start() method newGame(). This seems to better 
Line 159: describe the responsibility of the method, in the context of a class named Wordz:
Line 160: public class NewGameTest {
Line 161:     @Test
Line 162:     void startsNewGame() {
Line 163:         var wordz = new Wordz();
Line 164:         var player = new Player();
Line 165:         wordz.newGame(player);
Line 166:     }
Line 167: }
Line 168: The class Wordz production code also has the method renamed.
Line 169: 3.	
Line 170: When we start a new game, we need to select a word to guess and start the sequence of attempts 
Line 171: the player has. These facts need to be stored in a repository. Let’s create the repository first. We 
Line 172: will call it interface GameRepository and add Mockito @Mock support for it in our test:
Line 173: package com.wordz.domain;
Line 174: import org.junit.jupiter.api.Test;
Line 175: import org.junit.jupiter.api.extension.ExtendWith;
Line 176: import org.mockito.Mock;
Line 177: 
Line 178: --- 페이지 263 ---
Line 179: Driving the Domain Layer
Line 180: 240
Line 181: import org.mockito.junit.jupiter.MockitoExtension;
Line 182: @ExtendWith(MockitoExtension.class)
Line 183: public class NewGameTest {
Line 184:     @Mock
Line 185:     private GameRepository gameRepository;
Line 186:     @InjectMocks
Line 187:     private Wordz wordz;
Line 188:     @Test
Line 189:     void startsNewGame() {
Line 190:         var player = new Player();
Line 191:         wordz.newGame(player);
Line 192:     }
Line 193: }
Line 194: We add the @ExtendWith annotation to the class to enable the Mockito library to automatically 
Line 195: create test doubles for us. We add a gameRepository field, which we annotated as a 
Line 196: Mockito @Mock. We use the @InjectMocks convenience annotation built into Mockito to 
Line 197: automatically inject this dependency into the Wordz constructor.
Line 198: 4.	
Line 199: We allow the IDE to create an empty interface for us:
Line 200: package com.wordz.domain;
Line 201: public interface GameRepository {
Line 202: }
Line 203: 5.	
Line 204: For the next step, we will confirm that gameRepository gets used. We decide to add a 
Line 205: create() method on the interface, which takes a class Game object instance as its only 
Line 206: parameter. We want to inspect that object instance of class Game, so we add an argument 
Line 207: captor. This allows us to assert on the game data contained in that object:
Line 208: public class NewGameTest {
Line 209:     @Mock
Line 210:     private GameRepository gameRepository;
Line 211:     @Test
Line 212:     void startsNewGame() {
Line 213: 
Line 214: --- 페이지 264 ---
Line 215: Starting a new game
Line 216: 241
Line 217:         var player = new Player();
Line 218:         wordz.newGame(player);
Line 219:         var gameArgument =
Line 220:                ArgumentCaptor.forClass(Game.class)
Line 221:         verify(gameRepository)
Line 222:            .create(gameArgument.capture());
Line 223:         var game = gameArgument.getValue();
Line 224:         assertThat(game.getWord()).isEqualTo("ARISE");
Line 225:         assertThat(game.getAttemptNumber()).isZero();
Line 226:         assertThat(game.getPlayer()).isSameAs(player);
Line 227:     }
Line 228: }
Line 229: A good question is why we are asserting against those particular values. The reason is that 
Line 230: we are going to cheat when we add the production code and fake it until we make it. We will 
Line 231: return a Game object that hardcodes these values as a first step. We can then work in small 
Line 232: steps. Once the cheat version makes the test pass, we can refine the test and test-drive the code 
Line 233: to fetch the word for real. Smaller steps provide more rapid feedback. Rapid feedback enables 
Line 234: better decision-making.
Line 235: Note on using getters in the domain model
Line 236: The Game class has getXxx() methods, known as getters in Java terminology, for every one 
Line 237: of its private fields. These methods break the encapsulation of data.
Line 238: This is generally not recommended. It can lead to important logic being placed into other 
Line 239: classes – a code smell known as a foreign method. Object-oriented programming is all about 
Line 240: co-locating logic and data, encapsulating both. Getters should be few and far between. That 
Line 241: does not mean we should never use them, however.
Line 242: In this case, the single responsibility of class Game is to transfer the current state of the 
Line 243: game being played to GameRepository. The most direct way of implementing this is to add 
Line 244: getters to the class. Writing simple, clear code beats following rules dogmatically.
Line 245: Another reasonable approach is to add a getXxx() diagnostic method at package-level 
Line 246: visibility purely for testing. Check with the team that this is not part of the public API and do 
Line 247: not use it in production code. It is more important to get the code correct than obsess over 
Line 248: design trivia.
Line 249: 
Line 250: --- 페이지 265 ---
Line 251: Driving the Domain Layer
Line 252: 242
Line 253: 6.	
Line 254: We create empty methods for these new getters using the IDE. The next step is to run 
Line 255: NewGameTest and confirm that it fails:
Line 256: Figure 13.1 – Our failing test
Line 257: 7.	
Line 258: This is enough for us to write some more production code:
Line 259: package com.wordz.domain;
Line 260: public class Wordz {
Line 261:     private final GameRepository gameRepository;
Line 262:     public Wordz(GameRepository gr) {
Line 263:         this.gameRepository = gr;
Line 264:     }
Line 265:     public void newGame(Player player) {
Line 266:         var game = new Game(player, "ARISE", 0);
Line 267:         gameRepository.create(game);
Line 268:     }
Line 269: }
Line 270: We can rerun NewGameTest and watch it pass:
Line 271: 
Line 272: --- 페이지 266 ---
Line 273: Starting a new game
Line 274: 243
Line 275: Figure 13.2 – The test passes
Line 276: The test now passes. We can move from our red-green phase to thinking about refactoring. The 
Line 277: thing that jumps out immediately is just how unreadable that ArgumentCaptor code is in 
Line 278: the test. It contains too much detail about the mechanics of mocking and not enough detail 
Line 279: about why we are using that technique. We can clarify that by extracting a well-named method.
Line 280: 8.	
Line 281: Extract the getGameInRepository() method for clarity:
Line 282: @Test
Line 283: void startsNewGame() {
Line 284:     var player = new Player();
Line 285:     wordz.newGame(player);
Line 286:     Game game = getGameInRepository();
Line 287:     assertThat(game.getWord()).isEqualTo("ARISE");
Line 288:     assertThat(game.getAttemptNumber()).isZero();
Line 289:     assertThat(game.getPlayer()).isSameAs(player);
Line 290: }
Line 291: private Game getGameInRepository() {
Line 292:     var gameArgument
Line 293:        = ArgumentCaptor.forClass(Game.class)
Line 294:     verify(gameRepository)
Line 295:             .create(gameArgument.capture());
Line 296:     return gameArgument.getValue();
Line 297: }
Line 298: 
Line 299: --- 페이지 267 ---
Line 300: Driving the Domain Layer
Line 301: 244
Line 302: That has made the test much simpler to read and see the usual Arrange, Act, and Assert pattern 
Line 303: in it. It is a simple test by nature and should read as such. We can now rerun the test and confirm 
Line 304: that it still passes. It does, and we are satisfied that our refactoring did not break anything.
Line 305: That completes our first test – a job well done! We’re making good progress here. It always feels good 
Line 306: to me to see a test go green, and that feeling never gets old. This test is essentially an end-to-end test 
Line 307: of a user story, acting only on the domain model. Using hexagonal architecture enables us to write 
Line 308: tests that cover the details of our application logic, while avoiding the need for test environments. We 
Line 309: get faster-running, more stable tests as a result.
Line 310: There is more work to do in our next test, as we need to remove the hardcoded creation of the Game 
Line 311: object. In the next section, we will address this by triangulating the word selection logic. We design 
Line 312: the next test to drive out the correct behavior of selecting a word at random.
Line 313: Triangulating word selection
Line 314: The next task is to remove the cheating that we used to make the previous test pass. We hardcoded 
Line 315: some data when we created a Game object. We need to replace that with the correct code. This code 
Line 316: must select a word at random from our repository of known five-letter words.
Line 317: 1.	
Line 318: Add a new test to drive out the behavior of selecting a random word:
Line 319:     @Test
Line 320:     void selectsRandomWord() {
Line 321:     }
Line 322: 2.	
Line 323: Random word selection depends on two external systems – the database that holds the words 
Line 324: to choose from and a source of random numbers. As we are using hexagonal architecture, the 
Line 325: domain layer cannot access those directly. We will represent them with two interfaces – the 
Line 326: ports to those systems. For this test, we will use Mockito to create stubs for those interfaces:
Line 327: @ExtendWith(MockitoExtension.class)
Line 328: public class NewGameTest {
Line 329:     @Mock
Line 330:     private GameRepository gameRepository;
Line 331:     @Mock
Line 332:     private WordRepository wordRepository ;
Line 333:     @Mock
Line 334:     private RandomNumbers randomNumbers ;
Line 335: 
Line 336: --- 페이지 268 ---
Line 337: Starting a new game
Line 338: 245
Line 339:     @InjectMocks
Line 340:     private Wordz wordz;
Line 341: This test introduces two new collaborating objects to class Wordz. These are instances 
Line 342: of any valid implementations of both interface WordRepository and interface 
Line 343: RandomNumbers. We need to inject those objects into the Wordz object to make use of them.
Line 344: 3.	
Line 345: Using dependency injection, inject the two new interface objects into the class 
Line 346: Wordz constructor:
Line 347: public class Wordz {
Line 348:     private final GameRepository gameRepository;
Line 349:     private final WordSelection wordSelection ;
Line 350:     public Wordz(GameRepository gr,
Line 351:                  WordRepository wr,
Line 352:                  RandomNumbers rn) {
Line 353:         this.gameRepository = gr;
Line 354:         this.wordSelection = new WordSelection(wr, rn);
Line 355:     }
Line 356: We’ve added two parameters to the constructor. We do not need to store them directly as fields. 
Line 357: Instead, we use the previously created class WordSelection. We create a WordSelection 
Line 358: object and store it in a field called wordSelection. Note that our earlier use of @InjectMocks 
Line 359: means that our test code will automatically pass in the mock objects to this constructor, without 
Line 360: further code changes. It is very convenient.
Line 361: 4.	
Line 362: We set up the mocks. We want them to simulate the behavior we expect from interface 
Line 363: WordRepository when we call the fetchWordByNumber() method and interface 
Line 364: RandomNumbers when we call next():
Line 365:     @Test
Line 366:     void selectsRandomWord() {
Line 367:         when(randomNumbers.next(anyInt())).thenReturn(2);
Line 368:         when(wordRepository.fetchWordByNumber(2))
Line 369:                .thenReturn("ABCDE");
Line 370:     }
Line 371: This will set up our mocks so that when next() is called, it will return the word number 2 
Line 372: every time, as a test double for the random number that will be produced in the full application. 
Line 373: When fetchWordByNumber() is then called with 2 as an argument, it will return the word 
Line 374: 
Line 375: --- 페이지 269 ---
Line 376: Driving the Domain Layer
Line 377: 246
Line 378: with word number 2, which will be "ABCDE" in our test. Looking at that code, we can add 
Line 379: clarity by using a local variable instead of that magic number 2. To future readers of the code, 
Line 380: the link between random number generator output and word repository will be more obvious:
Line 381:     @Test
Line 382:     void selectsRandomWord() {
Line 383:         int wordNumber = 2;
Line 384:         when(randomNumbers.next(anyInt()))
Line 385:            .thenReturn(wordNumber);
Line 386:         when(wordRepository
Line 387:            .fetchWordByNumber(wordNumber))
Line 388:                .thenReturn("ABCDE");
Line 389:     }
Line 390: 5.	
Line 391: That still looks too detailed once again. There is too much emphasis on mocking mechanics and 
Line 392: too little on what the mocking represents. Let’s extract a method to explain why we are setting 
Line 393: up this stub. We will also pass in the word we want to be selected. That will help us more easily 
Line 394: understand the purpose of the test code:
Line 395:     @Test
Line 396:     void selectsRandomWord() {
Line 397:         givenWordToSelect("ABCDE");
Line 398:     }
Line 399:     private void givenWordToSelect(String wordToSelect){
Line 400:         int wordNumber = 2;
Line 401:         when(randomNumbers.next(anyInt()))
Line 402:                 .thenReturn(wordNumber);
Line 403:         when(wordRepository
Line 404:                 .fetchWordByNumber(wordNumber))
Line 405:                 .thenReturn(wordToSelect);
Line 406:     }
Line 407: 
Line 408: --- 페이지 270 ---
Line 409: Starting a new game
Line 410: 247
Line 411: 6.	
Line 412: Now, we can write the assertion to confirm that this word is passed down to the gameRepository 
Line 413: create() method – we can reuse our getGameInRepository() assert helper method:
Line 414: @Test
Line 415: void selectsRandomWord() {
Line 416:     givenWordToSelect("ABCDE");
Line 417:     var player = new Player();
Line 418:     wordz.newGame(player);
Line 419:     Game game = getGameInRepository();
Line 420:     assertThat(game.getWord()).isEqualTo("ABCDE");
Line 421: }
Line 422: This follows the same approach as the previous test, startsNewGame.
Line 423: 7.	
Line 424: Watch the test fail. Write production code to make the test pass:
Line 425: public void newGame(Player player) {
Line 426:     var word = wordSelection.chooseRandomWord();
Line 427:     Game game = new Game(player, word, 0);
Line 428:     gameRepository.create(game);
Line 429: }
Line 430: 8.	
Line 431: Watch the new test pass and then run all tests:
Line 432: Figure 13.3 – Original test failing
Line 433: Our initial test has now failed. We’ve broken something during our latest code change. TDD 
Line 434: has kept us safe by providing a regression test for us. What has happened is that after removing 
Line 435: the hardcoded word "ARISE" that the original test relied on, it fails. The correct solution is to 
Line 436: 
Line 437: --- 페이지 271 ---
Line 438: Driving the Domain Layer
Line 439: 248
Line 440: add the required mock setup to our original test. We can reuse our givenWordToSelect() 
Line 441: helper method to do this.
Line 442: 9.	
Line 443: Add the mock setup to the original test:
Line 444: @Test
Line 445: void startsNewGame() {
Line 446:     var player = new Player();
Line 447:     givenWordToSelect("ARISE");
Line 448:     wordz.newGame(player);
Line 449:     Game game = getGameInRepository();
Line 450:     assertThat(game.getWord()).isEqualTo("ARISE");
Line 451:     assertThat(game.getAttemptNumber()).isZero();
Line 452:     assertThat(game.getPlayer()).isSameAs(player);
Line 453: }
Line 454: 10.	 Rerun all tests and confirm that they all pass:
Line 455: Figure 13.4 – All tests passing
Line 456: We’ve test-driven our first piece of code to start a new game, with a randomly selected word to guess, 
Line 457: and made the tests pass. Before we move on, it is time to consider what – if anything – we should 
Line 458: refactor. We have been tidying the code as we write it, but there is one glaring feature. Take a look at 
Line 459: the two tests. They seem very similar now. The original test has become a superset of the one we used 
Line 460: to test-drive adding the word selection. The selectsRandomWord() test is a scaffolding test that 
Line 461: no longer serves a purpose. There’s only one thing to do with code like that – remove it. As a minor 
Line 462: readability improvement, we can also extract a constant for the Player variable:
Line 463: 1.	
Line 464: Extract a constant for the Player variable:
Line 465: private static final Player PLAYER = new Player();
Line 466: @Test
Line 467: 
Line 468: --- 페이지 272 ---
Line 469: Playing the game
Line 470: 249
Line 471: void startsNewGame() {
Line 472:     givenWordToSelect("ARISE");
Line 473:     wordz.newGame(PLAYER);
Line 474:     Game game = getGameInRepository();
Line 475:     assertThat(game.getWord()).isEqualTo("ARISE");
Line 476:     assertThat(game.getAttemptNumber()).isZero();
Line 477:     assertThat(game.getPlayer()).isSameAs(PLAYER);
Line 478: }
Line 479: 2.	
Line 480: We’ll run all the tests after this to make sure that they all still pass and that 
Line 481: selectsRandomWord() has gone.
Line 482: Figure 13.5 – All tests passing
Line 483: That’s it! We have test-driven out all the behavior we need to start a game. It’s a significant achievement 
Line 484: because that test covers a complete user story. All the domain logic has been tested and is known to 
Line 485: be working. The design looks straightforward. The test code is a clear specification of what we expect 
Line 486: our code to do. This is great progress.
Line 487: Following this refactoring, we can move on to the next development task – code that supports playing 
Line 488: the game.
Line 489: Playing the game
Line 490: In this section, we will build the logic to play the game. The gameplay consists of making a number of 
Line 491: guesses at the selected word, reviewing the score for that guess, and having another guess. The game 
Line 492: ends either when the word has been guessed correctly or when the maximum number of allowed 
Line 493: attempts has been made.
Line 494: We’ll begin by assuming that we are at the start of a typical game, about to make our first guess. We 
Line 495: will also assume that this guess is not completely correct. This allows us to defer decisions about 
Line 496: end-of-the-game behavior, which is a good thing, as we have enough to decide already.
Line 497: 
Line 498: --- 페이지 273 ---
Line 499: Driving the Domain Layer
Line 500: 250
Line 501: Designing the scoring interface
Line 502: The first design decision we must take is what we need to return following a guess at the word. We 
Line 503: need to return the following information to the user:
Line 504: •	 The score for the current guess
Line 505: •	 Whether or not the game is still in play or has ended
Line 506: •	 Possibly the previous history of scoring for each guess
Line 507: •	 Possibly a report of user input errors
Line 508: Clearly, the most important information for the player is the score for the current guess. Without 
Line 509: that, the game cannot be played. As the game has a variable length – ending when either the word 
Line 510: has been guessed, or when a maximum number of guesses has been attempted – we need an indicator 
Line 511: that another guess will be allowed.
Line 512: The idea behind returning the history of scores for previous guesses is that it might help the consumer 
Line 513: of our domain model – ultimately, a user interface of some sort. If we return only the score for the 
Line 514: current guess, the user interface will most likely need to retain its own history of scores, in order to 
Line 515: present them properly. If we return the entire history of scores for this game, that information is easily 
Line 516: available. A good rule of thumb in software is to follow the you ain’t gonna need it (YAGNI) principle. 
Line 517: As there is no requirement for a history of scores, we won’t build that at this stage.
Line 518: The last decision we need to write our test is to think about the programming interface we want for 
Line 519: this. We will choose an assess() method on class Wordz. It will accept String, which is the 
Line 520: current guess from the player. It will return record, which is a modern Java (since Java 14) way of 
Line 521: indicating a pure data structure is to be returned:
Line 522: We've now got enough to write a test. We'll make a new test for all guess-related behavior called class 
Line 523: GuessTest. The test looks like this:
Line 524: @ExtendWith(MockitoExtension.class)
Line 525: public class GuessTest {
Line 526:     private static final Player PLAYER = new Player();
Line 527:     private static final String CORRECT_WORD = "ARISE";
Line 528:     private static final String WRONG_WORD = "RXXXX";
Line 529:     @Mock
Line 530:     private GameRepository gameRepository;
Line 531:     @InjectMocks
Line 532:     private Wordz wordz;
Line 533: 
Line 534: --- 페이지 274 ---
Line 535: Playing the game
Line 536: 251
Line 537:     @Test
Line 538:     void returnsScoreForGuess() {
Line 539:         givenGameInRepository(
Line 540:                        Game.create(PLAYER, CORRECT_WORD));
Line 541:         GuessResult result = wordz.assess(PLAYER, WRONG_WORD);
Line 542:         Letter firstLetter = result.score().letter(0);
Line 543:         assertThat(firstLetter)
Line 544:                .isEqualTo(Letter.PART_CORRECT);
Line 545:     }
Line 546:     private void givenGameInRepository(Game game) {
Line 547:         when(gameRepository
Line 548:            .fetchForPlayer(eq(PLAYER)))
Line 549:               .thenReturn(Optional.of(game));
Line 550:     }
Line 551: }
Line 552: There are no new TDD techniques in the test. It drives out the calling interface for our new assess() 
Line 553: method. We’ve used the static constructor idiom to create the game object using Game.create(). 
Line 554: This method has been added to class Game:
Line 555:     static Game create(Player player, String correctWord) {
Line 556:         return new Game(player, correctWord, 0, false);
Line 557:     }
Line 558: This clarifies the information necessary to create a new game. To get the test to compile, we create 
Line 559: record GuessResult:
Line 560: package com.wordz.domain;
Line 561: import java.util.List;
Line 562: public record GuessResult(
Line 563:         Score score,
Line 564:         boolean isGameOver
Line 565: ) { }
Line 566: 
Line 567: --- 페이지 275 ---
Line 568: Driving the Domain Layer
Line 569: 252
Line 570: We can make the test pass by writing the production code for the assess() method in class 
Line 571: Wordz. To do that, we will reuse the class Word class that we have already written:
Line 572: public GuessResult assess(Player player, String guess) {
Line 573:     var game = gameRepository.fetchForPlayer(player);
Line 574:     var target = new Word(game.getWord());
Line 575:     var score = target.guess(guess);
Line 576:     return new GuessResult(score, false);
Line 577: }
Line 578: The assertion checks only that the score for the first letter is correct. This is intentionally a weak test. 
Line 579: The detailed testing for scoring behavior is done in class WordTest, which we wrote previously. 
Line 580: The test is described as weak, as it does not fully test the returned score, only the first letter of it. Strong 
Line 581: testing of the scoring logic happens elsewhere, in class WordTest. The weak test here confirms 
Line 582: we have something capable of scoring at least one letter correctly and is enough for us to test-drive 
Line 583: the production code. We avoid duplicating tests here.
Line 584: Running the test shows that it passes. We can review the test code and production code to see whether 
Line 585: refactoring will improve their design. At this point, nothing needs our urgent attention. We can move 
Line 586: on to tracking progress through the game.
Line 587: Triangulating game progress tracking
Line 588: We need to track the number of guesses that have been made so that we can end the game after a 
Line 589: maximum number of attempts. Our design choice is to update the attemptNumber field in the 
Line 590: Game object and then store it in GameRepository:
Line 591: 1.	
Line 592: We add a test to drive this code out:
Line 593: @Test
Line 594: void updatesAttemptNumber() {
Line 595:     givenGameInRepository(
Line 596:                Game.create(PLAYER, CORRECT_WORD));
Line 597:     wordz.assess(PLAYER, WRONG_WORD);
Line 598:     var game = getUpdatedGameInRepository();
Line 599:     assertThat(game.getAttemptNumber()).isEqualTo(1);
Line 600: }
Line 601: private Game getUpdatedGameInRepository() {
Line 602: 
Line 603: --- 페이지 276 ---
Line 604: Playing the game
Line 605: 253
Line 606:     ArgumentCaptor<Game> argument
Line 607:             = ArgumentCaptor.forClass(Game.class);
Line 608:     verify(gameRepository).update(argument.capture());
Line 609:     return argument.getValue();
Line 610: }
Line 611: This test introduces a new method, update(), into our interface GameRepository, 
Line 612: responsible for writing the latest game information to storage. The Assert step uses a Mockito 
Line 613: ArgumentCaptor to inspect the Game object that we pass into update(). We have written 
Line 614: a getUpdatedGameInRepository() method to deemphasize the inner workings of how 
Line 615: we check what was passed to the gameRepository.update() method.  assertThat() 
Line 616: in the test verifies that attemptNumber has been incremented. It started at zero, due to 
Line 617: us creating a new game, and so the expected new value is 1. This is the desired behavior for 
Line 618: tracking an attempt to guess the word:
Line 619: 2.	
Line 620: We add the update() method to the GameRepository interface:
Line 621: package com.wordz.domain;
Line 622: public interface GameRepository {
Line 623:     void create(Game game);
Line 624:     Game fetchForPlayer(Player player);
Line 625:     void update(Game game);
Line 626: }
Line 627: 3.	
Line 628: We add the production code to the assess() method in class Wordz to increment 
Line 629: attemptNumber and call update():
Line 630: public GuessResult assess(Player player, String guess) {
Line 631:     var game = gameRepository.fetchForPlayer(player);
Line 632:     game.incrementAttemptNumber();
Line 633:     gameRepository.update(game);
Line 634:     var target = new Word(game.getWord());
Line 635:     var score = target.guess(guess);
Line 636:     return new GuessResult(score, false);
Line 637: }
Line 638: 4.	
Line 639: We add the incrementAttemptNumber() method to class Game:
Line 640: public void incrementAttemptNumber() {
Line 641:     attemptNumber++;
Line 642: }
Line 643: 
Line 644: --- 페이지 277 ---
Line 645: Driving the Domain Layer
Line 646: 254
Line 647: The test now passes. We can think about any refactoring improvements we want to make. There are 
Line 648: two things that seem to stand out:
Line 649: •	 The duplicated test setup between class NewGameTest and class GuessTest.
Line 650: At this stage, we can live with this duplication. The options are to combine both tests into the 
Line 651: same test class, to extend a common test base class, or to use composition. None of them seem 
Line 652: likely to aid readability much. It seems quite nice to have the two different test cases separate 
Line 653: for now.
Line 654: •	 The three lines inside the assess() method must always be called as a unit when we attempt 
Line 655: another guess. It is possible to forget to call one of these, so it seems better to refactor to eliminate 
Line 656: that possible error. We can refactor like this:
Line 657: public GuessResult assess(Player player, String guess) {
Line 658:     var game = gameRepository.fetchForPlayer(player);
Line 659:     Score score = game.attempt( guess );
Line 660:     gameRepository.update(game);
Line 661:     return new GuessResult(score, false);
Line 662: }
Line 663: We move the code that used to be here into the newly created method: attempt() on 
Line 664: class Game:
Line 665: public Score attempt(String latestGuess) {
Line 666:     attemptNumber++;
Line 667:     var target = new Word(targetWord);
Line 668:     return target.guess(latestGuess);
Line 669: }
Line 670: Renaming the method argument from guess to latestGuess improves readability.
Line 671: That completes the code needed to take a guess at the word. Let’s move on to test-driving the code we 
Line 672: will need to detect when a game has ended.
Line 673: Ending the game
Line 674: In this section, we will complete the tests and production code we need to drive out detecting the end 
Line 675: of a game. This will happen when we do either of the following:
Line 676: •	 Guess the word correctly
Line 677: •	 Make our final allowed attempt, based on a maximum number
Line 678: We can make a start by coding the end-of-game detection when we guess the word correctly.
Line 679: 
Line 680: --- 페이지 278 ---
Line 681: Ending the game
Line 682: 255
Line 683: Responding to a correct guess
Line 684: In this case, the player guesses the target word correctly. The game is over, and the player is awarded 
Line 685: a number of points, based on how few attempts were needed before the correct guess was made. We 
Line 686: need to communicate that the game is over and how many points have been awarded, leading to two 
Line 687: new fields in our class GuessResult. We can add a test to our existing class GuessTest 
Line 688: as follows:
Line 689: @Test
Line 690: void reportsGameOverOnCorrectGuess(){
Line 691:     var player = new Player();
Line 692:     Game game = new Game(player, "ARISE", 0);
Line 693:     when(gameRepository.fetchForPlayer(player))
Line 694:                           .thenReturn(game);
Line 695:     var wordz = new Wordz(gameRepository,
Line 696:                            wordRepository, randomNumbers);
Line 697:     var guess = "ARISE";
Line 698:     GuessResult result = wordz.assess(player, guess);
Line 699:     assertThat(result.isGameOver()).isTrue();
Line 700: }
Line 701: This drives out both a new isGameOver()accessor in class GuessResult and the behavior 
Line 702: to make that true:
Line 703: public GuessResult assess(Player player, String guess) {
Line 704:     var game = gameRepository.fetchForPlayer(player);
Line 705:     Score score = game.attempt( guess );
Line 706:     if (score.allCorrect()) {
Line 707:         return new GuessResult(score, true);
Line 708:     }
Line 709:     gameRepository.update(game);
Line 710:     return new GuessResult(score, false);
Line 711: }
Line 712: This itself drives out two new tests in class WordTest:
Line 713: @Test
Line 714: void reportsAllCorrect() {
Line 715: 
Line 716: --- 페이지 279 ---
Line 717: Driving the Domain Layer
Line 718: 256
Line 719:     var word = new Word("ARISE");
Line 720:     var score = word.guess("ARISE");
Line 721:     assertThat(score.allCorrect()).isTrue();
Line 722: }
Line 723: @Test
Line 724: void reportsNotAllCorrect() {
Line 725:     var word = new Word("ARISE");
Line 726:     var score = word.guess("ARI*E");
Line 727:     assertThat(score.allCorrect()).isFalse();
Line 728: }
Line 729: These themselves drive out an implementation in class Score:
Line 730: public boolean allCorrect() {
Line 731:     var totalCorrect = results.stream()
Line 732:             .filter(letter -> letter == Letter.CORRECT)
Line 733:             .count();
Line 734:     return totalCorrect == results.size();
Line 735: }
Line 736: With this, we have a valid implementation for the isGameOver accessor in record GuessResult. 
Line 737: All tests pass. Nothing seems to need refactoring. We’ll move on to the next test.
Line 738: Triangulating the game over due to too many incorrect guesses
Line 739: The next test will drive out the response to exceeding the maximum number of guesses allowed in 
Line 740: a game:
Line 741: @Test
Line 742: void gameOverOnTooManyIncorrectGuesses(){
Line 743:     int maximumGuesses = 5;
Line 744:     givenGameInRepository(
Line 745:             Game.create(PLAYER, CORRECT_WORD,
Line 746:                     maximumGuesses-1));
Line 747:     GuessResult result = wordz.assess(PLAYER, WRONG_WORD);
Line 748: 
Line 749: --- 페이지 280 ---
Line 750: Ending the game
Line 751: 257
Line 752:     assertThat(result.isGameOver()).isTrue();
Line 753: }
Line 754: This test sets up gameRepository to allow one, final guess. It then sets up the guess to be incorrect. 
Line 755: We assert that isGameOver() is true in this case. The test fails initially, as desired. We add an 
Line 756: extra static constructor method in class Game to specify an initial number of attempts.
Line 757: We add the production code to end the game based on a maximum number of guesses:
Line 758: public GuessResult assess(Player player, String guess) {
Line 759:     var game = gameRepository.fetchForPlayer(player);
Line 760:     Score score = game.attempt( guess );
Line 761:     if (score.allCorrect()) {
Line 762:         return new GuessResult(score, true);
Line 763:     }
Line 764:     gameRepository.update(game);
Line 765:     return new GuessResult(score,
Line 766:                            game.hasNoRemainingGuesses());
Line 767: }
Line 768: We add this decision support method to class Game:
Line 769: public boolean hasNoRemainingGuesses() {
Line 770:     return attemptNumber == MAXIMUM_NUMBER_ALLOWED_GUESSES;
Line 771: }
Line 772: All our tests now pass. There is something suspicious about the code, however. It has been very finely 
Line 773: tuned to work only if a guess is correct and within the allowed number of guesses, or when the guess 
Line 774: is incorrect and exactly at the allowed number. It’s time to add some boundary condition tests and 
Line 775: double-check our logic.
Line 776: Triangulating response to guess after game over
Line 777: We need a couple more tests around the boundary conditions of the game over detection. The first 
Line 778: one drives out the response to an incorrect guess being submitted after a correct guess:
Line 779: @Test
Line 780: void rejectsGuessAfterGameOver(){
Line 781:     var gameOver = new Game(PLAYER, CORRECT_WORD,
Line 782:                 1, true);
Line 783: 
Line 784: --- 페이지 281 ---
Line 785: Driving the Domain Layer
Line 786: 258
Line 787:     givenGameInRepository( gameOver );
Line 788:     GuessResult result = wordz.assess(PLAYER, WRONG_WORD);
Line 789:     assertThat(result.isError()).isTrue();
Line 790: }
Line 791: There are a couple of design decisions captured in this test:
Line 792: •	 Once the game ends, we record this in a new field, isGameOver, in class Game.
Line 793: •	 This new field will need to be set whenever the game ends. We will need more tests to drive 
Line 794: that behavior out.
Line 795: •	 We will use a simple error-reporting mechanism – a new field, isError, in class 
Line 796: GuessResult.
Line 797: This leads to a bit of automated refactoring to add the fourth parameter to the class Game 
Line 798: constructor. Then, we can add code to make the test pass:
Line 799: public GuessResult assess(Player player, String guess) {
Line 800:     var game = gameRepository.fetchForPlayer(player);
Line 801:     if(game.isGameOver()) {
Line 802:         return GuessResult.ERROR;
Line 803:     }
Line 804:     Score score = game.attempt( guess );
Line 805:     if (score.allCorrect()) {
Line 806:         return new GuessResult(score, true, false);
Line 807:     }
Line 808:     gameRepository.update(game);
Line 809:     return new GuessResult(score,
Line 810:                    game.hasNoRemainingGuesses(), false);
Line 811: }
Line 812: 
Line 813: --- 페이지 282 ---
Line 814: Ending the game
Line 815: 259
Line 816: The design decision here is that as soon as we fetch the Game object, we check whether the game was 
Line 817: previously marked as being over. If so, we report an error and we’re done. It’s simple and crude but 
Line 818: adequate for our purposes. We also add a static constant, GuessResult.ERROR, for readability:
Line 819:     public static final GuessResult ERROR
Line 820:                   = new GuessResult(null, true, true);
Line 821: One consequence of this design decision is that we must update GameRepository whenever the 
Line 822: Game.isGameOver field changes to true. An example of one of these tests is this:
Line 823: @Test
Line 824: void recordsGameOverOnCorrectGuess(){
Line 825:     givenGameInRepository(Game.create(PLAYER, CORRECT_WORD));
Line 826:     wordz.assess(PLAYER, CORRECT_WORD);
Line 827:     Game game = getUpdatedGameInRepository();
Line 828:     assertThat(game.isGameOver()).isTrue();
Line 829: }
Line 830: Here is the production code to add that recording logic:
Line 831: public GuessResult assess(Player player, String guess) {
Line 832:     var game = gameRepository.fetchForPlayer(player);
Line 833:     if(game.isGameOver()) {
Line 834:         return GuessResult.ERROR;
Line 835:     }
Line 836:     Score score = game.attempt( guess );
Line 837:     if (score.allCorrect()) {
Line 838:         game.end();
Line 839:         gameRepository.update(game);
Line 840:         return new GuessResult(score, true, false);
Line 841:     }
Line 842:     gameRepository.update(game);
Line 843:     return new GuessResult(score,
Line 844: 
Line 845: --- 페이지 283 ---
Line 846: Driving the Domain Layer
Line 847: 260
Line 848:                  game.hasNoRemainingGuesses(), false);
Line 849: }
Line 850: We need another test to drive out the recording of game over when we run out of guesses. That will 
Line 851: lead to a change in the production code. Those changes can be found in GitHub at the link given at 
Line 852: the start of this chapter. They are very similar to the ones made previously.
Line 853: Finally, let’s review our design and see whether we can improve it still further.
Line 854: Reviewing our design
Line 855: We’ve been making small, tactical refactoring steps as we write the code, which is always a good idea. 
Line 856: Like gardening, it is far easier to keep the garden tidy if we pull up weeds before they grow. Even so, 
Line 857: it is worth taking a holistic look at the design of our code and tests before we move on. We may never 
Line 858: get the chance to touch this code again, and it has our name on it. Let’s make it something that we are 
Line 859: proud of and that will be safe and simple for our colleagues to work with in the future.
Line 860: The tests we’ve already written enable us great latitude in refactoring. They have avoided testing specific 
Line 861: implementations, instead testing desired outcomes. They also test larger units of code – in this case, 
Line 862: the domain model of our hexagonal architecture. As a result, without changing any tests, it is possible 
Line 863: to refactor our class Wordz to look like this:
Line 864: package com.wordz.domain;
Line 865: public class Wordz {
Line 866:     private final GameRepository gameRepository;
Line 867:     private final WordSelection selection ;
Line 868:     public Wordz(GameRepository repository,
Line 869:                  WordRepository wordRepository,
Line 870:                  RandomNumbers randomNumbers) {
Line 871:         this.gameRepository = repository;
Line 872:         this.selection =
Line 873:              new WordSelection(wordRepository, randomNumbers);
Line 874:     }
Line 875:     public void newGame(Player player) {
Line 876:         var word = wordSelection.chooseRandomWord();
Line 877:         gameRepository.create(Game.create(player, word));
Line 878:     }
Line 879: 
Line 880: --- 페이지 284 ---
Line 881: Ending the game
Line 882: 261
Line 883: Our refactored assess() method now looks like this:
Line 884:     public GuessResult assess(Player player, String guess) {
Line 885:         Game game = gameRepository.fetchForPlayer(player);
Line 886:         if(game.isGameOver()) {
Line 887:             return GuessResult.ERROR;
Line 888:         }
Line 889:         Score score = game.attempt( guess );
Line 890:         gameRepository.update(game);
Line 891:         return new GuessResult(score,
Line 892:                                game.isGameOver(), false);
Line 893:     }
Line 894: }
Line 895: That’s looking simpler. The class GuessResult constructor code now stands out as being 
Line 896: particularly ugly. It features the classic anti-pattern of using multiple Boolean flag values. We need 
Line 897: to clarify what the different combinations actually mean, to simplify creating the object. One useful 
Line 898: approach is to apply the static constructor idiom once more:
Line 899: package com.wordz.domain;
Line 900: public record GuessResult(
Line 901:         Score score,
Line 902:         boolean isGameOver,
Line 903:         boolean isError
Line 904: ) {
Line 905:     static final GuessResult ERROR
Line 906:          = new GuessResult(null, true, true);
Line 907:     static GuessResult create(Score score,
Line 908:                               boolean isGameOver) {
Line 909:         return new GuessResult(score, isGameOver, false);
Line 910:     }
Line 911: }
Line 912: 
Line 913: --- 페이지 285 ---
Line 914: Driving the Domain Layer
Line 915: 262
Line 916: This simplifies the assess() method by eliminating the need to understand that final Boolean flag:
Line 917: public GuessResult assess(Player player, String guess) {
Line 918:     Game game = gameRepository.fetchForPlayer(player);
Line 919:     if(game.isGameOver()) {
Line 920:         return GuessResult.ERROR;
Line 921:     }
Line 922:     Score score = game.attempt( guess );
Line 923:     gameRepository.update(game);
Line 924:     return GuessResult.create(score, game.isGameOver());
Line 925: }
Line 926: Another improvement to aid understanding concerns creating new instances of class Game. The 
Line 927: rejectsGuessAfterGameOver() test uses Boolean flag values in a four-argument constructor 
Line 928: to set the test up in a game-over state. Let’s make the goal of creating a game-over state explicit. We 
Line 929: can make the Game constructor private, and increase the visibility of the end() method, which is 
Line 930: already used to end a game. Our revised test looks like this:
Line 931: @Test
Line 932: void rejectsGuessAfterGameOver(){
Line 933:     var game = Game.create(PLAYER, CORRECT_WORD);
Line 934:     game.end();
Line 935:     givenGameInRepository( game );
Line 936:     GuessResult result = wordz.assess(PLAYER, WRONG_WORD);
Line 937:     assertThat(result.isError()).isTrue();
Line 938: }
Line 939: The Arrange step is now more descriptive. The four-argument constructor is no longer accessible, 
Line 940: steering future development to use the safer, more descriptive static constructor methods. This improved 
Line 941: design helps prevent defects from being introduced in the future.
Line 942: We have made great progress in this chapter. Following these final refactoring improvements, we have 
Line 943: an easily readable description of the core logic of our game. It is fully backed by FIRST unit tests. We 
Line 944: 
Line 945: --- 페이지 286 ---
Line 946: Summary
Line 947: 263
Line 948: have even achieved a meaningful 100% code coverage of lines of code executed by our tests. This is 
Line 949: shown in the IntelliJ code coverage tool:
Line 950: Figure 13.6 – Code coverage report
Line 951: That’s the core of our game finished. We can start a new game, play a game, and end a game. The game 
Line 952: can be developed further to include features such as awarding a points score based on how quickly the 
Line 953: word was guessed and a high score table for players. These would be added using the same techniques 
Line 954: we have been applying throughout this chapter.
Line 955: Summary
Line 956: We’ve covered a lot of ground in this chapter. We have used TDD to drive out the core application logic 
Line 957: for our Wordz game. We have taken small steps and used triangulation to steadily drive more details 
Line 958: into our code implementation. We have used hexagonal architecture to enable us to use FIRST unit 
Line 959: tests, freeing us from cumbersome integration tests with their test environments. We have employed 
Line 960: test doubles to replace difficult-to-control objects, such as the database and random number generation.
Line 961: We built up a valuable suite of unit tests that are decoupled from specific implementations. This 
Line 962: enabled us to refactor the code freely, ending up with a very nice software design, based on the SOLID 
Line 963: principles, which will reduce maintenance efforts significantly.
Line 964: We finished with a meaningful code coverage report that showed 100% of the lines of production code 
Line 965: were executed by our tests, giving us a high degree of confidence in our work.
Line 966: Next, in Chapter 14, Driving the Database Layer, we will write the database adapter along with an 
Line 967: integration test to implement our GameRepository, using the Postgres database.
Line 968: 
Line 969: --- 페이지 287 ---
Line 970: Driving the Domain Layer
Line 971: 264
Line 972: Questions and answers
Line 973: 1.	
Line 974: Does every method in every class have to have its own unit test?
Line 975: No. That seems to be a common view, but it is harmful. If we use that approach, we are locking 
Line 976: in the implementation details and will not be able to refactor without breaking tests.
Line 977: 2.	
Line 978: What is the significance of 100% code coverage when running our tests?
Line 979: Not much, by itself. It simply means that all the lines of code in the units under the test were 
Line 980: executed during the test run. For us, it means a little more due to our use of test-first TDD. We 
Line 981: know that every line of code was driven by a meaningful test of behavior that is important to 
Line 982: our application. Having 100% coverage is a double-check that we didn’t forget to add a test.
Line 983: 3.	
Line 984: Does 100% code coverage during the test run mean we have perfect code?
Line 985: No. Testing can only reveal the presence of defects, never their absence. We can have 100% 
Line 986: coverage with very low-quality code in terms of readability and edge case handling. It is 
Line 987: important to not attach too much importance to code coverage metrics. For TDD, they serve 
Line 988: as a cross-check that we haven’t missed any boundary condition tests.
Line 989: 4.	
Line 990: Is all this refactoring normal?
Line 991: Yes. TDD is all about rapid feedback loops. Feedback helps us explore design ideas and change 
Line 992: our minds as we uncover better designs. It frees us from the tyranny of having to understand 
Line 993: every detail – somehow – before we start work. We discover a design by doing the work and 
Line 994: have working software to show for it at the end.
Line 995: Further reading
Line 996: •	 AssertJ documentation – read more about the various kinds of assertion matchers built into 
Line 997: AssertJ, as well as details on how to create custom assertions here: https://assertj.
Line 998: github.io/doc/.
Line 999: •	 Refactoring – Improving the Design of Existing Code, Martin Fowler (first edition), 
Line 1000: ISBN 9780201485677:
Line 1001: The bulk of our work in TDD is refactoring code, continuously providing a good-enough 
Line 1002: design to support our new features. This book contains excellent advice on how to approach 
Line 1003: refactoring in a disciplined, step-by-step way.
Line 1004: The first edition of the book uses Java for all its examples, so is more useful to us than the 
Line 1005: JavaScript-based second edition.
Line 1006: 
Line 1007: --- 페이지 288 ---
Line 1008: Further reading
Line 1009: 265
Line 1010: •	 Design Patterns – Elements of Reusable Object-Oriented Software, Gamma, Helm, Vlissides, 
Line 1011: Johnson, ISBN 9780201633610:
Line 1012: A landmark book that cataloged common combinations of classes that occur in object-oriented 
Line 1013: software. Earlier in the chapter, we used a controller class. This is described as a façade pattern, 
Line 1014: in the terms of this book. The listed patterns are free of any kind of framework or software layer 
Line 1015: and so are very useful in building the domain model of hexagonal architecture.
Line 1016: 
Line 1017: --- 페이지 289 ---