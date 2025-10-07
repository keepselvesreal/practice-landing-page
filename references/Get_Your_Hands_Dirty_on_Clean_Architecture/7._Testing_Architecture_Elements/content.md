Line 1: 
Line 2: --- 페이지 64 ---
Line 3: 7. Testing Architecture Elements
Line 4: In many projects I’ve witnessed, automated testing is a mystery. Everyone writes tests as he or she
Line 5: sees fit, because it’s required by some dusted rule documented in a wiki, but no one can answer
Line 6: targeted questions about the team’s testing strategy.
Line 7: This chapter provides a testing strategy for a hexagonal architecture. For each element of our
Line 8: architecture, we’ll discuss the type of test to cover it.
Line 9: The Test Pyramid
Line 10: Let’s start the discussion about testing along the lines of the test pyramid²² in figure 21, which is a
Line 11: metaphor helping us to decide on how many tests of which type we should aim for.
Line 12: Figure 21 - According to the test pyramid, we should create many cheap tests and less expensive ones.
Line 13: The basic statement is that we should have high coverage of fine-grained tests that are cheap to
Line 14: build, easy to maintain, fast-running, and stable. These are unit tests verifying that a single “unit”
Line 15: (usually a class) works as expected.
Line 16: Once tests combine multiple units and cross unit boundaries, architectural boundaries, or even
Line 17: system boundaries, they tend to become more expensive to build, slower to run and more brittle
Line 18: (failing due to some configuration error instead of a functional error). The pyramid tells us that the
Line 19: more expensive those tests become, the less we should aim for a high coverage of these tests, because
Line 20: otherwise we’ll spend too much time building tests instead of new functionality.
Line 21: Depending on the context, the test pyramid is often shown with different layers. Let’s take a look at
Line 22: the layers I chose to discuss testing our hexagonal architecture. Note that the definition of “unit test”,
Line 23: “integration test”, and “system test” varies with context. In one project they may mean a different
Line 24: ²²The test pyramid can be traced back to Mike Cohn’s book “Succeeding with Agile” from 2009.
Line 25: 
Line 26: --- 페이지 65 ---
Line 27: 7. Testing Architecture Elements
Line 28: 59
Line 29: thing than in another. The following are interpretations of these terms as we’ll use them in this
Line 30: chapter.
Line 31: Unit Tests are the base of the pyramid. A unit test usually instantiates a single class and tests its
Line 32: functionality through its interface. If the class under test has dependencies to other classes, those
Line 33: other classes are not instantiated, but replaced with mocks, simulating the behavior of the real classes
Line 34: as it’s needed during the test.
Line 35: Integration tests form the next layer of the pyramid. These tests instantiate a network of multiple
Line 36: units and verify if this network works as expected by sending some data into it through the interface
Line 37: of an entry class. In our interpretation, integration tests will cross the boundary between two layers,
Line 38: so the network of objects is not complete or must work against mocks at some point.
Line 39: System tests, at last, spin up the whole network of objects that make up our application and verify
Line 40: if a certain use case works as expected through all the layers of the application.
Line 41: Above the system tests, there might be a layer of end-to-end tests that include the UI of the
Line 42: application. We’ll not consider end-to-end tests here, since we’re only discussing a backend
Line 43: architecture in this book.
Line 44: Now that we have defined some test types, let’s see which type of test fits best to each of the layers
Line 45: of our hexagonal architecture.
Line 46: Testing a Domain Entity with Unit Tests
Line 47: We start by looking at a domain entity at the center of our architecture. Let’s recall the Account
Line 48: entity from chapter 4 “Implementing a Use Case”. The state of an Account consists of a balance the
Line 49: account had at a certain point in the past (the baseline balance) and a list of deposits and withdrawals
Line 50: (activities) since then.
Line 51: We now want to verify that the withdraw() method works as expected:
Line 52: 1
Line 53: class AccountTest {
Line 54: 2
Line 55: 3
Line 56: @Test
Line 57: 4
Line 58: void withdrawalSucceeds() {
Line 59: 5
Line 60: AccountId accountId = new AccountId(1L);
Line 61: 6
Line 62: Account account = defaultAccount()
Line 63: 7
Line 64: .withAccountId(accountId)
Line 65: 8
Line 66: .withBaselineBalance(Money.of(555L))
Line 67: 9
Line 68: .withActivityWindow(new ActivityWindow(
Line 69: 10
Line 70: defaultActivity()
Line 71: 11
Line 72: .withTargetAccount(accountId)
Line 73: 12
Line 74: .withMoney(Money.of(999L)).build(),
Line 75: 13
Line 76: defaultActivity()
Line 77: 
Line 78: --- 페이지 66 ---
Line 79: 7. Testing Architecture Elements
Line 80: 60
Line 81: 14
Line 82: .withTargetAccount(accountId)
Line 83: 15
Line 84: .withMoney(Money.of(1L)).build()))
Line 85: 16
Line 86: .build();
Line 87: 17
Line 88: 18
Line 89: boolean success = account.withdraw(Money.of(555L), new AccountId(99L));
Line 90: 19
Line 91: 20
Line 92: assertThat(success).isTrue();
Line 93: 21
Line 94: assertThat(account.getActivityWindow().getActivities()).hasSize(3);
Line 95: 22
Line 96: assertThat(account.calculateBalance()).isEqualTo(Money.of(1000L));
Line 97: 23
Line 98: }
Line 99: 24
Line 100: }
Line 101: The above test is a plain unit test that instantiates an Account in a specific state, calls its withdraw()
Line 102: method, and verifies that the withdrawal was successful and had the expected side effects to the
Line 103: state of the Account object under test.
Line 104: The test is rather easy to setup, easy to understand, and it runs very fast. Tests don’t come much
Line 105: simpler than this. Unit tests like this are our best bet to verify the business rules encoded within our
Line 106: domain entities. We don’t need any other type of test, since domain entity behavior has little to no
Line 107: dependencies to other classes.
Line 108: Testing a Use Case with Unit Tests
Line 109: Going a layer outward, the next architecture element to test is the use cases. Let’s look at a test of
Line 110: the SendMoneyService discussed in chapter 4 “Implementing a Use Case”. The “Send Money” use
Line 111: case locks the source Account so no other transaction can change its balance in the meantime. If we
Line 112: can successfully withdraw the money from the source account, we lock the target account as well
Line 113: and deposit the money there. Finally, we unlock both accounts again.
Line 114: We want to verify that everything works as expected when the transaction succeeds:
Line 115: 1
Line 116: class SendMoneyServiceTest {
Line 117: 2
Line 118: 3
Line 119: // declaration of fields omitted
Line 120: 4
Line 121: 5
Line 122: @Test
Line 123: 6
Line 124: void transactionSucceeds() {
Line 125: 7
Line 126: 8
Line 127: Account sourceAccount = givenSourceAccount();
Line 128: 9
Line 129: Account targetAccount = givenTargetAccount();
Line 130: 10
Line 131: 11
Line 132: givenWithdrawalWillSucceed(sourceAccount);
Line 133: 12
Line 134: givenDepositWillSucceed(targetAccount);
Line 135: 
Line 136: --- 페이지 67 ---
Line 137: 7. Testing Architecture Elements
Line 138: 61
Line 139: 13
Line 140: 14
Line 141: Money money = Money.of(500L);
Line 142: 15
Line 143: 16
Line 144: SendMoneyCommand command = new SendMoneyCommand(
Line 145: 17
Line 146: sourceAccount.getId(),
Line 147: 18
Line 148: targetAccount.getId(),
Line 149: 19
Line 150: money);
Line 151: 20
Line 152: 21
Line 153: boolean success = sendMoneyService.sendMoney(command);
Line 154: 22
Line 155: 23
Line 156: assertThat(success).isTrue();
Line 157: 24
Line 158: 25
Line 159: AccountId sourceAccountId = sourceAccount.getId();
Line 160: 26
Line 161: AccountId targetAccountId = targetAccount.getId();
Line 162: 27
Line 163: 28
Line 164: then(accountLock).should().lockAccount(eq(sourceAccountId));
Line 165: 29
Line 166: then(sourceAccount).should().withdraw(eq(money), eq(targetAccountId));
Line 167: 30
Line 168: then(accountLock).should().releaseAccount(eq(sourceAccountId));
Line 169: 31
Line 170: 32
Line 171: then(accountLock).should().lockAccount(eq(targetAccountId));
Line 172: 33
Line 173: then(targetAccount).should().deposit(eq(money), eq(sourceAccountId));
Line 174: 34
Line 175: then(accountLock).should().releaseAccount(eq(targetAccountId));
Line 176: 35
Line 177: 36
Line 178: thenAccountsHaveBeenUpdated(sourceAccountId, targetAccountId);
Line 179: 37
Line 180: }
Line 181: 38
Line 182: 39
Line 183: // helper methods omitted
Line 184: 40
Line 185: }
Line 186: To make the test a little more readable, it’s structured into given/when/then sections that are
Line 187: commonly used in Behavior-Driven Development.
Line 188: In the “given” section, we create the source and target Accounts and put them into the correct state
Line 189: with some methods whose names start with given...(). We also create a SendMoneyCommand to act
Line 190: as input to the use case. In the “when” section, we simply call the sendMoney() method to invoke
Line 191: the use case. The “then” section asserts that the transaction was successful and verifies that certain
Line 192: methods have been called on the source and target Accounts and on the AccountLock instance that
Line 193: is responsible for locking and unlocking the accounts.
Line 194: Under the hood, the test makes use of the Mockito²³ library to create mock objects in the given...()
Line 195: methods. Mockito also provides the then() method to verify if a certain method has been called on
Line 196: a mock object.
Line 197: ²³https://site.mockito.org/
Line 198: 
Line 199: --- 페이지 68 ---
Line 200: 7. Testing Architecture Elements
Line 201: 62
Line 202: Since the use case service under test is stateless, we cannot verify a certain state in the “then”
Line 203: section. Instead, the test verifies that the service interacted with certain methods on its (mocked)
Line 204: dependencies. This means that the test is vulnerable to changes in the structure of the code under
Line 205: test and not only its behavior. This, in turn, means that there is a higher chance that the test has to
Line 206: be modified if the code under test is refactored.
Line 207: With this in mind, we should think hard about which interactions we actually want to verify in the
Line 208: test. It might be a good idea not to verify all interactions as we did in the test above, but instead
Line 209: focus on the most important ones. Otherwise we have to change the test with every single change
Line 210: to the class under test, undermining the value of the test.
Line 211: While this test is still a unit test, it borders on being an integration test, because we’re testing the
Line 212: interaction on dependencies. It’s easier to create and maintain than a full-blown integration test,
Line 213: however, because we’re working with mocks and don’t have to manage the real dependencies.
Line 214: Testing a Web Adapter with Integration Tests
Line 215: Moving outward another layer, we arrive at our adapters. Let’s discuss testing a web adapter.
Line 216: Recall that a web adapter takes input, for example in the form of JSON strings, via HTTP, might
Line 217: do some validation on it, maps the input to the format a use case expects and then passes it to that
Line 218: use case. It then maps the result of the use case back to JSON and returns it to the client via HTTP
Line 219: response.
Line 220: In the test for a web adapter, we want to make certain that all those steps work as expected:
Line 221: 1
Line 222: @WebMvcTest(controllers = SendMoneyController.class)
Line 223: 2
Line 224: class SendMoneyControllerTest {
Line 225: 3
Line 226: 4
Line 227: @Autowired
Line 228: 5
Line 229: private MockMvc mockMvc;
Line 230: 6
Line 231: 7
Line 232: @MockBean
Line 233: 8
Line 234: private SendMoneyUseCase sendMoneyUseCase;
Line 235: 9
Line 236: 10
Line 237: @Test
Line 238: 11
Line 239: void testSendMoney() throws Exception {
Line 240: 12
Line 241: 13
Line 242: mockMvc.perform(
Line 243: 14
Line 244: post("/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amount}",
Line 245: 15
Line 246: 41L, 42L, 500)
Line 247: 16
Line 248: .header("Content-Type", "application/json"))
Line 249: 17
Line 250: .andExpect(status().isOk());
Line 251: 18
Line 252: 
Line 253: --- 페이지 69 ---
Line 254: 7. Testing Architecture Elements
Line 255: 63
Line 256: 19
Line 257: then(sendMoneyUseCase).should()
Line 258: 20
Line 259: .sendMoney(eq(new SendMoneyCommand(
Line 260: 21
Line 261: new AccountId(41L),
Line 262: 22
Line 263: new AccountId(42L),
Line 264: 23
Line 265: Money.of(500L))));
Line 266: 24
Line 267: }
Line 268: 25
Line 269: 26
Line 270: }
Line 271: The above test is a standard integration test for a web controller named SendMoneyController built
Line 272: with the Spring Boot framework. In the method testSendMoney(), we’re creating an input object
Line 273: and then send a mock HTTP request to the web controller. The request body contains the input
Line 274: object as a JSON string.
Line 275: With the isOk() method, we then verify that the status of the HTTP response is 200 and we verify
Line 276: that the mocked use case class has been called.
Line 277: Most responsibilities of a web adapter are covered by this test.
Line 278: We’re not actually testing over the HTTP protocol, since we’re mocking that away with the MockMvc
Line 279: object. We trust that the framework translates everything to and from HTTP properly. No need to
Line 280: test the framework.
Line 281: The whole path from mapping the input from JSON into a SendMoneyCommand object is covered,
Line 282: however. If we built the SendMoneyCommand object as a self-validating command, as explained
Line 283: in chapter 4 “Implementing a Use Case”, we have even made sure that this mapping produces
Line 284: syntactically valid input to the use case. Also, we have verified that the use case is actually called
Line 285: and that the HTTP response has the expected status.
Line 286: So, why is this an integration test and not a unit test? Even though it seems that we’re only testing
Line 287: a single web controller class in this test, there’s a lot more going on under the covers. With the
Line 288: @WebMvcTest annotation we tell Spring to instantiate a whole network of objects that is responsible
Line 289: for responding to certain request paths, mapping between Java and JSON, validating HTTP input,
Line 290: and so on. And in this test, we’re verifying that our web controller works as a part of this network.
Line 291: Since the web controller is heavily bound to the Spring framework, it makes sense to test it integrated
Line 292: into this framework instead of testing it in isolation. If we tested the web controller with a plain unit
Line 293: test, we’d lose coverage of all the mapping and validation and HTTP stuff and we could never be
Line 294: sure if it actually worked in production, where it’s just a cog in the machine of the framework.
Line 295: Testing a Persistence Adapter with Integration Tests
Line 296: For a similar reason it makes sense to cover persistence adapters with integration tests instead of
Line 297: unit tests, since we not only want to verify the logic within the adapter, but also the mapping into
Line 298: the database.
Line 299: 
Line 300: --- 페이지 70 ---
Line 301: 7. Testing Architecture Elements
Line 302: 64
Line 303: We want to test the persistence adapter we built in chapter 6 “Implementing a Persistence Adapter”.
Line 304: The adapter has two methods, one for loading an Account entity from the database and another to
Line 305: save new account activities to the database:
Line 306: 1
Line 307: @DataJpaTest
Line 308: 2
Line 309: @Import({AccountPersistenceAdapter.class, AccountMapper.class})
Line 310: 3
Line 311: class AccountPersistenceAdapterTest {
Line 312: 4
Line 313: 5
Line 314: @Autowired
Line 315: 6
Line 316: private AccountPersistenceAdapter adapterUnderTest;
Line 317: 7
Line 318: 8
Line 319: @Autowired
Line 320: 9
Line 321: private ActivityRepository activityRepository;
Line 322: 10
Line 323: 11
Line 324: @Test
Line 325: 12
Line 326: @Sql("AccountPersistenceAdapterTest.sql")
Line 327: 13
Line 328: void loadsAccount() {
Line 329: 14
Line 330: Account account = adapter.loadAccount(
Line 331: 15
Line 332: new AccountId(1L),
Line 333: 16
Line 334: LocalDateTime.of(2018, 8, 10, 0, 0));
Line 335: 17
Line 336: 18
Line 337: assertThat(account.getActivityWindow().getActivities()).hasSize(2);
Line 338: 19
Line 339: assertThat(account.calculateBalance()).isEqualTo(Money.of(500));
Line 340: 20
Line 341: }
Line 342: 21
Line 343: 22
Line 344: @Test
Line 345: 23
Line 346: void updatesActivities() {
Line 347: 24
Line 348: Account account = defaultAccount()
Line 349: 25
Line 350: .withBaselineBalance(Money.of(555L))
Line 351: 26
Line 352: .withActivityWindow(new ActivityWindow(
Line 353: 27
Line 354: defaultActivity()
Line 355: 28
Line 356: .withId(null)
Line 357: 29
Line 358: .withMoney(Money.of(1L)).build()))
Line 359: 30
Line 360: .build();
Line 361: 31
Line 362: 32
Line 363: adapter.updateActivities(account);
Line 364: 33
Line 365: 34
Line 366: assertThat(activityRepository.count()).isEqualTo(1);
Line 367: 35
Line 368: 36
Line 369: ActivityJpaEntity savedActivity = activityRepository.findAll().get(0);
Line 370: 37
Line 371: assertThat(savedActivity.getAmount()).isEqualTo(1L);
Line 372: 38
Line 373: }
Line 374: 39
Line 375: 
Line 376: --- 페이지 71 ---
Line 377: 7. Testing Architecture Elements
Line 378: 65
Line 379: 40
Line 380: }
Line 381: With @DataJpaTest, we’re telling Spring to instantiate the network of objects that are needed for
Line 382: database access, including our Spring Data repositories that connect to the database. We add some
Line 383: additional @Imports to make sure that certain objects are added to that network. These objects are
Line 384: needed by the adapter under test to map incoming domain objects into database objects, for instance.
Line 385: In the test for the method loadAccount(), we put the database into a certain state using an SQL
Line 386: script. Then, we simply load the account through the adapter API and verify that it has the state
Line 387: that we would expect it to have given the database state in the SQL script.
Line 388: The test for updateActivities() goes the other way around. We’re creating an Account object with
Line 389: a new account activity and pass it to the adapter to persist. Then, we check if the activity has been
Line 390: saved to the database through the API of ActivityRepository.
Line 391: An important aspect of these tests is that we’re not mocking away the database. The tests are actually
Line 392: hitting the database. Had we mocked the database away, the tests would still cover the same lines
Line 393: of code, producing the same high coverage of lines of code. But despite this high coverage the tests
Line 394: would still have a rather high chance of failing in a setup with a real database due to errors in SQL
Line 395: statements or unexpected mapping errors between database tables and Java objects.
Line 396: Note that by default, Spring will spin up an in-memory database to use during tests. This is very
Line 397: practical, as we don’t have to configure anything and the tests will work out of the box.
Line 398: Since this in-memory database is most probably not the database we’re using in production, however,
Line 399: there is still a significant chance of something going wrong with the real database even when the
Line 400: tests worked perfectly against the in-memory database. Databases love to implement their own
Line 401: flavor of SQL, for instance.
Line 402: For this reason, persistence adapter tests should run against the real database. Libraries like
Line 403: Testcontainers²⁴ are a great help in this regard, spinning up a Docker container with a database
Line 404: on demand.
Line 405: Running against the real database has the added benefit that we don’t have to take care of two
Line 406: different database systems. If we’re using the in-memory database during tests, we might have to
Line 407: configure it in a certain way, or we might have to create separate versions of database migration
Line 408: scripts for each database, which is no fun at all.
Line 409: Testing Main Paths with System Tests
Line 410: On top of the pyramid are system tests. A system test starts up the whole application and runs
Line 411: requests against its API, verifying that all our layers work in concert.
Line 412: In a system test for the “Send Money” use case, we send an HTTP request to the application and
Line 413: validate the response as well as the new balance of the account:
Line 414: ²⁴https://www.testcontainers.org/
Line 415: 
Line 416: --- 페이지 72 ---
Line 417: 7. Testing Architecture Elements
Line 418: 66
Line 419: 1
Line 420: @SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
Line 421: 2
Line 422: class SendMoneySystemTest {
Line 423: 3
Line 424: 4
Line 425: @Autowired
Line 426: 5
Line 427: private TestRestTemplate restTemplate;
Line 428: 6
Line 429: 7
Line 430: @Test
Line 431: 8
Line 432: @Sql("SendMoneySystemTest.sql")
Line 433: 9
Line 434: void sendMoney() {
Line 435: 10
Line 436: 11
Line 437: Money initialSourceBalance = sourceAccount().calculateBalance();
Line 438: 12
Line 439: Money initialTargetBalance = targetAccount().calculateBalance();
Line 440: 13
Line 441: 14
Line 442: ResponseEntity response = whenSendMoney(
Line 443: 15
Line 444: sourceAccountId(),
Line 445: 16
Line 446: targetAccountId(),
Line 447: 17
Line 448: transferredAmount());
Line 449: 18
Line 450: 19
Line 451: then(response.getStatusCode())
Line 452: 20
Line 453: .isEqualTo(HttpStatus.OK);
Line 454: 21
Line 455: 22
Line 456: then(sourceAccount().calculateBalance())
Line 457: 23
Line 458: .isEqualTo(initialSourceBalance.minus(transferredAmount()));
Line 459: 24
Line 460: 25
Line 461: then(targetAccount().calculateBalance())
Line 462: 26
Line 463: .isEqualTo(initialTargetBalance.plus(transferredAmount()));
Line 464: 27
Line 465: 28
Line 466: }
Line 467: 29
Line 468: 30
Line 469: private ResponseEntity whenSendMoney(
Line 470: 31
Line 471: AccountId sourceAccountId,
Line 472: 32
Line 473: AccountId targetAccountId,
Line 474: 33
Line 475: Money amount) {
Line 476: 34
Line 477: 35
Line 478: HttpHeaders headers = new HttpHeaders();
Line 479: 36
Line 480: headers.add("Content-Type", "application/json");
Line 481: 37
Line 482: HttpEntity<Void> request = new HttpEntity<>(null, headers);
Line 483: 38
Line 484: 39
Line 485: return restTemplate.exchange(
Line 486: 40
Line 487: "/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amount}",
Line 488: 41
Line 489: HttpMethod.POST,
Line 490: 42
Line 491: request,
Line 492: 43
Line 493: Object.class,
Line 494: 
Line 495: --- 페이지 73 ---
Line 496: 7. Testing Architecture Elements
Line 497: 67
Line 498: 44
Line 499: sourceAccountId.getValue(),
Line 500: 45
Line 501: targetAccountId.getValue(),
Line 502: 46
Line 503: amount.getAmount());
Line 504: 47
Line 505: }
Line 506: 48
Line 507: 49
Line 508: // some helper methods omitted
Line 509: 50
Line 510: }
Line 511: With @SpringBootTest, we’re telling Spring to start up the whole network of objects that makes up
Line 512: the application. We’re also configuring the application to expose itself on a random port.
Line 513: In the test method, we simply create a request, send it to the application, and then check the response
Line 514: status and the new balance of the accounts.
Line 515: We’re using a TestRestTemplate for sending the request, and not MockMvc, as we did earlier in the
Line 516: web adapter test. This means we’re doing real HTTP, bringing the test a little closer to a production
Line 517: environment.
Line 518: Just like we’re going over real HTTP, we’re going through the real output adapters. In our case, this
Line 519: is only a persistence adapter that connects the application to a database. In an application that talks
Line 520: to other systems, we would have additional output adapters in place. It’s not always feasible to have
Line 521: all those third party systems up-and-running, even for a system test, so we might mock them away,
Line 522: after all. Our hexagonal architecture makes this as easy as it can be for us, since we only have to
Line 523: stub out a couple of output port interfaces.
Line 524: Note that I went out of my way to make the test as readable as possible. I hid every bit of ugly logic
Line 525: within helper methods. These methods now form a domain-specific language that we can use to
Line 526: verify the state of things.
Line 527: While a domain-specific language like this is a good idea in any type of test, it’s even more important
Line 528: in system tests. System tests simulate the real users of the application much better than unit or
Line 529: integration test can, so we can use them to verify the application from the viewpoint of the user.
Line 530: This is much easier with a suitable vocabulary at hand. This vocabulary also enables domain experts,
Line 531: who are best suited to embody a user of the application, and who probably aren’t programmers, to
Line 532: reason about the tests and give feedback. There are whole libraries for behavior-driven development
Line 533: like JGiven²⁵ that provide a framework to create a vocabulary for your tests.
Line 534: If we have created unit and integration tests as described in the previous sections, the system tests
Line 535: will cover a lot of the same code. Do they even provide any additional benefit? Yes, they do. Usually
Line 536: they flush out other types of bugs than the unit and integration tests do. Some mapping between
Line 537: the layers could be off, for instance, which we would not notice with the unit and integration tests
Line 538: alone.
Line 539: System tests play out their strength best if they combine multiple use cases to create scenarios. Each
Line 540: scenario represents a certain path a user might typically take through the application. If the most
Line 541: ²⁵http://jgiven.org/
Line 542: 
Line 543: --- 페이지 74 ---
Line 544: 7. Testing Architecture Elements
Line 545: 68
Line 546: important scenarios are covered by passing system tests, we can assume that we haven’t broken
Line 547: them with our latest modifications and are ready to ship.
Line 548: How Much Testing is Enough?
Line 549: A question many project teams I’ve been part of couldn’t answer is how much testing we should
Line 550: do. Is it enough if our tests cover 80% of our lines of code? Should it be higher than that?
Line 551: Line coverage is a bad metric to measure test success. Any goal other than 100% is completely
Line 552: meaningless²⁶, because important parts of the codebase might not be covered at all. And even at
Line 553: 100% we still can’t be sure that every bug has been squashed.
Line 554: I suggest measuring test success in how comfortable we feel to ship the software. If we trust the tests
Line 555: enough to ship after having executed them, we’re good. The more often we ship, the more trust we
Line 556: have in our tests. If we only ship twice a year, no one will trust the tests because they only prove
Line 557: themselves twice a year.
Line 558: This requires a leap of faith the first couple times we ship, but if we make it a priority to fix and
Line 559: learn from bugs in production, we’re on the right track. For each production bug, we should ask
Line 560: the question “Why didn’t our tests catch this bug?”, document the answer, and then add a test that
Line 561: covers it. Over time this will make us comfortable with shipping and the documentation will even
Line 562: provide a metric to gauge our improvement over time.
Line 563: It helps, however, to start with a strategy that defines the tests we should create. One such strategy
Line 564: for our hexagonal architecture is this one:
Line 565: • while implementing a domain entity, cover it with a unit test
Line 566: • while implementing a use case, cover it with a unit test
Line 567: • while implementing an adapter, cover it with an integration test
Line 568: • cover the most important paths a user can take through the application with a system test.
Line 569: Note the words “while implementing”: when tests are done during development of a feature and
Line 570: not after, they become a development tool and no longer feel like a chore.
Line 571: If we have to spend an hour fixing tests each time we add a new field, however, we’re doing
Line 572: something wrong. Probably our tests are too vulnerable to structure changes in the code and we
Line 573: should look at how to improve that. Tests lose their value if we have to modify them for each
Line 574: refactoring.
Line 575: How Does This Help Me Build Maintainable Software?
Line 576: The Hexagonal Architecture style cleanly separates between domain logic and outward facing
Line 577: adapters. This helps us to define a clear testing strategy that covers the central domain logic with
Line 578: unit tests and the adapters with integration tests.
Line 579: ²⁶https://reflectoring.io/100-percent-test-coverage/
Line 580: 
Line 581: --- 페이지 75 ---
Line 582: 7. Testing Architecture Elements
Line 583: 69
Line 584: The input and output ports provide very visible mocking points in tests. For each port, we can decide
Line 585: to mock it, or to use the real implementation. If the ports are each very small and focused, mocking
Line 586: them is a breeze instead of a chore. The less methods a port interface provides, the less confusion
Line 587: there is about which of the methods we have to mock in a test.
Line 588: If it becomes too much of a burden to mock things away or if we don’t know which kind of test we
Line 589: should use to cover a certain part of the codebase, it’s a warning sign. In this regard, our tests have
Line 590: the additional responsibility as a canary - to warn us about flaws in the architecture and to steer us
Line 591: back on the path to creating a maintainable code base.