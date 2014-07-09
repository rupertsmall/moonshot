# some functions to give statistics on the satellite's orbit, based on the coordinate data
# which is given as output from the moonshot_cartesian.py program


from math import sqrt

#does satellite hit earth
def hits_earth():
    radius_earth = 6371000.0
    radius_moon = 1737100.0
    d = 3840000000.0    #distance between the earth and moon 
    np = open('moon_shot.txt','r')
    hits = False
    for eachline in np:
        x=float(eachline.split()[0])
        y=float(eachline.split()[1])
        distance = sqrt(x**2 + y**2)
        if distance <= radius_earth: hits = True
    np.close()
    return hits

#does satellite hit moon
def hits_moon():
    radius_earth = 6371000.0
    radius_moon = 1737100.0
    d = 3840000000.0    #distance between the earth and moon 
    np = open('moon_shot.txt','r')
    hits = False
    for eachline in np:
        x=float(eachline.split()[0])
        y=float(eachline.split()[1])
        distance = sqrt(x**2 + (y-d)**2)
        if distance <=radius_moon: hits = True
    np.close()
    return hits


#does the satellite pass within the 500km band
def within_band():
    radius_earth = 6371000.0
    radius_moon = 1737100.0
    d = 3840000000.0    #distance between the earth and moon 
    np = open('moon_shot.txt','r')
    within_band = False
    for eachline in np:
        x=float(eachline.split()[0])
        y=float(eachline.split()[1])
        distance = sqrt(x**2 + (y-d)**2)
        if distance < radius_moon + 500000: within_band = True
    np.close()
    return within_band


#minimum distance to moon's surface
def min_moon():
    radius_earth = 6371000.0
    radius_moon = 1737100.0
    d = 3840000000.0    #distance between the earth and moon 
    min_distance = d
    np = open('moon_shot.txt','r')
    for eachline in np:
        x=float(eachline.split()[0])
        y=float(eachline.split()[1])
        distance = sqrt(x**2 + (y-d)**2) - radius_moon
        if min_distance > distance:
            min_distance = distance
        if min_distance < 0:
            min_distance = 0
    np.close()
    return min_distance

#minimum distance to earth's surface on return
def min_earth():
    radius_earth = 6371000.0
    radius_moon = 1737100.0
    d = 3840000000.0    #distance between the earth and moon 
    min_distance = d
    np = open('moon_shot.txt','r')
    index=0         #line number -- make sure enough time has passed before checking if particle is close to earth again
    for eachline in np:
        if index > 30000:
            x=float(eachline.split()[0])
            y=float(eachline.split()[1])
            distance = sqrt(x**2 + y**2) - radius_earth
            if min_distance > distance:
                min_distance = distance
            if min_distance < 0:
                min_distance = 0
        index += 1
    np.close()
    return min_distance

#time taken to reach a certain distance from the earth's surface
def time_taken(m, dt):
    EPSILON = 25 #allowed error in position
    index=0
    index2=0
    radius_earth = 6371000.0
    np=open('moon_shot.txt','r')
    for eachline in np:
        x = float(eachline.split()[0])
        y = float(eachline.split()[1])
        if abs(m - sqrt(x**2 + y**2) + radius_earth) < EPSILON: index2=index
        index += 1
    return index2*dt/3600.0
    np.close()



if __name__ == '__main__':      #only run if called directly

#use library functions to print statistics:
    if hits_earth(): print 'satellite hits earth'
    else: print "satellite doesn't hit earth"
    if hits_moon(): print 'satellite hits moon'
    else: print "satellite doesn't hit moon"
    if within_band(): print 'satellite passes within 500km of moon'
    else: print "satellite doesn't pass within 500km of moon"
    print 'min distance to moon: ', min_moon()
    print 'min distance to earth: ', min_earth()
