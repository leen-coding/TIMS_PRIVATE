import torchvision
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from torch import nn
# from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms
import torch
import cv2
import os
from PIL import Image

root_path = "C:/LeenWS/yolov5/2ndC/"
open_dir = "0"
close_dir = "1"


# openList = os.listdir(openImgPath)
#
# img = cv2.imread(os.path.join(openImgPath, openList[0]))
# cv2.imshow("capture", img)
# cv2.waitKey(0)



class BinaryData(Dataset):

    def __init__(self, root_dir, label_dir, transform):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)
        self.transform = transform

    def __getitem__(self, item):
        img_name = self.img_path[item]
        img_item_path = os.path.join(self.path, img_name)
        img = cv2.imread(img_item_path)
        label = int(self.label_dir)
        img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.img_path)


if __name__ == '__main__':
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((100,100)),#touch or not (50,50)close or not
        # transforms.Grayscale(num_output_channels=1)
        # transforms.RandomHorizontalFlip(),
        # transforms.RandomRotation(degrees=(-180, 180)),
    ])
    open_dataset = BinaryData(root_path, open_dir, transform)
    close_dataset = BinaryData(root_path, close_dir, transform)
    full_dataset = open_dataset + close_dataset
    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])

    train_dataloader = DataLoader(dataset=train_dataset, batch_size=8, shuffle=True, num_workers=0, drop_last=True)
    test_dataloader = DataLoader(dataset=test_dataset, batch_size=8, shuffle=True, num_workers=0, drop_last=True)
    # myModel = Net()

    myModel = torchvision.models.resnet50(num_classes=2)
    # myModel.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    # print(myModel)
    # myModel = torchvision.models.mobilenet_v3_small(weights=None)

    # myModel = Tudui()

    loss_fn = torch.nn.CrossEntropyLoss()

    if torch.cuda.is_available():
        myModel = myModel.cuda()
        loss_fn = loss_fn.cuda()

    learning_rate = 1e-3
    optimizer = torch.optim.SGD(myModel.parameters(), lr=learning_rate, momentum=0.9)

    total_train_step = 0
    # 记录测试的次数
    total_test_step = 0
    # 训练的轮数
    epoch = 50
    # writer = SummaryWriter("../logs_train")
    for i in range(epoch):
        print("-------第 {} 轮训练开始-------".format(i + 1))
        train_acc = 0
        total_train_acc = 0
        total_train_loss = 0
        # 训练步骤开始
        myModel.train()
        for data in train_dataloader:
            imgs, targets = data
            # print(targets)
            if torch.cuda.is_available():
                imgs = imgs.cuda()
                targets = targets.cuda()
            outputs = myModel(imgs)
            loss = loss_fn(outputs, targets)
            total_train_loss = total_train_loss + loss.item()
            train_acc = (outputs.argmax(1) == targets).sum()
            # print(outputs.argmax(1))
            total_train_acc = total_train_acc + train_acc
            # 优化器优化模型
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_train_step = total_train_step + 1
            if total_train_step % 100 == 0:
                print("训练次数：{}, Loss: {}".format(total_train_step, loss.item()))
                # writer.add_scalar("train_loss", loss.item(), total_train_step)
        print("整体测试集上的Loss: {}".format(total_train_loss))
        print("整体训练集上的正确率: {}".format(total_train_acc / train_size))
        # 测试步骤开始
        myModel.eval()
        total_test_loss = 0
        total_accuracy = 0
        with torch.no_grad():
            for data in test_dataloader:
                imgs, targets = data
                if torch.cuda.is_available():
                    imgs = imgs.cuda()

                    targets = targets.cuda()
                outputs = myModel(imgs)
                loss = loss_fn(outputs, targets)
                total_test_loss = total_test_loss + loss.item()
                accuracy = (outputs.argmax(1) == targets).sum()
                # print(outputs.argmax(1))
                total_accuracy = total_accuracy + accuracy

        print("整体测试集上的Loss: {}".format(total_test_loss))
        print("整体测试集上的正确率: {}".format(total_accuracy / test_size))
        # writer.add_scalar("test_loss", total_test_loss, total_test_step)
        # writer.add_scalar("test_accuracy", total_accuracy / test_size, total_test_step)
        total_test_step = total_test_step + 1

        torch.save(myModel, "binaryModel_{}.pth".format(i))
        print("模型已保存")

    # writer.close()
