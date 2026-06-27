# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""Kaya et al. 2018 large motor-imagery dataset (MOABB: Kaya2018).

Generated stub (scripts/generate_moabb_study.py); bibtex/description/_info
still need curation + a full-download _info capture before PR.
"""

from __future__ import annotations

import typing as tp

from neuralfetch.studies.moabb2025 import _BaseMoabb
from neuralset.events import study as studies


class Kaya2018Large(_BaseMoabb):
    """Subset of MOABB: Kaya2018 — CLA motor imagery (3-class).

    Motor-imagery EEG (CLA paradigm): left hand, right hand, and passive
    rest, 19 channels @ 200 Hz. Part of a large multi-paradigm MI corpus.
    """

    aliases: tp.ClassVar[tuple[str, ...]] = ("Kaya2018",)
    # If a real load needs an extra reader package (e.g. curryreader), add a
    # `requirements` DELTA here (base auto-prepends moabb>=1.5.0). Default: none.
    bibtex: tp.ClassVar[str] = """
        @article{kaya2018large,
          doi = {10.1038/sdata.2018.211},
          url = {https://doi.org/10.1038/sdata.2018.211},
          author = {TODO: paste verbatim Google Scholar BibTeX},
          title = {TODO},
          year = {2018}
        }
    """
    url: tp.ClassVar[str] = (
        "https://figshare.com/collections/A_large_electroencephalographic_motor_imagery_dataset_for_electroencephalographic_brain_computer_interfaces/3917698"
    )
    licence: tp.ClassVar[str] = "CC-BY-4.0"
    description: tp.ClassVar[str] = (
        "Motor-imagery EEG (19-ch @ 200 Hz): left hand, right hand, and "
        "passive rest (CLA paradigm)."
    )
    event_id: tp.ClassVar[dict[str, int]] = {
        "left_hand": 1,
        "right_hand": 2,
        "passive": 3,
    }
    # Capture _info from a FULL download, then paste the literal here:
    #   update_source_info("Kaya2018Large")
    _info: tp.ClassVar[studies.StudyInfo | None] = None
