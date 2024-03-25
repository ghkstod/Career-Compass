import streamlit as st
import pandas as pd
import sqlite3

class SurveyMatcher:
    def __init__(self, data_path='./db_data/', db_path='./db/responses.db'):
        self.data_path = data_path
        self.db_path = db_path
        self.load_data()
        self.initialize_db()

    def load_data(self):
        self.question_df = pd.read_csv(self.data_path + 'question.csv')
        self.tag_df = pd.read_csv(self.data_path + 'tag.csv')
        self.tag_class_df = pd.read_csv(self.data_path + 'tag_class.csv')
        self.tag_to_jobs_df = pd.read_csv(self.data_path + 'tag_to_jobs.csv')
        self.jobs_df = pd.read_csv(self.data_path + 'jobs.csv')
        self.prepare_questions_tags_map()

    def prepare_questions_tags_map(self):
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
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS responses (response_id INTEGER PRIMARY KEY AUTOINCREMENT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_responses (response_id INTEGER, tag_id INTEGER, FOREIGN KEY(response_id) REFERENCES responses(response_id))''')
        conn.commit()
        conn.close()

    def save_responses(self, tag_ids):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO responses DEFAULT VALUES')
        response_id = c.lastrowid
        for tag_id in tag_ids:
            c.execute('INSERT INTO user_responses (response_id, tag_id) VALUES (?, ?)', (response_id, tag_id))
        conn.commit()
        conn.close()

    def run_survey(self):
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
        ranks_to_display = 0

        for count in top_counts:
            current_rank_jobs = job_match_counts[job_match_counts['match_count'] == count]
            if len(current_rank_jobs) >= 4 and ranks_to_display == 0:
                ranks_to_display = 1
                break
            elif len(current_rank_jobs) < 4:
                ranks_to_display += 1

        if ranks_to_display > 0:
            st.write("이런 직업들이 어울리겠는데??:")
            for i, count in enumerate(top_counts[:ranks_to_display], start=1):
                self.display_job_rank(i, count, job_match_counts)
        else:
            st.write("선택한 태그에 해당하는 추천 직업이 없습니다.")

    def display_job_rank(self, rank, count, job_match_counts):
        current_rank_jobs = job_match_counts[job_match_counts['match_count'] == count]
        current_rank_job_ids = current_rank_jobs['id_jobs'].unique()
        matched_jobs_names = self.jobs_df[self.jobs_df['id_jobs'].isin(current_rank_job_ids)]['name_jobs'].tolist()

        st.write(f"{rank}순위 ")
        for job_name in matched_jobs_names:
            st.markdown(f"{job_name}")
        if rank == 1 and len(matched_jobs_names) >= 4:
            return

if __name__ == '__main__':
    survey_app = SurveyMatcher()
    survey_app.run_survey()
