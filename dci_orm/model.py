# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2018 Red Hat, Inc
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

import re

from sqlalchemy import create_engine
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy import MetaData
from sqlalchemy.orm.interfaces import ONETOMANY
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.orm import Session


class ORM(object):

    def __init__(self, db_uri="postgresql+psycopg2://dci:dci@localhost/dci"):
        self.engine = create_engine(db_uri, pool_size=20, max_overflow=0,
                                    encoding='utf8', convert_unicode=True)

        self.session = Session(self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(self.engine)

        # NOTE(Gonéri): ensure the associated resources list get sorted using
        # the created_at key.
        def _gen_relationship(base, direction, return_fn,
                              attrname, local_cls, referred_cls, **kw):
            ref_columns = referred_cls.__table__.columns
            if direction is ONETOMANY and 'created_at' in ref_columns:
                kw['order_by'] = ref_columns.created_at
            return generate_relationship(
                base, direction, return_fn,
                attrname, local_cls, referred_cls, **kw)
        self.base = automap_base(metadata=self.metadata)
        self.base.prepare(generate_relationship=_gen_relationship)

        # engine.echo = True

        # NOTE(Gonéri): Create the foreign table attribue to be able to
        # do job.remoteci.name
        for table in self.metadata.tables:
            # print('* %s' % table)
            try:
                cur_db = getattr(self.base.classes, table)
            except AttributeError:
                continue
            for column in cur_db.__table__.columns:
                # print('  - "%s"' % column)
                if str(column) == 'topics.next_topic_id':
                    foreign_table_name = 'topic'
                    '->'
                elif str(column) == 'teams.parent_id':
                    foreign_table_name = 'team'
                elif str(column) == 'jobs.previous_job_id':
                    # foreign_table_name = 'job'
                    continue
                elif str(column) == 'jobs.update_previous_job_id':
                    # foreign_table_name = 'job'
                    continue
                elif str(column) == 'logs.user_id':
                    continue
                elif str(column) == 'jobs_events.job_id':
                    continue
                elif str(column) == 'jobs_events.topic_id':
                    continue
                else:
                    m = re.search(r"\.(\w+)_id$", str(column))
                    if not m:
                        continue
                    foreign_table_name = m.group(1)
                # print('      fk table name: %s' % foreign_table_name)

                foreign_table_object = getattr(
                    self.base.classes, foreign_table_name + 's')
                remote_side = None
                remote_side = [foreign_table_object.id]
                setattr(cur_db, foreign_table_name, relationship(
                    foreign_table_object, uselist=False,
                    remote_side=remote_side))

#        setattr(self.base.classes.jobdefinitions, 'components',
#                association_proxy(
#                    'jobdefinition_components_collection', 'component'))
        setattr(self.base.classes.jobs, 'jobstates', relationship(
            self.base.classes.jobstates, uselist=True, lazy='dynamic',
            order_by=self.base.classes.jobstates.created_at.desc()))
        self._Session = sessionmaker(bind=self.engine)
