from clarity_ext.domain.validation import ValidationException, ValidationType
import datetime


class Dilute(object):
    # Enclose sample data, user input and derived variables for a
    # single row in a dilution
    def __init__(self, input_analyte, output_analyte):
        self.source_well = input_analyte.well
        self.source_container = input_analyte.container
        self.source_concentration = input_analyte.concentration
        self.source_well_index = None
        self.source_plate_pos = None

        self.target_concentration = output_analyte.target_concentration
        self.target_volume = output_analyte.target_volume
        self.target_well = output_analyte.well
        self.target_container = output_analyte.container

        self.sample_name = output_analyte.name
        self.sample_volume = None
        self.buffer_volume = None
        self.target_well_index = None
        self.target_plate_pos = None
        self.has_to_evaporate = None

    def __str__(self):
        source = "source({}/{}, conc={})".format(self.source_container,
                                                 self.source_well, self.source_concentration)
        target = "target({}/{}, conc={}, vol={})".format(self.target_container, self.target_well,
                                                         self.target_concentration, self.target_volume)
        return "{} => {}".format(source, target)

    def __repr__(self):
        return "<Dilute {}>".format(self.sample_name)


class RobotDeckPositioner(object):
    """
    Handle plate positions on the robot deck (target and source)
    as well as well indexing
    """
    def __init__(self, robot_name, dilutes, plate):
        self.robot_name = robot_name
        self.plate = plate
        index_method_map = {"Hamilton": lambda well: well.index_down_first}
        self.indexer = index_method_map[robot_name]
        self.target_plate_sorting_map = self._build_plate_sorting_map(
            [dilute.target_container for dilute in dilutes])
        self.target_plate_position_map = self._build_plate_position_map(
            self.target_plate_sorting_map, "END"
        )
        self.source_plate_sorting_map = self._build_plate_sorting_map(
            [dilute.source_container for dilute in dilutes])
        self.source_plate_position_map = self._build_plate_position_map(
            self.source_plate_sorting_map, "DNA"
        )

    def find_sort_number(self, dilute):
        """Sort dilutes according to plate and well positions in source
        :param dilute:
        """
        plate_base_number = self.plate.size.width * self.plate.size.height + 1
        plate_sorting = self.source_plate_sorting_map[
            dilute.source_container.id]
        # Sort order for wells are always based on down first indexing
        # regardless the robot type
        return plate_sorting * plate_base_number + dilute.source_well.index_down_first

    @staticmethod
    def _build_plate_position_map(plate_sorting_map, plate_pos_prefix):
        # Fetch an unique list of container names from input
        # Make a dictionary with container names and plate positions
        # eg. END1, DNA2
        plate_positions = []
        for key, value in plate_sorting_map.iteritems():
            plate_position = "{}{}".format(plate_pos_prefix, value)
            plate_positions.append((key, plate_position))

        plate_positions = dict(plate_positions)
        return plate_positions

    @staticmethod
    def _build_plate_sorting_map(containers):
        # Fetch an unique list of container names from input
        # Make a dictionary with container names and plate position sort numbers
        unique_containers = sorted(list(
            {container.id for container in containers}))
        positions = range(1, len(unique_containers) + 1)
        plate_position_numbers = dict(zip(unique_containers, positions))
        return plate_position_numbers

    def __str__(self):
        return "<{type} {robot} {height}x{width}>".format(type=self.__class__.__name__,
                                                          robot=self.robot_name,
                                                          height=self.plate.size.height,
                                                          width=self.plate.size.width)


class DilutionScheme(object):
    """Creates a dilution scheme, given input and output analytes."""

    def __init__(self, artifact_service, robot_name):
        """
        Calculates all derived values needed in dilute driver file.
        """
        pairs = artifact_service.all_analyte_pairs()
        self.current_step_id = artifact_service.step_repository.session.current_step_id

        # TODO: Is it safe to just check for the container for the first output
        # analyte?
        container = pairs[0].output_artifact.container

        self.dilutes = [Dilute(pair.input_artifact, pair.output_artifact)
                        for pair in pairs]

        self.analyte_pair_by_dilute = {dilute: pair for dilute, pair in zip(self.dilutes, pairs)}

        # Handle volumes etc.
        for dilute in self.dilutes:
            dilute.sample_volume = \
                dilute.target_concentration * dilute.target_volume / \
                dilute.source_concentration
            dilute.buffer_volume = \
                max(dilute.target_volume - dilute.sample_volume, 0)
            dilute.has_to_evaporate = \
                (dilute.target_volume - dilute.sample_volume) < 0

        # Handle positioning
        self.robot_deck_positioner = RobotDeckPositioner(robot_name, self.dilutes, container)
        for dilute in self.dilutes:
            dilute.source_well_index = self.robot_deck_positioner.indexer(dilute.source_well)
            dilute.source_plate_pos = self.robot_deck_positioner. \
                source_plate_position_map[dilute.source_container.id]
            dilute.target_well_index = self.robot_deck_positioner.indexer(
                dilute.target_well)
            dilute.target_plate_pos = self.robot_deck_positioner \
                .target_plate_position_map[dilute.target_container.id]

        self.dilutes = sorted(self.dilutes,
                              key=lambda curr_dil: self.robot_deck_positioner.find_sort_number(curr_dil))

    def validate(self):
        """
        Yields validation errors or warnings

        TODO: These validation errors should not be in clarity-ext (implementation specific)
        """
        def pos_str(dilute):
            return "{}=>{}".format(dilute.source_well, dilute.target_well)

        for dilute in self.dilutes:
            if dilute.sample_volume < 2:
                yield ValidationException("Too low sample volume: " + pos_str(dilute))
            elif dilute.sample_volume > 50:
                yield ValidationException("Too high sample volume: " + pos_str(dilute))
            if dilute.has_to_evaporate:
                yield ValidationException("Sample has to be evaporated: " + pos_str(dilute), ValidationType.WARNING)
            if dilute.buffer_volume > 50:
                yield ValidationException("Too high buffer volume: " + pos_str(dilute))

    def __str__(self):
        return "<DilutionScheme positioner={}>".format(self.robot_deck_positioner)

    @property
    def driver_file_name(self):
        # TODO: Fetch user initials
        pid = self.current_step_id
        today = datetime.date.today().strftime("%y%m%d")
        return "DriverFile_EEX_{}_{}".format(today, pid)
