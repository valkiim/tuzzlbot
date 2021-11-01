import asyncio
import discord
from walletPile import walletPile
from tuzzCoinCost import tuzzCoinCost
from discord.ext import tasks, commands
tokenFile = open('token.txt', 'r')
TOKEN = tokenFile.read()
intents =discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)
botRoomID = 899345648825032765


@tasks.loop(minutes=5)
async def flux():
    CC.costFluxuation()
    print("Five minute flux applied")
    ## economy sanity checks
    pricePer = CC.coincosts[-1]/CC.coinInTotl[-1]
    if (pricePer < 0.01):
        botRoom = bot.get_channel(botRoomID)
        print('currency value negative, Inflating')
        await botRoom.send('THE ECONOMY IS IN SHAMBLES!')
        await botRoom.send('Processing Government Bailout...')
        CC.coincosts.append(CC.coinInTotl[-1]*0.02)
        CC.saveCosts()
    elif (pricePer > 1000000000.00):
        botRoom = bot.get_channel(botRoomID)
        print('Currency worth too much, Flooring')
        await botRoom.send('TO THE MOON!')
        await botRoom.send('wait where did the money go...')
        CC.coincosts.append(50000.00)
        CC.saveCosts()


@bot.event
async def on_ready():
    print('TuzzCoin ATM bot, Online as {0.user}'.format(bot))
    print('Opening Value {}'.format(CC.coincosts[-1]))
    flux.start()
        
@bot.event
async def on_message(message):
    #print('On_Message processed -')
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        #print('Hello get, Responding\n')
        await message.channel.send('Hello! I\'m Tuzzbot!')
    if "puff" in message.content:
        CC.AdjustCost(1.01)
    if "inflation" in message.content:
        CC.AdjustCost(1.01)
    if "tuzzleton" in message.content:
        CC.AdjustCost(1.01)
    if "jazz" in message.content:
        CC.AdjustCost(1.01)
    if "balloon" in message.content:
        CC.AdjustCost(1.01)
    if "blimp" in message.content:
        CC.AdjustCost(1.01)
    if "helium" in message.content:
        CC.AdjustCost(1.01)
    #print('Processing possible commands-')
    await bot.process_commands(message) # so we actually run the commands at the end of the day. 
    #print(' Processing Finished\n')

#@bot.command()
#async def test(ctx, arg1, arg2):
#    await ctx.send('You passed {} and {}'.format(arg1, arg2))

@bot.command(name='hey')
async def heytest(ctx):
    await ctx.send('hey user {}'.format(ctx.message.author.id))
    # proof of concept user ID test case

@bot.command(name='value')
async def get_coinval(ctx):
    NumCoinsBank = CC.coinInBank[-1]
    NumCoinsTotl = CC.coinInTotl[-1]
    TotlCoinVal = round(CC.getCost(), 2)
    ValPerCoin = round(TotlCoinVal / float(NumCoinsTotl), 2)
    await ctx.send('There are {} coins in rotation, {} are in the bank.\nAt {} USD per coin, the Currency is worth {} USD in total.'.format(NumCoinsTotl, NumCoinsBank, ValPerCoin, TotlCoinVal))
    #returns the current tuzzcoin value


@bot.command(name='ping')
async def pongreply(ctx):
    await ctx.send('Pong!')

@bot.command(name='?')
async def TCcommandList(ctx):
    await ctx.send('You can check the **$value** or your **$wallet**, $**make** new coins, even **$buy** and **$sell**!')

@bot.command(name='wallet')
async def walletstatus(ctx):
    usrWallet = WP.loadWallet(ctx.message.author.id)
    await ctx.send('User Wallet - {}\n Total Coins - {}\n Current Value- {}'.format(usrWallet.ID, usrWallet.coins, round(usrWallet.coins*CC.getCost() / float(CC.coinInTotl[-1]),2)))

@bot.command(name='buy')
async def buyTuzzCoin(ctx, num):
    usrWallet = WP.loadWallet(ctx.message.author.id)
    try:
        number = int(num)
    except ValueError:
        await ctx.send('Transaction Failed, Try \"**$buy** [num]\"!')
    else:
        if (number < 0):
            await ctx.send('Do you mean to **$sell**?')
        elif (number == 0):
            await ctx.send('Do you think this is a fucking Joke?')
            await ctx.send('It is a joke. Buy Tuzzleton!')
        elif (number > 128):
            await ctx.send('Due to market regulations, there is a limit of 128 TuzzCoin per purchase.')
        elif (number > CC.coinInBank[-1]):
            await ctx.send('I\'m Sorry, we do not have enough TuzzCoins. Please $make some!')
        else:
            print('{} bought {} TuzzCoin.'.format(ctx.author, number))
            usrWallet.coins += number
            WP.saveWallet(usrWallet)
            cost = CC.buyTuzzCoin(number)
            await ctx.send('You purchased {} TuzzCoin for {} USD!'.format(number, round(cost, 2)))

@bot.command(name='make')
async def makeTuzzCoin(ctx, num):
    try:
        number = int(num)
    except ValueError:
        await ctx.send('Transaction Failed, Try \"**$make** [num]\"!')
    else:
        if(number <= 69 and number > 9):
            CC.makeTuzzCoin(number)
            if(number== 69):
                await ctx.send('Nice.')
            await ctx.send('With great effort, You helped produce {} new TuzzCoins!'.format(num))
            print('{} made {} TuzzCoin.'.format(ctx.author, number))
            usrWallet = WP.loadWallet(ctx.message.author.id)
            usrWallet.coins += 5
            WP.saveWallet(usrWallet)
        else:
            await ctx.send('Modern tuzzcoin production can only handle 10-69 coins per function')

@bot.command(name='sell all')
async def sellAllCoin(ctx):
    usrWallet = WP.loadWallet(ctx.message.author.id)
    await sellTuzzCoin(ctx, usrWallet.coins)

@bot.command(name='sell')
async def sellTuzzCoin(ctx, num):
    usrWallet = WP.loadWallet(ctx.message.author.id)
    try:
        number = int(num)
    except ValueError:
        if(num=='all'):
            await sellAllCoin(ctx)
        else:
            await ctx.send('Transaction Failed, Try \"**$sell** [num]\"!')
    else:
        if (number < 0):
            await ctx.send('Do you mean to **$buy**?')
        elif (number == 0):
            await ctx.send('Do you think this is a fucking Joke?')
            await ctx.send('It is a joke. Buy Tuzzleton!')
        else:
            if (usrWallet.coins >= number):
                usrWallet.coins -= number
                WP.saveWallet(usrWallet)
                cost = CC.sellTuzzCoin(number)
                print('{} sold {} TuzzCoin.'.format(ctx.author, number))
                await ctx.send('You sold {} TuzzCoin for {} USD!'.format(number, round(cost, 2)))
            else:
                await ctx.send('Insufficient TuzzCoin, Please buy more Tuzzleton!')

### Ironically, Setup crap goes here
WP = walletPile()    
CC = tuzzCoinCost()
bot.run(TOKEN)