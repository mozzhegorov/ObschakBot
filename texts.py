from aiogram.utils.markdown import code, text, italic, bold

START_TEXT = text(bold('Общак бот \n'),
                  'Расчет долгов сложных трат при оплате одним человеком \n',
                  'Список возможных команд: \n',
                  italic('/new'), ' - Новый расчет \n',
                  italic('Имя1 300 Имя2 Имя3'), ' - Формат ввода данных чека. Имя1 - оплатил чек, '
                                                '300 - сумма чека, Имя2 и Имя3 - должники  \n',
                  italic('/report'), ' - Вывод текущего расчета \n',
                  italic('/picreport'), ' - Вывод текущего расчета в виде  \n',
                  italic('/report Имя1 Имя2'), ' - Вывод детали расчета. '
                                               'Можно узнать сколько Имя2 должен Имя2 \n',
                  italic('/all'), ' - Вывод всех расчетов \n',
                  italic('/del1'), ' - Удаление расчета под номером 1 \n',
                  italic('/calc1'), ' - Сделать активным расчет под номером 1 '
                                    'для ввода данных или печати отчета \n',
                  italic('/delall'), ' - Удалить все расчета \n',
                  # italic('/detail1'), ' - Детальная информация о расчете номер 1 \n',
                  # italic('/delreceipt4'), ' - Удалить чек номер 4 из активного расчета \n',
                  '', )


def text_for_report(calc_id, calc_alias, report_data,
                    sponsor_request=None, consumer_request=None, full_report=False):
    answer = f'Сформировали ваш отчет по расчету {calc_id} с именем {calc_alias} \n'
    for sponsor, consumers in report_data.items():
        for consumer, money in consumers.items():
            if money > 0 and \
                    (sponsor == sponsor_request or full_report) and \
                    (consumer == consumer_request or full_report):
                answer += f'{consumer} -> {sponsor}: {money}\n'
    return answer


def text_all_calcs(all_calcs):
    answer = bold('Список всех расчетов\n')
    for calc_id, calc_alias in all_calcs.items():
        calc_alias = calc_alias if calc_alias else '(Без имени)'
        answer += f'Номер расчета {calc_id}, имя {calc_alias}.  ' \
                  f'Удалить - /del{calc_id}, ' \
                  f'Сделать активным /calc{calc_id} \n'
    return text(answer)


def text_all_receipts(all_receipts):
    calc_id = all_receipts[0][1]
    calc_alias = all_receipts[0][2]
    calc_alias = calc_alias if calc_alias else '(Без имени)'
    answer = text(bold(f'Список всех чеков по расчету номер {calc_id} с именем {calc_alias} \n'))
    for receipt in all_receipts:
        user_id, calc_id, calc_alias, receipt_num, sponsor, receipt_money, *consumers = receipt
        answer.join(text(italic(f'{receipt_num}'),
                    f'{sponsor} оплатил {receipt_money} за {consumers}'))
    return text(answer)
