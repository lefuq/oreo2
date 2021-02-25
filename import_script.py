from sqlalchemy.ext.automap import automap_base
from adbk.database import engine, metadata
from sqlalchemy.orm import sessionmaker
import csv

metadata.reflect(engine, only=['abonents', 'mails', 'phones'])
Sessionloc = sessionmaker(autocommit=True, autoflush=False, bind=engine)

Base = automap_base(metadata=metadata)
Base.prepare()

Abonent, Phone, Mail = Base.classes.abonents, Base.classes.phones, \
    Base.classes.mails

with open('99-contacts-addressees.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    s = Sessionloc()
    objs = []
    for row in reader:
        obj = Abonent(
            name=row[0],
            sex=row[1],
            live=row[2],
            photo=row[3],
            birth=row[4])
        objs.append(obj)
    s.bulk_save_objects(objs)

with open('99-contacts-phones.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    s = Sessionloc()
    objs = []
    for row in reader:
        obj = Phone(ab_id=row[0], number=row[1], type=row[2])
        objs.append(obj)
    s.bulk_save_objects(objs)

with open('99-contacts-mails.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    s = Sessionloc()
    objs = []
    for row in reader:
        obj = Mail(ab_id=row[0], address=row[1], type=row[2])
        objs.append(obj)
    s.bulk_save_objects(objs)
