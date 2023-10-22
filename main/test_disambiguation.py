import Levenshtein as L
import pickle
import pandas as pd

def load_from_result_test(path): 
    case_word_list = []
    case_label_list = []
    word_list = []
    label_list = []
    with open(path, 'r', encoding='utf-8') as f1:
        for line in f1:
            line.strip('\n')
            line = line[:-1]
            line_split = line.split(' ')
            if line_split[0] == '=':
                case_word_list.append(word_list)
                case_label_list.append(label_list)
                word_list = []
                label_list = []
                continue
            if line_split[0] == '\n' or line_split[0] == ' ' or line_split[-1] == ' ' or line_split[-1] == '\n' or line_split[-1] == '' or line_split[-1] == '':
                continue
            word_list.append(line_split[0])
            label_list.append(line_split[-1])
            assert (line_split[-1] != '')
        case_word_list.append(word_list)
        case_label_list.append(label_list)


    case_words_org = [[] for i in range(len(case_label_list))]
    case_words_sto = [[] for i in range(len(case_label_list))]

    for idx in range(len(case_label_list)):
        label_list = case_label_list[idx]
        word_list = case_word_list[idx]
        begin_pos = -1  
        for i in range(len(label_list)):
            if label_list[i] == 'O' and begin_pos == -1:
                continue
            if label_list[i] == 'O' and begin_pos != -1:
                reg = ''.join(word_list[begin_pos:i])
                sto_count = 0
                org_count = 0
                for j in range(begin_pos, i):
                    ty = label_list[j][2:]
                    if ty == 'STO':
                        sto_count += 1
                    else:
                        org_count += 1
                if sto_count < org_count:
                    case_words_org[idx].append(reg)
                else:
                    case_words_sto[idx].append(reg)
                begin_pos = -1
                continue
            if label_list[i][0] == 'B':
                begin_pos = i
                continue
            if label_list[i][0] == 'I':
                continue
    return case_words_org, case_words_sto

def disambiguation_stringmatch_test(data_base_path, case_words_org, case_words_sto):
    data_base1 = pd.read_csv(data_base_path, encoding='utf-8', error_bad_lines=False, header=0)
    db1 = pd.DataFrame(data_base1)
    total_case = len(case_words_org)
    assert (len(case_words_org) == len(case_words_sto))
    case_sto_list = [[] for i in range(total_case)]
    case_org_list = [[] for i in range(total_case)]
    for i in range(total_case):
        print('-------------current case: ', i, 'total case: ', total_case)
        words = dict()
        words['STO'] = set(case_words_sto[i])
        words['ORG'] = set(case_words_org[i])
        count = 0
        total_round = len(words['STO']) + len(words['ORG'])
        print(words['STO'])
        print(words['ORG'])
        print(len(words['STO']))
        print(len(words['ORG']))
        words['STO'] = set(['哔哩哔哩有限公司' if x == 'b站' else x for x in case_words_sto[i]])
        words['ORG'] = set(['哔哩哔哩有限公司' if x == 'b站' else x for x in case_words_org[i]])
        print(words['STO'])
        print(words['ORG'])
        print(len(words['STO']))
        print(len(words['ORG']))
        for sto in words['STO']:
            count += 1
            if count % 5 == 0:
                print('------current round:', count, 'total round:', total_round, '------------')
            target_sto_id = -1
            target_org_id = -1
            max_sto_score = 0
            max_org_score = 0
            for row in range(len(db1)):
                temp_org_score = L.jaro(sto.lower(), db1.iloc[row]['companyName'].lower())
                if temp_org_score > max_org_score:
                    max_org_score = temp_org_score
                    target_org_id = db1.iloc[row]['companyId']
                if pd.isna(db1.iloc[row]['stockName']):
                    continue
                temp_sto_score = L.jaro(sto.lower(), db1.iloc[row]['stockName'].lower())
                if temp_sto_score > max_sto_score:
                    max_sto_score = temp_sto_score
                    target_sto_id = db1.iloc[row]['stockId']
            case_sto_list[i].append((sto, target_sto_id, max_sto_score, target_org_id, max_org_score))
        for org in words['ORG']:
            count += 1
            if count % 5 == 0:
                print('------current round:', count, 'total round:', total_round, '------------')
            target_sto_id = -1
            target_org_id = -1
            max_sto_score = 0
            max_org_score = 0
            for row in range(len(db1)):
                temp_org_score = L.jaro(org.lower(), db1.iloc[row]['companyName'].lower())
                if temp_org_score > max_org_score:
                    max_org_score = temp_org_score
                    target_org_id = db1.iloc[row]['companyId']
                if pd.isna(db1.iloc[row]['stockName']):
                    continue
                temp_sto_score = L.jaro(org.lower(), db1.iloc[row]['stockName'].lower())
                if temp_sto_score > max_sto_score:
                    max_sto_score = temp_sto_score
                    target_sto_id = db1.iloc[row]['stockId']
            case_org_list[i].append((org, target_sto_id, max_sto_score, target_org_id, max_org_score))
    d = dict()
    d['sto'] = case_sto_list
    d['org'] = case_org_list
    with open('./result-all_train_test_lower.pkl', 'wb') as f1:
        pickle.dump(d, f1)

if __name__ == '__main__':
    case_words_org, case_words_sto = load_from_result_test('../output/token_labels_.txt')
    disambiguation_stringmatch_test('../input/raw_database.csv', case_words_org, case_words_sto)
    with open('./result-all_train_test_lower.pkl', 'rb') as f:
        results = pickle.load(f)
    data_base = pd.read_csv('../input/raw_database.csv', encoding='utf-8', error_bad_lines=False, header=0)
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
    '''
    with open('./test_output_final.txt', 'w', encoding='utf-8') as f:
        for i in case_pre_list:
            f.write(str(i))
            f.write('\n')
    '''
    
    xlsx = pd.read_excel('../test_output.xlsx', )
    for i in range(len(xlsx.index)):
        out_list = []
        current_set = set(case_pre_list[i])
        for j in current_set:
            out = dict()
            out['mention'] = j[0]
            ty = j[1]
            idx = j[2]
            if ty == 'company':
                out['type'] = '机构_公司'
                out['companyId'] = idx
                out['stockId'] = 'null'
            elif ty == 'stock':
                out['type'] = db[db['stockId'] == idx]['type'].iloc[0]
                out['companyId'] = db[db['stockId'] == idx]['companyId'].iloc[0]
                out['stockId'] = idx
            else:
                print('Wrong type!')
            out_list.append(out)
        xlsx['需输出entities(实体标准词、类型(公司/证券)、公司id、证券id）'].iloc[i] = out_list
    xlsx.to_excel('../test_output.xlsx')