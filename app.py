import streamlit as st
from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

# Initialize services
user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()

st.set_page_config(page_title="🎬 Watchlist Manager", layout="wide")
st.title("🎬 Watchlist Manager")

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigate",
    ["Users", "Titles", "Watchlist"]
)

# ------------------ USERS ------------------
if menu == "Users":
    st.header("👤 User Management")
    tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Delete", "📋 List", "🔎 Get by ID"])

    # Add User
    with tabs[0]:
        with st.form("add_user"):
            name = st.text_input("Name", key="add_user_name")
            email = st.text_input("Email", key="add_user_email")
            if st.form_submit_button("Add User"):
                res = user_service.create_user(name, email)
                st.success(res)

    # Update User
    with tabs[1]:
        with st.form("update_user"):
            user_id = st.text_input("User ID", key="update_user_id")  
            name = st.text_input("New Name (optional)", key="update_user_name")
            email = st.text_input("New Email (optional)", key="update_user_email")
            if st.form_submit_button("Update"):
                res = user_service.update_user(user_id, name or None, email or None)
                st.success(res)

    # Delete User
    with tabs[2]:
        with st.form("delete_user"):
            user_id = st.text_input("User ID", key="delete_user_id")  
            if st.form_submit_button("Delete"):
                res = user_service.delete_user(user_id)
                st.warning(res)

    # List Users
    with tabs[3]:
        if st.button("Refresh Users"):
            pass
        st.table(user_service.list_users())

    # Get User by ID
    with tabs[4]:
        user_id = st.text_input("Enter User ID", key="get_user_by_id")  
        if st.button("Fetch User"):
            st.write(user_service.get_user(user_id))


# ------------------ TITLES ------------------
elif menu == "Titles":
    st.header("🎥 Title Management")
    tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Delete", "📋 List", "🔎 Search"])

    # Add Title
    with tabs[0]:
        with st.form("add_title"):
            title = st.text_input("Title Name", key="add_title_name")
            t_type = st.selectbox("Type", ["movie", "show", "anime"], key="add_title_type")
            genre = st.text_input("Genre (optional)", key="add_title_genre")
            if st.form_submit_button("Add"):
                res = title_service.add_title(title, t_type, genre or None)
                st.success(res)

    # Update Title
    with tabs[1]:
        with st.form("update_title"):
            movie_id = st.text_input("Movie/Show ID", key="update_title_id")  
            new_title = st.text_input("New Title (optional)", key="update_title_name")
            new_type = st.text_input("New Type (movie/show/anime, optional)", key="update_title_type")
            if st.form_submit_button("Update"):
                res = title_service.update_title(movie_id, new_title or None, new_type or None)
                st.success(res)

    # Delete Title
    with tabs[2]:
        with st.form("delete_title"):
            movie_id = st.text_input("Movie/Show ID", key="delete_title_id")  
            if st.form_submit_button("Delete"):
                res = title_service.delete_title(movie_id)
                st.warning(res)

    # List Titles
    with tabs[3]:
        if st.button("Refresh Titles"):
            pass
        st.table(title_service.list_all_titles())

    # Search Titles
    with tabs[4]:
        query = st.text_input("Search keyword", key="search_titles")
        if st.button("Search"):
            res = title_service.search_titles(query)
            st.table(res)


# ------------------ WATCHLIST ------------------
elif menu == "Watchlist":
    st.header("📺 Watchlist Management")
    tabs = st.tabs([
        "➕ Add", "✏️ Update", "❌ Remove",
        "📋 User Watchlist", "🔎 Filter by Status"
    ])

    # Add to Watchlist
    with tabs[0]:
        with st.form("add_watchlist"):
            user_id = st.text_input("User ID", key="add_watchlist_user_id")  
            movie_id = st.text_input("Movie/Show ID", key="add_watchlist_movie_id")  
            status = st.selectbox("Status", ["watched", "planning", "dropped"], key="add_watchlist_status")
            rating = st.number_input("Rating (1-10)", min_value=1, max_value=10, step=1, value=5, key="add_watchlist_rating")
            review = st.text_area("Review (optional)", key="add_watchlist_review")
            if st.form_submit_button("Add"):
                res = watchlist_service.add_to_watchlist(user_id, movie_id, status, rating, review or None)
                st.success(res)

    # Update Watchlist
    with tabs[1]:
        with st.form("update_watchlist"):
            watchlist_id = st.text_input("Watchlist ID", key="update_watchlist_id")
            status = st.text_input("New Status (optional)", key="update_watchlist_status")
            rating = st.text_input("New Rating (optional)", key="update_watchlist_rating")
            review = st.text_area("New Review (optional)", key="update_watchlist_review")
            if st.form_submit_button("Update"):
                res = watchlist_service.update_watchlist_entry(
                    watchlist_id,
                    status or None,
                    int(rating) if rating else None,
                    review or None,
                )
                st.success(res)

    # Remove from Watchlist
    with tabs[2]:
        with st.form("delete_watchlist"):
            watchlist_id = st.text_input("Watchlist ID", key="delete_watchlist_id")
            if st.form_submit_button("Remove"):
                res = watchlist_service.remove_from_watchlist(watchlist_id)
                st.warning(res)

    # Get User Watchlist
    with tabs[3]:
        user_id = st.text_input("User ID", key="get_watchlist_user_id")
        if st.button("Show Watchlist"):
            res = watchlist_service.get_user_watchlist(user_id)
            st.table(res)

    # Filter Watchlist by Status
    with tabs[4]:
        user_id = st.text_input("User ID", key="filter_watchlist_user_id")
        status = st.selectbox("Status", ["watched", "planning", "dropped"], key="filter_watchlist_status")
        if st.button("Filter"):
            res = watchlist_service.get_user_watchlist_by_status(user_id, status)
            st.table(res)
