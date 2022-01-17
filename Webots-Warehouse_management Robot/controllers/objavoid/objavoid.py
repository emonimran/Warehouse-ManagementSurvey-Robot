from controller import Robot, Camera, Display, GPS
import math
import csv
import _thread
import time

TIME_STEP = 64
robot = Robot()
ds = []
dsNames = ['ds_right', 'ds_left']

# Enable camera
camera = robot.getDevice("camera")
camera.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)

camera1 = robot.getDevice("camera(1)")
camera1.enable(TIME_STEP)
camera1.recognitionEnable(TIME_STEP)

# Enable gps
gps = robot.getDevice("gps")
gps.enable(TIME_STEP)


    
# Enable distace sensor
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)

# Enable wheels
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(6)

# Enable ir sensors
left_ir = robot.getDevice('ir1')
left_ir.enable(TIME_STEP)
    
right_ir = robot.getDevice('ir0')
right_ir.enable(TIME_STEP)

            
# Step simulation

names = list()
idss = list()
time = list()
gpsy = list()
gpsx = list()
speed = set()

entry = {b'Box 400', b'Box 285', b'Box 234', b'Box 124', b'Box 45', b'Box 133', b'Box 291', b'Box 337', b'Box 210', b'Box 200', b'Box 164', b'Box 336', b'Box 11', b'Box 299', b'Box 171', b'Box 104', b'Box 101', b'Box 314', b'Box 307', b'Box 211', b'Box 263', b'Box 88', b'Box 95', b'Box 257', b'Box 141', b'Box 80', b'Box 147', b'Box 213', b'Box 287', b'Box 220', b'Box 137', b'Box 42', b'Box 25', b'Box 317', b'Box 98', b'Box 206', b'Box 331', b'Box 109', b'Box 92', b'Box 127', b'Box 193', b'Box 10',
         b'Box 219', b'Box 156', b'Box 246', b'Box 120', b'Box 306', b'Box 333', b'Box 335', b'Box 222', b'Box 296', b'Box 74', b'Box 36', b'Box 339', b'Box 265', b'Box 121', b'Box 241', b'Box 57', b'Box 235', b'Box 139', b'Box 360', b'Box 303', b'Box 277', b'Box 230', b'Box 266', b'Box 297', b'Box 173', b'Box 351', b'Box 316', b'Box 150', b'Box 298', b'Box 48', b'Box 343', b'Box 39', b'Box 202', b'Box 100', b'Box 143', b'Box 255', b'Box 112', b'Box 50', b'Box 79', b'Box 252', b'Box 128', b'Box 105',
         b'Box 315', b'Box 324', b'Box 223', b'Box 107', b'Box 184', b'Box 70', b'Box 274', b'Box 272', b'Box 345', b'Box 283', b'Box 96', b'Box 310', b'Box 77', b'Box 135', b'Box 209', b'Box 97', b'Box 56', b'Box 60', b'Box 4', b'Box 305', b'Box 62', b'Box 245', b'Box 84', b'Box 197', b'Box 295', b'Box 215', b'Box 76', b'Box 196', b'Box 123', b'Box 27', b'Box 161', b'Box 238', b'Box 73', b'Box 93', b'Box 318', b'Box 311', b'Box 262', b'Box 126', b'Box 1', b'Box 114', b'Box 13', b'Box 59', b'Box 185', 
         b'Box 26', b'Box 58', b'Box 78', b'Box 86', b'Box 340', b'Box 289', b'Box 21', b'Box 69', b'Box 5', b'Box 146', b'Box 89', b'Box 72', b'Box 332', b'Box 327', b'Box 254', b'Box 325', b'Box 8', b'Box 118', b'Box 106', b'Box 142', b'Box 260', b'Box 155', b'Box 229', b'Box 61', b'Box 19', b'Box 187', b'Box 94', b'Box 65', b'Box 247', b'Box 319', b'Box 31', b'Box 358', b'Box 2', b'Box 279', b'Box 357', b'Box 110', b'Box 23', b'Box 288', b'Box 292', b'Box 52', b'Box 329', b'Box 312', b'Box 348', 
         b'Box 18', b'Box 125', b'Box 165', b'Box 83', b'Box 278', b'Box 276', b'Box 259', b'Box 186', b'Box 117', b'Box 174', b'Box 322', b'Box 264', b'Box 49', b'Box 251', b'Box 328', b'Box 67', b'Box 226', b'Box 116', b'Box 85', b'Box 301', b'Box 334', b'Box 149', b'Box 24', b'Box 35', b'Box 267', b'Box 194', b'Box 81', b'Box 347', b'Box 201', b'Box 136', b'Box 145', b'Box 338', b'Box 249', b'Box 352', b'Box 218', b'Box 273', b'Box 14', b'Box 7', b'Box 188', b'Box 344', b'Box 47', b'Box 189', 
         b'Box 300', b'Box 244', b'Box 111', b'Box 280', b'Box 179', b'Box 275', b'Box 176', b'Box 3', b'Box 302', b'Box 239', b'Box 90', b'Box 180', b'Box 290', b'Box 268', b'Box 330', b'Box 15', b'Box 286', b'Box 356', b'Box 91', b'Box 131', b'Box 102', b'Box 167', b'Box 320', b'Box 261', b'Box 51', b'Box 326', b'Box 242', b'Box 166', b'Box 63', b'Box 130', b'Box 237', b'Box 253', b'Box 32', b'Box 231', b'Box 182', b'Box 172', b'Box 236', b'Box 355', b'Box 17', b'Box 71', b'Box 28', b'Box 341', 
         b'Box 40', b'Box 122', b'Box 250', b'Box 269', b'Box 108', b'Box 216', b'Box 6', b'Box 205', b'Box 323', b'Box 162', b'Box 284', b'Box 175', b'Box 159', b'Box 304', b'Box 350', b'Box 177', b'Box 270', b'Box 181', b'Box 233', b'Box 294', b'Box 228', b'Box 256', b'Box 163', b'Box 119', b'Box 87', b'Box 113', b'Box 192', b'Box 198', b'Box 148', b'Box 66', b'Box 30', b'Box 170', b'Box 308', b'Box 152', b'Box 43', b'Box 353', b'Box 309', b'Box 22', b'Box 227', b'Box 243', b'Box 158', b'Box 64', 
         b'Box 154', b'Box 221', b'Box 153', b'Box 225', b'Box 178', b'Box 75', b'Box 138', b'Box 157', b'Box 54', b'Box 144', b'Box 207', b'Box 258', b'Box 282', b'Box 151', b'Box 183', b'Box 293', b'Box 346', b'Box 12', b'Box 212', b'Box 203', b'Box 29', b'Box 99', b'Box 160', b'Box 115', b'Box 20', b'Box 359', b'Box 41', b'Box 349', b'Box 240', b'Box 204', b'Box 53', b'Box 208', b'Box 342', b'Box 132', b'Box 33', b'Box 37', b'Box 46', b'Box 321', b'Box 232', b'Box 199', b'Box 82', b'Box 354', b'Box 9', 
         b'Box 281', b'Box 129', b'Box 103', b'Box 248', b'Box 313', b'Box 55', b'Box 169', b'Box 34', b'Box 38', b'Box 16', b'Box 134', b'Box 68', b'Box 168', b'Box 224', b'Box 217', b'Box 271', b'Box 191', b'Box 44', b'Box 214', b'Box 140', b'Box 190', b'Box 195'}

present = set()
missed = list()

avoidObstacleCounter = 0
while robot.step(TIME_STEP) != -1:

    numberOfObjects = camera.getRecognitionNumberOfObjects()
    numberOfObjects1 = camera1.getRecognitionNumberOfObjects()
    
        
    # read ir sensors
    left_ir_value = left_ir.getValue()
    right_ir_value = right_ir.getValue()
    #print("left: {} right{}".format(left_ir_value, right_ir_value))

    leftSpeed = 6
    rightSpeed = 6
    
              
    if(left_ir_value > right_ir_value) and (500 < left_ir_value < 1500):
        #print('Go left')
        leftSpeed = -6
                
    elif (right_ir_value > left_ir_value) and (500 < right_ir_value < 1500):
        #print('Go right')
        rightSpeed = -6
        
                   
    elif (camera.hasRecognition) or (camera1.hasRecognition):#If there are recognizable objects in the image
        my_object = camera.getRecognitionObjects()#Return the object object to my_object        
        my_object1 = camera1.getRecognitionObjects()
        
        
        for k in range (numberOfObjects1):
            #print(my_object[k].get_id())
            #print(my_object[k].get_model())
            #print(my_object1[k].get_position())
            #print(my_object[k].get_position_on_image())
            #print(robot.getTime())
            names.append(my_object1[k].get_model())
            present.add(my_object1[k].get_model())
            idss.append(my_object1[k].get_id())
            time.append(robot.getTime())
            values = gps.getValues()
            gpsx.append(values[0])
            gpsy.append(values[1])
            speed.add(gps.getSpeed())
            #print(f'the speed is {speed}')
            #t = robot.getTime()
            #miss = entry.difference(present)
            #missed.add(str(entry.difference(present)))
            miss = (str(entry.difference(present)))
            missed.append(miss)
            
                               
        for i in range (numberOfObjects):
            #print(my_object[i].get_id())
            #print(my_object[i].get_model())
            names.append(my_object[i].get_model())
            present.add(my_object[i].get_model())
            idss.append(my_object[i].get_id())
            time.append(robot.getTime())
            values = gps.getValues()
            gpsx.append(values[0])
            gpsy.append(values[1])
            #speed.add(gps.getSpeed())
            #t = robot.getTime()
            #miss =entry.difference(present)
            #missed.add(str(entry.difference(present))) 
            #missed = str(entry.difference(present))
            miss = (str(entry.difference(present)))
            missed.append(miss)
                      
        namess = [i for n, i in enumerate(names) if i not in names[:n]]
        times = [i for n, i in enumerate(time) if i not in time[:n]]
        iddss = [i for n, i in enumerate(idss) if i not in idss[:n]]
        gpsxx = [i for n, i in enumerate(gpsx) if i not in gpsx[:n]]                          
        gpsyy = [i for n, i in enumerate(gpsy) if i not in gpsy[:n]]  
        missedd = [i for n, i in enumerate(missed) if i not in missed[:n]]                         
        
                    
        with open(f'Product_Lists.csv','w', newline='') as csvfile:
            fieldnames = ['Time', 'Name', 'ID', 'GPS Latitude', 'GPS longitude','Missing Status']  
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            
                       
                          
            for (x, y, z, a, b, c) in zip( times, namess, iddss, gpsxx, gpsyy, missedd):                                         
                thewriter.writerow({'Time' : x, 'Name' : y, 'ID' : z, 'GPS Latitude' : a, 'GPS longitude' : b, 'Missing Status' : c})
            #with open(f'Missing_Lists.csv','w', newline='') as csvfile:
            #fieldnames = ['Missing']  
            #thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #thewriter.writeheader()
                    
            #for d in missed:                                         
                #thewriter.writerow({'Missing' : missed})               
                #print(f'Products found are: {names} {idss} {z}')
                
                
                if avoidObstacleCounter > 0:
                    avoidObstacleCounter -= 1
                    leftSpeed = 0
                    rightSpeed = 0
                    
                    camera.recognitionDisable()
                    camera1.recognitionDisable()
                                                              
                elif avoidObstacleCounter <= 0:  # read sensors
                    camera.recognitionEnable(TIME_STEP)
                    camera1.recognitionEnable(TIME_STEP)
                    for i in range(2):
                        if ds[i].getValue() < 950.0:
                            avoidObstacleCounter = 100
                
                                        
                                                              
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)

    print(f'Products found are: {namess} {iddss} {times} {gpsxx} {gpsy} {missedd}')
# Enter here exit cleanup code.
