import os
import pickle

import numpy as np
from matplotlib import pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split

# PATH = "traj_data"
# record = []
# for path in os.listdir(PATH):
#     txt_path = os.path.join(PATH,path)
#     record.append(np.loadtxt(txt_path))


# # 创建包含重复元素的数组

# from collections import OrderedDict

# # 创建包含重复元素的数组

# unique_record = []
# down_sample = []
# for arr in record:
#     unique_arr = np.array(list(OrderedDict.fromkeys(map(tuple, arr))))
#     unique_record.append(unique_arr)
#     indices = np.linspace(0, unique_arr.shape[0]-1, 1500, dtype=np.int32)
#     down_sample.append(np.take(unique_arr, indices, axis=0))

# count = []
# for i in range(0, 1500, 1):
#     count.append(i)
# count = np.array(count)
# Y = []
# X = []
# for traj in down_sample:
#     for x in count:
#         Y.append(traj[x])
#         X.append(x)
# Y = np.array(Y)
# X = np.array(X)
# X = X.reshape(-1,1)
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)



# 打开文件
with open('src\micro_control_pkg\scripts\GPRpickle_file', 'rb') as f:
    # 读取文件内容
    data = pickle.load(f)

# 使用 data 作为参数调用 GaussianProcessRegressor
model = GaussianProcessRegressor.set_params(data)
count = []
for i in range(0, 632, 1):
    count.append(i)
count = np.array(count)
out_list = []
std_list = []
for x in count:
    x = np.array(x)
    x = x.reshape(-1,1)
    out = model.predict(x)
    print(out)
    out= out.reshape(3,)
    # std =std.reshape(3,)
    out_list.append(out)
    # std_list.append(std)


out_list = np.array(out_list)
std_list = np.array(std_list)
np.savetxt('src\micro_control_pkg\scripts\gprfile.txt', out_list, newline='\n')
# Define the list of strings
# mean_prediction = model.predict(count)
# mean_prediction = out_list.squeeze()
# std_prediction = std_list.squeeze()

# std_prediction = std_prediction.squeeze()
# plt.plot(X, y, label=r"$f(x) = x \sin(x)$", linestyle="dotted")
# plt.errorbar(
#     X,
#     Y[:,2],
#     # noise_std,
#     linestyle="None",
#     color="tab:blue",
#     marker=".",
#     markersize=1,
#     label="Observations",
#     zorder=1
# )
# plt.plot(mean_prediction,color = 'r',linewidth = '1', label="Mean prediction",zorder=2)
# plt.fill_between(
#     count.ravel(),
#     mean_prediction - 19.6 * std_prediction,
#     mean_prediction + 19.6 * std_prediction,
#     color="tab:orange",
#     alpha=0.5,
#     label=r"95% confidence interval",
# )
# plt.legend()
# plt.xlabel("$t$")
# plt.ylabel("$Z$")
# _ = plt.title("Gaussian process regression on Z axis of trajectory")
# plt.show()
# Open the file for writing


print(out_list)