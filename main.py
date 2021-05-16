#erinisafox
#UsernameHunter

#Purpose :: Testing how many (and how accurately) usernames can be automatically
#           flagged for inapprpriate words.

#Files   :: last-month-users.txt, provided by sysadmin.
#           usernameblacklist.txt, created by me and viewable in repo
#           usernamewhitelist.txt, created by me and viewable in repo
#           usernametestedlist.txt, copied from admin spreadsheet
#           usernamedecisions.txt, copied from admin spreadsheet

from math import *

print("This can take a bit to run depending on file size. Currently running...")

#Contains every username from the last month in separate rows
usernames = open("last-month-users.txt","r")
#Contains blacklisted words in separate rows. ENDOFFILE is a dummy word.
blacklist = open("usernameblacklist.txt","r")
#Contains whitelisted words in separate rows. ENDOFFILE is a dummy word.
whitelist = open("usernamewhitelist.txt","r")
#Contains subset of usernames that were checked manually by mods 
testedlist = open("usernametestedlist.txt","r")
#Contains decisions from the subset of manually tested usernames
decisionlist = open("usernamedecisions.txt","r")

#Initialize arrays. :-1 is to get rid of the \n at the end of every entry
flaggednames = [] #keeps track of bad usernames
numberoftotalusernames = 0 #keeps track of total number of usernames
blist = [] #blacklisted words list
wlist = [] #whitelisted words list
namefrequency = [] #tracker for how often a blacklisted word triggers
namecheck = [] #tracker for how often a blacklisted word is manually reviewed
namehit = [] #tracker for whether the trigger and manual review agree
tested = [] #list of tested usernames
decision = [] #list of decisions
for line in testedlist:
    tested.append(line[14:-5]) #format is of the form lichess.org/@/XXX?mod
    namehit.append(0)
    namecheck.append(0)
for line in decisionlist:
    if line[:-1] != "bad": #the majority of usernames are unclear/unchecked
        decision.append("good") #assume they're good if not explicitly bad
    else:
        decision.append(line[:-1])
for line in blacklist: #load blacklist
    blist.append(line[:-1])
    namefrequency.append(0)
for line in whitelist: #load whitelist
    wlist.append(line[:-1])

#Actually do the checking. The loops get nested and confusing
for line in usernames: #loop over every username
    line = line.lower() #normalize everything to lowercase
    numberoftotalusernames = numberoftotalusernames + 1

    #Check if a username contains a blacklisted word but not a whitelisted word.
    #If that's true, then great. Check to see if it was ever manually checked.
    #If it was, then great. We now know if we got a false positive detection.
    #If it was never manually checked, oh well, that's too bad.
    for bword in range(0,len(blist)): #loop over every blacklisted word
        if blist[bword] in line: #bword counts elements in blsit
            isinwhitelist = False
            for wword in wlist: #check to see if a word is whitelisted
                if wword in line:
                    isinwhitelist = True
                    break
            if not isinwhitelist: #was the word truly bad?
                flaggednames.append(line[:-1])
                namefrequency[bword] = namefrequency[bword] + 1
                for check in range(0, len(tested)): #was it manually reviewed?
                    if line[:-1] == tested[check]:
                        namecheck[bword] = namecheck[bword] + 1
                        if decision[check]  == "bad": #was it reviewed as bad?
                            namehit[bword] = namehit[bword] + 1
            break

#Print blacklist and whitelist
print("\nBlacklist")
print("---------")
print(blist[:-1])
print("\nWhitelist")
print("---------")
print(wlist[:-1])

#Print all flagged usernames in hyperlink form (for easy trasnfer to spreadsheet)
print("\nFlagged names:")
print("--------------")
for X in range(0,len(flaggednames)):
    print("lichess.org/@/"+flaggednames[X]+"?mod")
            
#Print various general stats
print("\nFlag counts:")
print("------------")
print("Monthly flags: " + str(sum(namefrequency)))
print("Total usernames: " + str(numberoftotalusernames))
print("Percentage flagged: " + str(round(100.0 * sum(namefrequency) / numberoftotalusernames,1)))
print("Report accuracy: " + str(round(100.0*sum(namehit)/sum(namecheck),1)))

#Calculate stats for more stats below, and print individual blacklist word stats
accuratehits = 0
accuratefreq = 0
goodnessthreshold = 0.30
suggestedblacklist = []
for X in range(0,len(blist)):
    if namecheck[X] != 0:
        print("%-20s %-40s" % (blist[X] , "\t(" + str(namefrequency[X]) + ") " + str(namehit[X]) + " / " + str(namecheck[X]) + " = " + str(round(100.0*namehit[X]/namecheck[X],1))))
        if namehit[X]/namecheck[X]>goodnessthreshold:
            accuratehits = accuratehits + namehit[X]
            accuratefreq = accuratefreq + namecheck[X]
            suggestedblacklist.append(blist[X])

#Print the >20 stats
print("\nIf we only allow hit accuracy of >30%")
print("-------------------------------------")
print("Monthly flags: " + str(accuratefreq))
print("Report accuracy: " + str(round(100.0*accuratehits/accuratefreq,1)))
print("Closures per day: " + str(round(accuratehits / 30.0,1)))
print("Reports per day: " + str(round(accuratefreq / 30.0,1)))

print("\nSuggested Blacklist")
print("-------------------")
print(suggestedblacklist)

#END
