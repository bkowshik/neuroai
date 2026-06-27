# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""Ear-EEG motor execution dataset from Wu et al. 2020 (MOABB: ``Wu2020``).

New-module proof-of-concept: subclasses ``_BaseMoabb`` from ``moabb2025``
rather than living inside it, so the existing module (and the in-flight PRs
that touch it) stay untouched.
"""

from __future__ import annotations

import typing as tp

from neuralfetch.studies.moabb2025 import _BaseMoabb
from neuralset.events import study as studies


class Wu2020Investigation(_BaseMoabb):
    """Subset of MOABB: Wu2020 — scalp + in-ear EEG motor execution.

    Motor **execution** (not imagery): participants physically clenched the
    left or right fist. 6 healthy participants recorded with 122-channel scalp
    EEG plus in-ear EEG electrodes. Re-hosted on Zenodo (record 18961128);
    original IEEE DataPort DOI 10.21227/j7rq-2p11.
    """

    aliases: tp.ClassVar[tuple[str, ...]] = ("Wu2020",)
    # List ONLY the extra dep: base.Step.__init_subclass__ auto-prepends the
    # base's ("moabb>=1.5.0",). Curry .dat reading (mne.io.read_raw_curry)
    # needs curryreader — surfaced by the end-to-end download proof.
    requirements: tp.ClassVar[tuple[str, ...]] = ("curryreader",)
    bibtex: tp.ClassVar[str] = """
        @article{wu2020investigation,
          doi = {10.1088/1741-2552/abc1b6},
          url = {https://doi.org/10.1088/1741-2552/abc1b6},
          author = {Wu, X. and Zhang, W. and Fu, Z. and
                    Cheung, R. T. H. and Chan, R. H. M.},
          title = {An investigation of in-ear sensing for motor task
                   classification},
          journal = {Journal of Neural Engineering},
          volume = {17},
          number = {6},
          pages = {066029},
          year = {2020}
        }
    """
    url: tp.ClassVar[str] = "https://zenodo.org/records/18961128"
    licence: tp.ClassVar[str] = "CC-BY-4.0"
    description: tp.ClassVar[str] = (
        "Motor execution EEG (122-ch scalp + in-ear) in 6 participants "
        "clenching the left or right fist."
    )
    event_id: tp.ClassVar[dict[str, int]] = {"left_hand": 1, "right_hand": 2}
    # Capture _info from a FULL (all-6-subject) download on Colab — see the
    # capture snippet: run download()+run(), then compute_study_info(...) and
    # paste the printed ``studies.StudyInfo(...)`` here. Until then None (the
    # study still downloads/runs; test_study_info skips when _info is None).
    _info: tp.ClassVar[studies.StudyInfo | None] = None
