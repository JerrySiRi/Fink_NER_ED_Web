import json
import sys,os
import pandas as pd
import pickle
import subprocess
from Flink.main.test_disambiguation import load_from_result_test, disambiguation_stringmatch_test


def test():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(r"D:\BERT_Chinese\Finish_API\Flink")#【【【需要添加相对搜索路径！！！现在找不到Flink】】】

    #指定了测试数据的路径 path_test 和预训练模型的路径 PATH_MODEL
    path_test = '../test.json'  # 部署的时候，manage.py的路径为当前路径
    with open(path_test, 'r', encoding='utf-8') as f1:
        test_data = json.load(f1)
    seq = ''
    for i in test_data['text']:
        if i == '。' or i == '；':
            seq += i + ' ' + 'O' + '\n' + '\n'
        else:
            seq += i + ' ' + 'O' + '\n'
    with open('../processed_data/test.txt', 'w', encoding='utf-8') as f2:
        f2.write(seq)
    print("=====================1111")
    # '--train_file', '../test_text.txt', '--eval_file', '../test_text.txt','--test_file', '../test_text.txt',
    subprocess.run(['python', '../main/ner.py',
                    '--model_name_or_path', "../bert-base-chinese", '--output_dir', '../output'])
    print("=====================2222")
    case_words_org, case_words_sto = load_from_result_test('../output/token_labels_.txt')
    print("=====================3333")
    disambiguation_stringmatch_test('./raw_database.csv', case_words_org, case_words_sto)
    print("=====================4444")
    with open('./result-all_train_test_lower.pkl', 'rb') as f:
        results = pickle.load(f)
    data_base = pd.read_csv('./raw_database.csv', encoding='utf-8', error_bad_lines=False, header=0)
    db = pd.DataFrame(data_base)
    case_sto_list = results['sto']
    case_org_list = results['org']
    case_pre_list = []
    for i in range(len(case_sto_list)):
        sto_list = case_sto_list[i]
        org_list = case_org_list[i]
        pre_list = []
        for sto in sto_list:
            if max(sto[2], sto[4]) < 0.8:
                continue
            if (sto[4] - sto[2]) / sto[2] > 0:
                m = db[db['companyId'] == int(sto[3])]['companyName'].iloc[0]
                pre_list.append((m, 'company', int(sto[3])))
            else:
                m = db[db['stockId'] == int(sto[1])]['stockName'].iloc[0]
                pre_list.append((m, 'stock', int(sto[1])))
        for org in org_list:
            if max(org[2], org[4]) < 0.8:
                continue
            if (org[2] - org[4]) / org[4] > 0:
                m = db[db['stockId'] == int(org[1])]['stockName'].iloc[0]
                pre_list.append((m, 'stock', int(org[1])))
            else:
                m = db[db['companyId'] == int(org[3])]['companyName'].iloc[0]
                pre_list.append((m, 'company', int(org[3])))
        case_pre_list.append(pre_list)
    return list(set(case_pre_list[0]))

    
    
    
    
    
    


