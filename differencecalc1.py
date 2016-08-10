#Difference Testing Node

import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

def main():
	file1, file2 = sys.argv[1:1+2]
	#Read images as 2D arrays (cvt to gray)
	img1 = to_grayscale(imread(file1).astype(float))
	img2 = to_grayscale(imread(file2).astype(float))
	#draw comparison
	n_m, n_0 = compare_images(img1, img2)
	print "Manhattan Norm:", n_m, "/ per pixel:", n_m/img1.size
	print "0 Norm:", n_0, "/ per pixel:", n_0*1.0/img1.size

def compare_images(img1, img2):
	#Normalize to control for minor changes between images (lighting etc.)
	img1 = normalize(img1)
	img2 = normalize(img2)

	#Calculate difference and norms
	diff = img1 - img2 #using the arrays
	m_norm = sum(abs(diff)) #Manhattan
	z_norm = norm(diff.ravel(), 0) #0
	return (z_norm*1.0/img1.size)

def to_grayscale(arr):
	"If array is a color image (3 dimensions), convert it to grayscale (2 dimensions)"
	if len(arr.shape) == 3:
		return average(arr, -1)
	else:
		return arr

def normalize(arr):
	rng = arr.max()-arr.min()
	amin = arr.min()
	return (arr-amin)*255/rng

if __name__=="__main__":
	main()

