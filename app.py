from Tkinter import *

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
        "q": "Hvilken av f�lgende oppgaver kan defineres som et prosjekt?",
        "a1": "Et mobiltelefonselskap aktiverer en ny kundetjeneste",
        "a2": "En bilprodusent produserer en dags kvote med kj�ret�y",
        "a3": "Et IT-firma utvikler en ny �Crash proof� operativsystem",
        "a4": "En forhandler fyller p� hyllene etter en dag med mye salg.",
        "answer": "a1",
        "read": "Where to read more"
    }
]

# Import questions, return JSON object with 
# questions, answers, and more reading material
def import_questions():
    return None

# Evaluates a question, returns True if correct answer, False otherwise
def evaluate_question(question, answer):
    return None

# Presents a question to the user with the help of the UI
def present_question(index):
    question = spm[index]["q"]
    a1 = spm[index]["a1"]
    a2 = spm[index]["a2"]
    a3 = spm[index]["a3"]
    a4 = spm[index]["a4"]
    
    #Question as a label
    labelText = StringVar()
    labelText.set(question)
    question = Label(app, textvariable=labelText, height="3").pack()
    
    #print "hei3"
    #Radiobuttons
    rb = Radiobutton(app, text=a1, value="a1", command=sendAlternative).pack()
    rb = Radiobutton(app, text=a2, value="a2", command=sendAlternative).pack()
    rb = Radiobutton(app, text=a3, value="a3", command=sendAlternative).pack()
    rb = Radiobutton(app, text=a4, value="a4", command=sendAlternative).pack()
    
    #Answer button
    answer = "a1"
    answerbutton = Button(app, text="Check Answer", width=20, padx=5, pady=5, command= lambda: checkAnswer(index, rb.value)).pack()
    
    #Next question button
    nextquestion = Button(app, text="Go to next question", width=20, padx=5, pady=5, command = lambda: nextQuestion(index)).pack()
    
    #Previous question button(work in progress)
    #previousQuestion = Button(app, text="Go to previous question", width=20, padx=5, pady=5, command = lambda: previousQuestion(index)).pack()

# Gives feedback to the user with the help of the UI
def give_feedback():
    return None

# Initiate the UI
def init_ui():
    return None

# Main function
def main():
    i = 0
    present_question(i)

#Displays app window in a loop
app.mainloop()
if __name__== "__main__":
  main()
