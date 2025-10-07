Line 1: 
Line 2: --- 페이지 429 ---
Line 3: 403
Line 4: Type-safe concurrent
Line 5: programming
Line 6: In Idris, a value of type IO () describes a sequence of actions for interacting with
Line 7: the user and operating system, which the runtime system executes sequentially. That
Line 8: is, it only executes one action at a time. You can refer to a sequence of interactive
Line 9: actions as a process.
Line 10:  As well as executing actions in sequence in a single process, it’s often useful to
Line 11: be able to execute multiple processes at the same time, concurrently, and to allow
Line 12: those processes to communicate with each other. In this chapter, I’ll introduce con-
Line 13: current programming in Idris.
Line 14: MESSAGE PASSING
Line 15: Concurrent programming is a large topic, and there
Line 16: are several approaches to it that would fill books of their own. We’ll look
Line 17: at some small examples of message-passing concurrency, where processes
Line 18: This chapter covers
Line 19: Using concurrency primitives
Line 20: Defining a type for describing concurrent processes
Line 21: Using types to ensure concurrent processes 
Line 22: communicate consistently
Line 23: 
Line 24: --- 페이지 430 ---
Line 25: 404
Line 26: CHAPTER 15
Line 27: Type-safe concurrent programming
Line 28: interact by sending messages to each other. Message passing is supported as a
Line 29: primitive by the Idris runtime system. In effect, sending a message to a pro-
Line 30: cess and receiving a reply corresponds to calling a method that returns a
Line 31: result in an object-oriented language.
Line 32: Concurrent programming has several advantages:
Line 33: You can continue to interact with a user while a large computation runs. For
Line 34: example, a user can continue browsing a web page while a large file downloads.
Line 35: You can display feedback on the progress of a large computation running in
Line 36: another process, such as displaying a progress bar for a download.
Line 37: You can take full advantage of the processing power of modern CPUs, dividing
Line 38: work between multiple processes running on separate CPU cores.
Line 39: This chapter presents a larger example of type-driven development. First, I’ll intro-
Line 40: duce the primitives for concurrent programming in Idris, and describe the problems
Line 41: that can arise in concurrent processes in general. Then, I’ll present an initial attempt
Line 42: at a type for describing concurrent processes. This initial attempt will have some
Line 43: shortcomings, so we’ll refine it and arrive at a type that allows processes to communi-
Line 44: cate with each other safely and consistently.
Line 45: 15.1
Line 46: Primitives for concurrent programming in Idris
Line 47: The Idris base library provides a module, System.Concurrency.Channels, that con-
Line 48: tains primitives for starting concurrent processes and for allowing those processes to
Line 49: communicate with each other. This allows you, in theory, to write applications that
Line 50: make efficient use of your CPUs and that remain responsive even when executing
Line 51: complex calculations.
Line 52:  But despite its advantages, concurrent programming is notoriously error-prone.
Line 53: The need for multiple processes to interact with each other greatly increases a pro-
Line 54: gram’s complexity. For example, if you’re displaying a progress bar while a file down-
Line 55: loads, the process downloading the file needs to coordinate with the process
Line 56: displaying the progress bar so that it knows how much of the file is downloaded. This
Line 57: complexity leads to new ways in which programs can fail at runtime:
Line 58: Deadlock—Two or more processes are waiting for each other to perform some
Line 59: action before they can continue.
Line 60: Race conditions—The behavior of a system depends on the ordering of actions in
Line 61: multiple concurrent processes.
Line 62: The effect of a deadlock is that the processes concerned freeze, no longer accepting
Line 63: input or giving output. Two concurrent processes—let’s call them client and
Line 64: server—could deadlock if client is waiting to receive a message from server at the
Line 65: same time that server is waiting to receive a message from client. If this happens,
Line 66: both client and server will freeze.
Line 67: 
Line 68: --- 페이지 431 ---
Line 69: 405
Line 70: Primitives for concurrent programming in Idris
Line 71:  Race conditions can be harder to identify. The pseudocode in figure 15.1 for client
Line 72: and server illustrates a race condition, where the value of the shared variable var
Line 73: depends on the order in which the concurrent operations execute. We’ll assume that
Line 74: the Read and Write operations respectively read and write the value of a shared mutable
Line 75: variable, so Read var reads the value of the shared variable var.
Line 76: Here, client and server execute concurrently, and the final value of var depends on
Line 77: the order in which the operations A, B, C, and D are executed. A will always run before
Line 78: B, and C before D, but otherwise there are six possible orderings for the operations.
Line 79: Table 15.1 lists these orderings and the resulting value of var in each case, assuming
Line 80: an initial value of 1.
Line 81: As the table shows, with an initial value for var of 1, there are two possible results for
Line 82: var, depending on the order in which the Read and Write operations run. Here, there
Line 83: are only two processes with two operations each. As programs grow, the likelihood of
Line 84: this kind of nondeterministic result becomes much larger.
Line 85:  Later in this chapter, using a variety of techniques that we’ve discussed earlier in
Line 86: this book, you’ll see how to write concurrent programs in Idris, avoiding problems
Line 87: such as deadlock and race conditions. But first, you need to understand the primitives
Line 88: Table 15.1
Line 89: Value of var for each sequence of operations 
Line 90: in figure 15.1, given an initial value of 1 for var
Line 91: Operation order
Line 92: Value of var
Line 93: A, B, C, D
Line 94: 3
Line 95: A, C, B, D
Line 96: 2
Line 97: A, C, D, B
Line 98: 2
Line 99: C, A, B, D
Line 100: 2
Line 101: C, A, D, B
Line 102: 2
Line 103: C, D, A, B
Line 104: 3
Line 105: var
Line 106: client
Line 107: do val <- Read var     -- A
Line 108:    Write var (val + 1) -- B
Line 109: server
Line 110: do val <- Read var     -- C
Line 111:    Write var (val + 1) -- D
Line 112: Figure 15.1
Line 113: Pseudocode for client and server, in which each process 
Line 114: reads and writes a shared variable, var. This could lead to an unexpected 
Line 115: result if lines A and C are executed before lines C and D.
Line 116: 
Line 117: --- 페이지 432 ---
Line 118: 406
Line 119: CHAPTER 15
Line 120: Type-safe concurrent programming
Line 121: that the Idris base library provides for concurrent programming and see the kinds of
Line 122: problems you’ll encounter when writing processes that need to coordinate with each
Line 123: other.
Line 124: 15.1.1 Defining concurrent processes
Line 125: In a complete Idris program, the main function, which has type IO (), describes the
Line 126: actions that the runtime system will execute when the program is run. The main func-
Line 127: tion, therefore, describes the actions that are executed in a single process.
Line 128:  The actions we’ve used have described console and file I/O operations, but the
Line 129: runtime system also supports actions for starting new processes and sending messages
Line 130: between processes. There are primitive operations for the following actions:
Line 131: Creating a new process. Each process is associated with a unique process identifier
Line 132: (PID).
Line 133: Sending a message to a process identified by its PID.
Line 134: Receiving a message from another process.
Line 135: Figure 15.2 illustrates one way we can use message passing to write concurrent pro-
Line 136: cesses that communicate with each other. In this figure, main and adder are two Idris
Line 137: processes, running concurrently, where each can send a message to the other.
Line 138:  The message that main sends to adder uses the following type:
Line 139: data Message = Add Nat Nat
Line 140: In this example, after main sends the message Add 2 3 to the adder process, it expects
Line 141: to receive a reply with the result of adding 2 and 3. In this way, you can use concurrently
Line 142: running processes to implement services that respond to requests sent by other pro-
Line 143: cesses. Here, we have a service that performs addition, running in a separate process.
Line 144: Concurrent processes
Line 145: in Idris coordinate
Line 146: through messages.
Line 147: main
Line 148: adder
Line 149: Add 2 3
Line 150: 5
Line 151: Time
Line 152: Figure 15.2
Line 153: Message-passing 
Line 154: between processes. A main process 
Line 155: sends an Add 2 3 message to an 
Line 156: adder process, which replies by 
Line 157: sending a 5 message back to main.
Line 158: 
Line 159: --- 페이지 433 ---
Line 160: 407
Line 161: Primitives for concurrent programming in Idris
Line 162:  I’ll use this as a running example of concurrent processes. Next, you’ll see how to
Line 163: use the concurrency primitives that Idris provides to implement an adder service in a
Line 164: separate process, and how to use that service from main. 
Line 165: 15.1.2 The Channels library: primitive message passing
Line 166: The System.Concurrency.Channels module, in the base library, defines data types
Line 167: and actions that allow Idris processes to create new processes and communicate with
Line 168: each other. It defines the following types:
Line 169: 
Line 170: PID—Represents a process identifier. Every process is associated with a PID that
Line 171: allows you to set up a communication channel with the process.
Line 172: 
Line 173: Channel—A link between two processes. It defines a communication channel
Line 174: along which you can send messages.
Line 175: The System.Concurrency.Channels module also defines the following functions for
Line 176: creating new processes and setting up communication channels:
Line 177: 
Line 178: spawn—Creates a new process for executing a sequence of actions of type IO (),
Line 179: and if successful returns its PID.
Line 180: 
Line 181: connect—Initiates a communication channel to a running process.
Line 182: 
Line 183: listen—Waits for another process to initiate a communication. When another
Line 184: process connects, it sets up a communication channel with that process.
Line 185: Finally, the module defines operations for sending and receiving messages on a
Line 186: Channel. We’ll come to the type definitions in System.Concurrency.Channels
Line 187: shortly, but first let’s look at how the processes and channels are set up for the main
Line 188: and adder processes. The main process works as follows:
Line 189: 1
Line 190: Starts the adder process using spawn
Line 191:  2
Line 192: Sets up a communication channel to adder using connect
Line 193:  3
Line 194: Sends an Add 2 3 message on the channel
Line 195: 4
Line 196: Receives a reply on the channel with the result
Line 197: Correspondingly, the adder process works as follows:
Line 198: 1
Line 199: Waits for another process to initiate a communication using listen and sets up
Line 200: a new communication channel when another process connects
Line 201:  2
Line 202: Receives a message on the channel containing the numbers to be added
Line 203:  3
Line 204: Sends a message on the channel with the result
Line 205: 4
Line 206: Returns to step 1, waiting for the next request
Line 207: The adder process provides a long-running service that waits for incoming requests
Line 208: and sends replies to those requests. Once main has started the adder process, any
Line 209: other process can also send requests to adder, as long as it knows adder’s PID.
Line 210:  The first listing shows the type declarations for channels and PIDs in System
Line 211: .Concurrency.Channels and the functions you can use to create processes and set up
Line 212: communication channels.
Line 213: 
Line 214: --- 페이지 434 ---
Line 215: 408
Line 216: CHAPTER 15
Line 217: Type-safe concurrent programming
Line 218:  
Line 219: data PID : Type
Line 220: data Channel : Type
Line 221: spawn : (process : IO ()) -> IO (Maybe PID)
Line 222: connect : (pid : PID) -> IO (Maybe Channel)
Line 223: listen : (timeout : Int) -> IO (Maybe Channel)
Line 224: When you listen for a connection or connect to another process, there’s no guaran-
Line 225: tee that you’ll succeed in setting up a communication channel. There may be no
Line 226: incoming connection, or the process you’re connecting to may no longer be running.
Line 227: So, to capture the possibility of failure, connect and listen return a value of type
Line 228: Maybe Channel.
Line 229:  You can use spawn, listen, and connect to set up adder and main as separate pro-
Line 230: cesses. The following listing outlines a program that sets up the processes, leaving
Line 231: holes for the parts of the processes that send messages to each other.
Line 232: import System.Concurrency.Channels
Line 233: adder : IO ()
Line 234: adder = do Just sender_chan <- listen 1
Line 235: | Nothing => adder
Line 236: ?adder_rhs
Line 237: main : IO ()
Line 238: main = do Just adder_id <- spawn adder
Line 239: | Nothing => putStrLn "Spawn failed"
Line 240: Just chan <- connect adder_id
Line 241: | Nothing => putStrLn "Connection failed"
Line 242: ?main_rhs
Line 243: Now that you’ve set up the processes and channels, main can send a message to adder,
Line 244: and adder can reply. You can use the following primitives:
Line 245: 
Line 246: unsafeSend—Sends a message of any type
Line 247: 
Line 248: unsafeRecv—Receives a message of an expected type
Line 249: As the names imply, these primitives are unsafe, because they don’t provide a way of
Line 250: checking that the sender and receiver are expecting messages to be sent in a specific
Line 251: Listing 15.1
Line 252: Channels and PIDs (defined in System.Concurrency.Channels)
Line 253: Listing 15.2
Line 254: Outline of a program that sets up an adder process (AdderChannel.idr)
Line 255: A PID is a process identifier that one process 
Line 256: can use to initiate communication with another.
Line 257: A Channel is a link between two processes, 
Line 258: allowing them to communicate.
Line 259: Starts a new concurrent process, 
Line 260: returning a Maybe PID. Returns 
Line 261: Nothing if it can’t create the process.
Line 262: Initiates a session for communicating 
Line 263: with a process with identifier pid
Line 264: Initiates a session by waiting 
Line 265: for another process to connect
Line 266: Waits 1 second for an incoming connection. 
Line 267: sender_chan is the name of the channel to 
Line 268: receive messages from the sender.
Line 269: If there’s no
Line 270: incoming
Line 271: connection
Line 272: after 1 second,
Line 273: loops
Line 274: Creates a new process 
Line 275: for executing adder
Line 276: spawn might fail if there aren’t 
Line 277: enough system resources, so 
Line 278: checks the result
Line 279: Creates a channel 
Line 280: for sending 
Line 281: messages to adder
Line 282: If connect returns 
Line 283: Nothing, the adder 
Line 284: process is no longer 
Line 285: running.
Line 286: 
Line 287: --- 페이지 435 ---
Line 288: 409
Line 289: Primitives for concurrent programming in Idris
Line 290: order, or that they’re sending and receiving messages of consistent types. Neverthe-
Line 291: less, for the moment we’ll use them to complete the implementations of main and
Line 292: adder. Later, in section 15.2, you’ll see how to make safe versions that ensure that pro-
Line 293: cesses send and receive messages with a consistent protocol.
Line 294: WHY SUPPORT AN UNSAFE CHANNEL TYPE?
Line 295: It might seem surprising that Idris,
Line 296: a language that’s designed to support type-driven development, supports
Line 297: such unsafe concurrency primitives rather than something more sophisti-
Line 298: cated. The reason is that there are many possible methods for implementing
Line 299: safe concurrent programs in a type-driven way, and by providing unsafe
Line 300: underlying primitives, Idris is not limited to only one of them. You’ll see one
Line 301: such method shortly.
Line 302: The following listing shows the type declarations for these primitive operations,
Line 303: defined in System.Concurrency.Channels.
Line 304: unsafeSend : Channel -> (val : a) -> IO Bool
Line 305: unsafeRecv : (expected : Type) -> Channel -> IO (Maybe expected)
Line 306: In the next listing, you can complete the definition of adder by receiving a request
Line 307: from the sender and then sending a reply. With unsafeRecv, you assert that the
Line 308: request is of type Message.
Line 309: data Message = Add Nat Nat
Line 310: adder : IO ()
Line 311: adder = do Just sender_chan <- listen 1
Line 312: | Nothing => adder
Line 313: Just msg <- unsafeRecv Message sender_chan
Line 314: | Nothing => adder
Line 315: case msg of
Line 316: Add x y => do ok <- unsafeSend sender_chan (x + y)
Line 317: adder
Line 318: Similarly, the following listing shows the complete definition of main, which sends a
Line 319: message using unsafeSend and receives a reply of type Nat with unsafeRecv.
Line 320: main : IO ()
Line 321: main = do Just adder_id <- spawn adder
Line 322: | Nothing => putStrLn "Spawn failed"
Line 323: Just chan <- connect adder_id
Line 324: | Nothing => putStrLn "Connection failed"
Line 325: ok <- unsafeSend chan (Add 2 3)
Line 326: Just answer <- unsafeRecv Nat chan
Line 327: Listing 15.3
Line 328: Primitive message passing 
Line 329: (defined in System.Concurrency.Channels)
Line 330: Listing 15.4
Line 331: Complete definition of adder (AdderChannel.idr)
Line 332: Listing 15.5
Line 333: Complete definition of main (AdderChannel.idr)
Line 334: Message is the type that 
Line 335: adder expects to receive.
Line 336: Waits for a message on 
Line 337: the channel you’ve just 
Line 338: created, of type Message
Line 339: Sends a reply on
Line 340: the channel, with
Line 341: the sum of the
Line 342: inputs of type Nat
Line 343: Sends a message on the 
Line 344: channel you’ve just 
Line 345: created, of type Message
Line 346: Waits for a reply
Line 347: on the channel,
Line 348: of type Nat
Line 349: 
Line 350: --- 페이지 436 ---
Line 351: 410
Line 352: CHAPTER 15
Line 353: Type-safe concurrent programming
Line 354: | Nothing => putStrLn "Send failed"
Line 355: printLn answer
Line 356: If you compile and execute main using :exec at the REPL, you’ll see that it receives the
Line 357: result 5 from adder:
Line 358: *AdderChannel> :exec main
Line 359: 5
Line 360: This only works because you’ve ensured that main and adder agree on a communica-
Line 361: tion pattern. When main sends a message on a channel, the adder process is expecting
Line 362: to receive a message on its corresponding channel, and vice versa. 
Line 363: 15.1.3 Problems with channels: type errors and blocking
Line 364: Channels provide a primitive method of setting up links between processes and send-
Line 365: ing messages across those links. The types of unsafeSend and unsafeRecv don’t, how-
Line 366: ever, provide any kind of guarantees about how processes coordinate with each other.
Line 367: As a result, it’s easy to make a mistake.
Line 368:  For example, adder sends a Nat in reply to main, but what if main is expecting to
Line 369: receive a String?
Line 370: main : IO ()
Line 371: main = do Just adder_id <- spawn adder
Line 372: | Nothing => putStrLn "Spawn failed"
Line 373: Just chan <- connect adder_id
Line 374: | Nothing => putStrLn "Connection failed"
Line 375: ok <- unsafeSend chan (Add 2 3)
Line 376: Just answer <- unsafeRecv String chan
Line 377: | Nothing => putStrLn "Send failed"
Line 378: printLn answer
Line 379: In this case, executing main will behave unpredictably, and will most likely crash,
Line 380: because at runtime there’s an inconsistency between the type of the message received
Line 381: and the expected type. Nothing in the types of unsafeSend and unsafeRecv explains
Line 382: how the sends and receives are coordinated between the two processes, so Idris is
Line 383: happy to accept main as valid even though the coordination is, in this case, incorrect.
Line 384:  A different problem occurs if the unsafeSend and unsafeReceive operations
Line 385: don’t correspond in each process. For example, main might send a second message on
Line 386: the same channel and expect a reply:
Line 387: main : IO ()
Line 388: main = do Just adder_id <- spawn adder
Line 389: | Nothing => putStrLn "Spawn failed"
Line 390: Just chan <- connect adder_id
Line 391: | Nothing => putStrLn "Connection failed"
Line 392: ok <- unsafeSend chan (Add 2 3)
Line 393: Just answer <- unsafeRecv Nat chan
Line 394: | Nothing => putStrLn "Send failed"
Line 395: printLn answer
Line 396: ok <- unsafeSend chan (Add 3 4)
Line 397: Prints the result received from adder
Line 398: main expects a 
Line 399: String, but adder 
Line 400: sends a Nat, so 
Line 401: behavior here is 
Line 402: undefined.
Line 403: main executes successfully 
Line 404: up to here.
Line 405: 
Line 406: --- 페이지 437 ---
Line 407: 411
Line 408: Defining a type for safe message passing
Line 409: Just answer <- unsafeRecv Nat chan
Line 410: | Nothing => putStrLn "Send failed"
Line 411: printLn answer
Line 412: Even though this type-checks successfully, when you attempt to execute it, it will print
Line 413: the first reply from adder but block while waiting for the second. After adder creates
Line 414: the channel using listen, it only replies to one message on that channel.
Line 415:  Although channels themselves are unsafe, you can use them as a primitive for
Line 416: defining type-safe communication. We’ll define a type for describing the coordination
Line 417: between communicating processes, and then write a run function that executes the
Line 418: description using the unsafe primitives. Even though, ultimately, you’ll need to use
Line 419: the primitives, you can encapsulate all the details in a single, descriptive type that you
Line 420: can then use for type-driven development of communicating systems. 
Line 421: 15.2
Line 422: Defining a type for safe message passing
Line 423: In the Idris runtime system, concurrent processes run independently of each other.
Line 424: There’s no shared memory, and the only way processes can communicate with each
Line 425: other is by sending messages to each other. Because there’s no shared memory, there
Line 426: are no race conditions caused by accessing shared state simultaneously, but there are
Line 427: several other problems to consider:
Line 428: How can you ensure that the type of the message that main sends is the same
Line 429: type that adder expects to receive?
Line 430: What happens if main sends a message to adder, but adder doesn’t reply?
Line 431: What happens if adder has stopped running when main sends a message?
Line 432: How can you prevent the situation where main and adder are both waiting for a
Line 433: message from each other?
Line 434: In this section, you’ll see how to solve these problems by defining a Process type,
Line 435: which allows you to describe well-typed communicating processes.
Line 436: Execution blocks here, because 
Line 437: adder only replies to the first 
Line 438: message on the channel.
Line 439: Types and concurrent programming
Line 440: Support for types in concurrent programming has generally been quite limited in main-
Line 441: stream programming languages, with some exceptions, such as typed channels in Go.
Line 442: One difficulty is that, as well as the types of messages that a channel can carry, you
Line 443: also need to think about the protocol for message passing. In other words, as well
Line 444: as what to send (the type), you also need to think about when to send it (the protocol).
Line 445: There has, nevertheless, been significant research into types for concurrent program-
Line 446: ming, most notably the study of session types that began with Kohei Honda’s 1993
Line 447: paper “Types for Dyadic Interaction.” The type we’ll implement in this section is an
Line 448: instance of a session type with a minimal protocol where a client sends one message
Line 449: and then receives one reply. If you’re interested in exploring further, a recent (2016)
Line 450: paper, “Certifying Data in Multiparty Session Types” by Bernardo Toninho and Nobuko
Line 451: Yoshida, describes a more sophisticated way of using types in concurrent programs.
Line 452: 
Line 453: --- 페이지 438 ---
Line 454: 412
Line 455: CHAPTER 15
Line 456: Type-safe concurrent programming
Line 457: We won’t get this implementation right on the first try, however. As is often the case in
Line 458: type-driven development, we’ll find that we need to refine the type to address the
Line 459: problems that become apparent after our first attempt. We’ll start by defining a type
Line 460: that’s specific to the adder service, and later refine it to support generic services that
Line 461: are guaranteed to respond to requests indefinitely.
Line 462: 15.2.1 Describing message-passing processes in a type
Line 463: Earlier, I described two problems with the primitive Channel type that make concur-
Line 464: rent programming, in this primitive form, unsafe:
Line 465: There’s no way to check that a response to a request has the correct type.
Line 466: There’s no way to check the correspondence between sending and receiving
Line 467: messages in communicating processes.
Line 468: We’ll solve both of these problems by defining a type for describing processes and
Line 469: then refining it as necessary to support the message-passing features we need.
Line 470:  To start, you can define a process type that supports IO actions, constructing pure
Line 471: values, and sequencing.
Line 472: data Process : Type -> Type where
Line 473: Action : IO a -> Process a
Line 474: Pure : a -> Process a
Line 475: (>>=) : Process a -> (a -> Process b) -> Process b
Line 476: run : Process t -> IO t
Line 477: run (Action act) = act
Line 478: run (Pure val) = pure val
Line 479: run (act >>= next) = do x <- run act
Line 480: run (next x)
Line 481: USING IO IN ACTION
Line 482: By using IO in Action, you can include arbitrary IO
Line 483: actions in processes, such as writing to the console or reading user input. This
Line 484: is a bit too general, because IO actions include, among other things, the
Line 485: unsafe communication primitives. You could restrict this by defining a more
Line 486: precise command type (see chapter 11 for an example), but we’ll stick with
Line 487: IO for this example.
Line 488: At the moment, Process is nothing more than a wrapper for sequences of IO actions.
Line 489: The next step is to extend it to support spawning new processes. You can define a data
Line 490: type for representing processes that can receive a Message, using PID from System
Line 491: .Concurrency.Channels:
Line 492: data MessagePID = MkMessage PID
Line 493: Next, you can add a constructor to Process that describes an action that spawns a new
Line 494: process and returns the MessagePID of that process, if it was successful:
Line 495: Spawn : Process () -> Process (Maybe MessagePID)
Line 496: Listing 15.6
Line 497: A type for describing processes (Process.idr)
Line 498: A process
Line 499: consisting
Line 500: of a single
Line 501: IO action
Line 502: A process with no action, 
Line 503: producing a pure value
Line 504: Sequences two 
Line 505: subprocesses, 
Line 506: and supports 
Line 507: do notation
Line 508: Executes a Process 
Line 509: description as a 
Line 510: sequence of IO actions
Line 511: 
Line 512: --- 페이지 439 ---
Line 513: 413
Line 514: Defining a type for safe message passing
Line 515: You also need to extend run to be able to execute the new Spawn command. This
Line 516: spawns a new process using the spawn primitive and then returns a MessagePID con-
Line 517: taining the new PID: 
Line 518: run (Spawn proc) = do Just pid <- spawn (run proc)
Line 519: | Nothing => pure Nothing
Line 520: pure (Just (MkMessage pid))
Line 521: ADDING NEW CONSTRUCTORS
Line 522: Remember that after you’ve added the Spawn
Line 523: constructor, you can add the missing cases to run in Atom by pressing Ctrl-
Line 524: Alt-A with the cursor over the name run.
Line 525: Next, you can add commands to allow processes to send messages to each other. In
Line 526: the previous examples, the main process sent requests of type Message and waited for
Line 527: corresponding replies of type Nat. You can encapsulate this behavior in a single
Line 528: Request command:
Line 529: Request : MessagePID -> Message -> Process (Maybe Nat)
Line 530: The reason for returning Maybe Nat, rather than Nat, is that you don’t have any guar-
Line 531: antee that the process to which MessagePID refers is still running. When you run a
Line 532: Request, you’ll need to connect to the process that services the request, send it a mes-
Line 533: sage, and then wait for the reply:
Line 534: run (Request (MkMessage process) msg)
Line 535: = do Just chan <- connect process
Line 536: | _ => pure Nothing
Line 537: ok <- unsafeSend chan msg
Line 538: if ok then do Just x <- unsafeRecv Nat chan
Line 539: | Nothing => pure Nothing
Line 540: pure (Just x)
Line 541: else pure Nothing
Line 542: ENCAPSULATING PRIMITIVES IN THE PROCESS TYPE
Line 543: You still need to use
Line 544: unsafeSend and unsafeRecv, but by encapsulating them in the Process
Line 545: data type, you know there’s only one place in your program where you use the
Line 546: unsafe primitives. You need to be careful to get this definition right, but once
Line 547: you do, you know that any message-passing program implemented in terms of
Line 548: the Process type will follow the message-passing protocol correctly.
Line 549: The adder process waited for an incoming message, calculated a result, and sent a
Line 550: response back to the requester. You can encapsulate this behavior in a single Respond
Line 551: command:
Line 552: Respond : ((msg : Message) -> Process Nat) -> Process (Maybe Message)
Line 553: This takes a function as an argument, which, when given a message received from a
Line 554: requester, calculates the Nat to send back. It returns a value of type Maybe Message,
Line 555: which is either Nothing, if it didn’t process an incoming message, or of the form Just
Line 556: Connects to the server process
Line 557: Connecting
Line 558: failed, so no
Line 559: result
Line 560: Connecting succeeded, so sends the request
Line 561: No reply received, 
Line 562: so no result
Line 563: Reply successfully
Line 564: received
Line 565: Sending the message 
Line 566: failed, so no result
Line 567: 
Line 568: --- 페이지 440 ---
Line 569: 414
Line 570: CHAPTER 15
Line 571: Type-safe concurrent programming
Line 572: msg, if it processed an incoming message (msg). This is useful if you need to do any
Line 573: further processing with the incoming message, even after sending a response.
Line 574:  When you run the Respond command, you’ll wait for one second for a message and
Line 575: then, if there is a message, calculate the response and send it back:
Line 576: run (Respond calc)
Line 577: = do Just sender <- listen 1
Line 578: | Nothing => pure Nothing
Line 579: Just msg <- unsafeRecv Message sender
Line 580: | Nothing => pure Nothing
Line 581: res <- run (calc msg)
Line 582: unsafeSend sender res
Line 583: pure (Just msg)
Line 584: ALTERNATIVE IMPLEMENTATIONS FOR RESPOND
Line 585: This implementation of the
Line 586: Respond case waits for 1 second if there’s no incoming message. An alterna-
Line 587: tive, and more flexible, implementation might allow the user to specify a
Line 588: timeout. For example, if there’s no incoming request, it might not make
Line 589: sense to continue waiting if a process has other work to do.
Line 590: Listing 15.7 shows how you can define adder and main using Process. We’ll call them
Line 591: procAdder and procMain to distinguish them from the earlier versions. In procAdder,
Line 592: you use Respond to explain how to respond to a Message, and in procMain you use
Line 593: Request to send a message to a spawned process.
Line 594: procAdder : Process ()
Line 595: procAdder = do Respond (\msg => case msg of
Line 596: Add x y => Pure (x + y))
Line 597: procAdder
Line 598: procMain : Process ()
Line 599: procMain = do Just adder_id <- Spawn procAdder
Line 600: | Nothing => Action (putStrLn "Spawn failed")
Line 601: Just answer <- Request adder_id (Add 2 3)
Line 602: | Nothing => Action (putStrLn "Request failed")
Line 603: Action (printLn answer)
Line 604: You can try this at the REPL, using run to translate procMain to a sequence of IO
Line 605: actions:
Line 606: *Process> :exec run procMain
Line 607: 5
Line 608: Unlike the previous version, procMain can’t expect to receive a String rather than a
Line 609: Nat, because the type of Request doesn’t allow it. You’ve also encapsulated the
Line 610: Listing 15.7
Line 611: Implementing a type-safe adder process (Process.idr)
Line 612: Waits for 1 second for an incoming connection
Line 613: No incoming connection, so does nothing
Line 614: No message
Line 615: received, so
Line 616: does nothing
Line 617: Calculates the response to the message
Line 618: Sends the response, of type Nat, 
Line 619: back to the requesting process
Line 620: Responds to a 
Line 621: message of the 
Line 622: form Add x y by 
Line 623: sending the 
Line 624: response x + y
Line 625: Continues
Line 626: waiting for
Line 627: responses
Line 628: Spawns a process that must send and receive 
Line 629: messages according to the Process protocol
Line 630: Sends a request. If successful,
Line 631: the response is given by answer.
Line 632: 
Line 633: --- 페이지 441 ---
Line 634: 415
Line 635: Defining a type for safe message passing
Line 636: communication protocol on a channel using Request and Respond, so you know that
Line 637: you won’t send or receive too many messages after creating a channel.
Line 638:  As a first attempt, this is an improvement over the primitive implementation with
Line 639: Channel, but there are a number of ways you can improve it. For example, procAdder
Line 640: is not total:
Line 641: *Process> :total procAdder
Line 642: Main.procAdder is possibly not total due to recursive path:
Line 643: Main.procAdder
Line 644: This is potentially a problem, because a process that isn’t total may not successfully
Line 645: respond to requests. As a first refinement, you can modify the Process type, and cor-
Line 646: respondingly the definition of run, so that indefinitely running processes like proc-
Line 647: Adder are total. 
Line 648: 15.2.2 Making processes total using Inf
Line 649: As you saw in chapter 11, you can mark parts of data as potentially infinite using Inf:
Line 650: Inf : Type -> Type
Line 651: You can then say a function is total if it produces a finite prefix of constructors of a well-
Line 652: typed infinite result in finite time. In practice, this means that any time you use a value
Line 653: with an Inf type, it needs to be an argument to a data constructor or a nested
Line 654: sequence of data constructors.
Line 655:  You’ve seen various ways to use Inf to define potentially infinite processes in chap-
Line 656: ters 11 and 12. Here, you can use it to explicitly mark the parts of a process that loop
Line 657: by adding the following constructor to Process:
Line 658: Loop : Inf (Process a) -> Process a
Line 659: For reference, the next listing shows the current definition of Process, including
Line 660: Loop, defined in a new file, ProcessLoop.idr.
Line 661: data Message = Add Nat Nat
Line 662: data MessagePID = MkMessage PID
Line 663: data Process : Type -> Type where
Line 664: Request : MessagePID -> Message -> Process (Maybe Nat)
Line 665: Respond : ((msg : Message) -> Process Nat) -> Process (Maybe Message)
Line 666: Spawn : Process () -> Process (Maybe MessagePID)
Line 667: Loop : Inf (Process a) -> Process a
Line 668: Action : IO a -> Process a
Line 669: Pure : a -> Process a
Line 670: (>>=) : Process a -> (a -> Process b) -> Process b
Line 671: Listing 15.8
Line 672: New Process type, extended with Loop (ProcessLoop.idr)
Line 673: The type of messages that a process can send
Line 674: PIDs for processes that can respond to messages
Line 675: Descriptions of processes that 
Line 676: can loop indefinitely
Line 677: Explicitly loops, 
Line 678: executing a potentially 
Line 679: infinite process
Line 680: 
Line 681: --- 페이지 442 ---
Line 682: 416
Line 683: CHAPTER 15
Line 684: Type-safe concurrent programming
Line 685: Using Loop, you can define procAdder as follows, explicitly noting that the recursive
Line 686: call to procAdder is a potentially infinite process:
Line 687: procAdder : Process ()
Line 688: procAdder = do Respond (\msg => case msg of
Line 689: Add x y => Pure (x + y))
Line 690: Loop procAdder
Line 691: This version of procAdder is total:
Line 692: *ProcessLoop> :total procAdder
Line 693: Main.procAdder is Total
Line 694: By using an explicit Loop constructor, you can mark the infinite parts of a Process so
Line 695: that you can at least be sure that any infinite recursion is intended. Moreover, as you’ll
Line 696: see in the next section, it will allow you to refine Process further so that you can con-
Line 697: trol exactly when a process is allowed to loop.
Line 698:  You’ll also need to extend run to support Loop. The simplest way is to execute the
Line 699: action directly:
Line 700: run (Loop act) = run act
Line 701: Unfortunately, this new definition of run isn’t total because the totality checker (cor-
Line 702: rectly!) doesn’t believe that act is a smaller sequence than Loop act:
Line 703: *ProcessLoop> :total run
Line 704: Main.run is possibly not total due to recursive path:
Line 705: Main.run, Main.run, Main.run
Line 706: As with the infinite processes in chapter 11, you can define a Fuel data type to give an
Line 707: explicit execution limit to run. Every time you Loop, you reduce the amount of Fuel
Line 708: available. The following listing shows how you can extend run so that it terminates
Line 709: when it runs out of Fuel, following the pattern you’ve already seen in chapter 11.
Line 710: data Fuel = Dry | More (Lazy Fuel)
Line 711: run : Fuel -> Process t -> IO (Maybe t)
Line 712: run Dry _ = pure Nothing
Line 713: run fuel (Request (MkMessage process) msg)
Line 714: = do Just chan <- connect process
Line 715: | _ => pure (Just Nothing)
Line 716: ok <- unsafeSend chan msg
Line 717: if ok then do Just x <- unsafeRecv Nat chan
Line 718: | Nothing => pure (Just Nothing)
Line 719: pure (Just (Just x))
Line 720: else pure (Just Nothing)
Line 721: run fuel (Respond calc)
Line 722: = do Just sender <- listen 1
Line 723: | Nothing => pure (Just Nothing)
Line 724: Just msg <- unsafeRecv Message sender
Line 725: | Nothing => pure (Just Nothing)
Line 726: Listing 15.9
Line 727: New run function, with an execution limit (ProcessLoop.idr)
Line 728: Returns Nothing when 
Line 729: the process is out of fuel
Line 730: Uses Just 
Line 731: when the 
Line 732: process still 
Line 733: has fuel
Line 734: 
Line 735: --- 페이지 443 ---
Line 736: 417
Line 737: Defining a type for safe message passing
Line 738: Just res <- run fuel (calc msg)
Line 739: | Nothing => pure Nothing
Line 740: unsafeSend sender res
Line 741: pure (Just (Just msg))
Line 742: run (More fuel) (Loop act) = run fuel act
Line 743: run fuel (Spawn proc) = do Just pid <- spawn (do run fuel proc
Line 744: pure ())
Line 745: | Nothing => pure Nothing
Line 746: pure (Just (Just (MkMessage pid)))
Line 747: run fuel (Action act) = do res <- act
Line 748: pure (Just res)
Line 749: run fuel (Pure val) = pure (Just val)
Line 750: run fuel (act >>= next) = do Just x <- run fuel act
Line 751: | Nothing => pure Nothing
Line 752: run fuel (next x)
Line 753: Remember that you can generate an infinite amount of Fuel and allow processes to
Line 754: run indefinitely by using a single partial function, forever:
Line 755: partial
Line 756: forever : Fuel
Line 757: forever = More forever
Line 758: Using a single forever function to say how long an indefinite process is allowed to
Line 759: run means that you minimize the number of nontotal functions you need. Because
Line 760: run is total, you know that it will continue executing process actions as long as there
Line 761: are actions to execute. For convenience, you can also define a function for initiating a
Line 762: process and discarding its result:
Line 763: partial
Line 764: runProc : Process () -> IO ()
Line 765: runProc proc = do run forever proc
Line 766: pure ()
Line 767: Then, you can try executing procMain as follows, which will display the answer 5 as
Line 768: before:
Line 769: *ProcessLoop> :exec runProc procMain
Line 770: 5
Line 771: Using Loop, you can write processes that loop forever and that are total by being
Line 772: explicit about when they loop. Unfortunately, though, there’s still no guarantee that a
Line 773: looping process will respond to any messages at all. For example, you could define
Line 774: procAdder as follows:
Line 775: procAdderBad1 : Process ()
Line 776: procAdderBad1 = do Action (putStrLn "I'm out of the office today")
Line 777: Loop procAdderBad1
Line 778: Or even like this:
Line 779: procAdderBad2 : Process ()
Line 780: procAdderBad2 = Loop procAdderBad2
Line 781: When you run 
Line 782: recursively, you 
Line 783: need to check 
Line 784: that the result 
Line 785: was valid before 
Line 786: continuing.
Line 787: The process consumes 
Line 788: fuel on every Loop.
Line 789: 
Line 790: --- 페이지 444 ---
Line 791: 418
Line 792: CHAPTER 15
Line 793: Type-safe concurrent programming
Line 794: Both of these programs type-check, and are both checked as total, but neither will
Line 795: respond to any messages because there’s no Respond command. In the case of proc-
Line 796: AdderBad2, it’s total because the recursive call to procAdderBad2 is an argument to the
Line 797: Loop constructor, so it will produce a finite prefix of constructors. Being total using
Line 798: Loop is, therefore, not enough to guarantee that a process will respond to a request.
Line 799: THE MEANING OF TOTALITY, IN PRACTICE
Line 800: Totality means that you’re guaranteed
Line 801: that a function behaves in exactly the way described by its type, so if the type
Line 802: isn’t precise enough, neither is the guarantee! With Process, the type isn’t
Line 803: precise enough to guarantee that a process contains a Respond command
Line 804: before any Loop.
Line 805: Furthermore, the Process type is specific to the problem of writing a concurrent ser-
Line 806: vice to add numbers. What if you want to write different services? You don’t want to have
Line 807: to write a different Process type for every kind of service you might want to Spawn.
Line 808:  To solve these problems, you’ll need to refine the Process type in two more ways:
Line 809: In section 15.2.3, you’ll refine it to ensure that a server process responds to
Line 810: requests on every iteration of a Loop.
Line 811: In section 15.2.4, you’ll see how to use first-class types to allow Process to
Line 812: respond to any kind of message.
Line 813: 15.2.3 Guaranteeing responses using a state machine and Inf
Line 814: In chapter 13, you saw how to guarantee that systems would execute necessary actions
Line 815: in the correct order by representing a state machine in a type. A server process like
Line 816: adder could be in one of several states, depending on whether or not it has received
Line 817: and processed a request:
Line 818: 
Line 819: NoRequest—It has not yet serviced any requests.
Line 820: 
Line 821: Sent—It has sent a response to a request.
Line 822: 
Line 823: Complete—It has completed an iteration of a loop and is ready to service the
Line 824: next request.
Line 825: Figure 15.3 illustrates how the Respond and Loop commands affect the state of a process.
Line 826: Sent
Line 827: NoRequest
Line 828: Respond
Line 829: Respond
Line 830: Loop
Line 831: Complete
Line 832: Figure 15.3
Line 833: A state transition diagram showing the states and operations in 
Line 834: a server process. A process begins in the NoRequest state and must end in 
Line 835: the Complete state, meaning that it has responded to at least one request.
Line 836: 
Line 837: --- 페이지 445 ---
Line 838: 419
Line 839: Defining a type for safe message passing
Line 840: If you have a process that begins in the NoRequest state and ends in the Complete
Line 841: state, you can be certain that it has replied to a request, because the only way to reach
Line 842: the Complete state is by calling Respond. You can also be certain that it’s continuing to
Line 843: receive requests, because the only way to reach the Complete state is by calling Loop.
Line 844: By expressing the state of a process in its type, you can then make stronger guarantees
Line 845: about how that process behaves.
Line 846:  You can refine the type of Process to represent the states before and after the pro-
Line 847: cess is executed:
Line 848: data ProcState = NoRequest | Sent | Complete
Line 849: data Process : Type ->
Line 850: (in_state : ProcState) ->
Line 851: (out_state : ProcState) ->
Line 852: Type
Line 853: The states in the type give the preconditions and postconditions of a process. For
Line 854: example:
Line 855: 
Line 856: Process () NoRequest Complete is the type of a process that responds to a
Line 857: request and then loops.
Line 858: 
Line 859: Process () NoRequest Sent is the type of a process that responds to one or
Line 860: more requests and then terminates.
Line 861: 
Line 862: Process () NoRequest NoRequest is the type of a process that responds to no
Line 863: requests and then terminates.
Line 864: Listing 15.10 shows the refined Process, where the type of each command explains
Line 865: how it affects the overall process state. In this definition, where there’s no precondi-
Line 866: tion on the state and no change in the state, the input and output states are both st.
Line 867: data Process : Type ->
Line 868: (in_state : ProcState) ->
Line 869: (out_state : ProcState) ->
Line 870: Type where
Line 871: Request : MessagePID -> Message -> Process Nat st st
Line 872: Respond : ((msg : Message) -> Process Nat NoRequest NoRequest) ->
Line 873: Process (Maybe Message) st Sent
Line 874: Spawn : Process () NoRequest Complete ->
Line 875: Process (Maybe MessagePID) st st
Line 876: Listing 15.10
Line 877: Annotating the Process type with its input and output states 
Line 878: (ProcessState.idr)
Line 879: The type of the result 
Line 880: of the process
Line 881: The state of the process before it’s executed
Line 882: The state of the process after it’s executed
Line 883: Request now returns a Nat 
Line 884: rather than a Maybe Nat.
Line 885: When processing, stays in the
Line 886: NoRequest state to ensure you don’t
Line 887: start processing a new response
Line 888: before completing this one
Line 889: You can respond to a request 
Line 890: at any time, and the resulting 
Line 891: state is Sent.
Line 892: You can only spawn a 
Line 893: process if it’s a looping 
Line 894: process (that is, it goes 
Line 895: from NoRequest to 
Line 896: Complete).
Line 897: 
Line 898: --- 페이지 446 ---
Line 899: 420
Line 900: CHAPTER 15
Line 901: Type-safe concurrent programming
Line 902: Loop : Inf (Process a NoRequest Complete) ->
Line 903: Process a Sent Complete
Line 904: Action : IO a -> Process a st st
Line 905: Pure : a -> Process a st st
Line 906: (>>=) : Process a st1 st2 -> (a -> Process b st2 st3) ->
Line 907: Process b st1 st3
Line 908: RETURN TYPE OF REQUEST
Line 909: Earlier, you sent requests of type Message and
Line 910: received responses of type Maybe Nat. You used Maybe because you had no
Line 911: guarantee that the service was still running, so the request could fail. Now
Line 912: you’ve set up the Process state so that services will always respond to
Line 913: requests. If you send a request, you’re guaranteed a response of type Nat in
Line 914: finite time.
Line 915: When you use this new definition, there’s no way for a function to invoke Loop unless
Line 916: the function can satisfy the precondition that it has sent a response to a request. More-
Line 917: over, Loop is also the only way for a process to reach the Complete state. As a result,
Line 918: you can only invoke Loop on a process that’s guaranteed to be looping, because the
Line 919: process must begin in the NoRequest state and end in the Complete state.
Line 920:  You can still define procAdder as before, because each command satisfies the pre-
Line 921: condition, and its type now states that it must respond to a request and then loop:
Line 922: procAdder : Process () NoRequest Complete
Line 923: procAdder = do Respond (\msg => case msg of
Line 924: Add x y => Pure (x + y))
Line 925: Loop procAdder
Line 926: The two incorrect versions defined earlier, however, no longer type-check, because
Line 927: the commands don’t satisfy the preconditions given by Process when you attempt to
Line 928: use them. For example, you can try the following definition:
Line 929: procAdderBad1 : Process () NoRequest Complete
Line 930: procAdderBad1 = do Action (putStrLn "I'm out of the office today")
Line 931: Loop procAdder
Line 932: Idris reports an error because there’s no Respond before the Loop:
Line 933: ProcessState.idr:63:21:
Line 934: When checking right hand side of procAdderBad1 with expected type
Line 935: Process () NoRequest Complete
Line 936: When checking an application of constructor Main.>>=:
Line 937: Type mismatch between
Line 938: Process a Sent Complete (Type of Loop _)
Line 939: and
Line 940: Process () NoRequest Complete (Expected type)
Line 941: Specifically:
Line 942: Type mismatch between
Line 943: You can only loop 
Line 944: with a process 
Line 945: that goes from 
Line 946: NoRequest to 
Line 947: Complete.
Line 948: You can only Loop after sending a message, and a 
Line 949: Loop puts the process into the Complete state.
Line 950: Sequences operations, going from 
Line 951: the input state of the first operation 
Line 952: to the output state of the second
Line 953: 
Line 954: --- 페이지 447 ---
Line 955: 421
Line 956: Defining a type for safe message passing
Line 957: Sent
Line 958: and
Line 959: NoRequest
Line 960: This error message means that when you call Loop, the process is supposed to be in
Line 961: the Sent state, but at this point it’s in the NoRequest state, not having sent any
Line 962: response yet. You’ll get a similar error message for the same reason with the following
Line 963: definition:
Line 964: procAdderBad2 : Process () NoRequest Complete
Line 965: procAdderBad2 = Loop procAdderBad2
Line 966: In order to execute programs using the refined Process, you’ll need to modify run
Line 967: and runProc. First, you need to modify their types:
Line 968: run : Fuel -> Process t in_state out_state -> IO (Maybe t)
Line 969: runProc : Process () in_state out_state -> IO ()
Line 970: The definitions mostly remain the same as the previous versions. The one change is in
Line 971: the definition of the Request case in run, now that you know a Request will always
Line 972: receive a reply in finite time:
Line 973: run fuel (Request (MkMessage process) msg)
Line 974: = do Just chan <- connect process
Line 975: | _ => pure Nothing
Line 976: ok <- unsafeSend chan msg
Line 977: if ok then do Just x <- unsafeRecv Nat chan
Line 978: | Nothing => pure Nothing
Line 979: pure (Just x)
Line 980: else pure Nothing
Line 981: RETURN VALUE OF RUN
Line 982: If run fails for any reason, it returns Nothing. Up to
Line 983: now, this could only happen if it ran out of Fuel. You’ve now set up Process
Line 984: so that senders and receivers are coordinated, so, at least in theory, communi-
Line 985: cation can’t fail. If communication does fail, there’s either an error in the
Line 986: implementation of run or a more serious runtime error, so you can also
Line 987: return Nothing in this case.
Line 988: You’ll also need to modify the type of procMain, to be consistent with the refined
Line 989: Process type. This type explicitly states that procMain isn’t intended to respond to
Line 990: any incoming requests because it ends in the NoRequest state:
Line 991: procMain : Process () NoRequest NoRequest
Line 992: It’s convenient to define type synonyms for clients, like procMain, and for services, like
Line 993: procAdder. They both use Process, but they differ in how they affect the state of the
Line 994: process:
Line 995: Service : Type -> Type
Line 996: Service a = Process a NoRequest Complete
Line 997: Client : Type -> Type
Line 998: Client a = Process a NoRequest NoRequest
Line 999: If communication 
Line 1000: fails, abandons 
Line 1001: execution
Line 1002: 
Line 1003: --- 페이지 448 ---
Line 1004: 422
Line 1005: CHAPTER 15
Line 1006: Type-safe concurrent programming
Line 1007: The following listing shows the refined definitions of procAdder and procMain using
Line 1008: these type synonyms for client and server processes.
Line 1009: procAdder : Service ()
Line 1010: procAdder = do Respond (\msg => case msg of
Line 1011: Add x y => Pure (x + y))
Line 1012: Loop procAdder
Line 1013: procMain : Client ()
Line 1014: procMain = do Just adder_id <- Spawn procAdder
Line 1015: | Nothing => Action (putStrLn "Spawn failed")
Line 1016: answer <- Request adder_id (Add 2 3)
Line 1017: Action (printLn answer)
Line 1018: If you try this at the REPL, you’ll see that it displays 5 as before:
Line 1019: *ProcessState> :exec runProc procMain
Line 1020: 5
Line 1021: You now have a definition of Process with the following guarantees, ensured by the
Line 1022: preconditions and postconditions in the definition of Process:
Line 1023: All requests of type Message are sent responses of type Nat.
Line 1024: Every process started with Spawn is guaranteed to loop indefinitely and respond
Line 1025: to requests on every iteration.
Line 1026: Therefore, every time a process sends a Request to a service started with Spawn,
Line 1027: it will receive a response in finite time as long as the service is defined by a total
Line 1028: function.
Line 1029: This means you can write type-safe concurrent programs that can’t deadlock, because
Line 1030: every request is guaranteed to receive a response eventually. But at this stage, it only
Line 1031: allows you to write one kind of service—one that receives a Message and sends back a
Line 1032: Nat. It would be far more useful if you could define generic message-passing processes
Line 1033: with user-defined interactions between the sender and receiver. As you’ll see, you can
Line 1034: achieve this with a final small refinement to Process. 
Line 1035: 15.2.4 Generic message-passing processes
Line 1036: When a process receives a request of the form Add x y, it sends back a response of type
Line 1037: Nat. You can express this relationship between the request and the response types in a
Line 1038: type-level function:
Line 1039: AdderType : Message -> Type
Line 1040: AdderType (Add x y) = Nat
Line 1041: This function describes the interface that Process supports: if it receives a message of
Line 1042: the form Add x y, it will send a response of type Nat. You could define other interfaces
Line 1043: Listing 15.11
Line 1044: Refined definitions of procAdder and procMain (ProcessState.idr)
Line 1045: A Client is a Process that begins
Line 1046: and ends in the NoRequest state.
Line 1047: A Service is a Process that begins in the 
Line 1048: NoRequest state and ends in the Complete state.
Line 1049: 
Line 1050: --- 페이지 449 ---
Line 1051: 423
Line 1052: Defining a type for safe message passing
Line 1053: this way; for example, the following listing gives a description of an interface to a pro-
Line 1054: cess that responds to requests to perform operations on lists.
Line 1055: data ListAction : Type where
Line 1056: Length : List elem -> ListAction
Line 1057: Append : List elem -> List elem -> ListAction
Line 1058: ListType : ListAction -> Type
Line 1059: ListType (Length xs) = Nat
Line 1060: ListType (Append {elem} xs ys) = List elem
Line 1061: In general, an interface to a process is a function like AdderType or ListType that cal-
Line 1062: culates a response type from a request. Instead of defining a specific type that pro-
Line 1063: cesses can send and receive, you can include the interface as part of a process’s type by
Line 1064: adding an additional argument for the interface, as figure 15.4 shows.
Line 1065: REQUEST TYPE OF PROCESS
Line 1066: The iface argument to Process includes a type
Line 1067: variable, reqType. This is an implicit argument, and it defines the type of mes-
Line 1068: sages the process can receive. Idris will infer reqType from the iface argu-
Line 1069: ment. For example, in procAdder, iface is AdderType, so reqType must
Line 1070: be Message.
Line 1071: We’ll come to the refined definition of Process shortly. Once it’s defined, the proc-
Line 1072: Adder service will respond to an interface defined by AdderType:
Line 1073: procAdder : Process AdderType () NoRequest Complete
Line 1074: Some processes, like procMain, don’t respond to any requests. You can make this
Line 1075: explicit in the type by defining their interfaces as follows:
Line 1076: NoRecv : Void -> Type
Line 1077: NoRecv = const Void
Line 1078: Listing 15.12
Line 1079: Describing an interface for List operations
Line 1080: The type of messages received 
Line 1081: by a process that manipulates 
Line 1082: lists concurrently
Line 1083: Getting the length of a list results in a Nat.
Line 1084: Appending two lists with element 
Line 1085: type elem results in a List elem.
Line 1086: data Process : (iface : reqType -> Type) -> Type
Line 1087:    -> (in_state : ProcState) -> (out_state : ProcState) -> Type
Line 1088: Interface process
Line 1089: responds to
Line 1090: Input state
Line 1091: of process
Line 1092: Output state
Line 1093: of process
Line 1094: Return type
Line 1095: of process
Line 1096: Figure 15.4
Line 1097: A refined Process type, including the interface that the 
Line 1098: process responds to as part of the type
Line 1099: 
Line 1100: --- 페이지 450 ---
Line 1101: 424
Line 1102: CHAPTER 15
Line 1103: Type-safe concurrent programming
Line 1104: Remember from chapter 8 that Void is the empty type, with no values. Because you
Line 1105: can never construct a value of type Void, a process that provides a NoRecv interface
Line 1106: can never receive a request. You can use it in the following type for procMain:
Line 1107: procMain : Process NoRecv () NoRequest NoRequest
Line 1108: You’ll also need to redefine the type synonyms Service and Client to include the
Line 1109: interface description. A Service has an interface, but a Client receives no requests:
Line 1110: Service : (iface : reqType -> Type) -> Type -> Type
Line 1111: Service iface a = Process iface a NoRequest Complete
Line 1112: Client : Type -> Type
Line 1113: Client a = Process NoRecv a NoRequest NoRequest
Line 1114: When you create a new process, you get a PID for the new process as a MessagePID. You
Line 1115: should only send messages to a process when the messages match the interface of that
Line 1116: process, so you can refine MessagePID to include the interface it supports in its type:
Line 1117: data MessagePID : (iface : reqType -> Type) -> Type where
Line 1118: MkMessage : PID -> MessagePID iface
Line 1119: Now, if you have a PID of type MessagePID AdderType, you know that you can send it
Line 1120: messages of type Message, because that’s the input type of AdderType.
Line 1121:  Putting all of this together, you can refine Process to describe its own interface
Line 1122: and to be explicit about when it’s safe to send a request of a particular type to another
Line 1123: Process. The next listing shows the refined types for Request, Respond, and Spawn.
Line 1124: data ProcState = NoRequest | Sent | Complete
Line 1125: data Process : (iface : reqType -> Type) ->
Line 1126: Type ->
Line 1127: (in_state : ProcState) ->
Line 1128: (out_state : ProcState) ->
Line 1129: Type where
Line 1130: Request : MessagePID service_iface ->
Line 1131: (msg : service_reqType) ->
Line 1132: Process iface (service_iface msg) st st
Line 1133: Respond : ((msg : reqType) ->
Line 1134: Process iface (iface msg) NoRequest NoRequest) ->
Line 1135: Process iface (Maybe reqType) st Sent
Line 1136: Spawn : Process service_iface () NoRequest Complete ->
Line 1137: Process iface (Maybe (MessagePID service_iface)) st st
Line 1138: {-- continued in Listing 15.14 --}
Line 1139: Listing 15.13
Line 1140: Refining Process to include its interface in the type, part 1 
Line 1141: (ProcessIFace.idr)
Line 1142: The PID for a
Line 1143: process with an
Line 1144: interface described
Line 1145: by service_iface
Line 1146: The req has type 
Line 1147: service_reqType, and 
Line 1148: service_iface has type 
Line 1149: service_reqType -> Type.
Line 1150: The reply from the service will be 
Line 1151: calculated by applying service_iface to the 
Line 1152: request to ensure that the reply type 
Line 1153: corresponds with the request.
Line 1154: If you spawn a server with an interface
Line 1155: described by service_iface, the PID has
Line 1156: type MessagePID service_iface.
Line 1157: If you receive a req message, the required
Line 1158: response type is calculated by iface req.
Line 1159: 
Line 1160: --- 페이지 451 ---
Line 1161: 425
Line 1162: Defining a type for safe message passing
Line 1163: The following listing completes the refined definition of Process, adding Loop,
Line 1164: Action, Pure, and (>>=). In each case, all you need to do is add an iface argument to
Line 1165: Process.
Line 1166: data Process : (iface : reqType -> Type) ->
Line 1167: Type ->
Line 1168: (in_state : ProcState) ->
Line 1169: (out_state : ProcState) ->
Line 1170: Type where
Line 1171: {-- continued from Listing 15.13 --}
Line 1172: Loop : Inf (Process iface a NoRequest Complete) ->
Line 1173: Process iface a Sent Complete
Line 1174: Action : IO a -> Process iface a st st
Line 1175: Pure : a -> Process iface a st st
Line 1176: (>>=) : Process iface a st1 st2 -> (a -> Process iface b st2 st3) ->
Line 1177: Process iface b st1 st3
Line 1178: Finally, you need to update run and runProc for the refined Process definition. List-
Line 1179: ing 15.15 shows the changes you need to make to run. You need only modify the cases
Line 1180: for Request and Respond to be explicit about the types of messages a process expects
Line 1181: to receive.
Line 1182: run : Fuel -> Process iface t in_state out_state -> IO (Maybe t)
Line 1183: run fuel (Request {service_iface} (MkMessage process) msg)
Line 1184: = do Just chan <- connect process
Line 1185: | _ => pure Nothing
Line 1186: ok <- unsafeSend chan msg
Line 1187: if ok then do Just x <- unsafeRecv (service_iface msg) chan
Line 1188: | Nothing => pure Nothing
Line 1189: pure (Just x)
Line 1190: else pure Nothing
Line 1191: run fuel (Respond {reqType} f)
Line 1192: = do Just sender <- listen 1
Line 1193: | Nothing => pure (Just Nothing)
Line 1194: Just msg <- unsafeRecv reqType sender
Line 1195: | Nothing => pure (Just Nothing)
Line 1196: Just res <- run fuel (f msg)
Line 1197: | Nothing => pure Nothing
Line 1198: unsafeSend sender res
Line 1199: pure (Just (Just msg))
Line 1200: For runProc, you need only change its type to add the iface argument to Process:
Line 1201: partial
Line 1202: runProc : Process iface () in_state out_state -> IO ()
Line 1203: Listing 15.14
Line 1204: Refining Process to include its interface in the type, part 2 
Line 1205: (ProcessIFace.idr)
Line 1206: Listing 15.15
Line 1207: Updating run for the refined Process (ProcessIFace.idr)
Line 1208: In Loop and (>>=), the
Line 1209: type explicitly states that the
Line 1210: interface does not change.
Line 1211: Brings service_iface into scope so that you 
Line 1212: can calculate the expected response type
Line 1213: Calculates the expected response
Line 1214: type from the message you sent
Line 1215: Brings reqType into scope 
Line 1216: so that you can say it’s the 
Line 1217: expected type of received 
Line 1218: messages
Line 1219: You expect to
Line 1220: receive a
Line 1221: message that
Line 1222: satisfies the
Line 1223: interface.
Line 1224: 
Line 1225: --- 페이지 452 ---
Line 1226: 426
Line 1227: CHAPTER 15
Line 1228: Type-safe concurrent programming
Line 1229: runProc proc = do run forever proc
Line 1230: pure ()
Line 1231: When designing data types, especially types that express strong guarantees like
Line 1232: Process, it’s often a good idea to begin by trying to solve a specific problem before
Line 1233: moving on to a more general solution. Here, we started with a type for Process that
Line 1234: only supported specific message and response types (Message and Nat). Only after
Line 1235: that worked did we use type-level functions to make a generic Process type. 
Line 1236: 15.2.5 Defining a module for Process
Line 1237: Once you’ve defined a generic type, it’s useful to define a new module to make that
Line 1238: type and its supporting functions available to other users. We’ll define a new module,
Line 1239: ProcessLib.idr, that defines Process and supporting definitions and exports them
Line 1240: as necessary.
Line 1241:  The next listing shows the overall structure of the module, omitting the definitions
Line 1242: but adding export modifiers to each declaration.
Line 1243: module ProcessLib
Line 1244: import System.Concurrency.Channels
Line 1245: %default total
Line 1246: export
Line 1247: data MessagePID : (iface : reqType -> Type) -> Type where
Line 1248: public export
Line 1249: data ProcState = NoRequest | Sent | Complete
Line 1250: public export
Line 1251: data Process : (iface : reqType -> Type) ->
Line 1252: Type ->
Line 1253: (in_state : ProcState) ->
Line 1254: (out_state : ProcState) ->
Line 1255: Type where
Line 1256: public export
Line 1257: data Fuel
Line 1258: The complete definitions are the same as those you’ve already seen for MessagePID,
Line 1259: ProcState, Process, and Fuel. Remember from chapter 10 that for data declarations,
Line 1260: an export modifier can be one of the following:
Line 1261: 
Line 1262: export—The type constructor is exported but not the data constructors.
Line 1263: 
Line 1264: public export—The type and data constructors are exported.
Line 1265: The following listing shows how you can export the supporting functions.
Line 1266: Listing 15.16
Line 1267: Defining Process in a module, omitting definitions (ProcessLib.idr)
Line 1268: Unless stated otherwise, all 
Line 1269: definitions in the file must be total.
Line 1270: Exports the MessagePID type but 
Line 1271: not the constructors
Line 1272: Exports the remaining types 
Line 1273: and their constructors
Line 1274: 
Line 1275: --- 페이지 453 ---
Line 1276: 427
Line 1277: Defining a type for safe message passing
Line 1278:  
Line 1279: export partial
Line 1280: forever : Fuel
Line 1281: export
Line 1282: run : Fuel -> Process iface t in_state out_state -> IO (Maybe t)
Line 1283: public export
Line 1284: NoRecv : Void -> Type
Line 1285: public export
Line 1286: Service : (iface : reqType -> Type) -> Type -> Type
Line 1287: public export
Line 1288: Client : Type -> Type
Line 1289: export partial
Line 1290: runProc : Process iface () in_state out_state -> IO ()
Line 1291: For functions, an export modifier can be one of the following:
Line 1292: 
Line 1293: export—The type is exported but not the definition.
Line 1294: 
Line 1295: public export—The type and definition are exported.
Line 1296: Unless there’s a specific reason to export a definition as well as a type, it’s better to use
Line 1297: export, hiding the details of the definition. Here, you use public export for Client
Line 1298: and Service because these are type synonyms, and other modules will need to know
Line 1299: that these are defined in terms of Process.
Line 1300:  Now that you’ve defined Process and a separate ProcessLib module that exports
Line 1301: the relevant definitions, we can try more examples. To conclude this section, we’ll
Line 1302: look at two examples of implementing concurrent programs using this generic
Line 1303: Process type. First, we’ll implement a process using ListType, which was defined ear-
Line 1304: lier in listing 15.12, and then we’ll look at a larger example using concurrency to run
Line 1305: a process in the background to count words in a file. 
Line 1306: 15.2.6 Example 1: List processing
Line 1307: To demonstrate how you can use Process to define services other than procAdder,
Line 1308: we’ll start with a service that responds to requests to carry out functions on List. The
Line 1309: interface of the service is defined by a ListType function. It provides two operations:
Line 1310: Length and Append.
Line 1311: data ListAction : Type where
Line 1312: Length : List elem -> ListAction
Line 1313: Append : List elem -> List elem -> ListAction
Line 1314: ListType : ListAction -> Type
Line 1315: ListType (Length xs) = Nat
Line 1316: ListType (Append {elem} xs ys) = List elem
Line 1317: Listing 15.17
Line 1318: Supporting function types for Process, omitting definitions 
Line 1319: (ProcessLib.idr)
Line 1320: Exports the 
Line 1321: types of run 
Line 1322: and runProc 
Line 1323: but not their 
Line 1324: definitions
Line 1325: Exports the 
Line 1326: types and 
Line 1327: definitions of 
Line 1328: the remaining 
Line 1329: functions
Line 1330: 
Line 1331: --- 페이지 454 ---
Line 1332: 428
Line 1333: CHAPTER 15
Line 1334: Type-safe concurrent programming
Line 1335: We’ll define a procList service that responds to requests on this interface. It has the
Line 1336: following type:
Line 1337: procList : Service ListType ()
Line 1338: You can define procList incrementally, taking the following steps:
Line 1339: 1
Line 1340: Define, type—As with procAdder, you can implement procList as a loop that
Line 1341: responds to a request on each iteration: 
Line 1342: procList : Service ListType ()
Line 1343: procList = do Respond (\msg => ?procList_rhs)
Line 1344: Loop procList
Line 1345: Looking at the ?procList_rhs type here, you can see that the type you need to
Line 1346: produce is calculated from the msg you receive: 
Line 1347: msg : ListAction
Line 1348: --------------------------------------
Line 1349: procList_rhs : Process ListType (ListType msg) NoRequest NoRequest
Line 1350:  2
Line 1351: Define—Because the type you need to produce depends on the value of msg, you
Line 1352: can continue the definition with a case statement, inspecting msg: 
Line 1353: procList : Service ListType ()
Line 1354: procList = do Respond (\msg => case msg of
Line 1355: case_val => ?procList_rhs)
Line 1356: Loop procList
Line 1357: Case splitting on case_val produces this: 
Line 1358: procList : Service ListType ()
Line 1359: procList = do Respond (\msg => case msg of
Line 1360: Length xs => ?procList_rhs_1
Line 1361: Append xs ys => ?procList_rhs_2)
Line 1362: Loop procList
Line 1363:  3
Line 1364: Type, refine—For ?procList_rhs_1, if you check the type, you’ll see that you
Line 1365: need to produce a Nat for the result of Length xs: 
Line 1366: msg : ListAction
Line 1367: a : Type
Line 1368: xs : List elem
Line 1369: --------------------------------------
Line 1370: procList_rhs_1 : Process ListType Nat NoRequest NoRequest
Line 1371: You can refine ?procList_rhs_1 as follows: 
Line 1372: procList : Service ListType ()
Line 1373: procList = do Respond (\msg => case msg of
Line 1374: Length xs => Pure (length xs)
Line 1375: Append xs ys => ?procList_rhs_2)
Line 1376: Loop procList
Line 1377: 4
Line 1378: Refine—To refine ?procList_rhs_2, you need to provide a List elem, and you
Line 1379: can complete the definition as follows: 
Line 1380: 
Line 1381: --- 페이지 455 ---
Line 1382: 429
Line 1383: Defining a type for safe message passing
Line 1384: procList : Service ListType ()
Line 1385: procList = do Respond (\msg => case msg of
Line 1386: Length xs => Pure (length xs)
Line 1387: Append xs ys => Pure (xs ++ ys))
Line 1388: Loop procList
Line 1389: Having completed procList, you can try it by spawning it in a process and sending it
Line 1390: requests. The following listing defines a process that sends two requests to an instance
Line 1391: of procList and displays their results.
Line 1392: procMain : Client ()
Line 1393: procMain = do Just list <- Spawn procList
Line 1394: | Nothing => Action (putStrLn "Spawn failed")
Line 1395: len <- Request list (Length [1,2,3])
Line 1396: Action (printLn len)
Line 1397: app <- Request list (Append [1,2,3] [4,5,6])
Line 1398: Action (printLn app)
Line 1399: You can try this at the REPL as follows:
Line 1400: *ListProc> :exec runProc procMain
Line 1401: 3
Line 1402: [1, 2, 3, 4, 5, 6]
Line 1403: Like procAdder, procList loops, waiting for incoming requests, and processes them
Line 1404: as necessary, but it doesn’t do any other computation while waiting for a request. Con-
Line 1405: current processes become far more useful if, rather than spending their time idling
Line 1406: and waiting for requests from other processes, they also do some computation. In the
Line 1407: next example, you’ll see how to do this. 
Line 1408: 15.2.7 Example 2: A word-counting process
Line 1409: When you define services, you can define separate requests for initiating an action
Line 1410: and getting the result of that action. For example, if you’re defining a word-count ser-
Line 1411: vice, you could allow a client to take the following steps:
Line 1412: 1
Line 1413: Send a request to a word-count service to load a file and count the number of
Line 1414: words in the file.
Line 1415:  2
Line 1416: While the word-count service is processing, the client continues its own work,
Line 1417: such as reading input and producing output.
Line 1418: 3
Line 1419: Send a second request to the word-count service to ask how many words were in
Line 1420: the file.
Line 1421: In this example, you’ll define the word-count service around the WCData record and
Line 1422: doCount function defined in listing 15.19. This function takes the contents of a file, in
Line 1423: a String, and produces a structure containing the numbers of words and lines in that
Line 1424: content.
Line 1425: Listing 15.18
Line 1426: A main program that uses the procList service (ListProc.idr)
Line 1427: Sets up the procList process
Line 1428: Invokes the
Line 1429: Length
Line 1430: command,
Line 1431: returning a Nat
Line 1432: Invokes the Append 
Line 1433: command, returning 
Line 1434: a List Integer
Line 1435: 
Line 1436: --- 페이지 456 ---
Line 1437: 430
Line 1438: CHAPTER 15
Line 1439: Type-safe concurrent programming
Line 1440:  
Line 1441: import ProcessLib
Line 1442: record WCData where
Line 1443: constructor MkWCData
Line 1444: wordCount : Nat
Line 1445: lineCount : Nat
Line 1446: doCount : (content : String) -> WCData
Line 1447: doCount content = let lcount = length (lines content)
Line 1448: wcount = length (words content) in
Line 1449: MkWCData lcount wcount
Line 1450: You can see an example of this in action at the REPL:
Line 1451: *WordCount> doCount "test test\ntest"
Line 1452: MkWCData 2 3 : WCData
Line 1453: The goal is to implement a process that provides word counting as a service. Rather than
Line 1454: loading and counting the words in a single request, you can provide two commands:
Line 1455: 
Line 1456: CountFile—Given a filename, loads that file and counts the number of words
Line 1457: in it
Line 1458: 
Line 1459: GetData—Given a filename, returns the WCData structure for that file, as long as
Line 1460: the file has already been processed with CountFile
Line 1461: Rather than returning the WCData structure itself, CountFile will return immediately
Line 1462: and continue loading the file in a separate process. That is, one request begins the
Line 1463: task and another retrieves the result. This will allow the requester to continue its own
Line 1464: work while the word-count service is processing the file. The following listing shows
Line 1465: the interface and a skeleton definition for the word-count service.
Line 1466: data WC = CountFile String
Line 1467: | GetData String
Line 1468: WCType : WC -> Type
Line 1469: WCType (CountFile x) = ()
Line 1470: WCType (GetData x) = Maybe WCData
Line 1471: wcService : (loaded : List (String, WCData)) ->
Line 1472: Service WCType ()
Line 1473: wcService loaded = ?wcService_rhs
Line 1474: We’ll come to the definition of wcService in a moment. The next listing shows how
Line 1475: you can invoke it and continue to execute interactive actions in the foreground while
Line 1476: wcService is processing a file in the background.
Line 1477: Listing 15.19
Line 1478: A small function to count the number of words and lines in a String
Line 1479: (WordCount.idr)
Line 1480: Listing 15.20
Line 1481: Interface for the word-count service (WordCount.idr)
Line 1482: Imports this so that you can create a 
Line 1483: concurrent word-counting process
Line 1484: See chapter 12 for more on records. This record contains 
Line 1485: fields for the number of words and lines in a file.
Line 1486: Returns a structure 
Line 1487: containing the number 
Line 1488: of words and lines in 
Line 1489: the content
Line 1490: Returns () because it 
Line 1491: merely initiates the 
Line 1492: processing of a file
Line 1493: Returns Maybe WCData 
Line 1494: because it will fail if the 
Line 1495: given file has not yet 
Line 1496: been processed
Line 1497: wcService loops indefinitely 
Line 1498: and takes a list of loaded files 
Line 1499: as an argument.
Line 1500: 
Line 1501: --- 페이지 457 ---
Line 1502: 431
Line 1503: Defining a type for safe message passing
Line 1504:  
Line 1505: procMain : Client ()
Line 1506: procMain = do Just wc <- Spawn (wcService [])
Line 1507: | Nothing => Action (putStrLn "Spawn failed")
Line 1508: Action (putStrLn "Counting test.txt")
Line 1509: Request wc (CountFile "test.txt")
Line 1510: Action (putStrLn "Processing")
Line 1511: Just wcdata <- Request wc (GetData "test.txt")
Line 1512: | Nothing => Action (putStrLn "File error")
Line 1513: Action (putStrLn ("Words: " ++ show (wordCount wcdata)))
Line 1514: Action (putStrLn ("Lines: " ++ show (lineCount wcdata)))
Line 1515: Listing 15.22 presents an incomplete implementation of wcService that shows how it
Line 1516: responds to the commands CountFile and GetData. Two parts of the definition are
Line 1517: missing:
Line 1518: Loading and processing the requested file
Line 1519: Looping, with the new file information added to the input, loaded
Line 1520: wcService : (loaded : List (String, WCData)) -> Service WCType ()
Line 1521: wcService loaded
Line 1522: = do Respond (\msg => case msg of
Line 1523: CountFile fname => Pure ()
Line 1524: GetData fname =>
Line 1525: Pure (lookup fname loaded))
Line 1526: ?wcService_rhs
Line 1527: To process the input, you can look at the return value from Respond. Remember that
Line 1528: Respond has the following type:
Line 1529: Respond : ((msg : reqType) ->
Line 1530: Process iface (iface msg) NoRequest NoRequest) ->
Line 1531: Process iface (Maybe reqType) st Sent
Line 1532: The return value from Respond, of type Maybe reqType, tells you which message, if any,
Line 1533: was received. If wcService received a CountFile command, it could load and process
Line 1534: the necessary file before processing its next input.
Line 1535:  The next listing shows a further refinement of wcService, still including a hole for
Line 1536: the function that processes the file.
Line 1537: Listing 15.21
Line 1538: Using the word-count service (WordCount.idr)
Line 1539: Listing 15.22
Line 1540: Responding to commands in wcService (WordCount.idr)
Line 1541: Starts a new 
Line 1542: process for the 
Line 1543: word-count 
Line 1544: service
Line 1545: Initiates the word count for a file
Line 1546: Does some work while the 
Line 1547: word-count process is running
Line 1548: Gets the result of the
Line 1549: word count of the file
Line 1550: Returns () immediately so that the 
Line 1551: requester can continue processing
Line 1552: Looks up the word-count data in
Line 1553: the existing list of processed files
Line 1554: 
Line 1555: --- 페이지 458 ---
Line 1556: 432
Line 1557: CHAPTER 15
Line 1558: Type-safe concurrent programming
Line 1559:  
Line 1560: wcService : List (String, WCData) -> Service WCType ()
Line 1561: wcService loaded
Line 1562: = do msg <- Respond (\msg => case msg of
Line 1563: CountFile fname => Pure ()
Line 1564: GetData fname =>
Line 1565: Pure (lookup fname loaded))
Line 1566: newLoaded <- case msg of
Line 1567: Just (CountFile fname) =>
Line 1568: ?countFile loaded fname
Line 1569: _ => Pure loaded
Line 1570: Loop (wcService newLoaded)
Line 1571: To see what you need to do to complete wcService, you can check the type of
Line 1572: ?countFile:
Line 1573: loaded : List (String, WCData)
Line 1574: fname : String
Line 1575: msg2 : Maybe WC
Line 1576: st2 : ProcState
Line 1577: a : Type
Line 1578: --------------------------------------
Line 1579: countFile : List (String, WCData) ->
Line 1580: String -> Process WCType (List (String, WCData)) Sent Sent
Line 1581: countFile needs to be a function that takes the current list of processed file data and
Line 1582: a filename, and then returns an updated list of processed file data. The next listing
Line 1583: shows how to define it using doCount, defined earlier, to process the file’s contents.
Line 1584: countFile : List (String, WCData) -> String ->
Line 1585: Process WCType (List (String, WCData)) Sent Sent
Line 1586: countFile files fname =
Line 1587: do Right content <- Action (readFile fname)
Line 1588: | Left err => Pure files
Line 1589: let count = doCount content
Line 1590: Action (putStrLn ("Counting complete for " ++ fname))
Line 1591: Pure ((fname, doCount content) :: files)
Line 1592: UPDATING THE HOLE FOR COUNTFILE
Line 1593: Remember that you need to define
Line 1594: countFile before you use it in wcService. Once you’ve defined count-
Line 1595: File, don’t forget to replace the ?countFile hole with a call to countFile.
Line 1596: Listing 15.23
Line 1597: Incomplete implementation of wcService (WordCount.idr)
Line 1598: Listing 15.24
Line 1599: Loading a file and counting words (WordCount.idr)
Line 1600: Respond returns the msg 
Line 1601: received, which you can 
Line 1602: now process further.
Line 1603: Calculates the new list of loaded 
Line 1604: file data, given the msg received
Line 1605: If asked to process a file,
Line 1606: process it here. We’ll
Line 1607: define countFile shortly.
Line 1608: Continues with the
Line 1609: new list of loaded files
Line 1610: Reading the file 
Line 1611: failed, so doesn’t 
Line 1612: update the files list
Line 1613: Prints a message to the console when 
Line 1614: processing of the file is complete
Line 1615: Adds the data for the 
Line 1616: newly processed file 
Line 1617: to the files list
Line 1618: 
Line 1619: --- 페이지 459 ---
Line 1620: 433
Line 1621: Summary
Line 1622: Now that you’ve defined countFile, you can try executing procMain, which starts
Line 1623: wcService, asks to count the words in a file, test.txt, and then displays the result.
Line 1624: You’ll need to create a test.txt file with content like the following:
Line 1625: test test
Line 1626: test
Line 1627: test test test
Line 1628: test
Line 1629: You can execute procMain at the REPL as follows:
Line 1630: *WordCount> :exec runProc procMain
Line 1631: Counting test.txt
Line 1632: Processing
Line 1633: Counting complete for test.txt
Line 1634: Words: 4
Line 1635: Lines: 7
Line 1636: With Process, you’ve defined a type that allows you to describe concurrently execut-
Line 1637: ing processes and to explain how processes can send each other messages safely, fol-
Line 1638: lowing a protocol:
Line 1639: A service must respond to every message it receives, on a specific interface, and
Line 1640: continue responding in a loop.
Line 1641: A client can then send a message to a process, with the correct interface, and be
Line 1642: sure of receiving a reply of the correct type.
Line 1643: This doesn’t solve all possible concurrent programming problems, but you’ve defined
Line 1644: a type that encapsulates the behavior of one kind of concurrent program. If a func-
Line 1645: tion describing a Process type-checks and is total, you can be confident that it won’t
Line 1646: deadlock and that all requests will receive replies. If you later refine Process further,
Line 1647: such as by allowing more-sophisticated descriptions of interactions between processes,
Line 1648: you’ll be able to implement more-sophisticated models of concurrent programs. 
Line 1649: 15.3
Line 1650: Summary
Line 1651: Concurrent programming involves multiple processes executing simultane-
Line 1652: ously.
Line 1653: Processes in Idris cooperate with each other by sending messages.
Line 1654: The System.Concurrency.Channels library provides primitive, but unsafe,
Line 1655: operations for message passing.
Line 1656: Primitive operations are unsafe because they provide no guarantees about
Line 1657: when processes send and receive messages, or about the correspondence
Line 1658: between the types of sent and received messages.
Line 1659: You can define a type for describing safe message-passing processes, imple-
Line 1660: mented using Channel as a primitive.
Line 1661: Using Inf, you can guarantee that looping processes continue to perform IO
Line 1662: actions.
Line 1663: Displayed by procMain before 
Line 1664: requesting to process test.txt
Line 1665: Displayed by procMain while wcService is processing
Line 1666: Displayed by wcService when it 
Line 1667: has finished processing
Line 1668: 
Line 1669: --- 페이지 460 ---
Line 1670: 434
Line 1671: CHAPTER 15
Line 1672: Type-safe concurrent programming
Line 1673: By defining a state machine in the type, you can be sure that a process will
Line 1674: respond to messages on every iteration of a loop.
Line 1675: The type of a process can be generic and describe the types of messages to
Line 1676: which a process will respond.