Line 1: 
Line 2: --- 페이지 266 ---
Line 3: Chapter 29 
Line 4: Case Study: Highly 
Line 5: Available Platform 
Line 6: “You just call out my name,
Line 7: And you know wherever I am
Line 8: I’ll come running, oh yeah baby
Line 9: To see you again.”
Line 10: Carole King, “You’ve Got a Friend” 
Line 11: Many corporate software systems depend on a highly available platform. This 
Line 12: chapter shows increasingly detailed acceptance tests for such a platform. 
Line 13: Context for Switching Servers 
Line 14: A highly available platform has at least two independent computers. If one goes 
Line 15: down, the other available computers take over the load. If the servers are run-
Line 16: ning close to capacity, not all the applications may be able to run. A predeter-
Line 17: mined priority mechanism determines which applications get to run. In addition 
Line 18: to switching applications when a server goes down, in the case study, the system 
Line 19: administrator is notiﬁed either via email or a text message. 
Line 20: The capacity of a server to run applications depends on the demands of the 
Line 21: applications, such as memory, processor usage, and input-output operations. 
Line 22: Instead of being overwhelmed by all the details at once, this study shows how to 
Line 23: introduce the details gradually. This is another manifestation of the separation 
Line 24: of concerns guideline. 
Line 25: 243
Line 26: 
Line 27: --- 페이지 267 ---
Line 28: Chapter 29 Case Study: Highly Available Platform 
Line 29: 244
Line 30: Test for Switching Servers 
Line 31: The ﬁrst test uses a simpliﬁed capacity that considers just the number of appli-
Line 32: cations that can be run on each server. This test demonstrates that the servers 
Line 33: switch applications properly when one of them goes down. There will be a lot 
Line 34: of technical work to perform to make that happen. Starting with this simple 
Line 35: acceptance test keeps the developer unit working while the customer unit exam-
Line 36: ines more detailed capacity issues. 
Line 37: Server Goes Down 
Line 38: Given these servers: 
Line 39: Servers
Line 40: Name 
Line 41: Capacity (Applications) 
Line 42: Freddy 
Line 43: 5
Line 44: Fannie 
Line 45: 3
Line 46: And these applications with their priority: 
Line 47: Applications
Line 48: Name 
Line 49: Priority
Line 50: CEO’s Pet 
Line 51: 100
Line 52: MP3 Download 
Line 53: 99
Line 54: Lost Episode Watching 
Line 55: 98
Line 56: External Web 
Line 57: 50
Line 58: Internal Web 
Line 59: 25
Line 60: Payroll 
Line 61: 10
Line 62: And the servers running these applications: 
Line 63: Server Load 
Line 64: Name 
Line 65: Applications
Line 66: Freddy
Line 67: CEO’s Pet 
Line 68: External Web 
Line 69: Internal Web 
Line 70: Payroll
Line 71: Fannie 
Line 72: Lost Episode Watching 
Line 73: MP3 Download 
Line 74: 
Line 75: --- 페이지 268 ---
Line 76: Test for Switching Servers 
Line 77: 245
Line 78: A second test ensures that the next part of the ﬂow is proper. Now that an 
Line 79: event has occurred, the administrator should be notiﬁed in the appropriate way. 
Line 80: When a server goes down, switch any applications running on it to the 
Line 81: alternate server. If the alternate server does not have the capacity for all the 
Line 82: applications, run the applications based on priority order. 
Line 83: Server Events 
Line 84: Event
Line 85: Servers
Line 86: Remaining? 
Line 87: Applications Running? 
Line 88: Action?
Line 89: Freddy Goes 
Line 90: Down
Line 91: Fannie
Line 92: CEO’s Pet 
Line 93: Lost Episode Watching 
Line 94: MP3 Download 
Line 95: Send event alert 
Line 96: “Freddy down” 
Line 97: Fannie Goes 
Line 98: Down
Line 99: Freddy
Line 100: CEO’s Pet 
Line 101: Lost Episode Watching 
Line 102: MP3 Download 
Line 103: External Web 
Line 104: Internal Web 
Line 105: Send event alert 
Line 106: “Fannie down” 
Line 107: Send Alert to Administrator 
Line 108: Given these preferences for an event alert: 
Line 109: Administrator Notiﬁcation 
Line 110: Notiﬁcation 
Line 111: Preference 
Line 112: Text ID 
Line 113: E-Mail 
Line 114: Action?
Line 115: E-mail 
Line 116: 123 
Line 117: AB@somewhere.com 
Line 118: Send mail to AB@
Line 119: somewhere.com
Line 120: When an event occurs, send the event alert to the system administrator 
Line 121: based on the notiﬁcation preference that the event occurred. 
Line 122: Event Response 
Line 123: Event 
Line 124: Response?
Line 125: Any event occurs 
Line 126: Send Mail to AB@somewhere.com 
Line 127: 
Line 128: --- 페이지 269 ---
Line 129: Chapter 29 Case Study: Highly Available Platform 
Line 130: 246
Line 131: You can create a similar test for three servers if one of them is going down. 
Line 132: That test would show how to distribute the applications among the remaining 
Line 133: two servers. 
Line 134: Test for Technical Rule 
Line 135: Now that application switching works, more complex rules can be applied to 
Line 136: the capacity of each server. The selection of what applications to run is a sepa-
Line 137: rable concern. The results can be tested independently of testing the switching 
Line 138: functionality.
Line 139: For example, if a single server is running, the applications that can be run 
Line 140: depend on selecting the highest priority applications that can run within the 
Line 141: capacity. It’s possible that an application that has a higher priority cannot be 
Line 142: run because there is insufﬁcient capacity. Then a lower priority application that 
Line 143: does not require as much capacity might be run. 
Line 144: In the following table, CPU usage is measured in millions of instructions per 
Line 145: second (MIPS). Memory usage is calculated in megabytes (MB). Input-output 
Line 146: usage is measured in total of reads and writes per second (RWS). 
Line 147: If the notiﬁcation fails, send the event alert via the other method. 
Line 148: Notiﬁcation 
Line 149: Previous Action = Send Mail to AB@somewhere.com 
Line 150: Event 
Line 151: Response?
Line 152: Mail not deliverable 
Line 153: Send text to 123 
Line 154: No response to mail 
Line 155: Send text to 123 
Line 156: Determine Applications to Run on Server 
Line 157: Given applications with these characteristics: 
Line 158: Application Characteristics 
Line 159: Name 
Line 160: Priority
Line 161: CPU Usage 
Line 162: (MIPS)
Line 163: Memory
Line 164: Usage (MB) 
Line 165: Input-Output
Line 166: Usage (RWS) 
Line 167: CEO’s Pet 
Line 168: 100 
Line 169: 1 
Line 170: 1000 
Line 171: 1000
Line 172: MP3 Download 
Line 173: 99 
Line 174: 10 
Line 175: 500 
Line 176: 2000
Line 177: Lost Episode Watching 
Line 178: 98 
Line 179: 5 
Line 180: 200 
Line 181: 3000
Line 182: continues
Line 183: 
Line 184: --- 페이지 270 ---
Line 185: Test for Technical Rule 
Line 186: 247
Line 187: In this test, “Lost Episode Watching” requires 5MIPS. The two higher pri-
Line 188: ority applications—“CEO’s Pet” and “MP3 Download”—use 11MIPS of the 
Line 189: 15MIPS available. So “Lost Episode Watching” cannot be run, but a lower pri-
Line 190: ority application “External Web” requires only 3MIPS, so it can be run. 
Line 191: You can create similar tests for two or more servers. The creation of these 
Line 192: tests brings up issues of how to balance applications between two servers. Given 
Line 193: this test, it’s clear that if there were a second server, at least “Lost Episode 
Line 194: Watching” should be running, as long as the server’s capacity was greater than 
Line 195: that application’s needs. Or perhaps “CEO’s Pet” will run on the second server, 
Line 196: allowing “Lost Episode Watching” to run on the ﬁrst one. 
Line 197: The tests for what applications should be run on what servers can become 
Line 198: fairly complicated. There are usually more issues, such as applications that need 
Line 199: speciﬁc devices that are only available on some of the servers, so they cannot be 
Line 200: run on the other servers. 
Line 201: Application Characteristics 
Line 202: Name 
Line 203: Priority
Line 204: CPU Usage 
Line 205: (MIPS)
Line 206: Memory
Line 207: Usage (MB) 
Line 208: Input-Output
Line 209: Usage (RWS) 
Line 210: External Web 
Line 211: 50 
Line 212: 3 
Line 213: 400 
Line 214: 500
Line 215: Internal Web 
Line 216: 25 
Line 217: 1 
Line 218: 100 
Line 219: 500
Line 220: Payroll 
Line 221: 10 
Line 222: 8 
Line 223: 10 
Line 224: 1000
Line 225: And a single server with the following capacity: 
Line 226: Server Characteristics 
Line 227: Name 
Line 228: CPU Usage (MIPS) 
Line 229: Memory Usage (MB) 
Line 230: Input-Output
Line 231: Usage (RWS) 
Line 232: Fanny 
Line 233: 15 
Line 234: 2000 
Line 235: 5000
Line 236: Then it should run the following applications. 
Line 237: Application Running 
Line 238: Name
Line 239: CPU Usage
Line 240: (MIPS)
Line 241: Memory Usage 
Line 242: (MB)
Line 243: Input-Output
Line 244: Usage (RWS) 
Line 245: CEO’s Pet 
Line 246: 1 
Line 247: 1000 
Line 248: 1000
Line 249: MP3 Download 
Line 250: 10 
Line 251: 500 
Line 252: 2000
Line 253: External Web 
Line 254: 3 
Line 255: 400 
Line 256: 500
Line 257: , Continued
Line 258: 
Line 259: --- 페이지 271 ---
Line 260: Chapter 29 Case Study: Highly Available Platform 
Line 261: 248
Line 262: At some point, an additional test that combines the switching and the selec-
Line 263: tion is created. From the acceptance point of view, this test need only demon-
Line 264: strate that the switching takes into account selection based on the more complex 
Line 265: selection rule. Lots of other combinations of applications and servers may be 
Line 266: tested to ensure that the code and design do not have more esoteric defects. 
Line 267: There would also be acceptance tests for the switching time performance. 
Line 268: Summary
Line 269: •  Separate tests so that each checks a different part of the ﬂow. 
Line 270: •  Separation of concerns makes for simpler testing. 