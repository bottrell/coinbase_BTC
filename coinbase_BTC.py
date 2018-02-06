import secrets
import datetime
from coinbase.wallet.client import Client

#to get a list of the wallets and transactions in our account
#accounts = client.get_accounts()

#payment_method = client.get_payment_methods()[0]
#really only necessary for using multiple accounts

######################HELPER FUNCTIONS##########################
def get_price(client):
	currency_code = 'USD'
	# Make the request
	price = client.get_spot_price(currency = currency_code)
	return price.amount

def limit_buy(client, account, current_price_BTC):
	#get the primary account
	btc_wallet = client.get_primary_account()
	#let's not add a payment method yet so we dont end up
	#accidentally buying coins lol
	buy_price_threshold = 0
	#if the current price is meets our threshold, buy 1 satoshi
	if float(current_price_BTC) <= buy_price_threshold:
		buy = account.buy(amount = '.000001',
						  currency = 'BTC',
						  payment_method = payment_method.id)

def current_profit(client, account, current_price_BTC):
	transactions = account.get_transactions()
	price_bought = 0.0
	price_sold = 0.0
	amount_profit = 0.0
	for transaction in transactions["data"]:
		if(transaction["type"] == "buy"):
			price_bought += float(transaction["native_amount"]["amount"])
			print(price_bought)
		#print(transaction, end = "\n\n\n\n\n\n\n\n\n")

##################################################################

def main():
	#since I only really use one account, I'll just use the following
	#for account in accounts.data:
	#balance = account.balance
	#print("%s: %s %s" % (account.name, balance.amount, balance.currency))
	#print(account.get_transactions())
	print("Starting coinbase...")
	
	client = Client(
	secrets.API_KEY,
	secrets.API_SECRET,
	api_version='2018-02-04' )

	#prints the current price of 1 bitcoin
	current_price = get_price(client)
	print('Current bitcoin price is %s USD' % current_price)
	#get the amount of BTC in the user's wallet
	primary_account = client.get_primary_account()
	primary_account.refresh()
	balance_BTC = primary_account.balance
	balance_USD = float(current_price) * float(balance_BTC.amount)
	print("{}: {} {}".format(primary_account.name, balance_BTC.amount, balance_BTC.currency))
	print("Your wallet value is: {}".format(balance_USD))

	current_profit(client, primary_account, current_price)


if __name__ == main():
	main()