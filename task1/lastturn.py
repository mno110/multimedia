import numpy as np
from PIL import Image
# sort に必要
from operator import attrgetter

class Cut:
    x  = 0
    y1 = 0
    y2 = 0
    
    def __init__(self, x, y1, y2):
        self.x  = x
        self.y1 = y1
        self.y2 = y2

class Pnm:
    
    
    @classmethod
    def construct_image(self, image1, image2, dx, dy, dt, r):
        
        # TODO rはとりあえず後回し
        resized_image = image2
        
        # 回転角を度からラジアンに変換
        dt = dt * np.pi / 180.0
        
        s1 = np.sin(dt)
        c1 = np.cos(dt)
        
        # 合成画像を含む最小の矩形を計算(image1の左上が座標の原点)
        
        
        # 上
        top = 0
        top = np.min([top, int(dy)])
        top = np.min([top, int(dy - resized_image.width * s1)])
        top = np.min([top, int(dy - resized_image.width * s1 + resized_image.height * c1)])
        top = np.min([top, int(dy + resized_image.height * c1)])
            
            
        # 下
        bottom = image1.height - 1
        bottom = np.max([bottom, int(np.ceil(dy) - 1)])
        bottom = np.max([bottom, int(np.ceil(dy - resized_image.width * s1) - 1)])
        bottom = np.max([bottom, int(np.ceil(dy - resized_image.width * s1 + resized_image.height * c1) - 1)])
        bottom = np.max([bottom, int(np.ceil(dy - resized_image.width * c1) - 1)])
        
           
        # 左
        left = 0
        left = np.min([left, int(dx)])
        left = np.min([left, int(dx + resized_image.width * c1)])
        left = np.min([left, int(dx + resized_image.width * c1 + resized_image.height * s1)])
        left = np.min([left, int(dx + resized_image.height * s1)])
        
        
        # 右
        right = image1.width - 1
        right = np.max([right, int(np.ceil(dx) - 1)])
        right = np.max([right, int(np.ceil(dx + resized_image.width * c1) - 1)])
        right = np.max([right, int(np.ceil(dx + resized_image.width * c1 + resized_image.height * s1) - 1)])
        right = np.max([right, int(np.ceil(dx + resized_image.height * s1) - 1)])
           
        # 合成画像の大きさを計算
        width  = right - left + 1
        height = bottom - top + 1
        
        image = Image.new("RGB", (width, height))
           
        # 合成画像の初期化(白で埋める)
        for i in range(height):
            for j in range(width):
                image.putpixel((j,i), (100, 100, 100))
           
        x1 = (- dx + left) * c1 - (- dy + top) * s1
        y1 = (- dx + left) * s1 + (- dy + top) * c1
        
           
        for i in range(image.height):
            for j in range(image.width):
                x = int((j - dx + left) * c1 - (i - dy + top) * s1)
                y = int((j - dx + left) * s1 + (i - dy + top) * c1)
           
                if(all([x >= 0, x < resized_image.width, y >= 0, y < resized_image.height])):
                    # image.putpixel((j,i), resized_image.getpixel((x,y)))
                   
                    # resized_imageを合成画像に書き出す
                    r,g,b = self.__get_pixel(resized_image, j, i, x1, y1, s1, c1)
                    image.putpixel((j, i), (r,g,b))
           
                    # image1の画像領域の場合、合成画像とimage1の平均で上書きする
                    if(all([i + top >= 0, i + top < image1.height, j + left >= 0, j + left < image1.width])):
                        r = (image.getpixel((j,i))[0] + image.getpixel((int(j + left), int(i + top)))[0]) / 2
                        g = (image.getpixel((j,i))[1] + image.getpixel((int(j + left), int(i + top)))[1]) / 2
                        b = (image.getpixel((j,i))[2] + image.getpixel((int(j + left), int(i + top)))[2]) / 2
                        image.putpixel((j,i), (int(r), int(g), int(b)))
                elif(all([i + top >= 0, i + top < image1.height, j + left >= 0, j + left < image1.width])):

                    tmp = (int(j+left), int(i+top))
                    image.putpixel((j,i), image1.getpixel(tmp))         
           
        return image
    

    @classmethod
    def __get_pixel(self, image, u, v, x1, y1, s1, c1):
        
        c, cut = self.__make_cut(u, v, x1, y1, s1, c1)
    
        
        s_sum = 0.0
        r = g = b = 0.0
        for i in range(1, c):
            
            
            ymin = cut[i-1].y1 if cut[i-1].y1 < cut[i].y1 else cut[i].y1
            ymax = cut[i-1].y2 if cut[i-1].y2 < cut[i].y2 else cut[i].y2
            
            yy = int(ymax)
            xx = int(cut[i-1].x)
            
            for yy in range(int(ymax), int(ymin) - 1,-1):
                
                
                if(cut[i-1].y1 > yy+1 or cut[i-1].y2 < yy):
                    continue
                if(cut[i].y1 > yy+1 or cut[i].y2 < yy):
                    continue
                t1 = cut[i-1].y1 if cut[i-1].y1 > yy   else yy
                t2 = cut[i-1].y2 if cut[i-1].y2 < yy+1 else yy+1
                t3 = cut[i].y1   if cut[i].y1   > yy   else yy
                t4 = cut[i].y2   if cut[i].y2   < yy+1 else yy+1
                s  = (t2 - t1 + t4 - t3) * (cut[i].x - cut[i-1].x) / 2.0
                
                s_sum += s
                
                if(any([cut[i-1].x < 0, cut[i].x > image.width, yy < 0, yy >= image.height])):
                    r += s * 255.0
                    g += s * 255.0
                    b += s * 255.0
                    
                else:
                    
                    r += s * image.getpixel((xx, yy))[0]
                    g += s * image.getpixel((xx, yy))[1]
                    b += s * image.getpixel((xx, yy))[2]

        r = np.min([r, 255.0])
        g = np.min([g, 255.0])
        b = np.min([b, 255.0])
        
        return int(r), int(g), int(b)
        
    
    @classmethod
    def __make_cut(self, u, v, x1, y1, s1, c1):
        
        cuts = []

        k = [0]*4
        xx = yy1 = yy2 = 0
        ind = [(0, 0), (1, 0), (1,1), (0,1)]

        X = [c1 * (u + ind[i][0]) - s1 * (v + ind[i][1]) + x1 for i in range(4)]
        Y = [s1 * (u + ind[i][0]) + c1 * (v + ind[i][1]) + y1 for i in range(4)]
            
            
        if(X[0] == X[3]):
            cut = Cut(X[0], Y[0], Y[3])
            cuts.append(cut)
            cut = Cut(X[1], Y[1], Y[2])
            cuts.append(cut)
        elif(X[0] < X[3]):
            cut = Cut(X[0], Y[0], Y[0])
            cuts.append(cut)
            cut = Cut(X[2], Y[2], Y[2])
            cuts.append(cut)
            if(X[1] == X[3]):
                cut = Cut(X[1], Y[1], Y[3])
                cuts.append(cut)
            elif(X[1] > X[3]):
                cut = Cut(X[1], Y[1], (X[1]-X[2]) * (Y[3]-Y[2]) / (X[3]-X[2]) + Y[2])
                cuts.append(cut)
                cut = Cut(X[3], Y[3], (X[3]-X[0]) * (Y[1]-Y[0]) / (X[1]-X[0] + Y[0]))
                cuts.append(cut)
            else:
                cut = Cut(X[1], Y[1], (X[1]-X[0]) * (Y[3]-Y[0]) / (X[3]-X[0]) + Y[0])
                cuts.append(cut)
                cut = Cut(X[3], Y[3], (X[3]-X[1]) * (Y[2]-Y[1]) / (X[2]-X[1]) + Y[1])
                cuts.append(cut)
                
        else:
            cut = Cut(X[3], Y[3], Y[3])
            cuts.append(cut)
            cut = Cut(X[1], Y[1], Y[1])
            cuts.append(cut)
            
            if(X[0] == X[2]):
                cut = Cut(X[0], Y[0], Y[2])
                cuts.append(cut)
                
            elif(X[0] > X[2]):
                cut = Cut(X[0], Y[0], (X[0]-X[1]) * (Y[2]-Y[1]) / (X[2]-X[1]) + Y[1] )
                cuts.append(cut)
                cut = Cut(X[2], Y[2], (X[2]-X[0]) * (Y[3]-Y[0]) / (X[3]-X[0]) + Y[0] )
                cuts.append(cut)
    
            else:
                cut = Cut(X[0], Y[0], (X[0]-X[2]) * (Y[3]-Y[2]) / (X[3]-X[2]) + Y[2] )
                cuts.append(cut)
                cut = Cut(X[2], Y[2], (X[2]-X[0]) * (Y[1]-Y[0]) / (X[1]-X[0]) + Y[0] )
                cuts.append(cut)
                        
                
        for i in range(4):
            for j in range(4):
                k[j] = (i +  j) % 4
                
            
            if(Y[k[3]] == Y[k[0]]):
                continue
                
            yy1 = Y[k[3]] if Y[k[3]] > Y[k[0]] else Y[k[0]]
            xx = (yy1 - Y[k[0]]) * (X[k[3]] - X[k[0]]) / (Y[k[3]] - Y[k[0]]) + X[k[0]]
            
            flag = 0
            
            for j in range(len(cuts)):
                if(xx == cuts[j].x):
                    flag =1
                    
                    break
                    
            if(flag):
                continue
                
            for j in range(3):
                if((X[k[j]] < xx and xx < X[k[j+1]]) or (X[k[j+1]] < xx and xx < X[k[j]])):
                    yy2 = (xx - X[k[j]]) * (Y[k[j+1]] - Y[k[j]]) / (X[k[j+1]] - X[k[j]] - Y[k[j]])
                    break
                        
                    
            cut_x = xx
            if(yy1 < yy2):
                cut_y1 = yy1 
                cut_y2 = yy2
            else:
                cut_y1 = yy2
                cut_y2 = yy1

                          
            cut = Cut(cut_x, cut_y1, cut_y2)
            cuts.append(cut)
                          
        for i in range(4):
            for j in range(4):
                k[j] = (i + j) % 4
                
            
            if(Y[k[3]] == Y[k[0]]):
                continue
                
            yy1 = Y[k[3]] if Y[k[3]] > Y[k[0]] else Y[k[0]]
            xx = (yy1 - Y[k[0]]) * (X[k[3]] - X[k[0]]) / (Y[k[3]] - Y[k[0]]) + X[k[0]]
            
            flag = 0
            
            for j in range(len(cuts)):
                if(xx == cuts[j].x):
                    flag =1
                    break
                    
            if(flag):
                continue
                
            for j in range(3):
                if((X[k[j]] < xx and xx < X[k[j+1]]) or (X[k[j+1]] < xx and xx < X[k[j]])):
                    yy2 = (xx - X[k[j]]) * (Y[k[j+1]] - Y[k[j]]) / (X[k[j+1]] - X[k[j]] - Y[k[j]])
                    break
                    
                
                        
                    
            cut_x = xx
            if(yy1 < yy2):
                cut_y1 = yy1 
                cut_y2 = yy2
            else:
                cut_y1 = yy2
                cut_y2 = yy1
                          
            cut = Cut(cut_x, cut_y1, cut_y2)
            cuts.append(cut)          
            
        cuts = sorted(cuts, key=attrgetter('x'))
        
            
        return len(cuts), cuts
        
 

            
            
        
           
        