# 5.5.1 An object-oriented example with a mock and a stub (pp.114-116)

---
**Page 114**

114
CHAPTER 5
Isolation frameworks
5.5
Stubbing behavior dynamically
Jest has a very simple API for simulating return values for modular and functional
dependencies: mockReturnValue() and mockReturnValueOnce().
test("fake same return values", () => {
  const stubFunc = jest.fn()
    .mockReturnValue("abc");
  //value remains the same
  expect(stubFunc()).toBe("abc");
  expect(stubFunc()).toBe("abc");
  expect(stubFunc()).toBe("abc");
});
test("fake multiple return values", () => {
  const stubFunc = jest.fn()
    .mockReturnValueOnce("a")
    .mockReturnValueOnce("b")
    .mockReturnValueOnce("c");
  //value remains the same
  expect(stubFunc()).toBe("a");
  expect(stubFunc()).toBe("b");
  expect(stubFunc()).toBe("c");
  expect(stubFunc()).toBe(undefined);
});
Notice that, in the first test, we’re setting a permanent return value for the duration of
the test. This is my preferred method of writing tests if I can use it, because it makes
the tests simple to read and maintain. If we do need to simulate multiple values, we
can use mockReturnValueOnce. 
 If you need to simulate an error or do anything more complicated, you can use
mockImplementation() and mockImplementationOnce():
yourStub.mockImplementation(() => {
  throw new Error();
});
5.5.1
An object-oriented example with a mock and a stub
Let’s add another ingredient into our Password Verifier equation. 
Let’s say that the Password Verifier is not active during a special maintenance
window, when software is being updated. 
When a maintenance window is active, calling verify() on the verifier will
cause it to call logger.info() with “under maintenance.” 
Otherwise it will call logger.info() with a “passed” or “failed” result. 
Listing 5.9
Stubbing a value from a fake function with jest.fn() 


---
**Page 115**

115
5.5
Stubbing behavior dynamically
For this purpose (and for the purpose of showing an object-oriented design decision),
we’ll introduce a MaintenanceWindow interface that will be injected into the construc-
tor of our Password Verifier, as illustrated in figure 5.3.
The following listing shows the code for the Password Verifier using the new dependency.
export class PasswordVerifier3 {
  private _rules: any[];
  private _logger: IComplicatedLogger;
  private _maintenanceWindow: MaintenanceWindow;
  constructor(
    rules: any[],
    logger: IComplicatedLogger,
    maintenanceWindow: MaintenanceWindow
  ) {
    this._rules = rules;
    this._logger = logger;
    this._maintenanceWindow = maintenanceWindow;
  }
  verify(input: string): boolean {
    if (this._maintenanceWindow.isUnderMaintenance()) {
      this._logger.info("Under Maintenance", "verify");
      return false;
    }
    const failed = this._rules
      .map((rule) => rule(input))
      .filter((result) => result === false);
    if (failed.length === 0) {
      this._logger.info("PASSED", "verify");
      return true;
    }
Listing 5.10
Password Verifier with a MaintenanceWindow dependency
verify()
Password
Verifier
MaintenanceWindow
Logger
info()
isUnderMaintenance(): bool
Figure 5.3
Using the MaintenanceWindow interface


---
**Page 116**

116
CHAPTER 5
Isolation frameworks
    this._logger.info("FAIL", "verify");
    return false;
  }
}
The MaintenanceWindow interface is injected as a constructor parameter (i.e., using
constructor injection), and it’s used to determine where to execute or not execute the
password verification and send the proper message to the logger.
5.5.2
Stubs and mocks with substitute.js
Now we’ll use substitute.js instead of Jest to create a stub of the MaintenanceWindow
interface and a mock of the IComplicatedLogger interface. Figure 5.4 illustrates this.
Creating stubs and mocks with substitute.js works the same way: we use the Substi-
tute.for<T> function. We can configure stubs with the .returns function and verify
mocks with the .received function. Both of these are part of the fake object that is
returned from Substitute.for<T>(). 
 Here’s what stub creation and configuration looks like:
const stubMaintWindow = Substitute.for<MaintenanceWindow>();
stubMaintWindow.isUnderMaintenance().returns(true);
Mock creation and verification looks like this:
const mockLog = Substitute.for<IComplicatedLogger>();
. . .
/// later down in the end of the test…
mockLog.received().info("Under Maintenance", "verify");
verify()
Password
Verifier
MaintenanceWindow
Logger
info()
isUnderMaintenance(): bool
Stub
Mock
Test
Figure 5.4
A MaintenanceWindow dependency


