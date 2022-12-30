from sdserver import api

import uuid
import click

@click.group()
def sdserver():
    pass

@sdserver.command()
def serve():
    click.echo('serve')

@sdserver.command()
@click.argument('filenames', nargs=-1)
def upscale(filenames):
    api.upscale(filenames)

@sdserver.command()
@click.argument('prompt')
@click.option(
    "--prompt-strength",
    default=7.5,
    show_default=True,
    help="How closely to follow the prompt. Image looks unnatural at higher values",
)
@click.option(
    "-r",
    "--repeats",
    default=1,
    show_default=True,
    type=int,
    help="How many times to repeat the renders. If you provide two prompts and --repeat=3 then six images will be generated.",
)
def imagine(prompt, prompt_strength, repeats):
    identifier = uuid.uuid4()
    for result in api.imagine(
        identifier,
        prompt,
        prompt_strength=prompt_strength,
        repeats=repeats,
    ):
        print(result)

if __name__ == '__main__':
    sdserver()