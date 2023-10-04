#!/usr/bin/env sh

die() {
    echo "$1"; exit 1
}
[ -z "$CONTAINER_NAME" ] && die 'CONTAINER_NAME is not set! Set envvar $CONTAINER_NAME'

runner_args=(run --rm -v $(git rev-parse --show-toplevel)/config.json.tmpl:/config.json.tmpl -e REDMINE_URL=$REDMINE_URL -e CFG=/config.json.tmpl -e K=$K -e T=$T "$CONTAINER_NAME")

case "$CONTAINER_RUNTIME" in
     podman)
         podman ${runner_args[@]};;
     *)
         docker ${runner_args[@]};;
esac
