
import sqlite3
import plotly.graph_objs as go
import plotly.express as px

def read_query(query):
    '''Connect to target database in sqlite and execute given query
    
    Parameters
    ----------
    string:
        query need to be executed

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    conn = sqlite3.connect("NFL.sqlite")
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    conn.close()
    return result

def find_available_team(query):
    results = read_query(query)
    team_list =[data[0] for data in results]
    return team_list

def display_bar_plot(xvals, yvals, title):
    bar_data = go.Bar(x=xvals, y=yvals)
    basic_layout = go.Layout(title=f"{title}")
    fig = go.Figure(data=bar_data, layout=basic_layout)
    return fig

def display_line_plot(xvals, yvals, title):
    fig = px.line(x=xvals, y=yvals, labels=dict(x="Year", y="TD"), title=title)
    return fig

def select_roster(team, no):
    query = f'''
    SELECT  R.Name, R.ATT, R.TD, T.Team
    FROM Rosters R JOIN Teams T ON R.Tid = T.Tid
    WHERE T.Team = "{team}"
    ORDER BY R.TD DESC
    LIMIT {no};
    '''
    return read_query(query)

def find_rosters_team():
    query='''
    SELECT T.Team
    FROM Teams T JOIN Rosters R
    ON T.Tid = R.Tid
    GROUP BY T.Team
    '''
    return find_available_team(query)

def top_rosters(team):
    ''' 
    team: select a team name or all
    mode: table or bar chart

    Top 3 rosters with TD
    '''
    results = select_roster(team, 3)
    xvals = [data[0] for data in results]
    yvals = [data[2] for data in results]
    return display_bar_plot(xvals, yvals, team)

def team_roster_performance(team_list):
    '''
    team_list: 5 team
    '''
    results = []
    for team in team_list:
        temp = select_roster(team, 1)
        results.extend(temp)
    results = sorted(results, key=lambda x : x[2], reverse=True)
    xvals = [f"{data[0]}/{data[3]}" for data in results]
    yvals = [data[2] for data in results]
    return display_bar_plot(xvals, yvals,"")

def select_teams_in_year(year):
    query=f'''
    SELECT T.Team
    FROM Teams T JOIN Stats S
    ON T.Tid = S.Tid
    WHERE S.Year = {year}
    GROUP BY T.Team
    '''
    return find_available_team(query)

def compare_team_performance(team_list, year):
    '''
    team_list: 2-5 teams
    year: year
    '''
    results=[]
    for team in team_list:
        query =f'''
        SELECT T.Team, S.TD
        FROM Teams T JOIN Stats S
        ON T.Tid = S.Tid
        WHERE T.Team = "{team}" and S.Year = "{year}"
        '''
        temp = read_query(query)
        results.extend(temp)
    xvals = [data[0] for data in results]
    yvals = [data[1] for data in results]
    return display_bar_plot(xvals, yvals,year)

def schedule_available_team():
    query='''
    SELECT  T.Team
    FROM Teams T JOIN Schedule S
    ON T.Tid = S.Tid 
	GROUP BY T.Team
    '''
    return find_available_team(query)

def team_schedule(team):
    '''
    team: null or name
    place: null or name
    '''
    query = f'''
    SELECT  T.Team, S.Team2, S.Time, S.Year
    FROM Teams T JOIN Schedule S
    ON T.Tid = S.Tid 
    WHERE T.Team = "{team}"
    '''
    results = read_query(query)
    headers = ["Team1", "Team2", "Time", "Year"]
    # print(display_table(results, headers))
    return headers, results

def team_history_available():
    query='''
    SELECT  T.Team
    FROM Teams T JOIN Stats S
    ON T.Tid = S.Tid 
    GROUP BY T.Team
    '''
    return find_available_team(query)

def team_performace_history(team, start_year, end_year):
    '''
    team: name
    start_year: year difference must be larger than 5 years
    end_year:
    '''
    query =f'''
    SELECT S.TD, S.Year
    FROM Teams T JOIN Stats S
    ON T.Tid = S.Tid 
    WHERE T.Team = "{team}"
    '''
    results = read_query(query)
    xvals = []
    yvals = []
    for data in results:
        if data[1] >= start_year and data[1] <= end_year:
            xvals.append(data[1])
            yvals.append(data[0])
    return display_line_plot(xvals, yvals, team)

