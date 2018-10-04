#!python
# -*- coding: utf-8 -*-

#voteMaser - client part

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

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 1920/2)
Config.set('graphics', 'height', 1200/2)

class voteMaser(App):
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
        authorizationLayout = BoxLayout(spacing = 10, size_hint = [1, .5])
        riba_kitBtn = Button(text='riba_kitBtn', on_press=self.riba_kitPress)
        tridevCarstvoBtn = Button(text='tridevCarstvoBtn', on_press=self.tridevCarstvoPress)
        lukomoreBtn = Button(text='lukomoreBtn', on_press=self.lukomorePress)
        morskayaDergavaBtn = Button(text='morskayaDergavaBtn', on_press=self.morskayaDergavaPress)
        shamahanBtn = Button(text='shamahanBtn', on_press=self.shamahanPress)
        adminBtn = Button(text='admin', on_press=self.adminPress, background_color=[1, 0, 0, 1])
        authorizationLayout.add_widget(riba_kitBtn)
        authorizationLayout.add_widget(tridevCarstvoBtn)
        authorizationLayout.add_widget(lukomoreBtn)
        authorizationLayout.add_widget(morskayaDergavaBtn)
        authorizationLayout.add_widget(shamahanBtn)
        authorizationLayout.add_widget(adminBtn)
        self.add_widget(authorizationLayout)

    def login(self, name):
        self.request.clientCallback()
        self.manager.current = 'Waiting'
        self.settings.clientCoutnry = name
        self.settings.store.put('clientCoutnry', data=name)
        self.settings.store.put('gameStatus', data='gameIsOn')

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
            self.settings.question = allSettings['question']
            self.updateAnswerLbl()
            self.settings.round = allSettings['round']
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
        self.round = 'zero'
        self.IP_Adress = 'http://localhost:8080'
        self.question = ''
        self.votingResult = {'zero_yes':0, 'zero_no':0}
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
#            Color(rgba=(1, 0, 0, 1))
#            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])          
            Color(rgba=background_color)
            self.rect2 = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
#        self.rect.pos = self.pos
#        self.rect.size = self.size
        self.rect2.pos = self.pos
        self.rect2.size = self.size

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
        blazonImg = Image(source='riba_kit.png', allow_stretch = True, size_hint=(1, .5))
        colsOneLayout.add_widget(blazonImg)
        colsOneLayout.add_widget(Widget())                           
        colsTwoLayout = BoxLayout(orientation='vertical', size_hint=(.5, 1))
        label = Label(
            text='[color=C8E3FE][b]Совещание совета безопасности[/b][/color]',  
            markup = True, 
            font_size = 28)
        colsTwoLayout.add_widget(label)
        colsTwoLayout.add_widget(Widget())
        waitBtn = RoundedFlatButton(
            text='[color=D7F5FF][b]ПРИСТУПИТЬ К ГОЛОСОВАНИЮ[/b][/color]', 
            on_press=self.imReady, 
            markup = True, 
            font_size = 24,
            background_color=[.47, .69, 1, 1],
            background_normal = '')  
        colsTwoLayout.add_widget(waitBtn)
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

    def imReady(self, *args):
        requests.get(self.settings.IP_Adress+'/authorization/'+self.settings.clientCoutnry)


class Answer(Screen):
    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        answerLayout = BoxLayout(orientation='vertical')
        self.questionLbl = Label(text='TestTEXT')
        btnLayout = BoxLayout(spacing = 20)
        btnYes = Button(text='YES', on_press = self.answerYes)
        btnNo = Button(text='NO', on_press = self.answerNo)
        btnLayout.add_widget(btnYes)
        btnLayout.add_widget(btnNo)
        answerLayout.add_widget(self.questionLbl)
        answerLayout.add_widget(btnLayout)
        self.add_widget(answerLayout)

    def updateLbl(self, *args):
        self.questionLbl.text = self.settings.question

    def answerYes(self, *args):
            requests.get(self.settings.IP_Adress+'/answer/'+self.settings.round+'/'+self.settings.clientCoutnry+'/yes')
            self.manager.current = 'Result'

    def answerNo(self, *args):
            requests.get(self.settings.IP_Adress+'/answer/'+self.settings.round+'/'+self.settings.clientCoutnry+'/no')
            self.manager.current = 'Result'


class Result(Screen):
    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        result = BoxLayout()
        self.ansYes = Label(text='0')
        self.ansNo = Label(text='0')
        result.add_widget(self.ansYes)
        result.add_widget(self.ansNo)
        self.add_widget(result)

    def updateLbl(self, *args):
        self.ansYes.text = str(self.settings.votingResult[self.settings.round+'_yes'])
        self.ansNo.text = str(self.settings.votingResult[self.settings.round+'_no'])
    

class Final(Screen):
    def __init__(self, **kwargs):
        super(Final, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        finalScreen = BoxLayout()
        finalLbl = Label(text='FINAL')
        finalScreen.add_widget(finalLbl)
        self.add_widget(finalScreen)   


if __name__ == "__main__":
    voteMaser().run()