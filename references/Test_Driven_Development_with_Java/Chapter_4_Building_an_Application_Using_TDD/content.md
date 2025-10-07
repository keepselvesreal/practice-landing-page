Line 1: 
Line 2: --- 페이지 68 ---
Line 3: 4
Line 4: Building an Application 
Line 5: Using TDD
Line 6: We’re going to learn the practical side of TDD by building the application test first. We are also going 
Line 7: to use an approach known as agile software development as we build. Being agile means building 
Line 8: our software in small, self-contained iterations instead of building it all at once. These small steps 
Line 9: allow us to learn more about the software design as we go. We adapt and refine the design over time, 
Line 10: as we become more certain of how a good design might look. We can offer working functionality to 
Line 11: early test users and receive their feedback long before the application is complete. This is valuable. 
Line 12: As we have seen in earlier chapters, TDD is an excellent approach for providing rapid feedback on 
Line 13: self-contained pieces of software. It is the perfect complement to agile development.
Line 14: To help us build in this way, this chapter will introduce the technique of user stories, which is a way 
Line 15: of capturing requirements that fits an agile approach well. We will prepare our Java development 
Line 16: environment ready for test-first development before describing what our application will do.  
Line 17: In this chapter, we’re going to cover the following topics:
Line 18: •	 Introducing the Wordz application
Line 19: •	 Exploring agile methods
Line 20: Technical requirements
Line 21: The final code for this chapter can be found at https://github.com/PacktPublishing/
Line 22: Test-Driven-Development-with-Java/tree/main/chapter04.
Line 23: To code along – which I highly recommend – we need to set up our development environment first. 
Line 24: This will use the excellent JetBrains IntelliJ Java Integrated Development Environment (IDE), a free-
Line 25: of-charge Java SDK from Amazon, and some libraries to help us with writing our tests and including 
Line 26: the libraries in our Java project. We will assemble all our development tools in the next section.
Line 27: 
Line 28: --- 페이지 69 ---
Line 29: Building an Application Using TDD
Line 30: 46
Line 31: Preparing our development environment
Line 32: For this project, we will be using the following tools:
Line 33: •	 IntelliJ IDEA IDE 2022.1.3 (Community Edition) or higher
Line 34: •	 Amazon Corretto Java 17 JDK
Line 35: •	 The JUnit 5 unit test framework
Line 36: •	 The AssertJ fluent assertions framework
Line 37: •	 The Gradle dependency management system
Line 38: We will begin by installing our Java IDE, the JetBrains IntelliJ IDE Community Edition, before adding 
Line 39: the rest of the tools. 
Line 40: Installing the IntelliJ IDE
Line 41: To help us work with Java source code, we will use the JetBrains IntelliJ Java IDE, using its free-of-charge 
Line 42: Community Edition. This is a popular IDE used in the software industry – and for good reason. It 
Line 43: combines an excellent Java editor with auto-completion and code suggestions, together with a debugger, 
Line 44: automated refactoring support, Git source control tools, and excellent integration for running tests. 
Line 45: To install IntelliJ, see the following steps:
Line 46: 1.	
Line 47: Go to https://www.jetbrains.com/idea/download/.
Line 48: 2.	
Line 49: Click on the tab for your operating system.
Line 50: 3.	
Line 51: Scroll down to the Community section.
Line 52: 4.	
Line 53: Follow the installation instructions for your operating system.
Line 54: Once complete, the IntelliJ IDE should be installed on your computer. The next step is to create an 
Line 55: empty Java project, using the Gradle package management system, and then set up whichever version 
Line 56: of Java we wish to use. The installations for Mac, Windows, and Linux are usually straightforward.
Line 57: Setting up the Java project and libraries
Line 58: Once IntelliJ is installed, we can import the starter project provided in the accompanying GitHub 
Line 59: repository. This will set up a Java project that uses the Amazon Corretto 17 Java Development Kit 
Line 60: (JDK), the JUnit 5 unit test runner, the Gradle build management system, and the AssertJ fluent 
Line 61: assertions library.
Line 62: 
Line 63: --- 페이지 70 ---
Line 64: Technical requirements
Line 65: 47
Line 66: To do this, see the following steps:
Line 67: 1.	
Line 68: In your web browser, go to https://github.com/PacktPublishing/Test-
Line 69: Driven-Development-with-Java.
Line 70: 2.	
Line 71: Use your preferred git tool to clone the whole repository on your computer. If you use the 
Line 72: git command-line tool, this will be as follows:
Line 73: git clone https://github.com/PacktPublishing/Test-Driven-
Line 74: Development-with-Java.git
Line 75: 3.	
Line 76: Launch IntelliJ. You should see the welcome screen:
Line 77: Figure 4.1 – IntelliJ welcome screen
Line 78: 4.	
Line 79: Click Open and then navigate to the chapter04 folder of the repository that we just cloned. 
Line 80: Click to highlight it: 
Line 81: Figure 4.2 – Select the code folder
Line 82: 5.	
Line 83: Click the Open button.
Line 84: 
Line 85: --- 페이지 71 ---
Line 86: Building an Application Using TDD
Line 87: 48
Line 88: 6.	
Line 89: Wait for IntelliJ to import the files. You should see this workspace open:
Line 90: Figure 4.3 – IntelliJ workspace view
Line 91: We now have the IDE set up with a skeleton project containing everything we need to make a start. 
Line 92: In the next section, we will describe the main features of the application we are going to build, which 
Line 93: we will start to do in the next chapter.
Line 94: Introducing the Wordz application
Line 95: In this section, we will describe the application that we are going to build at a high level, before going 
Line 96: on to look at the agile process we will use to build it. The application is called Wordz and it is based 
Line 97: on a popular word guessing game. Players try to guess a five-letter word. Points are scored based on 
Line 98: how quickly a player guesses the word. The player gets feedback on each guess to steer them towards 
Line 99: the right answer. We are going to build the server-side components of this application throughout 
Line 100: the remainder of this book using various TDD techniques.
Line 101: 
Line 102: --- 페이지 72 ---
Line 103: Introducing the Wordz application
Line 104: 49
Line 105: Describing the rules of Wordz
Line 106: To play Wordz, a player will have up to six attempts to guess a five-letter word. After each attempt, 
Line 107: letters in the word are highlighted as follows:
Line 108: •	 The correct letter in the correct position has a black background
Line 109: •	 The correct letter in the wrong position has a gray background
Line 110: •	 Incorrect letters not present in the word have a white background 
Line 111: The player can use this feedback to make a better next guess. Once a player guesses the word correctly, 
Line 112: they score some points. They get six points for a correct guess on the first attempt, five points for a 
Line 113: correct guess on the second attempt, and one point for a correct guess on the sixth and final attempt. 
Line 114: Players compete against each other in various rounds to gain the highest score. Wordz is a fun game 
Line 115: as well as a gentle brain workout.
Line 116: Whilst building a user interface is outside the scope of this book, it is very helpful to see a possible 
Line 117: example:
Line 118: Figure 4.4 – The Wordz game
Line 119: Technically, we are going to create the backend web service component for this game. It will expose 
Line 120: an Application Programming Interface (API) so that a user interface can use the service and will 
Line 121: keep track of the game state in a database.  
Line 122: To focus on the techniques of TDD, we will leave certain things out of our scope, such as user 
Line 123: authentication and the user interface. A production version would, of course, include these aspects. 
Line 124: But to implement these features, we don’t need any new TDD techniques. 
Line 125: This simple design will allow us to fully explore TDD through all the layers of a typical web application.
Line 126: Now that we’ve defined what we’re going to build, the next section will introduce the development 
Line 127: approach we will use to build it.
Line 128: 
Line 129: --- 페이지 73 ---
Line 130: Building an Application Using TDD
Line 131: 50
Line 132: Exploring agile methods
Line 133: As we build Wordz, we are going to use an iterative approach, where we build the application as a 
Line 134: series of features that our users can work with. This is known as agile development. It is effective as 
Line 135: it allows us to ship features to users earlier and on a regular schedule. It allows us as developers to 
Line 136: learn more about the problems we are solving and how a good software design looks as we go. This 
Line 137: section will compare the benefits of agile development to waterfall approaches, then introduce an 
Line 138: agile requirements gathering tool called user stories.
Line 139: The predecessor to agile is called waterfall development. It is called this because the project stages 
Line 140: flow as a waterfall does, each one is fully completed before the next one is begun.
Line 141: In a waterfall project, we split development into sequential stages:
Line 142: 1.	
Line 143: Collecting requirements
Line 144: 2.	
Line 145: Performing an analysis of requirements
Line 146: 3.	
Line 147: Creating a complete software design 
Line 148: 4.	
Line 149: Writing all the code 
Line 150: 5.	
Line 151: Testing the code 
Line 152: In theory, every stage is perfectly executed, everything works, and there are no problems. In reality, 
Line 153: there are always problems. 
Line 154: We discover certain requirements we had missed. We find that the design documents cannot be 
Line 155: coded exactly as they were written. We find missing parts of the design. The coding itself can run into 
Line 156: difficulties. The worst part is that the end user never sees any working software until the very end. If 
Line 157: what they see is not what they had in mind, we have a very expensive set of changes and reworking to do. 
Line 158: The reason for this is that humans have limited foresight. Try as we might, we cannot predict the future 
Line 159: with any accuracy. I can sit here with a hot cup of coffee and know accurately that it will go cold in 
Line 160: twenty minutes. But I can’t tell you what the weather will be three months from now. Our ability to 
Line 161: predict the future is limited to short time frames, for processes with clear-cut causes and effects.
Line 162: Waterfall development performs very poorly in the face of uncertainty and change. It is designed 
Line 163: around the notion that all things can be known and planned in advance. A better approach is to 
Line 164: embrace change and uncertainty, making it an active part of the development process. This is the 
Line 165: basis of agile development. At its core lies an iterative approach, where we take one small feature that 
Line 166: our users care about, then build that feature completely, allowing our users to try it out. If changes 
Line 167: are needed, we do another iteration of development. The costs of change are much lower when our 
Line 168: development process actively supports change.
Line 169: Professional agile development processes rely on maintaining one single code base that is always tested 
Line 170: and represents the best version to date of our software. This code is always ready to deploy to users. We 
Line 171: grow this code base one feature at a time, continuously improving its design as we go.
Line 172: 
Line 173: --- 페이지 74 ---
Line 174: Exploring agile methods
Line 175: 51
Line 176: Techniques such as TDD play a major role in this, by ensuring our code is well designed and thoroughly 
Line 177: tested. Every time we commit code to the main trunk, we already know it has passed many TDD tests. 
Line 178: We know we are happy with its design.
Line 179: To better support iterative development, we choose an iterative technique for capturing requirements. 
Line 180: This technique is called user stories, which we will describe in the next section.
Line 181: Reading user stories – the building block of planning
Line 182: As development is iterative and embraces refactoring and reworking, it makes sense that the old 
Line 183: methods of specifying requirements won’t work. We are no longer served by thousands of pages of 
Line 184: requirements set in stone up front. We are better served by taking one requirement at a time, building 
Line 185: it, and learning from it. Over time, we can prioritize the features users want and learn more about 
Line 186: how a good design will look. 
Line 187: Through agile techniques, we do not have to know the future in advance; we can discover it alongside 
Line 188: our users. 
Line 189: Supporting this change is a new way to express requirements. Waterfall projects start with a complete 
Line 190: requirements document, detailing every feature formally. The complete set of requirements – often 
Line 191: thousands of them – were expressed in formal language such as “The system shall…” and then the 
Line 192: details were explained in terms of changes to the software system. With agile development, we don’t 
Line 193: want to capture requirements in that way. We want to capture them following two key principles:
Line 194: •	 Requirements are presented one at a time in isolation
Line 195: •	 We emphasize the value to the user, not the technical impact on the system
Line 196: The technique for doing this is called the user story. The first user story to tackle for Wordz looks 
Line 197: as follows: 
Line 198: Figure 4.5 – The user story
Line 199: 
Line 200: --- 페이지 75 ---
Line 201: Building an Application Using TDD
Line 202: 52
Line 203: The format of a user story is always the same – it comprises three sections:
Line 204: •	 As a [person or machine that uses the software], …
Line 205: •	 I want [a specific outcome from that software] …
Line 206: •	 … so that [a task that is important is achieved].
Line 207: The three sections are written this way to emphasize that agile development centers around value 
Line 208: delivered to the users of the system. These are not technical requirements. They do not (indeed, must 
Line 209: not) specify a solution. They simply state which user of the system should get what valuable outcome 
Line 210: out of it.
Line 211: The first part always starts with “As a ….” It then names the user role that this story will improve. This 
Line 212: can be any user – whether human or machine – of the system. The one thing it must never be is the 
Line 213: system itself, as in, “As a system.” This is to enforce clear thinking in our user stories; they must always 
Line 214: deliver some benefit to some user of the system. They are never an end in themselves. 
Line 215: To give an example from a photo-taking app, as developers, we might want a technical activity to 
Line 216: optimize photo storage. We might write a story such as, “As a system, I want to compact my image data 
Line 217: to optimize storage.” Instead of writing from a technical viewpoint, we can reframe this to highlight 
Line 218: the benefit to the user: “As a photographer, I want fast access to my stored photographs and to maximize 
Line 219: space for new ones.”
Line 220: The “I want…” section describes the desired outcome the user wants. It is always described in user 
Line 221: terminology, not technical terminology. Again, this helps us focus on what our users want our software 
Line 222: to achieve for them. It is the purest form of capturing the requirements. There is no attempt made at 
Line 223: this stage to suggest how anything will be implemented. We simply capture what it is that the user 
Line 224: sets out to do.
Line 225: The final part, “…so that…”, provides context. The “As a …” section describes who benefits, the “I 
Line 226: want…” section describes how they benefit, and the “…so that…” section describes why they need 
Line 227: this feature. This forms the justification for the time and costs required for developing this feature. It 
Line 228: can be used to prioritize which features to develop next. 
Line 229: This user story is where we start development. The heart of the Wordz application is its ability to 
Line 230: evaluate and score the player’s current guess at a word. It’s worth looking at how this work will proceed.
Line 231: Combining agile development with TDD
Line 232: TDD is a perfect complement to agile development. As we learned in earlier chapters, TDD helps us 
Line 233: improve our design and prove that our logic is correct. Everything we do is aimed at delivering working 
Line 234: software to our users, without defects, as quickly as possible. TDD is a great way to achieve this.
Line 235: 
Line 236: --- 페이지 76 ---
Line 237: Summary
Line 238: 53
Line 239: The workflow we will use is typical for an agile TDD project:
Line 240: 1.	
Line 241: Pick a user story prioritized for impact.
Line 242: 2.	
Line 243: Think a little about the design to aim for.
Line 244: 3.	
Line 245: Use TDD to write the application logic in the core.
Line 246: 4.	
Line 247: Use TDD to write code to connect the core to a database.
Line 248: 5.	
Line 249: Use TDD to write code to connect to an API endpoint.
Line 250: This process repeats. It forms the rhythm of writing the core application logic under a unit test, then 
Line 251: growing the application outward, connecting it to API endpoints, user interfaces, databases, and 
Line 252: external web services. Working this way, we retain a lot of flexibility within our code. We can also 
Line 253: work quickly, concentrating upfront on the most important parts of our application code. 
Line 254: Summary
Line 255: We’ve learned the key ideas that let us build an application iteratively, getting value at each step and 
Line 256: avoiding a big design up front approach that often disappoints. We can read user stories, which will 
Line 257: drive building our TDD application in small, well-defined steps. We now also know the process we 
Line 258: will use to build our application – using TDD to get a thoroughly tested, central core of clean code, 
Line 259: and then drive out connections to the real world.
Line 260: In the next chapter, we’ll make a start on our application. We will learn the three key components of 
Line 261: every TDD test by writing our first test and making sure it passes.
Line 262: Questions and answers
Line 263: 1.	
Line 264: Waterfall development sounds as though it should work well – why doesn’t it?
Line 265: Waterfall development would work well if we knew about every missing requirement, every 
Line 266: change request from the users, every bad design decision, and every coding error at the start 
Line 267: of the project. But humans have limited foresight, and it is impossible to know these things 
Line 268: in advance. So, waterfall projects never work smoothly. Expensive changes crop up at a later 
Line 269: stage of the project – just when you don’t have the time to address them.
Line 270: 2.	
Line 271: Can we do agile development without TDD?
Line 272: Yes, although that way, we miss out on the advantages of TDD that we’ve covered in previous 
Line 273: chapters. We also make our job harder. An important part of Agile development is always 
Line 274: demonstrating the latest working code. Without TDD, we need to add a large manual test 
Line 275: cycle into our process. This slows us down significantly.
Line 276: 
Line 277: --- 페이지 77 ---
Line 278: Building an Application Using TDD
Line 279: 54
Line 280: Further reading
Line 281: •	 Mastering React Test-Driven Development, ISBN 9781789133417 
Line 282: If you would like to build a user interface for the Wordz application, using the popular 
Line 283: React web UI framework is an excellent way to do it. This Packt book is one of my personal 
Line 284: favorites. It shows how to apply the same kind of TDD techniques we are using server-side 
Line 285: into frontend work. It also explains React development from the ground up in a highly 
Line 286: readable way.
Line 287: •	 Agile Model-Based Systems Engineering Cookbook, ISBN 9781838985837
Line 288: This book provides further details on how to craft effective user stories and other useful 
Line 289: techniques for capturing agile requirements, modeling, and analysis.