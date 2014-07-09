#Moon shot optimization

from math import sqrt, sin, cos, tan, exp, atan, pi


#HARD-WIRED CONSTANTS: 
dt = 100                     #step size in seconds
r0 = 7000000.0              #radius of near earth orbit in meters 
mass_earth = 5.9736e24      #in kilograms
mass_moon = 7.347e22        #in kilograms
radius_earth = 6371000.0    #in meters
radius_moon = 1737100.0     #in meters
d = 3840000000.0            #distance between center of moon and center of earth in meters
G = 6.67259e-11             #universal gravitational constant


#functions for working out the dynamics of the situation

def next_accell_x(x,y):
    accell_moon_x = -G*(mass_moon*sin(moon_angle(x,y))/(x**2 + (y-d)**2))
    accell_earth_x = -G*(mass_earth*cos(earth_angle(x,y))/(x**2 + y**2))
    needed = accell_earth_x + accell_moon_x
    return needed


def next_accell_y(x,y):
    accell_moon_y = G*(mass_moon*cos(moon_angle(x,y))/(x**2 + (y-d)**2))
    accell_earth_y = -G*(mass_earth*sin(earth_angle(x,y))/(x**2 + y**2))
    needed = accell_earth_y + accell_moon_y
    return needed


def next_dx(x,y,dx): 
    return dx + next_accell_x(x,y)*dt

def next_dy(x,y,dy):
    return  dy + next_accell_y(x,y)*dt

def next_x(x,dx):
    return  x + dx*dt

def next_y(y,dy):
    return  y + dy*dt

def next_t(t):
    return t + dt

def moon_angle(x,y):
    if y < d:
        angle = atan(x/(d-y))
    elif y == d and x>0:
        angle = pi/2
    elif y == d and x<0:
        angle = -pi/2
    else:
        angle = atan(x/(d-y)) + pi    
    return angle

def earth_angle(x,y):
    if (x>0 and y>=0) or (x>0 and y<=0):
        angle = atan(y/x)
    elif x == 0 and y > 0:
        angle = pi/2
    elif x == 0 and y < 0:
        angle = -pi/2
    else:
        angle = atan(y/x) + pi
    return angle

#optimization functions

def within_margin(x,y): #does trajectory pass close enough to moon
    if sqrt(x**2 + (y-d)**2) < radius_moon + 500000 and sqrt(x**2 + (y-d)**2) > radius_moon:
        return True
    else:
        return False    #satellite doesnt pass close enough, or crashes into moon
    
def optimization_surface(velocity, angle, distance_of_closest_pass):    #create a surface of closest pass for each velocity-angle pair
    np=open('within_band.txt','a')
    np.write(str(velocity)+'\t'+str(angle)+'\t'+str(distance_of_closest_pass))
    np.write('\n')
    np.close()

def distance_to_moon(x,y):  #distance between the satellite and the moon
    return sqrt(x**2 + (y-d)**2)

def too_close(x,y):
    if distance_to_moon(x,y) <= radius_moon: return True
    else: return False


#MORE CONSTANTS
INITIAL_BURN_VEL = 10644.0
INITIAL_K = 2.0

#SEARCH BAND -- area in K-V space wherin to search for an optimum trajectory.
K_BAND = .3
VELOCITY_BAND = .8
K_STEP = .01
VELOCITY_STEP = .01

TIME_END = 7000
FINAL_K = INITIAL_K + K_BAND
FINAL_VELOCITY = INITIAL_BURN_VEL + VELOCITY_BAND
K = INITIAL_K

#MAIN PROGRAM LOOP: PLOT OPTIMIZATION SURFACE COORDINATES AND SAVE DATA OF INITIAL VALUES SATISFYING PATH CONDITIONS
while K <= FINAL_K:
    angle = -pi/K
    v_burn = INITIAL_BURN_VEL
    while v_burn <= FINAL_VELOCITY:
        min_distance = d
        optimization_velocity = optimization_angle = False  #default is: not optimum
        t=0
        x = r0*cos(angle)
        y = r0*sin(angle)
        dx = -sin(angle)*v_burn
        dy = cos(angle)*v_burn
        while t/3600.0 < TIME_END: 
            x = next_x(x,dx)
            y = next_y(y,dy)
            dx = next_dx(x,y,dx)
            dy = next_dy(x,y,dy)
            t = next_t(t)
            if min_distance > distance_to_moon(x,y):
                min_distance = distance_to_moon(x,y)
                min_x = x
                min_y = y
            if too_close(x,y):
                min_distance = radius_moon
        if within_margin(min_x,min_y):
            optimization_velocity = v_burn
            optimization_angle = angle
#        elif too_close(min_x,min_y):
#            min_distance = d                            #let d be the "junk value", since accuracy of shot will be proportional to 1/min_distance
        if optimization_velocity:                       #if optimization_velocity has been set
            optimization_surface(optimization_velocity, optimization_angle, min_distance)
        print v_burn, '\t',K, '\t', 1/min_distance

        v_burn += VELOCITY_STEP
    K += K_STEP


#END

