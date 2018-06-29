#! /usr/bin/python


def split_log_drop_path(log_path):
    """
    test_output_folder: i.e.  /sandbox/qadrop/automation_logs/gx/Mar29_1636/
    into:
        server_path: /sandbox/qadrop/
        test_log_folder: gx/Mar29_1636/
        Return split value or a empty strings to accommodate local test run.
    """
    if 'automation_logs' in log_path:
        return log_path.split('automation_logs/')
    else:
        return '', ''


HADES_URL_PATH = 'http://hades.corero.com/automation/'
SPLUNK_SEARCH_URL = 'https://{0}:8000/en-GB/app/securewatch_analytics/search?q=search%20index%3D*%20earliest%3D{1}%20latest%3D{2}'
TEST_RESULT_COMMENT_URL = '[{0}]({1})'

REPORT_TEMPLATE = """<html>
    <head></head>
    <body style='font-family:Calibri; font-size:90%'>
        <style type='text/css'>
            <!--
                .tab {{ margin-left: 40px; }}
            -->
        </style>
        <p>Hi<br>Test report<br></p>
        <p>{0}
        <br><br>{1}
        </p>
        {2}{3}
    </body>
</html>"""

STATS_TEMPLATE = """Total = {0}
<p class='tab'>
    Pass = {1}<br>
    Fail = {2}<br>
    Blocked = {3}<br>
</p>
Executed = {1} + {2} = {4}<br>
Pass Rate = {1} / {4} = {5}%<br>
Run Time: {6}"""

TEST_FILE_FOLDER = "<a href={0}{1}>Test log and diagnostic files folder</a>"

TABLE_TEMPLATE_FAILURES = """<p>List of failed tests</p>
<p><table style="width:100%; font-family:Calibri; font-size:90%">
  <tr>
    <td>ID</td>
    test<td>Version</td>
    <td>Title</td>
    <td>Bug ID</td>
    <td>Last 7 runs</td>
    <td>History</td>
  </tr>
  {0}
</table></p>"""

ROW_TEMPLATE_FAILURES = """<tr>
<td>{0}</td>
<td>{1}</td>
<td>{2}</td>
<td>{3}</td>
<td bgcolor="#ff3300">Failed {4}x</td>
<td>{5}</td>
</tr>"""

TABLE_TEMPLATE_ALL_RESULTS = """<p>List of all test results</p>
<p><table style="width:100%; font-family:Calibri; font-size:90%">
  <tr>
    <td>ID</td>
    <td>Version</td>
    <td>Title</td>
    <td>Status</td>
    <td>History</td>
  </tr>
  {0}
</table></p>"""

ROW_TEMPLATE_ALL_RESULTS = """<tr>
<td>{0}</td>
<td>{1}</td>
<td>{2}</td>
<td bgcolor="{3}">{4}</td>
<td>{5}</td>
</tr>"""

ROW_TEMPLATE_SECTION = """<tr><th colspan=4>{0}</th></tr>"""

RESULT_HISTORY = """<table style="width:50%">{0}</table>"""
RESULT_HISTORY_ENTRY = """<td bgcolor="{0}"></td>"""

TEST_TITLE = '<a href="http://testrail.corero.com/testrail/index.php?/tests/view/{0}">{1}</a>'
BUG_ID = '<a href="https://jira.corero.com/browse/{0}">{0}</a>'
EMAIL_TITLE = '{0}, Pass rate {1}% ({2}/{3}) - {4}'
TIME_TAKEN = '{0} hours {1} minutes'
