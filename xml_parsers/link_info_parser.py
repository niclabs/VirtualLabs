class LinkInfoParser:
    def __init__(self, settings):
        self.settings = settings
        self.bandwidth = settings['bandwidth'] if 'bandwidth' in settings else ''

    def parse_delay(self):
        delay_dic = {}

        if 'delay' in self.settings:
            delay = self.settings['delay']

            delay_dic['value'] = delay['value'] if 'value' in delay else 0
            delay_dic['ran'] = delay['random_variation'] if 'random_variation' in delay else 0
            delay_dic['corr'] = delay['correlation'] if 'correlation' in delay else 0
            delay_dic['dist'] = delay['distribution'] if 'distribution' in delay else ''

        return delay_dic

    def parse_loss(self):
        loss_dic = {}

        if 'loss' in self.settings:
            loss = self.settings['loss']

            loss_dic['value'] = int(loss['value']) if 'value' in loss else 0
            loss_dic['ran'] = int(loss['random_variation']) if 'random_variation' in loss else 0

        return loss_dic

    def parse_bandwidth(self):
        pass

    def parse_duplication(self):
        dup = 0
        if 'duplication' in self.settings:
            dup = self.settings['duplication']

        return dup

    def parse_corruption(self):
        cor = 0
        if 'corruption' in self.settings:
            cor = self.settings['corruption']

        return cor

    def parse_gap_reordering(self):
        gap_dic = {}

        if 'gap' in self.settings:
            gap = self.settings['gap']

            gap_dic['pac'] = gap['pac_index'] if 'pac_index' in gap else 0
            gap_dic['delay'] = gap['delay'] if 'delay' in gap else 0

        return gap_dic

    def parse_reordering(self):
        reor_dic = {}

        if 'reordering' in self.settings:
            reor = self.settings['reordering']

            reor_dic['delay'] = reor['delay'] if 'delay' in reor else 0
            reor_dic['prob'] = reor['probability'] if 'probability' in reor else 0
            reor_dic['corr'] = reor['correlation'] if 'correlation' in reor else 0

        return reor_dic

    def get_all_parsed(self):
        return {'delay': self.parse_delay(), 'loss': self.parse_loss(), 'bandwidth': self.parse_bandwidth(),
                'duplication': self.parse_duplication(), 'corruption': self.parse_corruption(),
                'gap': self.parse_gap_reordering(), 'reordering': self.parse_reordering()}
