#!/usr/bin/env python

import unittest

import sys
import json
from subprocess import check_output

# public APP key for mPulse Demo
KEY = "PH7E4-H9YBZ-6NM8T-L4UQK-ZJAPW"
CMD = f"./bin/akamai-mpulse --json --api {KEY}"

class ModuleTest(unittest.TestCase):
  def test_summary(self):
    cmd = CMD.split() + ['--type', 'summary', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ('median', 'moe', 'n', 'p95', 'p98'):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_histogram(self):
    cmd = CMD.split() + ['--type', 'histogram', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("chartTitle", "chartTitleSuffix", "datasetName", "reportType", "resultName", "series"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_sessions_pplt(self):
    """Check sessions-per-page-load-time output"""
    cmd = CMD.split() + ['--type', 'sessions-per-page-load-time', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("chartTitle", "chartTitleSuffix", "datasetName", "reportType", "resultName", "series"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_metric_pplt(self):
    """Check metric-per-page-load-time output"""
    cmd = CMD.split() + ['--type', 'metric-per-page-load-time', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("chartTitle", "chartTitleSuffix", "datasetName", "reportType", "resultName", "series"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_by_minute(self):
    cmd = CMD.split() + ['--type', 'by-minute', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("chartTitle", "chartTitleSuffix", "datasetName", "reportType", "resultName", "series"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_geography(self):
    cmd = CMD.split() + ['--type', 'geography', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    self.assertIn('data', ret, "Tests if response has a field: data")

    data = ret.get('data') or []
    for entry in data:
      for i in ("country", "timerMOE", "timerN", "timerMedian", "timerID"):
        self.assertIn(i, entry, f"Tests if per-country entry has a field: {i}")
      break # only check first entry

  def test_page_groups(self):
    cmd = CMD.split() + ['--type', 'page-groups', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("columnNames", "data"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_browsers(self):
    cmd = CMD.split() + ['--type', 'browsers', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("columnNames", "data"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_bandwidth(self):
    cmd = CMD.split() + ['--type', 'bandwidth', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("chartTitle", "chartTitleSuffix", "datasetName", "reportType", "resultName", "series"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_ab_tests(self):
    cmd = CMD.split() + ['--type', 'ab-tests', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("columnNames", "data"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_timers_metrics(self):
    cmd = CMD.split() + ['--type', 'timers-metrics', '--timer', 'PageLoad']
    ret = json.loads(check_output(cmd))

    for i in ("dataTimeZone", "values"):
      self.assertIn(i, ret, f"Tests if response has a field: {i}")

  def test_metrics_by_dimension(self):
    pass

  def test_dimension_values(self):
    pass

if __name__ == '__main__':
  unittest.main()
