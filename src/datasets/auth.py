from .logic import organisations_for_user


def user_can_edit_dataset(user, dataset):
    return user.is_staff or \
        dataset.creator == user or \
        dataset.organisation in organisations_for_user(user)

def user_can_edit_datafile(user, datafile):
    return user_can_edit_dataset(user, datafile.dataset)
