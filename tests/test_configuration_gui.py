#from unittest import TestCase
#
#import os
#
#from supplychainpy._gui.controller.validate import host
#from supplychainpy._gui.launch import home
#
#
#class TestValidation(TestCase):
#    """"""
#    def test_host_address(self):
#        self.assertTrue(host('192.166.2.111'))
#        self.assertFalse(host('1921662.111'))
#
#    def test_data_source_path_validation(self):
#        configuration_gui = home(True)
#        configuration_gui.finished_btn.invoke()
#        configuration_gui.parent.update()
#        self.assertEqual('Please enter a valid path ', configuration_gui.data_entry_validation.cget("text"))
#        configuration_gui.parent.destroy()
#
#    def test_data_source_path(self):
#        configuration_gui = home(True)
#        current_dir = os.path.abspath(os.curdir)
#        sample_data_dir = os.path.abspath('{}{}..{}sample_data'.format(current_dir, os.path.sep, os.path.sep))
#        data_set_path = '{}{}complete_data_set_small.csv'.format(sample_data_dir, os.path.sep)
#        configuration_gui.data_entry.insert(0, data_set_path)
#        configuration_gui.validate_completed_form()
#        configuration_gui.data_entry.update()
#        self.assertEqual(data_set_path, configuration_gui.data_entry.get())
#        configuration_gui.parent.destroy()
#
#    def test_database_path(self):
#        configuration_gui = home(True)
#        current_dir = os.path.abspath(os.curdir)
#        sample_data_dir = os.path.abspath('{}{}..{}sample_data'.format(current_dir, os.path.sep, os.path.sep))
#        data_set_path = '{}{}complete_data_set_small.csv'.format(sample_data_dir, os.path.sep)
#        configuration_gui.data_entry.insert(0, data_set_path)
#        configuration_gui.data_entry.update()
#        db_path = configuration_gui.db_path(data_set_path)
#        configuration_gui.update_db_path(data_set_path)
#        configuration_gui.database_entry.update()
#        configuration_gui.finished_btn.invoke()
#        configuration_gui.finished_btn.update()
#        configuration_gui.validate_completed_form()
#        self.assertEqual(db_path, configuration_gui.database_entry.get())
#        configuration_gui.parent.destroy()
#
#    def test_host(self):
#        configuration_gui = home(True)
#        host_address = "0.0.0.0"
#        configuration_gui.host_entry.insert(0, host_address)
#        configuration_gui.host_entry.update()
#        self.assertEqual(host_address, configuration_gui.host_entry.get())
#        configuration_gui.parent.destroy()
#
#    def test_host_validation(self):
#        configuration_gui = home(True)
#        host_address = "0.0.0.0"
#        configuration_gui.host_entry.insert(0, host_address)
#        res = configuration_gui.validate_host(host_address)
#        self.assertTrue(res)
#        configuration_gui.host_entry_var.set(configuration_gui.HOST_VALIDATION)
#        self.assertEqual(configuration_gui.HOST_VALIDATION, configuration_gui.host_entry_validation.cget("text"))
#        configuration_gui.parent.destroy()
#
#    def test_port(self):
#        configuration_gui = home(True)
#        current_dir = os.path.abspath(os.curdir)
#        sample_data_dir = os.path.abspath('{}{}..{}sample_data'.format(current_dir, os.path.sep, os.path.sep))
#        data_set_path = '{}{}complete_data_set_small.csv'.format(sample_data_dir, os.path.sep)
#        configuration_gui.data_entry.insert(0, data_set_path)
#        port_num = 5000
#        configuration_gui.port_entry.insert(0, port_num)
#        configuration_gui.validate_completed_form()
#        configuration_gui.port_entry.update()
#        self.assertEqual(port_num, int(configuration_gui.port_entry.get()))
#        configuration_gui.parent.destroy()
#
#    def test_port_validation(self):
#        configuration_gui = home(True)
#        port_num = 5000
#        res = configuration_gui.validate_port(port_num)
#        self.assertTrue(res)
#        configuration_gui.port_entry.update()
#        configuration_gui.port_entry_var.set(configuration_gui.PORT_VALIDATION)
#        self.assertEqual(configuration_gui.PORT_VALIDATION, configuration_gui.port_entry_validation.cget("text"))
#        configuration_gui.parent.destroy()
#
#    def test_check_validation(self):
#        configuration_gui = home(True)
#        configuration_gui.launch_var.set(False)
#        configuration_gui.analysis_var.set(False)
#        res = configuration_gui.validate_settings_check_buttons(configuration_gui.launch_var.get(),
#                                                                configuration_gui.analysis_var.get())
#        self.assertFalse(res)
#        configuration_gui.settings_checkbox_var.set(configuration_gui.CHECKBOX_VALIDATION)
#        self.assertEqual(configuration_gui.CHECKBOX_VALIDATION,
#                         configuration_gui.settings_checkbox_validation.cget("text"))
#        configuration_gui.parent.destroy()