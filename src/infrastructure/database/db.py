from domain.models.customer import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(OperationalError),
)
def create_engine_session_factory(user, password, host, db_name, port):
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(url, 
                           echo=False,
                           poolclass=QueuePool,
                           pool_size=10,       
                           max_overflow=5,      
                           pool_timeout=30,
                           pool_recycle=1800)
    Base.metadata.create_all(engine) 
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
    return SessionLocal
