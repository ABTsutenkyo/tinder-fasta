from setuptools import setup

setup(name='tinder_fasta',
      version='0.1',
      description="It's a match!",
      url='https://github.com/celliern/tinder-fasta',
      author='Nicolas Cellier',
      author_email='contact@nicolas-cellier.net',
      license='MIT',
      install_requires=[
          "click",
          "awesome-slugify",
          "biopython",
          "path.py"
      ],
      packages=['tinder_fasta'],
      entry_points={'console_scripts':
                    ['tinder-fasta=tinder_fasta:match']},
      zip_safe=False)
