import cv2

depth_exr = cv2.imread("/home/weiheng/code/bio_inspired/BioVision-SS2020/sim_flying_room_stereo/cam0/depthmaps/frame_00000013.exr", cv2.IMREAD_UNCHANGED)

print(depth_exr.shape)

cv2.imshow("depth", depth_exr)