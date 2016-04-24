# -*- coding: utf-8 -*-

import os
import datetime
import flask
from flask import render_template, redirect, request, url_for
from urlparse import urlparse, urljoin

from utils import utils

import sosweb
from sosweb.gear import collect

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/reports/')
@app.route('/reports/<int:page>')
def reports(page=1):
    """Show reports list."""
    data = collect.reports()
    size = sosweb.PAGESIZE
    start = (page-1)*size
    end = start+size
    dat = data[start:end]
    page_next = page
    page_back = page-1
    link_count = int(round(len(data)/float(size)))
    current_link = page_next
    if page_next == link_count:
        page_next = -1
    return render_template('reports.html', reports=dat,
                           next_link=page_next+1, prev_link=page_back,
                           current_link=current_link, link_count=link_count)


@app.route('/extract/<report>')
def extract_report(report=None):
    """Show plugins reports"""
    output, report_status = collect.extract(report)
    if report_status != 500:
        return redirect_back('reports')
    else:
        return "Error : {}<br>Message:<br>{}".format(report_status, output)


@app.route('/reports/plain/<report>')
def plain_report(report=None):
    """Show plugins plaint text reports"""
    plain_report = collect.read(report, 'TXT')
    data = ''
    with open(plain_report) as fread:
        data = fread.readlines()
    return '<br>'.join(data).replace('  *', '&nbsp;&nbsp;*&nbsp;').replace(
          '-  commands executed:', '-&nbsp;&nbsp; commands executed:').replace(
          '-  files copied:', '-&nbsp;&nbsp; files copied:')


@app.route('/reports/html/<report>')
def html_report(report=None):
    """Show plugins html reports"""
    html_report = collect.read(report)
    if html_report:
        return render_template('report_details.html', plugins=html_report,
                               report_name=report)
    else:
        html_report = collect.read(report, 'HTML')
        data = ''
        with open(html_report) as fread:
            data = "".join(fread.readlines())
            data = data.replace('donot.css', '/static/css/donot.css')
            data = data.replace('a href="../',
                                'a href="../../report/{}/'.format(report))
            return data


@app.route('/report/', defaults={'path': ''})
@app.route('/report/<path:path>')
def report(path=None):
    """Show log content."""
    sos = sosweb.REPORT_PATH+path
    try:
        with open(sos) as fread:
            return render_template('display_report.html', fread=fread)
    except Exception as e:
        return "Can not read permission :{}".format(e)


@app.template_filter('timesince')
def timesince(date, dformat="%A, %d. %B %Y %I:%M%p"):
    """
    Returns date in correct format
    """
    return date.strftime(dformat)


if __name__ == '__main__':
    app.run(host=sosweb.HOST, port=sosweb.PORT, debug=sosweb.DEBUG)
