import threading



class CAR:
    
    def __init__(self) -> None:
        self.states = [{"volume":0},{"temp":28}]
    def play_music(self):
        
        def increase():
            for i in range(100):
                self.states[0]["volume"] = self. states[0]["volume"] + 1
       

        t1 = threading.Thread(target=increase)
        t1.start()

        return {"Success":True}

    def air_conditioner(self):

        def decrease():
            for i in range(self.states[1]["temp"] - 18):
                self.states[1]["temp"] = self. states[1]["temp"] - 1
        
        t2 = threading.Thread(target=decrease)
        t2.start()

        return {"Success":True}


    def all_states(self):
        return self.states