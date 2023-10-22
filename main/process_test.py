import os
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('../input/raw_test.csv', encoding='utf-8', error_bad_lines=False,
                       usecols=lambda x: x[0] != 'U' and x[0] != 'i')
    df = pd.DataFrame(data)
    seq = ''
    for i in range(len(df.index)):
        temp_s = ['O' for times in range(len(df['text（正文）'][i]))]
        count = 0
        for j in range(len(df['text（正文）'][i])):
            count += 1
            if df['text（正文）'][i][j] == '。':
                if count >= 256:
                    print(i)
                    print(df['text（正文）'][i])
                count = 0
            if df['text（正文）'][i][j] == '。' or df['text（正文）'][i][j] == '；':
                seq += df['text（正文）'][i][j] + ' ' + temp_s[j] + '\n' + '\n'
            elif df['text（正文）'][i][j] == '':
                seq += '#' + ' ' + temp_s[j] + '\n'
            else:
                seq += df['text（正文）'][i][j] + ' ' + temp_s[j] + '\n'
        seq += '=' + ' ' + 'O' + '\n'
    with open('../processed_data/test.txt', 'w', encoding='utf-8') as f:
        f.write(seq)
    #print(seq)
