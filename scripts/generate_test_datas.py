import os
import json
from random import randint
#from faker import Faker
from jobplus.models import db, User, Job, Company

#fake = Faker()

user_lst = [
            ['admin', 'admin', 'admin@example.com', 'jobplus', 30],
            ['ABC', 'company1', 'abc@example.com', 'jobplus', 20],
            ['Jack Lee', 'user1', 'jacklee@example.com', 'jobplus', 10],
            ['Jack Ma', 'user2', 'jackma@example.com', 'jobplus', 10]
           ]

def iter_users():
    for user in user_lst:
        yield User(
            name=user[0],
            username=user[1],
            email=user[2],
            password=user[3],
            role=user[4]
    )

def iter_companies():
    user = User.query.filter_by(name='ABC').first()
    yield Company(
        location='Beijing',
        logo='test',
        user_id=user.id
    )
        
def iter_jobs():
    company = User.query.filter_by(name='ABC').first()
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'jobs.json'), encoding='utf-8') as f:
        jobs = json.load(f)
    for job in jobs:
        yield Job(
            title=job['title'],
            salary=job['salary'],
            location=job['location'],
            experience=job['experience'],
            company=company
        )

 
def run(): 
    db.create_all()
    for user in iter_users():
        db.session.add(user)
    
    for company in iter_companies():
        db.session.add(company)   
    
    for job in iter_jobs():
        db.session.add(job)
    
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
