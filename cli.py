import pandas as pd
import random
from timeit import default_timer as timer
import time
import os.path
from rich.box import Box
from rich.text import Text
from rich.console import Console
from rich.theme import Theme
from rich.table import Table


theme = Theme({"correct":"bold green","wrong":"bold red"})
console = Console(theme=theme)


data = pd.read_csv("data_added.csv")
options = ["A","B","C","D"]
beginner_count=intermediate_count=advanced_count = 0
point = 0 
question_array = []

df = pd.DataFrame(columns=['qid', 'Answer', 'Selected Answer', 'Time Taken', 'Mark Obtained', 'Level'])
df.to_csv('report.csv', index=False, mode='w')

def typing_display(text, delay=0):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def program_exp():
    user_ans = input("Do you have programing experience?(1=yes and 0=No)\nChoose option: ")
    print()
    return user_ans

def run_quiz():
    console.print("[b]---PRE-ASSESSMENT TEST----[/b]", justify="center", style="bold")
    console.print("[b]Subject : PYTHON[/b]", justify="center", style="bold blue")
    response = program_exp()
    for count in range(15):
        question_set = question(count)
        selection_set =  select_answer()
        check_answer(question_set,selection_set,response)
    print(question_array)
    proficiency_prediction()

def select_answer():
    starting_time = timer()
    answer = input("select option : ").upper()
    print("\n")
    end_time = timer()
    time_taken = end_time - starting_time
    return answer,time_taken

def question(count):
    global beginner_count,intermediate_count,advanced_count
    while True:
        random_index = random.choice(data.index)
        random_row = data.loc[random_index]
        question_id = random_row['Question ID']
        if question_id not in question_array:
            question_array.append(question_id)
            break
    question = random_row['Question']
    answer = random_row['Correct Answer']
    level = random_row['Difficulty Level']

    
    if level == "Beginner" and beginner_count<5:
        typing_display(f"{count+1} - {question}")
        beginner_count+=1
    elif level == "Intermediate" and intermediate_count<5:
        typing_display(f"{count+1} - {question}")
        intermediate_count+=1
    elif level == "Advanced" and advanced_count<5:
        typing_display(f"{count+1} - {question}")  
        advanced_count+=1

    for i, op in enumerate(random_row[options]):
        print(f"{options[i]}) {op}", end="\n")
    print("--------------------------------------")
    return question_id,question,answer,level

def check_answer(question_set,selection_set,response):
    global point,status
    if selection_set[0] == question_set[2]:
        message = Text("Correct!!", style="correct")
        point = mark_obtained(question_set[3])
        status = "correct"
    else:
        message = Text("Wrong!!", style="wrong")
        status = "wrong"
    console.print()
    console.print("[b]Question Analysis[/b]", justify="center", style="bold")
    console.print()
    console.print(message, justify="center")
    console.print()
    generate_analysis_report(question_set,selection_set,point,status,response)
    console.print(f"Question Level: {question_set[3]}", justify="center")
    console.print(f"Time Taken: {'{:.2f}'.format(selection_set[1])} sec", justify="center")
    console.print()
    point = 0

def mark_obtained(level):
    if level == "Beginner":
        return 1
    elif level == "Intermediate":
        return 2
    else:
        return 3

def generate_analysis_report(question_set,selection_set,point,status,response):
    analysis_data = {
    'qid': question_set[0],
    'prog exp': response,
    'Answer': question_set[2],
    'Selected Answer': selection_set[0],
    'Time Taken':'{:.2f}'.format(selection_set[1]),
    'Status' : status,
    'Mark Obtained' : point,
    'Level' : question_set[3] 
    }
    new_row = pd.DataFrame([analysis_data])
    csv_file = 'report.csv'

    if os.path.isfile(csv_file):
        df = pd.concat([pd.read_csv('report.csv'), new_row], ignore_index=True)
        df.to_csv(csv_file, index=False)
    else:
        df = pd.DataFrame([new_row])
        df.to_csv(csv_file, index=False)


def proficiency_prediction():
    with open('gen.py', 'r') as f:
        code_to_execute = f.read()
    exec(code_to_execute)

if __name__ == "__main__":
    run_quiz()