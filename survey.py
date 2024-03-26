import streamlit as st
import pandas as pd
import sqlite3

class SurveyMatcher:
    '''
    사용자의 설문 응답을 바탕으로 직업을 추천하는 애플리케이션.
    
    이 클래스는 Streamlit을 이용하여 웹 기반 인터페이스를 제공하고, 설문 데이터를 처리하며,
    사용자의 응답을 SQLite DB에 저장합니다. 사용자는 여러 설문 질문에 응답하고, 
    이 응답을 바탕으로 선호와 능력에 맞는 직업을 추천받을 수 있습니다.
    
    속성 :
        data_path(str) : 데이터 파일이 위치한 디렉토리의 경로
        db_path(str) : 사용자의 응답을 저장하는 SQLite DB의 파일 경로
        
    메서드 :
        load_data : 해당 애플리케이션에 필요한 데이터 파일들을 로드하고, 데이터 프레임화 합니다.
        prepare_questions_tags_map : 질문과 태그를 매핑합니다.
        initialize_db : SQLite DB를 초기화하고, 필요한 데이터 테이블을 생성합니다.
        save_responses : 사용자 응답을 DB에 저장합니다.
        run_survey : Streamlit을 통해 사용자에게 설문 조사 인터페이스를 제공합니다.
        process_responses : 사용자의 응답을 처리하고, 누락된 응답이 있는지 확인합니다.
        dispaly_matched_jobs : 사용자 응답을 바탕으로 매칭된 직업을 추천하여 출력합니다.
        display_job_rank : 사용자에게 매칭된 직업의 순위를 출력합니다.
        '''
    def __init__(self, db_path='./db/data.db'):
        '''
        SurveyMatcher 클래스의 인스턴스를 초기화합니다.
        
        매개변수 :
            db_path(str) : 사용자의 응답을 저장하는 SQLite DB의 파일 경로
        '''
        self.db_path = db_path
        self.initialize_db()
        self.load_data()

    def load_data(self):
        '''
        SQLite 데이터베이스에서 필요한 데이터를 로드합니다.
        '''
        conn = sqlite3.connect(self.db_path)

        self.question_df = pd.read_sql_query('SELECT * FROM question', conn)
        self.tag_df = pd.read_sql_query('SELECT * FROM tag', conn)
        self.tag_class_df = pd.read_sql_query('SELECT * FROM tag_class', conn)
        self.tag_to_jobs_df = pd.read_sql_query('SELECT * FROM tag_to_jobs', conn)
        self.jobs_df = pd.read_sql_query('SELECT * FROM jobs', conn)

        conn.close()
        self.prepare_questions_tags_map()

    def prepare_questions_tags_map(self):
        '''
        질문과 태그를 매핑합니다.
        질문 id와 태그 id의 앞 2글자를 통해 매핑을 하여 사용자에게 적절한 설문의 태그를 뽑는데 사용합니다.
        '''
        self.questions_tags_map = {}
        self.tags_code_map = {}
        for _, row in self.question_df.iterrows():
            question_tags = self.tag_df[self.tag_df['id_tag'].astype(str).str.startswith(str(row['id_tag_class']))]
            self.questions_tags_map[row['id_question']] = {
                'question': f"Q{row['id_question']} {row['name_question']}",
                'tags': [f"#{tag}" for tag in question_tags['answer_tag'].tolist()]
            }
            for _, tag_row in question_tags.iterrows():
                self.tags_code_map[f"#{tag_row['answer_tag']}"] = str(tag_row['id_tag'])

    def initialize_db(self):
        '''
        SQLite DB를 초기화하고, 필요한 데이터 테이블을 생성합니다.
        '''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS responses (response_id INTEGER PRIMARY KEY AUTOINCREMENT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_responses (response_id INTEGER, tag_id INTEGER, FOREIGN KEY(response_id) REFERENCES responses(response_id))''')
        conn.commit()
        conn.close()

    def save_responses(self, tag_ids):
        '''
        사용자가 선택한 태그 ID들을 데이터베이스에 저장합니다.
        매개변수 :
            tag_ids(list) : 사용자가 선택한 태그id 목록
        '''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO responses DEFAULT VALUES')
        response_id = c.lastrowid
        for tag_id in tag_ids:
            c.execute('INSERT INTO user_responses (response_id, tag_id) VALUES (?, ?)', (response_id, tag_id))
        conn.commit()
        conn.close()

    def run_survey(self):
        '''
        Streamlit을 통해 사용자에게 설문 조사 인터페이스를 제공합니다.
        '''
        st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">직업추천</h1>', unsafe_allow_html=True)
        st.write('밑의 설문조사를 작성하고, 너의 취향에 맞는 직업을 추천받아 봐!')
        responses = {}
        missing_responses = []

        for q_id, q_data in self.questions_tags_map.items():
            st.write(q_data['question'])
            cols = st.columns(1) if q_id in [1, 3] else st.columns(3)

            for i, tag in enumerate(q_data['tags']):
                col_index = i % len(cols)
                response = cols[col_index].checkbox(tag, key=f"{q_id}_{i}")
                if response:
                    responses.setdefault(q_id, []).append(self.tags_code_map[tag])

        if st.button("제출"):
            self.process_responses(responses)

    def process_responses(self, responses):
        '''
        사용자의 응답을 처리하고, 누락된 응답이 있는지 확인합니다.
        매개변수 : 
            responses(dict) : 사용자의 응답을 담은 딕셔너리
        '''
        missing_responses = [f"{q_id}번 질문" for q_id in self.questions_tags_map if q_id not in responses]

        if missing_responses:
            st.error(f"질문은 빠짐없이 체크해야해!!: {', '.join(missing_responses)}")
        else:
            self.display_matched_jobs(responses)

    def display_matched_jobs(self, responses):
        selected_tags = [int(tag) for tags in responses.values() for tag in tags]
        self.save_responses(selected_tags)
        job_match_counts = self.tag_to_jobs_df[self.tag_to_jobs_df['id_tag'].isin(selected_tags)].groupby('id_jobs')['id_tag'].count().reset_index(name='match_count').sort_values(by='match_count', ascending=False)
        top_counts = job_match_counts['match_count'].unique()[:3]

        if job_match_counts.empty:
            st.write("선택한 태그에 해당하는 추천 직업이 없습니다.")
            return

        st.write("이런 직업들이 어울리겠는데??:")

        # 순위별로 직업 수를 계산하고 저장합니다.
        jobs_per_rank = {rank: 0 for rank in range(1, 4)}
        for i, count in enumerate(top_counts, start=1):
            current_rank_jobs_count = len(job_match_counts[job_match_counts['match_count'] == count])
            jobs_per_rank[i] = current_rank_jobs_count

        # 1순위 조건 검사 및 출력
        if jobs_per_rank[1] >= 3:
            self.display_job_rank(1, top_counts[0], job_match_counts)
        else:
            self.display_job_rank(1, top_counts[0], job_match_counts)
            # 2순위 조건 검사 및 출력
            if jobs_per_rank[2] >= 3:
                # 2순위가 3개 이상인 경우, 3순위는 출력하지 않음
                self.display_job_rank(2, top_counts[1], job_match_counts)
            elif jobs_per_rank[2] > 0:
                # 2순위가 3개 미만이고 존재하는 경우, 2순위를 출력
                self.display_job_rank(2, top_counts[1], job_match_counts)
                # 3순위 조건 검사 및 출력
                if jobs_per_rank[3] > 0:
                    self.display_job_rank(3, top_counts[2], job_match_counts)




    def display_job_rank(self, rank, count, job_match_counts):
        '''
        사용자에게 매칭된 직업의 순위를 출력합니다.
        매개변수 :
            rank(int) : 직업의 우선 순위
            count(int) : 매칭 카운트
            job_match_counts(DataFrame) : 직업과 매치된 카운트를 포함하는 데이터 프레임
        '''
        # 순위별 배경색 설정
        background_colors = {1: '#FFD700', 2: '#C0C0C0', 3: '#CD7F32'}
        background_color = background_colors.get(rank, '#FFFFFF')  # 기본색은 흰색

        # 배경색이 밝은 경우 글자색을 검정색으로 설정
        text_color = '#000000' if background_color in ['#FFD700', '#C0C0C0', '#CD7F32'] else '#FFFFFF'

        current_rank_jobs = job_match_counts[job_match_counts['match_count'] == count]
        current_rank_job_ids = current_rank_jobs['id_jobs'].unique()
        matched_jobs_names = self.jobs_df[self.jobs_df['id_jobs'].isin(current_rank_job_ids)]['name_jobs'].tolist()

        # 순위별 배경색과 글자색을 적용하여 직업 이름 출력
        st.markdown(f'<div style="background-color: {background_color}; color: {text_color}; margin: 10px 0px; padding: 10px; border-radius: 10px;"><h3>{rank}순위 직군</h3>', unsafe_allow_html=True)
        for job_name in matched_jobs_names:
            st.markdown(f'<p style="margin-left: 20px; font-size : 20px; ">- {job_name}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    survey_app = SurveyMatcher()
    survey_app.run_survey()
