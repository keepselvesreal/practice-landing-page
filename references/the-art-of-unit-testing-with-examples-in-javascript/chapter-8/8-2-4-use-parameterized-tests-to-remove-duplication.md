# 8.2.4 Use parameterized tests to remove duplication (pp.176-177)

---
**Page 176**

176
CHAPTER 8
Maintainability
of objects. Sometimes it’s about removing duplication in assertion logic or call-
ing out code in a specific way.
Setup methods can’t have parameters or return values.
Setup methods can’t be used as factory methods that return values. They’re run
before the test executes, so they must be more generic in the way they work.
Tests sometimes need to request specific things or call shared code with a
parameter for the specific test (for example, retrieving an object and setting its
property to a specific value).
Setup methods should only contain code that applies to all the tests in the cur-
rent test class, or the method will be harder to read and understand.
I’ve almost entirely stopped using setup methods for the tests I write. Test code should
be nice and clean, just like production code, but if your production code looks horri-
ble, please don’t use that as a crutch to write unreadable tests. Use factory and helper
methods, and make the world a better place for the generation of developers that will
have to maintain your code in 5 or 10 years.
NOTE
We looked at an example of moving from using beforeEach to helper
functions in section 8.2.3 (listing 8.9) and also in chapter 2.
8.2.4
Use parameterized tests to remove duplication
Another great option for replacing setup methods, if all your tests look the same, is
to use parameterized tests. Different test frameworks in different languages support
parameterized tests—if you’re using Jest, you can use the built-in test.each or it.each
functions. 
 Parameterization helps move the setup logic that would otherwise remain dupli-
cated or would reside in the beforeEach block to the test’s arrange section. It also
helps avoid duplication of the assertion logic, as shown in the following listing.
const sum = numbers => {
    if (numbers.length > 0) {
        return parseInt(numbers);
    }
    return 0;
};
describe('sum with regular tests', () => {
    test('sum number 1', () => {
        const result = sum('1');    
        expect(result).toBe(1);     
    });
    test('sum number 2', () => {
        const result = sum('2');    
        expect(result).toBe(2);     
    });
});
Listing 8.10
Parameterized tests with Jest
Duplicated setup 
and assertion logic


---
**Page 177**

177
8.3
Avoid overspecification
describe('sum with parameterized tests', () => {
    test.each([
        ['1', 1],   
        ['2', 2]    
    ])('add ,for %s, returns that number', (input, expected) => {
            const result = sum(input);       
            expect(result).toBe(expected);   
        }
    )
});
In the first describe block, we have two tests that repeat each other with different input
values and expected outputs. In the second describe block, we’re using test.each
to provide an array of arrays, where each subarray lists all the values needed for the
test function.
 Parameterized tests can help reduce a lot of duplication between tests, but we
should be careful to only use this technique in cases where we repeat the exact same
scenario and only change the input and output. 
8.3
Avoid overspecification
An overspecified test is one that contains assumptions about how a specific unit under
test (production code) should implement its internal behavior, instead of only check-
ing that the observable behavior (exit points) is correct. 
 Here are ways unit tests are often overspecified:
A test asserts purely internal state in an object under test.
A test uses multiple mocks.
A test uses stubs as mocks.
A test assumes a specific order or exact string matches when that isn’t required.
Let’s look at some examples of overspecified tests.
8.3.1
Internal behavior overspecification with mocks
A very common antipattern is to verify that an internal function in a class or module is
called, instead of checking the exit point of the unit of work. Here’s a password veri-
fier that calls an internal function, which the test shouldn’t care about.
export class PasswordVerifier4 {
  private _rules: ((input: string) => boolean)[];
  private _logger: IComplicatedLogger;
  constructor(rules: ((input) => boolean)[],
      logger: IComplicatedLogger) {
    this._rules = rules;
    this._logger = logger;
  }
Listing 8.11
Production code that calls a protected function
Test data used
for setup and
assertion
Setup and 
assertion without 
duplication


