from dataclasses import dataclass
from queenbee_dsl.function import Function, command, Inputs, Outputs


@dataclass
class AddRemoveMatrix(Function):
    """Remove direct sky from total sky and add direct sun."""

    total_sky_matrix = Inputs.file(
        description='Path to matrix for total sky contribution.',
        path='sky.ill', extensions=['ill', 'dc']
    )

    direct_sky_matrix = Inputs.file(
        description='Path to matrix for direct sky contribution.',
        path='sky_dir.ill', extensions=['ill', 'dc']
    )

    sunlight_matrix = Inputs.file(
        description='Path to matrix for direct sunlight contribution.',
        path='sun.ill', extensions=['ill', 'dc']
    )

    @command
    def create_matrix(self):
        return 'rmtxop sky.ill + -s -1.0 sky_dir.ill + sun.ill > final.ill'

    results_file = Outputs.file(description='Radiance matrix file.', path='final.ill')


@dataclass
class AddRemoveMatrixWithConversion(AddRemoveMatrix):
    """Remove direct sky from total sky and add direct sun."""
    conversion = Inputs.str(
        description='conversion as a string which will be passed to -c',
        default='47.4 119.9 11.6'
    )

    output_format = Inputs.str(
        default='-fa',
        spec={'type': 'string', 'enum': ['-fa', '-fd']}
    )

    @command
    def create_matrix(self):
        return 'rmtxop {{self.output_format}} sky.ill + -s -1.0 sky_dir.ill + sun.ill ' \
            '-c {{self.conversion}} | getinfo - > final.ill'


@dataclass
class CreateOctree(Function):
    """Generate an octree from a Radiance folder."""

    # inputs
    include_aperture = Inputs.str(
        default='include',
        description='A value to indicate if the static aperture should be included in '
        'octree. Valid values are include and exclude. Default is include.',
        spec={'type': 'string', 'enum': ['include', 'exclude']}
    )

    black_out = Inputs.str(
        default='default',
        description='A value to indicate if the black material should be used. Valid '
        'values are default and black. Default value is default.',
        spec={'type': 'string', 'enum': ['black', 'default']}
    )

    model = Inputs.folder(description='Path to Radiance model folder.', path='model')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct ' \
            '--{{self.include_aperture}}-aperture --{{self.black_out}}'

    # outputs
    scene_file = Outputs.file(description='Output octree file.', path='scene.oct')


@dataclass
class CreateOctreeWithSky(CreateOctree):
    """Generate an octree from a Radiance folder and a sky!"""

    # inputs
    sky = Inputs.file(description='Path to sky file.', path='sky.sky')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct ' \
            '--{{self.include_aperture}}-aperture --{{self.black_out}} ' \
            '--add-before sky.sky'


@dataclass
class GenSkyWithCertailIllum(Function):
    """Generates a sky with certain illuminance level."""

    illuminance = Inputs.float(
        default=100000,
        description='Sky illuminance level.'
    )

    @command
    def gen_100000_sky(self):
        return 'honeybee-radiance sky illuminance {{self.illuminance}}'

    sky = Outputs.file(description='Generated sky file.', path='overcast.sky')


@dataclass
class CreateRadianceFolder(Function):
    """Create a Radiance folder from a HBJSON input file."""

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    sensor_grids = Outputs.dict(
        description='Sensor grids information.', path='model/grid/_info.json'
    )


@dataclass
class CreateSkyDome(Function):
    """Create a skydome for daylight coefficient studies."""

    @command
    def gen_sky_dome(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky'

    sky_dome = Outputs.file(
        description='A sky hemisphere with ground.', path='rflux_sky.sky'
    )


@dataclass
class CreateSkyMatrix(Function):
    """Generate a sun-up sky matrix."""

    north = Inputs.int(
        description='An angle for north direction. Default is 0.',
        default=0, spec={'type': 'integer', 'maximum': 360, 'minimum': 0}
    )

    sky_component = Inputs.str(
        description='A switch for generating sun-only using -d or exclude sun '
        'contribution using -s. The default is an empty string for including both.',
        default=' ', spec={'type': 'string', 'enum': ['-s', '-d', ' ']}
    )

    wea = Inputs.file(
        description='Path to a wea file.', extensions=['wea'], path='sky.wea'
    )

    @command
    def generate_sky_matrix(self):
        return 'gendaymtx -u -O0 -r {{self.north}} -v {{self.sky_component}} sky.wea > sky.mtx'

    sky_matrix = Outputs.file(description='Output Sky matrix', path='sky.mtx')


@dataclass
class MergeFiles(Function):
    """Merge several files with similar starting name into one."""

    extension = Inputs.str(
        description='File extension including the . before the extension (e.g. .res, '
        '.ill)'
    )

    folder = Inputs.folder(
        description='Target folder with the input files.',
        path='input_folder'
    )

    @command
    def merge_files(self):
        return 'honeybee-radiance grid merge input_folder grid {{self.extension}}'

    result_file = Outputs.file(
        description='Output result file.', path='grid{{self.extension}}'
    )


class RayTracingDaylightFactor(Function):
    """Run ray-tracing and post-process the results for a daylight factor simulation."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I and -h are already included in the command.',
        default='-ab 2'
    )

    sky_illum = Inputs.float(
        description='Sky illuminance level for the sky included in octree.',
        default=100000
    )

    fixed_radiance_parameters = Inputs.str(
        description='Parameters that should not be overwritten by radiance_parameters '
        'input.', default='-I -h'
    )

    grid = Inputs.file(description='Input sensor grid.', path='grid.pts')

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct'
    )

    @command
    def ray_tracing(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts ' \
            '--rad-params "{{self.radiance_parameters}}" --rad-params-locked ' \
            '"{{self.fixed_radiance_parameters}}" --sky-illum {{self.sky_illum}} ' \
            '--output grid.res'

    result = Outputs.file(
        description='Daylight factor results file. The results for each sensor is in a '
        'new line.', path='grid.res'
    )


@dataclass
class SplitGrid(Function):
    """Split a single sensor grid file into multiple smaller grids."""

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    input_grid = Inputs.file(description='Input grid file.', path='grid.pts')

    @command
    def split_grid(self):
        return 'honeybee-radiance grid split grid.pts ' \
            '{{self.sensor_count}} --folder output --log-file output/grids_info.json'

    grids_list = Outputs.dict(
        description='A JSON array that includes information about generated sensor '
        'grids.', path='output/grids_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with new sensor grids.', path='output'
    )


@dataclass
class SplitGridFromFolder(SplitGrid):
    """Split a single sensor grid file into multiple grids based on maximum number
    of sensors.

    This function takes a folder of sensor grids and find the target grid based on
    grid-name.
    """

    name = Inputs.str(description='Grid name.')

    input_grid = Inputs.folder(description='Path to sensor grids folder.', path='.')

    @command
    def split_grid(self):
        return 'honeybee-radiance grid split {{self.name}}.pts ' \
            '{{self.sensor_count}} --folder output --log-file output/grids_info.json'
