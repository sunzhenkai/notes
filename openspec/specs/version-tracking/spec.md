## ADDED Requirements

### Requirement: State File Structure
The system SHALL store synchronization state in `.cache/readme-sync-state.json` with the following fields: `last_sync_hash` (SHA256 hex string), `last_sync_date` (ISO 8601 timestamp), `cached_readme` (full README.md text), and optionally `synced_to_commit` (git commit SHA).

#### Scenario: State file created on first sync
- **WHEN** the first synchronization runs successfully
- **THEN** the system SHALL create `.cache/readme-sync-state.json` with all required fields populated

#### Scenario: State file read on subsequent sync
- **WHEN** a subsequent synchronization runs
- **THEN** the system SHALL read `last_sync_hash` and `cached_readme` from the state file to compare with the current README.md

#### Scenario: State file updated after sync
- **WHEN** a synchronization completes successfully
- **THEN** the system SHALL update all fields in the state file to reflect the new baseline

### Requirement: Hash-Based Change Detection
The system SHALL compute and compare SHA256 hashes of README.md content to determine whether synchronization is needed.

#### Scenario: Hash match
- **WHEN** the computed SHA256 hash of the current README.md equals `last_sync_hash` in the state file
- **THEN** the system SHALL determine that no changes have occurred and skip the sync process

#### Scenario: Hash mismatch
- **WHEN** the computed SHA256 hash of the current README.md differs from `last_sync_hash` in the state file
- **THEN** the system SHALL determine that changes have occurred and proceed with the sync process

#### Scenario: Empty README
- **WHEN** README.md is empty or does not exist
- **THEN** the system SHALL report an error and abort without creating or updating the state file

### Requirement: Cached Content for Diff
The system SHALL store the full text of README.md in the state file to enable content diff computation without relying on git history.

#### Scenario: Diff computation
- **WHEN** the system detects a hash mismatch and needs to compute the diff
- **THEN** the system SHALL compare the current README.md text against the `cached_readme` field in the state file

#### Scenario: Cached content removed by user
- **WHEN** the state file exists but the `cached_readme` field is empty or missing
- **THEN** the system SHALL fall back to `git diff` for README.md if available, or treat as an initial sync if git is not available

### Requirement: Human-Readable Sync Marker
The system MAY update the `update` field in README.md's YAML Front Matter to reflect the synchronization time as a human-readable marker.

#### Scenario: Update field injection
- **WHEN** a synchronization completes and README.md contains YAML Front Matter with an `update` field
- **THEN** the system MAY update that field's value to the current date/time, and this update SHALL not trigger a recursive sync

#### Scenario: No Front Matter present
- **WHEN** README.md does not contain YAML Front Matter
- **THEN** the system SHALL skip the update field injection and proceed normally
