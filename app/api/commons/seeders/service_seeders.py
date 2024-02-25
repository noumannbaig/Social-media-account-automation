from sqlalchemy.sql import table
from datetime import datetime
import sqlalchemy as sa
import uuid
from app.api.services.db_models import Services
from app.database.session import update_session ,delete_entity
from fastapi import Depends
from app.database.session import SessionLocal
from app.database.session import get_db
from sqlalchemy.orm import Session

def seed_services_data(session: Session):
    services = table('services',
        sa.Column('id', sa.String()),
        sa.Column('name', sa.String()),
        sa.Column('descripton', sa.String()),
        sa.Column('priority', sa.Integer()),
        sa.Column('is_active', sa.Boolean()),
        sa.Column('create_time', sa.DateTime()),
        sa.Column('update_time', sa.DateTime()),
    )
    data=  [
            {
                'id': str(uuid.uuid4()),
                'name': 'Web App Development',
                'descripton': 'Description for Web App Development',
                'is_active': True,
                'priority':0,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Mobile App Development',
                'descripton': 'Description for Mobile App Development',
                'is_active': True,
                'priority':1,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Education Technology',
                'descripton': 'Description for Education Technology',
                'is_active': True,
                'priority':2,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Web Scraping',
                'descripton': 'Description for Web Scraping',
                'is_active': True,
                'priority':3,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Data and Artificial Intelligence',
                'descripton': 'Description for Data and AI',
                'is_active': True,
                'priority':4,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'QA and Software Testing',
                'descripton': 'Description for QA and Testing',
                'is_active': True,
                'priority':5,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'UX, Product and Design',
                'descripton': 'Description for UX and Design',
                'is_active': True,
                'priority':6,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Enterprise Software Development',
                'descripton': 'Description for Enterprise Software',
                'is_active': True,
                'priority':7,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'MVP for Startups',
                'descripton': 'Description for MVP Startups',
                'is_active': True,
                'priority':8,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Custom Devops Solutions',
                'descripton': 'Description for Custom Devops',
                'is_active': True,
                'priority':9,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'E-commerce Solutions',
                'descripton': 'Description for E-commerce',
                'is_active': True,
                'priority':10,
                'create_time': datetime.utcnow(),
                'update_time': datetime.utcnow(),
            },
        ]
    for entry in data:
        session.execute(
            sa.insert(services).values(
                id=entry['id'],
                name=entry['name'],
                descripton=entry['descripton'],
                is_active=entry['is_active'],
                priority=entry['priority'],
                create_time=entry['create_time'],
                update_time=entry['update_time'],
            )
        )
    
    session.commit()
    
