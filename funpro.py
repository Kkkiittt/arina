import json
import re #regex
from datetime import datetime
def imya(name):
    return re.fullmatch(r"[A-Za-z\s'-]+", name) is not None #перепроверить
def birtg(birth):
    try:
        datetime.strptime(birth.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False
def id(aydi): 
    return aydi.isdigit()
def que():
    return [
        ("do you regularly drink herbal tea while studying?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("do you prefer herbal tea over caffeinated drinks during study sessions?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("do you consume herbal tea specifically to improve your concentration??",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("do you drink herbal tea at least 3 times per week while studying?",
         [("never", 0), ("rarely", 1), ("maybe", 2), ("often", 3), ("always", 4)]),
        ("do you choose specific types of herbal tea based on their calming effects?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("does drinking herbal tea help you stay focused for longer periods??",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("do you feel more mentally alert after drinking herbal tea??",
         [("always", 0), ("often", 1), ("maybe", 2), ("rarely", 3), ("never", 4)]),
        ("how often do you feel calm?",
         [("always", 0), ("often", 1), ("sometimes", 2), ("rarely", 3), ("never", 4)]),
        ("does herbal tea improve your overall study performance?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("very often", 3), ("always", 4)]),
        ("does herbal tea reduce distractions during your study sessions??",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("does herbal tea help you feel calmer while studying?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("super often", 3), ("always", 4)]),
        ("do you experience less stress when you drink herbal tea during study sessions?",
         [("always", 0), ("often", 1), ("sometimes", 2), ("rarely", 3), ("never", 4)]),
        ("does herbal tea help reduce anxiety before exams or assignments?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("do you feel more relaxed and less overwhelmed when drinking herbal tea?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)]),
        ("does herbal tea create a comfortable and productive study environment for you?",
         [("never", 0), ("rarely", 1), ("sometimes", 2), ("often", 3), ("always", 4)])
    ]
def surv():
    questions=que() #чек листы
    totscore=0
    for h,(question,options) in enumerate(questions,1): #or use range? range(len(totscore))
        print(f"\nQue{h}:{question}")
        for hamburger, (option,_) in enumerate(options,1):
            print(f"{hamburger}.{option}")

        while True:
            try:
                choice=int(input("choose var: "))
                if 1<=choice<=len(options):
                    totscore+=options[choice-1][1]  #gg andrey i komil
                    break
                else:
                    print("incorrect var") 
            except:
                print("ent a number")

    return totscore
def result(score):
    if score<=15:
        return "very low effect"
    elif score<=30:
        return "preference to search for other methods"
    elif score<=50:
        return "neutral impact"
    elif score<=60:
        return "high calm focus from herbal tea"
    else:
        return "negative or opposite effect"
def saveres(data):
    with open("results.json","w") as file:
        json.dump(data,file,indent=4)
    print("saved to results.json")
def loadres():
    try:
        with open("results.json","r") as file:
            data=json.load(file)
            print("\nloaded result:")
            print(data)
    except:
        print("no saved file found")
def main():
    print("1.load previous result")
    print("2.start new survey")

    choice=input("choose: ")

    if choice=="1":
        loadres()
    elif choice=="2":
        while True:
            name=input("enter name: ")
            if imya(name):
                break
            print("invalid name")

        while True:
            birth=input("enter date of birth (year-month-date): ")
            if birtg(birth):
                break
            print("invalid date.")

        while True:
            aydi=input("enter id: ")
            if id(aydi):
                break
            print("incorrect id")

        score=surv()
        finresult=result(score)

        print(f"\ntotal score: {score}")
        print(f"result: {finresult}")

        save=input("save result? (yeah/nope): ")
        if save.lower()=='yeah':
            data = {
                "name": name,
                "date of birth": birth,
                "id": aydi,
                "score": score,
                "result": finresult
            }
            saveres(data)

    else:
        print("invalid choice.")
if __name__=="__main__":
    main()
