mod data;

use data::{Video, WatchLater};
use rinput::rinput;

fn is_valid_link(link: &str) -> bool {
    link.starts_with("http:/") || link.starts_with("https:/")
}

fn create_video() -> Video {
    let link: String = loop {
        let input = rinput!("Enter your link: ");
        let input = input.trim();

        if is_valid_link(input) {
            break input.to_owned();
        }
    };

    let title: String = loop {
        let input = rinput!("Call your video: ");
        let input = input.trim();

        if input.is_empty() {
            println!("Please write a title");
        } else {
            break input.to_owned();
        }
    };

    let description = {
        let input = rinput!("Enter your description (optional): ");
        let input = input.trim();

        if input.is_empty() {
            None
        } else {
            Some(input.to_owned())
        }
    };

    Video {
        title,
        link,
        description,
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    clearscreen::clear()?;
    let vid = create_video();
    WatchLater::add_video(vid)?;
    let rand_vid = WatchLater::random_video()?;
    println!("{:?}", rand_vid);
    Ok(())
}
