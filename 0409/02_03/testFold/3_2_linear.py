from matplotlib import pyplot as plt
from mxnet import  autograd ,nd
import random

num_inputs = 2
num_examples = 1000

true_w = [2, -3.4]
true_b = 4.2

features = nd.random.normal(scale=1,shape=(num_examples, num_inputs))
labels = true_w[0]*features[:,0] + true_w[1]*features[:,1] + true_b
labels += nd.random.normal(scale=0.01,shape=labels.shape)


def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    random.shuffle(indices)

    for i in range(0, num_examples, batch_size):
        j = nd.array(indices[i:min(batch_size + i, num_examples)])
        yield features.take(j), labels.take(j)


batch_size = 10
#
# for X, y in data_iter(batch_size, features, labels):
#     print(X, y)
#     break

w = nd.random.normal(scale=0.01, shape=(num_inputs, 1))
b = nd.zeros(shape=(1,))

w.attach_grad()
b.attach_grad()

def linreg(X, w, b):
    return nd.dot(X, w) + b

def squared_loss(y_hat, y):
    return (y_hat - y.reshape(y_hat.shape))**2/2

def sgd(params, lr, batch_size):
    for param in params:
        param[:] = param - lr*param.grad/batch_size

lr = 0.03
num_epochs = 3
net = linreg
iters = data_iter
loss = squared_loss

# for epoch in range(num_epochs):
#
#     for X, y in iters(batch_size, features, labels):
#         with autograd.record():
#             y_hat = net(X, w, b)
#             l = loss(y_hat, y)
#         l.backward()
#         sgd([w, b], lr, batch_size)
#
#     train_l = loss(net(features,w,b),labels)
#     print('epoch %d, loss %.2f'%(epoch+1, train_l.mean().asnumpy()))
#
for epoch in range(num_epochs):  # 训练模型一共需要num_epochs个迭代周期
    # 在每一个迭代周期中，会使用训练数据集中所有样本一次（假设样本数能够被批量大小整除）。X
    # 和y分别是小批量样本的特征和标签
    for X, y in data_iter(batch_size, features, labels):
        with autograd.record():
            l = loss(net(X, w, b), y)  # l是有关小批量X和y的损失
        l.backward()  # 小批量的损失对模型参数求梯度
        sgd([w, b], lr, batch_size)  # 使用小批量随机梯度下降迭代模型参数
    train_l = loss(net(features, w, b), labels)
    print('epoch %d, loss %f' % (epoch + 1, train_l.mean().asnumpy()))

print(true_w, w)
print(true_b, b)
