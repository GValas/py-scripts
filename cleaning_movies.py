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
    "fastsub",
    "french",
    "h264",
    "hdlight",
    "hdr",
    "hdtv",
    "hq",
    "imax",
    "multi",
    "multitruefrench",
    "proper",
    "repack",
    "subfrench",
    "truefrench",
    "vff",
    "vostfr",
    "web",
    "webdl",
    "webdl1080p",
    "webrip",
    "x264",
    "xvid",
}

# get movies dirs
def get_movies_dirs(roots):
    alls = set()
    for root in roots:
        for rootdir, dirnames, filenames in os.walk(root):
            dir = [os.path.join(rootdir, dir) for dir in dirnames]
            alls.update(dir)
    return alls


# get movies titles
def get_movies_titles(roots):
    alls = set()
    for root in roots:
        for rootdir, dirnames, filenames in os.walk(root):
            filepath = [os.path.join(rootdir, filename) for filename in filenames]
            alls.update(filepath)
    return alls


# clean movie dir
def clean_movies_dir(dir: str):

    # split dir and base names
    dir_name = os.path.dirname(dir)
    base_name = os.path.basename(dir)

    # remove useless characters
    base_name = re.sub(r"[()\s-]", ".", base_name)
    base_name = re.sub(r"\.{2,}", ".", base_name)

    # capitalize tokens
    words = base_name.split(".")
    words = [word.capitalize() for word in words]
    base_name = ".".join(words)

    # remove fisrt dot
    base_name = re.sub(r"^\.", "", base_name)

    return os.path.join(dir_name, base_name)


# clean movie title
def clean_movie_title(title: str):

    # split dir and base names
    dir_name = os.path.dirname(title)
    base_name = os.path.basename(title)

    # remove useless characters
    base_name = re.sub(r"[()\s-]", ".", base_name)
    base_name = re.sub(r"\.{2,}", ".", base_name)

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
    new_title = re.sub(r"\b(\d{4})\b", "(\\1)", new_title)

    # remove fisrt dot
    new_title = re.sub(r"^\.", "", new_title)

    return os.path.join(dir_name, new_title)


def clean_movies_dirs(dirs):
    return [clean_movies_dir(dir) for dir in dirs]


def clean_movies_titles(titles):
    return [clean_movie_title(title) for title in titles]


def print_movies(old_movies, new_movies):
    # log_file = os.path.join(os.path.realpath(__file__), "out.txt")
    # with open(log_file, "w", encoding="utf-8") as out:
    #     for old, new in zip(old_movies, new_movies):
    #         if old != new:
    #             print(old, new)
    #             out.write("\n" + old + "\n")
    #             out.write(new + "\n" if old != new else "*** same ***\n")

    # co sorting lists
    old_movies, new_movies = zip(*sorted(zip(old_movies, new_movies)))

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

    # root dirs
    roots = set(sys.argv[1].split(";"))
    print("Cleaning movies of ...")
    print(roots)

    # cleaning & renaming dirs
    olds = get_movies_dirs(roots)
    news = clean_movies_dirs(olds)
    rename_movies(olds, news)
    # print_movies(olds, news)

    # cleaning & renaming titles
    olds = get_movies_titles(roots)
    news = clean_movies_titles(olds)
    rename_movies(olds, news)
    # print_movies(olds, news)


if __name__ == "__main__":
    main()
