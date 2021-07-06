from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question

from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')


# 라우트 함수로 페이지 구현

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc()) #get question list by using Question.query
    question_list = question_list.paginate(page, per_page=10) # 페이지 당 10개 출력
    return render_template('question/question_list.html', question_list=question_list) #question list render, render html


@bp.route('/detail/<int:question_id>/') #id 별 question detail을 출력해주는 페이지
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) # 해당 question id 가 없을 경우 404 출력
    return render_template('question/question_detail.html', question=question, form=form) #question render, render html


@bp.route('/create/', methods=('GET', 'POST')) #질문 폼 생성, 메소드는 GET과 POST
@login_required # 로그인이 되어있는지 애너테이션을 통해 확인
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user) #유저 아이디 추가
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)