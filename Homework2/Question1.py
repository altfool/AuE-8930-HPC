def solution(list, num): 
    a=0 
    b=0 
    '''type in your solution, find a and b in array that a+b=num'''
    mylist = []
    for val in list:
        if num-val in mylist:
            a = num - val
            b = val
        else:
            mylist.append(val)
    return a, b 
  
numbers = [0, 21, 78, 19, 90, 13] 
print(solution(numbers, 21)) 
print(solution(numbers, 25)) 
