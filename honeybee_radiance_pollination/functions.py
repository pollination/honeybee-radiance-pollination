from queenbee_dsl.function import function, command, Inputs, Outputs


@function
class CreateOctreeWithSky:
    """Generate an octree from a Radiance folder and sky!"""

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

    sky = Inputs.file(description='Path to sky file.', path='sky.sky')

    @command
    def create_octree(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct ' \
            '--{{self.include_aperture}}-aperture --{{self.black_out}} ' \
            '--add-before sky.sky'

    # outputs
    scene_file = Outputs.file(description='Output octree file.', path='scene.oct')


@function
class GenSky:
    """Generates a 100000 lux sky."""

    @command
    def gen_100000_sky(self):
        return 'honeybee-radiance sky illuminance 100000'

    sky = Outputs.file(description='Generated sky file.', path='100000_lux.sky')


@function
class CreateRadianceFolder:
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
