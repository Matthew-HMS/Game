import random

score = random.randint(0, 100)

max_score = 0
def write_record():
    global max_score,score,score_list
    file = open("test.txt", "a")
    file.write(str(score) + "\n")
    file = open("test.txt", "r")
    if file.mode == 'r':
        contents = file.read()
        score_list = contents.split("\n")
        for i in score_list:
            if i == '':
                continue
            else:
                int(i)
                score_list.sort(reverse = True)
    file.close()

def rank():
    count = 1
    for i in score_list:
        if i == '':
            continue
        else:
            print(str(count) + ".  " + str(i))
            count += 1


write_record()
print(score_list)
rank()  