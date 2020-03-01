#!/usr/bin/python3
# Работа с UR10 через CoppeliaSim (V-REP)

import time
from ur_vrep import UR
from time import sleep

def pick(pos, orient):
	(x, y, z) = pos
	
	z += zOffset
	
	gripperOpen(True)
	sleep(1)

	lin([x, y, z + zOffset], orient)
	lin([x, y, z], orient)

	gripperOpen(False)
	sleep(1)

	lin([x, y, z + zOffset], orient)
	
def place2(pos, orient):
	(x, y, z) = pos
	
	z += zOffset
	
	(x0, y0, z0) = getPosition()
	lin([x, y, z0], orient)

	lin([x, y, z + zOffset], orient)
	lin([x, y, z], orient)

	gripperOpen(True)
	sleep(1)

	lin([x, y, z + zOffset], orient)
	

##################### Настройка ###############################

# номер порта указан в remoteApiConnections.txt
port = 19997

################### Интерфейс взаимодействия #################

robot = UR(port) 

################ Синонимы для вызова функций ##################

#		движение
ptp = robot.ptp					# движение к положению в пространстве конфигураций, например ptp([1,2,3,4,5,6])
lin = robot.lin					# переход к положению и ориентации в декартовом пространстве, например lin([0.1,0.2,0.3],[40,50,60])
						# или движение с постоянной ориентацией, например lin([0.1,0.2,0.3])
#		инструмент
gripperOpen = robot.gripperOpen			# открыть/закрыть захват, например gripperOpen(True)
#		текущее состояние
getJoints = robot.getJointPosition		# определить углы в осях
getPosition = robot.getPosition			# определить положение инструмента в декартовом пространстве
getOrientation = robot.getOrientation		# определить ориентацию в декартовом пространстве
#		установки
setCvel = robot.setCvel				# задать коэффициент изменения скорости в декартовом пространстве, например setCvel(x=2)
setCacc = robot.setCacc				# задать коэффициент изменения ускорения в декартовом пространстве, например setCacc(y=3)
setJvel = robot.setJvel				# задать коэффициент изменения скорости в пространстве конфигураций, например setJvel(q3=0.5)
setJacc = robot.setJacc 			# задать коэффициент изменения ускорения в пространстве конфигураций, например setJacc(q4=3)

#############################################################

robot.startSimulation()

zOffset = 0.04
startPoint = [90,0,-90,30,90,0]
targetPoint = [-90,0,-90,30,90,-180]

yellowCube = [0.6, 0.4, 0.28]
redCube = [0.6, 0.4, 0.2]
greenCube = [0.6, 0.4, 0.12]
blueCube = [0.6, 0.4, 0.04]

orient = [0, -180, 90]

######################## Ваше решение #######################

ptp(startPoint)

tmpPos = 0.8
cubesDestroy = [yellowCube, redCube]
cubesAssembly = [greenCube, yellowCube, blueCube, redCube]

for cube in cubesDestroy:
	sleep(1)

	pick(cube, orient)

	cube[2] = 0.04
	cube[0] = tmpPos

	place2(cube, orient)
	
	tmpPos += 0.2
	
tmpPos = 0.04
	
for cube in cubesAssembly:
	ptp(startPoint)
	
	sleep(1)

	pick(cube, orient)

	cube[0] = -0.6
	cube[1] = 0.4
	cube[2] = tmpPos
	
	ptp(targetPoint)

	place2(cube, orient)
	
	tmpPos += 0.08
	

#############################################################
# закомментируйте, если хотите сохранить финальное состояние
sleep(10)
#ptp([0,0,0,0,0,0])
robot.stopSimulation()




