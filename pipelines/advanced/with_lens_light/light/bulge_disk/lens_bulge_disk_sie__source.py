import autofit as af
import autolens as al

# In this pipeline, we fit the lens light of a strong lens using a two component bulge + disk model.

# The mass model and source are initialized using an already run 'source' pipeline. Although the lens light was
# fitted in this pipeline, we do not use this model to set priors in this pipeline.

# The bulge and disk are modeled using EllipticalSersic and EllipticalExponential profiles respectively. Their alignment
# (centre, phi, axis_ratio) and whether the disk component is instead modeled using an EllipticalSersic profile
# can be customized using the pipeline settings.

# The pipeline is one phase:

# Phase 1:

# Fit the lens light using a bulge + disk model, with the lens mass and source fixed to the
# result of the previous pipeline

# Lens Light & Mass: EllipticalSersic + EllipticalExponential
# Lens Mass: EllipticalIsothermal + ExternalShear
# Source Light: Previous 'source' pipeline.
# Previous Pipelines: with_lens_light/source/*/lens_bulge_disk_sie__source_*.py
# Prior Passing: Lens Mass (instance -> previous pipeline), Source (instance -> previous pipeliine).
# Notes: Can be customized to vary the lens mass and source.


def make_pipeline(
    pipeline_general_settings,
    pipeline_light_settings,
    phase_folders=None,
    redshift_lens=0.5,
    positions_threshold=None,
    sub_size=2,
    signal_to_noise_limit=None,
    bin_up_factor=None,
    pixel_scale_interpolation_grid=0.05,
):

    ### SETUP PIPELINE & PHASE NAMES, TAGS AND PATHS ###

    # A source tag distinguishes if the previous pipeline models used a parametric or inversion model for the source.

    source_tag = al.pipeline_settings.source_tag_from_source(
        source=af.last.instance.galaxies.source
    )

    pipeline_name = (
        "pipeline_light_bulge_disk__lens_bulge_disk_sie__source_" + source_tag
    )

    # This pipeline's name is tagged according to whether:

    # 1) Hyper-fitting settings (galaxies, sky, background noise) are used.
    # 2) The bulge + disk centres, rotational angles or axis ratios are aligned.
    # 3) The disk component of the lens light model is an Exponential or Sersic profile.
    # 4) The lens galaxy mass model includes an external shear.

    phase_folders.append(pipeline_name)
    phase_folders.append(pipeline_general_settings.tag + pipeline_light_settings.tag)

    ### PHASE 1 ###

    # In phase 1, we fit the lens galaxy's light, where we:

    # 1) Fix the lens galaxy's mass and source galaxy to the results of the previous pipeline.
    # 2) Vary the lens galaxy hyper noise factor if hyper-galaxies noise scaling is on.

    # If hyper-galaxy noise scaling is on, it may over-scale the noise making this new light profile fit the data less
    # well. This can be circumvented by including the noise scaling as a free parameter.

    if pipeline_general_settings.hyper_galaxies:
        hyper_galaxy = af.last.hyper_combined.instance.galaxies.lens.hyper_galaxy
        hyper_galaxy.noise_factor = (
            af.last.hyper_combined.model.galaxies.lens.hyper_galaxy.noise_factor
        )
    else:
        hyper_galaxy = None

    # Model the disk as a Sersic if input.

    if pipeline_light_settings.disk_as_sersic:
        disk = af.PriorModel(al.lp.EllipticalSersic)
    else:
        disk = af.PriorModel(al.lp.EllipticalExponential)

    lens = al.GalaxyModel(
        redshift=redshift_lens,
        bulge=al.lp.EllipticalSersic,
        disk=disk,
        mass=af.last.instance.galaxies.lens.mass,
        shear=af.last.instance.galaxies.lens.shear,
        hyper_galaxy=hyper_galaxy,
    )

    # Adjust the alignment of the bulge and disk to the input of the pipeline settings.

    if pipeline_light_settings.align_bulge_disk_centre:
        lens.bulge.centre = lens.disk.centre

    if pipeline_light_settings.align_bulge_disk_axis_ratio:
        lens.bulge.axis_ratio = lens.disk.axis_ratio

    if pipeline_light_settings.align_bulge_disk_phi:
        lens.bulge.phi = lens.disk.phi

    phase1 = al.PhaseImaging(
        phase_name="phase_1__lens_bulge_disk_sie__source_" + source_tag,
        phase_folders=phase_folders,
        galaxies=dict(lens=lens, source=af.last.instance.galaxies.source),
        hyper_image_sky=af.last.hyper_combined.instance.optional.hyper_image_sky,
        hyper_background_noise=af.last.hyper_combined.instance.optional.hyper_background_noise,
        positions_threshold=positions_threshold,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        optimizer_class=af.MultiNest,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 50
    phase1.optimizer.sampling_efficiency = 0.2

    # If the source is parametric, the inversion hyper phase below will be skipped.

    phase1 = phase1.extend_with_multiple_hyper_phases(
        hyper_galaxy=pipeline_general_settings.hyper_galaxies,
        inversion=True,
        include_background_sky=pipeline_general_settings.hyper_image_sky,
        include_background_noise=pipeline_general_settings.hyper_background_noise,
    )

    return al.PipelineDataset(pipeline_name, phase1)