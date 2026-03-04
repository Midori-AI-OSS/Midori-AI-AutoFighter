# Quick Linting Reference

This is a quick reference for developers working with linting in the Stained Glass Odyssey: Endless repository.

## Essential Commands

### Before Every Commit (Backend)
```bash
cd backend
ruff check . --fix
```
**Expected result**: `All checks passed!`

### Check Entire Repository
```bash
ruff check .
```

### Check Specific Directory
```bash
ruff check backend    # Backend code
ruff check legacy     # Legacy code  
```

### Auto-fix Issues
```bash
ruff check . --fix
```

## Quick Troubleshooting

### ❌ Import Issues
```python
# Problem: Unused import
import os
import sys  # ← Not used

# Solution: Remove or use the import
import os
```

### ❌ Whitespace Issues
```python
# Problem: Trailing whitespace or blank lines with spaces
def my_function():    
    pass    

# Solution: Clean whitespace (auto-fixed with --fix)
def my_function():
    pass
```

### ❌ Import Sorting
```python
# Problem: Wrong import order
import sys
import os
from typing import List

# Solution: Proper order (auto-fixed with --fix)  
import os
import sys

from typing import List
```

## Common Workflow

1. **Make code changes**
2. **Run linting**: `ruff check . --fix`
3. **Fix any remaining issues manually**
4. **Verify**: `ruff check .` should show "All checks passed!"
5. **Commit changes**

## CI Integration

The CI workflow automatically runs:
- `uvx ruff check backend` 
- `uvx ruff check legacy`

Pull requests are blocked if linting fails.

## Get Help

- 📖 Full documentation: `.agents/implementation/linting-standards.md`
- ⚙️ Configuration: `ruff.toml`
- 🐛 Rule reference: https://docs.astral.sh/ruff/rules/

## Editor Setup

Install the Ruff extension in your editor for real-time linting and auto-fixes on save.