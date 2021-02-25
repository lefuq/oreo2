from fastapi import APIRouter, HTTPException
from typing import List
from adbk import crud
from adbk.models import AbonentIn, Abonent, PhoneIn, MailIn
from adbk.logs.logging import set_config
import logging

logger = logging.getLogger(__name__)
set_config(logger)

router = APIRouter()


@router.put("/", response_model=Abonent, status_code=201)
async def put_abonent(abonent: AbonentIn):
    """эндпоинт создания абонента. На вход подаётся схема создания абонента для
    валидации, на возврат - схема вывода"""
    abonent_data = abonent.dict()  # десериализуем данные из схемы
    if 'phone' in abonent_data:  # проверяем, была ли подана инфа о телефоне
        phone_data = abonent_data.pop('phone')  # извлекаем, если была
    if 'mail' in abonent_data:  # проверяем, была ли подана инфа о емейле
        mail_data = abonent_data.pop('mail')  # извлекаем, если была
    db_abonent = AbonentIn(**abonent_data)  # сериализуем данные обратно
    # отправляем данные в круд, получаем обратно id созданного объекта
    abonent_id = await crud.create_abonent(db_abonent)
    # если инфа о телефоне была подана:
    if phone_data:
        phone_data['ab_id'] = abonent_id  # присваеваем id абонента
        db_phone = PhoneIn(**phone_data)  # сериализуем данные в схему телефона
        await crud.create_phone(db_phone)  # отправляем данные в круд
    # если инфа о почтовом адресе была подана:
    if mail_data:
        mail_data['ab_id'] = abonent_id  # присваеваем id абонента
        db_mail = MailIn(**mail_data)  # сериализуем данные в схему телефона
        await crud.create_mail(db_mail)  # отправляем данные в круд
    # создаём объект с параметрами созданного абонента
    response_object = {
        "id": abonent_id,
        **abonent_data
    }
    # пишем сообщение в лог о создании объекта
    message = f"Created abonent instance (id={abonent_id})"
    logger.warning(message)
    # возвращаем пользователю информацию о созданном объекте
    return response_object


@router.post("/{id}/", response_model=Abonent)
async def post_abonent(id: int):
    "эндпоинт чтения конкретного абонента. Возвращаем данные в схеме вывода"
    # проверяем, есть ли абонент с указанным id в бд
    abonent = await crud.read_abonent(id)
    if not abonent:
        raise HTTPException(status_code=404, detail="Abonent not found")
    return abonent


@router.post("/", response_model=List[Abonent])
async def post_abonents(ordering: str = None, page: int = 1, opp: int = 10):
    "эндпоинт чтения всех абонентов. Возвращаем данные в листе схем вывода"
    # проверяем, был ли задан параметр сортировки, а так же проверяем
    # местоположение знака "-" (должен быть либо 0, либо -1 (если его нет))
    if ordering and (ordering.find('-') > 0):
        raise HTTPException(
            status_code=400,
            detail="Incorrect ordering parameter")
    abonents = await crud.read_abonents(ordering, page, opp)
    return abonents


@router.patch("/{id}/", response_model=Abonent)
async def patch_abonent(id: int, abonent: AbonentIn):
    "эндпоинт апдейта конкретного абонента. Возвращаем данные в схеме вывода"
    # проверяем, есть ли абонент с указанным id в бд
    abonent_inst = await crud.read_abonent(id)
    if not abonent_inst:
        raise HTTPException(status_code=404, detail="Abonent not found")
    abonent_id = await crud.update_abonent(id, abonent)
    response_object = {
        "id": abonent_id,
        "name": abonent.name,
        "photo": abonent.photo,
        "sex": abonent.sex,
        "birth": abonent.birth,
        "live": abonent.live
    }
    # пишем сообщение в лог об обновлении объекта
    message = f"Updated abonent instance (id={abonent_id})"
    logger.warning(message)
    return response_object


@router.delete("/{id}/")
async def delete_abonent(id: int):
    """эндпоинт удаления конкретного абонента. Возвращаем сообщение об
    успешном завершении операций"""
    # проверяем, есть ли абонент с указанным id в бд
    abonent_inst = await crud.read_abonent(id)
    if not abonent_inst:
        raise HTTPException(status_code=404, detail="Abonent not found")
    await crud.delete_abonent(id)
    return {"msg": "Abonent instance №{} just deleted from database"
            .format(abonent_inst['id'])}
