import argparse
import pydub
import glob
import os
import random
import itertools
import tqdm
from collections import Counter


class RandomBag:
    def __init__(self):
        self.probabilities = Counter()

    def add(self, item, prob):
        self.probabilities[item] += int(prob)

    def sample_and_remove(self):
        chain = list(
            itertools.chain(
                *(
                    itertools.repeat(item, prob)
                    for item, prob in self.probabilities.items()
                )
            )
        )
        item = random.choice(chain)
        self.probabilities.pop(item)
        return item

    def __len__(self):
        return len(self.probabilities)


def generate_sequence(samples, target_length: int):
    bag = RandomBag()

    output = None
    with tqdm.tqdm(total=target_length) as prog:
        for i in itertools.count(1):
            if not len(bag):  # Bag emptied, replenish it
                for filename, sample in samples.items():
                    bag.add(filename, len(sample) / 1000)

            sample_name = bag.sample_and_remove()
            sample = samples[sample_name]
            if output is None:
                output = sample
            else:
                output = output.append(sample, crossfade=100)
            out_len = len(output)
            prog.n = 0
            prog.set_description(f"Iteration {i}, bag size {len(bag)}", refresh=False)
            prog.update(out_len)
            if out_len >= target_length:
                break
    return output


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input-dir", required=True)
    ap.add_argument("-o", "--output-file", required=True)
    ap.add_argument("-l", "--output-length", required=True, type=int)
    ap.add_argument("-n", "--n-files", type=int)
    args = ap.parse_args()
    output_format = os.path.splitext(args.output_file)[1].strip(".")
    assert output_format in ("wav", "mp3")
    target_length = args.output_length * 1000
    filenames = glob.glob(os.path.join(args.input_dir, "*.wav"))
    samples = {
        filename: pydub.AudioSegment.from_file(filename)
        for filename in tqdm.tqdm(filenames, desc="Loading samples")
    }
    if not args.n_files:
        output = generate_sequence(samples, target_length)
        print("Writing output...")
        output.export(args.output_file, format=output_format)
    else:
        for x in range(args.n_files):
            print(f"Generating file {x + 1}/{args.n_files}...")
            base, ext = os.path.splitext(args.output_file)
            filename = f"{base}_{x:04d}{ext}"
            output = generate_sequence(samples, target_length)
            print(f"Writing {filename}...")
            output.export(filename, format=output_format)


if __name__ == "__main__":
    main()
