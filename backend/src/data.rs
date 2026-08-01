use rand::seq::IndexedRandom;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

const FILE_PATH: &str = "data/videos.json";

// Template for json item
#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub struct Video {
    pub title: String,
    pub link: String,
}

// Template of json file
#[derive(Serialize, Deserialize, Debug)]
pub struct JsonData {
    videos: Vec<Video>,
}

// Class WatchLater
pub struct WatchLater;

impl WatchLater {
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

    fn save(data: &JsonData) -> Result<(), Box<dyn std::error::Error>> {
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

    pub fn get_random_video() -> Result<Video, Box<dyn std::error::Error>> {
        let data: JsonData = Self::load()?;
        match data.videos.choose(&mut rand::rng()) {
            Some(i) => Ok(i.clone()),
            None => Ok(Video::default()),
        }
    }

    pub fn remove_video(input_link: String) -> Result<(), Box<dyn std::error::Error>> {
        let mut data: JsonData = Self::load()?;
        if let Some(index) = data.videos.iter().position(|v| v.link == input_link) {
            data.videos.remove(index);
        }

        Self::save(&data)?;

        Ok(())
    }
}
