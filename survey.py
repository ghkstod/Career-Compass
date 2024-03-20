import streamlit as st
import pandas as pd

# 데이터 로드 및 전처리 함수
def survey():
    def load_data():
        questions = pd.read_csv('./db_data/question.csv')
        tags = pd.read_csv('./db_data/tag.csv')
        tag_classes = pd.read_csv('./db_data/tag_class.csv')
        return questions, tags, tag_classes

    def preprocess_data(questions, tags, tag_classes):
        # 태그와 태그 클래스 정보를 병합
        tags_with_class = pd.merge(tags, tag_classes, on='id_tag_class')
        # 질문 정보와 태그 정보를 병합하여 각 질문에 대한 가능한 태그들을 매핑
        questions_with_tags = pd.merge(questions, tags_with_class, on='id_tag_class')
        return questions_with_tags

    questions, tags, tag_classes = load_data()
    questions_with_tags = preprocess_data(questions, tags, tag_classes)
    
    st.title('설문조사')

    responses = {}  # 사용자 응답 저장 딕셔너리
    
    for _, row in questions.iterrows():
        st.markdown(f"**Q {row['id_question']}: {row['name_question']}**")
        options = questions_with_tags[questions_with_tags['id_question'] == row['id_question']]
        
        selected_options = []
        if row['id_question'] in [1, 3]:  # 1번과 3번 질문의 경우
            for _, option_row in options.iterrows():
                option_text = f"#{option_row['answer_tag']}"  # 선택지 앞에 # 추가
                if st.checkbox(option_text, key=f"{row['id_question']}_{option_row['id_tag']}"):
                    # 응답을 ID와 태그 클래스 ID로 저장
                    selected_options.append({'id_tag': option_row['id_tag'], 'id_tag_class': option_row['id_tag_class']})
        else:  # 다른 질문들의 경우
            options_split = [options.iloc[i:i + 4] for i in range(0, len(options), 4)]
            for option_group in options_split:
                cols = st.columns(len(option_group))
                for col, (_, option_row) in zip(cols, option_group.iterrows()):
                    option_text = f"#{option_row['answer_tag']}"
                    if col.checkbox(option_text, key=f"{row['id_question']}_{option_row['id_tag']}"):
                        # 응답을 ID와 태그 클래스 ID로 저장
                        selected_options.append({'id_tag': option_row['id_tag'], 'id_tag_class': option_row['id_tag_class']})

        responses[row['id_question']] = selected_options

    if st.button('제출'):
        # 사용자 응답 출력 (개선 가능)
        for question_id, options in responses.items():
            st.write(f"Q {question_id}: ", [f"ID Tag: {opt['id_tag']}, ID Tag Class: {opt['id_tag_class']}" for opt in options])

if __name__ == '__main__':
    survey()
