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
cd premier-league-data-analysis
```
### 2. Create a virtual environment
```bash
python3 -m venv .venv
```
macOS/Linux:
```
source .venv/bin/activate
```
Windows:
```
.venv/Scripts/activate
```

### #3. Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
### 4. Add your API token
Create a .env like example and replace 'your_token_here' with your token from football-data.org

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
- Home win percentage
- Away win percentage
- Draw percentage

For example:
```
Home Win Probability: 34.1%
Away Win Probability: 31.7%
Draw Probability: 34.1%
```

## Visualizations
The program displays and saves an image visualizing a sample of the stats:
<img width="4470" height="2965" alt="league_analysis" src="https://github.com/user-attachments/assets/bf3786cd-200c-4680-b0d7-838336a542ec" />


## Future Improvements
- Add more advanced statistics
- Allow tool to be easily repurposed for other sports/leagues
- Building a web interfaces
- Making the visualizations interactive
- Explore predictive modelling
