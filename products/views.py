from django.shortcuts import render
from .models import *
import json

def index(request):

    category_products = Categories.catmanger.get_all_products()
    addtion_categories = AdditionCategories.addi_catmanger.get_all_additions()
    context = {'category_products': category_products, 'addtion_categories': json.dumps(addtion_categories)}
    return render(request, 'products/index.html', context=context)

    category_products = [
        {
            "id": "c01",
            "name": "蛋餅",
            "products": [
            {
                "id": "p012",
                "name": "玉米蛋餅",
                "catId": "c01",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p012.jpg",
                "comment": "手工蛋餅皮+滿滿玉米",
                "isSoldOut": False,
                "price": 30,
                "additionIds": [
                "AH01"
                ]
            },
            {
                "id": "p013",
                "catId": "c01",
                "name": "培根蛋餅",
                "price": 35,
                "comment": "手工蛋餅皮+雙份培根",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p013.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p014",
                "catId": "c01",
                "name": "火腿蛋餅",
                "price": 35,
                "comment": "手工蛋餅皮+整條火腿",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p014.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p015",
                "catId": "c01",
                "name": "鮪魚沙拉蛋餅",
                "price": 35,
                "comment": "手工蛋餅皮+一整罐鮪魚",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p015.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p016",
                "catId": "c01",
                "name": "起司蛋餅",
                "price": 35,
                "comment": "手工蛋餅皮+爆漿起司",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p016.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            }
            ]
        },
        {
            "id": "c02",
            "name": "吐司",
            "products": [
            {
                "id": "p021",
                "catId": "c02",
                "name": "果醬吐司",
                "price": 15,
                "comment": "切邊烤土司+一公分厚塗果醬",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p021.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p022",
                "catId": "c02",
                "name": "鮪魚沙拉吐司",
                "price": 35,
                "comment": "切邊烤土司+一整罐鮪魚",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p022.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p023",
                "catId": "c02",
                "name": "培根吐司",
                "price": 35,
                "comment": "切邊烤土司+雙份培根",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p023.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p024",
                "catId": "c02",
                "name": "里肌豬排吐司",
                "price": 35,
                "comment": "切邊烤土司+厚切里肌豬排",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p024.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            }
            ]
        },
        {
            "id": "c03",
            "name": "漢堡",
            "products": [
            {
                "id": "p031",
                "catId": "c03",
                "name": "紐澳良豬排堡",
                "price": 55,
                "comment": "就是豬排加生菜的漢堡啦",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p031.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p032",
                "catId": "c03",
                "name": "美味蟹堡",
                "price": 45,
                "comment": "是誰住在深海的大鳳梨裡",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p032.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p033",
                "catId": "c03",
                "name": "阿拉斯加鱈魚堡",
                "price": 45,
                "comment": "鱈~魚~堡~",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p033.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p034",
                "catId": "c03",
                "name": "日式和牛堡",
                "price": 100,
                "comment": "日本來的和牛，頂級享受",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p034.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            },
            {
                "id": "p035",
                "catId": "c03",
                "name": "薯泥堡",
                "price": 40,
                "comment": "內含薯泥沙拉，美味蔬食",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p035.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": True
            },
            {
                "id": "p036",
                "catId": "c03",
                "name": "無骨雞腿堡",
                "price": 55,
                "comment": "精選黃金右腿去骨雞腿排",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p036.jpg",
                "additionIds": [
                "AH01"
                ],
                "isSoldOut": False
            }
            ]
        },
        {
            "id": "c04",
            "name": "沙拉",
            "products": [
            {
                "id": "p041",
                "catId": "c04",
                "name": "經典美味沙拉",
                "price": 55,
                "comment": "全素草食餐",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p041.jpg",
                "additionIds": [
                "AH01",
                "AH04"
                ],
                "isSoldOut": False
            },
            {
                "id": "p042",
                "catId": "c04",
                "name": "低脂蛋白沙拉",
                "price": 55,
                "comment": "很多葉子搭配水煮蛋、舒肥雞胸肉",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p042.jpg",
                "additionIds": [
                "AH01",
                "AH04"
                ],
                "isSoldOut": False
            }
            ]
        },
        {
            "id": "c05",
            "name": "點心",
            "products": [
            {
                "id": "p051",
                "name": "歡樂薯餅",
                "catId": "c05",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p051.jpg",
                "comment": "薯餅薯餅得第一",
                "isSoldOut": False,
                "price": 10,
                "additionIds": [
                "AH01",
                "AH04"
                ]
            },
            {
                "id": "p052",
                "catId": "c05",
                "name": "雞塊",
                "price": 30,
                "comment": "一份4塊",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p052.jpg",
                "additionIds": [
                "AH04"
                ],
                "isSoldOut": False
            },
            {
                "id": "p053",
                "catId": "c05",
                "name": "薯條",
                "price": 30,
                "comment": "酥脆薯條，素食可用",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p053.jpg",
                "additionIds": [
                "AH04"
                ],
                "isSoldOut": False
            },
            {
                "id": "p054",
                "catId": "c05",
                "name": "熱狗",
                "price": 30,
                "comment": "國產熱狗",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p054.jpg",
                "additionIds": [
                "AH04"
                ],
                "isSoldOut": False
            },
            {
                "id": "p055",
                "catId": "c05",
                "name": "月亮蝦餅",
                "price": 30,
                "comment": "泰式月亮蝦餅搭配泰式酸辣醬",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p055.jpg",
                "additionIds": [
                "AH04"
                ],
                "isSoldOut": False
            }
            ]
        },
        {
            "id": "c06",
            "name": "飲品",
            "products": [
            {
                "id": "p061",
                "catId": "c06",
                "name": "早餐店奶茶",
                "price": 15,
                "comment": "台灣特色，早餐店奶茶",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p061.jpg",
                "additionIds": [
                "AH02",
                "AH03"
                ],
                "isSoldOut": False
            },
            {
                "id": "p062",
                "catId": "c06",
                "name": "經典紅茶",
                "price": 15,
                "comment": "台灣高山茶葉沖泡",
                "img": "https://raw.githubusercontent.com/ColdingPoTaTo/resCollection/main/breakfast/menu/p062.jpg",
                "additionIds": [
                "AH02",
                "AH03"
                ],
                "isSoldOut": False
            }
            ]
        }
    ]

    return render(request, 'products/index.html', {'category_products': category_products})
