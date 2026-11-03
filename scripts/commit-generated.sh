#!/usr/bin/env bash
# Commit regenerated images in profile/ and push them.
#
# Used by .github/workflows/profile.yml. To keep history small, when the
# commit at the tip of the branch is already one of these bot commits (same
# message, only touches profile/), it is amended and force-pushed with a lease
# instead of stacking a new commit every day. If that push is refused (for
# example by branch protection, or because someone pushed in the meantime),
# it falls back to an ordinary new commit.
#
# Usage: scripts/commit-generated.sh ["commit message"]

set -euo pipefail

msg="${1:-Update profile cards}"
branch="${GITHUB_REF_NAME:?GITHUB_REF_NAME is not set; run this from GitHub Actions}"
bot_name="github-actions[bot]"
bot_email="41898282+github-actions[bot]@users.noreply.github.com"

git config user.name "$bot_name"
git config user.email "$bot_email"

mkdir -p profile
git add -A profile
if git diff --cached --quiet; then
  echo "No changes in profile/, nothing to commit."
  exit 0
fi

# Is HEAD one of our own image commits?
amend=false
if [ "$(git log -1 --format=%ae)" = "$bot_email" ] &&
   [ "$(git log -1 --format=%s)" = "$msg" ] &&
   git rev-parse -q --verify HEAD~1 >/dev/null &&
   ! git diff --name-only HEAD~1 HEAD | grep -qv '^profile/'; then
  amend=true
fi

if [ "$amend" = true ]; then
  old="$(git rev-parse HEAD)"
  git commit --amend --no-edit --quiet
  if git push --quiet --force-with-lease="refs/heads/$branch:$old" origin "HEAD:refs/heads/$branch"; then
    echo "Amended the previous image commit ${old:0:7}."
    exit 0
  fi
  echo "::warning::Could not replace the previous image commit; making a new commit instead."
  # Back to the original tip, keeping today's images staged.
  git reset --quiet --soft "$old"
fi

git commit --quiet -m "$msg"
for attempt in 1 2 3; do
  if git push --quiet origin "HEAD:refs/heads/$branch"; then
    echo "Pushed a new image commit."
    exit 0
  fi
  echo "Push rejected (attempt $attempt); rebasing onto the latest $branch."
  git pull --quiet --rebase origin "$branch"
done
echo "::error::Could not push the updated images."
exit 1
