# 南京大学“AI+”大学生创新技能挑战赛
# 实体识别模型：BERT(wwm)-BiLSTM-CRF 
# 实体消歧模型：Jaro_distance-Embedding match
Last Update code：[![github](https://img.shields.io/badge/time-2023--10-18cf)](https://github.com/time-2023--10-18cf)

### 1. 运行环境

```
python == 3.7.4
pytorch == 1.7.1 
pytorch-crf == 0.7.2  
pytorch-transformers == 1.2.0
Flask == 2.2.2         
autocorrect == 2.6.1
nltk == 3.7

```

### 2. 初始大模型及fine-tunned模型下载
#### initial model：
**下载后请放在bert-base-chinese文件夹中，改名为pytorch_model**

链接：https://pan.baidu.com/s/1WRvzm8UitfvnArDU-DNGQQ?pwd=4fn0 
提取码：4fn0
####  fine-tunned model：
**下载后请放在ouput文件夹中，改名为pytorch_model。如若想重新训练，请在命令行中运行下面提及的命令，或import subprocess在IDE中运行**

链接：https://pan.baidu.com/s/1iRLgOb6V9Qmx6tMURZRExw?pwd=18ez 
提取码：18ez

### 3. 运行方式
**请在最外层创建一个名为Flink的文件夹，把所有文件包含在内**
请不要移动相关文件位置，在各文档读取过程中均使用相对路径
若使用vscode出现路径报错问题，请修改部分相对路径或使用pycharm运行


**final_result_test_output.xlsx为存放了测试集的识别+消歧的最终结果**
**以下为重新训练模型、对测试集进行抽取+消歧的步骤**
1. 请先运行dataprocess.py，获取训练集预处理过BIO标注的文件，并划分70%训练集和30%验证集。dev.txt和train.txt存放在processed_data中

2. 请运行process_test.py，获取测试集处理过的BIO标注的文件。test.txt存放在processed_data中

3. 请在命令行当前项目目录下、配置完成的环境中键入以下命令，对预训练模型进行fine tunning

```c++
 python ner.py --model_name_or_path ../bert-base-chinese --do_train True --do_eval True --do_test True --max_seq_length 256 --train_file ../processed_data/train.txt --eval_file ../processed_data/dev.txt --test_file ../processed_data/test.txt --train_batch_size 8 --eval_batch_size 8 --num_train_epochs 10 --do_lower_case --logging_steps 200 --need_birnn True --rnn_dim 256 --clean True --output_dir ../output
```
最终得到的模型在output/pytorch_model.bin，本文件中token_labels_.txt为测试集的初步预测结果

4. 最终运行test_disambiguation.py获得数据库消歧、模型集成后的测试集结果，将存放在最外侧的initial_raw_test.xlsx文件之中
   （final_result_test_output.xlsx为已处理好的测试集结果）

    
### 网页展示
**以下为使用fine-tunning后模型，对单个金融资讯从Web端调用模型进行预测并展示**

**1.** 请运行Flask_Web中的api.py，复制终端给出的网址到浏览器中即可呈现页面

tip：可能会出现卡顿，必要时可以连接vpn


**2.** 网站部分截图如下，具体演示视频课件readme_image中
![](https://github.com/JerrySiRi/Fink_NER_ED_Web/blob/main/readme_image/1.png)
![](https://github.com/JerrySiRi/Fink_NER_ED_Web/blob/main/readme_image/2.png)

![](https://github.com/JerrySiRi/Fink_NER_ED_Web/blob/main/readme_image/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91.mp4)

