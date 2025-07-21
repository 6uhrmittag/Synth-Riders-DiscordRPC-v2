# Status Badges

Add these badges to your main `readme.md` file to show the status of your CI/CD pipelines:

## Test Status
```markdown
![Tests](https://github.com/{username}/{repo}/workflows/Test/badge.svg)
```

## Build Status
```markdown
![Build](https://github.com/{username}/{repo}/workflows/Build/badge.svg)
```

## Complete CI Status
```markdown
![CI](https://github.com/{username}/{repo}/workflows/CI%20-%20Build%20and%20Test/badge.svg)
```

## Code Coverage
```markdown
![Codecov](https://codecov.io/gh/{username}/{repo}/branch/main/graph/badge.svg)
```

## Python Version
```markdown
![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)
```

## License
```markdown
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

## Example Usage
Replace `{username}` and `{repo}` with your actual GitHub username and repository name:

```markdown
# Synth Riders Discord RPC

[![Tests](https://github.com/6uhrmittag/Synth-Riders-DiscordRPCv2/workflows/Test/badge.svg)](https://github.com/6uhrmittag/Synth-Riders-DiscordRPCv2/actions?query=workflow%3ATest)
[![Build](https://github.com/6uhrmittag/Synth-Riders-DiscordRPCv2/workflows/Build/badge.svg)](https://github.com/6uhrmittag/Synth-Riders-DiscordRPCv2/actions?query=workflow%3ABuild)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Discord Rich Presence integration for Synth Riders VR rhythm game.
```

## Badge URLs

### Test Workflow
- **Status**: `https://github.com/{username}/{repo}/workflows/Test/badge.svg`
- **Link**: `https://github.com/{username}/{repo}/actions?query=workflow%3ATest`

### Build Workflow
- **Status**: `https://github.com/{username}/{repo}/workflows/Build/badge.svg`
- **Link**: `https://github.com/{username}/{repo}/actions?query=workflow%3ABuild`

### Complete CI Workflow
- **Status**: `https://github.com/{username}/{repo}/workflows/CI%20-%20Build%20and%20Test/badge.svg`
- **Link**: `https://github.com/{username}/{repo}/actions?query=workflow%3A%22CI+-+Build+and+Test%22`

### Codecov Coverage
- **Status**: `https://codecov.io/gh/{username}/{repo}/branch/main/graph/badge.svg`
- **Link**: `https://codecov.io/gh/{username}/{repo}`

## Customization

### Branch-specific badges
For specific branches, replace `main` with your branch name:
```markdown
![Tests](https://github.com/{username}/{repo}/workflows/Test/badge.svg?branch=develop)
```

### Event-specific badges
For specific events (push, pull_request):
```markdown
![Tests](https://github.com/{username}/{repo}/workflows/Test/badge.svg?event=push)
```

### Custom colors
You can customize badge colors using shields.io:
```markdown
![Tests](https://img.shields.io/github/workflow/status/{username}/{repo}/Test?color=green&label=tests)
``` 