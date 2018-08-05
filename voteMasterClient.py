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
        authorization = Authorization(name='Authorization')
        myScreenmanager.add_widget(authorization)
        myScreenmanager.current = 'Authorization'
        return myScreenmanager

class Authorization(Screen):
    def __init__(self, **kwargs):
        super(Authorization, self).__init__(**kwargs)

        authorizationLayout = BoxLayout()
        riba_kitBtn = Button(text = 'riba_kitBtn')
        tridevCarstvoBtn = Button(text = 'tridevCarstvoBtn')
        lukomoreBtn = Button(text = 'lukomoreBtn')
        morskayaDergavaBtn = Button(text = 'morskayaDergavaBtn')
        shahmanBtn = Button(text = 'shahmanBtn')
        authorizationLayout.add_widget(riba_kitBtn)
        authorizationLayout.add_widget(tridevCarstvoBtn)
        authorizationLayout.add_widget(lukomoreBtn)
        authorizationLayout.add_widget(morskayaDergavaBtn)
        authorizationLayout.add_widget(shahmanBtn)


if __name__ == "__main__":
    voteMaser().run()