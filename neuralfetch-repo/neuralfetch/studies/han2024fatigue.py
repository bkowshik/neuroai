# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""Han et al. 2024 SSVEP fatigue dataset (MOABB: Han2024Fatigue).

Generated stub (scripts/generate_moabb_study.py); bibtex/description/_info
still need curation + a full-download _info capture before PR.
"""

from __future__ import annotations

import typing as tp

from neuralfetch.studies.moabb2025 import _BaseMoabb
from neuralset.events import study as studies


class Han2024Fatigue(_BaseMoabb):
    """Subset of MOABB: Han2024Fatigue — 32-class SSVEP, alert vs fatigue.

    SSVEP EEG recorded in alert and fatigue sessions (dynamic-stopping
    paradigm), 24 subjects, 64 channels @ 1000 Hz. Useful for fatigue and
    cross-session domain-shift studies.
    """

    aliases: tp.ClassVar[tuple[str, ...]] = ("Han2024Fatigue",)
    # If a real load needs an extra reader package (e.g. curryreader), add a
    # `requirements` DELTA here (base auto-prepends moabb>=1.5.0). Default: none.
    bibtex: tp.ClassVar[str] = """
        @article{han2024fatigue,
          doi = {10.1109/TNSRE.2024.3380635},
          url = {https://doi.org/10.1109/TNSRE.2024.3380635},
          author = {TODO: paste verbatim Google Scholar BibTeX},
          title = {TODO},
          year = {2024}
        }
    """
    url: tp.ClassVar[str] = "https://zenodo.org/records/10507229"
    licence: tp.ClassVar[str] = "CC-BY-4.0"
    description: tp.ClassVar[str] = (
        "SSVEP EEG (64-ch @ 1000 Hz) across alert and fatigue sessions in "
        "24 subjects; for fatigue / cross-session domain-shift studies."
    )
    event_id: tp.ClassVar[dict[str, int]] = {
        "8": 1,
        "12.5": 10,
        "13": 11,
        "13.5": 12,
        "14": 13,
        "14.5": 14,
        "15": 15,
        "15.5": 16,
        "25.5": 17,
        "26": 18,
        "26.5": 19,
        "8.5": 2,
        "27": 20,
        "27.5": 21,
        "28": 22,
        "28.5": 23,
        "29": 24,
        "29.5": 25,
        "30": 26,
        "30.5": 27,
        "31": 28,
        "31.5": 29,
        "9": 3,
        "32": 30,
        "32.5": 31,
        "33": 32,
        "9.5": 4,
        "10": 5,
        "10.5": 6,
        "11": 7,
        "11.5": 8,
        "12": 9,
    }
    # Capture _info from a FULL download, then paste the literal here:
    #   update_source_info("Han2024Fatigue")
    _info: tp.ClassVar[studies.StudyInfo | None] = None
