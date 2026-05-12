import sensor, image, time, machine
from machine import UART

# =========================
# 摄像头初始化
# =========================
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)

clock = time.clock()

# =========================
# 串口
# =========================
uart = UART(2, 115200)

# =========================
# 加载车牌模板
# =========================
template = image.Image("/template1.pgm")

threshold = 0.70
detect_count = 0
detect_threshold = 2

# =========================
# 主循环
# =========================
while(True):
    clock.tick()
    img = sensor.snapshot()
    result = 0

    # =========================
    # 关键修复：去掉 roi 参数！！！
    # =========================
    r = img.find_template(template, threshold, step=4, search=image.SEARCH_EX)

    if r:
        img.draw_rectangle(r, color=255)
        detect_count += 1
        if detect_count >= detect_threshold:
            result = 1
    else:
        detect_count = 0

    uart.write(str(result) + "\n")
    print("识别结果:",result," FPS:", clock.fps())
