import streamlit as st
import pandas as pd
import sqlite3

def survey():
    # CSV 파일 로드
    question_df = pd.read_csv('./db_data/question.csv')
    tag_df = pd.read_csv('./db_data/tag.csv')
    tag_class_df = pd.read_csv('./db_data/tag_class.csv')
    tag_to_jobs_df = pd.read_csv('./db_data/tag_to_jobs.csv')
    jobs_df = pd.read_csv('./db_data/jobs.csv')

    # 질문 데이터와 태그 데이터를 매핑
    questions_tags_map = {}
    tags_code_map = {}  # 태그 이름을 태그 코드로 매핑
    for _, row in question_df.iterrows():
        question_tags = tag_df[tag_df['id_tag'].astype(str).str.startswith(str(row['id_tag_class']))]
        questions_tags_map[row['id_question']] = {
            'question': f"Q{row['id_question']} {row['name_question']}",
            'tags': [f"#{tag}" for tag in question_tags['answer_tag'].tolist()]
        }
        for _, tag_row in question_tags.iterrows():
            tags_code_map[f"#{tag_row['answer_tag']}"] = str(tag_row['id_tag'])
            
    def initialize_db(db_path='./db/responses.db'):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS responses (response_id INTEGER PRIMARY KEY AUTOINCREMENT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_responses (response_id INTEGER, tag_id INTEGER, FOREIGN KEY(response_id) REFERENCES responses(response_id))''')
        conn.commit()
        conn.close()

    initialize_db()

    def save_responses(tag_ids, db_path='./db/responses.db'):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO responses DEFAULT VALUES')
        response_id = c.lastrowid
        for tag_id in tag_ids:
            c.execute('INSERT INTO user_responses (response_id, tag_id) VALUES (?, ?)', (response_id, tag_id))
        conn.commit()
        conn.close()

    def app():
        st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">직업추천</h1>', unsafe_allow_html=True)
        st.write('밑의 설문조사를 작성하고, 너의 취향에 맞는 직업을 추천받아 봐!')
        responses = {}
        missing_responses = []

        for q_id, q_data in questions_tags_map.items():
            st.write(q_data['question'])
            cols = st.columns(1) if q_id in [1, 3] else st.columns(3)

            for i, tag in enumerate(q_data['tags']):
                col_index = i % len(cols)
                response = cols[col_index].checkbox(tag, key=f"{q_id}_{i}")
                if response:
                    responses.setdefault(q_id, []).append(tags_code_map[tag])

        if st.button("제출"):
            for q_id in questions_tags_map:
                if q_id not in responses:
                    missing_responses.append(f"{q_id}번 질문")
            
            if missing_responses:
                st.error(f"질문은 빠짐없이 체크해야해!!: {', '.join(missing_responses)}")
            else:
                selected_tags = [int(tag) for tags in responses.values() for tag in tags]
                save_responses(selected_tags)
                job_match_counts = tag_to_jobs_df[tag_to_jobs_df['id_tag'].isin(selected_tags)].groupby('id_jobs')['id_tag'].count().reset_index(name='match_count').sort_values(by='match_count', ascending=False)

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
                    st.write("이런 직업들이 어울리겠는데??")
                    for i, count in enumerate(top_counts[:ranks_to_display], start=1):
                        current_rank_jobs = job_match_counts[job_match_counts['match_count'] == count]
                        current_rank_job_ids = current_rank_jobs['id_jobs'].unique()
                        matched_jobs_names = jobs_df[jobs_df['id_jobs'].isin(current_rank_job_ids)]['name_jobs'].tolist()
                        
                        st.write(f"{i}순위 ")
                        for job_name in matched_jobs_names:
                            st.markdown(f"{job_name}")
                        # 1순위에 4개 이상 직업이 있으면 그만 출력
                        if i == 1 and len(matched_jobs_names) >= 4:
                            break
                else:
                    st.write("선택한 태그에 해당하는 추천 직업이 없습니다.")


    app()
