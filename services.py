from typing import List

from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session

from models import (
    engine,
    sessionmaker,
    Receipt,
    Calculation, Person,
)
from exceptions import *


def open_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_data_from_user(message: str):
    sponsor, money, *consumers = message.split()
    try:
        sponsor = str(sponsor)
        money = float(money)
    except ValueError as e:
        print(f'value error - {e}')
        raise NotCorrectReceipt
    return sponsor, money, consumers


def get_last_receipt_by_user(user_id: int, session: Session):
    last_receipt = session.query(Receipt). \
        join(Calculation,
             (Receipt.calc_id == Calculation.calc_id)). \
        where(Receipt.user_id == user_id). \
        where(Receipt.user_id == Calculation.user_id). \
        where(Calculation.active).order_by(Receipt.receipt_id.desc()).first()
    return last_receipt


def get_last_active_calc_by_user(user_id: int, session: Session):
    last_calc_query = session.query(Calculation). \
        where(Calculation.user_id == user_id). \
        where(Calculation.active). \
        order_by(Calculation.calc_id).first()
    return last_calc_query


def get_last_calc_by_user(user_id: int, session: Session):
    last_calc_query = session.query(Calculation). \
        where(Calculation.user_id == user_id). \
        order_by(Calculation.calc_id.desc()).first()
    return last_calc_query


def add_peceipt(message: str, user_id: int):
    try:
        sponsor, money, consumers = get_data_from_user(message)
    except ValueError as e:
        print(f'value error - {e}')
        raise NotCorrectReceipt
    session = open_session()
    last_receipt = get_last_receipt_by_user(user_id, session)
    new_receipt_id = last_receipt.receipt_id + 1 if last_receipt else 1
    active_calc = get_last_active_calc_by_user(user_id, session)
    sponsor = get_or_create(session, Person, name=sponsor)
    new_receipt = Receipt(
        user_id=user_id,
        calc_id=active_calc.calc_id,
        calc_alias=active_calc.calc_alias,
        receipt_id=new_receipt_id,
        sponsor=sponsor,
        sum=money,
    )
    for consumer in consumers:
        consumer_to_add = get_or_create(session, Person, name=consumer)
        new_receipt.consumers.append(consumer_to_add)
    session.add(new_receipt)
    session.commit()


def add_new_calc(alias: str, user_id: int):
    session = open_session()
    calculations_data: Calculation = get_last_calc_by_user(user_id, session)
    if calculations_data:
        calculations_data.active = False
        new_calculation: Calculation = Calculation(
            user_id=user_id,
            calc_id=calculations_data.calc_id + 1,
            calc_alias=alias,
            active=True,
        )
        session.add(new_calculation)
    else:
        new_calculation: Calculation = Calculation(
            user_id=user_id,
            calc_id=1,
            calc_alias=alias,
            active=True,
        )
        session.add(new_calculation)
    session.commit()


def get_all_calcs(user_id: int) -> List[Calculation]:
    session = open_session()
    all_calcs = session.query(Calculation).\
        where(Calculation.user_id == user_id).\
        order_by(Calculation.calc_id).all()
    return all_calcs


def get_all_receipts(user_id: int) -> List[Receipt]:
    session = open_session()
    all_receipts = session.query(Receipt). \
        join(Calculation, Receipt.calc_id == Calculation.calc_id). \
        where(Calculation.active). \
        where(Calculation.user_id == user_id).\
        order_by(Receipt.receipt_id).all()
    return all_receipts


def delete_calc(user_id: int, calc_id: int):
    session = open_session()
    calculation_for_delete = session.query(Calculation).\
        where(Calculation.calc_id == calc_id). \
        where(Calculation.user_id == user_id)
    if calculation_for_delete is None:
        return False
    calc_is_active = calculation_for_delete.first().active
    calculation_for_delete.delete()
    session.flush()
    if calc_is_active:
        new_active_calc = get_last_calc_by_user(user_id, session)
        new_active_calc.active = True
    session.query(Receipt).\
        filter(Receipt.calc_id == calc_id). \
        filter(Receipt.user_id == user_id).delete()
    # session.delete(receipt_for_delete)
    session.commit()
    return True


def delete_receipt(user_id: int, receipt_id: int):
    session = open_session()
    active_calc = get_last_active_calc_by_user(user_id, session)
    # receipt = session.query(Receipt).\
    #     filter(Receipt.user_id == user_id). \
    #     filter(Receipt.calc_id == active_calc.calc_id). \
    #     filter(Receipt.receipt_id == receipt_id).first()
    # print("RECCCCCEIPT", receipt)
        # session.delete(receipt)
    receipt = session.query(Receipt). \
        filter(Receipt.user_id == user_id). \
        filter(Receipt.calc_id == active_calc.calc_id). \
        filter(Receipt.receipt_id == receipt_id).delete()
        # session.commit()
    return receipt
    # else:
    #     return False


def change_calc(user_id: int, calc_id: int):
    session = open_session()
    active_calc = get_last_active_calc_by_user(user_id, session)
    print(active_calc)
    if active_calc:
        active_calc.active = False
    calc = session.query(Calculation).where(Calculation.calc_id == calc_id). \
        where(Calculation.user_id == user_id).one()
    calc.active = True
    session.commit()
    return calc.calc_id, calc.calc_alias


def get_dict_of_credits_data(user_id: int):
    session = open_session()
    print("qweqweqwe", user_id)
    all_receipts: List[Receipt] = session.query(Receipt, Calculation). \
        filter(Receipt.calc_id == Calculation.calc_id). \
        filter(Calculation.active). \
        filter(Calculation.user_id == user_id).all()
    print([receipt for receipt in all_receipts])
    active_calc = get_last_active_calc_by_user(user_id, session)
    result_dict = {}
    alias = str
    all_persons = set()
    for receipt in all_receipts:
        consumers_receipt = [consumer for consumer in receipt[0].consumers]
        all_persons.update(consumers_receipt)
        sponsor = receipt[0].sponsor
        all_persons.add(sponsor)
    for sponsor in all_persons:
        result_dict[sponsor] = {consumer: 0 for consumer in all_persons}
    print(all_persons)
    for receipt in all_receipts:
        alias = receipt[0].calc_alias
        sponsor = receipt[0].sponsor
        money = receipt[0].sum
        consumers_receipt = [consumer for consumer in receipt[0].consumers]
        for consumer in consumers_receipt:
            if consumer == sponsor:
                continue
            result_dict[consumer][sponsor] -= round(money / len(consumers_receipt), 2)
            result_dict[sponsor][consumer] += round(money / len(consumers_receipt), 2)
    return active_calc, alias, result_dict


def delete_all_calcs(user_id: int):
    session = open_session()
    session.query(Calculation).where(Calculation.user_id == user_id).delete()
    session.query(Receipt).where(Receipt.user_id == user_id).delete()
    session.commit()


if __name__ == '__main__':
    # change_calc(1, 4)
    # print(add_peceipt("sponsor3 800 con1 con2", 333))
    print(delete_all_calcs(333))
