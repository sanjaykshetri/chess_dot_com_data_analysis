#!/usr/bin/env python3
"""
Chess.com Analytics Dashboard
Interactive web dashboard for analyzing chess.com game data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

from chess_data_fetcher import ChessDataFetcher
from chess_data_analyzer import ChessDataAnalyzer


# Page configuration
st.set_page_config(
    page_title="Chess.com Analytics Dashboard",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1e88e5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">♟️ Chess.com Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyze your chess.com performance with AI-powered insights</div>', unsafe_allow_html=True)
    
    # Sidebar for user input
    with st.sidebar:
        st.header("⚙️ Settings")
        
        username = st.text_input(
            "Enter Chess.com Username",
            placeholder="e.g., sanjaykshetri123",
            help="Your chess.com username (case-insensitive)"
        )
        
        max_months = st.slider(
            "Months of data to fetch",
            min_value=1,
            max_value=60,
            value=12,
            help="Fetch recent N months of game data. More months = longer load time."
        )
        
        timezone = st.selectbox(
            "Your Timezone",
            ["America/New_York", "America/Los_Angeles", "America/Chicago", 
             "Europe/London", "Europe/Paris", "Asia/Kolkata", "Asia/Tokyo",
             "Australia/Sydney"],
            help="Used for time-based analysis"
        )
        
        analyze_button = st.button("🔍 Analyze My Games", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This dashboard fetches your chess.com game history and provides:
        - 📊 Performance statistics
        - 📈 Rating progression
        - 🎯 Opening analysis
        - ⏰ Best playing times
        - 💡 Improvement suggestions
        """)
        
        st.markdown("---")
        st.markdown("**Developed by Sanjay Kshetri**")
        st.markdown("[GitHub Repository](https://github.com/sanjaykshetri/chess_dot_com_data_analysis)")
    
    # Main content area
    if not analyze_button:
        # Welcome screen
        st.info("👈 Enter your chess.com username in the sidebar and click 'Analyze My Games' to get started!")
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Comprehensive Stats")
            st.write("Track your wins, losses, draws, and rating progression over time.")
        
        with col2:
            st.markdown("### 🎯 Opening Analysis")
            st.write("Discover your strongest and weakest openings to focus your study.")
        
        with col3:
            st.markdown("### 💡 AI Insights")
            st.write("Get personalized recommendations to improve your chess game.")
        
        st.markdown("---")
        st.markdown("### 🎮 Example Analysis Preview")
        st.image("https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/PedroPinhata/phpmeXx6V.png", 
                 caption="Sample chess analytics visualization")
        
    else:
        if not username:
            st.error("❌ Please enter a chess.com username!")
            return
        
        # Start analysis
        with st.spinner(f"🔍 Validating user '{username}'..."):
            fetcher = ChessDataFetcher(username)
            is_valid, user_data = fetcher.validate_user()
        
        if not is_valid:
            st.error(f"❌ User '{username}' not found on chess.com. Please check the username and try again.")
            return
        
        # Show user info
        st.success(f"✅ Found user: **{username}**")
        
        if user_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Member Since", datetime.fromtimestamp(user_data.get('joined', 0)).strftime('%Y-%m-%d'))
            with col2:
                st.metric("Status", user_data.get('status', 'Unknown'))
            with col3:
                followers = user_data.get('followers', 0)
                st.metric("Followers", f"{followers:,}")
        
        # Fetch games
        st.markdown("---")
        st.subheader("📥 Fetching Game Data")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(current, total):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"Fetching games... {current}/{total} months complete")
        
        with st.spinner("Downloading your game history..."):
            df = fetcher.fetch_all_games(max_months=max_months, progress_callback=update_progress)
        
        progress_bar.empty()
        status_text.empty()
        
        if df.empty:
            st.warning("⚠️ No games found for this user. Make sure you have played games on chess.com!")
            return
        
        st.success(f"✅ Successfully fetched **{len(df):,}** games!")
        
        # Initialize analyzer
        analyzer = ChessDataAnalyzer(df, timezone=timezone)
        
        # Display analysis
        display_analysis(analyzer, df, username)


def display_analysis(analyzer: ChessDataAnalyzer, df: pd.DataFrame, username: str):
    """Display comprehensive analysis results"""
    
    st.markdown("---")
    st.header("📊 Performance Analysis")
    
    # Overview Statistics
    st.subheader("📈 Overview Statistics")
    stats = analyzer.get_overview_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Games", f"{stats['total_games']:,}")
    with col2:
        st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
    with col3:
        st.metric("Wins", stats['wins'], delta=None)
    with col4:
        st.metric("Draws", stats['draws'])
    with col5:
        st.metric("Losses", stats['losses'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if stats.get('current_rating'):
            st.metric("Current Rating", stats['current_rating'])
    with col2:
        if stats.get('rating_change'):
            st.metric("Rating Change", stats['rating_change'], delta=stats['rating_change'])
    with col3:
        st.metric("Days Playing", f"{stats['days_playing']:,}")
    with col4:
        st.metric("Avg Games/Day", f"{stats['avg_games_per_day']:.1f}")
    
    # Time spent
    time_stats = analyzer.calculate_total_time_spent()
    if time_stats:
        st.info(f"⏱️ **Estimated Total Time Playing**: {time_stats['total_hours']:.1f} hours ({time_stats['total_days']:.2f} days)")
    
    # Rating Progression Chart
    st.markdown("---")
    st.subheader("📈 Rating Progression")
    
    rating_data = analyzer.get_rating_progression()
    if not rating_data.empty:
        fig = px.line(
            rating_data,
            x='game_number',
            y='user_rating',
            title=f"{username}'s Rating Over Time",
            labels={'game_number': 'Game Number', 'user_rating': 'Rating'},
            template='plotly_white'
        )
        fig.update_traces(line_color='#1e88e5', line_width=2)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Rating progression data not available")
    
    # Performance by Color and Time Class
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Performance by Color")
        color_perf = analyzer.get_performance_by_color()
        if not color_perf.empty:
            fig = px.bar(
                color_perf,
                x='user_color',
                y='win_rate',
                title='Win Rate by Color',
                labels={'user_color': 'Color', 'win_rate': 'Win Rate (%)'},
                text='win_rate',
                color='win_rate',
                color_continuous_scale='RdYlGn',
                template='plotly_white'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show table
            st.dataframe(color_perf, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("⏱️ Performance by Time Class")
        time_perf = analyzer.get_performance_by_time_class()
        if not time_perf.empty:
            fig = px.bar(
                time_perf,
                x='time_class',
                y='score_pct',
                title='Score by Time Class',
                labels={'time_class': 'Time Class', 'score_pct': 'Score (%)'},
                text='score_pct',
                color='score_pct',
                color_continuous_scale='Viridis',
                template='plotly_white'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show table
            st.dataframe(time_perf, use_container_width=True, hide_index=True)
    
    # Performance by Time of Day
    st.markdown("---")
    st.subheader("⏰ Performance by Hour of Day")
    
    hour_perf = analyzer.get_performance_by_hour()
    if not hour_perf.empty:
        fig = px.line(
            hour_perf,
            x='hour',
            y='score_pct',
            title='Performance Throughout the Day',
            labels={'hour': 'Hour of Day', 'score_pct': 'Score (%)'},
            markers=True,
            template='plotly_white'
        )
        fig.update_traces(line_color='#ff6b6b', line_width=3, marker=dict(size=8))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Find best hours
        best_hours = hour_perf.nlargest(3, 'score_pct')
        st.info(f"🌟 **Your best performing hours**: {', '.join([f'{int(h)}:00' for h in best_hours['hour'].values])}")
    
    # Performance by Day of Week
    st.markdown("---")
    st.subheader("📅 Performance by Day of Week")
    
    dow_perf = analyzer.get_performance_by_day_of_week()
    if not dow_perf.empty:
        fig = px.bar(
            dow_perf,
            x='day_of_week',
            y='score_pct',
            title='Performance by Day',
            labels={'day_of_week': 'Day', 'score_pct': 'Score (%)'},
            text='score_pct',
            color='score_pct',
            color_continuous_scale='Blues',
            template='plotly_white'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Opening Analysis
    st.markdown("---")
    st.subheader("♟️ Opening Analysis")
    
    strengths, weaknesses = analyzer.get_opening_analysis()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💪 Your Strongest Openings")
        if not strengths.empty:
            st.dataframe(
                strengths[['eco', 'opening_name', 'games', 'score_pct']].head(5),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Play more games with each opening to see your strengths!")
    
    with col2:
        st.markdown("### 📚 Openings to Study")
        if not weaknesses.empty:
            st.dataframe(
                weaknesses[['eco', 'opening_name', 'games', 'score_pct']].head(5),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Play more games with each opening to identify weaknesses!")
    
    # Monthly Activity
    st.markdown("---")
    st.subheader("📊 Monthly Activity")
    
    monthly = analyzer.get_monthly_activity()
    if not monthly.empty:
        fig = go.Figure()
        
        # Add bar chart for games count
        fig.add_trace(go.Bar(
            x=monthly['month'],
            y=monthly['games'],
            name='Games Played',
            marker_color='lightblue',
            yaxis='y'
        ))
        
        # Add line chart for performance
        fig.add_trace(go.Scatter(
            x=monthly['month'],
            y=monthly['score_pct'],
            name='Score %',
            marker_color='red',
            yaxis='y2',
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='Monthly Activity and Performance',
            xaxis=dict(title='Month'),
            yaxis=dict(title='Games Played', side='left'),
            yaxis2=dict(title='Score (%)', side='right', overlaying='y'),
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Improvement Suggestions
    st.markdown("---")
    st.subheader("💡 Personalized Improvement Suggestions")
    
    suggestions = analyzer.generate_improvement_suggestions()
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")
    
    # Download Data
    st.markdown("---")
    st.subheader("💾 Download Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Game Data (CSV)",
            data=csv,
            file_name=f"chesscom_{username}_games_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    
    with col2:
        if not strengths.empty:
            strengths_csv = strengths.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Opening Strengths (CSV)",
                data=strengths_csv,
                file_name=f"chesscom_{username}_opening_strengths_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
