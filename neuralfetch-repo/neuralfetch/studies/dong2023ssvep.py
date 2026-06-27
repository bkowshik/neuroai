# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""Dong & Tian 2023 SSVEP dataset (MOABB: Dong2023).

Generated stub (scripts/generate_moabb_study.py); bibtex/description/_info
still need curation + a full-download _info capture before PR.
"""

from __future__ import annotations

import typing as tp

from neuralfetch.studies.moabb2025 import _BaseMoabb
from neuralset.events import study as studies


class Dong2023Ssvep(_BaseMoabb):
    """Subset of MOABB: Dong2023 — 40-class SSVEP speller.

    SSVEP EEG from 59 subjects viewing 40 targets frequency-coded from
    8.0-15.8 Hz (0.2 Hz steps). 8 channels @ 250 Hz.
    """

    aliases: tp.ClassVar[tuple[str, ...]] = ("Dong2023",)
    # If a real load needs an extra reader package (e.g. curryreader), add a
    # `requirements` DELTA here (base auto-prepends moabb>=1.5.0). Default: none.
    bibtex: tp.ClassVar[str] = """
        @article{dong2023ssvep,
          doi = {10.26599/BSA.2023.9050020},
          url = {https://doi.org/10.26599/BSA.2023.9050020},
          author = {TODO: paste verbatim Google Scholar BibTeX},
          title = {TODO},
          year = {2023}
        }
    """
    url: tp.ClassVar[str] = "https://zenodo.org/records/18847318"
    licence: tp.ClassVar[str] = "CC-BY-NC-4.0"
    description: tp.ClassVar[str] = (
        "SSVEP EEG (8-ch @ 250 Hz) from 59 subjects viewing 40 "
        "frequency-coded targets (8.0-15.8 Hz)."
    )
    event_id: tp.ClassVar[dict[str, int]] = {
        "8": 1,
        "9.8": 10,
        "10": 11,
        "10.2": 12,
        "10.4": 13,
        "10.6": 14,
        "10.8": 15,
        "11": 16,
        "11.2": 17,
        "11.4": 18,
        "11.6": 19,
        "8.2": 2,
        "11.8": 20,
        "12": 21,
        "12.2": 22,
        "12.4": 23,
        "12.6": 24,
        "12.8": 25,
        "13": 26,
        "13.2": 27,
        "13.4": 28,
        "13.6": 29,
        "8.4": 3,
        "13.8": 30,
        "14": 31,
        "14.2": 32,
        "14.4": 33,
        "14.6": 34,
        "14.8": 35,
        "15": 36,
        "15.2": 37,
        "15.4": 38,
        "15.6": 39,
        "8.6": 4,
        "15.8": 40,
        "8.8": 5,
        "9": 6,
        "9.2": 7,
        "9.4": 8,
        "9.6": 9,
    }
    # Capture _info from a FULL download, then paste the literal here:
    #   update_source_info("Dong2023Ssvep")
    _info: tp.ClassVar[studies.StudyInfo | None] = None
