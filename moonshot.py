#Moon shot.

from math import sqrt, sin, cos, tan, exp, atan, pi


#HARD-WIRED CONSTANTS: 
dt = 5                      #step size in seconds
r0 = 7000000.0              #radius of near earth orbit in meters 
mass_earth = 5.9736e24      #in kilograms
mass_moon = 7.347e22        #in kilograms
radius_earth = 6371000.0    #in meters
radius_moon = 1737100.0     #in meters
d = 3840000000.0            #distance between center of moon and center of earth in meters
G = 6.67259e-11             #universal gravitational constant


#functions for working out the dynamics of the situation

def next_accell_theta(r, theta):
    whats_needed = 0 #-G*mass_moon*cos(theta + atan((d+r*cos(theta))/(r*sin(theta))))/(((d+r*cos(theta))**2 + (r*sin(theta)**2))*r)
    return whats_needed

def next_accell_r(r, theta, dtheta):
    whats_needed = -G*(mass_earth/r**2) #+ mass_moon*sin(theta + atan((d+r*cos(theta))/(r*sin(theta))))/((d+r*cos(theta))**2 + (r*sin(theta))**2)
    return whats_needed

def next_theta_velocity(r, theta, dtheta): 
    change = dt*next_accell_theta(r, theta) 
    next_dtheta = dtheta + change
    return next_dtheta

def next_r_velocity(r, theta, dr, dtheta):
    change = dt*next_accell_r(r, theta, dtheta)
    next_dr = dr + change
    return next_dr

def next_theta(theta, dtheta):
    change = dt*dtheta    
    theta = theta + change
    return theta

def next_r(r, dr):
    change = dt*dr
    r = r + change
    return r        

def next_t(t):
    return t+dt


#MORE CONSTANTS
INITIAL_BURN_VEL = 0
BURN_FINAL = 1000                  #meters per second
BURN_STEP = 50
THETA_START = 0.0000001
ANGLE_STEP = pi/32
THETA_END = pi/34
time_end = 2                       #in hours 
v_burn = INITIAL_BURN_VEL
theta_outer = THETA_START

#MAIN PRORGAM LOOP
while theta_outer <= THETA_END:
    while v_burn <= BURN_FINAL:
        theta_inner = theta_outer
        dtheta = v_burn/r0          #set dtheta/dt at t=0
        r=r0
        dr = 0                      #set dr/dt at t=0
        t=0
        fp = open('g'+str(theta_outer)+'_'+str(v_burn)+'.txt', 'a')
        fp.write(str(theta_inner) + '\t\t' + str(r) + '\n')
        while t/3600.0 < time_end:
            r = next_r(r,dr)
            theta_inner = next_theta(theta_inner, dtheta)
            dr = next_r_velocity(r, theta_inner, dr, dtheta)
            dtheta = next_theta_velocity(r, theta_inner, dtheta)
            fp.write(str(theta_inner) + '\t\t' + str(r) + '\n')
            t = next_t(t)
        fp.close()
        v_burn += BURN_STEP
    v_burn = INITIAL_BURN_VEL #initialize back to initial value for next iteration
    theta_outer += ANGLE_STEP

#do loops again to create gnuplot files and shell script
theta = THETA_START
v_burn = INITIAL_BURN_VEL
shell_file_pointer = open('gnuplot_shell_script', 'a')
while theta <= THETA_END:
    np = open('g'+str(theta)+'_gnuplot_file.txt', 'a')
    np.write('''set terminal postscript colour eps
set title "Moon Shot"
set output "'''+'g'+str(theta)+'_gnuplot_file.eps"\n'+\
'''set grid
set title "'''+str(theta)+'''"
set polar
plot ''')
    shell_file_pointer.write('gnuplot '+ 'g'+str(theta)+'_gnuplot_file.txt\n') 
    while v_burn <= BURN_FINAL:
        np.write('"g'+str(theta)+'_'+str(v_burn)+'.txt" title "'+str(v_burn)+'" with lines, ')
        v_burn += BURN_STEP
    np.write('"null_file.txt"') #work-around for the comma at the end of the line
    v_burn = INITIAL_BURN_VEL  #initialize back to initial burn velocity for next iteration
    np.close()
    theta += ANGLE_STEP
    
shell_file_pointer.close()
