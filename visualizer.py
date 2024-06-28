import vpython as vp
from subatomic_particles import Particle, Electron, Nucleus

# Customize Visualizer
particle_size_scalar = .1    # Scalar for particle sizes
visualize_path       = False # Trace the path of each particle

particle_colors = {
    Electron: vp.color.blue,  # e- color
    Nucleus: vp.color.red    # nucleus color
}

vp.canvas( 
    width = 1280, 
    height = 720
) # Canvas size


def visualize_particle(particle: Electron | Nucleus) -> None:
    x, y, z = particle.get_pos()
    atom_type = type(particle)

    if atom_type == Electron:
        r = particle_size_scalar
    if atom_type == Nucleus:
        r = particle_size_scalar * particle.get_protons() * 2

    return vp.sphere(
            pos        = vp.vector(x, y, z),
            color      = particle_colors.get(atom_type),
            radius     = r,
            make_trail = visualize_path
        )

def update_particle(obj: vp.sphere, particle: Electron | Nucleus):
    x, y, z = particle.get_pos()
    obj.pos = vp.vector(x, y, z)