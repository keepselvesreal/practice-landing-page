# 5.4 Example 4: Testing the Basket class (pp.129-136)

---
**Page 129**

129
Example 4: Testing the Basket class
Jqwik will generate a large number of random inputs for this method, ensuring that
regardless of where the value to find is, and regardless of the chosen start index, the
method will always return the expected index. Notice how this property-based test bet-
ter exercises the properties of the method than the testing method we used earlier.
 I hope this example shows you that writing property-based tests requires creativity.
Here, we had to come up with the idea of generating a random value that is never in
the list so that the indexOf method could find it without ambiguity. We also had to be
creative when doing the assertion, given that the randomly generated indexToAdd-
Element could be larger or smaller than the startIndex (which would drastically
change the output). Pay attention to these two points:
1
Ask yourself, “Am I exercising the property as closely as possible to the real
world?” If you come up with input data that will be wildly different from what
you expect in the real world, it may not be a good test.
2
Do all the partitions have the same likelihood of being exercised by your test?
In the example, the element to be found is sometimes before and sometimes
after the start index. If you write a test in which, say, 95% of the inputs have the
element before the start index, you may be biasing your test too much. You
want all the partitions to have the same likelihood of being exercised.
In the example code, given that both indexToAddElement and startIndex
are random numbers between 0 and 99, we expect about a 50-50 split between
the partitions. When you are unsure about the distribution, add some debug-
ging instructions and see what inputs or partitions your test generates or
exercises. 
5.4
Example 4: Testing the Basket class
Let’s explore one last example that revisits the Basket class from chapter 4. The class
offers two methods: an add() method that receives a product and adds it a quantity
of times to the basket, and a remove() method that removes a product completely
from the cart. Let’s start with the add method.
import static java.math.BigDecimal.valueOf;
public class Basket {
  private BigDecimal totalValue = BigDecimal.ZERO;
  private Map<Product, Integer> basket = new HashMap<>();
  public void add(Product product, int qtyToAdd) {
    assert product != null : "Product is required";               
    assert qtyToAdd > 0 : "Quantity has to be greater than zero"; 
    BigDecimal oldTotalValue = totalValue; 
Listing 5.12
Implementation of Baskets add method
Checks all the
pre-conditions
Stores the old value so we can check 
the post-condition later


---
**Page 130**

130
CHAPTER 5
Property-based testing
    int existingQuantity = basket.getOrDefault(product, 0); 
    int newQuantity = existingQuantity + qtyToAdd;
    basket.put(product, newQuantity);
    BigDecimal valueAlreadyInTheCart = product.getPrice()
      .multiply(valueOf(existingQuantity)); 
    BigDecimal newFinalValueForTheProduct = product.getPrice()
      .multiply(valueOf(newQuantity));      
    totalValue = totalValue
      .subtract(valueAlreadyInTheCart)
      .add(newFinalValueForTheProduct); 
    assert basket.containsKey(product) : "Product was not inserted in     
    ➥ the basket";                                                       
    assert totalValue.compareTo(oldTotalValue) == 1 : "Total value should 
    ➥ be greater than previous total value";                             
    assert invariant() : "Invariant does not hold";                       
  }
}
The implementation is straightforward. First it does the pre-condition checks we dis-
cussed in chapter 4. The product cannot be null, and the quantity of the product to
be added to the cart has to be larger than zero. Then the method checks whether the
basket already contains the product. If so, it adds the quantity on top of the quantity
already in the cart. It then calculates the value to add to the total value of the basket.
To do so, it calculates the value of that product based on the previous amount in the
basket, subtracts that from the total value, and then adds the new total value for that
product. Finally, it ensures that the invariant (the total value of the basket must be
positive) still holds.
 The remove method is simpler than the add method. It looks for the product in
the basket, calculates the amount it needs to remove from the total value of the bas-
ket, subtracts it, and removes the product (listing 5.13). The method also ensures
the same two pre-conditions we discussed before: the product cannot be null, and
the product has to be in the basket.
public void remove(Product product) {
    assert product != null : "product can't be null";                 
    assert basket.containsKey(product) : "Product must already be in  
    ➥ the basket";                                                   
    int qty = basket.get(product);
    BigDecimal productPrice = product.getPrice();             
    BigDecimal productTimesQuantity = productPrice.multiply(  
      ➥ valueOf(qty));                                       
    totalValue = totalValue.subtract(productTimesQuantity);   
Listing 5.13
Implementation of Baskets remove method
If the product 
is already in the 
cart, add to it.
Calculates the
previous and the
new value of the
product for the
relevant quantities
Subtracts the previous value of the 
product from the total value of the 
basket and adds the new final value 
of the product to it
Post-conditions and 
invariant checks
Pre-
conditions
check
Calculates the 
amount that 
should be removed 
from the basket


---
**Page 131**

131
Example 4: Testing the Basket class
    basket.remove(product); 
    assert !basket.containsKey(product) : "Product is still  
    ➥ in the basket";                                       
    assert invariant() : "Invariant does not hold";          
  }
A developer who did not read the chapters on specification-based testing and struc-
tural testing would come up with at least three tests: one to ensure that add() adds the
product to the cart, another to ensure that the method behaves correctly when
the same product is added twice, and one to ensure that remove() indeed removes
the product from the basket. Then they would probably add a few tests for the excep-
tional cases (which in this class are clearly specified in the contracts). Here are the
automated test cases.
import static java.math.BigDecimal.valueOf;
public class BasketTest {
  private Basket basket = new Basket();
  @Test
  void addProducts() { 
    basket.add(new Product("TV", valueOf(10)), 2);
    basket.add(new Product("Playstation", valueOf(100)), 1);
    assertThat(basket.getTotalValue())
        .isEqualByComparingTo(valueOf(10*2 + 100*1));
  }
  @Test
  void addSameProductTwice() { 
    Product p = new Product("TV", valueOf(10));
    basket.add(p, 2);
    basket.add(p, 3);
    assertThat(basket.getTotalValue())
        .isEqualByComparingTo(valueOf(10*5));
  }
  @Test
  void removeProducts() { 
    basket.add(new Product("TV", valueOf(100)), 1);
    Product p = new Product("PlayStation", valueOf(10));
    basket.add(p, 2);
    basket.remove(p);
    assertThat(basket.getTotalValue())
        .isEqualByComparingTo(valueOf(100)); 
  }
Listing 5.14
Non-systematic tests for the Basket class
Removes the product 
from the hashmap
Post-conditions 
and invariant 
check
Ensures that 
products are added 
to the basket
If the same product is 
added twice, the basket 
sums up the quantities.
Ensures that products are 
removed from the basket
Food for thought: is this 
assertion enough? You 
might also want to verify 
that PlayStation is not in 
the basket.


---
**Page 132**

132
CHAPTER 5
Property-based testing
  // tests for exceptional cases...
}
NOTE
I used the isEqualByComparingTo assert instruction. Remember that
BigDecimals are instances of a strange class, and the correct way to compare
one BigDecimal to another is with the compareTo() method. That is what the
isEqualByComparingTo assertion does. Again, the BigDecimal class is not
easy to handle.
The problem with these tests is that they do not exercise the feature extensively. If
there is a bug in our implementation, it is probably hidden and will only appear after
a long and unexpected sequence of adds and removes to and from the basket. Finding
this specific sequence might be hard to see, even after proper domain and structural
testing. However, we can express it as a property: given any arbitrary sequence of addi-
tions and removals, the basket still calculates the correct final amount. We have to cus-
tomize jqwik so that it understands how to randomly call a sequence of add()s and
remove()s, as shown in figure 5.2.
Fasten your seatbelt, because this takes a lot of code. The first step is to create a bunch
of jqwik Actions to represent the different actions that can happen with the basket.
Actions are a way to explain to the framework how to execute a more complex action.
In our case, two things can happen: we can add a product to the basket, or we can
remove a product from the basket. We define how these two actions work so that later,
jqwik can generate a random sequence of actions.
 Let’s start with the add action. It will receive a Product and a quantity and insert
the Product into the Basket. The action will then ensure that the Basket behaved as
expected by comparing its current total value against the expected value. Note that
everything happens in the run() method: this method is defined by jqwik’s Action
interface, which our action implements. In practice, jqwik will call this method when-
ever it generates an add action and passes the current basket to the run method. The
following listing shows the implementation of the AddAction class.
 
Add
Remove
Add
Add
Remove
Add
Add
Add
Remove
Add
Add
Add
Add
Remove
Add
Remove Remove
T1 =
T2 =
T3 =
We want to call arbitrary sequences
of adds and removes and assert that
the basket is still in a correct state.
T4 =
….
Figure 5.2
We want our test to call arbitrary sequences of add and remove 
actions.


---
**Page 133**

133
Example 4: Testing the Basket class
class AddAction
  implements Action<Basket> { 
  private final Product product;
  private final int qty;
  public AddAction(Product product, int qty) { 
    this.product = product;
    this.qty = qty;
  }
  @Override
  public Basket run(Basket basket) { 
    BigDecimal currentValue = basket.getTotalValue(); 
    basket.add(product, qty); 
    BigDecimal newProductValue = product.getPrice()
      .multiply(valueOf(qty));
    BigDecimal newValue = currentValue.add(newProductValue);
    assertThat(basket.getTotalValue())
      .isEqualByComparingTo(newValue); 
    return basket; 
  }
}
Now let’s implement the remove action. This is tricky: we need a way to get the set of
products that are already in the basket and their quantities. Note that we do not
have such a method in the Basket class. The simplest thing to do is add such a
method to the class.
 You might be thinking that adding more methods for the tests is a bad idea. It’s a
trade-off. I often favor anything that eases testing. An extra method will not hurt and
will help our testing, so I’d do it, as shown next.
class Basket {
  // ... the code of the class here ...
  public int quantityOf(Product product) { 
    assert basket.containsKey(product);
    return basket.get(product);
  }
  public Set<Product> products() { 
    return Collections.unmodifiableSet(basket.keySet());
  }
}
Listing 5.15
The AddAction action
Listing 5.16
Basket class modified to support the test
Actions have to implement the 
jqwik Action interface.
The constructor receives 
a product and a quantity. 
These values will be randomly 
generated later by jqwik.
The run method receives a 
Basket and, in this case, adds 
a new random product to it.
Gets the current total 
value of the basket, 
so we can make the 
assertion later
Adds the
product to
the basket
Asserts that the value of the basket 
is correct after the addition
Returns the current basket so 
the next action starts from it
We only return the quantity if 
the product is in the cart. Note 
that here, we could have gone 
for a weaker pre-condition: for 
example, if the product is not 
in the basket, return 0.
Returns a copy of 
the set, not the 
original one!


---
**Page 134**

134
CHAPTER 5
Property-based testing
The remove action picks a random product from the basket, removes it, and then
ensures that the current total value is the total value minus the value of the product
that was just removed. The pickRandom() method chooses a random product from
the set of products; I do not show the code here, to save space, but you can find it in
the book’s code repository.
class RemoveAction implements Action<Basket> {
  @Override
  public Basket run(Basket basket) {
    BigDecimal currentValue = basket.getTotalValue(); 
    Set<Product> productsInBasket = basket.products(); 
    if(productsInBasket.isEmpty()) {
      return basket;
    }
    Product randomProduct = pickRandom(productsInBasket); 
    double currentProductQty = basket.quantityOf(randomProduct);
    basket.remove(randomProduct);
    BigDecimal basketValueWithoutRandomProduct = currentValue
      .subtract(randomProduct.getPrice()
      .multiply(valueOf(currentProductQty))); 
    assertThat(basket.getTotalValue())
      .isEqualByComparingTo(basketValueWithoutRandomProduct); 
    return basket; 
  }
  // ...
}
Jqwik now knows how to call add() (via AddAction) and remove() (via RemoveAction).
The next step is to explain how to instantiate random products and sequences of
actions. Let’s start by explaining to jqwik how to instantiate an arbitrary AddAction.
First we randomly pick a product from a predefined list of products. Then we gener-
ate a random quantity value. Finally, we add the random product in the random quan-
tity to the basket.
class BasketTest {
  // ...
  private Arbitrary<AddAction> addAction() {
    Arbitrary<Product> products = Arbitraries.oneOf( 
      randomProducts
        .stream()
        .map(product -> Arbitraries.of(product))
        .collect(Collectors.toList()));
Listing 5.17
The RemoveAction class
Listing 5.18
Instantiating add actions
Gets the current
value of the
basket for the
assertion later
If the basket is 
empty, we skip this 
action. This may 
happen, as we do not 
control the sequence 
jqwik generates.
Picks a
random
element in
the basket
to be
removed
Calculates the new 
value of the basket
Asserts the value of the
basket without the random
product we removed
Returns the current 
basket so the next action 
can continue from here
Creates an arbitrary 
product out of the 
list of predefined 
products


---
**Page 135**

135
Example 4: Testing the Basket class
    Arbitrary<Integer> qtys =
      Arbitraries.integers().between(1, 100); 
    return Combinators
        .combine(products, qtys)
        .as((product, qty) -> new AddAction(product, qty)); 
  }
  static List<Product> randomProducts = new ArrayList<>() {{   
    add(new Product("TV", new BigDecimal("100")));
    add(new Product("PlayStation", new BigDecimal("150.3")));
    add(new Product("Refrigerator", new BigDecimal("180.27")));
    add(new Product("Soda", new BigDecimal("2.69")));
  }};
}
This is a complex piece of code, and it involves a lot of details about how jqwik works.
Let’s digest it step by step:
1
Our first goal is to randomly select an arbitrary Product from the list of products.
To do so, we use jqwik’s Arbitraries.oneOf() method, which randomly picks an
arbitrary element of a given set of options. Given that the oneOf method needs a
List<Arbitrary<Product>>, we have to convert our randomProducts (which
is a List<Product>). This is easily done using Java’s Stream API.
2
We generate a random integer that will serve as the quantity to pass to the add()
method. We define an Arbitrary<Integer> with numbers between 1 and 100
(random choices that I made after exploring the method’s source code).
3
We return an AddAction that is instantiated using a combination of arbitrary
products and quantities.
We can now create our test. The property test should receive an ActionSequence, which
we define as an arbitrary sequence of AddActions and RemoveActions. We do so with the
Arbitraries.sequences() method. Let’s define this in an addsAndRemoves method.
 We also need arbitrary remove actions, as we did for add actions, but this is much
simpler since the RemoveAction class does not receive anything in its constructor. So,
we use Arbitraries.of().
private Arbitrary<RemoveAction> removeAction() {
  return Arbitraries.of(new RemoveAction()); 
}
@Provide
Arbitrary<ActionSequence<Basket>> addsAndRemoves() {
  return Arbitraries.sequences(Arbitraries.oneOf( 
      addAction(),
      removeAction()));
}
Listing 5.19
Adding remove actions to the test
Creates arbitrary 
quantities
Combines products 
and quantities, and 
generates AddActions
A static list of 
hard-coded 
products
Returns an arbitrary 
remove action
This is where the magic 
happens: jqwik generates 
random sequences of add 
and remove actions.


---
**Page 136**

136
CHAPTER 5
Property-based testing
We now only need a @Property test method that runs the different sequences of
actions generated by the addsAndRemoves method.
@Property
void sequenceOfAddsAndRemoves(
  @ForAll("addsAndRemoves") 
  ActionSequence<Basket> actions) {
    actions.run(new Basket());
}
And we are finished. As soon as we run the test, jqwik randomly invokes sequences of
adds and removes, passing random Products and quantities and ensuring that the
value of the basket is always correct.
 This was a long, complex property-based test, and you may be wondering if it is
worth the effort. For this specific Basket implementation, I would probably write thor-
ough example-based tests. But I hope this example illustrates the power of property-
based testing. Although they tend to be more complicated than traditional example-
based tests, you will get used to it, and you will soon be writing them quickly. 
5.5
Example 5: Creating complex domain objects
Building more complex objects may come in handy when testing business systems.
This can be done using jqwik’s Combinators feature, which we’ll use in the following
listing. Imagine that we have the following Book class, and we need to generate differ-
ent books for a property-based test.
public class Book {
  private final String title;
  private final String author;
  private final int qtyOfPages;
  public Book(String title, String author, int qtyOfPages) {
    this.title = title;
    this.author = author;
    this.qtyOfPages = qtyOfPages;
  }
  // getters...
}
One way to do this would be to have a property test that receives three parameters: a
String for title, a String for author, and an Integer for quantity of pages. Inside
the property test, we would instantiate the Book class. Jqwik offers a better way to do
that, as shown in the next listing.
Listing 5.20
Property-based test that generates adds and removes
Listing 5.21
A simple Book class
The property receives 
a sequence of Basket 
actions defined by the 
addsAndRemoves method.


