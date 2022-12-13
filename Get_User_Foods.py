import pymysql

class Get_User_Foods:
    def __init__(self, user_id):
        # 使用者id
        self.user_id = user_id
        self.browse_foods = []
        self.record_foods = []

    # 取得瀏覽紀錄且沒有食用紀錄
    def get_browse_not_record(self):
        sql = 'SELECT restaurant_dish_id FROM `user_browse` Browse \
                WHERE NOT EXISTS( \
                    SELECT restaurant_dish_id FROM `user_record_food` WHERE Browse.restaurant_dish_id = restaurant_dish_id) \
                AND user_id = {}'.format(str(self.user_id))
        cursor.execute(sql)
        result = cursor.fetchall()

        # 對應成分
        self.ingredient("Browse", result)
           
    # 取得食用紀錄
    def get_record_food(self):
        sql = "SELECT restaurant_dish_id FROM `user_record_food` WHERE EXISTS(SELECT user_id FROM `user_record` WHERE user_id = {})".format(str(self.user_id))
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # 對應成分
        self.ingredient("Record", result)

    # 找成分
    def ingredient(self, type, dish_ids):
        for dish_id in dish_ids:
            sql = 'SELECT name FROM `restaurant_dish_ingredients` WHERE restaurant_dish_id = {}'.format(dish_id[0])
            cursor.execute(sql)
            ingredients = cursor.fetchall()

            temp_ingredients = []
            temp_ingredients.append(dish_id[0])
            
            # 找成分
            for item in ingredients:
                temp_ingredients.append(item[0])
            
            if type == 'Browse':
                self.browse_foods.append(temp_ingredients)
            else:
                self.record_foods.append(temp_ingredients)

db = pymysql.connect(host="127.0.0.1", user="sideJR", passwd="08130263", db="at_ease_with_eating")
cursor = db.cursor()