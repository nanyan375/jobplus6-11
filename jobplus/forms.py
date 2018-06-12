from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,\
                    IntegerField,ValidationError,SelectField,DateTimeField
from wtforms.validators import Length, Email, Required, EqualTo, NumberRange, URL
from jobplus.models import db, User, Company, Job

class LoginForm(FlaskForm):
    email=StringField('邮箱',validators=[Required(),Email()])
    password=PasswordField('密码',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交') 

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱没有注册！')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user: #and not user.check_password(field.data):
            raise ValidationError('密码错误')

class UserForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(5, 32)])
    name = StringField('姓名', validators=[Required(), Length(5, 32)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    mobile = IntegerField('手机号', validators=[Required(), NumberRange(min=11, message='无效的手机号')])
    work_year = IntegerField('工作年限', validators=[Required()])
    resume_url = StringField('简历链接', validators=[Required(), URL()])
    submit = SubmitField('提交')
    
    def add_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    

class CompanyForm(FlaskForm):
    username = StringField('用户名', validators=[Required()])
    name = StringField('企业名称', validators=[Required()])
    email = StringField('企业邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填则保持不变)')
    description = StringField('简要描述', validators=[Required(), Length(8,150)])
    location = StringField('企业地址', validators=[Required()])
    workers_num = SelectField('企业规模', choices=[('small','1~50'),('middle','51~100'),('big','101~200'), ('huge','200+')])
    logo = StringField('LOGO', validators=[Required(), URL()])
    site = StringField('企业网址', validators=[URL()])
    field = StringField('公司领域', validators=[Required()])
    tags = StringField('公司技术标签(最多不超过十个，用空格隔开)', validators=[Required()])
    finance_stage = SelectField('融资进度', choices=[('p','初创企业'), ('a', '融资A轮'), ('b', '融资B轮'), ('c', '融资C轮'),('s','已上市')])
    welfares = StringField('公司福利(最多不超过十个，用空格隔开)', validators=[Required()])
    submit = SubmitField('提交')
    
    def add_company(self):
        company = Company()
        user = User()
        user.role = 20
        self.populate_obj(user)
        self.populate_obj(company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
        return company
    
    def update_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        
        #如果密码填写了就要改变密码
        if self.password.data:
            user.password = self.password.data

        #先判断公司数据是否是第一次建立
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id
        self.populate_obj(obj=company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()

class CompanyRegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    name = StringField('企业名称', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    location = StringField('所在地', validators=[Required()])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def create_company(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    role=20)
        company = Company(location=self.location.data)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
        #return user

class CompanyEditForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Length(6,24)])
    name = StringField('企业名称', validators=[Length(3, 24)])
    mobile = StringField('电话')
    site = StringField('企业网站', validators=[URL()])
    description = StringField('企业简介', validators=[Length(6, 128)])
    submit = SubmitField('保存')

    def update(self, company):
        company.name = self.name.data
        company.email = self.email.data
        company.mobile = self.mobile.data

        if self.password.data:
            company.password = self.password.data

        if company.company_detail:
            company_detail = company.company_detail
        else:
            company_detail = Company()
            company_detail.user_id = company.id
        company_detail.site = self.site.data
        company_detail.description = self.description.data
        db.session.add(company)
        db.session.add(company_detail)
        db.session.commit()

class UserRegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    name = StringField('姓名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def create_user(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    role=10)
        db.session.add(user)
        db.session.commit()
        return user

class UserEditForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Length(6,24)])
    name = StringField('姓名', validators=[Length(3, 24)])
    mobile = StringField('手机')
    submit = SubmitField('保存')

    def update(self, user):
        self.populate_obj(user)
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()

class JobForm(FlaskForm):
    title = StringField('职位名称', validators=[Required(), Length(3, 24)])
    salary = SelectField('工资水平', choices=[
        ('a', '3000以下'),
        ('b', '3000-5000'), 
        ('c', '5000-8000'),
        ('d', '8000-12000'), 
        ('e', '12000以上')
        ])
    experience = SelectField('工作经验', choices=[
        ('a', '不需要工作经验'), 
        ('b', '1-3年'),
        ('c', '3-5年'),
        ('d', '5-10年'),
        ('e', '10年以上')
        ])
    desc = StringField('职位描述', validators=[Length(8, 256)])
    requirement = StringField('职位要求', validators=[Length(8, 256)])
    submit = SubmitField('发布')

    def create_job(self, company):
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job
