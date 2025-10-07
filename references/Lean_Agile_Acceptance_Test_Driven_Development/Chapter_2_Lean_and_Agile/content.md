Line 1: 
Line 2: --- 페이지 38 ---
Line 3: Chapter 2 
Line 4: Lean and Agile 
Line 5: “You’re a lean, mean, ﬁghting machine!”
Line 6: Bill Murray as John Winger in Stripes
Line 7: The triad of Cathy the customer, Debbie the developer, and Tom the tester 
Line 8: has its ﬁrst meeting. Debbie describes the differences between traditional devel-
Line 9: opment and acceptance test-driven development (ATDD). It’s explained how 
Line 10: ATDD ﬁts into lean and agile. 
Line 11: The Triad and Its Units 
Line 12:  
Line 13: Many books on agility refer to the developer team and the business team. Names 
Line 14: often have a connotation. On a football ﬁeld, two teams compete to see who can 
Line 15: score more points and win the game. On a single football team, there is an of-
Line 16: fensive unit, a defensive unit, and a special teams unit. The offensive’s unit job is 
Line 17: to score points. The defensive’s unit responsibility is to keep the other team from 
Line 18: scoring. The special team unit has the goal of scoring points when it receives a 
Line 19: kicked ball and preventing the other team from scoring when it kicks the ball. 
Line 20: All three units must do their job to win the game. 
Line 21: Although each unit has a primary job, it doesn’t stop there. If the offensive 
Line 22: unit fumbles the football and the other team recovers, it does not simply stop 
Line 23: playing and call for the defensive unit to come on the ﬁeld. Instead, it plays 
Line 24: defense until the end of the play. 
Line 25: 15
Line 26: 
Line 27: --- 페이지 39 ---
Line 28: Chapter 2 Lean and Agile
Line 29: 16
Line 30: The three basic units in a software project are the customer unit, the devel-
Line 31: oper unit, and the testing unit. 1 The customer unit (which may include product 
Line 32: owner, business analysts, and subject matter experts) determines the require-
Line 33: ments, creates acceptance tests, and sets priorities. The developer unit imple-
Line 34: ments the requirements and ensures the implementation meets the acceptance 
Line 35: tests. The testing unit checks that an implementation does what it is supposed to 
Line 36: do and does not do what it is not supposed to do. The testers help the customer 
Line 37: unit develop acceptance tests, and the developer unit passes those tests. The 
Line 38: triad works together to produce quality software. 2
Line 39: We start the story with Debbie, representing the developer unit, explaining 
Line 40: to Cathy, the customer unit, two ways that teams approach software develop-
Line 41: ment. Tom, the testing unit, is sitting in the meeting of the triad (see Figure 2.1).
Line 42: Cathy
Line 43: the
Line 44: Customer
Line 45: Tom
Line 46: the
Line 47: Tester
Line 48: Debbie
Line 49: the
Line 50: Developer
Line 51: Figure 2.1 The Triad 
Line 52: 2. There are other players, such as the stakeholder who owns the charter (see Chapter 
Line 53: 5, “The Example Project”) and the users who use the system. Their roles will be 
Line 54: introduced at appropriate times. 
Line 55: 1. As suggested in the previous chapter, some agile teams work more like a soccer team 
Line 56: or a basketball team. Players have particular strengths, but everyone plays both 
Line 57: defense and offense. The testing unit consists of players currently acting one way—
Line 58: focused on testing—but the same players may be part of the developer unit that acts 
Line 59: another way—focused on implementation. 
Line 60: 
Line 61: --- 페이지 40 ---
Line 62: Post-Implementation Tests 
Line 63: 17
Line 64: Post-Implementation Tests 
Line 65: Debbie and Tom meet with Cathy to explain how the development process 
Line 66: works. Debbie begins with how the ﬂow often works and compares it to how 
Line 67: Debbie and Tom prefer to work. 
Line 68: Debbie introduces the chart shown in Figure 2.2.
Line 69: “Cathy, this is how many development teams work to implement a require-
Line 70: ment.3 As a developer, I elicit a requirement from the customer. Then I gather 
Line 71: detail on the requirement, followed by designing and coding an implementation. 
Line 72: I turn over the program to a tester like Tom. He develops functional tests to 
Line 73: check that the requirement passes. He works with the customer or his repre-
Line 74: sentative to create and run some acceptance tests.” 
Line 75: “If the functional tests pass, as well as other tests, such as performance and 
Line 76: usability, the system is ready to be deployed. Now if everything is perfect, the 
Line 77: program passes through these stages in a straight line. But perfection only occurs 
Line 78: in fairy tales. In reality, there are often misunderstandings. We don’t always use 
Line 79: the same words with the same meaning. You may say always when you really 
Line 80: mean usually. Or I may hear usually and think it means always.”
Line 81: “Now when a misunderstanding is found, it needs to be corrected. If Tom 
Line 82: ﬁnds that misunderstanding during testing, we have to ﬁgure out how to correct 
Line 83: it. It could be that I simply made a mistake in coding. So you see a loopback 
Line 84: shown by the line from test back to code in Figure 2.2. Tom tells me about the 
Line 85: issue he discovered, and I correct it.” 
Line 86: “It could be a misunderstanding that occurred while gathering details of a 
Line 87: requirement. In that case, Tom and I would revisit the requirement. He might 
Line 88: have interpreted one way and I might have interpreted another. We would check 
Line 89: back with you to see which one of our interpretations was correct or whether 
Line 90: you meant something else entirely different.” 
Line 91:   3 . Particularly any team that does not use some form of test-driven development 
Line 92: (TDD).
Line 93: Gather
Line 94: details,
Line 95: design,
Line 96: code
Line 97: Develop
Line 98: acceptance
Line 99: tests and
Line 100: execute
Line 101: Elicit a
Line 102: requirement
Line 103: Figure 2.2 Typical Development Flow 
Line 104: 
Line 105: --- 페이지 41 ---
Line 106: Chapter 2 Lean and Agile
Line 107: 18
Line 108: “This cycling back causes a delay in deploying the product, as well as extra 
Line 109: cost in creating the product. So Tom and I like to operate in a different mode 
Line 110: that uses quick feedback.” 
Line 111: Quick Feedback Better Than Slow Feedback 
Line 112: Before describing Debbie and Tom’s alternative process, let’s look at the idea 
Line 113: of feedback. Feedback involves using current output to inﬂuence future output. 
Line 114: Feedback in software development is not quite the same as feedback in control 
Line 115: systems. In control systems, values from the output are fed back into the input 
Line 116: to regulate the output. In audio systems, the output sound from the speakers can 
Line 117: accidentally get back into the input to the microphone. That positive feedback 
Line 118: can cause an explosive sound to emit from the speakers. Instead, think of soft-
Line 119: ware feedback as a listener commenting that the sound from your stereo speak-
Line 120: ers is not the desired level. You adjust the ampliﬁer volume to make the sound 
Line 121: closer to what the listener likes. 
Line 122: Imagine you want to show off your new stereo to someone. You turn it on, 
Line 123: but the listener says he cannot hear the music very well. You constantly increase 
Line 124: the volume. If the listener gives you frequent feedback, you’ll stop the increase 
Line 125: just after you’ve increased past where he wanted it to be. So the volume will be 
Line 126: pretty close to what he wants. You may home in even further by reducing the 
Line 127: volume more slowly. If the listener does not give you frequent feedback, you will 
Line 128: increase the volume well above what he wants and then decrease it well below. 
Line 129: You will continually cycle between too loud and too quiet. 
Line 130: Quick Feedback on Mileage 
Line 131: Quick feedback promotes different behavior. Energy-efﬁcient cars, such 
Line 132: as the Toyota Prius and the Honda Insight, have instantaneous mileage 
Line 133: displays. When you drive one of these cars, you ﬁnd out quickly which ac-
Line 134: tions decrease or increase mileage. For example, rapid acceleration shows 
Line 135: up as really low mileage. Trying to beat the car next to you when the light 
Line 136: turns green quickly indicates that you have used a lot of gas. Drivers of 
Line 137: cars without mileage displays sometimes check their mileage every time 
Line 138: they ﬁll up the tank. But then it is hard to determine what actions during 
Line 139: the previous tank-full caused either good or bad mileage. All that you can 
Line 140: ascertain is that something during that period caused the mileage to vary. 
Line 141: Quick feedback means less delay. Quick feedback is good. The output will be 
Line 142: closer to the desired outcome. 
Line 143: 
Line 144: --- 페이지 42 ---
Line 145: Preimplementation Tests 
Line 146: 19
Line 147: Preimplementation Tests 
Line 148: “So how are things going to be different working with you?,” Cathy asks. 
Line 149: Debbie starts to describe another process. She shows Cathy the chart in Fig-
Line 150: ure 2.3.
Line 151: “Here’s the process that Tom and I use. After we elicit a requirement from 
Line 152: you, Cathy, we work together to create some acceptance tests for the require-
Line 153: ment. These are speciﬁc examples of the requirement in action. When I’m cod-
Line 154: ing, I’ll use these tests to ensure that my implementation meets the tests. When it 
Line 155: does, I’ll turn it over to Tom for the other types of tests that are discussed later 
Line 156: [in the next chapter].” 
Line 157: Tom chimes in. “This is a small application relative to some we’ve worked 
Line 158: on in the past. Debbie’s machine will be almost an exact duplicate of your com-
Line 159: puter where the application will be deployed. So when she turns the application 
Line 160: over to me and I run it on the test system that exactly matches your computer, I 
Line 161: don’t expect any acceptance tests that we’ve created to fail.” 
Line 162: “What this means,” Debbie continues, “is that the three of us will be creat-
Line 163: ing these tests together to make sure that we all have a clear understanding of 
Line 164: what a requirement means. When a requirement is delivered, it will work as 
Line 165: understood.”
Line 166: “I really don’t know anything about testing,” Cathy states. “So how will I 
Line 167: help?”
Line 168: Debbie replies, “The test creation starts with getting examples from you on 
Line 169: how a requirement should work. Tom and I can take these examples and turn 
Line 170: them into the actual tests.” 
Line 171: “We will not be doing this up front for all the requirements. As you decide 
Line 172: what the next requirement to work on is, we’ll get together and work on the 
Line 173: details. I know you have to work at the store and there is no room for us to set 
Line 174: up our computers there. But because we’re only a couple of miles away and 
Line 175: there is a great bike path between our places, we’ll ride over for these meetings. 
Line 176: We’ve found that meeting face to face is much more effective than having a long 
Line 177: conference call on the phone” [Cockburn01]. 
Line 178: Gather
Line 179: details by
Line 180: developing
Line 181: acceptance
Line 182: tests
Line 183: Elicit a
Line 184: requirement
Line 185: Design,
Line 186: code, and
Line 187: execute
Line 188: acceptance
Line 189: tests
Line 190: Figure 2.3 ATDD Flow 
Line 191: 
Line 192: --- 페이지 43 ---
Line 193: Chapter 2 Lean and Agile
Line 194: 20
Line 195: Cathy interjects, “I’m not always available. I have a lot of other work that 
Line 196: Sam needs me to do.” 
Line 197: Debbie answers, “I understand. We’ll schedule the face-to-face meetings at 
Line 198: your convenience. For things that are pretty standard in software, such as add-
Line 199: ing an item, Tom and I will make up the examples for the tests and then review 
Line 200: them with you before I start implementing. If it’s a quick question, we’ll give you 
Line 201: a call. The only thing we ask is that you get back to us relatively soon. We can 
Line 202: often work on other pieces of the problem, but if the question regards something 
Line 203: that is fundamental to the design, we’ll need a quick answer. And we’ll identify 
Line 204: the difference between that which we need as soon as possible and that which 
Line 205: can wait a little while. Of course, if the little while turns into a day or a week, 
Line 206: your project will be delayed and there will be more costs.” 
Line 207: Lean and Agile Principles 
Line 208: ATDD is based on some lean principles and some agile principles. The lean 
Line 209: principles come from Mary and Tom Poppendieck [Poppendieck02], [Pop-
Line 210: pendieck03], [Poppendieck04]. 4 The agile principles are listed in “The Agile 
Line 211: Manifesto,” which is a widely recognized statement on how to better develop 
Line 212: software [Agile01]. 
Line 213: The Poppendiecks developed principles of lean software development derived 
Line 214: from lean manufacturing. One principle is to reduce waste in a process. Creating 
Line 215: acceptance tests up front reduces waste by decreasing the loopbacks from testing 
Line 216: back to coding. 
Line 217: Another principle is to build in integrity. Acceptance tests for each portion of 
Line 218: the system help to ensure that the modules are high quality. The tests are run as 
Line 219: each module is developed, not when the developers have completed the entire 
Line 220: system.
Line 221: The collaboration between the members of the triad helps amplify learning, 
Line 222: which is another lean principle. The members learn from each other about the 
Line 223: business domain and the development and testing issues. 
Line 224: The triad is one manifestation of the Agile Manifesto principle that “busi-
Line 225: ness people and developers must work together daily throughout the project.” 
Line 226: Although they may not be physically together, they will be working together 
Line 227: continuously.
Line 228: Another agile principle is that “working software is the primary measure 
Line 229: of progress.” With the acceptance tests, Debbie and Tom can deliver not only 
Line 230:   4 . See [Shalloway01] and [Larman01] for another explanation of lean principles. 
Line 231: 
Line 232: --- 페이지 44 ---
Line 233: Summary 
Line 234: 21
Line 235: working software, but software that delivers more precisely what Cathy is ask-
Line 236: ing for. 
Line 237: Summary
Line 238: • The triad consists of the three units—customer, developer, and tester—
Line 239: that collaborate to create high-quality software. 
Line 240: • Quick feedback is better than slow feedback.ATDD reduces unnecessary 
Line 241: loopbacks.
Line 242: • ATDD is lean and agile. 
Line 243: 
Line 244: --- 페이지 45 ---
Line 245: This page intentionally left blank 