Line 1: 
Line 2: --- 페이지 110 ---
Line 3: 79
Line 4: Chapter 9
Line 5: Prioritizing Themes
Line 6: “The indispensable first step to getting what you want is this:
Line 7: Decide what you want.”
Line 8: —Ben Stein
Line 9: There is rarely, if ever, enough time to do everything. So we prioritize. The re-
Line 10: sponsibility for prioritizing is shared among the whole team, but the effort is led
Line 11: by the product owner. Unfortunately, it is generally difficult to estimate the value
Line 12: of small units of functionality, such as a single user story. To get around this, in-
Line 13: dividual user stories or features are aggregated into themes. Stories and themes
Line 14: are then prioritized relative to one another for the purpose of creating a release
Line 15: plan. Themes should be selected such that each defines a discrete set of user- or
Line 16: customer-valued functionality. For example, in developing the SwimStats web-
Line 17: site, we would have themes such as these:
Line 18: ◆Keep track of all personal records and let swimmers view them.
Line 19: ◆Allow coaches to assign swimmers to events optimally and predict the team
Line 20: score of a meet.
Line 21: ◆Allow coaches to enter practice activities and track practice distances swum.
Line 22: ◆Integrate with popular handheld computers for use at the pool.
Line 23: ◆Import and export data.
Line 24: ◆Allow officials to track event results and score a meet.
Line 25: 
Line 26: --- 페이지 111 ---
Line 27: 80
Line 28: |
Line 29: Chapter 9
Line 30: Prioritizing Themes
Line 31: Each of these themes has tangible value to the users of the software. And it
Line 32: would be possible to put a monetary value on each. With some research we could
Line 33: determine that support for handheld computers is likely to result in ¤150,000 of
Line 34: new sales. We could compare that with the expected ¤200,000 in new sales if the
Line 35: next version can be used for scoring a swim meet. We could then prioritize those
Line 36: themes. There is more to prioritizing, however, than simply considering the
Line 37: monetary return from each new set of features. 
Line 38: Factors in Prioritization
Line 39: Determining the value of a theme is difficult, and product owners on agile
Line 40: projects are often given the vague and mostly useless advice of “prioritize on
Line 41: business value.” This may be great advice at face value, but what is business
Line 42: value? To provide a more practical set of guidelines for prioritizing, in this chap-
Line 43: ter we will look at four factors that must be considered when prioritizing the de-
Line 44: velopment of new capabilities.
Line 45: 1. The financial value of having the features.
Line 46: 2. The cost of developing (and perhaps supporting) the new features.
Line 47: 3. The amount and significance of learning and new knowledge created by
Line 48: developing the features.
Line 49: 4. The amount of risk removed by developing the features.
Line 50: Because most projects are undertaken either to save or to make money, the
Line 51: first two factors often dominate prioritization discussions. However, proper con-
Line 52: sideration of the influence of learning and risk on the project is critical if we are
Line 53: to prioritize optimally.
Line 54: Value
Line 55: The first factor in prioritizing work is the financial value of the theme. How
Line 56: much money will the organization make or save by having the new features in-
Line 57: cluded in the theme? This alone is often what is meant when product owners are
Line 58: given the advice to “prioritize on business value.”
Line 59: Often, an ideal way to determine the value of a theme is to estimate its finan-
Line 60: cial impact over a period of time—usually the next few months, quarters, or pos-
Line 61: sibly years. This can be done if the product will be sold commercially, as, for
Line 62: example, a new word processor or a calculator with embedded software would
Line 63: 
Line 64: --- 페이지 112 ---
Line 65: Cost 
Line 66: |
Line 67: 81
Line 68: be. It can also be done for applications that will be used within the orgainzation
Line 69: developing them. Chapter 10, “Financial Prioritization,” describes various ap-
Line 70: proaches to estimating the financial value of themes. 
Line 71: It can be difficult to estimate the financial return on a theme. Doing so usu-
Line 72: ally involves estimating the number of new sales, the average value of a sale (in-
Line 73: cluding follow-on sales and maintenance agreements), the timing of sales
Line 74: increases, and so on. Because of the complexity in doing this, it is often useful to
Line 75: have an alternate method for estimating value. Because the value of a theme is
Line 76: related to the desirability of that theme to new and existing users, it is possible to
Line 77: use nonfinancial measures of desirability to represent value. This will be the sub-
Line 78: ject of Chapter 11, “Prioritizing Desirability.”
Line 79: Cost
Line 80: Naturally, the cost of a feature is a huge determinant in the overall priority of a
Line 81: feature. Many features seem wonderful until we learn their cost. An important,
Line 82: yet often overlooked, aspect of cost is that the cost can change over time. Adding
Line 83: support for internationalization today may take four weeks of effort; adding it in
Line 84: six months may take six weeks. So we should add it now, right? Maybe. Suppose
Line 85: we spend four weeks and do it now. Over the next six months, we may spend an
Line 86: additional three weeks changing the original implementation based on knowl-
Line 87: edge gained during that six months. In that case, we would have been better off
Line 88: waiting. Or what if we spend four weeks now and later discover that a simpler
Line 89: and faster implementation would have been adequate? The best way to reduce
Line 90: the cost of change is to implement a feature as late as possible—effectively when
Line 91: there is no more time for change.
Line 92: Themes often seem worthwhile when viewed only in terms of the time they
Line 93: will take. As trite as it sounds, it is important to remember that time costs
Line 94: money. Often, the best way to do this while prioritizing is to do a rough conver-
Line 95: sion of story points or ideal days into money. Suppose you add up the salaries for
Line 96: everyone involved in a project over the past twelve weeks and come up with
Line 97: ¤150,000. This includes the product owner and the project manager, as well as
Line 98: all of the programmers, testers, database engineers, analysts, user interface de-
Line 99: signers, and so on. During those twelve weeks, the team completed 120 story
Line 100: points. We can tell that at a total cost of ¤150,000, 120 story points cost ¤1,250
Line 101: each. Suppose a product owner is trying to decide whether thirty points of func-
Line 102: tionality should be included in the next release. One way for her to decide is to
Line 103: ask herself whether the new functionality is worth an investment of ¤37,500
Line 104: (
Line 105: ).
Line 106: 30
Line 107: 1,250
Line 108: u
Line 109: 37,500
Line 110: =
Line 111: 
Line 112: --- 페이지 113 ---
Line 113: 82
Line 114: |
Line 115: Chapter 9
Line 116: Prioritizing Themes
Line 117: Chapter 10, “Financial Prioritization,” will have much more to say about
Line 118: cost and about prioritizing based on financial reward relative to cost.
Line 119: New Knowledge
Line 120: On many projects, much of the the overall effort is spent in the pursuit of new
Line 121: knowledge. It is important that this effort be acknowledged and considered fun-
Line 122: damental to the project. Acquiring new knowledge is important because at the
Line 123: start of a project, we never know everything that we’ll need to know by the end of
Line 124: the project. The knowledge that a team develops can be classified into two areas:
Line 125: ◆Knowledge about the product
Line 126: ◆Knowledge about the project
Line 127: Product knowledge is knowledge about what will be developed. It is knowl-
Line 128: edge about the features that will be included and about those that will not be in-
Line 129: cluded. The more product knowledge a team has, the better able they will be to
Line 130: make decisions about the nature and features of the product. 
Line 131: Project knowledge, by contrast, is knowledge about how the product will be
Line 132: created. Examples include knowledge about the technologies that will be used,
Line 133: about the skills of the developers, about how well the team functions together,
Line 134: and so on. 
Line 135: The flip side of acquiring knowledge is reducing uncertainty. At the start of
Line 136: a project there is some amount of uncertainty about what features the new prod-
Line 137: uct should contain. There is also uncertainty about how we’ll build the product.
Line 138: Laufer (1996) refers to these types of uncertainty as end uncertainty and means
Line 139: uncertainty. End uncertainty is reduced by acquiring more knowledge about the
Line 140: product; means uncertainty is reduced through acquiring more knowledge
Line 141: about the project. 
Line 142: A project following a waterfall process tries to eliminate all uncertainty
Line 143: about what is being built before tackling the uncertainty of how it will be built.
Line 144: This is the origin of the common advice that analysis is about what will be built,
Line 145: and design is about how it will be built. Figure 9.1 shows both the waterfall and
Line 146: agile views of removing uncertainty.
Line 147: On the waterfall side of Figure 9.1, the downward arrow shows a traditional
Line 148: team’s attempt to eliminate all end uncertainty at the start of the project. This
Line 149: means that before they begin developing, there will be no remaining uncertainty
Line 150: about the end that is being pursued. The product is fully defined. The rightward
Line 151: arrow on the waterfall side of Figure 9.1 shows that means uncertainty (about
Line 152: 
Line 153: --- 페이지 114 ---
Line 154: New Knowledge 
Line 155: |
Line 156: 83
Line 157: how the product will be built) is reduced over time as the project progresses. Of
Line 158: course, the complete up-front elimination of all end uncertainty is unachievable.
Line 159: Customers and users are uncertain about exactly what they need until they be-
Line 160: gin to see parts of it. They can then successively elaborate their needs.
Line 161: Contrast this view with the agile approach to reducing uncertainty, which is
Line 162: shown on the right side of Figure 9.1. Agile teams acknowledge that it is impos-
Line 163: sible at the start of a project to eliminate all uncertainty about what the product
Line 164: is to be. Parts of the product need to be developed and shown to customers, feed-
Line 165: back needs to collected, opinions refined, and plans adjusted. This takes time.
Line 166: While this is occuring the team will also be learning more about how they will
Line 167: develop the system. This leads to simultaneously reducing both end and means
Line 168: uncertainty, as shown in the agile view in Figure 9.1.
Line 169: Figure 9.1 Traditional and agile views of reducing uncertainty. Adapted from Laufer 
Line 170: (1996).
Line 171: I’ve drawn the curve in the agile side of Figure 9.1 to show a preference to-
Line 172: ward early reduction of end uncertainty. Why didn’t I draw a straight line or one
Line 173: that favors early reduction of means uncertainty? I drew the line as I did to re-
Line 174: flect the importance of reducing uncertainty about what a product should be as
Line 175: early as possible. End uncertainty does not need to be eliminated at the outset
Line 176: (as hoped for in the traditional view), and it cannot be. However, one of the
Line 177: greatest risks to most projects is the risk of building the wrong product. This
Line 178: risk can be dramatically reduced by developing early those features that will best
Line 179: allow us to get working software in front of or in the hands of actual users.
Line 180: High
Line 181: Low
Line 182: Low
Line 183: High
Line 184: Means Uncertainty
Line 185: (How)
Line 186: Waterfall
Line 187: End Uncertainty
Line 188: (What)
Line 189: Means Uncertainty
Line 190: (How)
Line 191: High
Line 192: Low
Line 193: Low
Line 194: High
Line 195: Agile
Line 196: End Uncertainty
Line 197: (What)
Line 198: 
Line 199: --- 페이지 115 ---
Line 200: 84
Line 201: |
Line 202: Chapter 9
Line 203: Prioritizing Themes
Line 204: Risk
Line 205: Closely aligned with the concept of new knowledge is the final factor in prioriti-
Line 206: zation: risk. Almost all projects contain tremendous amounts of risk. For our
Line 207: purposes, a risk is anything that has not yet happened but might and that would
Line 208: jeopardize or limit the success of the project. There are many different types of
Line 209: risk on projects, including:
Line 210: ◆Schedule risk (“We might not be done by October”)
Line 211: ◆Cost risk (“We might not be able to buy hardware for the right price”)
Line 212: ◆Functionality risk (“We might not be able to get that to work”)
Line 213: Additionally, risks can be classified as either technological or business risks. 
Line 214: A classic struggle exists between the high-risk and the high-value features of
Line 215: a project. Should a project team start by focusing on high-risk features that
Line 216: could derail the entire project? Or should a project team focus on what Tom Gilb
Line 217: (1988) called the “juicy bits,” the high-value features that will deliver the most
Line 218: immediate bang for the customer’s buck? 
Line 219: To choose among them, let’s consider the drawbacks of each approach. The
Line 220: risk-driven team accepts the chance that work they perform will turn out to be
Line 221: unneeded or of low value. They may develop infrastructural support for features
Line 222: that turn out unnecessary as the product owner refines her vision of the project
Line 223: based on what she learns from users as the project progresses. On the other
Line 224: hand, a team that focuses on value to the exclusion of risk may develop a signifi-
Line 225: cant amount of an application before hitting a risk that jeopardizes the delivery
Line 226: of the product.
Line 227: The solution, of course, is to give neither risk nor value total supremacy
Line 228: when prioritizing. To prioritize work optimally, it is important to consider both
Line 229: risk and value. Consider Figure 9.2, which maps the relationship between the
Line 230: risk and value of a feature into four quadrants. At the top right are high-risk,
Line 231: high-value features. These features are highly desirable to the customer but pos-
Line 232: sess significant development risk. Perhaps features in this quadrant rely on un-
Line 233: proven technologies, integration with unproven subcontractors, technical
Line 234: innovation (such as the development of a new algorithm), or any of a number of
Line 235: similar risks. At the bottom right are features that are equally desirable but that
Line 236: are less risky. Whereas features in the right half of Figure 9.2 are highly desir-
Line 237: able, features falling in the left half are of lower value.
Line 238: 
Line 239: --- 페이지 116 ---
Line 240: Risk 
Line 241: |
Line 242: 85
Line 243: Figure 9.2 The four quadrants of the risk–value relationship.
Line 244: The appropriate development sequence for the features is shown in
Line 245: Figure 9.3. The high-value, high-risk features should be developed first. These
Line 246: features deliver the most value, and working on them eliminates significant
Line 247: risks. Next are the high-value, low-risk features. These features offer as much
Line 248: value as the first set, but they are less risky. Therefore, they can be done later in
Line 249: the schedule. Because of this, use the guideline to work first on high-value fea-
Line 250: tures, but use risk as a tie-breaker.
Line 251: Figure 9.3 Combining risk and value in prioritizing features.
Line 252: Next are the low-value, low-risk features. These are sequenced third because
Line 253: they will have less impact on the total value of the product if they are dropped,
Line 254: and because they are low risk. 
Line 255: Finally, features that deliver low value, but are high risk, are best avoided.
Line 256: Defer work on all low-value features, especially those that are also high risk. Try
Line 257: Risk
Line 258: Low
Line 259: High
Line 260: High risk
Line 261: Low value
Line 262: High risk
Line 263: High value
Line 264: Low risk
Line 265: Low value
Line 266: Low risk
Line 267: High value
Line 268: Value
Line 269: Low
Line 270: High
Line 271: Risk
Line 272: Low
Line 273: High
Line 274: Avoid
Line 275: Do first
Line 276: Do last
Line 277: Do second
Line 278: Value
Line 279: Low
Line 280: High
Line 281: 
Line 282: --- 페이지 117 ---
Line 283: 86
Line 284: |
Line 285: Chapter 9
Line 286: Prioritizing Themes
Line 287: to defer low-value, high-risk items right out of the project. There is no reason to
Line 288: take on a high degree of risk for a feature of limited value. Be aware that a fea-
Line 289: ture’s risk and value profile changes over time. A low-value, low-risk feature in
Line 290: the Avoid quadrant of Figure 9.3 today could be in the Do first quadrant six
Line 291: months from now if all other features have been finished.
Line 292: Combining the Four Factors
Line 293: To combine the four prioritiziaton factors, think first about the value of the fea-
Line 294: ture relative to what it would cost to develop today. This gives you an initial pri-
Line 295: ority order for the themes. Those themes with a high value-to-cost ratio are
Line 296: those that should be done first. 
Line 297: Next, think of the other prioritization factors as moving themes forward or
Line 298: backward. Suppose that based on its value and cost, a theme is of medium prior-
Line 299: ity. Therefore, the team would tend to work on this theme midway through the
Line 300: current release. However, the technology needed to develop this story is very
Line 301: risky. This would move the theme forward in priority and on the schedule. 
Line 302: It’s not necessary that this initial ranking followed by shifting forward and
Line 303: back be a formal activity. It can (and often does) take place entirely in the head of
Line 304: the product owner. The product owner will then typically present her priorities
Line 305: to the team, who may entreat the product owner to alter priorities slightly based
Line 306: on its assessment of the themes.
Line 307: Some Examples
Line 308: To make sure that these four prioritization factors are practical and useful, let’s
Line 309: see how they can be applied to two typical prioritization challenges: infrastruc-
Line 310: ture and user interface design. In the following sections, I’ll consider a theme
Line 311: and show how these prioritization factors can be applied.
Line 312: Infrastructure
Line 313: One common prioritization challenge comes in the form of developing the infra-
Line 314: structure or architectural elements of an application. As an example, consider a
Line 315: security framework that will be used throughout an application. Considered
Line 316: solely on the merits of the value it delivers to customers, a security framework is
Line 317: unlikely to be prioritized into the early iterations of a project. After all, even
Line 318: though security is critical to many applications, most applications are not
Line 319: 
Line 320: --- 페이지 118 ---
Line 321: User Interface Design 
Line 322: |
Line 323: 87
Line 324: generally purchased solely because of how secure they are. The application must
Line 325: do something before security is relevant.
Line 326: The next prioritization factor is cost. Adding a security framework to our
Line 327: website today will probably cost less than adding the same security framework
Line 328: later. This is true for many infrastructure elements, and is the basis for many ar-
Line 329: guments in favor of developing them early. However, if a feature is developed
Line 330: early, there is a chance that it will change by the end of the project. The cost of
Line 331: these changes needs to be considered in any now/later decision. Additionally, in-
Line 332: troducing the security framework early may add complexity that will be a hidden
Line 333: cost on all future work. This cost, too, would need to be considered.
Line 334: Our next factor says that we should accelerate the development of features
Line 335: that generate new product or project knowledge. Depending upon the product
Line 336: being built, a security framework is unlikely to generate relevant new knowledge
Line 337: about the product. However, developing the security framework may generate
Line 338: new knowledge about the project. For example, I worked on a project a handful
Line 339: of years ago that needed to authenticate users through an LDAP server. None of
Line 340: the developers had done this before, so there was a lot of uncertainty about how
Line 341: much effort it would take. To eliminate that uncertainty, the stories about LDAP
Line 342: authentication were moved up to around the middle of a project rather than be-
Line 343: ing left near the end.
Line 344: The final prioritization factor is risk. Is there a risk to the project’s success
Line 345: that could be reduced or eliminated by implementing security earlier rather
Line 346: than later? Perhaps not in this example. However, the failure of a framework, key
Line 347: component, or other infrastructure is often a significant risk to a project. This
Line 348: may be enough to warrant moving development sooner than would be justified
Line 349: solely on the basis of value.
Line 350: User Interface Design
Line 351: Common agile advice is that user interface design should be done entirely within
Line 352: the iteration in which the underlying feature is developed. However, this some-
Line 353: times runs counter to arguments that the usability of a system is improved when
Line 354: designers are allowed to think about the overall user interface up front. What
Line 355: can we learn from applying our prioritization factors?
Line 356: First, will the development of the user interface generate significant, useful
Line 357: new knowledge? If so, we should move some of the work forward in the schedule.
Line 358: Yes, in many cases developing some of the main user interface components or
Line 359: the navigational model will generate significant, useful new knowledge about
Line 360: the product. The early development of parts of the user interface allows for the
Line 361: 
Line 362: --- 페이지 119 ---
Line 363: 88
Line 364: |
Line 365: Chapter 9
Line 366: Prioritizing Themes
Line 367: system to be shown to real or likely users in an early form. Feedback from these
Line 368: users will result in new knowledge about the product, and this knowledge can be
Line 369: used to make sure the team is developing the most valuable product possible. 
Line 370: Second, will developing the user interface reduce risk? It probably doesn’t
Line 371: eliminate technical risk (unless this is the team’s first endeavor with this type of
Line 372: user interface). However, early development of features that show off the user in-
Line 373: terface often reduces the most serious risk facing most projects: the risk of de-
Line 374: veloping the wrong product. A high prioritization of features that will show off
Line 375: significant user-facing functionality will allow for more early feedback from us-
Line 376: ers. This is the best way of avoiding the risk of building the wrong product. 
Line 377: Finally, if the cost of developing the user interface will be significantly lower
Line 378: if done early, that would be another point in favor of scheduling such features
Line 379: early. In most cases, this is not the case.
Line 380: So because of the additional learning and risk reduction that can be had, it
Line 381: seems reasonable to move earlier in the schedule those themes that will allow
Line 382: users to provide the most feedback on the usability and functionality of the sys-
Line 383: tem. This does not mean that we would work on the user interface in isolation or
Line 384: separate from the functionality that exists beneath the user interface. Rather,
Line 385: this means that it might be appropriate to move forward in the schedule those
Line 386: features with significant user interface components that would allow us to get
Line 387: the most useful feedback from customers and users.
Line 388: Summary
Line 389: Because there is rarely enough time to do everything, we need to prioritize what
Line 390: is worked on first. There are four primary factors to be considered when priori-
Line 391: tizing.
Line 392: 1. The financial value of having the features.
Line 393: 2. The cost of developing (and perhaps supporting) the new features.
Line 394: 3. The amount and significance of learning and new knowledge created by
Line 395: developing the features.
Line 396: 4. The amount of risk removed by developing the features.
Line 397: These factors are combined by thinking first of the value and cost of the
Line 398: theme. Doing so sorts the themes into an initial order. Themes can then be
Line 399: moved forward or back in this order based on the other factors. 
Line 400: 
Line 401: --- 페이지 120 ---
Line 402: Discussion Questions 
Line 403: |
Line 404: 89
Line 405: Discussion Questions
Line 406: 1. A feature on the project to which you have been assigned is of fairly low pri-
Line 407: ority. Right now it looks like it will make it into the current release, but it
Line 408: could be dropped if time runs out. The feature needs to be developed in a
Line 409: language no one on the team has any familiarity with. What do you do?
Line 410: 2. What types of product and project knowledge have your current team ac-
Line 411: quired since beginning the project? Is there additional knowledge that needs
Line 412: to be acquired quickly and that should be accounted for in the project’s
Line 413: priorities?
Line 414: 
Line 415: --- 페이지 121 ---
Line 416: This page intentionally left blank 