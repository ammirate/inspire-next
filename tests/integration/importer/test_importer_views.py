# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2019 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import json
import os

import vcr


my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir=os.path.join(
        os.path.dirname(__file__), 'fixtures/cassettes',
    ),
    record_mode='once',
)


def test_import_arxiv_view_404(api_client):
    with my_vcr.use_cassette('arxiv_404.yml'):
        resp = api_client.post('/import/arxiv/1234')

        assert resp.status_code == 404
        assert 'Article 1234 not found' in resp.data


def test_import_arxiv_view_ok(api_client):
    with my_vcr.use_cassette('arxiv_ok.yml'):
        resp = api_client.post('/import/arxiv/0804.2273')
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['arxiv_eprints'][0]['value'] == '0804.2273'


def test_import_arxiv_view_500(api_client):
    with my_vcr.use_cassette('arxiv_broken_record.yml'):
        resp = api_client.post('/import/arxiv/0804.1111')

        assert resp.status_code == 500
        assert 'An error occurred while parsing article ' \
               'oai:arXiv.org:0804.1111' in resp.data

