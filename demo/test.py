# 学习笔记

##   循环
# for item in range(5):
    # print(item)
# ---------------------------------------------------------
##   列表
arr = [1,2,3,4,5,6]

# print(arr[0:2]) # 截取 0-2下标的字段 生成一个新数组

# print(arr[:2]) # 截取到下标 2的字段 生成一个新数组
# print(arr[2:]) # 从下标2开始
# print(arr[::-1]) # 倒叙输出
# print(arr[::2]) # 隔2个输出

# arr.append('傻狗')# 单个
# arr.extend(['灭吧','弱智'])# 多个
# arr.insert(1,['灭吧','弱智'])# 多个
# arr.insert(len(arr),['灭吧2','弱智3'])# 多个

# arr[2:] = ['五十']
# arr[-1] 取最后一项
# arr2 = [1,2,3]
# arr2.sort()
# arr2.reverse()
# print(arr2)

# oho = [1,2,3,4]
# for i in range(len(oho)):
#     print(i)
# ---------------------------------------------------------

##   列表推导式
# oho2 = [i*2 for i in oho]
# print(oho2)
# [2, 4, 6, 8]# arr[2:] = ['五十']

# s = [[0]*3 for i in range(3)]
# arr = [[1,2,3],[4,5,6],[7,8,9]]
# s = [j for i in arr for j in i]# 展开
# print(s)

# ---------------------------------------------------------
##   元组
# 元组 不可修改、列表可修改 
yz = 1,2,3,4,'asd'
# print(yz)

# 解包（适用于数组、字符串、元组）
# 注：左边数量必须与右边原数据数量一致，否则报错
# 除非加 *
# a,b,c,d,e=yz
# print(a,b,c,d)

# a,*b = yz
# print(a,b)

# ---------------------------------------------------------
##   字符串
x = '12321'
# print('yes' if x==x[::-1] else 'no')
# print(f"we are format{x}")

# ---------------------------------------------------------
##   序列
print(list(x))
print(len(x))
print(tuple(x))
print(str(x))
 
# ---------------------------------------------------------
##   序列
print('nc_id:',id(x))#   查找内存地址
# 检查内存地址 是否相同
print(x is x)#   
print(x is not  x)#   
# 检查 是否包含
print('f' in 'asdf')#   
print('f' not in 'asdf')#   

# 删除
del x
# print(x)#   name 'x' is not defined
arr = [1,2,3,4,5]
# arr[1:4] = [] == del arr[1:4]
del arr[:]
print(arr)#  []

# all() || any()
x = [1,1,0]
y=[1,1,9]

print(all(x))# 
print(any(x))# 

for i,v in enumerate(x):
    print(i,v)# 

# zip()
print(list(zip(x,y)))# 
def pow(a):
    return a*2
def filterFn(a):
    return a==2
ss = map(pow,[1,2,3])
print(list(ss))# 

ss = filter(filterFn,[1,2,3])
print(list(ss))# 

x = [1,2,3,4,5]
y = iter(x)

print(type(x),type(y))
