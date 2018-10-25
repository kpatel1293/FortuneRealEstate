sample = [{"letter": 'a'}, {"letter":'b'}, {"letter":'c'}, {"letter":'d'}, {"letter":'e'}, {"letter":'f'}, {"letter":'g'}]
arr = []
newarr = []
print sample

for s in sample:
    if len(arr) == 3:
        newarr.append(arr)
        arr = []

    arr.append(s)

if len(arr) != 0:
    newarr.append(arr)
    arr = []
    
print newarr