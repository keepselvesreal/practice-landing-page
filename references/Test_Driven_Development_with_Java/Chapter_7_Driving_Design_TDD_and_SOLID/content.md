Line 1: 
Line 2: --- 페이지 118 ---
Line 3: 7
Line 4: Driving Design – TDD 
Line 5: and SOLID
Line 6: So far, we’ve created some basic unit tests that have driven out a simple design for a couple of classes. 
Line 7: We’ve experienced how test-driven development (TDD) makes decision-making about design choices 
Line 8: central. In order to build out to a larger application, we are going to need to be able to handle designs 
Line 9: of greater complexity. To do this, we are going to apply some recommended approaches to assessing 
Line 10: what makes one design preferable to another.
Line 11: The SOLID principles are five design guidelines that steer designs toward being more flexible and 
Line 12: modular. The word SOLID is an acronym, where each letter represents one of five principles whose 
Line 13: names begin with that letter. These principles existed long before they were known by this name. They 
Line 14: have proven helpful in my experience, and it is worth understanding the benefits each one brings and 
Line 15: how we can apply them to our code. To do this, we will use a running code example in this chapter. 
Line 16: It is a simple program that draws shapes of various kinds using simple American Standard Code for 
Line 17: Information Interchange (ASCII) art on a console.
Line 18: Before we start, let’s think about the best order to learn these five principles. The acronym SOLID is easy 
Line 19: to say, but it isn’t the easiest way to learn the principles. Some principles build on others. Experience 
Line 20: shows that some are used more than others, especially when doing TDD. For this reason, we’re going 
Line 21: to review the principles in the order SDLOI. It doesn’t sound as good, as I’m sure you will agree, but 
Line 22: it makes a better order of learning.
Line 23: Originally, the SOLID principles were conceived as patterns that applied to classes in object-oriented 
Line 24: programming (OOP), but they are more general-purpose than that. They equally apply to individual 
Line 25: methods in a class as well as the class itself. They also apply to the design of microservice interconnections 
Line 26: and function design in functional programming. We will be seeing examples applied at both the class 
Line 27: level and the method level in this chapter.
Line 28: 
Line 29: --- 페이지 119 ---
Line 30: Driving Design – TDD and SOLID
Line 31: 96
Line 32: In this chapter, we’re going to cover the following main topics:
Line 33: •	 Test guide–we drive the design
Line 34: •	 Single Responsibility Principle (SRP)–simple building blocks
Line 35: •	 Dependency Inversion Principle (DIP)–hiding irrelevant details
Line 36: •	 Liskov Substitution Principle (LSP)–swappable objects
Line 37: •	 Open-Closed Principle (OCP)–extensible design
Line 38: •	 Interface Segregation Principle (ISP)–effective interfaces
Line 39: Technical requirements
Line 40: The code for this chapter can be found at https://github.com/PacktPublishing/Test-
Line 41: Driven-Development-with-Java/tree/main/chapter07. A running example of code 
Line 42: that draws shapes using all five SOLID principles is provided.
Line 43: Test guide – we drive the design
Line 44: In Chapter 5, Writing Our First Test, we wrote our first test. To do that, we ran through a number of 
Line 45: design decisions. Let’s review that initial test code and list all the design decisions we had to make, 
Line 46: as follows:
Line 47: @Test
Line 48: public void oneIncorrectLetter() {
Line 49:     var word = new Word("A");
Line 50:     var score = word.guess("Z");
Line 51:     assertThat( score.letter(0) ).isEqualTo(Letter.INCORRECT);
Line 52: }
Line 53: We decided on the following:
Line 54: •	 What to test
Line 55: •	 What to call the test
Line 56: •	 What to call the method under test
Line 57: •	 Which class to put that method on
Line 58: •	 The signature of that method
Line 59: 
Line 60: --- 페이지 120 ---
Line 61: SRP – simple building blocks
Line 62: 97
Line 63: •	 The constructor signature of the class
Line 64: •	 Which other objects should collaborate
Line 65: •	 The method signatures involved in that collaboration
Line 66: •	 What form the output of this method will take
Line 67: •	 How to access that output and assert that it worked
Line 68: These are all design decisions that our human minds must make. TDD leaves us very much hands-on 
Line 69: when it comes to designing our code and deciding how it should be implemented. To be honest, I 
Line 70: am happy about that. Designing is rewarding and TDD provides helpful scaffolding rather than a 
Line 71: prescriptive approach. TDD acts as a guide to remind us to make these design decisions early. It also 
Line 72: provides a way to document these decisions as test code. Nothing more, but equally, nothing less.
Line 73: It can be helpful to use techniques such as pair programming or mobbing (also known as ensemble 
Line 74: programming) as we make these decisions—then, we add more experience and more ideas to our 
Line 75: solution. Working alone, we simply have to take the best decisions we can, based on our own experience.
Line 76: The critical point to get across here is that TDD does not and cannot make these decisions for us. We 
Line 77: must make them. As such, it is useful to have some guidelines to steer us toward better designs. A set 
Line 78: of five design principles known as the SOLID principles are helpful. SOLID is an acronym for the 
Line 79: following five principles:
Line 80: •	 SRP
Line 81: •	 OCP
Line 82: •	 LSP
Line 83: •	 ISP
Line 84: •	 DIP
Line 85: In the following sections, we will learn what these principles are and how they help us write well-
Line 86: engineered code and tests. We will start with SRP, which is arguably the most foundational principle 
Line 87: of any style of program design.
Line 88: SRP – simple building blocks
Line 89: In this section, we will examine the first principle, known as SRP. We will use a single code example 
Line 90: throughout all sections. This will clarify how each principle is applied to an object-oriented (OO) 
Line 91: design. We’re going to look at a classic example of OO design: drawing shapes. The following diagram 
Line 92: is an overview of the design in Unified Modeling Language (UML), describing the code presented 
Line 93: in the chapter:
Line 94: 
Line 95: --- 페이지 121 ---
Line 96: Driving Design – TDD and SOLID
Line 97: 98
Line 98: Figure 7.1 – UML diagram for shapes code
Line 99: This diagram shows an overview of the Java code available in the GitHub folder for this chapter. We’ll 
Line 100: be using specific parts of the code to illustrate how each of the SOLID principles has been used to 
Line 101: create this design.
Line 102: UML diagrams
Line 103: UML was created in 1995 by Grady Booch, Ivar Jacobson, and James Rumbaugh. UML 
Line 104: is a way of visualizing OO designs at a high level. The preceding diagram is a UML class 
Line 105: diagram. UML offers many other kinds of useful diagrams. You can learn more at https://
Line 106: www.packtpub.com/product/uml-2-0-in-action-a-project-based-
Line 107: tutorial/9781904811558.
Line 108: SRP guides us to break code down into pieces that encapsulate a single aspect of our solution. Maybe 
Line 109: that is a technical aspect in nature—such as reading a database table—or maybe it is a business rule. 
Line 110: Either way, we split different aspects into different pieces of code. Each piece of code is responsible 
Line 111: for a single detail, which is where the name SRP comes from. Another way of looking at this is that 
Line 112: a piece of code should only ever have one reason to change. Let’s examine why this is an advantage in 
Line 113: the following sections.
Line 114: 
Line 115: --- 페이지 122 ---
Line 116: SRP – simple building blocks
Line 117: 99
Line 118: Too many responsibilities make code harder to work with
Line 119: A common programming mistake is to combine too many responsibilities into a single piece of code. 
Line 120: If we have a class that can generate Hypertext Markup Language (HTML), execute a business rule, 
Line 121: and fetch data from a database table, that class will have three reasons to change. Any time a change 
Line 122: in one of these areas is necessary, we will risk making a code change that breaks the other two aspects. 
Line 123: The technical term for this is that the code is highly coupled. This leads to changes in one area rippling 
Line 124: out and affecting other areas.
Line 125: We can visualize this as code block A in the following diagram:
Line 126: Figure 7.2 – Single component: multiple reasons to change
Line 127: Block A deals with three things, so a change to any of them implies a change in A. To improve this, 
Line 128: we apply SRP and separate out the code responsible for creating HTML, applying business rules, and 
Line 129: accessing the database. Each of those three code blocks—A, B, and C—now only has one reason to 
Line 130: change. Changing any single code block should not result in changes rippling out to the other blocks.
Line 131: We can visualize this in the following diagram:
Line 132: Figure 7.3 – Multiple components: one reason to change
Line 133: 
Line 134: --- 페이지 123 ---
Line 135: Driving Design – TDD and SOLID
Line 136: 100
Line 137: Each code block deals with one thing and has only one reason to change. We can see that SRP works 
Line 138: to limit the scope of future code changes. It also makes it easier to find code in a large code base, as 
Line 139: it is logically organized.
Line 140: Applying SRP gives other benefits, as follows:
Line 141: •	 Ability to reuse code
Line 142: •	 Simplified future maintenance
Line 143: Ability to reuse code
Line 144: Reusing code has been a goal of software engineering for a long time. Creating software from scratch 
Line 145: takes time, costs money, and prevents a software engineer from doing something else. It makes sense 
Line 146: that if we create something that is generally useful, we use it again wherever possible. The barrier to 
Line 147: this happens when we have created large, application-specific pieces of software. The fact that they 
Line 148: are highly specialized means they can only be used in their original context.
Line 149: By creating smaller, more general-purpose software components, we will be able to use those again 
Line 150: in different contexts. The smaller the scope of what the component aims to do, the more likely it is 
Line 151: that we can reuse it without modification. If we have a small function or class that does one thing, it 
Line 152: becomes easy to reuse that across our code base. It may even end up as part of a framework or library 
Line 153: that we can reuse across multiple projects.
Line 154: SRP does not guarantee that code will be reusable, but it does aim to reduce the scope of what any 
Line 155: piece of code does. This way of thinking about code as a series of building blocks where each one does 
Line 156: a small part of the overall task is more likely to result in reusable components.
Line 157: Simplified future maintenance
Line 158: As we write code, we’re aware that we are not just writing to solve a problem now, but also writing 
Line 159: code that might be revisited in the future. This might be done by other people in the team or maybe 
Line 160: by ourselves. We want to make this future work as simple as possible. To achieve this, we need to keep 
Line 161: our code well-engineered—making it safe and easy to work with later.
Line 162: Duplicated code is a problem for maintenance—it complicates future code changes. If we copy and 
Line 163: paste a section of code three times, let’s say, it seems quite obvious to us at the time what we are doing. 
Line 164: We have one concept that needs to happen three times, so we paste it three times. But when it comes 
Line 165: time to read the code again, that thought process has been lost. It just reads as three unrelated pieces 
Line 166: of code. We lose engineering information by copy and paste. We will need to reverse-engineer that code 
Line 167: to work out that there are three places where we need to change it.
Line 168: 
Line 169: --- 페이지 124 ---
Line 170: SRP – simple building blocks
Line 171: 101
Line 172: Counter-example – shapes code that violates SRP
Line 173: To see the value of applying SRP, let’s consider a piece of code that doesn’t use it. The following code 
Line 174: snippet has a list of shapes that all get drawn when we call the draw() method:
Line 175: public class Shapes {
Line 176:     private final List<Shape> allShapes = new ArrayList<>();
Line 177:     public void add(Shape s) {
Line 178:         allShapes.add(s);
Line 179:     }
Line 180:     public void draw(Graphics g) {
Line 181:         for (Shape s : allShapes) {
Line 182:             switch (s.getType()) {
Line 183:                 case "textbox":
Line 184:                     var t = (TextBox) s;
Line 185:                     g.drawText(t.getText());
Line 186:                     break;
Line 187:                 case "rectangle":
Line 188:                     var r = (Rectangle) s;
Line 189:                     for (int row = 0;
Line 190:                           row < r.getHeight();
Line 191:                           row++) {
Line 192:                         g.drawLine(0, r.getWidth());
Line 193:                     }
Line 194:             }
Line 195:         }
Line 196:     }
Line 197: }
Line 198: We can see that this code has four responsibilities, as follows:
Line 199: •	 Managing the list of shapes with the add() method
Line 200: •	 Drawing all the shapes in the list with the draw() method
Line 201: •	 Knowing every type of shape in the switch statement
Line 202: •	 Has implementation details for drawing each shape type in the case statements
Line 203: 
Line 204: --- 페이지 125 ---
Line 205: Driving Design – TDD and SOLID
Line 206: 102
Line 207: If we want to add a new type of shape—triangle, for example—then we’ll need to change this code. 
Line 208: This will make it longer, as we need to add details about how to draw the shape inside a new case 
Line 209: statement. This makes the code harder to read. The class will also have to have new tests.
Line 210: Can we change this code to make adding a new type of shape easier? Certainly. Let’s apply SRP 
Line 211: and refactor.
Line 212: Applying SRP to simplify future maintenance
Line 213: We will refactor this code to apply SRP, taking small steps. The first thing to do is to move that 
Line 214: knowledge of how to draw each type of shape out of this class, as follows:
Line 215: package shapes;
Line 216: import java.util.ArrayList;
Line 217: import java.util.List;
Line 218: public class Shapes {
Line 219:     private final List<Shape> allShapes = new ArrayList<>();
Line 220:     public void add(Shape s) {
Line 221:         allShapes.add(s);
Line 222:     }
Line 223:     public void draw(Graphics g) {
Line 224:         for (Shape s : allShapes) {
Line 225:             switch (s.getType()) {
Line 226:                 case "textbox":
Line 227:                     var t = (TextBox) s;
Line 228:                     t.draw(g);
Line 229:                     break;
Line 230:                 case "rectangle":
Line 231:                     var r = (Rectangle) s;
Line 232:                     r.draw(g);
Line 233:             }
Line 234:         }
Line 235:     }
Line 236: }
Line 237: 
Line 238: --- 페이지 126 ---
Line 239: SRP – simple building blocks
Line 240: 103
Line 241: The code that used to be in the case statement blocks has been moved into the shape classes. Let’s 
Line 242: look at the changes in the Rectangle class as one example—you can see what’s changed in the 
Line 243: following code snippet:
Line 244: public class Rectangle {
Line 245:     private final int width;
Line 246:     private final int height;
Line 247:     public Rectangle(int width, int height){
Line 248:         this.width = width;
Line 249:         this.height = height;
Line 250:     }
Line 251:     public void draw(Graphics g) {
Line 252:         for (int row=0; row < height; row++) {
Line 253:             g.drawHorizontalLine(width);
Line 254:         }
Line 255:     }
Line 256: }
Line 257: We can see how the Rectangle class now has the single responsibility of knowing how to draw a 
Line 258: rectangle. It does nothing else. The one and only reason it will have to change is if we need to change 
Line 259: how a rectangle is drawn. This is unlikely, meaning that we now have a stable abstraction. In other 
Line 260: words, the Rectangle class is a building block we can rely on. It is unlikely to change.
Line 261: If we examine our refactored Shapes class, we see that it too has improved. It has one responsibility 
Line 262: less because we moved that out into the TextBox and Rectangle classes. It is simpler to read 
Line 263: already, and simpler to test.
Line 264: SRP
Line 265: Do one thing and do it well. Have only one reason for a code block to change.
Line 266: More improvements can be made. We see that the Shapes class retains its switch statement and 
Line 267: that every case statement looks duplicated. They all do the same thing, which is to call a draw() 
Line 268: method on a shape class. We can improve this by replacing the switch statement entirely—but that 
Line 269: will have to wait until the next section, where we introduce the DIP.
Line 270: Before we do that, let’s think about how SRP applies to our test code itself.
Line 271: 
Line 272: --- 페이지 127 ---
Line 273: Driving Design – TDD and SOLID
Line 274: 104
Line 275: Organizing tests to have a single responsibility
Line 276: SRP also helps us to organize our tests. Each test should test only one thing. Perhaps this would be 
Line 277: a single happy path or a single boundary condition. This makes it simpler to localize any faults. We 
Line 278: find the test that failed, and because it concerns only a single aspect of our code, it is easy to find the 
Line 279: code where the defect must be. The recommendation to only have a single assertion for each test 
Line 280: flows naturally from this.
Line 281: Separating tests with different configurations
Line 282: Sometimes, a group of objects can be arranged to collaborate in multiple different ways. The 
Line 283: tests for this group are often better if we write a single test per configuration. We end up with 
Line 284: multiple smaller tests that are easier to work with.
Line 285: This is an example of applying SRP to each configuration of that group of objects and capturing 
Line 286: that by writing one test for each specific configuration.
Line 287: We’ve seen how SRP helps us create simple building blocks for our code that are simpler to test and 
Line 288: easier to work with. The next powerful SOLID principle to look at is DIP. This is a very powerful tool 
Line 289: for managing complexity.
Line 290: DIP – hiding irrelevant details
Line 291: In this section, we will learn how the DIP allows us to split code into separate components that can 
Line 292: change independently of each other. We will then see how this naturally leads to the OCP part of SOLID.
Line 293: Dependency inversion (DI) means that we write code to depend on abstractions, not details. The 
Line 294: opposite of this is having two code blocks, one that depends on the detailed implementation of the 
Line 295: other. Changes to one block will cause changes to another. To see what this problem looks like in 
Line 296: practice, let’s review a counter-example. The following code snippet begins where we left off with the 
Line 297: Shapes class after applying SRP to it:
Line 298: package shapes;
Line 299: import java.util.ArrayList;
Line 300: import java.util.List;
Line 301: public class Shapes {
Line 302: 
Line 303: --- 페이지 128 ---
Line 304: DIP – hiding irrelevant details
Line 305: 105
Line 306:     private final List<Shape> allShapes = new ArrayList<>();
Line 307:     public void add(Shape s) {
Line 308:         allShapes.add(s);
Line 309:     }
Line 310:     public void draw(Graphics g) {
Line 311:         for (Shape s : allShapes) {
Line 312:             switch (s.getType()) {
Line 313:                 case "textbox":
Line 314:                     var t = (TextBox) s;
Line 315:                     t.draw(g);
Line 316:                     break;
Line 317:                 case "rectangle":
Line 318:                     var r = (Rectangle) s;
Line 319:                     r.draw(g);
Line 320:             }
Line 321:         }
Line 322:     }
Line 323: }
Line 324: This code does work well to maintain a list of Shape objects and draw them. The problem is that it 
Line 325: knows too much about the types of shapes it is supposed to draw. The draw() method features a 
Line 326: switch-on-type of object that you can see. That means that if anything changes about which types 
Line 327: of shapes should be drawn, then this code must also change. If we want to add a new Shape to the 
Line 328: system, then we have to modify this switch statement and the associated TDD test code.
Line 329: The technical term for one class knowing about another is that a dependency exists between them. 
Line 330: The Shapes class depends on the TextBox and Rectangle classes. We can represent that visually 
Line 331: in the following UML class diagram:
Line 332: 
Line 333: --- 페이지 129 ---
Line 334: Driving Design – TDD and SOLID
Line 335: 106
Line 336: Figure 7.4 – Depending on the details
Line 337: We can see that the Shapes class depends directly on the detail of the Rectangle and TextBox 
Line 338: classes. This is shown by the direction of the arrows in the UML class diagram. Having these dependencies 
Line 339: makes working with the Shapes class more difficult for the following reasons:
Line 340: •	 We have to change the Shapes class to add a new kind of shape
Line 341: •	 Any changes in the concrete classes such as Rectangle will cause this code to change
Line 342: •	 The Shapes class will get longer and less easy to read
Line 343: •	 We will end up with more test cases
Line 344: •	 Each test case will be coupled to concrete classes such as Rectangle
Line 345: This is a very procedural approach to creating a class that deals with multiple kinds of shapes. It violates 
Line 346: SRP by doing too much and knowing too much detail about each kind of shape object. The Shapes 
Line 347: class depends on the details of concrete classes such as Rectangle and TextBox, which directly 
Line 348: causes the aforementioned problems.
Line 349: Thankfully, there is a better way. We can use the power of an interface to improve this, by making 
Line 350: it so that the Shapes class does not depend on those details. This is called DI. Let’s see what that 
Line 351: looks like next.
Line 352: Applying DI to the shapes code
Line 353: We can improve the shapes code by applying the Dependency Inversion Principle (DIP) described 
Line 354: in the previous chapter. Let’s add a draw() method to our Shape interface, as follows:
Line 355: package shapes;
Line 356: public interface Shape {
Line 357:     void draw(Graphics g);
Line 358: }
Line 359: 
Line 360: --- 페이지 130 ---
Line 361: DIP – hiding irrelevant details
Line 362: 107
Line 363: This interface is our abstraction of the single responsibility that each shape has. Each shape must 
Line 364: know how to draw itself when we call the draw() method. The next step is to make our concrete 
Line 365: shape classes implement this interface.
Line 366: Let’s take the Rectangle class as an example. You can see this here:
Line 367: public class Rectangle implements Shape {
Line 368:     private final int width;
Line 369:     private final int height;
Line 370:     public Rectangle(int width, int height){
Line 371:         this.width = width;
Line 372:         this.height = height;
Line 373:     }
Line 374:     @Override
Line 375:     public void draw(Graphics g) {
Line 376:         for (int row=0; row < height; row++) {
Line 377:             g.drawHorizontalLine(width);
Line 378:         }
Line 379:     }
Line 380: }
Line 381: We’ve now introduced the OO concept of polymorphism into our shape classes. This breaks the 
Line 382: dependency that the Shapes class has on knowing about the Rectangle and TextBox classes. 
Line 383: All that the Shapes class now depends on is the Shape interface. It no longer needs to know the 
Line 384: type of each shape.
Line 385: We can refactor the Shapes class to look like this:
Line 386: public class Shapes {
Line 387:     private final List<Shape> all = new ArrayList<>();
Line 388:     public void add(Shape s) {
Line 389:         all.add(s);
Line 390:     }
Line 391:     public void draw(Graphics graphics) {
Line 392:         all.forEach(shape->shape.draw(graphics));
Line 393: 
Line 394: --- 페이지 131 ---
Line 395: Driving Design – TDD and SOLID
Line 396: 108
Line 397:     }
Line 398: }
Line 399: This refactoring has completely removed the switch statement and the getType() method, making 
Line 400: the code much simpler to understand and test.  If we add a new kind of shape, the Shapes class 
Line 401: no longer needs to change. We have broken that dependency on knowing the details of shape classes.
Line 402: One minor refactor moves the Graphics parameter we pass into the draw() method into a field, 
Line 403: initialized in the constructor, as illustrated in the following code snippet:
Line 404: public class Shapes {
Line 405:     private final List<Shape> all = new ArrayList<>();
Line 406:     private final Graphics graphics;
Line 407:     public Shapes(Graphics graphics) {
Line 408:         this.graphics = graphics;
Line 409:     }
Line 410:     public void add(Shape s) {
Line 411:         all.add(s);
Line 412:     }
Line 413:     public void draw() {
Line 414:         all.forEach(shape->shape.draw(graphics));
Line 415:     }
Line 416: }
Line 417: This is DIP at work. We’ve created an abstraction in the Shape interface. The Shapes class is a 
Line 418: consumer of this abstraction. The classes implementing that interface are providers. Both sets of classes 
Line 419: depend only on the abstraction; they do not depend on details inside each other. There are no references 
Line 420: to the Rectangle class in the Shapes class, and there are no references to the Shapes inside 
Line 421: the Rectangle class. We can see this inversion of dependencies visualized in the following UML 
Line 422: class diagram—see how the direction of the dependency arrows has changed compared to Figure 7.4:
Line 423: 
Line 424: --- 페이지 132 ---
Line 425: LSP – swappable objects
Line 426: 109
Line 427: Figure 7.5 – Inverting dependencies
Line 428: In this version of the UML diagram, the arrows describing the dependencies between classes point the 
Line 429: opposite way. The dependencies have been inverted—hence, the name of this principle. Our Shapes 
Line 430: class now depends on our abstraction, the Shape interface. So do all the Rectangle class and 
Line 431: TextBox class concrete implementations. We have inverted the dependency graph and turned the 
Line 432: arrows upside down. DI fully decouples classes from each other and, as such, is very powerful. We 
Line 433: will see how this leads to a key technique for TDD testing when we look at Chapter 8, Test Doubles 
Line 434: – Stubs and Mocks.
Line 435: DIP
Line 436: Make code depend on abstractions and not on details.
Line 437: We’ve seen how DIP is a major tool we can use to simplify our code. It allows us to write code that 
Line 438: deals with an interface, and then use that code with any concrete class that implements that interface. 
Line 439: This begs a question: can we write a class that implements an interface but will not work correctly? 
Line 440: That’s the subject of our next section.
Line 441: LSP – swappable objects
Line 442: Turing Award winner Barbara Liskov is the creator of a rule concerning inheritance that is now 
Line 443: commonly known as LSP. It was brought about by a question in OOP: if we can extend a class and use 
Line 444: it in place of the class we extended, how can we be sure the new class will not break things?
Line 445: We’ve seen in the previous section on DIP how we can use any class that implements an interface in 
Line 446: place of the interface itself. We also saw how those classes can provide any implementation they like 
Line 447: for that method. The interface itself provides no guarantees at all about what might lurk inside that 
Line 448: implementation code.
Line 449: 
Line 450: --- 페이지 133 ---
Line 451: Driving Design – TDD and SOLID
Line 452: 110
Line 453: There is, of course, a bad side to this—which LSP aims to avoid. Let’s explain this by looking at a 
Line 454: counter-example in code. Suppose we made a new class that implemented interface Shape, 
Line 455: such as this one (Warning: Do NOT run the code that follows in the MaliciousShape class!):
Line 456: public class MaliciousShape implements Shape {
Line 457:     @Override
Line 458:     public void draw(Graphics g) {
Line 459:         try {
Line 460:             String[] deleteEverything = {"rm", "-Rf", "*"};
Line 461:             Runtime.getRuntime().exec(deleteEverything,null);
Line 462:             g.drawText("Nothing to see here...");
Line 463:         } catch (Exception ex) {
Line 464:             // No action
Line 465:         }
Line 466:     }
Line 467: }
Line 468: Notice anything a little odd about that new class? It contains a Unix command to remove all our 
Line 469: files! This is not what we are expecting when we call the draw() method on a shape object. Due to 
Line 470: permissions failures, it might not be able to delete anything, but it’s an example of what can go wrong.
Line 471: An interface in Java can only protect the syntax of method calls we expect. It cannot enforce any 
Line 472: semantics. The problem with the preceding MaliciousShape class is that it does not respect the 
Line 473: intent behind the interface.
Line 474: LSP guides us to avoid this error. In other words, LSP states that any class that implements an interface 
Line 475: or extends another class must handle all the input combinations that the original class/interface could. It 
Line 476: must provide the expected outputs, it must not ignore valid inputs, and it must not produce completely 
Line 477: unexpected and undesired behavior. Classes written like this are safe to use through a reference to 
Line 478: their interface. The problem with our MaliciousShape class is that it was not compatible with 
Line 479: LSP—it added some extra totally unexpected and unwanted behavior.
Line 480: LSP formal definition
Line 481: American computer scientist Barbara Liskov came up with a formal definition: If p(x) is a 
Line 482: property provable about objects x of type T, then p(y) should be true for objects y of type S 
Line 483: where S is a subtype of T.
Line 484: 
Line 485: --- 페이지 134 ---
Line 486: LSP – swappable objects
Line 487: 111
Line 488: Reviewing LSP usage in the shapes code
Line 489: The classes that implement Shape all conform to LSP. This is clear in the TextBox class, as we can 
Line 490: see here:
Line 491: public class TextBox implements Shape {
Line 492:     private final String text;
Line 493:     public TextBox(String text) {
Line 494:         this.text = text;
Line 495:     }
Line 496:     @Override
Line 497:     public void draw(Graphics g) {
Line 498:         g.drawText(text);
Line 499:     }
Line 500: }
Line 501: The preceding code clearly can handle drawing any valid text provided to its constructor. It also provides 
Line 502: no surprises. It draws the text, using primitives from the Graphics class, and does nothing else.
Line 503: Other examples of LSP compliance can be seen in the following classes:
Line 504: •	 Rectangle
Line 505: •	 Triangle
Line 506: LSP
Line 507: A code block can be safely swapped for another if it can handle the full range of inputs and 
Line 508: provide (at least) all expected outputs, with no undesired side effects.
Line 509: There are some surprising violations of LSP. Perhaps the classic one for the shapes code example is about 
Line 510: adding a Square class. In mathematics, a square is a kind of rectangle, with the extra constraint that 
Line 511: its height and width are equal. In Java code, should we make the Square class extend the Rectangle 
Line 512: class? How about the Rectangle class extending Square?
Line 513: Let’s apply LSP to decide. We will imagine some code that expects a Rectangle class so that it can 
Line 514: change its height, but not its width. If we passed a Square class to that code, would it work properly? 
Line 515: The answer is no. You would then have a square with unequal width and height. This fails LSP.
Line 516: The point of LSP is about making classes properly conform to interfaces. In the next section, we’ll 
Line 517: look at OCP, which is closely related to DI.
Line 518: 
Line 519: --- 페이지 135 ---
Line 520: Driving Design – TDD and SOLID
Line 521: 112
Line 522: OCP – extensible design
Line 523: In this section, we’ll see how OCP helps us write code that we can add new features to, without 
Line 524: changing the code itself. This does sound like an impossibility at first, but it flows naturally from DIP 
Line 525: combined with LSP.
Line 526: OCP results in code that is open to extension but closed to modification. We saw this idea at work 
Line 527: when we looked at DIP. Let’s review the code refactoring we did in the light of OCP.
Line 528: Let’s start with the original code for the Shapes class, as follows:
Line 529: public class Shapes {
Line 530:     private final List<Shape> allShapes = new ArrayList<>();
Line 531:     public void add(Shape s) {
Line 532:         allShapes.add(s);
Line 533:     }
Line 534:     public void draw(Graphics g) {
Line 535:         for (Shape s : allShapes) {
Line 536:             switch (s.getType()) {
Line 537:                 case "textbox":
Line 538:                     var t = (TextBox) s;
Line 539:                     g.drawText(t.getText());
Line 540:                     break;
Line 541:                 case "rectangle":
Line 542:                     var r = (Rectangle) s;
Line 543:                     for (int row = 0;
Line 544:                           row < r.getHeight();
Line 545:                           row++) {
Line 546:                         g.drawLine(0, r.getWidth());
Line 547:                     }
Line 548:             }
Line 549:         }
Line 550:     }
Line 551: }
Line 552: 
Line 553: --- 페이지 136 ---
Line 554: OCP – extensible design
Line 555: 113
Line 556: Adding a new type of shape requires modification of the code inside the draw() method. We will 
Line 557: be adding a new case statement in to support our new shape.
Line 558: Modifying existing code has several disadvantages, as set out here:
Line 559: •	 We invalidate prior testing. This is now different code than we had tested.
Line 560: •	 We might introduce an error that breaks some of the existing support for shapes.
Line 561: •	 The code will become longer and more difficult to read.
Line 562: •	 We might have several developers add shapes at the same time and get a merge conflict when 
Line 563: we combine their work.
Line 564: By applying DIP and refactoring the code, we ended up with this:
Line 565: public class Shapes {
Line 566:     private final List<Shape> all = new ArrayList<>();
Line 567:     private final Graphics graphics;
Line 568:     public Shapes(Graphics graphics) {
Line 569:         this.graphics = graphics;
Line 570:     }
Line 571:     public void add(Shape s) {
Line 572:         all.add(s);
Line 573:     }
Line 574:     public void draw() {
Line 575:         all.forEach(shape->shape.draw(graphics));
Line 576:     }
Line 577: }
Line 578: We can now see that adding a new type of shape does not need modification to this code. This is an 
Line 579: example of OCP at work. The Shapes class is open to having new kinds of shapes defined, but it is 
Line 580: closed against the need for modification when that new shape is added. This also means that any tests 
Line 581: relating to the Shapes class will remain unchanged, as there is no difference in behavior for this 
Line 582: class. That is a powerful advantage.
Line 583: OCP relies on DI to work. It is more or less a restatement of a consequence of applying DIP. It also 
Line 584: provides us with a technique to support swappable behavior. We can use DIP and OCP to create 
Line 585: plugin systems.
Line 586: 
Line 587: --- 페이지 137 ---
Line 588: Driving Design – TDD and SOLID
Line 589: 114
Line 590: Adding a new type of shape
Line 591: To see how this works in practice, let’s create a new type of shape, the RightArrow class, as follows:
Line 592: public class RightArrow implements Shape {
Line 593:   public void draw(Graphics g) {
Line 594:     g.drawText( "   \" );
Line 595:     g.drawText( "-----" );
Line 596:     g.drawText( "   /" );
Line 597:   }
Line 598: }
Line 599: The RightArrow class implements the Shape interface and defines a draw() method. To 
Line 600: demonstrate that nothing in the Shapes class needs to change in order to use this, let’s review some 
Line 601: code that uses both the Shapes and our new class, RightArrow, as follows:
Line 602: package shapes;
Line 603: public class ShapesExample {
Line 604:     public static void main(String[] args) {
Line 605:         new ShapesExample().run();
Line 606:     }
Line 607:     private void run() {
Line 608:         Graphics console = new ConsoleGraphics();
Line 609:         var shapes = new Shapes(console);
Line 610:         shapes.add(new TextBox("Hello!"));
Line 611:         shapes.add(new Rectangle(32,1));
Line 612:         shapes.add(new RightArrow());
Line 613:         shapes.draw();
Line 614:     }
Line 615: }
Line 616: We see that the Shapes class is being used in a completely normal way, without change. In fact, the 
Line 617: only change needed to use our new RightArrow class is to create an object instance and pass it to 
Line 618: the add() method of shapes.
Line 619: 
Line 620: --- 페이지 138 ---
Line 621: ISP – effective interfaces
Line 622: 115
Line 623: OCP
Line 624: Make code open for new behaviors, but closed for modifications.
Line 625: The power of OCP should now be clear. We can extend the capabilities of our code and keep changes 
Line 626: limited. We greatly reduce the risk of breaking code that is already working, as we no longer need 
Line 627: to change that code. OCP is a great way to manage complexity. In the next section, we’ll look at the 
Line 628: remaining SOLID principle: ISP.
Line 629: ISP – effective interfaces
Line 630: In this section, we will look at a principle that helps us write effective interfaces. It is known as ISP.
Line 631: ISP advises us to keep our interfaces small and dedicated to achieving a single responsibility. By small 
Line 632: interfaces, we mean having as few methods as possible on any single interface. These methods should 
Line 633: all relate to some common theme.
Line 634: We can see that this principle is really just SRP in another form. We are saying that an effective interface 
Line 635: should describe a single responsibility. It should cover one abstraction, not several. The methods on 
Line 636: the interface should strongly relate to each other and also to that single abstraction.
Line 637: If we need more abstractions, then we use more interfaces. We keep each abstraction in its own 
Line 638: separate interface, which is where the term interface segregation comes from —we keep different 
Line 639: abstractions apart.
Line 640: The related code smell to this is a large interface that covers several different topics in one. We could 
Line 641: imagine an interface having hundreds of methods in little groups—some relating to file management, 
Line 642: some about editing documents, and some about printing documents. Such interfaces quickly become 
Line 643: difficult to work with. ISP suggests that we improve this by splitting the interface into several smaller 
Line 644: ones. This split would preserve the groups of methods—so, you might see interfaces for file management, 
Line 645: editing, and printing, with relevant methods under each. We have made our code simpler to understand 
Line 646: by splitting apart these separate abstractions.
Line 647: Reviewing ISP usage in the shapes code
Line 648: The most noticeable use of ISP is in the Shape interface, as illustrated here:
Line 649: interface Shape {
Line 650:   void draw(Graphics g);
Line 651: }
Line 652: This interface clearly has a single focus. It is an interface with a very narrow focus, so much so that 
Line 653: only one method needs to be specified: draw(). There is no confusion arising from other mixed-in 
Line 654: 
Line 655: --- 페이지 139 ---
Line 656: Driving Design – TDD and SOLID
Line 657: 116
Line 658: concepts here and no unnecessary methods. That single method is both necessary and sufficient. The 
Line 659: other major example is in the Graphics interface, as shown here:
Line 660: public interface Graphics {
Line 661:     void drawText(String text);
Line 662:     void drawHorizontalLine(int width);
Line 663: }
Line 664: The Graphics interface contains only methods related to drawing graphics primitives on screen. 
Line 665: It has two methods—drawText to display a text string, and drawHorizontalLine to draw a 
Line 666: line in a horizontal direction. As these methods are strongly related—known technically as exhibiting 
Line 667: high cohesion—and few in number, ISP is satisfied. This is an effective abstraction over the graphics 
Line 668: drawing subsystem, tailored to our purposes.
Line 669: For completeness, we can implement this interface in a number of ways. The example in GitHub uses 
Line 670: a simple text console implementation:
Line 671: public class ConsoleGraphics implements Graphics {
Line 672:     @Override
Line 673:     public void drawText(String text) {
Line 674:         print(text);
Line 675:     }
Line 676:     @Override
Line 677:     public void drawHorizontalLine(int width) {
Line 678:         var rowText = new StringBuilder();
Line 679:         for (int i = 0; i < width; i++) {
Line 680:             rowText.append('X');
Line 681:         }
Line 682:         print(rowText.toString());
Line 683:     }
Line 684:     private void print(String text) {
Line 685:         System.out.println(text);
Line 686:     }
Line 687: }
Line 688: 
Line 689: --- 페이지 140 ---
Line 690: Summary
Line 691: 117
Line 692: That implementation is also LSP-compliant—it can be used wherever the Graphics interface 
Line 693: is expected.
Line 694: ISP
Line 695: Keep interfaces small and strongly related to a single idea.
Line 696: We’ve now covered all five of the SOLID principles and shown how they have been applied to the 
Line 697: shapes code. They have guided the design toward compact code, having a well-engineered structure 
Line 698: to assist future maintainers. We know how to incorporate these principles into our own code to gain 
Line 699: similar benefits.
Line 700: Summary
Line 701: In this chapter, we’ve looked at simple explanations of how the SOLID principles help us design both 
Line 702: our production code and our tests. We’ve worked through an example design that uses all five SOLID 
Line 703: principles. In future work, we can apply SRP to help us understand our design and limit the rework 
Line 704: involved in future changes. We can apply DIP to split up our code into independent small pieces, 
Line 705: leaving each piece to hide some of the details of our overall program, creating a divide-and-conquer 
Line 706: effect. Using LSP, we can create objects that can be safely and easily swapped. OCP helps us design 
Line 707: software that is simple to add functionality to. ISP will keep our interfaces small and easy to understand.
Line 708: The next chapter puts these principles to use to solve a problem in testing—how do we test the 
Line 709: collaborations between our objects?
Line 710: Questions and answers 
Line 711: 1.	
Line 712: Do the SOLID principles only apply to OO code?
Line 713: No. Although originally applied to an OO context, they have uses in both functional programming 
Line 714: and microservice design. SRP is almost universally useful—sticking to one main focus is 
Line 715: helpful for anything, even paragraphs of documentation. SRP thinking also helps us write a 
Line 716: pure function that does only one thing and a test that does only one thing. DIP and OCP are 
Line 717: easily done in functional contexts by passing in the dependency as a pure function, as we do 
Line 718: with Java lambdas. SOLID as a whole gives a set of goals for managing coupling and cohesion 
Line 719: among any kind of software components.
Line 720: 2.	
Line 721: Do we have to use SOLID principles with TDD?
Line 722: No. TDD works by defining the outcomes and public interface of a software component. How we 
Line 723: implement that component is irrelevant to a TDD test, but using principles such as SRP and DIP 
Line 724: makes it much easier to write tests against that code by giving us the test access points we need.
Line 725: 
Line 726: --- 페이지 141 ---
Line 727: Driving Design – TDD and SOLID
Line 728: 118
Line 729: 3.	
Line 730: Are SOLID principles the only ones we should use?
Line 731: No. We should use every technique at our disposal.
Line 732: The SOLID principles make a great starting point in shaping your code and we should take 
Line 733: advantage of them, but there are many other valid techniques to design software. The whole 
Line 734: catalog of design patterns, the excellent system of General Responsibility Assignment Software 
Line 735: Patterns (GRASP) by Craig Larman, the idea of information hiding by David L. Parnas, and the 
Line 736: ideas of coupling and cohesion all apply. We should use any and every technique we know—or 
Line 737: can learn about—to serve our goal of making software that is easy to read and safe to change.
Line 738: 4.	
Line 739: If we do not use the SOLID principles, can we still do TDD?
Line 740: Yes—very much so. TDD concerns itself with testing the behavior of code, not the details of 
Line 741: how it is implemented. SOLID principles simply help us create OO designs that are robust 
Line 742: and simpler to test.
Line 743: 5.	
Line 744: How does SRP relate to ISP?
Line 745: ISP guides us to prefer many shorter interfaces over one large interface. Each of the shorter 
Line 746: interfaces should relate to one single aspect of what a class should provide. This is usually some 
Line 747: kind of role, or perhaps a subsystem. ISP can be thought of as making sure our interfaces each 
Line 748: apply the SRP and do only one thing—well.
Line 749: 6.	
Line 750: How does OCP relate to DIP and LSP?
Line 751: OCP guides us to create software components that can have new capabilities added without 
Line 752: changing the component itself. This is done by using a plugin design. The component will allow 
Line 753: separate classes to be plugged in providing the new capabilities. The way to do this is to create 
Line 754: an abstraction of what a plugin should do in an interface—DIP. Then, create concrete plugin 
Line 755: implementations of this conforming to LSP. After that, we can inject these new plugins into 
Line 756: our component. OCP relies on DIP and LSP to work.