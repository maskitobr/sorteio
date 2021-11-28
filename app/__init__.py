from app import models
from flask import Flask, _app_ctx_stack
from sqlalchemy.orm import scoped_session
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

from app import routes
