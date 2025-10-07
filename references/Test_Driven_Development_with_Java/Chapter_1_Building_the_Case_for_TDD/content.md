Line 1: 
Line 2: --- 페이지 26 ---
Line 3: 1
Line 4: Building the Case for TDD
Line 5: Before we dive into what test-driven development (TDD) is and how to use it, we’re going to need 
Line 6: to understand why we need it. Every seasoned developer knows that bad code is easier to write than 
Line 7: good code. Even good code seems to get worse over time. Why?
Line 8: In this chapter, we will review the technical failures that make source code difficult to work with. We’ll 
Line 9: consider the effect that bad code has on both the team and the business bottom line. By the end of the 
Line 10: chapter, we’ll have a clear picture of the anti-patterns we need to avoid in our code.
Line 11: In this chapter, we’re going to cover the following main topics:
Line 12: •	 Writing code badly
Line 13: •	 Recognizing bad code
Line 14: •	 Decreasing team performance
Line 15: •	 Diminishing business outcomes
Line 16: Writing code badly
Line 17: As every developer knows, it seems a lot easier to write bad code than to engineer good code. We can 
Line 18: define good code as being easy to understand and safe to change. Bad code is therefore the opposite 
Line 19: of this, where it is very difficult to read the code and understand what problem it is supposed to be 
Line 20: solving. We fear changing bad code – we know that we are likely to break something.
Line 21: My own troubles with bad code go all the way back to my first program of note. This was a program 
Line 22: written for a school competition, which aimed to assist realtors to help their customers find the 
Line 23: perfect house. Written on the 8-bit Research Machines 380Z computer at school, this was 1981’s 
Line 24: answer to Rightmove.
Line 25: In those pre-web days, it existed as a simple desktop application with a green-screen text-based user 
Line 26: interface. It did not have to handle millions, never mind billions, of users. Nor did it have to handle 
Line 27: millions of houses. It didn’t even have a nice user interface.
Line 28: 
Line 29: --- 페이지 27 ---
Line 30: Building the Case for TDD
Line 31: 4
Line 32: As a piece of code, it was a couple of thousand lines of Microsoft Disk BASIC 9 code. There was no code 
Line 33: structure to speak of, just thousands of lines resplendent with uneven line numbers and festooned 
Line 34: with global variables. To add an even greater element of challenge, BASIC limited every variable to a 
Line 35: two-letter name. This made every name in the code utterly incomprehensible. The source code was 
Line 36: intentionally written to have as few spaces in it as possible in order to save memory. When you only had 
Line 37: 32KB of RAM to fit all of the program code, the data, and the operating system in, every byte mattered.
Line 38: The program only offered its user basic features. The user interface was of its time, using only text-based 
Line 39: forms. It predated graphical operating systems by a decade. The program also had to implement its 
Line 40: own data storage system, using files on 5.25-inch floppy disks. Again, affordable database components 
Line 41: were of the future. The main feature of the program in question was that users could search for 
Line 42: houses within certain price ranges and feature sets. They could filter by terms such as the number of 
Line 43: bedrooms or price range.
Line 44: However, the code itself really was a mess. See for yourself – here is a photograph of the original listing:
Line 45: Figure 1.1 – The estate agent code listing
Line 46: 
Line 47: --- 페이지 28 ---
Line 48: Writing code badly
Line 49: 5
Line 50: This horror is the original paper listing of one of the development versions. It is, as you can see, 
Line 51: completely unreadable. It’s not just you. Nobody would be able to read it easily. I can’t and I wrote it. 
Line 52: I would go as far as to say it is a mess, my mess, crafted by me, one keystroke at a time.
Line 53: This kind of code is a nightmare to work with. It fails our definition of good code. It is not at all easy 
Line 54: to read that listing and understand what the code is supposed to be doing. It is not safe to change 
Line 55: that code. If we attempted to, we would find that we could never be certain about whether we have 
Line 56: broken some feature or not. We would also have to manually retest the entire application. This would 
Line 57: be time-consuming.
Line 58: Speaking of testing, I never thoroughly tested that code. It was all manually tested without even following 
Line 59: a formal test plan. At best, I would have run a handful of happy path manual tests. These were the 
Line 60: kind of tests that would confirm that you could add or delete a house, and that some representative 
Line 61: searches worked, but that was all. There was no way I ever tested every path through that code. I just 
Line 62: guessed that it would work.
Line 63: If the data handling had failed, I would not have known what had happened. I never tried it. Did 
Line 64: every possible search combination work? Who knew? I certainly had no idea. I had even less patience 
Line 65: to go through all that tedious manual testing. It worked, enough to win an award of sorts, but it was 
Line 66: still bad code.
Line 67: Understanding why bad code is written
Line 68: In my case, it was simply down to a lack of knowledge. I did not know how to write good code. But 
Line 69: there are also other reasons unrelated to skill. Nobody ever sets out to write bad code intentionally. 
Line 70: Developers do the best job they can with the tools available and to the best of their ability at that time.
Line 71: Even with the right skills, several common issues can result in bad code:
Line 72: •	 A lack of time to refine the code due to project deadlines
Line 73: •	 Working with legacy code whose structure prevents new code from being added cleanly
Line 74: •	 Adding a short-term fix for an urgent production fault and then never reworking it
Line 75: •	 Unfamiliarity with the subject area of the code
Line 76: •	 Unfamiliarity with the local idioms and development styles
Line 77: •	 Inappropriately using idioms from a different programming language
Line 78: Now that we’ve seen an example of code that is difficult to work with, and understood how it came 
Line 79: about, let’s turn to the obvious next question: how can we recognize bad code?
Line 80: 
Line 81: --- 페이지 29 ---
Line 82: Building the Case for TDD
Line 83: 6
Line 84: Recognizing bad code
Line 85: Admitting that our code is difficult to work with is one thing, but to move past that and write good 
Line 86: code, we need to understand why code is bad. Let’s identify the technical issues.
Line 87: Bad variable names
Line 88: Good code is self-describing and safe to change. Bad code is not.
Line 89: Names are the most critical factor in deciding whether code will be easy to work with or not. Good 
Line 90: names tell the reader clearly what to expect. Bad names do not. Variables should be named according 
Line 91: to what they contain. They should answer “why would I want to use this data? What will it tell me?”
Line 92: A string variable that has been named string is badly named. All we know is that it is a string. 
Line 93: This does not tell us what is in the variable or why we would want to use it. If that string represented 
Line 94: a surname, then by simply calling it surname, we would have helped future readers of our code 
Line 95: understand our intentions much better. They would be able to easily see that this variable holds a 
Line 96: surname and should not be used for any other purpose.
Line 97: The two-letter variable names we saw in the listing in Figure 1.1 represented a limitation of the BASIC 
Line 98: language. It was not possible to do better at the time, but as we could see, they were not helpful. It is 
Line 99: much harder to understand what sn means than surname, if that’s what the variable stores. To carry 
Line 100: that even further, if we decide to hold a surname in a variable named x, we have made things really 
Line 101: difficult for readers of our code. They now have two problems to solve:
Line 102: •	 They have to reverse-engineer the code to work out that x is used to hold a surname
Line 103: •	 They have to mentally map x with the concept of surname every time that they use it
Line 104: It is so much easier when we use descriptive names for all our data, such as local variables, method 
Line 105: parameters, and object fields. In terms of more general guidelines, the following Google style guide is a 
Line 106: good source: https://google.github.io/styleguide/javaguide.html#s5-naming.
Line 107: Best practice for naming variables
Line 108: Describe the data contained, not the data type.
Line 109: We now have a better idea of how to go about naming variables. Now, let’s look at how to name 
Line 110: functions, methods, and classes properly.
Line 111: Bad function, method, and class names
Line 112: The names of functions, methods, and classes all follow a similar pattern. In good code, function 
Line 113: names tell us why we should call that function. They describe what they will do for us as users of that 
Line 114: function. The focus is on the outcome – what will have happened by the time the function returns. 
Line 115: 
Line 116: --- 페이지 30 ---
Line 117: Recognizing bad code
Line 118: 7
Line 119: We do not describe how that function is implemented. This is important. It allows us to change our 
Line 120: implementation of that function later if that becomes advantageous, and the name will still describe 
Line 121: the outcome clearly.
Line 122: A function named calculateTotalPrice is clear about what it is going to do for us. It will 
Line 123: calculate the total price. It won’t have any surprising side effects. It won’t try and do anything else. It 
Line 124: will do what it says it will. If we abbreviate that name to ctp, then it becomes much less clear. If we 
Line 125: call it func1, then it tells us absolutely nothing at all that is useful.
Line 126: Bad names force us to reverse-engineer every decision made every time we read the code. We have 
Line 127: to pore through the code to try and find out what it is used for. We should not have to do this. Names 
Line 128: should be abstractions. A good name will speed up our ability to understand code by condensing a 
Line 129: bigger-picture understanding into a few words.
Line 130: You can think of the function name as a heading. The code inside the function is the body of text. It 
Line 131: works just the same way that the text you’re reading now has a heading, Recognizing bad code, which 
Line 132: gives us a general idea of the content in the paragraphs that follow. From reading the heading, we 
Line 133: expect the paragraphs to be about recognizing bad code, nothing more and nothing less.
Line 134: We want to be able to skim-read our software through its headings – the function, method, class, and 
Line 135: variable names – so that we can focus on what we want to do now, rather than relearning what was 
Line 136: done in the past.
Line 137: Method names are treated identically to function names. They both describe an action to be taken. 
Line 138: Similarly, you can apply the same rules for function names to method names.
Line 139: Best practice for method and function names
Line 140: Describe the outcome, not the implementation.
Line 141: Again, class names follow descriptive rules. A class often represents a single concept, so its name should 
Line 142: describe that concept. If a class represents the user profile data in our system, then a class name of 
Line 143: UserProfile will help readers of our code to understand that.
Line 144: A name’s length depends on namespacing
Line 145: One further tip applies to all names with regard to their length. The name should be fully descriptive 
Line 146: but its length depends on a few factors. We can choose shorter names when one of the following applies:
Line 147: •	 The named variable has a small scope of only a few lines
Line 148: •	 The class name itself provides the bulk of the description
Line 149: •	 The name exists within some other namespace, such as a class name
Line 150: Let’s look at a code example for each case to make this clear.
Line 151: 
Line 152: --- 페이지 31 ---
Line 153: Building the Case for TDD
Line 154: 8
Line 155: The following code calculates the total of a list of values, using a short variable name, total:
Line 156: int calculateTotal(List<Integer> values) {
Line 157:     int total = 0;
Line 158:     for ( Integer v : values ) {
Line 159:         total += v;
Line 160:     }
Line 161:     return total ;
Line 162: }
Line 163: This works well because it is clear that total represents the total of all values. We do not need a 
Line 164: name that is any longer given the context around it in the code. Perhaps an even better example lies 
Line 165: in the v loop variable. It has a one-line scope, and within that scope, it is quite clear that v represents 
Line 166: the current value within the loop. We could use a longer name such as currentValue instead. 
Line 167: However, does this add any clarity? Not really.
Line 168: In the following method, we have a parameter with the short name gc:
Line 169: private void draw(GraphicsContext gc) {
Line 170:     // code using gc omitted
Line 171: }
Line 172: The reason we can choose such a short name is that the GraphicsContext class carries most of 
Line 173: the description already. If this were a more general-purpose class, such as String, for example, then 
Line 174: this short name technique would be unhelpful.
Line 175: In this final code example, we are using the short method name of draw():
Line 176: public class ProfileImage {
Line 177:     public void draw(WebResponse wr) {
Line 178:         // Code omitted
Line 179:     }
Line 180: }
Line 181: The class name here is highly descriptive. The ProfileImage class name we’ve used in our system 
Line 182: is one that is commonly used to describe the avatar or photograph that shows on a user’s profile page. 
Line 183: The draw() method is responsible for writing the image data to a WebResponse object. We could 
Line 184: choose a longer method name, such as drawProfileImage(), but that simply repeats information 
Line 185: that has already been made clear given the name of the class. Details such as this are what give Java its 
Line 186: 
Line 187: --- 페이지 32 ---
Line 188: Recognizing bad code
Line 189: 9
Line 190: reputation for being verbose, which I feel is unfair; it is often us Java programmers who are verbose, 
Line 191: rather than Java itself.
Line 192: We’ve seen how properly naming things makes our code easier to understand. Let’s take a look at 
Line 193: the next big problem that we see in bad code – using constructs that make logic errors more likely.
Line 194: Error-prone constructs
Line 195: Another tell-tale sign of bad code is that it uses error-prone constructs and designs. There are always 
Line 196: several ways of doing the same thing in code. Some of them provide more scope to introduce mistakes 
Line 197: than others. It therefore makes sense to choose ways of coding that actively avoid errors.
Line 198: Let’s compare two different versions of a function to calculate a total value and analyze where errors 
Line 199: might creep in:
Line 200:  int calculateTotal(List<Integer> values) {
Line 201:     int total = 0;
Line 202:     for ( int i=0; i<values.size(); i++) {
Line 203:         total += values.get(i);
Line 204:     }
Line 205:     return total ;
Line 206: }
Line 207: The previous listing is a simple method that will take a list of integers and return their total. It’s the 
Line 208: sort of code that has been around since Java 1.0.2. It works, yet it is error prone. In order for this code 
Line 209: to be correct, we need to get several things right:
Line 210: •	 Making sure that total is initialized to 0 and not some other value
Line 211: •	 Making sure that our i loop index is initialized to 0
Line 212: •	 Making sure that we use < and not <= or == in our loop comparison
Line 213: •	 Making sure that we increment the i loop index by exactly one
Line 214: •	 Making sure that we add the value from the current index in the list to total
Line 215: Experienced programmers do tend to get all this right first time. My point is that there is a possibility 
Line 216: of getting any or all of these things wrong. I’ve seen mistakes made where <= has been used instead 
Line 217: of < and the code fails with an ArrayIndexOutOfBounds exception as a result. Another easy 
Line 218: mistake is to use = in the line that adds to the total value instead of +=. This has the effect of returning 
Line 219: only the last value, not the total. I have even made that mistake as a pure typo – I honestly thought I 
Line 220: had typed the right thing but I was typing quickly and I hadn’t.
Line 221: 
Line 222: --- 페이지 33 ---
Line 223: Building the Case for TDD
Line 224: 10
Line 225: It is clearly much better for us to avoid these kinds of errors entirely. If an error cannot happen, then 
Line 226: it will not happen. This is a process I call designing out errors. It is a fundamental clean-code practice. 
Line 227: To see how we could do this to our previous example, let’s look at the following code:
Line 228: int calculateTotal(List<Integer> values) {
Line 229:     return values.stream().mapToInt(v -> v).sum();
Line 230: }
Line 231: This code does the same thing, yet it is inherently safer. We have no total variable, so we cannot initialize 
Line 232: that incorrectly, nor can we forget to add values to it. We have no loop and so no loop index variable. We 
Line 233: cannot use the wrong comparison for the loop end and so cannot get an ArrayIndexOutOfBounds 
Line 234: exception. There is simply far less that can go wrong in this implementation of the code. It generally 
Line 235: makes the code clearer to read as well. This, in turn, helps with onboarding new developers, code 
Line 236: reviews, adding new features, and pair programming.
Line 237: Whenever we have a choice to use code with fewer parts that could go wrong, we should choose that 
Line 238: approach. We can make life easier for ourselves and our colleagues by choosing to keep our code as 
Line 239: error-free and simple as possible. We can use more robust constructs to give bugs fewer places to hide.
Line 240: It is worth mentioning that both versions of the code have an integer overflow bug. If we add integers 
Line 241: together whose total is beyond the allowable range of -2147483648 to 2147483647, then the code will 
Line 242: produce the wrong result. The point still stands, however: the later version has fewer places where 
Line 243: things can go wrong. Structurally, it is simpler code.
Line 244: Now that we have seen how to avoid the kinds of errors that are typical of bad code, let’s turn to other 
Line 245: problem areas: coupling and cohesion.
Line 246: Coupling and cohesion
Line 247: If we have a number of Java classes, coupling describes the relationship between those classes, while 
Line 248: cohesion describes the relationships between the methods inside each one.
Line 249: Our software designs become easier to work with once we get the amounts of coupling and cohesion 
Line 250: right. We will learn techniques to help us do this in Chapter 7, Driving Design–TDD and SOLID. 
Line 251: For now, let’s understand the problems that we will face when we get this wrong, starting with the 
Line 252: problem of low cohesion.
Line 253: Low cohesion inside a class
Line 254: Low cohesion describes code that has many different ideas all lumped together in it in a single place. 
Line 255: The following UML class diagram shows an example of a class with low cohesion among its methods:
Line 256: 
Line 257: --- 페이지 34 ---
Line 258: Recognizing bad code
Line 259: 11
Line 260: Figure 1.2 – Low cohesion
Line 261: The code in this class attempts to combine too many responsibilities. They are not all obviously 
Line 262: related – we are writing to a database, sending out welcome emails, and rendering web pages. This 
Line 263: large variety of responsibilities makes our class harder to understand and harder to change. Consider 
Line 264: the different reasons we may need to change this class:
Line 265: •	 Changes to the database technology
Line 266: •	 Changes to the web view layout
Line 267: •	 Changes to the web template engine technology
Line 268: •	 Changes to the email template engine technology
Line 269: •	 Changes to the news feed generation algorithm
Line 270: There are many reasons why we would need to change the code in this class. It is always better to give 
Line 271: classes a more precise focus, so that there are fewer reasons to change them. Ideally, any given piece 
Line 272: of code should only have one reason to be changed.
Line 273: Understanding code with low cohesion is hard. We are forced to understand many different ideas 
Line 274: at once. Internally, the code is very interconnected. Changing one method often forces a change in 
Line 275: others because of this. Using the class is difficult, as we need to construct it with all its dependencies. 
Line 276: In our example, we have a mixture of templating engines, a database, and code for creating a web page. 
Line 277: This also makes the class very difficult to test. We need to set up all these things before we can run 
Line 278: test methods against that class. Reuse is limited with a class like this. The class is very tightly bound 
Line 279: to the mix of features that are rolled into it.
Line 280: 
Line 281: --- 페이지 35 ---
Line 282: Building the Case for TDD
Line 283: 12
Line 284: High coupling between classes
Line 285: High coupling describes where one class needs to connect to several others before it can be used. 
Line 286: This makes it difficult to use in isolation. We need those supporting classes to be set up and working 
Line 287: correctly before we can use our class. For the same reason, we cannot fully understand that class 
Line 288: without understanding the many interactions it has. As an example, the following UML class diagram 
Line 289: shows classes with a high degree of coupling between each other:
Line 290: Figure 1.3 – High coupling
Line 291: In this fictitious example of a sales tracking system, several of the classes need to interact with each 
Line 292: other. The User class in the middle couples to four other classes: Inventory, EmailService, 
Line 293: SalesAppointment, and SalesReport. This makes it harder to use and test than a class that 
Line 294: couples to fewer other classes. Is the coupling here too high? Maybe not, but we can imagine other 
Line 295: designs that would reduce it. The main thing is to be aware of the degree of coupling that classes have 
Line 296: in our designs. As soon as we spot classes with many connections to others, we know we are going to 
Line 297: have a problem understanding, maintaining, and testing them.
Line 298: We’ve seen how the technical elements of high coupling and low cohesion make our code difficult to 
Line 299: work with, but there is a social aspect to bad code as well. Let’s consider the effect bad code has on 
Line 300: the development team.
Line 301: Decreasing team performance
Line 302: A good way to look at bad code is code lacking the technical practices that help other developers 
Line 303: understand what it is doing.
Line 304: 
Line 305: --- 페이지 36 ---
Line 306: Decreasing team performance
Line 307: 13
Line 308: When you’re coding solo, it doesn’t matter so much. Bad code will just slow you down and feel a little 
Line 309: demoralizing at times. It does not affect anybody else. However, most professionals code in development 
Line 310: teams, which is a whole different ball game. Bad code really slows a team down.
Line 311: The following two studies are interesting as far as this is concerned:
Line 312: •	 https://dl.acm.org/doi/abs/10.1145/3194164.3194178
Line 313: •	 https://www.sciencedirect.com/science/article/abs/pii/
Line 314: S0164121219301335
Line 315: The first study shows that developers waste up to 23% of their time on bad code. The second study 
Line 316: shows that in 25% of cases of working with bad code, developers are forced to increase the amount 
Line 317: of bad code still further. In these two studies, the term technical debt is used, rather than referring 
Line 318: to bad code. There is a difference in intention between the two terms. Technical debt is code that is 
Line 319: shipped with known technical deficiencies in order to meet a deadline. It is tracked and managed 
Line 320: with the intention that it will later be replaced. Bad code might have the same defects, but it lacks the 
Line 321: redeeming quality of intentionality.
Line 322: It is all too easy to check in code that has been easy to write but will be hard to read. When I do that, 
Line 323: I have effectively placed a tax on the team. The next developer to pull my changes will have to figure 
Line 324: out what on earth they need to do and my bad code will have made that much harder.
Line 325: We’ve all been there. We start a piece of work, download the latest code, and then just stare at our screens 
Line 326: for ages. We see variable names that make no sense, mixed up with tangled code that really does not 
Line 327: explain itself very well at all. It’s frustrating for us personally, but it has a real cost in a programming 
Line 328: business. Every minute we spend not understanding code is a minute where money is being spent on 
Line 329: us achieving nothing. It’s not what we dreamed of when we signed up to be a developer.
Line 330: Bad code disrupts every future developer who has to read the code, even us, the original authors. We 
Line 331: forget what we previously meant. Bad code means more time spent by developers fixing mistakes, 
Line 332: instead of adding value. It means more time is lost on fixing bugs in production that should have 
Line 333: been easily preventable.
Line 334: Worse still, this problem compounds. It is like interest on a bank loan. If we leave bad code in place, 
Line 335: the next feature will involve adding workarounds for the bad code. You may see extra conditionals 
Line 336: appear, giving the code yet more execution paths and creating more places for bugs to hide. Future 
Line 337: features build on top of the original bad code and all of its workarounds. It creates code where most 
Line 338: of what we read is simply working around what never worked well in the first place.
Line 339: Code of this kind drains the motivation out of developers. The team starts spending more time 
Line 340: working around problems than they spend adding value to the code. None of this is fun for the typical 
Line 341: developer. It’s not fun for anybody on the team.
Line 342: Project managers lose track of the project status. Stakeholders lose confidence in the team’s ability to 
Line 343: deliver. Costs overrun. Deadlines slip. Features get quietly cut, just to claw back a little slack in the 
Line 344: 
Line 345: --- 페이지 37 ---
Line 346: Building the Case for TDD
Line 347: 14
Line 348: schedule. Onboarding new developers becomes painful, to the point of awkwardness, whenever they 
Line 349: see the awful code.
Line 350: Bad code leaves the whole team unable to perform to the level they are capable of. This, in turn, does 
Line 351: not make for a happy development team. Beyond unhappy developers, it also negatively impacts 
Line 352: business outcomes. Let’s understand those consequences.
Line 353: Diminishing business outcomes
Line 354: It’s not just the development team who suffers from the effects of bad code. It’s bad for the entire business.
Line 355: Our poor users end up paying for software that doesn’t work, or at least that doesn’t work properly. There 
Line 356: are many ways that bad code can mess up a user’s day, whether as a result of lost data, unresponsive 
Line 357: user interfaces, or any kind of intermittent fault. Each one of these can be caused by something as 
Line 358: trivial as setting a variable at the wrong time or an off-by-one error in a conditional somewhere.
Line 359: The users see neither any of that nor the thousands of lines of code that we got right. They just see 
Line 360: their missed payment, their lost document that took 2 hours to type, or that fantastic last-chance ticket 
Line 361: deal that simply never happened. Users have little patience for things like this. Defects of this kind 
Line 362: can easily lose us a valuable customer.
Line 363: If we are lucky, users will fill out a bug report. If we are really lucky, they will let us know what they 
Line 364: were doing at the time and provide us with the right steps to reproduce the fault. But most users will 
Line 365: just hit delete on our app. They’ll cancel future subscriptions and ask for refunds. They’ll go to review 
Line 366: sites and let the world know just how useless our app and company are.
Line 367: At this point, it isn’t merely bad code; it is a commercial liability. The failures and honest human errors 
Line 368: in our code base are long forgotten. Instead, we were just a competitor business that came and went 
Line 369: in a blaze of negativity.
Line 370: Decreased revenue leads to decreased market share, a reduced Net Promoter Score®™ (NPS), 
Line 371: disappointed shareholders, and all the other things that make your C-suite lose sleep at night. Our 
Line 372: bad code has become a problem at the business level.
Line 373: This isn’t hypothetical. There have been several incidents where software failures have cost the business. 
Line 374: Security breaches for Equifax, Target, and even the Ashley Madison site all resulted in losses. The 
Line 375: Ariane rocket resulted in the loss of both spacecraft and satellite payload, a total cost of billions of 
Line 376: dollars! Even minor incidents resulting in downtime for e-commerce systems can soon have costs 
Line 377: mounting, while consumer trust crashes down.
Line 378: In each case, the failures may have been small errors in comparatively few lines of code. Certainly, they 
Line 379: will have been avoidable in some way. We know that humans make mistakes, and that all software is 
Line 380: built by humans, yet a little extra help may have been all it would have taken to stop these disasters 
Line 381: from unfolding.
Line 382: The advantage of finding failures early is shown in the following diagram:
Line 383: 
Line 384: --- 페이지 38 ---
Line 385: Diminishing business outcomes
Line 386: 15
Line 387: Figure 1.4 – Costs of defect discovery
Line 388: In the previous figure, the cost of the repair of a defect gets higher the later it is found:
Line 389: •	 Found by a failing test before code:
Line 390: The cheapest and fastest way to discover a defect is by writing a test for a feature before we 
Line 391: write the production code. If we write the production code that we expect should make the 
Line 392: test pass, but instead the test fails, we know there is a problem in our code.
Line 393: •	 Found by a failing test after code:
Line 394: If we write the production code for a feature, and then write a test afterward, we may find 
Line 395: defects in our production code. This happens a little later in the development cycle. We will 
Line 396: have wasted a little more time before discovering the defect.
Line 397: •	 Found during manual QA:
Line 398: Many teams include Quality Assurance (QA) engineers. After code has been written by a 
Line 399: developer, the QA engineer will manually test the code. If a defect is found here, this means 
Line 400: significant time has passed since the developer first wrote the code. Rework will have to be done.
Line 401: •	 Found by the end user once code is in production:
Line 402: This is as bad as it gets. The code has been shipped to production and end users are using it. 
Line 403: An end user finds a bug. The bug has to be reported, triaged, a fix scheduled for development, 
Line 404: then retested by QA then redeployed to production. This is the slowest and most expensive 
Line 405: path to discovering a defect.
Line 406: 
Line 407: --- 페이지 39 ---
Line 408: Building the Case for TDD
Line 409: 16
Line 410: The earlier we find the fault, the less time and money we will have to spend on correcting it. The ideal 
Line 411: is to have a failing test before we even write a line of code. This approach also helps us design our 
Line 412: code. The later we leave it to find a mistake, the more trouble it causes for everyone.
Line 413: We’ve seen how low-quality code gives rise to defects and is bad for business. The earlier we detect 
Line 414: failures, the better it is for us. Leaving defects in production code is both difficult and expensive to 
Line 415: fix, and negatively affects our business reputation.
Line 416: Summary
Line 417: We can now recognize bad code from its technical signs and appreciate the problems that it causes 
Line 418: for both development teams and business outcomes.
Line 419: What we need is a technique to help us avoid these problems. In the next chapter, we’ll take a look at 
Line 420: how TDD helps us deliver clean, correct code that is a true business asset.
Line 421: Questions and answers
Line 422: 1.	
Line 423: Isn’t it enough to have working code?
Line 424: Sadly not. Code that meets user needs is an entry-level step with professional software. We also 
Line 425: need code that we know works, and that the team can easily understand and modify.
Line 426: 2.	
Line 427: Users don’t see the code. Why does it matter to them?
Line 428: This is true. However, users expect things to work reliably, and they expect our software to 
Line 429: be updated and improved continuously. This is only possible when the developers can work 
Line 430: safely with the existing code.
Line 431: 3.	
Line 432: Is it easier to write good code or bad code?
Line 433: It is much harder to write good code, unfortunately. Good code does more than simply work 
Line 434: correctly. It must also be easy to read, easy to change, and safe for our colleagues to work with. 
Line 435: That’s why techniques such as TDD have an important role to play. We need all the help we 
Line 436: can get to write clean code that helps our colleagues.
Line 437: Further reading
Line 438: •	 More about the loss of the Ariane rocket: https://www.esa.int/Newsroom/Press_
Line 439: Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report