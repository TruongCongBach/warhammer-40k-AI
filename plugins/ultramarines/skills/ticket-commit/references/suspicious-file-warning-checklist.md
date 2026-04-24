# Suspicious File Warning Checklist

## Purpose

Use this checklist for files that often slip into commits accidentally.

## High-Caution Files

- `.idea/`, `.vscode/`, editor or workspace files
- `dist/`, `build/`, generated output
- lockfiles: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Podfile.lock`
- package manifests when dependency changes were not expected
- screenshots, temp files, logs, archives
- global config files
- unrelated docs or README changes
- snapshot files with broad churn

## Review Questions

- Was this file change necessary for the issue?
- Was it intentionally changed?
- Would another engineer expect this file to move with the issue?
- Is the file generated rather than authored?
- Can the issue be committed cleanly without it?

## Rule

If the answer is not clearly favorable, keep the file out of the commit and place it in `needs review`.
