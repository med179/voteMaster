#!python
# -*- coding: utf-8 -*-

#voteMaser - client part

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
import requests


class voteMaser(App):
    def build(self):
        myScreenmanager = ScreenManager()
        settings = MySettings()
        authorization = Authorization(name='Authorization', settings=settings)
        answer = Answer(name='Answer', settings=settings)
        waiting = Waiting(name='Waiting', settings=settings)
        admin = Admin(name='Admin', settings=settings)
        myScreenmanager.add_widget(authorization)
        myScreenmanager.add_widget(answer)
        myScreenmanager.add_widget(waiting)
        myScreenmanager.add_widget(admin)
      
        myScreenmanager.current = 'Authorization'
        return myScreenmanager

class Authorization(Screen):
    def __init__(self, **kwargs):
        super(Authorization, self).__init__(**kwargs)
#добавить администратора 
        self.settings = kwargs['settings']
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
        readyLabels = BoxLayout(orientation='horizontal', spacing=10)

        riba_kitRdyLbl = Label(text='riba_kit is not ready')
        tridevCarstvoRdyLbl = Label(text='tridevCarstvo is not ready')
        lukomoreRdyLbl = Label(text='lukomore is not ready')
        morskayaDergavaRdyLbl = Label(text='morskayaDergava is not ready')
        shamahanRdyLbl = Label(text='shamahan is not ready')
        readyLabels.add_widget(riba_kitRdyLbl)
        readyLabels.add_widget(tridevCarstvoRdyLbl)
        readyLabels.add_widget(lukomoreRdyLbl)
        readyLabels.add_widget(morskayaDergavaRdyLbl)
        readyLabels.add_widget(shamahanRdyLbl)
        startBtn = Button(text='Start voting', on_press=self.startVoting, size_hint=[.3, .3], background_color=[1, 0, 0, 1])
        adminLayout.add_widget(readyLabels)
        adminLayout.add_widget(startBtn)
        self.add_widget(adminLayout)

    def startVoting(self, *args):
        #доделать, сейчас показывает статус участников
        isPlayersReady = requests.get(self.settings.IP_Adress+'/authorization/admin')
        print(isPlayersReady.text)


#тут нужно разобраться, что такое object
class MySettings(object):
    def __init__(self):
        self.clientCoutnry = 'test'
        self.rounds = ['one', 'two', 'three', 'four', 'five']
        self.lap = 'one'
        self.IP_Adress = 'http://localhost:8080' 


class Waiting(Screen):
    def __init__(self, **kwargs):
        super(Waiting, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        waitLayout = BoxLayout()
        waitBtn = Button(text='Приступрить к голосованию', on_press=self.changeScreen)
        waitLayout.add_widget(waitBtn)
        self.add_widget(waitLayout)
        
    def changeScreen(self, *args):
        self.manager.current = 'Answer'
        requests.get(self.settings.IP_Adress+'/authorization/'+self.settings.clientCoutnry)
        print(self.settings.lap)
        print(self.settings.clientCoutnry)

class Answer(Screen):
    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)
        self.settings = kwargs['settings']

        answerLayout = BoxLayout(orientation='vertical')
        self.questionLbl = Label(text='TestTEXT')

        btnLayout = BoxLayout(spacing = 20)
        btnYes = Button(text='YES', on_press = self.answerYes)
        btnNo = Button(text='NO', on_press = self.answerNo)
        self.votingResultLbl = Label(text='Проголосовало ЗА: 0'+'    ***     Проголосовало ПРОТИВ: 0')

        btnLayout.add_widget(btnYes)
        btnLayout.add_widget(btnNo)
        answerLayout.add_widget(self.votingResultLbl)
        answerLayout.add_widget(self.questionLbl)
        answerLayout.add_widget(btnLayout)
        self.add_widget(answerLayout)
        self.bind(on_pre_enter=self.updateLbl)


    def updateLbl(self, *args):
        questionRequests = requests.get(self.settings.IP_Adress+'/interrogatory/'+self.settings.lap+'/'+self.settings.clientCoutnry)
        self.questionLbl.text = questionRequests.text


    def answerYes(self, *args):
            sendAnswer = requests.get(self.settings.IP_Adress+'/answer/'+self.settings.lap+'/'+self.settings.clientCoutnry+'/yes')
            self.votingResultLbl.text = sendAnswer.text

    def answerNo(self, *args):
            sendAnswer = requests.get(self.settings.IP_Adress+'/answer/'+self.settings.lap+'/'+self.settings.clientCoutnry+'/no')
            self.votingResultLbl.text = sendAnswer.text


if __name__ == "__main__":
    voteMaser().run()