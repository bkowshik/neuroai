# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import logging
import re
import typing as tp

import mne
import pandas as pd
from mne_bids import BIDSPath, read_raw_bids

from neuralfetch import download
from neuralset.events import study

logger = logging.getLogger(__name__)

# task-film events.tsv: only the alternating speech/music stimulus blocks are
# kept; the "start task" (value 9) / "end task" (value 4) boundary markers are
# dropped (Neuralset convention: keep meaningful events, not session markers).
_STIMULUS_CODES: dict[str, int] = {"speech": 1, "music": 2}

_ACQ_RE = re.compile(r"_acq-([A-Za-z0-9]+)_")
_RUN_RE = re.compile(r"_run-([0-9]+)_")


class Berezutskaya2022Film(study.Study):
    url: tp.ClassVar[str] = "https://openneuro.org/datasets/ds003688/"
    """Berezutskaya2022Film: intracranial EEG during naturalistic audiovisual film watching.

    Open multimodal iEEG dataset recorded while participants watched a short
    (~6.5 min) audiovisual film with alternating ~30 s blocks of speech and
    music. This is the first intracranial-EEG study in the catalog (the
    framework already supports the ``Ieeg`` modality via ``Ieeg``/``IeegExtractor``).

    Experimental Design:
        - iEEG recordings (ECoG subdural grids and/or sEEG depth electrodes, 2048 Hz)
        - 51 participants with iEEG (of 63 in the full dataset; the rest are fMRI-only)
        - One ``task-film`` run per participant (a few have repeats), plus ``task-rest``
        - Paradigm: naturalistic audiovisual film with block-design speech/music stimuli

    Notes:
        - Only ``task-film`` recordings are exposed here (they carry the
          stimulus-locked speech/music labels). ``task-rest`` is intentionally
          left out of v1.
        - Channel montages vary across participants (ECoG vs sEEG, varying
          counts), so ``data_shape`` is reported for the reference timeline only.
        - The ``acq`` entity (``clinical`` / ``HDgrid``) is present on the
          recording files but absent from ``events.tsv`` (BIDS inheritance), so
          the events path is built without it.
    """

    aliases: tp.ClassVar[tuple[str, ...]] = (
        "ds003688",
        "Berezutskaya2022",
        "iEEG-fMRI film",
    )

    licence: tp.ClassVar[str] = "CC0"
    bibtex: tp.ClassVar[str] = """
    @article{berezutskaya2022open,
        title={Open multimodal {{iEEG-fMRI}} dataset from naturalistic stimulation with a short audiovisual film},
        author={Berezutskaya, Julia and Vansteensel, Mariska J. and Aarnoutse, Erik J. and Freudenburg, Zachary V. and Piantoni, Giovanni and Branco, Mariana P. and Ramsey, Nick F.},
        year=2022,
        journal={Scientific Data},
        volume={9},
        number={1},
        pages={91},
        publisher={Nature Publishing Group},
        doi={10.1038/s41597-022-01173-0},
        url={https://doi.org/10.1038/s41597-022-01173-0},
    }

    @misc{berezutskaya2022ds003688,
        title={Open multimodal {{iEEG-fMRI}} dataset from naturalistic stimulation with a short audiovisual film},
        author={Berezutskaya, Julia and Vansteensel, Mariska J. and Aarnoutse, Erik J. and Freudenburg, Zachary V. and Piantoni, Giovanni and Branco, Mariana P. and Ramsey, Nick F.},
        year=2022,
        publisher={OpenNeuro},
        doi={10.18112/openneuro.ds003688.v1.0.7},
        url={https://openneuro.org/datasets/ds003688/},
    }
    """
    description: tp.ClassVar[str] = (
        "Intracranial EEG (ECoG/sEEG) from 51 participants watching a short "
        "audiovisual film with alternating speech and music blocks. First iEEG "
        "study in the catalog."
    )
    _info: tp.ClassVar[study.StudyInfo] = study.StudyInfo(
        num_timelines=54,  # task-film iEEG recordings (51 subjects; 3 have 2 runs)
        num_subjects=51,
        # default query selects the first timeline (sub-01 task-film):
        num_events_in_query=14,  # 1 Ieeg + 13 speech/music blocks (6 speech, 7 music)
        event_types_in_query={"Ieeg", "Stimulus"},
        # 103 SEEG channels; n_times ~= RecordingDuration (420.046 s) * 2048 Hz.
        # TODO: confirm exactly with ``utils.update_source_info`` after a Sample
        # download — n_times rounding cannot be derived from the JSON sidecar alone.
        data_shape=(103, 860254),
        frequency=2048.0,
    )

    _SESSION: tp.ClassVar[str] = "iemu"
    _TASK: tp.ClassVar[str] = "film"

    def _download(self) -> None:
        download.Openneuro(study="ds003688", dset_dir=self.path).download()

    def _ieeg_subjects(self) -> list[str]:
        """Subject ids (without the ``sub-`` prefix) that have an iEEG recording."""
        participants = pd.read_csv(
            self.path / "download" / "participants.tsv", sep="\t"
        )
        ids = participants.loc[participants["iEEG"] == "yes", "participant_id"]
        return [str(pid).removeprefix("sub-") for pid in ids]

    def iter_timelines(self) -> tp.Iterator[dict[str, tp.Any]]:
        """One timeline per ``task-film`` iEEG recording, discovered on disk.

        Globs the actual files so that varying ``acq`` (clinical/HDgrid) and
        ``run`` entities are handled without hard-coding them per subject.
        """
        for sub_id in self._ieeg_subjects():
            ieeg_dir = (
                self.path / "download" / f"sub-{sub_id}" / f"ses-{self._SESSION}" / "ieeg"
            )
            pattern = f"sub-{sub_id}_ses-{self._SESSION}_task-{self._TASK}_*_ieeg.vhdr"
            for vhdr in sorted(ieeg_dir.glob(pattern)):
                acq = _ACQ_RE.search(vhdr.name)
                run = _RUN_RE.search(vhdr.name)
                yield dict(
                    subject=sub_id,
                    session=self._SESSION,
                    task=self._TASK,
                    acquisition=acq.group(1) if acq else None,
                    run=run.group(1) if run else None,
                )

    def _get_bids_path(self, timeline: dict[str, tp.Any]) -> BIDSPath:
        """BIDS path of the iEEG recording for a timeline."""
        return BIDSPath(
            subject=timeline["subject"],
            session=timeline["session"],
            task=timeline["task"],
            acquisition=timeline["acquisition"],
            run=timeline["run"],
            datatype="ieeg",
            suffix="ieeg",
            extension=".vhdr",
            root=self.path / "download",
        )

    def _load_timeline_events(self, timeline: dict[str, tp.Any]) -> pd.DataFrame:
        # events.tsv drops the acq entity (BIDS inheritance) — clear it.
        events_path = (
            self._get_bids_path(timeline)
            .copy()
            .update(acquisition=None, suffix="events", extension=".tsv")
        )
        raw = pd.read_csv(events_path.fpath, sep="\t")
        stim = raw[raw["trial_type"].isin(_STIMULUS_CODES)].copy()
        stim = stim.rename(columns={"onset": "start", "trial_type": "description"})
        stim["type"] = "Stimulus"
        stim["modality"] = "audio"
        stim["code"] = stim["description"].map(_STIMULUS_CODES)
        stim = stim[["type", "start", "duration", "code", "modality", "description"]]

        loader = study.SpecialLoader(method=self._load_raw, timeline=timeline).to_json()
        ieeg = pd.DataFrame([dict(type="Ieeg", filepath=loader, start=0)])
        return pd.concat([ieeg, stim], ignore_index=True)

    def _load_raw(self, timeline: dict[str, tp.Any]) -> mne.io.BaseRaw:
        # channels.tsv types (SEEG/ECOG) map to seeg/ecog, which IeegExtractor
        # picks; electrodes.tsv positions are applied automatically by mne-bids.
        return read_raw_bids(self._get_bids_path(timeline), verbose=False)


# # # # # mini dataset # # # # #


class Berezutskaya2022FilmSample(Berezutskaya2022Film):
    """Sample version of Berezutskaya2022Film: one subject for fast CI.

    Downloads only ``sub-01`` (sEEG, 103 channels) and its ``task-film`` run —
    a few hundred MB rather than the full ~16 GB dataset.

    OpenNeuro dataset: https://openneuro.org/datasets/ds003688/
    Data: iEEG (ECoG/sEEG), 2048 Hz, naturalistic audiovisual film (speech/music)
    """

    description: tp.ClassVar[str] = (
        "Sample Berezutskaya2022Film: 1 subject (sub-01, sEEG) for rapid testing. "
        "iEEG during audiovisual film with speech/music blocks."
    )

    _SAMPLE_SUBJECTS: tp.ClassVar[tuple[str, ...]] = ("01",)

    _info: tp.ClassVar[study.StudyInfo] = study.StudyInfo(
        num_timelines=1,
        num_subjects=1,
        num_events_in_query=14,  # 1 Ieeg + 13 speech/music blocks
        event_types_in_query={"Ieeg", "Stimulus"},
        data_shape=(103, 860254),  # TODO: confirm via update_source_info
        frequency=2048.0,
    )

    def _download(self) -> None:
        include = [
            "dataset_description.json",
            "participants.tsv",
            "participants.json",
        ] + [f"sub-{sub_id}/**" for sub_id in self._SAMPLE_SUBJECTS]
        download.Openneuro(
            study="ds003688", dset_dir=self.path, include=include
        ).download()

    def _ieeg_subjects(self) -> list[str]:
        return list(self._SAMPLE_SUBJECTS)
