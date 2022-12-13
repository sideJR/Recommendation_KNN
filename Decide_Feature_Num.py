import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn import metrics

class Feature_Num:
    def __init__(self) -> None:
        self.accTrain = []
        self.accTest = []

    # 找出最好的特徵數
    def get_better_num(self, accTrain):
        better_num = 0
        max = 0.0

        for i in range(len(accTrain)):
            if(round(accTrain[i],2) >= max):
                max = accTrain[i]
                better_num = i+1
        
        return better_num

    # 畫圖
    def draw(self, accTrain, accTest):       
        plt.plot(range(1, parse+1), accTrain, marker='o', label='Train')
        plt.plot(range(1, parse+1), accTest, marker='o', label='Test')
        plt.legend()
        plt.xlabel('Number of features')
        plt.ylabel('Accurarcy')

        plt.show()

    # 載入資料
    def loding_data(self, X, Y):        
        # random_state:亂數種子，設定常數能夠保證每次PCA結果都一樣
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3, random_state=42)

        pca = PCA()
        pca.fit(X_train)
        rx_train = pca.transform(X_train)
        rx_test = pca.transform(X_test)

        global parse
        parse = rx_train.shape
        parse = parse[1]

        for i in range(parse):
            pca = PCA(i+1)
            # 訓練PCA
            pca.fit(X_train)
                
            # 將X_train、X_test降到低維度
            rx_train = pca.transform(X_train)
            rx_test = pca.transform(X_test)
                
            knn = KNeighborsClassifier(3)
            knn.fit(rx_train, Y_train)
                
            y_pred_train = knn.predict(rx_train) 
            # 預測train
            self.accTrain.append(metrics.accuracy_score(Y_train, y_pred_train))
                    
            y_pred_test = knn.predict(rx_test) 
            # 預測test
            self.accTest.append(metrics.accuracy_score(Y_test, y_pred_test))

        better = self.get_better_num(self.accTrain)

        self.draw(self.accTrain, self.accTest)

        return better