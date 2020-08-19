import cv2
import numpy as np

from board import Board


image_name = "sudoku-grid-2.png"
image_directory = "resources/"
output_directory = "output/"
image_filepath = image_directory + image_name

board_image = cv2.imread(image_filepath)
gray_board_image = cv2.cvtColor(board_image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_board_image, 50,150, apertureSize=3)
cv2.imwrite(output_directory + image_name + '-edges.jpg', edges)
line_max = 1000

lines = cv2.HoughLines(edges, 1, np.pi/180, 300)

#The code below is to investigate the HoughTransform
f = open(output_directory+image_name+ '-houghlinestext.csv', 'w+')
fg = open(output_directory+image_name+'-linestext.csv', 'w+')
f.write("rho,theta,a,b,x0,y0,x1,y1,x2,y2\n")
fg.write("x1,x2,y1,y2,m,b\n")



def sort_lines(line_array):

    rho_array = line_array[:,0,0]
    theta_array = line_array[:,0,0]

    ind = np.lexsort(rho_array, theta_array)

    output_array = [(rho_array[i], theta_array[i]) for i in ind]
    return output_array



#line_array = sort_lines(lines)


for line in lines:
    #For Graphing Lines
    rho = line[0][0]
    theta = line[0][1]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + line_max * (-b))
    y1 = int(y0 + line_max * (a))
    x2 = int(x0 - line_max * (-b))
    y2 = int(y0 - line_max * (a))
    #For Line Equations solve X * m = Y where X = 2x2 matrix (x1, 1), (x2, 1) , Y = (y1, y2) and m = (m, b) for y=mx+b

    X = np.array([[x1, 1],[x2,1]])
    Y = np.array([y1,y2])

    #m = solve_lines(X,Y)
    np.savetxt(fg, [x1,x2,y1,y2],newline=",")
    #np.savetxt(fg,m, newline=",")
    fg.write("\n")






    cv2.line(board_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    for t in [rho,theta,a,b,x0,y0,x1,y1,x2,y2]:
        f.write(str(t) + ", ")
    f.write("\n")




f.close()
fg.close()

cv2.imwrite(output_directory + image_name + '-houghlines.jpg', board_image)

# cv2.imshow("Sudoku Board", board_image)
# cv2.waitKey(0)
#
# sudoku = Board()
#
# sudoku.create(5)
#
# print(sudoku.size)