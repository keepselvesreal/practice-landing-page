Line 1: 
Line 2: --- 페이지 106 ---
Line 3: 12. Deciding on an Architecture Style
Line 4: So far, this book has provided an opinionated approach of building a web application in a hexagonal
Line 5: architecture style. From organizing code to taking shortcuts, we have answered many questions that
Line 6: this architecture style confronts us with.
Line 7: Some of the answers in this book can be applied to the conventional layered architecture style. Some
Line 8: answers can only be implemented in a domain-centric approach like the one proposed in this book.
Line 9: And some answers you might not even agree with, because they don’t work in your experience.
Line 10: The final questions we want answers for, however, are these: When should we actually use the
Line 11: hexagonal architecture style? And when should we rather stick with the conventional layered style
Line 12: (or any other style for that matter)?
Line 13: The Domain is King
Line 14: It should have become obvious in the previous chapters that the main feature of a hexagonal
Line 15: architecture style is that we can develop the domain code free from diversions such as persistence
Line 16: concerns and dependencies to external systems.
Line 17: Evolving domain code free from external influence is the single most important argument
Line 18: for the hexagonal architecture style.
Line 19: This is why this architecture style is such a good match for DDD practices. To state the obvious,
Line 20: in DDD the domain drives the development. And we can best reason about the domain if we don’t
Line 21: have to think about persistence concerns and other technical aspects at the same time.
Line 22: I would even go so far as to say that domain-centric architecture styles like the hexagonal style are
Line 23: enablers of DDD. Without an architecture that puts the domain into the center of things, without
Line 24: inverting the dependencies towards the domain code, we have no chance of really doing Domain-
Line 25: Driven Design. The design will always be driven by other factors.
Line 26: So, as a first indicator of whether to use the architecture style presented in this book or not: if the
Line 27: domain code is not the most important thing in your application, you probably don’t need this
Line 28: architecture style.
Line 29: Experience is Queen
Line 30: We’re creatures of habit. Habits automate decisions for us so we don’t have to spend time on them.
Line 31: If there’s a lion running towards us, we run. If we build a new web application, we use the layered
Line 32: architecture style. We have done it so often in the past that it has become a habit.
Line 33: 
Line 34: --- 페이지 107 ---
Line 35: 12. Deciding on an Architecture Style
Line 36: 101
Line 37: I’m not saying that this is necessarily a bad decision. Habits are just as good in helping to make a
Line 38: right decision as they are in making a bad one. I’m saying that we’re doing what we’re experienced
Line 39: in. We’re comfortable with what we’ve done in the past, so why should we change anything?
Line 40: So, the only way to make an educated decision about an architecture style is by having experience
Line 41: in different architecture styles. If you’re unsure about the hexagonal architecture style, try it out
Line 42: on a small module of the application that you’re currently building. Get used to the concepts. Get
Line 43: comfortable. Apply the ideas in this book, modify them, and add your own ideas to develop a style
Line 44: you’re comfortable with.
Line 45: This experience can then guide your next architecture decision.
Line 46: It Depends
Line 47: I would love to provide a list of multiple-choice questions to decide on an architecture style just
Line 48: like all those “Which Personality Type Are You?” and “What Kind of Dog Are You?” tests that are
Line 49: regularly swirling around in the social media³⁴.
Line 50: But it isn’t as easy as that. My answer to the question which architecture style to choose remains
Line 51: the professional consultant’s “It depends…”. It depends on the type of software to be built. It depends
Line 52: on the role of the domain code. It depends on the experience of the team. And finally, it depends on
Line 53: being comfortable with a decision.
Line 54: I hope, however, that this book has provided some sparks to help with the architecture question.
Line 55: If you have a story to tell about architecture decisions, with or without hexagonal architecture, I’d
Line 56: love to hear about it³⁵.
Line 57: ³⁴I’m the “Defender” personality type and if I were a dog, I would apparently be a Pit Bull.
Line 58: ³⁵You can drop me an email at tom@reflectoring.io.