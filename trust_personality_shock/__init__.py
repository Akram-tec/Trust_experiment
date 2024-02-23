from otree.api import *

doc = """
This is the intervention by the experimenter. In one round,
80% of the amount sent by player A will be deducted. The Players
will pay 3 more rounds after that.
"""


class C(BaseConstants):

    NAME_IN_URL = 'shock_treatment'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
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

    def apply_deduction(self, amount):
        # Apply 80% deduction logic in the first round for all groups
        if self.round_number == 1:
            return amount * 0.2  # Apply the 80% deduction
        return amount  # No deduction from the second round onwards



class Player(BasePlayer):
    pass



def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    # Apply any adjustments for deductions.
    # This uses the corrected method name assuming you've implemented it as discussed.
    adjusted_sent_amount = group.apply_deduction(group.additional_sent_amount or 0)

    # Always start with a base of 10 for the initial sent amount.
    total_sent = 10 + adjusted_sent_amount

    # Calculate the total amount received by Player 2, based on the adjusted sent amount.
    total_received = total_sent * C.MULTIPLIER

    # The automatic return is a fixed percentage of the total received.
    automatic_return = total_received * 0.2

    # For Player 1's payoff, the deduction in the first round affects only the amount that gets multiplied.
    # They still "send" the full amount, but the game mechanics adjust how much is received and returned based on the deduction.
    # Therefore, the endowment deduction should reflect the initial intention to send for all rounds.
    total_sent_for_payoff = 10 + (group.additional_sent_amount or 0)

    # Update payoffs considering the correct deductions and additions
    p1.payoff = C.COMPANY_ENDOWMENT - total_sent_for_payoff + automatic_return + group.sent_back_amount
    p2.payoff = total_received - automatic_return - group.sent_back_amount


#pages
class TransitionPage(Page):
    pass



class Send_shock(Page):
    form_model = 'group'
    form_fields = ['additional_sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        # Ensure this page is displayed only for Player A and only during the practice rounds
        return player.id_in_group == 1 and player.round_number <= C.NUM_ROUNDS



# page to communicate the deduction to Player A
class DeductionInformation_shock(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1 and player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        deduction_percentage = 80  # Customize as needed
        return {'deduction_percentage': deduction_percentage}



class SendBack_shock(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        # Ensure this page is displayed only for Player B during the game rounds
        return player.id_in_group == 2 and player.round_number <= C.NUM_ROUNDS


    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        # Determine the actual sent amount considering the 80% deduction for the first round
        if group.round_number == 1:
            # Apply the 80% deduction only in the first round
            adjusted_sent_amount = group.apply_deduction(group.additional_sent_amount or 0)
        else:
            # No deduction from the second round onwards
            adjusted_sent_amount = group.additional_sent_amount or 0

        # The display_sent_amount should be what Player B sees, which includes the deduction for the first round
        #display_sent_amount = adjusted_sent_amount + 10

        # The total_before_tripling should also consider the adjusted amount for the first round
        total_before_tripling = 10 + adjusted_sent_amount
        tripled_amount = total_before_tripling * C.MULTIPLIER

        # Calculate the min and max returnable amounts after automatic deduction
        automatic_deduction = tripled_amount * 0.2
        min_return = 0
        max_return = tripled_amount - automatic_deduction

        return {
            'adjusted_sent_amount': adjusted_sent_amount,  # Corrected to show the deducted amount for the first round
            'tripled_amount': tripled_amount,  # Correctly reflects tripling after considering the deduction for the first round
            'min_return': min_return,
            'max_return': max_return,
        }



class SendWaitPage_shock(WaitPage):
    pass



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs



class ResultsA_shock(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        is_first_round = group.round_number == 1

        # Original amount sent by Player A, not including the fixed 10
        original_sent_amount = group.additional_sent_amount or 0

        # Apply the 80% deduction in the first round to the amount sent by Player A
        if is_first_round:
            adjusted_sent_amount = group.apply_deduction(original_sent_amount)
        else:
            adjusted_sent_amount = original_sent_amount

        # Total sent includes the fixed 10, but it's only added after deduction for the first round
        total_sent_after_deduction = adjusted_sent_amount + 10
        tripled_amount = total_sent_after_deduction * C.MULTIPLIER

        # Fetch previous round's payoff
        previous_round_payoff = None
        if player.round_number > 1:
            previous_player = player.in_round(player.round_number - 1)
            previous_round_payoff = previous_player.payoff

        return {
            'tripled_amount': tripled_amount,
            'effective_sent_amount': adjusted_sent_amount if is_first_round else original_sent_amount + 10,  # Use adjusted amount for the first round
            'original_sent_amount': original_sent_amount,  # Original amount intended to send, including the fixed 10
            'is_first_round': is_first_round,
            'previous_round_payoff': previous_round_payoff,
        }


# Include DeductionInformation in the page sequence before Send_baseline for Player A
page_sequence = [TransitionPage, Send_shock, DeductionInformation_shock,  SendWaitPage_shock, SendBack_shock, ResultsWaitPage, ResultsA_shock]
