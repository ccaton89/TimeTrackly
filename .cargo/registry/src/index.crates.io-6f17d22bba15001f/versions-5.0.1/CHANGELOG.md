# `versions` Changelog

## 5.0.1 (2023-08-13)

#### Changed

- Bumped `itertools` dependency.

## 5.0.0 (2023-05-09)

This introduces a very small, technically breaking change to the API involving a
single type. If you're just doing basic parsing and comparisons and not actually
inspecting the types themselves, you shouldn't notice a difference.

#### Changed

- Versions with `~` in their metadata will now parse as a `Mess`. Example: `12.0.0-3ubuntu1~20.04.5`

## 4.1.0 (2022-04-21)

#### Added

- `FromStr` and `TryFrom` instances for each type.

## 4.0.0 (2022-01-07)

#### Added

- The `Release` type.

#### Changed

- `SemVer` and `Version` have had their prerel field changed to `Release`.
- The `Chunk` type has changed from a struct to an enum.

#### Removed

- The `Unit` type.

#### Fixed

- A bug involving zeroes in `SemVer` prereleases.
- A bug involving the `Display` instance for `Version`.

## 3.0.3 (2021-08-23)

#### Changed

- Upgraded to `nom-7.0`.

## 3.0.2 (2021-05-27)

#### Added

- A proper LICENSE file.

#### Changed

- The `Hash` instance of `SemVer` is now hand-written to uphold the Law that:

```
k1 == k2 -> hash(k1) == hash(k2)
```

## 3.0.1 (2021-05-09)

#### Changed

- Certain parsers are now faster and use less memory.

## 3.0.0 (2021-04-16)

This release brings `versions` in line with version `2.0.0` of the SemVer spec.
The main addition to the spec is the allowance of hyphens in both the prerelease
and metadata sections. As such, **certain versions like 1.2.3+1-1 which
previously would not parse as SemVer now do.**

To accomodate this and other small spec updates, the `SemVer` and `Version`
types have received breaking changes here.

#### Added

- [`Serde`](https://serde.rs/) support through the optional `serde` feature.
- `Versioning::nth` to pick out certain fields of a generically parsed version.
- `Default` is now derived on `Versioning`, `SemVer`, `Version`, `Mess` and
  `Chunks` so that it's possible to initialize as a struct's field.

#### Changed

- **Breaking:** `SemVer::meta` and `Version::meta` no longer parse as `Chunks`
  but as vanilla `String`s.
- **Breaking:** As a semantic change, `Version`s now expect metadata to come
  **after** any prerelease, just as with `SemVer`. `Version` is now thus fairly
  similar to `SemVer`, except that is allows letters in more permissive
  positions.

#### Fixed

- Two small bugs involving `SemVer`/`Version` comparisons.

## 2.1.0 (2021-03-22)

#### Added

- `SemVer::parse`, `Version::parse`, and `Mess::parse` have been made `pub` so
  that these parsers can be integrated into other general `nom` parsers.

## 2.0.2 (2021-01-23)

#### Changed

- Updated to `itertools-0.10`.

## 2.0.1 (2020-11-19)

#### Changed

- Updated to `nom-6.0`.
- Utilize new type linking in docstrings, thanks to the latest stable Rust.

## 2.0.0 (2020-10-21)

#### Changed

- **Breaking:** `Mess::chunk` renamed to `Mess::chunks` to match `Version`.
- **Breaking:** `Mess` now stores smarter `Vec<MChunk>` instead of `String`s.
- `SemVer::to_version` is no longer a lossy conversion, due to the new field in `Version` (see below).
- Most `Display` instances are more efficient.

#### Added

- **Breaking:** The `meta: Option<Chunks>` field for `Version`.
- The `MChunk` type which allows `Mess` to do smarter comparisons.

#### Fixed

- A number of comparison edge cases.

## 1.0.1 (2020-06-15)

#### Changed

- Performance and readability improvements.

## 1.0.0 (2020-06-03)

This is the initial release of the library.

#### Added

- All types, parsers, and tests.
