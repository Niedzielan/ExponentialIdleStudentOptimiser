import math
import json

def readJSONinput(js):
    json_string = json.loads(js)
    if "ft" in json_string:
        ft = float(json_string["ft"])
    else:
        ft = None
    if "t" in json_string:
        t = float(json_string["t"])
    else:
        t = None
    if "students" in json_string:
        students = int(json_string["students"])
    else:
        students = None
    if "stars" in json_string:
        stars = float(json_string["stars"])
    else:
        stars = None
    if "AdBonus" in json_string:
        AdBonus = bool(json_string["AdBonus"])
    else:
        AdBonus = True
    if "IgnoreTheories" in json_string:
        IgnoreTheories = bool(json_string["IgnoreTheories"])
    else:
        IgnoreTheories = False
    if "Acceleration" in json_string:
        Acceleration = bool(json_string["Acceleration"])
    else:
        Acceleration = False
    if "AccelerationBonus" in json_string:
        AccelerationBonus = float(json_string["AccelerationBonus"])
    else:
        AccelerationBonus = 2.8538
    if "Highest_Theory_bought" in json_string:
        Highest_Theory_bought = int(json_string["Highest_Theory_bought"])
    else:
        Highest_Theory_bought = 0
    if "Theory_Speed_upgrades" in json_string:
        Theory_Speed_upgrades = int(json_string["Theory_Speed_upgrades"])
    else:
        Theory_Speed_upgrades = 0
    return students, t, ft, stars, Highest_Theory_bought, Theory_Speed_upgrades, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus

def outputJSON(order, total):
    return json.dumps({"order":order, "total":total})

def calcJSON(js):
    students, t, ft, stars, Highest_Theory_bought, Theory_Speed_upgrades, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus = readJSONinput(js)
    order, boosts, total = calc(students, t, ft, stars, Highest_Theory_bought, Theory_Speed_upgrades, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus)
    return outputJSON(order, total)

def getcost(num):
    if num % 2 == 1:
        return (num**2-1)/4 + (num+1)/2
    else:
        return (num**2 + 2*num)/4

def getnextcost(num):
    return getcost(num+1)-getcost(num)

def getcostOrder(order):
    cost = 0
    for i in range(len(order)-1):
        cost += getcost(order[i])
    cost += 2*order[6]
    return cost

def getTotalBoost(order, boosts):
    res = 0
    for i in range(6):
        res += order[i]*boosts[i]
    return (1+order[6]*0.1)*res

def getdt(ft):
    dt_speed_upgrades = ft/15.0/math.log(2,10)
    dt_speed = (dt_speed_upgrades+0.1)/10
    dt_levels = ft/math.log(4,10)
    return dt_speed*dt_levels

def getMaxBuy():
    return [-1, -1, -1, 8, 8, 8, 6]

def getAllForks(order, students, highest, boosts, required = [0]*7):
    maxBuy = getMaxBuy()
    tmp = []
    for i in range(7):
        tmp1 = [x for x in order]
        tmp1[i] = order[i] +1
        if maxBuy[i] > 0:
            tmp1[i] = min(maxBuy[i],tmp1[i] )
        if getTotalBoost(tmp1, boosts) < getTotalBoost(highest, boosts):
            continue        
        tmp2 = [x for x in required]
        tmp2[i] = order[i]+1
        if maxBuy[i] > 0:
            tmp2[i] = min(maxBuy[i],tmp1[i] )
        if getcostOrder(tmp2) > students:
            continue
        if tmp2 not in tmp:
            tmp.append(tmp2)
    return tmp

def getBestTotal(order, boosts, totalStudents, highest = [0]*7):
    remainingStudents = totalStudents - getcostOrder(order)
    best_boost_per_cost = 0
    best_i = -1
    for i in range(len(order)):
        if (i in range(3,6) and order[i] == 8) or (i is 6 and order[i] == 6):
            continue
        boost_per_cost = 0
        cost = 0
        if i == 6:
            boost_per_cost = 0.05*(order[0]*boosts[0] + order[1]*boosts[1] + order[2]*boosts[2] + order[3]*boosts[3] + order[4]*boosts[4] + order[5]*boosts[5])
            cost = 2
        else:
            cost = getnextcost(order[i])
            extra_boost = (1+order[6]*boosts[6])*boosts[i]
            boost_per_cost = extra_boost/cost
        if boost_per_cost > best_boost_per_cost:
            if cost > remainingStudents:
                continue
            best_boost_per_cost = boost_per_cost
            best_i = i
    if best_i != -1:
        order[best_i] += 1
        if getTotalBoost(order, boosts) > getTotalBoost(highest, boosts):
            highest = [x for x in order]
        return order, boosts, totalStudents, highest
    else:
        return order, boosts, 0, highest

def calc(students, t, ft, stars, Highest_Theory_bought = 0, Theory_Speed_upgrades = 0, AdBonus = True, IgnoreTheories = False, Acceleration = False, AccelerationBonus = 2.8538):
    log_10_dmu = ft
    log_10_db = (ft*0.8) - math.log(4*(10**6),10)
    #old dpsi = 2**(ft/25.0-1) -0.5
    log_10_dpsi = (ft/25.0-1)*math.log(2,10)

    dt = getdt(ft)

    if AdBonus:
        dt *= 1.5
    if Acceleration:
        dt *= AccelerationBonus
        
    boosts = (math.log(dt,10), 0.7*math.log(1+t,10), math.log(stars,10), log_10_db/(100*log_10_db)**0.5, log_10_dmu/1300.0, log_10_dpsi/225*(log_10_dpsi**0.5),0.1) #old math.log(1+dpsi,10)/225*(math.log(10+dpsi,10)**0.5)

    order = [0]*7
    cost = 0

    studentCosts = [[20, 5, 5, 5, 5, 5, 5, 5, 20], [10, 10, 10]]
    temp_students = students
    if not IgnoreTheories:
        for i in range(Highest_Theory_bought):
            temp_students -= studentCosts[0][i]
        if Highest_Theory_bought >= 8:
            for j in range(Theory_Speed_upgrades):
                temp_students -= studentCosts[1][j]
        elif Theory_Speed_upgrades > 0:
            print("Theory Speed upgrades will be ignored as Theory 8 has not been bought")
    if temp_students < 0:
        print("Not enough students for given Theories, continuing with IgnoreTheories assumed True")
    else:
        students = temp_students

    temp_students = students
    while temp_students > 0:
        order, boosts, temp_students, highest = getBestTotal(order, boosts, temp_students, order)
    highest = order

    possibles = getAllForks(highest, students, highest, boosts)
    done_possibles = []

    while len(possibles) > 0:
        possible = possibles.pop(0)
        done_possibles.append([x for x in possible])
        order = [x for x in possible]
        total_students = students
        while total_students > 0:
            order, boosts, total_students, highest = getBestTotal(order, boosts, total_students, highest)
        tmp_possibles = getAllForks(order, students, highest, boosts, possible)
        for tmp_possible in tmp_possibles:
            if tmp_possible in possibles or tmp_possible in done_possibles:
                continue
            else:
                possibles.append(tmp_possible)

    order = highest
        
    total = getTotalBoost(order, boosts)
    return order, boosts, total

def printcalc(order,total):
    print("e%f" %(total))
    print(order)
    print("Total students spent: %d" %(getcostOrder(order)))

if __name__ == "__main__":
##    students = 18
##    t = 1.5e9
##    ft = 4995
##    stars = 3000000
    test_dict = {
        "students": 33,
        "t": 1.5e9,
        "ft": 10500,
        "stars": 2400000,
        "Highest_Theory_bought":1
                 }

    test_json = json.dumps(test_dict)
    
    students, t, ft, stars, Highest_Theory_bought, Theory_Speed_upgrades, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus = readJSONinput(test_json)
    
    order, boosts, total = calc(students, t, ft, stars, Highest_Theory_bought, Theory_Speed_upgrades, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus)
    printcalc(order, total)
