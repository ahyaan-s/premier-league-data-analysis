import requests
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


load_dotenv()

#get API token from env
api_token = os.getenv("FOOTBALL_DATA_API_TOKEN")


if not api_token:
    print("ERROR: No API token found in .env file.")
    print("Please add your token to the .env file.")
    exit(1)

url = "https://api.football-data.org/v4/competitions/PL/matches"

headers = {
    "X-Auth-Token": api_token
}

try:

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Successfully retrieved Premier League data.")
        
        # Convert JSON response to Python dictionary
        data = response.json()
        
        # Print number of matches retrieved
        matches = data.get("matches", [])
        print(f"Number of matches retrieved: {len(matches)}")


    # Extract matches 
    processed_matches = []
    for match in data.get('matches', []):
        if match['status'] == 'FINISHED':  # Only finished matches
            processed_matches.append({
                'date': match['utcDate'].split('T')[0],
                'home_team': match['homeTeam']['name'],
                'away_team': match['awayTeam']['name'],
                'home_score': match['score']['fullTime']['home'],
                'away_score': match['score']['fullTime']['away'],
                'status': match['status']
            })
        
    # Pandas DataFrame
    df = pd.DataFrame(processed_matches)

    # Display basic information about data
    print("\n📋 First 5 matches:")
    print(df.head())
    
        
    # Write to CSV
    df.to_csv('premier_league_matches.csv', index=False)
    print("\n💾 Data saved to 'premier_league_matches.csv'")

    #Calculate probabilities
    print("Calculating real-time probabilities...")


        # Group teams to calculate performance metrics
    team_stats = {}

    #Get all teams
    all_teams = set(df['home_team'].tolist() + df['away_team'].tolist())


    # Calculate statistics for each team
    for team in all_teams:
        home_matches = df[df['home_team'] == team]
        away_matches = df[df['away_team'] == team]
        
        # Combine all matches for this team
        all_team_matches = pd.concat([home_matches, away_matches])
        
        if len(all_team_matches) > 0:
            # Calculate wins, losses, draws
            wins = 0
            losses = 0
            draws = 0
            
            # For home matches
            for _, match in home_matches.iterrows():
                if match['home_score'] > match['away_score']:
                    wins += 1
                elif match['home_score'] < match['away_score']:
                    losses += 1
                else:
                    draws += 1
            
            # For away matches  
            for _, match in away_matches.iterrows():
                if match['away_score'] > match['home_score']:
                    wins += 1
                elif match['away_score'] < match['home_score']:
                    losses += 1
                else:
                    draws += 1
            
            total_matches = len(all_team_matches)
            
            # Calculate win/loss/draw percentages
            win_pct = (wins / total_matches) * 100 if total_matches > 0 else 0
            loss_pct = (losses / total_matches) * 100 if total_matches > 0 else 0
            draw_pct = (draws / total_matches) * 100 if total_matches > 0 else 0
            
            # Calculate points (3 for win, 1 for draw, 0 for loss)
            points = wins * 3 + draws * 1
            avg_points_per_match = points / total_matches if total_matches > 0 else 0
            
            team_stats[team] = {
                'total_matches': total_matches,
                'wins': wins,
                'losses': losses,
                'draws': draws,
                'win_percentage': win_pct,
                'loss_percentage': loss_pct,
                'draw_percentage': draw_pct,
                'points': points,
                'avg_points_per_match': avg_points_per_match
            }
    
    # Display team statistics
    print("\n🏆 Team Statistics:")
    print("-" * 80)
    print(f"{'Team':<25} {'Matches':<10} {'Wins':<8} {'Losses':<8} {'Draws':<8} {'Win%':<8} {'Points':<8}")
    print("-" * 80)
    
    # Sort by points descending
    sorted_teams = sorted(team_stats.items(), key=lambda x: x[1]['points'], reverse=True)
    
    for team, stats in sorted_teams:
        print(f"{team:<25} {stats['total_matches']:<10} {stats['wins']:<8} {stats['losses']:<8} {stats['draws']:<8} {stats['win_percentage']:.1f}{'%':<8} {stats['points']:<8}")
    
    # Calculate head-to-head probabilities
    print("\n⚔️ Head-to-Head Probabilities:")
    print("-" * 60)
    
    # Get all unique pairs of teams that have played against each other
    pairs = set()
    for _, match in df.iterrows():
        pair = tuple(sorted([match['home_team'], match['away_team']]))
        pairs.add(pair)
    
    # Calculate probability for each pair
    head_to_head_probs = {}
    for team1, team2 in pairs:
        if team1 != team2:
            # Get matches between these two teams
            matches_between = df[
                ((df['home_team'] == team1) & (df['away_team'] == team2)) |
                ((df['home_team'] == team2) & (df['away_team'] == team1))
            ]
            
            if len(matches_between) > 0:
                team1_wins = 0
                team2_wins = 0
                draws = 0
                
                for _, match in matches_between.iterrows():
                    if match['home_team'] == team1:
                        if match['home_score'] > match['away_score']:
                            team1_wins += 1
                        elif match['home_score'] < match['away_score']:
                            team2_wins += 1
                        else:
                            draws += 1
                    else:  # team2 is home
                        if match['away_score'] > match['home_score']:
                            team1_wins += 1
                        elif match['away_score'] < match['home_score']:
                            team2_wins += 1
                        else:
                            draws += 1
                
                total = len(matches_between)
                prob_team1 = (team1_wins / total) * 100 if total > 0 else 0
                prob_team2 = (team2_wins / total) * 100 if total > 0 else 0
                prob_draw = (draws / total) * 100 if total > 0 else 0
                
                head_to_head_probs[(team1, team2)] = {
                    'prob_team1': prob_team1,
                    'prob_team2': prob_team2,
                    'prob_draw': prob_draw
                }
                
                print(f"{team1} vs {team2}:")
                print(f"  {team1}: {prob_team1:.1f}% | {team2}: {prob_team2:.1f}% | Draw: {prob_draw:.1f}%")
    
    # Calculate overall league probabilities
    print("\n📈 Overall League Probabilities:")
    print("-" * 50)
    
    # Get all teams that have played at least one match
    teams_with_matches = set(df['home_team'].tolist() + df['away_team'].tolist())
    
    # Calculate overall win/loss/draw probabilities for the league
    total_matches = len(df)
    total_home_wins = sum(1 for _, match in df.iterrows() if match['home_score'] > match['away_score'])
    total_away_wins = sum(1 for _, match in df.iterrows() if match['away_score'] > match['home_score'])
    total_draws = sum(1 for _, match in df.iterrows() if match['home_score'] == match['away_score'])
    
    home_win_prob = (total_home_wins / total_matches) * 100
    away_win_prob = (total_away_wins / total_matches) * 100  
    draw_prob = (total_draws / total_matches) * 100
    
    print(f"Home Win Probability: {home_win_prob:.1f}%")
    print(f"Away Win Probability: {away_win_prob:.1f}%")
    print(f"Draw Probability: {draw_prob:.1f}%")
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # 1. Team Points Distribution (Top 10)
    plt.subplot(2, 3, 1)
    team_points = [stats['points'] for _, stats in sorted_teams[:10]]
    team_names = [team for team, _ in sorted_teams[:10]]
    bars = plt.bar(range(len(team_points)), team_points, color='skyblue')
    plt.title('Top 10 Teams by Points')
    plt.xlabel('Teams')
    plt.ylabel('Points')
    plt.xticks(range(len(team_names)), team_names, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, (bar, points) in enumerate(zip(bars, team_points)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(points), ha='center', va='bottom')
    
    # 2. Team Win Percentages (Top 10)
    plt.subplot(2, 3, 2)
    win_pcts = [stats['win_percentage'] for _, stats in sorted_teams[:10]]
    bars = plt.bar(range(len(win_pcts)), win_pcts, color='lightgreen')
    plt.title('Top 10 Teams by Win Percentage')
    plt.xlabel('Teams')
    plt.ylabel('Win Percentage (%)')
    plt.xticks(range(len(team_names)), team_names, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, (bar, pct) in enumerate(zip(bars, win_pcts)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{pct:.1f}%', ha='center', va='bottom')
    
    # 3. Match Outcome Distribution
    plt.subplot(2, 3, 3)
    outcomes = ['Home Win', 'Away Win', 'Draw']
    percentages = [home_win_prob, away_win_prob, draw_prob]
    colors = ['lightblue', 'orange', 'gray']
    plt.pie(percentages, labels=outcomes, autopct='%1.1f%%', colors=colors)
    plt.title('Overall Match Outcome Distribution')
    
    # 4. Goals Distribution
    plt.subplot(2, 3, 4)
    df['total_goals'] = df['home_score'] + df['away_score']
    plt.hist(df['total_goals'], bins=15, color='purple', alpha=0.7)
    plt.title('Distribution of Total Goals')
    plt.xlabel('Total Goals')
    plt.ylabel('Frequency')
    
    # 5. Average Goals per Match
    plt.subplot(2, 3, 5)
    avg_goals = df['total_goals'].mean()
    plt.bar(['Average Goals'], [avg_goals], color='red')
    plt.title('Average Goals per Match')
    plt.ylabel('Goals')
    plt.ylim(0, max(df['total_goals']) + 1)
    
    # Add value label
    plt.text(0, avg_goals + 0.1, f'{avg_goals:.1f}', ha='center', va='bottom')
    
    # 6. Team Performance Overview (Top 5 teams)
    plt.subplot(2, 3, 6)
    top_teams = [team for team, _ in sorted_teams[:5]]
    win_rates = [stats['win_percentage'] for team, stats in sorted_teams[:5]]
    draw_rates = [stats['draw_percentage'] for team, stats in sorted_teams[:5]]
    loss_rates = [stats['loss_percentage'] for team, stats in sorted_teams[:5]]
    
    x = range(len(top_teams))
    plt.bar(x, win_rates, label='Wins', color='green', alpha=0.7)
    plt.bar(x, draw_rates, bottom=win_rates, label='Draws', color='gray', alpha=0.7)
    plt.bar(x, loss_rates, bottom=[w + d for w, d in zip(win_rates, draw_rates)], 
            label='Losses', color='red', alpha=0.7)
    
    plt.title('Top 5 Teams Performance')
    plt.xlabel('Teams')
    plt.ylabel('Percentage (%)')
    plt.xticks(x, top_teams, rotation=45, ha='right')
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('league_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Summary
    print("\n📋 Summary:")
    print("-" * 50)
    print(f"Total matches analyzed: {total_matches}")
    print(f"Teams played: {len(teams_with_matches)}")
    print(f"Average goals per match: {df['total_goals'].mean():.2f}")
    print(f"Most successful team: {sorted_teams[0][0]} ({sorted_teams[0][1]['points']} points)")
    print(f"Least successful team: {sorted_teams[-1][0]} ({sorted_teams[-1][1]['points']} points)")

except Exception as e:
    print(f"An error occurred: {e}")
