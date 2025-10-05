import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

# ---- Initialize services ----
user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()

# ---- Session state ----
if "user" not in st.session_state:
    st.session_state.user = None
if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False


# ---- Helper ----
def handle_response(res):
    """Standardized response handling"""
    if isinstance(res, dict) and "error" in res:
        st.error(res["error"])
    else:
        st.success(res if isinstance(res, str) else "✅ Done!")


# ---- Dashboard ----
def dashboard(show_user_data=True):
    st.header("📊 Dashboard Overview")

    # Fetch data
    users = user_service.list_users()
    total_users = len(users) if users else 0

    titles = title_service.list_all_titles()
    total_titles = len(titles) if titles else 0

    watchlist = []
    total_watchlist, watched, planning, dropped = 0, 0, 0, 0

    if show_user_data and st.session_state.user:
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        total_watchlist = len(watchlist) if watchlist else 0
        watched = len([w for w in watchlist if w.get("status") == "watched"])
        planning = len([w for w in watchlist if w.get("status") == "planning"])
        dropped = len([w for w in watchlist if w.get("status") == "dropped"])

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Users", total_users)
    col2.metric("🎥 Total Titles", total_titles)
    col3.metric("📺 My Watchlist", total_watchlist)

    if show_user_data and st.session_state.user:
        # Watchlist breakdown
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


# ---- Login/Register Page ----
def login_page():
    st.markdown("<h1 style='text-align: center;'>🎬 Watchlist Manager</h1>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])  # left = dashboard, right = login/register

    # Left → Dashboard (no user-specific watchlist yet)
    with left:
        dashboard(show_user_data=False)

    # Right → Login/Register
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
                    st.rerun()


# ---- Main App ----
def main_app():
    st.sidebar.title(f"👋 Hello, {st.session_state.user['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.show_main_app = False
        st.rerun()

    menu = st.sidebar.radio("Menu", ["Dashboard", "My Watchlist", "Titles"])

    # ---------------- Dashboard ----------------
    if menu == "Dashboard":
        dashboard()

    # ---------------- Watchlist ----------------
    elif menu == "My Watchlist":
        st.header("📺 My Watchlist")
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])

        if watchlist:
            st.dataframe(pd.DataFrame(watchlist))
        else:
            st.info("Your watchlist is empty. Add something!")

        tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Remove"])

        # Add
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
                    handle_response(res)

        # Update
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
                        handle_response(res)

        # Remove
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
                        st.warning(res)

    # ---------------- Titles ----------------
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

        # Add
        with tabs[0]:
            with st.form("add_title"):
                title = st.text_input("Title Name")
                t_type = st.selectbox("Type", ["movie", "show", "anime"])
                genre = st.text_input("Genre (optional)")
                if st.form_submit_button("Add"):
                    res = title_service.add_title(title, t_type, genre or None)
                    handle_response(res)

        # Update
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
                        handle_response(res)

        # Delete
        with tabs[2]:
            if titles:
                options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("delete_title"):
                    movie_id = st.selectbox("Select Title to Delete", options.keys())
                    if st.form_submit_button("Delete"):
                        res = title_service.delete_title(options[movie_id])
                        st.warning(res)


# ---- Run App ----
if st.session_state.user and st.session_state.show_main_app:
    main_app()
else:
    login_page()
