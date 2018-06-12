#-*- coding:utf-8 -*-#

from flask import render_template,url_for,Blueprint,flash,redirect,request, current_app, abort
from flask_login import login_required, current_user
from jobplus.models import User,Company,Job
from jobplus.forms import CompanyForm

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_company:
        flash('您不是企业用户！', 'warning')
        return redirect(url_for('front.index'))
    form = CompanyForm(obj=current_user.company)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)

@company.route('/', methods=['GET'])
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Company.query.paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False)
    
    #使用try来防止在没有建立数据库的情况下访问网页引发的错误
    #for future use
    #try:
    #    pagination = User.query.filter(User.role==User.ROLE_COMPANY).order_by(User.created_at.desc()).paginate(
     #           page=page,
      #          per_page=12,
       #         error_out=False
        #        )
    #except:
     #   return '<h2>No any data here</h2>'
    return render_template('company/index.html', pagination=pagination)

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company)

@company.route('/job/admin', methods=['GET', 'POST'])
@login_required
def company_admin():
    #这里设置的权限是只有企业才能有职位管理的接口
    #管理员虽然也有权限，但它的接口在控制台
    if current_user.role != 20:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=current_user.id).paginate(
            page = page,
            per_page = current_app.config['INDEX_PER_PAGE'],
            error_out = False
            )
    return render_template('company/admin.html', pagination=pagination)

