from exceptions import *
from db import *


def get_data_from_user(message: str):
    sponsor, money, *consumers = message.split()
    try:
        sponsor = str(sponsor)
        money = float(money)
        consumers = consumers + (19 - len(consumers)) * [None]
    except ValueError as e:
        print(f'value error - {e}')
        raise NotCorrectReceipt
    return sponsor, money, consumers


def add_peceipt(message: str, user_id: int):
    try:
        sponsor, money, consumers = get_data_from_user(message)
    except ValueError as e:
        print(f'value error - {e}')
        raise NotCorrectReceipt
    last_receipt = data_base_fetchone(GET_LAST_RECEIPT_DATA, (user_id,))
    calc_id, calc_alias = data_base_fetchone(LAST_CALC_DATA, (user_id,))
    receipt_id = last_receipt[2] if last_receipt else 0
    receipt = (
        user_id,
        calc_id,
        calc_alias,
        receipt_id + 1,
        sponsor,
        money,
        *consumers
    )
    data_base_action(INSERT_RECEIPT, receipt)


def add_new_calc(alias: str, user_id: int):
    calculations_data = data_base_fetchone(GET_CALC_BY_USER, (user_id,))
    if calculations_data:
        data_base_action(UPDATE_CALC, (calculations_data[0] + 1, alias, user_id))
    else:
        data_base_action(INSERT_CALC, (user_id, 1, alias))


def get_all_calcs(user_id: int):
    all_calcs = data_base_fetch(ALL_CALCS_BY_USER, (user_id,))
    dict_of_calcs = {calc[0]: calc[1] for calc in all_calcs}
    return dict_of_calcs


def get_all_receipts(user_id: int):
    all_receipts = data_base_fetch(RECEIPTS_BY_USER_LAST_CALC, (user_id,))
    list_of_receipts = [calc[0:24] for calc in all_receipts]
    return list_of_receipts


def delete_calc(user_id: int, calc_id: int):
    calcs_in_cashdata = data_base_fetch(GET_CALC_BY_USER_CALCID_IN_CASHS, (user_id, calc_id))
    calcs_in_calcs = data_base_fetch(GET_CALC_BY_USER_CALCID_IN_CALCS, (user_id, calc_id))
    if calcs_in_cashdata or calcs_in_calcs:
        data_base_action(DELETE_CALC_FROM_CALCS, (calc_id, user_id))
        data_base_action(DELETE_CALC_FROM_CASHDATA, (calc_id, user_id))
        return True
    else:
        return False


def change_calc(user_id: int, calc_id: int):
    calc_alias = data_base_fetchone(GET_CALC_ALIAS, (user_id, calc_id))[0]
    data_base_action(UPDATE_CALC, (calc_id, calc_alias, user_id))
    return calc_id, calc_alias


def get_dict_of_credits_data(user_id: int):
    calculations_data = data_base_fetch(LAST_CALC_DATA, (user_id,))
    last_calc_id = calculations_data[0][0] if calculations_data else 0
    get_all_receipts = data_base_fetch(GET_ALL_RECEIPT_DATA, (user_id, last_calc_id))
    result_dict = {}
    alias = str
    all_persons = set()
    for receipt in get_all_receipts:
        consumers_receipt = [consumer for consumer in receipt[7:25] if consumer is not None]
        all_persons.update(consumers_receipt)
        sponsor = receipt[5]
        all_persons.add(sponsor)
    for sponsor in all_persons:
        result_dict[sponsor] = {consumer: 0 for consumer in all_persons}

    for receipt in get_all_receipts:
        alias = receipt[3]
        sponsor = receipt[5]
        money = receipt[6]
        consumers_receipt = [consumer for consumer in receipt[7:25] if consumer is not None]
        for consumer in consumers_receipt:
            if consumer == sponsor:
                continue
            result_dict[consumer][sponsor] -= round(money / len(consumers_receipt), 2)
            result_dict[sponsor][consumer] += round(money / len(consumers_receipt), 2)
    return last_calc_id, alias, result_dict


def delete_all_calcs(user_id: int):
    data_base_action(DELETE_ALL_CALCS_FROM_CASHDATA, (user_id,))
    data_base_action(DELETE_ALL_CALCS_FROM_CALCS, (user_id,))


if __name__ == '__main__':
    change_calc(1, 4)
