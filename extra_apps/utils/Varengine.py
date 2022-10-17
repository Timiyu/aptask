# coding=utf8
from string import Template


class LocalTemplate(Template):
    # 局部参数化 ${var}--var
    delimiter = '$'
    pattern = r'''
    \$\{(?:
      (?P<escaped>\$\{)                  |   # Escape sequence of two delimiters
      (?P<named>[_a-z][_a-z0-9]*)\}      |   # delimiter and a Python identifier
      (?P<braced>[_a-z][_a-z0-9]*)}\}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    '''


class GlobalTemplate(Template):
    # 全局参数化 ${{var}}--var
    delimiter = '$'
    pattern = r'''
    \$\{\{(?:
      (?P<escaped>\$\{\{)                  |   # Escape sequence of two delimiters
      (?P<named>[_a-z][_a-z0-9]*)\}\}      |   # delimiter and a Python identifier
      (?P<braced>[_a-z][_a-z0-9]*)}\}\}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    '''


def local_var_template_exchange(template_string, values):
    try:
        template_string = LocalTemplate(template_string)
        return template_string.safe_substitute(values)
    except Exception as e:
        print(e)
        return template_string


def global_var_template_exchange(template_string, values):
    try:
        template_string = GlobalTemplate(template_string)
        return template_string.safe_substitute(values)
    except Exception as e:
        print(e)
        return template_string


if __name__ == '__main__':
    # 局部常量
    print(local_var_template_exchange("""${{name}}-${n}------${{name}} has ${n} message.""", {'n': 37}))
    # 全局常量
    print(global_var_template_exchange("""${{name}}-${n}------${{name}} has ${n} message.""", {'name': 'wanghuan'}))
