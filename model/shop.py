class Shop:
    def __init__(self, json_data):
        items = []
        for shop_item in json_data['items']:
            items.append(ShopItem(shop_item))
        self.shop_id = json_data['ShopID']
        self.shop_name = json_data['sName']
        self.items = items
        self.is_member = json_data['bUpgrd'] == "1"
        
    def get_item(self, item_name: str):
        for item in self.items:
            if item.item_name == item_name:
                return item
        return None

class ShopItem:
    def __init__(self, json_data):
        self.item_id = json_data['ItemID']
        self.shop_item_id = json_data['ShopItemID']
        self.item_name = json_data['sName']
        self.cost = json_data['iCost']
        self.is_acs = json_data['bCoins'] == "1"