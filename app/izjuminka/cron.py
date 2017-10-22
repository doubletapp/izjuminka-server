# from django.contrib.auth.models import User

def test_scheduled_job():
    print(1)


if __name__ == "__main__":
    # print(User.objects())


    import vk

    session = vk.Session(access_token='6e7f31b2f7bb14a27e2a756fe9d3a07b650e44ad9c8a2959fb2043b8ab9fc0a40e9ef9612d7b185729258')
    api = vk.API(session)


    print(api)

    print(api.users.get(user_ids=95586611, fields='photo_200'))