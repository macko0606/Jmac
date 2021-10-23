knownStocks = ["NOK","GME","BB","AAPL","TSLA","NKLA","NIO","RIDE","RUN","CRSR","AMD"]
knownNonStocks = []


def initiate():
    import praw
    reddit = praw.Reddit(client_id='DA4lc6KxY-dIXA', \
                     client_secret='5TZEhmf6AdsXTHNgnjhJJGsEFmQ', \
                     user_agent='Mimifur', \
                     username='HereComesTheMoneyyy', \
                     password='EggSalami7')
    return reddit


def get_hot_subreddit(login,subreddit,size):
    import praw
    storage =[]
    hot_posts = login.subreddit('wallstreetbets').hot(limit=size)
    for post in hot_posts:
        try:
            storage.append(post.title+post.selftext)
        except:
            pass
    return storage
def get_top_subreddit(login,subreddit,size):
    import praw
    storage =[]
    hot_posts = login.subreddit('wallstreetbets').top(limit=size)
    for post in hot_posts:
        try:
            storage.append(post.title+post.selftext)
        except:
            pass
    return storage
def get_new_subreddit(login,subreddit,size):
    import praw
    storage =[]
    hot_posts = login.subreddit('wallstreetbets').new(limit=size)
    for post in hot_posts:
        try:
            storage.append(post.title+post.selftext)
        except:
            pass
    print(len(storage))
    return storage
def get_rising_subreddit(login,subreddit,size):
    import praw
    storage =[]
    hot_posts = login.subreddit('wallstreetbets').rising(limit=size)
    for post in hot_posts:
        try:
            storage.append(post.title+post.selftext)
        except:
            pass
    return storage

def scan_sub(subList): 
    import praw 
    tickerDict={}
    try:
        for post in subList:
            post+=("x")
            for i in range(0,len(post)):
                if post[i] =="$":
                    tempString='$'
                    iterator=1
                    continuer=True
                    while continuer == True:
                        if post[i+iterator].isupper():
                            tempString+=post[i+iterator]
                            iterator+=1
                        else:
                            continuer=False
                            if tempString in tickerDict:
                                 tickerDict[tempString] = int(tickerDict[tempString]+1)
                            elif tempString!="$":
                                tickerDict[tempString] = 1
    except:
        "Something happened!"
    return tickerDict

def sort(dictionary):
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

def revert(myList):
    newDict={}
    for obj in myList:
        ticker = ''
        quantity = 0
        for i in str(obj):
            if i.isalpha()==True:
                ticker+=i
            elif i.isnumeric():
                quantity+=int(i)
        newDict[ticker] = quantity
    return newDict

def clean_list(theList):
    tempList=str(theList).split(')')
    returnList=[]
    for string in tempList:
        newString=''
        for i in string:
            if i.isnumeric() or i.isalpha():
                newString += str(i)
        returnList.append(newString)
        with open("data.txt","w") as file:
            for item in returnList:
                file.write(item+"\n")
    return returnList




    



def template(dictionary,name,number,sub,numberOfStocks):
    body="How's it going {}? \nHere are the top {} stocks by mention today, taken from {} posts on r/{}!\n {}\n\nThank you for using Mimifur, as we continue to develop our algorithms our results will become more precise.".format(name,str(numberOfStocks),str(number),sub,template2(numberOfStocks,dictionary))
    #body="How's it going {}? \n {}".format(name,dictionary[0])
    return body

def template2(numberOfStocks,dictionary):
    string = ''
    for index in range(0,numberOfStocks):
        string+='\n'
        string+=str(dictionary[index])
    return string

def send_mail(body,dictionary,reciever):
    import smtplib

    with smtplib.SMTP('smtp.gmail.com',587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()

        connection.login("mimifurapp@gmail.com", "5uXLEf@<ca^X#$%E`6eGeGy's")

        subject = 'Mimifur Hot Stocks!'

        msg=f'Subject: {subject}\n\n{body}'

        connection.sendmail('mimifurapp@gmail.com', reciever, msg)

def scan2(theList):
    import yfinance as yf
    tickerDict={}
    tempList=str(theList).split()
    temporaryList=[]
    returnList=[]
    for string in tempList:

        newString=''
        for i in string:
            if i.isalpha():
                newString += str(i)
        temporaryList.append(newString)
    for i in temporaryList:
        tryBool=False   
        if i.isupper():
            if check_ticker(i) == True:
                if i in tickerDict:
                    tickerDict[i] = int(tickerDict[i]+1)
                else:
                    tickerDict[i] = 1
    return tickerDict   

def check_ticker(ticker):
        global knownStocks
        global knownNonStocks
        import yfinance as yf
        
        datafile = open('stopwords.txt')
        found = 1
        tempStock=yf.Ticker(ticker)
        if ticker in knownStocks:
            print(ticker," found again")
            return True
        if ticker in knownNonStocks:
            print(ticker," not found again")
            return False
        for line in datafile:
                if ticker.lower() in line:
                        found =0
                        
        if found ==1 and len(ticker)<6:
            try:
                
                x=tempStock.info["regularMarketOpen"]
                print(ticker," found")
                found+=1
                knownStocks.append(ticker)
            except:
                print(ticker," not found")
                found = 0
                knownNonStocks.append(ticker)
            
        else:
            found=0
        if found==2:
            return True
        else:
            return False

def show_data(dictionary,name,number,sub,numberOfStocks):
    return dictionary
