# python3
# Copyright 2021 InstaDeep Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Install script for setuptools."""

import datetime
import sys
from importlib import util as import_util

from setuptools import find_packages, setup

spec = import_util.spec_from_file_location("_metadata", "mava/_metadata.py")
_metadata = import_util.module_from_spec(spec)  # type: ignore
spec.loader.exec_module(_metadata)  # type: ignore

reverb_requirements = [
    "dm-reverb~=0.6.1",
]

tf_requirements = [
    "tensorflow~=2.7.0",
    "tensorflow_probability~=0.15.0",
    "dm-sonnet",
    "trfl",
]

jax_requirements = [
    "chex",
    "jax",
    "jaxlib",
    "dm-haiku",
    "flax",
    "optax",
    "rlax",
] + tf_requirements

pettingzoo_requirements = [
    "pettingzoo~=1.17.0",
    "multi_agent_ale_py",
    "supersuit==3.3.4",
    "pygame",
    "pysc2",
]

launchpad_requirements = ["dm-launchpad~=0.3.2"]

smac_requirements = ["pysc2", "SMAC @ git+https://github.com/oxwhirl/smac.git"]
testing_formatting_requirements = [
    "pytest==6.2.4",
    "pre-commit",
    "mypy==0.941",
    "pytest-xdist",
    "flake8==3.8.2",
    "black==22.3.0",
    "pytest-cov",
    "interrogate",
    "pydocstyle",
    "types-six",
]

record_episode_requirements = ["array2gif"]

flatland_requirements = ["flatland-rl==3.0.1"]
open_spiel_requirements = ["open_spiel"]

long_description = """Mava is a library for building multi-agent reinforcement
learning (MARL) systems. Mava builds off of Acme and in a similar way strives
to expose simple, efficient, and readable components, as well as examples that
serve both as reference implementations of popular algorithms and as strong
baselines, while still providing enough flexibility to do novel research.
For more information see
[github repository](https://github.com/instadeepai/mava)."""

# Get the version from metadata.
version = _metadata.__version__  # type: ignore

# If we're releasing a nightly/dev version append to the version string.
if "--nightly" in sys.argv:
    sys.argv.remove("--nightly")
    version += ".dev" + datetime.datetime.now().strftime("%Y%m%d")

setup(
    name="id-mava",
    version=version,
    description="A Python library for Multi-Agent Reinforcement Learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="InstaDeep Ltd",
    license="Apache License, Version 2.0",
    keywords="multi-agent reinforcement-learning python machine learning",
    packages=find_packages(),
    install_requires=[
        "dm-acme~=0.2.4",
        "chex",
        "absl-py",
        "dm_env",
        "dm-tree",
        "numpy~=1.21.4",
        "pillow",
        "matplotlib",
        "dataclasses",
        "box2d-py",
        "gym<=0.23.0",
    ],
    extras_require={
        "tf": tf_requirements,
        "pz": pettingzoo_requirements,
        "flatland": flatland_requirements,
        "open_spiel": open_spiel_requirements,
        "reverb": reverb_requirements,
        "launchpad": launchpad_requirements,
        "testing_formatting": testing_formatting_requirements,
        "record_episode": record_episode_requirements,
        "sc2": smac_requirements,
        "envs": pettingzoo_requirements + open_spiel_requirements + smac_requirements,
        "jax": jax_requirements,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
