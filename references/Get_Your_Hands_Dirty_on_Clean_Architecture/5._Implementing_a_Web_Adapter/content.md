Line 1: 
Line 2: --- 페이지 45 ---
Line 3: 5. Implementing a Web Adapter
Line 4: Most applications today have some kind of web interface - either a UI that we can interact with via
Line 5: web browser or an HTTP API that other systems can call to interact with our application.
Line 6: In our target architecture, all communication with the outside world goes through adapters. So, let’s
Line 7: discuss how we can implement an adapter that provides such a web interface.
Line 8: Dependency Inversion
Line 9: Figure 13 gives a zoomed-in view of the architecture elements that are relevant to our discussion of
Line 10: a web adapter - the adapter itself and the ports through which it interacts with our application core:
Line 11: Figure 13 - An incoming adapter talks to the application layer through dedicated incoming ports which are interfaces
Line 12: implemented by the application services.
Line 13: The web adapter is a “driving” or “incoming” adapter. It takes requests from the outside and
Line 14: translates them into calls to our application core, telling it what to do. The control flow goes from
Line 15: the controllers in the web adapter to the services in the application layer.
Line 16: The application layer provides specific ports through which the web adapter may communicate. The
Line 17: services implement these ports and the web adapter may call these ports.
Line 18: If we look closer, we notice that this is the Dependency Inversion Principle in action. Since the
Line 19: control flow goes from left to right, we could just as well let the web adapter call the use cases
Line 20: directly, as shown in figure 14.
Line 21: 
Line 22: --- 페이지 46 ---
Line 23: 5. Implementing a Web Adapter
Line 24: 40
Line 25: Figure 14 - We can remove the port interfaces and call the services directly.
Line 26: So why do we add another layer of indirection between the adapter and the use cases? The reason
Line 27: is that the ports are a specification of the places where the outside world can interact with our
Line 28: application core. Having ports in place, we know exactly which communication with the outside
Line 29: world takes place, which is a valuable information for any maintenance engineer working on your
Line 30: legacy codebase.
Line 31: Having said that, one of the shortcuts we’ll talk about in chapter 11 “Taking Shortcuts Consciously”
Line 32: is just leaving the incoming ports out and calling the application services directly.
Line 33: One question remains, though, which is relevant for highly interactive applications. Imagine an
Line 34: application that sends real-time data to the user’s browser via web sockets. How does the application
Line 35: core send this real-time data to the web adapter which in turns sends it to the user’s browser?
Line 36: For this scenario, we definitely need a port. This port must be implemented by the web adapter and
Line 37: called by the application core as depicted in figure 15.
Line 38: Figure 15 - If an application must actively notify a web adapter, we need to go through an outgoing port to keep the
Line 39: dependencies in the right direction.
Line 40: Technically speaking, this would be an outgoing port and make the web adapter an incoming and
Line 41: outgoing adapter. But there is no reason that the same adapter can not be both at the same time.
Line 42: 
Line 43: --- 페이지 47 ---
Line 44: 5. Implementing a Web Adapter
Line 45: 41
Line 46: For the rest of this chapter we’ll assume that the web adapter is an incoming adapter only, since this
Line 47: is the most common case.
Line 48: Responsibilities of a Web Adapter
Line 49: What does a web adapter actually do? Let’s say we want to provide a REST API for our BuckPal
Line 50: application. Where do the responsibilities of the web adapter start and where do they end?
Line 51: A web adapter usually does these things:
Line 52: 1. Map HTTP request to Java objects
Line 53: 2. Perform authorization checks
Line 54: 3. Validate input
Line 55: 4. Map input to the input model of the use case
Line 56: 5. Call the use case
Line 57: 6. Map output of the use case back to HTTP
Line 58: 7. Return HTTP response
Line 59: First of all, a web adapter must listen to HTTP requests that match certain criteria like a certain URL
Line 60: path, HTTP method and content type. The parameters and the content of a matching HTTP request
Line 61: must then be deserialized into objects we can work with.
Line 62: Commonly, a web adapter then does an authentication and authorization check and returns an error
Line 63: if it fails.
Line 64: The state of the incoming objects can then be validated. But haven’t we already discussed input
Line 65: validation as a responsibility of the input model to the use cases? Yes, the input model to the use
Line 66: cases should only allow input that is valid in the context of the use cases. But here, we’re talking about
Line 67: the input model to the web adapter. It might have a completely different structure and semantics
Line 68: from the input model to the use cases, so we might have to perform different validations.
Line 69: I don’t advocate to implement the same validations in the web adapter as we have already done in
Line 70: the input model of the use cases. Instead, we should validate that we can transform the input model
Line 71: of the web adapter into the input model of the use cases. Anything that prevents us from doing this
Line 72: transformation is a validation error.
Line 73: This brings us to the next responsibility of a web adapter: to call a certain use case with the
Line 74: transformed input model. The adapter then takes the output of the use case and serializes it into
Line 75: an HTTP response which is sent back to the caller.
Line 76: If anything goes wrong on the way and an exception is thrown, the web adapter must translate the
Line 77: error into a message that is sent back to the caller.
Line 78: That’s a lot of responsibilities weighing on the shoulders of our web adapter. But it’s also a lot of
Line 79: responsibilities that the application layer should not be concerned with. Anything that has to do
Line 80: 
Line 81: --- 페이지 48 ---
Line 82: 5. Implementing a Web Adapter
Line 83: 42
Line 84: with HTTP must not leak into the application layer. If the application core knows that we’re dealing
Line 85: with HTTP on the outside, we have essentially lost the option to perform the same domain logic
Line 86: from other incoming adapters that do not use HTTP. In a good architecture, we want to keep options
Line 87: open.
Line 88: Note that this boundary between web adapter and application layer comes naturally if we start
Line 89: development with the domain and application layers instead of with the web layer. If we implement
Line 90: the use cases first, without thinking about any specific incoming adapter, we are not tempted to blur
Line 91: the boundary.
Line 92: Slicing Controllers
Line 93: In most web frameworks - like Spring MVC in the Java world - we create controller classes that
Line 94: perform the responsibilities we have discussed above. So, do we build a single controller that answers
Line 95: all requests directed at our application? We don’t have to. A web adapter may certainly consist of
Line 96: more than one class.
Line 97: We should take care, however, to put these classes into the same package hierarchy to mark them as
Line 98: belonging together, as discussed in chapter 3 “Organizing Code”.
Line 99: So, how many controllers do we build? I say we should rather build too many than too few. We
Line 100: should make sure that each controller implements a slice of the web adapter that is as narrow as
Line 101: possible and that shares as little as possible with other controllers.
Line 102: Let’s take the operations on an account entity within our BuckPal application. A popular approach is
Line 103: to create a single AccountController that accepts requests for all operations that relate to accounts.
Line 104: A Spring controller providing a REST API might look like the following code snippet.
Line 105: 1
Line 106: package buckpal.adapter.web;
Line 107: 2
Line 108: 3
Line 109: @RestController
Line 110: 4
Line 111: @RequiredArgsConstructor
Line 112: 5
Line 113: class AccountController {
Line 114: 6
Line 115: 7
Line 116: private final GetAccountBalanceQuery getAccountBalanceQuery;
Line 117: 8
Line 118: private final ListAccountsQuery listAccountsQuery;
Line 119: 9
Line 120: private final LoadAccountQuery loadAccountQuery;
Line 121: 10
Line 122: 11
Line 123: private final SendMoneyUseCase sendMoneyUseCase;
Line 124: 12
Line 125: private final CreateAccountUseCase createAccountUseCase;
Line 126: 13
Line 127: 14
Line 128: @GetMapping("/accounts")
Line 129: 15
Line 130: List<AccountResource> listAccounts(){
Line 131: 16
Line 132: ...
Line 133: 
Line 134: --- 페이지 49 ---
Line 135: 5. Implementing a Web Adapter
Line 136: 43
Line 137: 17
Line 138: }
Line 139: 18
Line 140: 19
Line 141: @GetMapping("/accounts/id")
Line 142: 20
Line 143: AccountResource getAccount(@PathVariable("accountId") Long accountId){
Line 144: 21
Line 145: ...
Line 146: 22
Line 147: }
Line 148: 23
Line 149: 24
Line 150: @GetMapping("/accounts/{id}/balance")
Line 151: 25
Line 152: long getAccountBalance(@PathVariable("accountId") Long accountId){
Line 153: 26
Line 154: ...
Line 155: 27
Line 156: }
Line 157: 28
Line 158: 29
Line 159: @PostMapping("/accounts")
Line 160: 30
Line 161: AccountResource createAccount(@RequestBody AccountResource account){
Line 162: 31
Line 163: ...
Line 164: 32
Line 165: }
Line 166: 33
Line 167: 34
Line 168: @PostMapping("/accounts/send/{sourceAccountId}/{targetAccountId}/{amount}")
Line 169: 35
Line 170: void sendMoney(
Line 171: 36
Line 172: @PathVariable("sourceAccountId") Long sourceAccountId,
Line 173: 37
Line 174: @PathVariable("targetAccountId") Long targetAccountId,
Line 175: 38
Line 176: @PathVariable("amount") Long amount) {
Line 177: 39
Line 178: ...
Line 179: 40
Line 180: }
Line 181: 41
Line 182: }
Line 183: Everything concerning the account resource is in a single class, which feels good. But let’s discuss
Line 184: the downsides of this approach.
Line 185: First, less code per class is a good thing. I have worked in a legacy project where the largest class
Line 186: had 30.000 lines of code¹⁹. That’s no fun. Even if the controller only accumulates 200 lines of code
Line 187: over the years, it’s still harder to grasp than 50 lines, even when it’s cleanly separated into methods.
Line 188: The same argument is valid for test code. If the controller itself has a lot of code, there will be a lot
Line 189: of test code. And often, test code is even harder to grasp than the productive code, because it tends
Line 190: to be more abstract. We also want to make the tests for a certain piece of production code to be easy
Line 191: to find, which is easier in small classes.
Line 192: Equally important, however, putting all operations into a single controller class encourages re-use
Line 193: of data structures. In the code example above, many operations share the AccountResource model
Line 194: class. It serves as a bucket for everything that is needed in any of the operations. AccountResource
Line 195: probably has an id field. This is not needed in the create operation and will probably confuse here
Line 196: ¹⁹It was actually a conscious architecture decision (by our predecessors, mind you) that lead to those 30.000 lines being in a single class:
Line 197: to change the system at runtime, without re-deployment, it allowed to upload compiled Java bytecode in a .class file. And it only allowed to
Line 198: upload a single file, so this file had to contain all the code… .
Line 199: 
Line 200: --- 페이지 50 ---
Line 201: 5. Implementing a Web Adapter
Line 202: 44
Line 203: more than it will help. Imagine that an Account has a one-to-many relationship with User objects.
Line 204: Do we include those User objects when creating or updating a book? Will the users be returned by
Line 205: the list operation? This is an easy example, yet, but in any above-playsize project, we’ll ask these
Line 206: questions at some point.
Line 207: So, I advocate the approach to create a separate controller, potentially in a separate package, for each
Line 208: operation. Also, we should name the methods and classes as close to our use cases as possible:
Line 209: 1
Line 210: package buckpal.adapter.web;
Line 211: 2
Line 212: 3
Line 213: @RestController
Line 214: 4
Line 215: @RequiredArgsConstructor
Line 216: 5
Line 217: public class SendMoneyController {
Line 218: 6
Line 219: 7
Line 220: private final SendMoneyUseCase sendMoneyUseCase;
Line 221: 8
Line 222: 9
Line 223: @PostMapping(path = "/accounts/sendMoney/{sourceAccountId}/{targetAccountId}/{amou\
Line 224: 10
Line 225: nt}")
Line 226: 11
Line 227: void sendMoney(
Line 228: 12
Line 229: @PathVariable("sourceAccountId") Long sourceAccountId,
Line 230: 13
Line 231: @PathVariable("targetAccountId") Long targetAccountId,
Line 232: 14
Line 233: @PathVariable("amount") Long amount) {
Line 234: 15
Line 235: 16
Line 236: SendMoneyCommand command = new SendMoneyCommand(
Line 237: 17
Line 238: new AccountId(sourceAccountId),
Line 239: 18
Line 240: new AccountId(targetAccountId),
Line 241: 19
Line 242: Money.of(amount));
Line 243: 20
Line 244: 21
Line 245: sendMoneyUseCase.sendMoney(command);
Line 246: 22
Line 247: }
Line 248: 23
Line 249: 24
Line 250: }
Line 251: Also, each controller can have its own model, like CreateAccountResource or UpdateAccountResource,
Line 252: or use primitives as input, like in the example above. Those specialized model classes may even
Line 253: be private to the controller’s package so they may not accidentally be re-used somewhere else.
Line 254: Controllers may still share models, but using shared classes from another package makes us think
Line 255: about it more and perhaps we find out that we don’t need half of the fields and create our own, after
Line 256: all.
Line 257: Also, we should think hard on the names of the controllers and services. Instead of CreateAccount,
Line 258: for instance, wouldn’t RegisterAccount be a better name? In our BuckPal application the only way
Line 259: to create an account is for a user to register it. So we use the word “register” in class names to better
Line 260: convey their meaning. There are certainly cases where the usual suspects Create..., Update..., and
Line 261: 
Line 262: --- 페이지 51 ---
Line 263: 5. Implementing a Web Adapter
Line 264: 45
Line 265: Delete... sufficiently describe a use case, but we might want to think twice before actually using
Line 266: them.
Line 267: Another benefit of this slicing style is that it makes parallel work on different operations a breeze.
Line 268: We won’t have merge conflicts if two developers work on different operations.
Line 269: How Does This Help Me Build Maintainable Software?
Line 270: When building a web adapter to an application we should keep in mind that we’re building an
Line 271: adapter that translates HTTP to method calls to use cases of our application and translates the
Line 272: results back to HTTP, and does not do any domain logic.
Line 273: The application layer, on the other hand, should not do HTTP, so we should make sure not to leak
Line 274: HTTP details. This makes the web adapter replaceable by another adapter should the need arise.
Line 275: When slicing web controllers, we should not be afraid to build many small classes that don’t share
Line 276: a model. They’re easier to grasp, to test and support parallel work. It’s more work initially to set up
Line 277: such fine-grained controllers, but it will pay off during maintenance.