# 10.3.1 Generating tests for common properties (pp.237-240)

---
**Page 237**

Testing Documentation and Property-Based Testing
Chapter 10
[ 237 ]
collected 1 item
tests/test_properties.py::test_adding_contacts PASSED [100%]
================= 1 passed in 0.42s =================
We have seen how Hypothesis can help us to identify bugs and design tests, but it can
actually do much more. It can even go as far as generating some tests for the most common
properties for us.
Generating tests for common properties
Through the hypothesis write command, we can use Hypothesis to generate tests for
use based on some of the most common properties functions might have. For example, if
we want to ensure that the Python sorted method is idempotent and calling it twice leads
to the exact same result, we can use hypothesis write --idempotent sorted to
generate a test that verifies such a property:
$ hypothesis write --idempotent sorted
from hypothesis import given, strategies as st
@given(
    iterable=st.one_of(st.iterables(st.integers()),
st.iterables(st.text())),
    key=st.none(),
    reverse=st.booleans(),
)
def test_idempotent_sorted(iterable, key, reverse):
    result = sorted(iterable, key=key, reverse=reverse)
    repeat = sorted(result, key=key, reverse=reverse)
    assert result == repeat, (result, repeat)
Or, we could test that a pair of encode/decode functions leads back to the original result
when chained using the hypothesis write --roundtrip generator.
If we want to check that for json.loads and json.dumps, for example, we could use
hypothesis write --roundtrip json.dumps json.loads, which would generate the
following code block:
$ hypothesis write --roundtrip json.dumps json.loads
import json
from hypothesis import given, strategies as st


---
**Page 238**

Testing Documentation and Property-Based Testing
Chapter 10
[ 238 ]
@given(
    allow_nan=st.booleans(),
    check_circular=st.booleans(),
    cls=st.none(),
    default=st.none(),
    ensure_ascii=st.booleans(),
    indent=st.none(),
    obj=st.nothing(),
    object_hook=st.none(),
    object_pairs_hook=st.none(),
    parse_constant=st.none(),
    parse_float=st.none(),
    parse_int=st.none(),
    separators=st.none(),
    skipkeys=st.booleans(),
    sort_keys=st.booleans(),
)
def test_roundtrip_dumps_loads(
    allow_nan,
    check_circular,
    cls,
    default,
    ensure_ascii,
    indent,
    obj,
    object_hook,
    object_pairs_hook,
    parse_constant,
    parse_float,
    parse_int,
    separators,
    skipkeys,
    sort_keys,
):
    value0 = json.dumps(
        obj=obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
    )
    value1 = json.loads(
        s=value0,


---
**Page 239**

Testing Documentation and Property-Based Testing
Chapter 10
[ 239 ]
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
    )
    assert obj == value1, (obj, value1)
When refactoring code, implementing performance optimizations, or modifying code to
port it from prior versions of Python, an essential property of the new implementation we
are going to write is that it must retain the exact same behavior of the old implementation.
The hypothesis write --equivalent command is able to do precisely this.
If, for example, we had two helper functions in contacts/utils.py, both meant to sum
two numbers, as follows:
def sum1(a: int, b: int) -> int:
    return a + b
def sum2(a: int, b: int) -> int:
    return sum((a, b))
In that case, hypothesis could generate a test that verifies the fact that both functions lead
to the exact same results:
$ hypothesis write --equivalent contacts.utils.sum1 contacts.utils.sum2
import contacts.utils
from hypothesis import given, strategies as st
@given(a=st.integers(), b=st.integers())
def test_equivalent_sum1_sum2(a, b):
    result_sum1 = contacts.utils.sum1(a=a, b=b)
    result_sum2 = contacts.utils.sum2(a=a, b=b)
    assert result_sum1 == result_sum2, (result_sum1, result_sum2)
While most of those tests could be written manually using hypothesis.given, it can be
convenient having Hypothesis inspect the functions for you and pick the right types.
Especially if you already did the effort of providing type hints for your functions,
Hypothesis will usually be able to do the right thing.
To know all the generators that are available in your version of Hypothesis, you can run
hypothesis write --help.


---
**Page 240**

Testing Documentation and Property-Based Testing
Chapter 10
[ 240 ]
Summary
In this chapter, we saw how to have tested documentation that can guarantee user guides
in sync with our code, and we saw how to make sure that our tests cover limit and corner
cases we might not have considered through property-based testing.
Hypothesis can take away from you a lot of the effort of providing all possible values to a
parameterized test, thereby making writing effective tests much faster, while doctest can
ensure that the examples we write in our user guides remain effective in the long term,
detecting whether any of them need to be updated when our code changes.
In the next chapter, we are going to shift our attention to the web development world,
where we will see how to test web applications both from the point of view of functional
tests and end-to-end tests.


