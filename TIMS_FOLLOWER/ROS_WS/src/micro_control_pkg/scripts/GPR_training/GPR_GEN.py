import os
import pickle

import numpy as np
from matplotlib import pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split



# 打开文件
with open('C:\LeenWS\src\micro_control_pkg\scripts\GPRpickle_file_rbf_good_1w_test', 'rb') as f:
    # 读取文件内容
    data = pickle.load(f)

# 使用 data 作为参数调用 GaussianProcessRegressor
model = GaussianProcessRegressor.set_params(data)
# model.score()
count = []
def range_with_floats(start, stop, step):
    while stop > start:
        yield start
        start += step


for i in range_with_floats(0, 632 , 0.1):
    count.append(i)
count = np.array(count)
out_list = []
std_list = []
for x in count:
    x = np.array(x)
    x = x.reshape(-1,1)
    out = model.predict(x)*10000
    print(out)
    out= out.reshape(3,)
    # std =std.reshape(3,)
    out_list.append(out)
    # std_list.append(std)


out_list = np.array(out_list)
std_list = np.array(std_list)
np.savetxt('src\micro_control_pkg\scripts\gprfile_rbf_best.txt', out_list, newline='\n')



print(out_list)