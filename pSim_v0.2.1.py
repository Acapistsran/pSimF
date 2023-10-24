# import stupid shit
import pygame
import random
import time
import math

# add some variables
pygame.init()
maxX = 1000
maxY = 600
screen = pygame.display.set_mode([maxX, maxY])
running = True
frame = -1


# useful functions
def randX(x=maxX):
    return random.randint(10, x - 10)


def randY(y=maxY):
    return random.randint(10, y - 10)


def randRun(x):
    return random.randint(x * -1, x)


def randRise(y):
    return random.randint(y * -1, y)


def fuckRoot(x):
    return math.sqrt(x)


# important independant variables
particleBook = {
    "proton": [100, 1, (255, 0, 0), 20],
    "electron": [0.1, -1, (0, 0, 255), 5],
    "neutron": [10, 0, (128, 128, 128), 20],
    "neutrino": [1, 0, (128, 128, 128), 5],
    "gluon": [0, 0, (255, 128, 255), 5],
    "roton": [0, 0, (128, 255, 255), 5],
}
reality = {}

# makes x random particles
population = 50
randList = [
    "proton",
    "proton",
    "electron",
    "electron",
    "neutron",
    "neutron",
    "neutron",
    "neutrino",
    "gluon",
    "roton",
]
for i in range(0, population):
    reality["p" + str(i)] = [random.choice(randList), [randX(), randY()], [0, 0]]

while running:
    # frame counting code
    frame += 1
    print("Frame " + str(frame) + " processed.")

    # frame clear and frame rate stuff
    screen.fill((255, 255, 255))
    time.sleep(1 / 60)

    # quit window code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ?????
    pList = list(reality.keys())
    random.shuffle(pList)

    # draws current state of the game
    for particle_id in pList:
        p = reality[particle_id]
        particle_type = p[0]
        particle_Position = (p[1][0], p[1][1])
        particle_mass = particleBook[particle_type][0]
        particle_charge = particleBook[particle_type][1]
        particle_color = particleBook[particle_type][2]
        particle_size = particleBook[particle_type][3]

        pygame.draw.circle(screen, particle_color, particle_Position, particle_size)

    # runs through each particle
    for particle_id in reality.keys():
        # grabs important shit
        p = reality[particle_id]
        particle_type = p[0]
        particle_Position = [p[1][0], p[1][1]]
        particle_velocity = [p[2][0], p[2][1]]
        particle_mass = particleBook[particle_type][0]
        particle_charge = particleBook[particle_type][1]
        particle_color = particleBook[particle_type][2]
        particle_size = particleBook[particle_type][3]

        # sets our acceleration stuff
        velocity_Difference = [0, 0]
        x_acceleration = 0.1
        y_acceleration = 0.1

        # second loop for attractions and rules
        for particle_id2 in reality.keys():
            # more important set up, with some special code for various errors and """"optimizations""""
            otherParticle = reality[particle_id2]
            if p == otherParticle:
                continue
            otherParticleType = otherParticle[0]
            otherParticleVelocity = [otherParticle[2][0], otherParticle[2][1]]
            otherParticlePosition = [otherParticle[1][0], otherParticle[1][1]]
            otherParticleMass = particleBook[otherParticleType][0]
            otherParticleCharge = particleBook[otherParticleType][1]
            otherParticleSize = particleBook[otherParticleType][3]
            x_Offset = particle_Position[0] - otherParticlePosition[0]
            y_Offset = particle_Position[1] - otherParticlePosition[1]
            try:
                Distance = fuckRoot(
                    ((particle_Position[0] - otherParticlePosition[0]) ** 2)
                    + ((particle_Position[1] - otherParticlePosition[1]) ** 2)
                )
            except:
                Distance = 0
            if Distance == 0:
                Distance = 0.0000000001
            Distance2 = Distance**2

            # strange magic rules
            try:
                velocity_Difference[0] += (
                    particle_charge
                    * otherParticleCharge
                    * (particle_Position[0] - otherParticlePosition[0])
                ) / (Distance * particle_mass)
                velocity_Difference[1] += (
                    particle_charge
                    * otherParticleCharge
                    * (particle_Position[1] - otherParticlePosition[1])
                ) / (Distance * particle_mass)
                if Distance <= otherParticleSize:
                    velocity_Difference[0] += (
                        particle_mass
                        * otherParticleMass
                        * (particle_Position[0] - otherParticlePosition[0])
                    ) / (Distance2 * particle_mass)
                    velocity_Difference[1] += (
                        particle_mass
                        * otherParticleMass
                        * (particle_Position[1] - otherParticlePosition[1])
                    ) / (Distance2 * particle_mass)
                    x_acceleration /= 2
                    y_acceleration /= 2
                elif particle_type != otherParticleType:
                    velocity_Difference[0] -= (
                        particle_mass
                        * otherParticleMass
                        * (particle_Position[0] - otherParticlePosition[0])
                    ) / (Distance2 * particle_mass)
                    velocity_Difference[1] -= (
                        particle_mass
                        * otherParticleMass
                        * (particle_Position[1] - otherParticlePosition[1])
                    ) / (Distance2 * particle_mass)
                if otherParticleType == "gluon" and Distance <= particle_size**2:
                    x_acceleration /= -1.5
                    y_acceleration /= -1.5

                    velocity_Difference[0] += otherParticleVelocity[0]
                    velocity_Difference[1] += otherParticleVelocity[1]
                if (
                    otherParticleType == "roton"
                    and Distance <= particle_size**2
                    and particle_velocity[0] == otherParticleVelocity[0]
                    or particle_velocity[1] == otherParticleVelocity[1]
                ):
                    vTemp = velocity_Difference[0]
                    velocity_Difference[0] = velocity_Difference[1] * -1
                    velocity_Difference[1] = vTemp

            except:
                pass

        # barrier parameters
        xNo = 1
        yNo = 1
        xStop = 1
        yStop = 1

        # barrier logic
        if particle_Position[0] < 0:
            xNo = -1
            particle_Position[0] = 10
        elif particle_Position[0] > maxX:
            xNo = -1
            particle_Position[0] = maxX - 10
        if particle_Position[1] < 0:
            yNo = -1
            particle_Position[1] = 10
        elif particle_Position[1] > maxY:
            yNo = -1
            particle_Position[1] = maxY - 10

        # updates position, adds acceleration, sets velocity and a bunch of other crap
        fType = particle_type
        fX = particle_Position[0] + particle_velocity[0] * xNo
        fY = particle_Position[1] + particle_velocity[1] * yNo
        fRun = particle_velocity[0] * x_acceleration * xNo + velocity_Difference[0]
        fRise = particle_velocity[1] * y_acceleration * yNo + velocity_Difference[1]

        reality[particle_id] = [fType, [fX, fY], [fRun, fRise]]

    # ????? came with the template and doesn't work without it, maybe it updates the window?
    pygame.display.flip()

# when the loop breaks the window closes
pygame.quit()
