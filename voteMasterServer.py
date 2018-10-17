#!python
# -*- coding: utf-8 -*-

#voteMaser - server part
from bottle import route, run, template

#список стран пользователей
statusPlayers = {'riba_kit':'', 'tridevCarstvo':'', 'lukomore':'', 'morskayaDergava':'', 'shamahan':''}

question = {
    'one':'Отказ от серебряно-золотого международного валютного стандарта', 
    'two':'Использование территории Чудо-юдо рыбы Кита для размещения коалиционного флота', 
    'three':'Приостановление членства в Организации Объединенных сказочных Наций Кощеева царства', 
    'four':'Введение эмбарго на мертвую воду для Кощеева царства', 
    'five':'Создание бесполетной зоны над Кощеевым царством'}
votingResult = {'zero_yes':0, 'zero_no':0, 'one_yes':0, 'one_no':0, 'two_yes':0, 'two_no':0, 'three_yes':0, 'three_no':0, 'four_yes':0, 'four_no':0, 'five_yes':0, 'five_no':0}
statusVote = {'round':'zero'}
whoHasAlreadyRestarted = {'riba_kit':'alreadyRestarted', 'tridevCarstvo':'alreadyRestarted', 'lukomore':'alreadyRestarted', 'morskayaDergava':'alreadyRestarted', 'shamahan':'alreadyRestarted'}


@route('/test')
def test():
    return 'True'

@route('/dictAllQuestions')
def dictAllQuestions():
    return question

@route('/allSettings/<round>/<name>')
def allSettings(round, name):
    YES = '(большинство должны проголосовать ЗА по этому вопросу)'
    NO = '(большинство должны проголосовать ПРОТИВ по этому вопросу)'

    global whoHasAlreadyRestarted
    returnToClient = {'isAllRight':'False'}
    returnToClient['addition'] = ' '
    returnToClient['numberOfQuestion'] = ' '
    if whoHasAlreadyRestarted[name] == 'heIsNotRestarted':
        returnToClient = {'isAllRight':'restartNow'}
        whoHasAlreadyRestarted[name] = 'alreadyRestarted'  
        return returnToClient
    if round == statusVote['round']:
        returnToClient['isAllRight'] = 'True'
        return returnToClient
    elif round == 'final':            
        returnToClient = votingResult
        returnToClient['isAllRight'] = 'True'
        return returnToClient
    else:
        if round == 'zero':
            returnToClient['question'] = question['one']
            returnToClient['round'] = 'one'
            returnToClient['numberOfQuestion'] = 'Вопрос 1'
            if name == 'riba_kit':
                returnToClient['addition'] = YES
            if name == 'tridevCarstvo':
                returnToClient['addition'] = NO
        if round == 'one':
            returnToClient['question'] = question['two']
            returnToClient['round'] = 'two'
            returnToClient['numberOfQuestion'] = 'Вопрос 2'
            if name == 'tridevCarstvo':
                returnToClient['addition'] = YES
            elif name == 'riba_kit':
                returnToClient['addition'] = NO
        if round == 'two':
            returnToClient['question'] = question['three']
            returnToClient['round'] = 'three'
            returnToClient['numberOfQuestion'] = 'Вопрос 3'
            if name == 'lukomore':
                returnToClient['addition'] = YES
            elif name == 'morskayaDergava':
                returnToClient['addition'] = NO
        if round == 'three':
            returnToClient['question'] = question['four']
            returnToClient['round'] = 'four'
            returnToClient['numberOfQuestion'] = 'Вопрос 4'
            if name == 'shamahan':
                returnToClient['addition'] = YES
            elif name == 'lukomore':
                returnToClient['addition'] = NO
        if round == 'four':
            returnToClient['question'] = question['five']
            returnToClient['round'] = 'five'
            returnToClient['numberOfQuestion'] = 'Вопрос 5'
            if name == 'morskayaDergava':
                returnToClient['addition'] = YES
            elif name == 'shamahan':
                returnToClient['addition'] = NO
        if round == 'five':
            returnToClient['round'] = 'final'
        return returnToClient
        
@route('/changeStatusVote')
def changeStatusVote():
    global statusVote
    global statusPlayers
    if statusVote['round'] == 'five':
        statusVote['round'] = 'final'   
        for key in statusPlayers:
            statusPlayers[key] = 'final'
    if statusVote['round'] == 'four':
        statusVote['round'] = 'five'
        for key in statusPlayers:
            statusPlayers[key] = 'answerIsNotGiven'    
    if statusVote['round'] == 'three':
        statusVote['round'] = 'four'
        for key in statusPlayers:
            statusPlayers[key] = 'answerIsNotGiven'
    if statusVote['round'] == 'two': 
        statusVote['round'] = 'three'
        for key in statusPlayers:
            statusPlayers[key] = 'answerIsNotGiven'    
    if statusVote['round'] == 'one':
        statusVote['round'] = 'two'
        for key in statusPlayers:
            statusPlayers[key] = 'answerIsNotGiven'    
    if statusVote['round'] == 'zero':
        statusVote['round'] = 'one'
        for key in statusPlayers:
            statusPlayers[key] = 'answerIsNotGiven'    
    return statusVote
   
@route('/status')
def status():
    global statusVote
    return statusVote

@route('/authorization/<name>')
def authorization(name):
    if name == 'admin':
        return statusPlayers
    else:
        statusPlayers[name] = 'im ready'
    
@route('/answer/<round>/<name>/<ans>')
def answer(round, name, ans):
    global votingResult
    global statusPlayers
    key = round + '_' + ans
    votingResult[key] += 1
    statusPlayers[name] = 'answerGiven'
    return 'You voted'

@route('/result/<round>')
def result(round):
    return votingResult

@route('/restartApp')
def restartApp():
    global statusVote
    global whoHasAlreadyRestarted
    global votingResult
    statusVote['round'] = 'zero'
    for key in whoHasAlreadyRestarted:
        whoHasAlreadyRestarted[key] = 'heIsNotRestarted'
    for key in votingResult:
        votingResult[key] =  0
    for key in statusPlayers:
        statusPlayers[key] = 'answerIsNotGiven'

run(host='localhost', port=8080)