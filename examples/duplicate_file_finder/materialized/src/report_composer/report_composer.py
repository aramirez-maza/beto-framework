"""
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.CLI_TOOL
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.TARGET_USERS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C1_NON_DESTRUCTIVE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C2_RECURSIVE_SCOPE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C3_REPORT_COMPLETENESS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R1_PERMISSION_ERRORS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.GENERATE_REPORT
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.OUTPUT.REPORT_ARTIFACT
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.REPORT_COMPOSER
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.REPORT_SIDE_EFFECT
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.REPORT_GENERATION
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC8.DECISION.REPORT_OUTPUT_FORMAT
"""

import json
from typing import List, Dict

class ReportComposer:
    def __init__(self, duplicate_groups: List[Dict[str, any]], total_recoverable_bytes: int):
        self.duplicate_groups = duplicate_groups
        self.total_recoverable_bytes = total_recoverable_bytes

    def generate_report(self, output_format: str = 'json', output_file: str = None) -> str:
        """
        Generates the report based on the duplicate groups and total recoverable bytes.
        
        :param output_format: Format of the report ('json', 'text')
        :param output_file: File path to write the report (optional)
        :return: Report as a string
        """
        report_data = {
            'duplicate_groups': self.duplicate_groups,
            'total_recoverable_bytes': self.total_recoverable_bytes
        }

        if output_format == 'json':
            report_str = json.dumps(report_data, indent=4)
        elif output_format == 'text':
            report_str = self._generate_text_report()
        else:
            raise ValueError("Unsupported output format")

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_str)

        return report_str

    def _generate_text_report(self) -> str:
        """
        Generates a human-readable text report.
        
        :return: Text report as a string
        """
        report_lines = [
            f"Total Recoverable Bytes: {self.total_recoverable_bytes}\n"
        ]

        for group in self.duplicate_groups:
            report_lines.append(f"Content Hash: {group['content_hash']}\n")
            report_lines.append("File Paths:\n")
            for file_path in group['file_paths']:
                report_lines.append(f"  {file_path}\n")
            report_lines.append("\n")

        return ''.join(report_lines)