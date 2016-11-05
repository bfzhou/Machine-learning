# Readme of Homework 2

### Team member: Baofeng Zhou(bzhou), Feiyu Zhu(fzhu)

## File Structure
Source.cpp   ---- ANN implementation program

votes.csv ---- Converted data set file for "Congressional Voting Data"

monks.csv ---- Converted data set file for "Monks-1"

wine.csv  ---- Converted data set file for "Wine Data"

Readme.md  ---- readme file


## To run the program
Our program is developed in C++ using Visual Studio. To re-create this experiment you need to have a g++ compatible build environment.

To run this program, issue the following code in command line under the containing folder:
```
g++ Source.cpp -o neural
./neural
```

## Parameters of the program
There is no input parameter needed for the program. 
All the parameters are defined at the beginning of the program.
```
 NumI	-----  number of input nodes
 NumH	-----  number of hidden nodes
 NumO	-----  number of output nodes
 PATH   -----  dataset file to run the algorithm on
```
The default dataset is monks.csv. 
The default number of hidden node is 4.
The parameters need to be changed if other datasets need to be tested.

The outputs in the command window will be the content of the dataset, results of traning set, and results of test set.
