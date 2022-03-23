from fastapi.testclient import TestClient
from application.main import app
from application.schemas import UserOut,Token
from jose import jwt
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
from application.config import settings
#from application.database import get_db, Base

#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

#engine = create_engine(SQLALCHEMY_DATABASE_URL)

#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)

#def override_get_db():
#    db = TestingSessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()

#app.dependency_overrides[get_db] = override_get_db






client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello world ;)"
   
# def test_create_user():
#    res = client.post("/users/", json={"email":"pj@example.com","password":"nepj"})
#    new_user = UserOut(**res.json())
#    assert res.status_code == 201
#    assert new_user.email == "pj@example.com"

def test_login():
    res = client.post("/login/", data={"username":"pj@example.com","password":"nepj"})
    user = Token(**res.json())
    print(user)
    payload = jwt.decode(user.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert payload == "nepj"
    assert res.status_code == 200
    assert user.token_type == "Bearer"