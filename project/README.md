# 50.007 Machine Learning Project 2021

## Dependencies needed to install
It is highly suggested to create a pip environment to run all the files as it is not very desirable to 'contaminate' your system. Run it on python 3.7 + and all should go fine.

## Running our scripts
Change directory to the folder. You can do it via any operating system specified below. <br/>
Note: If you are running Windows, use ```python``` instead of ```python3``` for each command specified below.

1. First alternative:<br/>
 Via powershell or git bash (Windows) or Mac/Linux:
```git clone https://github.com/caramelmelmel/machine_learning_2021.git```
```cd machine_learning_2021```
``` git checkout project```
```cd project```

2. Second Alternative (submitted files): <br/>
```cd ${PWD}/project```

### Running the Script
The same commands can be run for each of the parts, just changing the [x] from 1 to 4.
a. Training and Predicting (Test): <br/>
```python3 part[x].py```<br/>
You should receive the outputs in the `ES/dev.p[x].out` file and also that in the `RU/dev.p[x].out`. <br/>
You may also supply a custom training, test, and output file path by adding arguments: <br/>
```python3 part[x].py [train_path] [test_path] [output_path]```

b. Evaluating result

For the Russian dataset:<br/>
For MacOS/Linux/ Powershell:<br/>
```python3 EvalScript/EvalScript.py RU/dev.out RU/dev.p[x].out```

For Command Prompt(Windows):<br/>
```python EvalScript/EvalScript.py RU/dev.out RU/dev.p[x].out```

For the Spanish dataset:<br/>
For MacOS/Linux/ Powershell:<br/>
```python3 EvalScript/EvalScript.py ES/dev.out ES/dev.p[x].out```

For Command Prompt (Windows): <br/>
```python EvalScript/EvalScript.py ES/dev.out ES/dev.p[x].out```



## Team Members
- Leon Tjandra
- Jerome Heng Hao Xiang
- Leong Yun Qin Melody


