from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    deadline = db.Column(db.DateTime, default=datetime.now, nullable=False)  # Default to today's date

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        deadline_str = request.form['deadline']
        deadline = datetime.strptime(deadline_str, '%d/%m/%Y')
        task = Task(title=title, desc=desc, deadline=deadline)
        db.session.add(task)
        db.session.commit()
    allTask = Task.query.all()
    today_date = datetime.now().strftime('%d/%m/%Y')  # Format today's date as dd/mm/yyyy
    return render_template('index.html', allTask=allTask, today_date=today_date)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    task = Task.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        deadline_str = request.form['deadline']
        deadline = datetime.strptime(deadline_str, '%d/%m/%Y')
        task.title = title
        task.desc = desc
        task.deadline = deadline
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    return render_template('update.html', task=task)

@app.route('/delete/<int:sno>')
def delete(sno):
    task = Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
