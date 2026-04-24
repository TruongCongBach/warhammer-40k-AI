# File Relevance Review Checklist

## Purpose

Use this checklist to decide whether a changed file truly belongs to the current Jira issue.

## Questions

- Does the file map to the screen, route, component, hook, service, or config area affected by the issue?
- Does the diff content support the described fix or feature?
- Is the file part of a necessary dependency chain for this issue?
- Is the file a direct follow-on from the approved implementation or review corrections?
- Would excluding this file make the issue implementation incomplete or broken?
- Is the file likely from another unfinished task?
- Is the file only touched because of formatting, local tooling, or unrelated cleanup?

## Include When

- the file directly supports the issue behavior
- the file is required for correctness of the scoped change
- the file is a justified dependency of the change

## Exclude Or Review When

- the connection to the issue is weak
- the diff looks like general cleanup
- the file belongs to another feature, bug, or experiment
- the file could be a local artifact
