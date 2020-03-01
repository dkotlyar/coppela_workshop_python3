# SCARA control in V-REP simulator

import sim as vrep
import math, time, random


# закрыть старые подключения
vrep.simxFinish(-1)
 
################################ Связь с симулятором ############################

clientID = vrep.simxStart('127.0.0.1',19997,True,True,5000,5)  # порт в remoteApiConnections.txt
if clientID!=-1: print ('Connected to remote API server')
    
################################## Указатели ###############################

jointID = [-1,-1,-1,-1]
for i in range(len(jointID)):
    err,h = vrep.simxGetObjectHandle(clientID,'MTB_axis'+str(i+1),vrep.simx_opmode_oneshot_wait)
    if err == -1:
        print ("No joint", i)
    else:
        jointID[i] = h   
        
err,gripperID = vrep.simxGetObjectHandle(clientID,'suctionPad',vrep.simx_opmode_oneshot_wait)  
if err == -1: print ('No sctionPad')  

jointID0 = [-1,-1,-1,-1]
for i in range(len(jointID)):
    err,h = vrep.simxGetObjectHandle(clientID,'MTB_axis'+str(i+1)+'#0',vrep.simx_opmode_oneshot_wait)
    if err == -1:
        print ("No joint", i)
    else:
        jointID0[i] = h   

########################### Методы ##########################

def setPosition(q,ids):
  for i,joint in enumerate(ids):
    vrep.simxSetJointPosition(clientID,joint,q[i],vrep.simx_opmode_oneshot_wait)

# Напишите функцию, которая принимает на вход текущие положение и ориентацию
# инструмента, а также список параметров робота, 
# и возвращает список углов    
def ik(pos,orient,parameters):  
  return [0,0,0,0]

# Определите здесь параметры робота, такие как длины звеньев
# и начальное положение базы  
parameters = []
   
############################# Запуск #############################
          
# включение симулятора
vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)

for i in range(100):
    # генерация случайных углов
    #goal = [random.random(), random.random(), random.random()*0.2, -random.random()]
    goal = [2*random.random()-1, 2*random.random()-1, random.random()*0.08, -random.random()]
    # переход в данное положение
    setPosition(goal,jointID)
    # вывод углов в консоль
    print (goal)
    # положение и ориентация инструмента
    _,pos = vrep.simxGetObjectPosition(clientID,gripperID,-1,vrep.simx_opmode_oneshot_wait)
    _,orient = vrep.simxGetObjectOrientation(clientID,gripperID,-1,vrep.simx_opmode_oneshot_wait)
    # пауза для наглядности
    time.sleep(1)  
    # решение обратной задачи кинематики
    q = ik(pos,orient,parameters)
    # переход в найденное положение
    setPosition(q,jointID0)
    # вывод углов в консоль
    print (q)
    time.sleep(1)
  
############################### Завершение работы ###############################

#vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
#vrep.simxFinish(clientID)
