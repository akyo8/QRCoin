import os
from MyQR.myqr import run
from PIL import Image
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('Words', help = 'The words to produce you QR-code picture, like a URL or a sentence. Please read the README file for the supported characters.')
argparser.add_argument('--coin_path', default='./coin.png')
argparser.add_argument('--qr_path', default='./qrcode.png')
argparser.add_argument('--bill_path', default='./bill.jpg')
args = argparser.parse_args()

def generate_qrcode(words):
    run(words, 1, 'Q')

def modify_qrcode(qrpath):
    org = Image.open(qrpath)
    org = org.convert('RGB')
    qr = Image.new('RGBA', (org.width - 72, org.height - 72))

    target_color = (0, 0, 0, 255)
    alpha_color = (255, 255, 255, 0)

    for i in range(qr.size[0]):
        for j in range(qr.size[1]):
            r, g, b = org.getpixel((i + 36, j + 36))
            if (i >= 0 and i < 0 + 63 and j >= 0 and j < 0 + 63) or (i >= 0 and i < 0 + 63 and j >= qr.size[0] - 63 and j < qr.size[0]) or (i >= qr.size[0] - 63 and i < qr.size[0] and j >= 0 and j < 0 + 63) or (i >= qr.size[0] - 81 and i < qr.size[0] - 36 and j >= qr.size[0] - 81 and j < qr.size[0] - 36):
                if r == 0 and g == 0 and b == 0:
                    qr.putpixel((i, j), target_color)
                else:
                    qr.putpixel((i, j), alpha_color)
            else:
                dist = (i % 9 - 4) * (i % 9 - 4) + (j % 9 - 4) * (j % 9 - 4)
                if r == 0 and g == 0 and b == 0 and dist < 4 * 4:
                    qr.putpixel((i, j), target_color)
                else:
                    qr.putpixel((i, j), alpha_color)
    
    qr.save('result.png')
    return qr

def process_main(words, bgpath, qrpath, billpath):
    generate_qrcode(words)
    qr = modify_qrcode(qrpath)
    width = qr.size[0]
    height = qr.size[1]

    bg = Image.open(bgpath)
    bg = bg.convert('RGBA')
    bg = bg.resize((width * 2, height * 2))

    bill = Image.open(billpath)
    bill = bill.convert('RGB')

    for i in range(width * 2):
        for j in range(height * 2):
            dist = (i - width) * (i - width) + (j - height) * (j - height)
            if dist > (width - 15) * (width - 15):
                bg.putpixel((i, j), (255, 255, 255, 0))
            else:
                rr, gg, bb, aa = bg.getpixel((i, j))
                if i >= int(width / 2) and i < int(width / 2) + width and j >= int(height / 2) and j < int(height / 2) + height:
                    r, g, b, a = qr.getpixel((i - int(width / 2), j - int(width / 2)))
                    if a != 0:
                        bg.putpixel((i, j), (r, g, b))

    # bg.save(bgpath[:-4] + '_result.png')
    # bg = bg.resize((124, 124))
    bill = bill.resize((4412, 1916))

    for i in range(800, 910 + bg.size[0]):
        for j in range(650, 760 + bg.size[1]):
            r, g, b = bill.getpixel((i, j))
            if r < 150 and g < 150 and b < 150:
                bill.putpixel((i, j), (240, 188, 76))

    for i in range(bg.size[0]):
        for j in range(bg.size[1]):
            rr, gg, bb, aa = bg.getpixel((i, j))
            if aa != 0:
                bill.putpixel((i + 863, j + 718), (rr, gg, bb))

    bill.save(billpath[:-4] + '_result.png')

process_main(args.Words, args.coin_path, args.qr_path, args.bill_path)