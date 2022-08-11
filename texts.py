from aiogram.utils.markdown import text

START_TEXT = text('*Общак бот \n*',
                  'Расчет долгов сложных трат при оплате одним человеком \n',
                  'Список возможных команд: \n',
                  '_/new_', ' - Новый расчет \n',
                  '_Имя1 300 Имя2 Имя3_', ' - Формат ввода данных чека. Имя1 - оплатил чек, '
                                          '300 - сумма чека, Имя2 и Имя3 - должники  \n',
                  '_/report_', ' - Вывод текущего расчета \n',
                  '_/picreport_', ' - Вывод текущего расчета в виде  \n',
                  '_/report Имя1 Имя2_', ' - Вывод детали расчета. '
                                         'Можно узнать сколько Имя2 должен Имя2 \n',
                  '_/all_', ' - Вывод всех расчетов \n',
                  '_/del1_', ' - Удаление расчета под номером 1 \n',
                  '_/calc1_', ' - Сделать активным расчет под номером 1 '
                              'для ввода данных или печати отчета \n',
                  '_/delall_', ' - Удалить все расчета \n',
                  # '_/detail1_', ' - Детальная информация о расчете номер 1 \n',
                  # '_/delreceipt4_', ' - Удалить чек номер 4 из активного расчета \n',
                  '', )


def text_for_report(calc_id, calc_alias, report_data,
                    sponsor_request=None, consumer_request=None, full_report=False):
    answer = f'Сформировали ваш отчет по расчету {calc_id} с именем {calc_alias} \n'
    for sponsor, consumers in report_data.items():
        for consumer, money in consumers.items():
            if money > 0 and \
                    (sponsor == sponsor_request or full_report) and \
                    (consumer == consumer_request or full_report):
                answer += f'{consumer.name} -> {sponsor.name}: {money}\n'
    return answer


def text_all_calcs(all_calcs):
    answer = '(Список всех расчетов\n*'
    for calc in all_calcs:
        calc_alias = calc.calc_alias
        calc_id = calc.calc_id

        calc_alias = calc_alias if calc_alias else '_Без имени_'
        answer += f'Номер расчета {calc_id}, имя {calc_alias}.  ' \
                  f'Удалить - /del{calc_id}, ' \
                  f'Сделать активным /calc{calc_id} \n'
    return text(answer)


def text_all_receipts(all_receipts):
    calc_id = all_receipts[0].calc_id
    calc_alias = all_receipts[0].calc_alias

    calc_alias = calc_alias if calc_alias else '(Без имени)'
    answer = f'*Список всех чеков по расчету номер {calc_id} с именем {calc_alias} \n*'
    for receipt in all_receipts:
        receipt_num = receipt.receipt_id
        sponsor = receipt.sponsor
        receipt_money = receipt.sum
        consumers = receipt.consumers

        consumers = [consumer for consumer in consumers if consumer is not None]
        answer += (f'*{receipt_num}:* ' +
                   f'*{sponsor}*' + ' оплатил ' + f'_{receipt_money}_ ' +
                   f'за {consumers}. ' + f'Удалить чек /receiptdel{receipt_num} \n')
    return text(answer)
