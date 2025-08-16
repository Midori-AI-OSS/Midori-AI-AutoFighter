# Add save management settings (`1001dff7`)

## Summary
Expose settings to end the current run, wipe all save data, and backup or restore saves with encryption and hash verification.

## Tasks
- [x] Provide UI and backend support for an "End Run" button that gracefully terminates the active run.
- [x] Add "Wipe Save Data" option that clears player and run records after confirmation.
- [x] Implement encrypted backup export: hash the plaintext save, embed the hash, then encrypt the package for download.
- [x] Implement import path that decrypts the backup, verifies the embedded hash, and rejects modified files.
- [x] Document backup/restore workflow and update tests covering integrity checks.

## Context
Current settings lack controls for managing runs or safeguarding progress. Secure backups protect against tampering and allow users to restore their data.

## Notes
Use the encrypted save system plan as a reference for key handling and storage.
