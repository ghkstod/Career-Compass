import pandas as pd
import sqlite3

conn = sqlite3.connect('./db/data.db')

def load_data():
    path='./db_data/'
    edu_company=pd.read_csv(path+'edu_company.csv')
    edu_program=pd.read_csv(path+'edu_program.csv')
    jobs_to_worknet=pd.read_csv(path+'jobs_to_worknet.csv')
    #jobs=pd.read_csv(path+'jobs.csv')
    #ncs_to_jobs=pd.read_csv(path+'ncs_to_jobs.csv')
    #ncs=pd.read_csv(path+'ncs.csv')
    #question=pd.read_csv(path+'question.csv')
    #tag_class=pd.read_csv(path+'tag_class.csv')
    #tag_to_jobs=pd.read_csv(path+'tag_to_jobs.csv')
    #tag=pd.read_csv(path+'tag.csv')
    worknet_company=pd.read_csv(path+'worknet_company.csv')
    worknet_positions=pd.read_csv(path+'worknet_positions.csv')
    
    # 각 데이터 프레임을 고유한 이름의 테이블로 저장
    edu_company.to_sql('edu_company', conn, if_exists='replace', index=False)
    edu_program.to_sql('edu_program', conn, if_exists='replace', index=False)
    jobs_to_worknet.to_sql('jobs_to_worknet', conn, if_exists='replace', index=False)
    #jobs.to_sql('jobs', conn, if_exists='replace', index=False)
    #ncs_to_jobs.to_sql('ncs_to_jobs', conn, if_exists='replace', index=False)
    #ncs.to_sql('ncs', conn, if_exists='replace', index=False)
    #question.to_sql('question', conn, if_exists='replace', index=False)
    #tag_class.to_sql('tag_class', conn, if_exists='replace', index=False)
    #tag_to_jobs.to_sql('tag_to_jobs', conn, if_exists='replace', index=False)
    #tag.to_sql('tag', conn, if_exists='replace', index=False)
    worknet_company.to_sql('worknet_company', conn, if_exists='replace', index=False)
    worknet_positions.to_sql('worknet_positions', conn, if_exists='replace', index=False)
    
load_data()
