#!/usr/bin/python3
# Работа с UR10 через CoppeliaSim (V-REP)

import time
from ur_vrep import UR
from time import sleep

def pPosition():
	print("x=%.2f \ty=%.2f \tz=%.2f" % tuple(getPosition()))
	
def pOrientation():
	print("a=%.2f \tb=%.2f \tg=%.2f" % tuple(getOrientation()))

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

cyl = [0.625 - 0.04, 0.275, 0.5]
goal = [-0.8 + 0.04, 0.5, 0.5]
orient = [180, 90, 90]
goalOrient = [180, -90, -90]

step0 = cyl.copy()
step0[0] = 0.5

######################## Ваше решение #######################

ptp([-200, 0, 0, 0, -90, 0])
ptp([-200, -60, 120, -20, -90, 0])
ptp([-200, -60, 135, 100, -20, 0])

lin(getPosition(), orient)

pos1 = getPosition()
pos1[2] = step0[2]
lin(pos1, orient)

pos2 = getPosition()
pos2[1] = step0[1]
lin(pos2, orient)

pos3 = getPosition()
pos3[0] = step0[0]
lin(pos3, orient)

gripperOpen(True)
sleep(1)
lin(cyl, orient)
gripperOpen(False)
sleep(1)

pos4 = getPosition()
pos4[2] += 0.1
lin(pos4, orient)

lin(pos1)
ptp([-200, 0, 0, 0, -90, 0])
sleep(3)
ptp([-20, 0, 0, 0, -90, 0])
sleep(3)
ptp([-20, -60, 120, -20, -90, 0])
sleep(3)
ptp([-20, -60, 135, 100, -20, 0])

pOrientation()

lin(getPosition(), goalOrient)

pos5 = getPosition()
pos5[2] = goal[2]
lin(pos5, goalOrient)

pos6 = getPosition()
pos6[1] = goal[1]
lin(pos6, goalOrient)

pos7 = getPosition()
pos7[0] = goal[0]
pos7[2] += 0.1
lin(pos7, goalOrient)

lin(goal, goalOrient)
gripperOpen(True)
sleep(1)

lin(pos6, goalOrient)


#############################################################
# закомментируйте, если хотите сохранить финальное состояние
# sleep(10)
#ptp([0,0,0,0,0,0])
#robot.stopSimulation()




