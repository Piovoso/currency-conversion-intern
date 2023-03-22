import requests, pandas, math
import IPython.display

currencies = ('AUD','CAD','PEN','EUR','GBP', #List of curriencies available.
              'JPY','MYR','MXN','INR','HKD')

intermediary = {}

def CurrencyConversion(headers, URL, currencyFrom, currencyTo, currencyAmount, fixedFrom): 
    querystring = {"from":str(currencyFrom),"to":str(currencyTo)} # query
    request = float(requests.request("GET", URL, headers=headers, params=querystring).text) #request 
    
    if fixedFrom[0] == currencyFrom: # if the currency passed from currencyFrom is equal to the selected start currency it will execute this
        # customer selected start currency to intermediary
        intermediary["customer"][currencyFrom][currencyTo] = request * float(currencyAmount)
        # bank selected start currency to intermediary
        intermediary["bank"][currencyFrom][currencyTo] = request * float(currencyAmount)

    else: # if the currency passed from currencyFrom is equal to the selected end currency it will execute this
        # customer intermediary to selected end currency
        intermediary["customer"][currencyTo][currencyFrom] = request * float(intermediary["customer"][fixedFrom[0]][currencyFrom])
        # bank profit intermediary to selected end currency
        intermediary["bank"][currencyTo][currencyFrom] = float(intermediary["customer"][fixedFrom[1]][currencyFrom]) - (math.trunc(float(intermediary["customer"][fixedFrom[1]][currencyFrom]) * 100) / 100)


if __name__ == "__main__":
    
    url = "https://currency-exchange.p.rapidapi.com/exchange" # API URL
    headers = {
    	"X-RapidAPI-Key": "e38d990d1cmsh2e9f27958ea4b2dp197761jsnb1b11869fbf2", # API KEY
    	"X-RapidAPI-Host": "currency-exchange.p.rapidapi.com" # API HOST
    }
    
    userAmount = input(f'Amount: ')
    userFrom = input(f'From Currency {currencies}: ')
    userTo = input(f'To Currency {currencies}: ')
    
    intermediary.update({"customer":{userFrom:{}, userTo:{}},"bank":{userFrom:{}, userTo:{}}}) # creating a dictionary to hold data

    for i in currencies: # shuffles through the possible currencies 
        if i == userFrom or i == userTo: pass # skips selected currencies
        else: CurrencyConversion(headers, url, userFrom, i, userAmount, (userFrom, userTo)) # continues to CurrencyConversion function 

    for i in currencies:
        if i == userFrom or i == userTo: pass # skips selected currencies
        else: CurrencyConversion(headers, url, i, userTo, userAmount, (userFrom, userTo))

    table = {'Intermediary Currency': intermediary["customer"][userTo].keys(), #Laying out the Intermediary Currency Column
             f'{userFrom} to inter.': [i for i in intermediary["customer"][userFrom].values()], # Laying out Selected start currency To Intermediary column
             f'inter. to {userTo}': [x for x in intermediary["customer"][userTo].values()], # Laying out Intermediary to Selected end currency column
             f'Profit': [x for x in intermediary["bank"][userTo].values()] # Laying out Bank profit column
            }
    pdFrame = pandas.DataFrame(table) # pandas Stuff
    IPython.display.display_png(pdFrame) # Using Ipython.display

    print(f'Best for Customer: {list(intermediary["customer"][userTo].keys())[list(intermediary["customer"][userTo].values()).index(max(intermediary["customer"][userTo].values()))]}')
    print(f'Best for Service Provider: {list(intermediary["bank"][userTo].keys())[list(intermediary["bank"][userTo].values()).index(max(intermediary["bank"][userTo].values()))]}')