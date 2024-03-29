import numpy as np
import pybullet as p
import time
import matplotlib.pyplot as plt
import pybullet_data

file = open("box.urdf", 'w')

mass = 1.0
lx= 1.0
ly= 0.5
lz = 0.1
ix = 1/12.0 * mass*(ly*ly+lz*lz)
iy = 1/12.0 * mass*(lx*lx+lz*lz)
iz = 1/12.0 * mass*(lx*lx+ly*ly)

file.write("""
<?xml version="1.0"?>
<robot name="physics">
  <link name="back">
    <visual>
      <geometry>
        <box size="{lx} {ly} {lz}" />
      </geometry>
      <origin rpy="0 0 0" xyz="0 0 0" />
      <material name="blue">
        <color rgba="1.0 1.0 1.0 1" />
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="1.0 0.5 0.1" />
      </geometry>
      <origin rpy="0 0 0" xyz="0 0 0" />
    </collision>
    <inertial>
      <mass value="{mass}" />
      <inertia ixx="{ix}" ixy="0.0" ixz="0.0" iyy="{iy}" iyz="0.0" izz="{iz}"/>
      <origin rpy="0 0 0" xyz="0 0 0" />
    </inertial>
  </link>
</robot>
""".format(lx=lx,ly=ly,lz=lz,mass=mass,ix=ix,iy=iy,iz=iz))
file.close()

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,0)
cubeStartPos = [0,0,0]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("box.urdf",cubeStartPos, cubeStartOrientation)
p.applyExternalTorque(boxId, -1, [0.0, 100.0, 0.05], flags=p.WORLD_FRAME)
p.changeDynamics(boxId, -1, angularDamping=0.001)

rfps = 256
dfps = 256
tmax = 10
p.setTimeStep(1.0 / rfps)
data=[]
pixels = [500, 500]
for i in range (rfps * tmax):
    start = time.time()
    pos, orientation = p.getBasePositionAndOrientation(boxId)
    orientation = p.getEulerFromQuaternion(orientation)
    data.append(orientation)
    p.stepSimulation()
    if i % 10 == 0:
        frame = int(i / 10)
        viewMatrix = p.computeViewMatrix([1,1,1],[0,0,0], [0,0,1])
        projecttionMatrix = p.computeProjectionMatrixFOV(60, pixels[0] / pixels[1], 0.01, 100)
        img_arr = p.getCameraImage(pixels[0], pixels[1], viewMatrix, projecttionMatrix, shadow=1, lightDirection=[1,1,1], renderer=p.ER_BULLET_HARDWARE_OPENGL)
        np_img_arr = np.reshape(img_arr[2], (img_arr[1], img_arr[0], 4))
        np_img_arr = np_img_arr * (1.0 / 255.0)
        plt.imsave("images/{}.png".format(frame), np_img_arr)

    time.sleep(max(1./dfps - (time.time() - start), 0))
p.disconnect()
# plt.plot(data)
# plt.show()
