<!--
SYNC IMPACT REPORT
Version change: (none) → 1.0.0
Modified principles: N/A (initial constitution)
Added sections: Core Principles (I–IV), No-Testing Policy, Development Workflow, Governance
Removed sections: N/A
Templates requiring updates:
  ⚠️ .specify/templates/plan-template.md — remove Testing field, remove tests/ directory from structure
  ⚠️ .specify/templates/spec-template.md — rename "User Scenarios & Testing" to "User Scenarios"
  ⚠️ .specify/templates/tasks-template.md — remove all test task examples and test phase sections
Follow-up TODOs: None
-->

# Testcase Constitution

## Core Principles

### I. Clarity Over Cleverness

Names MUST communicate intent. Functions, variables, and modules MUST be named to reveal purpose without
requiring comments. Abbreviations are FORBIDDEN unless universally understood (e.g., `id`, `url`).
If a name requires explanation, rename it.

### II. Single Responsibility

Every function, class, and module MUST do exactly one thing. A unit of code that can be described with
"and" violates this principle. Extract when in doubt; merge only when the two responsibilities are truly
inseparable.

### III. Simplicity (YAGNI)

Code MUST only solve the current, stated problem. Abstractions and extensibility hooks are FORBIDDEN
unless the second use case already exists. Complexity MUST be justified by present need — never by
anticipated future need.

### IV. No Dead Code

Unused functions, variables, imports, and commented-out code MUST be deleted immediately.
Version control is the history — the codebase MUST contain only live, working code.

## No-Testing Policy

Automated tests of any kind are FORBIDDEN in this project. This includes:

- Unit tests
- Integration tests
- End-to-end (e2e) tests
- Contract tests
- Any other automated test suites

Correctness is validated through code review and manual verification only.

## Development Workflow

All code changes MUST pass review before merge. Reviewers MUST verify compliance with each Core Principle.
Complexity violations MUST be justified in the PR description before approval is granted.

## Governance

This constitution supersedes all other development guidelines. Amendments require a documented rationale,
team consensus, and an updated version number. Principles are non-negotiable without a constitutional
amendment. All PRs and code reviews MUST verify compliance.

**Version**: 1.0.0 | **Ratified**: 2026-04-20 | **Last Amended**: 2026-04-20
