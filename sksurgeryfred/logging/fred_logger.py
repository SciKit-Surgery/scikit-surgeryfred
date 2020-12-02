""" Class to handle sksurgeryfred logging """

from logging import getLogger, FileHandler, Formatter, INFO
import csv
from sksurgeryfredbe import __version__

class Logger():
    """
    Implements logging functionality for sksurgeryfred.
    Configuration is done by passing a dictionary on construction.
    Subsequent calls to log("message") will write to log file.

    :param config: - a dictionary containing configuration
            parameters. If dictionary contains no "logger" entry then
            an empty logger is created and subsequent calls to log() will
            have no effect. Otherwise a logger is created according to the
            entries in the logger config dictionary. ("log file name",
            "overwrite existing"

    :raises: IOError if the user can't write to the named log file?
    """

    def __init__(self, config):
        """
        Initialises the logger based on the passed configuration:
        """

        self._no_logging = True
        log_config = config.get("logger")
        if log_config is not None:
            version_string = __version__
            friendly_vs = version_string if version_string else 'unknown'
            self._logger = getLogger("sksurgeryfred v" + friendly_vs)

            self.log_file_name = log_config.get("log file name",
                                                "sksurgeryfred.log")
            overwrite = log_config.get("overwrite existing", False)

            mode = 'a'
            if overwrite:
                mode = 'w'

            file_handler = FileHandler(self.log_file_name, mode)

            formatter = Formatter('%(asctime)s - %(name)s -' +
                                  ' %(levelname)s - %(message)s')

            file_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)
            self._logger.setLevel(INFO)
            self._no_logging = False

    def log(self, message):
        """If logging, passes message to logger"""
        if self._no_logging:
            return

        self._logger.info(message)

    def log_result(self, actual_tre, fre, expected_tre, expected_fre, mean_fle,
                   no_fids):
        """
        Writes the registration result to log file
        """
        msg = ("success, {0:.4f}, {1:.4f}, {2:.4f}, {3:.4f}, {4:.4f}," +
               "{5:2d}").format(
                   actual_tre, fre, expected_tre, expected_fre, mean_fle,
                   no_fids)
        self._logger.info(msg)

    def log_score(self, state_string, score):
        """
        Writes the registration result to log file
        """
        msg = ("ablation, {0:}, {1:}").format(state_string, score)
        self._logger.info(msg)



    def read_log(self):
        """
        reads a log file and returns lists of values
        """
        actual_tres = []
        actual_fres = []
        expected_tres = []
        expected_fres = []
        mean_fles = []
        no_fids = []

        samples = 0
        with open(self.log_file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    actual_tres.append(float(row[2]))
                    actual_fres.append(float(row[3]))
                    expected_tres.append(float(row[4]))
                    expected_fres.append(float(row[5]))
                    mean_fles.append(float(row[6]))
                    no_fids.append(int(row[7]))
                    samples += 1
                except IndexError:
                    raise IOError(("Failed to read log file, " +
                                   "{0:}".format(self.log_file_name) +
                                   " near line: {0:}".format(samples))) \
                                                   from IOError
        return [actual_tres, actual_fres, expected_tres, expected_fres,
                mean_fles, no_fids]

    def __del__(self):
        """Releases the log file"""
        if not self._no_logging:
            self._logger.handlers[0].flush()
            self._logger.handlers[0].close()
