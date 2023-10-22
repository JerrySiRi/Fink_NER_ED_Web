import pickle
import output_process
import pandas as pd

# TODO:
# (sto\org名称（bert的偏好）, 在sto中相似度最高的id , 在sto中相似度最高的得分 , 在org中相似度最高的id , 在org中相似度最高的得分 )
# bert的偏好在字典的键之中

# 
predict_dir ="../result.pkl"# result中的是预测的，已经到数据集中匹配过了，是当前的entities name
real_dir = "../dev_label.pkl"

type_list=['sto','org']

df_comid=pd.read_csv('../input/raw_database.csv',usecols=['companyId','companyName'],index_col=0)
df_stoid=pd.read_csv('../input/raw_database.csv',usecols=['stockId','stockName'],index_col=0)

line=0.76

def F1_P_R(project,correct):
    total_num=len(project)+len(correct)+1e-8
    inter_num=len(project.intersection(correct))
    return 2*inter_num/total_num, inter_num/(len(project)+1e-8), inter_num/(len(correct)+1e-8)


def predict_process(loaded_data):
    predict_result=set()
    for type in type_list:
        cur_cate = loaded_data[type]
        for cur_index in range(len(cur_cate)):
#TODO:(加权得到的type, 在sto中相似度最高的id , 在sto中相似度最高的得分 , 在org中相似度最高的id , 在org中相似度最高的得分 )
# --->(entities name,type,id)
            temp =list()
            #temp.append(cur_cate[cur_index][-1])
            if type == 'sto':
                stockid = cur_cate[cur_index][1]
                if stockid == -1:
                    continue
                df_temp=df_stoid.loc[int(stockid),'stockName']
                if isinstance(df_temp,str):
                    temp.append(df_temp)
                else:
                    df_temp=pd.DataFrame(df_temp)
                    df_temp=pd.DataFrame(df_temp.iloc[0])
                    sName=df_temp.iat[0,0]
                    temp.append(sName)
                temp.append(type)
                temp.append(int(cur_cate[cur_index][1]))
            else:
                companyid = cur_cate[cur_index][3]
                # companyid会有-1 ('org', -1, 0, -1, 0)#相似度为0，id是-1》》database中没有，就可以continue了
                if companyid == -1:
                    continue
                df_temp=df_comid.loc[int(companyid),'companyName']
                if isinstance(df_temp,str):
                    temp.append(df_temp)
                else:
                    df_temp=pd.DataFrame(df_temp)
                    df_temp=pd.DataFrame(df_temp.iloc[0])
                    cName=df_temp.iat[0,0]#当前的companyName
                    temp.append(cName)
                temp.append(type)
                temp.append(int(cur_cate[cur_index][3]))
            predict_result.add(tuple(temp))
    return predict_result

def real_process():
    real_result=set()
    with open(real_dir,'rb') as f:
        unpickler=pickle.Unpickler(f)
        loaded_data = unpickler.load()
        for type in type_list:
            cur_cate = loaded_data[type]#类别全是stock\organization的列表，元素是元祖
            for cur_index in range(len(cur_cate)):
#TODO:(id,mentions name)--->(entities name,type,id)
                temp = list()
            #temp.append(cur_cate[cur_index][-1])
                if type == 'sto':
                    stockid = cur_cate[cur_index][0]
                    df_temp=df_stoid.loc[int(stockid),'stockName']
                    if isinstance(df_temp,str):
                        temp.append(df_temp)
                    else:    
                        df_temp=pd.DataFrame(df_temp)
                        df_temp=pd.DataFrame(df_temp.iloc[0])
                        sName=df_temp.iat[0,0]
                        temp.append(sName)
                    temp.append(type)
                    temp.append(int(cur_cate[cur_index][0]))
                else:
                    companyid = cur_cate[cur_index][0]
                    df_temp=df_comid.loc[int(companyid),'companyName']
                    if isinstance(df_temp,str):
                        temp.append(df_temp)
                    else:
                        df_temp=pd.DataFrame(df_temp)
                        df_temp=pd.DataFrame(df_temp.iloc[0])
                        cName=df_temp.iat[0,0]#当前的companyName
                        temp.append(cName)
                    temp.append(type)
                    temp.append(int(cur_cate[cur_index][0]))
                real_result.add(tuple(temp))
    return real_result





if __name__ == '__main__':
    with open(predict_dir,'rb') as f:
        unpickler=pickle.Unpickler(f)
        loaded_data = unpickler.load() # 呈形{'sto':[(,,,),],'org':[(,,,),]}
        #print(loaded_data)
        #以下对sto_data，org_data进行修改，仍需拼接成一个字典
        sto_data=loaded_data['sto']#bert认为是stock的相似度匹配结果
        org_data=loaded_data['org']#bert认为是org的相似度匹配结果
        type_list=['sto','org']
        share=[0,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        for cur_pro in share:#bert的结果所占比例
            cur_sto_data=[]
            cur_org_data=[]
            for type in type_list:#bert的两种偏好分别进行考量
                if type == 'sto':#bert认为是stock。sto_data*1，org_data*0
                    for index in range(len(sto_data)):
                        if sto_data[index][2]<=line:#本条stock的相似度
                            continue
                        s_score,o_score=0,0
                        s_score = cur_pro * 1+sto_data[index][2]*(1-cur_pro)
                        o_score = sto_data[index][-1]*(1-cur_pro)

                        if s_score >= o_score:
                            temp = list(sto_data[index])
                            temp[0] = 'sto'
                            cur_sto_data.append(tuple(temp))
                        else:
                            temp = list(sto_data[index])
                            temp[0] = 'org'
                            cur_org_data.append(tuple(temp))
                            
                else:#bert认为是org。sto_data*1，org_data*0
                    for index in range(len(org_data)):
                        if org_data[index][-1]<=line:
                            continue
                        s_score,o_score=0,0
                        s_score = org_data[index][2]*(1-cur_pro)
                        o_score = cur_pro*1 + org_data[index][-1]*(1-cur_pro)
                        if s_score < o_score:
                            temp = list(org_data[index])
                            temp[0] = 'org'
                            cur_org_data.append(tuple(temp))
                        else:
                            temp = list(org_data[index])
                            temp[0] = 'sto'
                            cur_sto_data.append(tuple(temp))
            
            print("当前bert模型的置信度为",cur_pro)
            new_data={'sto':cur_sto_data,'org':cur_org_data}#加权得到的所属stock和organization的分类
            predict_set=predict_process(new_data)
            real_set=real_process()
            F1,P,R=F1_P_R(predict_set,real_set)
            print("F1=",F1,"P=",P,"R=",R)


            
                    
                            








