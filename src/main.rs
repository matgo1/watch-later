mod data;

use data::{Video, WatchLater};
use std::io;

pub fn read_line(text: Option<&str>) -> io::Result<String> {
    if let Some(t) = text {
        println!("{}", t);
    }
    let mut input = String::new();
    io::stdin().read_line(&mut input)?;
    Ok(input.trim().to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    clearscreen::clear()?;
    // Test example
    let vid = Video {
        title: "Jopa".to_string(),
        link: "Jopa".to_string(),
        description: None,
    };
    WatchLater::add_video(vid)?;
    Ok(())
}
