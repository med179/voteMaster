#!python
# -*- coding: utf-8 -*-

#voteMaser - client part

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager


class voteMaser(App):
    def build(self):
        myScreenmanager = ScreenManager()
        settings = MySettings()
        authorization = Authorization(name='Authorization', settings=settings)
        answer = Answer(name='Answer', settings=settings)
        waiting = Waiting(name='Waiting')
        myScreenmanager.add_widget(authorization)
        myScreenmanager.add_widget(answer)
        myScreenmanager.add_widget(waiting)
      
        myScreenmanager.current = 'Authorization'
        return myScreenmanager

class Authorization(Screen):
    def __init__(self, **kwargs):
        super(Authorization, self).__init__(**kwargs)

        authorizationLayout = BoxLayout(spacing = 10, size_hint = [1, .5])
        riba_kitBtn = Button(text = 'riba_kitBtn', on_press = self.riba_kitPress)
        tridevCarstvoBtn = Button(text = 'tridevCarstvoBtn')
        lukomoreBtn = Button(text = 'lukomoreBtn')
        morskayaDergavaBtn = Button(text = 'morskayaDergavaBtn')
        shahmanBtn = Button(text = 'shahmanBtn')
        authorizationLayout.add_widget(riba_kitBtn)
        authorizationLayout.add_widget(tridevCarstvoBtn)
        authorizationLayout.add_widget(lukomoreBtn)
        authorizationLayout.add_widget(morskayaDergavaBtn)
        authorizationLayout.add_widget(shahmanBtn)
        self.add_widget(authorizationLayout)

    def login(self, name):
        self.manager.current = 'Waiting'
        self.settings.clientCoutnry = name

    def riba_kitPress(self, *args):
        self.login('riba_kit')

#тут нужно разобраться, что такое object
class MySettings(object):
    def __init__(self):
        clientCoutnry = 'test'


class Waiting(Screen):
    def __init__(self, **kwargs):
        super(Waiting, self).__init__(**kwargs)



class Answer(Screen):
    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)




if __name__ == "__main__":
    voteMaser().run()