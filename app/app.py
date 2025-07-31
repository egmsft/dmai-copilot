from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for incidents (for demo purposes)
incidents = []

@app.route('/')
def index():
    return render_template('index.html', incidents=incidents)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        incident = {
            'type': request.form['type'],
            'description': request.form['description'],
            'date': request.form['date']
        }
        incidents.append(incident)
        return redirect(url_for('index'))
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
