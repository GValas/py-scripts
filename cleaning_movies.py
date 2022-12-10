import os
import re
import glob

ROOT = r"\\horus\movies"
LOG_FILE = "out.txt"
TECH_WORDS = {
    "multi",
    "1080p",
    "720p",
    "web",
    "h264",
    "french",
    "bdrip",
    "brrip",
    "4k",
    "vff",
    "2160p",
    "hdr",
    "dvdrip",
    "bluray",
    "dts",
    "x264",
    "ac3",
    "hdlight",
    "aac",
    "divx",
    "french",
    "imax",
    "xvid",
}

# get movies
def get_movies(root):
    path = os.path.join(root, f"\**\*.*")
    return set(glob.glob(path, recursive=True))


# clean movie
def clean_movie(title: str):

    # split dir and base names
    dir_name = os.path.dirname(title)
    base_name = os.path.basename(title)

    # remove useless characters
    base_name = re.sub("[()\s-]", ".", base_name)
    base_name = re.sub("\.{2,}", ".", base_name)

    # remove title after tech words, keeping the extension
    words = base_name.split(".")
    words2 = []
    for idx, word in enumerate(words[:-1]):
        if word.lower() in TECH_WORDS:
            break
        else:
            words2.append(word.capitalize())

    new_title = ".".join(words2) + "." + words[-1]
    new_title = re.sub("(\d{4})", "(\\1)", new_title)

    return os.path.join(dir_name, new_title)


def clean_movies(movies):
    return [clean_movie(movie) for movie in movies]


def print_movies(old_movies, new_movies):
    with open(LOG_FILE, "w", encoding="utf-8") as out:
        for old, new in zip(old_movies, new_movies):
            # out.write("\n" + old + "\n")
            out.write(new + "\n")


def rename_movies(old_movies, new_movies):
    for old, new in zip(old_movies, new_movies):
        if old != new:
            try:
                os.rename(old, new)
            except:
                print("--- error ---")
                print(old)
                print(new)


def main():
    movies = get_movies(ROOT)
    new_movies = clean_movies(movies)
    rename_movies(movies, new_movies)
    # print_movies(sorted(movies), sorted(new_movies))


if __name__ == "__main__":
    main()
