# ObschakBot v0.9

## Основные зависимости:

1. python3.8
2. aiogram
3. psycopg2
4. matplotlib
5. postgresql12+

## Описание:

Telegram бот для фиксации и расчета сложных трат, когда один платит за всех в разных вариациях. 

## Первичная настройка:

`API_TOKEN` - API токен бота

`DATABASE_URL` - URL базы данных на PostgreSQL

API_TOKEN и DATABASE_URL предлагается заполнять либо в файле .env, либо в Config Vars хостинга Heroku.

Для разворачивания на Heroku присутствует Procfile. 

Для работы с Docker присутствует Dockerfile. 

```
docker build -t obschaki ./
docker run -d --name obschak obschaki
```

## Описание работы

Бот принимаем на вход строку с параметрами для формирования чека с указанием «потребителей», «спонсора» и суммой чека (позиции чека).
Примерный вид строки следующий (с 1 пробелом, без табуляции):

`Трус      300           Балбес          Бывалый`

[спонсор] [сумма чека]  [потребитель 1] [потребитель 2]

Максимальное количество потребителей - 20. 

Новый расчет заводится командой `/new` Новый расчет, где Новый расчет – название расчета. Название расчета может быть не уникальным, 
при запросе всех расчетов служит пояснением к расчету. 

Отчеты выводятся в формате таблицы при вводе команды `/report`, где в качестве столбца участвует «спонсор», а в качестве строки «потребитель», 
т.е. если в ячейке положительное число, то "строка" должна "столбцу", а если отрицательное, то наоборот. 

Также отдельную деталь расчета возможно получить при вводе `/report` Балбес Трус, при этом в ответе будет отображаться кто кому должен в текущем расчете. 
Трус -> Балбес | 300 рублей

Список всех расчетов возможно выводить с помощью команды `/all`. При этом в ответе возможен выбор команды для удаления расчета по номеру расчета, 
например `/del1`. Либо удаление всех расчетов `/delall`.

Для корректировки расчета возможно переключение между расчетами с помощью команды `/calc1`, где 1 – номер расчета для переключения. 

Для проверки всех данных по активному расчету (количество чеков, все «потребители» и «спонсоры») применяется команда `/receipts`.

Командой `/receiptdel4` возможно удалить чек из расчета, в данном случае чек номер 4.
