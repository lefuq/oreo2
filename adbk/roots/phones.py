from fastapi import APIRouter, HTTPException
from typing import List
from adbk import crud
from adbk.models import PhoneIn, Phone
from adbk.logs.logging import set_config
import logging

logger = logging.getLogger(__name__)
set_config(logger)

router = APIRouter()


@router.put("/", response_model=Phone, status_code=201)
async def put_phone(phone: PhoneIn):
    """эндпоинт создания телефона. На вход подаётся схема создания
    для валидации, на возврат - схема вывода"""
    # проверяем, есть ли абонент с указанным id в бд
    abonent_inst = await crud.read_abonent(phone.ab_id)
    if not abonent_inst:
        raise HTTPException(
            status_code=404,
            detail="Abonent with following id not found")
    # отправляем данные в круд, получаем обратно id созданного объекта
    phone_id = await crud.create_phone(phone)
    # создаём объект с параметрами созданного телефона
    response_object = {
        "id": phone_id,
        "ab_id": phone.ab_id,
        "type": phone.type,
        "number": phone.number
    }
    # пишем сообщение в лог о создании объекта
    message = f"Created phone instance (id={phone_id})"
    logger.warning(message)
    return response_object


@router.post("/{id}/", response_model=Phone)
async def post_phone(id: int):
    "эндпоинт чтения конкретного телефона. Возвращаем данные в схеме вывода"
    # проверяем, есть ли телефон с указанным id в бд
    phone = await crud.read_phone(id)
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone


@router.post("/", response_model=List[Phone])
async def post_phones(ordering: str = None, page: int = 1, opp: int = 10):
    "эндпоинт чтения всех телефонов. Возвращаем данные в листе схем вывода"
    # проверяем, был ли задан параметр сортировки, а так же проверяем
    # местоположение знака "-" (должен быть либо 0, либо -1 (если его нет))
    if ordering and (ordering.find('-') > 0):
        raise HTTPException(
            status_code=400,
            detail="Incorrect ordering parameter")
    phones = await crud.read_phones(ordering, page, opp)
    return phones


@router.patch("/{id}/", response_model=Phone)
async def patch_phone(id: int, phone: PhoneIn):
    "эндпоинт апдейта конкретного телефона. Возвращаем данные в схеме вывода"
    # проверяем, есть ли абонент с указанным id в бд
    abonent_inst = await crud.read_abonent(phone.ab_id)
    if not abonent_inst:
        raise HTTPException(
            status_code=404,
            detail="Abonent with following id not found")
    # проверяем, есть ли телефон с указанным id в бд
    phone_inst = await crud.read_phone(id)
    if not phone_inst:
        raise HTTPException(status_code=404, detail="Phone not found")
    phone_id = await crud.update_phone(id, phone)
    response_object = {
        "id": phone_id,
        "ab_id": phone.ab_id,
        "type": phone.type,
        "number": phone.number
    }
    # пишем сообщение в лог об обновлении объекта
    message = f"Updated phone instance (id={phone_id})"
    logger.warning(message)
    return response_object


@router.delete("/{id}/")
async def delete_phone(id: int):
    """эндпоинт удаления конкретного емейла. Возвращаем сообщение об
    успешном завершении операций"""
    # проверяем, есть ли телефон с указанным id в бд
    phone_inst = await crud.read_phone(id)
    if not phone_inst:
        raise HTTPException(status_code=404, detail="Phone not found")
    await crud.delete_phone(id)
    return {"msg": "Phone instance №{} just deleted from database"
            .format(phone_inst['id'])}
