class LinkInfoParser:
    def __init__(self, settings, bridge):
        self.settings = settings
        self.bridge = bridge


        self.loss = settings['loss'] if 'loss' in settings else ''
        self.bandwidth = settings['bandwidth'] if 'bandwidth' in settings else ''
        self.duplication = settings['duplication'] if 'duplication' in settings else ''
        self.corruption = settings['corruption'] if 'corruption' in settings else ''
        self.gap_reordering = settings['gap_reordering'] if 'gap_reordering' in settings else ''

    def set_delay(self):
        delay_dic = {}

        if 'delay' in self.settings:
            delay = self.settings['delay']
            if 'value' in delay:
                delay_dic['value'] = delay['value']
            #Else: throw an error
            if 'random_variation' in delay:
                delay_dic['ran'] = delay['random_variation']

            self.bridge.add_delay()