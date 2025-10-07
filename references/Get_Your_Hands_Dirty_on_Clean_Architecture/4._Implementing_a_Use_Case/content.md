Line 1: 
Line 2: --- 페이지 32 ---
Line 3: 4. Implementing a Use Case
Line 4: Let’s finally look at how we can manifest the architecture we have discussed in actual code.
Line 5: Since the application, web and persistence layers are so loosely coupled in our architecture, we’re
Line 6: totally free to model our domain code as we see fit. We can do DDD, we can implement a rich or an
Line 7: anemic domain model, or invent our own way of doing things.
Line 8: This chapter describes an opinionated way of implementing use cases within the hexagonal
Line 9: architecture style we have introduced in the previous chapters.
Line 10: As is fitting for a domain-centric architecture, we’ll start with a domain entity and then build a use
Line 11: case around it.
Line 12: Implementing the Domain Model
Line 13: We want to implement the use case of sending money from one account to another. One way to
Line 14: model this in object-oriented fashion is to create an Account entity that allows to withdraw and
Line 15: deposit money, so that we can withdraw money from the source account and deposit it to the target
Line 16: account:
Line 17: 1
Line 18: package buckpal.domain;
Line 19: 2
Line 20: 3
Line 21: public class Account {
Line 22: 4
Line 23: 5
Line 24: private AccountId id;
Line 25: 6
Line 26: private Money baselineBalance;
Line 27: 7
Line 28: private ActivityWindow activityWindow;
Line 29: 8
Line 30: 9
Line 31: // constructors and getters omitted
Line 32: 10
Line 33: 11
Line 34: public Money calculateBalance() {
Line 35: 12
Line 36: return Money.add(
Line 37: 13
Line 38: this.baselineBalance,
Line 39: 14
Line 40: this.activityWindow.calculateBalance(this.id));
Line 41: 15
Line 42: }
Line 43: 16
Line 44: 17
Line 45: public boolean withdraw(Money money, AccountId targetAccountId) {
Line 46: 18
Line 47: 19
Line 48: if (!mayWithdraw(money)) {
Line 49: 
Line 50: --- 페이지 33 ---
Line 51: 4. Implementing a Use Case
Line 52: 27
Line 53: 20
Line 54: return false;
Line 55: 21
Line 56: }
Line 57: 22
Line 58: 23
Line 59: Activity withdrawal = new Activity(
Line 60: 24
Line 61: this.id,
Line 62: 25
Line 63: this.id,
Line 64: 26
Line 65: targetAccountId,
Line 66: 27
Line 67: LocalDateTime.now(),
Line 68: 28
Line 69: money);
Line 70: 29
Line 71: this.activityWindow.addActivity(withdrawal);
Line 72: 30
Line 73: return true;
Line 74: 31
Line 75: }
Line 76: 32
Line 77: 33
Line 78: private boolean mayWithdraw(Money money) {
Line 79: 34
Line 80: return Money.add(
Line 81: 35
Line 82: this.calculateBalance(),
Line 83: 36
Line 84: money.negate())
Line 85: 37
Line 86: .isPositive();
Line 87: 38
Line 88: }
Line 89: 39
Line 90: 40
Line 91: public boolean deposit(Money money, AccountId sourceAccountId) {
Line 92: 41
Line 93: Activity deposit = new Activity(
Line 94: 42
Line 95: this.id,
Line 96: 43
Line 97: sourceAccountId,
Line 98: 44
Line 99: this.id,
Line 100: 45
Line 101: LocalDateTime.now(),
Line 102: 46
Line 103: money);
Line 104: 47
Line 105: this.activityWindow.addActivity(deposit);
Line 106: 48
Line 107: return true;
Line 108: 49
Line 109: }
Line 110: 50
Line 111: 51
Line 112: }
Line 113: The Account entity provides the current snapshot of an actual account. Every withdrawal from and
Line 114: deposit to an account is captured in an Activity entity. Since it would not be wise to always load all
Line 115: activities of an account into memory, the Account entity only holds a window of the last few days
Line 116: or weeks of activities, captured in the ActivityWindow value object.
Line 117: To still be able to calculate the current account balance, the Account entity additionally has the
Line 118: attribute baselineBalance, representing the balance the account had just before the first activity of
Line 119: the activity window. The total balance then is the baseline balance plus the balance of all activities
Line 120: in the window.
Line 121: With this model, withdrawing and depositing money to an account is a matter of adding a new
Line 122: 
Line 123: --- 페이지 34 ---
Line 124: 4. Implementing a Use Case
Line 125: 28
Line 126: activity to the activity window, as is done in the withdraw() and deposit() methods. Before we can
Line 127: withdraw, we check the business rule that says that we cannot overdraw an account.
Line 128: Now that we have an Account that allows us to withdraw and deposit money, we can move outward
Line 129: to build a use case around it.
Line 130: A Use Case in a Nutshell
Line 131: First, let’s discuss what a use case actually does. Usually, it follows these steps:
Line 132: 1. Take input
Line 133: 2. Validate business rules
Line 134: 3. Manipulate model state
Line 135: 4. Return output
Line 136: A use case takes input from an incoming adapter. You might wonder why I didn’t call this step
Line 137: “Validate input”. The answer is that I believe use case code should care about the domain logic and
Line 138: we shouldn’t pollute it with input validation. So, we’ll do input validation somewhere else, as we’ll
Line 139: see shortly.
Line 140: The use case is, however, responsible for validating business rules. It shares this responsibility
Line 141: with the domain entities. We’ll discuss the distinction between input validation and business rule
Line 142: validation later in this chapter.
Line 143: If the business rules were satisfied, the use case then manipulates the state of the model in one way
Line 144: or another, based on the input. Usually, it will change the state of a domain object and pass this new
Line 145: state to a port implemented by the persistence adapter to be persisted. A use case might also call
Line 146: any other outgoing adapter, though.
Line 147: The last step is to translate the return value from the outgoing adapter into an output object which
Line 148: will be returned to the calling adapter.
Line 149: With these steps in mind, let’s see how we can implement our “Send Money” use case.
Line 150: To avoid the problem of broad services discussed in chapter 1 “What’s Wrong with Layers?”, we’ll
Line 151: create a separate service class for each use case instead of putting all use cases into a single service
Line 152: class.
Line 153: Here’s a teaser:
Line 154: 
Line 155: --- 페이지 35 ---
Line 156: 4. Implementing a Use Case
Line 157: 29
Line 158: 1
Line 159: package buckpal.application.service;
Line 160: 2
Line 161: 3
Line 162: @RequiredArgsConstructor
Line 163: 4
Line 164: @Transactional
Line 165: 5
Line 166: public class SendMoneyService implements SendMoneyUseCase {
Line 167: 6
Line 168: 7
Line 169: private final LoadAccountPort loadAccountPort;
Line 170: 8
Line 171: private final AccountLock accountLock;
Line 172: 9
Line 173: private final UpdateAccountStatePort updateAccountStatePort;
Line 174: 10
Line 175: 11
Line 176: @Override
Line 177: 12
Line 178: public boolean sendMoney(SendMoneyCommand command) {
Line 179: 13
Line 180: // TODO: validate business rules
Line 181: 14
Line 182: // TODO: manipulate model state
Line 183: 15
Line 184: // TODO: return output
Line 185: 16
Line 186: }
Line 187: 17
Line 188: }
Line 189: The service implements the incoming port interface SendMoneyUseCase and calls the outgoing port
Line 190: interface LoadAccountPort to load an account and the port UpdateAccountStatePort to persist
Line 191: an updated account state in the database. Figure 11 gives a graphical overview of the relevant
Line 192: components.
Line 193: Figure 11 - A service implements a use case, modifies the domain model and calls an outgoing port to persist the
Line 194: modified state.
Line 195: Let’s take care of those // TODOs we left in the code above.
Line 196: 
Line 197: --- 페이지 36 ---
Line 198: 4. Implementing a Use Case
Line 199: 30
Line 200: Validating Input
Line 201: Now we’re talking about validating input, even though I just claimed that it’s not a responsibility of
Line 202: a use case class. I still think, however, that it belongs into the application layer, so this is the place
Line 203: to discuss it.
Line 204: Why not let the calling adapter validate the input before sending it to the use case? Well, do we
Line 205: want to trust the caller to have validated everything as is needed for the use case? Also, the use case
Line 206: might be called by more than one adapter, so the validation would have to be implemented by each
Line 207: adapter and one might get it wrong or forget it altogether.
Line 208: The application layer should care about input validation because, well, otherwise it might get invalid
Line 209: input from outside the application core. And this might cause damage to the state of our model.
Line 210: But where to put the input validation, if not in the use case class?
Line 211: We’ll let the input model take care of it. For the “Send Money” use case, the input model is the
Line 212: SendMoneyCommand class we have already seen in the previous code example. More precisely, we’ll
Line 213: do it within the constructor:
Line 214: 1
Line 215: package buckpal.application.port.in;
Line 216: 2
Line 217: 3
Line 218: @Getter
Line 219: 4
Line 220: public class SendMoneyCommand {
Line 221: 5
Line 222: 6
Line 223: private final AccountId sourceAccountId;
Line 224: 7
Line 225: private final AccountId targetAccountId;
Line 226: 8
Line 227: private final Money money;
Line 228: 9
Line 229: 10
Line 230: public SendMoneyCommand(
Line 231: 11
Line 232: AccountId sourceAccountId,
Line 233: 12
Line 234: AccountId targetAccountId,
Line 235: 13
Line 236: Money money) {
Line 237: 14
Line 238: this.sourceAccountId = sourceAccountId;
Line 239: 15
Line 240: this.targetAccountId = targetAccountId;
Line 241: 16
Line 242: this.money = money;
Line 243: 17
Line 244: requireNonNull(sourceAccountId);
Line 245: 18
Line 246: requireNonNull(targetAccountId);
Line 247: 19
Line 248: requireNonNull(money);
Line 249: 20
Line 250: requireGreaterThan(money, 0);
Line 251: 21
Line 252: }
Line 253: 22
Line 254: }
Line 255: For sending money, we ned the IDs of the source and target account and the amount of money that
Line 256: is to be transferred. None of the parameters must be null and the amount must be greater than zero.
Line 257: 
Line 258: --- 페이지 37 ---
Line 259: 4. Implementing a Use Case
Line 260: 31
Line 261: If any of these conditions is violated, we simply refuse object creation by throwing an exception
Line 262: during construction.
Line 263: By making the fields of SendMoneyCommand final, we effectively make it immutable. So, once
Line 264: constructed successfully, we can be sure that the state is valid and cannot be changed to something
Line 265: invalid.
Line 266: Since SendMoneyCommand is part of the use cases’ API, it’s located in the incoming port package.
Line 267: Thus, the validation remains in the core of the application (within the hexagon of our hexagonal
Line 268: architecture) but does not pollute the sacred use case code.
Line 269: But do we really want to implement each validation check by hand when there are tools that can
Line 270: do the dirty work for us? In the Java world, the de-facto standard for this kind of work is the Bean
Line 271: Validation API¹⁷. It allows us to express the validation rules we need as annotations on the fields of
Line 272: a class:
Line 273: 1
Line 274: package buckpal.application.port.in;
Line 275: 2
Line 276: 3
Line 277: @Getter
Line 278: 4
Line 279: public class SendMoneyCommand extends SelfValidating<SendMoneyCommand> {
Line 280: 5
Line 281: 6
Line 282: @NotNull
Line 283: 7
Line 284: private final AccountId sourceAccountId;
Line 285: 8
Line 286: @NotNull
Line 287: 9
Line 288: private final AccountId targetAccountId;
Line 289: 10
Line 290: @NotNull
Line 291: 11
Line 292: private final Money money;
Line 293: 12
Line 294: 13
Line 295: public SendMoneyCommand(
Line 296: 14
Line 297: AccountId sourceAccountId,
Line 298: 15
Line 299: AccountId targetAccountId,
Line 300: 16
Line 301: Money money) {
Line 302: 17
Line 303: this.sourceAccountId = sourceAccountId;
Line 304: 18
Line 305: this.targetAccountId = targetAccountId;
Line 306: 19
Line 307: this.money = money;
Line 308: 20
Line 309: requireGreaterThan(money, 0);
Line 310: 21
Line 311: this.validateSelf();
Line 312: 22
Line 313: }
Line 314: 23
Line 315: }
Line 316: The abstract class SelfValidating provides the method validateSelf() which we simply call as the
Line 317: last statement in the constructor. This will evaluate the Bean Validation annotations on the fields
Line 318: (@NotNull, in this case) and throw an exception in case of a violation. In case Bean Validation is not
Line 319: ¹⁷https://beanvalidation.org/
Line 320: 
Line 321: --- 페이지 38 ---
Line 322: 4. Implementing a Use Case
Line 323: 32
Line 324: expressive enough for a certain validation, we can still implement it by hand, as we did for checking
Line 325: the amount is greater than zero.
Line 326: The implementation of the SelfValidating class might look like this:
Line 327: 1
Line 328: package shared;
Line 329: 2
Line 330: 3
Line 331: public abstract class SelfValidating<T> {
Line 332: 4
Line 333: 5
Line 334: private Validator validator;
Line 335: 6
Line 336: 7
Line 337: public SelfValidating(){
Line 338: 8
Line 339: ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
Line 340: 9
Line 341: validator = factory.getValidator();
Line 342: 10
Line 343: }
Line 344: 11
Line 345: 12
Line 346: protected void validateSelf() {
Line 347: 13
Line 348: Set<ConstraintViolation<T>> violations = validator.validate((T) this);
Line 349: 14
Line 350: if (!violations.isEmpty()) {
Line 351: 15
Line 352: throw new ConstraintViolationException(violations);
Line 353: 16
Line 354: }
Line 355: 17
Line 356: }
Line 357: 18
Line 358: 19
Line 359: }
Line 360: With validation located in the input model we have effectively created an anti-corruption layer
Line 361: around our use case implementations. This is not a layer in the sense of a layered architecture,
Line 362: calling the next layer below, but instead a thin, protective screen around our use cases that bounces
Line 363: bad input back to the caller.
Line 364: The Power of Constructors
Line 365: Our input model above, SendMoneyCommand, puts a lot of responsibility to its constructor. Since the
Line 366: class is immutable, the constructor’s argument list contains a parameter for each attribute of the
Line 367: class. And since the constructor also validates the parameters, it’s not possible to create an object
Line 368: with invalid state.
Line 369: In our case, the constructor has only three parameters. What if we more parameters? Couldn’t we
Line 370: use the Builder pattern to make it more convenient to use? We could make the constructor with the
Line 371: long parameter list private and hide the call to it in the build() method of our builder. Then, instead
Line 372: of having to call a constructor with 20 parameters, we could build an object like this:
Line 373: 
Line 374: --- 페이지 39 ---
Line 375: 4. Implementing a Use Case
Line 376: 33
Line 377: 1
Line 378: new SendMoneyCommandBuilder()
Line 379: 2
Line 380: .sourceAccountId(new AccountId(41L))
Line 381: 3
Line 382: .targetAccountId(new AccountId(42L))
Line 383: 4
Line 384: // ... initialize many other fields
Line 385: 5
Line 386: .build();
Line 387: We could still let our constructor do the validation so that the builder cannot construct an object
Line 388: with invalid state.
Line 389: Sounds good? Think about what happens if we have to add another field to SendMoneyCommandBuilder
Line 390: (which will happen quite a few times in the lifetime of a software project). We add the new field
Line 391: to the constructor and to the builder. Then, a colleague (or a phone call, an email, a butterfly…)
Line 392: interrupts our train of thought. After the break we go back to coding and forget to add the new field
Line 393: to the code that calls the builder.
Line 394: We don’t get a word of warning from the compiler about trying to create an immutable object in
Line 395: an invalid state! Sure, at runtime - hopefully in a unit test - our validation logic will still kick in and
Line 396: throw an error because we missed a parameter.
Line 397: But if we use the constructor directly instead of hiding it behind a builder, each time a new field is
Line 398: added or an existing field is removed we can just follow the trail of compile errors to reflect that
Line 399: change in the rest of the codebase.
Line 400: Long parameter lists can even be formatted nicely and good IDEs help with parameter name hints:
Line 401: Figure 12 - The IDE shows parameter name hints in parameter lists to help us not to get lost.
Line 402: So why not let the compiler guide us?
Line 403: Different Input Models for Different Use Cases
Line 404: We might be tempted to use the same input model for different use cases. Let’s consider the use
Line 405: cases “Register Account” and “Update Account Details”. Both will initially need almost the same
Line 406: input, namely some account details like a description of the account.
Line 407: The difference is that the “Update Account Details” use case also needs the ID of the account to be
Line 408: able to update that specific account. And the “Register Account” use case might need the ID of the
Line 409: 
Line 410: --- 페이지 40 ---
Line 411: 4. Implementing a Use Case
Line 412: 34
Line 413: owner, so that it can assign it to him or her. So if we share the same input model between both use
Line 414: cases, we’d have to allow a null account ID being passed into the “Update Account Details” use case
Line 415: and a null owner ID being passed into the “Register Account” use case.
Line 416: Allowing null as a valid state of a field in our immutable command object is a code smell by itself.
Line 417: But more importantly, how are we handling input validation now? Validation has to be different
Line 418: for the register and update use cases, since each needs an id the other doesn’t. We’d have to build
Line 419: custom validation logic into the use cases themselves, polluting our sacred business code with input
Line 420: validation concerns.
Line 421: Also, what do we do if the account ID field accidentally has a non-null value in the “Register
Line 422: Account” use case? Do we throw an error? Do we simply ignore it? These are the questions the
Line 423: maintenance engineers - including future us - will ask when seeing the code.
Line 424: A dedicated input model for each use case makes the use case much clearer and also decouples it
Line 425: from other use cases, preventing unwanted side effects. It comes with a cost, however, because we
Line 426: have to map incoming data into different input models for different use cases. We’ll discuss this
Line 427: mapping strategy along with other mapping strategies in chapter 8 “Mapping Between Boundaries”.
Line 428: Validating Business Rules
Line 429: While validating input is not part of the use case logic, validating business rules definitely is. Business
Line 430: rules are the core of the application and should be handled with appropriate care. But when are we
Line 431: dealing with input validation and when with a business rule?
Line 432: A very pragmatic distinction between the two is that validating a business rule requires access
Line 433: to the current state of the domain model while validating input does not. Input validation can be
Line 434: implemented declaratively, like we did with the @NotNull annotations above, while a business rule
Line 435: needs more context.
Line 436: We might also say that input validation is a syntactical validation, while a business rule is a
Line 437: semantical validation in the context of a use case.
Line 438: Let’s take the rule “the source account must not be overdrawn”. By the definition above, this is a
Line 439: business rule since it needs access to the current state of the model to check if the source and target
Line 440: accounts do exist.
Line 441: In contrast, the rule “the transfer amount must be greater than zero” can be validated without access
Line 442: to the model and thus can be implemented as part of the input validation.
Line 443: I’m aware that this distinction may be subject to debate. You might argue that the transfer amount
Line 444: is so important that validating it should be considered a business rule in any case.
Line 445: The distinction above helps us, however, to place certain validations within the codebase and easily
Line 446: find them again later on. It’s as simple as answering the question if the validation needs access to
Line 447: the current model state or not. This not only helps us to implement the rule in the first place, but it
Line 448: also helps the future maintenance engineer to find it again.
Line 449: 
Line 450: --- 페이지 41 ---
Line 451: 4. Implementing a Use Case
Line 452: 35
Line 453: So, how do we implement a business rule?
Line 454: The best way is to do put the business rules into a domain entity as we did for the rule “the source
Line 455: account must not be overdrawn”:
Line 456: 1
Line 457: package buckpal.domain;
Line 458: 2
Line 459: 3
Line 460: public class Account {
Line 461: 4
Line 462: 5
Line 463: // ...
Line 464: 6
Line 465: 7
Line 466: public boolean withdraw(Money money, AccountId targetAccountId) {
Line 467: 8
Line 468: if (!mayWithdraw(money)) {
Line 469: 9
Line 470: return false;
Line 471: 10
Line 472: }
Line 473: 11
Line 474: // ...
Line 475: 12
Line 476: }
Line 477: 13
Line 478: }
Line 479: This way, the business rule is easy to locate and reason about, because it’s right next to the business
Line 480: logic that requires this rule to be honored.
Line 481: If it’s not feasible to validate a business rule in a domain entity, we can simply do it in the use case
Line 482: code before it starts working on the domain entities:
Line 483: 1
Line 484: package buckpal.application.service;
Line 485: 2
Line 486: 3
Line 487: @RequiredArgsConstructor
Line 488: 4
Line 489: @Transactional
Line 490: 5
Line 491: public class SendMoneyService implements SendMoneyUseCase {
Line 492: 6
Line 493: 7
Line 494: // ...
Line 495: 8
Line 496: 9
Line 497: @Override
Line 498: 10
Line 499: public boolean sendMoney(SendMoneyCommand command) {
Line 500: 11
Line 501: requireAccountExists(command.getSourceAccountId());
Line 502: 12
Line 503: requireAccountExists(command.getTargetAccountId());
Line 504: 13
Line 505: ...
Line 506: 14
Line 507: }
Line 508: 15
Line 509: }
Line 510: We simply call a method that does the actual validation and throws a dedicated exception in the
Line 511: case that this validation fails. The adapter interfacing with the user can then display this exception
Line 512: to the user as an error message or handle it any other way it seems fit.
Line 513: 
Line 514: --- 페이지 42 ---
Line 515: 4. Implementing a Use Case
Line 516: 36
Line 517: In the case above, the validation simply checks if the source and target accounts actually exist in the
Line 518: database. More complex business rules might require us to load the domain model from the database
Line 519: first and then do some checks on its state. If we have to load the domain model anyways, we should
Line 520: implement the business rule in the domain entities themselves, like we did with the rule “the source
Line 521: account must not be overdrawn” above.
Line 522: Rich vs. Anemic Domain Model
Line 523: Our architecture style leaves open how to implement our domain model. This is a blessing, because
Line 524: we can do what seems right in our context, and a curse, because we don’t have any guidelines to
Line 525: help us.
Line 526: A frequent discussion is whether to implement a rich domain model following the DDD philosophy
Line 527: or an “anemic” domain model. I’m not going to favor one of the two, but let’s discuss how each of
Line 528: those fits into our architecture.
Line 529: In a rich domain model, as much of the domain logic as possible is implemented within the entities
Line 530: at the core of the application. The entities provide methods to change state and only allow changes
Line 531: that are valid according to the business rules. This is the way we pursued with the Account entity
Line 532: above. Where is our use case implementation in this scenario?
Line 533: In this case, our use case serves as an entry point to the domain model. A use case then only
Line 534: represents the intent of the user and translates it into orchestrated method calls to the domain
Line 535: entities which do the actual work. Many of the business rules are located in the entities instead
Line 536: of the use case implementation.
Line 537: The “Send Money” use case service would load the source and target account entities, call their
Line 538: withdraw() and deposit() methods, and send them back to the database¹⁸.
Line 539: In an “anemic” domain model, the entities themselves are very thin. They usually only provide fields
Line 540: to hold the state and getter and setter methods to read and change it. They don’t contain any domain
Line 541: logic.
Line 542: This means that the domain logic is implemented in the use case classes. They are responsible to
Line 543: validate business rules, to change the state of the entities and pass them into the outgoing ports
Line 544: responsible for storing them in the database. The “richness” is contained within the use cases instead
Line 545: of the entities.
Line 546: Both styles, and any number of other styles, can be implemented using the architecture approach
Line 547: discussed in this book. Feel free to choose the one that fits your needs.
Line 548: Different Output Models for Different Use Cases
Line 549: Once the use case has done its work, what should it return to the caller?
Line 550: ¹⁸Actually, the use case would also have to make sure that no other money transfer to and from the source and target account is happening
Line 551: at the same time to avoid overdrawing an account.
Line 552: 
Line 553: --- 페이지 43 ---
Line 554: 4. Implementing a Use Case
Line 555: 37
Line 556: Similar to the input, it has benefits if the output is as specific to the use case as possible. The output
Line 557: should only include the data that is really needed for the caller to work.
Line 558: In the example code of the “Send Money” use case above, we return a boolean. This is the minimal
Line 559: and most specific value we could possibly return in this context.
Line 560: We might be tempted to return a complete Account with the updated entity to the caller. Perhaps
Line 561: the caller is interested in the new balance of the account?
Line 562: But do we really want to make the “Send Money” use case return this data? Does the caller really
Line 563: need it? If so, shouldn’t we create a dedicated use case for accessing that data that can be used by
Line 564: different callers?
Line 565: There is no right answer to these questions. But we should ask them to try to keep our use cases as
Line 566: specific as possible. When in doubt, return as little as possible.
Line 567: Sharing the same output model between use cases also tends to tightly couple those use cases. If one
Line 568: of the use cases needs a new field in the output model, the other use cases have to handle this field
Line 569: as well, even if it’s irrelevant for them. Shared models tend to grow tumorously for multiple reasons
Line 570: in the long run. Applying the Single Responsibility Principle and keeping models separated helps
Line 571: decoupling use cases.
Line 572: For the same reason we might want to resist the temptation to use our domain entities as output
Line 573: model. We don’t want our domain entities to change for more reasons than necessary. However,
Line 574: we’ll talk more about using entities as input or output models in chapter 11 “Taking Shortcuts
Line 575: Consciously”.
Line 576: What About Read-Only Use Cases?
Line 577: Above, we have discussed how we might implement a use case that modifies the state of our model.
Line 578: How do we go about implementing read-only cases?
Line 579: Let’s assume the UI needs to display the balance of an account. Do we create a specific use case
Line 580: implementation for this?
Line 581: It’s awkward to talk of use cases for read-only operations like this one. Sure, in the UI the requested
Line 582: data is needed to implement a certain use case we might call “View Account Balance”. If this is
Line 583: considered a use case in the context of the project, by all means we should implement it just like the
Line 584: other ones.
Line 585: From the viewpoint of the application core, however, this is a simple query for data. So if it’s not
Line 586: considered a use case in the context of the project, we can implement it as a query to set it apart
Line 587: from the real use cases.
Line 588: One way of doing this within our architecture style is to create a dedicated incoming port for the
Line 589: query and implement it in a “query service”:
Line 590: 
Line 591: --- 페이지 44 ---
Line 592: 4. Implementing a Use Case
Line 593: 38
Line 594: 1
Line 595: package buckpal.application.service;
Line 596: 2
Line 597: 3
Line 598: @RequiredArgsConstructor
Line 599: 4
Line 600: class GetAccountBalanceService implements GetAccountBalanceQuery {
Line 601: 5
Line 602: 6
Line 603: private final LoadAccountPort loadAccountPort;
Line 604: 7
Line 605: 8
Line 606: @Override
Line 607: 9
Line 608: public Money getAccountBalance(AccountId accountId) {
Line 609: 10
Line 610: return loadAccountPort.loadAccount(accountId, LocalDateTime.now())
Line 611: 11
Line 612: .calculateBalance();
Line 613: 12
Line 614: }
Line 615: 13
Line 616: }
Line 617: The query service acts just as our use case services do. It implements an incoming port we named
Line 618: GetAccountBalanceQuery and calls the outgoing port LoadAccountPort to actually load the data from
Line 619: the database.
Line 620: This way, read-only queries are clearly distinguishable from modifying use cases (or “commands”)
Line 621: in our codebase. This plays nicely with concepts like Command-Query Separation (CQS) and
Line 622: Command-Query Responsibility Segregation (CQRS).
Line 623: In the code above, the service doesn’t really do any work other than passing the query on to the
Line 624: outgoing port. If we use the same model across layers, we can take a shortcut and let the client call the
Line 625: outgoing port directly. We’ll talk about this shortcut in chapter 11 “Taking Shortcuts Consciously”.
Line 626: How Does This Help Me Build Maintainable Software?
Line 627: Our architecture lets us implement the domain logic as we see fit, but if we model the input and
Line 628: output of our use cases independently, we avoid unwanted side effects.
Line 629: Yes, it’s more work than just sharing models between use cases. We have to introduce a separate
Line 630: model for each use case and map between this model and our entities.
Line 631: But use case-specific models allow for a crisp understanding of a use case, making it easier to
Line 632: maintain in the long run. Also, they allow multiple developers to work on different use cases in
Line 633: parallel without stepping on each other’s toes.
Line 634: Together with a tight input validation, use case-specific input and output models go a long way
Line 635: toward a maintainable codebase.