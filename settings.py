from os import environ


SESSION_CONFIGS = [

    # control Group
    {
        'name':'control_group',
        'display_name': 'Control Group',
        'num_demo_participants': 2,
        'app_sequence': [
            'trust_personality',
            'trust_personality_baseline',
            'trust_personality_shock',
            'trust_personality_control',
            'bigfive'
        ],
    },

    # Communication Group
    {
        'name':'communication_group',
        'display_name': 'Communication Group',
        'num_demo_participants': 2,
        'app_sequence': [
            'trust_personality',
            'trust_personality_baseline',
            'trust_personality_shock',
            'trust_personality_communication',
            'bigfive'
        ],
    },
        # Apology Group
        {
            'name':'apology_group',
            'display_name': 'Apology Group',
            'num_demo_participants': 2,
            'app_sequence': [
                'trust_personality',
                'trust_personality_baseline',
                'trust_personality_shock',
                'trust_personality_apology',
                'bigfive'
            ],
    },
    # Compensation Group
        {
            'name':'compensation_group',
            'display_name': 'Compensation Group',
            'num_demo_participants': 2,
            'app_sequence': [
                'trust_personality',
                'trust_personality_baseline',
                'trust_personality_shock',
                'trust_personality_compensation',
                'bigfive'
            ],
},

    # add trust personality game practice
    {
        'name':'trust_personality',
        'display_name': 'Personality Trust Game',
        'num_demo_participants': 2,
        'app_sequence': ['trust_personality'],
    },
    # add trust personality BASELINE_ROUNDS
    {
        'name':'trust_personality_baseline',
        'display_name': 'Personality Trust baseline',
        'num_demo_participants': 2,
        'app_sequence': ['trust_personality_baseline'],
    },
    # add trust personality shock
    {
        'name':'shock_treatment',
        'display_name': 'Personality Trust shock',
        'num_demo_participants': 2,
        'app_sequence': ['trust_personality_shock'],
    },
    # add apology treatment
    {
        'name':'apology_treatment',
        'display_name': 'Personality Trust Apology',
        'num_demo_participants': 2,
        'app_sequence': ['trust_personality_apology'],
    },
    # adding chat treatment
    {
        'name':'chat_treatment',
        'display_name': 'trust_personality_communication',
        'num_demo_participants': 2,
        'app_sequence': ['trust_personality_communication'],
    },
    # adding compensation treatment
    {
        'name':'compensation_treatment',
        'display_name': 'trust_personality_compensation',
        'num_demo_participants': 2,
        'app_sequence': ['trust_personality_compensation'],

    },
    # final survey
    {
        'name':'bigfive',
        'display_name': 'bigfive',
        'num_demo_participants': 2,
        'app_sequence': ['bigfive'],

    },

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '6990504244425'

INSTALLED_APPS = ['otree']
