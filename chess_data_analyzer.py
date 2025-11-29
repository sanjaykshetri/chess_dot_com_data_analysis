#!/usr/bin/env python3
"""
Chess Data Analyzer Module
Analyzes chess game data and generates insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class ChessDataAnalyzer:
    """Analyzes chess game data and generates insights"""
    
    def __init__(self, df: pd.DataFrame, timezone: str = "America/New_York"):
        """
        Initialize analyzer with game data
        
        Args:
            df: DataFrame containing game data
            timezone: Timezone for time-based analysis
        """
        self.df = df.copy()
        self.timezone = timezone
        self.min_games_threshold = 20  # Minimum games for opening analysis
        
        if not self.df.empty:
            self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data with derived features"""
        # Score mapping
        score_map = {"W": 1.0, "D": 0.5, "L": 0.0, "U": 0.0}
        self.df["score"] = self.df["user_result"].map(score_map)
        
        # Parse timestamps
        self.df["end_time_utc"] = pd.to_datetime(self.df["end_time_utc"], errors="coerce")
        self.df["end_time_local"] = self.df["end_time_utc"].dt.tz_localize("UTC").dt.tz_convert(self.timezone)
        
        # Time-based features
        self.df["date"] = self.df["end_time_local"].dt.date
        self.df["hour"] = self.df["end_time_local"].dt.hour
        self.df["day_of_week"] = self.df["end_time_local"].dt.day_name()
        self.df["month"] = self.df["end_time_local"].dt.to_period("M").astype(str)
        self.df["year"] = self.df["end_time_local"].dt.year
        
        # Calculate game number (chronological)
        self.df["game_number"] = range(1, len(self.df) + 1)
    
    def get_overview_stats(self) -> Dict:
        """
        Get comprehensive overview statistics
        
        Returns:
            Dictionary with overview metrics
        """
        if self.df.empty:
            return {}
        
        total_games = len(self.df)
        wins = (self.df["user_result"] == "W").sum()
        draws = (self.df["user_result"] == "D").sum()
        losses = (self.df["user_result"] == "L").sum()
        
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        # Rating stats
        current_rating = self.df["user_rating"].iloc[-1] if "user_rating" in self.df.columns else None
        starting_rating = self.df["user_rating"].iloc[0] if "user_rating" in self.df.columns else None
        rating_change = current_rating - starting_rating if (current_rating and starting_rating) else 0
        
        # Time span
        first_game = self.df["end_time_local"].min()
        last_game = self.df["end_time_local"].max()
        days_playing = (last_game - first_game).days if first_game and last_game else 0
        
        # Average games per day
        avg_games_per_day = total_games / days_playing if days_playing > 0 else 0
        
        return {
            "total_games": total_games,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate": win_rate,
            "current_rating": current_rating,
            "starting_rating": starting_rating,
            "rating_change": rating_change,
            "first_game_date": first_game.strftime("%Y-%m-%d") if first_game else None,
            "last_game_date": last_game.strftime("%Y-%m-%d") if last_game else None,
            "days_playing": days_playing,
            "avg_games_per_day": avg_games_per_day,
        }
    
    def get_performance_by_color(self) -> pd.DataFrame:
        """Get performance statistics by color"""
        if self.df.empty:
            return pd.DataFrame()
        
        color_stats = self.df.groupby("user_color").agg({
            "score": ["count", "sum", "mean"],
            "user_result": lambda x: (x == "W").sum()
        }).round(3)
        
        color_stats.columns = ["games", "total_score", "avg_score", "wins"]
        color_stats["win_rate"] = (color_stats["wins"] / color_stats["games"] * 100).round(1)
        
        return color_stats.reset_index()
    
    def get_performance_by_time_class(self) -> pd.DataFrame:
        """Get performance statistics by time class"""
        if self.df.empty:
            return pd.DataFrame()
        
        time_stats = self.df.groupby("time_class").agg({
            "score": ["count", "mean"],
        }).round(3)
        
        time_stats.columns = ["games", "avg_score"]
        time_stats["score_pct"] = (time_stats["avg_score"] * 100).round(1)
        
        return time_stats.sort_values("score_pct", ascending=False).reset_index()
    
    def get_performance_by_hour(self) -> pd.DataFrame:
        """Get performance by hour of day"""
        if self.df.empty:
            return pd.DataFrame()
        
        hour_stats = self.df.groupby("hour").agg({
            "score": ["count", "mean"]
        }).round(3)
        
        hour_stats.columns = ["games", "avg_score"]
        hour_stats["score_pct"] = (hour_stats["avg_score"] * 100).round(1)
        
        return hour_stats.reset_index()
    
    def get_performance_by_day_of_week(self) -> pd.DataFrame:
        """Get performance by day of week"""
        if self.df.empty:
            return pd.DataFrame()
        
        # Define day order
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        dow_stats = self.df.groupby("day_of_week").agg({
            "score": ["count", "mean"]
        }).round(3)
        
        dow_stats.columns = ["games", "avg_score"]
        dow_stats["score_pct"] = (dow_stats["avg_score"] * 100).round(1)
        dow_stats = dow_stats.reset_index()
        
        # Sort by day order
        dow_stats["day_of_week"] = pd.Categorical(
            dow_stats["day_of_week"], 
            categories=day_order, 
            ordered=True
        )
        dow_stats = dow_stats.sort_values("day_of_week")
        
        return dow_stats
    
    def get_opening_analysis(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Analyze opening performance
        
        Returns:
            Tuple of (strengths_df, weaknesses_df)
        """
        if self.df.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        # Group by opening
        opening_stats = self.df.groupby(["eco", "opening_name"]).agg({
            "score": ["count", "mean"]
        }).round(3)
        
        opening_stats.columns = ["games", "avg_score"]
        opening_stats["score_pct"] = (opening_stats["avg_score"] * 100).round(1)
        opening_stats = opening_stats.reset_index()
        
        # Filter by minimum games
        opening_stats = opening_stats[opening_stats["games"] >= self.min_games_threshold]
        
        if opening_stats.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        # Sort for strengths and weaknesses
        strengths = opening_stats.nlargest(10, "score_pct")
        weaknesses = opening_stats.nsmallest(10, "score_pct")
        
        return strengths, weaknesses
    
    def get_rating_progression(self) -> pd.DataFrame:
        """Get rating progression over time"""
        if self.df.empty or "user_rating" not in self.df.columns:
            return pd.DataFrame()
        
        # Sample data points for cleaner visualization
        df_sample = self.df[["game_number", "user_rating", "end_time_local"]].copy()
        df_sample = df_sample.dropna(subset=["user_rating"])
        
        return df_sample
    
    def get_monthly_activity(self) -> pd.DataFrame:
        """Get monthly game count and performance"""
        if self.df.empty:
            return pd.DataFrame()
        
        monthly = self.df.groupby("month").agg({
            "score": ["count", "mean"]
        }).round(3)
        
        monthly.columns = ["games", "avg_score"]
        monthly["score_pct"] = (monthly["avg_score"] * 100).round(1)
        
        return monthly.reset_index()
    
    def get_termination_analysis(self) -> pd.DataFrame:
        """Analyze game termination types"""
        if self.df.empty or "termination" not in self.df.columns:
            return pd.DataFrame()
        
        term_stats = self.df.groupby("termination").agg({
            "score": ["count", "mean"]
        }).round(3)
        
        term_stats.columns = ["games", "avg_score"]
        term_stats["score_pct"] = (term_stats["avg_score"] * 100).round(1)
        
        return term_stats.sort_values("games", ascending=False).reset_index()
    
    def calculate_total_time_spent(self) -> Dict:
        """
        Calculate estimated total time spent playing chess
        
        Returns:
            Dictionary with time estimates
        """
        if self.df.empty:
            return {}
        
        # Estimate time per game based on time class
        time_estimates = {
            "bullet": 3,      # ~3 minutes average
            "blitz": 6,       # ~6 minutes average
            "rapid": 15,      # ~15 minutes average
            "daily": 0,       # Not counted for active time
        }
        
        total_minutes = 0
        for time_class, minutes in time_estimates.items():
            games_count = (self.df["time_class"] == time_class).sum()
            total_minutes += games_count * minutes
        
        hours = total_minutes / 60
        days = hours / 24
        
        return {
            "total_minutes": int(total_minutes),
            "total_hours": round(hours, 1),
            "total_days": round(days, 2),
        }
    
    def generate_improvement_suggestions(self) -> List[str]:
        """
        Generate personalized improvement suggestions
        
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        if self.df.empty:
            return ["Not enough data for analysis"]
        
        # Color performance
        color_perf = self.get_performance_by_color()
        if not color_perf.empty:
            white_score = color_perf[color_perf["user_color"] == "white"]["score_pct"].values
            black_score = color_perf[color_perf["user_color"] == "black"]["score_pct"].values
            
            if len(white_score) > 0 and len(black_score) > 0:
                if white_score[0] < black_score[0] - 5:
                    suggestions.append(f"🎯 **White Piece Improvement Needed**: Your score with White ({white_score[0]:.1f}%) is lower than Black. Focus on studying white opening repertoire.")
                elif black_score[0] < white_score[0] - 5:
                    suggestions.append(f"🎯 **Black Piece Improvement Needed**: Your score with Black ({black_score[0]:.1f}%) is lower than White. Practice defensive and counter-attacking play.")
        
        # Time class performance
        time_perf = self.get_performance_by_time_class()
        if not time_perf.empty and len(time_perf) > 1:
            best_class = time_perf.iloc[0]
            worst_class = time_perf.iloc[-1]
            suggestions.append(f"💡 **Best Performance**: You perform best in {best_class['time_class']} ({best_class['score_pct']:.1f}%). Consider focusing on this format for rating improvement.")
            if worst_class["games"] >= 20:
                suggestions.append(f"⚠️ **Needs Work**: Your {worst_class['time_class']} performance ({worst_class['score_pct']:.1f}%) could be improved. Practice time management in this format.")
        
        # Opening weaknesses
        _, weaknesses = self.get_opening_analysis()
        if not weaknesses.empty:
            worst_opening = weaknesses.iloc[0]
            suggestions.append(f"📚 **Opening to Study**: {worst_opening['opening_name']} ({worst_opening['eco']}) - only {worst_opening['score_pct']:.1f}% score in {int(worst_opening['games'])} games. Review key variations and common mistakes.")
        
        # Time of day performance
        hour_perf = self.get_performance_by_hour()
        if not hour_perf.empty and len(hour_perf) > 3:
            best_hours = hour_perf.nlargest(3, "score_pct")
            best_hour_range = f"{best_hours['hour'].min()}-{best_hours['hour'].max()}"
            avg_best_score = best_hours["score_pct"].mean()
            suggestions.append(f"⏰ **Optimal Playing Time**: You perform best between {best_hour_range}:00 ({avg_best_score:.1f}% avg). Try to play important games during these hours.")
        
        # Recent performance trend
        if len(self.df) >= 50:
            recent_50 = self.df.tail(50)["score"].mean() * 100
            older_50 = self.df.iloc[-100:-50]["score"].mean() * 100 if len(self.df) >= 100 else None
            
            if older_50:
                if recent_50 > older_50 + 5:
                    suggestions.append(f"📈 **Improving!** Your recent performance ({recent_50:.1f}%) is better than before ({older_50:.1f}%). Keep up the good work!")
                elif recent_50 < older_50 - 5:
                    suggestions.append(f"📉 **Recent Slump**: Your recent performance ({recent_50:.1f}%) has decreased. Consider taking a break or reviewing fundamentals.")
        
        # Add general advice
        total_games = len(self.df)
        if total_games < 100:
            suggestions.append("🎮 **Play More Games**: With more games, the analysis will become more reliable and insights more accurate.")
        
        return suggestions if suggestions else ["Keep playing and improving! More games will provide better insights."]
