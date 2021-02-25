import sqlalchemy
import databases
from sqlalchemy.schema import ForeignKey
import os

# файл для работы с базой данных. Описана точка входа в бд, само подключение,
# а так же модели сущностей

DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    os.environ['POSTGRES_USER'],
    os.environ['POSTGRES_PASSWORD'],
    os.environ['POSTGRES_SERVER'],
    os.environ['POSTGRES_DB']
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

abonents = sqlalchemy.Table(
    'abonents',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("photo", sqlalchemy.String),
    sqlalchemy.Column("sex", sqlalchemy.String),
    sqlalchemy.Column("birth", sqlalchemy.Date),
    sqlalchemy.Column("live", sqlalchemy.Text)
)

phones = sqlalchemy.Table(
    'phones',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "ab_id",
        sqlalchemy.Integer,
        ForeignKey("abonents.id", onupdate="CASCADE", ondelete="CASCADE")),
    sqlalchemy.Column("type", sqlalchemy.String),
    sqlalchemy.Column("number", sqlalchemy.String)
)

mails = sqlalchemy.Table(
    'mails',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "ab_id",
        sqlalchemy.Integer,
        ForeignKey("abonents.id", onupdate="CASCADE", ondelete="CASCADE")),
    sqlalchemy.Column("type", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String)
)
