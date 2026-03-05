import qrcode

url = "http://YOUR-IP:8501/?mode=user"

img = qrcode.make(url)

img.save("qrcode.png")
