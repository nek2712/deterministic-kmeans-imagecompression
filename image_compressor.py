from kmeans import k_means
from image_diversion import ptp_idm
import numpy as np
import argparse
import time
import cv2

if __name__ == '__main__':
	
	# Script arguments
	ap = argparse.ArgumentParser(
		description = 'Compress an image with specified amount of colors'
	)
	ap.add_argument(
		'-i',
		'--image',
		required = True,
		help = 'Path to image'
	)
	ap.add_argument(
		'-c',
		'--colors',
		required = True,
		type = int,
		help = 'Number of colors'
	)
	args = ap.parse_args()
	
	# Define constants
	IM_PATH = args.image
	K = args.colors
	
	# Read image
	image = cv2.imread(IM_PATH)
	# Store original shape
	original_shape = image.shape
	# Reshape into a numpy 2d array
	image = image.reshape([image.shape[0] * image.shape[1], 3])
	
	# Run k-means
	t0 = time.time()
	c_means, clusters, mse = k_means(image, K)
	t1 = time.time()
	
	# Create compressed image
	compressed_image = np.zeros(image.shape, dtype = np.uint8)
	for i in range(compressed_image.shape[0]):
		compressed_image[i] = c_means[clusters[i]].astype(np.uint8)
		
	# Return to original shape
	image = image.reshape(original_shape).astype(np.uint8)
	compressed_image = compressed_image.reshape(original_shape).astype(np.uint8)
	
	# Store original and resulting image in png format
	cv2.imwrite('original.png', image)
	cv2.imwrite('compressed.png', compressed_image)
	
	print('Done compressing!\nFinal MSE:', mse)
	print('IDM:', ptp_idm(image, compressed_image))
	print('Took:', t1-t0, 's')
	
