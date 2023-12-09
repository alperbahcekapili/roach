import test

obj=test.OPENAIController()
mylist=[{"role": "system", "content": "You are a car assistant system."},
        {"role": "user", "content": "The driver is about to sleep. Talk with him to keep him awake"}]


while True:
    resp=obj.generateSuggestions(mylist)
    print(resp.content)
    mylist.append(resp)
    driver_resp=input("Speak:")
    driver_resp={"role":"user","content":driver_resp}
    mylist.append(driver_resp)
    