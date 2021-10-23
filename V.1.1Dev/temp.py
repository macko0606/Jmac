# img_viewer.py
import PySimpleGUI as sg
import os.path

knownStocks = ["NOK","GME","BB","AAPL","TSLA","NKLA","NIO","RIDE","RUN","CRSR","AMD","ACB","CGC"]
knownNonStocks = []


def initiate():
    import praw
    reddit = praw.Reddit(client_id='DA4lc6KxY-dIXA', \
                     client_secret='5TZEhmf6AdsXTHNgnjhJJGsEFmQ', \
                     user_agent='Mimifur', \
                     username='HereComesTheMoneyyy', \
                     password='EggSalami7')
    return reddit


def get_hot_subreddit(login,sub,size):
    import praw
    storage =[]
    hot_posts = login.subreddit(sub).hot(limit=size)
    for post in hot_posts:
        try:
            storage.append(post.title+post.selftext)
        except:
            pass
    return storage
def get_top_subreddit(login,sub,size):
    import praw
    storage =[]
    hot_posts = login.subreddit(sub).top(limit=size)
    for post in hot_posts:
        try:
            storage.append(post.title+post.selftext)
        except:
            pass
    return storage
def get_new_subreddit(login,subreddit,size):
    import praw
    storage =[]
    hot_posts = login.subreddit(sub).new(limit=size)
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
    hot_posts = login.subreddit(sub).rising(limit=size)
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

def sign_in(client_id,client_secret,user_agent,username,password):
    import praw
    temp=''
    try:
        reddit = praw.Reddit(client_id = client_id, \
                         client_secret= client_secret, \
                         user_agent= user_agent, \
                         username= username, \
                         password=password)
        for i in reddit.subreddit('hello').hot(limit=1):
            temp=i
    except:
        reddit = "Invalid credentials."
    return reddit



def runAlg(sub,posts):
    global knowNonStocks
    print("building...")
    number = int(posts)
    sentiment={}
    numberOfStocks=0
    print("Logging in...")
    login = initiate()
    print("Done!")
    print("Fetching posts...")
    myList = get_hot_subreddit(login, sub, number)
    print("Done!")
    print("Scanning for tickers...")
    print(myList)
    myDict = scan2(myList)
    print("Done!")
    print("Sorting by magnitude...")
    myList = sort(myDict)
    print("Done!")
    print("Formatting data...")

    myList= clean_list(myList)
    print("Done!")
    
    print("Writing to files... ")
    writeToTxtFile("stopwords.txt", knownNonStocks)
    print("Done!")
    return show_data(myList,"MacLaren", number,sub,numberOfStocks)


def loginPage(): #This is the function responsible for the login page 
    creds=[] #temp array of credentials
    with open("credentials.txt","r") as file:
        file.seek(0) #go to start of txt file
        for line in file: 
            creds.append(line) #add credentials to array
            print(line) 
        file.close()
    print(creds)
    errorMessage = ''
    client=creds[0]
    secret=creds[1]
    agent=creds[2]
    username=creds[3]
    password=creds[4]
    redditAccount=''
    page = [
        [sg.Text("Sign-In to Reddit Developer Account")],
        [sg.HSeparator()],
        [sg.Text("client id:",size=(20,1)),
        sg.Input(client,size=(25, 1), enable_events=True, key="-CLIENT-")],
        [sg.Text("client secret:",size=(20,1)),
        sg.Input(secret,size=(25, 1), enable_events=True, key="-SECRET-")],
        [sg.Text("user agent:",size=(20,1)),
        sg.Input(agent,size=(25, 1), enable_events=True, key="-AGENT-")],
        [sg.Text("username:",size=(20,1)),
        sg.Input(username,size=(25, 1), enable_events=True, key="-USERNAME-")],
        [sg.Text("password:",size=(20,1)),
        sg.Input(password,size=(25, 1), enable_events=True, key="-PASS-")],
        [sg.Text(errorMessage,size=(30,1),text_color='red',key="-ERROR-",background_color='white')],
        [sg.Button("SAVE",size=(10,1),border_width = buttonBW, enable_events = True,key="-SAVE-"),sg.Button("HELP",size=(10,1),border_width = buttonBW,enable_events=True,key="-HELP-"),sg.Button("CLEAR",size=(10,1),border_width = buttonBW,enable_events=True,key="-CLEAR-")]
        
        
        
    ]
    window = sg.Window("Sign-In",page)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "-SAVE-":
            if values["-CLIENT-"] != '' or values["-SECRET-"] != '' or values["-AGENT-"] != '' or values["-USERNAME-"] != '' or values["-PASS-"] != '':
                errorMessage = "Signing in..."
                window["-ERROR-"].update(errorMessage)
                client=values["-CLIENT-"]
                secret=values["-SECRET-"]
                agent=values["-AGENT-"]
                username=values["-USERNAME-"]
                password=values["-PASS-"]
                redditAccount = sign_in(client,secret,agent,username,password)
                if redditAccount != "Invalid credentials.":
                    errorMessage = "Success!"
                    window["-ERROR-"].update(errorMessage)
                    f = open("credentials.txt")
                    f.write(client+"\n")
                    f.write(secret+"\n")
                    f.write(agent+"\n")
                    f.write(username+"\n")
                    f.write(password)
                    f.close()
                    return redditAccount
                    break
                else:
                    errorMessage = redditAccount
                    window["-ERROR-"].update(errorMessage)
                    redditAccount=''
                    

            else:
                errorMessage = "Please enter the missing data."
                window["-ERROR-"].update(errorMessage)

def writeToTxtFile(targetFile,dataList): #target file takes format, file.txt as a string | datalist is a list of lowercase strings
    #write a list to a txt file, for each word that doesnt exist in it
    txtFile = open(targetFile, "a")

    for word in dataList:
        txtFile.write(word+"\n")
    txtFile.close()
    
            


    

display = "\n\n\nData will be shown on the right once the algorithm runs successfully\nNote: performance varies based on processing power and connection\nOn a typical machine, expect 7-10 posts per minute"
# First the window layout in 2 columns

sg.theme("Python")
buttonBW = 6
file_list_column = [
    [
        sg.Text("                      INTELLIGENT ALGORITHMS\n\n\n\n\n",font="callibri")
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Text("Number of posts loaded:",size=(20,1)),
        sg.Input(size=(25, 1), enable_events=True, key="-POSTS-"),
    ],
    [
        sg.Text("Please Enter a Subreddit:",size=(20,1)),
        sg.Input(size=(25, 1), enable_events=True, key="-SUB-"),
    ],
    [sg.Button("Retrieve Data", size = (17,.7),key="-GO-",enable_events=True,border_width=buttonBW),sg.Button("Sign-In to Reddit", size = (17,.7), key="-SIGN-",border_width=buttonBW)
     ],
    [
        sg.Text(display)
    ],
    [sg.Text("\n\n\n\n\n\n\n\n\n\nIntelligent Algorithms from Mimifur™ 2021\nDeveloped by MacLaren Scott")]
]

fieldText = "      \n           \n             \n            "

image_viewer_column = [
    [sg.Text(fieldText, text_color="Black",
             background_color="White",size=(80,30),key="-DATA-")],
    [sg.Text("LOAD DATA:",size=(10,1)),sg.FileBrowse("UPLOAD",size=(20,1)),
     sg.Text("               SAVE DATA:",size=(20,1)),sg.Button("DOWNLOAD",size=(20,1))],
    [sg.Text("Please only upload '.txt' and '.csv' files.")]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


window = sg.Window("Intelligent Algorithms from Mimifur V.1.1(Dev.Py Edition)",layout)
windowData=''
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        print(knownNonStocks)
        break
    # Folder name was filled in, make a list of files in the folder
    elif event == "-SIGN-":
        print("SI")
        loginPage()
    elif event == "-GO-":
        window["-DATA-"].update("Loading...")
        print(values["-SUB-"])
        windowData = runAlg(values["-SUB-"],values["-POSTS-"])
        window["-DATA-"].update(windowData)

window.close()
