'''
Author: Dong
Date: 2021-01-06 20:54:53
LastEditors: Dong
LastEditTime: 2021-01-07 22:21:12
'''
import pandas as pd
import numpy as np

list = ['旗舰','专营']

p = pd.read_excel('1.xlsx')
p['品牌'] = None
for i in range(len(list)):
  for j in p.index:
    if list[i] in p.loc[j, '店铺名称']:
      p.loc[j, '品牌'] = list[i]
    elif not p.loc[j, '品牌']:
      p.loc[j, '品牌'] = ''

p.to_excel('data.xlsx')
print(p)