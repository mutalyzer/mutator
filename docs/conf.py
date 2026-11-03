from subprocess import call

call('pip install ..', shell=True)

from mutalyzer_mutator import author, copyright, project, release


autoclass_content = 'both'
extensions = ['sphinx.ext.autodoc']
master_doc = 'index'
