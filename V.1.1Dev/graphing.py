def graphData(path):
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas
    colnames = ['Ticker','Value']
    data = pandas.read_csv(path, names=colnames)
    tickers = data["Ticker"]
    values = data["Value"]
    print(values)
    for i in range(len(tickers)-1):
        tickers[i] = str(tickers[i])
        values[i] = str(values[i])
    plt.bar(tickers[0:15], values[0:15])
    label = str
    plt.title(label,text = "Reddit Tickers")
    plt.ylabel(label,text = "Mentions")
    plt.show()
