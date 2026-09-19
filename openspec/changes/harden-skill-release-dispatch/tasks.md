## 1. Package quality

- [x] 1.1 Repair broken or non-granular skill references in the source package
- [x] 1.2 Add deterministic structure, link and TRACE gates with a 4.5 threshold
- [x] 1.3 Verify every skill and preserve generated evaluation evidence

## 2. Release dispatch

- [x] 2.1 Replace branch-driven or legacy dispatch with `release.published`
- [x] 2.2 Send package, release tag and peeled commit SHA to every current consumer
- [x] 2.3 Fail clearly when `SKILLS_SYNC_TOKEN` is unavailable or GitHub rejects the request

## 3. Publication

- [ ] 3.1 Validate and archive the OpenSpec change
- [ ] 3.2 Commit and push the skill package, then confirm CI
- [ ] 3.3 Create a new immutable tag and GitHub Release
- [ ] 3.4 Confirm consumer dispatch or record the exact secret-visibility blocker
