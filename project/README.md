# 50.007 Machine Learning Project 2021

## Dependencies needed to install
It is highly suggested to create a pipenvironment to run all the files as it is not very desirable to 'contaminate' your system. Run it on python 3.8 + and all should go fine.

## Running our scripts
Change directory to the folder. You can do it via any operating system specified below:

1. First alternative:<br/>
 Via powershell or git bash (Windows) or Mac/Linux:
```git clone https://github.com/caramelmelmel/machine_learning_2021.git```
```cd machine_learning_2021```
``` git checkout project```
```cd project```

2. Second Alternative (submitted files): <br/>
```cd ${PWD}/project```

### Part 1
a. Training and Predicting (Test):
```python3 part1.py```
You should receive the outputs in the `ES/dev.p1.out` file and also that in the `RU/dev.p1.out`.

b. Evaluating result

For the Russian dataset:
```python3 EvalScript/EvalScript.py RU/dev.out RU/dev.p1.out```

For the Spanish dataset:
```python3 EvalScript/EvalScript.py ES/dev.out ES/dev.p1.out```

### Part 2
Training and Predicting (Test):
```python3 part2.py```
You should receive the outputs in the `ES/dev.p2.out` file and also that in the `RU/dev.p2.out`.

b. Evaluating result

For the Russian dataset:
```python3 EvalScript/EvalScript.py RU/dev.out RU/dev.p2.out```

For the Spanish dataset:
```python3 EvalScript/EvalScript.py ES/dev.out ES/dev.p2.out```



## Team Members
- Leon Tjandra
- Jerome Heng Hao Xiang
- Leong Yun Qin Melody


