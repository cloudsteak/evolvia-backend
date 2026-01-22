import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Logging
    log_level: str

    # Redis
    redis_host: str
    redis_port: int
    redis_db: int

    # Auth0
    auth0_domain: str
    auth0_audience: str
    auth0_algorithms: str

    # GitHub
    github_repo: str
    github_workflow_filename: str
    github_token: str

    # WordPress
    wordpress_webhook_url: str | None
    wordpress_secret_key: str | None

    # Internal
    internal_secret: str

    # Messenger service
    messenger_host: str
    messenger_path: str
    messenger_template: str
    internal_messenger_api_key: str

    # Verify service
    verify_lab_host: str
    verify_lab_path: str
    internal_verify_api_key: str


def get_settings() -> Settings:
    return Settings(
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", 6379)),
        redis_db=int(os.getenv("REDIS_DB", 0)),

        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_audience=os.environ["AUTH0_AUDIENCE"],
        auth0_algorithms=os.getenv("AUTH0_ALGORITHMS", "RS256"),

        github_repo=os.environ["GITHUB_REPO"],
        github_workflow_filename=os.environ["GITHUB_WORKFLOW_FILENAME"],
        github_token=os.environ["GITHUB_TOKEN"],

        wordpress_webhook_url=os.getenv("WORDPRESS_WEBHOOK_URL"),
        wordpress_secret_key=os.getenv("WORDPRESS_SECRET_KEY"),

        internal_secret=os.environ["INTERNAL_SECRET"],

        messenger_host=os.environ["MESSENGER_HOST"],
        messenger_path=os.environ["MESSENGER_PATH"],
        messenger_template=os.getenv("MESSENGER_TEMPLATE", "lab_ready_default"),
        internal_messenger_api_key=os.environ["INTERNAL_MESSENGER_API_KEY"],

        verify_lab_host=os.environ["VERIFY_LAB_HOST"],
        verify_lab_path=os.environ["VERIFY_LAB_PATH"],
        internal_verify_api_key=os.environ["INTERNAL_VERIFY_API_KEY"],
    )
