#!/usr/bin/env python3
"""
Chess.com Data Fetcher Module
Fetches and processes chess game data from Chess.com API
"""

import requests
import pandas as pd
from datetime import datetime
import time
from typing import List, Dict, Optional, Tuple


class ChessDataFetcher:
    """Handles fetching and processing chess.com game data"""
    
    BASE_URL = "https://api.chess.com/pub"
    
    def __init__(self, username: str):
        """
        Initialize fetcher for a specific chess.com username
        
        Args:
            username: Chess.com username
        """
        self.username = username.lower().strip()
        self.headers = {
            'User-Agent': 'ChessAnalysis/2.0 (https://github.com/sanjaykshetri/chess_dot_com_data_analysis)'
        }
    
    def validate_user(self) -> Tuple[bool, Optional[Dict]]:
        """
        Validate that the username exists on Chess.com
        
        Returns:
            Tuple of (success: bool, user_data: dict or None)
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/player/{self.username}", 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, None
            else:
                return False, None
                
        except Exception as e:
            print(f"Error validating user: {e}")
            return False, None
    
    def get_player_stats(self) -> Optional[Dict]:
        """
        Get player statistics including ratings
        
        Returns:
            Dictionary with player stats or None
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/player/{self.username}/stats",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"Error fetching player stats: {e}")
            return None
    
    def get_archives(self) -> List[str]:
        """
        Get list of available monthly game archives
        
        Returns:
            List of archive URLs
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/player/{self.username}/games/archives",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('archives', [])
            return []
            
        except Exception as e:
            print(f"Error fetching archives: {e}")
            return []
    
    def fetch_monthly_games(self, archive_url: str) -> List[Dict]:
        """
        Fetch games from a specific monthly archive
        
        Args:
            archive_url: URL of the monthly archive
            
        Returns:
            List of game dictionaries
        """
        try:
            response = requests.get(archive_url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                return response.json().get('games', [])
            return []
        except Exception as e:
            print(f"Error fetching games from {archive_url}: {e}")
            return []
    
    def fetch_all_games(self, max_months: Optional[int] = None, progress_callback=None) -> pd.DataFrame:
        """
        Fetch all games for the user
        
        Args:
            max_months: Maximum number of months to fetch (None for all)
            progress_callback: Optional callback function for progress updates
            
        Returns:
            DataFrame containing all games
        """
        archives = self.get_archives()
        
        if not archives:
            return pd.DataFrame()
        
        # Limit to recent months if specified
        if max_months:
            archives = archives[-max_months:]
        
        all_games = []
        total_archives = len(archives)
        
        for idx, archive_url in enumerate(archives, 1):
            games = self.fetch_monthly_games(archive_url)
            all_games.extend(games)
            
            if progress_callback:
                progress_callback(idx, total_archives)
            
            # Be respectful to the API
            time.sleep(0.15)
        
        if not all_games:
            return pd.DataFrame()
        
        # Process games into DataFrame
        return self._process_games(all_games)
    
    def _process_games(self, games: List[Dict]) -> pd.DataFrame:
        """
        Process raw game data into structured DataFrame
        
        Args:
            games: List of game dictionaries from API
            
        Returns:
            Processed DataFrame
        """
        processed_games = []
        
        for game in games:
            # Determine user's color and result
            white_player = game.get('white', {}).get('username', '').lower()
            black_player = game.get('black', {}).get('username', '').lower()
            
            if white_player == self.username:
                user_color = 'white'
                user_result = game.get('white', {}).get('result', 'unknown')
                opponent = black_player
                user_rating = game.get('white', {}).get('rating', None)
                opponent_rating = game.get('black', {}).get('rating', None)
            elif black_player == self.username:
                user_color = 'black'
                user_result = game.get('black', {}).get('result', 'unknown')
                opponent = white_player
                user_rating = game.get('black', {}).get('rating', None)
                opponent_rating = game.get('white', {}).get('rating', None)
            else:
                continue  # Skip games where user didn't play
            
            # Convert result to simple W/L/D
            if 'win' in user_result:
                simple_result = 'W'
            elif 'lose' in user_result or 'resigned' in user_result or 'checkmated' in user_result:
                simple_result = 'L'
            elif 'draw' in user_result or 'agreed' in user_result or 'stalemate' in user_result or 'repetition' in user_result or 'insufficient' in user_result or 'timevsinsufficient' in user_result:
                simple_result = 'D'
            else:
                simple_result = 'U'  # Unknown
            
            # Extract game details
            processed_game = {
                'url': game.get('url', ''),
                'pgn': game.get('pgn', ''),
                'time_control': game.get('time_control', ''),
                'time_class': game.get('time_class', ''),
                'rules': game.get('rules', ''),
                'rated': game.get('rated', False),
                'end_time': game.get('end_time', 0),
                'end_time_utc': datetime.fromtimestamp(game.get('end_time', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                'user_color': user_color,
                'user_result': simple_result,
                'user_rating': user_rating,
                'opponent': opponent,
                'opponent_rating': opponent_rating,
                'eco': game.get('eco', ''),
                'opening_name': self._extract_opening_name(game.get('pgn', '')),
                'termination': self._extract_termination(game.get('pgn', '')),
            }
            
            processed_games.append(processed_game)
        
        df = pd.DataFrame(processed_games)
        
        # Sort by end_time
        if not df.empty:
            df = df.sort_values('end_time').reset_index(drop=True)
        
        return df
    
    def _extract_opening_name(self, pgn: str) -> str:
        """Extract opening name from PGN"""
        try:
            for line in pgn.split('\n'):
                if line.startswith('[ECOUrl'):
                    # Extract opening name from URL
                    parts = line.split('/')
                    if len(parts) > 0:
                        opening = parts[-1].replace('"]', '').replace('-', ' ').strip()
                        return opening.title()
                elif line.startswith('[Opening'):
                    return line.split('"')[1] if '"' in line else ''
            return 'Unknown'
        except:
            return 'Unknown'
    
    def _extract_termination(self, pgn: str) -> str:
        """Extract termination reason from PGN"""
        try:
            for line in pgn.split('\n'):
                if line.startswith('[Termination'):
                    return line.split('"')[1] if '"' in line else 'Unknown'
            return 'Unknown'
        except:
            return 'Unknown'
