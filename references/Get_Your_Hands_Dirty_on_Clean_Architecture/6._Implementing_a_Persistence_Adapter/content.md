Line 1: 
Line 2: --- 페이지 52 ---
Line 3: 6. Implementing a Persistence
Line 4: Adapter
Line 5: In chapter 1 I ranted about a traditional layered architecture and claimed that it supports “database-
Line 6: driven design”, because, in the end, everything depends on the persistence layer. In this chapter,
Line 7: we’ll have a look at how to make the persistence layer a plugin to the application layer to invert this
Line 8: dependency.
Line 9: Dependency Inversion
Line 10: Instead of a persistence layer, we’ll talk about a persistence adapter that provides persistence
Line 11: functionality to the application services. Figure 16 shows how we can apply the Dependency
Line 12: Inversion Principle to do just that.
Line 13: Figure 16 - The services from the core use ports to access the persistence adapter.
Line 14: Our application services call port interfaces to access persistence functionality. These ports are
Line 15: implemented by a persistence adapter class that does the actual persistence work and is responsible
Line 16: for talking to the database.
Line 17: In Hexagonal Architecture lingo, the persistence adapter is a “driven” or “outgoing” adapter, because
Line 18: it’s called by our application and not the other way around.
Line 19: The ports are effectively a layer of indirection between the application services and the persistence
Line 20: code. Let’s remind ourselves that we’re adding this layer of indirection in order to be able to
Line 21: evolve the domain code without having to think about persistence problems, meaning without code
Line 22: dependencies to the persistence layer. A refactoring in the persistence code will not necessarily lead
Line 23: to a code change in the core.
Line 24: 
Line 25: --- 페이지 53 ---
Line 26: 6. Implementing a Persistence Adapter
Line 27: 47
Line 28: Naturally, at runtime we still have a dependency from our application core to the persistence adapter.
Line 29: If we modify code in the persistence layer and introduce a bug, for example, we may still break
Line 30: functionality in the application core. But as long as the contracts of the ports are fulfilled, we’re free
Line 31: to do as we want in the persistence adapter without affecting the core.
Line 32: Responsibilities of a Persistence Adapter
Line 33: Let’s have a look at what a persistence adapter usually does:
Line 34: 1. Take input
Line 35: 2. Map input into database format
Line 36: 3. Send input to the database
Line 37: 4. Map database output into application format
Line 38: 5. Return output
Line 39: The persistence adapter takes input through a port interface. The input model may be a domain
Line 40: entity or an object dedicated to a specific database operation, as specified by the interface.
Line 41: It then maps the input model to a format it can work with to modify or query the database. In Java
Line 42: projects, we commonly use the Java Persistence API (JPA) to talk to a database, so we might map
Line 43: the input into JPA entity objects that reflect the structure of the database tables. Depending on the
Line 44: context, mapping the input model into JPA entities may be a lot of work for little gain, so we’ll talk
Line 45: about strategies without mapping in chapter 8 “Mapping Between Boundaries”.
Line 46: Instead of using JPA or another object-relational mapping framework, we might use any other
Line 47: technique to talk to the database. We might map the input model into plain SQL statements and
Line 48: send these statements to the database or we might serialize incoming data into files and read them
Line 49: back from there.
Line 50: The important part is that the input model to the persistence adapter lies within the application core
Line 51: and not within the persistence adapter itself, so that changes in the persistence adapter don’t affect
Line 52: the core.
Line 53: Next, the persistence adapter queries the database and receives the query results.
Line 54: Finally, it maps the database answer into the output model expected by the port and returns it. Again,
Line 55: it’s important that the output model lies within the application core and not within the persistence
Line 56: adapter.
Line 57: Aside from the fact that the input and output models lie in the application core instead of the
Line 58: persistence adapter itself, the responsibilities are not really different from those of a traditional
Line 59: persistence layer.
Line 60: But implementing a persistence adapter as described above will inevitably raise some questions that
Line 61: we probably wouldn’t ask when implementing a traditional persistence layer, because we’re so used
Line 62: to the traditional way that we don’t think about them.
Line 63: 
Line 64: --- 페이지 54 ---
Line 65: 6. Implementing a Persistence Adapter
Line 66: 48
Line 67: Slicing Port Interfaces
Line 68: One question that comes to mind when implementing services is how to slice the port interfaces
Line 69: that define the database operations available to the application core.
Line 70: It’s common practice to create a single repository interface that provides all database operations for
Line 71: a certain entity as sketched in figure 17.
Line 72: Figure 17 - Centralizing all database operations into a single outgoing port interface makes all services depend on
Line 73: methods they don’t need.
Line 74: Each service that relies on database operations will then have a dependency to this single “broad”
Line 75: port interface, even if it uses only a single method from the interface. This means we have
Line 76: unnecessary dependencies in our codebase.
Line 77: Dependencies to methods that we don’t need in our context make the code harder to understand
Line 78: and to test. Imagine we’re writing a unit test for the RegisterAccountService from the figure above.
Line 79: Which of the methods of the AccountRepository interface do we have to create a mock for? We have
Line 80: to first find out which of the AccountRepository methods the service actually calls. Having mocked
Line 81: only part of the interface may lead to other problems as the next person working on that test might
Line 82: expect the interface to be completely mocked and run into errors. So he or she again has to do some
Line 83: research.
Line 84: To put it in the words of Martin C. Robert:
Line 85: Depending on something that carries baggage that you don’t need can cause you troubles
Line 86: that you didn’t expect.²⁰
Line 87: The Interface Segregation Principle provides an answer to this problem. It states that broad interfaces
Line 88: should be split into specific ones so that clients only know the methods they need.
Line 89: If we apply this to our outgoing ports, we might get a result as shown in figure 18.
Line 90: ²⁰Clean Architecture by Robert C. Martin, page 86.
Line 91: 
Line 92: --- 페이지 55 ---
Line 93: 6. Implementing a Persistence Adapter
Line 94: 49
Line 95: Figure 18 - Applying the Interface Segregation Principle removes unnecessary dependencies and makes the existing
Line 96: dependencies more visible.
Line 97: Each service now only depends on the methods it actually needs. What’s more, the names of the
Line 98: ports clearly state what they’re about. In a test, we no longer have to think about which methods to
Line 99: mock, since most if the time there is only one method per port.
Line 100: Having very narrow ports like these makes coding a plug and play experience. When working on a
Line 101: service, we just “plug in” the ports we need. No baggage to carry around.
Line 102: Of course, the “one method per port” approach may not be applicable in all circumstances. There
Line 103: may be groups of database operations that are so cohesive and often used together that we may
Line 104: want to bundle them together in a single interface.
Line 105: Slicing Persistence Adapters
Line 106: In the figures above, we have seen a single persistence adapter class that implements all persistence
Line 107: ports. There is no rule, however, that forbids us to create more than one class, as long as all persistence
Line 108: ports are implemented.
Line 109: We might choose, for instance, to implement one persistence adapter per domain class for which we
Line 110: need persistence operations (or “aggregate” in DDD lingo), as shown in figure 19.
Line 111: 
Line 112: --- 페이지 56 ---
Line 113: 6. Implementing a Persistence Adapter
Line 114: 50
Line 115: Figure 19 - We can create multiple persistence adapters, one for each aggregate.
Line 116: This way, our persistence adapters are automatically sliced along the seams of the domain that we
Line 117: support with persistence functionality.
Line 118: We might split our persistence adapters into even more classes, for instance when we want to
Line 119: implement a couple persistence ports using JPA or another OR-Mapper and some other ports using
Line 120: plain SQL for better performance. We might then create one JPA adapter and one plain SQL adapter,
Line 121: each implementing a subset of the persistence ports.
Line 122: Remember that our domain code doesn’t care about which class ultimately fulfills the contracts
Line 123: defined by the persistence ports. We’re free to do as we see fit in the persistence layer, as long as all
Line 124: ports are implemented.
Line 125: The “one persistence adapter per aggregate” approach is also a good foundation for separating the
Line 126: persistence needs for multiple bounded contexts in the future. Say, after a time we identify a bounded
Line 127: context responsible for use cases around billing. Figure 20 gives an overview of this scenario.
Line 128: 
Line 129: --- 페이지 57 ---
Line 130: 6. Implementing a Persistence Adapter
Line 131: 51
Line 132: Figure 20 - If we want to create hard boundaries between bounded contexts, each bounded context should have its
Line 133: own persistence adapter(s).
Line 134: Each bounded context has its own persistence adapter (or potentially more than one, as described
Line 135: above). The term “bounded context” implies boundaries, which means that services of the account
Line 136: context may not access persistence adapters of the billing context and vice versa. If one context
Line 137: needs something of the other, it can access it via a dedicated incoming port.
Line 138: Example with Spring Data JPA
Line 139: Let’s have a look at a code example that implements the AccountPersistenceAdapter from the
Line 140: figures above. This adapter will have to save and load accounts to and from the database. We have
Line 141: already seen the Account entity in chapter 4 “Implementing a Use Case”, but here is its skeleton
Line 142: again for reference:
Line 143: 
Line 144: --- 페이지 58 ---
Line 145: 6. Implementing a Persistence Adapter
Line 146: 52
Line 147: 1
Line 148: package buckpal.domain;
Line 149: 2
Line 150: 3
Line 151: @AllArgsConstructor(access = AccessLevel.PRIVATE)
Line 152: 4
Line 153: public class Account {
Line 154: 5
Line 155: 6
Line 156: @Getter private final AccountId id;
Line 157: 7
Line 158: @Getter private final ActivityWindow activityWindow;
Line 159: 8
Line 160: private final Money baselineBalance;
Line 161: 9
Line 162: 10
Line 163: public static Account withoutId(
Line 164: 11
Line 165: Money baselineBalance,
Line 166: 12
Line 167: ActivityWindow activityWindow) {
Line 168: 13
Line 169: return new Account(null, baselineBalance, activityWindow);
Line 170: 14
Line 171: }
Line 172: 15
Line 173: 16
Line 174: public static Account withId(
Line 175: 17
Line 176: AccountId accountId,
Line 177: 18
Line 178: Money baselineBalance,
Line 179: 19
Line 180: ActivityWindow activityWindow) {
Line 181: 20
Line 182: return new Account(accountId, baselineBalance, activityWindow);
Line 183: 21
Line 184: }
Line 185: 22
Line 186: 23
Line 187: public Money calculateBalance() {
Line 188: 24
Line 189: // ...
Line 190: 25
Line 191: }
Line 192: 26
Line 193: 27
Line 194: public boolean withdraw(Money money, AccountId targetAccountId) {
Line 195: 28
Line 196: // ...
Line 197: 29
Line 198: }
Line 199: 30
Line 200: 31
Line 201: public boolean deposit(Money money, AccountId sourceAccountId) {
Line 202: 32
Line 203: // ...
Line 204: 33
Line 205: }
Line 206: 34
Line 207: 35
Line 208: }
Line 209: Note that the Account class is not a simple data class with getters and setters but instead tries to be
Line 210: as immutable as possible. It only provides factory methods that create an Account in a valid state
Line 211: and all mutating methods do some validation, like checking the account balance before withdrawing
Line 212: money, so that we cannot create an invalid domain model.
Line 213: We’ll use Spring Data JPA to talk to the database, so we also need @Entity-annotated classes
Line 214: representing the database state of an account:
Line 215: 
Line 216: --- 페이지 59 ---
Line 217: 6. Implementing a Persistence Adapter
Line 218: 53
Line 219: 1
Line 220: package buckpal.adapter.persistence;
Line 221: 2
Line 222: 3
Line 223: @Entity
Line 224: 4
Line 225: @Table(name = "account")
Line 226: 5
Line 227: @Data
Line 228: 6
Line 229: @AllArgsConstructor
Line 230: 7
Line 231: @NoArgsConstructor
Line 232: 8
Line 233: class AccountJpaEntity {
Line 234: 9
Line 235: 10
Line 236: @Id
Line 237: 11
Line 238: @GeneratedValue
Line 239: 12
Line 240: private Long id;
Line 241: 13
Line 242: 14
Line 243: }
Line 244: 1
Line 245: package buckpal.adapter.persistence;
Line 246: 2
Line 247: 3
Line 248: @Entity
Line 249: 4
Line 250: @Table(name = "activity")
Line 251: 5
Line 252: @Data
Line 253: 6
Line 254: @AllArgsConstructor
Line 255: 7
Line 256: @NoArgsConstructor
Line 257: 8
Line 258: class ActivityJpaEntity {
Line 259: 9
Line 260: 10
Line 261: @Id
Line 262: 11
Line 263: @GeneratedValue
Line 264: 12
Line 265: private Long id;
Line 266: 13
Line 267: 14
Line 268: @Column private LocalDateTime timestamp;
Line 269: 15
Line 270: @Column private Long ownerAccountId;
Line 271: 16
Line 272: @Column private Long sourceAccountId;
Line 273: 17
Line 274: @Column private Long targetAccountId;
Line 275: 18
Line 276: @Column private Long amount;
Line 277: 19
Line 278: 20
Line 279: }
Line 280: The state of an account consists merely of an id at this stage. Later, additional fields like a user ID
Line 281: may be added. More interesting is the ActivityJpaEntity, which contains all activities to a specific
Line 282: account. We could have connected the ActivitiyJpaEntity with the AccountJpaEntity via JPAs
Line 283: @ManyToOne or @OneToMany annotations to mark the relation between them, but we have opted to
Line 284: leave this out for now, as it adds side effects to the database queries. In fact, at this stage it would
Line 285: 
Line 286: --- 페이지 60 ---
Line 287: 6. Implementing a Persistence Adapter
Line 288: 54
Line 289: probably be easier to use a simpler object relational mapper than JPA to implement the persistence
Line 290: adapter, but we use it anyways because we think we might need it in the future²¹.
Line 291: Next, we use Spring Data to create repository interfaces that provide basic CRUD functionality out
Line 292: of the box as well as custom queries to load certain activities from the database:
Line 293: 1
Line 294: interface AccountRepository extends JpaRepository<AccountJpaEntity, Long> {
Line 295: 2
Line 296: }
Line 297: 1
Line 298: interface ActivityRepository extends JpaRepository<ActivityJpaEntity, Long> {
Line 299: 2
Line 300: 3
Line 301: @Query("select a from ActivityJpaEntity a " +
Line 302: 4
Line 303: "where a.ownerAccountId = :ownerAccountId " +
Line 304: 5
Line 305: "and a.timestamp >= :since")
Line 306: 6
Line 307: List<ActivityJpaEntity> findByOwnerSince(
Line 308: 7
Line 309: @Param("ownerAccountId") Long ownerAccountId,
Line 310: 8
Line 311: @Param("since") LocalDateTime since);
Line 312: 9
Line 313: 10
Line 314: @Query("select sum(a.amount) from ActivityJpaEntity a " +
Line 315: 11
Line 316: "where a.targetAccountId = :accountId " +
Line 317: 12
Line 318: "and a.ownerAccountId = :accountId " +
Line 319: 13
Line 320: "and a.timestamp < :until")
Line 321: 14
Line 322: Long getDepositBalanceUntil(
Line 323: 15
Line 324: @Param("accountId") Long accountId,
Line 325: 16
Line 326: @Param("until") LocalDateTime until);
Line 327: 17
Line 328: 18
Line 329: @Query("select sum(a.amount) from ActivityJpaEntity a " +
Line 330: 19
Line 331: "where a.sourceAccountId = :accountId " +
Line 332: 20
Line 333: "and a.ownerAccountId = :accountId " +
Line 334: 21
Line 335: "and a.timestamp < :until")
Line 336: 22
Line 337: Long getWithdrawalBalanceUntil(
Line 338: 23
Line 339: @Param("accountId") Long accountId,
Line 340: 24
Line 341: @Param("until") LocalDateTime until);
Line 342: 25
Line 343: 26
Line 344: }
Line 345: Spring Boot will automatically find these repositories and Spring Data will do its magic to provide
Line 346: an implementation behind the repository interface that will actually talk to the database.
Line 347: Having JPA entities and repositories in place, we can implement the persistence adapter that provides
Line 348: the persistence functionality to our application:
Line 349: ²¹Does that sound familiar to you? You choose JPA as an OR mapper because it’s the thing people use for this problem. A couple months
Line 350: into development you curse eager and lazy loading and the caching features and wish for something simpler. JPA is a great tool, but for many
Line 351: problems, simpler solutions may be, well, simpler.
Line 352: 
Line 353: --- 페이지 61 ---
Line 354: 6. Implementing a Persistence Adapter
Line 355: 55
Line 356: 1
Line 357: @RequiredArgsConstructor
Line 358: 2
Line 359: @Component
Line 360: 3
Line 361: class AccountPersistenceAdapter implements
Line 362: 4
Line 363: LoadAccountPort,
Line 364: 5
Line 365: UpdateAccountStatePort {
Line 366: 6
Line 367: 7
Line 368: private final AccountRepository accountRepository;
Line 369: 8
Line 370: private final ActivityRepository activityRepository;
Line 371: 9
Line 372: private final AccountMapper accountMapper;
Line 373: 10
Line 374: 11
Line 375: @Override
Line 376: 12
Line 377: public Account loadAccount(
Line 378: 13
Line 379: AccountId accountId,
Line 380: 14
Line 381: LocalDateTime baselineDate) {
Line 382: 15
Line 383: 16
Line 384: AccountJpaEntity account =
Line 385: 17
Line 386: accountRepository.findById(accountId.getValue())
Line 387: 18
Line 388: .orElseThrow(EntityNotFoundException::new);
Line 389: 19
Line 390: 20
Line 391: List<ActivityJpaEntity> activities =
Line 392: 21
Line 393: activityRepository.findByOwnerSince(
Line 394: 22
Line 395: accountId.getValue(),
Line 396: 23
Line 397: baselineDate);
Line 398: 24
Line 399: 25
Line 400: Long withdrawalBalance = orZero(activityRepository
Line 401: 26
Line 402: .getWithdrawalBalanceUntil(
Line 403: 27
Line 404: accountId.getValue(),
Line 405: 28
Line 406: baselineDate));
Line 407: 29
Line 408: 30
Line 409: Long depositBalance = orZero(activityRepository
Line 410: 31
Line 411: .getDepositBalanceUntil(
Line 412: 32
Line 413: accountId.getValue(),
Line 414: 33
Line 415: baselineDate));
Line 416: 34
Line 417: 35
Line 418: return accountMapper.mapToDomainEntity(
Line 419: 36
Line 420: account,
Line 421: 37
Line 422: activities,
Line 423: 38
Line 424: withdrawalBalance,
Line 425: 39
Line 426: depositBalance);
Line 427: 40
Line 428: 41
Line 429: }
Line 430: 42
Line 431: 43
Line 432: private Long orZero(Long value){
Line 433: 
Line 434: --- 페이지 62 ---
Line 435: 6. Implementing a Persistence Adapter
Line 436: 56
Line 437: 44
Line 438: return value == null ? 0L : value;
Line 439: 45
Line 440: }
Line 441: 46
Line 442: 47
Line 443: 48
Line 444: @Override
Line 445: 49
Line 446: public void updateActivities(Account account) {
Line 447: 50
Line 448: for (Activity activity : account.getActivityWindow().getActivities()) {
Line 449: 51
Line 450: if (activity.getId() == null) {
Line 451: 52
Line 452: activityRepository.save(accountMapper.mapToJpaEntity(activity));
Line 453: 53
Line 454: }
Line 455: 54
Line 456: }
Line 457: 55
Line 458: }
Line 459: 56
Line 460: 57
Line 461: }
Line 462: The persistence adapter implements two ports that are needed by the application, LoadAccountPort
Line 463: and UpdateAccountStatePort.
Line 464: To load an account from the database, we load it from the AccountRepository and then load the
Line 465: activities of this account for a certain time window through the ActivityRepository.
Line 466: To create a valid Account domain entity, we also need the balance the account had before the start
Line 467: of this activity window, so we get the sum of all withdrawals and deposits of this account from the
Line 468: database.
Line 469: Finally, we map all this data to an Account domain entity and return it to the caller.
Line 470: To update the state of an account, we iterate all activities of the Account entity and check if they have
Line 471: IDs. If they don’t, they are new activities, which we the persist through the ActivityRepository.
Line 472: In the scenario described above, we have a two-way mapping between the Account and Activity
Line 473: domain model and the AccountJpaEntity and ActivityJpaEntity database model. Why the effort
Line 474: of mapping back and forth? Couldn’t we just move the JPA annotations to the Account and Activity
Line 475: classes and directly store them entities in the database?
Line 476: Such a “no mapping” strategy may be a valid choice, as we’ll see in chapter 8 “Mapping Between
Line 477: Boundaries” when we’ll be talking about mapping strategies. However, JPA then forces us to
Line 478: make compromises in the domain model. For instance, JPA requires entities to have a no-args
Line 479: constructor. Or it might be that in the persistence layer, a @ManyToOne relationship makes sense
Line 480: from a performance point of view, but in the domain model we want this relationship to be the
Line 481: other way around because we always only load part of the data anyways.
Line 482: So, if we want to create a rich domain model without compromises to the underlying persistence,
Line 483: we’ll have to map between domain model and persistence model.
Line 484: 
Line 485: --- 페이지 63 ---
Line 486: 6. Implementing a Persistence Adapter
Line 487: 57
Line 488: What about Database Transactions?
Line 489: We have not touched the topic of database transactions, yet. Where do we put our transaction
Line 490: boundaries?
Line 491: A transaction should span all write operations to the database that are performed within a certain
Line 492: use case so that all those operations can be rolled back together if one of them fails.
Line 493: Since the persistence adapter doesn’t know which other database operations are part of the same use
Line 494: case, it cannot decide when to open and close a transaction. We have to delegate this responsibility
Line 495: to the services that orchestrate the calls to the persistence adapter.
Line 496: The easiest way to do this with Java and Spring is to add the @Transactional annotation to the
Line 497: application service classes so that Spring will wrap all public methods with a transaction:
Line 498: 1
Line 499: package buckpal.application.service;
Line 500: 2
Line 501: 3
Line 502: @Transactional
Line 503: 4
Line 504: public class SendMoneyService implements SendMoneyUseCase {
Line 505: 5
Line 506: ...
Line 507: 6
Line 508: }
Line 509: If we want our services to stay pure and not be stained with @Transactional annotations, we may use
Line 510: aspect-oriented programming (for example with AspectJ) in order to weave transaction boundaries
Line 511: into our codebase.
Line 512: How Does This Help Me Build Maintainable Software?
Line 513: Building a persistence adapter that acts as a plugin to the domain code frees the domain code from
Line 514: persistence details so that we can build a rich domain model.
Line 515: Using narrow port interfaces, we’re flexible to implement one port this way and another port that
Line 516: way, perhaps even with a different persistence technology, without the application noticing. We can
Line 517: even switch out the complete persistence layer, as long as the port contracts are obeyed.