# -*- coding: utf-8 -*-
from Tkinter import *
import json, pprint, io

#Creating tkinter app window:
app = Tk()
app.title("Quiz Application")
app.geometry('450x450+200+200')

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
        print ('Useing default dummy data instead')
        return spm
    except Exception as e: 
        print('Problem loading JSON object.')
        print('Errormessage: ' + e)
        print ('Useing default dummy data instead')
        return spm


# Evaluates a question, returns True if correct answer, False otherwise
def evaluate_question(index, answer):
    if spm[index]["answer"] == spm[index][answer]:
        labelText = StringVar()
        labelText.set("Riktig Svar! Bra jobba!")
        feedbackMessage = Label(app, textvariable=labelText, height="3", foreground="green").pack()
    else:
        labelText = StringVar()
        labelText.set(spm[index]["read"])
        feedbackMessage = Label(app, textvariable=labelText, height="3").pack()
    
#This function removes all unessary widgets from the frame
def remove_frames():
    for widget in app.winfo_children():
        widget.destroy()

#This function goes to the next question
#It can only increment the i value if i is less then the length of the list
#If i is equal to the length of the list i will be set to 0(first question)
def next_question(i):
    remove_frames()
    #print i
    if i == len(spm)-1:
        i = 0
    elif i < len(spm)-1:
        i += 1
    present_question(i)

# Presents a question to the user with the help of the UI
def present_question(index):
    remove_frames()
    question = spm[index]["q"]
    
    #Question as a label
    labelText = StringVar()
    labelText.set(question)
    question = Label(app, textvariable=labelText, height="3", wraplength="250").pack()

    #Value for radiobutton
    rbValue = StringVar(value=2)
    rbValue2 = StringVar()
    
    #Answer button
    answerbutton = Button(app, text="Check Answer", width=20, padx=5, pady=5, state="disabled", command = lambda: give_feedback(index, rbValue.get()))
    #Radiobuttons
    #This is made to support questions with varying number of alternatives
    #radiobuttons also sets the answer button to active, to keep the application from crashing
    rbContainer = Frame(app)
    for i in range(1, len(spm[index])-2):
        valueString = "a" + str(i)
        rb = Radiobutton(rbContainer, text=spm[index][valueString], justify="left",  variable=rbValue, value=valueString, command = lambda: answerbutton.config(state="active"))
        rb.pack(anchor="w")
    rbContainer.pack()
    #Answer button rendering
    answerbutton.pack()

    #Next question button
    nextquestion = Button(app, text="Gå til neste spørsmål", width=20, padx=5, pady=5, command = lambda: next_question(index)).pack()
    discontinue = Button(app, text="Avslutt quiz", width=20, padx=5, pady=5, command = lambda: front_page()).pack()


# Gives feedback to the user with the help of the UI
def give_feedback(index, answer):
    remove_frames()
    question = spm[index]["q"]
    
    #Question as a label
    labelText = StringVar()
    labelText.set(question)
    question = Label(app, textvariable=labelText, height="3", wraplength="250").pack()

    #Render labels with varying colors of corretnes
    #Red is for wrong answer, green is for right answer
    answerContainer = Frame(app)
    if spm[index]["answer"] == spm[index][answer]:
        for i in range(1,len(spm[index])-2):
            labelText = StringVar()
            valueString = "a" + str(i)
            if spm[index]["answer"] == spm[index][valueString]:
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", foreground="green").pack(anchor="w")
            else:
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", foreground="red").pack(anchor="w")
    else:
        for i in range(1,len(spm[index])-2):
            labelText = StringVar()
            valueString = "a" + str(i)
            #print valueString
            #print spm[index]["answer"]
            #print spm[index]
            if spm[index][answer] == spm[index][valueString]:
                #print "du er rød"
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", foreground="red").pack(anchor="w")
            else:
                #print "du er svart"
                labelText.set(spm[index][valueString])
                Label(answerContainer, textvariable=labelText, height="2", foreground="black").pack(anchor="w")

    answerContainer.pack()
    evaluate_question(index, answer)
    
    #Next question button
    nextquestion = Button(app, text="Gå til neste spørsmål", width=20, padx=5, pady=5, command = lambda: next_question(index)).pack()
    discontinue = Button(app, text="Avslutt quiz", width=20, padx=5, pady=5, command = lambda: front_page()).pack()
    

def front_page():
    remove_frames()
    labelText = StringVar()
    labelText.set("Velkommen til quiz i praktisk prosjektledelse")
    title = Label(app, textvariable=labelText, height="3", ).pack()
    #title.config(font=("Arial",30))

    Button(app, text="Start quiz", width=20, padx=5, pady=5, command = lambda: present_question(0)).pack()

    labelText = StringVar()
    labelText.set("Laget av gruppe 19.")
    title = Label(app, textvariable=labelText, height="3", ).pack()
    
    
# Initiate the UI
def init_ui():
    front_page()

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
