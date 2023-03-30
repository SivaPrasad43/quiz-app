import pandas as pd
import random
from timeit import default_timer as timer
import time
import os.path

data = pd.read_csv("data_added.csv")
options = ["A","B","C","D"]
beginner_count=intermediate_count=advanced_count = 0
point = 0 


df = pd.DataFrame(columns=['qid', 'Answer', 'Selected Answer', 'Time Taken', 'Mark Obtained', 'Level'])
df.to_csv('report.csv', index=False, mode='w')

def typing_display(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def program_exp():
    user_ans = input("Do you have programing experience?(1=yes and 0=No)")
    return user_ans

def run_quiz():
    print("---PRE-ASSESSMENT TEST----\n")
    print("Subject : PYTHON")
    response = program_exp()
    for count in range(15):
        question_set = question(count)
        selection_set =  select_answer()
        check_answer(question_set,selection_set,response)

def select_answer():
    starting_time = timer()
    answer = input("select option : ").upper()
    end_time = timer()
    time_taken = end_time - starting_time
    return answer,time_taken

def question(count):
    print("--------------------------------------")
    random_index = random.choice(data.index)
    random_row = data.loc[random_index]
    question_id = random_row['Question ID']
    question = random_row['Question']
    answer = random_row['Correct Answer']
    level = random_row['Difficulty Level']
    global beginner_count,intermediate_count,advanced_count
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
    print(f"status => big : {beginner_count} inter : {intermediate_count} adv: {advanced_count}\n")
    return question_id,question,answer,level

def check_answer(question_set,selection_set,response):
    global point,status
    if selection_set[0] == question_set[2]:
        print("Correct!!")
        point = mark_obtained(question_set[3])
        status = "correct"
    else:
        print(f"Wrong!!")
        status = "wrong"
    generate_analysis_report(question_set,selection_set,point,status,response)
    print(f"Question Level : {question_set[3]}")
    print(f"Time Taken : {'{:.2f}'.format(selection_set[1])} sec")
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
    if os.path.isfile('report.csv'):
        df = pd.read_csv('report.csv')
        df = df.append(new_row, ignore_index=True)
        df.to_csv('report.csv', index=False)
    else:
        df = pd.DataFrame([analysis_data])
        df.to_csv('report.csv', index=False)

if __name__ == "__main__":
    run_quiz()