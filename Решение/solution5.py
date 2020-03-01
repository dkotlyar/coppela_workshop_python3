#!/usr/bin/python3
# Работа с UR10 через CoppeliaSim (V-REP)

import time
from ur_vrep import UR
from time import sleep

orient = [0, -180, 90]

def pPosition():
	print("x=%.2f \ty=%.2f \tz=%.2f" % tuple(getPosition()))
	
def pOrientation():
	print("a=%.2f \tb=%.2f \tg=%.2f" % tuple(getOrientation()))
	
def pick(n, start, dX):
	x = int(n/4)
	y = n % 4
	pos = start.copy()
	pos[2] = 0.7
	pos[0] += x * dX
	pos[1] += y * dY
	lin(pos, orient)
	gripperOpen(True)
	sleep(1)
	pos2 = pos.copy()
	pos2[2] = start[2]
	lin(pos2, orient)
	gripperOpen(False)
	sleep(1)
	lin(pos, orient)
	
def place(x, y):
	pos = px0.copy()
	pos[2] = 0.6
	pos[0] += x * dPX
	pos[1] += y * dPX
	lin(pos, orient)
	pos2 = pos.copy()
	pos2[2] = px0[2]
	lin(pos2, orient)
	gripperOpen(True)
	sleep(1)
	lin(pos, orient)

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

px0 = [-0.94, 0.235, 0.5]
dPX = 0.12


white0 = [-0.425, -0.075, 0.5]
black0 = [0.025, -0.075, 0.5]
dY = -0.1
dXw = 0.15
dXb = 0.125

picture = [[0, 1, 0, 1, 0],
		   [1, 0, 1, 0, 1],
		   [0, 1, 0, 1, 0],
		   [1, 0, 1, 0, 1],
		   [0, 1, 0, 1, 0]]

# picture = [[0, 1, 0, 1, 0],
		   # [0, 1, 0, 1, 0],
		   # [0, 0, 0, 0, 0],
		   # [1, 0, 0, 0, 1],
		   # [0, 1, 1, 1, 0]]

bN = 11
wN = 11

######################## Ваше решение #######################

joints = getJoints()

for x in range(0, 5):
	for y in range(0, 5):
		px = picture[x][y]
		if (px == 1):
			if (wN < 0):
				print("Фишки закончились")
			else:
				pick(wN, white0, dXw)
				wN -= 1
		else:
			if (bN < 0):
				print("Фишки закончились")
			else:
				pick(bN, black0, dXb)
				bN -= 1
		place(x, y)	

ptp(joints)


#############################################################
# закомментируйте, если хотите сохранить финальное состояние
# ptp([0,0,0,0,0,0])
# robot.stopSimulation()




