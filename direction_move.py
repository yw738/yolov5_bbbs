import time

from directkeys import key_down, key_up,key_down,key_up

#               上： i        下：  k        左：  l       右：    j
# direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}
direct_dic = {"UP": 'I', "DOWN": 'K', "LEFT": 'L', "RIGHT": 'J'}
#         方向                                       按下延时         抬起延时
def move(direct, material=False, action_cache=None, press_delay=0.1, release_delay=0.1):
    if direct == "RIGHT":
        right = direct_dic["RIGHT"]
        if action_cache != None:
            if action_cache != "RIGHT":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    key_down(right)
                else:
                    key_down(right)
                key_up(right)
                if not material:
                    time.sleep(press_delay)
                    key_down(right)
                    time.sleep(release_delay)
                    key_up(right)
                action_cache = "RIGHT"
                print("向右移动",right)
            else:
                print("向右移动",right)
        else:
            key_up(right)
            if not material:
                time.sleep(press_delay)
                key_down(right)
                time.sleep(release_delay)
                key_up(right)
            action_cache = "RIGHT"
            print("向右移动")
        return action_cache

    elif direct == "LEFT":
        left = direct_dic["LEFT"]
        if action_cache != None:
            if action_cache != "LEFT":
                key_down(left)
                key_up(left)
                if not material:
                    time.sleep(press_delay)
                    key_up(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    key_down(direct_dic["LEFT"])
                action_cache = "LEFT"
                print("向左移动")
            else:
                print("向左移动")
        else:
            key_down(direct_dic["LEFT"])
            if not material:
                time.sleep(press_delay)
                key_up(direct_dic["LEFT"])
                time.sleep(release_delay)
                key_down(direct_dic["LEFT"])
            action_cache = "LEFT"
            print("向左移动")
        return action_cache

    elif direct == "UP":
        if action_cache != None:
            if action_cache != "UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    key_up(direct_dic["UP"])
                else:
                    key_up(direct_dic[action_cache])
                key_down(direct_dic["UP"])
               
                action_cache = "UP"
                print("向上移动")
            else:
                print("向上移动")
        else:
            key_down(direct_dic["UP"])
           
            action_cache = "UP"
            print("向上移动")
        return action_cache

    elif direct == "DOWN":
        if action_cache != None:
            if action_cache != "DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    key_up(direct_dic["DOWN"])
                else:
                    key_up(direct_dic[action_cache])
                key_down(direct_dic["DOWN"])
             
                action_cache = "DOWN"
                print("向下移动")
            else:
                print("向下移动")
        else:
            key_down(direct_dic["DOWN"])
          
            action_cache = "DOWN"
            print("向下移动")
        return action_cache


if __name__ == "__main__":
    action_cache = None
    t1 = time.time()
    # while True:
        # if  int(time.time() - t1) % 2 == 0:
        #     action_cache = move("LEFT_DOWN", material=False, action_cache=action_cache, press_delay=0.1, release_delay=0.1)
        # else:
    action_cache = move("RIGHT_UP", material=True, action_cache=action_cache, press_delay=0.1, release_delay=0.1)