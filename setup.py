#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Gonéri Le Bouder
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import setuptools

import dci_orm


setuptools.setup(
    name='dci_orm',
    version=dci_orm.__version__,
    author='Gonéri Le Bouder',
    author_email='goneri@lebouder.net',
    description='An unofficial ORM for the DCI DB',
    url='https://github.com/goneri/dci-orm',
    license='Apache v2.0',
    packages=['dci_orm'],
)
