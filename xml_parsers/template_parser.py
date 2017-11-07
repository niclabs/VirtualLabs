class TemplateParser:
    def __init__(self):
        pass

    def parse_template(self, template_dic):
        dic = {}

        if '@name' in template_dic:
            dic['name'] = str(template_dic['name'])

        if '@id' in template_dic:
            dic['id'] = int(template_dic['id'])

        return dic
