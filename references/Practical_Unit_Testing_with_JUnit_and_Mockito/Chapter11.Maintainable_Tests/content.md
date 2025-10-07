Line 1: 
Line 2: --- 페이지 223 ---
Line 3: Chapter 11. Maintainable Tests
Line 4: Applications maintainability - the holy grail of software development! We write code every day,
Line 5: trying to make it so good it will withstand the test of time. We hope that we, or our colleagues,
Line 6: working with this code sometime in the future, will be able to understand it at a glance. We hope to be
Line 7: able to introduce changes easily without causing chaos throughout the entire application.
Line 8: We should write our tests with the same attitude, trying to make them maintainable. Why? Because,
Line 9: as we have already discussed, they play a crucial role in supporting and documenting our production
Line 10: code. In this section we will discuss various aspects of the maintainability of tests.
Line 11: 11.1. Test Behaviour, not Methods
Line 12: Follow the whisper of your test methods: "Please keep us small & focused on single
Line 13: behavior".
Line 14: — Mockito documentation
Line 15: The rule we will be discussing in this section is very simple: "Test behaviour, not methods!". This
Line 16: means that when writing tests, we should think about the SUT in terms of its responsibilities - in terms
Line 17: of the contract it has with its client. We should abstract from the SUT’s implementation, which is of
Line 18: only secondary importance. What matters is that the SUT should fulfill the requirements for which it
Line 19: was designed. And to make sure it really does, we should write these requirements in the form of test
Line 20: cases. The requirements know nothing about the actual implementation, and neither should our tests.
Line 21: This may seem trivial, but unfortunately I frequently see this simple rule being violated,
Line 22: which leads me to be think that it is, after all, worth discussing.
Line 23: Below, in Listing 11.1, an example of a suboptimal test of the BankAccount class is presented. Each
Line 24: test method attempts to test a single method of the public API of BankAccount: getBalance(),
Line 25: deposit() and withdraw().
Line 26: In order to better present the main issue of this section, I have decided to keep all tests truncated to a
Line 27: very limited number of test cases. In reality, I would use many more test cases, probably employing
Line 28: parameterized tests.
Line 29: Listing 11.1. One test method per one production code method
Line 30: public class BankAccountTest {
Line 31:     private BankAccount account = new BankAccount();
Line 32:     @Test
Line 33:     void testBalance() { 
Line 34:         account.deposit(200);
Line 35:         assertThat(account.getBalance()).isEqualTo(200);
Line 36:     }
Line 37:     @Test
Line 38:     void testDeposit() { 
Line 39: 208
Line 40: 
Line 41: --- 페이지 224 ---
Line 42: Chapter 11. Maintainable Tests
Line 43:         account.deposit(100);
Line 44:         assertThat(account.getBalance()).isEqualTo(100);
Line 45:         account.deposit(100);
Line 46:         assertThat(account.getBalance()).isEqualTo(200);
Line 47:     }
Line 48:     @Test
Line 49:     void testWithdraw() { 
Line 50:         account.deposit(100);
Line 51:         account.withdraw(30);
Line 52:         assertThat(account.getBalance()).isEqualTo(70);
Line 53:         account.withdraw(20);
Line 54:         assertThat(account.getBalance()).isEqualTo(50);
Line 55:     }
Line 56: }
Line 57: Test for the getBalance() method. Note that it also uses a deposit() method.
Line 58: Test for the deposit() method. It also calls getBalance().
Line 59: Test for the withdraw() method, which likewise also calls getBalance() and deposit()
Line 60: methods.
Line 61: As Listing 11.1 shows, isolation is not possible in unit tests at the level of methods. Each test method
Line 62: calls various methods of the SUT - not only the one they have pretensions to testing. It has to be like
Line 63: that, because you really cannot test the deposit() method without checking the account’s balance
Line 64: (using the getBalance() method).
Line 65: There are also some other issues with this approach. Let us list them:
Line 66: • If any of the test methods should fail, then an error message (e.g. "testDeposit has failed") will not
Line 67: be informative enough for us to instantly understand which of the SUT’s requirements has not been
Line 68: fulfilled (where this is really important from the client’s point of view).
Line 69: • Each of the SUT’s methods is involved in multiple user-stories, so it is very hard to keep a "one test
Line 70: method per production code method" pattern. For example, how might we add a test to the existing
Line 71: code, which would verify that after creation an account has a balance of zero? We could enhance
Line 72: the testBalance() method with an additional assertion, but that would make it prone to fail for
Line 73: more than one reason. Which is not good, and leads to confusion when the test does fail.
Line 74: • Test methods tend to grow as the SUT is enhanced to reflect new requirements.
Line 75: • Sometimes it is hard to decide which of the SUT’s methods is really being tested in a certain
Line 76: scenario (because more than one is being used).
Line 77: • Test methods overlap with each other - e.g. testBalance() is a repetition of what will be tested by
Line 78: testDeposit() and testWithdraw(). In fact, it is hard to say why testBalance() is there at all -
Line 79: probably because a developer felt she/he "needed to have a test for the getBalance() method".
Line 80: When I see test code like this, I know for sure that it was written after the SUT had already
Line 81: been implemented. The structure of the test reflects the structure (implementation) of the SUT
Line 82: code, which is a clear sign of this approach. From what I have observed, such tests rarely cover
Line 83: everything required of the SUT. They check what obviously needs to be checked, given the SUT’s
Line 84: implementation, but do not try to test anything more (thus avoiding solving some of the dilemmas
Line 85: listed above).
Line 86: 209
Line 87: 
Line 88: --- 페이지 225 ---
Line 89: Chapter 11. Maintainable Tests
Line 90: What is interesting is that this test is good enough to achieve 100% code coverage of a
Line 91: valid implementation of the BankAccount class. This is one more reason not to trust the
Line 92: code coverage (see also Section 12.3).
Line 93: Is there a better approach? Yes, and - what is really nice - it does not require any additional work. It
Line 94: only requires us to concentrate on the SUT’s behaviour (which reflects its responsibilities) and write it
Line 95: down in the form of tests.
Line 96: An example of this approach is shown in the two listings below. As can be seen, some of its methods
Line 97: are identical to the previous approach, but the test as a whole has been created with a completely
Line 98: different mindset, and it covers a broader set of the SUT’s responsibilities.
Line 99: Listing 11.2. Testing behaviour, not implementation
Line 100: public class GoodBankAccountTest {
Line 101:     private BankAccount account = new BankAccount();
Line 102:     @Test
Line 103:     void shouldBeEmptyAfterCreation() { 
Line 104:         assertThat(account.getBalance()).isEqualTo(0);
Line 105:     }
Line 106:     @Test
Line 107:     void shouldAllowToCreditAccount() { 
Line 108:         account.deposit(100);
Line 109:         assertThat(account.getBalance()).isEqualTo(100);
Line 110:         account.deposit(100);
Line 111:         assertThat(account.getBalance()).isEqualTo(200);
Line 112:     }
Line 113:     @Test
Line 114:     void shouldAllowToDebitAccount() { 
Line 115:         account.deposit(100);
Line 116:         account.withdraw(30);
Line 117:         assertThat(account.getBalance()).isEqualTo(70);
Line 118:         account.withdraw(20);
Line 119:         assertThat(account.getBalance()).isEqualTo(50);
Line 120:     }
Line 121: ...
Line 122: There is no test for the getBalance() method, because its proper functioning is validated by
Line 123: other tests.
Line 124: This is identical to the previous testDeposit() method, with the exception of the method
Line 125: name, which is much more informative.
Line 126: As above - identical to the testWithdraw() method, but better named.
Line 127: Listing 11.3. Testing behaviour, not implementation
Line 128: ...
Line 129:     @Test
Line 130:     void shouldNotAllowToDebitAnEmptyAccount() { 
Line 131:         // checking an exception is thrown
Line 132: 210
Line 133: 
Line 134: --- 페이지 226 ---
Line 135: Chapter 11. Maintainable Tests
Line 136:         // when withdrawing from empty account
Line 137:     }
Line 138:     @Test
Line 139:     void shouldNotAllowToUseNegativeAmountForCredit() { 
Line 140:         // checking an exception is thrown
Line 141:         // when depositing negative amount of money
Line 142:     }
Line 143:     @Test
Line 144:     void shouldNotAllowToUseNegativeAmountForDebit() { 
Line 145:         // checking an exception is thrown
Line 146:         // when withdrawing negative amount of money
Line 147:     }
Line 148: }
Line 149: New methods added. This was possible because the developer was thinking in terms of the
Line 150: SUT’s responsibility.
Line 151:  The two versions of the BankAccountTest test class differ substantially when it comes to test
Line 152: methods naming. Good test method names include information about the scenario they verify. This
Line 153: topic is discussed in detail in Section 10.2.2.
Line 154: Let us compare what was tested and how, with both approaches.
Line 155: Table 11.1. Comparison of two approaches to testing
Line 156: use-case scenario
Line 157: testing
Line 158: implementation
Line 159: testing behaviour
Line 160: when opening a
Line 161: new account, its
Line 162: balance should be
Line 163: zero
Line 164: oops, forgot about
Line 165: this one!
Line 166: shouldBeEmptyAfterCreation()
Line 167: it is possible to
Line 168: credit an account
Line 169: testDeposit()
Line 170: and
Line 171: testBalance()
Line 172: shouldAllowToCreditAccount()
Line 173: it is possible to
Line 174: debit an account
Line 175: testWithdraw()
Line 176: shouldAllowToDebitAccount()
Line 177: should not allow
Line 178: for accounts
Line 179: misuse
Line 180: oops, forgot about
Line 181: these too!
Line 182: shouldNotAllowToWithrdrawFromEmptyAccount(),
Line 183: shouldNotAllowToUseNegativeAmountForDeposit() and
Line 184: shouldNotAllowToUseNegativeAmountForWithdraw()
Line 185: One might be tempted to claim that this is just a single example, and a biased one at that. Well
Line 186: actually, no. I have witnessed this far too many times to have any doubts about it being how things
Line 187: are. When testing implementation:
Line 188: • only a subset of scenarios is being verified,
Line 189: • test methods are overlapping,
Line 190: • test methods are prone to grow to include all possible scenarios for each method they verify.
Line 191: 211
Line 192: 
Line 193: --- 페이지 227 ---
Line 194: Chapter 11. Maintainable Tests
Line 195: The key is to think about test methods as about mini user stories: each of them should ensure that
Line 196: some functionality important from the client’s point of view is working properly.
Line 197: So, as a rule of thumb, forget about implementation. Think about requirements. TDD might make it
Line 198: easier for you to code like this.
Line 199: Some IDEs offer "a feature" which generates test methods based on production code (so
Line 200: if your class has a doSomething() method, the tool will generate a testDoSomething()
Line 201: method). This can lead you down the wrong path - that of methods testing rather than class
Line 202: responsibilities testing. Avoid such solutions. Stay on the safe side by following the test-
Line 203: first approach. 
Line 204: 11.2. Complexity Leads to Bugs
Line 205: Controlling complexity is the essence of computer programming.
Line 206: — Brian Kernighan
Line 207: Do not put any complexity into your tests! No if structure, no switch statements, no decision
Line 208: making. Otherwise you risk finding yourself in a situation where the results of tests are influenced by
Line 209: two factors at the same time: the quality of the logic of production code and the quality of the logic of
Line 210: test code. This is one too many.
Line 211: If any test fails, you need to discover where the bug is - in the production code or the test code. A
Line 212: worse thing can also happen - it is possible that tests pass thanks to errors in test code unintentionally
Line 213: rectifying errors in production code. (Yes, two wrongs sometimes make a right!) This is a serious
Line 214: danger.
Line 215: Another thing you lose out on by putting logic inside your test code is that it can no longer serve as
Line 216: documentation. Who wants to read documentation that requires the solving of logical puzzles?
Line 217: Remember, what you are supposed to be doing is testing the correctness of production code. Do not
Line 218: make it any harder than necessary.
Line 219: 11.3. Follow the Rules or Suffer
Line 220: Procedural code gets information, then makes decisions. Object-oriented code tells
Line 221: objects to do things.
Line 222: — Alec Sharp
Line 223: Daughter, do not talk with strangers!
Line 224: — Demeter Ancient Greece (700 BC)
Line 225:   The two quotes which open this section refer to two famous principles of good design, both of them
Line 226: notorious for being breached: "Tell, Don’t Ask!"1 and "Law of Demeter"2. The first one states that the
Line 227: object should ask others to do whatever it wants, rather than doing the job based on the data they are
Line 228: willing to provide. The second principle dictates with whom the object is allowed to talk.
Line 229: 1See http://pragprog.com/articles/tell-dont-ask for details.
Line 230: 2See http://en.wikipedia.org/wiki/Law_of_Demeter for a more detailed description.
Line 231: 212
Line 232: 
Line 233: --- 페이지 228 ---
Line 234: Chapter 11. Maintainable Tests
Line 235: This section gives an example of what happens when you break these two rules.
Line 236: 11.3.1. Real Life is Object-Oriented
Line 237: Imagine you get in a taxi. "To the airport, please!", you say, and the driver nods his head. Now, you
Line 238: want to know how long it will take to get there. What question would you rather ask:
Line 239: 1. How long will it take?
Line 240: 2. Please tell me (so I can do the maths myself):
Line 241: a. How far is the airport?
Line 242: b. What is your average speed travelling to the airport from here?
Line 243: I have never heard of anyone who used the second approach. In real life we act quite smartly, asking
Line 244: people who know (or at least should do) and only caring about the result (i.e. leaving the boring
Line 245: details to them). So why on earth do we write code that follows the second approach? And we really
Line 246: do! I see this happening all the time.
Line 247: Let us have a look at an example from the domain of finance3 in order to illustrate the difference
Line 248: between these two approaches. The example is as follows. There is a function that calculates the value
Line 249: of all assets of a client. It takes a collection of funds as a parameter and returns a single number as an
Line 250: output. Each fund consists of two registers. A client has a number of entities within each register.
Line 251: 11.3.2. The Non-Object-Oriented Approach
Line 252: A possible implementation of a Client class is shown in Listing 11.4. Some details have been
Line 253: omitted, so we can concentrate on the crucial part: calculating the value of a client’s assets.
Line 254: Listing 11.4. Client class written using a non-object-oriented approach
Line 255: public class Client {
Line 256:     private final List<IFund> funds;
Line 257:     ...
Line 258:     public BigDecimal getValueOfAllFunds() {
Line 259:         BigDecimal value = BigDecimal.ZERO;
Line 260:         for (IFund f : funds) {
Line 261:             value = value.add(f.getCurrentValue().getValue().multiply(
Line 262:                 new BigDecimal(
Line 263:                     f.getRegisterX().getNbOfUnits()
Line 264:                     + f.getRegisterY().getNbOfUnits()
Line 265:                 )
Line 266:             ));
Line 267:         }
Line 268:         return value;
Line 269:     }
Line 270: 3The example is only a slightly modified version of a real business domain problem and real code that once got implemented as
Line 271: part of some long-forgotten project.
Line 272: 213
Line 273: 
Line 274: --- 페이지 229 ---
Line 275: Chapter 11. Maintainable Tests
Line 276: }
Line 277: As shown in Listing 11.4, a client has to do some complex calculations in order to obtain the result.
Line 278: For each fund it needs to:
Line 279: • get the current fund value (f.getCurrentValue().getValue()), which is a two-step process,
Line 280: because IFund returns ICurrentValue object, which contains the real value,
Line 281: • multiply this value by the number of units in both registers.
Line 282: Then, the results for all funds must be added together to obtain the final amount.
Line 283: If you are seriously into object-oriented programming, you will surely have noticed that the code in
Line 284: Listing 11.4 breaches both of the principles mentioned at the beginning of this section:
Line 285: • "Tell, Don’t Ask!" has been broken, because Client asks for data instead of telling others to give
Line 286: him results,
Line 287: • "Law of Demeter" has been broken, because Client talks with friends of his friends (i.e. with
Line 288: registers and current value, both of which are accessed as friends of funds).
Line 289:  This makes it obvious that we are in trouble. The client seems to know everything about everything,
Line 290: when in fact all they should be interested in is the value of each fund they own. The details of
Line 291: the internal structure of funds should be completely hidden from them, but are not. Based on
Line 292: this observation, we can say that the types used in this example have a serious problem with
Line 293: information hiding4: they reveal their internal design. This goes against the norms of good practice in
Line 294: programming, and will cause problems when the code needs to be changed.
Line 295: …but the main problem with such code is… that it works! The results obtained are
Line 296: correct. This code really calculates what it should. This leads people to conclude that the
Line 297: code itself is also correct. The widespread "If it works, don’t fix it!" approach5 results in
Line 298: such code being left as it is. The problems come later - usually when the code should be
Line 299: changed. This is when the troubles begin.
Line 300: So, right now we will attempt to test it. There are many test cases that should be verified (with
Line 301: different combinations of number of funds and values), but for our purposes it will suffice to choose
Line 302: just one: a client having two funds. This does not sound like a difficult task, does it? Well, let us take
Line 303: a closer look.
Line 304: Okay, so here is what I will need for my test: two test doubles of the IFund type, each
Line 305: of them having a value; so two ICurrentValue test doubles will also be required.
Line 306: Each fund also has two registers, so another four test doubles will be required (of the
Line 307: IRegister type). And it seems like all of these test doubles will be stubs. I only need
Line 308: them because I want them to return some canned values. Anything else? No, these are
Line 309: the main points. So let us get started.
Line 310: — Tomek Thinking Aloud about How to Test Non-Object-Oriented Code
Line 311: The listing is divided into two parts, so it renders better.
Line 312: 4See http://en.wikipedia.org/wiki/Information_hiding
Line 313: 5Please consult [martin2008] for a different approach - the Boy Scout Rule rule: "Leave the campground cleaner than you found
Line 314: it.".
Line 315: 214
Line 316: 
Line 317: --- 페이지 230 ---
Line 318: Chapter 11. Maintainable Tests
Line 319: Listing 11.5. Test of the non-object-oriented Client class - setup
Line 320: public class ClientTest {
Line 321:     private int NB_OF_UNITS_AX = 5; 
Line 322:     private int NB_OF_UNITS_AY = 1;
Line 323:     private int NB_OF_UNITS_BX = 4;
Line 324:     private int NB_OF_UNITS_BY = 1;
Line 325:     private BigDecimal FUND_A_VALUE = new BigDecimal(3);
Line 326:     private BigDecimal FUND_B_VALUE = new BigDecimal(2);
Line 327:     @Test
Line 328:     void totalValueShouldBeEqualToSumOfAllFundsValues() {
Line 329:         Client client = new Client(); 
Line 330:         IFund fundA = mock(IFund.class); 
Line 331:         IFund fundB = mock(IFund.class);
Line 332:         IRegister regAX = mock(IRegister.class);
Line 333:         IRegister regAY = mock(IRegister.class);
Line 334:         IRegister regBX = mock(IRegister.class);
Line 335:         IRegister regBY = mock(IRegister.class);
Line 336:         ICurrentValue currentValueA = mock(ICurrentValue.class);
Line 337:         ICurrentValue currentValueB = mock(ICurrentValue.class);
Line 338:         ...
Line 339: Some primitive values that are also required for this test.
Line 340: A client: our SUT.
Line 341: The SUT’s collaborators - direct and indirect.
Line 342: Listing 11.6. Test of the non-object-oriented Client class - actual tests
Line 343:         ...
Line 344:         when(fundA.getRegisterX()).thenReturn(regAX); 
Line 345:         when(fundA.getRegisterY()).thenReturn(regAY);
Line 346:         when(fundB.getRegisterX()).thenReturn(regBX);
Line 347:         when(fundB.getRegisterY()).thenReturn(regBY);
Line 348:         when(regAX.getNbOfUnits()).thenReturn(NB_OF_UNITS_AX);
Line 349:         when(regAY.getNbOfUnits()).thenReturn(NB_OF_UNITS_AY);
Line 350:         when(regBX.getNbOfUnits()).thenReturn(NB_OF_UNITS_BX);
Line 351:         when(regBY.getNbOfUnits()).thenReturn(NB_OF_UNITS_BY);
Line 352:         when(fundA.getCurrentValue()).thenReturn(currentValueA); 
Line 353:         when(fundB.getCurrentValue()).thenReturn(currentValueB);
Line 354:         when(currentValueA.getValue()).thenReturn(FUND_A_VALUE);
Line 355:         when(currentValueB.getValue()).thenReturn(FUND_B_VALUE);
Line 356:         client.addFund(fundA); 
Line 357:         client.addFund(fundB);
Line 358:     assertThat(client.getValueOfAllFunds()) 
Line 359:       .isEqualByComparingTo(BigDecimal.valueOf((5+1)*3 + (4+1)*2));
Line 360:     }
Line 361: }
Line 362: Instructing stubs on what they should return.
Line 363: Hmm, interesting - instructing a stub to return a stub…
Line 364: 215
Line 365: 
Line 366: --- 페이지 231 ---
Line 367: Chapter 11. Maintainable Tests
Line 368: Setting the SUT in the desired state - it should own two funds.
Line 369: Verification.
Line 370: This test is very long, and it has some really disturbing and confusing features:
Line 371: • the test class knows all about the internalities of funds and registers and is aware of niuances of the
Line 372: algorithm of calculation,
Line 373: • a number of test doubles are required for this test,
Line 374: • the test methods consist mostly of instructions for stubs concerning the values they should return,
Line 375: • stubs are returning stubs.
Line 376: All this makes our test hard to understand and maintain, and also fragile (it needs to be rewritten
Line 377: every time we change anything in the funds value calculation algorithm).
Line 378: And now some really bad news: we would need more than one test like this. We need a test for 0
Line 379: funds, for 1 fund, and for 7 funds (when the marketing guys come up with a brilliant idea of some
Line 380: extra bonus for people who have invested in more than 6 funds), and all this multiplied by various
Line 381: values of funds. Uh, that would hurt really bad.
Line 382: Do We Need Mocks?
Line 383:  In the example as presented so far, we have used test doubles for all collaborators of the Client
Line 384: class. In fact, a few lines of test code could have been spared, if we had used real objects instead of
Line 385: classes. True, but on the other hand:
Line 386: • as discussed in Section 5.5, this would be no more than a short-term solution,
Line 387: • in real life, the values of funds might be fetched from some external source (e.g. a web service),
Line 388: which would make it much harder to test.
Line 389: Because of this, replacing all collaborators with test doubles seems a valid choice.
Line 390: 11.3.3. The Object-Oriented Approach
Line 391: Mentally scarred - no doubt - by what we have just witnessed, let us now try out a different
Line 392: implementation of the Client class, and compare the effort required to test it with that involved in the
Line 393: previous example. This time we shall make our Client more object-oriented.
Line 394: Listing 11.7. The Client class - object-oriented version
Line 395: public class Client {
Line 396:     private final List<IFund> funds;
Line 397:     ...
Line 398:     public BigDecimal getValueOfAllFunds() {
Line 399:         BigDecimal value = BigDecimal.ZERO;
Line 400:         for (IFund f : funds) {
Line 401:             value = value.add(f.getValue()); 
Line 402:         }
Line 403: 216
Line 404: 
Line 405: --- 페이지 232 ---
Line 406: Chapter 11. Maintainable Tests
Line 407:         return value;
Line 408:     }
Line 409: }
Line 410: This time all calculation of fund value is encapsulated within a getValue() method of the
Line 411: IFund type. All the client does is add up the results.
Line 412: Writing a test for such a class is straightforward - we need only two stubs for this (one per each fund
Line 413: that the client has, and we have decided in advance that for the first test, the client will have two
Line 414: funds)
Line 415: Listing 11.8. Test of the object-oriented Client class
Line 416: public class ClientTest {
Line 417:     private final static BigDecimal VALUE_A = new BigDecimal(9);
Line 418:     private final static BigDecimal VALUE_B = new BigDecimal(2);
Line 419:     @Test
Line 420:     void totalValueShouldBeEqualToSumOfAllFundsValues() {
Line 421:         Client client = new Client();
Line 422:         IFund fundA = mock(IFund.class);
Line 423:         IFund fundB = mock(IFund.class);
Line 424:         when(fundA.getValue()).thenReturn(VALUE_A);
Line 425:         when(fundB.getValue()).thenReturn(VALUE_B);
Line 426:         client.addFund(fundA);
Line 427:         client.addFund(fundB);
Line 428:     assertThat(client.getValueOfAllFunds())
Line 429:       .isEqualByComparingTo(VALUE_A.add(VALUE_B));
Line 430:     }
Line 431: }
Line 432: Wow, this differs substantially from what we were seeing before. The test is concise and does not
Line 433: contain any information on the internalities of funds.
Line 434: Pursuing this object-oriented approach further, we would have to write tests for each and every class
Line 435: (e.g. we need a test for implementation of the IFund interface, and also for the IRegister interface),
Line 436: but all of them would be very, very simple indeed. Each of these tests would also depend only on the
Line 437: SUT. No information about other classes would be used within the test code. This is very different
Line 438: from what we saw in Listing 11.5.
Line 439: Coming back to the question we asked when discussing a non-object-oriented version of this test,
Line 440: would it be hard to write tests for 0, 1 and 7 funds? This time the answer is no. It would not be.
Line 441: 11.3.4. How To Deal with Procedural Code?
Line 442: We have just witnessed the (disastrous) impact that procedural code can have on testing. If your code
Line 443: does not adhere to basic rules of object-oriented design, it will be hard to test. Now, let us discuss
Line 444: what is the right way to deal with such code.
Line 445: As usual, the best thing you can do is to act before the damage has been done. Do not let procedural
Line 446: code creep into your codebase! TDD seems to be very good at deterring procedural code. As
Line 447: 217
Line 448: 
Line 449: --- 페이지 233 ---
Line 450: Chapter 11. Maintainable Tests
Line 451: discussed previously, it is very painful to write tests for such code. If you start out with the tests
Line 452: themselves, you will definitely end up coming up with solutions that are more object-oriented (and
Line 453: less procedural).
Line 454: The above advice will not be of much use, though, if you have just inherited 100k lines of procedural
Line 455: code. There are techniques that can help you deal with such an unfortunate situation, but the topic
Line 456: goes beyond the scope of this book. Please refer to the excellent work of [feathers2004] for guidance.
Line 457: 11.3.5. Conclusions
Line 458: As the code examples within this section have demonstrated, bad code makes it hard to write tests.
Line 459: Allow me to back up this claim with two quotes, illustrating the most important points connected with
Line 460: what we have just been discussing.
Line 461: Consistency. It is only a virtue, if you are not a screwup.
Line 462: — Wisdom of the Internet ;)
Line 463:     The misery begins with a single, innocent-seeming line such as "ask object x for the value of y
Line 464: (x.getY()) and make some decisions based on the value of y". If you encounter code which breaches
Line 465: the "Tell, Don’t Ask!" principle, then do not copy and paste it into your code. What you should do,
Line 466: instead, is clean it, usually by adding methods in places where they ought to be6. Then proceed -
Line 467: writing clean, well-designed code.
Line 468: Do not copy other sloppy work! Do not become one of the blind led by the blind! An abyss
Line 469: awaits you if you do. (Wow, that has really got you scared, hasn’t it?)
Line 470: Every time a mock returns a mock, a fairy dies.
Line 471: — Twitter @damianguy 2009 Oct 19
Line 472:  When writing a test requires you to have a test double which returns another test double, then you
Line 473: know you are about to do something very bad indeed. Such a situation indicates that the code you are
Line 474: working with contravenes "Law of Demeter", which is really most regrettable. Repair the code, and
Line 475: only then get down to testing it. After all…you do not want fairies to die, do you?
Line 476: 11.4. Rewriting Tests when the Code
Line 477: Changes
Line 478: A change in the requirements occurs. Developers analyze it and implement the required changes. Then
Line 479: tests are run and some of them fail. You can see the disappointment written all over the developers’
Line 480: faces when they sit down to "fix these *(&(#$ failed tests!".
Line 481: Have you ever witnessed such a scenario? Have you ever had the feeling that your tests are a major
Line 482: nuisance, and that their existence makes the process of introducing changes a good deal longer
Line 483: and harder than it would be without them? Well, I have certainly seen this many times, and have
Line 484: personally become angry at the fact that after having performed some updates of production code I
Line 485: also had to take care of the tests (instead of moving on to another task).
Line 486: 6If you need more information about this, please read about the "Feature Envy" code smell.
Line 487: 218
Line 488: 
Line 489: --- 페이지 234 ---
Line 490: Chapter 11. Maintainable Tests
Line 491: There are two explanations of why this situation is so common. The first relates to the quality of your
Line 492: tests, the second to the code-first approach.
Line 493: Let us agree on something, before we begin. If you rewrite part of your implementation, then it
Line 494: is normal that some of your tests will start to fail. In fact, in the majority of cases this is even
Line 495: desirable: if no tests fail, then it means your tests were not good enough!7 The real problems arise if:
Line 496: • the change which made the tests fail is really a refactoring - it does not influence the observable
Line 497: external behaviour of the SUT,
Line 498: • the failed tests do not seem to have anything to do with the functionality that has changed,
Line 499: • a single change results in many tests failing.
Line 500: The last of the above highlights the fact of there being some duplication in respect of tests – with the
Line 501: result that multiple tests are verifying the same functionality. This is rather simple to spot and fix. The
Line 502: other two issues are more interesting, and will be discussed below.
Line 503: 11.4.1. Avoid Overspecified Tests
Line 504: The most important rule of thumb we follow to keep our tests flexible is: Specify
Line 505: exactly what you want to happen and no more.
Line 506: — JMock tutorial
Line 507: What is an overspecified test? There is no consensus about this, and many examples that can be found
Line 508: describe very different features of tests. For the sake of this discussion, let us accept a very simple
Line 509: "definition": a test is overspecified if it verifies some aspects which are irrelevant to the scenario
Line 510: being tested.
Line 511: Now, which parts of the tests are relevant and which are not? How can we distinguish them just by
Line 512: looking at the test code?
Line 513: Well, good test method names are certainly very helpful in this respect. For example, if we analyze the
Line 514: test in the listing below, we find that it is a little bit overspecified.
Line 515: Listing 11.9. Overspecified test - superfluous verification
Line 516: @Test
Line 517: void itemsAvailableIfTheyAreInStore() {
Line 518:         when(store.itemsLeft(ITEM_NAME)).thenReturn(2); 
Line 519:         assertThat(shop.isAvailable(ITEM_NAME)).isTrue(); 
Line 520:         verify(store).itemsLeft(ITEM_NAME); 
Line 521: }
Line 522: stubbing of store collaborator,
Line 523: asserting on the SUT’s functionality,
Line 524: verifying the collaborator’s behaviour.
Line 525: If this test truly sets out to verify that "items are available if they are in store" (as the test method
Line 526: name claims), then what is the last verification doing? Does it really help to achieve the goal of the
Line 527: 7This is exactly the behaviour that mutation testing takes advantage of; see Section 12.4.
Line 528: 219
Line 529: 
Line 530: --- 페이지 235 ---
Line 531: Chapter 11. Maintainable Tests
Line 532: test? Not really. If this cooperation with the store collaborator is really a valuable feature of the SUT
Line 533: (is it?), then maybe it would be more appropriate to have a second test to verify it:
Line 534: Listing 11.10. Two better-focused tests
Line 535: @Test
Line 536: void itemsAvailableIfTheyAreInStore() {
Line 537:     when(store.itemsLeft(ITEM_NAME)).thenReturn(2);
Line 538:     assertThat(shop.isAvailable(ITEM_NAME)).isTrue();
Line 539: }
Line 540: @Test
Line 541: void shouldCheckStoreForItems() {
Line 542:     shop.isAvailable(ITEM_NAME);
Line 543:     verify(store).itemsLeft(ITEM_NAME);
Line 544: }
Line 545: Each of the tests in Listing 11.10 has only one reason to fail, while the previous version (in Listing
Line 546: 11.9) has two. The tests are no longer overspecified. If we refactor the SUT’s implementation, it may
Line 547: turn out that only one fails, thus making it clear which functionality was broken.
Line 548:  Another test-double based example is the use of specific parameter values ("my item", 7 or new
Line 549: Date(x,y,z)) when something more generic would suffice (anyString(), anyInt(), anyDate())8.
Line 550: Again, the question we should ask is whether these specific values are really important for the test
Line 551: case in hand. If not, let us use more relaxed values.
Line 552:   Also, you might be tempted to test very defensively, to verify that some interactions have not
Line 553: happened. Sometimes this makes sense. For example in Section 5.4.3 we verified whether no
Line 554: messages had been sent to some collaborators. And such a test was fine - it made sure that the
Line 555: unsubscribe feature worked fine. However, do not put such verifications in when they are not
Line 556: necessary. You could guard each and every one of the SUT’s collaborators with verifications that
Line 557: none of their methods have been called9, but do not do so, unless they are important relative to the
Line 558: given scenario. Likewise, checking whether certain calls to collaborators happened in the order
Line 559: requested (using Mockito’s inOrder() method) will usually just amount to overkill.   
Line 560: We can find numerous examples of overspecified tests outside of the interactions testing domain,
Line 561: as well. A common case is to expect a certain exact form of text, where what is in fact important is
Line 562: only that it should contain several statements. Like with the example discussed above, it is usually
Line 563: possible to divide such tests into two smaller, more focused ones. For example, the first test could
Line 564: check whether a message that has been created contains the user’s name and address, while the second
Line 565: one might perform a full text-matching. This is also an example of when test dependencies make
Line 566: sense: there is no point in bothering with an exact message comparison (which is what the second test
Line 567: verifies), if you know that it does not contain any vital information (verified by the first test).
Line 568: Based on what we have learned so far, we can say that a good rule of thumb for writing decent,
Line 569: focused tests is as follows: test only the minimally necessary set of features using each test
Line 570: method.
Line 571: 8See Section 7.7 for discussion and more examples.
Line 572: 9Mockito provides some interesting functions for this - verifyZeroInteractions() and
Line 573: verifyNoMoreInteractions().
Line 574: 220
Line 575: 
Line 576: --- 페이지 236 ---
Line 577: Chapter 11. Maintainable Tests
Line 578: As is by no means unusual where problems connected with tests are concerned, the real
Line 579: culprit may be the production code. If your test really needs to repeat the petty details of
Line 580: the SUT’s implementation (which will certainly lead to it being overspecified), then maybe
Line 581: the problem lies with how the SUT works with its collaborators. Does the SUT respect the
Line 582: "Tell-Don’t-Ask!" principle?
Line 583: 11.4.2. Are You Really Coding Test-First?
Line 584: So the change request came. A developer updated the production code, and then also worked
Line 585: on the failed tests which stopped working because of the implemented change. Wait! What? By
Line 586: implementing changes in production code first, we have just reverted to code-first development, with
Line 587: all its issues! The price that we pay is that now we will have to rewrite some tests looking at the code
Line 588: we wrote a few minutes ago. But this is boring: such tests will probably not find any bugs, and they
Line 589: themselves will most probably be very closely linked to the implementation of the production code (as
Line 590: was already discussed in Chapter 4, Test Driven Development).
Line 591: Much better results (and less frustration for developers) can be achieved by trying to mimic the TDD
Line 592: approach, following the order of actions given below:
Line 593: • requirements change,
Line 594: • developers analyze which tests should be updated to reflect the new requirements,
Line 595: • tests are updated (and fail because code does not meet the new requirements),
Line 596: • developers analyze what changes should be introduced into the production code,
Line 597: • code is updated and tests pass.
Line 598: This is somewhat different from the TDD approach as we have observed it so far. If we
Line 599: write a new functionality, then we ensure that each individual test that fails is dealt with at
Line 600: once. However, when the requirements of an existing functionality change, we may find
Line 601: ourselves forced to rewrite several tests at once, and then have to deal with all of them
Line 602: failing.
Line 603: We may sum things up here by saying that in order to avoid having to fix tests after code changes
Line 604: (which is pretty annoying, let’s face it), you should:
Line 605: • write good tests (i.e. loosely coupled to implementation), minimizing the number of failed tests,
Line 606: • use test-first in all phases of the development process - both when working on new features and
Line 607: when introducing changes to the existing codebase.
Line 608: 11.4.3. Conclusions
Line 609: The mime: Developing the code first and then repeating what the code does with
Line 610: expectations mocks. This makes the code drive the tests rather than the other way
Line 611: around. Usually leads to excessive setup and poorly named tests that are hard to see
Line 612: what they do. 
Line 613: — James Carr
Line 614: 221
Line 615: 
Line 616: --- 페이지 237 ---
Line 617: Chapter 11. Maintainable Tests
Line 618: As with many other things related to quality, how you start makes a difference. If you start
Line 619: with production code, then your tests will (inevitably, as experience proves) contain too many
Line 620: implementation details, and thus become fragile. They will start to fail every time you touch the
Line 621: production code. But you can also start from the other end: writing tests first or, rather, designing your
Line 622: production code using tests. Do that and your tests will not really be testing classes, so much as the
Line 623: functionalities embedded within them, and as such will have more chances of staying green when
Line 624: classes change.
Line 625: Of course, it would be naive to expect that your tests can survive any changes to production code.
Line 626: We already know that many of our tests focus on interactions of objects (and to do so, use knowledge
Line 627: about the internal implementation of those objects), so such false hopes should be abandoned. The
Line 628: question remains, how many tests will be undermined by a single change in your production code, and
Line 629: how easy will it be to update them so they meet the altered requirements.
Line 630: Probably the most important lesson we should remember is that we should write tests which verify
Line 631: the expected outcome of systems behaviour, and not the behaviour itself. If possible, let us verify
Line 632: that the system works properly by analyzing returned values. Only when this is not possible should we
Line 633: resort to interactions testing. As Gerard Meszaros puts it (see [meszaros2007]): "use the front door".
Line 634: The focus should be on the goal of the test. There is usually a single feature that is tested by each test.
Line 635: We should put aside anything that is not really essential to its verification. For example, by using
Line 636: stubs (whose behaviour is not verified) instead of mocks (which are verified) whenever possible.
Line 637: Another example is the use of more argument matchers - both in stubbing and verification (see
Line 638: Section 7.7).
Line 639: And finally, now for some very obvious advice: your tests should be run very frequently. If not, then
Line 640: one day you will learn that 50% of them need to be rewritten. And then there will be nothing you can
Line 641: do - except wail in despair!
Line 642: 11.5. Things Too Simple To Break
Line 643: Yep, you should be unit testing every breakable line of code.
Line 644: — Bob Gregory
Line 645: It’s necessary to be very good at testing to decide correctly when you don’t need it, and
Line 646: then very good at programming to get away with it.
Line 647: — Twitter @RonJeffries 2012 Jan 31
Line 648: After reading about the benefits of developer tests, you should be tempted to test everything. Very
Line 649: good, this is the right attitude. If you code test-first, then you get high code coverage "for free".
Line 650: Everything is tested as a result of writing methods to satisfy a failed test. But if you follow the code-
Line 651: first approach, then you might quickly start questioning the idea of testing everything. In the case of
Line 652: some code parts, writing unit tests seems superfluous. This section is devoted to exactly these sorts of
Line 653: doubt or uncertainty.
Line 654: Please note, that only a minority of methods are too simple to be considered
Line 655: "unbreakable". Most of the code you write calls for decent tests!
Line 656: Let us take the example of simple getter/setter methods, as shown in Listing 11.11.
Line 657: 222
Line 658: 
Line 659: --- 페이지 238 ---
Line 660: Chapter 11. Maintainable Tests
Line 661: Listing 11.11. Getters/Setters - too simple to break
Line 662: public class User {
Line 663:     private String name;
Line 664:     public String getName() {
Line 665:         return name;
Line 666:     }
Line 667:     public void setName(String name) {
Line 668:         this.name = name;
Line 669:     }
Line 670: }
Line 671: Yes, you definitely can write a test for this code - but please ask yourself: what kind of bugs, current
Line 672: or future, do you expect to catch by having such a test?
Line 673: In my opinion there is no sense to writing tests for such code after the code has already been written.
Line 674: There are two reasons for this, which are as follows:
Line 675: • there is no logic there worth testing,
Line 676: • the code has probably been generated by the IDE (which then eliminates the threat of a silly
Line 677: copy&paste error).
Line 678: However, if the getter and setter methods are to be changed, entailing that some complexity will be
Line 679: added (even of the simplest sort), then a test should be created. For example, if the setName() method
Line 680: evolves and takes care of validation, along the lines shown in Listing 11.12, then it surely should be
Line 681: tested.
Line 682: Listing 11.12. Getters/Setters with validation - not so simple anymore
Line 683: public void setName(String name) {
Line 684:     if (name == null || name.isEmpty()) {
Line 685:         throw new IllegalArgumentException();
Line 686:     }
Line 687:     this.name = name;
Line 688: }
Line 689: Many people argue that because of the possible future evolution of code (which is hard to predict
Line 690: when the first version is actually being written), you should write a test even for such trivial cases as
Line 691: the first version of the setName() method (the one without validation). I tend to disagree, and I would
Line 692: encourage you to refrain from writing such tests. On the other hand, once things get complicated it is
Line 693: crucial to write them. Then there is no excuse, and tests have to be written.
Line 694: It is true that adding tests for even these simple methods guards against the possibility
Line 695: that someone refactors and makes the methods "not-so-simple" anymore. In that case,
Line 696: though, the refactorer needs to be aware that the method is now complex enough to
Line 697: break, and should write tests for it - and preferably before the refactoring.
Line 698: — J.B. Raisenberg JUnit FAQ
Line 699: However, none of this matters if you write code test-first. In that case, every method will be preceded
Line 700: with a case of a test failing. The complexity does not matter. If it exists, there must be a test for it. It
Line 701: does not necessarily mean that your test code will be full of trivial getter/setter tests. On the contrary,
Line 702: 223
Line 703: 
Line 704: --- 페이지 239 ---
Line 705: Chapter 11. Maintainable Tests
Line 706: when your design is being guided by tests, you might well find yourself writing less getters and
Line 707: setters than you used to. This is one of the benefits of allowing design to be driven by functionality
Line 708: requirements (expressed in the form of tests).
Line 709: Returning to the code-first approach, let us take a look at another example, which shows a piece of
Line 710: code often included in the "too simple to break" category. Listing 11.13 shows a simple delegator - a
Line 711: method whose main task is to tell some other object to do the job.
Line 712: Listing 11.13. Delegator - too simple to break
Line 713: public class DelegatorExample {
Line 714:     private Collaborator collaborator;
Line 715:     public void delegate() {
Line 716:         collaborator.doSomething();
Line 717:     }
Line 718: }
Line 719: True, proper testing of such simple code does require some effort. If you are to use test doubles
Line 720: (which you probably should do), then the test will probably be longer, and even more complicated,
Line 721: than the tested method itself. This will definitely discourage us from writing unit tests - especially in
Line 722: cases where the benefits are not clearly visible. There is no easy answer to the question of whether
Line 723: you should write a test for such a method. It depends on (at least) three factors, namely:
Line 724: • the type (i.e. specific features) of the Collaborator class,
Line 725: • the complexity of the delegating method,
Line 726: • the existence of other types of test.
Line 727: Let us concentrate on these three factors, and run through a few comments that seem relevant to the
Line 728: issue:
Line 729: • there is usually (if not always) something more involved than simply telling the collaborator to do
Line 730: the job. A delegating method will take some arguments and pass them to the collaborator, often
Line 731: performing some actions before it does so (validation of parameters, creation of some objects based
Line 732: on received parameters, etc.).
Line 733: • the collaborator’s doSomething() method will often return some values being used by the SUT in
Line 734: diverse ways,
Line 735: • a collaborator’s doSomething() method might throw exceptions, which will somehow have to be
Line 736: handled by the SUT,
Line 737: • other types of test - e.g. integration tests - might cover this functionality. For example, an
Line 738: integration test might check if a class of service layer delegates tasks to a class of DAO layer.
Line 739: However, it is rare for integration tests to cover all the possible scenarios (i.e. exceptions thrown by
Line 740: collaborators), so there might still be some gaps to be filled by unit tests.
Line 741: My point is that the rather simple appearance of such delegating methods may be deceptive. There can
Line 742: be much more to them than meets the eye. By thinking about possible usage scenarios and interactions
Line 743: between the SUT and collaborators, you can reveal this hidden complexity and test it. But, as has
Line 744: 224
Line 745: 
Line 746: --- 페이지 240 ---
Line 747: Chapter 11. Maintainable Tests
Line 748: already been said, every instance of such code can be considered individually, and there might be
Line 749: cases where writing a test is a waste of time.
Line 750: Once again: you had better write tests. I have seen enough bugs hidden in seemingly
Line 751: trivial code written by some pretty experienced developers to understand that we should be
Line 752: writing tests by default.
Line 753: 11.6. Conclusions
Line 754: Among the topics discussed in this chapter, there are two fundamental things that I would like you
Line 755: to remember. The first is the Test behaviour, not implementation! rule: if you stick to this, it will
Line 756: guide you towards high-quality testing (on every level, not only for unit tests). The second can be
Line 757: expressed by two rules that apply to production code, commonly known as the Law of Demeter and
Line 758: the Tell, Don’t Ask! principle. Expect trouble when testing code that does not abide by either of them.
Line 759: The rest of this chapter has been devoted to problems of logic within test code, the notion of "things
Line 760: that are too simple to break", and to the problem of test maintenance.
Line 761: 225
Line 762: 
Line 763: --- 페이지 241 ---
Line 764: Chapter 11. Maintainable Tests
Line 765: 11.7. Exercises
Line 766: 11.7.1. A Car is a Sports Car if …
Line 767: After three months of analysis a team of business analysts have decided that a car can be marked with
Line 768: the "sports" tag if it satisfies all of the following requirements:
Line 769: • it is red,
Line 770: • it was manufactured by Ferrari,
Line 771: • its engine has more than 6 cylinders.
Line 772: Based on these detailed requirements a team of top-notch developers have come up with the following
Line 773: implementation of the CarSearch class:
Line 774: Listing 11.14. CarSearch class implementation
Line 775: public class CarSearch {
Line 776:     private List<Car> cars = new ArrayList<Car>();
Line 777:     public void addCar(Car car) {
Line 778:         cars.add(car);
Line 779:     }
Line 780:     public List<Car> findSportCars() {
Line 781:         List<Car> sportCars = new ArrayList<Car>();
Line 782:         for (Car car : cars) {
Line 783:             if (car.getEngine().getNbOfCylinders() > 6
Line 784:                     && Color.RED == car.getColor()
Line 785:                     && "Ferrari".equals(car.getManufacturer().getName())) {
Line 786:                 sportCars.add(car);
Line 787:             }
Line 788:         }
Line 789:         return sportCars;
Line 790:     }
Line 791: }
Line 792: The Car, Engine and Manufacturer interfaces are presented below:
Line 793: Listing 11.15. Car interface
Line 794: public interface Car {
Line 795:     Engine getEngine();
Line 796:     Color getColor();
Line 797:     Manufacturer getManufacturer();
Line 798: }
Line 799: Listing 11.16. Engine interface
Line 800: public interface Engine {
Line 801:     int getNbOfCylinders();
Line 802: }
Line 803: 226
Line 804: 
Line 805: --- 페이지 242 ---
Line 806: Chapter 11. Maintainable Tests
Line 807: Listing 11.17. Manufacturer interface
Line 808: public interface Manufacturer {
Line 809:     String getName();
Line 810: }
Line 811: Your task is to write some tests for the findSportCars() method of the CarSearch class. Basically,
Line 812: what you have to do is pass some cars to the CarSearch class (using its addCar()) method, and then
Line 813: verify, whether only sports cars are being returned by the findSportsCars() method.
Line 814: Initially, do this for the original implementation of the CarSearch class. Then, redesign the Car
Line 815: interface, so that the CarSearch class does not violate either the "Law of Demeter" or the "Tell, Don’t
Line 816: Ask!" principles, and write the tests once again. Compare the amount of work involved in each case.
Line 817: 11.7.2. Stack Test
Line 818: Based on what was discussed in Section 11.1, implement a Stack10 class and a corresponding
Line 819: StackTest class. Please follow the TDD approach, so that the tests are written before the
Line 820: implementation. Make sure you think in terms of class responsibilities!
Line 821: 10See http://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29.
Line 822: 227