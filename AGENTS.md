# Repository Guidelines

## Project Structure & Module Organization
- Core app entrypoint: `app.py` (Flask).
- Primary engines: `InsightEngine/`, `MediaEngine/`, `QueryEngine/`, `ReportEngine/`, `ForumEngine/`.
- Data collection: `MindSpider/`.
- Models: `SentimentAnalysisModel/`.
- Supporting systems: `thinking/`, `utils/`, `migrations/`.
- Web assets/templates: `static/`, `templates/`.
- Tests: `tests/` (pytest is configured to discover `test_*.py`).
- Config/scripts: `config/`, `scripts/`, `deploy.sh`, `docker-compose*.yml`.

## Build, Test, and Development Commands
- `python -m venv venv && source venv/bin/activate` — create/activate a virtual environment.
- `pip install -r requirements.txt` — install Python dependencies.
- `python app.py` — run the Flask app locally.
- `python run_unit_tests.py` — run the unit test runner (works around some pytest conflicts).
- `pytest -v` — run pytest using settings in `pytest.ini`.
- `./deploy.sh` or `docker-compose -f docker-compose.yml up` — containerized deployment options.

## Coding Style & Naming Conventions
- Python 3.9+ codebase; follow PEP 8 conventions where not stated otherwise.
- Indentation: 4 spaces; no tabs.
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Keep modules focused: place agent-specific logic inside the corresponding `*Engine/` directory.

## Testing Guidelines
- Pytest configuration lives in `pytest.ini` (`testpaths = tests`, `python_files = test_*.py`).
- Markers used: `unit`, `integration`, `security`, `performance`.
- Some long-running or environment-dependent tests are excluded via `collect_ignore` in `pytest.ini`.
- When adding tests, name files `test_*.py` and keep them under `tests/`.

## Commit & Pull Request Guidelines
- Commit messages follow a Conventional Commits style: `type: short description` (e.g., `fix: handle empty query`).
- Branch naming: `feature/your-feature` or `fix/your-fix`.
- PRs target `main` and should include a clear summary of changes and any related issue links.
- Include screenshots/logs when a change affects UI, reports, or external integrations.

## Configuration & Security Notes
- Copy `.env.example` (or `.env.prod.template` for production) and fill in API keys/DB settings.
- Do not commit `.env` files or credentials.
- Health endpoints: `/health`, `/ready`, `/metrics` for local validation.
