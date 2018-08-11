#!python
# -*- coding: utf-8 -*-


#voteMaser - server part

#список стран пользователей
countries = ['riba_kit', 'tridevCarstvo', 'lukomore', 'morskayaDergava', 'shahman']
question = ["TEST111", 'Отказ от серебряно-золотого международного валютного стандарта', 'Использование территории Чудо-юдо рыбы Кита для размещения коалиционного флота', 'Приостановление членства в Организации Объединенных сказочных Наций Кощеева царства', 'Введение эмбарго на мертвую воду для Кощеева царства', 'Создание бесполетной зоны над Кощеевым царством']
from bottle import route, run, template

@route('/authorization/<round>/<name>')
def authorization(round, name):
    if round == 'one':
        i = 0
        if name == 'riba_kit':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'tridevCarstvo':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]
    if round == 'two':
        i = 1
        if name == 'tridevCarstvo':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'riba_kit':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]
    if round == 'three':
        i = 2
        if name == 'lukomore':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'morskayaDergava':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]
    if round == 'four':
        i = 3
        if name == 'shahman':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'lukomore':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]
    if round == 'five':
        i = 4
        if name == 'morskayaDergava':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'shahman':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]

votingResult = [0, 0]

@route('/answer/<round>/<name>/<ans>')
def answer(round, name, ans):
#    count = 0
    global votingResult
    if ans == 'yes':
        votingResult[0] += 1
        return 'Проголосовало ЗА: ' + str(votingResult[0]) +'    ***     Проголосовало ПРОТИВ: '+str(votingResult[1])
    if ans == 'no':
        votingResult[1] += 1
        return 'Проголосовало ЗА: ' + str(votingResult[0]) +'    ***     Проголосовало ПРОТИВ: '+str(votingResult[1])

run(host='localhost', port=8080)