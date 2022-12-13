import pymysql
from Get_User_Foods import Get_User_Foods
from Decide_Feature_Num import Feature_Num
from KNN_Parse_Martix import KNN
from Disease_Limit import Disease

# 取得使用者瀏覽、食用紀錄
def user_foods(user_id):
    global user
    user = Get_User_Foods(user_id)
    user.get_browse_not_record()
    user.get_record_food()

# 顯示推薦飲食名稱
def show_name(all_recommend_food):
    for item in all_recommend_food:
        sql = 'SELECT name FROM `restaurant_dish` WHERE id = {}'.format(str(item))
        cursor.execute(sql)
        name = cursor.fetchall()

# 將瀏覽、食用紀錄轉換為訓練資料
def train_data():
    global data
    data = Feature_Num()
    
    sql = 'SELECT DISTINCT name FROM `restaurant_dish_ingredients`'
    cursor.execute(sql)
    result = cursor.fetchall()

    # 所有食材(features)
    global all_ingredient
    all_ingredient = []

    for item in result:
        all_ingredient.append(item[0])

    # 放置轉換成one-hot的資料
    global x_train
    x_train = []
    # 分類瀏覽(0)、食用(1)兩類
    global label
    label = []
   
    # 轉換成one-hot
    # 瀏覽
    for item in user.browse_foods:
        train = [0] * len(all_ingredient)
        for i in range(1, len(item)):
            for ingredient in all_ingredient:
                if item[i] in ingredient:
                    train[all_ingredient.index(item[i])] = 1
        x_train.append(train)
        label.append(0)
    # 食用
    for item in user.record_foods:
        train = [0] * len(all_ingredient)
        for i in range(1, len(item)):
            for ingredient in all_ingredient:
                if item[i] in ingredient:
                    train[all_ingredient.index(item[i])] = 1
        x_train.append(train)
        label.append(1)
   
    better = data.loding_data(x_train, label)

    return better

# 預測飲食喜好
def predict_food(user_id):
    knn = KNN(3, better)
    knn.set_data(x_train, label)
    
    # sql = 'SELECT id FROM `restaurant_dish`'
    sql = '''
        SELECT DISTINCT restaurant_dish.id
        FROM `restaurant_dish` 
        RIGHT JOIN `restaurant_dish_ingredients`
        ON `restaurant_dish`.`id` = `restaurant_dish_ingredients`.`restaurant_dish_id`
        WHERE restaurant_dish_ingredients.name NOT LIKE '%null%'
    '''
    cursor.execute(sql)
    # 資料庫中所有飲食
    all_dish_ids = cursor.fetchall()
    # 所有飲食預測結果
    all_recommend_food = []

    # 對每一個飲食成分轉換成one-hot
    for dish_id in all_dish_ids:
        all = []
        # 設一個結束
        # if dish_id[0] > 30:
        #     break
        print("id=>",dish_id[0])
        sql = 'SELECT name FROM `restaurant_dish_ingredients` WHERE restaurant_dish_id = {}'.format(dish_id[0])
        cursor.execute(sql)
        ingredients = cursor.fetchall()

        temp_ingredients = []
        temp_ingredients.append(dish_id[0])

        # 找成分
        for item in ingredients:
            temp_ingredients.append(item[0])
        
        predict_food = []
        rx_new = [0] * len(all_ingredient)
        
        # 轉換成one-hot
        for ingredient in temp_ingredients:
            if ingredient in all_ingredient:
                rx_new[all_ingredient.index(ingredient)] = 1
        
        predict_food.append(rx_new)
        
        # 原資料降維
        rx_train = knn.train_PCA()
        # 預測飲食降維
        rx_new = knn.reduce_PCA(predict_food)                        
        # 預測飲食
        predict = knn.predict(rx_train, rx_new)

        # 將推薦飲食放進all_recommend_food裡
        if predict == 1:            
            all.append(dish_id[0])
            # all.append(predict)        
            all_recommend_food.append(all[0])
    print("可能喜好飲食：", all_recommend_food)
    # 加入疾病限制
    # disease_limit(user_id, all_recommend_food)

# 加入疾病限制
def disease_limit(user_id, all_recommend_food):

    sql = 'SELECT disease_id FROM `user_disease` WHERE user_id={}'.format(user_id)
    cursor.execute(sql)
    diseases = cursor.fetchall()
    print('diseases =>', diseases)

    for disease in diseases:
        # 列出user疾病
        disease = str(diseases[0][0])

        # 回傳刪除疾病限制(禁忌)飲食
        all_recommend_food = list(Disease.disease_limit(disease, all_recommend_food))

        print("intersection_eat", all_recommend_food)
        print("\nlen：", len(all_recommend_food))

        # all_recommend_food = indicators_nutrients_day_limit(disease, all_recommend_food)

        # # 腎臟病(ckd)
        # if disease == 'ckd':
        #     Disease.ckd_limit()
        # # 心血管疾病(cvd)
        # elif disease == 'cvd':
        #     Disease.cvd_limit(all_recommend_food)
        # # 糖尿病(dm)
        # elif disease == 'dm':
        #     Disease.dm_limit()
        # # 高血壓(htn)
        # elif disease == 'htn':
        #     Disease.htn_limit()
        # # 痛風(ma)
        # elif disease == 'ma':
        #     Disease.ma_limit()
        # else:
        #     print('沒有疾病')    

    # for i in range(0, 5):
    #     print(all_recommend_food[i])
        
# 將一日營養限制放入排序
def indicators_nutrients_day_limit(disease, all_recommend_food):  
    sql = 'SELECT * FROM `user_indicators_nutrients_day_limit`'
    cursor.execute(sql)
    day_limit = cursor.fetchall()

    # 營養素
    saturated_fat = day_limit[0][3] # 飽和脂肪
    trans_fat = day_limit[0][4] # 反式脂肪
    carbohydrate = day_limit[0][6]  # 碳水化合物
    cholesterol = day_limit[0][7]   # 膽固醇
    sodium = day_limit[0][8]    # 鈉
    dietary_fiber = day_limit[0][10] # 膳食纖維(目前不需要)
    fat = day_limit[0][12]   # 脂肪
    sugar = day_limit[0][13]    # 糖
    protein = day_limit[0][15]   # 蛋白質

    important_nurtrients = []

    # 所有飲食營養排序
    all_foods_nurtrient_limit = []

    # 心血管疾病(cvd)
    if(disease == 'cvd'):
        # 對應nurtrient_limit index
        important_nurtrients = [9, 8, 3, 2]
        # 將所有推薦飲食營養放入all_foods_nurtrient_limit
        for dish_id in all_recommend_food:
            sql = 'SELECT * FROM `restaurant_dish` WHERE id={}'.format(str(dish_id))
            cursor.execute(sql)
            temp_nurtrient_limit = cursor.fetchall()
            # 前兩個id、restaurant_dish
            # 單一飲食營養
            limit = [temp_nurtrient_limit[0][0], temp_nurtrient_limit[0][1], \
                    temp_nurtrient_limit[0][15], temp_nurtrient_limit[0][16], temp_nurtrient_limit[0][11], \
                    temp_nurtrient_limit[0][18], temp_nurtrient_limit[0][13], temp_nurtrient_limit[0][12], \
                    temp_nurtrient_limit[0][14], temp_nurtrient_limit[0][10]]
            # 放進全部之中
            all_foods_nurtrient_limit.append(limit)

    print("before ：", all_foods_nurtrient_limit)

    # 依照important_nurtrients排序
    # 目前只有依據糖排序
    all_foods_nurtrient_limit.sort(key = lambda s: s[important_nurtrients[0]]) 

    print("\npre ：", all_foods_nurtrient_limit)

db = pymysql.connect(host="127.0.0.1", user="sideJR", passwd="08130263", db="at_ease_with_eating")
cursor = db.cursor()

user_id = 2
# 取得使用者食用、瀏覽紀錄
user_foods(user_id)
better = train_data()

# 預測飲食
predict_food(user_id)