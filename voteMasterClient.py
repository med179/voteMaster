#!python
# -*- coding: utf-8 -*-

#voteMaser - client part

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
import requests



class voteMaser(App):
    def build(self):
        myScreenmanager = ScreenManager()
        settings = MySettings()
        authorization = Authorization(name='Authorization', settings=settings)
        answer = Answer(name='Answer', settings=settings)
        waiting = Waiting(name='Waiting', settings=settings)
        admin = Admin(name='Admin', settings=settings)
        result = Result(name='Result', settings=settings)
        myScreenmanager.add_widget(authorization)
        myScreenmanager.add_widget(answer)
        myScreenmanager.add_widget(waiting)
        myScreenmanager.add_widget(admin) 
        myScreenmanager.add_widget(result)    
        myScreenmanager.current = 'Authorization'
        return myScreenmanager

class Authorization(Screen):
    def __init__(self, **kwargs):
        super(Authorization, self).__init__(**kwargs)
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
        a = requests.get(self.settings.IP_Adress+'/changeStatusVote')
        print(a.text) 

    def callback(self, *args):
        Clock.schedule_interval(self.startVoting, 1)

    def startVoting(self, *args):
        #доделать, сейчас показывает статус участников
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
        print(isPlayersReady.text)


#тут нужно разобраться, что такое object
class MySettings(object):
    def __init__(self):
        self.clientCoutnry = 'test'
        self.rounds = ['zero', 'one', 'two', 'three', 'four', 'five', 'final']
        self.round = 'zero'
        self.IP_Adress = 'http://localhost:8080' 


class Waiting(Screen):
    def __init__(self, **kwargs):
        super(Waiting, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        waitLayout = BoxLayout()
        waitBtn = Button(text='Приступрить к голосованию', on_press=self.callback)
        waitLayout.add_widget(waitBtn)
        self.add_widget(waitLayout)
        
    def callback(self, *args):
        Clock.schedule_interval(self.changeScreen, 1)

    def changeScreen(self, *args):
        requests.get(self.settings.IP_Adress+'/authorization/'+self.settings.clientCoutnry)
        statusJS = requests.get(self.settings.IP_Adress+'/status')
        status = statusJS.json()
        if status['round'] == 'one':
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
        self.votingResultLbl = Label(text='Проголосовало ЗА: 0'+'    ***     Проголосовало ПРОТИВ: 0')
        btnLayout.add_widget(btnYes)
        btnLayout.add_widget(btnNo)
        answerLayout.add_widget(self.votingResultLbl)
        answerLayout.add_widget(self.questionLbl)
        answerLayout.add_widget(btnLayout)
        self.add_widget(answerLayout)
        self.bind(on_pre_enter=self.updateLbl)

    def updateLbl(self, *args):
        questionRequests = requests.get(self.settings.IP_Adress+'/interrogatory/'+self.settings.round+'/'+self.settings.clientCoutnry)
        self.questionLbl.text = questionRequests.text

#тут можно оптимизировать

    def answerYes(self, *args):
            sendAnswer = requests.get(self.settings.IP_Adress+'/answer/'+self.settings.round+'/'+self.settings.clientCoutnry+'/yes')
            self.votingResultLbl.text = sendAnswer.text
            self.manager.current = 'Result'

    def answerNo(self, *args):
            sendAnswer = requests.get(self.settings.IP_Adress+'/answer/'+self.settings.round+'/'+self.settings.clientCoutnry+'/no')
            self.votingResultLbl.text = sendAnswer.text
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
        resultJS = requests.get(self.settings.IP_Adress+'/result/'+self.settings.round)
        result = resultJS.json()
        self.ansYes.text = str(result[self.settings.round+'_yes'])
        self.ansNo.text = str(result[self.settings.round+'_no'])


if __name__ == "__main__":
    voteMaser().run()