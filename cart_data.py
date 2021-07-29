from DataBase import *

dict_shop, dict_cart = {}, {}
for row in get_what_we_have():
    arr_data = list(row.split())
    count = int(arr_data[-1])
    arr_data.pop()
    obj = " ".join(arr_data)
    dict_shop[obj] = int(count)


def get_used(item):
    return dict_cart(item, 0)


def show_items_now(type):
    list_of_items = get_items_list(type)
    result = "We have: "
    for obj in list_of_items:
        name_of_obj = ' '.join(obj)
        cnt = dict_shop.get(name_of_obj, 0) - dict_cart.get(name_of_obj, 0)
        if cnt > 0:
            result = result + "\n" + name_of_obj + " for price: " + str(
                get_price_for(name_of_obj)) + " in shop we have: " + str(cnt)
    return result


def modify_cart(item, number):
    if number < 0:
        number = min(-number, get_used(item))
        dict_cart[item] = dict_cart[item] - number if item in dict_cart else 0
        return "We succesfully removed " + str(number) + " of " + item + " from your cart"

    if dict_shop.get(item, 0) >= dict_cart.get(item, 0) + number:
        dict_cart[item] = dict_cart[item] + number if item in dict_cart else number
        return "We succesfully added " + str(number) + " of " + item + " to your cart"
    number = dict_shop.get(item, 0) - dict_cart.get(item, 0)
    dict_cart[item] = dict_cart[item] + number if item in dict_cart else number
    return "Sorry we have only " + str(number) + " of " + item + " but still we added everything we have to your cart"


def current_cart():
    return dict_cart.items()
