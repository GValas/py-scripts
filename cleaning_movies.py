import os
import re
import sys

TECH_WORDS = {
    "1080p",
    "2160p",
    "4k",
    "576p",
    "720p",
    "aac",
    "ac3",
    "bdrip",
    "bluray",
    "brrip",
    "divx",
    "dts",
    "dvdrip",
    "french",
    "french",
    "h264",
    "hdlight",
    "hdr",
    "hdtv",
    "hq",
    "imax",
    "multi",
    "proper",
    "subfrench",
    "truefrench",
    "vff",
    "web",
    "webdl",
    "webdl1080p",
    "x264",
    "xvid",
}

# get movies
def get_movies(roots):
    all_movies = set()
    for root in roots:
        for rootdir, dirnames, filenames in os.walk(root):
            filepath = [os.path.join(rootdir, filename) for filename in filenames]
            all_movies.update(filepath)
    return all_movies


# clean movie
def clean_movie(title: str):

    # split dir and base names
    dir_name = os.path.dirname(title)
    base_name = os.path.basename(title)

    # remove useless characters
    base_name = re.sub("[()\s-]", ".", base_name)
    base_name = re.sub("\.{2,}", ".", base_name)

    # remove remaining title after 1st tech word, keeping the extension
    words = base_name.split(".")
    words2 = []
    for idx, word in enumerate(words[:-1]):
        if word.lower() in TECH_WORDS:
            break
        else:
            if re.match("s\d+e\d+", word.lower()):
                words2.append(word.upper())
            else:
                words2.append(word.capitalize())

    new_title = ".".join(words2) + "." + words[-1]

    # set dates between parentheses
    new_title = re.sub("\b(\d{4})\b", "(\\1)", new_title)

    # remove fisrt dot
    new_title = re.sub("^\.", "", new_title)

    return os.path.join(dir_name, new_title)


def clean_movies(movies):
    return [clean_movie(movie) for movie in movies]


def print_movies(old_movies, new_movies):
    # log_file = os.path.join(os.path.realpath(__file__), "out.txt")
    # with open(log_file, "w", encoding="utf-8") as out:
    #     for old, new in zip(old_movies, new_movies):
    #         if old != new:
    #             print(old, new)
    #             out.write("\n" + old + "\n")
    #             out.write(new + "\n" if old != new else "*** same ***\n")

    for old, new in zip(old_movies, new_movies):
        if old != new:
            print(old)
            print(new if old != new else "*** same ***")
            print()


def rename_movies(old_movies, new_movies):
    for old, new in zip(old_movies, new_movies):
        if old != new:
            try:
                os.rename(old, new)
            except:
                print("--- error ---")

            print(f"{old} >>> {new}")


def main():

    # managing script input
    if len(sys.argv) != 2:
        print("Invalid arguments")
        exit(0)

    # root folders
    roots = set(sys.argv[1].split(";"))
    print("Cleaning movies of ...")
    print(roots)

    # former and new files
    movies = get_movies(roots)
    new_movies = clean_movies(movies)

    # renaming
    rename_movies(movies, new_movies)
    # print_movies(sorted(movies), sorted(new_movies))


if __name__ == "__main__":
    main()
