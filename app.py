import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json, os
from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()

SESSION_FILE = "session.json"

if os.path.exists(SESSION_FILE) and "user" not in st.session_state:
    with open(SESSION_FILE, "r") as f:
        st.session_state.user = json.load(f)
        st.session_state.show_main_app = True

if "user" not in st.session_state:
    st.session_state.user = None
if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False

def save_session(user):
    with open(SESSION_FILE, "w") as f:
        json.dump(user, f)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    st.session_state.user = None
    st.session_state.show_main_app = False

def handle_response(res, success_message="✅ Done!"):
    if isinstance(res, dict) and "error" in res:
        st.error(res["error"])
    else:
        st.success(success_message)
        st.rerun()

def dashboard(show_user_data=True, outer=True):
    st.header("📊 Dashboard Overview")

    users = user_service.list_users()
    total_users = len(users) if users else 0

    titles = title_service.list_all_titles()
    total_titles = len(titles) if titles else 0

    total_watchlist, watched, planning, dropped = 0, 0, 0, 0

    if show_user_data and st.session_state.user:
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        total_watchlist = len(watchlist) if watchlist else 0
        watched = len([w for w in watchlist if w.get("status") == "watched"])
        planning = len([w for w in watchlist if w.get("status") == "planning"])
        dropped = len([w for w in watchlist if w.get("status") == "dropped"])

    if outer:
        col1, col2 = st.columns(2)
        col1.metric("👥 Total Users", total_users)
        col2.metric("🎥 Total Titles", total_titles)

    if show_user_data and st.session_state.user:
        st.subheader("📺 My Watchlist Breakdown")
        c1, c2, c3 = st.columns(3)
        c1.metric("✅ Watched", watched)
        c2.metric("📌 Planning", planning)
        c3.metric("❌ Dropped", dropped)

        if total_watchlist > 0:
            labels = ["Watched", "Planning", "Dropped"]
            sizes = [watched, planning, dropped]
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)

def login_page():
    st.markdown("<h1 style='text-align: center;'>🎬 Watchlist Manager</h1>", unsafe_allow_html=True)
    left, right = st.columns([2, 1])

    with left:
        dashboard(show_user_data=False, outer=True)

    with right:
        st.subheader("🔐 Login / Register")
        choice = st.radio("Choose", ["Login", "Register"])

        if choice == "Login":
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                user = user_service.authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.show_main_app = True
                    save_session(user)
                    st.success(f"Welcome {user['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif choice == "Register":
            name = st.text_input("Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            if st.button("Register"):
                res = user_service.register_user(name, email, password)
                if isinstance(res, dict) and "error" in res:
                    st.error(res["error"])
                else:
                    st.success("✅ Account created! Logging you in...")
                    st.session_state.user = res
                    st.session_state.show_main_app = True
                    save_session(res)
                    st.rerun()

def main_app():
    st.sidebar.image("default.png", width=80)
    st.sidebar.title(f"👋 Hello, {st.session_state.user['name']}")
    if st.sidebar.button("Logout"):
        clear_session()
        st.rerun()

    menu = st.sidebar.radio("Menu", ["Dashboard", "My Watchlist", "Titles"])

    if menu == "Dashboard":
        dashboard(outer=False)

    elif menu == "My Watchlist":
        st.header("📺 My Watchlist")
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])

        if watchlist:
            st.dataframe(pd.DataFrame(watchlist))
        else:
            st.info("Your watchlist is empty. Add something!")

        tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Remove"])

        with tabs[0]:
            with st.form("add_watchlist"):
                titles = title_service.list_all_titles()
                title_options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                                 for t in titles if "movie_id" in t}

                movie_id = st.selectbox("Select Title", list(title_options.keys()))
                status = st.selectbox("Status", ["watched", "planning", "dropped"], key="add_status")
                rating = st.number_input("Rating (1-10)", min_value=1, max_value=10, step=1, key="add_rating")
                review = st.text_area("Review (optional)", key="add_review")
                if st.form_submit_button("Add"):
                    res = watchlist_service.add_to_watchlist(
                        st.session_state.user["user_id"], title_options[movie_id], status, rating, review or None
                    )
                    handle_response(res, "✅ Added successfully!")

        with tabs[1]:
            if watchlist:
                options = {
                    f"{w.get('title', 'Untitled')} (ID: {w.get('watchlist_id', '?')})": w["watchlist_id"]
                    for w in watchlist if "watchlist_id" in w
                }
                with st.form("update_watchlist"):
                    watchlist_id = st.selectbox("Select Entry", options.keys())
                    new_status = st.selectbox("New Status", ["", "watched", "planning", "dropped"])
                    new_rating = st.number_input("New Rating (leave 0 if unchanged)", min_value=0, max_value=10, step=1)
                    new_review = st.text_area("New Review (optional)")
                    if st.form_submit_button("Update"):
                        res = watchlist_service.update_watchlist_entry(
                            options[watchlist_id],
                            new_status if new_status else None,
                            new_rating if new_rating > 0 else None,
                            new_review or None,
                        )
                        handle_response(res, "✅ Updated successfully!")

        with tabs[2]:
            if watchlist:
                options = {
                    f"{w.get('title', 'Untitled')} (ID: {w.get('watchlist_id', '?')})": w["watchlist_id"]
                    for w in watchlist if "watchlist_id" in w
                }
                with st.form("remove_watchlist"):
                    watchlist_id = st.selectbox("Select Entry to Remove", options.keys())
                    if st.form_submit_button("Remove"):
                        res = watchlist_service.remove_from_watchlist(options[watchlist_id])
                        handle_response(res, "❌ Removed successfully!")

    elif menu == "Titles":
        st.header("🎥 Titles")

        st.subheader("🔎 Search Titles")
        query = st.text_input("Search keyword")
        if query and st.button("Search"):
            res = title_service.search_movies(query)
            if res:
                st.dataframe(pd.DataFrame(res))
            else:
                st.info("No results found.")

        titles = title_service.list_all_titles()
        st.subheader("All Titles")
        if titles:
            st.dataframe(pd.DataFrame(titles))
        else:
            st.info("No titles available.")

        tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Delete"])

        with tabs[0]:
            with st.form("add_title"):
                title = st.text_input("Title Name")
                t_type = st.selectbox("Type", ["movie", "show", "anime"])
                genre = st.text_input("Genre (optional)")
                if st.form_submit_button("Add"):
                    res = title_service.add_title(title, t_type, genre or None)
                    handle_response(res, "✅ Added successfully!")

        with tabs[1]:
            if titles:
                options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("update_title"):
                    movie_id = st.selectbox("Select Title", options.keys())
                    new_title = st.text_input("New Title (optional)")
                    new_type = st.selectbox("New Type (optional)", ["", "movie", "show", "anime"])
                    new_genre = st.text_input("New Genre (optional)")
                    if st.form_submit_button("Update"):
                        res = title_service.update_title(
                            options[movie_id],
                            new_title or None,
                            new_type or None,
                            new_genre or None,
                        )
                        handle_response(res, "✅ Updated successfully!")

        with tabs[2]:
            if titles:
                options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("delete_title"):
                    movie_id = st.selectbox("Select Title to Delete", options.keys())
                    if st.form_submit_button("Delete"):
                        res = title_service.delete_title(options[movie_id])
                        handle_response(res, "❌ Deleted successfully!")


if st.session_state.user and st.session_state.show_main_app:
    main_app()
else:
    login_page()
