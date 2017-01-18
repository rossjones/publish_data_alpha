from .logic import organisations_for_user


def user_can_edit_dataset(user, dataset):
    return dataset.organisation in organisations_for_user(user)

def user_can_edit_datafile(user, datafile):
    return user_can_edit_dataset(user, datafile.dataset)
