import streamlit as st
import mysql.connector
import reports.dashboard 


mydb = mysql.connector.connect(
    host= st.secrets["host"],
    user= st.secrets["user"],
    password = st.secrets["password"],
    database= st.secrets["database"],
    port= st.secrets["port"],
)

mycursor = mydb.cursor()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()



def createUser():
    name = st.text_input("Enter your name: ")
    email = st.text_input("Enter your email:")
    if st.button('Create'):
        sql = "insert into user(name,email) values(%s,%s)"
        val = (name, email)
        mycursor.execute(sql,val)
        mydb.commit()
        st.success("Record Created Successfully")
        
if st.session_state.logged_in:
    createUser()

def showUser():
    if st.button('Show User'):
        sql = "select * from user"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        for row in data:
            st.write(row)
        st.success("data fetched successfully")
        
if st.session_state.logged_in:
    showUser()



login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "reports/dashboard.py", title="Dashboard", icon=":material/dashboard:",default=True
)
bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page(
    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
)

search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()