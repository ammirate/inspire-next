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

"""Importer views."""

from __future__ import absolute_import, division, print_function

import requests

from flask import jsonify
from flask.blueprints import Blueprint
from hepcrawl.parsers import ArxivParser

blueprint = Blueprint(
    'inspire_importer',
    __name__,
    url_prefix='/import'
)

PLACEHOLDER = '<ID>'
ARXIV_URL = 'http://export.arxiv.org/oai2?' \
            'verb=GetRecord&' \
            'identifier=oai:arXiv.org:<ID>&' \
            'metadataPrefix=arXiv'


@blueprint.route('/arxiv/<arxiv_id>', methods=('POST',))
def import_arxiv_view(arxiv_id):
    try:
        url = ARXIV_URL.replace(PLACEHOLDER, arxiv_id)
        resp = requests.get(url=url)

        if 'Malformed identifier' in str(resp.text):
            return jsonify(message='Article {} not found'.format(arxiv_id)), 404

        parser = ArxivParser(resp.text)
        data = parser.parse()
        return jsonify(data)

    except Exception as e:
        return jsonify(
            message='An error occurred while parsing article oai:arXiv.org:{}'.
            format(arxiv_id),
            error=str(e)
        ), 500


@blueprint.route('/arxiv/<doi>')
def import_doi_view(doi):
    return jsonify(message='Article {} not found'.format(doi)), 404
