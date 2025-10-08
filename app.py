import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
from config import supabase
from services.user_service import UserService
from services.title_service import TitleService
from services.watchlist_service import WatchlistService

user_service = UserService()
title_service = TitleService()
watchlist_service = WatchlistService()


st.set_page_config(
    page_title="Watchlist Manager",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            width: 100px;
            margin-right: 10px;
            transition: all 0.3s ease;
            color: #a0a0a0;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            padding: auto auto;
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
        
        .page-header {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 40px 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .page-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), transparent);
            pointer-events: none;
        }
        
        .page-header h1 {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2, #667eea);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            position: relative;
            z-index: 1;
        }
        
        .page-header p {
            color: #a0a0a0;
            font-size: 16px;
            margin-top: 10px;
            position: relative;
            z-index: 1;
        }
        
        .sidebar-title {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border-color: rgba(102, 126, 234, 0.5);
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #a0a0a0;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
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
        
        .section-title {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin-top: 30px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    session = supabase.auth.get_session()
    if session and session.user:
        st.session_state.user = {
            "user_id": session.user.id,
            "name": session.user.user_metadata.get("name", ""),
            "email": session.user.email
        }
        st.session_state.show_main_app = True
    else:
        st.session_state.user = None
        st.session_state.show_main_app = False


def clear_session():
    st.session_state.user = None
    st.session_state.show_main_app = False
    st.rerun()


def handle_response(res, success_message="✅ Done!"):
    if isinstance(res, dict) and "error" in res:
        st.error(f"❌ {res['error']}", icon="⚠️")
    else:
        st.success(success_message, icon="✅")
        st.rerun()


def render_page_header(title, subtitle=""):
    st.markdown(f"""
        <div class="page-header">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def display_stat_card(label, value, icon=""):
    st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def display_dashboard(show_user_data=True,outer=True):
    users = user_service.list_users()
    total_users = len(users) if users else 0
    
    titles = title_service.list_all_titles()
    total_titles = len(titles) if titles else 0
    
    col1, col2 = st.columns(2)
    if(outer==True):
        with col1:
            display_stat_card("Total Users", total_users, "👥")
        with col2:
            display_stat_card("Total Titles", total_titles, "🎥")
    
    if show_user_data and st.session_state.user:
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        total_watchlist = len(watchlist) if watchlist else 0
        
        watched = len([w for w in watchlist if w.get("status") == "watched"])
        planning = len([w for w in watchlist if w.get("status") == "planning"])
        dropped = len([w for w in watchlist if w.get("status") == "dropped"])
        
        st.markdown("<h3 class='section-title'>📊 Your Watchlist Breakdown</h3>", unsafe_allow_html=True)
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            display_stat_card("Watched", watched, "✅")
        with stat_col2:
            display_stat_card("Planning", planning, "📌")
        with stat_col3:
            display_stat_card("Dropped", dropped, "❌")
        
        if total_watchlist > 0:
            st.markdown("<h3 class='section-title'>📈 Statistics Visualization</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1.2, 1])
            
            with col1:
                
                fig, ax = plt.subplots(figsize=(7, 6), facecolor='none')
                ax.set_facecolor('none')

                labels = ["Watched", "Planning", "Dropped"]
                sizes = [watched, planning, dropped]

                glow_colors = ["#5168FF", "#6B8AFF", "#9550FF"]
                transparent_colors = ["#4159D029", "#5A7FDB5A", "#7C3AED39"]  # 75% transparent

                for width, alpha in zip([4], [0.06]):
                    start_angle = 90
                    total = sum(sizes)
                    for size, glow_color in zip(sizes, glow_colors):
                        theta1 = start_angle
                        theta2 = start_angle + (size / total) * 360
                        
                        ax.pie(
                            [1],
                            radius=1,
                            startangle=theta1,
                            colors=["none"],
                            wedgeprops={
                                'edgecolor': glow_color,
                                'linewidth': width,
                                'alpha': alpha
                            }
                        )
                        start_angle = theta2

                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=transparent_colors,
                    wedgeprops={
                        'linewidth': 4,
                        'edgecolor': glow_colors[0],
                        'alpha': 0.75
                    }
                )
                for i, wedge in enumerate(wedges):
                    wedge.set_edgecolor(glow_colors[i])
                for t in texts:
                    t.set_color('#ffffff')
                    t.set_fontsize(13)
                    t.set_fontweight('bold')
                    t.set_path_effects([patheffects.withStroke(linewidth=3, foreground='#000000')])

                for autotext in autotexts:
                    autotext.set_color('#ffffff')
                    autotext.set_fontsize(12)
                    autotext.set_fontweight('bold')
                    autotext.set_path_effects([patheffects.withStroke(linewidth=2, foreground='#000000')])

                ax.axis("equal")

                st.pyplot(fig, transparent=True, use_container_width=True)
            
            with col2:
                st.markdown("""
                    <div style="padding: 20px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.3); height: 100%;">
                        <h4 style="color: #667eea; margin-top: 0;">📊 Overview</h4>
                        <div style="color: #a0a0a0; font-size: 14px; line-height: 1.8;">
                            <p><strong>Total Entries:</str  ong> """ + str(total_watchlist) + """</p>
                            <p><strong>Completion Rate:</strong> """ + f"{(watched/total_watchlist*100):.1f}%" if total_watchlist > 0 else "0%" + """</p>
                            <p><strong>In Progress:</strong> """ + str(planning) + """</p>
                            <p><strong>Not Started:</strong> """ + str(dropped) + """</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

def login_page():
    render_page_header("🎬 Watchlist Manager", "Organize your entertainment, track your progress, manage your time")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("<h3 class='section-title'>📊 Platform Overview</h3>", unsafe_allow_html=True)
        display_dashboard(show_user_data=False)
    
    with col2:
        st.markdown("<h3 class='section-title'>🔐 Authentication</h3>", unsafe_allow_html=True)
        
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
                                st.rerun()
                    else:
                        st.warning("⚠️ Please fill in all fields.")

def main_app():
    with st.sidebar:
        st.markdown("---")
        user = st.session_state.user or {}
        st.markdown("<div style='font-size:50px;'>👤</div>", unsafe_allow_html=True)
        
        st.markdown(
        f"<div class='sidebar-title'>👋 {user.get('name', 'User')}</div>",
        unsafe_allow_html=True
        )
        
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
    
    if menu == "📊 Dashboard":
        render_page_header("📊 Dashboard", "Your personalized watchlist dashboard")
        display_dashboard(outer=False)
    
    elif menu == "📋 My Watchlist":
        render_page_header("📋 My Watchlist", "Manage your collection of watched and planned titles")
        
        watchlist = watchlist_service.get_user_watchlist(st.session_state.user["user_id"])
        
        if watchlist:
            st.markdown("<h3 class='section-title'>Your Entries</h3>", unsafe_allow_html=True)
            for item in watchlist:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        title=title_service.get_title(movie_id=item.get('movie_id'))
                        x=title[0]
                        st.markdown(f"**{x['title']}**")
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
            st.markdown("<h3 class='section-title'>Add to Watchlist</h3>", unsafe_allow_html=True)
            with st.form("add_watchlist"):
                titles = title_service.list_all_titles()
                title_options = {f"{t.get('title')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                                 for t in titles if "movie_id" in t}
                
                if title_options:
                    movie_id = st.selectbox("Select a Title", list(title_options.keys()))
                    status = st.selectbox("Status", ["Watched", "Planning", "Dropped"])
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
            st.markdown("<h3 class='section-title'>Update Entry</h3>", unsafe_allow_html=True)
            if watchlist:
                title=title_service.get_title(movie_id=item.get('movie_id'))
                x=title[0]
                options = {
                    f"{w.get(x['title'])} (ID: {w.get('movie_id', '?')})": w["watchlist_id"]
                    for w in watchlist if "watchlist_id" in w
                }
                with st.form("update_watchlist"):
                    watchlist_id = st.selectbox("Select Entry to Update", options.keys())
                    new_status = st.selectbox("New Status", ["", "Watched", "Planning", "Dropped"])
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
            st.markdown("<h3 class='section-title'>Remove Entry</h3>", unsafe_allow_html=True)
            if watchlist:
                options = {
                    f"{w.get('title')} (ID: {w.get('watchlist_id', '?')})": w["watchlist_id"]
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
        render_page_header("🎥 Titles Database", "Browse and manage all titles in the system")
        
        st.markdown("<h3 class='section-title'>🔍 Search & Browse</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search titles", placeholder="Enter Movie, Show, or Anime name...", label_visibility="collapsed")
        with col2:
            search_btn = st.button("Search", use_container_width=True)
        
        if search_btn and search_query:
            res = title_service.search_movies(search_query)
            if res:
                st.markdown("<h3 class='section-title'>Search Results</h3>", unsafe_allow_html=True)
                for item in res:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{item.get('title')}**")
                            st.caption(f"Type: {item.get('type', 'N/A')} | Genre: {item.get('genre', 'N/A')}")
                        with col2:
                            st.caption(f"ID: {item.get('movie_id', '?')}")
            else:
                st.warning("⚠️ No titles found. Try another search.")
        
        st.divider()
        
        titles = title_service.list_all_titles()
        st.markdown("<h3 class='section-title'>📚 All Titles</h3>", unsafe_allow_html=True)
        
        if titles:
            for item in titles:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**{item.get('title')}**")
                    with col2:
                        st.caption(f"📺 {item.get('type', 'N/A')}")
                    with col3:
                        st.caption(f"ID: {item.get('movie_id', '?')}")
        else:
            st.info("📭 No titles available yet.")
        
        st.divider()
        
        tabs = st.tabs(["➕ Add", "✏️ Update", "❌ Delete"])
        
        with tabs[0]:
            st.markdown("<h3 class='section-title'>Add New Title</h3>", unsafe_allow_html=True)
            with st.form("add_title"):
                title = st.text_input("Title Name", placeholder="Enter title...")
                t_type = st.selectbox("Type", ["Movie", "Show", "Anime"])
                genre = st.text_input("Genre (optional)", placeholder="e.g., Action, Drama, Comedy...")
                
                if st.form_submit_button("➕ Add Title", use_container_width=True):
                    if title:
                        res = title_service.add_title(title, t_type, genre or None)
                        handle_response(res, "✅ Title added successfully!")
                    else:
                        st.warning("⚠️ Please enter a title name.")
        
        with tabs[1]:
            st.markdown("<h3 class='section-title'>Update Title</h3>", unsafe_allow_html=True)
            if titles:
                options = {f"{t.get('title')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("update_title"):
                    movie_id = st.selectbox("Select Title to Update", options.keys())
                    new_title = st.text_input("New Title (optional)")
                    new_type = st.selectbox("New Type (optional)", ["", "Movie", "Show", "Anime"])
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
            st.markdown("<h3 class='section-title'>Delete Title</h3>", unsafe_allow_html=True)
            if titles:
                options = {f"{t.get('title')} (ID: {t.get('movie_id', '?')})": t["movie_id"]
                           for t in titles if "movie_id" in t}
                with st.form("delete_title"):
                    movie_id = st.selectbox("Select Title to Delete", options.keys())
                    
                    st.warning("⚠️ This action cannot be undone.")
                    
                    if st.form_submit_button("❌ Delete Title", use_container_width=True, type="secondary"):
                        res = title_service.delete_title(options[movie_id])
                        handle_response(res, "✅ Title deleted!")
            else:
                st.info("📭 No titles to delete.")

if st.session_state.user and st.session_state.show_main_app:
    main_app()
else:
    login_page()