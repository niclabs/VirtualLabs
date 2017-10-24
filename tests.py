import resources.resources as res
import resources.template as tem

print res.os_templates.list_templates()
print res.router_templates.list_templates()
print res.switch_templates.list_templates()

print tem.Template('terminal', 0)