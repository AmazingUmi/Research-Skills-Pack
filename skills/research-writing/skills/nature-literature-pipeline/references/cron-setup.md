# Scheduled literature delivery: verification and recovery

This synthetic example shows how to verify a one-shot or recurring literature-delivery job and recover when a scheduled run does not appear. All identifiers, dates, targets, and paths below are placeholders.

## Scenario

A user reports that a scheduled literature digest was not delivered at the expected time.

Example job configuration:

- job ID: `<JOB_ID>`
- name: `literature-digest`
- schedule: `<SCHEDULE>`
- delivery target: `<DELIVERY_TARGET>`

## Verification sequence

1. List scheduled jobs and confirm that `<JOB_ID>` exists in the current profile.
2. Inspect the job's schedule, repeat policy, delivery target, and enabled state.
3. Run retrieval and formatting in a local dry run with delivery disabled.
4. Verify delivery independently from archival.
5. Confirm that the archive contains the expected note and deduplication marker.

A successful create response is not sufficient: always read the stored job back from the scheduler.

## Recovery path

1. Match existing jobs in the same profile by ID and by schedule, target, and research profile. Update or re-enable the matching job and verify its stored configuration.
2. Create a replacement only if the matching job is absent. If the scheduler cannot update a broken job, disable it before activating the replacement. Record the active ID.
3. Dry-run retrieval and formatting locally. Check the delivery receipt and archive marker for the date, target and profile. Retry only the missing stage; confirm the actual delivery state before repeating a send. Send a separate live test only on request.
4. Write missing archive entries under `{ARCHIVE_ROOT}/raw/literature/`, deduplicated by paper ID.

Example retrieval themes:

- `topic keyword method`
- `material property application`
- `author institution research question`

Example result set:

1. Study A — monitoring method for a representative system.
2. Study B — processing route and performance evaluation.
3. Study C — continuous purification or separation method.
4. Study D — electrochemical characterization workflow.
5. Study E — modeling study for a generic alloy system.

## Placeholder delivery record

- target: `<DELIVERY_TARGET>`
- chat ID: `<CHAT_ID>`
- message ID: `<MESSAGE_ID>`

Never publish real chat IDs, message IDs, group names, scheduler IDs, or delivery logs in an example.

## Placeholder archive layout

```text
{ARCHIVE_ROOT}/raw/literature/
├── core/
│   ├── study-a.md
│   └── study-b.md
├── supporting/
│   └── study-c.md
└── references.ris
```

Use project-relative placeholders in public documentation. Keep machine-specific home, mount, vault, and organization paths in private configuration.

## Operational lessons

- Verify every created job by listing it from the same profile and runtime.
- Test retrieval, delivery, and archival as separate stages.
- For time-sensitive digests, restore delivery first and investigate the scheduler second.
- Recurring jobs need a manual-run check, delivery check, archive check, deduplication check, and failure alert.
- Document troubleshooting as a synthetic scenario rather than publishing a real incident transcript.
