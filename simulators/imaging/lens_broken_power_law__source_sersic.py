import autofit as af
import autolens as al
import autolens.plot as aplt
import os

# This tool allows one to make simulated datasets of strong lenses, which can be used to test example pipelines and
# investigate strong lens modeling where the 'true' answer is known.

# The 'dataset label' is the name of the dataset folder and 'dataset_name' the folder the dataset is stored in, e.g:

# The image will be output as '/autolens_workspace/dataset/dataset_label/dataset_name/image.fits'.
# The noise-map will be output as '/autolens_workspace/dataset/dataset_label/dataset_name/lens_name/noise_map.fits'.
# The psf will be output as '/autolens_workspace/dataset/dataset_label/dataset_name/psf.fits'.

# Setup the path to the autolens_workspace, using a relative directory name.
workspace_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))

# (these files are already in the autolens_workspace and are remade running this script)
dataset_label = "imaging"
dataset_name = "lens_broken_power_law__source_sersic"

# Create the path where the dataset will be output, which in this case is
# '/autolens_workspace/dataset/imaging/lens_sie__source_sersic/'
dataset_path = af.path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=["dataset", dataset_label, dataset_name]
)

# The pixel scale of the image to be simulated
pixel_scales = 0.05

# Simulate a simple Gaussian PSF for the image.
psf = al.kernel.from_gaussian(shape_2d=(11, 11), sigma=0.1, pixel_scales=pixel_scales)

# To simulate the imaging dataset we first create a simulator, which defines the shape, resolution and pixel-scale of the
# image that is simulated, as well as its expoosure time, noise levels and psf.
simulator = al.simulator.imaging(
    shape_2d=(180, 180),
    pixel_scales=pixel_scales,
    sub_size=2,
    exposure_time=300.0,
    psf=psf,
    background_level=0.1,
    add_noise=True,
)

# Setup the lens galaxy's mass (SIE+Shear) and source galaxy light (elliptical Sersic) for this simulated lens.
lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mp.EllipticalBrokenPowerLaw(
        centre=(0.0, 0.0),
        axis_ratio=0.3,
        phi=45.0,
        einstein_radius=1.3,
        inner_slope=1.5,
        outer_slope=2.5,
        break_radius=0.5,
    ),
)

source_galaxy = al.Galaxy(
    redshift=1.0,
    light=al.lp.EllipticalSersic(
        centre=(0.03, 0.03),
        axis_ratio=0.8,
        phi=60.0,
        intensity=0.3,
        effective_radius=1.0,
        sersic_index=2.5,
    ),
)

# Use these galaxies to setup a tracer, which will generate the image for the simulated imaging dataset.
tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

# Lets look at the tracer's image - this is the image we'll be simulating.

# To make this figure, we need to pass the plotter a grid which it uses to create the image. The simulator has its
# grid accessible as a property, which we can use to do this.
aplt.tracer.profile_image(tracer=tracer, grid=simulator.grid)
aplt.tracer.subplot_tracer(tracer=tracer, grid=simulator.grid)

# We can now pass this simulator a tracer, which creates the ray-traced image plotted above and simulates it as an
# imaging dataset.
imaging = simulator.from_tracer(tracer=tracer)

# Lets plot the simulated imaging dataset before we output it to fits.
aplt.imaging.subplot_imaging(imaging=imaging)

# Finally, lets output our simulated dataset to the dataset path as .fits files.
imaging.output_to_fits(
    image_path=dataset_path + "image.fits",
    psf_path=dataset_path + "psf.fits",
    noise_map_path=dataset_path + "noise_map.fits",
    overwrite=True,
)


####################################### OTHER EXAMPLE IMAGES #####################################


# (these files are already in the autolens_workspace and are remade running this script)
dataset_name = "lens_broken_power_law__source_sersic__2"

# Create the path where the dataset will be output, which in this case is
# '/autolens_workspace/dataset/imaging/lens_sie__source_sersic/'
dataset_path = af.path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=["dataset", dataset_label, dataset_name]
)

# The pixel scale of the image to be simulated
pixel_scales = 0.05

# Simulate a simple Gaussian PSF for the image.
psf = al.kernel.from_gaussian(shape_2d=(11, 11), sigma=0.1, pixel_scales=pixel_scales)

# To simulate the imaging dataset we first create a simulator, which defines the shape, resolution and pixel-scale of the
# image that is simulated, as well as its expoosure time, noise levels and psf.
simulator = al.simulator.imaging(
    shape_2d=(180, 180),
    pixel_scales=pixel_scales,
    sub_size=2,
    exposure_time=300.0,
    psf=psf,
    background_level=0.1,
    add_noise=True,
)

# Setup the lens galaxy's mass (SIE+Shear) and source galaxy light (elliptical Sersic) for this simulated lens.
lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mp.EllipticalBrokenPowerLaw(
        centre=(0.0, 0.0),
        axis_ratio=0.8,
        phi=45.0,
        einstein_radius=0.8,
        inner_slope=1.2,
        outer_slope=1.7,
        break_radius=0.2,
    ),
)

source_galaxy = al.Galaxy(
    redshift=1.0,
    light=al.lp.EllipticalSersic(
        centre=(0.1, -0.07),
        axis_ratio=0.6,
        phi=30.0,
        intensity=0.3,
        effective_radius=0.5,
        sersic_index=2.0,
    ),
)

# Use these galaxies to setup a tracer, which will generate the image for the simulated imaging dataset.
tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

# Lets look at the tracer's image - this is the image we'll be simulating.

# To make this figure, we need to pass the plotter a grid which it uses to create the image. The simulator has its
# grid accessible as a property, which we can use to do this.
aplt.tracer.profile_image(tracer=tracer, grid=simulator.grid)
aplt.tracer.subplot_tracer(tracer=tracer, grid=simulator.grid)

# We can now pass this simulator a tracer, which creates the ray-traced image plotted above and simulates it as an
# imaging dataset.
imaging = simulator.from_tracer(tracer=tracer)

# Lets plot the simulated imaging dataset before we output it to fits.
aplt.imaging.subplot_imaging(imaging=imaging)

# Finally, lets output our simulated dataset to the dataset path as .fits files.
imaging.output_to_fits(
    image_path=dataset_path + "image.fits",
    psf_path=dataset_path + "psf.fits",
    noise_map_path=dataset_path + "noise_map.fits",
    overwrite=True,
)