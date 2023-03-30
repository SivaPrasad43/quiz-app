import pandas as pd

# read pre-test report from CSV file
pretest_report = pd.read_csv('report.csv')

# define weights and time thresholds for each difficulty level
difficulty_weights = {'Beginner': 3, 'Intermediate': 5, 'Advanced': 8}
time_thresholds = {'Beginner': 10, 'Intermediate': 20, 'Advanced': 30}
penalty_factor = 1

# set proficiency levels and minimum score thresholds
proficiency_levels = ['Beginner', 'Intermediate', 'Advanced']
min_scores = [0, 30, 60]

# initialize total score and elapsed time
total_score = 0
elapsed_time = 0
correct_ans = 0
adv_q = 0
intr_q =0
big_q = 0
# iterate over each row in the pre-test report
for index, row in pretest_report.iterrows():
    # extract relevant fields from the row
    user_answer = row['Selected Answer']
    correct_answer = row['Answer']
    time_taken = row['Time Taken']
    difficulty_level = row['Level']
    status = row['Status']

    # calculate the score for the current question
    if status == "correct":
        correct_ans+=1
        if difficulty_level == "Beginner":
            big_q+=1
        elif difficulty_level == "Intermediate":
            intr_q+=1
        elif difficulty_level == "Advanced":
            adv_q+=1

        weight = difficulty_weights[difficulty_level]
        time_threshold = time_thresholds[difficulty_level]
        penalty = penalty_factor * max(0, time_taken - time_threshold)
        bonus = 1 if time_taken < time_threshold else 0
        score = (weight * (1 + bonus)) - penalty
    else:
        score = 0

    # add the score to the total score
    total_score += score

    # add the elapsed time for the current question
    elapsed_time += time_taken

# calculate the index of the proficiency level based on the score and minimum score thresholds
level_index = -1
for i in range(len(proficiency_levels)):
    if total_score >= min_scores[i]:
        level_index = i

# ensure the index is within valid bounds
if level_index == -1:
    proficiency_level = 'No proficiency level'
else:
    proficiency_level = proficiency_levels[level_index]

# output the determined proficiency level
print("Your score is "+ str(total_score))
print(f"You are Answered {correct_ans} questions Correctly!!\n")
print(f"They are Beginner:{big_q} Intermediate:{intr_q} Advanced:{adv_q}\n")
print('The student belongs to', proficiency_level, 'proficiency level\n')
