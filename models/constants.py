from util.env import Env

class Constants(object):
    TIP_MINIMUM = 1.0 if Env.banano() else 1
    TIP_UNIT = 'BAN' if Env.banano() else 'WATERMELONANO'
    WITHDRAW_COOLDOWN = 1 # Seconds
    # TODO - set to 1 for testing
    RAIN_MIN_ACTIVE_COUNT = 1 # Amount of people who have to be active for rain to work
    RAIN_MSG_REQUIREMENT = 1 # Amount of decent messages required to receive rain
    REPRESENTATIVE='ban_1tipbotgges3ss8pso6xf76gsyqnb69uwcxcyhouym67z7ofefy1jz7kepoy' if Env.banano() else 'watermelon1aunch1qxkfrjkmhwhewqx9mucmy3f5n5urnf7xh4dhrs4hecf4fx3mit1sk'
