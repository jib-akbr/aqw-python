def checkOperator(obj1, obj2, operator: str):
    flag = False
    if operator == ">=":
        flag = obj1 >= obj2
    if operator == ">":
        flag = obj1 > obj2
    if operator == "<=":
        flag = obj1 <= obj2
    if operator == ">":
        flag = obj1 > obj2
    if operator == "<":
        flag = obj1 < obj2
    if operator == "==":
        flag = obj1 == obj2
    if operator == "!=":
        flag = obj1 != obj2
    return flag