from pynput.mouse import Listener
import pynput.mouse
from SendInput import *
from ScreenShot import screenshot
from utils.torch_utils import smart_inference_mode
from utils.plots import Annotator
from utils.general import (cv2, non_max_suppression, scale_boxes, xyxy2xywh)
from models.common import DetectMultiBackend
from utils.augmentations import letterbox
import torch
import numpy as np
import math
import threading
import time
print('go')


is_x2_pressed = False


def mouse_click(x, y, button, pressed):
    global is_x2_pressed
    # print(x, y, button, pressed)
    if pressed and button == pynput.mouse.Button.x2:
        is_x2_pressed = True
    elif not pressed and button == pynput.mouse.Button.x2:
        is_x2_pressed = False


def mouse_listener():
    with Listener(on_click=mouse_click) as listener:
        listener.join()


@smart_inference_mode()
def run():
    global is_x2_pressed
    # Load model
    # device = torch.device('cuda:0')
    device = torch.device('cpu')
    # fp16=True
    # model = DetectMultiBackend(weights='./weights/yolov5n.pt', device=device, dnn=False, data=False, fp16=False)
    # 载入模型
    model = DetectMultiBackend(
        weights='./weights/best.pt', device=device, dnn=False, data=False, fp16=False)
    names = model.names

    # 读取图片
    while True:
        im = screenshot()  # 当前屏幕截图
        im0 = im
        # 处理图片 这块代码别动
        im = letterbox(im, (640, 640), stride=32, auto=True)[
            0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        # 推理
        pred = model(im, augment=False, visualize=False)
        # 非极大值抑制
        # classes => 检测的个数 None为不限制
        pred = non_max_suppression(
            pred, conf_thres=0.6, iou_thres=0.45, classes=None, max_det=1000)

        # 处理推理内容
        for i, det in enumerate(pred):
            # 画框
            print(i, det)
            annotator = Annotator(im0, line_width=2)
            if len(det):
                distance_list = []
                target_list = []
                # 将转换后的图片画框结果转换成原图上的结果
                det[:, :4] = scale_boxes(
                    im.shape[2:], det[:, :4], im0.shape).round()
                # 处理推理出来每个目标的信息
                for *xyxy, conf, cls in reversed(det):
                    # xyxy|相似度|下标
                    # 转换xywh形式，方便计算距离
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))
                            ).view(-1).tolist()  # normalized xywh

                    X = xywh[0]  # 计算物体距离截图中心点的X
                    Y = xywh[1]  # 计算物体距离截图中心点的Y

                    print(X, Y, xywh)
                    distance = math.sqrt(X ** 2 + Y ** 2)  # 计算物体距离截图中心点的距离
                    # xywh.append(distance)
                    # 设置框的样式
                    annotator.box_label(xyxy, label=f'[{names[int(cls)]}:{round(distance, 2)}]',
                                        color=(34, 139, 34),
                                        txt_color=(0, 191, 255))
                    # distance_list.append(distance) # 添加目标距离
                    # target_list.append(xywh) # 添加目标信息

                # target_info = target_list[distance_list.index(min(distance_list))]  # 获取离屏幕最近敌人的信息

                # if is_x2_pressed:
                #     mouse_xy(int(target_info[0] - 320), int(target_info[1] - 320))
                #     time.sleep(0.003)  # 主动睡眠，防止推理过快,鼠标移动相同的两次

            im0 = annotator.result()

            #  第一个参数为窗口名称，如果窗口不存在，那么会默认创建一个窗口，窗口名称就是这里填的窗口名称，
            #  第二个参数为图像的矩阵，这里由于没有读入图像，可以用0代替
            cv2.imshow('window', im0)  # 使用函数imshow可以显示图像 =>画框
            cv2.waitKey(1)  # 里面传入一个整数，表示延迟


if __name__ == "__main__":
    threading.Thread(target=mouse_listener).start()
    run()
