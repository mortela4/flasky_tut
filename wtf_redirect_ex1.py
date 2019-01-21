from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from flask import flash

from wtforms import BooleanField, StringField, IntegerField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm
from flask_wtf import CSRFProtect


class RegistrationForm(FlaskForm):
    # Fields:
    username = StringField(label='User name', validators=[validators.Length(min=4, max=25)])
    age = IntegerField(label='Age', validators=[validators.NumberRange(min=18, max=150)])
    accept_rules = BooleanField(label='I accept the site rules', validators=[validators.InputRequired()])
    sub_mittor = SubmitField(label="Check and register user ...")
    # street_name = None
    # street_number = None
    # add_user = None


class RegistrationFormExtended(RegistrationForm):
    """ Avoids 'setattr()' usage etc. """
    # Fields:
    street_name = StringField(label='Street name', validators=[validators.Length(min=4, max=25)])
    street_number = IntegerField(label='Street number', validators=[validators.NumberRange(min=1, max=999)])
    add_user = SubmitField(label="Add user!")


app = Flask(__name__)
app.secret_key = "xyz"
csrf = CSRFProtect(app)
# csrf.init_app()
# csrf.generate_token()


@app.route('/step_two/<u_name>/<u_age>/<u_accept>', methods=["GET", "POST"])
@csrf.exempt
def step_two(u_name, u_age, u_accept):
    #
    print("Entering 'step_two() w. args: u_name=%s, u_age=%d and u_accept=%s ..." % (u_name, int(u_age), u_accept))
    #
    reg_form_ext = RegistrationFormExtended(csrf_enabled=False)
    print("Created new form = 'reg_form_ext' ...")
    #
    if request.method == 'POST':
        print("Handling step2 POST ...")
        streetname = reg_form_ext.street_name.data
        streetnum = reg_form_ext.street_number.data
        # DEBUG:
        print("Got street name: '%s' and street number = %d" % (streetname, streetnum))
        # Back to START:
        return redirect('/')
    print("Handling step2 GET ...")
    # Fill in form:
    if not u_accept:
        flash('ERROR: first step NOT taken!')
        return
    else:
        print("First step taken OK! Proceeding with u_name=%s, u_age=%d ..." % (u_name, int(u_age)))
        reg_form_ext.accept_rules.data = u_accept
        reg_form_ext.username.data = u_name
        reg_form_ext.age.data = u_age
        #
        print("Extending FORM ...")
        #
        # Rendering:
        return render_template('wtf_ex2_step2.html', form=reg_form_ext)


@app.route('/', methods=["GET", "POST"])
@csrf.exempt
def main():
    session['entry_ok'] = False
    reg_form = RegistrationForm(csrf_enabled=False)
    print("Now handling request: %s" % request)
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
            session['entry_ok'] = True
            print("Form data OK ...")
            name = reg_form.username.data
            age = reg_form.age.data
            accept = reg_form.accept_rules.data
            #
            return redirect(url_for('step_two', u_name=name, u_age=age, u_accept=accept))
        else:
            print("Form data invalid! Errors: %s" % reg_form.errors)
    # Rendering:
    return render_template('wtf_ex2_step1.html', form=reg_form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

