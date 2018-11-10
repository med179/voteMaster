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

divider = 1
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 1920/divider)
Config.set('graphics', 'height', 1200/divider)

class VoteMaser(App):
    def build(self):
        myScreenmanager = ScreenManager()
        self.settings = MySettings()
        self.answer = Answer(name='Answer', settings=self.settings)
        waiting = Waiting(name='Waiting', settings=self.settings)
        admin = Admin(name='Admin', settings=self.settings)
        adminPauseScreen = AdminPauseScreen(name='AdminPauseScreen', settings=self.settings)
        self.result = Result(name='Result', settings=self.settings)
        final = Final(name='Final', settings=self.settings)
        request = Request(settings=self.settings, myScreenmanager=myScreenmanager, restartResult=self.result.restartResult, restartAnswer=self.answer.restartAnswer, updateAnswerLbl=self.answer.updateLbl, updateResultLbl=self.result.updateLbl)
        authorization = Authorization(name='Authorization', settings=self.settings, admin=admin, request=request)
        enterNewIP = EnterNewIP(name='EnterNewIP', settings=self.settings)
        testNewIP = TestNewIP(name='TestNewIP', settings=self.settings)
        myScreenmanager.add_widget(authorization)
        myScreenmanager.add_widget(self.answer)
        myScreenmanager.add_widget(waiting)
        myScreenmanager.add_widget(admin) 
        myScreenmanager.add_widget(adminPauseScreen)
        myScreenmanager.add_widget(self.result)
        myScreenmanager.add_widget(final)
        myScreenmanager.add_widget(enterNewIP)
        myScreenmanager.add_widget(testNewIP)
        #проверка, досупен ли сервер
        try:
            testIP = requests.get(self.settings.IP_Adress + '/test')
        except:
            testIP = 'False'
        if testIP == 'False':
            myScreenmanager.current = 'EnterNewIP'
        else:
        #если доступен, проверяем, логинился ли уже этот игрок/получаем статусы всех игроков
            if self.settings.store.exists('gameStatus'):
                if self.settings.store.get('gameStatus')['data'] == 'gameIsOn':
                    self.settings.clientCoutnry = self.settings.store.get('clientCoutnry')['data']
                #открываем нужный экран    
                    getRound = requests.get(self.settings.IP_Adress+'/status')
                    rounsJson = getRound.json()
                    if rounsJson['round'] == 'zero':
                        myScreenmanager.current = 'Waiting'  
                        return myScreenmanager
                    if rounsJson['round'] == 'one':
                        self.settings.round = 'zero'
                        self.settings.previousRound = 'zero'
                        self.settings.intRound = 0
                    if rounsJson['round'] == 'two':
                        self.settings.round = 'one'
                        self.settings.previousRound = 'one'
                        self.settings.intRound = 1
                    if rounsJson['round'] == 'three':              
                        self.settings.round = 'two'     
                        self.settings.previousRound = 'two'  
                        self.settings.intRound = 2   
                    if rounsJson['round'] == 'four':
                        self.settings.round = 'three'
                        self.settings.previousRound = 'three'
                        self.settings.intRound = 3
                    if rounsJson['round'] == 'five':
                        self.settings.round = 'four'   
                        self.settings.previousRound = 'four' 
                        self.settings.intRound = 4
                    self.updateSettings()
                    self.addAnswerRightWitgets()
                    self.addResultRightWitgets()
                    getData = requests.get(self.settings.IP_Adress+'/authorization/admin')
                    statusPlayers = getData.json()
                    if statusPlayers[self.settings.clientCoutnry] == 'answerIsNotGiven':      
                        myScreenmanager.current = 'Answer'
                    if statusPlayers[self.settings.clientCoutnry] == 'answerGiven':
                        self.settings.round = rounsJson['round']
                        getQuestions = requests.get(self.settings.IP_Adress+'/dictAllQuestions')
                        questionsJson = getQuestions.json()
                        numberOfQuestion = 'Вопрос ' + str(self.settings.intRound+1)
                        question = questionsJson[self.settings.round]
                        result = 'ЗА - '+str(self.settings.votingResult[self.settings.round+'_yes'])+', ПРОТИВ - '+str(self.settings.votingResult[self.settings.round+'_no'])
                        self.answer.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=numberOfQuestion, question=question, result=result))
                        self.answer.colsTwoLayout.add_widget(self.answer.listOfWitgetsOnRightCol[-1].mainLayout)
                        myScreenmanager.current = 'Result'

                    if statusPlayers[self.settings.clientCoutnry] == 'final':
                        myScreenmanager.current = 'Final'

                    request.clientCallback()
            else:
                myScreenmanager.current = 'Authorization'        
        return myScreenmanager

    def addAnswerRightWitgets(self, *args):
        getQuestions = requests.get(self.settings.IP_Adress+'/dictAllQuestions')
        questionsJson = getQuestions.json()
        for i in range(self.settings.intRound):
            strRound = self.settings.dictRounds[str(i+1)]
            numberOfQuestion = 'Вопрос ' + str(i+1)
            question = questionsJson[strRound]
            result = 'ЗА - '+str(self.settings.votingResult[strRound+'_yes'])+', ПРОТИВ - '+str(self.settings.votingResult[strRound+'_no'])
            self.answer.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=numberOfQuestion, question=question, result=result))
            self.answer.colsTwoLayout.add_widget(self.answer.listOfWitgetsOnRightCol[-1].mainLayout)      

    def addResultRightWitgets(self, *args):
        getQuestions = requests.get(self.settings.IP_Adress+'/dictAllQuestions')
        questionsJson = getQuestions.json()
        for i in range(self.settings.intRound):
            strRound = self.settings.dictRounds[str(i+1)]
            numberOfQuestion = 'Вопрос ' + str(i+1)
            question = questionsJson[strRound]
            result = 'ЗА - '+str(self.settings.votingResult[strRound+'_yes'])+', ПРОТИВ - '+str(self.settings.votingResult[strRound+'_no'])
            self.result.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=numberOfQuestion, question=question, result=result))
            self.result.colsTwoLayout.add_widget(self.result.listOfWitgetsOnRightCol[-1].mainLayout)     

    def updateSettings(self, *args):
        response = requests.get(self.settings.IP_Adress+'/allSettings/' + self.settings.previousRound + '/' + self.settings.clientCoutnry)
        allSettings = response.json()
        self.settings.numberOfQuestion = allSettings['numberOfQuestion']
        self.settings.question = allSettings['question']
        self.settings.questionAddition = allSettings['addition']
        response = requests.get(self.settings.IP_Adress+'/result/'+self.settings.round)
        votingResult = response.json()
        self.settings.votingResult = votingResult

class EnterNewIP(Screen):
    def __init__(self, **kwargs):
        super(EnterNewIP, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        self.newIP = ''
        fonLayout = FloatLayout()
        fonEnterNewIP = Image(source='fonWait.png', allow_stretch = True)	
        enterNewIPLayout = BoxLayout(orientation = 'horizontal')
        colOne = BoxLayout(size_hint=[.25, 1])
        colTwo = BoxLayout(orientation = 'vertical', size_hint=[.5, 1])
        colThree = BoxLayout(size_hint=[.25, 1])    
        inputIP = Label(text='[color=C8E3FE][b]Server not found.\nEnter new IP, please.[/b][/color]', markup = True, font_size = 28, size_hint=[1, .3])
        self.textInput = TextInput(multiline = False, size_hint=[1, .05])
        self.textInput.bind(text=self.on_text)
        sendNewIPBtn = RoundedFlatButton(
            on_press=self.sendNewIP,
            text='[color=D7F5FF][b]Test new IP[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=[1, .2],
            background_color=[.47, .69, 1, 1],
            background_normal = '')

        colTwo.add_widget(inputIP)
        colTwo.add_widget(self.textInput)
        colTwo.add_widget(Widget(size_hint=[1, .05]))
        colTwo.add_widget(sendNewIPBtn)
        colTwo.add_widget(Widget(size_hint=[1, .4]))
        enterNewIPLayout.add_widget(colOne)
        enterNewIPLayout.add_widget(colTwo)
        enterNewIPLayout.add_widget(colThree)
        fonLayout.add_widget(fonEnterNewIP)
        fonLayout.add_widget(enterNewIPLayout)
        self.add_widget(fonLayout)

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
        self.statusLbl = Label(text='Connection...')
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
            halign = 'center',
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        tridevCarstvoBtn = RoundedFlatButton(
            on_press=self.tridevCarstvoPress,
            text='[color=D7F5FF][b]Тридевятое\nцарство[/b][/color]', 
            markup = True, 
            halign = 'center',
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        lukomoreBtn = RoundedFlatButton(
            on_press=self.lukomorePress,
            text='[color=D7F5FF][b]Лукоморье[/b][/color]', 
            markup = True, 
            halign = 'center',
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        morskayaDergavaBtn = RoundedFlatButton(
            on_press=self.morskayaDergavaPress,
            text='[color=D7F5FF][b]Морская\nдержава[/b][/color]', 
            markup = True, 
            halign = 'center',
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        shamahanBtn = RoundedFlatButton(
            on_press=self.shamahanPress,
            text='[color=D7F5FF][b]Шамахан[/b][/color]', 
            markup = True, 
            halign = 'center',
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        adminBtn = RoundedFlatButton(
            on_press=self.adminPress,
            text='[color=D7F5FF][b]Админ[/b][/color]', 
            markup = True, 
            halign = 'center',
            font_size = 24,
            size_hint=[1, .25],
            background_color=[1, .10, .10, 1],
            background_normal = '')
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Label(text='[color=C8E3FE][b]Выберите государство[/b][/color]', markup = True, font_size = 28))
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())    
        authorizationLayout.add_widget(riba_kitBtn)
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(tridevCarstvoBtn)
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(lukomoreBtn)
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(morskayaDergavaBtn)
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(shamahanBtn)
        authorizationLayout.add_widget(Widget(size_hint=[1, .5]))
        authorizationLayout.add_widget(Widget(size_hint=[1, .5]))
        authorizationLayout.add_widget(Widget(size_hint=[1, .5]))
        authorizationLayout.add_widget(Widget(size_hint=[1, .5]))
        authorizationLayout.add_widget(Widget(size_hint=[1, .5]))     
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(Widget())
        authorizationLayout.add_widget(adminBtn)
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
        self.red = '[color=DF2447][b]'
        self.green = '[color=01CC8B][b]'
        fonLayout = FloatLayout()
        adminFon = Image(source='adminFon.jpg', allow_stretch = True)
        fonLayout.add_widget(adminFon)
        adminLayout = BoxLayout(orientation='horizontal', spacing=10)
        colOne = BoxLayout(orientation='vertical', spacing=10, size_hint=[.3, 1])
        colTwo = BoxLayout(orientation='vertical', spacing=10, size_hint=[.3, 1])
        riba_kitImg = Image(source='riba_kit.png', allow_stretch = True)
        tridevCarstvoImg = Image(source='tridevCarstvo.png', allow_stretch = True)
        lukomoreImg = Image(source='lukomore.png', allow_stretch = True)
        morskayaDergavaImg = Image(source='morskayaDergava.png', allow_stretch = True)
        shamahanImg  = Image(source='shamahan.png', allow_stretch = True)
        self.riba_kitRdyLbl = Label(text=self.red+'Isn`t ready[/b][/color]', markup = True, font_size = 24)
        self.tridevCarstvoRdyLbl = Label(text=self.red+'Isn`t ready[/b][/color]', markup = True, font_size = 24)
        self.lukomoreRdyLbl = Label(text=self.red+'Isn`t ready[/b][/color]', markup = True, font_size = 24)
        self.morskayaDergavaRdyLbl = Label(text=self.red+'Isn`t ready[/b][/color]', markup = True, font_size = 24)
        self.shamahanRdyLbl = Label(text=self.red+'Isn`t ready[/b][/color]', markup = True, font_size = 24)
        riba_kitBox = BoxLayout(orientation='horizontal', spacing=10)
        tridevCarstvoBox = BoxLayout(orientation='horizontal', spacing=10)
        lukomoreBox = BoxLayout(orientation='horizontal', spacing=10)
        morskayaDergavaBox = BoxLayout(orientation='horizontal', spacing=10)
        shamahanBox = BoxLayout(orientation='horizontal', spacing=10)
        riba_kitBox.add_widget(riba_kitImg)
        riba_kitBox.add_widget(self.riba_kitRdyLbl)
        tridevCarstvoBox.add_widget(tridevCarstvoImg)
        tridevCarstvoBox.add_widget(self.tridevCarstvoRdyLbl)
        lukomoreBox.add_widget(lukomoreImg)
        lukomoreBox.add_widget(self.lukomoreRdyLbl)
        morskayaDergavaBox.add_widget(morskayaDergavaImg)
        morskayaDergavaBox.add_widget(self.morskayaDergavaRdyLbl)
        shamahanBox.add_widget(shamahanImg)
        shamahanBox.add_widget(self.shamahanRdyLbl)
        startBtn = RoundedFlatButton(
            on_press=self.changeStatusVote,
            text='[color=D7F5FF][b]Start next round[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=[1, .3],
            background_color=[.47, .69, 1, 1],
            background_normal = '')
        restartBtn = RoundedFlatButton(
            on_press=self.restartApp,
            text='[color=D7F5FF][b]Restart App[/b][/color]', 
            markup = True, 
            font_size = 24,
            size_hint=[1, .3],
            background_color=[.81, .14, .28, 1],
            background_normal = '')
        colOne.add_widget(Widget(size_hint=[1, .15]))
        colOne.add_widget(riba_kitBox)
        colOne.add_widget(tridevCarstvoBox)
        colOne.add_widget(lukomoreBox)
        colOne.add_widget(morskayaDergavaBox)
        colOne.add_widget(shamahanBox)
        colOne.add_widget(Widget(size_hint=[1, .15]))
        colTwo.add_widget(Widget(size_hint=[1, .3]))
        colTwo.add_widget(startBtn)
        colTwo.add_widget(Widget(size_hint=[1, .2]))
        colTwo.add_widget(restartBtn)
        colTwo.add_widget(Widget(size_hint=[1, .3]))
        adminLayout.add_widget(Widget(size_hint=[.05, 1]))
        adminLayout.add_widget(colOne)
        adminLayout.add_widget(Widget(size_hint=[.3, 1]))
        adminLayout.add_widget(colTwo)
        adminLayout.add_widget(Widget(size_hint=[.05, 1]))
        fonLayout.add_widget(adminLayout)
        self.add_widget(fonLayout)
        self.bind(on_pre_enter=self.cleanStatusPlayers)
    
    def restartApp(self, *args):
        requests.get(self.settings.IP_Adress+'/restartApp')
        self.cleanStatusPlayers()

    def cleanStatusPlayers(self, *args):
        self.riba_kitRdyLbl.text = self.red+'Isn`t ready[/b][/color]'
        self.tridevCarstvoRdyLbl.text = self.red+'Isn`t ready[/b][/color]'
        self.lukomoreRdyLbl.text = self.red+'Isn`t ready[/b][/color]'
        self.morskayaDergavaRdyLbl.text = self.red+'Isn`t ready[/b][/color]'
        self.shamahanRdyLbl.text = self.red+'Isn`t ready[/b][/color]'

    def changeStatusVote(self, *args):
        requests.get(self.settings.IP_Adress+'/changeStatusVote')
        self.manager.current = 'AdminPauseScreen'

    def callback(self, *args):
        Clock.schedule_interval(self.getStatusPlayrs, 1)

    def getStatusPlayrs(self, *args):
        isPlayersReady = requests.get(self.settings.IP_Adress+'/authorization/admin')
        playersStatus = isPlayersReady.json()
        if playersStatus['riba_kit'] == 'im ready' or playersStatus['riba_kit'] == 'answerGiven':
            self.riba_kitRdyLbl.text = self.green+'Is ready[/b][/color]'
        if playersStatus['tridevCarstvo'] == 'im ready' or playersStatus['tridevCarstvo'] == 'answerGiven':
            self.tridevCarstvoRdyLbl.text = self.green+'Is ready[/b][/color]'
        if playersStatus['lukomore'] == 'im ready' or playersStatus['lukomore'] == 'answerGiven':
            self.lukomoreRdyLbl.text = self.green+'Is ready[/b][/color]'
        if playersStatus['morskayaDergava'] == 'im ready' or playersStatus['morskayaDergava'] == 'answerGiven':
            self.morskayaDergavaRdyLbl.text = self.green+'Is ready[/b][/color]'
        if playersStatus['shamahan'] == 'im ready' or playersStatus['shamahan'] == 'answerGiven':
            self.shamahanRdyLbl.text = self.green+'Is ready[/b][/color]'


class AdminPauseScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminPauseScreen, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        fonLayout = FloatLayout()
        adminFon = Image(source='adminFon.jpg', allow_stretch = True)
        mainScreen = BoxLayout()
        roundLbl = Label(text='[color=D7F5FF][b]Transition to the \nnext level...[/b][/color]', markup = True, font_size = 30, size_hint=[1, .3])
        mainScreen.add_widget(roundLbl)
        mainScreen.add_widget(Widget(size_hint=[1, .8]))
        fonLayout.add_widget(adminFon)
        fonLayout.add_widget(mainScreen)
        self.add_widget(fonLayout)
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
        self.restartAnswer = kwargs['restartAnswer']
        self.restartResult = kwargs['restartResult']

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
        self.restartAnswer()
        self.restartResult()
        for key in self.settings.votingResult:
            self.settings.votingResult[key] = 0
        self.settings.store.put('gameStatus', data='gameIsOff')
        self.myScreenmanager.current = 'Waiting'


class MySettings(object):
    def __init__(self, *args):
        self.store = DictStore('user.dat')
        self.clientCoutnry = 'notSpecified'
        self.previousRound = ''
        self.intRound = 0
        self.dictRounds = {'0':'zero', '1':'one', '2':'two', '3':'three', '4':'four', '5':'five'}
        self.round = 'zero'
        self.IP_Adress = 'http://localhost:8080'
        self.question = ''
        self.questionAddition = ''
        self.numberOfQuestion = ''
        self.votingResult = {'zero_yes':0, 'zero_no':0, 'one_yes':0, 'one_no':0, 'two_yes':0, 'two_no':0, 'three_yes':0, 'three_no':0, 'four_yes':0, 'four_no':0, 'five_yes':0, 'five_no':0, 'final_yes':0, 'final_no':0}
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
        #тут же обновим текст на кнопке
        self.waitBtn.text = '[color=D7F5FF][b]ПРИСТУПИТЬ К ГОЛОСОВАНИЮ[/b][/color]'


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
        rowsOneInColsOneLayout.add_widget(Widget(size_hint=(0.05, 1)))
        rowsOneInColsOneLayout.add_widget(self.blazonImg)
        rowsOneInColsOneLayout.add_widget(Widget(size_hint=(0.05, 1)))
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
        if self.settings.round == 'zero' or self.settings.round == 'one':
            self.listOfWitgetsOnRightCol.append(WitgetForRightCol(numberOfQuestion=self.settings.numberOfQuestion, question=self.settings.question))
            self.colsTwoLayout.add_widget(self.listOfWitgetsOnRightCol[-1].mainLayout)
        else:
            self.listOfWitgetsOnRightCol[-1].rowThreeLbl.text = '[color=D9FFFF]ЗА - ' + str(self.settings.votingResult[self.settings.previousRound +'_yes']) + ', ПРОТИВ - ' + str(self.settings.votingResult[self.settings.previousRound+'_no']) + '[/color]'
            print (str(self.settings.votingResult[self.settings.previousRound +'_yes']) + ', ПРОТИВ - ' + str(self.settings.votingResult[self.settings.previousRound+'_no']))
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

    def restartAnswer(self, *args):
        for i in range(len(self.listOfWitgetsOnRightCol)):
            self.colsTwoLayout.remove_widget(self.listOfWitgetsOnRightCol[i].mainLayout)


class WitgetForRightCol(Widget):
    def __init__(self, numberOfQuestion, question, **kwargs):
        super(WitgetForRightCol, self).__init__(**kwargs)
        result  = 'Обсуждается'               
        col = '[color=D9FFFF]'
        colClose = '[/color]'
        bs = '[b]'
        bc = '[/b]'
        if kwargs.has_key('result'):
            result = kwargs['result']
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
        rowsOneInColsOneLayout.add_widget(Widget(size_hint=(0.05, 1)))        
        rowsOneInColsOneLayout.add_widget(self.blazonImg)
        rowsOneInColsOneLayout.add_widget(Widget(size_hint=(0.05, 1)))        
        rowsOneInColsOneLayout.add_widget(self.questionLbl)
        colsOneLayout.add_widget(rowsOneInColsOneLayout)
        rowsTwoInColsOneLayout = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        self.ansYes = Label(
            text='[color=01CC8B][b]ЗА[/b][/color]', 
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

    def restartResult(self, *args):
        for i in range(len(self.listOfWitgetsOnRightCol)):
            self.colsTwoLayout.remove_widget(self.listOfWitgetsOnRightCol[i].mainLayout)

    def updateColsTwo(self, *args):
        if self.settings.round == 'zero' or self.settings.round == 'one':
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
        self.ansYes.text = '[color=01CC8B][b]ЗА  [size=48]' + str(self.settings.votingResult[self.settings.round+'_yes']) + '[/size] [/b][/color]'
        self.ansNo.text = '[color=DF2447][b][size=48]' + str(self.settings.votingResult[self.settings.round+'_no']) + '[/size] ПРОТИВ[/b][/color]'
    

class Final(Screen):
    def __init__(self, **kwargs):
        super(Final, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        fonLayout = FloatLayout()
        authFon = Image(source='authFon.png', allow_stretch = True)
        fonLayout.add_widget(authFon)
        finalScreen = GridLayout(spacing = 1, padding=20, cols=5)
        self.roundOne = Label(markup = True, font_size = 15, halign = 'center')
        self.roundTwo = Label(markup = True, font_size = 15, halign = 'center')
        self.roundThree = Label(markup = True, font_size = 15, halign = 'center')
        self.roundFour = Label(markup = True, font_size = 15, halign = 'center')
        self.roundFive = Label(markup = True, font_size = 15, halign = 'center')
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
            return '\n[color=DF2447][b]РЕШЕНИЕ ОТКЛОНЕНО[/b][/color]'
        else:
            return '\n[color=01CC8B][b]РЕШЕНИЕ ПРИНЯТО[/b][/color]'


if __name__ == "__main__":
    VoteMaser().run()