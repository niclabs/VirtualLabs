class LinkInfoChecker:
    def __init__(self):
        pass

    def check_settings(self, settings):
        if 'delay' in settings:
            delay = settings['delay']

            settings['delay']['value'] = self.append_miliseconds(delay['value']) if 'value' in delay else '0ms'
            settings['delay']['random_variation'] = self.append_percentage(delay['random_variation']) if 'random_variation' in delay else '0%'
            settings['delay']['corr'] = self.append_percentage(delay['correlation']) if 'correlation' in delay else '0%'
            settings['delay']['distribution'] = delay['distribution'] if 'distribution' in delay else ''

        if 'loss' in settings:
            loss = settings['loss']
            settings['loss']['value'] = self.append_percentage(loss['value']) if 'value' in loss else '0%'
            settings['loss']['random_variation'] = self.append_percentage(loss['random_variation']) \
                if 'random_variation' in loss else '0%'

        if 'bandwidth' in settings:
            bandwidth = settings['bandwidth']

            if 'speed' in settings['bandwidth']:
                settings['bandwidth']['up'] = self.append_rate(bandwidth['speed'])
                settings['bandwidth']['down'] = self.append_rate(bandwidth['speed'])
            elif 'up' in settings['bandwidth'] and 'down' in settings['bandwidth']:
                settings['bandwidth']['up'] = self.append_rate(bandwidth['up'])
                settings['bandwidth']['down'] = self.append_rate(bandwidth['down'])
            else:
                raise ValueError("Can not set an upload speed without limiting download speed")

        if 'duplication' in settings:
            settings['duplication'] = self.append_percentage(settings['duplication'])

        if 'corruption' in settings:
            settings['corruption'] = self.append_percentage(settings['corruption'])

        if 'gap' in settings:
            gap = settings['gap']

            settings['gap']['packet'] = gap['pac_index'] if 'pac_index' in gap else 0
            settings['gap']['delay'] = self.append_miliseconds(gap['delay']) if 'delay' in gap else '0ms'

        if 'reordering' in settings:
            reor = settings['reordering']

            settings['reordering']['delay'] = self.append_miliseconds(reor['delay']) if 'delay' in reor else '0ms'
            settings['reordering']['probability'] = self.append_percentage(reor['probability']) if 'probability' in reor else '0%'
            settings['reordering']['correlation'] = self.append_percentage(reor['correlation']) if 'correlation' in reor else '0%'

    @staticmethod
    def append_percentage(value):
        if not value.endswith('%'):
            value += '%'
        return value

    @staticmethod
    def append_miliseconds(value):
        if not value.endswith('ms'):
            value += 'ms'
        return value

    @staticmethod
    def append_rate(value):
        if not value.endswith('kbps'):
            value += 'kbps'
        return value
