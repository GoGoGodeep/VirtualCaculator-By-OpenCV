import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)  # 白底
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (50, 50, 50), 3)  # 黑框
        cv2.putText(img, self.value, (self.pos[0]+30, self.pos[1]+70), cv2.FONT_HERSHEY_PLAIN,
                    4, (50, 50, 50), 2)   # 数字

    def checkClick(self, x, y):
        if  self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)  # 白底
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)  # 黑框
            cv2.putText(img, self.value, (self.pos[0]+20, self.pos[1]+80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)  # 数字
            return True
        else:
            return False

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1080)    # 宽度
cap.set(4, 720)     # 高度
detector = HandDetector(detectionCon=0.8, maxHands=1)

# 创建按钮
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 700
        ypos = y*100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# 变量
myEquation = ''
delayCounter = 0

# 循环
while True:
    # 从摄像头读取图像
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 识别手
    hands, img = detector.findHands(img, flipType=False)

    # 绘制所有按钮
    cv2.rectangle(img, (700, 50), (700 + 400, 70 + 100),
                  (225, 225, 225), cv2.FILLED)  # 结果输出框
    cv2.rectangle(img, (700, 50), (700 + 400, 70 + 100),
                  (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)

    # 检查手
    if hands:
        lmList = hands[0]['lmList']  # 手指的所有点
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        x, y = lmList[8]
        if length < 80:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # 显示结果
    cv2.putText(img, myEquation, (720, 120), cv2.FONT_HERSHEY_PLAIN,
                    4, (50, 50, 50), 3)

    # 显示图像
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''