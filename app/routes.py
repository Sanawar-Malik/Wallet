from flask import render_template, request, flash, redirect, sessions, url_for, current_app
from app import app
from flask_login import login_user, logout_user, login_required,current_user
from wtforms import form
from app import db
from app.models import User, Wallet, Entry
from app.forms import RegisterForm, LoginForm
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
@app.route('/index')
@login_required
def wallet_page():
    our_users = User.query.all()
    # current user wallet show and entries show
    users = User.query.get(current_user.id)
    wallets = users.wallets.all()
    entries=users.entriesrelationuser.all()
    if(wallets == 1):
        print("Hello! I am an alert box!!")
    else:
        pass    
    return render_template('wallet.html', wallets=wallets, our_users=our_users, information=entries)
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('wallet_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('wallet_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)
@app.route('/wallet/', methods=['POST', 'GET'])
def create_wallet():
    if request.method == 'POST':
      name = request.form.get('name')
      balance = request.form.get('balance')
      wallets= Wallet(name=name, balance= balance, user_id=current_user.id)
      db.session.add(wallets)
      db.session.commit()
      return redirect(url_for('wallet_page'))
    return render_template('wallet.html', wallets=Wallet.query.all())  
@app.route('/wallet/<int:wallet_id>/entry/new', methods=['POST', 'GET'])
def create_entry(wallet_id):
    if request.method == 'POST':
      name = request.form.get('name')
      Entryamount = request.form.get('amount')
      selectOption= request.form.get('selector')
      balancedbq = Wallet.query.filter(Wallet.name == selectOption).first()
      num_rows_updated = Wallet.query.filter_by(name = selectOption).update(dict(balance= int(balancedbq.balance)-int(Entryamount)))
      print(num_rows_updated)
      entries= Entry(name=name, amount=Entryamount, wallet_id=wallet_id, userentries_id=current_user.id)
      db.session.add(entries)
      db.session.commit()
      return redirect(url_for('wallet_page'))
    return render_template('wallet.html')  
@app.route('/delete/<int:id>', methods=['POST'])
def user_delete(id):
    form = RegisterForm
    users = User.query.get_or_404(id)
    try:
        db.session.delete(users)
        db.session.commit()
        flash('User Deleted Successfully!!', category='danger')
        return render_template('home_page', form = form)
    except:
        flash('User Deleted error!!', category='danger')
        return render_template('home.html', form = form)
@app.route('/wallet/delete/<int:id>', methods=['POST'])
@login_required
def wallet_delete(id):
    wallets = Wallet.query.get_or_404(id)
    id == current_user.id
    try:
        db.session.delete(wallets)
        db.session.commit()
        flash('Wallet Deleted Successfully!!', category='success')
        return redirect(url_for('wallet_page'))
    except:
        return render_template('wallet.html')
@app.route('/entry/delete/<int:id>', methods=['POST'])
@login_required
def entry_delete(id):
    entries = Entry.query.get_or_404(id)
    id == current_user.id
    try:
        db.session.delete(entries)
        db.session.commit()
        flash('Entry Deleted Successfully!!', category='success')
        return redirect(url_for('wallet_page'))
        
    except:
        return render_template('wallet.html')
@app.route('/logout',  methods=['POST'])
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))