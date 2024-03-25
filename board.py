import streamlit as st
import sqlite3

class BoardApp:
    def __init__(self, db_path='./db/bulletin_board.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            content TEXT, 
            likes INTEGER DEFAULT 0
        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            post_id INTEGER, 
            content TEXT, 
            likes INTEGER DEFAULT 0
        )''')
        self.conn.commit()

    def update_post(self, post_id, title, content):
        self.c.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
        self.conn.commit()

    def update_comment(self, comment_id, content):
        self.c.execute("UPDATE comments SET content=? WHERE id=?", (content, comment_id))
        self.conn.commit()

    def like_post(self, post_id):
        self.c.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
        self.conn.commit()
        self.rerun_if_possible()

    def like_comment(self, comment_id):
        self.c.execute("UPDATE comments SET likes = likes + 1 WHERE id=?", (comment_id,))
        self.conn.commit()
        self.rerun_if_possible()

    def get_comment_count(self, post_id):
        return self.c.execute("SELECT COUNT(*) FROM comments WHERE post_id=?", (post_id,)).fetchone()[0]

    def search_posts(self, keyword):
        return self.c.execute("SELECT id, title FROM posts WHERE title LIKE ? ORDER BY id DESC", ('%' + keyword + '%',)).fetchall()

    def add_post(self, title, content):
        self.c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        self.conn.commit()

    def add_comment(self, post_id, content):
        self.c.execute("INSERT INTO comments (post_id, content) VALUES (?, ?)", (post_id, content))
        self.conn.commit()

    def delete_post(self, post_id):
        self.c.execute("DELETE FROM comments WHERE post_id=?", (post_id,))
        self.c.execute("DELETE FROM posts WHERE id=?", (post_id,))
        self.conn.commit()

    def delete_comment(self, comment_id):
        self.c.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        self.conn.commit()

    def rerun_if_possible(self):
        if 'refresh' in st.session_state:  # 세션 상태를 사용하여 UI 갱신
            st.experimental_rerun()

    def run(self):
        if 'current_view' not in st.session_state:
            st.session_state['current_view'] = 'main_page'
        
        if st.session_state['current_view'] == 'main_page':
            self.main_page()
        elif st.session_state['current_view'] == 'view_post':
            self.view_post(st.session_state['post_id'])
        elif st.session_state['current_view'] == 'add_post':
            self.display_post_form()
        elif st.session_state['current_view'] == 'edit_post':
            self.edit_post_form(st.session_state['edit_post_id'])

    def edit_post_form(self, post_id):
        """게시글 수정 양식"""
        post_details = self.c.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,)).fetchone()
        if post_details:
            new_title = st.text_input("제목", post_details[0])
            new_content = st.text_area("내용", post_details[1])
            if st.button("변경사항 저장"):
                self.update_post(post_id, new_title, new_content)
                st.session_state['current_view'] = 'view_post'
                st.session_state['post_id'] = post_id  # 수정한 게시물을 바로 볼 수 있도록 설정
                self.rerun_if_possible()
        else:
            st.error("게시물을 찾을 수 없습니다.")

    def view_post(self, post_id):
        """게시글 보기 및 수정, 삭제 기능"""
        post = self.c.execute("SELECT title, content, likes FROM posts WHERE id = ?", (post_id,)).fetchone()
        if post:
            title, content, likes = post
            st.subheader(title)
            st.write(content)
            st.write(f"Likes: {likes}")
            col1, col2, col3, col4 = st.columns(4)
            if col1.button("좋아요", key=f"like_{post_id}"):
                self.like_post(post_id)
                self.rerun_if_possible()
            '''
            if col2.button("수정하기", key=f"edit_{post_id}"):
                st.session_state['current_view'] = 'edit_post'
                st.session_state['edit_post_id'] = post_id
                self.rerun_if_possible()
            if col3.button("삭제하기", key=f"delete_{post_id}"):
                self.delete_post(post_id)
                st.session_state['current_view'] = 'main_page'
                self.rerun_if_possible()
            '''
            if col4.button("메인으로 돌아가기"):
                st.session_state['current_view'] = 'main_page'
                self.rerun_if_possible()
            self.display_comments_section(post_id)
        else:
            st.error("게시물을 찾을 수 없습니다.")

    def display_comments_section(self, post_id):
        comments = self.c.execute("SELECT id, content, likes FROM comments WHERE post_id = ?", (post_id,)).fetchall()
        for comment_id, content, likes in comments:
            st.markdown(f"- {content} (Likes: {likes})")
            if st.button("좋아요", key=f"like_comment_{comment_id}"):
                self.like_comment(comment_id)
                self.rerun_if_possible()
        comment_content = st.text_area("댓글 작성하기", key=f"comment_{post_id}")
        if st.button("댓글 올리기"):
            if comment_content.strip():
                self.add_comment(post_id, comment_content)
                st.experimental_rerun()

    def display_post_form(self):
        """새 게시글 작성 양식을 표시합니다."""
        with st.form("new_post"):
            title = st.text_input("제목")
            content = st.text_area("내용")
            submitted = st.form_submit_button("제출")
            if submitted and title and content:
                self.add_post(title, content)
                st.success("게시글이 성공적으로 추가되었습니다.")
                st.session_state['current_view'] = 'main_page'
                self.rerun_if_possible()

    def main_page(self):
        """메인 페이지와 새 게시글 작성 버튼을 표시합니다."""
        st.markdown('<h1 style = "color : #2ec4b6; font-size : 50px; text-align : left;">커뮤니티</h1>', unsafe_allow_html=True)
        if st.button("새 게시글 작성"):
            st.session_state['current_view'] = 'add_post'
        search_keyword = st.text_input("게시물 검색")
        if search_keyword:
            posts = self.search_posts(search_keyword)
        else:
            posts = self.c.execute("SELECT id, title FROM posts ORDER BY id DESC").fetchall()
        for post_id, title in posts:
            if st.button(title, key=f"post_{post_id}"):
                st.session_state['current_view'] = 'view_post'
                st.session_state['post_id'] = post_id

    def run(self):
        if 'current_view' not in st.session_state:
            st.session_state['current_view'] = 'main_page'
        view = st.session_state['current_view']
        if view == 'main_page':
            self.main_page()
        elif view == 'view_post':
            self.view_post(st.session_state['post_id'])
        elif view == 'add_post':
            self.display_post_form()
        elif view == 'edit_post':
            self.edit_post_form(st.session_state['edit_post_id'])


if __name__ == '__main__':
    app = BoardApp()
    app.run()
