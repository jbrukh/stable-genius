from setuptools import setup

setup(
    name="sdserver",
    author="Jake Brukhman",
    version="0.0.0",
    description="Backend for serving generative AI functions (based on imaginAIry)",
    entry_points={
        "console_scripts": [
            "sdserver=sdserver.cmds:sdserver",
        ],
    },
    install_requires=[
        "imaginairy==7.3.0",
    ],
)
