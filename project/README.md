# 50.007 Machine Learning Project 2021

## Dependencies needed to install
It is highly suggested to create a pip environment to run all the files as it is not very desirable to 'contaminate' your system. Run it on python 3.7 + and all should go fine. If all else to run the script in part 4, copy and paste this into your command line interface. <br/>

<b> MacOS/Linux</b>
```
pip3 install numpy
```
<b>Windows</b>
```
pip install numpy
```

## Running our scripts
Change directory to the folder. You can do it via any operating system specified below. <br/>
Note: If you are running Windows, use ```python``` instead of ```python3``` for each command specified below.

1. First alternative:<br/>
 Via<b> powershell or git bash (Windows) or Mac/Linux:</b>

```git clone https://github.com/caramelmelmel/machine_learning_2021.git```
```cd machine_learning_2021```
``` git checkout project```
```cd project```

2. Second Alternative (submitted files): <br/>
```cd ${PWD}/project```

### Running the Script
The same commands can be run for each of the parts, just changing the [x] from 1 to 4. The x has to be in INTEGER form.

a. Training and Predicting (Test): <br/>
```python3 part[x].py```<br/>
You should receive the outputs in the `ES/dev.p[x].out` file and also that in the `RU/dev.p[x].out`. <br/>
You may also supply a custom training, test, and output file path by adding arguments: <br/>
```python3 part[x].py [train_path] [test_path] [output_path]```<br/>
Note: For part 4, you can supply the alpha value like below
```python3 part4.py 0.1```
Please save the `test.p4.out` before running the script via the above command.

b. Evaluating result

For the Russian dataset:<br/>
<b>For MacOS/Linux/ Powershell:</b><br/>
```python3 EvalScript/EvalScript.py RU/dev.out RU/dev.p[x].out```

<b>For Command Prompt(Windows):</b><br/>
```python EvalScript/EvalScript.py RU/dev.out RU/dev.p[x].out```

For the Spanish dataset:<br/>
<b>For MacOS/Linux/ Powershell:</b><br/>
```python3 EvalScript/EvalScript.py ES/dev.out ES/dev.p[x].out```

<b>For Command Prompt(Windows):</b><br/>
```python EvalScript/EvalScript.py ES/dev.out ES/dev.p[x].out```

c. Playing around with what we do for part 4.
This script runs the range of values of our factor from 0.0 to 1.0.

For <b>MacOS/Linux:</b>

```python3 part4_script.py```

For <b>Windows:</b>

```python part4_script.py```

## Team Members
- Leon Tjandra
- Jerome Heng Hao Xiang
- Leong Yun Qin Melody


