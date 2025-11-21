# 5.5.2 Stubs and mocks with substitute.js (pp.116-117)

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


---
**Page 117**

117
5.6
Advantages and traps of isolation frameworks
The following listing shows the full code for a couple of tests that use a mock and a stub.
import { Substitute } from "@fluffy-spoon/substitute";
const makeVerifierWithNoRules = (log, maint) =>
  new PasswordVerifier3([], log, maint);
describe("working with substitute part 2", () => {
  test("verify, during maintanance, calls logger", () => {
    const stubMaintWindow = Substitute.for<MaintenanceWindow>();
    stubMaintWindow.isUnderMaintenance().returns(true);
    const mockLog = Substitute.for<IComplicatedLogger>();
    const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
    verifier.verify("anything");
    mockLog.received().info("Under Maintenance", "verify");
  });
  test("verify, outside maintanance, calls logger", () => {
    const stubMaintWindow = Substitute.for<MaintenanceWindow>();
    stubMaintWindow.isUnderMaintenance().returns(false);
    const mockLog = Substitute.for<IComplicatedLogger>();
    const verifier = makeVerifierWithNoRules(mockLog, stubMaintWindow);
    verifier.verify("anything");
    mockLog.received().info("PASSED", "verify");
  });
});
We can successfully and relatively easily simulate values in our tests with dynamically
created objects. I encourage you to research the flavor of an isolation framework
you’d like to use. I’ve only used substitute.js as an example in this book. It’s not the
only framework out there.
 This test requires no handwritten fakes, but notice that it’s already starting to take
a toll on the readability for the test reader. Functional designs are usually much slim-
mer than this. In an object-oriented setting, sometimes this is a necessary evil. How-
ever, we could easily refactor the creation of various helpers, mocks, and stubs to
helper functions as we refactor our code, so that the test can be simpler and shorter to
read. More on that in part 3 of this book.
5.6
Advantages and traps of isolation frameworks
Based on what we’ve covered in this chapter, we’ve seen distinct advantages to using
isolation frameworks:
Easier modular faking—Module dependencies can be hard to get around without
some boilerplate code, which isolation frameworks help us eliminate. This point
Listing 5.11
Testing Password Verifier with substitute.js


