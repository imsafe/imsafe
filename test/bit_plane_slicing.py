from slicing.BitPlane import BitPlane
import cv2

bp = BitPlane()
planes = bp.slice('img/coin.png')

# img = bp.get_plane(8) + bp.get_plane(7) + bp.get_plane(6) + bp.get_plane(5)
cv2.imwrite('results/ms4.png', bp.get_ms(4))
# cv2.imwrite('results/ms3.png', bp.get_ms(3))
# cv2.imwrite('results/ls4.png', bp.get_ls4())
# for i in range(len(planes)):
#     cv2.imwrite('results/slice-.png', planes[i])

print('x')
print(len(bp.get_plane(8)[0]))
print('y')
print(len(bp.get_plane(8)))

bp.concat()
