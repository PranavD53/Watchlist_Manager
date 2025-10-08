import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json, os
from datetime import datetime
from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

# Initialize services
user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()

SESSION_FILE = "session.json"

# Page config
st.set_page_config(
    page_title="Watchlist Manager",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
        }
        
        .main {
            background: rgba(15, 12, 41, 0.9);
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            margin-right: 5px;
            transition: all 0.3s ease;
            color: #a0a0a0;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .metric-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .stButton button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 14px;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
            border-radius: 8px;
        }
        
        .header-container {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 15px;
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .sidebar-title {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        
        .watchlist-item {
            background: rgba(255, 255, 255, 0.05);
            border-left: 4px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        
        .watchlist-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-watched {
            background: rgba(34, 139, 34, 0.3);
            color: #90ee90;
            border: 1px solid rgba(34, 139, 34, 0.6);
        }
        
        .status-planning {
            background: rgba(65, 105, 225, 0.3);
            color: #87ceeb;
            border: 1px solid rgba(65, 105, 225, 0.6);
        }
        
        .status-dropped {
            background: rgba(220, 20, 60, 0.3);
            color: #ff6b6b;
            border: 1px solid rgba(220, 20, 60, 0.6);
        }
        
        .rating-display {
            font-size: 18px;
            font-weight: 700;
            color: #ffd700;
            letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)

# Session management
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
        st.error(f"❌ {res['error']}", icon="⚠️")
    else:
        st.success(success_message, icon="✅")
        st.rerun()

def display_dashboard(show_user_data=True, outer=True):
    col1, col2 = st.columns(2)
    
    users = user_service.list_users()
    total_users = len(users) if users else 0
    
    titles = title_service.list_all_titles()
    total_titles = len(titles) if titles else 0

    if outer==True:
        with col1:
            st.metric("👥 Total Users", total_users, delta=None)
        with col2:
            st.metric("🎥 Total Titles", total_titles, delta=None)
        
    if show_user_data and st.session_state.user:
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        total_watchlist = len(watchlist) if watchlist else 0
        watched = len([w for w in watchlist if w.get("status") == "watched"])
        planning = len([w for w in watchlist if w.get("status") == "planning"])
        dropped = len([w for w in watchlist if w.get("status") == "dropped"])
        
        st.divider()
        st.subheader("📊 Your Watchlist Statistics")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("✅ Watched", watched)
        with stat_col2:
            st.metric("📌 Planning", planning)
        with stat_col3:
            st.metric("❌ Dropped", dropped)
        
        # Pie chart
        if total_watchlist > 0:
            fig, ax = plt.subplots(figsize=(6, 5), facecolor='none')
            ax.set_facecolor('none')
            
            labels = ["Watched", "Planning", "Dropped"]
            sizes = [watched, planning, dropped]
            colors = ["#6a0dad", "#1e3c72", "#8a2be2"]
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
                wedgeprops={'edgecolor': "#161313", 'linewidth': 2}
            )
            
            for t in texts + autotexts:
                t.set_color('white')
                t.set_fontsize(11)
                t.set_fontweight('bold')
            
            ax.axis("equal")
            st.pyplot(fig, transparent=True, use_container_width=True)

def login_page():
    st.markdown("""
        <div class="header-container">
            <h1>🎬 Watchlist Manager</h1>
            <p style="color: #a0a0a0; font-size: 16px; margin-top: 10px;">
                Organize your entertainment, track your progress, manage your time
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("📊 Platform Overview")
        display_dashboard(show_user_data=False, outer=True)
    
    with col2:
        st.markdown("### 🔐 Authentication")
        
        choice = st.radio("Choose an action", ["Login", "Register"], horizontal=True, label_visibility="collapsed")
        
        st.divider()
        
        if choice == "Login":
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="your@email.com")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    if email and password:
                        user = user_service.authenticate_user(email, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.show_main_app = True
                            save_session(user)
                            st.success(f"👋 Welcome back, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password. Please try again.")
                    else:
                        st.warning("⚠️ Please fill in all fields.")
        
        elif choice == "Register":
            with st.form("register_form"):
                name = st.text_input("👤 Full Name", placeholder="Your name")
                email = st.text_input("📧 Email", placeholder="your@email.com")
                password = st.text_input("🔑 Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Confirm your password")
                submit = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if submit:
                    if name and email and password and confirm_password:
                        if password != confirm_password:
                            st.error("❌ Passwords don't match.")
                        else:
                            res = user_service.register_user(name, email, password)
                            if isinstance(res, dict) and "error" in res:
                                st.error(f"❌ {res['error']}")
                            else:
                                st.success("✅ Account created! Logging you in...")
                                st.session_state.user = res
                                st.session_state.show_main_app = True
                                save_session(res)
                                st.rerun()
                    else:
                        st.warning("⚠️ Please fill in all fields.")

def main_app():
    # Sidebar
    with st.sidebar:
        st.markdown("---")
        if st.session_state.user.get("default.png"):
            st.image(st.session_state.user["default.png"], width=100)
        
        st.markdown(f"<div class='sidebar-title'>👋 {st.session_state.user['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #a0a0a0; font-size: 13px;'>{st.session_state.user.get('email', 'User')}</p>", unsafe_allow_html=True)
        
        st.divider()
        
        menu = st.radio(
            "Navigation",
            ["📊 Dashboard", "📋 My Watchlist", "🎥 Titles"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            clear_session()
            st.rerun()
    
    # Main content
    if menu == "📊 Dashboard":
        st.markdown("<div class='header-container'><h2>📊 Dashboard</h2></div>", unsafe_allow_html=True)
        display_dashboard(outer=False)
    
    elif menu == "📋 My Watchlist":
        st.markdown("<div class='header-container'><h2>📋 My Watchlist</h2></div>", unsafe_allow_html=True)
        
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        
        if watchlist:
            st.subheader("Your Entries")
            for item in watchlist:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{item.get('title', 'Untitled')}**")
                    with col2:
                        status = item.get("status", "").lower()
                        status_class = f"status-{status}"
                        st.markdown(f"<span class='status-badge {status_class}'>{status}</span>", unsafe_allow_html=True)
                    with col3:
                        if item.get("rating"):
                            st.markdown(f"<div class='rating-display'>⭐ {item['rating']}/10</div>", unsafe_allow_html=True)
                    with col4:
                        st.caption(f"ID: {item.get('watchlist_id', '?')}")
        else:
            st.info("📭 Your watchlist is empty. Add something to get started!")
        
        st.divider()
        
        tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Remove"])
        
        with tabs[0]:
            st.subheader("Add to Watchlist")
            with st.form("add_watchlist"):
                titles = title_service.list_all_titles()
                title_options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                                 for t in titles if "movie_id" in t}
                
                if title_options:
                    movie_id = st.selectbox("Select a Title", list(title_options.keys()))
                    status = st.selectbox("Status", ["watched", "planning", "dropped"])
                    rating = st.slider("Rating", 1, 10, 5)
                    review = st.text_area("Review (optional)", placeholder="Share your thoughts...")
                    
                    if st.form_submit_button("➕ Add to Watchlist", use_container_width=True):
                        res = watchlist_service.add_to_watchlist(
                            st.session_state.user["user_id"], title_options[movie_id], status, rating, review or None
                        )
                        handle_response(res, "✅ Added to watchlist!")
                else:
                    st.warning("⚠️ No titles available. Please add titles first.")
        
        with tabs[1]:
            st.subheader("Update Entry")
            if watchlist:
                options = {
                    f"{w.get('title', 'Untitled')} (ID: {w.get('watchlist_id', '?')})": w["watchlist_id"]
                    for w in watchlist if "watchlist_id" in w
                }
                with st.form("update_watchlist"):
                    watchlist_id = st.selectbox("Select Entry to Update", options.keys())
                    new_status = st.selectbox("New Status", ["", "watched", "planning", "dropped"])
                    new_rating = st.slider("New Rating", 0, 10, 0)
                    new_review = st.text_area("New Review (optional)")
                    
                    if st.form_submit_button("✏️ Update Entry", use_container_width=True):
                        res = watchlist_service.update_watchlist_entry(
                            options[watchlist_id],
                            new_status if new_status else None,
                            new_rating if new_rating > 0 else None,
                            new_review or None,
                        )
                        handle_response(res, "✅ Updated successfully!")
            else:
                st.info("📭 Your watchlist is empty.")
        
        with tabs[2]:
            st.subheader("Remove Entry")
            if watchlist:
                options = {
                    f"{w.get('title', 'Untitled')} (ID: {w.get('watchlist_id', '?')})": w["watchlist_id"]
                    for w in watchlist if "watchlist_id" in w
                }
                with st.form("remove_watchlist"):
                    watchlist_id = st.selectbox("Select Entry to Remove", options.keys())
                    
                    if st.form_submit_button("❌ Remove Entry", use_container_width=True, type="secondary"):
                        res = watchlist_service.remove_from_watchlist(options[watchlist_id])
                        handle_response(res, "✅ Removed from watchlist!")
            else:
                st.info("📭 Your watchlist is empty.")
    
    elif menu == "🎥 Titles":
        st.markdown("<div class='header-container'><h2>🎥 Titles Database</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search titles", placeholder="Enter movie, show, or anime name...")
        with col2:
            search_btn = st.button("Search", use_container_width=True)
        
        if search_btn and search_query:
            res = title_service.search_movies(search_query)
            if res:
                st.subheader("Search Results")
                for item in res:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{item.get('title', 'Untitled')}**")
                            st.caption(f"Type: {item.get('type', 'N/A')} | Genre: {item.get('genre', 'N/A')}")
                        with col2:
                            st.caption(f"ID: {item.get('movie_id', '?')}")
            else:
                st.warning("⚠️ No titles found. Try another search.")
        
        st.divider()
        
        titles = title_service.list_all_titles()
        st.subheader(f"All Titles ({len(titles) if titles else 0})")
        
        if titles:
            for item in titles:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**{item.get('title', 'Untitled')}**")
                    with col2:
                        st.caption(f"📺 {item.get('type', 'N/A')}")
                    with col3:
                        st.caption(f"ID: {item.get('movie_id', '?')}")
        else:
            st.info("📭 No titles available yet.")
        
        st.divider()
        
        tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Delete"])
        
        with tabs[0]:
            st.subheader("Add New Title")
            with st.form("add_title"):
                title = st.text_input("Title Name", placeholder="Enter title...")
                t_type = st.selectbox("Type", ["movie", "show", "anime"])
                genre = st.text_input("Genre (optional)", placeholder="e.g., Action, Drama, Comedy...")
                
                if st.form_submit_button("➕ Add Title", use_container_width=True):
                    if title:
                        res = title_service.add_title(title, t_type, genre or None)
                        handle_response(res, "✅ Title added successfully!")
                    else:
                        st.warning("⚠️ Please enter a title name.")
        
        with tabs[1]:
            st.subheader("Update Title")
            if titles:
                options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("update_title"):
                    movie_id = st.selectbox("Select Title to Update", options.keys())
                    new_title = st.text_input("New Title (optional)")
                    new_type = st.selectbox("New Type (optional)", ["", "movie", "show", "anime"])
                    new_genre = st.text_input("New Genre (optional)")
                    
                    if st.form_submit_button("✏️ Update Title", use_container_width=True):
                        res = title_service.update_title(
                            options[movie_id],
                            new_title or None,
                            new_type or None,
                            new_genre or None,
                        )
                        handle_response(res, "✅ Title updated!")
            else:
                st.info("📭 No titles to update.")
        
        with tabs[2]:
            st.subheader("Delete Title")
            if titles:
                options = {f"{t.get('title', 'Untitled')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("delete_title"):
                    movie_id = st.selectbox("Select Title to Delete", options.keys())
                    
                    st.warning("⚠️ This action cannot be undone.")
                    
                    if st.form_submit_button("❌ Delete Title", use_container_width=True, type="secondary"):
                        res = title_service.delete_title(options[movie_id])
                        handle_response(res, "✅ Title deleted!")
            else:
                st.info("📭 No titles to delete.")

# Route to appropriate page
if st.session_state.user and st.session_state.show_main_app:
    main_app()
else:
    login_page()