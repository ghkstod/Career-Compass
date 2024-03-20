import streamlit as st
import pandas as pd

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

    # Streamlit 앱
    def app():
        st.title("설문조사 앱")

        # 사용자 응답 저장을 위한 딕셔너리
        responses = {}

        # 질문별로 Streamlit 컴포넌트 생성
        for q_id, q_data in questions_tags_map.items():
            # 질문 표시
            st.write(q_data['question'])
            cols = st.columns(1 if q_id in [1, 3] else 4)  # 1번과 3번 질문은 하나의 열, 나머지는 4열로 표시
            for i, tag in enumerate(q_data['tags']):
                # 각 태그를 적절한 열에 배치
                col_index = i % len(cols)
                response = cols[col_index].checkbox(tag, key=f"{q_id}_{i}")
                if response:
                    responses.setdefault(q_id, []).append(tags_code_map[tag])  # "#" 제거 및 코드로 변환
        
        # 모든 응답을 처리하고 결과를 표시
        if st.button("제출"):
            st.write("선택한 답변:")
            selected_tags = [int(tag) for tags in responses.values() for tag in tags]  # 태그 코드를 정수형으로 변환

            # 각 직업별로 선택된 태그와 일치하는 태그의 수를 카운트
            job_match_counts = tag_to_jobs_df[tag_to_jobs_df['id_tag'].isin(selected_tags)]
            job_match_counts = job_match_counts.groupby('id_jobs')['id_tag'].count().reset_index(name='match_count')

            # 일치하는 태그의 수를 기준으로 정렬
            job_match_counts = job_match_counts.sort_values(by='match_count', ascending=False)

            # 상위 3순위 직업의 일치 태그 수를 구함
            top_counts = job_match_counts['match_count'].unique()[:3]

            if len(top_counts) > 0:
                st.write("추천 직업:")
                for i, count in enumerate(top_counts, start=1):
                    # 현재 순위에 해당하는 모든 직업 ID 찾기
                    current_rank_jobs = job_match_counts[job_match_counts['match_count'] == count]
                    current_rank_job_ids = current_rank_jobs['id_jobs'].unique()
                    
                    # 일치하는 직업 이름 찾기
                    matched_jobs_names = jobs_df[jobs_df['id_jobs'].isin(current_rank_job_ids)]['name_jobs'].tolist()
                    
                    st.write(f"{i}순위 (일치하는 태그 수: {count}):")
                    for job_name in matched_jobs_names:
                        st.write(f"- {job_name}")
            else:
                st.write("선택한 태그에 해당하는 추천 직업이 없습니다.")

    app()
