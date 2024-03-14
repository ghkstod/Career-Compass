import streamlit as st
import sqlite3
import bcrypt

def board():
    # 데이터베이스 연결 및 테이블 생성
    conn = sqlite3.connect('bulletin_board.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY, 
        title TEXT, 
        content TEXT, 
        likes INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY,
        post_id INTEGER, 
        content TEXT, 
        likes INTEGER DEFAULT 0
    )''')
    conn.commit()


    def update_post(post_id, title, content):
        c.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
        conn.commit()

    def update_comment(comment_id, content):
        c.execute("UPDATE comments SET content=? WHERE id=?", (content, comment_id))
        conn.commit()

    def like_post(post_id):
        c.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
        conn.commit()
        if 'refresh' in st.session_state:  # 세션 상태를 사용하여 UI 갱신
            st.experimental_rerun()

    def like_comment(comment_id):
        c.execute("UPDATE comments SET likes = likes + 1 WHERE id=?", (comment_id,))
        conn.commit()
        if 'refresh' in st.session_state:  # 세션 상태를 사용하여 UI 갱신
            st.experimental_rerun()

    def get_comment_count(post_id):
        return c.execute("SELECT COUNT(*) FROM comments WHERE post_id=?", (post_id,)).fetchone()[0]

    def search_posts(keyword):
        return c.execute("SELECT id, title FROM posts WHERE title LIKE ? ORDER BY id DESC", ('%' + keyword + '%',)).fetchall()

    def add_post(title, content):
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()

    def add_comment(post_id, content):
        c.execute("INSERT INTO comments (post_id, content) VALUES (?, ?)", (post_id, content))
        conn.commit()

    def delete_post(post_id):
        c.execute("DELETE FROM comments WHERE post_id=?", (post_id,))
        c.execute("DELETE FROM posts WHERE id=?", (post_id,))
        conn.commit()

    def delete_comment(comment_id):
        c.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        conn.commit()

    def edit_post_form(post_id):
        """게시글 수정 양식"""
        post_details = c.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,)).fetchone()
        if post_details:
            new_title = st.text_input("제목", post_details[0])
            new_content = st.text_area("내용", post_details[1])
            if st.button("변경사항 저장"):
                update_post(post_id, new_title, new_content)
                st.session_state['current_view'] = 'view_post'
                st.experimental_rerun()
        else:
            st.error("게시물을 찾을 수 없습니다.")

    def view_post(post_id):
        """게시글 보기 및 수정, 삭제 기능"""
        post = c.execute("SELECT title, content, likes FROM posts WHERE id = ?", (post_id,)).fetchone()
        if post:
            title, content, likes = post
            st.subheader(title)
            st.write(content)
            st.write(f"Likes: {likes}")

            # 버튼 그룹을 열로 구분하여 표시
            col1, col2, col3, col4 = st.columns(4)
            
            # 좋아요 버튼
            if col1.button("좋아요", key=f"like_{post_id}"):
                like_post(post_id)
                st.success("게시글에 좋아요를 눌렀습니다.")
                st.experimental_rerun()
                
            # 게시글 수정 버튼
            if col2.button("수정하기", key=f"edit_{post_id}"):
                st.session_state['current_view'] = 'edit_post'
                st.session_state['edit_post_id'] = post_id
            
            # 게시글 삭제 버튼
            if col3.button("삭제하기", key=f"delete_{post_id}"):
                delete_post(post_id)
                st.success("게시글이 삭제되었습니다.")
                st.session_state['current_view'] = 'main_page'
                st.experimental_rerun()
            
            # 메인으로 돌아가기 버튼
            if col4.button("메인으로 돌아가기", key=f"back_to_main_from_view"):
                st.session_state['current_view'] = 'main_page'
                st.experimental_rerun()

            display_comments_section(post_id)
        else:
            st.error("게시물을 찾을 수 없습니다.")

    def display_comments_section(post_id):
        # 댓글 입력 세션 상태 키를 생성합니다.
        comment_input_key = f"comment_input_{post_id}"
        
        # 세션 상태에서 댓글 입력값을 가져오거나 기본값으로 빈 문자열을 설정합니다.
        if comment_input_key not in st.session_state:
            st.session_state[comment_input_key] = ""

        comments = c.execute("SELECT id, content, likes FROM comments WHERE post_id = ?", (post_id,)).fetchall()
        for comment_id, content, likes in comments:
            # 댓글과 댓글 좋아요 버튼, 댓글 삭제 버튼을 표시합니다.
            st.markdown(f"- {content} ")
            if st.button("삭제", key=f"delete_comment_{comment_id}"):
                delete_comment(comment_id)
                st.success("댓글이 삭제되었습니다.")
                st.experimental_rerun()
                    
            # 댓글 작성 및 제출 부분
        comment_content = st.text_area("댓글 작성하기", value=st.session_state[comment_input_key], key=f"comment_{post_id}")
        if st.button("댓글 올리기", key=f"submit_comment_{post_id}"):
            if comment_content.strip():  # 댓글 내용이 비어있지 않은 경우에만 추가합니다.
                add_comment(post_id, comment_content)
                st.session_state[comment_input_key] = ""  # 댓글을 추가한 후 입력란을 비웁니다.
                st.experimental_rerun()

    def display_post_form():
        """새 게시글 작성 양식을 표시합니다."""
        with st.form("new_post"):
            title = st.text_input("제목")
            content = st.text_area("내용")
            submitted = st.form_submit_button("제출")
            if submitted and title and content:
                add_post(title, content)
                st.success("게시글이 성공적으로 추가되었습니다.")
                st.session_state['current_view'] = 'main_page'
        
        # '메인으로 돌아가기' 버튼을 폼 바깥에 추가합니다.
        if st.button("메인으로 돌아가기"):
            st.session_state['current_view'] = 'main_page'
            st.experimental_rerun()

    def main_page():
        """메인 페이지와 새 게시글 작성 버튼을 표시합니다."""
        st.title("게시판")
        if st.button("새 게시글 작성"):
            st.session_state['current_view'] = 'add_post'

        search_keyword = st.text_input("게시물 검색")
        if search_keyword:
            posts = search_posts(search_keyword)
        else:
            posts = c.execute("SELECT id, title FROM posts ORDER BY id DESC").fetchall()
        for post_id, title in posts:
            if st.button(title, key=f"post_{post_id}"):
                st.session_state['current_view'] = 'view_post'
                st.session_state['post_id'] = post_id

    # 앱의 초기 상태를 설정합니다.
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'main_page'

    # 앱의 뷰 로직
    if st.session_state['current_view'] == 'main_page':
        main_page()
    elif st.session_state['current_view'] == 'view_post':
        view_post(st.session_state['post_id'])
    elif st.session_state['current_view'] == 'add_post':
        display_post_form()
    elif st.session_state['current_view'] == 'edit_post':
        edit_post_form(st.session_state['edit_post_id'])
