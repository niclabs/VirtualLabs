class LinkSettingsParser:
    """ Parses the XML tags used to set the properties of a link
    Attributes:
        settings(dict): Dictionary with the information to parse
    """
    def __init__(self, settings):
        """
        :param settings: Dictionary (from XML) with all settings included
        """
        self.settings = settings

    def parse_delay(self):
        """ Parses the delay tag (if it exists)
        :return: Dictionary with the delay information
        """
        delay_dic = {}

        if 'delay' in self.settings:
            delay = self.settings['delay']

            if 'value' in delay:
                delay_dic['value'] = str(delay['value'])
            if 'random_variation' in delay:
                delay_dic['random_variation'] = str(delay['random_variation'])
            if 'correlation' in delay:
                delay_dic['correlation'] = str(delay['correlation'])
            if 'distribution' in delay:
                delay_dic['dist'] = str(delay['distribution'])

        return delay_dic

    def parse_loss(self):
        """ Parses the loss tag (if it exists)
        :return: Dictionary with the loss information
        """
        loss_dic = {}

        if 'loss' in self.settings:
            loss = self.settings['loss']

            if 'value' in loss:
                loss_dic['value'] = str(loss['value'])

            if 'random_variation' in loss:
                loss_dic['random_variation'] = str(loss['random_variation'])

        return loss_dic

    def parse_bandwidth(self):
        """ Parses the bandwidth tag (if it exists)
        :return: Dictionary with the bandwidth information
        """
        bandwidth_dic = {}

        if 'bandwidth' in self.settings:
            if 'speed' in self.settings['bandwidth']:
                bandwidth_dic['speed'] = str(self.settings['bandwidth']['speed'])

            if 'up' in self.settings['bandwidth']:
                bandwidth_dic['up'] = str(self.settings['bandwidth']['up'])

            if 'down' in self.settings['bandwidth']:
                bandwidth_dic['down'] = str(self.settings['bandwidth']['down'])

        return bandwidth_dic

    def parse_duplication(self):
        """ Parses the duplication tag (if it exists)
        :return: Dictionary with the duplication information
        """
        dup = 0
        if 'duplication' in self.settings:
            dup = str(self.settings['duplication'])

        return dup

    def parse_corruption(self):
        """ Parses the corruption tag (if it exists)
        :return: Dictionary with the corruption information
        """
        cor = 0
        if 'corruption' in self.settings:
            cor = str(self.settings['corruption'])

        return cor

    def parse_gap_reordering(self):
        """ Parses the gap reordering tag (if it exists)
        :return: Dictionary with the gap reordering information
        """
        gap_dic = {}

        if 'gap' in self.settings:
            gap = self.settings['gap']

            if 'pac_index' in gap:
                gap_dic['packet'] = int(gap['pac_index'])

            if 'delay' in gap:
                gap_dic['delay'] = str(gap['delay'])

        return gap_dic

    def parse_reordering(self):
        """ Parses the reordering tag (if it exists)
        :return: Dictionary with the reordering information
        """
        reor_dic = {}

        if 'reordering' in self.settings:
            reor = self.settings['reordering']

            if 'delay' in reor:
                reor_dic['delay'] = str(reor['delay'])

            if 'probability' in reor:
                reor_dic['probability'] = str(reor['probability'])

            if 'correlation' in reor:
                reor_dic['correlation'] = str(reor['correlation'])

        return reor_dic

    def get_all_parsed(self):
        """
        :return: Dictionary with all properties parsed (including empty dictionaries in those not originally included)
        """
        return {'delay': self.parse_delay(), 'loss': self.parse_loss(), 'bandwidth': self.parse_bandwidth(),
                'duplication': self.parse_duplication(), 'corruption': self.parse_corruption(),
                'gap': self.parse_gap_reordering(), 'reordering': self.parse_reordering()}
