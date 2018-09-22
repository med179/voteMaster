#!python
# -*- coding: utf-8 -*-

#voteMaser - client part

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore
from kivy.uix.textinput import TextInput
import requests
from time import sleep



class voteMaser(App):
    def build(self):
        myScreenmanager = ScreenManager()
        settings = MySettings()
        answer = Answer(name='Answer', settings=settings)
        waiting = Waiting(name='Waiting', settings=settings)
        admin = Admin(name='Admin', settings=settings)
        adminRoundScreen = AdminRoundScreen(name='AdminRoundScreen', settings=settings)
        result = Result(name='Result', settings=settings)
        final = Final(name='Final', settings=settings)
        request = Request(settings=settings, changeWating=waiting.changeScreen, changeResult=result.changeScreen, changeToFinalScreen = result.changeToFinalScreen)
        authorization = Authorization(name='Authorization', settings=settings, clientCallback=request.clientCallback)
        enterNewIP = EnterNewIP(name='EnterNewIP', settings=settings)
        testNewIP = TestNewIP(name='TestNewIP', settings=settings)
        myScreenmanager.add_widget(authorization)
        myScreenmanager.add_widget(answer)
        myScreenmanager.add_widget(waiting)
        myScreenmanager.add_widget(admin) 
        myScreenmanager.add_widget(adminRoundScreen)
        myScreenmanager.add_widget(result)
        myScreenmanager.add_widget(final)
        myScreenmanager.add_widget(enterNewIP)
        myScreenmanager.add_widget(testNewIP)

        try:
            testIP = requests.get(settings.IP_Adress + '/test')
        except:
            testIP = 'False'
        if testIP == 'False':
            myScreenmanager.current = 'EnterNewIP'
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
        print('The widget', instance, 'have:', value)
        self.newIP = value

    def sendNewIP(self, *args):
        self.settings.IP_Adress = self.newIP
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
        self.clientCallback = kwargs['clientCallback']
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
        self.manager.current = 'Waiting'
        self.settings.clientCoutnry = name
        self.clientCallback()

    def adminPress(self, *args):
        self.settings.clientCoutnry = 'admin'
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
        startBtn = Button(text='Start voting (get status)',  size_hint=[.3, .3], on_press=self.changeStatusVote, background_color=[1, 0, 0, 1])
        adminLayout.add_widget(readyBtns)
        adminLayout.add_widget(startBtn)
        self.add_widget(adminLayout)
        self.bind(on_pre_enter=self.callback)

    def changeStatusVote(self, *args):
        requests.get(self.settings.IP_Adress+'/changeStatusVote')
        self.manager.current = 'AdminRoundScreen'

    def callback(self, *args):
        Clock.schedule_interval(self.statusPlayrs, 1)

    def statusPlayrs(self, *args):
        isPlayersReady = requests.get(self.settings.IP_Adress+'/authorization/admin')
        playersStatus = isPlayersReady.json()
        if playersStatus['riba_kit'] == 'im ready':
            self.riba_kitRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['tridevCarstvo'] == 'im ready':
            self.tridevCarstvoRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['lukomore'] == 'im ready':
            self.lukomoreRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['morskayaDergava'] == 'im ready':
            self.morskayaDergavaRdyLbl.background_color = [0, 1, 0, 1]
        if playersStatus['shamahan'] == 'im ready':
            self.shamahanRdyLbl.background_color = [0, 1, 0, 1]        


class AdminRoundScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminRoundScreen, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        mainScreen = BoxLayout()#(anchor_x='center', anchor_y='center')
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
        self.changeWating = kwargs['changeWating']
        self.changeResult = kwargs['changeResult']
        self.changeToFinalScreen = kwargs['changeToFinalScreen']
        
    def clientCallback(self, *args):
        Clock.schedule_interval(self.callbackAllSettings, 1)
        Clock.schedule_interval(self.callbackAnswers, 1)

    def callbackAllSettings(self, *args): 
        response = requests.get(self.settings.IP_Adress+'/allSettings/' + self.settings.round + '/' + self.settings.clientCoutnry)
        print str(self.settings.IP_Adress+'/allSettings/' + self.settings.round + '/' + self.settings.clientCoutnry)
        allSettings = response.json()
        print allSettings
        if allSettings['isAllRight'] == 'False':
            self.settings.question = allSettings['question']
            if self.settings.round == 'zero':
                self.settings.round = 'one'
                self.changeWating()
            elif self.settings.round == 'five':
                self.settings.round = 'final'
                self.changeToFinalScreen()
            else: 
                self.settings.round = allSettings['round']
                self.changeResult()

    def callbackAnswers(self, *args): 
        response = requests.get(self.settings.IP_Adress+'/result/'+self.settings.round)
        answers = response.json()
        print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print answers
        self.settings.answers = answers


class MySettings(object):
    def __init__(self, *args):
        self.clientCoutnry = 'test'
        self.rounds = ['zero', 'one', 'two', 'three', 'four', 'five', 'final']
        self.round = 'zero'
        self.IP_Adress = 'hthost:8080'
#        self.IP_Adress = 'http://localhost:8080'
        self.question = ''
        self.answers = {}
  

class Waiting(Screen):
    def __init__(self, **kwargs):
        super(Waiting, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        waitLayout = BoxLayout()
        waitBtn = Button(text='Приступрить к голосованию', on_press=self.imReady)
        waitLayout.add_widget(waitBtn)
        self.add_widget(waitLayout)

    def imReady(self, *args):
        requests.get(self.settings.IP_Adress+'/authorization/'+self.settings.clientCoutnry)
        
    def changeScreen(self):    
        self.manager.current = 'Answer'


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
        self.bind(on_pre_enter=self.updateLbl)

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
        self.bind(on_pre_enter=self.callback)

    def callback(self, *args):
        Clock.schedule_interval(self.updateLbl, 1)

    def updateLbl(self, *args):
        self.ansYes.text = str(self.settings.answers[self.settings.round+'_yes'])
        self.ansNo.text = str(self.settings.answers[self.settings.round+'_no'])

    def changeScreen(self, *args):
        self.manager.current = 'Answer'
    
    def changeToFinalScreen(self, *args):
        self.manager.current = 'Final'


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