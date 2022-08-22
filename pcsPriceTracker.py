from telegram import *
from telegram.ext import *
from web3 import Web3
import requests

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

tokenAddress = web3.toChecksumAddress('0xDF22a2fA5b9c98361fbEB73FEEd9d35627e0E8b5')
pairAddress = web3.toChecksumAddress('0x955b745363Dbca94F8F61C447da731e9Be4BAab8') #Write Checksummed Addresses
wbnbContract = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
wbnbABI = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
contract = web3.eth.contract(address=wbnbContract, abi=wbnbABI)

botToken = '5526163505:AAEfG2W58BpKWBRo1OPAXunH4vuCICkrb6s'
bot = Bot(botToken)
updater=Updater(botToken,use_context=True)
dispatcher=updater.dispatcher

def test_function(update:Update,context:CallbackContext):
    tokenPrice = requests.get(f'https://api.pancakeswap.info/api/v2/tokens/{tokenAddress}').json()
    BnbData = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT').json()
    BnbPrice = float(BnbData['price'])
    liquidity = contract.functions.balanceOf(pairAddress).call()
    
    bot.send_message(chat_id=update.effective_chat.id, text=f'''
Name : Colossal Finance
Symbol : CSL
CSL Price : ${round(float(tokenPrice['data']['price']), 7)}
BNB Price : ${BnbPrice}
LP Holdings : ${int(float(web3.fromWei(liquidity, 'ether'))*(BnbPrice*2))}
''')

start_value=CommandHandler('price', test_function)
dispatcher.add_handler(start_value)
print(bot.get_me())
updater.start_polling()