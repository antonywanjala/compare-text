import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class RemoteImage:
    """Represents an image hosted on a remote server/gallery."""
    image_id: str
    url: str
    alt_text: str


class RemoteGallery:
    """Simulates a remote API or database storing image metadata."""

    def __init__(self):
        self.images: Dict[str, RemoteImage] = {}

    def add_image(self, image_id: str, url: str, alt_text: str):
        self.images[image_id] = RemoteImage(image_id, url, alt_text)

    def get_image(self, image_id: str) -> RemoteImage:
        return self.images.get(image_id)


@dataclass
class Post:
    """Represents a timeline post that can contain injected image tags."""
    post_id: int
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

    def render_with_injections(self, gallery: RemoteGallery) -> str:
        """Parses the content for [img:id] tags and injects gallery images."""
        pattern = r'\[img:(.+?)\]'

        def replace_match(match):
            img_id = match.group(1)
            image = gallery.get_image(img_id)
            if image:
                return f'<img src="{image.url}" alt="{image.alt_text}" />'
            return f'[Image {img_id} not found]'

        return re.sub(pattern, replace_match, self.content)


class Timeline:
    """Manages a chronological list of posts."""

    def __init__(self):
        self.posts: List[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)
        # Ensure posts are ordered newest to oldest
        self.posts.sort(key=lambda p: p.timestamp, reverse=True)

    def display(self, gallery: RemoteGallery) -> str:
        """Renders the full timeline with injected images."""
        output = []
        for post in self.posts:
            time_str = post.timestamp.strftime("%Y-%m-%d %H:%M")
            rendered_content = post.render_with_injections(gallery)
            output.append(f"--- Post {post.post_id} | {time_str} ---\n{rendered_content}\n")
        return "\n".join(output)


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Setup the Remote Gallery
    gallery = RemoteGallery()
    gallery.add_image("img_001", "https://remote.cdn/images/vacation.jpg", "Beach sunset")
    gallery.add_image("img_002", "https://remote.cdn/images/hike.jpg", "Mountain peak")

    # 2. Create Timeline and Posts
    timeline = Timeline()

    timeline.add_post(Post(
        post_id=1,
        content="Just got back from the beach! Look at this view: [img:img_001]\nIt was amazing."
    ))

    timeline.add_post(Post(
        post_id=2,
        content="The mountains were cold but worth it. [img:img_002]\nNext time, bringing a heavier coat."
    ))

    # 3. Output the rendered timeline
    print(timeline.display(gallery))
