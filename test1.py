
def test_dict():
    print("Testing dictionaries")

    me = {
        "first_name": "Gibrahn",
        "last_name": "Duarte",
        "age": 25,
        "address":  {
            "num": 1,
            "street": "Silver Street",
            "city": "Gotham"
    }
    }

    # print full name 
    print(me["first_name"] + " " + me["last_name"])

    #modify
    me["age"] = me["age"] + 1
    print(me["age"])

    #add new keys
    me["color"] = "Dark gray"
    print (me["color"])

    #print the address
    print(me["address"])

    # street numb and city
    address = me["address"] 
    print(address["street"] + " #" + str(address["num"]) + " ," + address["city"])

    print (f"{address['street']}, #{address['num']}, {address['city']}")

    # last, first
    print (f"{me['last_name']}, #{me['first_name']}")

    #hi my name is _____ ______, and I'm _____ years old 
    print(f"hi my name is {me['first_name']} {me['last_name']}, and I'm {me['age']} years old.")

    #red a key that doesn't exist
    try:
        print(me['xyz'])
    except:
        print("Unexpected error")

    print(me)


test_dict()