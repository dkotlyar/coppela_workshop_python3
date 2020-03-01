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
#gripperOpen(True)

######################## Ваше решение #######################

ptp([0,0,0,0,0,0])

print("Координаты в нулевых углах")
pPosition()
pOrientation()

(c1, c2, c3, c4, c5, c6) = getJoints()
c2 -= 50
c3 += 50
c5 += 90

ptp([c1, c2, c3, c4, c5, c6])

print("Начальное положение")
pPosition()
pOrientation()
print

sleep(5)

(x, y, z) = getPosition()
z -= 0.3
lin([x, y, z])

print("Положение на 0.3 м ниже")
pPosition()
pOrientation()
print

sleep(5)

joints = getJoints()
(a, b, g) = getOrientation()
a += 30
g += 30

lin(getPosition(), [a, b, g])

print("Повернутые оси X и Z")
pPosition()
pOrientation()
print

sleep(5)

ptp(joints)

print("Вернулись")
print

setCvel(y=0.5)
(x, y, z) = getPosition()
x = -0.0164
y = 0.375
orient = getOrientation()
orient[2] += 180
lin([x, y, z], orient) 


print("Сдвинулись в плоскости XOY")
pPosition()
pOrientation()
print

sleep(10)

#############################################################
# закомментируйте, если хотите сохранить финальное состояние
#ptp([0,0,0,0,0,0])
#robot.stopSimulation()




