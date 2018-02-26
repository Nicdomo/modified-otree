from ._builtin import Page, WaitPage
from .models import Constants, cost_from_effort
import itertools
from collections import Counter



class Introduction(Page):
    pass

class ShuffleWaitPage(WaitPage):
    NINT = []
    INT = []
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        '''


        #self.subsession.group_randomly()
        all_players = self.subsession.get_players()
        all_groups = self.subsession.get_groups()
        current_round = self.round_number
        for g in all_groups:
            g.treatment = Constants.treatment[current_round]
            for p in g:
                p.count_treat
                if(p.canBeAssignedToINT()):
                    p.treatment = Constants.treatment[current_round]
                    p.set_partner()
                else:
                    p.treatment = Constants.treatment[current_round]
                    p.set_partner()
        '''
        '''
        NINT = []
        INT = []
        all_players = self.subsession.get_players()
        if self.round_number ==1:
            self.group_randomly()
            treatment = itertools.cycle(['N-INT', 'IN-T'])
            for g in self.get_groups():
                g.treatment = next(treatment)
                if g.treatment == 'N-INT':
                    g.isnint = True;
                else:
                    g.isnint = False;

                for p in g.get_players():
                    p.set_partner()
                    p.participant.vars['roundpayoff'] = 0
                    p.treatment = g.treatment
        else:
            Constants.randomizeTreatment(all_players)
            INT = Constants.groupByINT()
            NINT = Constants.groupByNINT()









        group_matrix = []
        ppg = Constants.players_per_group
        #group muna

        #set treatment

        if self.round_number ==1:
            self.subsession.group_randomly()
            all_groups = self.subsession.get_groups()

        if self.round_number ==1:
            self.subsession.group_randomly()
            for i in all_players:
                for j in all_players:
                    if(j.participant.id_in_session)


        else:
            currentRound = self.round_number
            for g in currentRound:
                #get all players for the round
                #
                for i in self.group.get_players():
                    for p in i.in_previous_rounds():
                        formerPartners = []
                        formerPartners.append(p.)
        '''





class Offer(Page):

    def is_displayed(self):
        return self.player.role() == 'firm'

    def vars_for_template(self):
        return {'wage':self.group.return_randomWage(), 'isnint':self.group.isnint}

    timeout_seconds = 120
    form_model = 'group'
    form_fields = ['agent_fixed_pay']
    #form_fields = ['agent_fixed_pay', 'agent_return_share']

    def timeout(self):
        if self.group.isnint==0:
            timeout_submission = {
                'agent_fixed_pay': 0,
            }
        else:
            timeout_submission = {
                'agent_fixed_pay': 0,
            }


class OfferWaitPage(WaitPage):
    def vars_for_template(self):
        if(self.group.treatment=="N-INT"):
            if self.player.role() == 'worker':
                body_text = "You are Participant B. Waiting for the proposed contract."
            else:
                body_text = "Waiting for Participant B."
        else:
            if self.player.role() == 'worker':
                body_text = "You are Participant B. Waiting for Participant A to propose a contract."
            else:
                body_text = "Waiting for Participant B."
        return {'body_text': body_text}


class Accept(Page):
    timeout_seconds = 120
    def is_displayed(self):
        return self.player.role() == 'worker'

    form_model = 'group'
    form_fields = ['agent_work_effort']

    timeout_submission = {
        'agent_work_effort': 0,
    }


class ResultsWaitPage(WaitPage):
    def setPartner(self):
        self.player.set_partner()

    def after_all_players_arrive(self):
        self.group.set_payoffs()



class Results(Page):
    def is_displayed(self):
        return  self.round_number<Constants.num_rounds

    #this is the end of a round, set partners to each other
    def vars_for_template(self):
        return {
            'received': self.player.payoff,
            'effort_cost': cost_from_effort(self.group.agent_work_effort),
        }



class FinalResults(Page):
    #this is the end of the final round
    def is_displayed(self):
        return self.round_number==Constants.num_rounds

    def vars_for_template(self):
        payoffs = []
        sortedAscending=[]
        sortedDescending = []
        partners = []

        payoffs = [float(p.payoff) for p in self.player.in_all_rounds()]
        partners = [p.partner for p in self.player.in_all_rounds()]
        sortedAscending = list(payoffs)
        sortedDescending = list(payoffs)

        sortedDescending.sort(reverse=True)
        sortedAscending.sort()
        max_payoff = float(sortedAscending.pop())
        min_payoff = float(sortedDescending.pop())
        pay_off_divided = (max_payoff + min_payoff)/2.0
        finalPayoff = float(pay_off_divided) * 1.5 + Constants.base_pay

        return {'max_payoff': max_payoff, 'min_payoff':min_payoff,'payoffs':payoffs, 'final_payoff':finalPayoff,'partners':partners}



page_sequence = [
                 Introduction,
                 Offer,
                 OfferWaitPage,
                 Accept,
                 ResultsWaitPage,
                 Results,
                 FinalResults,
                ]
