## 0.3.6

* Fix Readme display

## 0.3.5

* Make string serialization look more like poetry's
* Implement `__hash__` for `VersionSpecifier`

## 0.3.4

* Python bindings for `VersionSpecifiers`

## 0.3.3

* Implement `Display` for `VersionSpecifiers`

## 0.3.2

* Expose `VersionSpecifier().operator` and `VersionSpecifier().version` to Python

## 0.3.1

* Expose `Version` from `PyVersion`

## 0.3.0

* Introduced a `PyVersion` wrapper specifically for the Python bindings to work around https://github.com/PyO3/pyo3/pull/2786
* Added `VersionSpecifiers::contains`
* Added `Version::from_release`, a constructor for a version that is just a release such as `3.8`.

## 0.2.0

* Added `VersionSpecifiers`, a thin wrapper around `Vec<VersionSpecifier>` with a serde implementation. `VersionSpecifiers::from_str` is now preferred over `parse_version_specifiers`.
* Reexport rust function for python module