from data import initial_fish
from collections import Counter

cc = Counter(initial_fish)

n_days = 256

for day in range(n_days):
    tmp = {k: int(0) for k in range(9)}
    for k, v in cc.items():
        if k == 0:
            tmp[6] += v
            tmp[8] += v
        else:
            tmp[k-1] += v
    cc = tmp
    print(f"day: {day + 1}: {sum(cc.values())}")




# too much memory!!
#for j in range(256):
#    for i in range(len(initial_fish)):
#        initial_fish[i] -= 1
#        if initial_fish[i] < 0:
#            initial_fish[i] = 6
#            initial_fish.append(8)
#    print(f"day: {j+1}, len: {len(initial_fish)}")


# way too much memory!!
#class LanternFish(object):
#    def __init__(self, timer: int):
#        self.timer_start = 6
#        self.timer = timer
#        self.birth_timer = 8
#
#    def advance(self) -> object:
#        self.timer -= 1
#        if self.timer == -1:
#            self.timer = self.timer_start
#            return LanternFish(8)
#        else:
#            return None
#
#
#
#fish = [LanternFish(int(x)) for x in initial_fish.split(",")]
#for i in range(256):
#    babies = []
#    for f in fish:
#        newfish = f.advance()
#        if newfish is not None:
#            babies.append(newfish)
#    fish = fish + babies
#    #print(f"{i+1} days: {[x.timer for x in fish]}")
#    print(f"{i+1} days: {len(fish)}")
