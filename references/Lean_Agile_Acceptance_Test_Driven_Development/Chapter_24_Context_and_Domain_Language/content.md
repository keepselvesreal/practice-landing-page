Line 1: 
Line 2: --- 페이지 228 ---
Line 3: Chapter 24 
Line 4: Context and Domain 
Line 5: Language
Line 6: “England and America are two countries separated by a common 
Line 7: language.”
Line 8: George Bernard Shaw 
Line 9: Communication requires a common language. During the collaboration in the 
Line 10: creation of acceptance tests, a common language emerges. 
Line 11: Ubiquitous Language 
Line 12: Domain-driven design (DDD) [Evans01], refers to the ubiquitous language. The 
Line 13: ubiquitous language involves the terms in which the customer and developers 
Line 14: talk about a system. The language arises from explanations given by a customer 
Line 15: or subject matter expert about the entities and processes in a system. The ubiq-
Line 16: uitous language transforms itself and becomes more reﬁned as developers and 
Line 17: customers discover ambiguities and unclearness. 
Line 18: The language evolves during the collaboration on the requirements and the 
Line 19: tests, as shown in Chapter 6, “The User Story Technique.” Contributions to the 
Line 20: language come from the column names in tables, the names of use cases and 
Line 21: their exceptions, and the business rules. Each term in the language should be 
Line 22: documented with a one-sentence description that the customer unit provides 
Line 23: and the developer and tester units understand. The customer unit leads the 
Line 24: terminology effort, but the developer unit can suggest that terms are unclear, 
Line 25: ambiguous, or redundant. 
Line 26: For example, the triad referred to entities as customer, CD, rental, and album. 
Line 27: They could be deﬁned with single sentences as: 
Line 28: 205
Line 29: 
Line 30: --- 페이지 229 ---
Line 31: Chapter 24 Context and Domain Language
Line 32: 206
Line 33: • A customer is someone to whom we rent CDs. 
Line 34: • An album is an artist’s release. 
Line 35: • A CD is a physical copy of an album that is rented. 
Line 36: • A rental contains the information on a CD that is rented. 
Line 37: You can use tables in deﬁning the terms. For example, the discount example 
Line 38: in Chapter 4, “An Introductory Acceptance Test,” referred to the terms Cus-
Line 39: tomer Type and Item Total. The Customer Type can be deﬁned by a table, such 
Line 40: as this. 
Line 41: Customer Type 
Line 42: Name 
Line 43: Meaning
Line 44: Regular 
Line 45: A common customer 
Line 46: Good 
Line 47: One we want to keep 
Line 48: Excellent 
Line 49: One we will cater to his every whim 
Line 50: Order Total might be part of a larger picture table. You might show relation-
Line 51: ships to other entities if that clariﬁes the picture. 
Line 52: Order Fields 
Line 53: Name 
Line 54: Meaning 
Line 55: Formula
Line 56: Item Price 
Line 57: What we charge for the item 
Line 58: Order Item 
Line 59: Item on an order 
Line 60: Item Quantity 
Line 61: Count of how many of an item is 
Line 62: ordered
Line 63: Item Total 
Line 64: Total price for a single item 
Line 65: Item Price * Item Quantity 
Line 66: Order Total 
Line 67: Total price for all items on an order 
Line 68: Sum of all Item Totals 
Line 69: The triad should agree not only on the meanings of the entities, but their 
Line 70: identity and  continuity. Identity is whether two entities are the same. For exam-
Line 71: ple, if a rental contract is reprinted, it represents the same entity as the ﬁrst 
Line 72: printout. However, a credit charge that is resubmitted may be construed as a 
Line 73: new charge, and the customer will get double-billed. If a customer checked in 
Line 74: two CDs within a short period, two legitimate charges could look the same. The 
Line 75: credit processor might interpret that as a duplicate billing and reject the second. 
Line 76: 
Line 77: --- 페이지 230 ---
Line 78: Two Domains 
Line 79: 207
Line 80: Continuity is how long an entity should persist. If a store customer wants 
Line 81: rental history to be completely private, a rental entity should persist only until 
Line 82: it is complete (that is, until the customer has checked-in the CD). On the other 
Line 83: hand, if Sam wants the rental history to determine favorite CDs for a customer so 
Line 84: he can offer him new releases in that same genre, the rental should be persistent. 
Line 85: Two Domains 
Line 86: The applicability of a ubiquitous language could be the entire enterprise. But of-
Line 87: ten, that is too big a context, so it’s just for the portion of the enterprise. (DDD 
Line 88: refers to this as the bounded context.) So each portion of the enterprise has its 
Line 89: own domain. Two domains may overlap if they use common resources. 
Line 90: Figure 24.1 is an example of overlapping domains. Both Check-Out/In System 
Line 91: and the Accounting System use a common domain—Rental Fees and Charges. 
Line 92: This requires that for the two domains, the customers agree on a shared lan-
Line 93: guage for the interface to the common one. 1
Line 94: Test Doubles 
Line 95: for Rental Fees 
Line 96: and Charges
Line 97: Output
Line 98: Rental
Line 99: Fees and
Line 100: Charges
Line 101: Acceptance
Line 102: Tests
Line 103: Accounting
Line 104: System
Line 105: Check
Line 106: Out/In
Line 107: System
Line 108: Input
Line 109: Input
Line 110: Figure 24.1 A Common Domain—One-Way Interface 
Line 111: The existence of a common domain impacts the acceptance tests. In Figure
Line 112: 24.1, the interface between Check-Out/In and Rental Fees and Charges is one-
Line 113: way (output only). The acceptance tests ensure that the proper data is being 
Line 114: created. The interface between Rental Fees and Charges and the Accounting 
Line 115: System is one way (input only). The test doubles allow the Accounting System 
Line 116: to be tested separate from the Check-Out/In system. 
Line 117:   1.  It would be ideal if the terminology of both domains matched so that developers and 
Line 118: testers did not have to switch meanings when working on the other domain. But the 
Line 119: coordination effort required may not be worth it. 
Line 120: 
Line 121: --- 페이지 231 ---
Line 122: Chapter 24 Context and Domain Language
Line 123: 208
Line 124: Summary
Line 125: • From collaboration on acceptance tests, a ubiquitous language emerges. 
Line 126: • Tests should be written using the ubiquitous language. 
Line 127: • Multiple systems using a common system need to agree on a ubiquitous 
Line 128: language for that common system. 
Line 129:  
Line 130: What Is a Flight? 
Line 131: An airline system is really large. There are reservation systems, ground 
Line 132: operations systems, and ﬂight operations, to name a few. The term  ﬂight
Line 133: is pretty common. Consider how you, the customer, think of a ﬂight. You 
Line 134: are going to catch a ﬂight. Do you use the same reference whether your 
Line 135: journey is going to be on a single plane or whether you have to transfer 
Line 136: between planes? 
Line 137: The airplane you board is for a particular ﬂight, identiﬁed by the ﬂight 
Line 138: number. A particular ﬂight number can represent the same airplane 
Line 139: traveling to many cities, only one of which you are interested in going 
Line 140: to. For example, Flight 1000 may go to Boston, then Philadelphia, then 
Line 141: Raleigh-Durham, then Atlanta. However, you may only be interested in 
Line 142: the Boston to Philadelphia portion. 
Line 143: As an example of continuity, the association between the airplane entity 
Line 144: and the ﬂight entity is not persistent. You may ﬂy on the same ﬂight 
Line 145: number multiple times and get a different airplane. 
Line 146: Each part of an airline system may use the term ﬂight in its own domain 
Line 147: context. For some parts, a ﬂight represents the entire travel of a physical 
Line 148: airplane through its entire day. For others, it represents the route of an 
Line 149: entity identiﬁed by a ﬂight number, regardless of what physical airplane 
Line 150: is ﬂying it. 
Line 151: To keep some degree of commonality, there is an agreed-upon term for 
Line 152: the portion between a single takeoff and the subsequent landing: a leg.
Line 153: When airline systems communicate with each other, they can communi-
Line 154: cate about this common entity. For example, a leg is Flight 100 from Bos-
Line 155: ton to Philadelphia. 