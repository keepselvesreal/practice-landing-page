Line 1: 
Line 2: --- 페이지 184 ---
Line 3: Chapter 18 
Line 4: Entities and Relationships 
Line 5: “The pure and simple truth is rarely pure and never simple.”
Line 6: Oscar Wilde 
Line 7: This chapter presents a more complex system and introduces a model diagram 
Line 8: and its representation in tables. 
Line 9: Relationships
Line 10: Sam’s system started off with a simple setup—a Customer table and a CD table. 
Line 11: The CD table had an entry for each physical CD. This corresponded to Sam’s 
Line 12: paper system, in which each CD had a separate index card that recorded its be-
Line 13: ing rented. The table looked like this. 
Line 14: CD Data 
Line 15: ID 
Line 16: Title 
Line 17: CD Category 
Line 18: Rented 
Line 19: Customer ID 
Line 20: Rental Due 
Line 21: CD3 
Line 22: Janet Jackson 
Line 23: Number Ones 
Line 24: Regular 
Line 25: Yes 
Line 26: 007 
Line 27: 1/23/2011
Line 28: CD7 
Line 29: Janet Jackson 
Line 30: Number Ones 
Line 31: Regular 
Line 32: No
Line 33: Entities and Relationships 
Line 34: A system is often more complex than Sam’s example. There are more entities 
Line 35: than just a CD, and there are relationships between these entities. The business 
Line 36: is the source of the information. Any diagrams, models, and tables are based on 
Line 37: the business’s understanding of the entities, not an underlying implementation. 
Line 38: 161
Line 39: 
Line 40: --- 페이지 185 ---
Line 41:  
Line 42: Chapter 18 Entities and Relationships
Line 43: 162
Line 44: For Sam’s application, there are CDs that are physical copies of an album. If 
Line 45: Cathy describes the system with these two concepts, the triad should use these 
Line 46: terms. The relationship between CDs and albums can be shown in a diagram. A 
Line 47: common diagramming method is Uniﬁed Modeling Language [UML]. 1 The enti-
Line 48: ties are shown in boxes in Figure 18.1. A simple way to represent the relation-
Line 49: ship that a CD “is a copy of” an album is to have an arrow with a label drawn 
Line 50: between the two boxes. 
Line 51: Copy of
Line 52: Album 
Line 53: CD 
Line 54: Figure 18.1 Diagram of CD/Album Relationship 
Line 55: In addition, the ends of the arrow can be labeled with an indication of how 
Line 56: many entities are on each side of the relationship, as in Figure 18.2. The * states 
Line 57: that there can be many CD copies of an album, and the 1 says that each CD is 
Line 58: a copy of only one album. If there is a value, such as the UPC code, that relates 
Line 59: the CD to the album, you can add that to the diagram. 
Line 60: Copy of
Line 61: UPC Code
Line 62: * 
Line 63: 1
Line 64: Album 
Line 65: CD 
Line 66: * 
Line 67: Copy of
Line 68: 1
Line 69: Album 
Line 70: CD 
Line 71: Figure 18.2 Diagram of CD/Album Relationship with Speciﬁc Relationship 
Line 72: Because the UPC code is what relates this CD to an album, the data for both 
Line 73: CD and album would include that value. The CD table now refers to the Album 
Line 74: table, as follows. 
Line 75: Album Data 
Line 76: UPC Code 
Line 77: Title 
Line 78: CD Category 
Line 79: UPC123456 
Line 80: Janet Jackson Number Ones 
Line 81: Regular
Line 82: 1. See [Wiki06] and [Ambler01] for details. 
Line 83: 
Line 84: --- 페이지 186 ---
Line 85: Relationships 
Line 86: 163
Line 87: and
Line 88: CD Data 
Line 89: ID 
Line 90: UPC Code 
Line 91: Rented 
Line 92: Customer ID 
Line 93: Rental Due 
Line 94: CD3 
Line 95: UPC123456 
Line 96: Yes 
Line 97: 007 
Line 98: 1/23/2011
Line 99: CD7 
Line 100: UPC123456 
Line 101: No
Line 102: Multiple Relationships 
Line 103: There could be another entity that Cathy talks about. Instead of a CD contain-
Line 104: ing the state of being rented, there could be a separate concept of a rental. The 
Line 105: rental is related to and to the CD by the CD ID and to the customer by the cus-
Line 106: tomer ID. Figure 18.3 shows this relationship. 
Line 107: Rental 
Line 108: CD 
Line 109: Customer 
Line 110: Rented by 
Line 111: Customer ID
Line 112: Rented
Line 113: CD ID
Line 114: Figure 18.3 Diagram of CD Customer Rental 
Line 115: With this new organization, the CD does not contain the concept of whether 
Line 116: it is rented or not. That information is now kept in another entity: Rental. This 
Line 117: separation of concerns makes a better design and easier testing. Here’s what the 
Line 118: tables look like. 
Line 119: CD Data 
Line 120: ID 
Line 121: UPC Code 
Line 122: CD3 
Line 123: UPC123456
Line 124: CD7 
Line 125: UPC123456
Line 126: Rental Data 
Line 127: CD ID 
Line 128: Rented 
Line 129: Customer ID 
Line 130: Rental Due 
Line 131: CD3 
Line 132: Yes 
Line 133: 007 
Line 134: 1/23/2011
Line 135: CD7 
Line 136: No
Line 137: Customer Data 
Line 138: Name 
Line 139: ID
Line 140: James 
Line 141: 007
Line 142: 
Line 143: --- 페이지 187 ---
Line 144: Chapter 18 Entities and Relationships
Line 145: 164
Line 146: You can further simplify these tables if the triad approves. For example, the 
Line 147: Customer ID and Rental Due ﬁelds are blank if the CD is not rented. There 
Line 148: could be a convention that if the CD is not rented, an entry does not appear in 
Line 149: the Rental Data table. So if only CD3 was rented and not CD7, the table would 
Line 150: look like this. 
Line 151: Rental Data 
Line 152: CD ID 
Line 153: Customer ID 
Line 154: Rental Due 
Line 155: CD3 
Line 156: 007 
Line 157: 1/23/2011
Line 158: With the additional entities, redundant information is eliminated. The number 
Line 159: of columns in each table is reduced, so there is less information to process. Using 
Line 160: these additional tables, the test for check-in 2 can be as follows. The setup part 
Line 161: could be in common with a number of other tests. 
Line 162:   2.  The ﬁrst three tables might be part of a common setup, as shown in  Chapter 31,
Line 163: “Test Setup.” 
Line 164: Check-In CD 
Line 165: Setup:
Line 166: Album Data 
Line 167: UPC Code 
Line 168: Title 
Line 169: CD Category 
Line 170: UPC123456 
Line 171: Janet Jackson Number Ones 
Line 172: Regular
Line 173: CD Data 
Line 174: ID 
Line 175: UPC Code 
Line 176: CD3 
Line 177: UPC123456
Line 178: CD7 
Line 179: UPC123456
Line 180: Customer Data 
Line 181: Name 
Line 182: ID
Line 183: James 
Line 184: 007
Line 185: 
Line 186: --- 페이지 188 ---
Line 187: Relationships 
Line 188: 165
Line 189:  
Line 190: You could discover this more complex relationship after creating the initial 
Line 191: tests (in Chapter 10, “User Story Breakup”) that used a single table, such as the 
Line 192: ﬁrst table in this chapter. You may not need to alter the original tests. You could 
Line 193: use them with what is called a view. The data in these three tables is combined 
Line 194: to appear as a single table. 3 The view decouples the way data is represented in 
Line 195: the database from the way the business deals with the data. 
Line 196: Given a customer with a rental: 
Line 197: Rental Data 
Line 198: Customer ID = 007 
Line 199: CD ID 
Line 200: Rental Due 
Line 201: CD3 
Line 202: 1/23/2011
Line 203: When the clerk checks in the CD: 
Line 204: Test Date 
Line 205: Date
Line 206: 1/23/2011
Line 207: Check-In CD 
Line 208: Enter 
Line 209: CD ID 
Line 210: CD3
Line 211: Press 
Line 212: Submit
Line 213: Then the CD is recorded as not rented and the rental fee is computed. (The 
Line 214: fee includes one late day.) 
Line 215: Rental Data 
Line 216: Customer ID = 007
Line 217: CD ID 
Line 218: Rental Due
Line 219: Rental Fee 
Line 220: Customer ID 
Line 221: Name 
Line 222: Title 
Line 223: Returned 
Line 224: Rental Fee? 
Line 225: 007 
Line 226: James 
Line 227: Janet Jackson 
Line 228: Number Ones 
Line 229: 1/23/2011 
Line 230: $2
Line 231:   3.  An exercise for the technical reader is to determine how the three tables can be 
Line 232: viewed as the original single table. 
Line 233: 
Line 234: --- 페이지 189 ---
Line 235: Chapter 18 Entities and Relationships
Line 236: 166
Line 237: Alternative Representations 
Line 238: The Rental data could be kept after the CD is checked in as a history of rentals. 
Line 239: This history could be represented as a separate table for use in tests (such as in 
Line 240: Chapter 13, “Simpliﬁcation by Separation”). For example, as shown here: 
Line 241: Rental History Data 
Line 242: CD ID 
Line 243: Customer ID 
Line 244: Rental Due 
Line 245: Returned
Line 246: CD3 
Line 247: 88 
Line 248: 12/21/2009 
Line 249: 12/23/2009
Line 250: CD3 
Line 251: 007 
Line 252: 1/23/2011 
Line 253: 1/23/2011
Line 254: If the business requirements stated that the rental history was only needed in 
Line 255: relationship to a CD, the history could be shown as a table embedded in another 
Line 256: table.4 This cuts down on the number of tables, but it also increases the table’s 
Line 257: size. For example, as shown here: 
Line 258: CD Data  
Line 259: ID 
Line 260: UPC Code 
Line 261: Rental History 
Line 262: CD3 UPC123456 
Line 263: Customer ID  Rental Due 
Line 264: Returned 
Line 265: 88 
Line 266: 12/21/2009 
Line 267: 12/23/2009 
Line 268: 007 
Line 269: 1/23/2011 
Line 270: 1/24/2011  
Line 271: Summary
Line 272: • Relationships between entities can be diagramed for ease of unders tanding.
Line 273: • Entity relationships can be shown in multiple ways in tables. 
Line 274: • The customer unit determines the preferred form of showing relationships.
Line 275: • Tests should reﬂect the entities and relationships. 
Line 276: 4. In domain-driven design (DDD) terminology, CD is the root of an aggregate. 