def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mov',
                        '.mpeg4',
                        '.mp4',
                        '.avi',
                        '.wmv',
                        '.mpegps',
                        '.flv',
                        '.3gpp',
                        '.webm',
                        '.dnxhr',
                        '.prores',
                        '.cineform',
                        '.hevc'
                        ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Please make sure that your file is a video.')
