from otree.api import *

doc = """
This game tries to understand the best trust repair strategies, and
how do they link to different personality types.
"""


class C(BaseConstants):
    NAME_IN_URL = 'personality_compensation'
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

    # The fixed and additional amount sent by Player A, which is subject to tripling
    total_sent = 10 + (group.additional_sent_amount or 0)
    # Only the total sent (excluding compensation) is tripled
    total_received = total_sent * C.MULTIPLIER

    # Compensation is added to Player B's total received but not tripled
    compensation = 60 if p1.round_number == 1 else 0

    # Automatic return calculation based on the tripled amount (not including compensation)
    automatic_return = total_received * 0.2

    # Player A's payoff calculation - does not subtract compensation
    p1.payoff = C.COMPANY_ENDOWMENT - total_sent + automatic_return + (group.sent_back_amount or 0)

    # Player B's payoff calculation - adds compensation directly to their total
    # Adjust for Player B to include compensation only in the first round, without tripling the compensation
    p2.payoff = (total_received - automatic_return - (group.sent_back_amount or 0)) + compensation


#page
class Compensation(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Show this page only in the first round
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        # Assuming compensation is a fixed value for demonstration
        compensation = 60
        # You might want to adjust this logic based on how you track/send this compensation in your app
        return dict(compensation=compensation)



class Send_compensation(Page):
    form_model = 'group'
    form_fields = ['additional_sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        # Ensure this page is displayed only for Player A and only during the practice rounds
        return player.id_in_group == 1 and player.round_number <= C.NUM_ROUNDS



class SendBack_compensation(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.round_number <= C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        additional_sent_amount = group.additional_sent_amount or 0
        # Compensation only in the first round and is not affected by the tripling multiplier
        compensation = 60 if player.round_number == 1 else 0

        # The total amount sent by Player A that is subject to tripling
        total_sent_subject_to_tripling = 10 + additional_sent_amount
        # Tripled amount is based only on the total amount subject to tripling
        tripled_amount_subject_to_tripling = total_sent_subject_to_tripling * C.MULTIPLIER

        # The total amount received by Player B includes the tripled amount plus any compensation directly
        total_received_by_B = tripled_amount_subject_to_tripling + compensation

        automatic_deduction = total_received_by_B * 0.2
        min_return = 0
        # Adjust max return to consider only the tripled amount minus automatic deductions
        max_return = total_received_by_B - automatic_deduction

        return {
            'tripled_amount': tripled_amount_subject_to_tripling,
            'final_amount': total_received_by_B,  # This now correctly includes compensation
            'min_return': min_return,
            'max_return': max_return,
            'compensation': compensation,
            }



class SendWaitPage_compensation(WaitPage):
    pass



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs



class ResultsA_compensation(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        total_sent = 10 + (group.additional_sent_amount or 0)  # Base amount sent
        compensation = 60 if player.round_number == 1 else 0  # Compensation only in the first round

        # Tripled amount calculation does not include compensation
        tripled_amount = total_sent * C.MULTIPLIER

        # Adjusting the display of the tripled amount for Player B to include compensation in the first round
        total_received_by_B = tripled_amount + compensation if player.id_in_group == 2 else tripled_amount

        # Added logic to fetch previous round's payoff
        previous_round_payoff = None
        if player.round_number > 1:
            previous_player = player.in_round(player.round_number - 1)
            previous_round_payoff = previous_player.payoff

        return {
            'tripled_amount': total_received_by_B,  # This now accounts for compensation for Player B
            'compensation': compensation,
            'previous_round_payoff': previous_round_payoff,
        }


page_sequence = [Compensation, Send_compensation, SendWaitPage_compensation, SendBack_compensation, ResultsWaitPage ,ResultsA_compensation,]
