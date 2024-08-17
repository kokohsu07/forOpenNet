import time

from gen_func import *
from variable import *
from config import *


def test_video_playing(mobile: Chrome):
    search_target_item(target_item, mobile)
    scroll_down_transform(scroll_times, offset, mobile)
    click_random_item(ele_video_list, mobile)

    isProfile=check_profile_page(mobile)
    while isProfile:
        mobile.back()
        click_random_item(ele_video_list, mobile)
        isProfile = check_profile_page(mobile)

    check_video_is_playing(ele_cur_video, mobile)
    take_screenshot(mobile, 'search_page')






