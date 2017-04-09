import json
from os import getenv
from sqlalchemy import Boolean, Column, DateTime, String, TypeDecorator, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

Base = declarative_base()


class Json(TypeDecorator):
    """
    Json class for storing json data
    """
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class Question(Base):
    """
    Question class.
    """
    __tablename__ = 'questions'
    id = Column(String(250), primary_key=True)
    question = Column(String(250))
    answer = Column(String(250))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    def update(self, id=None, question=None, answer=None, created_at=None, updated_at=None):
        if id is not None:
            self.id = id
        if question is not None:
            self.question = question
        if answer is not None:
            self.answer = answer
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


class JobApplication(Base):
    """
    JobApplication class.
    """
    __tablename__ = 'job_applications'
    id = Column(String(250), primary_key=True)
    name = Column(String(255))
    applicant_responses = Column(Json(128))
    accepted = Column(Boolean())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())

    def update(self, id=None, name=None, applicant_responses=None, accepted=None, created_at=None, updated_at=None):
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if applicant_responses is not None:
            self.applicant_responses = applicant_responses
        if accepted is not None:
            self.accepted = accepted
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


def init_db(uri):
    """
    Initialize the database connection.
    """
    db_dir= getenv('DB_DIR', './data')
    db_file_name = getenv('DB_FILE_NAME', 'jobber.db')
    db_engine = 'sqlite:///{}/{}'.format(db_dir, db_file_name)
    engine = create_engine(db_engine, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session