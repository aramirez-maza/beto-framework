"""
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.CLI_TOOL
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.TARGET_USERS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C1_NON_DESTRUCTIVE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C2_RECURSIVE_SCOPE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C3_REPORT_COMPLETENESS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R1_PERMISSION_ERRORS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R2_HASH_COLLISION
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R3_LARGE_DIRECTORY_TREES
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.CALCULATE_RECOVERABLE_SPACE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.OUTPUT.TOTAL_RECOVERABLE_SPACE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.SPACE_CALCULATOR
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.SPACE_CALCULATION
"""

import typing

class SpaceCalculator:
    def calculate_recoverable_space(self, duplicate_groups: typing.List[typing.Dict[str, typing.Any]]) -> typing.Dict[str, typing.Any]:
        total_recoverable_bytes = 0
        for group in duplicate_groups:
            group_size = group['group_size']
            num_duplicates = len(group['file_paths']) - 1
            recoverable_bytes = group_size * num_duplicates
            group['recoverable_bytes'] = recoverable_bytes
            total_recoverable_bytes += recoverable_bytes
        
        return {
            'duplicate_groups': duplicate_groups,
            'total_recoverable_bytes': total_recoverable_bytes
        }