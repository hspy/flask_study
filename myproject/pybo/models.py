  
from pybo import db

#db shape, sql object - row order (id, subject, content, create_date)
#real db is column oriented dbms

#table object
#no duplicate data
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True) #for id, primary_key used
    subject = db.Column(db.String(200), nullable=False) #nullable false to set variable not null
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True) #modify
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set')) # secondary, voter이 다대다 관계임, backref
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) #질문자 아이디 값을 question model에 포함, 해당 유저 모델이 삭제되면 질문 모델 데이터도 삭제
    user = db.relationship('User', backref=db.backref('question_set')) #QUESTION 모델에서 유저 모델 참조 (이렇게 해서 유저 정보를 불러옴)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE')) #use foreignkey to connect question model, model's id, delete option
    question = db.relationship('Question', backref=db.backref('answer_set')) #use db relationship to reference question model
    #backref is dereference, use this to reference from question model to answer model
    content = db.Column(db.Text(), nullable=False) 
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True) #modify
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))

