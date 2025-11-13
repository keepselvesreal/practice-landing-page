# 4.8.1 Example of a complicated interface (pp.98-99)

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


---
**Page 99**

99
4.8
Dealing with complicated interfaces
    warn(text: string)
    error(text: string, location: string, stacktrace: string)
}
export class PasswordVerifier2 {
    private _rules: any[];
    private _logger: IComplicatedLogger;                     
    constructor(rules: any[], logger: IComplicatedLogger) {  
        this._rules = rules;
        this._logger = logger;
    }
...
}
As you can see, the new IComplicatedLogger interface will be part of production
code, which will make the logger replaceable. I’m leaving off the implementation of a
real logger, because it’s not relevant for our examples. That’s the benefit of abstract-
ing away things with an interface: we don’t need to reference them directly. Also
notice that the type of parameter expected in the class’s constructor is that of the
IComplicatedLogger interface. This allows me to replace the instance of the logger
class with a fake one, just like we did before.
4.8.2
Writing tests with complicated interfaces
Here’s what the test looks like. It has to override each and every interface function,
which creates long and annoying boilerplate code.
describe("working with long interfaces", () => {
  describe("password verifier", () => {
    class FakeComplicatedLogger            
        implements IComplicatedLogger {    
      infoWritten = "";
      debugWritten = "";
      errorWritten = "";
      warnWritten = "";
      debug(text: string, obj: any) {
        this.debugWritten = text;
      }
      error(text: string, location: string, stacktrace: string) {
        this.errorWritten = text;
      }
      info(text: string) {
        this.infoWritten = text;
      }
      warn(text: string) {
        this.warnWritten = text;
Listing 4.16
Test code with a complicated logger interface
The class now 
works with the 
new interface.
A fake logger class that 
implements the new interface


