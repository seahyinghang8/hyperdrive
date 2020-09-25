import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image

import pdf2image
from scipy import spatial

from parser import process_image

WORD_DIST_MULTIPLIER = 1.25

def cluster_font(pdf_path):
	image = pdf2image.convert_from_path(pdf_path)[0]
	df = process_image(image)

def cluster_font_size(word1, word2):
	word1_width = word1['width'] / len(word1['word'])
	word2_width = word2['width'] / len(word2['word'])
	width_prop = min(word1_width, word2_width) / max(word1_width, word2_width)
	height_prop = (
		min(word1['height'], word2['height']) /
		max(word1['height'], word2['height']))
	return (width_prop + height_prop) / 2

def cluster_color(image, word1, word2):
	return 1. - spatial.distance.cosine(
		get_color_hist(
			image, word1['left'], word1['top'],
			word1['height'], word1['width']),
		get_color_hist(
			image, word2['left'], word2['top'],
			word2['height'], word2['width'])
	)

def get_color_hist(image, left, top, height, width):
	mask = np.zeros((int(image.size[1]), int(image.size[0])))
	mask[top: top+height, left: left+width] = np.ones((height, width))
	return image.histogram(Image.fromarray(np.uint8(255*mask)))


if __name__ == "__main__":
    pdf_path = '../w2/w2.pdf'
    cluster_font(pdf_path)



