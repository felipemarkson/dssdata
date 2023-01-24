from pandas.testing import assert_frame_equal


def assert_df_no_ang(correct, to_test):
    to_test_noang = to_test.loc[:, ~to_test.columns.str.startswith("ang_")]
    correct_noang = correct.loc[:, ~correct.columns.str.startswith("ang_")]

    assert_frame_equal(correct_noang, to_test_noang, check_dtype=False, atol=1e-2)
