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
    return students, t, ft, stars, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus

def outputJSON(order, total):
    return json.dumps({"order":order, "total":total})

def calcJSON(js):
    students, t, ft, stars, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus = readJSONinput(js)
    order, boosts, total = calc(students, t, ft, stars, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus)
    return outputJSON(order, total)

def getcost(num):
    if num % 2 == 1:
        return (num**2-1)/4 + (num+1)/2
    else:
        return (num**2 + 2*num)/4

def getboosts(ft,):
    dt = getdt(ft)
    return (math.log(dt,10), 0.7*math.log(1+t,10), math.log(stars,10), log_10_db/(100*log_10_db)**0.5, log_10_dmu/1300.0, log_10_dpsi/225*(log_10_dpsi**0.5),0.1) #old math.log(1+dpsi,10)/225*(math.log(10+dpsi,10)**0.5)

def getdt(ft):
    dt_speed_upgrades = ft/15.0/math.log(2,10)
    dt_speed = (dt_speed_upgrades+0.1)/10
    dt_levels = ft/math.log(4,10)
    return dt_speed*dt_levels

def getBest(order, boosts, remainingStudents):
    best_boost_per_cost = 0
    best_i = -1
    best_cost  = 0
    for i in range(len(order)):
        if (i in range(3,6) and order[i] == 8) or (i is 6 and order[i] == 6):
            continue
        if i == 6 and remainingStudents >= 2:
            boost_per_cost = 0.05*(order[0]*boosts[0] + order[1]*boosts[1] + order[2]*boosts[2] + order[3]*boosts[3] + order[4]*boosts[4] + order[5]*boosts[5])
            cost = 2
        elif i == 6:
            continue
        else:
            cost = (getcost(order[i]+1)-getcost(order[i]))
            if cost > remainingStudents:
                continue
            extra_boost = (1+order[6]*boosts[6])*boosts[i]
            boost_per_cost = extra_boost/cost
        if boost_per_cost > best_boost_per_cost:
            best_boost_per_cost = boost_per_cost
            best_i = i
            best_cost = cost
    if best_i != -1:
        order[best_i] += 1
        return order, remainingStudents-best_cost
    else:
        return order, 0

def calc(students, t, ft, stars, AdBonus = True, IgnoreTheories = False, Acceleration = False, AccelerationBonus = 2.8538):
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

    if not IgnoreTheories:
        if students >=60:
            students -= 60
        elif students >= 20:
            students -= 20
            while students >= 5:
                students -= 5

    remaining_students = students
    while remaining_students > 0:
        order, remaining_students = getBest(order, boosts, remaining_students)
    total = (1+order[6]*boosts[6])*(order[0]*boosts[0] + order[1]*boosts[1] + order[2]*boosts[2] + order[3]*boosts[3] + order[4]*boosts[4] + order[5]*boosts[5])
    return order, boosts, total

def printcalc(order,total):
    print("e%f" %(total))
    print(order)

if __name__ == "__main__":
##    students = 18
##    t = 1.5e9
##    ft = 4995
##    stars = 3000000
    test_dict = {
        "students": 18,
        "t": 1.5e9,
        "ft": 4995,
        "stars": 3000000
                 }

    test_json = json.dumps(test_dict)
    
    students, t, ft, stars, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus = readJSONinput(test_json)
    
    order, boosts, total = calc(students, t, ft, stars, AdBonus, IgnoreTheories, Acceleration, AccelerationBonus)
    printcalc(order, total)
