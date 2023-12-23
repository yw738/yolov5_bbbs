import random
import time

import directkeys
from direction_move import move
from directkeys import ReleaseKey



def filteLabel(x):
    return x["label"]

def filterName(x):
    return x["label"]

def filterXywh(x):
    return x["xywh"]

def filterUser(arr):
    """
    查询 角色的坐标
    """
    for i,v in enumerate(arr):
        if(v['label']=='user'):
            return v['xywh']
        else:
            continue



# 主进程 
def init(cls_arr):
    """
    检测主程序
    """
    # 设置所有用到的参数
    window_size = (0, 0, 1280, 800)  # 截屏的位置
    img_size = 640  # 输入到yolo5中的模型尺寸
    paused = False
    view_img = True  # 是否观看目标检测结果
    save_txt = False
    conf_thres = 0.3  # NMS的置信度过滤
    iou_thres = 0.2  # NMS的IOU阈值
    classes = None
    agnostic_nms = False  # 不同类别的NMS时也参数过滤
    skill_char = "XYHGXFAXDSWXETX"  # 技能按键，使用均匀分布随机抽取
    direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}  # 上下左右的键码
    names = ['user', 'small_map', "monster", 'money', 'material', 'door', 'BOSS', 'box', 'options']  # 所有类别名
    action_cache = None  # 动作标记
    press_delay = 0.1  # 按压时间
    release_delay = 0.1  # 释放时间
    frame = 0  # 帧
    door1_time_start = -20
    next_door_time = -20
    fs = 1  # 每四帧处理一次

    # 游戏
    thx = 30  # 捡东西时，x方向的阈值
    thy = 30  # 捡东西时，y方向的阈值
    attx = 150  # 攻击时，x方向的阈值
    atty = 50  # 攻击时，y方向的阈值
    cls_object = list(map(filterName,cls_arr))
    img_object = (map(filterXywh,cls_arr))
    # directkeys.key_press("A")
    move(direct="RIGHT",release_delay=0.5)
    # move(direct="LEFT",release_delay=0.5)
    # directkeys.key_press("L")
    return
    # 扫描英雄
    if "user" in cls_object:
        # hero_xywh = img_object[cls_object.index("user")]
        hero_xywh = filterUser(cls_arr)
    # for idx, (c, box) in enumerate(cls_arr):
    #    print(idx)
    # 打怪
    if "monster" in cls_object or "BOSS" in cls_object:
        min_distance = float("inf")
        for idx, (c, box) in enumerate(zip(cls_object, img_object)):
            # 找到怪了
            if c == 'monster' or c == "BOSS":
                dis = ((hero_xywh[0] - box[0]) ** 2 + (hero_xywh[1] - box[1]) ** 2) ** 0.5
                if dis < min_distance:
                    monster_box = box
                    monster_index = idx
                    min_distance = dis
        # 处于攻击距离8
        if abs(hero_xywh[0] - monster_box[0]) < attx and abs(hero_xywh[1] - monster_box[1]) < atty:
            directkeys.key_press("A")
            # if "BOSS" in cls_object:
            #     directkeys.key_press("A")
            #
            #     skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
            #     while True:
            #         if skill_rec(skill_name, img0):
            #             directkeys.key_press(skill_name)
            #             directkeys.key_press(skill_name)
            #             directkeys.key_press(skill_name)
            #             break
            #         else:
            #             skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
            # else:
            #     skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
            #     while True:
            #         if skill_rec(skill_name, img0):
            #             directkeys.key_press(skill_name)
            #             directkeys.key_press(skill_name)
            #             directkeys.key_press(skill_name)
            #             break
            #         else:
            #             skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
            print("释放技能攻击")
            if not action_cache:
                pass
            elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                action_cache = None
            elif action_cache:
                ReleaseKey(direct_dic[action_cache])
                action_cache = None
            # break
        # 怪物在英雄右上  ， 左上     左下   右下
        elif monster_box[1] - hero_xywh[1] < 0 and monster_box[0] - hero_xywh[0] > 0:
            # y方向 小于攻击距离
            if abs(monster_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            #
            elif hero_xywh[1] - monster_box[1] < monster_box[0] - hero_xywh[0]:
                action_cache = move(direct="RIGHT_UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - monster_box[1] >= monster_box[0] - hero_xywh[0]:
                action_cache = move(direct="UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
            # break
        elif monster_box[1] - hero_xywh[1] < 0 and monster_box[0] - hero_xywh[0] < 0:
            if abs(monster_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - monster_box[1] < hero_xywh[0] - monster_box[0]:
                action_cache = move(direct="LEFT_UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - monster_box[1] >= hero_xywh[0] - monster_box[0]:
                action_cache = move(direct="UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        elif monster_box[1] - hero_xywh[1] > 0 and monster_box[0] - hero_xywh[0] < 0:
            if abs(monster_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif monster_box[1] - hero_xywh[1] < hero_xywh[0] - monster_box[0]:
                action_cache = move(direct="LEFT_DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif monster_box[1] - hero_xywh[1] >= hero_xywh[0] - monster_box[0]:
                action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        elif monster_box[1] - hero_xywh[1] > 0 and monster_box[0] - hero_xywh[0] > 0:
            if abs(monster_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif monster_box[1] - hero_xywh[1] < monster_box[0] - hero_xywh[0]:
                action_cache = move(direct="RIGHT_DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif monster_box[1] - hero_xywh[1] >= monster_box[0] - hero_xywh[0]:
                action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
    # 移动到下一个地图
    # "material" not in cls_object and 布料 
    if "door" in cls_object and "monster" not in cls_object and "BOSS" not in cls_object and  "money" not in cls_object:
        for idx, (c, box) in enumerate(zip(cls_object, img_object)):
            if c == 'door':
                door_box = box
                door_index = idx8
        # 门的位置小于抓取的一半，在左侧
        # if door_box[0] < img0.shape[0] // 2:
        if door_box[0]:
            action_cache = move(direct="RIGHT", action_cache=action_cache, press_delay=press_delay,
                                release_delay=release_delay)
            # break
        # 门在右下方
        elif door_box[1] - hero_xywh[1] < 0 and door_box[0] - hero_xywh[0] > 0:
            if abs(door_box[1] - hero_xywh[1]) < thy and abs(door_box[0] - hero_xywh[0]) < thx:
                action_cache = None
                print("进入下一地图")
                # break
            elif abs(door_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="RIGHT", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - door_box[1] < door_box[0] - hero_xywh[0]:
                action_cache = move(direct="RIGHT_UP", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - door_box[1] >= door_box[0] - hero_xywh[0]:
                action_cache = move(direct="UP", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        # 门在右上方
        elif door_box[1] - hero_xywh[1] < 0 and door_box[0] - hero_xywh[0] < 0:
            if abs(door_box[1] - hero_xywh[1]) < thy and abs(door_box[0] - hero_xywh[0]) < thx:
                action_cache = None
                print("进入下一地图")
                # break
            elif abs(door_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="LEFT", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - door_box[1] < hero_xywh[0] - door_box[0]:
                action_cache = move(direct="LEFT_UP", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - door_box[1] >= hero_xywh[0] - door_box[0]:
                action_cache = move(direct="UP", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        # 门在左下方
        elif door_box[1] - hero_xywh[1] > 0 and door_box[0] - hero_xywh[0] < 0:
            if abs(door_box[1] - hero_xywh[1]) < thy and abs(door_box[0] - hero_xywh[0]) < thx:
                action_cache = None
                print("进入下一地图")
                # break
            elif abs(door_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="LEFT", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif door_box[1] - hero_xywh[1] < hero_xywh[0] - door_box[0]:
                action_cache = move(direct="LEFT_DOWN", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif door_box[1] - hero_xywh[1] >= hero_xywh[0] - door_box[0]:
                action_cache = move(direct="DOWN", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        # 门在左上方
        elif door_box[1] - hero_xywh[1] > 0 and door_box[0] - hero_xywh[0] > 0:
            if abs(door_box[1] - hero_xywh[1]) < thy and abs(door_box[0] - hero_xywh[0]) < thx:
                action_cache = None
                print("进入下一地图")
                # break
            elif abs(door_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="RIGHT", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif door_box[1] - hero_xywh[1] < door_box[0] - hero_xywh[0]:
                action_cache = move(direct="RIGHT_DOWN", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif door_box[1] - hero_xywh[1] >= door_box[0] - hero_xywh[0]:
                action_cache = move(direct="DOWN", action_cache=action_cache, press_delay=press_delay,
                                    release_delay=release_delay)
                # break
    
    if "money" not in cls_object and "material" not in cls_object and "monster" not in cls_object \
            and "BOSS" not in cls_object and "door" not in cls_object and 'box' not in cls_object \
            and 'options' not in cls_object:
        # if next_door(img0) == 0 and abs(time.time()) - next_door_time > 10:
        #     next_door_time = time.time()
        #     action_cache = move(direct="LEFT", action_cache=action_cache, press_delay=press_delay,
        #                         release_delay=release_delay)
        #     # time.sleep(3)
        # else:
        #     action_cache = move(direct="RIGHT", action_cache=action_cache, press_delay=press_delay,
        #                     release_delay=release_delay)

        #没有识别到 则向右走
        action_cache = move(direct="RIGHT", action_cache=action_cache, press_delay=press_delay,
                            release_delay=release_delay)
        # break

    # 捡材料
    if "monster" not in cls_object and "user" in cls_object and (
            "material" in cls_object or "money" in cls_object):
        min_distance = float("inf")
        hero_xywh[1] = hero_xywh[1] + (hero_xywh[3] // 2) * 0.7
        thx = thx / 2
        thy = thy / 2
        for idx, (c, box) in enumerate(zip(cls_object, img_object)):
            if c == 'material' or c == "money":
                dis = ((hero_xywh[0] - box[0]) ** 2 + (hero_xywh[1] - box[1]) ** 2) ** 0.5
                if dis < min_distance:
                    material_box = box
                    material_index = idx
                    min_distance = dis
        if abs(material_box[1] - hero_xywh[1]) < thy and abs(material_box[0] - hero_xywh[0]) < thx:
            if not action_cache:
                pass
            elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                action_cache = None
            else:
                ReleaseKey(direct_dic[action_cache])
                action_cache = None
            time.sleep(1)
            directkeys.key_press("X")
            print("捡东西")
            # break

        elif material_box[1] - hero_xywh[1] < 0 and material_box[0] - hero_xywh[0] > 0:

            if abs(material_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - material_box[1] < material_box[0] - hero_xywh[0]:
                action_cache = move(direct="RIGHT_UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - material_box[1] >= material_box[0] - hero_xywh[0]:
                action_cache = move(direct="UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        elif material_box[1] - hero_xywh[1] < 0 and material_box[0] - hero_xywh[0] < 0:
            if abs(material_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - material_box[1] < hero_xywh[0] - material_box[0]:
                action_cache = move(direct="LEFT_UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif hero_xywh[1] - material_box[1] >= hero_xywh[0] - material_box[0]:
                action_cache = move(direct="UP", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        elif material_box[1] - hero_xywh[1] > 0 and material_box[0] - hero_xywh[0] < 0:
            if abs(material_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif material_box[1] - hero_xywh[1] < hero_xywh[0] - material_box[0]:
                action_cache = move(direct="LEFT_DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif material_box[1] - hero_xywh[1] >= hero_xywh[0] - material_box[0]:
                action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
        elif material_box[1] - hero_xywh[1] > 0 and material_box[0] - hero_xywh[0] > 0:
            if abs(material_box[1] - hero_xywh[1]) < thy:
                action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif material_box[1] - hero_xywh[1] < material_box[0] - hero_xywh[0]:
                action_cache = move(direct="RIGHT_DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break
            elif material_box[1] - hero_xywh[1] >= material_box[0] - hero_xywh[0]:
                action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                                    press_delay=press_delay,
                                    release_delay=release_delay)
                # break

    # 重新开始
    time_option = -20
    if "options" in cls_object:
        if not action_cache:
            pass
        elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
            ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
            action_cache = None
        else:
            ReleaseKey(direct_dic[action_cache])
            action_cache = None
        if time.time() - time_option > 10:
            directkeys.key_press("NUM0")
            print("移动物品到脚下")
            directkeys.key_press("X")
            time_option = time.time()
        directkeys.key_press("F2")
        print("重新开始F2")
        # break

    print(list)
    

if __name__ == "__main__":
    cls_arr = [{'xywh': [511.0, 130.5, 82.0, 73.0], 'label': 'monster'}, {'xywh': [259.5, 352.0, 59.0, 24.0], 'label': 'door'}, {'xywh': [490.5, 320.5, 75.0, 21.0], 'label': 'user'}]
    init(cls_arr)
