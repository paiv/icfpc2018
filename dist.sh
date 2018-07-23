#!/usr/bin/env bash
set -e

TARGET_FILE='paivf-1.zip'

if [ -z "$1" ]; then
    echo 'usage: dist <dir>'
    exit 1
fi

. .secrets

MYDIR=$(pwd)
pushd "$1"

zip --encrypt --password "$ICFPC_TEAM_SECRET" "$MYDIR/$TARGET_FILE" *.nbt

popd

SHACODE=$(shasum -a 256 "$TARGET_FILE" | cut -d ' ' -f1)
echo "SHA-256: $SHACODE"

echo "Upload $TARGET_FILE and give me the share link:"
read -p 'Share link: ' -r SHARE_URL

# curl -L \
#   --data-urlencode action=submit \
#   --data-urlencode privateID="$ICFPC_TEAM_SECRET" \
#   --data-urlencode submissionURL="$SHARE_URL" \
#   --data-urlencode submissionSHA="$SHACODE" \
#   https://script.google.com/macros/s/AKfycbzQ7Etsj7NXCN5thGthCvApancl5vni5SFsb1UoKgZQwTzXlrH7/exec

curl -L \
  --data-urlencode entry.1763695394="$ICFPC_TEAM_SECRET" \
  --data-urlencode entry.1501594990="$SHARE_URL" \
  --data-urlencode entry.1453391049="$SHACODE" \
  https://docs.google.com/forms/u/2/d/e/1FAIpQLSd0RMj0IUNsoVmhlQotcDVMZakK921zShK8H42zQJiweRhb4g/formResponse
