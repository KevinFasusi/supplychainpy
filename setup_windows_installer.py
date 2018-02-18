import cx_Freeze

base = None

executables = [cx_Freeze.Executable(
    "supplychainpy.py",
    base=base,
    icon='chain.ico'
    )]

cx_Freeze.setup(
    name="supplychainpy",
    option={
        "build_exe":{"packages": ["tkinter",
                                  "numpy",
                                  "cython",
                                  "flask",
                                  "scipy",
                                  "pandas",
                                  "sqlalchemy",
                                  "flask-restful",
                                  "flask-restless",
                                  "flask-script",
                                  "flask-sqlalchemy",
                                  "flask-uploads",
                                  "flask-wtf",
                                  "textblob",
                                  "Simplejson",
                                  "wtforms"],
                     "include_files":['chain.ico',
                                      'reporting/static/images/*',
                                      'reporting/static/fonts/*',
                                      'reporting/static/scripts/*',
                                      'reporting/static/styles/*',
                                      'reporting/static/*',
                                      'reporting/templates/*',
                                      'sample_data/*.csv',
                                      'sample_data/*.py',
                                      '_pickled/*']}
    },
    version="0.0.6",
    description="",
    executables= executables, 

)