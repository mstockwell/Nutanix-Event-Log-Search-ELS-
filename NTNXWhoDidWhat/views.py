from NTNXWhoDidWhat import app
from WdWController import test_credentials, get_events_data
from flask import request, render_template, redirect, url_for, session


@app.route('/', methods=['GET', 'POST'])
def homepage():
    error = None
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        try:
            status, cluster_info = test_credentials(username, password, ip_address)
            session["cluster_name"] = cluster_info.get('name')
            if status == 200:
                return redirect(url_for('querymainpage', cluster_name=session["cluster_name"]))
            else:
                return render_template("error.html", error=status)
        except Exception as e:
            return render_template("error.html", error=str(e))
    return render_template('homepage.html', error=error)


@app.route('/querymainpage', methods=['GET', 'POST'])
def querymainpage():
    error = None
    if request.method == 'POST':
        investigate_date = request.form['investigate_date']
        if investigate_date != "":
            events = get_events_data(investigate_date)
            return render_template('results.html', cluster_name=session["cluster_name"], num_events=len(events),
                                   events_list=events,
                                   investigate_date=investigate_date)
        else:
            error = "You must enter a valid date to seach"
            return render_template('querymainpage.html', cluster_name=session["cluster_name"], error=error)
    else:
        return render_template('querymainpage.html', cluster_name=session["cluster_name"], error=error)
