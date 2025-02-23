import pickle

portfolio = {'AAPL': 20, 'TSLA': 5, 'GS': 10}

with open("portfolio.pkl", "wb") as f:
    pickle.dump(portfolio, f)

print("✅ portfolio.pkl has been created successfully!")
