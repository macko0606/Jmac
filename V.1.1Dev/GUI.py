
import PySimpleGUI as sg
import os.path
import time
login = None
knownStocks = []
knownNonStocks = []


currentData = []
def sub_exists(sub,reddit):
    from prawcore import NotFound
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

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
    #print(len(storage))
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

def clean_list(theList): #removes parentheses and other junk
    tempList=str(theList).split(')')
    returnList=[]
    for string in tempList:
        newString=''
        for i in string:
            if i.isnumeric() or i.isalpha():
                newString += str(i)
        returnList.append(newString)
        with open("txt/data.txt","w") as file:
            for item in returnList:
                file.write(item+"\n")
    return returnList
def split_list(myList): #converts to 2 lists
    list1 = []
    list2 = []
    for item in myList:
        for char in item:
            if char.isalpha():
                list1.append(char)
            else:
                list2.append(char)
    return [list1,list2]

    



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
        
        stopwords = open('txt/stopwords.txt')
        gowords = open('txt/gowords.txt')
        found = 1
        for line in gowords:
            if ticker.lower() in line:
                gowords.close()
                stopwords.close()
                return True
        tempStock=yf.Ticker(ticker)
        if ticker in knownStocks:
            gowords.close()
            stopwords.close()
            #print(ticker," found again")
            return True
        if ticker in knownNonStocks:
            #print(ticker," not found again")
            gowords.close()
            stopwords.close()
            return False
        for line in stopwords:
                if ticker.lower() in line:
                        found =0
                        
        if found ==1 and len(ticker)<6:
            try:
                
                x=tempStock.info["regularMarketOpen"]
                #print(ticker," found")
                found+=1
                knownStocks.append(ticker)
            except:
                #print(ticker," not found")
                found = 0
                knownNonStocks.append(ticker)
            
        else:
            found=0
        if found==2:
            gowords.close()
            stopwords.close()
            return True
        else:
            gowords.close()
            stopwords.close()
            return False

def show_data(dictionary,name,number,sub,numberOfStocks):
    return dictionary

def sign_in(client_id,client_secret,user_agent,username,password):
    global login
    import praw
    temp=''
    print(password)
    status = False
    try:
        print(username+"--")
        reddit = praw.Reddit(client_id = client_id.strip(), \
                            client_secret= client_secret.strip(), \
                            user_agent= user_agent.strip(), \
                            username= username.strip(), \
                            password=password.strip())
        for i in reddit.subreddit('hello').hot(limit=1):
            temp=i.title
        login = reddit
        status = True
    except Exception as e: 
        reddit = "Unable to log in to Reddit: " + str(e)
        

    return [status,reddit]




def runAlg(sub,posts):
    import WriteUp
    global knowNonStocks
    global currentData
    global login
    if login == None:
        return "Login Error"
    #print("building...")
    #number = int(posts)
    numberOfStocks=0
    #print("Logging in...")
    print(login)
    #print("Done!")
    #print("Fetching posts...")

    myList = get_hot_subreddit(login, sub, int(posts))
    #print("Done!")
    #print("Scanning for tickers...")
    #print(myList)
    myDict = scan2(myList)
    #print("Done!")
    #print("Sorting by magnitude...")
    myList = sort(myDict)
    #print("Done!")
    #print("Formatting data...")

    myList= clean_list(myList)
    #print("Done!")
    
    #print("Writing to files... ")
    writeToTxtFile("txt/stopwords.txt", knownNonStocks)
    writeToTxtFile("txt/gowords.txt", knownStocks)
    #print("Done!")
    #print("Writing up...")
    currentData = myList
    #print("Done!")
    return show_data(myList,"MacLaren", int(posts),sub,numberOfStocks)



def writeToTxtFile(targetFile,dataList): #target file takes format, file.txt as a string | datalist is a list of lowercase strings
    #write a list to a txt file, for each word that doesnt exist in it
    txtFile = open(targetFile, "a")

    for word in dataList:
        txtFile.write(word+"\n")
    txtFile.close()
    
            

def GUI():
    global currentData
    import WriteUp
    from datetime import datetime
    dTime = datetime.now()
    fileTypes = data = [('csv', '*.csv')]
    path = "timedata/" + dTime.strftime("%Y-%m-%d") + ".csv" #string directory/date.csv
    def help():
        import webbrowser
        page = [
                [sg.Text("To use this software you must have access to the Reddit API. Don't worry, its not as hard as it seems. Links are clickable.")],
                [sg.Text("You will need to create an app. Apps allow you to access reddit via the API.")],
                [sg.Text("- Create a Reddit acount "),sg.Text("https://www.reddit.com/",key="-LINK1-",enable_events = True)],
                [sg.Text("- Navigate to the dev apps section, and click 'create another app' at the bottom "),sg.Text("https://www.reddit.com/prefs/apps",key="-LINK2-",enable_events = True)],
                [sg.Text("- Choose a name, type in http://localhost:8080 for the redirect uri, you can leave the rest blank.")],
                [sg.Text("\n\nApps have 5 key pieces of data you need to log in... ")],
                [sg.Text("1. client id, 14 digit code located in the top left, to the right of the icon.")],
                [sg.Text("1. client secret, 28 digit code located under the name, to the right of the icon.")],
                [sg.Text("2. client secret, 14 digit code located in top/mid left, just below name.")],
                [sg.Text("3. user_agent, The name of your app.")],
                [sg.Text("4. username, Your Reddit username, located at top of page.")],
                [sg.Text("5. password, Your Reddit password, located in safety deposit box...")],
                [sg.Text("\n\n If you are still having issues please review all the info and make sure it is correct.")],
                [sg.Text("If you think you may have encountered a bug, please feel free to message me on reddit: HereComesTheMoneyyy")]
            ]
        window = sg.Window("Reddit API Guide",page)
        while True:
            event,values = window.read()
            print(event)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event =="-LINK1-":
                webbrowser.open('https://www.reddit.com/', new=2)
            elif event =="-LINK2-":
                webbrowser.open('https://www.reddit.com/prefs/apps', new=2)
    def pop(title,text):
        page = [
            [sg.Text(text)],
            [sg.HSeparator()],
            [sg.Button("YES",size=(10,1),border_width = 10, enable_events = True,key="-YES-"),sg.Button("NO",size=(10,1),border_width = 10,enable_events=True,key="-NO-")]
    ]
        window = sg.Window(title,page)
        while True:
            event, values = window.read() 
            if event == "-YES-":
                window.close()
                return True
            elif event == "-NO-":
                window.close()
                return False
            else:
                return False
        window.close()
    def loginPage(): #This is the function responsible for the login page 
        import os
        creds=[] #temp array of reddit api credentials
        if os.stat("txt/credentials.txt").st_size != 0:
            with open("txt/credentials.txt","r") as file:
                file.seek(0) #go to start of txt file
                for line in file: 
                    creds.append(line) #add credentials to array
                    #print(line) 
                file.close()
            client=creds[0]
            secret=creds[1]
            agent=creds[2]
            username=creds[3]
            password=creds[4]
        else:
            client=''
            secret=''
            agent=''
            username=''
            password=''
        errorMessage = ''
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
            sg.Input(password,size=(25, 1), enable_events=True, key="-PASS-",password_char='*')],
            [sg.Text(errorMessage,size=(30,1),text_color='red',key="-ERROR-",background_color='white')],
            [sg.Button("SAVE",size=(10,1),border_width = buttonBW, enable_events = True,key="-SAVE-"),sg.Button("HELP",size=(10,1),border_width = buttonBW,enable_events=True,key="-HELP-"),sg.Button("CLEAR",size=(10,1),border_width = buttonBW,enable_events=True,key="-CLEAR-")]
            
            
            
        ]
        window = sg.Window("Sign-In",page)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "-HELP-":
                window.close()
                help()
            elif event == "-CLEAR-":
                #print("clear")
                window["-CLIENT-"].update('')
                window["-SECRET-"].update('')
                window["-AGENT-"].update('')
                window["-USERNAME-"].update('')
                window["-PASS-"].update('')
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
                    if redditAccount[0]:
                        errorMessage = "Success!"
                        window["-ERROR-"].update(errorMessage)
                        f = open("txt/credentials.txt","w")
                        f.write(client)
                        f.write(secret)
                        f.write(agent)
                        f.write(username)
                        f.write(password)
                        f.close()
                        return redditAccount[1]
                        break
                    else:
                        errorMessage = redditAccount[1]
                        window["-ERROR-"].update("Unable to sign-in to Reddit")
                        redditAccount=''
                        

                else:
                    errorMessage = "Please enter the missing data."
                    window["-ERROR-"].update(errorMessage)

    display = "\n\n\nData will be shown on the right once the algorithm runs successfully\nNote: performance varies based on processing power and connection\nPlease allow enough runtime, a few minutes per 100 posts"
    # First the window layout in 2 columns

    sg.theme("Python")
    sg.set_options(font="callibri")
    buttonBW = 6
    file_list_column = [
        [
            sg.Text("                      INTELLIGENT ALGORITHMS\n\n\n\n\n",)
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
                 background_color="White",size=(80,30),key="-PROMPT-")],
        [sg.Input(key='-FILE-', enable_events=True, visible = False),sg.FileBrowse("LOAD",size=(20,1),target = "-FILE-",file_types=("CSV Files", "*.csv")),
        sg.Button("OPEN",size=(20,1),key="-OPEN-"),
        sg.Input(key='-SAVEFILE-', enable_events=True, visible = False),
         sg.FileSaveAs("SAVE",size=(20,1),target="-SAVEFILE-",file_types=".csv",initial_folder='timedata')],
        [sg.Text("Note: only csv files are acceptable")]
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]


    window = sg.Window("Intelligent Algorithms from Mimifur V.1.1(Dev.Py Edition)",resizable=True).Layout(layout)
    window.finalize()
    windowData=''
    # Run the Event Loop
    while True:
        event, values = window.read()
        print(event)
        if event == "Exit" or event == sg.WIN_CLOSED:
            #print(knownNonStocks)
            break
        # Folder name was filled in, make a list of files in the folder
        elif event == "-SIGN-":
            #print("SI")
            loginPage()
        elif event == "-GO-":
            window["-PROMPT-"].update("Loading...")
            #print(values["-SUB-"])
            
            if values["-POSTS-"] == '' or values["-SUB-"] == '':
                window["-PROMPT-"].update("Please enter the proper information")
            elif values["-POSTS-"].isnumeric()==False:
                window["-PROMPT-"].update("Please enter a number between 1 and 1000")
            elif float(values["-POSTS-"])%2 != 0:
                window["-PROMPT-"].update("Please enter a number between 1 and 1000")
            elif login == None:
                window["-PROMPT-"].update("Please login to Reddit")
            elif sub_exists(values["-SUB-"],login) == False:
                window["-PROMPT-"].update("Invalid subreddit")
            else:
                window["-PROMPT-"].update("Working magic")
                temp = runAlg(values["-SUB-"],values["-POSTS-"])
                print(temp)
                if temp == "Login Error":
                    window["-PROMPT-"].update("Please login to Reddit")
                else:
                    window["-PROMPT-"].update("")
                    windowData = temp
                    window["-PROMPT-"].update("Data is ready, Save?")
        elif event == "-FILE-":
            if values["-FILE-"][-4:] == ".csv": #Checks if last 4 chars are equal to .csv
                window["-PROMPT-"].update("Open "+values["-FILE-"]+"?")
            else:
                window["-PROMPT-"].update("Invalid File format")
                values["-FILE-"] = ''
        elif event == "-SAVEFILE-":
            print("saving")
            if windowData == '':
                window["-PROMPT-"].update("Data is empty")
            elif pop("Warning","File will be saved as " + values["-SAVEFILE-"] + ".csv | Any conflicting files will be overwritten. Continue?"):
                if values["-SAVEFILE-"][-4:]!=".csv":
                    values["-SAVEFILE-"] = values["-SAVEFILE-"] + ".csv"
                wU = WriteUp.WriteUpObject(WriteUp.split_list(currentData),values["-SAVEFILE-"])
                wU.newCSV()
                window["-PROMPT-"].update("Data has been stored at " + wU.path)
        elif event == "-OPEN-":
            if values["-FILE-"] != '':
                window["-PROMPT-"].update("")
                import graphing
                graphing.graphData(values["-FILE-"])
            else:
                window["-PROMPT-"].update("No file has been selected")
        
            

    window.close()

GUI()
