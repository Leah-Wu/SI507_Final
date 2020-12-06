from flask import Flask
from flask import render_template
from flask import request
import process_data as data
import time
import os
import CreateDatabase

# Initialize database:
# CreateDatabase.fillup_database()
app = Flask("__NFL__")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/func1")
def func1():
    team_list = data.find_rosters_team()
    return render_template('func1.html', team_list = team_list, flag=False)

@app.route("/handle_func1", methods=['POST'])
def handle_func1():
    team = request.form["team"]
    # mode = request.form["mode"]
    fig = data.top_rosters(team)
    new_graph_name = save_plot(fig)
    return render_template('func1.html', flag=True, graph=new_graph_name)

def save_plot(fig):
    new_graph_name = "graph" + str(time.time()) + ".png"
    for filename in os.listdir('static/'):
        if filename.startswith('graph'):  # not to remove other images
            os.remove('static/' + filename)
    fig.write_image('static/'+new_graph_name)
    return new_graph_name

@app.route("/func2")
def func2():
    team_list = data.find_rosters_team()
    return render_template('func2.html', team_list = team_list, flag=False)

@app.route("/handle_func2", methods=['POST'])
def handle_func2():
    team_list = request.form.getlist("team")
    fig = data.team_roster_performance(team_list)
    new_graph_name = save_plot(fig)
    return render_template('func2.html', flag=True, graph=new_graph_name)

@app.route("/func3")
def func3():
    return render_template('func3.html', flag=0)

@app.route("/handle_func3", methods=['POST'])
def handle_func3():
    if "year" in request.form:
        year = request.form["year"]
        if year == "":
            team_list = []
        else:
            team_list = data.select_teams_in_year(year)
        return render_template('func3.html', team_list=team_list,flag=1)
    team_list = request.form.getlist("team")
    year = request.form["year2"]
    fig = data.compare_team_performance(team_list, year)
    new_graph_name = save_plot(fig)
    return render_template('func3.html', flag=2, graph=new_graph_name)

@app.route("/func4")
def func4():
    team_list = data.team_history_available()
    return render_template('func4.html', team_list=team_list, flag=False)

@app.route("/handle_func4", methods=['POST'])
def handle_func4():
    team = request.form["team"]
    year = request.form["year"]
    if year == "":
        return render_template('func4.html', results=False, flag=True)

    years = year.split('-')
    if len(years) != 2:
        return render_template('func4.html', results=False, flag=True)
    start_year = years[0]
    end_year = years[1]
    if start_year < '2005' or end_year > '2020' or start_year > end_year:
        return render_template('func4.html', results=False, flag=True)
    fig = data.team_performace_history(team, start_year, end_year)
    new_graph_name = save_plot(fig)
    return render_template('func4.html', results=True, flag=True, graph=new_graph_name)

@app.route("/func5")
def func5():
    team_list = data.schedule_available_team()
    return render_template('func5.html', team_list=team_list,flag=False)

@app.route("/handle_func5", methods=['POST'])
def handle_func5():
    team = request.form["team"]
    headers, results = data.team_schedule(team)
    return render_template('func5.html', flag=True, headers=headers,data=results)

if __name__ == "__main__":
    app.run(debug=True)
