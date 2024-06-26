import pybullet as p
import time

import pybullet_data

p.connect(p.GUI)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath('..')
p.setAdditionalSearchPath(pybullet_data.getDataPath())
fixed = True #False
humanoid = p.loadURDF("urdf/digit_model.urdf", useFixedBase=fixed, basePosition=[0, 0, 1])
plane = p.loadURDF("plane.urdf") 

# gravId = p.addUserDebugParameter("gravity", -10, 10, 0)
jointIds = []
paramIds = []

p.setPhysicsEngineParameter(numSolverIterations=10)
p.changeDynamics(humanoid, -1, linearDamping=0, angularDamping=0)

for j in range(p.getNumJoints(humanoid)):
  p.changeDynamics(humanoid, j, linearDamping=0, angularDamping=0)
  info = p.getJointInfo(humanoid, j)
  #print(info)
  jointName = info[1]
  jointType = info[2]
  if (jointType == p.JOINT_PRISMATIC or jointType == p.JOINT_REVOLUTE):
    jointIds.append(j)
    paramIds.append(p.addUserDebugParameter(jointName.decode("utf-8"), -4, 4, 0))

p.setRealTimeSimulation(1)
while (1):
  # p.setGravity(0, 0, p.readUserDebugParameter(gravId))
  for i in range(len(paramIds)):
    c = paramIds[i]
    targetPos = p.readUserDebugParameter(c)
    p.setJointMotorControl2(humanoid, jointIds[i], p.POSITION_CONTROL, targetPos, force=5 * 240.)
  p.stepSimulation()
  time.sleep(0.001)