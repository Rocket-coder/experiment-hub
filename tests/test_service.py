from tests.test_runs import test_complete_run, test_patch_finished_run

def test_update_running_to_completed():
    test_complete_run()


def test_try_to_update_finished_run():
    test_patch_finished_run()
