from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = "postgresql://username:password@host:port/database_name"
DATABASE_URL = "postgresql://postgres:password123@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
