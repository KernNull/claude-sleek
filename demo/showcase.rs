//! A tiny word counter, used to show off Rust colors.
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct Counter<'a> {
    words: HashMap<&'a str, usize>,
    limit: Option<usize>,
}

impl<'a> Counter<'a> {
    pub const MAX: usize = 1_000;

    pub fn new(limit: Option<usize>) -> Self {
        Self { words: HashMap::new(), limit }
    }

    pub fn add(&mut self, word: &'a str) -> Result<(), String> {
        let n = self.words.entry(word).or_insert(0);
        *n += 1;
        match self.limit {
            Some(max) if *n > max => Err(format!("too many {word:?}")),
            _ => Ok(()),
        }
    }
}

fn main() {
    let mut c = Counter::new(Some(3));
    for w in "a b a c a".split_whitespace() {
        if let Err(e) = c.add(w) {
            eprintln!("{e}");
        }
    }
    println!("{:#?}", c);
}
