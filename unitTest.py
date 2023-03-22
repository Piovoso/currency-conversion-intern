import main
from collections import Counter
bank, user = [], []

for curFrom in main.currencies:
    for curTo in main.currencies:
        if curFrom == curTo: pass
        else:
            for amount in range(1,3):
                customer, provider = main.currencyConversion.main(float(amount), curFrom, curTo, True)
                user.append(customer)
                bank.append(provider)
                print(f'{curFrom}-{curTo}:{amount}')

print(f'{Counter(customer)}\n{Counter(bank)}')