# 4.8.2 Writing tests with complicated interfaces (pp.99-100)

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


---
**Page 100**

100
CHAPTER 4
Interaction testing using mock objects
      }
    }
    ...
    test("verify passing, with logger, calls logger with PASS", () => {
      const mockLog = new FakeComplicatedLogger();
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.infoWritten).toMatch(/PASSED/);
    });
    test("A more JS oriented variation on this test", () => {
      const mockLog = {} as IComplicatedLogger;
      let logged = "";
      mockLog.info = (text) => (logged = text);
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(logged).toMatch(/PASSED/);
    });
  });
});
Here, we’re declaring, again, a fake logger class (FakeComplicatedLogger) that imple-
ments the IComplicatedLogger interface. Look at how much boilerplate code we
have. This will be especially true if we’re working in strongly typed object-oriented lan-
guages such as Java, C#, or C++. There are ways around all this boilerplate code, which
we’ll touch on in the next chapter. 
4.8.3
Downsides of using complicated interfaces directly
There are other downsides to using long, complicated interfaces in our tests:
If we’re saving arguments being sent in manually, it’s more cumbersome to ver-
ify multiple arguments across multiple methods and calls. 
It’s likely that we are depending on third-party interfaces instead of internal
ones, and this will end up making our tests more brittle as time goes by. 
Even if we are depending on internal interfaces, long interfaces have more rea-
sons to change, and now so do our tests. 
What does this mean for us? I highly recommend using only fake interfaces that meet
both of these conditions:
You control the interfaces (they are not made by a third party).
They are adapted to the needs of your unit of work or component. 


