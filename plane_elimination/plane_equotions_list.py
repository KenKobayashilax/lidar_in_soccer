#These equotions list are created manually by using 

#list of coefficients of plane equotions <- ax + by + cz + b = 0
planes_list = [
    [0.00, -0.02, 1.00, 0.95], #floor
    [-0.00, -0.02, 1.00, -2.00], #ceiling
    [0.04, 1, 0.03, -3.30], #left wall
    [0.04, 1.0, 0.03, 0.50], #right wall
    [1, 0.04, 0, -59.7] #end wall
]

#list of whether equotions are < or >. If true, ax + by + cz + b < 0
bool_list = [
    False, 
    True, 
    True,
    False,
    True
]