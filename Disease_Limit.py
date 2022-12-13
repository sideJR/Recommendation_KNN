import pymysql

class Disease:
    db = pymysql.connect(host="127.0.0.1", user="sideJR", passwd="08130263", db="at_ease_with_eating")
    global cursor
    cursor = db.cursor()
    # 將禁忌飲食刪除
    def disease_limit(disease, all_recommend_food):        
        sql = 'SELECT DISTINCT dish_id FROM `indicators_ingredients` WHERE disease_id LIKE "{}" AND category NOT LIKE "%忌%"'.format(str(disease))
        cursor.execute(sql)
        temp_can_eat_foods = cursor.fetchall()

        # 轉換成陣列
        can_eat_foods = []
        for item in temp_can_eat_foods:
            can_eat_foods.append(item[0])

        print("can_eat_foods：", can_eat_foods)

        # 找出交集的飲食
        intersection = set(can_eat_foods).intersection(set(all_recommend_food))
        
        return intersection

    

    # # 腎臟病(ckd)
    # def ckd_limit():
    #     print("ckd")

    # # 心血管疾病(cvd)
    # def cvd_limit(all_recommend_food):
        
        
    #     dish_ids = cursor.fetchall()
    #     print('cvd')
    
    # # 糖尿病(dm)
    # def dm_limit():
    #     print('dm')
    
    # # 高血壓(htn)
    # def htn_limit():
    #     print('htn')
    
    # # 痛風(ma)
    # def ma_limit():
    #     print('ma')
