# 2.4.13 The role of experience and creativity (pp.59-59)

---
**Page 59**

59
Exercises
    cart.add(new CartItem("Chocolate", 2, 2.5));
    assertThat(cart.totalPrice())   
      .isEqualTo(120 + 2.5*2);
  }
}
Again, the mechanics are the same. We just have to take more into consideration when
engineering the test cases. 
2.4.13 The role of experience and creativity
If two testers performed the specification-based testing technique I described earlier
in the same program, would they develop the same set of tests? Ideally, but possibly
not. In the substringsBetween() example, I would expect most developers to come
up with similar test cases. But it is not uncommon for developers to approach a prob-
lem from completely different yet correct angles.
 I am trying to reduce the role of experience and creativity by giving developers a
process that everybody can follow, but in practice, experience and creativity make a
difference in testing. We observed that in a small controlled experiment (Yu, Treude,
and Aniche, 2019).
 In the substringsBetween() example, experienced testers may see more compli-
cated test cases, but a novice tester may have difficulty spotting those. A more experi-
enced tester may realize that spaces in the string play no role and skip this test,
whereas a novice developer may be in doubt and write an extra “useless” test. This is
why I like the specification-based testing systematic approach I described in this
chapter: it will help you remember what to think about. But it is still up to you to do
the thinking!
Exercises
2.1
Which statement is false about applying the specification-based testing method
on the following Java method?
/**
 * Puts the supplied value into the Map,
 * mapped by the supplied key.
 * If the key is already in the map, its
 * value will be replaced by the new value.
 *
 * NOTE: Nulls are not accepted as keys;
 *  a RuntimeException is thrown when key is null.
 *
 * @param key the key used to locate the value
 * @param value the value to be stored in the HashMap
 * @return the prior mapping of the key,
 *  or null if there was none.
*/
public V put(K key, V value) {
  // implementation here
}
… as well as for 
many items in 
the cart.


