import secrets
from coinbase.wallet.client import Client

client = Client(
	secrets.API_KEY,
	secrets.API_SECRET,
	api_version='2018-02-04' )