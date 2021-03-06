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

# added a limit parameter, so we never have a static limit_buy setting,
# that way we can be sure to not get stuck in a buy loop if a limit
# gets set at a super low threshold.
def limit_buy(client, account, current_price_BTC, limit):
	#get the primary account
	btc_wallet = client.get_primary_account()
	#let's not add a payment method yet so we dont end up
	#accidentally buying coins lol
	buy_price_threshold = limit
	#if the current price is meets our threshold, buy 1 satoshi
	if float(current_price_BTC) <= buy_price_threshold:
		buy = account.buy(amount = '.000001',
						  currency = 'BTC',
						  payment_method = payment_method.id)

# Pass in peak so the function doesn't get stuck in a loop of selling
# all of my bitcoins on any sort of price peak
def sell_high(client, account, current_price_BTC, peak):
	pass


def current_profit(client, account, current_price_BTC, account_balance):
	transactions = account.get_transactions()
	price_bought = 0.0
	price_after_fees = 0.0
	for transaction in transactions["data"]:
		if(transaction["type"] == "buy"):
			if(transaction["details"]["payment_method_name"][0] == "M"):
				price_bought += float(transaction["native_amount"]["amount"])
				amount = float(transaction["native_amount"]["amount"]) - (.04 * float(transaction["native_amount"]["amount"]))
				price_after_fees += amount
				#print(transaction)
			else:
				price_bought += float(transaction["native_amount"]["amount"])
				amount = float(transaction["native_amount"]["amount"]) - (.01 * float(transaction["native_amount"]["amount"]))
				price_after_fees += amount
				#print(transaction)

	amount_payed_fees = round((price_bought - price_after_fees), 2)
	print("Amount payed in fees: " + str(amount_payed_fees))
	profit = round((account_balance - price_after_fees), 2)
	print("Total profit to this point: %s" % profit)
	return profit
		#print(transaction, end = "\n\n\n\n\n\n\n\n\n")

#-------------------------------------------------------------#
#
# DEFINITELY TEST THE HECK OUT OF THIS AS TO NOT LOSE MONEY
#
#-------------------------------------------------------------#
def trade(client, account, account_balance):
	pass
##################################################################

def main():
	#since I only really use one account, I'll just use the following
	#for account in accounts.data:
	#balance = account.balance
	#print("%s: %s %s" % (account.name, balance.amount, balance.currency))
	#print(account.get_transactions())
	print("\n\nSTARTING COINBASE...", end = "\n\n\n")
	
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
	balance_USD = round(balance_USD, 2)
	print("{}: {} {}".format(primary_account.name, balance_BTC.amount, balance_BTC.currency))
	print("Your wallet value is: {}".format(balance_USD))

	current_profit(client, primary_account, current_price, balance_USD)

	print("\n\n\nBUYING AND SELLING BTC BASED ON METRICS FROM PAST WEEK...\n\n\n")


if __name__ == main():
	main()