Line 1: 
Line 2: --- 페이지 122 ---
Line 3: 91
Line 4: Chapter 10
Line 5: Financial Prioritization
Line 6: “As a general rule of thumb,
Line 7: when benefits are not quantified at all,
Line 8: assume there aren’t any.”
Line 9: —Tom DeMarco and Timothy Lister
Line 10: Some projects are undertaken to generate revenue and others to cut expenses,
Line 11: and some strive for both. If we can estimate the amount of money that will be
Line 12: made or saved by each theme, we can use that to help prioritize. Forecasting the
Line 13: financial value of a theme is the responsibility of the product owner, but it is a
Line 14: responsibility shared with all other team members—programmers, testers, ana-
Line 15: lysts, project managers, and so on. In most cases, the product owner will also
Line 16: need to draw on business knowledge and forecasts from the sales and marketing
Line 17: groups.
Line 18: The way I like to determine the financial value of a theme is to hold a meet-
Line 19: ing attended by as many of these individuals as practical. The goal of such a
Line 20: theme valuation meeting is to complete a form like the one shown in Table 10.1
Line 21: for each theme. Depending on the number of themes and participants, this may
Line 22: take more than one meeting.
Line 23: Table 10.1 includes a row for each quarter in the next two years. The time
Line 24: horizon is up to the team. In some cases, teams may want to look at monthly re-
Line 25: turns for one or two years. In other cases, quarterly forecasts are adequate. I find
Line 26: that looking out two years works well on most projects. It strikes a good balance
Line 27: between guessing at the distant future and looking far enough ahead. Because of
Line 28: 
Line 29: --- 페이지 123 ---
Line 30: 92
Line 31: |
Line 32: Chapter 10
Line 33: Financial Prioritization
Line 34: the high amount of uncertainty on software development projects, others con-
Line 35: cur (Bills 2004a).
Line 36: Table 10.1 also includes columns for various types of returns a theme may
Line 37: have. If your project has different types of returns, use different column head-
Line 38: ings. Similarly, use different column headings if a theme will benefit from more
Line 39: specific column headings (perhaps Increased Revenue from U.S. Customers and
Line 40: Increased Revenue for European Customers). It is not necessary to estimate all
Line 41: themes with the same set of columns.
Line 42: Meeting participants complete the worksheet by estimating the value in a
Line 43: cell that they believe will be affected by the development of the theme. A sample
Line 44: completed theme-return worksheet is shown in Table 10.2. In this case, the
Line 45: availability of this theme will attract new customers (New Revenue) and will also
Line 46: lead to increased revenue from existing customers (Incremental Revenue). The
Line 47: new theme will have no impact on either retained revenue or on operational
Line 48: efficiencies.
Line 49: Where do these numbers come from? Ideally from the market research that
Line 50: was used in the business case that initiated the project. At a minimum, whoever
Line 51: requested the theme should be able to quantify the reasons for developing it.
Line 52: Table 10.1 An Empty Theme-Return Worksheet
Line 53: Quarter
Line 54: New Revenue
Line 55: Incremental 
Line 56: Revenue
Line 57: Retained 
Line 58: Revenue
Line 59: Operational 
Line 60: Efficiencies
Line 61: 1
Line 62: 2
Line 63: 3
Line 64: 4
Line 65: 5
Line 66: 6
Line 67: 7
Line 68: 8
Line 69: 
Line 70: --- 페이지 124 ---
Line 71: New Revenue 
Line 72: |
Line 73: 93
Line 74: We cannot compare projects and make prioritization decisions simply by
Line 75: summing the total row of a worksheet like Table 10.2 for each theme. A revenue
Line 76: stream that delivers ¤100k in the first quarter, ¤200k the next, and ¤500k in the
Line 77: third quarter is far less valuable than a stream that delivers those same returns
Line 78: but in the opposite sequence. To compare multiple themes, we need to use one
Line 79: or more standard financial measures. In this chapter, we will look at
Line 80: ◆Net present value
Line 81: ◆Internal rate of return
Line 82: ◆Payback period
Line 83: ◆Discounted payback period
Line 84: However, before looking at these financial measures, we must consider how
Line 85: projects make or save money.
Line 86: Sources of Return
Line 87: The return on a project can come from a variety of sources. For convenience, we
Line 88: can categorize these as new revenue, incremental revenue, retained revenue,
Line 89: and operational efficiencies. Although it is common for one category to domi-
Line 90: nate the return of a specific project, most projects will earn returns from more
Line 91: than one category. 
Line 92: New Revenue
Line 93: Certainly, one of the most common contributors to the return on a project is the
Line 94: opportunity for new revenue. Very few companies are satisfied with their market
Line 95: Table 10.2 A Sample Theme-Return Worksheet
Line 96: Quarter
Line 97: New Revenue
Line 98: Incremental 
Line 99: Revenue
Line 100: Retained 
Line 101: Revenue
Line 102: Operational 
Line 103: Efficiencies
Line 104: 1
Line 105: ¤25,000
Line 106: ¤20,000
Line 107: 0
Line 108: 0
Line 109: 2
Line 110: ¤35,000
Line 111: ¤30,000
Line 112: 0
Line 113: 0
Line 114: 3
Line 115: ¤50,000
Line 116: ¤40,000
Line 117: 0
Line 118: 0
Line 119: 4
Line 120: ¤70,000
Line 121: ¤60,000
Line 122: 0
Line 123: 0
Line 124: Total
Line 125: ¤180,000
Line 126: ¤150,000
Line 127: 0
Line 128: 0
Line 129: 
Line 130: --- 페이지 125 ---
Line 131: 94
Line 132: |
Line 133: Chapter 10
Line 134: Financial Prioritization
Line 135: share, and most companies would like new customers. Even if a software prod-
Line 136: uct is not sold directly, adding new features can lead to new revenue. For exam-
Line 137: ple, I worked at a company that developed software for our own use in serving
Line 138: our hospital customers. At one point, our CEO realized that with some enhance-
Line 139: ments, our software could be used to provide those same services to health in-
Line 140: surers. We made the changes and were able to bring an entirely new source of
Line 141: revenue into the company because of what the new software enabled.
Line 142: Incremental Revenue
Line 143: It is often useful to distinguish revenue from new customers from additional, in-
Line 144: cremental revenue from existing customers. Incremental revenue can result be-
Line 145: cause the new system or product:
Line 146: ◆Encourages existing customers to purchase more licenses
Line 147: ◆Includes optional, add-on modules that can be sold separately
Line 148: ◆Includes features that allow charging a higher price
Line 149: ◆Encourages the use of consulting services (for example, to integrate with a
Line 150: separate third-party application)
Line 151: Retained Revenue
Line 152: Separate from both new and incremental revenue is retained revenue. Retained
Line 153: revenue refers to the revenue an organization will lose if the project or theme is
Line 154: not developed. Suppose you’ve been successfully selling a patient scheduling
Line 155: product to solo-practitioner chiropractors. Some of your customers have been
Line 156: doing well and are expanding to have two or three chiropractors in the practice.
Line 157: Unless your software is enhanced to support scheduling patients among multiple
Line 158: chiropractors, you stand to lose the business of these growing practices. A
Line 159: project to add this capability would allow the company to retain this revenue. In-
Line 160: terestingly, there could also be an opportunity for incremental revenue because
Line 161: you may be able to charge more for the version that supports more than one
Line 162: chiropractor.
Line 163: Operational Efficiencies
Line 164: No organization is ever as efficient as it could be. There’s always some task that
Line 165: could be streamlined or eliminated. If you’re developing software for use by in-
Line 166: ternal customers, you are probably quite aware of the importance of operational
Line 167: 
Line 168: --- 페이지 126 ---
Line 169: Operational Efficiencies 
Line 170: |
Line 171: 95
Line 172: efficiencies. However, even if you’re working on commercial software that is sold
Line 173: to others outside your company, some tasks within your project may still con-
Line 174: tribute to improving operational efficiencies. In your case, though, most often
Line 175: this will refer to your own inefficiency. For example, a number of projects I’ve
Line 176: been on have chosen to develop their own object-relational mapping tool to sim-
Line 177: plify the mapping of objects in the programming language to relational database
Line 178: tables. Similarly, almost every project I’ve been on has developed some form of
Line 179: tool to assist in the work of developing the software. 
Line 180: Often, the drive to improve operational efficiencies comes from anticipated
Line 181: growth. An inefficiency that may not be a problem today rapidly becomes a prob-
Line 182: lem when the company becomes much larger. As an example, suppose your com-
Line 183: pany has developed a website for selling picture frames. You sell a huge variety of
Line 184: standard frames but also sell frames in custom sizes. Business is doing well, and
Line 185: the company anticipates strong growth over the next two years. In fact, it ex-
Line 186: pects sales to increase tenfold over that period. As in any business, a certain per-
Line 187: centage of sold items end up being sent back to the company as returned
Line 188: merchandise. It’s never been a high priority to have a highly automated, efficient
Line 189: solution for processing returns, and right now it takes one person about two
Line 190: hours a day to process returns, including updating inventory and crediting the
Line 191: buyer’s credit card. The two hours spent on this may not be a critical issue today.
Line 192: But when sales have increased 1,000%, returned items will probably increase
Line 193: 1,000%, and processing returns will take twenty person-hours each day. By that
Line 194: point, it will certainly be worth considering whether this is an operational ineffi-
Line 195: ciency that should be addressed.
Line 196: In looking to improve operational efficiency, some likely places include
Line 197: ◆Anything that takes a long time or that would take a long time if the
Line 198: company grew
Line 199: ◆Better integration or communication between departments
Line 200: ◆Reduced employee turnover
Line 201: ◆Shorter training time for new employees
Line 202: ◆Any time-sensitive process
Line 203: ◆Combining multiple processes
Line 204: ◆Anything that improves accuracy and reduces rework
Line 205: 
Line 206: --- 페이지 127 ---
Line 207: 96
Line 208: |
Line 209: Chapter 10
Line 210: Financial Prioritization
Line 211: An Example: WebPayroll
Line 212: Using these techniques, let’s estimate the returns for a project. Suppose our
Line 213: company, WebPayroll, offers a web-based payroll system to companies too small
Line 214: to calculate their own payroll taxes, print checks, and so on. We’re fairly success-
Line 215: ful already but are enhancing the software to improve turnaround time.
Line 216: Currently, we tell customers that they need to enter payroll information on
Line 217: our website three days before they need checks to distribute to their employees.
Line 218: Our goal with the new system is to offer next-day service. If payroll information
Line 219: is entered on the WebPayroll site by 5:00 p.m., we can generate checks, print
Line 220: them, and have them delivered overnight. Checks will be in our customers’
Line 221: hands the next morning.
Line 222: Before we can begin estimating the return on the overnight project, we need
Line 223: to decide when it will be available. Assume that the developers have already esti-
Line 224: mated the stories in this theme and that they came up with 150 story points. At
Line 225: the team’s historical velocity of 20 story points per two-week iteration, develop-
Line 226: ing the theme will take 
Line 227:  iterations. This means that in-
Line 228: creased revenue and operational efficiencies can begin after the eighth iteration
Line 229: (unless we can find a way to deliver a partial solution, which should always be a
Line 230: goal).
Line 231: Calculating New Revenue
Line 232: Offering next-day instead of three-day service will open new revenue opportu-
Line 233: nies. To quantify these opportunities, we first estimate the number of new cus-
Line 234: tomers we’ll acquire. We don’t have any solid data. But our main salesperson,
Line 235: Terry, says that around one-third of the customers she talks with reject WebPay-
Line 236: roll because of our three-day requirement. Based on current sales projections,
Line 237: Terry believes she can attract fifty new customers per quarter this year and then
Line 238: one hundred customers per quarter next year. These values are added to the New
Line 239: Customers column of Table 10.3. Even though the overnight feature won’t be
Line 240: available until the middle of the second quarter, Terry believes she can still sign
Line 241: up fifty new customers in that quarter.
Line 242: Next, we estimate the revenue per customer. We can do this by thinking
Line 243: about likely new customers relative to our current customers. We know, for ex-
Line 244: ample, that the average WebPayroll customer pays us ¤400 per year in fees. How-
Line 245: ever, we think that overnight delivery will be most appealing to smaller
Line 246: customers—those that pay us an average of ¤200 per year. We think we’ll make
Line 247: another ¤100 per year from each of these customers. The total value of each new
Line 248: customer is then ¤300 per year, or ¤75 per quarter. Because overnight service
Line 249: 150 20
Line 250: e
Line 251: 7.5
Line 252: 8
Line 253: =
Line 254: =
Line 255: 
Line 256: --- 페이지 128 ---
Line 257: Calculating Retained Revenue 
Line 258: |
Line 259: 97
Line 260: will be available only for two-thirds of the second quarter, the revenue per cus-
Line 261: tomer is lowered appropriately in that quarter. These values are added to the
Line 262: Revenue per Customer column of Table 10.3, which also allows us to calculate
Line 263: the New Revenue column.
Line 264: Calculating Incremental Revenue
Line 265: Incremental revenue refers to additional revenue we can get from existing cus-
Line 266: tomers. Based on what we know of our current customers, how often they are
Line 267: late submitting payroll information, and so on, we estimate that we’ll sign up
Line 268: about 100 customers per quarter until 400 of our current customers are using
Line 269: the overnight service. As for new customers, the service will generate about ¤100
Line 270: per year or ¤25 per quarter after it’s available a third of the way into the second
Line 271: quarter. Table 10.4 is created to calculate the total incremental revenue per
Line 272: quarter from these estimates.
Line 273: Calculating Retained Revenue
Line 274: Retained revenue is what we will no longer lose because customers are dissatis-
Line 275: fied with our product, outgrow it, or otherwise decide to switch away from Web-
Line 276: Payroll. The company currently doesn’t have any good metric for tracking this.
Line 277: We know it’s beginning to be an issue and will become much more significant
Line 278: over the next few years.
Line 279: Table 10.3 Projected New Revenue from the WebPayroll Project
Line 280: Quarter
Line 281: New 
Line 282: Customers
Line 283: Revenue per 
Line 284: Customer
Line 285: New Revenue
Line 286: 1
Line 287: 0
Line 288: ¤0
Line 289: ¤0
Line 290: 2
Line 291: 50
Line 292: ¤50
Line 293: ¤2,500
Line 294: 3
Line 295: 50
Line 296: ¤75
Line 297: ¤3,750
Line 298: 4
Line 299: 50
Line 300: ¤75
Line 301: ¤3,750
Line 302: 5
Line 303: 100
Line 304: ¤75
Line 305: ¤7,500
Line 306: 6
Line 307: 100
Line 308: ¤75
Line 309: ¤7,500
Line 310: 7
Line 311: 100
Line 312: ¤75
Line 313: ¤7,500
Line 314: 8
Line 315: 100
Line 316: ¤75
Line 317: ¤7,500
Line 318: 
Line 319: --- 페이지 129 ---
Line 320: 98
Line 321: |
Line 322: Chapter 10
Line 323: Financial Prioritization
Line 324: We estimate that by having an overnight service, we’ll prevent the loss of
Line 325: twenty customers per quarter in the first year and forty customers per quarter in
Line 326: the second year. Significantly, these customers will stick with WebPayroll now,
Line 327: even though the functionality won’t be available until the second quarter. That
Line 328: means that the benefits of the overnight project begin in the first quarter, even
Line 329: though overnight delivery won’t be available until the second quarter. 
Line 330: Because each current customer is worth ¤400 per year, that is ¤100 per
Line 331: quarter. With that, we can calculate retained revenue as shown in Table 10.5.
Line 332: Calculating Operational Efficiencies
Line 333: For the overnight project to be successful, we will need to eliminate almost all of
Line 334: the manual intervention our system relies on today. Currently, the system relies
Line 335: on a payroll clerk in the WebPayroll office to verify the correctness of the payroll
Line 336: information, and then submit it manually through a couple of workflow steps.
Line 337: We have two payroll clerks doing this today.
Line 338: Without the overnight features, the staffing plan calls for adding two clerks
Line 339: in the middle of this year and two in the middle of next year. Because of the effi-
Line 340: ciencies planned as part of the overnight project, we expect to be able to elimi-
Line 341: nate one of these positions each year. 
Line 342: Table 10.4 Projected Incremental Revenue from the WebPayroll Project
Line 343: Quarter
Line 344:  Customers
Line 345: Revenue per 
Line 346: Customer
Line 347: Incremental 
Line 348: Revenue
Line 349: 1
Line 350: 0
Line 351: ¤0
Line 352: ¤0
Line 353: 2
Line 354: 100
Line 355: ¤16
Line 356: ¤1,600
Line 357: 3
Line 358: 200
Line 359: ¤25
Line 360: ¤5,000
Line 361: 4
Line 362: 300
Line 363: ¤25
Line 364: ¤7,500
Line 365: 5
Line 366: 400
Line 367: ¤25
Line 368: ¤10,000
Line 369: 6
Line 370: 400
Line 371: ¤25
Line 372: ¤10,000
Line 373: 7
Line 374: 400
Line 375: ¤25
Line 376: ¤10,000
Line 377: 8
Line 378: 400
Line 379: ¤25
Line 380: ¤10,000
Line 381: 
Line 382: --- 페이지 130 ---
Line 383: Calculating Operational Efficiencies 
Line 384: |
Line 385: 99
Line 386: Payroll clerks make an average of ¤20,000 per year. Each one, however, also
Line 387: takes up space in the office, is assigned some equipment and software, and is
Line 388: given benefits. In total, these additional, hidden expenses account for around an-
Line 389: other 50% of an employee’s salary, meaning the true cost of a payroll clerk is
Line 390: closer to ¤30,000 annually. This is known as the fully burdened labor cost. The
Line 391: number of clerks not hired and the fully burdened labor cost for each can be
Line 392: multiplied each quarter to give the total operational efficiencies, as shown in
Line 393: Table 10.6.
Line 394: Table 10.5 Projected Retained Revenue from the WebPayroll Project
Line 395: Quarter
Line 396: Retained 
Line 397: Customers
Line 398: Revenue per 
Line 399: Customer
Line 400: Retained 
Line 401: Revenue
Line 402: 1
Line 403: 20
Line 404: ¤100
Line 405: ¤2,000
Line 406: 2
Line 407: 20
Line 408: ¤100
Line 409: ¤2,000
Line 410: 3
Line 411: 20
Line 412: ¤100
Line 413: ¤2,000
Line 414: 4
Line 415: 20
Line 416: ¤100
Line 417: ¤2,000
Line 418: 5
Line 419: 40
Line 420: ¤100
Line 421: ¤4,000
Line 422: 6
Line 423: 40
Line 424: ¤100
Line 425: ¤4,000
Line 426: 7
Line 427: 40
Line 428: ¤100
Line 429: ¤4,000
Line 430: 8
Line 431: 40
Line 432: ¤100
Line 433: ¤4,000
Line 434: Table 10.6 Projected Operational Efficiencies from the WebPayroll Project
Line 435: Quarter
Line 436: Payroll Clerks 
Line 437: Not Needed
Line 438: Fully Burdened 
Line 439: Labor Cost
Line 440: Operational 
Line 441: Efficiencies
Line 442: 1
Line 443: 0
Line 444: 0
Line 445: 0
Line 446: 2
Line 447: 0
Line 448: 0
Line 449: 0
Line 450: 3
Line 451: 1
Line 452: ¤7,500
Line 453: ¤7,500
Line 454: 4
Line 455: 1
Line 456: ¤7,500
Line 457: ¤7,500
Line 458: 5
Line 459: 1
Line 460: ¤7,500
Line 461: ¤7,500
Line 462: 6
Line 463: 1
Line 464: ¤7,500
Line 465: ¤7,500
Line 466: 7
Line 467: 2
Line 468: ¤7,500
Line 469: ¤15,000
Line 470: 8
Line 471: 2
Line 472: ¤7,500
Line 473: ¤15,000
Line 474: 
Line 475: --- 페이지 131 ---
Line 476: 100 |
Line 477: Chapter 10
Line 478: Financial Prioritization
Line 479: Estimating Development Cost
Line 480: To complete the investment profile of the WebPayroll overnight project, we need
Line 481: to estimate the expected development cost of the theme. To do this, let’s look at
Line 482: the salaries of everyone involved in the project, as shown in Table 10.7.
Line 483: The fully burdened labor cost in Table 10.7 is calculated as 50% more than
Line 484: each person’s salary alone. Because iterations are two weeks, the burdened cost
Line 485: per iteration is 1/26th of the fully burdened labor cost. The Time on Project col-
Line 486: umn indicates the portion of time that each team member allocates to the
Line 487: project. Everyone is full time except one programmer. The Adjusted Cost per It-
Line 488: eration column shows the cost to the project of each individual based on bur-
Line 489: dened labor cost and the amount of time spent on the project. In total, the team
Line 490: shown in Table 10.7 costs ¤13,550 per iteration. We’ll round that to ¤13,500.
Line 491: It is often useful to know the cost per story point (or ideal day). To calculate
Line 492: this, divide the adjusted cost per iteration by the team’s average or expected ve-
Line 493: locity. Because the WebPayroll team has an average velocity of 20 story points
Line 494: per iteration, their cost per story point is 
Line 495:  This information is
Line 496: useful because if the team is asked how much it will cost to develop something
Line 497: estimated at 100 story points, they know the answer is ¤67,500 (
Line 498: ).
Line 499: The cost of the WebPayroll team can be summarized as shown in Table 10.8.
Line 500: Table 10.7 The WebPayroll Project Team
Line 501: Role
Line 502: Annual 
Line 503: Salary
Line 504: Fully 
Line 505: Burdened 
Line 506: Labor Cost
Line 507: Burdened 
Line 508: Cost per 
Line 509: Iteration
Line 510: Time on 
Line 511: Project
Line 512: Adjusted 
Line 513: Cost per 
Line 514: Iteration
Line 515: Product owner
Line 516: ¤50,000
Line 517: ¤75,000
Line 518: ¤2,900
Line 519: 100%
Line 520: ¤2,900
Line 521: Programmer
Line 522: ¤50,000
Line 523: ¤75,000
Line 524: ¤2,900
Line 525: 100%
Line 526: ¤2,900
Line 527: Programmer
Line 528: ¤30,000
Line 529: ¤45,000
Line 530: ¤1,700
Line 531: 50%
Line 532: ¤850
Line 533: Analyst
Line 534: ¤40,000
Line 535: ¤60,000
Line 536: ¤2,300
Line 537: 100%
Line 538: ¤2,300
Line 539: Tester
Line 540: ¤30,000
Line 541: ¤45,000
Line 542: ¤1,700
Line 543: 100%
Line 544: ¤1,700
Line 545: Tester
Line 546: ¤50,000
Line 547: ¤75,000
Line 548: ¤2,900
Line 549: 100%
Line 550: ¤2,900
Line 551: Total
Line 552: ¤13,550
Line 553: 13,500 20
Line 554: e
Line 555: 675.
Line 556: =
Line 557: 100
Line 558: 675
Line 559: u
Line 560: 
Line 561: --- 페이지 132 ---
Line 562: Putting It All Together 
Line 563: |
Line 564: 101
Line 565: Putting It All Together
Line 566: From this analysis of cost, new revenue, incremental revenue, and operational
Line 567: efficiencies, we can put together Table 10.9.
Line 568: The overnight feature is expected to be finished in the eighth iteration, or af-
Line 569: ter sixteen weeks. The first quarter will be thirteen of those weeks for a cost of
Line 570: ¤87,750 (
Line 571: ). The second quarter will be another three weeks for a cost
Line 572: of ¤20,250. 
Line 573: Table 10.8 Summary of Costs for the WebPayroll Team
Line 574: Measure
Line 575: Cost
Line 576: Cost per story point
Line 577: ¤675
Line 578: Cost per week
Line 579: ¤6,750
Line 580: Cost per iteration
Line 581: ¤13,500
Line 582: Table 10.9 Projected Returns from the WebPayroll Project
Line 583: Quarter
Line 584: Development
Line 585: Cost
Line 586: New
Line 587: Revenue
Line 588: Incremental
Line 589: Revenue
Line 590: Retained
Line 591: Revenue
Line 592: Operational
Line 593: Efficiencies
Line 594: Net Cash
Line 595: Flow
Line 596: 1
Line 597: –¤87,750
Line 598: ¤0
Line 599: ¤0
Line 600: ¤2,000
Line 601: ¤0
Line 602: –¤85,750
Line 603: 2
Line 604: –¤20,250
Line 605: ¤2,500
Line 606: ¤1,600
Line 607: ¤2,000
Line 608: ¤0
Line 609: –¤14,150
Line 610: 3
Line 611: ¤3,750
Line 612: ¤5,000
Line 613: ¤2,000
Line 614: ¤7,500
Line 615: ¤18,250
Line 616: 4
Line 617: ¤3,750
Line 618: ¤7,500
Line 619: ¤2,000
Line 620: ¤7,500
Line 621: ¤20,750
Line 622: 5
Line 623: ¤7,500
Line 624: ¤10,000
Line 625: ¤4,000
Line 626: ¤7,500
Line 627: ¤29,000
Line 628: 6
Line 629: ¤7,500
Line 630: ¤10,000
Line 631: ¤4,000
Line 632: ¤7,500
Line 633: ¤29,000
Line 634: 7
Line 635: ¤7,500
Line 636: ¤10,000
Line 637: ¤4,000
Line 638: ¤15,000
Line 639: ¤36,500
Line 640: 8
Line 641: ¤7,500
Line 642: ¤10,000
Line 643: ¤4,000
Line 644: ¤15,000
Line 645: ¤36,500
Line 646: 13
Line 647: 6,750
Line 648: u
Line 649: 
Line 650: --- 페이지 133 ---
Line 651: 102 |
Line 652: Chapter 10
Line 653: Financial Prioritization
Line 654: Financial Measures
Line 655: Having come up with a way of estimating the cash flow stream that will be gen-
Line 656: erated by each theme, we next turn our attention to various ways of analyzing
Line 657: and evaluating those cash flow streams. In this section, we will look at net
Line 658: present value, internal rate of return, payback period, and discounted payback
Line 659: period. Each of these measures can be used for comparing the returns on a
Line 660: theme. But first, it’s important to understand the time value of money.
Line 661: The Time Value of Money
Line 662: In the early Popeye comic strips, Wimpy would tell the other characters, “I’ll
Line 663: gladly pay you on Tuesday for a hamburger today.” Only a sucker would take
Line 664: Wimpy up on that deal, because money today is more valuable than money next
Line 665: Tuesday.
Line 666: To determine the value today of a future amount of money, we think in
Line 667: terms of how much money would have to be put in the bank today for it to grow
Line 668: to the future amount. To buy a ¤5 hamburger next Tuesday, I might need to put
Line 669: ¤4.99 in the bank today. The amount I have to invest today to have a known
Line 670: amount in the future is called the present value. As a simple case, if I can earn
Line 671: 10% on my money and want to have ¤1.00 a year from now, I need to invest
Line 672: ¤0.91 today. In other words, with a 10% interest rate, ¤0.91 is the present value
Line 673: of ¤1.00 in a year. If I could earn 20% on my money, I would need to invest only
Line 674: ¤0.83 today.
Line 675: The process of moving future amounts back into their present value is
Line 676: known as discounting. Clearly, the interest rate that is used for discounting fu-
Line 677: ture amounts is critical to determining the present value of a future amount.
Line 678: The rate at which organizations discount future money is known as their
Line 679: opportunity cost and reflects the percentage return that is passed up to make
Line 680: this investment. We all—individuals and organizations—have various opportu-
Line 681: nities for investing our money. I can put my money into a bank saving account,
Line 682: or I can invest in stocks. I can invest it in real estate, or I can put it under my
Line 683: mattress. Organizations can invest their money in these same ways, or they can
Line 684: invest money on various projects. If an organization has typically earned 20% on
Line 685: past projects, new projects should be assessed against this same 20%. The orga-
Line 686: nization’s opportunity cost is 20% because an investment in a new project
Line 687: means that the organization gave up the opportunity to invest in some other
Line 688: project, which would have earned 20%.
Line 689: 
Line 690: --- 페이지 134 ---
Line 691: Net Present Value 
Line 692: |
Line 693: 103
Line 694: Net Present Value
Line 695: The first formula we’ll look at for evaluating a theme is the net present value
Line 696: (NPV). To determine NPV, sum the present values of each item in a stream of fu-
Line 697: ture values. The formula for doing so is
Line 698: where i is the interest rate and Ft is the net cash flow in period t.
Line 699: To see how this works, let’s continue with the WebPayroll example. As deter-
Line 700: mined earlier, the overnight project is expected to cost ¤108,000 and to generate
Line 701: the revenue and savings summarized in Table 10.9, which are repeated in the
Line 702: Net Cash Flow column of Table 10.10. The Present Value Factor column of that
Line 703: table is the 
Line 704:  portion of the NPV calculation and represents the amount
Line 705: by which the future net cash flow will be discounted. The final column, Present
Line 706: Value, is the product of the Net Cash Flow and Present Value Factor columns. It
Line 707: indicates, for example, that the present value of ¤18,250 at the end of the third
Line 708: quarter year is ¤16,701. Summing the values in the Present Value column gives
Line 709: the total NPV, which is ¤46,341 in this case.
Line 710: Table 10.10 Determining the NPV for WebPayroll
Line 711: End of 
Line 712: Quarter
Line 713: Net Cash 
Line 714: Flow
Line 715: Present Value 
Line 716: Factor
Line 717: (12% / Year)
Line 718: Present Value
Line 719: 1
Line 720: –¤85,750
Line 721: 0.971
Line 722: –¤83,252
Line 723: 2
Line 724: –¤14,150
Line 725: 0.943
Line 726: –¤13,338
Line 727: 3
Line 728: ¤18,250
Line 729: 0.915
Line 730: ¤16,701
Line 731: 4
Line 732: ¤20,750
Line 733: 0.888
Line 734: ¤18,436
Line 735: 5
Line 736: ¤29,000
Line 737: 0.863
Line 738: ¤25,016
Line 739: 6
Line 740: ¤29,000
Line 741: 0.837
Line 742: ¤24,287
Line 743: 7
Line 744: ¤36,500
Line 745: 0.813
Line 746: ¤29,677
Line 747: 8
Line 748: ¤36,500
Line 749: 0.789
Line 750: ¤28,813
Line 751: NPV (12%) =
Line 752: ¤46,341
Line 753: NPV(i)
Line 754: Ft 1
Line 755: i
Line 756: +
Line 757: 
Line 758: 
Line 759: 
Line 760: 
Line 761: t
Line 762: –
Line 763: t
Line 764: 0
Line 765: =
Line 766: n
Line 767: ¦
Line 768: =
Line 769: 1
Line 770: i
Line 771: +
Line 772: 
Line 773: 
Line 774: 
Line 775: 
Line 776: t
Line 777: –
Line 778: 
Line 779: --- 페이지 135 ---
Line 780: 104 |
Line 781: Chapter 10
Line 782: Financial Prioritization
Line 783: Using net present value to compare and prioritize themes has the advan-
Line 784: tages of being easy to calculate and easy to understand. The primary disadvan-
Line 785: tage to NPV is that comparing the values of two different cash flow streams can
Line 786: be misleading. Suppose we are trying to choose between two projects. The first
Line 787: project requires huge up-front investments but has an NPV of ¤100,000. The sec-
Line 788: ond project requires only a small up-front investment but also has an NPV of
Line 789: ¤100,000. Clearly, we’d prefer to make the investment in the theme that ties up
Line 790: less cash but that has the same NPV. What we’d really like is to express the return
Line 791: on a theme in percentage terms so that we can compare themes directly.
Line 792: Internal Rate of Return
Line 793: Internal Rate of Return (IRR, and sometimes called Return on Investment or
Line 794: ROI) provides a way of expressing the return on a project in percentage terms.
Line 795: Where NPV is a measure of how much money a project can be expected to return
Line 796: (in today’s present value), IRR is a measure of how quickly the money invested in
Line 797: a project will increase in value. With IRR we can more readily compare projects,
Line 798: as shown in Table 10.11. Which project would you prefer?
Line 799: Most people would prefer to make 43% on their money, even though the
Line 800: NPV is higher for Project A, which also requires the higher initial investment.
Line 801: Cash flows for these two projects are shown in Table 10.12.
Line 802: Many organizations will specify a minimum attractive rate of return, or
Line 803: MARR. Only projects or themes with an IRR that exceeds the MARR will be
Line 804: funded. It is impractical to set a similar threshold for NPV, because NPV values
Line 805: are highly dependent on the magnitude of the project. If an NPV threshold were
Line 806: in place, small (but valuable) projects would never be approved.
Line 807: IRR is defined as the interest rate at which the NPV of a cash flow stream is
Line 808: equal to 0. In other words, it is the value for i* such that
Line 809: Table 10.11 Comparing Two Projects across NPV and IRR
Line 810: Project
Line 811: Investment
Line 812: NPV
Line 813: IRR
Line 814: Project A
Line 815: ¤200,000
Line 816: ¤98,682
Line 817: 27%
Line 818: Project B
Line 819: ¤100,000
Line 820: ¤79,154
Line 821: 43%
Line 822: 0
Line 823: PV i*
Line 824: 
Line 825: 
Line 826: 
Line 827: 
Line 828: Ft 1
Line 829: i
Line 830: +
Line 831: 
Line 832: 
Line 833: 
Line 834: 
Line 835: t
Line 836: –
Line 837: t
Line 838: 0
Line 839: =
Line 840: n
Line 841: ¦
Line 842: =
Line 843: =
Line 844: 
Line 845: --- 페이지 136 ---
Line 846: Internal Rate of Return 
Line 847: |
Line 848: 105
Line 849: The formula for calculating IRR is complex and beyond the scope of this
Line 850: book. Fortunately, most major spreadsheet programs include easy-to-use IRR
Line 851: functions. If you want to calculate IRR by hand, Steve Tockey (2004) provides the
Line 852: best description. However, even though you can use a spreadsheet to calculate
Line 853: IRR, there are a couple of preconditions for its use that you need to be aware of:
Line 854: ◆The first one or more items in the cash flow stream must be expenses. (Note
Line 855: that there must be at least one.)
Line 856: ◆Once the cash flow stream turns positive, it must remain positive.
Line 857: ◆The sum of the positive items is larger than the sum of the negative items—
Line 858: that is, money is made overall.
Line 859: Because the cash stream for the WebPayroll overnight-delivery theme satis-
Line 860: fies these preconditions, we can calculate the IRR for the theme. To do so in
Line 861: Excel, enter this formula into a cell:
Line 862: +IRR({0, –85750, –14150, 18250, 20750, 29000, 29000, 36500, 36500})
Line 863: The numbers within the curly braces are the cash flow streams for each of
Line 864: the eight quarters. The initial 0 indicates that no up-front costs occurred on the
Line 865: first day of the project (as might if WebPayroll had to buy additional servers to
Line 866: initiate the project). For the WebPayroll overnight project the IRR is 12%, which
Line 867: means that the expected cash flow stream is equivalent to earning a 12% annual
Line 868: return on the company’s investment.
Line 869: A first advantage to using IRR is that there is no requirement to establish
Line 870: (or, in the worst case, guess at) an organization’s discount rate, as is necessary
Line 871: when calculating NPV. 
Line 872: A second advantage to IRR is that it can be used directly in comparing
Line 873: projects. A project with a 45% IRR has a higher return on its investment than
Line 874: Table 10.12 Cash Flows for the Projects in Table 10.11
Line 875: Year
Line 876: Project A
Line 877: Project B
Line 878: 0
Line 879: –200,000
Line 880: –100,000
Line 881: 1
Line 882: 50,000
Line 883: 50,000
Line 884: 2
Line 885: 75,000
Line 886: 75,000
Line 887: 3
Line 888: 100,000
Line 889: 50,000
Line 890: 4
Line 891: 170,000
Line 892: 50,000
Line 893: 
Line 894: --- 페이지 137 ---
Line 895: 106 |
Line 896: Chapter 10
Line 897: Financial Prioritization
Line 898: does a project with a 25% IRR. You cannot usually use IRR in isolation, though,
Line 899: for making decisions. Suppose the project returning 45% is very small, so the
Line 900: 45% return comes on a small investment yet the project ties up a critical devel-
Line 901: oper. Further, suppose that the project returning 25% does so against a large in-
Line 902: vestment but requires the same critical developer. You may choose to make
Line 903: more money by doing the second project, the one with the lower IRR.
Line 904: As an additional example, you may prefer the project with the 45% IRR, but
Line 905: it requires two years of investment before it begins generating spectacular re-
Line 906: turns. The project with 25% IRR begins earning money after a year. If the orga-
Line 907: nization cannot afford to make two years of investment, the project with the
Line 908: lower IRR may be preferable.
Line 909: A first disadvantage to IRR is that because the calculation is hard to do by
Line 910: hand, the result may be more subject to distrust by some. A second disadvantage
Line 911: is that IRR cannot be calculated in all situations. As we saw previously, three pre-
Line 912: conditions must be met to calculate a meaningful IRR. 
Line 913: Payback Period
Line 914: Through NPV, we can look at a cash flow stream as a single, present value
Line 915: amount. Alternatively, we can look at a cash flow stream as an interest rate
Line 916: through IRR. An additional way of looking at a cash flow stream is as the amount
Line 917: of time required to earn back the initial investment. This is known as the pay-
Line 918: back period. To see how it is determined, Table 10.13 shows the payback calcula-
Line 919: tions for the WebPayroll overnight project.
Line 920: Table 10.13 Determing the Payback Period for the WebPayroll Overnight Project
Line 921: Quarter
Line 922: Net Cash Flow at
Line 923: End of Quarter
Line 924: Running Total
Line 925: 1
Line 926: –¤85,750
Line 927: –¤85,750
Line 928: 2
Line 929: –¤14,150
Line 930: –¤99,900
Line 931: 3
Line 932: ¤18,250
Line 933: –¤81,650
Line 934: 4
Line 935: ¤20,750
Line 936: –¤60,900
Line 937: 5
Line 938: ¤29,000
Line 939: –¤31,900
Line 940: 6
Line 941: ¤29,000
Line 942: –¤2,900
Line 943: 7
Line 944: ¤36,500
Line 945: ¤33,600
Line 946: 8
Line 947: ¤36,500
Line 948: ¤70,100
Line 949: 
Line 950: --- 페이지 138 ---
Line 951: Discounted Payback Period 
Line 952: |
Line 953: 107
Line 954: During the first quarter, WebPayroll invests ¤85,750 in the project. In the
Line 955: second quarter, it makes an additional net investment of ¤14,150. In the third
Line 956: quarter it starts earning back the investment by making ¤18,250. Sometime dur-
Line 957: ing the seventh quarter, the net investment in the project turns positive, and the
Line 958: project’s payback period is said to be seven quarters.
Line 959: There are two primary advantages to using payback period when comparing
Line 960: and prioritizing themes. First, the calculations and interpretation are straight-
Line 961: forward. Second, it measures the amount and duration of financial risk taken on
Line 962: by the organization. The larger the payback period, the riskier the project, be-
Line 963: cause anything could change during that period.
Line 964: The primary disadvantage to payback period is that it fails to take into ac-
Line 965: count the time value of money. Money received three years in the future is val-
Line 966: ued as highly as money paid out today. The second drawback to payback period is
Line 967: that it is not a measure of the profitability of a project or theme. Payback period-
Line 968: will tell us that an organization will recover its money in seven quarters, but it
Line 969: doesn’t address how much money will be made.
Line 970: Discounted Payback Period
Line 971: It is easy to remedy the first drawback of the payback-period calculation. To do so
Line 972: we simply apply the appropriate discount factor to each item in the cash flow
Line 973: stream. The way to do this is shown in Table 10.14 for the WebPayroll overnight
Line 974: project.
Line 975: Table 10.14 Determing the WebPayroll Overnight Project’s Discounted Payback Period
Line 976: End of 
Line 977: Quarter
Line 978: Net Cash Flow
Line 979: Present Value 
Line 980: Factor
Line 981: (12%/ Year)
Line 982: Discounted 
Line 983: Cash Flow
Line 984: Running Total
Line 985: 1
Line 986: –¤85,750
Line 987: 0.971
Line 988: –¤83,252
Line 989: –¤83,252
Line 990: 2
Line 991: –¤14,150
Line 992: 0.943
Line 993: –¤13,338
Line 994: –¤96,590
Line 995: 3
Line 996: ¤18,250
Line 997: 0.915
Line 998: ¤16,701
Line 999: –¤79,889
Line 1000: 4
Line 1001: ¤20,750
Line 1002: 0.888
Line 1003: ¤18,436
Line 1004: –¤61,453
Line 1005: 5
Line 1006: ¤29,000
Line 1007: 0.863
Line 1008: ¤25,016
Line 1009: –¤36,437
Line 1010: 6
Line 1011: ¤29,000
Line 1012: 0.837
Line 1013: ¤24,287
Line 1014: –¤12,150
Line 1015: 7
Line 1016: ¤36,500
Line 1017: 0.813
Line 1018: ¤29,677
Line 1019: ¤17,527
Line 1020: 8
Line 1021: ¤36,500
Line 1022: 0.789
Line 1023: ¤28,813
Line 1024: ¤46,340
Line 1025: 
Line 1026: --- 페이지 139 ---
Line 1027: 108 |
Line 1028: Chapter 10
Line 1029: Financial Prioritization
Line 1030: As Table 10.14 shows, the running total of discounted cash flow becomes
Line 1031: positive in the seventh quarter (just as it did in the simple payback-period
Line 1032: calculation).
Line 1033: Comparing Returns
Line 1034: As you assess each theme, you build up information that can be used to compare
Line 1035: the themes and make the prioritization decisions that are driving this analysis.
Line 1036: The results of valuing multiple themes can be presented as shown in Table 10.15.
Line 1037: A table such as this lets an organization quickly review its options and choose to
Line 1038: work on the highest-valued themes. 
Line 1039: In this case, the overnight theme has the highest net present value, but it
Line 1040: takes the longest to earn back the investment. The partner integration theme
Line 1041: has the highest return on investment and the shortest discounted payback pe-
Line 1042: riod, but it has the lowest NPV. Custom reporting has the lowest rate of return
Line 1043: on investment. However, it could be combined with partner integration and
Line 1044: done with the same cost as the overnight service theme. Making a decision is not
Line 1045: cut and dried; the product owner and team will need to consider a variety of sit-
Line 1046: uationally specific factors, such as the organization’s tolerance for risk, need for
Line 1047: short payback periods, availability of resources, other options for investment
Line 1048: money, and so on.
Line 1049: Table 10.15 Various Valuations for Each Theme in a Project
Line 1050: Theme
Line 1051: Story 
Line 1052: Points
Line 1053: Cost
Line 1054: NPV
Line 1055: ROI
Line 1056: Discounted 
Line 1057: Payback 
Line 1058: Period
Line 1059: Overnight service
Line 1060: 150
Line 1061: ¤101,250
Line 1062: ¤46,341
Line 1063: 45%
Line 1064: 7 quarters
Line 1065: Custom reporting
Line 1066: 90
Line 1067: ¤60,750
Line 1068: ¤34,533
Line 1069: 15%
Line 1070: 6 quarters
Line 1071: Partner integration
Line 1072: 60
Line 1073: ¤40,500
Line 1074: ¤30,013
Line 1075: 49%
Line 1076: 3 quarters
Line 1077: For More on Project Economics
Line 1078: Although this chapter provides a basic overview of how to use and calcu-
Line 1079: late four financial measures, much more could be said. For more on the
Line 1080: subject of software project economics, Steve Tockey’s Return on Soft-
Line 1081: ware: Maximizing the Return on Your Software Investment (2004) is a
Line 1082: wonderful book. The four financial measures here, including their for-
Line 1083: mulas, are drawn from Tockey’s book.
Line 1084: 
Line 1085: --- 페이지 140 ---
Line 1086: Discussion Questions 
Line 1087: |
Line 1088: 109
Line 1089: Summary
Line 1090: Financial analysis of themes helps in prioritization because for most organiza-
Line 1091: tions the bottom line is the amount of money earned or saved. It is usually suffi-
Line 1092: cient to forecast revenue and operational efficiencies for the next two years. You
Line 1093: can look further ahead, however, if necessary.
Line 1094: A good way of modeling the return from a theme is to consider the revenue
Line 1095: it will generate from new customers, from current customers buying more cop-
Line 1096: ies or additional services, from customers who might have otherwise gone to a
Line 1097: competitive product, and from any operational efficiencies it will provide. 
Line 1098: Money earned or spent today is worth more than money earned or spent in
Line 1099: the future. To compare a current amount with a future amount, the future
Line 1100: amount is discounted back into a current amount. The current amount is the
Line 1101: amount that could be deposited in a bank or into some other relatively safe in-
Line 1102: vestment and that would grow to the future amount by the future time.
Line 1103: Four good ways to evaluate a cash flow stream are net present value, internal
Line 1104: rate or return (return on investment), payback period, and discounted payback
Line 1105: period. By calculating these values for each theme, the product owner and team
Line 1106: can make intelligent decisions about the relative priorities of the themes.
Line 1107: Discussion Questions
Line 1108: 1. If your organization were choosing among the themes in Table 10.15, what
Line 1109: would be the most appropriate decision? Why?
Line 1110: 2. How would you model the return for a theme on your current project? Are
Line 1111: the suggested categories of new revenue, incremental revenue, retained rev-
Line 1112: enue, and operational efficiencies appropriate? What categories would you
Line 1113: use instead? 
Line 1114: 
Line 1115: --- 페이지 141 ---
Line 1116: This page intentionally left blank 