from environment import *
from driver import *
from robot import *
from mcl import *
#Plotting requires matplotlib.
import matplotlib
matplotlib.use('GTK') #Feel free to change the backend
#['ps', 'Qt4Agg', 'GTK', 'GTKAgg', 'svg', 'agg', 'cairo', 'MacOSX', 'GTKCairo', 'WXAgg', 'TkAgg', 'QtAgg', 'FltkAgg', 'pdf', 'CocoaAgg', 'emf', 'gdk', 'template', 'WX']
import matplotlib.pyplot as plt
from math import pi
def makeEnviron():
  e = Environment([])
  for x in range(5):
    for y in range(5):
      e.obstacles.append(Rect(2*x,2*y,1,1))
  return e
def makeEnviron2():
  O = []
  O.append(Rect(1,0,1,1))
  O.append(Rect(0,2,1,1))
  O.append(Rect(2,2,1,1))
  O.append(Rect(4,0,1,3))
  O.append(Rect(0,4,1,1))
  O.append(Rect(2,4,3,1))

  B = Boundary(-1,-1,7,7)
  O.append(B)
  e = Environment(B,O)
  return e

def makeMotion1(v_max=5,w_max=6):
  a1=0.05 #v->vr
  a2=0.05 #w->vr
  a3=0.008#v->wr
  a4=0.01 #w->wr
  a5=0.002#v->gr
  a6=0.005#w->gr
  mot = Robot_Motion_Model(a1,a2,a3,a4,a5,a6, v_max=v_max, w_max=w_max)
  return mot
def makeMotion2(v_max=5,w_max=6):
  a1=0.20 #v->vr
  a2=0.20 #w->vr
  a3=0.01 #v->wr
  a4=0.02 #w->wr
  a5=0.004#v->gr
  a6=0.010#w->gr
  mot = Robot_Motion_Model(a1,a2,a3,a4,a5,a6, v_max=v_max, w_max=w_max)
  return mot

def testdriver1():
  env = makeEnviron2()
  env.plot(plt)
  P = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,1),(3,1),(3,0.5),(3.25,0),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]
  plt.ion()
  plt.show()

  mot = Robot_Motion_Model()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=0,fov=pi/8)
  start_pose = Pose(0.5,1.5,2.8)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  #print(r)
  driver = Robot_Driver(r,P,v_max = 20, w_max = 3)
  while (not driver.finished):
    u = driver.next_control()
    #print(u)
    r.tick(u,driver.dt)
    #print(driver.count)
    r.plot(plt)

  plt.ioff()
  plt.show()
def testdriver2():
  env = makeEnviron2()
  env.plot(plt)
  P = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]
  plt.ion()
  plt.show()

  mot = makeMotion()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=4,fov=pi/8)
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  #print(r)
  driver = Robot_Driver(r,P,v_max = 5, w_max = 6)
  while (not driver.finished):
    u = driver.next_control()
    #print(u)
    r.tick(u,driver.dt)
    #print(driver.count)
    r.plot(plt)

  plt.ioff()
  plt.show()
def testlaser1():
  env = Environment([Rect(4,0,1,3)])
  env.plot(plt)
  plt.ion()
  plt.show()

  mot = Robot_Motion_Model()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=4,fov=pi/8)
  start_pose = Pose(3,0.5,0)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  print(r)
  r.tick((0,0),0.1)
  r.plot(plt)

  plt.ioff()
  plt.show()
def testmotion1():
  env = makeEnviron2()
  env.plot(plt)
  plt.ion()
  plt.show()

  mot = makeMotion()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=0,fov=pi/8)
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,mot,odom,meas,start_pose)
  r.tick((0,0),0.1)
  r.plot(plt)
  path = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]

  P0 = []
  for i in range(100):
    p_temp = Particle(env,mot,meas,start_pose)
    #p_temp.plot(plt)
    P0.append(p_temp)

  P = [P0]
  i = 0

  driver = Robot_Driver(r,path,v_max = 5, w_max = 6)
  while (not driver.finished):
    u_command = driver.next_control()
    P_temp = []
    for p in P[i]:
      p_temp = p.sample_mov(u_command,0.1)
      p_temp.plot(plt)
      P_temp.append(p_temp)
    P.append(P_temp)
    i = i + 1
      
    #u = r.mot.sample_motion(u_command,r.x,0.1)
    #plt.plot(u.x,u.y,'b.')
    r.tick(u_command,driver.dt)
    r.plot(plt)


  plt.ioff()
  plt.show()

def testmotion2(u = (5,3)):
  env = Environment([Rect(-10,-10,20,20)])#for reference
  env.plot(plt)
  mot = makeMotion1()
  odom = Robot_Odometry_Model()
  meas = Robot_Measurement_Model(measure_count=0,fov=pi/8)
  start_pose = Pose(0.5,1.5,0.5)

  p1 = Particle(env,mot,meas,start_pose)
  p1.plot(plt)
  P0 = []
  for i in range(10):
    p_temp = p1.sample_mov(u,0.2)
    p_temp.plot(plt)
    P0.append(p_temp)
  P = [P0]
  for i in range(10):
    P_temp = []
    for p in P[i]:
      p_temp = p.sample_mov(u,0.1)
      p_temp.plot(plt)
      P_temp.append(p_temp)
    P.append(P_temp)
  plt.ioff()
  plt.show()
def mcl1():
  env = makeEnviron2()
  env.plot(plt)
  v_max = 5
  w_max = 6
  sim_mot = makeMotion1(v_max,w_max)
  part_mot = makeMotion1(v_max,w_max)
  odom = Robot_Odometry_Model()
  sim_meas = Robot_Measurement_Model(measure_count=3,fov=pi/2,sd_hit=0.1)
  part_meas = Robot_Measurement_Model(measure_count=3,fov=pi/2,sd_hit=0.1)
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,sim_mot,odom,sim_meas,start_pose)
  r.tick((0,0),0.1)
  r.plot(plt)
  path = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5),(0.5,-1),(3.5,-1),(3.5,1.5),(1.5,1.5),(1.5,5.5)]

  P0 = []
  for i in range(100):
    p_temp = Particle(env,part_mot,part_meas,start_pose)
    P0.append(p_temp)

  P = [Particle_Collection(P0,env,part_mot,part_meas)]
  i = 0
  plt.ion()
  plt.show()

  driver = Robot_Driver(r,path,v_max = v_max, w_max = w_max)
  while (not driver.finished):
    u_command = driver.next_control()
    r.tick(u_command,driver.dt)
    Z = r.Z
    P_new = P[i].sample_mov(u_command,driver.dt)
    P_resampled = P_new.KLD_resample(Z,0.15,1.35)
    P.append(P_resampled)
    i = i + 1


    plt.figure(0)
    plt.clf()
    env.plot(plt)
    P_new.plot(plt,p_rgb)
    r.plot(plt)
    plt.draw()

    plt.figure(1)
    plt.clf()
    plt.hist(P_new.W)
    plt.draw()

  plt.ioff()
  plt.show()
def mcl2():
  env = makeEnviron2()
  v_max = 5
  w_max = 6
  sim_mot = makeMotion1(v_max,w_max)
  #part_mot = makeMotion1(v_max,w_max)
  part_mot=sim_mot
  odom = Robot_Odometry_Model()
  sim_meas = Robot_Measurement_Model(measure_count=4,fov=pi/2,sd_hit=0.2)
  #part_meas = Robot_Measurement_Model(measure_count=4,fov=pi/2,sd_hit=0.4)
  part_meas=sim_meas
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,sim_mot,odom,sim_meas,start_pose)
  r.tick((0,0),0.1)
  path = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]

  P0 = Particle_Collection([],env,part_mot,part_meas)
  P0.draw_n_random(300)
  #print([str(p) for p in P0.P])
  P = [P0]
  i = 0
  plt.ion()

  driver = Robot_Driver(r,path,v_max = v_max, w_max = w_max)
  while (not driver.finished):
    u_command = driver.next_control()
    r.tick(u_command,driver.dt)
    Z = r.Z
    P_new = P[i].sample_mov(u_command,driver.dt)
    P_resampled = P_new.resample(Z)
    P.append(P_resampled)
    i = i + 1

    plt.figure(0)
    plt.clf()
    env.plot(plt)
    P_new.plot(plt,p_rgb)
    r.plot(plt)
    plt.draw()
    plt.figure(1)
    plt.clf()
    plt.hist(P_new.W)
    plt.draw()
  plt.ioff()
  plt.show()
def mcl3():
  env = makeEnviron2()
  v_max = 5
  w_max = 6
  sim_mot = makeMotion1(v_max,w_max)
  #part_mot = makeMotion1(v_max,w_max)
  part_mot=sim_mot
  odom = Robot_Odometry_Model()
  sim_meas = Robot_Measurement_Model(measure_count=2,fov=pi/2,sd_hit=0.2)
  #part_meas = Robot_Measurement_Model(measure_count=4,fov=pi/2,sd_hit=0.4)
  part_meas=sim_meas
  start_pose = Pose(0.5,1.5,0)

  r = Robot_Sim(env,sim_mot,odom,sim_meas,start_pose)
  r.tick((0,0),0.1)
  path = [(0.5,1.5),(2.5,1.5),(2.5,0.5),(3.5,0.5),(3.5,3.5),(1.5,3.5),(1.5,1.5),(0.5,1.5)]

  P0 = Particle_Collection([],env,part_mot,part_meas)
  P0.draw_n_random(100)
  #print([str(p) for p in P0.P])
  P = [P0]
  i = 0
  plt.ion()

  driver = Robot_Driver(r,path,v_max = v_max, w_max = w_max)
  while (not driver.finished):
    u_command = driver.next_control()
    r.tick(u_command,driver.dt)
    Z = r.Z
    P_new = P[i].sample_mov(u_command,driver.dt)
    P_resampled = P_new.KLD_resample(Z,0.15,1.45)
    P.append(P_resampled)
    i = i + 1

    plt.figure(0)
    plt.clf()
    env.plot(plt)
    P_new.plot(plt,p_rgb)
    #P_resampled.plot(plt,'b')
    r.plot(plt)
    plt.draw()
    plt.figure(1)
    plt.clf()
    plt.hist(P_new.W)
    plt.draw()
  plt.ioff()
  plt.show()
def test_random_particle():
  env = makeEnviron2()
  env.plot(plt)
  plt.ion()
  plt.show()
  for i in range(1000):
    x = env.B.x + uniform(-1,env.B.width+2)
    y = env.B.y + uniform(-1,env.B.height+2)
    if (not env.inside(x,y)):
      plt.plot(x,y,"g.")
    else:
      plt.plot(x,y,"r.")
    plt.draw()
  plt.ioff()
def p_rgb(p):
  p_inv = 1.0-p
  g = min([p,1.0]) * 255
  b = min([p_inv*255,1.0]) * 255
  r = p_inv * 255 
  #print("r",r,"g",g,"b",b)
  return "#%.2X%.2X%.2X" % (r,g,b)

def test_measurement_prob():
  env = makeEnviron2()
  env.plot(plt)

  meas = Robot_Measurement_Model(measure_count=2,fov=pi/8, sd_hit = 0.2)
  pos = Pose(0.5,1.5,0)
  pos.plot(plt)
  plt.ion()
  plt.show()
  Z = meas.sample_measurement(env,pos)
  x_count = 100
  y_count = 100
  for i in range(x_count):
    for j in range(y_count):
      x = env.B.x + env.B.width * i * 1.0/x_count
      y = env.B.y + env.B.height * j* 1.0/y_count
      X = Pose(x,y,pos.th)
      p = meas.measure_prob(env,X,Z)
      #print(x,y,p,p_rgb(p))
      plt.plot(x,y,'.',color=p_rgb(p))
      plt.draw()
  plt.ioff()
  plt.show()

def test_measurement_prob_2():
  env = makeEnviron2()
  env.plot(plt)

  meas = Robot_Measurement_Model(measure_count=1,fov=pi/8, sd_hit = 0.2)
  pos = Pose(0.5,1.5,0)
  pos.plot(plt)
  plt.ion()
  plt.show()
  Z = meas.sample_measurement(env,pos)
  P = Particle_Collection([],env,None,meas)
  for i in range(2000):
    p = P.draw_random()
    z = p.measure_prob(Z)
    p.plot(plt,p_rgb)
    plt.draw()
  plt.ioff()
  plt.show()


if __name__ == "__main__":
  #test_gaussian(plt)
  #test_random_particle()
  #test_measurement_prob_2()
  #mcl1()
  mcl1()
