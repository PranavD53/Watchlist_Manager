import streamlit as st
from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()

if "user" not in st.session_state:
    st.session_state.user = None
if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False

def login_page():
    st.title("🔐 Login / Register")
    choice = st.radio("Choose", ["Login", "Register"])

    if choice == "Login":
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = user_service.authenticate_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.show_main_app = True
                st.success(f"Welcome {user['name']}!")
            else:
                st.error("❌ Invalid credentials")

    elif choice == "Register":
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            res = user_service.register_user(name, email, password)
            if "error" in res:
                st.error(res["error"])
            else:
                st.success("✅ Account created! Please log in.")

def dashboard():
    st.header("📊 Dashboard Overview")

    users = user_service.list_users()
    total_users = len(users)

    titles = title_service.list_all_titles()
    total_titles = len(titles)

    watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
    total_watchlist = len(watchlist)
    watched = len([w for w in watchlist if w["status"] == "watched"])
    planning = len([w for w in watchlist if w["status"] == "planning"])
    dropped = len([w for w in watchlist if w["status"] == "dropped"])

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Users", total_users)
    col2.metric("🎥 Total Titles", total_titles)
    col3.metric("📺 My Watchlist", total_watchlist)

    st.subheader("📺 My Watchlist Breakdown")
    c1, c2, c3 = st.columns(3)
    c1.metric("✅ Watched", watched)
    c2.metric("📌 Planning", planning)
    c3.metric("❌ Dropped", dropped)

def main_app():
    st.sidebar.title(f"👋 Hello, {st.session_state.user['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.show_main_app = False
        st.experimental_rerun()

    menu = st.sidebar.radio("Menu", ["Dashboard", "My Watchlist", "Titles"])

    if menu == "Dashboard":
        dashboard()

    elif menu == "My Watchlist":
        st.header("📺 My Watchlist")

        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        st.subheader("Your Watchlist")
        st.table(watchlist)

        st.subheader("➕ Add to Watchlist")
        with st.form("add_watchlist"):
            movie_id = st.text_input("Movie/Show ID", key="add_movie_id")
            status = st.selectbox("Status", ["watched", "planning", "dropped"], key="add_status")
            rating = st.number_input("Rating (1-10)", min_value=1, max_value=10, step=1, key="add_rating")
            review = st.text_area("Review (optional)", key="add_review")
            if st.form_submit_button("Add"):
                res = watchlist_service.add_to_watchlist(
                    st.session_state.user["user_id"],
                    movie_id,
                    status,
                    rating,
                    review or None,
                )
                st.success(res)

        st.subheader("✏️ Update Watchlist Entry")
        with st.form("update_watchlist"):
            watchlist_id = st.text_input("Watchlist ID", key="update_watchlist_id")
            new_status = st.text_input("New Status (optional)", key="update_status")
            new_rating = st.text_input("New Rating (optional)", key="update_rating")
            new_review = st.text_area("New Review (optional)", key="update_review")
            if st.form_submit_button("Update"):
                res = watchlist_service.update_watchlist_entry(
                    watchlist_id,
                    new_status or None,
                    int(new_rating) if new_rating else None,
                    new_review or None,
                )
                st.success(res)

        st.subheader("❌ Remove from Watchlist")
        with st.form("remove_watchlist"):
            watchlist_id = st.text_input("Watchlist ID", key="remove_watchlist_id")
            if st.form_submit_button("Remove"):
                res = watchlist_service.remove_from_watchlist(watchlist_id)
                st.warning(res)

    elif menu == "Titles":
        st.header("🎥 Titles")

        st.subheader("All Titles")
        titles = title_service.list_all_titles()
        st.table(titles)

        st.subheader("➕ Add New Title")
        with st.form("add_title"):
            title = st.text_input("Title Name", key="add_title_name")
            t_type = st.selectbox("Type", ["movie", "show", "anime"], key="add_title_type")
            genre = st.text_input("Genre (optional)", key="add_title_genre")
            if st.form_submit_button("Add"):
                res = title_service.add_title(title, t_type, genre or None)
                st.success(res)

        st.subheader("🔎 Search Titles")
        query = st.text_input("Search keyword", key="search_query")
        if st.button("Search"):
            res = title_service.search_movies(query)
            st.table(res)

        st.subheader("✏️ Update Title")
        with st.form("update_title"):
            movie_id = st.text_input("Movie/Show ID", key="update_movie_id")
            new_title = st.text_input("New Title (optional)", key="update_title_name")
            new_type = st.text_input("New Type (movie/show/anime, optional)", key="update_type")
            new_genre = st.text_input("New Genre (optional)", key="update_genre")
            if st.form_submit_button("Update"):
                res = title_service.update_title(
                    movie_id, new_title or None, new_type or None, new_genre or None
                )
                st.success(res)

        st.subheader("❌ Delete Title")
        with st.form("delete_title"):
            movie_id = st.text_input("Movie/Show ID", key="delete_movie_id")
            if st.form_submit_button("Delete"):
                res = title_service.delete_title(movie_id)
                st.warning(res)

if st.session_state.user and st.session_state.show_main_app:
    main_app()
else:
    login_page()
