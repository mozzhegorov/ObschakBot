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
        data_base_action(UPDATE_CALC, (calculations_data[0]+1, alias, user_id))
    else:
        data_base_action(INSERT_CALC, (user_id, 1, alias))


def get_all_calcs(user_id: int):
    all_calcs = data_base_fetch(ALL_CALCS_BY_USER, (user_id,))
    dic_of_calcs = {calc[0]: calc[1] for calc in all_calcs}
    return dic_of_calcs


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
    for receipt in get_all_receipts:
        alias = receipt[3]
        sponsor = receipt[5]
        money = receipt[6]
        consumers = [consumer for consumer in receipt[7:25] if consumer is not None]
        if sponsor not in result_dict:
            result_dict[sponsor] = {}
        for consumer in consumers:
            if consumer == sponsor:
                continue
            if consumer not in result_dict[sponsor]:
                result_dict[sponsor][consumer] = 0
            if consumer in result_dict and sponsor in result_dict[consumer]:
                dif_money = result_dict[consumer][sponsor] - money / len(consumers)
                result_dict[consumer][sponsor] += dif_money
                if dif_money < 0:
                    result_dict[sponsor][consumer] -= dif_money
            else:
                result_dict[sponsor][consumer] += money / len(consumers)
    return last_calc_id, alias, result_dict


def delete_all_calcs(user_id: int):
    data_base_action(DELETE_ALL_CALCS_FROM_CASHDATA, (user_id,))
    data_base_action(DELETE_ALL_CALCS_FROM_CALCS, (user_id,))


if __name__ == '__main__':
    change_calc(1, 4)
