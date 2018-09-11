#!python
# -*- coding: utf-8 -*-


#voteMaser - server part

#список стран пользователей
countries = {'riba_kit':'', 'tridevCarstvo':'', 'lukomore':'', 'morskayaDergava':'', 'shamahan':''}
question = {'one':'Отказ от серебряно-золотого международного валютного стандарта', 'two':'Использование территории Чудо-юдо рыбы Кита для размещения коалиционного флота', 'three':'Приостановление членства в Организации Объединенных сказочных Наций Кощеева царства', 'four':'Введение эмбарго на мертвую воду для Кощеева царства', 'five':'Создание бесполетной зоны над Кощеевым царством'}
statusVote = {'round':'zero'}
allRight = {'isAllRight':'allRight'}
from bottle import route, run, template


@route('/allSettings/<roud>/<name>')
def allSettings(round, name):
    returnToClient = {}
    if round == statusVote['round']:
        return allRight
    else:
        if round == 'zero':
            if name == 'riba_kit':
                returnToClient['question'] = question['one'] + 'ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА'
            if name == 'tridevCarstvo':
                returnToClient['question'] = question['one'] + 'ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ'
            else:
                returnToClient['question'] = question['one']
            returnToClient['round'] = 'one'
        if round == 'one':
            if name == 'tridevCarstvo':
                returnToClient['question'] = question['two'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА'
            if name == 'riba_kit':
                returnToClient['question'] = question['two'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ'
            else:
                returnToClient['question'] = question['two']
            returnToClient['round'] = 'two'
        if round == 'two':
            if name == 'lukomore':
                returnToClient['question'] = question['three'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА'
            if name == 'morskayaDergava':
                returnToClient['question'] = question['three'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ'
            else:
                returnToClient['question'] = question['three']
            returnToClient['round'] = 'three'
        if round == 'three':
            if name == 'shamahan':
                returnToClient['question'] = question['four'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА'
            if name == 'lukomore':
                returnToClient['question'] = question['four'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ'
            else:
                returnToClient['question'] = question['four']
            returnToClient['round'] = 'four'
        if round == 'four':
            if name == 'morskayaDergava':
                returnToClient['question'] = question['five'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ЗА'
            if name == 'shamahan':
                returnToClient['question'] = question['five'] + ' ЗА ЭТОТ ВОПРОС БОЛЬШИНСТВО ДОЛЖНЫ ПРОГОЛОСОВАТЬ ПРОТИВ'
            else:
                returnToClient['question'] = question['five']
            returnToClient['round'] = 'four'
        return returnToClient
        

@route('/changeStatusVote')
def changeStatusVote():
    global statusVote
    if statusVote['round'] == 'five':
        statusVote['round'] = 'final'             
    if statusVote['round'] == 'four':
        statusVote['round'] = 'five'
    if statusVote['round'] == 'tree':
        statusVote['round'] = 'four'
    if statusVote['round'] == 'two': 
        statusVote['round'] = 'tree'
    if statusVote['round'] == 'one':
        statusVote['round'] = 'two'
    if statusVote['round'] == 'zero':
        statusVote['round'] = 'one'

    print('***************************************')
    print(statusVote)
    return statusVote

       
@route('/status')
def status():
    global statusVote
    return statusVote

@route('/authorization/<name>')
def authorization(name):
    if name == 'admin':
        return countries
    else:
        countries[name] = 'im ready'
    

#@route('/interrogatory/<round>/<name>')
#def interrogatory(round, name):


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