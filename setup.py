from setuptools import setup, find_packages
from codecs import open
from os import path

def here():         return path.abspath(path.dirname(__file__))
def load(filename): return open(path.join(here(), filename)).read()
def load_config():  return cfg2kv(load('project.cfg'))
def load_desc():    return load('README.md')
def unquote(s:str): return s.replace('"','').replace("'",'').strip()

def cfg2kv(cfg):
    """
    Parses ini file content with simple `[group]` and `key=value` lines
    and returns the content as dict: `{"group": {"key": "value"}}`
    """
    cat = 'project'
    res = {cat: {}}
    for line in cfg.split('\n'):
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        if line.startswith('[') and line.endswith(']'):
            cat = line[1:][:-1]
            if cat not in res: res[cat] = {}
            continue
        k, *v = line.split('=')
        res[cat][unquote(k)] = unquote('='.join(v))
    return res

def run_setup():
    readme  = load_desc()
    cfg     = load_config()
    project = cfg['project']
    scripts = cfg.get('scripts',     {})
    classif = cfg.get('classifiers', {})

    name        = project['name']
    binary      = project.get('binary')
    main        = project.get('main')
    requires    = project.get('requires','').split(' ')
    keywords    = project.get('keywords','').split(' ')
    version     = project['version']
    description = project['description']
    status      = project['status']

    repo         = project.get('repo')
    owner        = project.get('owner')
    owner_email  = project.get('owner_email')
    owner_handle = project.get('owner_handle')

    classifiers     = list(classif.values())
    console_scripts = ['{}={}'.format(k, scripts[k]) for k in scripts]
    entry_points    = {'console_scripts': console_scripts}

    if binary is not None and main is not None:
        script = '{b}={m}:main'.format(b=binary, m=main)
        console_scripts.append(script)

    print(console_scripts)

    setup(
        name            = name,
        version         = version,
        description     = description,
        url             = f'https://{repo}',
        author          = owner,
        author_email    = owner_email,
        python_requires = '>=3.5',
        license         = 'MIT',

        long_description              = readme,
        long_description_content_type = "text/markdown",

        # see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers = [
            status,
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ] + classifiers,

        keywords = keywords,
        packages = find_packages(
            exclude = ['contrib', 'docs', 'tests'],
        ),
        # see: https://packaging.python.org/en/latest/requirements.html
        install_requires = requires,
        # example: pip install widdy[dev]
        extras_require = {
            'dev': ['pytest','flake8','twine'],
            # check-mainfest coverage
        },
        # data files
        # package_data={ 'sample': ['package_data.dat'] },
        # extern data files installed into '<sys.prefix>/my_data'
        # data_files=[('my_data', ['data/data_file'])],
        entry_points = entry_points,
        # The key is used to render the link text on PyPI.
        project_urls = {
            'Documentation': f'https://{repo}',
            'Bug Reports':   f'https://{repo}/issues',
            'Funding':       f'https://{repo}',
            'Say Thanks!':   f'https://saythanks.io/to/{owner_handle}',
            'Source':        f'https://{repo}',
        },
    )

if __name__ == '__main__': run_setup()
