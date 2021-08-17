from pathlib import Path

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import RichTraceback

import nestedtext as nt

from data_correctness import check_resume_data_correctness

RESUME_DATA_FILENAME = 'data.nt'
RESUME_TEMPLATE_FILENAME = 'resume.template'
RENDERED_RESUME_FILENAME = 'site/index.html'

def get_resume_data():
    try: 
        resume_data = nt.load(RESUME_DATA_FILENAME, top='dict')
    except nt.NestedTextError as e:
        e.terminate()
    except OSError as e:
        fatal(os_error(e))
    return resume_data

def print_rich_traceback(rich_traceback):
    for (filename, lineno, function, line) in rich_traceback.traceback:
        print("File %s, line %s, in %s" % (filename, lineno, function))
        print(line, "\n")
    print("%s: %s" % \
                (
                str(rich_traceback.error.__class__.__name__),
                rich_traceback.error
                )
            )

def get_resume_template():
    try:
        template_lookup = TemplateLookup(directories=['.'])
        resume_template = \
                Template(
                        filename=RESUME_TEMPLATE_FILENAME,
                        lookup=template_lookup,
                        strict_undefined=True
                        )
    except:
        print_rich_traceback(RichTraceback())
    return resume_template

def render_resume_template(resume_template, resume_data):
    rendered_resume = resume_template.render(data=resume_data)
    return rendered_resume

def write_rendered_resume(rendered_resume):
    Path(RENDERED_RESUME_FILENAME).parent.mkdir(parents=True,exist_ok=True)
    with open(RENDERED_RESUME_FILENAME, 'w') as f:
        f.write(rendered_resume)

def main():
    resume_data = get_resume_data()
    check_resume_data_correctness(resume_data)
    resume_template = get_resume_template()
    rendered_resume = render_resume_template(resume_template, resume_data)
    write_rendered_resume(rendered_resume)

if __name__ == "__main__":
    main()
