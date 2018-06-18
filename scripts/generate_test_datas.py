import os
import json
import random
from faker import Faker
from jobplus.models import db, User, Job, Company

fake = Faker()

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

def iter_users_company():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'companies.json'), encoding='utf-8') as f:
        users = json.load(f)
    for user in users:
        yield User(
            name = user['title'],
            username = fake.user_name(),
            email=fake.email(),
            role=User.ROLE_COMPANY,
            password = 'jobplus'
        )

def iter_companies():
    #users = User.query.filter_by(role=User.ROLE_COMPANY).all()
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'companies.json'), encoding='utf-8') as f:
        companies = json.load(f)
    for company in companies:
        user = User.query.filter_by(name=company['title']).first()
        yield Company(
            #name=company['title'],
            logo=company['logo'],
            site=company['site'],
            description=company['desc'],
            location=company['location'],
            field=company['field'],
            user = user
        )
        
def iter_jobs():
    companies = User.query.filter_by(role=User.ROLE_COMPANY).all()
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'jobs.json'), encoding='utf-8') as f:
        jobs = json.load(f)
    for job in jobs:
        company = random.choice(companies)
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

    for company_user in iter_users_company():
        db.session.add(company_user)
    
    for company in iter_companies():
        db.session.add(company)   
    
    for job in iter_jobs():
        db.session.add(job)
    
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
