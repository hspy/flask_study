from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request #앱 요청 전에 로그인되었는지 확인
def load_logged_in_user(): 
    user_id = session.get('user_id') #세션 확인
    if user_id is None: #로그인 되었는지 확인
        g.user = None
    else:
        g.user = User.query.get(user_id) #글로벌 컨텍스트


@bp.route('/signup/', methods=('GET', 'POST')) #회원가입 페이지
def signup():
    form = UserCreateForm() #회원가입 폼
    if request.method == 'POST' and form.validate_on_submit(): #유효성 검사
        user = User.query.filter_by(username=form.username.data).first() #동일한 유저명이 있다면, 유저에 대한 id를 return
        if not user: # 존재하지 않는 유저명이라면 (가입이 가능하다면)
            user = User(username=form.username.data, 
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data) #회원가입할 수 있도록 (비밀번호는 해시 암호화 처리)
            db.session.add(user) #db에 추가
            db.session.commit() #db 커밋
            return redirect(url_for('main.index')) #메인페이지로 리디렉션
        else:
            flash('이미 존재하는 사용자입니다.') #메세지
    return render_template('auth/signup.html', form=form) #다시 회원가입 페이지로


@bp.route('/login/', methods=('GET', 'POST')) # 로그인 페이지
def login():
    form = UserLoginForm() #로그인폼
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first() #존재하지 않으면 -1 리턴
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): #존재하면 해당 아이디의 비밀번호가 맞는지
            error = "비밀번호가 올바르지 않습니다."
        if error is None: #모두 맞다면
            session.clear() #세션 clear
            session['user_id'] = user.id #아이디에 대한 세션 생성
            return redirect(url_for('main.index')) #메인페이지로
        flash(error)
    return render_template('auth/login.html', form=form) #다시 로그인 페이지로

@bp.route('/logout/') #logout 
def logout():
    session.clear() # session end
    return redirect(url_for('main.index')) #메인페이지로 복귀

def login_required(view): #데코레이터 함수
    @functools.wraps(view)
    def wrapped_view(**kwargs): #래펒
        if g.user is None:
            return redirect(url_for('auth.login')) # 로그인이 안된 상태면 로그인 페이지로 이동
        return view(**kwargs)
    return wrapped_view