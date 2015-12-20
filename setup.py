#!/usr/bin/env python
# -*- coding: utf-8 -*-

# +---------------------------------------------------------------------------+
# | pylstar : Implementation of the LSTAR Grammatical Inference Algorithm     |
# +---------------------------------------------------------------------------+
# | Copyright (C) 2015 Georges Bossert                                        |
# | This program is free software: you can redistribute it and/or modify      |
# | it under the terms of the GNU General Public License as published by      |
# | the Free Software Foundation, either version 3 of the License, or         |
# | (at your option) any later version.                                       |
# |                                                                           |
# | This program is distributed in the hope that it will be useful,           |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of            |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
# | GNU General Public License for more details.                              |
# |                                                                           |
# | You should have received a copy of the GNU General Public License         |
# | along with this program. If not, see <http://www.gnu.org/licenses/>.      |
# +---------------------------------------------------------------------------+
# | @url      : https://github.com/gbossert/pylstar                           |
# | @contact  : gbossert@miskin.fr                                            |
# +---------------------------------------------------------------------------+

# +----------------------------------------------------------------------------
# | Global Imports
# +----------------------------------------------------------------------------
import sys

from setuptools import setup, find_packages

sys.path.insert(0, 'src/')
from pylstar import release
from resources.sdist.test_command import test_command
from resources.sdist.utils import opj

# +----------------------------------------------------------------------------
# | Definition of the dependencies
# +----------------------------------------------------------------------------
dependencies = []
with open('requirements.txt', 'r') as fd_requirements:
    for dependency in fd_requirements:
        dependencies.append(dependency.strip())

extra_dependencies = {
    'docs': ['Sphinx>=1.1.3']
}

dependency_links = []

data_files = []

# Extract the long description from README.rst and NEWS.rst files
README = open('README.md', 'rt').read()
NEWS = open('CHANGELOG.md', 'rt').read()

# +----------------------------------------------------------------------------
# | Extensions in the build operations (test, ...)
# +----------------------------------------------------------------------------
CMD_CLASS = {
    'test': test_command
}
# +----------------------------------------------------------------------------
# | Definition of the package
# +----------------------------------------------------------------------------
setup(
    name=release.name,
    packages=find_packages(where='src'),
    package_dir={
        "pylstar": opj("src", "pylstar")
    },
    data_files=data_files,
    install_requires=dependencies,
    extras_require=extra_dependencies,
    dependency_links=dependency_links,
    version=release.version,
    license=release.licenseName,
    description=release.description,
    platforms=release.platforms,
    author=release.author,
    author_email=release.author_email,
    url=release.url,
    download_url=release.download_url,
    keywords=release.keywords,
    long_description=README + '\n' + NEWS,
    cmdclass=CMD_CLASS,
)

