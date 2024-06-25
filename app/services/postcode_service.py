from app.models.models import PostCode
from app.repositories.postcode_repository import PostcodeRepository

postcode_repository = PostcodeRepository()

class PostCodeService:
    def get_all_postcodes(self):
        return postcode_repository.get_all_postcodes()