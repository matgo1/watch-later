mod data;

use axum::{
    Json, Router,
    http::StatusCode,
    routing::{get, post},
};
use data::{Video, WatchLater};

fn is_valid_link(link: &str) -> bool {
    link.starts_with("http://") || link.starts_with("https://")
}

async fn get_random_handler() -> Result<Json<Video>, StatusCode> {
    match WatchLater::get_random_video() {
        Ok(video) => Ok(Json(video)),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

async fn add_video_handler(Json(payload): Json<Video>) -> Result<StatusCode, StatusCode> {
    // Vadlidate link and title
    if !is_valid_link(&payload.link) || payload.title.trim().is_empty() {
        return Err(StatusCode::BAD_REQUEST);
    }

    match WatchLater::add_video(payload) {
        Ok(_) => Ok(StatusCode::CREATED),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

async fn remove_video_handler(Json(link): Json<String>) -> Result<StatusCode, StatusCode> {
    match WatchLater::remove_video(link) {
        Ok(_) => Ok(StatusCode::NO_CONTENT),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Build the router
    let app = Router::new()
        .route("/random", get(get_random_handler))
        .route("/add", post(add_video_handler))
        .route("/remove", post(remove_video_handler));

    // Bind on port 3000
    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await?;
    println!("WatchLater API Backend running on http://127.0.0.1:3000");

    axum::serve(listener, app).await?;
    Ok(())
}
