import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from realys import init_relays, set_relays, gpio_cleanup

def main():
    parser = argparse.ArgumentParser(description="Test relay switching.")
    parser.add_argument('-d', '--duration', type=int, default=5, help='Seconds to keep relay on (default: 5)')
    args = parser.parse_args()

    init_relays()
    try:
        print(f"Relay ON for {args.duration}s...")
        set_relays(True)
        time.sleep(args.duration)
        print("Relay OFF")
        set_relays(False)
    finally:
        gpio_cleanup()
        print("Done")

if __name__ == '__main__':
    main()