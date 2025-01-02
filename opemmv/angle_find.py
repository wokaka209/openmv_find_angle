import time
import sensor
import math
import image
import display
import pyb

#红色阈值
thresholds = [(12, 29, 17, 50, -56, 48),(4, 21, 12, 49, -17, 57),(6, 36, 20, 72, -6, 38),(11, 26, 14, 97, -90, 70),(8, 18, 8, 25, 7, 24)]
area_threshold_user=300
x_stride_user=3
y_stride_user=4
blobs=0
lcd=0
i=0
angle=0
new_angle=0
formatted_number=0

received_data =0
received_data_str=0

flag_open=0
#roi_1=(0,114,)
#roi_2=()

#last_blob = [0, 0]
#v1=0
#v2=0
#cross_product=0



sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)# QVGA的中心坐标：160,120
sensor.skip_frames(time=2000)    # 跳过2000毫秒的帧让相机图像在改变相机设置后稳定下来
sensor.set_auto_gain(False)      # 必须关闭才能进行颜色跟踪
sensor.set_auto_whitebal(False)  # 必须关闭才能进行颜色跟踪
clock = time.clock()
lcd = display.SPIDisplay()
uart = pyb.UART(3, 115200)




#检测5mm红线偏度
while(True):
    clock.tick()
    img=sensor.snapshot()
    if uart.any():  # 检查串口是否有数据可读
            received_data = uart.readline()  # 读取一行数据，发送端发送的字符串末尾通常有换行符，所以用readline比较合适
            received_data_str = received_data.decode('utf-8').strip()  # 将接收到的字节数据转换为字符串，并去除两端的空白字符（如换行符、空格等）
            if received_data_str == "open":
                flag_open=1
    blobs = img.find_blobs(thresholds,area_threshold=area_threshold_user,merge=True,x_stride = x_stride_user,y_stride= y_stride_user)
    for blob_0 in blobs:
        img.draw_cross(blob_0.cx(),blob_0.cy())
        img.draw_line(blob_0.minor_axis_line())
#        img.draw_rectangle(blob_0.rect())
        angle=blob_0.rotation_deg()
#        angle_r=90-blob_0.rotation_rad()*180.0/math.pi
        if 90 >=angle >= 0  and  114<=blob_0.cx() <=289 and 77<= blob_0.cy()<= 228 :
            new_angle =90 -  angle
        elif 180 >=angle > 90  and 108<blob_0.cx() <288 and 17< blob_0.cy()<77:
            new_angle = 270 - angle
        elif 67<=blob_0.cx() <=118 and 77< blob_0.cy()<223:
            new_angle =  90 - angle
        elif 71<=blob_0.cx() <=119 and 17< blob_0.cy()<71:
            new_angle = 180
        print("cx:%dcy:%d" %(blob_0.cx(), blob_0.cy()))

#        v1=(last_blob[0],last_blob[1])
#        v2=(blob_0.cx(),blob_0.cy())
#        cross_product=v1[0] * v2[1] - v1[1] * v2[0]
#        last_blob[0] = blob_0.cx()
#        last_blob[1] = blob_0.cy()
#        print("cross_product:%d" %cross_product)
#        if angle_r <0:
#            angle_r = 0;
#        elif angle_r > 90:
#            angle_r=90
        i=i+1
        if (i>10000):
            i=0
#        if abs(angle - 90) < 10 or abs(angle - 270) < 10:  # 判断是否接近垂直方向，阈值可调整
#                   if y_max - y_min > 0:  # 如果垂直方向长度大于0，说明有上下方向区分
#                       if y_max > img.height() / 2 + 30:  # 如果大部分在图像下半部分
#                           if new_angle < 180:
#                               new_angle += 180
#                       else:  # 如果大部分在图像上半部分
#                           if new_angle > 180:
#                               new_angle -= 180
        print("%d:new_angle_:%d" %(i, new_angle))
#        print("%d:angle:%.1f" %(i,angle))
        # 获取blob的长轴和短轴长度
#        print("%d:%.2f" %(i, angle_r))
        if flag_open ==1:
            number_to_send = new_angle
            formatted_number = "{:03d}".format(number_to_send)
            uart.write('%' + str(formatted_number) + '\n')
    lcd.write(sensor.snapshot())

