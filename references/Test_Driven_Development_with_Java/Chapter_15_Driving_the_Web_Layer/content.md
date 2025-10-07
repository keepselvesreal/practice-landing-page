Line 1: 
Line 2: --- 페이지 306 ---
Line 3: 15
Line 4: Driving the Web Layer
Line 5: In this chapter, we complete our web application by adding a web endpoint. We will learn how to 
Line 6: write HTTP integration tests using the built-in Java HTTP client. We will test-drive the web adapter 
Line 7: code that runs this endpoint, using an open source HTTP server framework. This web adapter is 
Line 8: responsible for converting HTTP requests into commands we can execute in our domain layer. At 
Line 9: the end of the chapter, we will assemble all the pieces of our application into a microservice. The web 
Line 10: adapter and database adapters will be linked to the domain model using dependency injection. We 
Line 11: will need to run a few manual database commands, install a web client called Postman, and then we 
Line 12: can play our game.
Line 13: In this chapter, we’re going to cover the following main topics:
Line 14: •	 Starting a new game
Line 15: •	 Playing the game
Line 16: •	 Integrating the application
Line 17: •	 Using the application
Line 18: Technical requirements
Line 19: The code for this chapter is available at https://github.com/PacktPublishing/Test-
Line 20: Driven-Development-with-Java/tree/main/chapter15.
Line 21: Before attempting to run the final application, perform the following steps:
Line 22: 1.	
Line 23: Ensure the Postgres database is running locally.
Line 24: 2.	
Line 25: Ensure the database setup steps from Chapter 14 , Driving the Database Layer, have been completed.
Line 26: 
Line 27: --- 페이지 307 ---
Line 28: Driving the Web Layer
Line 29: 284
Line 30: 3.	
Line 31: Open the Postgres pqsl command terminal and enter the following SQL command:
Line 32: insert into word values (1, 'ARISE'), (2, 'SHINE'), (3, 
Line 33: 'LIGHT'), (4, 'SLEEP'), (5, 'BEARS'), (6, 'GREET'), (7, 
Line 34: 'GRATE');
Line 35: 4.	
Line 36: Install Postman by following the instructions at https://www.postman.com/downloads/.
Line 37: Starting a new game
Line 38: In this section, we will test-drive a web adapter that will provide our domain model with an HTTP 
Line 39: API.  External web clients will be able to send HTTP requests to this endpoint to trigger actions in 
Line 40: our domain model so that we can play the game. The API will return appropriate HTTP responses, 
Line 41: indicating the score for the submitted guess and reporting when the game is over.
Line 42: The following open source libraries will be used to help us write the code:
Line 43: •	 Molecule: This is a lightweight HTTP framework
Line 44: •	 Undertow: This is a lightweight HTTP web server that powers the Molecule framework
Line 45: •	 GSON: This is a Google library that converts between Java objects and  JSON structured data
Line 46: To start building, we first add the required libraries as dependencies to the build.gradle file. Then 
Line 47: we can begin writing an integration test for our HTTP endpoint and test-drive the implementation.
Line 48: Adding required libraries to the project
Line 49: We need to add the three libraries Molecule, Undertow, and Gson to the build.gradle file before 
Line 50: we can use them:
Line 51: Add the following code to the build.gradle file:
Line 52: dependencies {
Line 53:     testImplementation 'org.junit.jupiter:junit-jupiter-
Line 54: api:5.8.2'
Line 55:     testRuntimeOnly 'org.junit.jupiter:junit-jupiter-
Line 56: engine:5.8.2'
Line 57:     testImplementation 'org.assertj:assertj-core:3.22.0'
Line 58:     testImplementation 'org.mockito:mockito-core:4.8.0'
Line 59:     testImplementation 'org.mockito:mockito-junit-
Line 60: jupiter:4.8.0'
Line 61:     testImplementation 'com.github.database-rider:rider-
Line 62: core:1.35.0'
Line 63: 
Line 64: --- 페이지 308 ---
Line 65: Starting a new game
Line 66: 285
Line 67:     testImplementation 'com.github.database-rider:rider-
Line 68: junit5:1.35.0'
Line 69:     implementation 'org.postgresql:postgresql:42.5.0'
Line 70:     implementation 'org.jdbi:jdbi3-core:3.34.0'
Line 71:     implementation 'org.apache.commons:commons-lang3:3.12.0'
Line 72:     implementation 'com.vtence.molecule:molecule:0.15.0'
Line 73:     implementation 'io.thorntail:undertow:2.7.0.Final'
Line 74:     implementation 'com.google.code.gson:gson:2.10'
Line 75: }
Line 76: Writing the failing test
Line 77: We will follow the normal TDD cycle to create our web adapter. When writing tests for objects in 
Line 78: the adapter layer, we must focus on testing the translation between objects in our domain layer and 
Line 79: communications with external systems. Our adapter layer will use the Molecule HTTP framework 
Line 80: to handle HTTP requests and responses.
Line 81: As we have used hexagonal architecture and started with the domain layer, we already know that 
Line 82: the game logic is working. The goal of this test is to prove that the web adapter layer is performing 
Line 83: its responsibility. That is to translate HTTP requests and responses to objects in our domain layer.
Line 84: As ever, we begin by creating a test class:
Line 85: 1.	
Line 86: First, we write our test class. We’ll call it WordzEndpointTest, and it belongs in the com.
Line 87: wordz.adapters.api package:
Line 88: package com.wordz.adapters.api;
Line 89: public class WordzEndpointTest {
Line 90: }
Line 91: The reason for including this package is as part of our hexagonal architecture. Code in this 
Line 92: web adapter is allowed to use anything from the domain model. The domain model itself is 
Line 93: unaware of the existence of this web adapter.
Line 94: Our first test will be to start a new game:
Line 95: @Test
Line 96: void startGame() {
Line 97: }
Line 98: 
Line 99: --- 페이지 309 ---
Line 100: Driving the Web Layer
Line 101: 286
Line 102: 2.	
Line 103: This test needs to capture the design decision that surrounds our intended web API. One decision 
Line 104: is that when a game has successfully started, we will return a simple 204 No Content HTTP 
Line 105: status code. We will start with the assert to capture this decision:
Line 106: @Test
Line 107: void startGame() {
Line 108:     HttpResponse res;
Line 109:     assertThat(res)
Line 110:        .hasStatusCode(HttpStatus.NO_CONTENT.code);
Line 111: }
Line 112: 3.	
Line 113: Next, we write the Act step. The action here is for an external HTTP client to send a request 
Line 114: to our web endpoint. To achieve this, we use the built-in HTTP client provided by Java itself. 
Line 115: We arrange the code to send the request, and then discard any HTTP response body, as our 
Line 116: design does not return a body:
Line 117: @Test
Line 118: void startGame() throws IOException,
Line 119:                         InterruptedException {
Line 120:     var httpClient = HttpClient.newHttpClient();
Line 121:     HttpResponse res
Line 122:         = httpClient.send(req,
Line 123:             HttpResponse.BodyHandlers.discarding());
Line 124:     assertThat(res)
Line 125:        .hasStatusCode(HttpStatus.NO_CONTENT.code);
Line 126: }
Line 127: 4.	
Line 128: The Arrange step is where we capture our decisions about the HTTP request to send. In order to 
Line 129: start a new game, we need a Player object to identify the player. We will send this as a Json 
Line 130: object in the Request body. The request will cause a state change on our server, so we choose 
Line 131: the HTTP POST method to represent that. Finally, we choose a route whose path is /start:
Line 132: @Test
Line 133: private static final Player PLAYER
Line 134:        = new Player("alan2112");
Line 135: void startGame() throws IOException,
Line 136:                         InterruptedException {
Line 137: 
Line 138: --- 페이지 310 ---
Line 139: Starting a new game
Line 140: 287
Line 141:     var req = HttpRequest.newBuilder()
Line 142:        .uri(URI.create("htp://localhost:8080/start"))
Line 143:        .POST(HttpRequest.BodyPublishers
Line 144:             .ofString(new Gson().toJson(PLAYER)))
Line 145:             .build();
Line 146:     var httpClient = HttpClient.newHttpClient();
Line 147:     HttpResponse res
Line 148:         = httpClient.send(req,
Line 149:             HttpResponse.BodyHandlers.discarding());
Line 150:     assertThat(res)
Line 151:        .hasStatusCode(HttpStatus.NO_CONTENT.code);
Line 152: }
Line 153: We see the Gson library being used to convert a Player object into its JSON representation. 
Line 154: We also see a POST method is constructed and sent to the /start path on localhost. 
Line 155: Eventually, we will want to move the localhost detail into configuration. But, for now, it 
Line 156: will get the test working on our local machine.
Line 157: 5.	
Line 158: We can run our integration test and confirm that it fails:
Line 159: Figure 15.1 – A failed test – no HTTP server
Line 160: Unsurprisingly, this test fails because it cannot connect to an HTTP server. Fixing that is our 
Line 161: next task.
Line 162: 
Line 163: --- 페이지 311 ---
Line 164: Driving the Web Layer
Line 165: 288
Line 166: Creating our HTTP server
Line 167: The failing test allows us to test-drive code that implements an HTTP server. We will use the Molecule 
Line 168: library to provide HTTP services to us:
Line 169: 1.	
Line 170: Add an endpoint class, which we will call class WordzEndpoint:
Line 171:     @Test
Line 172:     void startGame() throws IOException,
Line 173:                             InterruptedException {
Line 174:         var endpoint
Line 175:            = new WordzEndpoint("localhost", 8080);
Line 176: The two parameters passed into the WordzEndpoint constructor define the host and port 
Line 177: that the web endpoint will run on.
Line 178: 2.	
Line 179: Using the IDE, we generate the class:
Line 180: package com.wordz.adapters.api;
Line 181: public class WordzEndpoint {
Line 182:     public WordzEndpoint(String host, int port) {
Line 183:     }
Line 184: }
Line 185: In this case, we’re not going to store the host and port details in fields. Instead, we are going to 
Line 186: start a WebServer using a class from the Molecule library.
Line 187: 3.	
Line 188: Create a WebServer using the Molecule library:
Line 189: package com.wordz.adapters.api;
Line 190: import com.vtence.molecule.WebServer;
Line 191: public class WordzEndpoint {
Line 192:     private final WebServer server;
Line 193:     public WordzEndpoint(String host, int port) {
Line 194:         server = WebServer.create(host, port);
Line 195:     }
Line 196: }
Line 197: 
Line 198: --- 페이지 312 ---
Line 199: Starting a new game
Line 200: 289
Line 201: The preceding code is enough to start an HTTP server running and allow the test to connect to 
Line 202: it. Our HTTP server does nothing useful in terms of playing our game. We need to add some 
Line 203: routes to this server along with the code to respond to them.
Line 204: Adding routes to the HTTP server
Line 205: To be useful, the HTTP endpoint must respond to HTTP commands, interpret them, and send them 
Line 206: as commands to our domain layer. As design decisions, we decide on the following:
Line 207: •	 That a /start route must be called to start the game
Line 208: •	 That we will use the HTTP POST method
Line 209: •	 That we will identify which player the game belongs to as JSON data in the POST body
Line 210: To add routes to the  HTTP server, do the following:
Line 211: 1.	
Line 212: Test-drive the /start route. To work in small steps, initially, we will return a NOT_
Line 213: IMPLEMENTED HTTP response code:
Line 214: public class WordzEndpoint {
Line 215:     private final WebServer server;
Line 216:     public WordzEndpoint(String host, int port) {
Line 217:         server = WebServer.create(host, port);
Line 218:         try {
Line 219:             server.route(new Routes() {{
Line 220:                 post("/start")
Line 221:                   .to(request -> startGame(request));
Line 222:             }});
Line 223:         } catch (IOException ioe) {
Line 224:             throw new IllegaStateException(ioe);
Line 225:         }
Line 226:     }
Line 227:     private Response startGame(Request request) {
Line 228:         return Response
Line 229:                  .of(HttpStatus.NOT_IMPLEMENTED)
Line 230:                  .done();
Line 231: 
Line 232: --- 페이지 313 ---
Line 233: Driving the Web Layer
Line 234: 290
Line 235:   }
Line 236: }
Line 237: 2.	
Line 238: We can run the WordzEndpointTest integration test:
Line 239: Figure 15.2 – An incorrect HTTP status
Line 240: The test fails, as expected. We have made progress because the test now fails for a different 
Line 241: reason. We can now connect to the web endpoint, but it does not return the right HTTP 
Line 242: response. Our next task is to connect this web endpoint to the domain layer code and take the 
Line 243: relevant actions to start a game.
Line 244: Connecting to the domain layer
Line 245: Our next task is to receive an HTTP request and translate that into domain layer calls. This involves 
Line 246: parsing JSON request data, using the Google Gson library, into Java objects, then sending that response 
Line 247: data to the class Wordz port:
Line 248: 1.	
Line 249: Add the code to call the domain layer port implemented as class Wordz. We will use 
Line 250: Mockito to create a test double for this object. This allows us to test only the web endpoint 
Line 251: code, decoupled from all other code:
Line 252: @ExtendWith(MockitoExtension.class)
Line 253: public class WordzEndpointTest {
Line 254:     @Mock
Line 255:     private Wordz mockWordz;
Line 256:     @Test
Line 257:     void startGame() throws IOException,
Line 258:                             InterruptedException {
Line 259:         var endpoint
Line 260: 
Line 261: --- 페이지 314 ---
Line 262: Starting a new game
Line 263: 291
Line 264:         = new WordzEndpoint(mockWordz,
Line 265:                             "localhost", 8080);
Line 266: 2.	
Line 267: We need to provide our class Wordz domain object to the class WordzEndpoint 
Line 268: object. We use dependency injection to inject it into the constructor:
Line 269: public class WordzEndpoint {
Line 270:     private final WebServer server;
Line 271:     private final Wordz wordz;
Line 272:     public WordzEndpoint(Wordz wordz,
Line 273:                          String host, int port) {
Line 274:         this.wordz = wordz;
Line 275: 3.	
Line 276: Next, we need to add the code to start a game. To do that, we first extract the Player object 
Line 277: from the JSON data in the request body. That identifies which player to start a game for. 
Line 278: Then we call the wordz.newGame() method. If it is successful, we return an HTTP status 
Line 279: code of 204 No Content, indicating success:
Line 280: private Response startGame(Request request) {
Line 281:     try {
Line 282:         Player player
Line 283:                 = new Gson().fromJson(request.body(),
Line 284:                                       Player.class);
Line 285:         boolean isSuccessful = wordz.newGame(player);
Line 286:         if (isSuccessful) {
Line 287:             return Response
Line 288:                     .of(HttpStatus.NO_CONTENT)
Line 289:                     .done();
Line 290:         }
Line 291:     } catch (IOException e) {
Line 292:         throw new RuntimeException(e);
Line 293:     }
Line 294:     throw new
Line 295:        UnsupportedOperationException("Not
Line 296:                                      implemented");
Line 297: }
Line 298: 
Line 299: --- 페이지 315 ---
Line 300: Driving the Web Layer
Line 301: 292
Line 302: 4.	
Line 303: Now, we can run the test, however, it fails:
Line 304: Figure 15.3 – An incorrect HTTP response
Line 305: It failed because the return value from wordz.newGame() was false. The mock object needs 
Line 306: to be set up to return true.
Line 307: 5.	
Line 308: Return the correct value from the mockWordz stub:
Line 309:    @Test
Line 310: void startsGame() throws IOException,
Line 311:                          InterruptedException {
Line 312:     var endpoint
Line 313:          = new WordzEndpoint(mockWordz,
Line 314:                              "localhost", 8080);
Line 315:     when(mockWordz.newGame(eq(PLAYER)))
Line 316:           .thenReturn(true);
Line 317: 6.	
Line 318: Then, run the test:
Line 319: Figure 15.4 – The test passes
Line 320: 
Line 321: --- 페이지 316 ---
Line 322: Starting a new game
Line 323: 293
Line 324: The integration test passes. The HTTP request has been received, called the domain layer code to start 
Line 325: a new game, and the HTTP response is returned. The next step is to consider refactoring.
Line 326: Refactoring the start game code
Line 327: As usual, once a test passes, we consider what – if anything – we need to refactor.
Line 328: It will be worthwhile to refactor the test to simplify writing new tests by collating common code into 
Line 329: one place:
Line 330: @ExtendWith(MockitoExtension.class)
Line 331: public class WordzEndpointTest {
Line 332:     @Mock
Line 333:     private Wordz mockWordz;
Line 334:     private WordzEndpoint endpoint;
Line 335:     private static final Player PLAYER
Line 336:                        = new Player("alan2112");
Line 337:     private final HttpClient httpClient
Line 338:                        = HttpClient.newHttpClient();
Line 339:     @BeforeEach
Line 340:     void setUp() {
Line 341:         endpoint = new WordzEndpoint(mockWordz,
Line 342:                                   "localhost", 8080);
Line 343:     }
Line 344:     @Test
Line 345:     void startsGame() throws IOException,
Line 346:                              InterruptedException {
Line 347:         when(mockWordz.newGame(eq(player)))
Line 348:                               .thenReturn(true);
Line 349:         var req = requestBuilder("start")
Line 350:                 .POST(asJsonBody(PLAYER))
Line 351:                 .build();
Line 352: 
Line 353: --- 페이지 317 ---
Line 354: Driving the Web Layer
Line 355: 294
Line 356:         var res
Line 357:           = httpClient.send(req,
Line 358:                 HttpResponse.BodyHandlers.discarding());
Line 359:         assertThat(res)
Line 360:              .hasStatusCode(HttpStatus.NO_CONTENT.code);
Line 361:     }
Line 362:     private HttpRequest.Builder requestBuilder(
Line 363:         String path) {
Line 364:         return HttpRequest.newBuilder()
Line 365:                 .uri(URI.create("http://localhost:8080/"
Line 366:                                   + path));
Line 367:     }
Line 368:     private HttpRequest.BodyPublisher asJsonBody(
Line 369:         Object source) {
Line 370:         return HttpRequest.BodyPublishers
Line 371:                  .ofString(new Gson().toJson(source));
Line 372:     }
Line 373: }
Line 374: Handling errors when starting a game
Line 375: One of our design decisions is that a player cannot start a game when one is in progress. We need to 
Line 376: test-drive this behavior. We choose to return an HTTP status of 409 Conflict to indicate that a 
Line 377: game is already in progress for a player and a new one cannot be started for them:
Line 378: 1.	
Line 379: Write the test to return a 409 Conflict if the game is already in progress:
Line 380:     @Test
Line 381:     void rejectsRestart() throws Exception {
Line 382:         when(mockWordz.newGame(eq(player)))
Line 383:                          .thenReturn(false);
Line 384:         var req = requestBuilder("start")
Line 385:                 .POST(asJsonBody(player))
Line 386: 
Line 387: --- 페이지 318 ---
Line 388: Starting a new game
Line 389: 295
Line 390:                 .build();
Line 391:         var res
Line 392:            = httpClient.send(req,
Line 393:                 HttpResponse.BodyHandlers.discarding());
Line 394:         assertThat(res)
Line 395:                .hasStatusCode(HttpStatus.CONFLICT.code);
Line 396:     }
Line 397: 2.	
Line 398: Next, run the test. It should fail, as we have yet to write the implementation code:
Line 399: Figure 15.5 – A failing test
Line 400: 3.	
Line 401: Test-drive the code to report that the game cannot be restarted:
Line 402: private Response startGame(Request request) {
Line 403:     try {
Line 404:         Player player
Line 405:                 = new Gson().fromJson(request.body(),
Line 406:                                       Player.class);
Line 407:         boolean isSuccessful = wordz.newGame(player);
Line 408:         if (isSuccessful) {
Line 409:             return Response
Line 410:                     .of(HttpStatus.NO_CONTENT)
Line 411:                     .done();
Line 412:         }
Line 413: 
Line 414: --- 페이지 319 ---
Line 415: Driving the Web Layer
Line 416: 296
Line 417:         return Response
Line 418:                 .of(HttpStatus.CONFLICT)
Line 419:                 .done();
Line 420:     } catch (IOException e) {
Line 421:         throw new RuntimeException(e);
Line 422:     }
Line 423: }
Line 424: 4.	
Line 425: Run the test again:
Line 426: Figure 15. 6 – The test passes
Line 427: The test passes when run on its own now that the implementation is in place. Let’s run all the 
Line 428: WordzEndpointTests tests to double-check our progress.
Line 429: 5.	
Line 430: Run all WordzEndpointTests:
Line 431: Figure 15.7 – Test failure due to restarting the server
Line 432: Unexpectedly, the tests fail when run one after the other.
Line 433: Fixing the unexpectedly failing tests
Line 434: When we run all of the tests, they now fail. The tests all previously ran correctly when run one at a 
Line 435: time. A recent change has clearly broken something. We lost our test isolation at some point. This 
Line 436: error message indicates the web server is being started twice on the same port, which is not possible.
Line 437: 
Line 438: --- 페이지 320 ---
Line 439: Starting a new game
Line 440: 297
Line 441: The options are to stop the web server after each test or to only start the web server once for all tests. 
Line 442: As this is intended to be a long-running microservice, only starting once seems the better choice here:
Line 443: 1.	
Line 444: Add a @BeforeAll annotation to only start the HTTP server once:
Line 445: @BeforeAll
Line 446: void setUp() {
Line 447:     mockWordz = mock(Wordz.class);
Line 448:     endpoint = new WordzEndpoint(mockWordz,
Line 449:                                  "localhost", 8080);
Line 450: }
Line 451: We change the @BeforeEach annotation to a @BeforeAll annotation to make the endpoint 
Line 452: creation only happen once per test. To support this, we also must create the mock and use an 
Line 453: annotation on the test itself to control the life cycle of objects:
Line 454: @ExtendWith(MockitoExtension.class)
Line 455: @TestInstance(TestInstance.Lifecycle.PER_CLASS)
Line 456: public class WordzEndpointTest {
Line 457: Both tests in WordzEndpointTest now pass.
Line 458: 2.	
Line 459: With all tests passing again, we can consider refactoring the code. A readability improvement 
Line 460: will come from extracting an extractPlayer() method. We can also make the conditional 
Line 461: HTTP status code more concise:
Line 462: private Response startGame(Request request) {
Line 463:     try {
Line 464:         Player player = extractPlayer(request);
Line 465:         boolean isSuccessful = wordz.newGame(player);
Line 466:         HttpStatus status
Line 467:                 = isSuccessful?
Line 468:                     HttpStatus.NO_CONTENT :
Line 469:                     HttpStatus.CONFLICT;
Line 470:             return Response
Line 471:                     .of(status)
Line 472:                     .done();
Line 473:     } catch (IOException e) {
Line 474:         throw new RuntimeException(e);
Line 475: 
Line 476: --- 페이지 321 ---
Line 477: Driving the Web Layer
Line 478: 298
Line 479:     }
Line 480: }
Line 481: private Player extractPlayer(Request request)
Line 482:                                  throws IOException {
Line 483:     return new Gson().fromJson(request.body(),
Line 484:                                Player.class);
Line 485: }
Line 486: We have now completed the major part of the coding needed to start a game. To handle the remaining 
Line 487: error condition, we can now test-drive the code to return 400 BAD REQUEST if the Player object 
Line 488: cannot be read from the JSON payload. We will omit that code here. In the next section, we will move 
Line 489: on to test-driving the code for guessing the target word.
Line 490: Playing the game
Line 491: In this section, we will test-drive the code to play the game. This involves submitting multiple guess 
Line 492: attempts to the endpoint until a game-over response is received.
Line 493: We start by creating an integration test for the new /guess route in our endpoint:
Line 494: 1.	
Line 495: The first step is to code the Arrange step. Our domain model provides the assess() method 
Line 496: on class Wordz to assess the score for a guess, along with reporting whether the game 
Line 497: is over. To test-drive this, we set up the mockWordz stub to return a valid GuessResult 
Line 498: object when the assess() method is called:
Line 499: @Test
Line 500: void partiallyCorrectGuess() {
Line 501:     var score = new Score("-U---");
Line 502:     score.assess("GUESS");
Line 503:     var result = new GuessResult(score, false, false);
Line 504:     when(mockWordz.assess(eq(player), eq("GUESS")))
Line 505:             .thenReturn(result);
Line 506: }
Line 507: 2.	
Line 508: The Act step will call our endpoint with a web request submitting the guess. Our design decision 
Line 509: is to send an HTTP POST request to the /guess route. The request body will contain a 
Line 510: JSON representation of the guessed word. To create this, we will use record GuessRequest 
Line 511: and use Gson to convert that into JSON for us:
Line 512: @Test
Line 513: void partiallyCorrectGuess() {
Line 514: 
Line 515: --- 페이지 322 ---
Line 516: Playing the game
Line 517: 299
Line 518:     var score = new Score("-U---");
Line 519:     score.assess("GUESS");
Line 520:     var result = new GuessResult(score, false, false);
Line 521:     when(mockWordz.assess(eq(player), eq("GUESS")))
Line 522:             .thenReturn(result);
Line 523:     var guessRequest = new GuessRequest(player, "-U---");
Line 524:     var body = new Gson().toJson(guessRequest);
Line 525:     var req = requestBuilder("guess")
Line 526:             .POST(ofString(body))
Line 527:             .build();
Line 528: }
Line 529: 3.	
Line 530: Next, we define the record:
Line 531: package com.wordz.adapters.api;
Line 532: import com.wordz.domain.Player;
Line 533: public record GuessRequest(Player player, String guess) {
Line 534: }
Line 535: 4.	
Line 536: Then, we send the request over HTTP to our endpoint, awaiting the response:
Line 537: @Test
Line 538: void partiallyCorrectGuess() throws Exception {
Line 539:     var score = new Score("-U---");
Line 540:     score.assess("GUESS");
Line 541:     var result = new GuessResult(score, false, false);
Line 542:     when(mockWordz.assess(eq(player), eq("GUESS")))
Line 543:             .thenReturn(result);
Line 544:     var guessRequest = new GuessRequest(player, "-U---");
Line 545:     var body = new Gson().toJson(guessRequest);
Line 546:     var req = requestBuilder("guess")
Line 547:             .POST(ofString(body))
Line 548:             .build();
Line 549: 
Line 550: --- 페이지 323 ---
Line 551: Driving the Web Layer
Line 552: 300
Line 553:     var res
Line 554:        = httpClient.send(req,
Line 555:             HttpResponse.BodyHandlers.ofString());
Line 556: }
Line 557: 5.	
Line 558: Then, we extract the returned body data and assert it against our expectations:
Line 559: @Test
Line 560: void partiallyCorrectGuess() throws Exception {
Line 561:     var score = new Score("-U--G");
Line 562:     score.assess("GUESS");
Line 563:     var result = new GuessResult(score, false, false);
Line 564:     when(mockWordz.assess(eq(player), eq("GUESS")))
Line 565:             .thenReturn(result);
Line 566:     var guessRequest = new GuessRequest(player,
Line 567:                                         "-U--G");
Line 568:     var body = new Gson().toJson(guessRequest);
Line 569:     var req = requestBuilder("guess")
Line 570:             .POST(ofString(body))
Line 571:             .build();
Line 572:     var res
Line 573:        = httpClient.send(req,
Line 574:             HttpResponse.BodyHandlers.ofString());
Line 575:     var response
Line 576:        = new Gson().fromJson(res.body(),
Line 577:                          GuessHttpResponse.class);
Line 578:     // Key to letters in scores():
Line 579:     // C correct, P part correct, X incorrect
Line 580:     Assertions.assertThat(response.scores())
Line 581:         .isEqualTo("PCXXX");
Line 582:     Assertions.assertThat(response.isGameOver())
Line 583: 
Line 584: --- 페이지 324 ---
Line 585: Playing the game
Line 586: 301
Line 587:         .isFalse();
Line 588: }
Line 589: One API design decision here is to return the per-letter scores as a five-character String 
Line 590: object. The single letters X, C, and P are used to indicate incorrect, correct, and partially correct 
Line 591: letters. We capture this decision in the assertion.
Line 592: 6.	
Line 593: We define a record to represent the JSON data structure we will return as a response from 
Line 594: our endpoint:
Line 595: package com.wordz.adapters.api;
Line 596: public record GuessHttpResponse(String scores,
Line 597:                                 boolean isGameOver) {
Line 598: }
Line 599: 7.	
Line 600: As we have decided to POST to a new /guess route, we need to add this route to the routing 
Line 601: table. We also need to bind it to a method that will take action, which we will call guessWord():
Line 602: public WordzEndpoint(Wordz wordz, String host,
Line 603:                      int port) {
Line 604:     this.wordz = wordz;
Line 605:     server = WebServer.create(host, port);
Line 606:     try {
Line 607:         server.route(new Routes() {{
Line 608:             post("/start")
Line 609:                 .to(request -> startGame(request));
Line 610:             post("/guess")
Line 611:                 .to(request -> guessWord(request));
Line 612:         }});
Line 613:     } catch (IOException e) {
Line 614:         throw new IllegalStateException(e);
Line 615:     }
Line 616: }
Line 617: We add an IllegalStateException to rethrow any problems that occur when starting 
Line 618: the HTTP server. For this application, this exception may propagate upwards and cause the 
Line 619: application to stop running. Without a working web server, none of the web code makes sense 
Line 620: to run.
Line 621: 
Line 622: --- 페이지 325 ---
Line 623: Driving the Web Layer
Line 624: 302
Line 625: 8.	
Line 626: We implement the guessWord() method with code to extract the request data from the 
Line 627: POST body:
Line 628: private Response guessWord(Request request) {
Line 629:     try {
Line 630:         GuessRequest gr =
Line 631:              extractGuessRequest(request);
Line 632:         return null ;
Line 633:     } catch (IOException e) {
Line 634:         throw new RuntimeException(e);
Line 635:     }
Line 636: }
Line 637: private GuessRequest extractGuessRequest(Request request) 
Line 638: throws IOException {
Line 639:     return new Gson().fromJson(request.body(),
Line 640:                                GuessRequest.class);
Line 641: }
Line 642: 9.	
Line 643: Now we have the request data, it’s time to call our domain layer to do the real work. We 
Line 644: will capture the GuessResult object returned, so we can base our HTTP response from 
Line 645: the endpoint on it:
Line 646: private Response guessWord(Request request) {
Line 647:     try {
Line 648:         GuessRequest gr =
Line 649:              extractGuessRequest(request);
Line 650:         GuessResult result
Line 651:                 = wordz.assess(gr.player(),
Line 652:                   gr.guess());
Line 653:         return null;
Line 654:     } catch (IOException e) {
Line 655:         throw new RuntimeException(e);
Line 656:     }
Line 657: }
Line 658: 
Line 659: --- 페이지 326 ---
Line 660: Playing the game
Line 661: 303
Line 662: 10.	 We choose to return a different format of data from our endpoint compared to the GuessResult 
Line 663: object returned from our domain model. We will need to transform the result from the 
Line 664: domain model:
Line 665: private Response guessWord(Request request) {
Line 666:     try {
Line 667:         GuessRequest gr =
Line 668:             extractGuessRequest(request);
Line 669:         GuessResult result = wordz.assess(gr.player(),
Line 670:                              gr.guess());
Line 671:         return Response.ok()
Line 672:                 .body(createGuessHttpResponse(result))
Line 673:                 .done();
Line 674:     } catch (IOException e) {
Line 675:         throw new RuntimeException(e);
Line 676:     }
Line 677: }
Line 678: private String createGuessHttpResponse(GuessResult 
Line 679: result) {
Line 680:     GuessHttpResponse httpResponse
Line 681:           = new
Line 682:             GuessHttpResponseMapper().from(result);
Line 683:     return new Gson().toJson(httpResponse);
Line 684: }
Line 685: 11.	 We add an empty version of the object doing the transformation, which is class 
Line 686: GuessHttpResponseMapper. In this first step, it will simply return null:
Line 687: package com.wordz.adapters.api;
Line 688: import com.wordz.domain.GuessResult;
Line 689: public class GuessHttpResponseMapper {
Line 690:     public GuessHttpResponse from(GuessResult result) {
Line 691:         return null;
Line 692:     }
Line 693: }
Line 694: 
Line 695: --- 페이지 327 ---
Line 696: Driving the Web Layer
Line 697: 304
Line 698: 12.	 This is enough to compile and be able to run the WordzEndpointTest test:
Line 699: Figure 15.8 – The test fails
Line 700: 13.	 With a failing test in place, we can now test-drive the details of the transform class. To do this, 
Line 701: we switch to adding a new unit test called class GuessHttpResponseMapperTest.
Line 702: Note
Line 703: The details of this are omitted but can be found on GitHub – it follows the standard approach 
Line 704: used throughout the book.
Line 705: 14.	 Once we have test-driven the detailed implementation of class GuessHttpResponseMapper, 
Line 706: we can rerun the integration test:
Line 707: Figure 15.9 – The endpoint test passes
Line 708: As we see in the preceding image, the integration test has passed! Time for a well-earned coffee break. 
Line 709: Well, mine’s a nice English breakfast tea, but that’s just me. After that, we can test-drive the response 
Line 710: to any errors that occurred. Then it’s time to bring the microservice together. In the next section, we 
Line 711: will assemble our application into a running microservice.
Line 712: Integrating the application
Line 713: In this section, we will bring together the components of our test-driven application. We will form 
Line 714: a microservice that runs our endpoint and provides the frontend web interface to our service. It will 
Line 715: use the Postgres database for storage.
Line 716: 
Line 717: --- 페이지 328 ---
Line 718: Integrating the application
Line 719: 305
Line 720: We need to write a short main() method to link together the major components of our code. This will 
Line 721: involve creating concrete objects and injecting dependencies into constructors. The main() method 
Line 722: exists on class WordzApplication, which is the entry point to our fully integrated web service:
Line 723: package com.wordz;
Line 724: import com.wordz.adapters.api.WordzEndpoint;
Line 725: import com.wordz.adapters.db.GameRepositoryPostgres;
Line 726: import com.wordz.adapters.db.WordRepositoryPostgres;
Line 727: import com.wordz.domain.Wordz;
Line 728: public class WordzApplication {
Line 729:     public static void main(String[] args) {
Line 730:         var config = new WordzConfiguration(args);
Line 731:         new WordzApplication().run(config);
Line 732:     }
Line 733:     private void run(WordzConfiguration config) {
Line 734:         var gameRepository
Line 735:          = new GameRepositoryPostgres(config.getDataSource());
Line 736:         var wordRepository
Line 737:          = new WordRepositoryPostgres(config.getDataSource());
Line 738:         var randomNumbers = new ProductionRandomNumbers();
Line 739:         var wordz = new Wordz(gameRepository,
Line 740:                               wordRepository,
Line 741:                               randomNumbers);
Line 742:         var api = new WordzEndpoint(wordz,
Line 743:                                     config.getEndpointHost(),
Line 744:                                     config.getEndpointPort());
Line 745:         waitUntilTerminated();
Line 746:     }
Line 747: 
Line 748: --- 페이지 329 ---
Line 749: Driving the Web Layer
Line 750: 306
Line 751:     private void waitUntilTerminated() {
Line 752:         try {
Line 753:             while (true) {
Line 754:                 Thread.sleep(10000);
Line 755:             }
Line 756:         } catch (InterruptedException e) {
Line 757:             return;
Line 758:         }
Line 759:     }
Line 760: }
Line 761: The main() method instantiates the domain model, and dependency injects the concrete version 
Line 762: of our adapter classes into it. One notable detail is the waitUntilTerminated()method. This 
Line 763: prevents main() from terminating until the application is closed down. This, in turn, keeps the 
Line 764: HTTP endpoint responding to requests.
Line 765: Configuration data for the application is held in class WordzConfiguration. This has default 
Line 766: settings for the endpoint host and port settings, along with database connection settings. These can 
Line 767: also be passed in as command line arguments. The class and its associated test can be seen in the 
Line 768: GitHub code for this chapter.
Line 769: In the next section, we will use the Wordz web service application using the popular HTTP testing 
Line 770: tool, Postman.
Line 771: Using the application
Line 772: To use our newly assembled web application, first ensure that the database setup steps and the Postman 
Line 773: installation described in the Technical requirements section have been successfully completed. Then 
Line 774: run the main() method of class WordzApplication in IntelliJ. That starts the endpoint, 
Line 775: ready to accept requests.
Line 776: Once the service is running, the way we interact with it is by sending HTTP requests to the endpoint. 
Line 777: Launch Postman and (on macOS) a window that looks like this will appear:
Line 778: 
Line 779: --- 페이지 330 ---
Line 780: Using the application
Line 781: 307
Line 782: Figure 15.10 – Postman home screen
Line 783: We first need to start a game. To do that, we need to send HTTP POST requests to the /start route 
Line 784: on our endpoint. By default, this will be available at http://localhost:8080/start. We need 
Line 785: to send a body, containing the JSON {"name":"testuser"} text.
Line 786: We can send this request from Postman. We click the Create a request button on the home page. This 
Line 787: takes us to a view where we can enter the URL, select the POST method and type our JSON body data:
Line 788: 1.	
Line 789: Create a POST request to start the game:
Line 790: Figure 15.11 – Start a new game
Line 791: 
Line 792: --- 페이지 331 ---
Line 793: Driving the Web Layer
Line 794: 308
Line 795: Click the blue Send button. The screenshot in Figure 15.11 shows both the request that was sent 
Line 796: – in the upper portion of the screen – and the response. In this case, the game was successfully 
Line 797: started for the player named testuser. The endpoint performed as expected and sent an 
Line 798: HTTP status code of 204 No Content. This can be seen in the response panel, towards 
Line 799: the bottom of the screenshot.
Line 800: A quick check of the contents of the game table in the database shows that a row for this game 
Line 801: has been created:
Line 802: wordzdb=# select * from game;
Line 803:  player_name | word  | attempt_number | is_game_over
Line 804: -------------+-------+----------------+--------------
Line 805:  testuser    | ARISE |              0 | f
Line 806: (1 row)
Line 807: wordzdb=#
Line 808: 2.	
Line 809: We can now make our first guess at the word. Let’s try a guess of "STARE". The POST request 
Line 810: for this and the response from our endpoint appears, as shown in the following screenshot:
Line 811: Figure 15.12 – Score returned
Line 812: 
Line 813: --- 페이지 332 ---
Line 814: Summary
Line 815: 309
Line 816: The endpoint returns an HTTP status code of 200 OK. This time, a body of JSON formatted 
Line 817: data is returned. We see "scores":"PXPPC" indicating that the first letter of our guess, S, 
Line 818: appears in the word somewhere but not in the first position. The second letter of our guess, T, 
Line 819: is incorrect and does not appear in the target word. We got two more part-correct letters and 
Line 820: one final correct letter in our guess, which was the letter E at the end.
Line 821: The response also shows "isGameOver":false. We haven’t finished the game yet.
Line 822: 3.	
Line 823: We will make one more guess, cheating slightly. Let’s send a POST request with a guess 
Line 824: of "ARISE":
Line 825: Figure 15.13 – A successful guess
Line 826: Winner! We see "scores":"CCCCC" telling us all five letters of our guess are correct. 
Line 827: "isGameOver":true tells us that our game has ended, on this occasion, successfully.
Line 828: We’ve successfully played one game of Wordz using our microservice.
Line 829: Summary
Line 830: In this section, we have completed our Wordz application. We used an integration test with TDD to 
Line 831: drive out an HTTP endpoint for Wordz. We used open source HTTP libraries – Molecule, Gson, and 
Line 832: Undertow. We made effective use of hexagonal architecture. Using ports and adapters, these frameworks 
Line 833: became an implementation detail rather than a defining feature of our design.
Line 834: 
Line 835: --- 페이지 333 ---
Line 836: Driving the Web Layer
Line 837: 310
Line 838: We assembled our final application to bring together the business logic held in the domain layer with 
Line 839: the Postgres database adapter and the HTTP endpoint adapter. Working together, our application 
Line 840: forms a small microservice.
Line 841: In this final chapter, we have arrived at a small-scale yet typical microservice comprising an HTTP 
Line 842: API and a SQL database. We’ve developed the code test first, using tests to guide our design choices. 
Line 843: We have applied the SOLID principles to improve how our software fits together. We have learned 
Line 844: how the ports and adapters of hexagonal architecture simplify the design of code that works with 
Line 845: external systems. Using hexagonal architecture is a natural fit for TDD, allowing us to develop our 
Line 846: core application logic with FIRST unit tests. We have created both a database adapter and an HTTP 
Line 847: adapter test first, using integration tests. We applied the rhythms of TDD – Red, Green, Refactor and 
Line 848: Arrange, Act and Assert to our work. We have applied test doubles using the Mockito library to stand 
Line 849: in for external systems, simplifying the development.
Line 850: In this book, we have covered a wide range of TDD and software design techniques. We can now 
Line 851: create code with fewer defects, and that is safer and easier to work with.
Line 852: Questions and answers
Line 853: 1.	
Line 854: What further work could be done?
Line 855: Further work could include adding a Continuous Integration (CI) pipeline so that whenever 
Line 856: we commit code, the application gets pulled from source control, built, and all tests run. We 
Line 857: could consider deployment and automation of that. One example might be to package up 
Line 858: the Wordz application and the Postgres database as a Docker image. It would be good to add 
Line 859: database schema automation, using a tool such as Flyway.
Line 860: 2.	
Line 861: Could we replace the Molecule library and use something else for our web endpoint?
Line 862: Yes. As the web endpoint sits in our adapter layer of the hexagonal architecture, it does not 
Line 863: affect the core functionality in the domain model. Any suitable web framework could be used.
Line 864: Further reading
Line 865: •	 https://martinfowler.com/articles/richardsonMaturityModel.html
Line 866: An overview of what a REST web interface means, along with some common variations
Line 867: •	 Java OOP Done Right, Alan Mellor, ISBN 9781527284449
Line 868: The author’s book gives some more details on OO basics with some useful design patterns
Line 869: •	 https://www.postman.com/
Line 870: A popular testing tool that sends HTTP requests and displays responses
Line 871: 
Line 872: --- 페이지 334 ---
Line 873: Further reading
Line 874: 311
Line 875: •	 http://molecule.vtence.com/
Line 876: A lightweight HTTP framework for Java
Line 877: •	 https://undertow.io/
Line 878: An HTTP server for Java that works well with the Molecule framework
Line 879: •	 https://github.com/google/gson
Line 880: Google’s library to convert between Java objects and the JSON format
Line 881: •	 https://aws.amazon.com/what-is/restful-api/
Line 882: Amazon’s guide to REST APIs
Line 883: •	 https://docs.oracle.com/en/java/javase/12/docs/api/java.net.
Line 884: http/java/net/http/HttpClient.html
Line 885: Official Java documentation about the test HHTP client used in this chapter
Line 886: 
Line 887: --- 페이지 335 ---