from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello') #route address blueprint object
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/') #메인페이지가 질문 리스트로 리디렉션
def index():
    return redirect(url_for('question._list')) # 메인페이지를 question list로 리디렉트