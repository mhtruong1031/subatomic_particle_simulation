import visualizer as vis
import subatomic_particles as sp
import vpython as vp

from time import sleep

# Customize Simulation
force_scalar = 1e-4
time_step = 5e-3

def main() -> None:
    nuc1 = sp.Nucleus(
        protons = 1,
        pos     = (-1, 0, 0),
    )
    e1 = sp.Electron(
        pos = (-.75, 1, 0),
        vel = (1e-2, 1e-2, 1e-1)
    )
    nuc2 = sp.Nucleus(
        protons = 1,
        pos     = (1, 0, 0),
    )
    e2 = sp.Electron(
        pos = (.75, 1, 0),
        vel = (1e-2, 1e-2, 1e-1)
    )
    particles = [nuc1, e1, nuc2, e2]


    visualizations = []
    for p in particles:
        p.set_tme(particles)
        visualizations.append(vis.visualize_particle(p))

    while True:
        tick(particles, visualizations, time_step)
        vp.rate(5000)


def tick(particles, visualizations, dt) -> None:
    for p in particles:
        for p_ in particles:
            if p_ is not p:
                p.apply_force(p_, force_scalar) # Apply forces from all objects

    for i in range(len(particles)):
        particles[i].update(dt, particles)
        vis.update_particle(visualizations[i], particles[i])


if __name__ == '__main__':
    main()