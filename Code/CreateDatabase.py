import sqlite3
import ScrapeData

conn = sqlite3.connect("NFL.sqlite")
cur = conn.cursor()
def create_database():
    drop_team = '''
    DROP TABLE IF EXISTS "Teams";
    '''
    drop_superbowl = '''
    DROP TABLE IF EXISTS "SuperBowl";
    '''
    drop_roster = '''
    DROP TABLE IF EXISTS "Rosters";
    '''
    drop_stats = '''
    DROP TABLE IF EXISTS "Stats";
    '''
    drop_schedule = '''
    DROP TABLE IF EXISTS "Schedule";
    '''
    cur.execute(drop_team)
    cur.execute(drop_superbowl)
    cur.execute(drop_roster)
    cur.execute(drop_stats)
    cur.execute(drop_schedule)


    create_team = '''
    CREATE TABLE "Teams"(
        "Tid"    INTEGER UNIQUE,
        "Team"  TEXT NOT NULL,
        PRIMARY KEY("Tid" AUTOINCREMENT)
    );
    '''

    # create_superbowl ='''
    # CREATE TABLE "SuperBowl"(
    #     "Id"    INTEGER UNIQUE,
    #     "Team1"  TEXT NOT NULL,
    #     "Score1" TEXT NOT NULL,
    #     "Team2"  TEXT NOT NULL,
    #     "Score2" TEXT NOT NULL,
    #     "Year"   TEXT NOT NULL,
    #     PRIMARY KEY("Id" AUTOINCREMENT)
    # );
    # '''

    create_rosters='''
    CREATE TABLE "Rosters"(
        "Id"    INTEGER UNIQUE,
        "Tid"   INTEGER NOT NULL,
        "Name"  TEXT NOT NULL,
        "ATT"  INTEGER NOT NULL,
        "TD" INTEGER NOT NULL,
        PRIMARY KEY("Id" AUTOINCREMENT),
        FOREIGN KEY (Tid) REFERENCES Teams (Tid)
    );
    '''

    create_stats='''
    CREATE TABLE "Stats"(
        "Id"    INTEGER UNIQUE,
        "Tid"   INTEGER NOT NULL,
        "Year"  TEXT NOT NULL,
        "TD"  INTEGER NOT NULL,
        PRIMARY KEY("Id" AUTOINCREMENT),
        FOREIGN KEY (Tid) REFERENCES Teams (Tid)
    );
    '''

    create_schedule='''
    CREATE TABLE "Schedule"(
        "Id"    INTEGER UNIQUE,
        "Tid"   INTEGER NOT NULL,
        "Team2" TEXT NOT NULL,
        "Year"  TEXT NOT NULL,
        "Time"  TEXT NOT NULL,
        PRIMARY KEY("Id" AUTOINCREMENT),
        FOREIGN KEY (Tid) REFERENCES Teams (Tid)
    );
    '''
    
    cur.execute(create_team)
    # cur.execute(create_superbowl)
    cur.execute(create_rosters)
    cur.execute(create_stats)
    cur.execute(create_schedule)

    conn.commit()

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
    result = cur.execute(query).fetchall()
    return result

team_dict={}

def insert_team():

    teams = ScrapeData.cache_find('team').keys()
    insert_teams = '''
    INSERT INTO Teams 
    VALUES (Null, ?);
    '''

    for team in teams:
        cur.execute(insert_teams, [team])

    conn.commit()


def insert_single_team(team, cur):
    insert_teams = '''
    INSERT INTO Teams 
    VALUES (Null, ?);
    '''
    cur.execute(insert_teams, [team])


def match_team_id():
    query = '''
    SELECT *
    FROM Teams
    '''
    for team in read_query(query):
        team_dict[team[1]] = team[0]

def insert_schedule():

    schedule = ScrapeData.cache_find('schedule')
    teams = schedule.keys()

    insert_schedules = '''
    INSERT INTO Schedule (Id, Team2, Time, Year, Tid)
    VALUES (Null, ?, ?, ?, ?);
    '''

    for team in teams:
        tid = team_dict[team]
        for match in schedule[team]:
            match.append(tid)
            # print(match)
            cur.execute(insert_schedules, match)
    conn.commit()


def insert_stats():
    stats = ScrapeData.cache_find('stats')
    years = stats.keys()

    insert_stats_query = '''
    INSERT INTO Stats (Id, Tid, Year, TD)
    VALUES (Null, ?, ?, ?);
    '''

    for year in years:
        curr_stats = stats[year]
        for team in curr_stats.keys():
            if team not in team_dict.keys():
                insert_single_team(team, cur)
                match_team_id()
            tid = team_dict[team]
            td = curr_stats[team]
            data = [tid, year, td]
            cur.execute(insert_stats_query, data)
    conn.commit()

def insert_rosters():
    rosters = ScrapeData.cache_find('rosters')
    teams = rosters.keys()

    insert_roster_query = '''
    INSERT INTO Rosters (Id, Name, TD, ATT, Tid)
    VALUES (Null, ?, ?, ?, ?);
    '''

    for team in teams:
        tid = team_dict[team]
        for roster in rosters[team]:
            roster.append(tid)
            cur.execute(insert_roster_query, roster)
    
    conn.commit()

def fillup_database():
    ScrapeData.scrape_all()
    create_database()
    insert_team()
    match_team_id()
    insert_schedule()
    insert_stats()
    insert_rosters()
    conn.close()

if __name__ == "__main__":
    fillup_database()