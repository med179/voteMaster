#!python
# -*- coding: utf-8 -*-


#voteMaser - server part

#список стран пользователей
countries = ['riba_kit', 'tridevCarstvo', 'lukomore', 'morskayaDergava', 'shahman']
question = ['test', 'Отказ от серебряно-золотого международного валютного стандарта', 'Использование территории Чудо-юдо рыбы Кита для размещения коалиционного флота', 'Приостановление членства в Организации Объединенных сказочных Наций Кощеева царства', 'Введение эмбарго на мертвую воду для Кощеева царства', 'Создание бесполетной зоны над Кощеевым царством']
from bottle import route, run, template

@route('/authorization/<name>')
def index(name):
    if name == 'riba_kit':
        return question  #+ '<b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
    if name == 'tridevCarstvo':
        return template('<b>Hello {{name}}</b>!', name=name)
    else:
        return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)