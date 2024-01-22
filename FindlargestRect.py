def largest_rectangle(matrix: list[list[int]]) -> tuple:
    """
    :param matrix: A 2D matrix of integers (1 <= len(matrix),
    len(matrix[0]) <= 100)
    :return: The area of the largest rectangle formed by similar numbers
    """
    # Your code here
    maxSizeRect = []
    for i in range(len(matrix)):
        n = len(matrix[i])
        temp_list = [[1 for col in range(2)] for row in range(n)]
        maxSizeRect.append(temp_list)

    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if j != 0 and matrix[i][j] == matrix[i][j-1]:
                maxSizeRect[i][j][0] = maxSizeRect[i][j-1][0] + 1
            if i != 0 and j < len(matrix[i-1]) and matrix[i][j] == matrix[i-1][j]:
                maxSizeRect[i][j][1] = maxSizeRect[i-1][j][1] + 1

    maxArea = -float('inf')            

    for row in range(len(maxSizeRect)):
        for col in range(len(maxSizeRect[row])):
            if maxSizeRect[row][col][0] == maxSizeRect[row][col][1]:
                continue
            currArea = maxSizeRect[row][col][0] * maxSizeRect[row][col][1]
            if currArea > maxArea:
                maxArea = currArea
                resNum = matrix[row][col]           
                
    print(resNum, maxArea)
    return (resNum, maxArea)


matrix_example = [
[1, 1, 1, 0, 1, -9],
[1, 1, 1, 1, 2, -9],
[1, 1, 1, 1, 2, -9],
[1, 0, 0, 0, 5, -9],
[5, 0, 0, 0, 5],
]
assert largest_rectangle(matrix_example) == (1, 8)