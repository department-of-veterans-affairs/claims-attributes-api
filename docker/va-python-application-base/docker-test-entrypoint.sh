#!/usr/bin/env bash

# docker-test-entrypoint.sh
# Used by the deployer and deployment unit as described
# here: https://github.com/department-of-veterans-affairs/health-apis-deployer/blob/qa/deployment-unit.md
# Usage: docker run --rm --network host api:testing [regression-test|smoke-test]

set -euo pipefail

usage() {
cat <<EOF
Commands
  list-tests
  test [--trust <host>] [-Dkey=value] <name> [name] [...]
  unit-test
  regression-test
  smoke-test
$1
EOF
exit 1
}

doListTests() {
  echo "No tests"
}

# Defaul Tests are ALL Tests
defaultTests() {
  doListTests 
}

# Runs the test using the configured properties and vars
doTest() {
  # Running specific tests otherwise do all
  local tests="$@"
  [ -z "$tests" ] && tests=$(defaultTests)

  # Run It
  # TODO

  # Exit on failure otherwise let other actions run.
  [ $? != 0 ] && exit 1
}

doUnitTest() {
  echo "Running Unit tests..."
  poetry run pytest -sv --cov=app --cov-report=xml --junitxml=test.xml
  RETURN_STATUS=$?
  echo "Return status: $RETURN_STATUS"
  exit "$RETURN_STATUS"
}

# Runs the Regression Test Suite
doRegressionTest() {
  echo "Running Regression tests..."
  poetry run pytest -sv
  RETURN_STATUS=$?
  echo "Return status: $RETURN_STATUS"
  exit "$RETURN_STATUS"
}

# Runs Smoke Tests
doSmokeTest() {
  echo "Running Smoke tests..."
  poetry run pytest -sv -m smoke
  RETURN_STATUS=$?
  echo "Return status: $RETURN_STATUS"
  exit "$RETURN_STATUS"
}

[ $# == 0 ] && usage "No command specified"
echo "Num: $#, Args: $@ , arg0: $0"
COMMAND=$1
shift
case "$COMMAND" in
  lt|list-tests) doListTests;;
  t|test) doTest "$@";;
  s|smoke-test) doSmokeTest;;
  u|unit-test) doUnitTest;;
  r|regression-test) doRegressionTest;;
  *) usage "Unknown command: $COMMAND";;
esac

exit 0