from flask import url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, 
            default=datetime.utcnow, 
            onupdate=datetime.utcnow)

user_job  = db.Table('user_job',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True))


class User(Base, UserMixin):
    __tablename__ = 'user'
    

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    name = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    work_year = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
    resume_url = db.Column(db.String(255), unique=True)
    company_detail = db.relationship('Company') 
    is_disable = db.Column(db.Boolean, default=False)
    jobs = db.relationship('Job', secondary=user_job, backref=db.backref('users'))

    def __repr__(self):
        return '<User:{}>'.format(self.username, uselist=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

class Job(Base):
    __tablename__ = 'job'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    salary = db.Column(db.String(32), nullable=False)
    experience = db.Column(db.String(128), default='经验不限')
    location = db.Column(db.String(128), nullable=False)
    is_disable = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('job', lazy='dynamic'))
    #company_detail = db.relationship('Company', uselist=False)
    
    @property
    def url(self):
        return url_for('job.detail', job_id=self.id)
    
    def __repr__(self):
        return '<Job:{}>'.format(self.name)

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    location = db.Column(db.String(64))
    scale = db.Column(db.String(64))
    workers_num = db.Column(db.String(32))
    logo = db.Column(db.String(255))
    site = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    field = db.Column(db.String(64))
    finance_stage = db.Column(db.String(64))
    welfares = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))
    #jobs = db.relationship('Job') #此行有用请勿隐藏

    @property
    def url(self):
        return url_for('company.detail', company_id=self.id)

    def __repr__(self):
        return '<Company: {}>'.format(self.name)
