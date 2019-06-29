from PIL import Image
import numpy as np
# pathをよしなにしてくれるライブラリ
import pathlib
# 画像表示するだけ
from IPython.display import display
# sort に必要
from operator import attrgetter
# 時間測定
import time
# 画像表示
import matplotlib.pyplot as plt

# debugger
from IPython.core.debugger import set_trace

from mosaic import Mosaic

from lastturn import Pnm

# 画像入力

img1_url = pathlib.Path('images/sample_img1/Level1/1-001-1.jpg')
img2_url = pathlib.Path('images/sample_img1/Level1/1-001-2.jpg')

# 元となる画像の読み込み
img1 = Image.open(img1_url)
img2 = Image.open(img2_url)

print("img1 size:{}".format(img1.size))
img1.show()
print("img2 size:{}".format(img2.size))
img2.show()

dx = dy = 0
dt = 0.0
r  = 1.0

# 時間測定開始
start = time.time()
print('start')

# 照合(別ファイル)
dx, dy, dt, r = Mosaic.mosaic(img1, img2, r)

# 時間測定終了
elapsed_time = time.time() - start

print("dx:{}, dy:{}, dt:{} r:{}".format(dx, dy, dt, r))
print("time:{}".format(elapsed_time))
print('end')

image3 = Pnm.construct_image(img1, img2, dx, dy, dt, 1.0)

#　表示
image3.show()
 
# 書き出し
# image3.save('')