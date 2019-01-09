from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from wtforms import BooleanField, StringField, IntegerField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ('en_US', 'en')
    # Fields:
    username = StringField('User name', [validators.Length(min=4, max=25)])
    age = IntegerField('Age', [validators.NumberRange(min=18, max=150)])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
    sub_mittor = SubmitField("Check and register user ...")


@app.route('/', methods=["GET", "POST"])
def main():
    reg_form = RegistrationForm()
    # POST-processing:
    if request.method == 'POST':
        user_name = reg_form.username.data
        user_age = reg_form.age.data
        ok_chk = reg_form.accept_rules.data
        # DEBUG:
        print("Got user with name = '%s' and age = %s" % (user_name, user_age))
        acceptance = {True: "yes", False: "no"}
        print("Acceptance: %s" % acceptance[ok_chk])
        vali_date = reg_form.validate()
        if vali_date:
            print("Form data OK ...")
        else:
            print("Form data invalid!")
    # Rendering:
    return render_template('wtf_ex1.html', form=reg_form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

