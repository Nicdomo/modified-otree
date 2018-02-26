from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = 'models.Player'
    form_fields = ['player.name', 'player.age']
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class Results(Page):
    pass


page_sequence = [
    MyPage,
    Results
]
