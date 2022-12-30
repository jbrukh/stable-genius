from imaginairy.enhancers.upscale_realesrgan import upscale_image
from imaginairy.schema import ImaginePrompt, ImagineResult
from imaginairy.api import imagine as imagine_cmd
from imaginairy.log_utils import configure_logging
from imaginairy import config
from PIL import Image, ImageDraw
from uuid import uuid4

import os

def upscale(filenames):
    for filename in filenames:
        with Image.open(filename) as img:
            print(f'Upscaling {filename}')
            upscaled_image = upscale_image(img)
            outfile = f"{uuid4()}.png"
            print(f'Writing to {outfile}')
            upscaled_image.save(outfile)

def imagine(
    identifier,
    prompt_text,
    negative_prompt=config.DEFAULT_NEGATIVE_PROMPT,
    prompt_strength=7.5,
    init_image=None,
    init_image_strength=0.6,
    outdir="output",
    output_file_extension="png",
    repeats=1,
    height=512,
    width=512,
    steps=25,
    seed=None,
    upscale=False,
    fix_faces=False,
    fix_faces_fidelity=None,
    sampler_type=config.DEFAULT_SAMPLER,
    tile=False,
    tile_x=False,
    tile_y=False,
    mask_image=None,
    mask_prompt=None,
    mask_mode="replace",
    mask_modify_original=True,
    precision="autocast",
    model_weights_path=config.DEFAULT_MODEL,
):
    configure_logging("ERROR")
    for _ in range(repeats):
        if tile:
            _tile_mode = "xy"
        elif tile_x:
            _tile_mode = "x"
        elif tile_y:
            _tile_mode = "y"
        else:
            _tile_mode = ""

        prompt = ImaginePrompt(
            prompt_text,
            negative_prompt=negative_prompt,
            prompt_strength=prompt_strength,
            init_image=init_image,
            init_image_strength=init_image_strength,
            seed=seed,
            sampler_type=sampler_type,
            steps=steps,
            height=height,
            width=width,
            mask_image=mask_image,
            mask_prompt=mask_prompt,
            mask_mode=mask_mode,
            mask_modify_original=mask_modify_original,
            upscale=upscale,
            fix_faces=fix_faces,
            fix_faces_fidelity=fix_faces_fidelity,
            tile_mode=_tile_mode,
            model=model_weights_path,
        )

    prompts = [prompt]
    output_file_extension = output_file_extension.lower()
    if output_file_extension not in {"jpg", "png"}:
        raise ValueError("Must output a png or jpg")

    results = []
    for result in imagine_cmd(
        prompts,
        precision=precision
    ):
        for image_type in result.images:
            subpath = os.path.join(outdir, image_type)
            os.makedirs(subpath, exist_ok=True)
            filepath = os.path.join(
                subpath, f"{identifier}.{output_file_extension}"
            )
            result.save(filepath, image_type=image_type)
        results.append(result)
    return results
        