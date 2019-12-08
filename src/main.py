from word_list import word_list
from pre_process import get_grid

import re
import time

#this global variable will store the result
results=[]

def solve(img_file, color, min_length=4, only_intersection=True):

	if color not in ("blue","orange"):
		raise ValueError("color must be one of 'blue' or 'orange' but got '{}'".format(color))

	if not isinstance(min_length,int):
		raise TypeError("min_length must be of type int and not {}".format(type(min_length)))

	grid=''
	my_grid, blue, orange= get_grid(img_file)
	#print(my_grid)

	if color=="blue": color_arr, other_arr= blue,orange
	else: color_arr, other_arr= orange,blue

	for row in my_grid:
		for each in row:
			grid+=each
		grid+=' '


	grid= grid.split()

	alphabet = ''.join(set(''.join(grid)))
	

	match=re.compile("["+alphabet+"]{"+str(min_length)+",}$",re.I).match

	words= [word for word in word_list if match(word)]
	prefixes= set()

	for word in words:
		for i in range(2,len(word)+1):
			prefixes.add(word[:i])

	final_res=[]
	for x, row in enumerate(grid):
		for y, letter in enumerate(row):
			if (x,y) in color_arr:
				path=[(x,y)]
				extending(letter, path, prefixes, grid, words)
				
				if results is not None:
					for result in results:
						if result not in final_res:
							final_res.append(result)
	
	if only_intersection:
		filtered_res=[]
		for result in final_res:
			if set(result[1])&set(other_arr):
				filtered_res.append(result)
		
		return filtered_res
	return final_res
				
def extending(prefix, path, prefixes, grid, words):
	global results
	if prefix in words:
		results+=[(prefix, path)]
	
	for (nx, ny) in neighbors(path[-1]):
		if (nx, ny) not in path:
			prefix1 = prefix + grid[nx][ny]
			
			if prefix1 in prefixes:
				extending(prefix1, path + [(nx, ny)], prefixes, grid, words)

def neighbors(path, ncols=10, nrows=13):
	neighs=[]
	x,y=path
	for nx in range(max(0, x-1), min(x+2, nrows)):
		for ny in range(max(0, y-1), min(y+2, ncols)):
			neighs+=[(nx, ny)]
	return neighs


if __name__=="__main__":
	t1= time.time()
	x= solve("12.png", "blue")
	print("Execution time: {}".format(time.time()-t1))

	for each in x:
		print(each)

