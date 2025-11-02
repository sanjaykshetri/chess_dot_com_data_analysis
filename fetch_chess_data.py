#!/usr/bin/env python3
"""
Chess.com API Data Fetcher
Simple script to fetch chess game data from Chess.com API
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime
from tqdm import tqdm

# Configuration
BASE_URL = "https://api.chess.com/pub"
USERNAME = "sanjaykshetri123"

def test_connection():
    """Test basic connection to Chess.com API"""
    print("🌐 Testing Chess.com API connection...")
    
    # Chess.com requires proper headers
    headers = {
        'User-Agent': 'ChessAnalysis/1.0 (https://github.com/sanjaykshetri/chess_dot_com_data_analysis)'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/player/{USERNAME}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connection successful!")
            print(f"👤 Player: {data.get('name', USERNAME)}")
            print(f"🏆 Title: {data.get('title', 'No title')}")
            print(f"📅 Joined: {datetime.fromtimestamp(data.get('joined', 0)).strftime('%Y-%m-%d')}")
            return True
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_archives():
    """Get list of available monthly archives"""
    headers = {
        'User-Agent': 'ChessAnalysis/1.0 (https://github.com/sanjaykshetri/chess_dot_com_data_analysis)'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/player/{USERNAME}/games/archives", headers=headers)
        if response.status_code == 200:
            archives = response.json()['archives']
            print(f"📁 Found {len(archives)} monthly archives")
            return archives
        else:
            print(f"❌ Failed to get archives: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting archives: {e}")
        return []

def fetch_monthly_games(archive_url):
    """Fetch games from a specific monthly archive"""
    headers = {
        'User-Agent': 'ChessAnalysis/1.0 (https://github.com/sanjaykshetri/chess_dot_com_data_analysis)'
    }
    
    try:
        response = requests.get(archive_url, headers=headers)
        if response.status_code == 200:
            return response.json()['games']
        else:
            return []
    except:
        return []

def main():
    """Main execution function"""
    print("🏁 Starting Chess.com data acquisition...")
    print("=" * 50)
    
    # Test connection first
    if not test_connection():
        print("Cannot proceed without API connection")
        return
    
    print("\n📊 Getting game archives...")
    archives = get_archives()
    
    if not archives:
        print("No archives found")
        return
    
    # Show latest few archives
    print(f"\n📅 Latest archives:")
    for archive in archives[-5:]:
        print(f"  • {archive}")
    
    # Ask user if they want to proceed
    print(f"\n🎯 Ready to fetch games from {len(archives)} archives")
    proceed = input("Continue? (y/n): ").lower().strip()
    
    if proceed != 'y':
        print("Aborted by user")
        return
    
    # Fetch all games
    all_games = []
    print("\n⬇️ Fetching games...")
    
    for archive_url in tqdm(archives, desc="Archives"):
        games = fetch_monthly_games(archive_url)
        all_games.extend(games)
        time.sleep(0.1)  # Be nice to the API
    
    print(f"\n🎉 Successfully fetched {len(all_games)} games!")
    
    # Convert to DataFrame and save
    if all_games:
        df = pd.json_normalize(all_games)
        output_file = f"chess_games_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)
        print(f"💾 Saved to: {output_file}")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"📈 Shape: {df.shape}")
    
    print("\n✅ Data acquisition complete!")

if __name__ == "__main__":
    main()