use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

const FILE_PATH: &str = "data/videos.json";

// Template for json item
#[derive(serde::Serialize, Deserialize, Debug)]
pub struct Video {
    title: String,
    link: String,
    description: Option<String>,
}

// Template of json file
#[derive(Serialize, Deserialize, Debug)]
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

    fn load() -> Result<JsonData, Box<dyn std::error::Error>> {
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

    pub fn save(data: &JsonData) -> Result<(), Box<dyn std::error::Error>> {
        let json = serde_json::to_string_pretty(data)?;
        fs::write(FILE_PATH, json)?;
        Ok(())
    }

    pub fn add_video(video: Video) -> Result<(), Box<dyn std::error::Error>> {
        let mut data: JsonData = Self::load()?;
        data.videos.push(video);
        Self::save(&data)?;
        Ok(())
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    clearscreen::clear()?;

    let testing: Video = Video {
        title: "test".to_string(),
        link: "https://testing.com".to_string(),
        description: Some(String::from("Jopa")),
    };

    WatchLater::add_video(testing);
    Ok(())
}
