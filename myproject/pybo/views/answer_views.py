# 답변을 위한 view 파일
from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from ..models import Question, Answer
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('GET', 'POST')) #method 속성은 Get과 POST 로 맞춰줘야 함 (question form으로 인해 GET 추가)
@login_required # 로그인이 되어있는지 애너테이션을 통해 확인
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) #해당 질문 아이디가 있는지
    if form.validate_on_submit(): #유효하다면
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user) #답변 저장, 유저명 추가
        question.answer_set.append(answer)
        db.session.commit() #디비에 추가
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)