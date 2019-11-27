"""
Version: Python3.7
Author: OniOn
Site: http://www.cnblogs.com/TM0831/
Time: 2019/9/29 16:18
"""
from random import randint
from PIL import Image, ImageDraw, ImageFont


def get_random_color():
    # 随机颜色RGB
    return randint(120, 200), randint(120, 200), randint(120, 200)


def get_random_code():
    # 随机字符
    codes = [[chr(i) for i in range(48, 58)], [chr(i) for i in range(65, 91)], [chr(i) for i in range(97, 123)]]
    codes = codes[randint(0, 2)]
    return codes[randint(0, len(codes)-1)]


def generate_captcha(width=140, height=60, length=4):
    # 生成验证码
    img = Image.new("RGB", (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/font.ttf", size=36)
    # 验证码文本
    text = ""
    for i in range(length):
        c = get_random_code()
        text += c

        rand_len = randint(-5, 5)
        draw.text((width * 0.2 * (i+1) + rand_len, height * 0.2 + rand_len), c, font=font, fill=get_random_color())
    # 加入干扰线
    for i in range(3):
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # 加入干扰点
    for i in range(16):
        draw.point((randint(0, width), randint(0, height)), fill=get_random_color())
    # 保存图片
    img.save("static/captcha/" + text + ".jpg")
    return text + ".jpg"


if __name__ == "__main__":
    for i in range(1000):
        generate_captcha()
