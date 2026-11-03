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
# It never amends a commit that another branch is built on (an open pull
# request, a work branch), because that branch would then conflict with main in
# profile/. If you made a branch from main before this check existed and it now
# shows conflicts in profile/, update it with `git pull --rebase` (not a merge).
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
# (Outputs are captured before testing them: with pipefail, `cmd | grep -q`
# can report failure when grep exits early and cmd gets SIGPIPE.)
amend=false
if [ "$(git log -1 --format=%ae)" = "$bot_email" ] &&
   [ "$(git log -1 --format=%s)" = "$msg" ] &&
   git rev-parse -q --verify HEAD~1 >/dev/null; then
  outside_profile="$(git diff --name-only HEAD~1 HEAD | grep -v '^profile/' || true)"
  if [ -z "$outside_profile" ]; then amend=true; fi
fi

# Keep a commit that another branch is built on.
if [ "$amend" = true ]; then
  git fetch --quiet --depth=50 origin '+refs/heads/*:refs/remotes/origin/*' || true
  others="$(git for-each-ref --contains HEAD --format='%(refname)' refs/remotes/origin |
            grep -vx -e "refs/remotes/origin/$branch" -e "refs/remotes/origin/HEAD" || true)"
  if [ -n "$others" ]; then
    echo "Another branch (${others//refs\/remotes\/origin\//}) is based on the previous image commit; making a new commit instead."
    amend=false
  fi
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
  # Only profile/ is in this commit, so on a conflict the fresh images win.
  git pull --quiet --rebase -X theirs origin "$branch"
done
echo "::error::Could not push the updated images."
exit 1
