Line 1: 
Line 2: --- 페이지 290 ---
Line 3: 14
Line 4: Driving the Database Layer
Line 5: In this chapter, we will implement a database adapter for one of our ports in the domain model, 
Line 6: represented by the WordRepository interface. This will allow our domain model to fetch words 
Line 7: to guess from a real database, in this case, using the popular open source database Postgres. We will 
Line 8: test-drive both the database setup and the code that accesses the database. To help us do that, we will 
Line 9: use a test framework that is designed to simplify writing database integration tests, called DBRider.
Line 10: By the end of the chapter, we will have written an integration test against a running database, 
Line 11: implemented the fetchesWordByNumber() method from the WordRepository interface, 
Line 12: and used the JDBI database access library to help us. We will create a database user with permissions 
Line 13: on a table storing words to guess. We will create that table, then write a SQL query that JDBI will use 
Line 14: to retrieve the word we are looking for. We will use a named parameter SQL query to avoid some 
Line 15: application security issues caused by SQL injections.
Line 16: In this chapter, we’re going to cover the following main topics:
Line 17: •	 Creating a database integration test
Line 18: •	 Implementing the word repository adapter
Line 19: Technical requirements
Line 20: The final code for this chapter can be found at https://github.com/PacktPublishing/
Line 21: Test-Driven-Development-with-Java/tree/main/chapter14.
Line 22: Installing the Postgres database
Line 23: We will be using the Postgres database in this chapter, which needs installation. To install Postgres, 
Line 24: follow these steps:
Line 25: 1.	
Line 26: Go to the following web page: https://www.postgresql.org/download/.
Line 27: 2.	
Line 28: Follow the installation instructions for your operating system.
Line 29: The code has been tested with version 14.5. It is expected to work on all versions.
Line 30: 
Line 31: --- 페이지 291 ---
Line 32: Driving the Database Layer
Line 33: 268
Line 34: With the setup completed, let’s get started implementing our database code. In the next section, we 
Line 35: will use the DBRider framework to create a database integration test.
Line 36: Creating a database integration test
Line 37: In this section, we will create the skeleton of a database integration test using a test framework called 
Line 38: DBRider. We will use this test to drive out the creation of a database table and database user. We will 
Line 39: be working towards implementing the WordRepository interface, which will access words stored 
Line 40: in a Postgres database.
Line 41: Previously, we created a domain model for our Wordz application, using hexagonal architecture to 
Line 42: guide us. Instead of accessing a database directly, our domain model uses an abstraction, known as a 
Line 43: port in hexagonal terminology. One such port is the WordRepository interface, which represents 
Line 44: stored words for guessing.
Line 45: Ports must always be implemented by adapters in hexagonal architecture. An adapter for the 
Line 46: WordRepository interface will be a class that implements the interface, containing all the code 
Line 47: needed to access the real database.
Line 48: To test-drive this adapter code, we will write an integration test, using a library that supports testing 
Line 49: databases. The library is called DBRider, and is one of the dependencies listed in the project’s gradle.
Line 50: build file:
Line 51: dependencies {
Line 52:     testImplementation 'org.junit.jupiter:junit-jupiter-
Line 53: api:5.8.2'
Line 54:     testRuntimeOnly 'org.junit.jupiter:junit-jupiter-
Line 55: engine:5.8.2'
Line 56:     testImplementation 'org.assertj:assertj-core:3.22.0'
Line 57:     testImplementation 'org.mockito:mockito-core:4.8.0'
Line 58:     testImplementation 'org.mockito:mockito-junit-
Line 59: jupiter:4.8.0'
Line 60:     testImplementation 'com.github.database-rider:rider-
Line 61: core:1.33.0'
Line 62:     testImplementation 'com.github.database-rider:rider-
Line 63: junit5:1.33.0'
Line 64:     implementation 'org.postgresql:postgresql:42.5.0'
Line 65: }
Line 66: 
Line 67: --- 페이지 292 ---
Line 68: Creating a database integration test
Line 69: 269
Line 70: DBRider has an accompanying library called rider-junit5, which integrates with JUnit5. With this 
Line 71: new test tooling, we can start to write our test. The first thing to do is set up the test so that it uses 
Line 72: DBRider to connect to our Postgres database.
Line 73: Creating a database test with DBRider
Line 74: Before we test-drive any application code, we will need a test that is connected to our Postgres database, 
Line 75: running locally. We start in the usual way, by writing a JUnit5 test class:
Line 76: 1.	
Line 77: Create a new test class file in the /test/ directory in the new com.wordz.adapters.
Line 78: db package:
Line 79: Figure 14.1 – Integration test
Line 80: The IDE will generate the empty test class for us.
Line 81: 2.	
Line 82: Add the @DBRider and @DBUnit annotations to the test class:
Line 83: @DBRider
Line 84: @DBUnit(caseSensitiveTableNames = true,
Line 85:         caseInsensitiveStrategy= Orthography.LOWERCASE)
Line 86: public class WordRepositoryPostgresTest {
Line 87: }
Line 88: The parameters in the @DBUnit annotation mitigate some odd interactions between Postgres 
Line 89: and the DBRider test framework to do with case sensitivity on table and column names.
Line 90: 3.	
Line 91: We want to test that a word can be fetched. Add an empty test method:
Line 92:     @Test
Line 93:     void fetchesWord()  {
Line 94:     }
Line 95: 
Line 96: --- 페이지 293 ---
Line 97: Driving the Database Layer
Line 98: 270
Line 99: 4.	
Line 100: Run the test. It will fail:
Line 101: Figure 14.2 – DBRider cannot connect to the database
Line 102: 5.	
Line 103: The next step to fixing this is to follow the DBRider documentation and add code that will 
Line 104: be used by the DBRider framework. We add a connectionHolder field and a javax.
Line 105: sqlDataSource field to support that:
Line 106: @DBRider
Line 107: public class WordRepositoryPostgresTest {
Line 108:     private DataSource dataSource;
Line 109:     private final ConnectionHolder connectionHolder
Line 110:                 = () -> dataSource.getConnection();
Line 111: }
Line 112: The dataSource is the standard JDBC way of creating a connection to our Postgres database. 
Line 113: We run the test. It fails with a different error message:
Line 114: Figure 14.3 – dataSource is null
Line 115: 6.	
Line 116: We correct this by adding a @BeforeEach method to set up dataSource:
Line 117:     @BeforeEach
Line 118:     void setupConnection() {
Line 119:         var ds = new PGSimpleDataSource();
Line 120:         ds.setServerNames(new String[]{"localhost"});
Line 121:         ds.setDatabaseName("wordzdb");
Line 122:         ds.setCurrentSchema("public");
Line 123:         ds.setUser("ciuser");
Line 124: 
Line 125: --- 페이지 294 ---
Line 126: Creating a database integration test
Line 127: 271
Line 128:         ds.setPassword("cipassword");
Line 129:         this.dataSource = ds;
Line 130:     }
Line 131: This specifies we want a user called ciuser with the password cipassword to connect to 
Line 132: a database called wordzdb, running on localhost at the default port for Postgres (5432).
Line 133: 7.	
Line 134: Run the test and see it fail:
Line 135: Figure 14.4 – User does not exist
Line 136: The error is caused because we do not have a ciuser user known to our Postgres database 
Line 137: yet. Let’s create one.
Line 138: 8.	
Line 139: Open a psql terminal and create the user:
Line 140: create user ciuser with password 'cipassword';
Line 141: 9.	
Line 142: Run the test again:
Line 143: Figure 14.5 – Database not found
Line 144: It fails because the DBRider framework is looking to connect our new ciuser user to the 
Line 145: wordzdb database. This database does not exist.
Line 146: 
Line 147: --- 페이지 295 ---
Line 148: Driving the Database Layer
Line 149: 272
Line 150: 10.	 In the psql terminal, create the database:
Line 151: create database wordzdb;
Line 152: 11.	 Run the test again:
Line 153: Figure 14.6 – Test passes
Line 154: The fetchesWord() test now passes. We recall that the test method itself is empty, but this means 
Line 155: we have enough database set up to proceed with test-driving production code. We will return to 
Line 156: database setup soon enough, but we will allow our test-driving to guide us. The next job is to add the 
Line 157: missing Arrange, Act, and Assert code to the fetchesWord() test.
Line 158: Driving out the production code
Line 159: Our goal is to test-drive code to fetch a word from the database. We want that code to be in a class that 
Line 160: implements the WordRepository interface, which we defined in the domain model. We will want 
Line 161: to design enough of our database schema to support this. By starting to add code to the Assert step, 
Line 162: we can drive out an implementation quickly. This is a useful technique – writing the test by starting 
Line 163: with the assert, so that we start with the desired outcome. We can then work backward to include 
Line 164: everything necessary for delivering it:
Line 165: 1.	
Line 166: Add the Assert step to our fetchesWord() test:
Line 167:     @Test
Line 168:     public void fetchesWord()  {
Line 169:         String actual = "";
Line 170:         assertThat(actual).isEqualTo("ARISE");
Line 171:     }
Line 172: We want to check that we can fetch the word ARISE from the database. This test fails. We need 
Line 173: to create a class to contain the necessary code.
Line 174: 
Line 175: --- 페이지 296 ---
Line 176: Creating a database integration test
Line 177: 273
Line 178: 2.	
Line 179: We want our new adapter class to implement the WordRepository interface, so we drive 
Line 180: this out in the Arrange step of our test:
Line 181:     @Test
Line 182:     public void fetchesWord()  {
Line 183:         WordRepository repository
Line 184:                  = new WordRepositoryPostgres();
Line 185:         String actual = "";
Line 186:         assertThat(actual).isEqualTo("ARISE");
Line 187:     }
Line 188: 3.	
Line 189: We now let the IDE wizard do most of the work in creating our new adapter class. Let’s call 
Line 190: it WordRepositoryPostgres, which links the two facts that the class implements the 
Line 191: WordRepository interface and is also implementing access to a Postgres database. We use 
Line 192: the New Class wizard and place it in a new package, com.wordz.adapters.db:
Line 193: Figure 14.7 – New Class wizard
Line 194: This results in an empty skeleton for the class:
Line 195: package com.wordz.adapters.db;
Line 196: import com.wordz.domain.WordRepository;
Line 197: public class WordRepositoryPostgres implements
Line 198:                                      WordRepository {
Line 199: }
Line 200: 
Line 201: --- 페이지 297 ---
Line 202: Driving the Database Layer
Line 203: 274
Line 204: 4.	
Line 205: The IDE will auto-generate method stubs for the interface:
Line 206: public class WordRepositoryPostgres implements 
Line 207: WordRepository {
Line 208:     @Override
Line 209:     public String fetchWordByNumber(int number) {
Line 210:         return null;
Line 211:     }
Line 212:     @Override
Line 213:     public int highestWordNumber() {
Line 214:         return 0;
Line 215:     }
Line 216: }
Line 217: 5.	
Line 218: Returning to our test, we can add the act line, which will call the fetchWordByNumber() method:
Line 219:     @Test
Line 220:     public void fetchesWord()  {
Line 221:         WordRepository repository
Line 222:                     = new WordRepositoryPostgres();
Line 223:         String actual =
Line 224:                repository.fetchWordByNumber(27);
Line 225:         assertThat(actual).isEqualTo("ARISE");
Line 226:     }
Line 227: A word of explanation about the mysterious constant 27 passed in to the fetchWordByNumber() 
Line 228: method. This is an arbitrary number used to identify a particular word. Its only hard requirement 
Line 229: is that it must line up with the word number given in the stub test data, which we will see a 
Line 230: little later in a JSON file. The actual value of 27 is of no significance beyond lining up with the 
Line 231: word number of the stub data.
Line 232: 6.	
Line 233: Pass dataSource in to the WordRepositoryPostgres constructor so that our class 
Line 234: has a way to access the database:
Line 235:     @Test
Line 236:     public void fetchesWord()  {
Line 237:         WordRepository repository
Line 238:               = new
Line 239: 
Line 240: --- 페이지 298 ---
Line 241: Creating a database integration test
Line 242: 275
Line 243:                 WordRepositoryPostgres(dataSource);
Line 244:         String actual = adapter.fetchWordByNumber(27);
Line 245:         assertThat(actual).isEqualTo("ARISE");
Line 246:     }
Line 247: This drives out a change to the constructor:
Line 248:     public WordRepositoryPostgres(DataSource dataSource){
Line 249:         // Not implemented
Line 250:     }
Line 251: 7.	
Line 252: The last bit of setup to do in our test is to populate the database with the word ARISE. We do 
Line 253: this using a JSON file that the DBRider framework will apply to our database on test startup:
Line 254: {
Line 255:   "word": [
Line 256:     {
Line 257:       "word_number": 27,
Line 258:       "word": "ARISE"
Line 259:     }
Line 260:   ]
Line 261: }
Line 262: The "word_number": 27 code here corresponds to the value used in the test code.
Line 263: 8.	
Line 264: This file must be saved in a specific location so that DBRider can find it. We call the file 
Line 265: wordTable.json and save it in the test directory, in /resources/adapters/data:
Line 266: Figure 14.8 – Location of wordTable.json
Line 267: 
Line 268: --- 페이지 299 ---
Line 269: Driving the Database Layer
Line 270: 276
Line 271: 9.	
Line 272: The final step in setting up our failing test is to link the test data wordTable.json file to 
Line 273: our fetchesWord() test method. We do this using the DBRider @DataSet annotation:
Line 274:     @Test
Line 275:     @DataSet("adapters/data/wordTable.json")
Line 276:     public void fetchesWord()  {
Line 277:         WordRepository repository
Line 278:             = new WordRepositoryPostgres(dataSource);
Line 279:         String actual =
Line 280:                     repository.fetchWordByNumber(27);
Line 281:         assertThat(actual).isEqualTo("ARISE");
Line 282:     }
Line 283: The test now fails and is in a position where we can make it pass by writing the database access code. 
Line 284: In the next section, we will use the popular library JDBI to implement database access in an adapter 
Line 285: class for our WordRepository interface.
Line 286: Implementing the WordRepository adapter
Line 287: In this section, we will use the popular database library JDBI to implement the fetchWordByNumber() 
Line 288: method of interface WordRepository and make our failing integration test pass.
Line 289: Hexagonal architectures were covered in Chapter 9, Hexagonal Architecture – Decoupling External 
Line 290: Systems. An external system like a database is accessed through a port in the domain model. The code 
Line 291: that is specific to that external system is contained in an adapter. Our failing test enables us to write 
Line 292: the database access code to fetch a word to guess.
Line 293: A little bit of database design thinking needs to be done before we begin writing code. For the task 
Line 294: at hand, it is enough to note that we will store all available words to guess in a database table named 
Line 295: word. This table will have two columns. There will be a primary key named word_number and a 
Line 296: five-letter word in a column named word.
Line 297: Let’s test-drive this out:
Line 298: 1.	
Line 299: Run the test to reveal that the word table does not exist:
Line 300: Figure 14.9 – Table not found
Line 301: 
Line 302: --- 페이지 300 ---
Line 303: Implementing the WordRepository adapter
Line 304: 277
Line 305: 2.	
Line 306: Correct this by creating a word table in the database. We use the psql console to run the 
Line 307: SQL create table command:
Line 308: create table word (word_number int primary key,
Line 309: word char(5));
Line 310: 3.	
Line 311: Run the test again. The error changes to show our ciuser user has insufficient permissions:
Line 312: Figure 14.10 – Insufficient permissions
Line 313: 4.	
Line 314: We correct this by running the SQL grant command in the psql console:
Line 315: grant select, insert, update, delete on all tables in 
Line 316: schema public to ciuser;
Line 317: 5.	
Line 318: Run the test again. The error changes to show us that the word has not been read from the 
Line 319: database table:
Line 320: Figure 14.11 – Word not found
Line 321: Accessing the database
Line 322: Having set up the database side of things, we can move on to adding the code that will access the 
Line 323: database. The first step is to add the database library we will use. It is JDBI, and to use it, we must add 
Line 324: the jdbi3-core dependency to our gradle.build file:
Line 325: dependencies {
Line 326:     testImplementation 'org.junit.jupiter:junit-jupiter-
Line 327: api:5.8.2'
Line 328:     testRuntimeOnly 'org.junit.jupiter:junit-jupiter-
Line 329: 
Line 330: --- 페이지 301 ---
Line 331: Driving the Database Layer
Line 332: 278
Line 333: engine:5.8.2'
Line 334:     testImplementation 'org.assertj:assertj-core:3.22.0'
Line 335:     testImplementation 'org.mockito:mockito-core:4.8.0'
Line 336:     testImplementation 'org.mockito:mockito-junit-
Line 337: jupiter:4.8.0'
Line 338:     testImplementation 'com.github.database-rider:rider-
Line 339: core:1.35.0'
Line 340:     testImplementation 'com.github.database-rider:rider-
Line 341: junit5:1.35.0'
Line 342:     implementation 'org.postgresql:postgresql:42.5.0'
Line 343:     implementation 'org.jdbi:jdbi3-core:3.34.0'
Line 344: }
Line 345: Note
Line 346: The code itself is as described in the JDBI documentation, found here: https://jdbi.
Line 347: org/#_queries.
Line 348: Follow these steps to access the database:
Line 349: 1.	
Line 350: First, create a jdbi object in the constructor of our class:
Line 351: public class WordRepositoryPostgres
Line 352:                          implements WordRepository {
Line 353:     private final Jdbi jdbi;
Line 354:     public WordRepositoryPostgres(DataSource
Line 355:                                       dataSource){
Line 356:         jdbi = Jdbi.create(dataSource);
Line 357:     }
Line 358: }
Line 359: This gives us access to the JDBI library. We have arranged it so that JDBI will access whatever 
Line 360: DataSource we pass into our constructor.
Line 361: 2.	
Line 362: We add the JDBI code to send a SQL query to the database and fetch the word corresponding to 
Line 363: the wordNumber we provide as a method parameter. First, we add the SQL query we will use:
Line 364:    private static final String SQL_FETCH_WORD_BY_NUMBER
Line 365:      = "select word from word where "
Line 366:                       + "word_number=:wordNumber";
Line 367: 
Line 368: --- 페이지 302 ---
Line 369: Implementing the WordRepository adapter
Line 370: 279
Line 371: 3.	
Line 372: The jdbi access code can be added to the fetchWordByNumber() method:
Line 373: @Override
Line 374: public String fetchWordByNumber(int wordNumber) {
Line 375:     String word = jdbi.withHandle(handle -> {
Line 376:         var query =
Line 377:          handle.createQuery(SQL_FETCH_WORD_BY_NUMBER);
Line 378:         query.bind("wordNumber", wordNumber);
Line 379:         return query.mapTo(String.class).one();
Line 380:     });
Line 381:     return word;
Line 382: }
Line 383: 4.	
Line 384: Run the test again:
Line 385: Figure 14.12 – Test passing
Line 386: Our integration test now passes. The adapter class has read the word from the database and returned it.
Line 387: Implementing GameRepository
Line 388: The same process is used to test-drive the highestWordNumber() method and to create adapters 
Line 389: for the other database access code implementing the GameRepository interface. The final code for 
Line 390: these can be seen on GitHub with comments to explore some of the issues in database testing, such 
Line 391: as how to avoid test failures caused by stored data.
Line 392: There is a manual step needed to test-drive the implementation code for the GameRepository 
Line 393: interface. We must create a game table.
Line 394: 
Line 395: --- 페이지 303 ---
Line 396: Driving the Database Layer
Line 397: 280
Line 398: In psql, type the following:
Line 399: CREATE TABLE game (
Line 400:     player_name character varying NOT NULL,
Line 401:     word character(5),
Line 402:     attempt_number integer DEFAULT 0,
Line 403:     is_game_over boolean DEFAULT false
Line 404: );
Line 405: Summary
Line 406: In this chapter, we have created an integration test for our database. We used that to test-drive the 
Line 407: implementation of a database user, the database table, and the code needed to access our data. This 
Line 408: code implemented the adapter for one of our ports in our hexagonal architecture. Along the way, 
Line 409: we used some new tools. The DBRider database test framework simplified our test code. The JDBI 
Line 410: database access library simplified our data access code.
Line 411: In the next and final chapter, Chapter 15, Driving the Web Layer, we will add an HTTP interface to our 
Line 412: application, turning it into a complete microservice. We will integrate all the components together, 
Line 413: then play our first game of Wordz using the HTTP test tool Postman.
Line 414: Questions and answers
Line 415: 1.	
Line 416: Should we automate the manual steps of creating the database?
Line 417: Yes. This is an important part of DevOps, where we developers are responsible for getting the 
Line 418: code into production and keeping it running there. The key technique is Infrastructure as Code 
Line 419: (IaC), which means automating manual steps as code that we check in to the main repository.
Line 420: 2.	
Line 421: What tools can help with automating database creation?
Line 422: Popular tools are Flyway and Liquibase. Both allow us to write scripts that are run at application 
Line 423: startup and will migrate the database schema from one version to the next. They assist in migrating 
Line 424: data across schema changes where that is required. These are outside the scope of this book.
Line 425: 3.	
Line 426: What tools can help with installing the database?
Line 427: Access to a running database server is part of platform engineering. For cloud-native designs 
Line 428: that run on Amazon Web Service, Microsoft Azure, or Google Cloud Platform, use configuration 
Line 429: scripting for that platform. One popular approach is to use Hashicorp’s Terraform, which aims 
Line 430: to be a cross-provider universal scripting language for cloud configuration. This is outside of 
Line 431: the scope of this book.
Line 432: 
Line 433: --- 페이지 304 ---
Line 434: Further reading
Line 435: 281
Line 436: 4.	
Line 437: How often should we run the integration tests?
Line 438: Before every check-in to the repository. While unit tests are fast to run and should be run all 
Line 439: the time, integration tests by nature are slower to execute. It is reasonable to run only unit 
Line 440: tests while working on domain code. We must always ensure we haven’t broken anything 
Line 441: unexpectedly. This is where running integration tests comes in. These reveal whether we have 
Line 442: accidentally changed something that affects the adapter layer code, or whether something has 
Line 443: changed regarding database layout.
Line 444: Further reading
Line 445: •	 Documentation for DBRider: https://github.com/database-rider/database-
Line 446: rider
Line 447: •	 JDBI documentation: https://jdbi.org/#_introduction_to_jdbi_3
Line 448: •	 Flyway is a library that allows us to store the SQL commands to create and modify our database 
Line 449: schema as source code. This allows us to automate database changes: https://flywaydb.
Line 450: org/
Line 451: •	 As our application design grows, our database schema will need to change. This website 
Line 452: and the accompanying books describe ways to do this while managing risk: https://
Line 453: databaserefactoring.com/
Line 454: •	 Hosting a Postgres database on Amazon Web Services using their RDS service: https://
Line 455: aws.amazon.com/rds
Line 456: 
Line 457: --- 페이지 305 ---