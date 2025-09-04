from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date

app = Flask(__name__)

# In-memory storage for incidents (for demo purposes)
incidents = []

def calculate_incident_free_days():
    """Calculate the number of days since the last incident"""
    if not incidents:
        return None  # No incidents means "Incident-free year!"
    
    # Find the most recent incident date
    most_recent_date = None
    for incident in incidents:
        incident_date = datetime.strptime(incident['date'], '%Y-%m-%d').date()
        if most_recent_date is None or incident_date > most_recent_date:
            most_recent_date = incident_date
    
    # Calculate days since the most recent incident
    today = date.today()
    days_since = (today - most_recent_date).days
    return days_since

@app.route('/')
def index():
    # Get the department filter from query parameters
    department_filter = request.args.get('department', '')
    
    # Filter incidents by department if a filter is selected
    if department_filter:
        filtered_incidents = [incident for incident in incidents if incident['department'] == department_filter]
    else:
        filtered_incidents = incidents
    
    # Get unique departments from all incidents for the dropdown
    departments = sorted(list(set(incident['department'] for incident in incidents)))
    
    # Calculate incident statistics for the chart
    incident_stats = {'Health': 0, 'Safety': 0, 'Environmental': 0}
    for incident in filtered_incidents:
        incident_type = incident['type']
        if incident_type in incident_stats:
            incident_stats[incident_type] += 1
    
    # Calculate max value for chart scaling
    max_count = max(incident_stats.values()) if incident_stats.values() else 0
    
    # Calculate incident-free days
    incident_free_days = calculate_incident_free_days()
    
    return render_template('index.html', 
                         incidents=filtered_incidents, 
                         departments=departments,
                         selected_department=department_filter,
                         incident_stats=incident_stats,
                         max_count=max_count,
                         incident_free_days=incident_free_days)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        incident = {
            'type': request.form['type'],
            'description': request.form['description'],
            'date': request.form['date'],
            'department': request.form['department']
        }
        incidents.append(incident)
        return redirect(url_for('index'))
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
