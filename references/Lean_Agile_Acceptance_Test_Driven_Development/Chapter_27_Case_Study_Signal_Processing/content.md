Line 1: 
Line 2: --- 페이지 254 ---
Line 3: Chapter 27 
Line 4: Case Study: Signal Processing 
Line 5: Lisa Simpson: Would you guys turn that down!
Line 6: Homer Simpson: Sweetie, if we didn’t turn it down
Line 7: for the cops, what chance do you have?
Line 8: The Simpsons “Little Big Mom” (2000) 
Line 9: Acceptance tests for a real-time signal processing system are presented in this 
Line 10: chapter.
Line 11: It’s Too Loud 
Line 12: I have produced software with Richard Cann of Grozier Technical Systems for 
Line 13: a number of years. Grozier produces sound level measurement systems. Numer-
Line 14: ous concert sites, particularly outdoor ones, use these systems to monitor sound 
Line 15: levels for regulatory reasons and to act as good neighbors. 
Line 16: The systems are composed of embedded systems that run multiple programs. 
Line 17: Richard produces some of the programs, particularly the display and control 
Line 18: components. I produce the real-time signal analysis portion [Wiki08]. 
Line 19: Sound Levels 
Line 20: The programs input the sound through the microphone input. Each second, 
Line 21: 22,500 samples are recorded. The signal analysis programs perform calculations 
Line 22: on each of these sets of samples. The output is a measure of loudness, (techni-
Line 23: cally the equivalent continuous sound level [Leq]). An overview of the process 
Line 24: is shown in Figure 27.1.
Line 25: 231
Line 26: 
Line 27: --- 페이지 255 ---
Line 28: Chapter 27 Case Study: Signal Processing
Line 29: 232
Line 30: Analog–
Line 31: Digital
Line 32: Conversion
Line 33: (Hardware)
Line 34: Audio
Line 35: Samples
Line 36: Process
Line 37: Samples
Line 38: Leq
Line 39: Figure 27.1 Sound Level Process 
Line 40: The sound is input through a microphone. The gain (how much the signal is 
Line 41: ampliﬁed) varies based on both the microphone and the volume setting on the 
Line 42: input. To correctly compute the Leq, you must adjust the gain so that a standard 
Line 43: sound source (a calibration source) produces a speciﬁc Leq result. 
Line 44: It is difﬁcult to replicate the entire system (microphone, calibration source, 
Line 45: and so forth) for testing. However, you can capture the sounds by using regular 
Line 46: recording methods and then replay them as input (a test double) for the tests. 
Line 47: Suppose the sounds produced by the calibration source are captured in a cali-
Line 48: bration ﬁle and sounds of known Leq are captured in separate ﬁles. These ﬁles 
Line 49: contain a second’s worth of data (22,500 samples). Then the test of the overall 
Line 50: system can be as follows. 
Line 51: Compute Leq 
Line 52: Given that the volume is adjusted so that calibration ﬁle (containing a 
Line 53: 1KHz signal) yields the standard Leq: 
Line 54: Calibration
Line 55: File 
Line 56: Leq (db) 
Line 57: calibration.wav 
Line 58: 94
Line 59: The test ﬁles should produce values of the expected Leq. 
Line 60: Leq Tests 
Line 61: Input File 
Line 62: Leq (db)? 
Line 63: test1.wav 
Line 64: 88
Line 65: test2.wav 
Line 66: 95
Line 67: To ensure that these Leqs are correct, the same test is repeated with calibrated 
Line 68: specialized hardware. The results of the hardware test become the oracle—the
Line 69: agreed-upon expected result. This is similar to using the outputs of an existing 
Line 70: system to be the expected results for a new system. 
Line 71: 
Line 72: --- 페이지 256 ---
Line 73: Summary 
Line 74: 233
Line 75: Developer Tests 
Line 76: The details of the process are shown in Figure 27.2. It shows that there are 
Line 77: two intermediate results in the computation: the windowed samples and the 
Line 78: A-weighted samples. 
Line 79: Windowed
Line 80: Samples
Line 81: Apply
Line 82: A-Weight
Line 83: A-
Line 84: Weighted
Line 85: Samples
Line 86: Compute
Line 87: Leq
Line 88: Leq
Line 89: Analog–
Line 90: Digital
Line 91: Conversion
Line 92: (Hardware)
Line 93: Audio
Line 94: Samples
Line 95: Apply
Line 96: Window
Line 97: Figure 27.2 Details of Sound-Level Process 
Line 98: Richard is particularly interested in the ﬁnal results. Is the Leq computed cor-
Line 99: rectly for a particular ﬁle? As a developer, it helps if I can apply tests to interme-
Line 100: diate results. These intermediate tests are usually termed unit tests because they 
Line 101: apply to lower-level modules. However, because Richard is highly experienced 
Line 102: in signal processing, he creates input and output ﬁles that can be used in accept-
Line 103: ance tests for the intermediate processing works. For example, for the Compute 
Line 104: Leq part, he creates an A-Weighted sample ﬁle. 
Line 105: Compute Leq 
Line 106: A-Weighted Sample File 
Line 107: Leq?
Line 108: Aweight1.data 
Line 109: 77
Line 110: Aweight2.data 
Line 111: 44
Line 112: The input and output ﬁles contain digital samples for 1 second. Equivalent 
Line 113: ﬁles are available for each of the other steps in the process. 
Line 114: Summary
Line 115: • Acceptance tests do not have to involve just simple values. They can be 
Line 116: entire sets of values (often represented in ﬁles). 
Line 117: • A subject matter expert can often create lower-level tests that can be used 
Line 118: as developer tests. 
Line 119: 
Line 120: --- 페이지 257 ---
Line 121: This page intentionally left blank 