import random
n, m = map(int, input().split())
data = []
for i in range(3):
    data.extend([j for j in range(1,n*m+1)])
random.shuffle(data)
flag = True
while flag:
    flag = False
    for i in range(0,n*m*3-3,3):
        temp = [data[i],data[i+1],data[i+2]]
        if len(temp) != len(set(temp)):
            flag = True
            random.shuffle(data)
            break
print(data)

