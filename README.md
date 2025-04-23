## About
This is a fully functional compiler that I coded, based on a provided template provided in the Cosc-261 course that converts a basic program into JVM instructions to produce an output.

I have added comments on the classes/functions that were written by me

## Authors
Samuel Beattie

## To Run
A provided test case has been provided in the test.txt file, this will read from the test_input file, which can be changed to provide different inputs that are identified using the read `var` tag
In the directory of the compiler and test file run:
1. `python3 compiler.py < program > Program.j`
2. `java -Xmx100m -jar jasmin.jar Program.j`
3. `java -Xmx100m Program < test_input > test_output`
