import numpy as np
import os
import pickle

from matplotlib import pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.model_selection import train_test_split
PATH = "C:\LeenWS\src\micro_control_pkg\scripts\GPR_data"
record = []
for path in os.listdir(PATH):
    txt_path = os.path.join(PATH,path)
    record.append(np.loadtxt(txt_path))


# 创建包含重复元素的数组

from collections import OrderedDict

# 创建包含重复元素的数组

unique_record = []
down_sample = []
min_len = 200000
for arr in record:
    unique_arr = np.array(list(OrderedDict.fromkeys(map(tuple, arr))))

    if min_len>len(unique_arr):
        min_len = len(unique_arr)
print(min_len)
for arr in record:
    unique_arr = np.array(list(OrderedDict.fromkeys(map(tuple, arr))))
    unique_record.append(unique_arr)


    indices = np.linspace(0, unique_arr.shape[0]-1,min_len, dtype=np.int16)
    down_sample.append(np.take(unique_arr, indices, axis=0))

# x = unique_arr[:, 0]
# y = unique_arr[:, 1]
# z = unique_arr[:, 2]

# # Creating figure
# fig = plt.figure(figsize=(10, 7))
# ax = plt.axes(projection="3d")
 
# # Creating plot
# ax.scatter3D(x, y, z, color="green")
# plt.title("simple 3D scatter plot")
 
# # show plot
# plt.show()


count = []
for i in range(0, min_len, 1):
    count.append(i)
count = np.array(count)
Y = []
X = []
for traj in down_sample:
    for x in count:
        Y.append(traj[x])
        X.append(x)
Y = np.array(Y)
Y_x = Y[:,0]
Y_y = Y[:,1]
Y_z = Y[:,2]
X = np.array(X)
X = X.reshape(-1,1)
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)



# 创建高斯过程回归模型

#
# kernel = C(100, (0.001, 100)) * RBF(0.5, (1e-4, 5000))
# # 创建高斯过程回归,并训练
# reg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=20, alpha=0.1)
# 创建高斯过程回归,并训练
reg = GaussianProcessRegressor()
# # 使用输入数据和输出数据拟合模型
reg.fit(X,Y)
GPRPickle = open('C:\LeenWS\src\micro_control_pkg\scripts\GPRpickle_file', 'wb')

# source, destination
pickle.dump(reg, GPRPickle)

# y_pred = reg.predict(X_test)

# from sklearn.metrics import mean_absolute_error
#
# mae = mean_absolute_error(y_test, y_pred)
# print(mae)




# print("ok")


