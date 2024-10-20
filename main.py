import asyncio, twikit, atproto, json
with open('vars.json') as f: envvars = json.load(f) # passwords idk how to do that without json sorry



# twitter scraper

#usrid = 1646013705874976768
usrid = envvars['scrapeid']

tcli = twikit.Client()

async def get_tweets():
    return await tcli.get_user_tweets(usrid, 'Tweets', count = 5)

async def main():
    await tcli.login(
        auth_info_1 = envvars['tauth1'],
        auth_info_2 = envvars['tauth3'],
        password = envvars['tauth2']
    )

    before = await get_tweets()
    print('got tweets, waiting for new ones...')

    while True:
        await asyncio.sleep(30)
        latest = await get_tweets()
        if before != latest:
            ntwt = []
            for tw in latest:
                if tw == before[0]:
                    break
                ntwt.append(tw)
            for tw in reversed(ntwt):
                print(f'sending tweet id {tw.id}')
                post(tw)
            print('waiting...')
        before = latest



# bsky post

bcli = atproto.Client()
bcli.login(envvars['bauth1'], envvars['bauth2'])

def post(tweet):
    txt = tweet.fulltext
    if tweet.retweeted_tweet:
        pos = txt.find(':')
        txt = txt[pos+1, -1]
        txt = f'Reposted from @{tweet.retweeted_tweet.user.name} : ' + txt + '\n\n'
    if tweet.quote:
        txt = f'QRT to: https://x.com/{tweet.retweeted_tweet.user.name}/status/{tweet.quote.id}' + txt + '\n\n'
    if tweet.media: # TODO
        media = []
        for m in tweet.media:
            media.append(m.media_url)
    else: media = None
    bcli.send_post(txt)



asyncio.run(main())