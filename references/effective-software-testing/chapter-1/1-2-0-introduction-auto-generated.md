# 1.2.0 Introduction [auto-generated] (pp.11-12)

---
**Page 11**

11
Effective software testing for developers
    if(lowestEstimate == null ||
        estimate.getEstimate() < lowestEstimate.getEstimate()) {
      lowestEstimate = estimate;
    }
  }
  if(lowestEstimate.equals(highestEstimate))  
    return Collections.emptyList();
  return Arrays.asList(
      lowestEstimate.getDeveloper(),
      highestEstimate.getDeveloper()
  );
}
Eleanor then writes a test to ensure that her implementation is correct.
@Test
void allDevelopersWithTheSameEstimate() {
  List<Estimate> list = Arrays.asList(  
      new Estimate("Mauricio", 10),
      new Estimate("Arie", 10),
      new Estimate("Andy", 10),
      new Estimate("Frank", 10),
      new Estimate("Annibale", 10)
  );
  List<String> devs = new PlanningPoker().identifyExtremes(list);
  assertThat(devs).isEmpty();  
}
Eleanor is now satisfied with the test suite she has engineered from the requirements.
As a next step, she decides to focus on the code itself. Maybe there is something that
no tests are exercising. To help her in this analysis, she runs the code coverage tool
that comes with her IDE (figure 1.3).
 All the lines and branches of the code are covered. Eleanor knows that tools are
not perfect, so she examines the code for other cases. She cannot find any, so she con-
cludes that the code is tested enough. She pushes the code and goes home for the
weekend. The code goes directly to the customers. On Monday morning, Eleanor is
happy to see that monitoring does not report a single crash.
1.2
Effective software testing for developers
I hope the difference is clear between the two developers in the previous section. Elea-
nor used automated tests and systematically and effectively engineered test cases. She
broke down the requirements into small parts and used them to derive test cases,
applying a technique called domain testing. When she was done with the specification,
Listing 1.9
Testing for an empty list if the estimates are all the same
If the lowest and highest 
estimate objects are the same, 
all developers have the same 
estimate, and therefore we 
return an empty list.
Declares a list of estimates, 
this time with all the 
developers having the 
same estimate
Asserts that the 
resulting list is empty


---
**Page 12**

12
CHAPTER 1
Effective and systematic software testing
she focused on the code; and through structural testing (or code coverage), she evalu-
ated whether the current test cases were sufficient. For some test cases, Eleanor wrote
example-based tests (that is, she picked a single data point for a test). For one specific
case, she used property-based testing, as it helped her better explore possible bugs in the
code. Finally, she reflected frequently about the contracts and pre- and post-conditions of
the method she was devising (although in the end, she implemented a set of valida-
tion checks and not pre-conditions per se; we discuss the differences between con-
tracts and validation in chapter 4).
 This is what I call effective and systematic software testing for developers. In the remain-
der of this chapter, I explain how software developers can perform effective testing
together with their development activities. Before we dive into the specific techniques,
I describe effective testing within the development processes and how testing tech-
niques complement each other. I discuss the different types of tests and which ones
you should focus on. Finally, I illustrate why software testing is so difficult.
1.2.1
Effective testing in the development process
In this book, I propose a straightforward flow for developers who apply effective and
systematic testing. First, we implement a feature, using tests to facilitate and guide
development. Once we are reasonably happy with the feature or small unit we’ve
coded, we dive into effective and systematic testing to ensure that it works as expected
(that is, we test to find bugs). Figure 1.4 illustrates the development workflow in more
detail; let’s walk through it:
IntelliJ indicates that these
lines are covered by adding
a color near the line. Green
indicates the line is covered;
red indicates the line is not
covered.
Here, due to the monochrome
ﬁgure, you can't see the green
color, but all lines are green.
Figure 1.3
The result of the code coverage analysis done by my IDE, IntelliJ. All lines are covered.


