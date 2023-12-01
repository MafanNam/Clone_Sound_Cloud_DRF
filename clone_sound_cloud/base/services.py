from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file):
    """Path to file avatar"""
    return f"avatar/user_{instance.id}/{file}"


def get_path_upload_album(instance, file):
    """Path to file album"""
    return f"album/user_{instance.id}/{file}"


def get_path_upload_track(instance, file):
    """Path to file album"""
    return f"track/user_{instance.id}/{file}"


def get_path_upload_playlist(instance, file):
    """Path to file playlist"""
    return f"playlist/user_{instance.id}/{file}"


def validate_size_image(file_obj):
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Max size for file {megabyte_limit}MB")


def validate_size_audio(file_obj):
    megabyte_limit = 6
    if file_obj.size > megabyte_limit * 1024 ** 6:
        raise ValidationError(f"Max size for audio file {megabyte_limit}MB")
