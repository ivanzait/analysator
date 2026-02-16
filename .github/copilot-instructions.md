<!-- Copilot / AI agent instructions for the Analysator repository -->

Purpose
- Provide succinct, actionable guidance so an AI coding assistant can be immediately productive editing Analysator.

Quick orientation
- Big picture: Analysator is a Python utility library and CLI-like collection of scripts for reading and analysing Vlasiator `.vlsv` files. Core components live under the `analysator/` package: mesh & file readers (`pyVlsv/`), calculation helpers (`pyCalculations/`), plotting (`pyPlots/`), and misc helpers (`miscellaneous/`). See [README.md](README.md) for user-level install/run instructions.
- Packaging: The project uses `pyproject.toml` with `hatchling` as the build backend. Typical dev install: `pip install --editable ./analysator` from the repo root. Dependencies are listed in [requirements.txt](requirements.txt) and `pyproject.toml`.

Important repository conventions
- Modules are usually imported as bare module names because `analysator/__init__.py` injects subdirectories into `sys.path`. Example: imports like `import vlsvfile` or `import calculations` are expected and should not be blindly converted to fully qualified package imports (changing these may break runtime behavior).
- Lazy imports: `analysator/__init__.py` defines `lazyimport()` and many modules are loaded lazily at runtime — respect this pattern when adding new modules or refactoring to avoid startup costs.
- Environment-driven behavior: runtime flags are controlled via environment variables (examples):
  - `PTNONINTERACTIVE` — disable interactive plotting
  - `PTBACKEND` — matplotlib backend override
  - `PTNOLATEX` — disable LaTeX rendering
  - `PTOUTPUTDIR` — default output directory
  - `ANALYSATOR_LOG_LEVEL` — logging level (default INFO)
  - `PTMAYAVI2` — opt-in loading of MayaVi2-related modules

Key implementation patterns to follow or be aware of
- I/O and binary parsing: `analysator/pyVlsv/vlsvreader.py` is the canonical vlsv reader — it reads XML footers, binary tags and exposes `VlsvReader`. New code that interacts with VLSV files should reuse `VlsvReader` or follow its read(tag=...) conventions.
- Vectorized numpy usage is pervasive; prefer numpy arrays and vectorized operations to Python loops where compatible with existing code style.
- Backwards-compatibility: the codebase supports older vlsv file variants; added features should preserve compatibility checks already present in readers.
- Avoid changing global import order or `sys.path` behavior unless necessary; many modules rely on the current import layout.

Build / run / debug commands (practical)
- Developer install: from repo root run:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install --editable ./analysator
  pip install -r requirements.txt
  ```
- Optional VTK extras: `pip install --editable ./analysator[vtk]` or `pip install --editable ./analysator[bvtk]` when testing VTK features.
- Run example scripts in `examples/` (e.g. `examples/generate_panel.py`) to exercise plotting and file readers. Set `PTNONINTERACTIVE=1` for non-GUI runs.

Testing and verification
- There are no formal unit tests in the repository root. Validate changes by running example scripts and small interactive sessions that import the modified modules. For reader changes, test against a small VLSV sample or create minimal mocks for `read(tag=...)` behavior.

When making edits, preferred style and constraints
- Maintain Python 3.6+ compatibility — avoid syntax only supported in very recent interpreters.
- Follow existing logging usage (use `logging.getLogger(__name__)` when adding modules; respect `ANALYSATOR_LOG_LEVEL`).
- Keep public APIs stable: many downstream scripts import top-level module names; prefer additive changes and deprecation warnings rather than breaking renames.
- Large/complex changes to `pyVlsv` or reader code: add a short runnable example in `examples/` demonstrating the change.

Files to inspect for context when modifying features
- [analysator/__init__.py](analysator/__init__.py) — sys.path injection + lazyimport
- [analysator/pyVlsv/vlsvreader.py](analysator/pyVlsv/vlsvreader.py) — canonical VLSV reader (largest single-file implementation)
- [requirements.txt](requirements.txt) and [pyproject.toml](pyproject.toml) — dependency and packaging hints
- [README.md](README.md) — install and runtime env vars examples

If you are unsure
- Prefer asking for a small runnable example (a minimal VLSV file or a short script reproducing the workflow you want to change). Changes to the reader and plotting code are easiest to validate with small example scripts in `examples/`.

Feedback
- If any runtime behavior or import layout is unclear, ask for a short failing reproduction and the target Python environment (python version and installed extras).
