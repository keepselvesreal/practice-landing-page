# 12.10 A.4.3 Avoid Jest’s manual mocks (pp.247-247)

---
**Page 247**

247
A.4
Faking module behavior in each test
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
  });
Here’s how you can approach each part of CFRA with Jest.
The jest.mock and jest.resetAllMocks methods are all about faking the module and
resetting the fake implementation to an empty one. Note that the module is still fake
after resetAllMocks. Only its behavior is reset to the default fake implementation. Call-
ing it without telling it what to return will yield weird errors.
 With the FromModule method, we replace the default implementation with a func-
tion that returns our hardcoded values in each test. 
 We could have used mockImplementationOnce() to do mocking, instead of the fake-
DataFromModule() method, but I find that this can create very brittle tests. With stubs,
we normally shouldn’t care how many times they return the fake values. If we did care
how many times they were called, we would use them as mock objects, and that’s the
subject of chapter 4.
A.4.3
Avoid Jest’s manual mocks
Jest contains the idea of manual mocks, but don’t use them if you can help it. This tech-
nique requires you to put a special __mocks__ folder in your tests that contain hard-
coded fake module code, with a naming convention based on the module’s name.
This will work, but the maintainability costs are too high when you want to control the
fake data. The readability costs are too high as well, as it increases scroll fatigue to an
unneeded level, requiring us to switch between multiple files to understand a test. You
can read more about manual mocks in the Jest documentation: https://jestjs.io/docs/
en/manual-mocks.html.
A.4.4
Stubbing a module with Sinon.js
For comparison, and so that you can see that the pattern of CFRA repeats in other
frameworks, here’s an implementation of the same test with Sinon.js—a framework
dedicated to creating stubs.
const sinon = require('sinon');
let dataModule;
Clear
jest.resetAllMocks 
Fake
jest.mock()+
[fake].mockImplementation()
Require
Regularly at the top of the file
Act
Regularly
Listing A.7
Stubbing a module with Sinon.js


