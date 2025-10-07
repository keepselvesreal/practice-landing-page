Line 1: 
Line 2: --- 페이지 91 ---
Line 3: 10. Enforcing Architecture Boundaries
Line 4: We have talked a lot about architecture in the previous chapters and it feels good to have a target
Line 5: architecture to guide us in our decisions on how to craft code and where to put it.
Line 6: In every above-playsize software project, however, architecture tends to erode over time. Boundaries
Line 7: between layers weaken, code becomes harder to test, and we generally need more and more time to
Line 8: implement new features.
Line 9: In this chapter, we’ll discuss some measures that we can take to enforce the boundaries within our
Line 10: architecture and thus to fight architecture erosion.
Line 11: Boundaries and Dependencies
Line 12: Before we talk about different ways of enforcing architecture boundaries, let’s discuss where the
Line 13: boundaries lie within our architecture and what “enforcing a boundary” actually means.
Line 14: Figure 27 - Enforcing architecture boundaries means enforcing that dependencies point in the right direction. Dashed
Line 15: arrows mark dependencies that are not allowed according to our architecture.
Line 16: 
Line 17: --- 페이지 92 ---
Line 18: 10. Enforcing Architecture Boundaries
Line 19: 86
Line 20: Figure 27 shows how the elements of our hexagonal architecture might be distributed across four
Line 21: layers resembling the generic Clean Architecture approach introduced in chapter 2 “Inverting
Line 22: Dependencies”.
Line 23: The innermost layer contains domain entities. The application layer may access those domain
Line 24: entities to implement use case within application services. Adapters access those services through
Line 25: incoming ports, or are being accessed by those services through outgoing ports. Finally, the
Line 26: configuration layer contains factories that create adapter and service objects and provides them
Line 27: to a dependency injection mechanism.
Line 28: In the above figure, our architecture boundaries become pretty clear. There is a boundary between
Line 29: each layer and its next inward and outward neighbor. According to the Dependency Rule,
Line 30: dependencies that cross such a layer boundary must always point inwards.
Line 31: This chapter is about ways to enforce the Dependency Rule. We want to make sure that there are
Line 32: no illegal dependencies that point in the wrong direction (dashed red arrows in the figure).
Line 33: Visibility Modifiers
Line 34: Let’s start with the most basic tool that Java provides us for enforcing boundaries: visibility
Line 35: modifiers.
Line 36: Visibility modifiers have been a topic in almost every entry-level job interview I have conducted in
Line 37: the last couple of years. I would ask the interviewee which visibility modifiers Java provides and
Line 38: what their differences are.
Line 39: Most of the interviewees only list the public, protected, and private modifiers. Almost none know
Line 40: the package-private (or “default”) modifier. This is always a welcome opportunity for me to ask
Line 41: some questions about why such a visibility modifier would make sense in order to find out if the
Line 42: interviewee could abstract from his or her previous knowledge.
Line 43: So, why is the package-private modifier such an important modifier? Because it allows us to use Java
Line 44: packages to group classes into cohesive “modules”. Classes within such a module that can access
Line 45: each other, but cannot be accessed from outside of the package. We can then choose to make specific
Line 46: classes public to act as entry points to the module. This reduces the risk of accidentally violating the
Line 47: Dependency Rule by introducing a dependency that points in the wrong direction.
Line 48: Let’s have another look at the package structure discussed in chapter 3 “Organizing Code” with
Line 49: visibiliy modifiers in mind:
Line 50: 
Line 51: --- 페이지 93 ---
Line 52: 10. Enforcing Architecture Boundaries
Line 53: 87
Line 54: 1
Line 55: buckpal
Line 56: 2
Line 57: └──account
Line 58: 3
Line 59: ├──adapter
Line 60: 4
Line 61: |
Line 62: ├──in
Line 63: 5
Line 64: |
Line 65: |
Line 66: └──web
Line 67: 6
Line 68: |
Line 69: |
Line 70: └──o AccountController
Line 71: 7
Line 72: |
Line 73: ├──out
Line 74: 8
Line 75: |
Line 76: |
Line 77: └──persistence
Line 78: 9
Line 79: |
Line 80: |
Line 81: ├──o AccountPersistenceAdapter
Line 82: 10
Line 83: |
Line 84: |
Line 85: └──o SpringDataAccountRepository
Line 86: 11
Line 87: ├──domain
Line 88: 12
Line 89: |
Line 90: ├──+ Account
Line 91: 13
Line 92: |
Line 93: └──+ Activity
Line 94: 14
Line 95: └──application
Line 96: 15
Line 97: └──o SendMoneyService
Line 98: 16
Line 99: └──port
Line 100: 17
Line 101: ├──in
Line 102: 18
Line 103: |
Line 104: └──+ SendMoneyUseCase
Line 105: 19
Line 106: └──out
Line 107: 20
Line 108: ├──+ LoadAccountPort
Line 109: 21
Line 110: └──+ UpdateAccountStatePort
Line 111: We can make the classes in the persistence package package-private package-private (marked with
Line 112: “o” in the tree above), because they don’t need to be accessed by the outside world. The persistence
Line 113: adapter is accessed through the output ports it implements. For the same reason, we can make the
Line 114: SendMoneyService class package-private. Dependency injection mechanisms usually use reflection
Line 115: to instantiate classes, so they will still be able to instantiate those classes even if they’re package-
Line 116: private.
Line 117: With Spring, this approach only works if we use the classpath scanning approach discussed in
Line 118: chapter 9 “Assembling the Application”, however, since the other approaches require us to create
Line 119: instances of those objects ourselves, which requires public access.
Line 120: The rest of the classes in the example have to be public (marked with “+”) by definition of the
Line 121: architecture: the domain package needs to be accessible by the other layers and the application
Line 122: layer needs to be accessible by the web and persistence adapters.
Line 123: The package-private modifier is awesome for small modules with no more than a couple handful
Line 124: of classes. Once a package reaches a certain number of classes, however, it grows confusing to have
Line 125: so many classes in the same package. In this case, I like to create sub-packages to make the code
Line 126: easier to find (and, I admit, to satisfy my need for aesthetics). This is where the package-private
Line 127: modifier fails to deliver, since Java treats sub-packages as different packages and we cannot access
Line 128: a package-private member of a sub-package. So, members in sub-packages must be public, exposing
Line 129: them to the outside world and thus making our architecture vulnerable to illegal dependencies.
Line 130: 
Line 131: --- 페이지 94 ---
Line 132: 10. Enforcing Architecture Boundaries
Line 133: 88
Line 134: Post-Compile Checks
Line 135: As soon as we use the public modifier on a class, the compiler will let any other class use it, even if
Line 136: the direction of the dependency points in the wrong direction according to our architecture.
Line 137: Since the compiler won’t help us out in these cases, we have to find other means to check that the
Line 138: Dependency Rule isn’t violated.
Line 139: One way is to introduce post-compile checks, i.e. checks that are conducted at runtime, when the
Line 140: code has already been compiled. Such runtime checks are best run during automated tests within a
Line 141: continuous integration build.
Line 142: A tool that supports this kind of checks for Java is ArchUnit²⁹. Among other things, ArchUnit
Line 143: provides an API to check if dependencies point in the expected direction. If it finds a violation,
Line 144: it will throw an exception. It’s best run from within a test based on a unit testing framework like
Line 145: JUnit, making the test fail in case of a dependency violation.
Line 146: With ArchUnit, we can now check the dependencies between our layers, assuming that each layer
Line 147: has its own package, as defined in the package structure discussed in the previous section. For
Line 148: example, we can check that there is no dependency from the domain layer to the outward-lying
Line 149: application layer:
Line 150: 1
Line 151: class DependencyRuleTests {
Line 152: 2
Line 153: 3
Line 154: @Test
Line 155: 4
Line 156: void domainLayerDoesNotDependOnApplicationLayer() {
Line 157: 5
Line 158: noClasses()
Line 159: 6
Line 160: .that()
Line 161: 7
Line 162: .resideInAPackage("buckpal.domain..")
Line 163: 8
Line 164: .should()
Line 165: 9
Line 166: .dependOnClassesThat()
Line 167: 10
Line 168: .resideInAnyPackage("buckpal.application..")
Line 169: 11
Line 170: .check(new ClassFileImporter()
Line 171: 12
Line 172: .importPackages("buckpal.."));
Line 173: 13
Line 174: }
Line 175: 14
Line 176: 15
Line 177: }
Line 178: With a little work, we can even create a kind of DSL (domain-specific language) on top of the
Line 179: ArchUnit API that allows us to specify all relevant packages within our hexagonal architecture and
Line 180: then automatically checks if all dependencies between those packages point in the right direction:
Line 181: ²⁹https://github.com/TNG/ArchUnit
Line 182: 
Line 183: --- 페이지 95 ---
Line 184: 10. Enforcing Architecture Boundaries
Line 185: 89
Line 186: 1
Line 187: class DependencyRuleTests {
Line 188: 2
Line 189: 3
Line 190: @Test
Line 191: 4
Line 192: void validateRegistrationContextArchitecture() {
Line 193: 5
Line 194: HexagonalArchitecture.boundedContext("account")
Line 195: 6
Line 196: .withDomainLayer("domain")
Line 197: 7
Line 198: .withAdaptersLayer("adapter")
Line 199: 8
Line 200: .incoming("web")
Line 201: 9
Line 202: .outgoing("persistence")
Line 203: 10
Line 204: .and()
Line 205: 11
Line 206: .withApplicationLayer("application")
Line 207: 12
Line 208: .services("service")
Line 209: 13
Line 210: .incomingPorts("port.in")
Line 211: 14
Line 212: .outgoingPorts("port.out")
Line 213: 15
Line 214: .and()
Line 215: 16
Line 216: .withConfiguration("configuration")
Line 217: 17
Line 218: .check(new ClassFileImporter()
Line 219: 18
Line 220: .importPackages("buckpal.."));
Line 221: 19
Line 222: }
Line 223: 20
Line 224: 21
Line 225: }
Line 226: In the code example above, we first specify the parent package of our bounded context (which
Line 227: might also be the complete application if it spans only a single bounded context). We then go on
Line 228: to specify the sub-packages for the domain, adapter, application and configuration layers. The final
Line 229: call to check() will then execute a set of checks, verifying that the package dependencies are valid
Line 230: according to the Dependency Rule. The code for this hexagonal architecture DSL is available on
Line 231: GitHub³⁰ if you would like to play around with it.
Line 232: While post-compile checks like above can be a great help in fighting illegal dependencies, they are
Line 233: not fail-safe. If we misspell the package name buckpal in the code example above, for example, the
Line 234: test will find no classes and thus no dependency violations. A single typo or, more importantly, a
Line 235: single refactoring renaming a package, can make the whole test useless. We might fix this by adding
Line 236: a check that fails if no classes are found, but it’s still vulnerable to refactorings. Post-compile checks
Line 237: always have to be maintained parallel to the codebase.
Line 238: Build Artifacts
Line 239: Until now, our only tool for demarcating architecture boundaries within our codebase have been
Line 240: packages. All of our code has been part of the same monolithic build artifact.
Line 241: ³⁰https://github.com/thombergs/buckpal/blob/master/buckpal-configuration/src/test/java/io/reflectoring/buckpal/archunit/
Line 242: HexagonalArchitecture.java
Line 243: 
Line 244: --- 페이지 96 ---
Line 245: 10. Enforcing Architecture Boundaries
Line 246: 90
Line 247: A build artifact is the result of a (hopefully automated) build process. The currently most popular
Line 248: build tools in the Java world are Maven and Gradle. So, until now, imagine we had a single Maven
Line 249: or Gradle build script and we could call Maven or Gradle to compile, test and package the code of
Line 250: our application into a single JAR file.
Line 251: A main feature of build tools is dependency resolution. To transform a certain codebase into a build
Line 252: artifact, a build tool first checks if all artifacts the codebase depends on are available. If not, it tries
Line 253: to load them from an artifact repository. If this fails, the build will fail with an error, before even
Line 254: trying to compile the code.
Line 255: We can leverage this to enforce the dependencies (and thus, enforce the boundaries) between the
Line 256: modules and layers of our architecture. For each such module or layer, we create a separate build
Line 257: module with its own codebase and its own build artifact (JAR file) as a result. In the build script
Line 258: of each module, we specify only those dependencies to other modules that are allowed according
Line 259: to our architecture. Developers can no longer inadvertently create illegal dependencies because the
Line 260: classes are not even available on the classpath and they would run into compile errors.
Line 261: Figure 28 - Different ways of dividing our architecture into multiple build artifacts to prohibit illegal dependencies.
Line 262: Figure 28 shows an incomplete set of options to divide our architecture into separate build artifacts.
Line 263: Starting on the left, we see a basic three-module build with a separate build artifact for the
Line 264: configuration, adapter and application layers. The configuration module may access the adapters
Line 265: module, which in turn may access the application module. The configuration module may also
Line 266: access the application module due to the implicit, transitive dependency between them.
Line 267: Note that the adapters module contains the web adapter as well as the persistence adapter. This
Line 268: means that the build tool will not prohibit dependencies between those adapters. While dependencies
Line 269: between those adapters are not strictly forbidden by the Dependency Rule (since both adapters are
Line 270: within the same outer layer), in most cases it’s sensible to keep adapters isolated from each other.
Line 271: 
Line 272: --- 페이지 97 ---
Line 273: 10. Enforcing Architecture Boundaries
Line 274: 91
Line 275: After all, we usually don’t want changes in the persistence layer to leak into the web layer and vice
Line 276: versa (remember the Single Responsiblity Principle!). The same holds true for other types of adapters,
Line 277: for example adapters connecting our application to a certain third party API. We don’t want details
Line 278: of that API leaking into other adapters by adding accidental dependencies between adapters.
Line 279: Thus, we may split the single adapters module into multiple build modules, one for each adapter, as
Line 280: shown in the second column of figure 28.
Line 281: Next, we could decide to split up the application module further. It currently contains the incoming
Line 282: and outgoing ports to our application, the services that implement or use those ports, and the domain
Line 283: entities that should contain much of our domain logic.
Line 284: If we decide that our domain entities are not to be used as transfer objects within our ports (i.e. we
Line 285: want to disallow the “No Mapping” strategy from chapter 8 “Mapping Between Boundaries”), we
Line 286: can apply the Dependency Inversion Principle and pull out a separate “api” module that contains
Line 287: only the port interfaces (third column in figure 28). The adapter modules and the application module
Line 288: may access the api module, but not the other way around. The api module does not have access to
Line 289: the domain entities and cannot use them within the port interfaces. Also, the adapters no longer
Line 290: have direct access to the entities and services, so they must go through the ports.
Line 291: We can even go a step further and split the api module in two, one part containing only the incoming
Line 292: ports and the other part only containing the outgoing ports (fourth column in figure 27). This way we
Line 293: can make very clear if a certain adapter is an incoming adapter or an outgoing adapter by declaring
Line 294: a dependency only to the input or the outgoing ports.
Line 295: Also, we could split the application module even further, creating a module containing only the
Line 296: services and another containing only the domain entities. This ensures that the entities don’t access
Line 297: the services and it would allow other applications (with different use cases and thus different
Line 298: services) to use the same domain entities by simply declaring a dependency to the domain build
Line 299: artifact.
Line 300: Figure 28 illustrates that there are a lot of different ways to divide an application into build modules,
Line 301: and there are of course more than just the four ways depicted in the figure. The gist is that the finer
Line 302: we cut our modules, the stronger we can control dependencies between them. The finer we cut,
Line 303: however, the more mapping we have to do between those modules, enforcing one of the mapping
Line 304: strategies introduced in chapter 8 “Mapping Between Boundaries”.
Line 305: Besides that, demarcating architecture boundaries with build modules has a number of advantages
Line 306: over using simple packages as boundaries.
Line 307: First, build tools absolutely hate circular dependencies. Circular dependencies are bad because a
Line 308: change in one module within the circle would potentially mean a change in all other modules within
Line 309: the circle, which is a violation of the Single Responsibility Principle. Build tools don’t allow circular
Line 310: dependencies because they would run into an endless loop while trying to resolve them. Thus, we
Line 311: can be sure that there are no circular dependencies between our build modules.
Line 312: The Java compiler, on the other hand, doesn’t care at all if there is a circular dependency between
Line 313: two or more packages.
Line 314: 
Line 315: --- 페이지 98 ---
Line 316: 10. Enforcing Architecture Boundaries
Line 317: 92
Line 318: Second, build modules allow isolated code changes within certain modules without having to take
Line 319: the other modules into consideration. Imagine we have to do a major refactoring in the application
Line 320: layer that causes temporary compile errors in a certain adapter. If the adapters and application layer
Line 321: are within the same build module, most IDEs will insist that all compile errors in the adapters must
Line 322: be fixed before we can run the tests in the application layer, even though the tests don’t need the
Line 323: adapters to compile. If the application layer is in its own build module, however, the IDE won’t care
Line 324: about the adapters at the moment, and we could run the application layer tests at will. Same goes
Line 325: for running a build process with Maven or Gradle: if both layers are in the same build module, the
Line 326: build would fail due to compile errors in either layer.
Line 327: So, multiple build modules allow isolated changes in each module. We could even choose to put each
Line 328: module into its own code repository, allowing different teams to maintain different modules.
Line 329: Finally, with each inter-module dependency explicitly declared in a build script, adding a new
Line 330: dependency becomes a conscious act instead of an accident. A developer who needs access to a
Line 331: certain class he currently cannot access will hopefully give some thought to the question if the
Line 332: dependency is really reasonable before adding it to the build script.
Line 333: These advantages come with the added cost of having to maintain a build script, though, so the
Line 334: architecture should be somewhat stable before splitting it into different build modules.
Line 335: How Does This Help Me Build Maintainable Software?
Line 336: Software architecture is basically all about managing dependencies between architecture elements.
Line 337: If the dependencies become a big ball of mud, the architecture becomes a big ball of mud.
Line 338: So, to preserve the architecture over time, we need to continually make sure that dependencies point
Line 339: in the right direction.
Line 340: When producing new code or refactoring existing code, we should keep the package structure in
Line 341: mind and use package-private visibility when possible to avoid dependencies to classes that should
Line 342: not be accessed from outside the package.
Line 343: If we need to enforce architecture boundaries within a single build module, and the package-private
Line 344: modifier doesn’t work because the package structure won’t allow it, we can make use of post-compile
Line 345: tools like ArchUnit.
Line 346: And anytime we feel that the architecture is stable enough we should extract architecture elements
Line 347: into their own build modules, because this gives explicit control over the dependencies.
Line 348: All three approaches can be combined to enforce architecture boundaries and thus keep the codebase
Line 349: maintainable over time.