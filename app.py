# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
#from ttkthemes import ThemedStyle
import json, io

#Creating tkinter app window:
app = Tk()

#OPTION 1 for theme: import ttkthemes
# Define style for how the app looks. Commented out commands show available styles. This uses ttkthemes with more theme options
#TTkthemes needs to be pip installed
#Change theme by simply change the value inside s.set_theme('')
#--------------------------------------------------------------
#s = ThemedStyle(app)
#print(s.theme_names())
#print(s.theme_use())
#s.set_theme('scidblue')
#print(s.theme_use())

#OPTION 2 for theme: default
#Same thing, but with less options. Vista seems to be best "looking" here imo
s = ttk.Style()
print(s.theme_names())
s.theme_use('vista')
print(s.theme_use())

#Fonts used for the app
font = ('Verdana 12')
fontSmall = ('Verdana 9')
fontBold = ('Verdana 12 bold')
fontsBold = ('Verdana 10 bold')
fontItalic = ('Verdana 10 italic')
s.configure('Correct', foreground='Green')
s.configure('Wrong', foreground='Red')
labelFont = "10"

app.title("Quiz Application")
app.geometry('600x600+200+200')
#app.configure(borderwidth=2, relief="solid")

#Dummy data:
#Can be deleted when questions are imported from spm.json
#Make sure to change present_questions if that is necessary
spm = [
    {
        "q": "Question 1",
        "a1": "Answer 1",
        "a2": "Answer 2",
        "a3": "Answer 3",
        "a4": "Answer 4",
        "answer": "a1",
        "read": "Where to read more about the question"
    },
    {
        "q": "Hvilken av følgende oppgaver kan defineres som et prosjekt?",
        "a1": "Et mobiltelefonselskap aktiverer en ny kundetjeneste",
        "a2": "En bilprodusent produserer en dags kvote med kjøretøy",
        "a3": "Et IT-firma utvikler en ny \"Crash proof\" operativsystem",
        "a4": "En forhandler fyller på hyllene etter en dag med mye salg.",
        "answer": "a1",
        "read": "Where to read more"
    }
]

stats = {
    "rightAnswers": 0,
    "wrongAnswers": 0
}

# Import questions, return JSON object with questions, answers, and more reading material
# Requires the JSON object to be in same dictionary and named: spm.json
# May be modified to account for different paths and names for JSON object
def import_questions():
    #global spm
    try:
        with io.open('spm.json', 'r', encoding='utf-8') as fh:
            json_object = json.load(fh)
            json_file = json_object.get(u'spm')
            return json_file
    except EnvironmentError:
        print('Problem loading JSON.')
        print('Check if json file exists in same dir and name is spm.json')
        print ('Using default dummy data instead')
        return spm
    except Exception as e: 
        print('Problem loading JSON object.')
        print('Errormessage: ' + e)
        print ('Using default dummy data instead')
        return spm


# Evaluates a question, returns True if correct answer, False otherwise
# Also increments the right and wrong answer variables
def evaluate_question(index, answer):
    if spm[index]["answer"] == spm[index][answer]:
        #Rendering the right answer and incrementing the rightAnswers variable
        #labelText = StringVar()
        #labelText.set("Riktig Svar! Bra jobba!")
        #Label(app, textvariable=labelText, height="3", font="10", foreground="green").pack()
        stats["rightAnswers"] += 1
        return("Riktig Svar! Bra jobba!")
    else:
        #Rendering the wrong answer and incrementing the wrongAnswers variable
        #labelText = StringVar()
        #labelText.set(spm[index]["read"])
        #Label(app, textvariable=labelText, height="3", font="10").pack()
        stats["wrongAnswers"] += 1
        return(spm[index]["read"])
    
#This function removes all widgets from the frame
def remove_frames():
    for widget in app.winfo_children():
        widget.destroy()

#This function goes to the next question
#It can only increment the i value if i is less then the length of the list
#If i is equal to the length of the list i will be set to 0(first question)
def next_question(i, questionLimit):
    remove_frames()
    if i == questionLimit-1:
        i = 0
    elif i < questionLimit-1:
        i += 1
    present_question(i, questionLimit)

#This function returns true if there is an illegal charater in the limit, returns false otherwise
def illegalCharacters(limit):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~+¤|'''
    for x in str(limit):
        for y in punctuations:
            if x == y:
                return TRUE
    return FALSE

# Presents a question to the user with the help of the UI
def present_question(index, limit):
    remove_frames()
    main_frame = ttk.Frame(app, borderwidth=1)
    main_frame.pack(fill='both', expand=True)

    #Error handling
    #If user enters in illegal characters, an empty string, letters, too large limits, just zero or a negative integer 
    #It sets the questionLimit to the length of all the questions in spm.json
    if illegalCharacters(limit) or limit == '' or str(limit).isalpha() or int(limit) > len(import_questions()) or int(limit) <= 0 :
        questionLimit = len(import_questions())
    else:
        questionLimit = int(limit)

    #Progression in the quiz
    progressionText = "Spørsmål " + str((index+1)) + " av " + str(questionLimit)
    labelText1 = StringVar()
    labelText1.set(progressionText)
    ttk.Label(main_frame, text=labelText1.get(), font=fontBold).pack(pady=10)

    #Question as a label
    question = spm[index]["q"]
    labelText2 = StringVar()
    labelText2.set(question)
    question = ttk.Label(main_frame, text=labelText2.get(), font=font, wraplength=450).pack(pady=20)

    #Value for radiobutton
    rbValue = StringVar(value=2)

    frame = ttk.Frame(main_frame)
    
    #Answer button
    answerbutton = ttk.Button(frame, text="Sjekk svar", state="disabled", command = lambda: give_feedback(index, rbValue.get(),questionLimit))
    
    #Radiobuttons
    #This is made to support questions with varying number of alternatives
    #radiobuttons also sets the answer button to active, to keep the application from crashing
    rbContainer = Frame(main_frame)
    for i in range(1, len(spm[index])-2):
        valueString = "a" + str(i)
        rb = ttk.Radiobutton(rbContainer, text=spm[index][valueString],  variable=rbValue, value=valueString, command = lambda: answerbutton.config(state="active"))
        rb.pack(anchor="w", fill='both')
    rbContainer.pack()

    frame.pack(pady=20)

    #Answer button rendering
    answerbutton.pack(side=LEFT, padx=10, ipadx=10, ipady=10)

    #Next question button
    nextquestion = ttk.Button(frame, text="Gå til neste spørsmål", command = lambda: next_question(index,questionLimit))
    
    #Stat page button
    statpage = ttk.Button(frame, text="Avsluttende Statistikk", command = lambda: stat_page(questionLimit))

    #Rendering the right button on where we are in the quiz
    if (index+1) < limit:
        nextquestion.pack(side=RIGHT, ipadx=10, ipady=10)
    else:
        statpage.pack(side=RIGHT, ipadx=10, ipady=10)
    
    #Discontinue button
    ttk.Button(main_frame, text="Avslutt quiz", command = lambda: front_page(questionLimit)).pack(pady=20)


# Gives feedback to the user with the help of the UI
def give_feedback(index, answer, questionLimit):
    remove_frames()
    main_frame = ttk.Frame(app, borderwidth=1)
    main_frame.pack(fill='both', expand=True)

    question = spm[index]["q"]

    #Progression in the quiz
    progressionText = "Spørsmål " + str((index+1)) + " av " + str(questionLimit)
    labelText1 = StringVar()
    labelText1.set(progressionText)
    ttk.Label(main_frame, text=labelText1.get(), font=fontBold).pack(pady=10)
    
    #Question as a label
    labelText = StringVar()
    labelText.set(question)
    question = ttk.Label(main_frame, text=labelText.get(), font=font).pack(pady=20)

    #Render labels with varying colors of corretnes
    #Red is for wrong answer, green is for right answer
    answerContainer = Frame(main_frame)
    if spm[index]["answer"] == spm[index][answer]:
        for i in range(1,len(spm[index])-2):
            labelText = StringVar()
            valueString = "a" + str(i)
            if spm[index]["answer"] == spm[index][valueString]:
                #Rendering the right answer with green color
                labelText.set(spm[index][valueString])
                ttk.Label(answerContainer, text=labelText.get(), font=fontSmall, foreground="limegreen").pack(anchor="w", fill='both')
            else:
                #Rendering the wrong alternatives with red color
                labelText.set(spm[index][valueString])
                ttk.Label(answerContainer, text=labelText.get(), font=fontSmall, foreground="red").pack(anchor="w", fill='both')
    else:
        for i in range(1,len(spm[index])-2):
            labelText = StringVar()
            valueString = "a" + str(i)
            if spm[index][answer] == spm[index][valueString]:
                #Rendering the wrong alternative with a red color
                labelText.set(spm[index][valueString])
                ttk.Label(answerContainer, text=labelText.get(), font=fontSmall, foreground="red").pack(anchor="w", fill='both')
            else:
                #Rendering the other alternatives with black
                labelText.set(spm[index][valueString])
                ttk.Label(answerContainer, text=labelText.get(), font=fontSmall, foreground="black").pack(anchor="w", fill='both')

    #Rendering the answer container
    answerContainer.pack()
    
    #Calling the evaluate question function
    feedback = evaluate_question(index, answer)
    if (feedback == "Riktig Svar! Bra jobba!"):
        ttk.Label(main_frame, text=feedback, font=fontsBold, foreground="limegreen").pack(pady=10)
    else:
        ttk.Label(main_frame, text=feedback, font=fontsBold).pack(pady=10)
    
    #Next question button
    nextquestion = ttk.Button(main_frame, text="Gå til neste spørsmål", command = lambda: next_question(index, questionLimit))

    #Stat page button
    statpage = ttk.Button(main_frame, text="Avsluttende Statistikk", command = lambda: stat_page(questionLimit))

    #Rendering the right button on where we are in the quiz
    if (index+1) < questionLimit:
        nextquestion.pack(ipadx=12, ipady=12, pady=20)
    else:
        statpage.pack(ipady=12, ipadx=12, pady=20)
    ttk.Button(main_frame, text="Avslutt quiz", command = lambda: front_page(questionLimit)).pack(pady=20)

#This function makes the front page of the application
def front_page(limit):
    #Removing existing frames
    remove_frames()
    main_frame = ttk.Frame(app, borderwidth=1)
    main_frame.pack(fill='both', expand=True)

    #Reset progress:
    stats["wrongAnswers"] = 0
    stats["rightAnswers"] = 0

    #The total amount of questions we have
    totalQuestions = len(import_questions())
    
    #Rendering the title of the front page
    labelText1 = StringVar()
    labelText1.set("Velkommen til Quiz i Praktisk Prosjektledelse!")
    title = ttk.Label(main_frame, text=labelText1.get(), font=fontBold)
    title.pack(padx=10, pady=10)
    

    #Rendering amount of questions title
    labelText2 = StringVar()
    labelText2.set("Hvor mange spørsmål vil du svare på?")
    title = ttk.Label(main_frame, text=labelText2.get(), font=font).pack(padx=10, pady=10)

    # Frame to put two widgets next to each other
    frame = ttk.Frame(main_frame)
    frame.pack(pady=10)

    #Input field
    entry = ttk.Entry(frame, width="2", font=labelFont)
    entry.insert(0,limit)
    entry.pack(side=LEFT)
    
    
    #Rendering the amount of questions we have in the quiz
    labelText = StringVar()
    labelText.set("av " + str(totalQuestions))
    title = ttk.Label(frame, text=labelText.get(), font=labelFont)
    title.pack(side=RIGHT)

    #Rendering the start button
    startbutton = ttk.Button(main_frame, text="Start Quiz", command = lambda: present_question(0, entry.get()))
    startbutton.pack(ipady=12, ipadx=12, pady=10)
    
    #Rendering the footer of the front page
    labelText = StringVar()
    labelText.set("Laget av gruppe 19.")
    title = ttk.Label(main_frame, text=labelText.get(), font=fontItalic).pack(pady=20)


def stat_page(questionLimit):
    remove_frames()
    main_frame = ttk.Frame(app, borderwidth=1)
    main_frame.pack(fill='both', expand=True)

    #Label for the title
    labelText = StringVar()
    labelText.set("Avsluttende Statistikk")
    ttk.Label(main_frame, text=labelText.get(), font=fontBold).pack(pady=20)

    #Label for unanswered questions
    uansweredQuestions = questionLimit - stats["wrongAnswers"] - stats["rightAnswers"]
    labelText = StringVar()
    #More accurate language
    if uansweredQuestions == 1:
        labelText.set("Du hadde " + str(uansweredQuestions) + " ubesvart spørsmål.")
    else:
        labelText.set("Du hadde " + str(uansweredQuestions) + " ubesvarte spørsmål.")
    unasweredQuestionsLabel = ttk.Label(main_frame, text=labelText.get(), font=font)

    #Label for right answers
    labelText = StringVar()
    #More accurate language
    if stats["rightAnswers"] == 1:
        labelText.set("Du hadde " + str(stats["rightAnswers"]) + " riktig svar av " + str(questionLimit) + ".")
    else:
        labelText.set("Du hadde " + str(stats["rightAnswers"]) + " riktige svar av " + str(questionLimit) + ".")
    rightAnswersLabel = ttk.Label(main_frame, text=labelText.get(), font=font)

    #Label for wrong answer
    labelText = StringVar()
    labelText.set("Du hadde " + str(stats["wrongAnswers"]) + " feil svar av " + str(questionLimit) + ".")
    wrongAnswersLabel = ttk.Label(main_frame, text=labelText.get(), font=font)

    #Conditional rendering of labels
    if stats["rightAnswers"] == questionLimit:
        labelText = StringVar()
        labelText.set("Supert! Du hadde rett på alt!")
        ttk.Label(main_frame, text=labelText.get(), font=font, foreground="limegreen").pack()
    elif stats["wrongAnswers"] == questionLimit:
        wrongAnswersLabel.pack()
    elif stats["rightAnswers"] == 0 and stats["wrongAnswers"] == 0:
        unasweredQuestionsLabel.pack()
    elif stats["rightAnswers"] == 0 and uansweredQuestions > 0:
        wrongAnswersLabel.pack()
        unasweredQuestionsLabel.pack()
    elif stats["wrongAnswers"] == 0 and uansweredQuestions > 0:
        rightAnswersLabel.pack()
        unasweredQuestionsLabel.pack()
    
    else:
        rightAnswersLabel.pack()
        wrongAnswersLabel.pack()
        if uansweredQuestions > 0:
            unasweredQuestionsLabel.pack()

    ttk.Button(main_frame, text="Avslutt quiz", command = lambda: front_page(questionLimit)).pack(ipady=12, ipadx=12, pady=20)


    
# Initiate the UI
def init_ui():
    limit = len(import_questions())
    front_page(limit)

# Main function
def main():
    global spm
    spm = import_questions()
    init_ui()
    #i = 0
    #present_question(i)


if __name__== "__main__":
  main()

#Displays app window in a loop
app.mainloop()
