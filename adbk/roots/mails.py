from fastapi import APIRouter, HTTPException
from typing import List
from adbk import crud
from adbk.models import MailIn, Mail
from adbk.logs.logging import set_config
import logging

logger = logging.getLogger(__name__)
set_config(logger)

router = APIRouter()


@router.put("/", response_model=Mail, status_code=201)
async def put_mail(mail: MailIn):
    """эндпоинт создания электронного адреса. На вход подаётся схема создания
    для валидации, на возврат - схема вывода"""
    # проверяем, есть ли абонент с указанным id в бд
    abonent_inst = await crud.read_abonent(mail.ab_id)
    if not abonent_inst:
        raise HTTPException(
            status_code=404,
            detail="Abonent with following id not found")
    # отправляем данные в круд, получаем обратно id созданного объекта
    mail_id = await crud.create_mail(mail)
    # создаём объект с параметрами созданного емейла
    response_object = {
        "id": mail_id,
        "ab_id": mail.ab_id,
        "type": mail.type,
        "address": mail.address
    }
    # пишем сообщение в лог о создании объекта
    message = f"Created mail instance (id={mail_id})"
    logger.warning(message)
    return response_object


@router.post("/{id}/", response_model=Mail)
async def post_mail(id: int):
    "эндпоинт чтения конкретного емейла. Возвращаем данные в схеме вывода"
    # проверяем, есть ли емейл с указанным id в бд
    mail = await crud.read_mail(id)
    if not mail:
        raise HTTPException(
            status_code=404,
            detail="Mail address not found")
    return mail


@router.post("/", response_model=List[Mail])
async def post_mails(ordering: str = None, page: int = 1, opp: int = 10):
    "эндпоинт чтения всех емейлов. Возвращаем данные в листе схем вывода"
    # проверяем, был ли задан параметр сортировки, а так же проверяем
    # местоположение знака "-" (должен быть либо 0, либо -1 (если его нет))
    if ordering and (ordering.find('-') > 0):
        raise HTTPException(
            status_code=400,
            detail="Incorrect ordering parameter")
    mails = await crud.read_mails(ordering, page, opp)
    return mails


@router.patch("/{id}/", response_model=Mail)
async def patch_mail(id: int, mail: MailIn):
    "эндпоинт апдейта конкретного абонента. Возвращаем данные в схеме вывода"
    # проверяем, есть ли абонент с указанным id в бд
    abonent_inst = await crud.read_abonent(mail.ab_id)
    if not abonent_inst:
        raise HTTPException(
            status_code=404,
            detail="Abonent with following id not found")
    # проверяем, есть ли емейл-адрес с указанным id в бд
    mail_inst = await crud.read_mail(id)
    if not mail_inst:
        raise HTTPException(
            status_code=404,
            detail="Mail address not found")
    mail_id = await crud.update_mail(id, mail)
    response_object = {
        "id": mail_id,
        "ab_id": mail.ab_id,
        "type": mail.type,
        "address": mail.address
    }
    # пишем сообщение в лог об обновлении объекта
    message = f"Updated mail instance (id={mail_id})"
    logger.warning(message)
    return response_object


@router.delete("/{id}/")
async def delete_mail(id: int):
    """эндпоинт удаления конкретного емейла. Возвращаем сообщение об
    успешном завершении операций"""
    # проверяем, есть ли емейл-адрес с указанным id в бд
    mail_inst = await crud.read_mail(id)
    if not mail_inst:
        raise HTTPException(
            status_code=404,
            detail="Mail address not found")
    await crud.delete_mail(id)
    return {"msg": "Mail instance №{} just deleted from database"
            .format(mail_inst['id'])}
