from skimage import transform
import tflearn
import tensorflow as tf
import cv2


class HWARecognizer:
    def create_net(self):
        net = tflearn.input_data(shape=[None, 784])  # input_layer
        net = tflearn.fully_connected(net, 1024, activation='relu', regularizer='L2', weight_decay=0.001)  # dense1
        net = tflearn.dropout(net, 0.9)  # dropout1
        net = tflearn.fully_connected(net, 512, activation='relu', regularizer='L2', weight_decay=0.001)  # dense2
        net = tflearn.dropout(net, 0.9)  # dropout2
        net = tflearn.fully_connected(net, 128, activation='relu', regularizer='L2', weight_decay=0.001)  # dense3
        net = tflearn.dropout(net, 0.9)  # dropout3
        softmax = tflearn.fully_connected(net, 26, activation='softmax')
        # Regression using SGD with learning rate decay and Top-3 accuracy
        sgd = tflearn.SGD(learning_rate=0.04, lr_decay=0.98, decay_step=1000)
        # top_k = tflearn.metrics.Top_k(3)
        net = tflearn.regression(softmax, optimizer=sgd, metric=tflearn.metrics.Accuracy(), loss='categorical_crossentropy')
        model = tflearn.DNN(net, tensorboard_verbose=0)
        model.load('./app/TK/model/model.tfl')
        return model

    def __init__(self):
        self.model = self.create_net()

    def recognize(self, img):
        img = cv2.GaussianBlur(img, (11, 11), 0)
        img = transform.resize(img, (28, 28))
        img = img[:, :, 0] * 255
        tf.reset_default_graph()
        tflearn.init_graph()
        pred = self.model.predict([img.reshape(784)])
        res_arr = []
        for i, n in enumerate(pred[0]):
            res_arr.append([float(n), chr(i + 65)])
        res_arr.sort()
        res_arr.reverse()
        return res_arr
