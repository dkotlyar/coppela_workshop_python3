# Communication with CoppeliaSim

#import vrep
import sim as vrep
import time, math

       
class UR:
  def __init__(self,port):
    # just in case, close all opened connections
    vrep.simxFinish(-1)
    # connect, get scene handl
    self.clientId = vrep.simxStart('127.0.0.1',port,True,True,5000,5) 
    assert (self.clientId != -1), "Impossible to connect!"
    print ("Connected to remote API server")
    # get joints
    self.jointNo = range(6)
    self.jointId = [-1,-1,-1,-1,-1,-1]
    for i in self.jointNo:
      err,h = vrep.simxGetObjectHandle(self.clientId,'UR10_joint'+str(i+1),vrep.simx_opmode_oneshot_wait)
      assert (err != -1), "No joint "+str(i)+" found!"
      self.jointId[i] = h
    # get gripper
    err,self.gripperId = vrep.simxGetObjectHandle(self.clientId,'RG2',vrep.simx_opmode_oneshot_wait)
    assert (err != -1), "No gripper found!"
    # get tip
    err,self.tipId = vrep.simxGetObjectHandle(self.clientId,'tip',vrep.simx_opmode_oneshot_wait)
    assert (err != -1), "No tip found!"
      
  # Start process
  def startSimulation(self):
    # start simulation
    vrep.simxStartSimulation(self.clientId, vrep.simx_opmode_blocking)
    self.begin = time.time()
    time.sleep(2)
    
  # Stop and exit program
  def stopSimulation(self):
    print("Time:", time.time()-self.begin)
    vrep.simxStopSimulation(self.clientId, vrep.simx_opmode_blocking)
    vrep.simxFinish(self.clientId)
    
  def ptp(self,_joints):
    joints = [math.radians(x) for x in _joints]
    ba = bytearray()
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],joints,['ptp'],ba, vrep.simx_opmode_blocking)
    while True:  # waiting for result
      res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'isReached',[],[],[''],ba, vrep.simx_opmode_blocking)
      if res[1][0] == 1: break
      time.sleep(0.1)
     
                                              
  def lin(self,pos,_orient=[]):
    ba = bytearray()
    orient = [math.radians(x) for x in _orient]
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],pos+orient,['lin'],ba, vrep.simx_opmode_blocking)
    while True:   # waiting for result
      res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'isReached',[],[],[''],ba, vrep.simx_opmode_blocking)
      if res[1][0] == 1: break
      time.sleep(0.1)
    
    
  def getJointPosition(self):
    res = [-1,-1,-1,-1,-1,-1]
    for i in self.jointNo:
      err,v = vrep.simxGetJointPosition(self.clientId,self.jointId[i],vrep.simx_opmode_oneshot_wait)
      assert (err != -1), "Can't get position"
      res[i] = v
    return [math.degrees(x) for x in res]
    
      
  # Open gripper if flag is True, close otherwise
  def gripperOpen(self,flag):
    vrep.simxSetIntegerSignal(self.clientId,'RG2_open',flag,vrep.simx_opmode_oneshot_wait)
    time.sleep(0.5)
      
  # Get current tool position    
  def getPosition(self):
    err,pos = vrep.simxGetObjectPosition(self.clientId,self.tipId,-1,vrep.simx_opmode_oneshot_wait)
    assert (err != -1), "Can't get position!"
    return pos
  
  # Get current tool orientation  
  def getOrientation(self):
    err,orient = vrep.simxGetObjectOrientation(self.clientId,self.tipId,-1,vrep.simx_opmode_oneshot_wait)
    assert (err != -1), "Can't get orientation!"
    return [math.degrees(x) for x in orient]
  
  # Define coefficients of proportionality for cartesian velocity limits  
  def setCvel(self,x=1,y=1,z=1,a=1):
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],[x,y,z,a],['cvel'],bytearray(), vrep.simx_opmode_blocking)
  
  # Define coefficients of proportionality for cartesian acceleration limits                                       
  def setCacc(self,x=1,y=1,z=1,a=1):
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],[x,y,z,a],['cacc'],bytearray(), vrep.simx_opmode_blocking)
  
  # Define coefficients of proportionality for cartesian jerk limits    
  def setCjerk(self,x=1,y=1,z=1,a=1):
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],[x,y,z,a],['cjerk'],bytearray(), vrep.simx_opmode_blocking)
  
  # Define coefficients of proportionality for joint velocity limits                                      
  def setJvel(self,q1=1,q2=1,q3=1,q4=1,q5=1,q6=1):
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],[q1,q2,q3,q4,q5,q6],['jvel'],bytearray(), vrep.simx_opmode_blocking)
  
  # Define coefficients of proportionality for joint acceleration limits
  def setJacc(self,q1=1,q2=1,q3=1,q4=1,q5=1,q6=1):
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],[q1,q2,q3,q4,q5,q6],['jacc'],bytearray(), vrep.simx_opmode_blocking)
  
  # Define coefficients of proportionality for joint jerk limits
  def setJjerk(self,q1=1,q2=1,q3=1,q4=1,q5=1,q6=1):
    res = vrep.simxCallScriptFunction(self.clientId,'UR10',vrep.sim_scripttype_childscript,
                                      'setRobotGoal',[],[q1,q2,q3,q4,q5,q6],['jjerk'],bytearray(), vrep.simx_opmode_blocking)
  
  
      
  
  