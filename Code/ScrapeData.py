from bs4 import BeautifulSoup
import requests
import json
import sqlite3

def open_cache(cache_name):
    ''' Opens the cache file if it exists and loads the JSON into the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(cache_name, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict, cache_name):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(cache_name,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def cache_find(key):
    CACHE_FILENAME = "data_cache.json"
    CACHE_DICT = open_cache(CACHE_FILENAME)
    if key in CACHE_DICT.keys():
        print("Cache hit")
        print("Using cache")
    else:
        print("Cache miss")
        if key == "team":
            team_dict = scrape_team()
            CACHE_DICT['team'] = team_dict
        if key == "schedule":
            schedule_dict = scrape_schedule()
            CACHE_DICT['schedule'] = schedule_dict
        if key == "stats":
            stats_dict = scrape_stats()
            CACHE_DICT['stats'] = stats_dict
        if key == "rosters":
            roster_dict = scrape_rosters()
            CACHE_DICT['rosters'] = roster_dict
        save_cache(CACHE_DICT, CACHE_FILENAME)
    return CACHE_DICT[key]

def cache_remove(key):
    CACHE_FILENAME = "data_cache.json"
    CACHE_DICT = open_cache(CACHE_FILENAME)
    if key in CACHE_DICT.keys():
        print("remove " + key)
        del CACHE_DICT[key]
        save_cache(CACHE_DICT, CACHE_FILENAME)

def get_soup(url):
    CACHE_FILENAME = "cache.json"   
    CACHE_DICT = open_cache(CACHE_FILENAME)
    if url not in CACHE_DICT.keys():
        print("Crawling")
        response = requests.get(url)
        CACHE_DICT[url] = response.text
        save_cache(CACHE_DICT, CACHE_FILENAME)
    else:
        print("Caching find page")
    soup = BeautifulSoup(CACHE_DICT[url], "html.parser")
    return soup

def scrape_team():
    url = "https://www.nfl.com/teams"
    soup = get_soup(url)
    team_lists_parent = soup.findAll('h4', class_="d3-o-media-object__roofline nfl-c-custom-promo__headline")
    sites_list_parent = soup.findAll('a', class_="d3-o-media-object__link d3-o-button nfl-o-cta nfl-o-cta--primary")
    teams=[]
    sites=[]
    for team_parent in team_lists_parent:
        teams.append(team_parent.text.strip())
    for site_parent in sites_list_parent:
        site_url = site_parent['href']
        if site_url[0] != 'h':
            site = "https://www.nfl.com"+site_url
            sites.append(site)
        else:
            sites.append(site_url)    
    j = 0
    team_dict={}
    for i in range(len(teams)):
        team_dict[teams[i]] = [sites[j], sites[j+1]] 
        j += 2

    return team_dict

def scrape_schedule():
    schedule_dict = {}

    team_dict = cache_find("team")
    for team in team_dict.keys():
        base_url = team_dict[team][1]
        schedule_url = base_url + "schedule/2020/"
        soup = get_soup(schedule_url)
        matches_parents = soup.findAll('div', class_="d3-l-col__col-12")

        match = []
        for matches in matches_parents:
            info = []
            team2 = matches.find('p', class_="nfl-o-matchup-cards__team-short-name")
            time = matches.find('span', class_="nfl-o-matchup-cards__date-info--date")
            if team2 != None and time != None:
                info.append(team2.text.strip())
                info.append(time.text.strip()[2:])
                info.append("2020")
                match.append(info)
        schedule_dict[team]=match
    return schedule_dict

def scrape_stats():
    years_stats = {}
    year = 2005
    while year <= 2020:
        url = f"https://www.nfl.com/stats/team-stats/offense/passing/{year}/reg/all"
        soup = get_soup(url)
        rows = soup.findAll('tr')

        stats = {}
        for row in rows:
            team = row.find('div', class_="d3-o-club-shortname")
            data = row.findAll('td')
            if team != None and data != []:
                team = team.text.strip()
                data = data[6].text.strip()
                stats[team] = data
        years_stats[year]=stats
        year += 1
    return years_stats

def scrape_rosters():
    roster_dict = {}

    team_dict = cache_find("team")
    for team in team_dict.keys():
        base_url = team_dict[team][1]
        team_url = base_url + "team/stats/"

        soup = get_soup(team_url)
        rushing_player = soup.findAll('div', class_="nfl-o-teamstats")[1]
        rows = rushing_player.findAll('tr')

        team_player = []
        for row in rows:
            info = []
            player = row.find('span', class_="nfl-o-roster__player-name")
            data = row.findAll('td')
            
            if player != None and data != []:
                TD = data[5]
                ATT = data[1]
                player = player.text.strip()
                TD = TD.text.strip()
                ATT = ATT.text.strip()
                info.append(player)
                info.append(TD)
                info.append(ATT)
            if info != []:
                team_player.append(info)        
        roster_dict[team] = team_player
    return roster_dict

def scrape_all():
    cache_remove('team')
    cache_remove('schedule')
    cache_remove('stats')
    cache_remove('rosters')
    cache_find('team')
    cache_find('schedule')
    cache_find('stats')
    cache_find('rosters')

if __name__ == "__main__":
    scrape_all()
