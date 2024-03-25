import streamlit as st
import sqlite3

class BoardApp:
    '''
    Streamlit과 SQLite를 사용하여 구현된 간단한 커뮤니티 게시판 애플리케이션.

    사용자는 게시글을 작성, 조회, 수정, 삭제할 수 있으며, 각 게시글에 대해 댓글을 달고 좋아요를 할 수 있습니다.
    게시글과 댓글 데이터는 SQLite 데이터베이스에 저장됩니다.

    속성:
        db_path (str): SQLite 데이터베이스 파일의 경로.
    
    메서드:
        initialize_db(): 데이터베이스 및 필요한 테이블을 초기화합니다.
        update_post(post_id, title, content): 주어진 ID의 게시글을 업데이트합니다.
        update_comment(comment_id, content): 주어진 ID의 댓글을 업데이트합니다.
        like_post(post_id): 주어진 ID의 게시글에 좋아요를 추가합니다.
        like_comment(comment_id): 주어진 ID의 댓글에 좋아요를 추가합니다.
        get_comment_count(post_id): 주어진 ID의 게시글에 대한 댓글 수를 반환합니다.
        search_posts(keyword): 제목에 주어진 키워드가 포함된 게시글을 검색합니다.
        add_post(title, content): 새 게시글을 추가합니다.
        add_comment(post_id, content): 새 댓글을 추가합니다.
        delete_post(post_id): 주어진 ID의 게시글을 삭제합니다.
        delete_comment(comment_id): 주어진 ID의 댓글을 삭제합니다.
        rerun_if_possible(): Streamlit 앱을 재실행합니다(있는 경우).
        run(): 애플리케이션의 메인 루프를 실행합니다.
    '''

    def __init__(self, db_path='./db/bulletin_board.db'):
        '''
        BoardApp 클래스의 인스턴스를 초기화하고, DB연결을 설정
        
        매개변수 : 
            db_path(str) : SQLite DB 파일의 경로
        '''
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        '''
        DB에 필요한 테이블을 초기화합니다.
        '''
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
        '''
        주어진 ID의 게시글을 업데이트합니다.
        
        매개변수:
            post_id (int): 업데이트할 게시글의 ID.
            title (str): 게시글의 새 제목.
            content (str): 게시글의 새 내용.
        '''
        self.c.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
        self.conn.commit()

    def update_comment(self, comment_id, content):
        """
        특정 댓글의 내용을 업데이트합니다.

        매개변수:
            comment_id (int): 업데이트할 댓글의 ID.
            content (str): 댓글의 새 내용.
        """
        self.c.execute("UPDATE comments SET content=? WHERE id=?", (content, comment_id))
        self.conn.commit()

    def like_post(self, post_id):
        """
        특정 게시글의 좋아요 수를 증가시킵니다.

        매개변수:
            post_id (int): 좋아요를 추가할 게시글의 ID.
        """
        self.c.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
        self.conn.commit()
        self.rerun_if_possible()

    def like_comment(self, comment_id):
        """
        특정 댓글의 좋아요 수를 증가시킵니다.

        매개변수:
            comment_id (int): 좋아요를 추가할 댓글의 ID.
        """
        self.c.execute("UPDATE comments SET likes = likes + 1 WHERE id=?", (comment_id,))
        self.conn.commit()
        self.rerun_if_possible()

    def get_comment_count(self, post_id):
        """
        특정 게시글에 달린 댓글의 수를 반환합니다.

        매개변수:
            post_id (int): 댓글 수를 조회할 게시글의 ID.

        반환값:
            int: 해당 게시글에 달린 댓글의 총 수.
        """
        return self.c.execute("SELECT COUNT(*) FROM comments WHERE post_id=?", (post_id,)).fetchone()[0]

    def search_posts(self, keyword):
        """
        제목에 주어진 키워드가 포함된 게시글을 검색합니다.

        매개변수:
            keyword (str): 검색할 키워드.

        반환값:
            list of tuples: 검색 결과에 해당하는 게시글의 ID와 제목을 포함하는 튜플의 리스트.
        """
        return self.c.execute("SELECT id, title FROM posts WHERE title LIKE ? ORDER BY id DESC", ('%' + keyword + '%',)).fetchall()

    def add_post(self, title, content):
        """
        새 게시글을 추가합니다.

        매개변수:
            title (str): 게시글의 제목.
            content (str): 게시글의 내용.
        """
        self.c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        self.conn.commit()

    def add_comment(self, post_id, content):
        """
        새 댓글을 특정 게시글에 추가합니다.

        매개변수:
            post_id (int): 댓글을 추가할 게시글의 ID.
            content (str): 댓글의 내용.
        """
        self.c.execute("INSERT INTO comments (post_id, content) VALUES (?, ?)", (post_id, content))
        self.conn.commit()

    def delete_post(self, post_id):
        """
        특정 게시글과 그에 연관된 모든 댓글을 삭제합니다.

        매개변수:
            post_id (int): 삭제할 게시글의 ID.
        """
        self.c.execute("DELETE FROM comments WHERE post_id=?", (post_id,))
        self.c.execute("DELETE FROM posts WHERE id=?", (post_id,))
        self.conn.commit()

    def delete_comment(self, comment_id):
        """
        특정 댓글을 삭제합니다.

        매개변수:
            comment_id (int): 삭제할 댓글의 ID.
        """
        self.c.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        self.conn.commit()

    def rerun_if_possible(self):
        """
        Streamlit 애플리케이션을 재실행합니다. 이는 UI를 최신 상태로 갱신하기 위해 사용됩니다.
        """
        if 'refresh' in st.session_state:  # 세션 상태를 사용하여 UI 갱신
            st.experimental_rerun()

    def run(self):
        """
        애플리케이션의 메인 루프를 실행합니다. 사용자의 현재 뷰 상태에 따라 적절한 페이지를 표시합니다.
        """
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
        """
        사용자에게 특정 게시글을 수정할 수 있는 양식을 제공합니다.

        이 메서드는 사용자로부터 새 제목과 내용을 입력받아, 해당 게시글을 데이터베이스에서 업데이트합니다.
        성공적으로 수정이 완료되면, 수정된 게시글을 바로 볼 수 있도록 페이지를 전환합니다.

        매개변수:
            post_id (int): 수정할 게시글의 ID.
        """
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
        """
        특정 게시글과 관련된 상세 정보를 사용자에게 표시합니다.

        게시글의 제목, 내용, 좋아요 수를 포함하여 사용자에게 보여주고, 게시글에 달린 댓글을 함께 표시합니다.
        사용자는 '메인으로 돌아가기' 버튼을 통해 메인 페이지로 돌아갈 수 있습니다.

        매개변수:
            post_id (int): 상세 정보를 보여줄 게시글의 ID.
        """
        post = self.c.execute("SELECT title, content, likes FROM posts WHERE id = ?", (post_id,)).fetchone()
        if post:
            title, content, likes = post
            st.subheader(title)
            st.write(content)
            #st.write(f"Likes: {likes}")
            col1, col2, col3, col4 = st.columns(4)
            #if col1.button("좋아요", key=f"like_{post_id}"):
            #    self.like_post(post_id)
            #    self.rerun_if_possible()
            
            #if col2.button("수정하기", key=f"edit_{post_id}"):
            #    st.session_state['current_view'] = 'edit_post'
            #    st.session_state['edit_post_id'] = post_id
            #    self.rerun_if_possible()
            #if col3.button("삭제하기", key=f"delete_{post_id}"):
            #    self.delete_post(post_id)
            #    st.session_state['current_view'] = 'main_page'
            #    self.rerun_if_possible()
            
            if col4.button("메인으로 돌아가기"):
                st.session_state['current_view'] = 'main_page'
                self.rerun_if_possible()
            self.display_comments_section(post_id)
        else:
            st.error("게시물을 찾을 수 없습니다.")

    def display_comments_section(self, post_id):
        """
        특정 게시글에 달린 댓글을 표시합니다.

        사용자는 이 메서드를 통해 게시글에 달린 모든 댓글을 확인할 수 있으며, 새 댓글을 추가할 수 있는 입력창이 제공됩니다.
        '댓글 올리기' 버튼을 클릭하여 새 댓글을 게시할 수 있습니다.

        매개변수:
            post_id (int): 댓글을 표시할 게시글의 ID.
        """
        comments = self.c.execute("SELECT id, content, likes FROM comments WHERE post_id = ?", (post_id,)).fetchall()
        for comment_id, content, likes in comments:
            st.markdown(f"- {content} ")
            #if st.button("좋아요", key=f"like_comment_{comment_id}"):
            #    self.like_comment(comment_id)
            #    self.rerun_if_possible()
            
        comment_content = st.text_area("댓글 작성하기", key=f"comment_{post_id}")
        if st.button("댓글 올리기"):
            if comment_content.strip():
                self.add_comment(post_id, comment_content)
                st.experimental_rerun()

    def display_post_form(self):
        """
        사용자에게 새 게시글을 작성할 수 있는 양식을 제공합니다.

        사용자는 제목과 내용을 입력하여 새 게시글을 작성할 수 있습니다. '제출' 버튼을 클릭하면, 게시글이 데이터베이스에 추가되며,
        성공 메시지가 표시됩니다. 사용자는 언제든지 '취소' 버튼을 클릭하여 메인 페이지로 돌아갈 수 있습니다.
        """
        with st.form("new_post"):
            title = st.text_input("제목")
            content = st.text_area("내용")
            submitted = st.form_submit_button("제출")
            
        if submitted and title and content:
            self.add_post(title, content)
            st.success("게시글이 성공적으로 추가되었습니다.")
            st.session_state['current_view'] = 'main_page'
            self.rerun_if_possible()

        cancelled = st.button("취소")
        if cancelled:
            st.session_state['current_view'] = 'main_page'
            self.rerun_if_possible()

    def main_page(self):
        """
        애플리케이션의 메인 페이지를 표시합니다.

        사용자는 이 메서드를 통해 '새 게시글 작성' 버튼을 클릭하여 게시글 작성 양식으로 이동할 수 있으며,
        게시글 검색 기능을 사용하여 특정 게시글을 찾을 수 있습니다. 검색 결과에 나타난 게시글 제목을 클릭하면,
        해당 게시글의 상세 페이지로 이동합니다.
        """
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

if __name__ == '__main__':
    app = BoardApp()
    app.run()
