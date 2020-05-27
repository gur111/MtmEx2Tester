#!/bin/bash
set -e

echo "Please choose which python version you want to run ,i.e '3.6'"
read PYTHON_VER
echo "how many tests would you like to run ?"
read NUM_OF_TESTS
if (( NUM_OF_TESTS > 1000 )); then
        echo "Just don't"
        exit 1
fi
echo "Generating ${NUM_OF_TESTS} Tests..."
for (( i=1; i<=${NUM_OF_TESTS};i++ ))
do
	echo -en "\r$i"
	python${PYTHON_VER} generate_test_file.py>>winner.txt
        cat winner.txt>>out1.txt
	cp test1.txt tests/in/test${i}.txt
	cp out1.txt tests/out/out${i}.txt
	rm test1.txt out1.txt
        rm winner.txt
	sed -i "s/ //" tests/out/out${i}.txt
done
echo ""
echo "Done!"
rm -r tests/myouts 2>/dev/null
mkdir tests/myouts
echo "Running Tests..."
for (( i=1; i<=${NUM_OF_TESTS};i++ ))
do
	echo -en "\r$i"
	cp tests/in/test${i}.txt input.txt
	python${PYTHON_VER} hw2.py>tests/myouts/out${i}.txt
done
echo ""
echo "Done!"
echo "looking for outputs diff..."
rm log.txt 2>/dev/null
touch log.txt
echo "scroll down to see if there are diffrences:">>log.txt
for (( i=1; i<=${NUM_OF_TESTS};i++ ))
do
	 echo -en "\r$i"
	 var=$(diff -q tests/out/out${i}.txt tests/myouts/out${i}.txt)
	 echo ${var}>>log.txt
done
echo ""
if grep -q "differ" log.txt;then
	echo "you didnt pass all tests,check log.txt file for more information"
else
	rm log.txt
	echo "Congratz you passed all ${NUM_OF_TESTS} tests!"
fi


