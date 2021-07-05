  
from pybo import db

#db shape, sql object - row order (id, subject, content, create_date)
#real db is column oriented dbms
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True) #for id, primary_key used
    subject = db.Column(db.String(200), nullable=False) #nullable false to set variable not null
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False) 

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE')) #use foreignkey to connect question model, model's id, delete option
    question = db.relationship('Question', backref=db.backref('answer_set')) #use db relationship to reference question model
    #backref is dereference, use this to reference from question model to answer model
    content = db.Column(db.Text(), nullable=False) 
    create_date = db.Column(db.DateTime(), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)