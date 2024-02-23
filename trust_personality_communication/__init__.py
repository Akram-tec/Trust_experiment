from otree.api import *

doc = """
This game tries to understand the best trust repair strategies, and
how do they link to different personality types. This file contains
setup for communication treatment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust_personality_communication'
    PLAYERS_PER_GROUP = 2  # Adjust based on your game design
    NUM_ROUNDS = 5
    COMPANY_ENDOWMENT = cu(100)
    MULTIPLIER = 3



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)



class Group(BaseGroup):
    additional_sent_amount = models.CurrencyField(
        min=0,
        max=C.COMPANY_ENDOWMENT - 10,  # Player A can send up to COMPANY_ENDOWMENT minus the fixed 10 units
        doc="Additional amount sent by Company",
        label="Please enter an additional amount from 0 to 90:",
    )
    sent_back_amount = models.CurrencyField(
    min=0,  # Player B can choose not to send back any additional tokens
    doc="Amount sent back by Community",
    )



class Player(BasePlayer):
    pass



def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    total_sent = 10 + (group.additional_sent_amount or 0)
    total_received = total_sent * C.MULTIPLIER
    automatic_return = total_received * 0.2  # 20% of the tripled amount

    # Update payoffs considering the automatic 20% return
    p1.payoff = C.COMPANY_ENDOWMENT - total_sent + automatic_return + group.sent_back_amount
    p2.payoff = total_received - automatic_return - group.sent_back_amount


#pages
class Chat_copy_copy(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Display this page only in the first round
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        # Assign nicknames based on the player's id_in_group
        nickname = "Player A" if player.id_in_group == 1 else "Player B"
        return {
            'nickname': nickname,
        }


class Send_chat(Page):
    form_model = 'group'
    form_fields = ['additional_sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        # Ensure this page is displayed only for Player A and only during the practice rounds
        return player.id_in_group == 1 and player.round_number <= C.NUM_ROUNDS



class SendBack_chat(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        # Ensure this page is displayed only for Player A and only during the baseline rounds
        return player.id_in_group == 2 and player.round_number <= C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        additional_sent_amount = group.additional_sent_amount or 0  # Handle None case

        # Calculate the total tripled amount, including the fixed 10 tokens and the additional sent amount
        total_sent = 10 + additional_sent_amount
        tripled_amount = total_sent * C.MULTIPLIER
        automatic_deduction = tripled_amount * 0.2
        min_return = 0
        max_return = tripled_amount - automatic_deduction

        return dict(tripled_amount=tripled_amount, min_return=min_return, max_return=max_return)



class SendWaitPage_chat(WaitPage):
    pass



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs



class ResultsA_chat(Page):

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        # logic to calculate tripled amount
        total_sent = 10 + (group.additional_sent_amount or 0)  # Handle case where additional_sent_amount might be None
        tripled_amount = total_sent * C.MULTIPLIER  # Calculate the tripled amount

        # Added logic to fetch previous round's payoff
        previous_round_payoff = None
        if player.round_number > 1:
            previous_player = player.in_round(player.round_number - 1)
            previous_round_payoff = previous_player.payoff

        # Combine all necessary variables to return
        return {
            'tripled_amount': tripled_amount,
            'previous_round_payoff': previous_round_payoff,
        }


#page_sequence
page_sequence = [SendWaitPage_chat, Chat_copy_copy, Send_chat, SendWaitPage_chat, SendBack_chat, ResultsWaitPage, ResultsA_chat]
