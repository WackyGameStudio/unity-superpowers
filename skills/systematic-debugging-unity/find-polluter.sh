#!/usr/bin/env bash
# Find which Unity test creates unwanted assets or state.
# Usage: ./find-polluter.sh <path_to_check> <test_names_file> <unity_executable> <project_path> [EditMode|PlayMode]
# Example: ./find-polluter.sh 'Assets/Generated/Debug.asset' test-names.txt "$UNITY_EDITOR" . EditMode

set -euo pipefail

if [ $# -lt 4 ] || [ $# -gt 5 ]; then
  echo "Usage: $0 <path_to_check> <test_names_file> <unity_executable> <project_path> [EditMode|PlayMode]"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_NAMES_FILE="$2"
UNITY_EDITOR="$3"
PROJECT_PATH="$4"
TEST_PLATFORM="${5:-EditMode}"

if [ ! -f "$TEST_NAMES_FILE" ]; then
  echo "Missing test names file: $TEST_NAMES_FILE"
  exit 1
fi

echo "Searching for Unity test that creates: $POLLUTION_CHECK"
echo "Project: $PROJECT_PATH"
echo "Platform: $TEST_PLATFORM"
echo ""

COUNT=0
while IFS= read -r TEST_NAME || [ -n "$TEST_NAME" ]; do
  if [ -z "$TEST_NAME" ]; then
    continue
  fi

  COUNT=$((COUNT + 1))

  if [ -e "$POLLUTION_CHECK" ]; then
    echo "Pollution already exists before test $COUNT: $TEST_NAME"
    echo "Remove it before continuing."
    exit 1
  fi

  RESULT_FILE="$(mktemp -t unity-test-results.XXXXXX.xml)"
  LOG_FILE="$(mktemp -t unity-test-log.XXXXXX.log)"

  echo "[$COUNT] Testing: $TEST_NAME"

  "$UNITY_EDITOR" \
    -batchmode \
    -projectPath "$PROJECT_PATH" \
    -runTests \
    -testPlatform "$TEST_PLATFORM" \
    -testFilter "$TEST_NAME" \
    -testResults "$RESULT_FILE" \
    -logFile "$LOG_FILE" \
    -quit >/dev/null 2>&1 || true

  if [ -e "$POLLUTION_CHECK" ]; then
    echo ""
    echo "FOUND POLLUTER"
    echo "Test: $TEST_NAME"
    echo "Created: $POLLUTION_CHECK"
    echo "Unity log: $LOG_FILE"
    echo "Test results: $RESULT_FILE"
    exit 1
  fi

  rm -f "$RESULT_FILE" "$LOG_FILE"
done < "$TEST_NAMES_FILE"

echo ""
echo "No polluter found."
exit 0
