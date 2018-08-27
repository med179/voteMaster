#!python
# -*- coding: utf-8 -*-


#voteMaser - server part

#список стран пользователей
countries = {'riba_kit':'', 'tridevCarstvo':'', 'lukomore':'', 'morskayaDergava':'', 'shamahan':''}
question = ['Отказ от серебряно-золотого международного валютного стандарта', 'Использование территории Чудо-юдо рыбы Кита для размещения коалиционного флота', 'Приостановление членства в Организации Объединенных сказочных Наций Кощеева царства', 'Введение эмбарго на мертвую воду для Кощеева царства', 'Создание бесполетной зоны над Кощеевым царством']
status = {'round':'zero'}

from bottle import route, run, template


@route('/authorization/<name>')
def authorization(name):
    if name == 'admin':
        return countries
    else:
        countries[name] = 'im ready'
    

@route('/interrogatory/<round>/<name>')
def interrogatory(round, name):
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
        if name == 'shamahan':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'lukomore':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]
    if round == 'five':
        i = 4
        if name == 'morskayaDergava':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА</b>'
        if name == 'shamahan':
            return question[i]  + '<br /> <b>ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ</b>'
        else:
            return question[i]

votingResult = {'one_yes':0, 'one_no':0, 'two_yes':0, 'two_no':0, 'three_yes':0, 'three_no':0, 'four_yes':0, 'four_no':0, 'five_yes':0, 'five_no':0}


@route('/answer/<round>/<name>/<ans>')
def answer(round, name, ans):
    global votingResult
    key = round + '_' + ans
    votingResult[key] += 1
    return 'Проголосовало ЗА: ' + str(votingResult[round + '_yes']) +'    ***     Проголосовало ПРОТИВ: '+str(votingResult[round + '_no'])

@route('/result/<round>')
def result(round):
    return votingResult



run(host='localhost', port=8080)