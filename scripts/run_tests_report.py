#!/usr/bin/env python3
"""Advanced pytest reporter.

This runner executes pytest with a JUnit XML output file, parses the XML to
collect per-test results and timings, and prints an advanced terminal report
including a colored table of test statuses, totals, and a success rate. If
`rich` is installed it will use it for nicer tables, otherwise it falls back
to simple ANSI colored text.

Usage: python scripts/run_tests_report.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict

try:
    from rich.table import Table
    from rich.console import Console
    from rich.text import Text
    RICH_AVAILABLE = True
    console = Console()
except Exception:
    RICH_AVAILABLE = False


def run_pytest_with_junit(xml_path: Path) -> int:
    cmd = ["pytest", "-q", f"--junitxml={str(xml_path)}"]
    # Run pytest and stream stdout/stderr so user sees test logs in real time
    proc = subprocess.run(cmd)
    return proc.returncode


def parse_junit(xml_path: Path) -> List[Dict]:
    if not xml_path.exists():
        return []
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    # pytest produces a <testsuite> containing <testcase>
    results = []
    for testcase in root.findall('.//testcase'):
        name = testcase.get('name') or ''
        classname = testcase.get('classname') or ''
        time = float(testcase.get('time') or 0.0)
        status = 'passed'
        message = ''
        if testcase.find('skipped') is not None:
            status = 'skipped'
            message = testcase.find('skipped').get('message') or ''
        elif testcase.find('failure') is not None:
            status = 'failed'
            message = testcase.find('failure').text or testcase.find('failure').get('message') or ''
        elif testcase.find('error') is not None:
            status = 'failed'
            message = testcase.find('error').text or testcase.find('error').get('message') or ''

        # Try to get captured output if available under system-out
        captured = ''
        so = testcase.find('system-out')
        if so is not None and so.text:
            captured = so.text.strip()

        results.append({
            'name': name,
            'classname': classname,
            'time': time,
            'status': status,
            'message': (message or '').strip(),
            'captured': captured,
        })
    return results


def print_advanced_report(results: List[Dict]):
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'passed')
    skipped = sum(1 for r in results if r['status'] == 'skipped')
    failed = sum(1 for r in results if r['status'] == 'failed')

    success_rate = (passed / total * 100.0) if total else 0.0

    header = Text('=== Test Summary ===\n') if RICH_AVAILABLE else None
    if RICH_AVAILABLE:
        console.print(header)
        t = Table(show_header=False)
        t.add_row('Total Tests:', str(total))
        t.add_row('Passed:', str(passed))
        t.add_row('Failed:', str(failed))
        t.add_row('Skipped:', str(skipped))
        t.add_row('Success Rate:', f'{success_rate:.1f}%')
        console.print(t)
    else:
        print('=== Test Summary ===')
        print(f'Total Tests: {total}')
        print(f'Passed: {passed}')
        print(f'Failed: {failed}')
        print(f'Skipped: {skipped}')
        print(f'Success Rate: {success_rate:.1f}%')

    # Print per-test table
    if RICH_AVAILABLE:
        table = Table('Status', 'Time(s)', 'Test', 'Note', show_header=True)
        for r in results:
            status = r['status']
            status_text = Text(status.upper())
            if status == 'passed':
                status_text.stylize('green')
            elif status == 'skipped':
                status_text.stylize('yellow')
            else:
                status_text.stylize('red')

            note = r['message'] or (r['captured'].splitlines()[0] if r['captured'] else '')
            table.add_row(status_text, f"{r['time']:.3f}", f"{r['classname']}.{r['name']}", note)
        console.print('\n')
        console.print(table)
    else:
        print('\nPer-test results:')
        for r in results:
            sym = '✔' if r['status'] == 'passed' else ('-' if r['status'] == 'skipped' else '✖')
            color_start = '\x1b[32m' if r['status'] == 'passed' else ('\x1b[33m' if r['status'] == 'skipped' else '\x1b[31m')
            color_end = '\x1b[0m'
            note = r['message'] or (r['captured'].splitlines()[0] if r['captured'] else '')
            print(f"{color_start}{sym} {r['status'].upper():6}{color_end} {r['time']:.3f}s {r['classname']}.{r['name']} {note}")

    if failed == 0 and total > 0:
        ok_msg = '[PASS] All tests passed! Framework is ready to use.'
        if RICH_AVAILABLE:
            console.print('\n')
            console.print(Text(ok_msg, style='bold green'))
            console.print(Text('Framework Setup Complete!\n\nNext Steps:', style='bold'))
        else:
            print('\n' + ok_msg)
            print('\nFramework Setup Complete!\n\nNext Steps:')
    else:
        fail_msg = '[FAIL] Some tests failed. See above for details.'
        if RICH_AVAILABLE:
            console.print('\n')
            console.print(Text(fail_msg, style='bold red'))
        else:
            print('\n' + fail_msg)


def main():
    with tempfile.TemporaryDirectory() as td:
        xml_path = Path(td) / 'pytest-junit.xml'
        code = run_pytest_with_junit(xml_path)
        results = parse_junit(xml_path)
        print_advanced_report(results)
        sys.exit(code)


if __name__ == '__main__':
    main()
