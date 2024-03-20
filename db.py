import sqlite3
import pandas as pd 

path='./db_data/'
edu_company=pd.read_csv(path+'edu_company.csv')
edu_program=pd.read_csv(path+'edu_program.csv')
jobs=pd.read_csv(path+'jobs.csv')
ncs_to_jobs=pd.read_csv(path+'ncs_to_jobs.csv')
question=pd.read_csv(path+'question.csv')
tag_class=pd.read_csv(path+'tag_class.csv')
tag=pd.read_csv(path+'tag.csv')

conn=sqlite3.connect('./db/CareerCompass.db')
c=conn.cursor()

c.execute('''CREATE TABLE "edu_company" (
	"id_edu_company"	INTEGER,
	"name_edu_company"	TEXT NOT NULL UNIQUE,
	"address"	TEXT,
	PRIMARY KEY("id_edu_company")
);''')

c.execute('''CREATE TABLE "edu_program" (
	"id_edu_program"	INTEGER NOT NULL,
	"id_edu_company"	INTEGER NOT NULL,
	"name_edu_program"	TEXT NOT NULL,
	"date_start"	INTEGER,
	"date_end"	INTEGER,
	"cost"	INTEGER NOT NULL,
	"oopc"	INTEGER NOT NULL,
	"link"	TEXT NOT NULL,
	"online_status"	TEXT NOT NULL,
	"employment_status"	TEXT NOT NULL
);''')

c.execute('''CREATE TABLE "jobs" (
	"id_jobs"	INTEGER UNIQUE,
	"name_jobs"	TEXT,
	PRIMARY KEY("id_jobs")
);''')

c.execute('''CREATE TABLE "ncs_to_jobs" (
	"id_jobs"	INTEGER,
	"ncs_code"	INTEGER
);''')

c.execute('''CREATE TABLE "question" (
	"id_question"	INTEGER NOT NULL,
	"id_tag_class"	INTEGER NOT NULL,
	"name_question"	TEXT NOT NULL,
	PRIMARY KEY("id_question")
);''')

c.execute('''CREATE TABLE "tag" (
	"id_tag_class"	INTEGER NOT NULL,
	"id_tag"	INTEGER NOT NULL,
	"name_tag"	TEXT NOT NULL
);''')

c.execute('''CREATE TABLE "tag_class" (
	"id_tag_class"	INTEGER NOT NULL,
	"name_tag_class"	TEXT NOT NULL,
	PRIMARY KEY("id_tag_class")
);''')

edu_company.to_sql('edu_company',conn,if_exists='append',index=False)
edu_program.to_sql('edu_program',conn,if_exists='append',index=False)
jobs.to_sql('jobs',conn,if_exists='append',index=False)
ncs_to_jobs.to_sql('ncs_to_jobs',conn,if_exists='append',index=False)
question.to_sql('question',conn,if_exists='append',index=False)
tag_class.to_sql('tag_class',conn,if_exists='append',index=False)
tag.to_sql('tag',conn,if_exists='append',index=False)

conn.close()