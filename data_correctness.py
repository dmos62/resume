from toolz.curried import *

def check_resume_data_correctness(resume_data):
    check_experiences(resume_data["experiences"])
    check_influentials(resume_data["influential books or lectures"])

def is_list(x):
    return isinstance(x, list)

@curry
def has_key(k, d):
    return k in d

@curry
def functional_assert(pred, x):
    assert pred(x)
    return x

def check_experiences(experiences):
    functional_assert(is_list, experiences)
    for experience in experiences:
        pipe( experience,
                functional_assert(has_key("title")),
                functional_assert(has_key("tags")),
                functional_assert(has_key("description")),
                functional_assert(has_key("time period")),
                )

def check_influentials(influentials):
    functional_assert(is_list, influentials)
    for influence in influentials:
        pipe( influence,
                functional_assert(has_key("title")),
                functional_assert(has_key("author")),
                functional_assert(has_key("link")),
                functional_assert(has_key("comment")),
                )
