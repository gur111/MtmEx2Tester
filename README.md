# How to use
This tester aims to cover as many edge cases as possible whilst giving convinient testing results.

## So what's it testing
 - [x] All test files located in the `in` folder (assuming there's a matching output file in the `out` folder)
 - [x] Testing `partA`
 - [x] Testing `partB`
 - [ ] Automagically create SWIG compiled files from .i .h and .o files
 - [ ] Automagically generates random tests
 - [ ] Automagically fetches tests with edge cases from the internet


## Prerequisites
1. Python3.6+ (`sudo apt install python3 python3-pip` on Ubuntu)
2. `termcolor` library (you can install it by typing `pip install termcolor`)
3. Have a few test files

## Folder structure
You must have the following folder structure to be able to run the tester

project:
 * ex2_tester.py
 * hw2.py
 * Olympics.py
 * Olympics.so
 * tests:
   * in:
     * test1.txt
     * test2.txt
     * ...
   * out:
     * out1.txt
     * out2.txt
     * ...

## How to run
On your computer you will likely be able to run it with
```python
python3 ex2_tester.py
```
On the CSL3 server, the default Python3 version is 3.4 so you will need to
```python
python3.6 ex2_tester.py
```
