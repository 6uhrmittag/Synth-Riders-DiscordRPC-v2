# GitHub Actions CI/CD Workflows

This directory contains GitHub Actions workflows for automated testing, building, and releasing the Synth Riders Discord RPC tool.

## Workflow Overview

### 1. Test Workflow (`test.yml`)
**Purpose**: Fast feedback on code changes
**Triggers**: 
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger

**Features**:
- Multi-Python version testing (3.9, 3.10, 3.11)
- Smoke test execution
- Unit test coverage reporting
- Codecov integration

### 2. Build Workflow (`build.yml`)
**Purpose**: Create executables and releases
**Triggers**:
- Push to `main` branch only
- Manual trigger

**Features**:
- Windows executable build
- Linux executable build
- Automatic GitHub release creation
- Build artifact upload

### 3. Complete CI Workflow (`ci.yml`)
**Purpose**: Full pipeline (testing + building)
**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger

**Features**:
- Testing and building in one workflow
- Cross-platform builds
- Release creation

## Workflow Details

### Test Workflow
```yaml
name: Test
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
```

**Steps**:
1. **Checkout**: Get the latest code
2. **Setup Python**: Install specified Python version
3. **Cache Dependencies**: Speed up builds with caching
4. **Install Dependencies**: Install requirements and test tools
5. **Run Smoke Tests**: Execute comprehensive smoke tests
6. **Run Unit Tests**: Execute pytest with coverage
7. **Upload Coverage**: Send coverage data to Codecov

### Build Workflow
```yaml
name: Build
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
  build-linux:
    runs-on: ubuntu-latest
  release:
    runs-on: ubuntu-latest
    needs: [build-windows, build-linux]
```

**Steps**:
1. **Checkout**: Get the latest code
2. **Setup Python**: Install Python 3.11
3. **Cache Dependencies**: Speed up builds
4. **Install Dependencies**: Install PyInstaller and requirements
5. **Build Application**: Create executable with PyInstaller
6. **Verify Build**: Check build output integrity
7. **Upload Artifacts**: Store build artifacts
8. **Create Release**: Generate GitHub release (main branch only)

## Build Process

### PyInstaller Configuration
The build process uses `main.spec` for PyInstaller configuration:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/*', 'assets'), ('settings/*', 'settings'), ('utils/*', 'utils')],
    hiddenimports=['utils.synth_db'],
    # ... other settings
)
```

### Build Verification
Each build job verifies:
- ✅ Executable file exists (`main.exe` on Windows, `main` on Linux)
- ✅ Settings directory copied to build output
- ✅ Version information available in `appinfo.ini`

### Release Process
When pushing to `main` branch:
1. Build Windows and Linux executables
2. Extract version from `settings/appinfo.ini`
3. Create GitHub release with tag `v{version}`
4. Upload executables as release assets

## Configuration

### Required Secrets
- `GITHUB_TOKEN`: Automatically provided by GitHub
- `CODECOV_TOKEN`: Optional, for Codecov integration

### Environment Variables
- `PYTHON_VERSION`: Set to '3.11' for builds
- `PYTHON_VERSIONS`: Array for test matrix

## Usage

### For Developers
1. **Push to develop**: Triggers test workflow only
2. **Create PR**: Triggers test workflow for validation
3. **Merge to main**: Triggers full CI pipeline (test + build + release)

### For Maintainers
1. **Manual Build**: Use "workflow_dispatch" trigger
2. **Release Management**: Automatic releases on main branch pushes
3. **Artifact Access**: Download from Actions tab or Releases page

## Monitoring

### Workflow Status
- **Green**: All tests pass, builds successful
- **Yellow**: Tests pass, build in progress
- **Red**: Tests fail or build failed

### Artifacts
- **Test Artifacts**: Coverage reports, test logs
- **Build Artifacts**: Windows/Linux executables
- **Release Assets**: Tagged releases with executables

### Notifications
- **Pull Requests**: Status checks for test workflow
- **Main Branch**: Full pipeline execution
- **Releases**: Automatic GitHub release creation

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check PyInstaller configuration
   - Verify all dependencies in `requirements.txt`
   - Check file paths in `main.spec`

2. **Test Failures**
   - Run tests locally: `python tests/run_smoke_tests.py`
   - Check test data in `tests/testdata/`
   - Verify Python version compatibility

3. **Release Failures**
   - Ensure version in `settings/appinfo.ini` is valid
   - Check GitHub token permissions
   - Verify release tag doesn't already exist

### Debugging
- **Local Testing**: Use `build.bat` for Windows builds
- **Logs**: Check Actions tab for detailed logs
- **Artifacts**: Download build artifacts for inspection

## Performance

### Optimization
- **Caching**: Dependencies cached between runs
- **Parallel Jobs**: Windows and Linux builds run in parallel
- **Matrix Testing**: Multiple Python versions tested simultaneously

### Timing
- **Test Workflow**: ~2-3 minutes per Python version
- **Build Workflow**: ~5-8 minutes total
- **Full CI**: ~10-15 minutes total

## Security

### Best Practices
- ✅ No secrets in workflow files
- ✅ Minimal permissions for GitHub token
- ✅ Secure dependency installation
- ✅ Verified build artifacts

### Dependencies
- ✅ Pinned versions in `requirements.txt`
- ✅ Trusted GitHub Actions
- ✅ Regular dependency updates

## Future Enhancements

### Planned Features
1. **macOS Builds**: Add macOS executable generation
2. **Docker Support**: Containerized builds
3. **Performance Tests**: Add load testing
4. **Security Scanning**: Add vulnerability scanning
5. **Automated Updates**: Auto-update dependencies

### Monitoring
1. **Metrics**: Build time tracking
2. **Alerts**: Failure notifications
3. **Analytics**: Test coverage trends
4. **Reporting**: Monthly build reports 