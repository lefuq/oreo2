from pydantic import BaseModel, validator
import datetime
from re import fullmatch
from os import path

# Модели (или схемы) сущностей. Модели Nested* нужны для создания абонентов в
# связке с телефоном и почтой. От них наследуются модели *In, которые использу-
# ются при создании отдельных экземпляров телефона и почты (а т.ж. абонента).
# Модели Abonent, Phone, Mail нужны для методов получения и для возврата ре-
# зультатов создания/изменения объектов.


class NestedPhoneIn(BaseModel):
    type: str
    number: str

    @validator('type')
    def type_must_be_one_of(cls, phone_type):
        """проверка типа телефона на принадлежность к двум определённым"""
        if phone_type not in ['Городской', 'Мобильный']:
            raise ValueError('Must be "Городоской" or "Мобильный".')
        return phone_type

    @validator('number')
    def must_be_following_format(cls, number):
        """проверка формата номера телефона для единообразия"""
        pattern = r"[+]\d{1} \d{3} \d{3} \d{4}"
        if not fullmatch(pattern, number):
            raise ValueError('Incorrect format. Must be +X XXX XXX XXXX.')
        return number


class PhoneIn(NestedPhoneIn):
    ab_id: int


class Phone(BaseModel):
    id: int
    ab_id: int
    type: str
    number: str


class NestedMailIn(BaseModel):
    type: str
    address: str

    @validator('type')
    def type_must_be_one_of(cls, mail_type):
        """проверка типа адреса на принадлежность к двум определённым"""
        if mail_type not in ['Рабочая', 'Личная']:
            raise ValueError('Must be "Рабочая" or "Личная".')
        return mail_type

    @validator('address')
    def must_be_following_format(cls, address):
        """простая проверка формата емейл-адреса"""
        pattern = r"[.\w]{1,}@[\w]{1,}[.][\w]{1,3}"
        if not fullmatch(pattern, address):
            raise ValueError('Incorrect mail format.')
        return address


class MailIn(NestedMailIn):
    ab_id: int


class Mail(BaseModel):
    id: int
    ab_id: int
    type: str
    address: str


class AbonentIn(BaseModel):
    name: str
    photo: str
    sex: str
    birth: datetime.date
    live: str
    phone: NestedPhoneIn = None
    mail: NestedMailIn = None

    @validator('name')
    def must_be_lt_100_and_contain_space(cls, name):
        """проверка имени на длину (от 3 до 100 символов), а так же на наличие
        пробельного символа в имени (не двух для возможности внесения имени без
        отчества)"""
        if not 3 < len(name) < 100:
            raise ValueError('Must contain from 3 to 100 symbols.')
        if ' ' not in name:
            raise ValueError('Must contain space.')
        return name

    @validator('photo')
    def must_exist_on_the_server(cls, photo):
        """базовая проверка наличия файла на сервере"""
        if not path.isfile('adbk/' + photo):
            raise ValueError('File not exist.')
        return photo

    @validator('sex')
    def sex_type_must_be_one_of(cls, sex):
        """проверка пола на принадлежность к двум определённым"""
        if sex not in ['Мужчина', 'Женщина']:
            raise ValueError('Must be "Мужчина" or "Женщина".')
        return sex

    @validator('live')
    def must_be_lt_300_and_contain_space(cls, place):
        """проверка адреса на длину (от 3 до 300 символов), а так же на наличие
        пробельного символа"""
        if not 3 < len(place) < 300:
            raise ValueError('Must contain from 3 to 300 symbols.')
        if ' ' not in place:
            raise ValueError('Must contain space.')
        return place


class Abonent(BaseModel):
    id: int
    name: str
    photo: str
    sex: str
    birth: datetime.date
    live: str
