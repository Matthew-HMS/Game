import random

score = random.randint(0, 100)

max_score = 0
def write_record():
    global max_score,score
    file = open("test.txt", "a")
    file.write(str(score) + "\n")
    file = open("test.txt", "r")
    if file.mode == 'r':
        contents = file.read()
        score_list = contents.split("\n")
        for i in score_list:
            if i == '':
                continue
            elif int(i) > max_score:
                max_score = int(i)
    file.close()

write_record()
print(max_score)