

def show(name='meibo',year='18'):
    print(f'{name},{year}')

show()
show(year=21,name='sad')
show(21,'sad')

def show2(*params,year='18'):
    print(f'{params[0]},{year}')
show2(21,15,'sad')

# 匿名函数
g = lambda x:x*2+1

print(g(5))

arr = [{'xywh': [511.0, 130.5, 82.0, 73.0], 'label': 'hbl_1'}, {'xywh': [259.5, 352.0, 59.0, 24.0], 'label': 'door'}, {'xywh': [490.5, 320.5, 75.0, 21.0], 'label': 'user'}]

for i,v in enumerate(arr):
    # if(arr[])
    if(v['label']=='user'):
        print(i,v)
    else:
        continue
