# Linting Standards and Guidelines

This document outlines the linting standards for the Stained Glass Odyssey: Endless repository to ensure code quality and consistency.

## Overview

We use `ruff` for Python linting with a progressive configuration that starts with essential rules and can be expanded over time. The current configuration focuses on:
- Critical syntax and runtime errors
- Import organization  
- Basic code formatting
- Essential whitespace issues

## Current Configuration Status

### ✅ Active Rules (All Code)
- **F**: Pyflakes errors (unused imports, undefined variables)
- **E4/E7/E9**: Critical pycodestyle errors (syntax, statements, runtime)
- **W291/W292/W293**: Whitespace issues
- **I001**: Import sorting

### 🔄 Progressive Enhancement
The configuration is designed for gradual improvement. Future enhancements may include:
- Naming conventions (N series)
- Modern Python syntax (UP series) 
- Code complexity rules (B, C4 series)
- Advanced style rules (SIM, RET series)

## Directory-Specific Rules

### Backend (`backend/`)
- **Comprehensive rules**: Full linting suite for new/actively maintained code
- **Strict enforcement**: All pull requests must pass linting

### Legacy (`legacy/`)
- **Relaxed rules**: Focus on critical errors only
- **Gradual improvement**: Can be enhanced over time without blocking development

### Tests (`**/tests/**`, `**/test_*.py`)
- **Flexible naming**: Relaxed variable naming conventions
- **Test-specific patterns**: Accommodates testing patterns and fixtures

## Pre-Commit Requirements

### Backend Development
**MANDATORY**: Run linting before every commit:

```bash
cd backend
ruff check . --fix
```

Expected result: `All checks passed!`

### Legacy Code
For legacy modifications:

```bash
ruff check legacy --fix
```

Legacy code should pass basic linting but extensive refactoring is not required.

### Full Repository Check
To check the entire repository:

```bash
ruff check . --fix
```

## Integration with CI/CD

The GitHub Actions CI workflow includes dedicated linting jobs:
- **Backend linting**: `uvx ruff check backend` 
- **Legacy linting**: `uvx ruff check legacy`
- **Pull requests are blocked** if linting fails

## Common Linting Issues and Solutions

### 1. Unused Imports (F401)
**Problem**: Import statements for modules not used in the file
**Solution**: Remove unused imports automatically with `--fix`

```python
# ❌ Before
import os
import sys  # Unused
import json

# ✅ After  
import os
import json
```

### 2. Undefined Variables (F821)
**Problem**: Using variables that haven't been defined
**Solution**: Define the variable or fix the typo

### 3. Import Sorting (I001)
**Problem**: Imports not sorted according to conventions
**Solution**: Use `--fix` to automatically sort imports

```python
# ❌ Before
import sys
import os
from typing import List

# ✅ After
import os
import sys

from typing import List
```

### 4. Whitespace Issues (W291, W292, W293)
**Problem**: Trailing whitespace, missing newlines, whitespace in blank lines
**Solution**: Automatically fixed with `--fix`

## Import Organization Standards

Following the repository's Python style guide:

```python
# Standard library imports (sorted shortest to longest)
import os
import sys
import json
import logging

# Third-party imports (sorted shortest to longest)
import pytest
import asyncio

from fastapi import FastAPI
from rich.console import Console

# Project imports (sorted shortest to longest)  
from autofighter.core import Player
from autofighter.effects import EffectManager
```

## Editor Integration

### VS Code
Install the Ruff extension and add to `settings.json`:

```json
{
    "python.linting.enabled": true,
    "ruff.enable": true,
    "ruff.organizeImports": true,
    "editor.formatOnSave": true,
    "ruff.lint.run": "onSave"
}
```

### Other Editors
Most editors have Ruff plugins available. Configure them to:
- Run linting on save
- Auto-fix issues where possible
- Organize imports automatically

## Gradual Improvement Strategy

### Phase 1 (Current): Essential Rules ✅
- Critical errors and syntax issues
- Import organization
- Basic whitespace cleanup

### Phase 2 (Future): Code Quality
- Naming conventions
- Modern Python syntax
- Basic complexity rules

### Phase 3 (Future): Advanced Standards
- Comprehensive style enforcement
- Performance optimizations
- Advanced pattern detection

## Troubleshooting

### Linting Failures in CI
1. Run `ruff check . --fix` locally
2. Commit the automatically fixed issues
3. Address any remaining manual issues
4. Verify with `ruff check .` before pushing

### Configuration Issues
If you encounter issues with the linting configuration:
1. Check `ruff.toml` syntax
2. Test with `ruff check --config ruff.toml .`
3. Review per-file ignores for specific directories

### Performance Considerations
- Linting is fast and should not impact development workflow significantly
- Use `--statistics` to understand rule frequency
- Current configuration focuses on essential rules for good performance

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rule Reference](https://docs.astral.sh/ruff/rules/)
- [Python Import Conventions (PEP 8)](https://pep8.org/#imports)
- [Repository configuration](../../ruff.toml)