use serde::{Deserialize, Serialize};

const FILE_PATH: &str = "data/videos.json";

// Template for json item
#[derive(serde::Serialize, Deserialize)]
pub struct Video {
    title: String,
    link: String,
    description: Option<String>,
}

// Template of json file
#[derive(Serialize, Deserialize)]
pub struct JsonData {
    videos: Vec<Video>,
}

// Class WatchLater
pub struct WatchLater;

impl WatchLater {
    // Functionality:
    // 1. add links to json
    // 2. write random link from json
    // 3. Optional! check if is valid link
    // 4. Load json

    pub fn load() -> Result<JsonData, Box<dyn std::error::Error>> {
        let data = std::fs::read_to_string(FILE_PATH)?;
        Ok(serde_json::from_str(&data)?)
    }

    pub fn check() {
        println!("OK");
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    clearscreen::clear()?;
    WatchLater::load()?;
    WatchLater::check();
    Ok(())
}
