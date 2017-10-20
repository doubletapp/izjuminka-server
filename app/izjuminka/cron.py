from django.contrib.auth.models import User

def test_scheduled_job():
    print(1)


if __name__ == "__main__":
    print(User.objects())


    # import vk
    #
    # session = vk.AuthSession(
    #     app_id='6227710',
    #     user_login='sardnej4@yandex.ru',
    #     user_password='tunis123qwe'
    # )
    # session = vk.Session(access_token='d599b7db708cdddea4b0b07f95939f89d28a53b2de54952afd94f02f0e812eb31d57faaac906f0305f368')
    # api = vk.API(session)

    #
    # print(api)
    #
    # print(api.wall.post(owner_id=444485291, message='Спасибо всем землянам'))