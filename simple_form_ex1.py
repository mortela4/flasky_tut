from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


app = Flask(__name__)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])


@app.route('/', methods=["GET", "POST"])
def main():
    name_and_age = MyForm()
    return render_template('simple_form_ex1.py.html', form=name_and_age)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

