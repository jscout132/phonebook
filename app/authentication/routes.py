from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

#partitioning our __init__.py 
@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            #intantiates the user class
            user = User(email, password = password)

            #db is using sql alchemy
            db.session.add(user)
            db.session.commit()

            #flash is a kind of pop up thing- i don't know if this is
            #actually going to work based on the videos
            #the second part of the flash statement talks to the application
            flash(f'You have successfully created a user account {email}','User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET','POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            #takes the email data, checks it against the 
            #formatting criteria, then query database to find the email
            #that matches the the user input
            logged_user = User.query.filter(User.email == email).first()
            
            #this checks if the password was the right password also checking to see if logged_user brings anything back
            #if logged_user is set as anything, it will come back truthy
            #and that's all this if statement is checking
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                #the second part of the flash statement talks to the application
                flash('You were successful in your login', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('you have failed in your attempt to access this content','auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data. Please check your form')
    return render_template('sign_in.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.him'))
