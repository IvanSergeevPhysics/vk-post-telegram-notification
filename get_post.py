import vk_api

class VKGrabber:

    def __init__(self, login, password):
        self.__vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
        self.__vk_session.auth()
        self.__vk = self.__vk_session.get_api()
        self.last_date = self.__vk.wall.get(domain='notitle.softgrunge', count=1)['items'][0]['date']


    def checkNewPost(self, groups):
        notify_message = str()
        img_lst = []
        for group in groups:
            obj_id = self.__vk.utils.resolveScreenName(screen_name=group)['object_id']
            post = self.__vk.wall.get(owner_id = -obj_id, domain=group, count=1)['items'][0]
            if post['date'] > self.last_date:
                self.last_date = post['date']
                group_ret, post_ret = group, post
                notify_message += f"A new post: https://vk.com/{group}?w=wall{post['owner_id']}_{post['id']}\n\nImages from the post:\n"
                for att in post['attachments']:
                    img_lst.append(att['photo']['sizes'][-1]['url'])
                    #notify_message += f"{att['photo']['sizes'][-1]['url']}\n"
        return notify_message, img_lst


    