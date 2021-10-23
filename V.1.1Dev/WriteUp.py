class WriteUpObject:
    """Takes the format of a csv file"""
    def __init__(self,data,path): #time takes array format [second,minute,hour,dayOfMonth,month(1-12),year]
        from datetime import datetime
        self.dateTime = datetime.now()
        self.data = data #array
        self.path = path #"timedata/" + self.dateTime.strftime("%Y-%m-%d") + ".csv" #string directory/date.csv
    def getPath(self):
        return self.path

    def returnCSV(self):
        file = open(self.getPath(),"r")
        rows = []
        for row in file:
            columns = row.split(",")
            rows.append(columns)
        file.close()
        return rows

    def newCSV(self):
        file = open(self.getPath(),"w")
        for i in range(0,len(self.data[0])):
            file.write(self.data[0][i])
            file.write(",")
            file.write(self.data[1][i])
            file.write("\n")

            
        file.close()

def split_list(myList): #converts to 2 lists
    iter = 0
    list1 = []
    list2 = []
    for item in myList:
        list1.append("")
        list2.append("")
    for item in myList:    
        for char in item:
            if char.isalpha():
                list1[iter]+=char
            else:
                list2[iter]+=char
        iter+=1
   
    return [list1,list2]
    