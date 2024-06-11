print("Welcome to my computer quiz!")

playing = input("Do you want to play? ")

if playing.lower()!= "yes":
    quit()
print("okay! This is a quiz game where you have 4 questions about your computer.Check out your knowledge of computer. :)",end='\n')
print("Let's play.....")

score=0

answer = input("what does CPU stand for? ").lower()
if answer=="central processing unit":
    print('currect!')
    score +=1
else:
    print("incorrect answer!")
            
answer = input("what does GPU stand for? ").lower()
if answer=="graphics processing unit":
    print('currect!')
    score +=1
else:
    print("incorrect answer!")
    
answer = input("what does RAM stand for? ").lower()
if answer=="random access memory":
    print('currect!')
    score +=1
else:
    print("incorrect answer!")
    
answer = input("what does SSD stand for? ").lower()
if answer=="solid state drive":
    print('currect!')
    score +=1
else:
    print("incorrect answer!")
    
print("You got " + str(score) + " questions correct!")
print("You got " + str((score/4)* 100) + "%.")