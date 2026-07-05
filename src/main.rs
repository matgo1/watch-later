use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

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
        // Create a dir if not exist
        if !Path::new("data").is_dir() {
            fs::create_dir("data")?;
        }

        // Create a file if not exist
        if !Path::new(FILE_PATH).exists() {
            fs::File::create(FILE_PATH)?;
        }

        let data = fs::read_to_string(FILE_PATH)?;
        if data.trim().is_empty() {
            return Ok(JsonData { videos: Vec::new() });
        }
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
