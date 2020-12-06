#!/usr/bin/env bash
set -euo pipefail

usage() {
cat <<EOF
Commands
  list-tests
  test [--trust <host>] [-Dkey=value] <name> [name] [...]
  smoke-test
  regression-test
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

# Runs Smoke Tests
doSmokeTest() {
  echo "Running Smoke tests..."
  poetry run "test"
  RETURN_STATUS=$?
  echo "Return status: $RETURN_STATUS"
  exit "$RETURN_STATUS"
}

# Runs the Regression Test Suite
doRegressionTest() {
  echo "Running Regression tests..."
  poetry run "test"
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
  r|regression-test) doRegressionTest;;
  *) usage "Unknown command: $COMMAND";;
esac

exit 0