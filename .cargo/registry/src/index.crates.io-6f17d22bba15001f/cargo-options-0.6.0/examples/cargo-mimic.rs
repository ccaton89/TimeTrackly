use cargo_options::{Build, Check, Clippy, Install, Metadata, Run, Rustc, Test};
use clap::Parser;

#[derive(Debug, Parser)]
#[command(name = "cargo-mimic", display_order = 1)]
enum Opt {
    #[command(name = "build", aliases = &["b"] )]
    Build(Build),
    #[command(name = "clippy")]
    Clippy(Clippy),
    #[command(name = "check", aliases = &["c"])]
    Check(Check),
    #[command(name = "install")]
    Install(Install),
    #[command(name = "metadata")]
    Metadata(Metadata),
    #[command(name = "rustc")]
    Rustc(Rustc),
    #[command(name = "run", alias = "r")]
    Run(Run),
    #[command(name = "test", alias = "t")]
    Test(Test),
}

fn main() {
    let _opt = Opt::parse();
}
