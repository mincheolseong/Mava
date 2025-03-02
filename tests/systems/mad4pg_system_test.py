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

"""Tests for mad4pg."""

import functools

import launchpad as lp
import sonnet as snt

import mava
from mava.components.tf import architectures
from mava.systems.tf import mad4pg
from mava.utils import lp_utils
from mava.utils.enums import ArchitectureType
from mava.utils.environments import debugging_utils


class TestMAD4PG:
    """Simple integration/smoke test for mad4pg."""

    def test_mad4pg_on_debugging_env(self) -> None:
        """Test feedforward mad4pg."""
        # environment
        environment_factory = functools.partial(
            debugging_utils.make_environment,
            env_name="simple_spread",
            action_space="continuous",
        )

        # networks
        network_factory = lp_utils.partial_kwargs(
            mad4pg.make_default_networks,
            policy_networks_layer_sizes=(64, 64),
            vmin=-10,
            vmax=50,
        )

        # system
        system = mad4pg.MAD4PG(
            environment_factory=environment_factory,
            network_factory=network_factory,
            num_executors=1,
            batch_size=32,
            min_replay_size=32,
            max_replay_size=1000,
            policy_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            critic_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            checkpoint=False,
        )
        program = system.build()

        (trainer_node,) = program.groups["trainer"]
        trainer_node.disable_run()

        # Launch gpu config - don't use gpu
        local_resources = lp_utils.to_device(
            program_nodes=program.groups.keys(), nodes_on_gpu=[]
        )

        lp.launch(
            program,
            launch_type="test_mt",
            local_resources=local_resources,
        )

        trainer: mava.Trainer = trainer_node.create_handle().dereference()

        for _ in range(2):
            trainer.step()

    def test_recurrent_mad4pg_on_debugging_env(self) -> None:
        """Test recurrent mad4pg."""
        # environment
        environment_factory = functools.partial(
            debugging_utils.make_environment,
            env_name="simple_spread",
            action_space="continuous",
        )

        # networks
        network_factory = lp_utils.partial_kwargs(
            mad4pg.make_default_networks,
            architecture_type=ArchitectureType.recurrent,
            policy_networks_layer_sizes=(32, 32),
            vmin=-10,
            vmax=50,
        )

        # system
        system = mad4pg.MAD4PG(
            environment_factory=environment_factory,
            network_factory=network_factory,
            num_executors=1,
            batch_size=16,
            min_replay_size=16,
            max_replay_size=1000,
            policy_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            critic_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            checkpoint=False,
            trainer_fn=mad4pg.training.MAD4PGDecentralisedRecurrentTrainer,
            executor_fn=mad4pg.execution.MAD4PGRecurrentExecutor,
            sequence_length=4,
            period=4,
            bootstrap_n=2,
        )
        program = system.build()

        (trainer_node,) = program.groups["trainer"]
        trainer_node.disable_run()

        # Launch gpu config - don't use gpu
        local_resources = lp_utils.to_device(
            program_nodes=program.groups.keys(), nodes_on_gpu=[]
        )

        lp.launch(
            program,
            launch_type="test_mt",
            local_resources=local_resources,
        )

        trainer: mava.Trainer = trainer_node.create_handle().dereference()

        for _ in range(2):
            trainer.step()

    def test_centralised_mad4pg_on_debugging_env(self) -> None:
        """Test centralised mad4pg."""
        # environment
        environment_factory = functools.partial(
            debugging_utils.make_environment,
            env_name="simple_spread",
            action_space="continuous",
        )

        # networks
        network_factory = lp_utils.partial_kwargs(
            mad4pg.make_default_networks,
            policy_networks_layer_sizes=(32, 32),
            vmin=-10,
            vmax=50,
        )

        # system
        system = mad4pg.MAD4PG(
            environment_factory=environment_factory,
            network_factory=network_factory,
            num_executors=1,
            batch_size=16,
            min_replay_size=16,
            max_replay_size=1000,
            policy_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            critic_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            checkpoint=False,
            architecture=architectures.CentralisedQValueCritic,
            trainer_fn=mad4pg.MAD4PGCentralisedTrainer,
            shared_weights=False,
        )
        program = system.build()

        (trainer_node,) = program.groups["trainer"]
        trainer_node.disable_run()

        # Launch gpu config - don't use gpu
        local_resources = lp_utils.to_device(
            program_nodes=program.groups.keys(), nodes_on_gpu=[]
        )

        lp.launch(
            program,
            launch_type="test_mt",
            local_resources=local_resources,
        )

        trainer: mava.Trainer = trainer_node.create_handle().dereference()

        for _ in range(2):
            trainer.step()

    def test_state_based_mad4pg_on_debugging_env(self) -> None:
        """Test state based mad4pg."""
        # environment
        environment_factory = functools.partial(
            debugging_utils.make_environment,
            env_name="simple_spread",
            action_space="continuous",
            return_state_info=True,
        )

        # networks
        network_factory = lp_utils.partial_kwargs(
            mad4pg.make_default_networks,
            policy_networks_layer_sizes=(32, 32),
            vmin=-10,
            vmax=50,
        )

        # system
        system = mad4pg.MAD4PG(
            environment_factory=environment_factory,
            network_factory=network_factory,
            num_executors=1,
            batch_size=16,
            min_replay_size=16,
            max_replay_size=1000,
            policy_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            critic_optimizer=snt.optimizers.Adam(learning_rate=1e-4),
            checkpoint=False,
            trainer_fn=mad4pg.MAD4PGStateBasedTrainer,
            architecture=architectures.StateBasedQValueCritic,
            shared_weights=False,
        )
        program = system.build()

        (trainer_node,) = program.groups["trainer"]
        trainer_node.disable_run()

        # Launch gpu config - don't use gpu
        local_resources = lp_utils.to_device(
            program_nodes=program.groups.keys(), nodes_on_gpu=[]
        )

        lp.launch(
            program,
            launch_type="test_mt",
            local_resources=local_resources,
        )

        trainer: mava.Trainer = trainer_node.create_handle().dereference()

        for _ in range(2):
            trainer.step()
