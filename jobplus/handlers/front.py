# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, url_for, render_template, flash
from jobplus.forms import LoginForm, CompanyRegisterForm, UserRegisterForm
from flask_login import login_user, login_required, logout_user
from jobplus.models import User,Company, Job

front=Blueprint('front',__name__)

@front.route('/')
def index():
    companies = Company.query.order_by(Company.created_at.desc()).all()[:12]
    return render_template('index.html', companies=companies)

@front.route('/latest_jobs')
def latest_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()[:9]
    return render_template('latest_jobs.html', jobs=jobs)

@front.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        if user.is_company:
            return redirect(url_for('company.profile'))
        else:
            return redirect(url_for('user.profile'))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经成功退出登录', 'success')
    return redirect(url_for('.index')) 

@front.route('/companyregister', methods=['GET', 'POST'])
def company_register():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('企业注册成功', 'success')
        return redirect(url_for('.company_register'))
    return render_template('company_register.html', form=form)

@front.route('/userregister', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户注册成功', 'success')
        return redirect(url_for('.user_register'))
    return render_template('user_register.html', form=form)
