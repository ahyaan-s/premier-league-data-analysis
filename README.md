# premier-league-data-analysis

A Python program that fetches English Premier League data and creates visualizations.

## Features
- Retrieves Premier League match data from an API
- Analyzes completed matches from the current season
- Processes match data using Pandas
- Saves processed match data to a CSV file
- Calculates team performance statistics
- Calculates win, loss, and draw percentages
- Calculates team points and average points per match
- Calculates historical head-to-head outcome probabilities
- Calculates overall Premier League match outcome probabilities
- Generates multiple data visualizations
- Displays a summary of the analyzed season

## Data Source

Match data is retrieved from the [football-data.org](https://www.football-data.org/) API.

The project uses retrieves match data from:
https://api.football-data.org/v4/competitions/PL/matches

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip


### 1. Clone the repository
```bash
git clone https://github.com/ahyaan-s/premier-league-data-analysis.git
cd premier-league-analysis
```
### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### #3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Add your API token
in .env, replace 'your_token_here' with your token from football-data.org

### 5. Run
```bash
python main.py
```

## Data Processing
The program retrieves the information and saves it to:
```
premier_league_matches.csv
```

### Head-to-Head Analysis
The program identifies the teams that have played each other and calculates the percentage of:
- Team 1 wins
- Team 2 wins
- Draws

For example:
```
Arsenal FC vs Chelsea FC:
  Arsenal FC: 100.0% | Chelsea FC: 0.0% | Draw: 0.0%
```

### League-Wide Analysis
The distribution of match outcomes are calculated:
- Home win probability
- Away win probability
- Draw probability

For example:
```
Home Win Probability: 34.1%
Away Win Probability: 31.7%
Draw Probability: 34.1%
```

## Visualizations
The program displays and saves an image visualizing a sample of the stats:
