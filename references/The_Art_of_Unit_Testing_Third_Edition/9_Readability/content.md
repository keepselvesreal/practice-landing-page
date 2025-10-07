Line 1: 
Line 2: --- 페이지 215 ---
Line 3: 187
Line 4: Readability
Line 5: Without readability, the tests you write are almost meaningless to whoever reads
Line 6: them later on. Readability is the connecting thread between the person who wrote
Line 7: the test and the poor soul who must read it a few months or years later. Tests are
Line 8: stories you tell the next generation of programmers on a project. They allow a
Line 9: developer to see exactly what an application is made of and where it started.
Line 10:  This chapter is all about making sure the developers who come after you will be
Line 11: able to maintain the production code and the tests that you write. They’ll need to
Line 12: understand what they’re doing and where they should be doing it.
Line 13:  There are several facets to readability:
Line 14: Naming unit tests
Line 15: Naming variables
Line 16: Separating asserts from actions
Line 17: Setting up and tearing down
Line 18: Let’s go through these one by one.
Line 19: This chapter covers
Line 20: Naming conventions for unit tests
Line 21: Writing readable tests
Line 22: 
Line 23: --- 페이지 216 ---
Line 24: 188
Line 25: CHAPTER 9
Line 26: Readability
Line 27: 9.1
Line 28: Naming unit tests
Line 29: Naming standards are important because they give you comfortable rules and tem-
Line 30: plates that outline what you should explain about the test. No matter how I order
Line 31: them, or what specific framework or language I am using, I try to make sure these
Line 32: three important pieces of information are present in the name of the test or in the
Line 33: structure of the file in which the test exists:
Line 34: The entry point to the unit of work (or the name of the feature being tested)
Line 35: The scenario under which you’re testing the entry point
Line 36: The expected behavior of the exit point of the unit of work
Line 37: The name of the entry point (or unit of work) is essential, so that you can easily
Line 38: understand the starting scope of the logic being tested. Having this as the first part of
Line 39: the test name also allows for easy navigation and as-you-type completion (if your IDE
Line 40: supports it) in the test file.
Line 41:  The scenario under which it’s being tested gives you the “with” part of the name:
Line 42: “When I call entry point X with a null value, then it should do Y.”
Line 43:  The expected behavior from the exit point of the unit of work is where the test
Line 44: specifies in plain English what the unit of work should do or return, or how it should
Line 45: behave, based on the current scenario: “When I call entry point X with a null value,
Line 46: then it should do Y as visible from this exit point of the unit of work.”
Line 47:  These three elements have to exist somewhere close to the eyes of the person read-
Line 48: ing the test. Sometimes they can all be encapsulated in the test’s function name, and
Line 49: sometimes you can include them with nested describe structures. Sometimes you can
Line 50: simply use a string description as a parameter or annotation for the test.
Line 51:  Some examples are shown in the following listing, all with the same pieces of infor-
Line 52: mation, but laid out differently. 
Line 53: test('verifyPassword, with a failing rule, returns error based on 
Line 54: rule.reason', () => { … }
Line 55: describe('verifyPassword', () => {
Line 56:   describe('with a failing rule', () => {
Line 57:     it('returns error based on the rule.reason', () => { ... }
Line 58: verifyPassword_withFailingRule_returnsErrorBasedonRuleReason()
Line 59: You can, of course, come up with other ways to structure this. (Who says you have to
Line 60: use underscores? That’s just my own preference for reminding me and others that
Line 61: there are three pieces of information.). The key point to take away is that if you
Line 62: remove one of these pieces of information, you’re forcing the person reading the test
Line 63: to read the code inside the test to find out the answer, wasting precious time. 
Line 64:  The following listing shows examples of tests with missing information.
Line 65: Listing 9.1
Line 66: Same information, different variations
Line 67: 
Line 68: --- 페이지 217 ---
Line 69: 189
Line 70: 9.2
Line 71: Magic values and naming variables
Line 72: test(failing rule, returns error based on rule.reason', () => { ... }  
Line 73: test('verifyPassword, returns error based on rule.reason', () => { ... }   
Line 74: test('verifyPassword, with a failing rule', () => { ... }   
Line 75: Your main goal with readability is to release the next developer from the burden of
Line 76: reading the test code in order to understand what the test is testing.
Line 77:  Another great reason to include all these pieces of information in the name of the
Line 78: test is that the name is usually the only thing that shows up when an automated build
Line 79: pipeline fails. You’ll see the names of the failed tests in the log of the build that failed,
Line 80: but you won’t see any comments or the code of the tests. If the names are good
Line 81: enough, you might not need to read the code of the tests or debug them; you may
Line 82: understand the cause of the failure simply by reading the log of the failed build. This
Line 83: can save precious debugging and reading time.
Line 84:  A good test name also serves to contribute to the idea of executable documenta-
Line 85: tion—if you can ask a developer who is new to the team to read the tests so they can
Line 86: understand how a specific component or application works, that’s a good sign of read-
Line 87: ability. If they can’t make sense of the application or the component’s behavior from
Line 88: the tests alone, it might be a red flag for readability. 
Line 89: 9.2
Line 90: Magic values and naming variables
Line 91: Have you heard the term “magic values”? It sounds awesome, but it’s the opposite of
Line 92: that. It should really be “witchcraft values” to convey the negative effects of using
Line 93: them. What are they, you ask? They are hardcoded, undocumented, or poorly under-
Line 94: stood constants or variables. The reference to magic indicates that these values work,
Line 95: but you have no idea why.
Line 96:  Consider the following test.
Line 97: describe('password verifier', () => {
Line 98:   test('on weekends, throws exceptions', () => {
Line 99:     expect(() => verifyPassword('jhGGu78!', [], 0))   
Line 100:       .toThrowError("It's the weekend!");
Line 101:   });
Line 102: });
Line 103: This test contains three magic values. Can a person who didn’t write the test and
Line 104: doesn't know the API being tested easily understand what the 0 value means? How
Line 105: about the [] array? The first parameter to that function kind of looks like a password,
Line 106: but even that has a magical quality to it. Let’s discuss:
Line 107: Listing 9.2
Line 108: Test names with missing information
Line 109: Listing 9.3
Line 110: A test with magic values
Line 111: What is the thing under test?
Line 112: When is this supposed to happen?
Line 113: What’s supposed 
Line 114: to happen then?
Line 115: Magic 
Line 116: values
Line 117: 
Line 118: --- 페이지 218 ---
Line 119: 190
Line 120: CHAPTER 9
Line 121: Readability
Line 122: The 0 could mean so many things. As the reader, I might have to search around
Line 123: in the code, or jump into the signature of the called function, to understand
Line 124: that this specifies the day of the week. 
Line 125: The [] forces me to look at the signature of the called function to understand
Line 126: that the function expects a password verification rule array, which means the
Line 127: test verifies the case with no rules.
Line 128: 
Line 129: jhGGu78! seems to be an obvious password value, but the big question I’ll have
Line 130: as a reader is, why this specific value? What’s important about this specific pass-
Line 131: word? It’s obviously important to use this value and not any other for this test,
Line 132: because it seems so damned specific. In reality it isn’t, but the reader won’t
Line 133: know this. They’ll likely end up using this password in other tests just to be safe.
Line 134: Magic values tend to propagate themselves in tests.
Line 135: The following listing shows the same test with the magic values fixed.
Line 136: describe("verifier2 - dummy object", () => {
Line 137:   test("on weekends, throws exceptions", () => {
Line 138:     const SUNDAY = 0, NO_RULES = [];
Line 139:     expect(() => verifyPassword2("anything", NO_RULES, SUNDAY))
Line 140:       .toThrowError("It's the weekend!");
Line 141:   });
Line 142: });
Line 143: By putting magic values into meaningfully named variables, we can remove the ques-
Line 144: tions people will have when reading our test. For the password value, I’ve decided to
Line 145: simply change the direct value to explain to the reader what is not important about
Line 146: this test.
Line 147:  Variable names and values are just as much about explaining to the reader what
Line 148: they should not care about as they are about explaining what is important.
Line 149: 9.3
Line 150: Separating asserts from actions
Line 151: For the sake of readability and all that is holy, avoid writing assertions and the method
Line 152: call in the same statement. The following listing shows what I mean.
Line 153: expect(verifier.verify("any value")[0]).toContain("fake reason");   
Line 154: const result = verifier.verify("any value");  
Line 155: expect(result[0]).toContain("fake reason");   
Line 156: See the difference between the two examples? The first example is much harder to
Line 157: read and understand in the context of a real test because of the length of the line and
Line 158: the nesting of the act and assert parts. 
Line 159: Listing 9.4
Line 160: Fixing magic values
Line 161: Listing 9.5
Line 162: Separating asserts from actions
Line 163: Bad example
Line 164: Good 
Line 165: example
Line 166: 
Line 167: --- 페이지 219 ---
Line 168: 191
Line 169: 9.4
Line 170: Setting up and tearing down
Line 171:  It’s also much easier to debug the second example than the first one, if you wanted
Line 172: to focus on the result value after the call. Don’t skimp on this small tip. The people
Line 173: after you will whisper a small thank you when your test doesn’t make them feel stupid
Line 174: for not understanding it.
Line 175: 9.4
Line 176: Setting up and tearing down
Line 177: Setup and teardown methods in unit tests can be abused to the point where the tests
Line 178: or the setup and teardown methods are unreadable. The situation is usually worse in
Line 179: the setup method than in the teardown method.
Line 180:  The following listing shows one possible abuse that is very common: using the
Line 181: setup (or beforeEach function) for setting up mocks or stubs.
Line 182: describe("password verifier", () => {
Line 183:   let mockLog;
Line 184:   beforeEach(() => {
Line 185:     mockLog = Substitute.for<IComplicatedLogger>();  
Line 186:   });
Line 187:   test("verify, with logger & passing, calls logger with PASS",() => {
Line 188:     const verifier = new PasswordVerifier2([], mockLog);  
Line 189:     verifier.verify("anything");
Line 190:     mockLog.received().info(                              
Line 191:       Arg.is((x) => x.includes("PASSED")),
Line 192:       "verify"
Line 193:     );
Line 194:   });
Line 195: }); 
Line 196: If you set up mocks and stubs in a setup method, that means they don’t get set up in
Line 197: the actual test. That, in turn, means that whoever is reading your test may not even
Line 198: realize that there are mock objects in use, or what the test expects from them.
Line 199:  The test in listing 9.6 uses the mockLog variable, which is initialized in the
Line 200: beforeEach function (a setup method). Imagine you have dozens or more of these
Line 201: tests in the file. The setup function is at the beginning of the file, and you are stuck
Line 202: reading a test way down in the file. You come across the mockLog variable and you
Line 203: have to start asking questions such as, “Where is this initialized? How will it behave
Line 204: in the test?” and more. 
Line 205:  Another problem that can arise if multiple mocks and stubs are used in various
Line 206: tests in the same file is that the setup function becomes a dumping group for all the
Line 207: various states used by your tests. It becomes a big mess, a soup of many parameters,
Line 208: some used by one test and others used somewhere else. It becomes difficult to manage
Line 209: and understand such a setup. 
Line 210:  It’s much more readable to initialize mock objects directly in the test, with all their
Line 211: expectations. The following listing is an example of initializing the mock in each test. 
Line 212: Listing 9.6
Line 213: Using a setup (beforeEach) function for mock setup
Line 214: Setting up 
Line 215: a mock
Line 216: Using the
Line 217: mock
Line 218: 
Line 219: --- 페이지 220 ---
Line 220: 192
Line 221: CHAPTER 9
Line 222: Readability
Line 223: describe("password verifier", () => {
Line 224:   test("verify, with logger & passing,calls logger with PASS",() => {
Line 225:     const mockLog = Substitute.for<IComplicatedLogger>();   
Line 226:     const verifier = new PasswordVerifier2([], mockLog);
Line 227:     verifier.verify("anything");
Line 228:     mockLog.received().info(
Line 229:       Arg.is((x) => x.includes("PASSED")),
Line 230:       "verify"
Line 231:     );
Line 232:   });
Line 233: When I look at this test, everything is clear as day. I can see when the mock is created,
Line 234: its behavior, and anything else I need to know. 
Line 235:  If you’re worried about maintainability, you can refactor the creation of the mock
Line 236: into a helper function that each test would call. That way, you’re avoiding the generic
Line 237: setup function and are instead calling the same helper function from multiple tests.
Line 238: As the following listing shows, you keep the readability and gain more maintainability.
Line 239: describe("password verifier", () => {
Line 240:   test("verify, with logger & passing,calls logger with PASS",() => {
Line 241:     const mockLog = makeMockLogger();        
Line 242:     const verifier = new PasswordVerifier2([], mockLog);
Line 243:     verifier.verify("anything");
Line 244:     mockLog.received().info(
Line 245:       Arg.is((x) => x.includes("PASSED")),
Line 246:       "verify"
Line 247:     );
Line 248:   });
Line 249: And yes, if you follow this logic, you can see that I’m perfectly OK with you not having
Line 250: any setup functions in your tests. I’ve often written full test suites that don’t have a
Line 251: setup function, instead calling helper methods from each test, for the sake of main-
Line 252: tainability. The tests were still readable and maintainable.
Line 253: Summary
Line 254: When naming a test, include the name of the unit of work under test, the cur-
Line 255: rent test scenario, and the expected behavior of the unit of work.
Line 256: Don’t leave magic values in your tests. Either wrap them in variables with mean-
Line 257: ingful names, or put the description into the value itself, if it’s a string.
Line 258: Listing 9.7
Line 259: Avoiding a setup function
Line 260: Listing 9.8
Line 261: Using a helper function
Line 262: Initializing 
Line 263: the mock 
Line 264: in the test 
Line 265: Using a helper 
Line 266: function to 
Line 267: initialize the 
Line 268: mock
Line 269: 
Line 270: --- 페이지 221 ---
Line 271: 193
Line 272: Summary
Line 273: Separate assertions from actions. Merging the two shortens the code but makes
Line 274: it significantly harder to understand.
Line 275: Try not to use test setups at all (such as beforeEach methods). Introduce helper
Line 276: methods to simplify the test’s arrange part, and use those helper methods in
Line 277: each test.
