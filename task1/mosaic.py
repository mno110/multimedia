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
# プロット
import matplotlib.pyplot as plt

# debugger
from IPython.core.debugger import set_trace

# 外部ファイルのインポート
# from mosaic import Mosaic

class Mosaic:
    
    
    
    @classmethod
    def mosaic(self, image1, image2, r):
        
        #image1_pixels = convert_image_to_array(image1)
        #image2_pixels = convert_image_to_array(image2)
        start=time.time()
        print('image1:start')
        index1, value1 = self.harrisope(image1)

        print('image2:start')        
        index2, value2 = self.harrisope(image2)
        print(time.time()-start)

        
        
        
        
        return
        
    @classmethod
    def harrisope(self,imag1):
        # harrisコーナー検出
        k = 0.04 # 0.04~0.06とか
        list_num = 5 # 奇数がいいなあ
        list_nh = list_num//2
        point_num = 30 # 特徴点の数

        im_list = np.array(imag1)
        im_list = np.sum(im_list, axis=2)/3
        feature_value = np.zeros( (imag1.height,imag1.width), dtype = float )
        
        for y in range(imag1.height):
            if y < list_nh or imag1.height-list_nh < y:
                continue

            for x in range(imag1.width):
                if x < list_nh or imag1.width-list_nh < x:
                    continue

                f_list = np.empty( (list_num, list_num), dtype = int )
                f_list = im_list[y-list_nh:y+list_nh, x-list_nh:x+list_nh]
                
                # for color in 3:
                feature_value[y,x]=np.linalg.det(f_list)-k*((np.trace(f_list))**2)
        

        feature_sort = sorted(np.ravel(feature_value), reverse=True)
        feature_sort = feature_sort[point_num]
        
        feature_index = np.where(feature_value > feature_sort)

        feature_value = feature_value[feature_value > feature_sort]
        
        #plt.figure()
        #plt.imshow(im_list)
        #plt.scatter(list(feature_index[1]), list(feature_index[0]))
        #plt.show()

        
        return feature_index,feature_value

