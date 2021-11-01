class wallet(object):
    """The easiest, Dumbest way to store who has what"""
    ID = 0 #ID - user's discord ID
    coins = 0 #coins - integer, number of coins a user has

    def __init__(self, ID, coins):
        # loads a wallet that already exists
        self.ID = ID
        self.coins = coins

    def __init__(self, ID):
        # creates a wallet for a new person
        
        self.ID = ID
        self.coins = 0
    def deets(self):
        return("Wallet ID - {}\nTuzzCoin balance - {}".format(self.ID, self.coins))


