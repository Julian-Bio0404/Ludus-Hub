"""File utils."""


def user_directory_path(instance, filename: str) -> str:
    return f'user_{instance.user.id}/{filename}'
