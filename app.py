from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for incidents (for demo purposes)
incidents = []

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
    
    return render_template('index.html', 
                         incidents=filtered_incidents, 
                         departments=departments,
                         selected_department=department_filter)

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
