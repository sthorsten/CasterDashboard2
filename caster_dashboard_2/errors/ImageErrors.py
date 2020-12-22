from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ImageTooLargeError(ValidationError):
    """Exception raised for too large images (default: >1MB)

     Attributes:
         image_size -- input salary which caused the error
         message -- explanation of the error
     """

    def __init__(self, image_size, message=None):
        self.image_size = image_size
        if message:
            self.message = message
        else:
            self.message = _("Image too large (can be 1MB, is %(image_size)sMB)") % {
                "image_size": round(self.image_size / 1024 / 1024, 2)}
        super().__init__(self.message)


class ImageNotSquareError(ValidationError):
    """Exception raised for not square images

     Attributes:
         width -- image width
         height -- image height
         message -- explanation of the error
     """

    def __init__(self, width, height, message=None):
        self.width = width
        self.height = height
        if message:
            self.message = message
        else:
            self.message = _("Image must be square (is %(width)sx%(height)s)") % {
                "width": self.width, "height": self.height}
        super().__init__(self.message)
