from django.core.cache import cache


popular_tags_cache_key = 'popular_tags'
best_members_cache_key = 'best_members'


def set_popular_tags(tags_list):
    cache.set(popular_tags_cache_key, tags_list)


def get_popular_tags():
    # return Tag.objects.all()[:10]
    return cache.get(popular_tags_cache_key, [])


def set_best_members(members_list):
    cache.set(best_members_cache_key, members_list)


def get_best_members():
    # return Member.objects.all()[:10]
    return cache.get(best_members_cache_key, [])
