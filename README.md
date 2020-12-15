# SI507_Final
This repo contains all the code needed for running a simple web app about retrieving data from NFL website

Startup: 
install packages:
flask, sqlite3, plotly, bs4, BeautifulSoup, requests

Run app:
Run app.py directly, then wait for initializing app and visit page link shown in terminal

Test guide:
Before start, you can check this video as guidance: https://drive.google.com/file/d/1b-IQ0CuyQgToxzOx9YyEHzXv18Azqlyr/view?usp=sharing
User face capabilities: 5 features to choose:
	1. A team’s/overall top 3 Rosters’ rushing performance comparison: TD, ATT
    input: choose a team avalilable for this feature
    output: a Bar chart with top 3 rosters': x: Name,  y: TD, title: team

    2. 5 team’s top Rosters’ rushing performance comparison: TD, ATT
    input: choose 5 teams to compare
    output: a Bar chart with each team's top roster: x: Name/team,  y: TD

    3. Choose 2 to 5 team to compare their TOUCHDOWNS in a specific year
    input: a year (2005-2020), choose 5 teams to compare
    output: a Bar chart with each team's TD: x: Team,  y: TD, title: year

    4. A team’s TOUCHDOWNS in continuous years
    input: team, start-end year (2005 to 2020) e.g. 2005-2009
    output: a line chart with TD in continuous years: x: year, y:TD, title: team

    5. A team’s schedule in regular season in 2020
    input: team
    output: a table contains all schedule of this team: team1, team2, time, year

