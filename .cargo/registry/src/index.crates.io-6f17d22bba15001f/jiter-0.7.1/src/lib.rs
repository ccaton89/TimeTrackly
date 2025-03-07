#![doc = include_str!("../README.md")]

mod errors;
mod jiter;
mod lazy_index_map;
mod number_decoder;
mod parse;
#[cfg(feature = "python")]
mod py_lossless_float;
#[cfg(feature = "python")]
mod py_string_cache;
#[cfg(feature = "python")]
mod python;
#[cfg(target_arch = "aarch64")]
mod simd_aarch64;
mod string_decoder;
mod value;

pub use errors::{JiterError, JiterErrorType, JsonError, JsonErrorType, JsonResult, JsonType, LinePosition};
pub use jiter::{Jiter, JiterResult};
pub use lazy_index_map::LazyIndexMap;
pub use number_decoder::{NumberAny, NumberInt};
pub use parse::Peek;
pub use value::{JsonArray, JsonObject, JsonValue};

#[cfg(feature = "python")]
pub use py_lossless_float::{FloatMode, LosslessFloat};
#[cfg(feature = "python")]
pub use py_string_cache::{cache_clear, cache_usage, cached_py_string, pystring_fast_new, StringCacheMode};
#[cfg(feature = "python")]
pub use python::{map_json_error, PythonParse};

#[derive(Debug, Clone, Copy)]
pub enum PartialMode {
    Off,
    On,
    TrailingStrings,
}

impl Default for PartialMode {
    fn default() -> Self {
        Self::Off
    }
}

impl From<bool> for PartialMode {
    fn from(mode: bool) -> Self {
        if mode {
            Self::On
        } else {
            Self::Off
        }
    }
}

impl PartialMode {
    pub fn is_active(self) -> bool {
        !matches!(self, Self::Off)
    }

    pub fn allow_trailing_str(self) -> bool {
        matches!(self, Self::TrailingStrings)
    }
}
