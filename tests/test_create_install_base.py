import unittest
from unittest import TestCase

import logging

from supplychainpy.production import create_install_base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestCreateInstallBase(TestCase):
    # arrange, act
    def test_machine_build(self):
        builder = create_install_base.SimpleMachineBuilder()
        machine_up = create_install_base.ProductionDirector(builder)
        machine_up.construct_machine(name="ghost")
        machine_down = machine_up.machine
        #builder2 = create_install_base.SimpleMachineBuilder()
        #machine2_up = create_install_base.ProductionDirector(builder2)
        #machine2_up.construct_machine(name="gremlin")
        #machine2_up.machine.add_down_time()
        #machine2_down = machine2_up.machine
        # assert
        self.assertIsInstance(machine_down, create_install_base.Machine)

    def test_machine_build_str(self):
        # arrange, act
        builder = create_install_base.SimpleMachineBuilder()
        machine_up = create_install_base.ProductionDirector(builder)
        machine_up.construct_machine(name="ghost")
        machine_down = machine_up.machine
        # assert
        self.assertEqual("ghost", str(machine_down))

if __name__ == '__main__':
    unittest.main()
