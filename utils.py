import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Web crawler arguments.")

    parser.add_argument(
        "-s", "--seeds",
        type=str,
        required=True,
        help="Path to a file containing seed URLs (one URL per line)."
    )

    parser.add_argument(
        "-n", "--limit",
        type=int,
        required=True,
        help="Target number of webpages to crawl."
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug mode (optional)."
    )

    args = parser.parse_args()
    return args

def load_seeds(seed_file_path):
    seeds = []
    with open(seed_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(line)
    return seeds
