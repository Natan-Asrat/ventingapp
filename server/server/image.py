from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

def validate_and_clean_image(file):
    from django.conf import settings
    from django.core.exceptions import ValidationError

    # --- 1. Check file size ---
    if file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image must be under {settings.MAX_FILE_SIZE_MB} MB.")

    # --- 2. Check content type ---
    content_type = getattr(file, "content_type", "")
    if content_type not in settings.ALLOWED_CONTENT_TYPES:
        raise ValidationError("Only JPG and PNG images are allowed.")

    # --- 3. Check file extension ---
    if not any(file.name.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
        raise ValidationError("Only JPG and PNG images are allowed.")

    # --- 4. Open and re-encode image ---
    try:
        img = Image.open(file)
        img = img.convert("RGB")  # re-encode safely
    except Exception:
        raise ValidationError("Uploaded file is not a valid image.")

    # --- 5. Save to in-memory file (Django can use this) ---
    buffer = BytesIO()
    img.save(buffer, format='JPEG')  # always save as JPEG
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=file.name)
