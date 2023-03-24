

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