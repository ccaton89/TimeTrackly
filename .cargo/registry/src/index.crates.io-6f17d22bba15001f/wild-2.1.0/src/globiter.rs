use crate::parser::CommandLineWParser;
use crate::parser::CharCode;
use std::ffi::OsString;
use std::fmt;

pub(crate) struct ArgOs {
    pub pattern: OsString,
    pub text: OsString,
    pub contains_glob: bool,
}

/// Iterator retuning glob-escaped arguments. Call `args()` to obtain it.
#[must_use]
pub(crate) struct GlobArgs<'argsline> {
    parser: CommandLineWParser<'argsline>,
}

impl<'a> fmt::Debug for GlobArgs<'a> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.parser.fmt(f)
    }
}

#[cfg(windows)]
use std::os::windows::ffi::OsStringExt;

/// This is used only in tests on non-Windows
#[cfg(not(windows))]
trait LossyOsStringExt {
    fn from_wide(wide: &[u16]) -> OsString {
        OsString::from(String::from_utf16_lossy(wide))
    }
}

#[cfg(not(windows))]
impl LossyOsStringExt for OsString {}

impl<'a> Iterator for GlobArgs<'a> {
    type Item = ArgOs;
    fn next(&mut self) -> Option<Self::Item> {
        let mut pattern = vec![];
        let mut text = vec![];
        let mut contains_glob = false;
        let has_arg = self.parser.accumulate_next(|c| {
            let (quoted, c) = match c {
                CharCode::Quoted(c) => (true, c),
                CharCode::Unquoted(c) => (false, c),
            };
            text.push(c);
            const Q: u16 = b'?' as u16;
            const A: u16 = b'*' as u16;
            const L: u16 = b'[' as u16;
            const R: u16 = b']' as u16;
            match c {
                Q | A | L | R => {
                    if quoted {
                        pattern.extend([
                            u16::from(b'['),
                            c,
                            u16::from(b']'),
                        ].iter().copied());
                    } else {
                        pattern.push(c);
                        contains_glob = true;
                    }
                },
                _ => pattern.push(c),
            };
        });
        if has_arg {
            Some(ArgOs {
                pattern: OsString::from_wide(&pattern),
                text: OsString::from_wide(&text),
                contains_glob,
            })
        } else {
            None
        }
    }
}

impl<'argsline> GlobArgs<'argsline> {
    /// UTF-16/UCS2 string from `GetCommandLineW`
    #[allow(dead_code)]
    pub(crate) fn new(command_line_args_ucs2: &'argsline [u16]) -> Self {
        Self {
            parser: CommandLineWParser::new(command_line_args_ucs2),
        }
    }
}
