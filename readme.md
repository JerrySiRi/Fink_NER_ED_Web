# BERT-BiLSTM-CRF模型

### 运行环境

```
python == 3.7.4
pytorch == 1.7.1 
pytorch-crf == 0.7.2  
pytorch-transformers == 1.2.0
Flask == 2.2.2         
autocorrect == 2.6.1
nltk == 3.7

```

### 运行方式
请不要移动相关文件位置，在各文档读取过程中均使用相对路径
若使用vscode出现路径报错问题，请修改部分相对路径或使用pycharm运行

**final_result_test_output.xlsx为存放了测试集的识别+消歧的最终结果**

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
1. 请运行Flask_Web中的api.py，复制终端给出的网址到浏览器中即可呈现页面

tip：可能会出现卡顿，必要时可以连接vpn