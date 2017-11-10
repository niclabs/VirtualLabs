class TemplateParser:
    def __init__(self):
        pass

    def parse_template(self, template_dic):
        dic = {}

        if '@name' in template_dic:
            dic['name'] = str(template_dic['@name'])

        if '@id' in template_dic:
            dic['id'] = int(template_dic['@id'])

        if 'ram' in template_dic:
            dic['ram'] = int(template_dic['ram'])

        if 'cores' in template_dic:
            dic['cores'] = int(template_dic['cores'])

        return dic
