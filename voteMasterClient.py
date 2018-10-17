#!python
# -*- coding: utf-8 -*-

#voteMaser - client part
from __future__ import unicode_literals

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore
from kivy.uix.textinput import TextInput
import requests
from time import sleep
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior

divider = 2
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 1920/divider)
Config.set('graphics', 'height', 1200/divider)

class VoteMaser(App):
    def build(self):
        myScreenmanager = ScreenManager()
        settings = MySettings()
        answer = Answer(name='Answer', settings=settings)
        waiting = Waiting(name='Waiting', settings=settings)
        admin = Admin(name='Admin', settings=settings)
        adminPauseScreen = AdminPauseScreen(name='AdminPauseScreen', settings=settings)
        result = Result(name='Result', settings=settings)
        final = Final(name='Final', settings=settings)
        request = Request(settings=settings, myScreenmanager=myScreenmanager, updateAnswerLbl=answer.updateLbl, updateResultLbl=result.updateLbl)
        authorization = Authorization(name='Authorization', settings=settings, admin=admin, request=request)
        enterNewIP = EnterNewIP(name='EnterNewIP', settings=settings)
        testNewIP = TestNewIP(name='TestNewIP', settings=settings)
        myScreenmanager.add_widget(authorization)
        myScreenmanager.add_widget(answer)
        myScreenmanager.add_widget(waiting)
        myScreenmanager.add_widget(admin) 
        myScreenmanager.add_widget(adminPauseScreen)
        myScreenmanager.add_widget(result)
        myScreenmanager.add_widget(final)
        myScreenmanager.add_widget(enterNewIP)
        myScreenmanager.add_widget(testNewIP)
        #проверка, досупен ли сервер
        try:
            testIP = requests.get(settings.IP_Adress + '/test')
        except:
            testIP = 'False'
        if testIP == 'False':
            myScreenmanager.current = 'EnterNewIP'
        else:
        #если доступен, проверяем, логинился ли уже этот игрок/получаем статусы всех игроков
            if settings.store.exists('gameStatus'):
                if settings.store.get('gameStatus')['data'] == 'gameIsOn':
                    settings.clientCoutnry = settings.store.get('clientCoutnry')['data']
                #открываем нужный экран    
                    getData = requests.get(settings.IP_Adress+'/authorization/admin')
                    statusPlayers = getData.json()
                    if statusPlayers[settings.clientCoutnry] == 'answerIsNotGiven':
                        getRound = requests.get(settings.IP_Adress+'/status')
                        rounsJson = getRound.json()
                        if rounsJson['round'] == 'one':
                            settings.round = 'zero'
                        if rounsJson['round'] == 'two':
                            settings.round = 'one'
                        if rounsJson['round'] == 'three':              
                            settings.round = 'two'          
                        if rounsJson['round'] == 'four':
                            settings.round = 'three'
                        if rounsJson['round'] == 'five':
                            settings.round = 'four'   
                        request.clientCallback()      
                        myScreenmanager.current = 'Answer'
                    if statusPlayers[settings.clientCoutnry] == 'answerGiven':
                        getRound = requests.get(settings.IP_Adress+'/status')
                        rounsJson = getRound.json()
                        settings.round = rounsJson['round']
                        request.clientCallback()
                        myScreenmanager.current = 'Result'
                    if statusPlayers[settings.clientCoutnry] == 'final':
                        request.clientCallback()
                        myScreenmanager.current = 'Final'
            else:
                myScreenmanager.current = 'Authorization'        
        return myScreenmanager


class EnterNewIP(Screen):
    def __init__(self, **kwargs):
        super(EnterNewIP, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        self.newIP = ''
        body = BoxLayout(orientation = 'vertical')
        inputIP = Label(text='Server not found.\nEnter new IP, please')
        self.textInput = TextInput(multiline = False)
        self.textInput.bind(text=self.on_text)
        sendNewIPBtn = Button(on_press=self.sendNewIP)
        body.add_widget(inputIP)
        body.add_widget(self.textInput)
        body.add_widget(sendNewIPBtn)
        self.add_widget(body)

    def on_text(self, instance, value):
        self.newIP = value

    def sendNewIP(self, *args):
        self.settings.IP_Adress = self.newIP
        self.settings.store.put('IP', data=self.newIP)
        self.manager.current = 'TestNewIP'


class TestNewIP(Screen):
    def __init__(self, **kwargs):
        super(TestNewIP, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        self.statusLbl = Label(text='Connection')
        self.add_widget(self.statusLbl)
        self.bind(on_enter=self.testNewIP)

    def testNewIP(self, *args):
        sleep(1)
        try:
            testIP = requests.get(self.settings.IP_Adress + '/test')
        except:
            testIP = 'False'
        if testIP == 'False':
            self.statusLbl.text = "It isn't working, try again."
            sleep(2)
            self.manager.current = 'EnterNewIP'
        else:
            self.statusLbl.text = "It's working, thank you!!!"
            sleep(2)
            self.manager.current = 'Authorization'


class Authorization(Screen):
    def __init__(self, **kwargs):
        super(Authorization, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        self.admin = kwargs['admin']
        self.request = kwargs['request']
        fonLayout = FloatLayout()
        authFon = Image(source='authFon.png', allow_stretch = True)
        fonLayout.add_widget(authFon)
        authorizationLayout = GridLayout(spacing = 20, cols=5)
        riba_kitBtn = RoundedFlatButton(
            on_press=self.riba_kitPress,
            text='[color=D7F5FF][b]Рыба-кит[/b][/color]', 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        tridevCarstvoBtn = RoundedFlatButton(
            on_press=self.tridevCarstvoPress,
            text='[color=D7F5FF][b]Тридевятое\nцарство[/b][/color]', 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        lukomoreBtn = RoundedFlatButton(
            on_press=self.lukomorePress,
            text='[color=D7F5FF][b]Лукоморье[/b][/color]', 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        morskayaDergavaBtn = RoundedFlatButton(
            on_press=self.morskayaDergavaPress,
            text='[color=D7F5FF][b]Морская\nдержава[/b][/color]', 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        shamahanBtn = RoundedFlatButton(
            on_press=self.shamahanPress,
            text='[color=D7F5FF][b]Шамахан[/b][/color]', 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        adminBtn = RoundedFlatButton(
            on_press=self.adminPress,
            text='[color=D7F5FF][b]Админ[/b][/color]', 
            markup = True, 
            font_size = 24,
            background_color=[1, .10, .10, 1],
            background_normal = '')
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Label(text='[color=C8E3FE][b]Выберите государство[/b][/color]', markup = True, font_size = 28))
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())    
        authorizationLayout.add_widget(riba_kitBtn)
        authorizationLayout.add_widget(tridevCarstvoBtn)
        authorizationLayout.add_widget(lukomoreBtn)
        authorizationLayout.add_widget(morskayaDergavaBtn)
        authorizationLayout.add_widget(shamahanBtn)
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(adminBtn)
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        fonLayout.add_widget(authorizationLayout)

        self.add_widget(fonLayout)

    def login(self, name):
        self.request.clientCallback()
        self.settings.clientCoutnry = name
        self.settings.store.put('clientCoutnry', data=name)
        self.settings.store.put('gameStatus', data='gameIsOn')
        self.manager.current = 'Waiting'

    def adminPress(self, *args):
        self.settings.clientCoutnry = 'admin'
        self.admin.callback()
        self.manager.current = 'Admin'

    def riba_kitPress(self, *args):
        self.login('riba_kit')

    def tridevCarstvoPress(self, *args):
        self.login('tridevCarstvo')

    def lukomorePress(self, *args):
        self.login('lukomore')

    def morskayaDergavaPress(self, *args):
        self.login('morskayaDergava')

    def shamahanPress(self, *args):
        self.login('shamahan')


class Admin(Screen):
    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        adminLayout = BoxLayout(orientation='vertical', spacing=10)
        readyBtns = BoxLayout(orientation='horizontal', spacing=10)
        self.riba_kitRdyLbl = Button(text='riba_kit', background_color=[1, 0, 0, 1])
        self.tridevCarstvoRdyLbl = Button(text='tridevCarstvo', background_color=[1, 0, 0, 1])
        self.lukomoreRdyLbl = Button(text='lukomore', background_color=[1, 0, 0, 1])
        self.morskayaDergavaRdyLbl = Button(text='morskayaDergava', background_color=[1, 0, 0, 1])
        self.shamahanRdyLbl = Button(text='shamahan', background_color=[1, 0, 0, 1])
        readyBtns.add_widget(self.riba_kitRdyLbl)
        readyBtns.add_widget(self.tridevCarstvoRdyLbl)
        readyBtns.add_widget(self.lukomoreRdyLbl)
        readyBtns.add_widget(self.morskayaDergavaRdyLbl)
        readyBtns.add_widget(self.shamahanRdyLbl)
        startBtn = Button(text='Start next round', size_hint=[.3, .3], on_press=self.changeStatusVote, background_color=[1, 0, 0, 1])
        restartBtn = Button(text='Restart App', size_hint=[.3, .3], on_press=self.restartApp, background_color=[0, 0, 1, 1] )
        adminLayout.add_widget(readyBtns)
        adminLayout.add_widget(startBtn)
        adminLayout.add_widget(restartBtn)
        self.add_widget(adminLayout)
        self.bind(on_pre_enter=self.cleanStatusPlayers)
    
    def restartApp(self, *args):
        requests.get(self.settings.IP_Adress+'/restartApp')
        self.cleanStatusPlayers()

    def cleanStatusPlayers(self, *args):
        self.riba_kitRdyLbl.background_color = [1, 0, 0, 1]
        self.tridevCarstvoRdyLbl.background_color = [1, 0, 0, 1]
        self.lukomoreRdyLbl.background_color = [1, 0, 0, 1]
        self.morskayaDergavaRdyLbl.background_color = [1, 0, 0, 1]
        self.shamahanRdyLbl.background_color = [1, 0, 0, 1]        

    def changeStatusVote(self, *args):
        requests.get(self.settings.IP_Adress+'/changeStatusVote')
        self.manager.current = 'AdminPauseScreen'

    def callback(self, *args):
        Clock.schedule_interval(self.getStatusPlayrs, 1)

    def getStatusPlayrs(self, *args):
        isPlayersReady = requests.get(self.settings.IP_Adress+'/authorization/admin')
        playersStatus = isPlayersReady.json()
        if playersStatus['riba_kit'] == 'im ready' or playersStatus['riba_kit'] == 'answerGiven':
            self.riba_kitRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['tridevCarstvo'] == 'im ready' or playersStatus['tridevCarstvo'] == 'answerGiven':
            self.tridevCarstvoRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['lukomore'] == 'im ready' or playersStatus['lukomore'] == 'answerGiven':
            self.lukomoreRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['morskayaDergava'] == 'im ready' or playersStatus['morskayaDergava'] == 'answerGiven':
            self.morskayaDergavaRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['shamahan'] == 'im ready' or playersStatus['shamahan'] == 'answerGiven':
            self.shamahanRdyLbl.background_color = [0, 1, 0, 1]        


class AdminPauseScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminPauseScreen, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        mainScreen = BoxLayout()
        roundLbl = Label(text='PAUSE')
        mainScreen.add_widget(roundLbl)
        self.add_widget(mainScreen)
        self.bind(on_enter=self.changeScreen)

    def changeScreen(self, *args):
        sleep(3)
        self.manager.current = 'Admin'


class Request():
    def __init__(self, **kwargs):
        self.settings = kwargs['settings']
        self.myScreenmanager = kwargs['myScreenmanager']
        self.updateResultLbl = kwargs['updateResultLbl']
        self.updateAnswerLbl = kwargs['updateAnswerLbl']

    def clientCallback(self, *args):
        Clock.schedule_interval(self.callbackAllSettings, 1)
        Clock.schedule_interval(self.callbackVotingResult, 1)

    def callbackAllSettings(self, *args): 
        response = requests.get(self.settings.IP_Adress+'/allSettings/' + self.settings.round + '/' + self.settings.clientCoutnry)
        allSettings = response.json()
        if allSettings['isAllRight'] == 'restartNow':
            self.restart()
        if allSettings['isAllRight'] == 'False':
            self.settings.previousRound = self.settings.round
            self.settings.round = allSettings['round']
            self.settings.numberOfQuestion = allSettings['numberOfQuestion']
            self.settings.question = allSettings['question']
            self.settings.questionAddition = allSettings['addition']
            self.updateAnswerLbl()
            if self.settings.round == 'final':
                self.myScreenmanager.current = 'Final'          
            else:
                self.myScreenmanager.current = 'Answer'

    def callbackVotingResult(self, *args): 
        response = requests.get(self.settings.IP_Adress+'/result/'+self.settings.round)
        votingResult = response.json()
        self.settings.votingResult = votingResult
        self.updateResultLbl()

    def restart(self, *args):
        self.settings.round = 'zero'
        self.settings.question = ''
        for key in self.settings.votingResult:
            self.settings.votingResult[key] = 0
        self.settings.store.put('gameStatus', data='gameIsOff')
        self.myScreenmanager.current = 'Waiting'


class MySettings(object):
    def __init__(self, *args):
        self.store = DictStore('user.dat')
        self.clientCoutnry = 'notSpecified'
        self.previousRound = ''
        self.round = 'zero'
        self.IP_Adress = 'http://localhost:8080'
        self.question = ''
        self.questionAddition = ''
        self.numberOfQuestion = ''
        self.votingResult = {'zero_yes':0, 'zero_no':0, 'final_yes':0, 'final_no':0}
        if self.store.exists('IP'):
            self.IP_Adress = self.store.get('IP')['data']


class RoundedWidget(Widget):
    def __init__(self, **kwargs):
        super(RoundedWidget, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0)
        self.background_normal = ''
        if kwargs.has_key('background_color'):
            background_color = kwargs['background_color']
        else:
            background_color = (1, 1, 1, 0)
        with self.canvas.before:    
            Color(rgba=background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RoundedFlatButton(ButtonBehavior, RoundedWidget, Label):
    pass


class Waiting(Screen):
    def __init__(self, **kwargs):
        super(Waiting, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        fonLayout = FloatLayout()
        fonWait = Image(source='fonWait.png', allow_stretch = True)	
        waitLayout = BoxLayout(orientation='horizontal')
        colsOneLayout = BoxLayout(orientation='vertical', size_hint=(.25, 1))
        colsOneLayout.add_widget(Widget(size_hint=(1, .1)))
        self.blazonImg = Image(allow_stretch = True, size_hint=(1, .5))
        colsOneLayout.add_widget(self.blazonImg)
        colsOneLayout.add_widget(Widget())                           
        colsTwoLayout = BoxLayout(orientation='vertical', size_hint=(.5, 1))
        label = Label(
            text='[color=C8E3FE][b]Совещание совета безопасности[/b][/color]',  
            markup = True, 
            font_size = 28)
        colsTwoLayout.add_widget(label)
        colsTwoLayout.add_widget(Widget())
        self.waitBtn = RoundedFlatButton(
            text='[color=D7F5FF][b]ПРИСТУПИТЬ К ГОЛОСОВАНИЮ[/b][/color]', 
            on_press=self.imReady, 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')  
        colsTwoLayout.add_widget(self.waitBtn)
        colsTwoLayout.add_widget(Widget())
        colsTwoLayout.add_widget(Widget())
        colsThreeLayout = BoxLayout(orientation='vertical', size_hint=(.25, 1))
        colsThreeLayout.add_widget(Widget())      
        waitLayout.add_widget(colsOneLayout)
        waitLayout.add_widget(colsTwoLayout)
        waitLayout.add_widget(colsThreeLayout)
        fonLayout.add_widget(fonWait)
        fonLayout.add_widget(waitLayout)
        self.add_widget(fonLayout)
        self.bind(on_pre_enter=self.updateBlazonImg)

    def imReady(self, *args):
        requests.get(self.settings.IP_Adress+'/authorization/'+self.settings.clientCoutnry)
        self.waitBtn.text = '[color=D7F5FF][b]ОЖИДАНИЕ ИГРОКОВ[/b][/color]'

    def updateBlazonImg(self, *args):
        self.blazonImg.source = self.settings.clientCoutnry + '.png'


class Answer(Screen):
    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        self.listOfWitgetsOnRightCol = []
        fonLayout = FloatLayout()
        fonAnswer = Image(source='fonAnswer.png', allow_stretch = True)	
        answerLayout = BoxLayout(orientation='horizontal')
        colsOneLayout = BoxLayout(orientation='vertical', size_hint=(.69, 1))
        rowsOneInColsOneLayout = BoxLayout(orientation='horizontal', size_hint=(1, .5))
        self.blazonImg = Image(source='riba_kit.png', allow_stretch = True, size_hint=(.4, 1))
        self.questionLbl = Label(text='ВОПРОС', size_hint=(.6, 1), markup = True, font_size = 28, halign='left', valign='center')
        self.questionLbl.bind(size=self.questionLbl.setter('text_size'))
        rowsOneInColsOneLayout.add_widget(self.blazonImg)
        rowsOneInColsOneLayout.add_widget(self.questionLbl)
        colsOneLayout.add_widget(rowsOneInColsOneLayout)

        rowsTwoInColsOneLayout = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        btnYes = RoundedFlatButton(
            on_press = self.answerYes,
            text='[color=D7F5FF][b]ЗА[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=(.7, .5),
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        btnNo = RoundedFlatButton(
            on_press = self.answerNo,
            text='[color=D7F5FF][b]ПРОТИВ[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=(.7, .5),
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        rowsTwoInColsOneLayout.add_widget(Widget(size_hint=(.2, 1)))
        rowsTwoInColsOneLayout.add_widget(btnYes)
        rowsTwoInColsOneLayout.add_widget(Widget(size_hint=(.1, 1)))
        rowsTwoInColsOneLayout.add_widget(btnNo)
        rowsTwoInColsOneLayout.add_widget(Widget(size_hint=(.2, 1)))
        colsOneLayout.add_widget(rowsTwoInColsOneLayout)
        colsOneLayout.add_widget(Widget(size_hint=(1, .2)))
        self.colsTwoLayout = GridLayout(rows=7, size_hint=(.31, 1), row_force_default=True, row_default_height=150)
        answerLayout.add_widget(colsOneLayout)
        answerLayout.add_widget(Widget(size_hint=(.05, 1)))
        answerLayout.add_widget(self.colsTwoLayout)
        fonLayout.add_widget(fonAnswer)
        fonLayout.add_widget(answerLayout)
        self.bind(on_pre_enter=self.updateColsTwo)
        self.bind(on_pre_enter=self.updateBlazonImg)
        self.add_widget(fonLayout)

    def updateBlazonImg(self, *args):
        self.blazonImg.source = self.settings.clientCoutnry + '.png'

    def updateColsTwo(self, *args):
        if self.settings.round == 'one':
            self.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=self.settings.numberOfQuestion, question=self.settings.question))
            self.colsTwoLayout.add_widget(self.listOfWitgetsOnRightCol[-1].mainLayout)
        else:
            print self.settings.votingResult
            self.listOfWitgetsOnRightCol[-1].rowThreeLbl.text = '[color=D9FFFF]ЗА - ' + str(self.settings.votingResult[self.settings.previousRound +'_yes']) + ', ПРОТИВ - ' + str(self.settings.votingResult[self.settings.previousRound+'_no']) + '[/color]'
            self.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=self.settings.numberOfQuestion, question=self.settings.question))          
            self.colsTwoLayout.add_widget(self.listOfWitgetsOnRightCol[-1].mainLayout)

    def updateLbl(self, *args):
        colOneBold = '[color=8B452D][b]'
        colOneBoldClose = '[/b][/color]'
        colTwo = '\n[color=7F635D]'
        colTrhee = '\n[color=A6A8B4]'
        colClose = '[/color]'
        self.questionLbl.text = colOneBold + self.settings.numberOfQuestion + colOneBoldClose + colTwo + self.settings.question + colClose + colTrhee + self.settings.questionAddition + colClose

    def answerYes(self, *args):
            requests.get(self.settings.IP_Adress+'/answer/'+self.settings.round+'/'+self.settings.clientCoutnry+'/yes')
            self.manager.current = 'Result'

    def answerNo(self, *args):
            requests.get(self.settings.IP_Adress+'/answer/'+self.settings.round+'/'+self.settings.clientCoutnry+'/no')
            self.manager.current = 'Result'


class WitgetForRightCol(Widget):
    def __init__(self, numberOfQuestion, question, **kwargs):
        super(WitgetForRightCol, self).__init__(**kwargs)
        result  = 'Обсуждается'               
        col = '[color=D9FFFF]'
        colClose = '[/color]'
        bs = '[b]'
        bc = '[/b]'
        self.mainLayout = BoxLayout(orientation='vertical')
        rowOneLbl = Label(markup = True, font_size = 18, halign='left', valign='center', size_hint=(1, .25))
        rowOneLbl.text = col + bs + numberOfQuestion + bc + colClose
        rowOneLbl.bind(size=rowOneLbl.setter('text_size'))
        rowTwoLbl = Label(markup = True, font_size = 16, halign='left', valign='center', size_hint=(1, .5))
        rowTwoLbl.text = col + question + colClose
        rowTwoLbl.bind(size=rowTwoLbl.setter('text_size'))
        self.rowThreeLbl = Label(markup = True, font_size = 14, halign='left', valign='center', size_hint=(1, .25))
        self.rowThreeLbl.text = col + result + colClose
        self.rowThreeLbl.bind(size=self.rowThreeLbl.setter('text_size'))
        self.mainLayout.add_widget(rowOneLbl)
        self.mainLayout.add_widget(rowTwoLbl)
        self.mainLayout.add_widget(self.rowThreeLbl)


class Result(Screen):
    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        self.listOfWitgetsOnRightCol = []
        fonLayout = FloatLayout()
        fonResult = Image(source='fonResult.png', allow_stretch = True)	
        resultLayout = BoxLayout(orientation='horizontal')
        colsOneLayout = BoxLayout(orientation='vertical', size_hint=(.69, 1))
        rowsOneInColsOneLayout = BoxLayout(orientation='horizontal', size_hint=(1, .5))
        self.blazonImg = Image(source='riba_kit.png', allow_stretch = True, size_hint=(.4, 1))
        self.questionLbl = Label(text='ВОПРОС', size_hint=(.6, 1), markup = True, font_size = 28, halign='left', valign='center')
        self.questionLbl.bind(size=self.questionLbl.setter('text_size'))
        rowsOneInColsOneLayout.add_widget(self.blazonImg)
        rowsOneInColsOneLayout.add_widget(self.questionLbl)
        colsOneLayout.add_widget(rowsOneInColsOneLayout)
        rowsTwoInColsOneLayout = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        self.ansYes = Label(
            text='[color=00642F][b]ЗА[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=(.7, .5))
        self.ansNo = Label(
            text='[color=FD0302][b]ПРОТИВ[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=(.7, .5))
        rowsTwoInColsOneLayout.add_widget(Widget(size_hint=(.2, 1)))
        rowsTwoInColsOneLayout.add_widget(self.ansYes)
        rowsTwoInColsOneLayout.add_widget(Widget(size_hint=(.1, 1)))
        rowsTwoInColsOneLayout.add_widget(self.ansNo )
        rowsTwoInColsOneLayout.add_widget(Widget(size_hint=(.2, 1)))
        colsOneLayout.add_widget(rowsTwoInColsOneLayout)
        colsOneLayout.add_widget(Widget(size_hint=(1, .2)))
        resultLayout.add_widget(colsOneLayout)
        resultLayout.add_widget(Widget(size_hint=(.05, 1)))
        self.colsTwoLayout = GridLayout(rows=7, size_hint=(.31, 1), row_force_default=True, row_default_height=150)
        resultLayout.add_widget(self.colsTwoLayout)
        fonLayout.add_widget(fonResult)
        fonLayout.add_widget(resultLayout)
        self.bind(on_pre_enter=self.updateBlazonImg)
        self.bind(on_pre_enter=self.updateQuestionLbl)
        self.bind(on_pre_enter=self.updateColsTwo)
        self.add_widget(fonLayout)

    def updateColsTwo(self, *args):
        if self.settings.round == 'one':
            self.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=self.settings.numberOfQuestion, question=self.settings.question))
            self.colsTwoLayout.add_widget(self.listOfWitgetsOnRightCol[-1].mainLayout)
        else:
            print self.settings.votingResult
            self.listOfWitgetsOnRightCol[-1].rowThreeLbl.text = '[color=D9FFFF]ЗА - ' + str(self.settings.votingResult[self.settings.previousRound +'_yes']) + ', ПРОТИВ - ' + str(self.settings.votingResult[self.settings.previousRound+'_no']) + '[/color]'
            self.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=self.settings.numberOfQuestion, question=self.settings.question))          
            self.colsTwoLayout.add_widget(self.listOfWitgetsOnRightCol[-1].mainLayout)

    def updateQuestionLbl(self, *args):
        colOneBold = '[color=8B452D][b]'
        colOneBoldClose = '[/b][/color]'
        colTwo = '\n[color=7F635D]'
        colTrhee = '\n[color=A6A8B4]'
        colClose = '[/color]'
        self.questionLbl.text = colOneBold + self.settings.numberOfQuestion + colOneBoldClose + colTwo + self.settings.question + colClose + colTrhee + self.settings.questionAddition + colClose

    def updateBlazonImg(self, *args):
        self.blazonImg.source = self.settings.clientCoutnry + '.png'

    def updateLbl(self, *args):
        self.ansYes.text = '[color=00642F][b]ЗА  [size=48]' + str(self.settings.votingResult[self.settings.round+'_yes']) + '[/size] [/b][/color]'
        self.ansNo.text = '[color=FD0302][b][size=48]' + str(self.settings.votingResult[self.settings.round+'_no']) + '[/size] ПРОТИВ[/b][/color]'
    

class Final(Screen):
    def __init__(self, **kwargs):
        super(Final, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        fonLayout = FloatLayout()
        authFon = Image(source='authFon.png', allow_stretch = True)
        fonLayout.add_widget(authFon)
        finalScreen = GridLayout(spacing = 1, cols=5)
        self.roundOne = Label(markup = True, font_size = 16)
        self.roundTwo = Label(markup = True, font_size = 16)
        self.roundThree = Label(markup = True, font_size = 16)
        self.roundFour = Label(markup = True, font_size = 16)
        self.roundFive = Label(markup = True, font_size = 16)
        finalScreen.add_widget(Widget())
        finalScreen.add_widget(Widget())
        finalScreen.add_widget(Label(text='[color=C8E3FE][b]Подведение итогов[/b][/color]', markup = True, font_size = 28))
        finalScreen.add_widget(Widget())
        finalScreen.add_widget(Widget())    
        finalScreen.add_widget(self.roundOne)
        finalScreen.add_widget(Widget())

        finalScreen.add_widget(self.roundTwo)
        finalScreen.add_widget(Widget())

        finalScreen.add_widget(self.roundThree)

        finalScreen.add_widget(Widget())

        finalScreen.add_widget(self.roundFour)
        finalScreen.add_widget(Widget())

        finalScreen.add_widget(self.roundFive)
        finalScreen.add_widget(Widget())

        finalScreen.add_widget(Widget())   
        finalScreen.add_widget(Widget())
        finalScreen.add_widget(Widget())   
        finalScreen.add_widget(Widget()) 
        finalScreen.add_widget(Widget()) 

        finalScreen.add_widget(Widget()) 
        finalScreen.add_widget(Widget()) 
        finalScreen.add_widget(Widget()) 
        finalScreen.add_widget(Widget()) 
        fonLayout.add_widget(finalScreen)
        self.bind(on_pre_enter=self.updateFinalLabels)
        self.add_widget(fonLayout)   

    def updateFinalLabels(self, *args):
        col = '[color=D9FFFF][b]'
        colClose = '[/b][/color]'
        getQuestions = requests.get(self.settings.IP_Adress+'/dictAllQuestions')
        questionsJson = getQuestions.json()
        self.roundOne.text = col + questionsJson['one'] + colClose + self.resultInRound('one')
        self.roundOne.bind(size=self.roundOne.setter('text_size'))
        self.roundTwo.text = col + questionsJson['two'] + colClose + self.resultInRound('two')
        self.roundTwo.bind(size=self.roundTwo.setter('text_size'))
        self.roundThree.text = col + questionsJson['three'] + colClose + self.resultInRound('three')
        self.roundThree.bind(size=self.roundThree.setter('text_size'))
        self.roundFour.text = col + questionsJson['four'] + colClose + self.resultInRound('four')
        self.roundFour.bind(size=self.roundFour.setter('text_size'))
        self.roundFive.text = col + questionsJson['five'] + colClose + self.resultInRound('five')
        self.roundFive.bind(size=self.roundFive.setter('text_size'))
        

    def resultInRound(self, round, *args):
        if self.settings.votingResult[round+'_yes'] < self.settings.votingResult[round+'_no']:
            return '\n[color=FD0302][b]РЕШЕНИЕ ОТКЛОНЕНО[/b][/color]'
        else:
            return '\n[color=00642F][b]РЕШЕНИЕ ПРИНЯТО[/b][/color]'





if __name__ == "__main__":
    VoteMaser().run()