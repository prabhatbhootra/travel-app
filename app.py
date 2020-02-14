from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

ENV='dev'

#Connecting to database
if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Prabhat1998@localhost/travel'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ornunldlzzbuis:423849f4566dcd5df093ad29bd3bdfd05efa1c4604707e85c8547186a28fda71@ec2-50-17-178-87.compute-1.amazonaws.com:5432/d84ooh1kgakn9d'

#Added to prevent warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creating database object
db = SQLAlchemy(app)

#Create model using class
class Feedback(db.Model):
    # to create feedback table quit pipenv shell in cli
    # type python to open interpreter and run commands
    #from app import db 
    # also run: db.create_all() to create feedback table
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    visitedAt = db.Column(db.Date)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    # This is constructor for class
    def __init__(self, title, visitedAt, rating, comments):
        self.title = title
        self.visitedAt = visitedAt
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        visitedAt = request.form['visitedAt']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(title, visitedAt, rating, comments)
        if title == '' or visitedAt == '':
            return render_template('index.html', message='Please make sure title and visited on are filled')
        if db.session.query(Feedback).filter(Feedback.title == title).count() == 0:
            data = Feedback(title, visitedAt, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='Please make sure new title is used')

@app.route('/journeys', methods=['GET'])
def getter():
    output = Feedback.query.all()
    return render_template('index.html', output_data = output)

if __name__ == '__main__':
    app.run()