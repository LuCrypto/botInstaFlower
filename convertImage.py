
# Convert png to jpg

from PIL import Image

for i in range(100):
    # chemin1 = f"images/image_{i+1}.png"
    # chemin2 = f"images/image_{i+1}.jpg"
    img = Image.open(f"images/image_{i+1}.png")
    img = img.convert('RGB')
    img.save(f"images/image_{i+1}.jpg")




