from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///students.db", echo=True)

Session=sessionmaker(bind=engine)
db=Session()

Base=declarative_base()

def get_db():
    db=Session()
    try:
        yield db
    finally:
        db.close()