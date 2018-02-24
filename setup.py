#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    ____  ____  ___ ____  __  __     
#   |  _ \|  _ \|_ _/ ___||  \/  |  _ 
#   | |_) | |_) || |\___ \| |\/| | (_)
#   |  __/|  _ < | | ___) | |  | |  _ 
#   |_|   |_| \_\___|____/|_|  |_| (_)
#                                     
#   ___                 _      _                  __                   __      
#    | _  _ ||_  _ \/ _|__ ._ |_).__ |_  _.|_ o|o(__|_o _  /\  _ _    (__|_o _ 
#    |(_)(_)||_)(_)/\  |(_)|  |  |(_)|_)(_||_)|||__)|_|(_ /--\(_(_)|_|__)|_|(_ 
#                                                                              
#    __                                          
#   (_  _  _|o._ _  _ .__|_ |\/| _.._ ._ o._  _  
#   __)(/_(_||| | |(/_| ||_ |  |(_||_)|_)|| |(_| 
#                                  |  |       _| 
#
#   |b|y| |D|a|n|i|e|l| |B|u|s|c|o|m|b|e|
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |d|a|n|i|e|l|.|b|u|s|c|o|m|b|e|@|n|a|u|.|e|d|u|

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import os, sys, glob
import inspect

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

# Directory of the current file 
SETUP_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))

# Read version from distmesh/__init__.py
with open(os.path.join('prism', '__init__.py')) as f:
    line = f.readline()
    while not line.startswith('__version__'):
        line = f.readline()
exec(line, globals())


# Set this to True to enable building extensions using Cython.
# Set it to False to build extensions from the C file (that
# was previously created using Cython).
# Set it to 'auto' to build with Cython if available, otherwise
# from the C file.
USE_CYTHON = True

ext_modules = [ ]
cmdclass = { }

if USE_CYTHON:
    ext_modules += [
        Extension("eigen", [ "pydensecrf/eigen.pyx" ],
        include_dirs=[np.get_include()]),
        Extension("prism.densecrf", [ "pydensecrf/densecrf.pyx" ],
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("eigen", [ "pydensecrf/eigen.c" ],
        include_dirs=[np.get_include()]),
        Extension("prism.densecrf", [ "pydensecrf/densecrf.c" ],
    ]

install_requires = [
    'numpy','scipy','Pillow','matplotlib', 'cython', 'pyproj', 'scikit-image', 'scikit-learn', 'tkcolorpicker', 'fiona', 'rasterio', 'shapely'
] #'basemap', 'pydensecrf', 'GDAL'

def setupPackage():
   setup(name='prism_mbes',
         version=__version__,
         description='Buscombe, D., 2017',
         #long_description=long_description,
         classifiers=[
             'Intended Audience :: Science/Research',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
             'Programming Language :: Python',
             'Topic :: Scientific/Engineering',
             'Topic :: Scientific/Engineering :: Physics',
         ],
         keywords='sonar sediment substrate classification',
         author='Daniel Buscombe',
         author_email='daniel.buscombe@nau.edu',
         url='https://github.com/dbuscombe-usgs/prism',
         download_url ='https://github.com/dbuscombe-usgs/prism/archive/master.zip',
         install_requires=install_requires,
         license = "GNU GENERAL PUBLIC LICENSE v3",
         packages=['prism'],
         cmdclass = cmdclass,
         ext_modules=ext_modules,
         platforms='OS Independent',
         package_data={'prism': ['*.png', 'data/newbex/bs/*.tiff', 'data/newbex/ref/*.shp', 'data/newbex/ref/*.shx', 'data/newbex/ref/*.dbf', 'data/newbex/ref/*.qpj', 'data/newbex/ref/*.prj', 'data/newbex/ref/*.cpg']} #
   )

if __name__ == '__main__':
    # clean --all does not remove extensions automatically
    if 'clean' in sys.argv and '--all' in sys.argv:
        import shutil
        # delete complete build directory
        path = os.path.join(SETUP_DIRECTORY, 'build')
        try:
            shutil.rmtree(path)
        except:
            pass
        # delete all shared libs from lib directory
        path = os.path.join(SETUP_DIRECTORY, 'prism')
        for filename in glob.glob(path + os.sep + '*.pyd'):
            try:
                os.remove(filename)
            except:
                pass
        for filename in glob.glob(path + os.sep + '*.so'):
            try:
                os.remove(filename)
            except:
                pass
    setupPackage()

