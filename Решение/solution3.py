#!/usr/bin/python3
# Работа с UR10 через CoppeliaSim (V-REP)

import time
from ur_vrep import UR
from time import sleep

yOffset = 0.035
zOffset = 0.035

def pick(pos, orient):
	(x, y, z) = pos
	
	y += yOffset
	
	gripperOpen(True)
	sleep(1)

	lin([x, y + yOffset, z], orient)
	lin([x, y, z], orient)

	gripperOpen(False)
	sleep(1)

	lin([x, y, z + zOffset], orient)
	
def place2(pos, orient):
	(x, y, z) = pos
	
	z += zOffset
	
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

startJoints = [0, 30, -90, -90, -90, 0]
goalJoints = [-90, 0, -90, 0, 90, 0]

pickPosition = [-0.203, -0.5, 0.3748]
pickOrient = [90, 0, 180]

goalOrient1 = [0, -180, 0]
goalOrient2 = [0, -180, -90]
goal1 = [-0.725, 0.4, 0.025]
goal2 = [-0.875, 0.4, 0.025]
goal3 = [-0.8, 0.475, 0.075]
goal4 = [-0.8, 0.325, 0.075]
goal5 = [-0.725, 0.4, 0.125]
goal6 = [-0.875, 0.4, 0.125]

######################## Ваше решение #######################

goals = [(goal1, goalOrient1), (goal2, goalOrient1), (goal3, goalOrient2), (goal4, goalOrient2), (goal5, goalOrient1), (goal6, goalOrient1)]


for goal, orient in goals:
	ptp(startJoints)
	pick(pickPosition, pickOrient)
	ptp(goalJoints)
	place2(goal, orient)
	
ptp(startJoints)


#############################################################
# закомментируйте, если хотите сохранить финальное состояние
sleep(10)
#ptp([0,0,0,0,0,0])
robot.stopSimulation()




