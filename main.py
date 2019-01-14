from time import sleep
from json import loads
import csv
import sys
from re import match
from requests import get

#print the prompt and punchline with a 2s interval
def run(prompt, punchline):
    print(prompt)
    sleep(2)
    print(punchline)

#determine users' input and raise a ValueError if anything other than "next" or "quit" is given
def read(userInput):
    if userInput == "next":
        return True
    elif userInput == "quit":
        return False
    else:
        raise ValueError("I don't understand. Please try again.")

#driver function. Run the program by running python3 main.py (csv file name or blank)
if __name__ == '__main__':
    if len(sys.argv) == 1:
        #deal with the case when a csv file is not given and the reddit posts are used as default jokes
        r = get('https://www.reddit.com/r/dadjokes.json', headers = {'User-agent': 'my bot 0.1'})
        #convert the Response object to a python dictionary. primary keys are "kind" and "data"
        content = loads(r.text)
        #extract all posts from dictionary
        posts = content["data"]["children"]
        #open a csv file to store the jokes
        with open('jokefile_default.csv', mode = 'w') as f:
            jokeWriter = csv.writer(f, delimiter = ',') #create writer object
            for post in posts:
                data = post["data"] #data for each post
                over_18 = data["over_18"] #check if safe for work
                title = data["title"] #prompt
                selftext = data["selftext"] #punchline
                #check if 1. prompt starts with Why/What/How; 2. not over 18; 3. punchline not empty
                if match('^(Why|What|How)', title) and not over_18 and not selftext == "":
                    jokeWriter.writerow([title, selftext]) #write joke in file
        f.close() #close file after done writing it
        csvfile = 'jokefile_default.csv' #set csvfile to default

        #else:
            #raise ValueError("Wrong number of parameters provided, no jokefile found")

    elif len(sys.argv) == 2: #when a csv file is given
        if not match('^.*\.(csv)$', sys.argv[1]):
            raise ValueError("A csv file should be supplied.") #check if the file's extension is csv
        csvfile = sys.argv[1] #set csvfile to the command line argument
    else:
        raise ValueError("Wrong number of arguments.")
    with open(csvfile, newline='') as f: #read csv file, whether default or set by command line
        jokeReader = csv.reader(f, delimiter = ',')
        nextRow = next(jokeReader) #get the first joke
        run(nextRow[0], nextRow[1]) #print the first joke
        while True:
            try:
                 userInput = input() #get user input. Catch exception if input not recognized
                 if read(userInput): #"next" case
                     nextRow = next(jokeReader) #get the next joke
                     run(nextRow[0], nextRow[1]) #print the next joke
                 else: #"quit" case
                     sys.exit(0) #exit the program
            except ValueError as v: #"unknown" inputs
                print(v) #print error message
                pass #back to start of the while loop
            except StopIteration as s: #stop when there's no more jokes to tell
                print("No more jokes to tell.")
                sys.exit(0) #exit the program
