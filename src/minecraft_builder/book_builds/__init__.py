from .registry import BOOK_BUILDS, BookBuild, get_build, match_build

__all__ = ["BOOK_BUILDS", "BookBuild", "generate_book_build", "get_build", "match_build"]

def generate_book_build(*args, **kwargs):
  from .generators import generate_book_build as _gen
  return _gen(*args, **kwargs)
