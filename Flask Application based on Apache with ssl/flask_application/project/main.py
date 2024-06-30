from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name, email=current_user.email)

@main.route('/edit')
@login_required
def edit():
  return render_template('edit.html', name=current_user.name, email=current_user.email)

@main.route('/edit', methods=['POST'])
@login_required
def edit_post():
    email = request.form.get('email')
    name = request.form.get('name')
    existing_password= request.form.get('existing_password')
    new_password = request.form.get('new_password')
    repeat_password = request.form.get('repeat_password')

    edited_user = User.query.filter_by(email=email).first()

    if edited_user and not (edited_user==current_user):
        flash('Email address already exists')
        return render_template('edit.html', name=current_user.name, email=current_user.email)

    if existing_password and new_password and repeat_password:
        if check_password_hash(current_user.password, existing_password):
            if new_password==repeat_password:
                new_password_hash = generate_password_hash(new_password, method='pbkdf2')
                current_user.password = new_password_hash
            else:
                flash('The values of New Password and Confirm Password should be the same')
                return render_template('edit.html', name=current_user.name, email=current_user.email)
        else:
            flash('Your current password does not match with the '
            'password you providedd. Please try again.')
            return render_template('edit.html', name=current_user.name, email=current_user.email)
    elif existing_password and new_password:
        flash('You did not confirm your new password')
        return render_template('edit.html', name=current_user.name, email=current_user.email)
    elif existing_password:
        flash('You did not provide new password')
        return render_template('edit.html', name=current_user.name, email=current_user.email)

    current_user.email = email
    current_user.name = name
    db.session.commit()

    return redirect(url_for('main.profile'))