from argparse import ArgumentParser
import math
from pathlib import Path

import filetype
import pillow_avif
from PIL import Image
from tqdm import tqdm


if __name__ == "__main__":
   parser = ArgumentParser()
   parser.add_argument("-i", "--input", required=True, help="input directory")
   parser.add_argument("-o", "--output", default="output", help="output directory")
   parser.add_argument("-e", "--caption_extension", default=".txt", help="caption file extension")
   parser.add_argument("-r", "--resolution", type=int, default=512, help="base resolution of saving images")
   parser.add_argument("-f", "--force", action="store_true", help="force overwriting existing files")
   args = parser.parse_args()

   input_dir = Path(args.input)
   output_dir = Path(args.output)

   output_dir.mkdir(parents=True, exist_ok=True)

   image_files = [f for f in input_dir.glob("*") if filetype.image_match(f)]

   for image_file in tqdm(image_files):
      image = Image.open(image_file)

      ratio = math.sqrt(image.height * image.width / (args.resolution * args.resolution))
      if ratio > 1.0:
         w = int(image.width / ratio)
         h = int(image.height / ratio)
         image = image.resize((w, h), Image.LANCZOS)

      output_file = output_dir / image_file.with_suffix(".avif").name
      if not output_file.exists() or args.force:
         image.save(output_file)

      caption_file = image_file.with_suffix(args.caption_extension)
      if caption_file.exists():
         output_file = output_dir / caption_file.name
         if not output_file.exists() or args.force:
            output_file.hardlink_to(caption_file)


