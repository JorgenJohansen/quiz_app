# -*- coding: utf-8 -*-
from Tkinter import *
import json, pprint, io

#Creating tkinter app window:
app = Tk()
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
        labelText = StringVar()
        labelText.set("Riktig Svar! Bra jobba!")
        Label(app, textvariable=labelText, height="3", font="10", foreground="green").pack()
        stats["rightAnswers"] += 1
    else:
        #Rendering the wrong answer and incrementing the wrongAnswers variable
        labelText = StringVar()
        labelText.set(spm[index]["read"])
        Label(app, textvariable=labelText, height="3", font="10").pack()
        stats["wrongAnswers"] += 1
    
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

    #Error handling
    #If user enters in illegal characters, an empty string, letters, too large limits, just zero or a negative integer 
    #It sets the questionLimit to the length of all the questions in spm.json
    if illegalCharacters(limit) or limit == '' or str(limit).isalpha() or int(limit) > len(import_questions()) or int(limit) <= 0 :
        questionLimit = len(import_questions())
    else:
        questionLimit = int(limit)
    
    #Fontsize:
    titleFont = "15"
    labelFont = "10"
    buttonFont = "8"

    #Progression in the quiz
    progressionText = "Spørsmål " + str((index+1)) + " av " + str(questionLimit)
    labelText1 = StringVar()
    labelText1.set(progressionText)
    Label(app, textvariable=labelText1, font=titleFont, height="3").pack()

    #Question as a label
    question = spm[index]["q"]
    labelText2 = StringVar()
    labelText2.set(question)
    question = Label(app, textvariable=labelText2, height="3", wraplength="400", font=titleFont).pack()

    #Value for radiobutton
    rbValue = StringVar(value=2)
    
    #Answer button
    answerbutton = Button(app, text="Sjekk svar", font=buttonFont, width=20, padx=5, pady=5, state="disabled", command = lambda: give_feedback(index, rbValue.get(),questionLimit))
    
    #Radiobuttons
    #This is made to support questions with varying number of alternatives
    #radiobuttons also sets the answer button to active, to keep the application from crashing
    rbContainer = Frame(app)
    for i in range(1, len(spm[index])-2):
        valueString = "a" + str(i)
        rb = Radiobutton(rbContainer, text=spm[index][valueString], justify="left", font=labelFont,  variable=rbValue, value=valueString, command = lambda: answerbutton.config(state="active"))
        rb.pack(anchor="w")
    rbContainer.pack()

    #Answer button rendering
    answerbutton.pack()

    #Next question button
    nextquestion = Button(app, text="Gå til neste spørsmål", font=buttonFont, width=20, padx=5, pady=5, command = lambda: next_question(index,questionLimit))
    
    #Stat page button
    statpage = Button(app, text="Avsluttende Statistikk", font=buttonFont, width=20, padx=5, pady=5, command = lambda: stat_page(questionLimit))

    #Rendering the right button on where we are in the quiz
    if (index+1) < limit:
        nextquestion.pack()
    else:
        statpage.pack()
    
    #Discontinue button
    Button(app, text="Avslutt quiz", font="10", width=20, padx=5, pady=5, command = lambda: front_page(questionLimit)).pack()


# Gives feedback to the user with the help of the UI
def give_feedback(index, answer, questionLimit):
    remove_frames()
    question = spm[index]["q"]

    #Fontsize:
    titleFont = "15"
    labelFont = "10"
    buttonFont = "8"

    #Progression in the quiz
    progressionText = "Spørsmål " + str((index+1)) + " av " + str(questionLimit)
    labelText1 = StringVar()
    labelText1.set(progressionText)
    Label(app, textvariable=labelText1, font=titleFont, height="3").pack()
    
    #Question as a label
    labelText = StringVar()
    labelText.set(question)
    question = Label(app, textvariable=labelText, height="3", wraplength="400", font=titleFont).pack()

    #Render labels with varying colors of corretnes
    #Red is for wrong answer, green is for right answer
    answerContainer = Frame(app)
    if spm[index]["answer"] == spm[index][answer]:
        for i in range(1,len(spm[index])-2):
            labelText = StringVar()
            valueString = "a" + str(i)
            if spm[index]["answer"] == spm[index][valueString]:
                #Rendering the right answer with green color
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", font=labelFont, foreground="green").pack(anchor="w")
            else:
                #Rendering the wrong alternatives with red color
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", font=labelFont, foreground="red").pack(anchor="w")
    else:
        for i in range(1,len(spm[index])-2):
            labelText = StringVar()
            valueString = "a" + str(i)
            if spm[index][answer] == spm[index][valueString]:
                #Rendering the wrong alternative with a red color
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", font=labelFont, foreground="red").pack(anchor="w")
            else:
                #Rendering the other alternatives with black
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", font=labelFont, foreground="black").pack(anchor="w")

    #Rendering the answer container
    answerContainer.pack()
    
    #Calling the evaluate question function
    evaluate_question(index, answer)
    
    #Next question button
    nextquestion = Button(app, text="Gå til neste spørsmål", font=buttonFont, width=20, padx=5, pady=5, command = lambda: next_question(index, questionLimit))

    #Stat page button
    statpage = Button(app, text="Avsluttende Statistikk", font=buttonFont, width=20, padx=5, pady=5, command = lambda: stat_page(questionLimit))

    #Rendering the right button on where we are in the quiz
    if (index+1) < questionLimit:
        nextquestion.pack()
    else:
        statpage.pack()
    Button(app, text="Avslutt quiz", font="10", width=20, padx=5, pady=5, command = lambda: front_page(questionLimit)).pack()
    
#This function makes the front page of the application
def front_page(limit):
    #Removing existing frames
    remove_frames()

    #Fontsize:
    buttonFont = "10"
    labelFont = "10"

    #Reset progress:
    stats["wrongAnswers"] = 0
    stats["rightAnswers"] = 0

    #The total amount of questions we have
    totalQuestions = len(import_questions())
    
    #Rendering the title of the front page
    labelText = StringVar()
    labelText.set("Velkommen til Quiz i Praktisk Prosjektledelse!")
    title = Label(app, textvariable=labelText, height="3", font="30").pack()

    #Rendering amount of questions title
    labelText = StringVar()
    labelText.set("Hvor mange spørsmål vil du svare på?")
    title = Label(app, textvariable=labelText, height="3", font="10").pack()
    
    #Input field
    entry = Entry(app, width="2", font=labelFont)
    entry.insert(0,limit)
    entry.grid(row=0, column=0)
    entry.pack()
    
    
    #Rendering the amount of questions we have in the quiz
    labelText = StringVar()
    labelText.set("av " + str(totalQuestions))
    title = Label(app, textvariable=labelText, font=labelFont)
    title.grid(row=0, column=1)
    title.pack()

    #Rendering the start button
    startbutton = Button(app, text="Start Quiz", width=20, font=buttonFont, padx="10", pady="10", command = lambda: present_question(0, entry.get()))
    startbutton.pack(pady=20)
    
    #Rendering the footer of the front page
    labelText = StringVar()
    labelText.set("Laget av gruppe 19.")
    title = Label(app, textvariable=labelText, height="3", font="20").pack()


def stat_page(questionLimit):
    remove_frames()

    #Fontsize:
    titleFont = "20"
    labelFont = "10"

    #Label for the title
    labelText = StringVar()
    labelText.set("Avsluttende Statistikk")
    Label(app, textvariable=labelText, height="3", font=titleFont).pack()

    #Label for unanswered questions
    uansweredQuestions = questionLimit - stats["wrongAnswers"] - stats["rightAnswers"]
    labelText = StringVar()
    #More accurate language
    if uansweredQuestions == 1:
        labelText.set("Du hadde " + str(uansweredQuestions) + " ubesvart spørsmål.")
    else:
        labelText.set("Du hadde " + str(uansweredQuestions) + " ubesvarte spørsmål.")
    unasweredQuestionsLabel = Label(app, textvariable=labelText, height="3", font=labelFont)

    #Label for right answers
    labelText = StringVar()
    #More accurate language
    if stats["rightAnswers"] == 1:
        labelText.set("Du hadde " + str(stats["rightAnswers"]) + " riktig svar av " + str(questionLimit) + ".")
    else:
        labelText.set("Du hadde " + str(stats["rightAnswers"]) + " riktige svar av " + str(questionLimit) + ".")
    rightAnswersLabel = Label(app, textvariable=labelText, height="3", font=labelFont)

    #Label for wrong answer
    labelText = StringVar()
    labelText.set("Du hadde " + str(stats["wrongAnswers"]) + " feil svar av " + str(questionLimit) + ".")
    wrongAnswersLabel = Label(app, textvariable=labelText, height="3", font=labelFont)

    #Conditional rendering of labels
    if stats["rightAnswers"] == questionLimit:
        labelText = StringVar()
        labelText.set("Supert! Du hadde rett på alt!")
        Label(app, textvariable=labelText, height="3", font=labelFont).pack()
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

    Button(app, text="Avslutt quiz", font="10", width=20, padx=5, pady=5, command = lambda: front_page(questionLimit)).pack()


    
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
