use std::collections::BTreeMap;
use std::fmt;
use std::sync::{Arc, Mutex};

use crate::value::{Object, ObjectKind, StructObject, Value};

/// Utility to enclose values for macros.
///
/// See `closure` on the [`Frame`] for how it's used.
#[derive(Debug, Default)]
pub(crate) struct Closure {
    values: Mutex<BTreeMap<Arc<str>, Value>>,
}

impl Closure {
    /// Stores a value by key in the closure.
    pub fn store(&self, key: &str, value: Value) {
        self.values.lock().unwrap().insert(Arc::from(key), value);
    }

    /// Upset a value into the closure.
    #[cfg(feature = "macros")]
    pub fn store_if_missing<F: FnOnce() -> Value>(&self, key: &str, f: F) {
        let mut values = self.values.lock().unwrap();
        if !values.contains_key(key) {
            values.insert(Arc::from(key), f());
        }
    }
}

impl fmt::Display for Closure {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut m = f.debug_map();
        for (key, value) in self.values.lock().unwrap().iter() {
            m.entry(&key, &value);
        }
        m.finish()
    }
}

impl Object for Closure {
    fn kind(&self) -> ObjectKind<'_> {
        ObjectKind::Struct(self)
    }
}

impl StructObject for Closure {
    fn fields(&self) -> Vec<Arc<str>> {
        self.values.lock().unwrap().keys().cloned().collect()
    }

    fn get_field(&self, name: &str) -> Option<Value> {
        self.values.lock().unwrap().get(name).cloned()
    }
}
