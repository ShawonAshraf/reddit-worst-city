from extractor import RedditCommentExtractor
from settings import settings
from praw import Reddit
from loguru import logger


def main():
    # =========== init reddit client ===========
    logger.info("Initializing Reddit client")
    client = Reddit(
        client_id=settings.reddit_client_id.get_secret_value(),
        client_secret=settings.reddit_client_secret.get_secret_value(),
        user_agent=settings.reddit_user_agent,
    )
    logger.success("Reddit client initialized")

    # =========== init reddit comment extractor ===========
    logger.info("Initializing Reddit comment extractor")
    extractor = RedditCommentExtractor(post_url=settings.post_url, client=client)
    logger.success("Reddit comment extractor initialized")

    # =========== extract comments ===========
    logger.info("Extracting comments")
    extractor.extract()
    logger.success("Comments extracted")

    # =========== save comments ===========
    logger.info("Saving comments")
    extractor.save()
    logger.success("Comments saved")


if __name__ == "__main__":
    main()
