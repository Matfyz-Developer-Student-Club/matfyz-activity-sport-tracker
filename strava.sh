#curl -X POST https://www.strava.com/api/v3/push_subscriptions\
#      -F client_id=63365 \
#      -F client_secret=873cc2b0d0f42dae20859c050ac9ab243ed268f7 \
#      -F 'callback_url=https://mathletics-test.ks.matfyz.cz/strava/webhook/endpoint' \
#      -F 'verify_token=STRAVA_MATHLETICS'

curl -G https://www.strava.com/api/v3/push_subscriptions \
    -d client_id=63365 \
    -d client_secret=873cc2b0d0f42dae20859c050ac9ab243ed268f7