import requests                              # Required import
import pandas, math, IPython.display         # additional imports

currencies = ('AUD','CAD','PEN','EUR','GBP', #List of curriencies available.
	    	  'JPY','MYR','MXN','INR','HKD')

intermediary = {}

class currencyConversion:
	def main(userAmount:float, userFrom:str, userTo:str, unitTest:bool=True):

		url = "https://currency-exchange.p.rapidapi.com/exchange"                   # API URL
		headers = {
			"X-RapidAPI-Key": "e38d990d1cmsh2e9f27958ea4b2dp197761jsnb1b11869fbf2", # API KEY
			"X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"                   # API HOST
		}
		try:
			if not unitTest:
				userAmount = float(input(f'Amount: '))
				userFrom = userTo = None # creating variables for the user selected curriencies.

				while userFrom not in currencies or userTo not in currencies: # Making sure the user choses one of the available currencies
					userFrom = input(f'From Currency {currencies}: ').upper()
					userTo = input(f'To Currency {currencies}: ').upper()

			intermediary.update({ "customer":{ userFrom:{}, userTo:{} }, "bank":{ userFrom:{}, userTo:{} } })  # updating a dictionary to hold data

			# i hate these for-loops, but unfortunately i don't posess the skills yet to do it another way.
			for i in currencies:
				if i == userFrom or i == userTo: pass   # skips selected currencies
				else: currencyConversion.query(headers, url, userFrom, i, userAmount, (userFrom, userTo)) 

			for i in currencies:
				if i == userFrom or i == userTo: pass   # skips selected currencies
				else: currencyConversion.query(headers, url, i, userTo, userAmount, (userFrom, userTo))

			# Visual style stuff.
			table = {'Intermediary Currency': intermediary["customer"][userTo].keys(),                     # Laying out the Intermediary column
						f'{userFrom} to inter.': [i for i in intermediary["customer"][userFrom].values()], # Laying out Selected START currency -> Intermediary column
						f'inter. to {userTo}': [x for x in intermediary["customer"][userTo].values()],     # Laying out Intermediary -> Selected END currency column
						f'Profit': [x for x in intermediary["bank"][userTo].values()]                      # Laying out Bank profit column
					}
			pdFrame = pandas.DataFrame(table)       # Pandas dataframe generation
			IPython.display.display_png(pdFrame)    # Using Ipython.display because it worked the best

			# honestly I hate and love both of these lines, so complex that it's kinda amazing but really horrible.
			customerBest = list(intermediary["customer"][userTo].keys())[list(intermediary["customer"][userTo].values()).index(max(intermediary["customer"][userTo].values()))]
			providerBest = list(intermediary["bank"][userTo].keys())[list(intermediary["bank"][userTo].values()).index(max(intermediary["bank"][userTo].values()))]
			print(f'Best for Customer: {customerBest}')
			print(f'Best for Service Provider: {providerBest}')

			if unitTest:
				return customerBest, providerBest

			#	 _	 Quack
			# __(.)<
			# \___)
		except ValueError:
			print('Amount must be a number')

	def query(headers, URL, currencyFrom, currencyTo, currencyAmount, fixedFromTo):
		"""Sends a request to Currency excnage API for the specified currencies"""

		querystring = {"from":str(currencyFrom),"to":str(currencyTo)}                            # query, unfortunately does not have functioning support for amount/quantity.
		request = float(requests.request("GET", URL, headers=headers, params=querystring).text)  # request and conversion to text.
	
		if fixedFromTo[0] == currencyFrom: # if the currency passed from currencyFrom is equal to the selected START currency it will execute this
			intermediary["customer"][currencyFrom][currencyTo] = request * float(currencyAmount) # customer selected START currency -> intermediary
			intermediary["bank"][currencyFrom][currencyTo] = request * float(currencyAmount)     # bank     selected START currency -> intermediary

		else:   # if the currency passed from currencyFrom is equal to the selected END currency it will execute this
				# customer    intermediary -> selected END currency
			intermediary["customer"][currencyTo][currencyFrom] = request * float(intermediary["customer"][fixedFromTo[0]][currencyFrom])
				# bank profit intermediary -> selected END currency
			intermediary["bank"][currencyTo][currencyFrom] = float(intermediary["customer"][fixedFromTo[1]][currencyFrom]) - (math.trunc(float(intermediary["customer"][fixedFromTo[1]][currencyFrom]) * 100) / 100)

if __name__ == "__main__":
    currencyConversion.main()