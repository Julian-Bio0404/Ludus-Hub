"""File utils."""


def user_directory_path(instance, filename: str) -> str:
    return f'user_{instance.user.id}/{filename}'


def sport_directory_path(instance, filename: str) -> str:
    return f'sport_{instance.id}/{filename}'
