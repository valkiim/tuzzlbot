from wallet import wallet
import pickle

class walletPile(object):
    #handles wallet processing bullshit

    def saveWallet(self, wallet):
        # export a wallet to file, carry on with life
        with open(str(wallet.ID)+'.txt', 'wb') as walletExportFile:
            pickle.dump(wallet, walletExportFile)

    def loadWallet(self, inputID):
        # check for file with inputID.txt
        try:
            with open(str(inputID)+'.txt', 'rb') as walletImportFile:
                loadedWallet = pickle.load(walletImportFile)
        except FileNotFoundError:
            #create a new wallet w/ 0 tuzzcoin
            newWallet = wallet(inputID)
            self.saveWallet(newWallet)
            return newWallet
        else:
            return loadedWallet
