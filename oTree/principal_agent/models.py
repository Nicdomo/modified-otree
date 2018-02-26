from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools
from itertools import chain
from collections import Counter



doc = """
The principal offers a contract to the agent, who can decide if to reject or
accept. The agent then chooses an effort level. The implementation is based on
<a href="http://www.nottingham.ac.uk/cedex/documents/papers/2006-04.pdf" target="_blank">
    Gaechter and Koenigstein (2006)
</a>.
"""


class Constants(BaseConstants):
    randomizedTreatment =["NIN-T","IN-T","IN-T",  "NIN-T","IN-T", "NIN-T",
                "NIN-T","IN-T", "NIN-T","IN-T", "NIN-T","NIN-T","IN-T", "IN-T", "NIN-T","IN-T"
                ]

    name_in_url = 'principal_agent'
    players_per_group = 2
    num_rounds = 16

    instructions_template = 'principal_agent/Instructions.html'

    base_pay = 20
    min_fixed_payment = 0
    max_fixed_payment = 100

    EFFORT_TO_COST = {
        0: 0,
        0.1: 1,
        0.2: 2,
        0.3: 3,
        0.4: 4,
        0.5: 6,
        0.6: 8,
        0.7: 10,
        0.8: 12,
        0.9: 15,
        1: 18}


    def return_wage(number):
        wage = -1
        if(number>=0 and number<=6):
            wage = 30
        elif (number>=7 and number<=8):
            wage = 10
        elif (number >= 9 and number <=15):
            wage = 65
        elif (number >= 16 and number <=19):
            wage = 45
        elif (number >= 20 and number <=21):
            wage = 50
        elif (number >= 22 and number <=26):
            wage = 40
        elif (number>=27 and number<=39):
            wage = 15
        elif (number >=40 and number <=46):
            wage = 60
        elif (number >= 47 and number <=55):
            wage = 20
        elif (number >= 56 and number <=62):
            wage = 55
        elif (number >= 63 and number <=73):
            wage = 35
        elif (number >= 74 and number <=75):
            wage = 75
        elif (number >= 76 and number <=99):
            wage = 25

        return wage




    def groupByINT(listOfPlayers):
        INT = [p for p in listOfPlayers if p.treatment == "IN-T"]
        return INT

    def groupByNINT(listOfPlayers):
        NINT = [p for p in listOfPlayers if p.treatment == "NIN-T"]
        return NINT











def cost_from_effort(effort):
    return c(Constants.EFFORT_TO_COST[effort])

'''
def return_from_effort(effort):
    return c(Constants.EFFORT_TO_RETURN[effort])
'''

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        treatment = itertools.cycle(['NIN-T', 'IN-T'])
        count = Constants.num_rounds
        current_round = self.round_number
        while count > 0:
            for g in self.get_groups():
                g.treatment = Constants.randomizedTreatment[current_round-1]
                if g.treatment =='NIN-T':
                    g.isnint = True;
                else:
                    g.isnint = False;

                for p in g.get_players():
                    #p.set_partner()
                    p.participant.vars['roundpayoff'] = 0
            count = count - 1

    pass

    '''
    def randomizeTreatment(self, player):
        intctr = player.participant.vars['intctr']
        nintctr = player.participant.vars['nintctr']
        randnum = random.randint(0,1) #1 is int, 0 is nintctr
        #if random number is 1 and the player hasnt played under intention treatment 8 times,
        # assign the player to int treatment, update counter
        if(randnum==1 and intctr < 8):
            player.treatment ="IN-T"
            player.participant.vars['intctr'] = player.participant.vars['intctr']+1
        #if the random number is 1 and the player already played under intention treatment 8 times,
        #assign the player to no intention treatment, update counter
        elif(randnum==1  and intctr >= 8):
            player.participant.vars['nintctr'] = player.participant.vars['nintctr'] + 1
            player.treatment ="NIN-T"
        # if random number is 0 and the player hasnt played under no intention treatment 8 times,
        # assign the player to nint treatment, update counter
        elif (randnum==0 and nintctr <8):
            player.treatment ="N-INT"
            player.participant.vars['nintctr'] = player.participant.vars['nintctr']+1
        # if the random number is 0 and the player already played under no intention treatment 8 times,
        # assign the player to intention treatment, update counter
        elif(randnum==0  and nintctr>=8):
            player.treatment = "I-NT"
            player.participant.vars['intctr'] = player.participant.vars['intctr'] + 1 
    '''

    '''
                second version (infinite loop)
                    def creating_session(self):
                    all_players = self.get_players()
                    if self.round_number==1:
                        self.group_randomly()
                        treatment = itertools.cycle(['N-INT', 'IN-T'])
                        count = Constants.num_rounds
            
                        for g in self.get_groups():
                            g.treatment = next(treatment)
                            if g.treatment =='N-INT':
                                g.isnint = True;
                            else:
                                g.isnint = False;
            
                            for p in g.get_players():
                                p.set_partner()
                                p.participant.vars['roundpayoff'] = 0
                                p.participant.vars['intctr'] = 0
                                p.participant.vars['nintctr'] = 0
                                p.treatment = g.treatment
                    else:
                        newAllPlayers = []
                        treatment = itertools.cycle(['NIN-T', 'IN-T'])
                        for p in all_players:
                            nextTreatment = next(treatment)
                            intctr = p.participant.vars['intctr']
                            nintctr = p.participant.vars['nintctr']
                            if (nextTreatment =='NIN-T' and nintctr <8):
                                p.treatment = nextTreatment
                                p.participant.vars['nintctr'] = p.participant.vars['nintctr'] + 1
                            elif (nextTreatment == 'NIN-T' and nintctr >= 8):
                                p.treatment = 'IN-T'
                                p.participant.vars['intctr'] = p.participant.vars['intctr'] + 1
                            elif(nextTreatment =='IN-T' and intctr <8):
                                p.treatment = nextTreatment
                                p.participant.vars['intctr'] = p.participant.vars['intctr'] + 1
                            elif(nextTreatment =='IN-T' and intctr >=8):
                                p.treatment = 'NIN-T'
                                p.participant.vars['nintctr'] = p.participant.vars['nintctr'] + 1
            
                            newAllPlayers.append(p)
                    INT = Constants.groupByINT(newAllPlayers)
                        NINT = Constants.groupByNINT(newAllPlayers)
            
                        group_matrix = []
            
                        while INT:
                            player1 = self.getRandomPlayer(INT)
                            player2 = self.getRandomPlayer(INT)
                            if(player1!=player2 and self.CheckIfNotPartners(player1,player2)and not(self.isInsideMatrix(group_matrix, player1))and not(self.isInsideMatrix(group_matrix, player2))):
                                newGroup = [player1,player2]
                                group_matrix.append(newGroup)
                                INT.remove(player1)
                                INT.remove(player2)
            
                        while NINT:
                            player3 = self.getRandomPlayer(NINT)
                            player4 = self.getRandomPlayer(NINT)
                            if (player3 != player4 and self.CheckIfNotPartners(player3, player4) and not(self.isInsideMatrix(group_matrix, player3)) and not(self.isInsideMatrix(group_matrix, player4))):
                                newGroup = [player3, player4]
                                group_matrix.append(newGroup)
                                NINT.remove(player3)
                                NINT.remove(player4)
            
                        self.set_group_matrix(group_matrix)
                '''


    '''
                randnum = random.randint(0, 1)  # 1 is int, 0 is nintctr
                # if random number is 1 and the player hasnt played under intention treatment 8 times,
                # assign the player to int treatment, update counter
                if (randnum == 1 and intctr < 8):
                    p.treatment = "IN-T"
                    p.participant.vars['intctr'] = p.participant.vars['intctr'] + 1
                # if the random number is 1 and the player already played under intention treatment 8 times,
                # assign the player to no intention treatment, update counter
                elif (randnum == 1 and intctr >= 8 and nintctr < 8):
                    p.participant.vars['nintctr'] = p.participant.vars['nintctr'] + 1
                    p.treatment = "NIN-T"
                # if random number is 0 and the player hasnt played under no intention treatment 8 times,
                # assign the player to nint treatment, update counter
                elif (randnum == 0 and nintctr < 8):
                    p.treatment = "N-INT"
                    p.participant.vars['nintctr'] = p.participant.vars['nintctr'] + 1
                # if the random number is 0 and the player already played under no intention treatment 8 times,
                # assign the player to intention treatment, update counter
                elif (randnum == 0 and nintctr >= 8 and intctr < 8):
                    p.treatment = "I-NT"
                    p.participant.vars['intctr'] = p.participant.vars['intctr'] + 1
                '''




    def isInsideMatrix(self, matrix, player1):
        return player1 in chain(*matrix)


    def getRandomPlayer(self, listOfPlayers):
        randnum1 = random.randint(0,len(listOfPlayers)-1)
        return listOfPlayers[randnum1]



    def CheckIfNotPartners(self, player1, player2):
        partners1 = [p.partner for p in player1.in_all_rounds()]
        partners2 = [p.partner for p in player2.in_all_rounds()]
        #if player 2 is not inside the list of partners of player 1
        if(partners1.count(player2))==0 and (partners2.count(player1))==0:
            return True
        else:
            return False




class Group(BaseGroup):
    isnint = models.BooleanField(doc = """true if the group is under nint treatment""")
    treatment = models.StringField(doc="""treatment for the group IN-T/N-INT""")

    agent_fixed_pay = models.CurrencyField(
        doc="""Amount offered as fixed pay to agent""",
        min=Constants.min_fixed_payment, max=Constants.max_fixed_payment,
    )



    agent_work_effort = models.FloatField(
        choices=[0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        doc="""Agent's work effort, [0, 1]""",
        widget=widgets.Select,
    )

    agent_work_cost = models.FloatField(
        doc="""Agent's cost of work effort"""
    )

    '''
    sets the payoff for each round
    '''
    def set_payoffs(self):
        principal = self.get_player_by_role('firm')
        agent = self.get_player_by_role('worker')

        self.agent_work_cost = cost_from_effort(self.agent_work_effort)
        #if round number is 1, set max and min payoff to initial payoff

        if self.treatment == "NIN-T":
            # money to be received by the firm for the round
            agent.payoff = float(self.agent_fixed_pay - self.agent_work_cost - 20)
            # money to be received by the firm for the round
            # [(100) – wage] * effort
            principal.payoff = float((100 - self.agent_fixed_pay) * self.agent_work_effort)

        else:
            agent.payoff = float(self.agent_fixed_pay - self.agent_work_cost - 20)
            principal.payoff = float((100 - self.agent_fixed_pay) * self.agent_work_effort)



    def return_randomWage(self):
        self.agent_fixed_pay = Constants.return_wage(self.return_randomnumber())
        return self.agent_fixed_pay

    def return_randomnumber(self):
        for x in range(1):
            return random.randint(0, 99)

    def return_treatment(self):
        return self.treatment


class Player(BasePlayer):
    count = models.IntegerField(
        doc="counter for each treatment"
    )
    treatment = models.StringField(
        doc = "treatment, it can be NIN-T or IN-T"
    )
    '''
        partner = models.StringField(
        doc ="partner for the current round"
    )
    '''


    def get_partner(self):
        return self.get_others_in_group()[0].participant.id_in_session

    def set_partner(self):
        self.partner = self.get_partner()
    def count_treat(self):
        int_count = 0
        nint_count = 0
        for p in self.in_all_rounds():
            if(p.treatment=="NIN-T"):
                nint_count += 1
            elif(p.treatment =="IN-T"):
                int_count += 1
            p.count = dict()
            p.count['NIN-T'] = nint_count
            p.count['IN-T'] = int_count

    def canBeAssignedToINT(self):
        self.count_treat()
        return self.count['IN-T']<8

    def canBeAssignedToNINT(self):
        self.count_treat()
        return self.count['NIN-T']<8

    def role(self):
        if self.id_in_group == 1:
            return 'firm'
        if self.id_in_group == 2:
            return 'worker'
