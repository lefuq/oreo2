from .models import AbonentIn, PhoneIn, MailIn
from .database import abonents, phones, mails, database


# Блок словарей для эндпоинтов получения сущностей


ab_order_dict = {
    'id': abonents.c.id,
    'sex': abonents.c.sex,
    'birth': abonents.c.birth,
    'name': abonents.c.name,
    'photo': abonents.c.photo,
    'live': abonents.c.live,
    None: None}

ph_order_dict = {
    'id': phones.c.id,
    'ab_id': phones.c.ab_id,
    'type': phones.c.type,
    'number': phones.c.number,
    None: None}

ml_order_dict = {
    'id': mails.c.id,
    'ab_id': mails.c.ab_id,
    'type': mails.c.type,
    'address': mails.c.address,
    None: None}


# Блок CRUD-операций для абонентов


async def create_abonent(abonent: AbonentIn):
    query = abonents.insert().values(
        name=abonent.name,
        photo=abonent.photo,
        sex=abonent.sex,
        birth=abonent.birth,
        live=abonent.live
    )
    return await database.execute(query)


async def read_abonent(id: int):
    query = abonents.select().where(abonents.c.id == id)
    return await database.fetch_one(query)


async def read_abonents(ordering: str = None, page: int = 1, opp: int = 10):
    if ordering and ordering.startswith('-'):
        # читаем параметр сортировки (если был подан; и был ли он обратным)
        # читаем номер страницы, если был задан
        # дефолтное ограничение по выводу на страницу - 10 записей
        query = abonents.select()\
            .order_by(ab_order_dict[ordering[1:]].desc())\
            .limit(opp).offset(opp*(page-1))
    else:
        query = abonents.select()\
            .order_by(ab_order_dict[ordering])\
            .limit(opp).offset(opp*(page-1))
    return await database.fetch_all(query)


async def update_abonent(id: int, abonent: AbonentIn):
    query = (
        abonents
        .update()
        .where(abonents.c.id == id)
        .values(
            name=abonent.name,
            photo=abonent.photo,
            sex=abonent.sex,
            birth=abonent.birth,
            live=abonent.live)
        .returning(abonents.c.id))
    return await database.execute(query)


async def delete_abonent(id: int):
    query = abonents.delete().where(abonents.c.id == id)
    return await database.execute(query)


# Блок CRUD-операций для телефонов


async def create_phone(phone: PhoneIn):
    query = phones.insert().values(
        ab_id=phone.ab_id,
        type=phone.type,
        number=phone.number,
    )
    return await database.execute(query)


async def read_phone(id: int):
    query = phones.select().where(phones.c.id == id)
    return await database.fetch_one(query)


async def read_phones(ordering: str = None, page: int = 1, opp: int = 10):
    if ordering and ordering.startswith('-'):
        # читаем параметр сортировки (если был подан; и был ли он обратным)
        # читаем номер страницы, если был задан
        # дефолтное ограничение по выводу на страницу - 10 записей
        query = phones.select()\
            .order_by(ph_order_dict[ordering[1:]].desc())\
            .limit(opp).offset(opp*(page-1))
    else:
        query = phones.select()\
            .order_by(ph_order_dict[ordering])\
            .limit(opp).offset(opp*(page-1))
    return await database.fetch_all(query)


async def update_phone(id: int, phone: PhoneIn):
    query = (
        phones
        .update()
        .where(phones.c.id == id)
        .values(
            ab_id=phone.ab_id,
            type=phone.type,
            number=phone.number)
        .returning(phones.c.id))
    return await database.execute(query)


async def delete_phone(id: int):
    query = phones.delete().where(phones.c.id == id)
    return await database.execute(query)


# Блок CRUD-операций для электронных адресов


async def create_mail(mail: MailIn):
    query = mails.insert().values(
        ab_id=mail.ab_id,
        type=mail.type,
        address=mail.address,
    )
    return await database.execute(query)


async def read_mail(id: int):
    query = mails.select().where(mails.c.id == id)
    return await database.fetch_one(query)


async def read_mails(ordering: str = None, page: int = 1, opp: int = 10):
    if ordering and ordering.startswith('-'):
        # читаем параметр сортировки (если был подан; и был ли он обратным)
        # читаем номер страницы, если был задан
        # дефолтное ограничение по выводу на страницу - 10 записей
        query = mails.select()\
            .order_by(ml_order_dict[ordering[1:]].desc())\
            .limit(opp).offset(opp*(page-1))
    else:
        query = mails.select()\
            .order_by(ml_order_dict[ordering])\
            .limit(opp).offset(opp*(page-1))
    return await database.fetch_all(query)


async def update_mail(id: int, mail: MailIn):
    query = (
        mails
        .update()
        .where(mails.c.id == id)
        .values(
            ab_id=mail.ab_id,
            type=mail.type,
            address=mail.address)
        .returning(mails.c.id))
    return await database.execute(query)


async def delete_mail(id: int):
    query = mails.delete().where(mails.c.id == id)
    return await database.execute(query)
