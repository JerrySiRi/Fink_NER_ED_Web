import os
import pandas as pd
import pickle

if __name__ == '__main__':
    processed_data_dir = '../processed_data'
    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)

    data = pd.read_csv('../input/raw_train.csv', encoding='utf-8', error_bad_lines=False,
                       usecols=lambda x: x[0] != 'U' and x[0] != 'i')
    df = pd.DataFrame(data)

    seq = ''
    train_num = int(0.7*len(df.index))
    eval_num = len(df.index) - train_num

    for i in range(train_num):#此处是训练集30%的划分验证集。
        #如若获得最终全部训练集训练结果，请把上train_num替换成len(df.index)
        temp_s = ['O' for times in range(len(df['text'][i]))]
        entities = df['entities'][i][1:-2]
        entities = entities.split('},')
        ent_list = []
        for ent in entities:
            if ent == '' or ent == '\n' or ent == '\t':
                continue
            if ent[-1] != '}':
                ent += '}'
            if ent[0] == ' ':
                ent = ent[1:]
            ent = ent.replace('null', '""')
            ent = eval(ent)
            ent_list.append(ent)
        for m_o in eval(df['mentions'][i]):
            men = m_o['mention']
            off = eval(m_o['offset'])
            m_type = ''
            for ent in ent_list:
                if men == ent['mention']:
                    m_type = ent['type']
                    break
            if m_type == '机构':
                temp_s[off[0]] = 'B-ORG'
                for cou in range(off[0]+1, off[1]):
                    temp_s[cou] = 'I-ORG'
            elif m_type == '证券':
                temp_s[off[0]] = 'B-STO'
                for cou in range(off[0]+1, off[1]):
                    temp_s[cou] = 'I-STO'
            elif m_type == '':
                temp_s[off[0]] = 'B-ORG'
                for cou in range(off[0]+1, off[1]):
                    temp_s[cou] = 'I-ORG'
        for j in range(len(df['text'][i])):
            if df['text'][i][j] == '。' or df['text'][i][j] == '；':
                seq += df['text'][i][j] + ' ' + temp_s[j] + '\n' + '\n'
            elif df['text'][i][j] == '':
                seq += '#' + ' ' + temp_s[j] + '\n'
            else:
                seq += df['text'][i][j] + ' ' + temp_s[j] + '\n'
    with open(processed_data_dir + '/train.txt', 'w', encoding='utf-8') as f:
        f.write(seq)

    seq = ''
    dev_org = []
    dev_sto = []
    dev_men = []
    for i in range(train_num, train_num+eval_num):
        temp_s = ['O' for times in range(len(df['text'][i]))]
        count = 0
        entities = df['entities'][i][1:-2]
        entities = entities.split('},')
        ent_list = []
        for ent in entities:
            if ent == '' or ent == '\n' or ent == '\t':
                continue
            if ent[-1] != '}':
                ent += '}'
            if ent[0] == ' ':
                ent = ent[1:]
            ent = ent.replace('null', '""')
            ent = eval(ent)
            ent_list.append(ent)
        for m_o in eval(df['mentions'][i]):
            men = m_o['mention']
            off = eval(m_o['offset'])
            m_type = ''
            for ent in ent_list:
                if men == ent['mention']:
                    m_type = ent['type']
                    break
            if m_type == '机构':
                # dev_org.append((ent['companyId'], men))
                temp_s[off[0]] = 'B-ORG'
                for cou in range(off[0] + 1, off[1]):
                    temp_s[cou] = 'I-ORG'
            elif m_type == '证券':
                # dev_sto.append((ent['stockId'], men))
                temp_s[off[0]] = 'B-STO'
                for cou in range(off[0] + 1, off[1]):
                    temp_s[cou] = 'I-STO'
            elif m_type == '':
                # dev_men.append(men)
                temp_s[off[0]] = 'B-ORG'
                for cou in range(off[0] + 1, off[1]):
                    temp_s[cou] = 'I-ORG'
        for j in range(len(df['text'][i])):
            count += 1
            if df['text'][i][j] == '。':
                if count >= 256:
                    print(i)
                count = 0
            if df['text'][i][j] == '。' or df['text'][i][j] == '；':
                seq += df['text'][i][j] + ' ' + temp_s[j] + '\n' + '\n'
            elif df['text'][i][j] == '':
                seq += '#' + ' ' + temp_s[j] + '\n'
            else:
                seq += df['text'][i][j] + ' ' + temp_s[j] + '\n'

    with open(processed_data_dir + '/dev.txt', 'w', encoding='utf-8') as f:
        f.write(seq)

    '''
    d = dict()
    d['org'] = dev_org
    d['sto'] = dev_sto
    d['men'] = dev_men
    with open('../dev_label.pkl', 'wb') as f:
        pickle.dump(d, f)

       
    data_base = pd.read_csv('../raw_database.csv', encoding='utf-8', error_bad_lines=False, header=0)
    db = pd.DataFrame(data_base)
    print(db.query('stockId == 265832'))'''