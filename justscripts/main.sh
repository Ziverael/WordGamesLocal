#!/usr/bin/env sh
# shellcheck disable=SC2015
# shellcheck disable=SC2120
# shellcheck disable=SC1091
. justscripts/env.sh
. justscripts/setup.sh
. justscripts/shell.sh
. justscripts/podman.sh

# Containers are a development aid only (tests, tooling).
# The application itself is a Kivy desktop program run on the host.
COMPOSE_FILE="docker-compose-dev.yaml"

init_project(){
    echo_title "Initializing project..."
    check_if_name_set "verbose"
    create_default_directories_and_files
    init_local_venv
    create_or_update_dotenv
    rebuild_project_image
}

refresh_project(){
    echo_title "Refreshing project..."
    stop_project_services
    sync_local_venv
    create_or_update_dotenv
    rebuild_project_image
    start_dev_helper
}

up_project(){
    echo_title "Starting project..."
    start_dev_helper
}

down_project(){
    echo_title "Stop project..."
    stop_project_services
}

run_app(){
    echo_title "Starting Word Games ($1 client)..."
    uv run "word-games-$1"
}

package_clients(){
    echo_title "Building teacher and student clients into dist/..."
    # Without this Kivy takes over Python logging and prints PyInstaller's
    # debug and trace records: hundreds of thousands of lines per build.
    KIVY_LOG_MODE=PYTHON uv run --group package pyinstaller --noconfirm packaging/word_games.spec
}

stop_project_services(){
    echo_default "Stopping project services..."
    podman-compose -f "${COMPOSE_FILE}" down
}

start_dev_helper(){
    echo_default "Starting dev helper..."
    start_service_if_it_is_not_running wordgames-app-dev-helper "${COMPOSE_FILE}"
}

stop_dev_helper(){
    echo_default "Stopping dev helper..."
    stop_service_if_it_is_running wordgames-app-dev-helper "${COMPOSE_FILE}"
}

rebuild_project_image(){
    podman-compose -f "${COMPOSE_FILE}" build wordgames-app-image
}

format_code () {
    TARGET="${1:-./}"
    IGNORE="${2}"
    [ -f "${TARGET}" ] && [ "$(get_lowercase_file_extension "${TARGET}")" != "py" ]\
        && echo "Not a python file. Skipped." && return
    [ -n "${IGNORE}" ] && IGNORE="--ignore ${IGNORE}"
    echo_title "Starting reformat with ruff..."
    uv run ruff format "${TARGET}" || ERROR=$?
    # shellcheck disable=SC2086
    uv run ruff check --fix ${IGNORE} "${TARGET}" || ERROR=$?
    show_ruff_hints_if_error_encountered ${ERROR}
}

check_code () {
    echo_title "Starting check with ruff..."
    uv run ruff check . || ERROR=$?
    uv run ruff format --check . || ERROR=$?
    show_ruff_hints_if_error_encountered ${ERROR}
    echo_title "Starting check with mypy..."
    uv run mypy --incremental --show-error-codes --pretty || ERROR=$?
    return $ERROR
}

show_ruff_hints_if_error_encountered () {
    ERROR="${1}"
    if [ -n "${ERROR}" ]
    then
        echo_default "Rule details available at https://docs.astral.sh/ruff/rules/."
    fi
}

test_code () {
    _test_path="${1:-./tests}"
    _opts="${2}"
    echo_title "Starting tests with pytest..."
    start_dev_helper
    _opts="${_opts} --cov word_games"
    _opts="${_opts} --cov-report html:coverage/htmlcov"
    _opts="${_opts} --cov-report xml:coverage/coverage.xml"
    _opts="${_opts} --cache-clear"
    _opts="${_opts} --pyargs ${_test_path}"
    # shellcheck disable=SC2086
    podman-compose -f "${COMPOSE_FILE}" exec wordgames-app-dev-helper uv run --no-sync pytest ${_opts}
    echo "Coverage report available at $(pwd)/.local/coverage/htmlcov/index.html."
}

start_bash_session(){
    start_dev_helper
    podman-compose -f "${COMPOSE_FILE}" exec wordgames-app-dev-helper bash
}

clean_pycached () {
    echo_title "Removing all __pycache__ directories and *.py[cod] files..."
    find . -type f -name "*.py[cod]" -delete -or -type d -name "__pycache__" -prune -exec rm -rf {} +
    echo_default "Done"
}

open_code_coverage_report () {
    echo_title "Opening code coverage report..."
    if [ -f ".local/coverage/htmlcov/index.html" ]
    then
        open_in_browser ".local/coverage/htmlcov/index.html"
    else
        echo_warning "Coverage report not found..."
    fi
}

profile_python_code () {
    FILE="${1:?}"
    _report=".local/scalene/$(basename "${FILE%.*}").html"
    echo_title "Profiling with scalene..."
    uv run scalene run "${FILE}" --html --outfile "${_report}"
    echo_title "Opening scalene report in default browser..."
    open_in_browser "${_report}"
}

init_local_venv(){
    echo_title "Initializing local venv..."
    uv sync
    echo_default "Initializing pre-commit..."
    uv run --no-sync pre-commit install
}

sync_local_venv(){
    echo_title "Synchronizing local venv..."
    uv sync
}

create_default_directories_and_files(){
    TMP_FILE=$(mktemp)
    {
        create_directory_if_it_does_not_exist ".local"
        create_directory_if_it_does_not_exist ".local/tmp"
        create_directory_if_it_does_not_exist ".local/coverage"
        create_directory_if_it_does_not_exist ".local/scalene"
        create_file_if_it_does_not_exist ".local/.bash_history"
    } >> "${TMP_FILE}"
    if [ -n "$(cat "${TMP_FILE}")" ]
    then
        echo_title "Creating files and directories..."
        echo_default "$(grep -v '^$' "${TMP_FILE}")"
    fi
    rm -f "${TMP_FILE}"
}
