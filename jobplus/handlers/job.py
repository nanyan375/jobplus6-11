from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, abort
from jobplus.models import db, Job, User, Delivery
from flask_login import current_user,login_required
from jobplus.forms import LoginForm

job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False)
    return render_template('job/index.html', pagination=pagination)

#企业的详情页面需要登录才能进入，这是为了针对不同的角色而展示不同的
#页面。例如，对求职者显示投简历按钮，对企业显示上线／下线按钮。
@job.route('/<int:job_id>')
@login_required
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)

@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    if current_user.is_authenticated:
        if current_user.role != User.ROLE_USER:
            abort(404)      
        job = Job.query.get_or_404(job_id)
        # user = User.query.get_or_404(current_user.id)
        delivery = Delivery()
        delivery.job_id = job.id
        delivery.user_id = current_user.id
        delivery.company_id = job.company_id
        db.session.add(delivery)
        # job.users.append(user)
        db.session.commit()
        flash('你已成功申请该职位', 'success')
        return redirect(url_for('job.detail', job_id=job_id))
        #return render_template("job/detail.html", job=job)
    else:
        form = LoginForm()
        return render_template("login.html", form=form)

@job.route('<int:job_id>/enable', methods=['GET', 'POST'])
@login_required
def enable_job(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.role == 10:
        return '<h1>You are not authorized to do it!</h1>', 401
    elif current_user.role == 20:
        job.is_disable = False
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("job.detail", job_id=job.id))
    else:
        job.is_disable = False
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('admin.jobs'))

@job.route('<int:job_id>/disable', methods=['GET', 'POST'])
@login_required
def disable_job(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.role == 10:
        return '<h1>You are not authorized to do it!</h1>', 401
    elif current_user.role == 20:
        job.is_disable = True
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("job.detail", job_id=job.id))
    else:
        job.is_disable = True
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('admin.jobs'))

