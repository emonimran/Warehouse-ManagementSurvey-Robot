from controller import Robot, Camera, Display, GPS
import math
import csv
import _thread


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
    wheels[i].setVelocity(2.0)

# Enable ir sensors
left_ir = robot.getDevice('ir1')
left_ir.enable(TIME_STEP)
    
right_ir = robot.getDevice('ir0')
right_ir.enable(TIME_STEP)
    
# Step simulation

names = set()
idss = set()

avoidObstacleCounter = 0
while robot.step(TIME_STEP) != -1:

    numberOfObjects = camera.getRecognitionNumberOfObjects()
    numberOfObjects1 = camera1.getRecognitionNumberOfObjects()
        
    # read ir sensors
    left_ir_value = left_ir.getValue()
    right_ir_value = right_ir.getValue()
    #print("left: {} right{}".format(left_ir_value, right_ir_value))

    leftSpeed = 2.0
    rightSpeed = 2.0
    
              
    if(left_ir_value > right_ir_value) and (500 < left_ir_value < 1500):
        #print('Go left')
        leftSpeed = -2
                
    elif (right_ir_value > left_ir_value) and (500 < right_ir_value < 1500):
        #print('Go right')
        rightSpeed = -2  
        
                   
    elif (camera.hasRecognition) or (camera1.hasRecognition):#If there are recognizable objects in the image
        my_object = camera.getRecognitionObjects()#Return the object object to my_object        
        my_object1 = camera1.getRecognitionObjects()
        for k in range (numberOfObjects1):
            #print(my_object[k].get_id())
            #print(my_object[k].get_model())
            names.add(my_object1[k].get_model())
            idss.add(my_object1[k].get_id())
      
        for i in range (numberOfObjects):
            #print(my_object[i].get_id())
            #print(my_object[i].get_model())
            names.add(my_object[i].get_model())
            idss.add(my_object[i].get_id())
                            
                    
        with open('tutorial.csv','w', newline='') as csvfile:
            fieldnames = ['Name', 'ID']  
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            
            namess = list(names)
            idd = list(idss)
            
            for (x, z) in zip(names, idd):                                         
                thewriter.writerow({'Name' : x, 'ID' : z}) 
                
            #for x in namess:                                         
                #thewriter.writerow({'name' : x})               
                #print(f'Products found are: {names} {idss} {z}')
                
                
                if avoidObstacleCounter > 0:
                    avoidObstacleCounter -= 1
                    leftSpeed = 0
                    rightSpeed = 0
                       
                elif avoidObstacleCounter <= 0:  # read sensors
                    for i in range(2):
                        if ds[i].getValue() < 950.0:
                            avoidObstacleCounter = 100
                        


                                   
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)

    print(f'Products found are: {names} {idss}')     
# Enter here exit cleanup code.