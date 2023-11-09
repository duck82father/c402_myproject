from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        # equest.form['content'] 코드는 POST 폼 방식으로 전송된 데이터 항목 중 name 속성이 content인 값을 의미한다.
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        # question.answer_set은 "질문에 달린 답변들"
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)