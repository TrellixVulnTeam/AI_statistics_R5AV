# import cv2
# import sys
# from matplotlib import pyplot as plt
# import matplotlib.font_manager as fm
#
# path = "./NanumBarunGothic.ttf"
# fontprop = fm.FontProperties(fname=path, size=12)
#
# src = cv2.imread('test.jpg')
#
# src_ycrcb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
# ycrcb_planes = cv2.split(src_ycrcb)
#
# ycrcb_planes[0] = cv2.equalizeHist(ycrcb_planes[0])
#
# dst_ycrcb = cv2.merge(ycrcb_planes)
# dst = cv2.cvtColor(dst_ycrcb, cv2.COLOR_YCrCb2BGR)
# dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
#
# plt.subplot(221), plt.imshow(src), plt.title('원본 이미지', fontproperties=fontprop)
# plt.subplot(222), plt.imshow(dst, cmap='gray'), plt.title('평활화 적용 이미지', fontproperties=fontprop)
# plt.subplot(223), plt.hist(src.ravel(), 256, [0,256])
# plt.subplot(224), plt.hist(dst.ravel(), 256, [0,256])
# plt.show()

import cv2
import sys
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

path = "./NanumBarunGothic.ttf"
fontprop = fm.FontProperties(fname=path, size=12)

bg = cv2.imread('1.png')
bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
img = cv2.imread('2.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

diff = cv2.absdiff(img, bg)

diff_g = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

th = cv2.adaptiveThreshold(diff_g,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)

plt.subplot(221), plt.imshow(bg), plt.title('배경 이미지', fontproperties=fontprop)
plt.subplot(222), plt.imshow(img), plt.title('촬영된 이미지', fontproperties=fontprop)
plt.subplot(223), plt.imshow(diff), plt.title('Subtract 적용', fontproperties=fontprop)
plt.subplot(224), plt.imshow(th, cmap='gray'), plt.title('Thresholding 적용', fontproperties=fontprop)
plt.show()

# cv2.imshow("diff", diff)
#
# cv2.waitKey()
# cv2.destroyAllWindows()