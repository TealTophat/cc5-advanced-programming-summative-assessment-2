from tkinter import *
from tkinter import ttk
import requests
import html

#----VARIABLE DECLARATION----
#trivia_info = "coconut"
question_amount = 10
category = 9
difficulty = "easy"
question_no = 0
points = 0

#----PYTHON CODE----

# Request and return trivia data
def get_trivia_info(amount = "10", category = "9", difficulty = "easy"):
    global trivia_info
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type=boolean"
    response = requests.get(url)
    print(f"{response}: Request is Successful!")
    print(f"Generated Link: {url}")

    if response.status_code == 200:
        trivia_data = response.json()
        #print(trivia_data)
        return trivia_data
    else:
        print(f"{response}: Failed to retrieve the data")
        return None  

# Change Title Screen Frame into Menu Frame
def startSelect():
    mainFrame.pack_forget()
    selectFrame.pack(fill="both",expand=True)

# Function for declaring the number of questions to be answered
def setQuestionAmount(event):
    global question_amount
    try:
        newamount = int(amountEntry.get())
        if newamount <= 50:
            question_amount = newamount
            print("New amount set: "+str(newamount))
        else:
            errorLabel.config(text="Please enter a number below 50.")
    except ValueError:
        print("Please input a valid integer.")
        return None
    
# Function for declating the trivia category
def setCategory(event):
    global category
    newcategory = categoryDropdown.get()
    match newcategory:
        case "General Knowledge":
            category = 9
        case "Entertainment: Books":
            category = 10
        case "Entertainment: Film":
            category = 11
        case "Entertainment: Music":
            category = 12
        case "Entertainment: Musicals & Theatres":
            category = 13
        case "Entertainment: Television":
            category = 14
        case "Entertainment: Video Games":
            category = 15
        case "Entertainment: Board Games":
            category = 16
        case "Science & Nature":
            category = 17
        case "Science: Computers":
            category = 18
        case "Science: Mathematics":
            category = 19
        case "Mythology":
            category = 20
        case "Sports":
            category = 21
        case "Geography":
            category = 22
        case "History":
            category = 23
        case "Politics":
            category = 24
        case "Art":
            category = 25
        case "Celebrities":
            category = 26
        case "Animals":
            category = 27
    print("New category set: "+str(category))

# Function for setting the trivia difficulty
def setDifficulty(event):
    global difficulty
    newdifficulty = difficultyDropdown.get()
    match newdifficulty:
        case "Easy":
            difficulty = "easy"
        case "Medium":
            difficulty = "medium"
        case "Hard":
            difficulty = "hard"
    print("New difficulty set: "+str(difficulty))

# Menu Frame -> Trivia Frame; Begin trivia loop with the first question
def startTrivia():
    global trivia_info
    global question_amount
    #Initialize trivia data and display the first question of the Trivia
    trivia_info = get_trivia_info(question_amount, category, difficulty)

    if trivia_info == None:
        errorLabel.config(text="API could not be requested.")
    elif trivia_info["response_code"] == 0:
        question_amount = len(trivia_info["results"])
        print("Response Code 0: Returned results successfully.")
        print("No. of Questions in this Trivia: "+str(question_amount))
        newquestion = (trivia_info["results"][0]["question"])
        triviaLabel.config(text=html.unescape(newquestion))
        selectFrame.pack_forget()
        triviaFrame.pack(fill="both",expand=True)
        errorLabel.config(text="")
    elif trivia_info["response_code"] == 1:
        print("Response Code 1: Could not return results. The API doesn't have enough questions for your query. (Ex. Asking for 50 Questions in a Category that only has 20.)")
        errorLabel.config(text="Could not return results. The API doesn't have enough questions for your query.")
        return
    else:
        errorLabel.config(text="Something has gone wrong.")
        return
    
# Function for recieveing and handling the user's answer
def questionAttempt(useranswer):
    global trivia_info
    global points
    global question_no
    correctanswer = trivia_info["results"][question_no]["correct_answer"]
    print("The correct answer to question "+str(question_no)+" was: "+correctanswer)
    if useranswer == correctanswer:
        triviaFrame.pack_forget()
        intermissionFrame.pack(fill="both",expand=True)
        intermissionLabel.config(text="You got it right!")
        question_no += 1
        points += 1
    else:
        triviaFrame.pack_forget()
        intermissionFrame.pack(fill="both",expand=True)
        intermissionLabel.config(text="Oops! That wasn't right!")
        question_no += 1

# Trivia Frame -> Intermission Frame; Main loop of the program
# Changes to Trivia Frame -> Results Frame if all questions are answered
def nextQuestion():
    global question_amount
    global question_no
    global points
    if question_no != question_amount:
        intermissionFrame.pack_forget()
        triviaFrame.pack(fill="both",expand=True)
        triviaLabel.config(text=html.unescape(trivia_info["results"][question_no]["question"]))
    else:
        intermissionFrame.pack_forget()
        resultFrame.pack(fill="both",expand=True)
        resultLabel.config(text=f"You finished the quiz with {points} out of {question_amount} points!")

# Reset all program variables and return to Main Frame
def resetTrivia():
    global question_amount
    global question_no
    global points
    global trivia_info
    #Hide resultFrame/Show mainFrame
    resultFrame.pack_forget()
    mainFrame.pack(fill="both",expand=True)
    #Reset variables and input fields
    question_amount = 10
    question_no = 0
    points = 0
    amountEntry.delete(0, END)
    categoryDropdown.set("")
    difficultyDropdown.set("")

trivia_info = get_trivia_info(question_amount, category, difficulty)


#----TKINTER SETUP----
root=Tk()
root.title("SUPER TRIVIA GAME")
root.geometry("640x360")
root.config(background="khaki")

#Frame 1: MAIN MENU
mainFrame = Frame(root, bg="khaki")
mainFrame.pack(fill="both", expand=True)

# Centering grid
mainFrame.grid_rowconfigure(0, weight=1)
mainFrame.grid_columnconfigure(0, weight=1)

mainContent = Frame(mainFrame, bg="khaki")
mainContent.grid(row=0, column=0)

mainLabel = Label(mainContent, text="SUPER TRIVIA", font=("Arial",50,"bold"), bg="khaki", wraplength=400)
mainButton = Button(mainContent, text="Begin Game", font=("Helvetica", 10, "bold"),bg="khaki3", command=startSelect)

mainLabel.pack(pady=20)
mainButton.pack()

#Frame 2: SELECTION MENU
selectFrame = Frame(root,bg="khaki")
selectFrame.grid_rowconfigure(0, weight=1)
selectFrame.grid_columnconfigure(0, weight=1)


selectContent = Frame(selectFrame, bg="khaki")
selectContent.grid(row=0, column=0)
selectContent.grid_rowconfigure(0, weight=1)
selectContent.grid_rowconfigure(1, weight=1)
selectContent.grid_rowconfigure(2, weight=1)
selectContent.grid_rowconfigure(3, weight=1)
selectContent.grid_rowconfigure(4, weight=1)
selectContent.grid_rowconfigure(5, weight=1)
selectContent.grid_columnconfigure(0, weight=1)
selectContent.grid_columnconfigure(1, weight=1)

selectLabel = Label(selectContent,text="Trivia Options",font=("Arial",20,"bold"),bg="khaki")
amountLabel = Label(selectContent,text="No. of Questions",font=("Arial",20,"bold"),bg="khaki")
amountEntry = Entry(selectContent,width=50)
amountEntry.bind("<Return>", setQuestionAmount)
categoryLabel = Label(selectContent,text="Category",font=("Arial",20,"bold"),bg="khaki")
categoryDropdown = ttk.Combobox(selectContent,width=50)
categoryDropdown["values"] = (
    "General Knowledge",
    "Entertainment: Books",
    "Entertainment: Film",
    "Entertainment: Music",
    "Entertainment: Musicals & Theatres",
    "Entertainment: Television",
    "Entertainment: Video Games",
    "Entertainment: Board Games",
    "Science & Nature",
    "Science: Computers",
    "Science: Mathematics",
    "Mythology",
    "Sports",
    "Geography",
    "History",
    "Politics",
    "Art",
    "Celebrities",
    "Animals")
categoryDropdown.bind("<<ComboboxSelected>>", setCategory)
difficultyLabel = Label(selectContent,text="Difficulty Level",font=("Arial",20,"bold"),bg="khaki")
difficultyDropdown = ttk.Combobox(selectContent,width=50)
difficultyDropdown["values"] = (
    "Easy",
    "Medium",
    "Hard")
difficultyDropdown.bind("<<ComboboxSelected>>", setDifficulty)
selectButton = Button(selectContent,text="START",font=("Helvetica", 10, "bold"),bg="khaki3",command=lambda:startTrivia())
errorLabel = Label(selectContent,text="",font=("Arial",10,"bold"),bg="khaki")

selectLabel.grid(row=0,column=0,columnspan=2,sticky="ew")
amountLabel.grid(row=1,column=0,sticky="")
amountEntry.grid(row=1,column=1,sticky="")
categoryLabel.grid(row=2,column=0,sticky="")
categoryDropdown.grid(row=2,column=1,sticky="")
difficultyLabel.grid(row=3,column=0,sticky="")
difficultyDropdown.grid(row=3,column=1,sticky="")
selectButton.grid(row=4,column=0,columnspan=2,sticky="n")
errorLabel.grid(row=5,column=0,columnspan=2,sticky="n")

#Frame 3: ACTIVE QUIZ
triviaFrame = Frame(root,bg="khaki")
triviaFrame.grid_rowconfigure(0, weight=1)
triviaFrame.grid_columnconfigure(0, weight=1)

triviaContent = Frame(triviaFrame,bg="wheat3")
triviaContent.grid(row=0, column=0)

triviaLabel = Label(triviaContent,text="Question",font=("Arial",15,"bold"),bg="wheat3",wraplength=400)
trueButton = Button(triviaContent,text="TRUE",font=("Helvetica", 10, "bold"),bg="khaki3",command=lambda: questionAttempt("True"))
falseButton = Button(triviaContent,text="FALSE",font=("Helvetica", 10, "bold"),bg="khaki3",command=lambda: questionAttempt("False"))

triviaLabel.grid(row=0,pady=20,columnspan=2,sticky="")
trueButton.grid(row=1,column=0,pady=20,padx=100,sticky="")
falseButton.grid(row=1,column=1,pady=20,padx=100,sticky="")

#Frame 4: QUESTION RESULT
intermissionFrame = Frame(root,bg="khaki")
intermissionFrame.grid_rowconfigure(0, weight=1)
intermissionFrame.grid_columnconfigure(0, weight=1)

intermissionContent = Frame(intermissionFrame,bg="wheat3")
intermissionContent.grid(row=0, column=0)

intermissionLabel = Label(intermissionContent,text="Result",font=("Arial",15,"bold"),bg="khaki3",wraplength=200)
intermissionButton = Button(intermissionContent,text="NEXT",font=("Helvetica", 10, "bold"),bg="khaki3",command=lambda:nextQuestion())

intermissionLabel.grid(row=0,pady=20,sticky="")
intermissionButton.grid(row=1,pady=20,padx=100,sticky="")

#Frame 5: FINAL RESULTS
resultFrame = Frame(root,bg="khaki")
resultFrame.grid_rowconfigure(0, weight=1)
resultFrame.grid_columnconfigure(0, weight=1)

resultContent = Frame(resultFrame,bg="khaki2")
resultContent.grid(row=0, column=0)

resultLabel = Label(resultContent,text="Results",font=("Arial",15,"bold"),bg="wheat3",wraplength=600)
resultButton = Button(resultContent,text="MAIN MENU",font=("Helvetica", 10, "bold"),bg="khaki3",command=lambda:resetTrivia())

resultLabel.grid(row=0,pady=20,sticky="")
resultButton.grid(row=1,pady=20,padx=100,sticky="")

root.mainloop()