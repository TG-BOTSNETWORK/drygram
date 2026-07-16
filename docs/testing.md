# Testing Guide

This guide describes how to run unit, integration, stress, and performance tests locally in DryGram.

## Running Tests

Run pytest inside the repository root:

```bash
python -m pytest
```

## Adding Custom Tests

Create new modules under `tests/unit/` and verify changes against mock connection engines.
