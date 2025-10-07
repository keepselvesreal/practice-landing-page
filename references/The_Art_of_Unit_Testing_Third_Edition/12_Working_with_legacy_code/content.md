Line 1: 
Line 2: --- 페이지 259 ---
Line 3: 231
Line 4: Working with legacy code
Line 5: I once consulted for a large development shop that produced billing software.
Line 6: They had over 10,000 developers and mixed .NET, Java, and C++ in products, sub-
Line 7: products, and intertwined projects. The software had existed in one form or
Line 8: another for over five years, and most of the developers were tasked with maintain-
Line 9: ing and building on top of existing functionality. 
Line 10:  My job was to help several divisions (using all languages) learn TDD techniques.
Line 11: For about 90% of the developers I worked with, this never became a reality for sev-
Line 12: eral reasons, some of which were a result of legacy code:
Line 13: It was difficult to write tests against existing code.
Line 14: It was next to impossible to refactor the existing code (or there wasn’t
Line 15: enough time to do it).
Line 16: Some people didn’t want to change their designs.
Line 17: Tooling (or a lack of tooling) was getting in the way.
Line 18: It was difficult to determine where to begin.
Line 19: This chapter covers
Line 20: Examining common problems with legacy code
Line 21: Deciding where to begin writing tests
Line 22: 
Line 23: --- 페이지 260 ---
Line 24: 232
Line 25: CHAPTER 12
Line 26: Working with legacy code
Line 27: Anyone who’s ever tried to add tests to an existing system knows that most such sys-
Line 28: tems are almost impossible to write tests for. They were usually written without proper
Line 29: places (called seams) in the software to allow extensions or replacements to existing
Line 30: components.
Line 31:  There are two problems that need to be addressed when dealing with legacy code:
Line 32: There’s so much work, where should you start to add tests? Where should you
Line 33: focus your efforts?
Line 34: How can you safely refactor your code if it has no tests to begin with?
Line 35: This chapter will tackle these tough questions associated with approaching legacy
Line 36: codebases by listing techniques, references, and tools that can help.
Line 37: 12.1
Line 38: Where do you start adding tests?
Line 39: Assuming you have existing code inside components, you’ll need to create a priority
Line 40: list of components for which testing makes the most sense. There are several factors to
Line 41: consider that can affect each component’s priority:
Line 42: Logical complexity —This refers to the amount of logic in the component, such as
Line 43: nested ifs, switch cases, or recursion. Such complexity is also called cyclomatic
Line 44: complexity, and you can use various tools to check it automatically.
Line 45: Dependency level—This refers to the number of dependencies in the component.
Line 46: How many dependencies do you have to break in order to bring this class under
Line 47: test? Does it communicate with an outside email component, perhaps, or does
Line 48: it call a static log method somewhere?
Line 49: Priority—This is the component’s general priority in the project.
Line 50: You can give each component a rating for these factors, from 1 (low priority) to 10
Line 51: (high priority). Table 12.1 shows classes with ratings for these factors. I call this a test-
Line 52: feasibility table.
Line 53: Table 12.1
Line 54: A simple test-feasibility table
Line 55: Component
Line 56: Logical 
Line 57: complexity
Line 58: Dependency 
Line 59: level
Line 60: Priority
Line 61: Notes
Line 62: Utils
Line 63: 6
Line 64: 1
Line 65: 5
Line 66: This utility class has few dependencies 
Line 67: but contains a lot of logic. It will be easy 
Line 68: to test, and it provides lots of value.
Line 69: Person
Line 70: 2
Line 71: 1
Line 72: 1
Line 73: This is a data-holder class with little 
Line 74: logic and no dependencies. There’s 
Line 75: little real value in testing this.
Line 76: TextParser
Line 77: 8
Line 78: 4
Line 79: 6
Line 80: This class has lots of logic and lots of 
Line 81: dependencies. To top it off, it’s part of 
Line 82: a high-priority task in the project. Test-
Line 83: ing this will provide lots of value but 
Line 84: will also be hard and time consuming.
Line 85: 
Line 86: --- 페이지 261 ---
Line 87: 233
Line 88: 12.1
Line 89: Where do you start adding tests?
Line 90: From the data in table 12.1, you can create a diagram like the one shown in figure 12.1,
Line 91: which graphs your components by the amount of value to the project and number of
Line 92: dependencies. You can safely ignore items that are below your designated threshold of
Line 93: logic (which I usually set at 2 or 3), so Person and ConfigManager can be ignored.
Line 94: You’re left with only the top two components in figure 12.1.
Line 95:  There are two basic ways to look at the graph and decide what you’d like to test
Line 96: first (see figure 12.2):
Line 97: Choose the one that’s more complex and easier to test (top left).
Line 98: Choose the one that’s more complex and harder to test (top right).
Line 99: The question now is what path you should take. Should you start with the easy stuff or
Line 100: the hard stuff?
Line 101: ConfigManager
Line 102: 1
Line 103: 6
Line 104: 1
Line 105: This class holds configuration data 
Line 106: and reads files from disk. It has little 
Line 107: logic but many dependencies. Testing 
Line 108: it will provide little value to the proj-
Line 109: ect and will also be hard and time 
Line 110: consuming.
Line 111: Table 12.1
Line 112: A simple test-feasibility table (continued)
Line 113: Component
Line 114: Logical 
Line 115: complexity
Line 116: Dependency 
Line 117: level
Line 118: Priority
Line 119: Notes
Line 120: Utils
Line 121: Person
Line 122: TextParser
Line 123: ConfigManager
Line 124: Logic
Line 125: Dependencies
Line 126: Figure 12.1
Line 127: Mapping components for test 
Line 128: feasibility
Line 129: Logic-driven
Line 130: (easy to test)
Line 131: Dependency-
Line 132: driven
Line 133: (hard to test)
Line 134: Ignore
Line 135: Logic
Line 136: Dependencies
Line 137: Figure 12.2
Line 138: Easy, hard, and irrelevant 
Line 139: component mapping based on logic and 
Line 140: dependencies
Line 141: 
Line 142: --- 페이지 262 ---
Line 143: 234
Line 144: CHAPTER 12
Line 145: Working with legacy code
Line 146: 12.2
Line 147: Choosing a selection strategy
Line 148: As the previous section explained, you can start with the components that are easy to
Line 149: test or the ones that are hard to test (because they have many dependencies). Each
Line 150: strategy presents different challenges. 
Line 151: 12.2.1 Pros and cons of the easy-first strategy
Line 152: Starting out with the components that have fewer dependencies will make writing the
Line 153: tests initially much quicker and easier. But there’s a catch, as figure 12.3 demonstrates.
Line 154: Figure 12.3 shows how long it takes to bring components under test during the life-
Line 155: time of the project. Initially it’s easy to write tests, but as time goes by, you’re left with
Line 156: components that are increasingly harder and harder to test, with the particularly
Line 157: tough ones waiting for you at the end of the project cycle, just when everyone is
Line 158: stressed about pushing a product out the door.
Line 159:  If your team is relatively new to unit testing techniques, it’s worth starting with the
Line 160: easy components. As time goes by, the team will learn the techniques needed to deal
Line 161: with the more complex components and dependencies. For such a team, it may be
Line 162: wise to initially avoid all components over a specific number of dependencies (with
Line 163: four being a reasonable limit).
Line 164: 12.2.2 Pros and cons of the hard-first strategy
Line 165: Starting with the more difficult components may seem like a losing proposition ini-
Line 166: tially, but it has an upside as long as your team has experience with unit testing tech-
Line 167: niques. Figure 12.4 shows the average time to write a test for a single component over
Line 168: the lifetime of the project, if you start testing the components with the most depen-
Line 169: dencies first.
Line 170:  With this strategy, you could be spending a day or more to get even the simplest
Line 171: tests going on the more complex components. But notice the quick decline in the
Line 172: time required to write the tests relative to the slow incline in figure 12.3. Every time
Line 173: you bring a component under test and refactor it to make it more testable, you may
Line 174: Time to
Line 175: write
Line 176: test
Line 177: Project lifetime
Line 178: Figure 12.3
Line 179: When starting with the easy 
Line 180: components, the time required to test 
Line 181: components increases more and more until 
Line 182: the hardest components are done.
Line 183: 
Line 184: --- 페이지 263 ---
Line 185: 235
Line 186: 12.3
Line 187: Writing integration tests before refactoring
Line 188: also be solving testability issues for the dependencies it uses or for other components.
Line 189: Because that component has lots of dependencies, refactoring it can improve things
Line 190: for other parts of the system. That’s the reason for the quick decline. 
Line 191:  The hard-first strategy is only possible if your team has experience in unit testing
Line 192: techniques, because it’s harder to implement. If your team does have experience, use
Line 193: the priority aspect of components to choose whether to start with the hard or easy
Line 194: components. You might want to choose a mix, but it’s important that you know in
Line 195: advance how much effort will be involved and what the possible consequences are.
Line 196: 12.3
Line 197: Writing integration tests before refactoring
Line 198: If you do plan to refactor your code for testability (so you can write unit tests), a prac-
Line 199: tical way to make sure you don’t break anything during the refactoring phase is to
Line 200: write integration-style tests against your production system. 
Line 201:  I consulted on a large legacy project, working with a developer who needed to
Line 202: work on an XML configuration manager. The project had no tests and was hardly test-
Line 203: able. It was also a C++ project, so we couldn’t use a tool to easily isolate components
Line 204: from dependencies without refactoring the code.
Line 205:  The developer needed to add another value attribute into the XML file and be
Line 206: able to read and change it through the existing configuration component. We ended
Line 207: up writing a couple of integration tests that used the real system to save and load con-
Line 208: figuration data and that asserted on the values the configuration component was
Line 209: retrieving and writing to the file. Those tests set the “original” working behavior of the
Line 210: configuration manager as our base of work. 
Line 211:  Next, we wrote an integration test that showed that once the component was reading
Line 212: the file, it contained no attribute in memory with the name we were trying to add. We
Line 213: proved that the feature was missing, and we now had a test that would pass once we
Line 214: added the new attribute to the XML file and correctly wrote to it from the component.
Line 215:  Once we wrote the code that saved and loaded the extra attribute, we ran the three
Line 216: integration tests (two tests for the original base implementation and a new one that
Line 217: tried to read the new attribute). All three passed, so we knew that we hadn’t broken
Line 218: existing functionality while adding the new functionality. 
Line 219: Time to
Line 220: write
Line 221: test
Line 222: Project lifetime
Line 223: Figure 12.4
Line 224: When you use a hard-first 
Line 225: strategy, the time required to test 
Line 226: components is initially high, but then 
Line 227: decreases as more dependencies are 
Line 228: refactored away.
Line 229: 
Line 230: --- 페이지 264 ---
Line 231: 236
Line 232: CHAPTER 12
Line 233: Working with legacy code
Line 234:  As you can see, the process is relatively simple:
Line 235: Add one or more integration tests (no mocks or stubs) to the system to prove
Line 236: the original system works as needed.
Line 237: Refactor or add a failing test for the feature you’re trying to add to the system.
Line 238: Refactor and change the system in small chunks, and run the integration tests
Line 239: as often as you can, to see if you break something.
Line 240: Sometimes, integration tests may seem easier to write than unit tests, because you
Line 241: don’t need to understand the internal structure of the code or where to inject various
Line 242: dependencies. But making those tests run on your local system may prove annoying or
Line 243: time consuming because you have to make sure every little thing the system needs is
Line 244: in place.
Line 245:  The trick is to work on the parts of the system that you need to fix or add features
Line 246: to. Don’t focus on the other parts. That way, the system grows in the right places, leav-
Line 247: ing other bridges to be crossed when you get to them.
Line 248:  As you continue adding more and more tests, you can refactor the system and add
Line 249: more unit tests to it, growing it into a more maintainable and testable system. This
Line 250: takes time (sometimes months and months), but it’s worth it.
Line 251:  Chapter 7 of Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov
Line 252: (Manning, 2020) contains an in-depth example of such refactoring. Refer to that
Line 253: book for more details.
Line 254: 12.3.1 Read Michael Feathers’ book on legacy code
Line 255: Working Effectively with Legacy Code by Michael Feathers (Pearson, 2004) is another valu-
Line 256: able source that deals with the issues you’ll encounter with legacy code. It shows many
Line 257: refactoring techniques and gotchas in depth that this book doesn’t attempt to cover.
Line 258: It’s worth its weight in gold. Get it. 
Line 259: 12.3.2 Use CodeScene to investigate your production code
Line 260: Another tool called CodeScene allows you to discover lots of technical debt and hid-
Line 261: den issues in legacy code, among many other things. It is a commercial tool, and while
Line 262: I have not personally used it, I've heard great things. You can learn more about it at
Line 263: https://codescene.com/. 
Line 264: Summary
Line 265: Before starting to write tests for legacy code, it’s important to map out the vari-
Line 266: ous components according to their number of dependencies, their amount of
Line 267: logic, and each component’s general priority in the project. A component’s log-
Line 268: ical complexity (or cyclomatic complexity) refers to the amount of logic in the
Line 269: component, such as nested ifs, switch cases, or recursion. 
Line 270: Once you have that information, you can choose the components to work on
Line 271: based on how easy or how hard it will be to get them under test.
Line 272: 
Line 273: --- 페이지 265 ---
Line 274: 237
Line 275: Summary
Line 276: If your team has little or no experience in unit testing, it’s a good idea to start
Line 277: with the easy components and let the team’s confidence grow as they add more
Line 278: and more tests to the system.
Line 279: If your team is experienced, getting the hard components under test first can
Line 280: help you get through the rest of the system more quickly.
Line 281: Before a large-scale refactoring, write integration tests that will sustain that
Line 282: refactoring mostly unchanged. After the refactoring is completed, replace most
Line 283: of these integration tests with smaller and more maintainable unit tests.
