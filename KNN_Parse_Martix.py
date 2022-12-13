from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from scipy.stats import pearsonr #匯入Pearsone

class KNN:
    def __init__(self, k, better):
        self.k = k
        self.better = better
        
    def set_data(self, X_train, Y_label):
        self.X_train = X_train
        self.Y_label = Y_label   

    # 使用Pearson計算距離
    def pearson_distance(self, x, y):
        distance = pearsonr(x, y)

        return distance
        
    # 找到最近的K個節點
    def find_K(self, dist):
        def Fun(a):
            return a[1]
        
        index_dist = [[v,k] for v,k in enumerate(dist)]
        new_dist = sorted(index_dist, key=Fun)
        
        res = []
        if len(new_dist) > self.k: # 訓練數據小於K
            for i in range(self.k):
                res.append(new_dist[i][0])
        else:
            for i in new_dist:
                res.append(i[0])
        return res
    
    def predict(self, X_train, X_test):
        label = 0

        for test in X_test:
            dist = []
            # 計算當前節點到所有節點之間的距離
            for k,v in enumerate(X_train):
                dist.append(self.pearson_distance(v, test))
            
            # 找到最近的K個節點
            k_node = self.find_K(dist)
            nnl = []
            
            for i in k_node:
                nnl.append(self.Y_label[i])
                
            nnl.sort() # 排序
            res = [1, nnl[0]]
                        
            # 找到出現最多的類別
            for i in range(1, len(nnl)):
                if nnl[i] == res[1]:
                    res[0] += 1
                else:
                    res[0] -= 1
                    if res[0] <= 0:
                        res[0] = 0
                        res[1] = nnl[i]
            label = res[1]
            
        return label
    # 訓練PCA降維
    def train_PCA(self):        
        pca = PCA(self.better)
        pca.fit(self.X_train)

        # 將X_train降到低維度
        rx_train = pca.transform(self.X_train)

        knn = KNeighborsClassifier(3)
        knn.fit(rx_train, self.Y_label)
        
        return rx_train
                 
    #PCA降維
    def reduce_PCA(self, X_test):
        pca = PCA(self.better)
        pca.fit(self.X_train)

        # 將X_test降到低維度
        rx_test = pca.transform(X_test)
        
        return rx_test
