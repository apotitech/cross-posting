import os
import requests
import streamlit as st

def post_article(title, body, tags, canonical_url, cover_image):
    tags = [tag.strip() for tag in tags.split(',')]
    platforms = [
        {
            "name": "Dev.to",
            "url": "https://dev.to/api/articles",
            "headers": {"Authorization": f'Bearer {os.getenv("DEV_TO_API_KEY")}'},
            "payload": {"article": {"body_markdown": body}}
        },
        {
            "name": "Hashnode",
            "url": "https://api.hashnode.com/",
            "headers": {"Authorization": f'Bearer {os.getenv("HASHNODE_TOKEN")}'},
            "payload": {
                "query": f'mutation {{\n  createPublicationStory(\n    input: {{\n      title: "{title}",\n      contentMarkdown: "{body}",\n      coverImageURL:""   }}\n    publicationId:"{os.getenv("HASHNODE_ID")}",\n    hideFromHashnodeFeed:false\n  ) {{\n    message\n    post{{\n      title\n    }}\n  }}\n}}\n'}
        },
        {
            "name": "Medium",
            "url": f'https://api.medium.com/v1/users/{os.getenv("MEDIUM_ID")}/posts',
            "headers": {"Authorization": f'Bearer {os.getenv("MEDIUM_TOKEN")}'},
            "payload": {
                'title': title,
                'contentFormat': 'markdown',
                'content': body,
                'canonicalUrl': canonical_url,
                'tags': tags,
                'publishStatus': 'public'
            }
        },
        {
            "name": "CodeNewbie",
            "url": "https://community.codenewbie.org/api/articles",
            "headers": {"api-key": os.getenv("CODENEWBIE_API_KEY")},
            "payload": {"article": {"body_markdown": body}}
        },
    ]
    return platforms

def validate_input(title, body, tags, canonical_url, cover_image):
    if not title:
        st.error("Please enter a title.")
        return False
    if not body:
        st.error("Please enter a body.")
        return False
    if not tags:
        st.error("Please enter some tags.")
        return False
    if not canonical_url:
        st.warning("Please enter a canonical URL.")
    if not cover_image:
        st.warning("Please enter a cover image URL.")
    return True

def main():
    st.title("Streamlit Article Crossposter")
    title = st.text_input("Title: ")
    body_file = st.file_uploader("Upload the article file", type='markdown')
    tags = st.text_input("Tags: ")
    canonical_url = st.text_input("Canonical URL: ")
    cover_image = st.text_input("Cover Image URL: ")

    if st.button("Post Article"):
        if not validate_input(title, body_file, tags, canonical_url, cover_image):
            return

        body = body_file.read() if body_file is not None else None
        platforms = post_article(title, body, tags, canonical_url, cover_image)

        with st.spinner("Posting article..."):
            progress_bar = st.progress(0)
            for platform in platforms:
                try:
                    response = requests.post(platform["url"], headers=platform["headers"], json=platform["payload"])
                    if response.status_code in [200, 201]:
                        st.success(f"Article posted to {platform['name']}.")
                    else:
                        st.error(f"Error posting to {platform['name']}. HTTP Status: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Exception occurred while posting to {platform['name']}: {str(e)}")
                progress_bar.progress(progress_bar.value + 1/len(platforms))

if __name__ == "__main__":
    main()
