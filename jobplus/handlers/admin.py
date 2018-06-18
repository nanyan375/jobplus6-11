# -*- coding: utf-8 -*-

from flask import Blueprint, render_template,url_for,request, redirect, flash
from flask_login import current_user
from jobplus.decorators import admin_required
from jobplus.models import db,User,Job
from jobplus.forms import UserForm, UserRegisterForm, CompanyRegisterForm, \
                            CompanyEditForm, UserEditForm, JobForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/admin_base.html')

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
            page=page,
            per_page=20,
            error_out=False)
    return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/adduser', methods=['GET','POST'])
@admin_required
def add_user():
    form = UserRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('增加求职者成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html', form=form)

@admin.route('/users/addcompany', methods=['GET','POST'])
@admin_required
def add_company():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('增加企业成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_company.html', form=form)

@admin.route('/users/<int:user_id>/edituser',methods=['GET','POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_company:
        form = CompanyEditForm(obj=user)
    else:
        form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.update(user)
        flash('编辑用户成功！', 'success')
        return redirect(url_for('admin.users'))
    #if user.is_company:
        #form.site.data = user.company_detail.site
        #form.desription = user.company_detail.description
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/user/<int:user_id>/edituser', methods=['GET', 'POST'])
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('已经成功启用用户', 'success')
    else:
        user.is_disable = True
        flash('已经成功禁用用户', 'success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.paginate(
            page=page,
            per_page=20,
            error_out=False)
    return render_template('admin/jobs.html', pagination=pagination)

@admin.route('jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功！', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('admin/edit_job.html', form=form, job=job)

@admin.route('jobs/add', methods=['GET', 'POST'])
@admin_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(current_user)
        flash('职位发布成功！', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('admin/job_add.html', form=form)