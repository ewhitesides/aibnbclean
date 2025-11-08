import argparse
import os
import aibnbclean

# only executes when run.py is called directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run aibnbclean with specific config directory"
    )

    parser.add_argument(
        "--config_dir",
        type=str,
        required=False,
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Path to the configuration directory"
    )

    args = parser.parse_args()

    aibnbclean.process(
        config_dir=args.config_dir
    )
