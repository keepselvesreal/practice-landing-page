# 4.7.2 Refactoring production code with interface injection (pp.96-98)

---
**Page 96**

96
CHAPTER 4
Interaction testing using mock objects
 In strongly typed languages like Java or C#, it’s common to extract the fake logger
as a separate class, like so:
class FakeLogger {
  logged = "";
  info(text) {
    this.logged = text;
  }
}
We simply implement the info function in the class, but instead of logging anything,
we just save the value being sent as a parameter to the function in a publicly visible
variable that we can assert again later in our test.
 Notice that I didn’t call the fake object MockLogger or StubLogger but FakeLogger.
This is so that I can reuse this class in multiple different tests. In some tests, it might
be used as a stub, and in others it might be used as a mock object. I use the word
“fake” to denote anything that isn’t real. Another common term for this sort of thing is
“test double.” Fake is shorter, so I like it. 
 In our tests, we’ll instantiate the class and send it over as a constructor parameter,
and then we’ll assert on the logged variable of the class, like so:
test("logger + passing scenario, calls logger with PASSED", () => {
   let logged = "";
   const mockLog = new FakeLogger();
   const verifier = new PasswordVerifier([], mockLog);
   verifier.verify("any input");
   expect(mockLog.logged).toMatch(/PASSED/);
});
4.7.2
Refactoring production code with interface injection
Interfaces play a large role in many object-oriented programs. They are one variation
on the idea of polymorphism: allowing one or more objects to be replaced with one
another as long as they implement the same interface. In JavaScript and other lan-
guages like Ruby, interfaces are not needed, since the language allows for the idea of
duck typing without needing to cast an object to a specific interface. I won’t touch
here on the pros and cons of duck typing. You should be able to use either technique
as you see fit, in the language of your choice. In JavaScript, we can turn to TypeScript
to use interfaces. The compiler, or transpiler, we’ll use can help ensure that we are
using types based on their signatures correctly.
 Listing 4.13 shows three code files: the first describes a new ILogger interface, the
second describes a SimpleLogger that implements that interface, and the third is our
PasswordVerifier, which uses only the ILogger interface to get a logger instance.
PasswordVerifier has no knowledge of the actual type of logger being injected. 


---
**Page 97**

97
4.7
Mocks in an object-oriented style
export interface ILogger {    
    info(text: string);       
}                             
//this class might have dependencies on files or network
class SimpleLogger implements ILogger {   
    info(text: string) {
    }
}
export class PasswordVerifier {
    private _rules: any[];
    private _logger: ILogger;                      
    constructor(rules: any[], logger: ILogger) {   
        this._rules = rules;
        this._logger = logger;                     
    }
    verify(input: string): boolean {
        const failed = this._rules
            .map(rule => rule(input))
            .filter(result => result === false);
        if (failed.length === 0) {
            this._logger.info('PASSED');
            return true;
        }
        this._logger.info('FAIL');
        return false;
    }
}
Notice that a few things have changed in the production code. I’ve added a new inter-
face to the production code, and the existing logger now implements this interface.
I’m changing the design to make the logger replaceable. Also, the PasswordVerifier
class works with the interface instead of the SimpleLogger class. This allows me to
replace the instance of the logger class with a fake one, instead of having a hard
dependency on the real logger. 
 The following listing shows what a test might look like in a strongly typed language,
but with a handwritten fake object that implements the ILogger interface.
class FakeLogger implements ILogger {
    written: string;
    info(text: string) {
        this.written = text;
    }
}
Listing 4.13
Production code gets an ILogger interface
Listing 4.14
Injecting a handwritten mock ILogger 
A new interface, 
which is part of 
production code
The logger now 
implements that 
interface.
The verifier
now uses the
interface.


---
**Page 98**

98
CHAPTER 4
Interaction testing using mock objects
describe('password verifier with interfaces', () => {
    test('verify, with logger, calls logger', () => {
        const mockLog = new FakeLogger();
        const verifier = new PasswordVerifier([], mockLog);
        verifier.verify('anything');
        expect(mockLog.written).toMatch(/PASS/);
    });
});
In this example, I’ve created a handwritten class called FakeLogger. All it does is over-
ride the one method in the ILogger interface and save the text parameter for future
assertion. We then expose this value as a field in the written class. Once this value is
exposed, we can verify that the fake logger was called by checking that field.
 I’ve done this manually because I wanted you to see that even in object-oriented
land, the patterns repeat themselves. Instead of having a mock function, we now have a
mock object, but the code and test work just like the previous examples. 
4.8
Dealing with complicated interfaces
What happens when the interface is more complicated, such as when it has more than
one or two functions in it, or more than one or two parameters in each function?
4.8.1
Example of a complicated interface
Listing 4.15 is an example of such a complicated interface, and of the production
code verifier that uses the complicated logger, injected as an interface. The ICompli-
catedLogger interface has four functions, each with one or more parameters. Every
function would need to be faked in our tests, and that can lead to complexity and
maintainability problems in our code and tests.
export interface IComplicatedLogger {   
    info(text: string)
    debug(text: string, obj: any)
Interface naming conventions
I’m using the naming convention of prefixing the logger interface with an “I” because
it’s going to be used for polymorphic reasons (i.e., I’m using it to abstract a role in
the system). This is not always the case for interface naming in TypeScript, such as
when we use interfaces to define the structure of a set of parameters (basically using
them as strongly typed structures). In that case, naming without an “I” makes sense
to me. 
For now, think of it like this: If you’re going to implement it more than once, you
should prefix it with an “I” to make the expected use of the interface more explicit. 
Listing 4.15
Working with a more complicated interface (production code)
A new interface, which is 
part of production code


