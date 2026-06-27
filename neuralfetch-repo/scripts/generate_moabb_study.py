"""Dev tool: emit a literal ``_BaseMoabb`` Study wrapper from a MOABB dataset.

Not shipped (lives under ``scripts/``, not packaged). It reads the moabb
dataset object (constructor only — NO download) and prints a paste-ready
``class X(_BaseMoabb): ...`` block with ``event_id`` and catalog-derived
metadata baked in as literals. Everything that genuinely needs a human or a
real download is emitted as a clearly-marked TODO:

  * class-name keyword (Scholar BibTeX key)   -> --class-name
  * full bibtex authors/title                  -> TODO in the block
  * extra reader deps (e.g. curryreader)       -> only surface on a real load
  * _info (num_timelines/data_shape/...)       -> capture after a full download

The produced wrapper is indistinguishable from a hand-written one, so every
existing mechanism (discovery, exca cache, StudyInfo tests) works unchanged.

Usage::

    python scripts/generate_moabb_study.py Wu2020 --class-name Wu2020Investigation
"""

from __future__ import annotations

import argparse
import re
import sys


def _meta(ds: object) -> dict:
    md = getattr(ds, "metadata", None)

    def g(group: str, attr: str) -> object:
        obj = getattr(md, group, None) if md else None
        return getattr(obj, attr, None) if obj is not None else None

    return {
        "sampling_rate": g("acquisition", "sampling_rate"),
        "n_channels": g("acquisition", "n_channels"),
        "n_subjects": g("participants", "n_subjects"),
        "license": g("documentation", "license"),
        "description": g("documentation", "description"),
        "data_url": g("documentation", "data_url"),
    }


def _event_id_literal(event_id: dict) -> tuple[str, str, list[str]]:
    """Return ``(literal, type_annotation, warnings)``."""
    items = sorted(event_id.items(), key=lambda kv: (str(kv[1]), kv[0]))
    warns: list[str] = []
    list_valued = any(isinstance(v, list) for v in event_id.values())
    numeric_keys = all(re.fullmatch(r"-?\d+(\.\d+)?", str(k)) for k in event_id)
    if list_valued:
        ann = "dict[str, list[int]]"
        warns.append("list-valued codes -> base handles via has_list_codes branch")
    else:
        ann = "dict[str, int]"
    if numeric_keys:
        warns.append(
            "numeric event_id keys -> _rename_numeric_descriptions applies; "
            "if this is a c-VEP dataset, subclass _BaseCvepTrialMoabb instead"
        )
    body = ", ".join(f'"{k}": {v!r}' for k, v in items)
    return "{" + body + "}", ann, warns


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate a _BaseMoabb wrapper stub.")
    ap.add_argument("moabb_name", help="MOABB dataset class name, e.g. Wu2020")
    ap.add_argument(
        "--class-name",
        default=None,
        help="neuroai class name (PascalCase Scholar key, e.g. Wu2020Investigation)",
    )
    args = ap.parse_args()

    from moabb.datasets.utils import dataset_list

    by = {c.__name__: c for c in dataset_list}
    if args.moabb_name not in by:
        sys.exit(f"MOABB dataset not found: {args.moabb_name}")

    ds = by[args.moabb_name]()  # constructor only — no download
    m = _meta(ds)
    cls = args.class_name or args.moabb_name
    bibkey = cls.lower()
    doi = getattr(ds, "doi", None) or ""
    year_match = re.search(r"(19|20)\d{2}", args.moabb_name)
    year = year_match.group(0) if year_match else "TODO"
    eid_lit, eid_ann, warns = _event_id_literal(dict(ds.event_id))

    url = m["data_url"] or (f"https://doi.org/{doi}" if doi else "TODO")
    url_note = "" if m["data_url"] else "  # TODO: prefer a data DOI/archive URL"
    licence = m["license"] or "UNKNOWN"
    lic_note = "" if m["license"] else "  # TODO: verify against the licence page"
    descr = m["description"] or (
        f"TODO: 1-2 sentence summary. paradigm={ds.paradigm}, "
        f"n_subjects={m['n_subjects']}, {m['n_channels']}-ch @ {m['sampling_rate']}Hz."
    )

    block = f'''class {cls}(_BaseMoabb):
    """Subset of MOABB: {args.moabb_name}.

    TODO: 2-4 sentence description. Paradigm={ds.paradigm};
    {m["n_subjects"]} subjects; {m["n_channels"]}-ch @ {m["sampling_rate"]}Hz.
    """

    aliases: tp.ClassVar[tuple[str, ...]] = ("{args.moabb_name}",)
    # If a real load needs an extra reader package (e.g. curryreader), add a
    # `requirements` DELTA here (base auto-prepends moabb>=1.5.0). Default: none.
    bibtex: tp.ClassVar[str] = """
        @article{{{bibkey},
          doi = {{{doi}}},
          url = {{https://doi.org/{doi}}},
          author = {{TODO: paste verbatim Google Scholar BibTeX}},
          title = {{TODO}},
          year = {{{year}}}
        }}
    """
    url: tp.ClassVar[str] = "{url}"{url_note}
    licence: tp.ClassVar[str] = "{licence}"{lic_note}
    description: tp.ClassVar[str] = (
        "{descr}"
    )
    event_id: tp.ClassVar[{eid_ann}] = {eid_lit}
    # Capture _info from a FULL download, then paste the literal here:
    #   update_source_info("{cls}")
    _info: tp.ClassVar[studies.StudyInfo | None] = None
'''

    print("# generated by scripts/generate_moabb_study.py — curate TODOs, ruff format")
    for w in warns:
        print(f"# WARNING: {w}")
    print(block, end="")


if __name__ == "__main__":
    main()
