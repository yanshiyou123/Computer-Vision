"""
CS 6384 Homework 1 Programming
Backprojection
"""

import cv2
import scipy.io
import numpy as np
import matplotlib.pyplot as plt


# backprojecting a depth image to a point cloud in the camera coordinate frame
# input: depth with shape (H, W)
# input: intrinsic_matrix, a 3x3 matrix
# output: a point cloud, pcloud with shape (H, W, 3)
#TODO: implement this function
def backproject(depth, intrinsic_matrix):
    Height, Width = depth.shape
    w,h = np.meshgrid(np.arange(Width), np.arange(Height))
    f_x = intrinsic_matrix[0,0]
    f_y = intrinsic_matrix[1,1]
    p_x = intrinsic_matrix[0,2]
    p_y = intrinsic_matrix[1,2]

    #3d point
    x = (w - p_x) * depth / f_x 
    y = (h - p_y) * depth/ f_y 
    z = depth

    pcloud = np.dstack((x, y, z))
    return pcloud


# main function
if __name__ == '__main__':

    # read the image in data
    # rgb image
    rgb_filename = 'Assignment1/data/000006-color.jpg'
    im = cv2.imread(rgb_filename)
    
    # depth image
    depth_filename = 'Assignment1/data/000006-depth.png'
    depth = cv2.imread(depth_filename, cv2.IMREAD_ANYDEPTH)
    # convert from mm to m
    depth = depth / 1000.0
    
    # read the mask image
    mask_filename = 'Assignment1/data/000006-label-binary.png'
    mask = cv2.imread(mask_filename)
    mask = mask[:, :, 0]
    
    # erode the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    
    # load matedata
    meta_filename = 'Assignment1/data/000006-meta.mat'
    meta = scipy.io.loadmat(meta_filename)
    
    # intrinsic matrix
    intrinsic_matrix = meta['intrinsic_matrix']
    print('intrinsic_matrix')
    print(intrinsic_matrix)
    
    # backprojection
    pcloud = backproject(depth, intrinsic_matrix)
        
    # get the points on the box
    pbox = pcloud[mask > 0, :]
    index = pbox[:, 2] > 0
    pbox = pbox[index]
    print(pbox.shape)
        
    # visualization for your debugging
    fig = plt.figure()
        
    # show RGB image
    ax = fig.add_subplot(2, 2, 1)
    plt.imshow(im[:, :, (2, 1, 0)])
    ax.set_title('RGB image')
        
    # show depth image
    ax = fig.add_subplot(2, 2, 2)
    plt.imshow(depth)
    ax.set_title('depth image')
        
    # show segmentation mask
    ax = fig.add_subplot(2, 2, 3)
    plt.imshow(mask)
    ax.set_title('segmentation mask')
        
    # up to now, suppose you get the points box as pbox
    # then you can use the following code to visualize the points in pbox
    # You shall see the figure in the homework assignment
    ax = fig.add_subplot(2, 2, 4, projection='3d')
    ax.scatter(pbox[:, 0], pbox[:, 1], pbox[:, 2], marker='.', color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D ploud cloud of the box')
                  
    plt.show()
