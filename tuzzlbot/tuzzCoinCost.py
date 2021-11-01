import random
import math
import pickle

class tuzzCoinCost(object):
    """a class for Storing/fucking with tuzzcoin costs"""
    # tuzzcoin starts at 69 USD
    # tuzzcoin has a 5% price fluxuation every 5 minutes
    # tuzzcoin inflates in value by 1% every time someone mentions
        # puff, Inflation, Tuzzleton, Jazz, baloon, blimp, or helium
    # tuzzcoin is sold at 80% of its price
    # Buying tuzzcoin increases value/cost by 1% per coin purchased (mult)
    # selling tuzzcoin decreases value/cost by 1% per coin sold (multiplicative)
    # Keep track of total currency value, and number of coins
    CostFile = 'TuzzCoinCost.tc'
    BankFile = 'TuzzCoinBank.tc'
    TotlFile = 'TuzzCoinTotl.tc'
    coincosts = [69.00]
    coinInBank = [69]
    coinInTotl = [69]
    def __init__(self):
        random.seed()
        try:
            with open(CostFile, 'rb') as CoinCostHistory:
                self.coincosts = pickle.load(CoinCostHistory)
        except FileNotFoundError:
            #create a new coin history, right meow!
            self.coincosts = [69.00]
            #im not gunna bother saving THIS list because its a single unit, I'll sav eon update. 
        try:
            with open(BankFile, 'rb') as CoinBank:
                self.coinInBank = pickle.load(CoinBank)
        except FileNotFoundError:
            #create a new coin history, right meow!
            self.coinInBank = [69.00]
            #im not gunna bother saving THIS list because its a single unit, I'll save on update
        try:
            with open(TotlFile, 'rb') as CoinTotl:
                self.coinInTotl = pickle.load(CoinTotl)
        except FileNotFoundError:
            #create a new coin history, right meow!
            self.coinInTotl = [69.00]
            #im not gunna bother saving THIS list because its a single unit, I'll save on update
        else:
            return

    def costFluxuation(self):
        #causes a price fluxuation of 5% when triggered
        flux = float(random.randint(-5, 5))/100.0
        self.AdjustCost(1+flux)
        return
    def makeTuzzCoin(self, Number):
        # mints new tuzzcoins, allowing more to be bought!
        self.coinInTotl.append(self.coinInTotl[-1]+Number)
        self.coinInBank.append(self.coinInBank[-1]+(Number-5))
        self.saveNums()
        return
    def buyTuzzCoin(self, Number):
        # returns cost of buying X tuzzcoin, then increases the cost of tuzzcoin
        transCost = (Number * self.coincosts[-1])/self.coinInTotl[-1]
        self.coinInBank.append(self.coinInBank[-1]-Number)
        self.AdjustCost(math.pow(1.01, Number))
        self.saveCosts()
        self.saveNums()
        return transCost
    def sellTuzzCoin(self, Number):
        #returns money gained by selling x tuzzcoin, then decreases the cost of tuzzcoin
        #tuzzcoin is sold at 80% market price
        transCost = (Number * self.coincosts[-1]*0.8)/(self.coinInTotl[-1])
        self.coinInBank.append(self.coinInBank[-1]+Number)
        self.AdjustCost(math.pow(0.95, Number))
        self.saveCosts()
        self.saveNums()
        return transCost
    def AdjustCost(self, flux):
        flux = min(flux, 1.05)
        print("Flux = {}".format(flux))
        self.coincosts.append(self.coincosts[-1]*(flux))
        self.saveCosts()
        return
    def getCost(self):
        return self.coincosts[-1]
    def saveCosts(self):
        with open(CostFile, 'wb') as CoinCostHistory:
            pickle.dump(self.coincosts, CoinCostHistory)
        return
    def saveNums(self):
        with open(BankFile, 'wb') as CoinBank:
            pickle.dump(self.coinInBank, CoinBank)
        with open(TotlFile, 'wb') as CoinTotl:
            pickle.dump(self.coinInTotl, CoinTotl)

