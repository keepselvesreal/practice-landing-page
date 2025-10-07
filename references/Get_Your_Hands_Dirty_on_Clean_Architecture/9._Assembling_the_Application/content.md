Line 1: 
Line 2: --- 페이지 83 ---
Line 3: 9. Assembling the Application
Line 4: Now that we have implemented some use cases, web adapters and persistence adapters, we need
Line 5: to assemble them into a working application. As discussed in chapter 3 “Organizing Code”, we rely
Line 6: on a dependency injection mechanism to instantiate our classes and wire them together at startup
Line 7: time. In this chapter, we’ll discuss some approaches of how we can do this with plain Java and the
Line 8: Spring and Spring Boot frameworks.
Line 9: Why Even Care About Assembly?
Line 10: Why aren’t we just instantiating the use cases and adapters when and where we need them? Because
Line 11: we want to keep the code dependencies pointed in the right direction. Remember: all dependencies
Line 12: should point inwards, towards the domain code of our application, so that the domain code doesn’t
Line 13: have to change when something in the outer layers changes.
Line 14: If a use case needs to call a persistence adapter and just instantiates it itself, we have created a code
Line 15: dependency in the wrong direction.
Line 16: This is why we created outgoing port interfaces. The use case only knows an interface and is provided
Line 17: an implementation of this interface at runtime.
Line 18: A nice side effect of this programming style is that the code we’re creating is much better testable.
Line 19: If we can pass all objects a class needs into its constructor, we can choose to pass in mocks instead
Line 20: of the real objects, which makes it easy to create an isolated unit test for the class.
Line 21: So, who’s responsible for creating our object instances? And how to do it without violating the
Line 22: Dependency Rule?
Line 23: The answer is that there must be a configuration component that is neutral to our architecture and
Line 24: that has a dependency to all classes in order to instantiate them as shown in figure 26.
Line 25: 
Line 26: --- 페이지 84 ---
Line 27: 9. Assembling the Application
Line 28: 78
Line 29: Figure 26 - A neutral configuration component may access all classes in order to instantiate them.
Line 30: In the “Clean Architecture” introduced in chapter 2 “Inverting Dependencies”, this configuration
Line 31: component would be in the outermost circle, which may access all inner layers, as defined by the
Line 32: Dependency Rule.
Line 33: The configuration component is responsible for assembling a working application from the parts we
Line 34: provided. It must
Line 35: • create web adapter instances,
Line 36: • ensure that HTTP requests are actually routed to the web adapters,
Line 37: • create use case instances,
Line 38: • provide web adapters with use case instances
Line 39: • create persistence adapter instances,
Line 40: • provide use cases with persistence adapter instances,
Line 41: • and ensure that the persistence adapters can actually access the database.
Line 42: Besides that, the configuration component should be able to access certain sources of configuration
Line 43: parameters, like configuration files or command line parameters. During application assembly, the
Line 44: configuration component then passes these parameters on to the application components to control
Line 45: behavior like which database to access or which server to use for sending email.
Line 46: These are a lot of responsibilities (read: “reasons to change”). Aren’t we violating the Single
Line 47: Responsibility Principle here? Yes, we are, but if we want to keep the rest of the application clean,
Line 48: we need an outside component that takes care of the wiring. And this component has to know all
Line 49: the moving parts to assemble them to a working application.
Line 50: 
Line 51: --- 페이지 85 ---
Line 52: 9. Assembling the Application
Line 53: 79
Line 54: Assembling via Plain Code
Line 55: There are several ways to implement a configuration component responsible for assembling
Line 56: the application. If we’re building an application without the support of a dependency injection
Line 57: framework, we can create such a component with plain code:
Line 58: 1
Line 59: package copyeditor.configuration;
Line 60: 2
Line 61: 3
Line 62: class Application {
Line 63: 4
Line 64: 5
Line 65: public static void main(String[] args) {
Line 66: 6
Line 67: 7
Line 68: AccountRepository accountRepository = new AccountRepository();
Line 69: 8
Line 70: ActivityRepository activityRepository = new ActivityRepository();
Line 71: 9
Line 72: AccountPersistenceAdapter accountPersistenceAdapter =
Line 73: 10
Line 74: new AccountPersistenceAdapter(accountRepository, activityRepository);
Line 75: 11
Line 76: 12
Line 77: SendMoneyUseCase sendMoneyUseCase =
Line 78: 13
Line 79: new SendMoneyUseService(
Line 80: 14
Line 81: accountPersistenceAdapter,
Line 82: // LoadAccountPort
Line 83: 15
Line 84: accountPersistenceAdapter); // UpdateAccountStatePort
Line 85: 16
Line 86: 17
Line 87: SendMoneyController sendMoneyController =
Line 88: 18
Line 89: new SendMoneyController(sendMoneyUseCase);
Line 90: 19
Line 91: 20
Line 92: startProcessingWebRequests(sendMoneyController);
Line 93: 21
Line 94: 22
Line 95: }
Line 96: 23
Line 97: }
Line 98: This code snippet is a simplified example of how such a configuration component might look like.
Line 99: In Java, an application is started from the main method. Within this method, we instantiate all the
Line 100: classes we need, from web controller to persistence adapter, and wire them together.
Line 101: Finally, we call the mystic method startProcessingWebRequests() which exposes the web con-
Line 102: troller via HTTP²⁸. The application is then ready to process requests.
Line 103: This plain code approach is the most basic way of assembling an application. It has some drawbacks,
Line 104: however.
Line 105: First of all, the code above is for an application that has only a single web controller, use case and
Line 106: persistence adapter. Imagine how much code like this we would have to produce to bootstrap a
Line 107: full-blown enterprise application!
Line 108: ²⁸This method is just a placeholder for any bootstrapping logic that is necessary to expose our web adapters via HTTP. We don’t really
Line 109: want to implement this ourselves.
Line 110: 
Line 111: --- 페이지 86 ---
Line 112: 9. Assembling the Application
Line 113: 80
Line 114: Second, since we’re instantiating all classes ourselves from outside of their packages, those classes
Line 115: all need to be public. This means, for example, that Java doesn’t prevent a use case directly accessing
Line 116: a persistence adapter, since it’s public. It would be nice if we could avoid unwanted dependencies
Line 117: like this by using package-private visibility.
Line 118: Luckily, there are dependency injection frameworks that can do the dirty work for us while still
Line 119: maintaining package-private dependencies. The Spring framework is currently the most popular
Line 120: one in the Java world. Spring also provides web and database support, among a lot of other things,
Line 121: so we don’t have to implement the mystic startProcessingWebRequests() method after all.
Line 122: Assembling via Spring’s Classpath Scanning
Line 123: If we use the Spring framework to assemble our application, the result is called the “application
Line 124: context”. The application context contains all objects that together make up the application (“beans”
Line 125: in Java lingo).
Line 126: Spring offers several approaches to assemble an application context, each having its own advantages
Line 127: and drawbacks. Let’s start with discussing the most popular (and most convenient) approach:
Line 128: classpath scanning.
Line 129: With classpath scanning, Spring goes through all classes that are available in the classpath and
Line 130: searches for classes that are annotated with the @Component annotation. The framework then creates
Line 131: an object from each of these classes. The classes should have a constructor that take all required fields
Line 132: as an argument, like our AccountPersistenceAdapter from chapter 6 “Implementing a Persistence
Line 133: Adapter”:
Line 134: 1
Line 135: @Component
Line 136: 2
Line 137: @RequiredArgsConstructor
Line 138: 3
Line 139: class AccountPersistenceAdapter implements
Line 140: 4
Line 141: LoadAccountPort,
Line 142: 5
Line 143: UpdateAccountStatePort {
Line 144: 6
Line 145: 7
Line 146: private final AccountRepository accountRepository;
Line 147: 8
Line 148: private final ActivityRepository activityRepository;
Line 149: 9
Line 150: private final AccountMapper accountMapper;
Line 151: 10
Line 152: 11
Line 153: @Override
Line 154: 12
Line 155: public Account loadAccount(AccountId accountId, LocalDateTime baselineDate) {
Line 156: 13
Line 157: ...
Line 158: 14
Line 159: }
Line 160: 15
Line 161: 16
Line 162: @Override
Line 163: 17
Line 164: public void updateActivities(Account account) {
Line 165: 
Line 166: --- 페이지 87 ---
Line 167: 9. Assembling the Application
Line 168: 81
Line 169: 18
Line 170: ...
Line 171: 19
Line 172: }
Line 173: 20
Line 174: 21
Line 175: }
Line 176: In this case, we didn’t even write the constructor ourselves, but instead let the Lombok library do
Line 177: it for us using the @RequiredArgsConstructor annotation which creates a constructor that takes all
Line 178: final fields as arguments.
Line 179: Spring will find this constructor and search for @Component-annotated classes of the required argu-
Line 180: ment types and instantiate them in a similar manner to add them to the application context. Once
Line 181: all required objects are available, it will finally call the constructor of AccountPersistenceAdapter
Line 182: and add the resulting object to the application context as well.
Line 183: Classpath scanning is a very convenient way of assembling an application. We only have to sprinkle
Line 184: some @Component annotations across the codebase and provide the right constructors.
Line 185: We can also create our own stereotype annotation for Spring to pick up. We could, for example,
Line 186: create a @PersistenceAdapter annotation:
Line 187: 1
Line 188: @Target({ElementType.TYPE})
Line 189: 2
Line 190: @Retention(RetentionPolicy.RUNTIME)
Line 191: 3
Line 192: @Documented
Line 193: 4
Line 194: @Component
Line 195: 5
Line 196: public @interface PersistenceAdapter {
Line 197: 6
Line 198: 7
Line 199: @AliasFor(annotation = Component.class)
Line 200: 8
Line 201: String value() default "";
Line 202: 9
Line 203: 10
Line 204: }
Line 205: This annotation is meta-annotated with @Component to let Spring know that it should be picked up
Line 206: during classpath scanning. We could now use @PersistenceAdapter instead of @Component to mark
Line 207: our persistence adapter classes as parts of our application. With this annotation we have made our
Line 208: architecture more evident to people reading the code.
Line 209: The classpath scanning approach has its drawbacks, however. First, it’s invasive in that it requires
Line 210: us to put a framework-specific annotation to our classes. If you’re a Clean Architecture hardliner,
Line 211: you’d say that this is forbidden as it binds our code to a specific framework.
Line 212: I’d say that in usual application development, a single annotation on a class is not such a big deal
Line 213: and can easily be refactored, if at all necessary.
Line 214: In other contexts, however, like when building a library or a framework for other developers to use,
Line 215: this might be a no-go, since we don’t want to encumber our users with a dependency to the Spring
Line 216: framework.
Line 217: 
Line 218: --- 페이지 88 ---
Line 219: 9. Assembling the Application
Line 220: 82
Line 221: Another potential drawback of the classpath scanning approach is that magic things might happen.
Line 222: And with “magic” I mean the bad kind of magic causing inexplicable effects that might take days to
Line 223: figure out if you’re not a Spring expert.
Line 224: Magic happens because classpath scanning is a very blunt weapon to use for application assembly.
Line 225: We simply point Spring at the parent package of our application and tell it to go looking for
Line 226: @Component-annotated classes within this package.
Line 227: Do you know by heart every single class that exists within your application? Probably not. There’s
Line 228: bound to be some class that we don’t actually want to have in the application context. Perhaps this
Line 229: class even manipulates the application context in evil ways, causing errors that are hard to track.
Line 230: Let’s look at an alternative approach that gives us a little more control.
Line 231: Assembling via Spring’s Java Config
Line 232: While classpath scanning is the cudgel of application assembly, Spring’s Java Config is the scalpel.
Line 233: This approach is similar to the plain code approach introduced earlier in this chapter, but it’s less
Line 234: messy and provides us with a framework so that we don’t have to code everything by hand.
Line 235: In this approach, we create configuration classes, each responsible for constructing a set of beans
Line 236: that are to be added to the application context.
Line 237: For example, we could create a configuration class that is responsible for instantiating all our
Line 238: persistence adapters:
Line 239: 1
Line 240: @Configuration
Line 241: 2
Line 242: @EnableJpaRepositories
Line 243: 3
Line 244: class PersistenceAdapterConfiguration {
Line 245: 4
Line 246: 5
Line 247: @Bean
Line 248: 6
Line 249: AccountPersistenceAdapter accountPersistenceAdapter(
Line 250: 7
Line 251: AccountRepository accountRepository,
Line 252: 8
Line 253: ActivityRepository activityRepository,
Line 254: 9
Line 255: AccountMapper accountMapper){
Line 256: 10
Line 257: return new AccountPersistenceAdapter(
Line 258: 11
Line 259: accountRepository,
Line 260: 12
Line 261: activityRepository,
Line 262: 13
Line 263: accountMapper);
Line 264: 14
Line 265: }
Line 266: 15
Line 267: 16
Line 268: @Bean
Line 269: 17
Line 270: AccountMapper accountMapper(){
Line 271: 18
Line 272: return new AccountMapper();
Line 273: 19
Line 274: }
Line 275: 
Line 276: --- 페이지 89 ---
Line 277: 9. Assembling the Application
Line 278: 83
Line 279: 20
Line 280: 21
Line 281: }
Line 282: The @Configuration annotation marks this class as a configuration class to be picked up by Spring’s
Line 283: classpath scanning. So, in this case, we’re still using classpath scanning, but we only pick up our
Line 284: configuration classes instead of every single bean, which reduces the chance of evil magic happening.
Line 285: The beans themselves are created within the @Bean-annotated factory methods of our configuration
Line 286: classes. In the case above, we add a persistence adapter to application context. It needs two
Line 287: repositories and a mapper as input to its constructor. Spring automatically provides these objects as
Line 288: input to the factory methods.
Line 289: But where does Spring get the repository objects from? If they are created manually in a factory
Line 290: method of another configuration class, then Spring would automatically provide them as parameters
Line 291: to the factory methods of the code example above. In this case, however, they are created by Spring
Line 292: itself, triggered by the @EnableJpaRepositories annotation. If Spring Boot finds this annotation,
Line 293: it will automatically provide implementations for all Spring Data repository interfaces we have
Line 294: defined.
Line 295: If you’re familiar with Spring Boot, you might know that we could have added the annotation
Line 296: @EnableJpaRepositories to the main application class instead of our custom configuration class.
Line 297: Yes, this is possible, but it would activate JPA repositories every time the application is started up.
Line 298: Even if we start the application within a test that doesn’t actually need persistence. So, by moving
Line 299: such “feature annotations” to a separate configuration “module”, we’ve just become much more
Line 300: flexible and can start up parts of our application instead of always having to start the whole thing.
Line 301: With the PersistenceAdapterConfiguration class, we have created a tightly-scoped persistence
Line 302: module that instantiates all objects we need in our persistence layer. It will be automatically picked
Line 303: up by Spring’s classpath scanning while we still have full control about which beans are actually
Line 304: added to the application context.
Line 305: Similarly, we could create configuration classes for web adapters, or for certain modules within
Line 306: our application layer. We can now create an application context that contains certain modules, but
Line 307: mocks the beans of other modules, which gives us great flexibility in tests. We could even push the
Line 308: code of each of those modules into its own codebase, its own package, or its own JAR file without
Line 309: much refactoring.
Line 310: Also, this approach does not force us to sprinkle @Component annotations all over our codebase,
Line 311: like the classpath scanning approach does. So, we can keep our application layer clean without any
Line 312: dependency to the Spring framework (or any other framework, for that matter).
Line 313: There is a catch with this solution, however. If the configuration class is not within the same package
Line 314: as the classes of the beans it creates (the persistence adapter classes in this case), those classes must
Line 315: be public. To restrict visibility, we can use packages as module boundaries and create a dedicated
Line 316: configuration class within each package. This way, we cannot use sub-packages, though, as will be
Line 317: discussed in chapter 10 “Enforcing Architecture Boundaries”.
Line 318: 
Line 319: --- 페이지 90 ---
Line 320: 9. Assembling the Application
Line 321: 84
Line 322: How Does This Help Me Build Maintainable Software?
Line 323: Spring and Spring Boot (and similar frameworks) provide a lot of features that make our lives easier.
Line 324: One of the main features is assembling the application out of the parts (classes) that we, as application
Line 325: developers, provide.
Line 326: Classpath scanning is a very convenient feature. We only have to point Spring to a package and it
Line 327: assembles an application from the classes it finds. This allows for rapid development, with us not
Line 328: having to think about the application as a whole.
Line 329: Once the codebase grows, however, this quickly leads to lack of transparency. We don’t know which
Line 330: beans exactly are loaded into the application context. Also, we cannot easily start up isolated parts
Line 331: of the application context to use in tests.
Line 332: By creating a dedicated configuration component responsible for assembling our application, we
Line 333: can liberate our application code from this responsibility (read: “reason for change” - remember the
Line 334: “S” in “SOLID”?). We’re rewarded with highly cohesive modules that we can start up in isolation
Line 335: from each other and that we can easily move around within our codebase. As usual, this comes at
Line 336: the price of spending some extra time to maintain this configuration component.