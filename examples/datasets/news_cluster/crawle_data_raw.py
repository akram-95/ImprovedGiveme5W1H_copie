import enum
import glob
import hashlib
import json
import os.path
import requests
import copy
import http
import urllib
from enum import Enum
from enum import auto
from typing import List

from newsplease import NewsPlease

"""
This is a dataset aiming to represent clustered news around topics. 


Used publisher:
    see research_helper


Event Source

    Crawled from 27.12.2017 - 01.01.2018
    https://news.google.com/news/headlines?ned=en&hl=en&gl=US
"""


def write_json(path, filename, object):
    """
    writes an object to a path as json
    :param path:
    :param object:
    :return:
    """
    with open(path + '/' + filename + '.' + 'json', 'w') as data_file:
        data_file.write(json.dumps(object, sort_keys=False, indent=2))
        data_file.close()

def file_exist_has_content(path, filename):
    _path = path + '/' + filename
    if os.path.exists(_path):
        if os.stat(_path).st_size != 0:
            return True
    return False

def check_image(article):
    file_exist_has_content
    # todo: skip, if already  donwlaoded
    if article['image_url']:
        extension = article['image_url'].split('.')[-1].split('?')[-1].lower()

        if extension in ['jpg', 'jpeg', 'tiff', 'tif', 'gif', 'bmp', 'png']:
            filename = article['dId'] + '.' + extension
            if not file_exist_has_content('data_image', filename):
                f = open('data_image/' + filename, 'wb')
                f.write(requests.get(article['image_url']).content)
                f.close()
#
# DATASET
#

@enum.unique
class Category(Enum):
    world = auto()
    business = auto()
    technology = auto()
    entertainment = auto()
    sports = auto()
    science = auto()


@enum.unique
class Topic(Enum):
    unspecific = auto()
    legancy = auto()


@enum.unique
class Event(Enum):
    # 27.12.2017 - 29.12.2017
    ## world
    less_1000_is_fighters_remain = auto()
    tourist_boat_hits_bridge_in_germany = auto()
    israel_approves_transfer_of_11_million_in_funding_for_west_bank_settlements = auto()
    ## business
    nyc_subway_work_trains_collide_in_tunnel_1_worker_injured = auto()
    woman_gets_284_billion_electric_bil = auto()
    erie_smashes_snowfall_record_with_flakes_still_falling = auto()
    ## technology
    iphone_8_and_iphone_8_plus_combined_to_outsell_the_iphone_x_in_its_launch_month = auto()
    amazon_and_microsoft_employees_caught_up_in_sex_trafficking_sting = auto()
    alleged_galaxy_s9_components_smile_for_the_camera_theres_a_spot_for_a_headphone_jack = auto()
    ## entertainment
    chrissy_teigen_live_tweets_nightmare_flight_after_bizarre_passenger_mishap = auto()
    cardi_b_desperately_working_to_find_offsets_hacker_after_they_leak_cheating_video__more = auto()
    rihanna_calls_for_an_end_to_gun_violence_after_death_of_her_cousin_in_barbados = auto()
    ##_sport
    pittsburgh_steelers_cruise_to_win_over_texans = auto()
    american_airlines_apologizes_after_g_league_players_accused_of_stealing_blankets_thrown_off_flight = auto()
    how_astros_first_base_coach_rich_dauer_escaped_near_death_after_world_series_parade = auto()
    ##_science
    possible_meteor_lights_up_night_sky_in_new_england = auto()
    smoke_rings_spotted_in_the_ocean_from_space = auto()
    elon_musk_reveals_red_tesla_roadster_bound_for_mars = auto()

    # 30.12.2017 - 31.12.
    ## world
    north_korea_received_oil_from_russia_in_violation_of_un_sanctions_report = auto()
    egypts_mohammed_morsi_sentenced_to_3_years_in_prison_for_insulting_judiciary = auto()
    berlin_sets_up_new_years_eve_safe_zone_for_women_amid_sexual_assault_concerns = auto()
    ## business = auto()
    police_arrest_alleged_nigerian_prince_email_scammer_in_louisiana = auto()
    digital_currency_ripple_soars_nearly_56_percent_becomes_second_largest_cryptocurrency_by_market_cap = auto()
    goldman_sachs_feels_tax_bills_burn_with_5b_charge = auto()
    ## technology = auto()
    chicagos_apple_store_has_a_falling_ice_problem = auto()
    ## entertainment = auto()
    tamar_braxton_slams_ex_vincent_herbert_for_having_a_baby_with_other_woman = auto()
    asking_if_kendall_jenner_is_pregnant_is_the_wrong_response_to_her_latest_selfie = auto()
    black_mirror_uss_callister_how_the_shatner_impression_surprise_cameo_and_flawless_production_happened = auto()
    ## sport = auto()
    uscs_cotton_bowl_loss_was_a_wake_up_call_and_not_just_for_sam_darnold = auto()
    packers_sign_center_linsley_to_contract_extension = auto()
    ## science = auto()
    the_broken_berg_stunning_nasa_image_captures_newly_created_iceberg_cracking_into_20_pieces = auto()
    russian_space_experts_regain_control_of_1st_angola_satellite = auto()
    january_will_bring_two_supermoons_a_blue_moon_and_a_total_lunar_eclipse = auto()

    # 01.01.2018
    ## world
    kim_jong_un_offers_rare_olive_branch_to_south_korea = auto()
    new_york_family_of_5_among_12_killed_in_costa_rica_plane_crash = auto()
    israel_indicts_palestinian_teenage_girl_who_punched_soldier_army = auto()
    thousands_flee_fireworks_explosion_at_australia_beach = auto()
    ##_business
    time_travel_hawaiian_airlines_flight_takes_off_in_2018_lands_in_2017 = auto()
    how_a_small_bird_managed_to_take_over_a_delta_flight = auto()
    ##_technology
    samsung_acknowledges_galaxy_note_8_battery_problems_says_very_few_phones_are_affected = auto()
    ##_entertainment
    jessica_alba_and_cash_warren_welcome_son_hayes_alba = auto()
    sun_fun_flowers_as_129th_rose_parade_rolls_in_california = auto()
    ##_sport
    chicago_bears_fire_coach_john_fox_after_5_11_season = auto()
    bruce_arians_emotional_in_announcing_retirement_from_coaching_cites_family = auto()
    ##_science
    new_years_day_full_moon_are_supermoons_really_that_super = auto()
    china_promises_the_moon = auto()
    chinas_tiangong_1_space_station_is_out_of_control_and_will_soon_fall_to_earth = auto()
    astronauts_identify_unknown_microbes_in_space_for_first_time = auto()

    #
    # Second Crawl
    #

    # Science
    First_Falcon_Heavy_launch = auto()
    fossil_sheds_light_on_origins_of_spiders = auto()
    first_planets_outside_the_Milky_Way = auto()


    # entertainment
    Top_Female__Recording_Academy = auto()
    The_New_Infinity_War_Trailer = auto()
    Quentin_Tarantino_Uma_Thurman_car_crash = auto()
    Justin_Timberlake_halftime_show = auto()
    Sarah_Silverman_and_Michael_Sheen_Break_Up = auto()

    # technology
    Apple_removed_Telegram = auto()
    Google_enables_Pixel_Visual_Core = auto()
    former_Facebook_and_Apple_employees = auto()
    Intel_smart_glass = auto()
    PS4_System_Update_5_50 = auto()
    Broadcom_Raises_Its_Qualcomm_Offer_to_121 = auto()
    Bitcoin_drops = auto()












    #
    # Old
    #
    ## misc
    las_vegas_shooting = auto()
    panama_papers = auto()  # global_politics, 3. April 2016, # Journalist Daphne Galizia
    boko_haram_21_schoolgirls_freed = auto()
    harambe = auto()  # 28. Mai 2016
    truck_attack_in_nice = auto()  # 14 July 2016
    NewYearsEveSexualAssaultsGermany = auto()
    ## north_korea
    north_Korea_hokkaido_missile = auto()
    north_Korea_Launches_satellite = auto()
    ## hacks
    hack_equifax_breach = auto()
    ## Gold_standart events
    Benghazi_US_consulate_attack = auto()  # 11. September 2012,
    croydon_tram_trash = auto()
    f1_crash = auto()
    cubs_win_championship = auto()
    china_boy_well = auto()


articles = []


def add_article(a_category: Category, a_topic: Topic, a_Event: Event, urls: List[str]):
    for ulr in urls:
        articles.append(
            {
                'CategoryId': a_category.value,
                'Category': a_category.name,
                'TopicId': a_topic.value,
                'Topic': a_topic.name,
                'EventId': a_Event.value,
                'Event': a_Event.name,
                'Url': ulr
            }
        )


# 27.12.2017 - 29.12.2017
## world
add_article(Category.world, Topic.unspecific, Event.less_1000_is_fighters_remain, [

])
add_article(Category.world, Topic.unspecific, Event.tourist_boat_hits_bridge_in_germany, [
    'https://www.nytimes.com/aponline/2017/12/27/world/europe/ap-eu-germany-ship-hits-bridge.html',
    'http://www.dailymail.co.uk/wires/ap/article-5214605/Tourist-ship-strikes-highway-bridge-Germany-27-hurt.html',
    'http://www.dw.com/en/germany-rhine-cruise-ship-hits-bridge-pylon-causing-injuries/a-41939790'
])
add_article(Category.world, Topic.unspecific,
            Event.israel_approves_transfer_of_11_million_in_funding_for_west_bank_settlements, [
                'https://www.i24news.tv/en/news/israel/163723-171227-israel-approves-transfer-of-11-million-in-funding-for-west-bank-settlements',
                'https://www.rt.com/news/414734-israel-annexation-west-bank-settlements/',
                'https://www.nytimes.com/2016/06/20/world/middleeast/israel-west-bank-settlements-palestinians.html'
            ])
## business
add_article(Category.business, Topic.unspecific, Event.nyc_subway_work_trains_collide_in_tunnel_1_worker_injured, [
    'http://www.dailyprogress.com/news/national/wire/nyc-subway-work-trains-collide-in-tunnel-worker-injured/article_3c3b5c1a-1ab1-54e1-878a-93c6f9689e8c.html',
    'http://abcnews.go.com/US/wireStory/nyc-subway-work-trains-collide-tunnel-worker-injured-52007031',
    'http://www.dailymail.co.uk/news/article-5215015/NYC-subway-work-trains-collide-tunnel-1-worker-injured.html',
    'https://www.washingtonpost.com/national/nyc-subway-work-trains-collide-in-tunnel-1-worker-injured/2017/12/27/ae5b04da-eafc-11e7-956e-baea358f9725_story.html?utm_term=.07cf57066120',
    'https://www.nytimes.com/aponline/2017/12/27/us/ap-us-subway-work-trains-collide.html'
])
add_article(Category.business, Topic.unspecific, Event.woman_gets_284_billion_electric_bil, [
    'http://www.hindustantimes.com/world-news/us-woman-gets-284-billion-electricity-bill-during-christmas-holiday-period/story-lccGPDC5vwwSg5dOm0HDpL.html',
    'http://www.huffingtonpost.com.au/2017/12/26/american-woman-receives-284-billion-electric-bill_a_23317450/?utm_hp_ref=au-homepage',
    'https://www.nytimes.com/aponline/2017/12/26/us/ap-us-billion-dollar-electric-bill.html',
    'https://www.npr.org/2017/12/26/573464352/homeowner-questions-exceedingly-high-electric-bill',
    'http://www.dailymail.co.uk/wires/ap/article-5212955/Woman-stunned-electric-bill-listed-284-billion.html',
    'https://www.washingtonpost.com/national/woman-stunned-to-find-electric-bill-listed-as-284-billion/2017/12/26/1ccee314-ea44-11e7-956e-baea358f9725_story.html?utm_term=.f04ca1439b00'
])
add_article(Category.business, Topic.unspecific, Event.erie_smashes_snowfall_record_with_flakes_still_falling, [
    'http://abcnews.go.com/US/wireStory/erie-smashes-snowfall-record-flakes-falling-52008284',
    'http://www.dailymail.co.uk/wires/ap/article-5214463/Erie-smashes-snowfall-record-flakes-falling.html',
    'https://www.nytimes.com/aponline/2017/12/27/us/ap-us-severe-weather-pennsylvania.html'
])
## technology
add_article(Category.business, Topic.unspecific,
            Event.iphone_8_and_iphone_8_plus_combined_to_outsell_the_iphone_x_in_its_launch_month, [
                'http://bgr.com/2017/12/27/iphone-x-vs-iphone-8-sales-launch-month/',
                'https://9to5mac.com/2017/12/26/iphone-x-outperformed-by-8-and-8-plus/'
            ])
add_article(Category.business, Topic.unspecific,
            Event.amazon_and_microsoft_employees_caught_up_in_sex_trafficking_sting, [
                'https://www.engadget.com/2017/12/25/amazon-microsoft-employees-sex-trafficking-sting/',
                'https://www.rt.com/usa/414266-amazon-microsoft-staff-sex-trafficking/',
                'http://www.newsweek.com/metoo-microsoft-amazon-trafficking-prostitution-sex-silicon-valley-755611'
            ])
add_article(Category.business, Topic.unspecific,
            Event.alleged_galaxy_s9_components_smile_for_the_camera_theres_a_spot_for_a_headphone_jack, [
                'https://www.phonearena.com/news/Galaxy-S9-headphone-jack_id101084',
                'https://www.thesun.co.uk/tech/5198156/samsungs-galaxy-s9-leaked-in-pics-ahead-of-rumoured-february-launch/',
                'http://www.dailymail.co.uk/sciencetech/article-5226899/Is-Samsungs-Galaxy-S9.html'
            ])

## entertainment
add_article(Category.entertainment, Topic.unspecific,
            Event.chrissy_teigen_live_tweets_nightmare_flight_after_bizarre_passenger_mishap, [
                'http://www.huffingtonpost.ca/entry/chrissy-teigen-flight-passenger-mishap_us_5a432f50e4b025f99e18a720',
                'http://edition.cnn.com/2017/12/27/us/chrissy-teigen-flight-mixup-trnd/index.html',
                'http://edition.cnn.com/2017/12/27/us/wrong-flight-passengers-trnd/index.html',
                'https://www.nytimes.com/2017/12/27/travel/chrissy-teigen-flight.html',
                'https://www.nytimes.com/reuters/2017/12/27/world/asia/27reuters-lax-flight.html',
                'https://www.npr.org/sections/thetwo-way/2017/03/27/521649877/outrage-explanations-after-united-bans-girls-from-flight-for-wearing-leggings',
                'http://www.dailymail.co.uk/news/article-5214223/LAX-Tokyo-flight-u-turns-unauthorized-person.html',
                'https://www.rt.com/usa/414330-flight-unauthorized-passenger-la/',
                'http://www.chinadaily.com.cn/cndy/2017-03/28/content_28700590.htm',
                'https://www.washingtonpost.com/national/plane-returns-to-la-because-passenger-was-on-wrong-flight/2017/12/27/e09e620c-eb1f-11e7-956e-baea358f9725_story.html'
            ])

add_article(Category.entertainment, Topic.unspecific,
            Event.cardi_b_desperately_working_to_find_offsets_hacker_after_they_leak_cheating_video__more, [
                'https://gazelle.popsugar.com/article/cardi-b-desperately-working-to-find-offsets-hacker-after-they-leak-cheating-video-more-7162002',
                'http://www.dailymail.co.uk/tvshowbiz/article-5207963/Cardi-B-fans-outraged-rapper-hit-sex-tape-claims.html'
            ])
add_article(Category.entertainment, Topic.unspecific,
            Event.rihanna_calls_for_an_end_to_gun_violence_after_death_of_her_cousin_in_barbados, [
                'http://www.thisisinsider.com/rihanna-cousin-dead-calls-for-gun-control-2017-12',
                'http://www.telegraph.co.uk/news/2017/12/27/rihanna-calls-end-gun-violence-cousin-shot-dead/',
                'http://www.dailymail.co.uk/wires/ap/article-5216099/Rihanna-mourns-cousins-death-calls-end-gun-violence.html',
                'https://www.rt.com/news/414348-rihanna-cousin-shot-dead/',
                'https://www.washingtonpost.com/entertainment/music/rihanna-mourns-cousins-death-calls-an-end-to-gun-violence/2017/12/27/f83e9708-eb40-11e7-956e-baea358f9725_story.html?utm_term=.c694e89b94ef'
            ])
## sport
add_article(Category.sports, Topic.unspecific,
            Event.american_airlines_apologizes_after_g_league_players_accused_of_stealing_blankets_thrown_off_flight,
            [
                'http://abcnews.go.com/Sports/american-airlines-apologizes-league-players-accused-stealing-blankets/story?id=52010243',
                'https://www.nytimes.com/aponline/2017/12/27/us/ap-us-american-airlines-players-removed.html',
                'http://www.dailymail.co.uk/wires/ap/article-5215769/American-sorry-accusing-NBA-G-League-players-theft.html',
                'http://www.dailymail.co.uk/news/article-5215065/American-sorry-accusing-pro-basketball-players-theft.html',
                'https://www.washingtonpost.com/business/american-sorry-for-accusing-pro-basketball-players-of-theft/2017/12/27/e629ec7a-eaff-11e7-956e-baea358f9725_story.html?utm_term=.0050a351a99a'
            ])
add_article(Category.sports, Topic.unspecific,
            Event.how_astros_first_base_coach_rich_dauer_escaped_near_death_after_world_series_parade, [
                'http://www.sportingnews.com/mlb/news/mlb-rich-dauer-astros-world-series-parade-the-athletic/1ufzt74dwoy31so676szepvlx',
                'http://www.dailymail.co.uk/news/article-5214549/Houston-Astros-coach-nearly-died-World-Series-win.html',
                'http://www.nydailynews.com/sports/baseball/astros-base-coach-died-collapsing-parade-article-1.3722556'
            ])
add_article(Category.sports, Topic.unspecific, Event.pittsburgh_steelers_cruise_to_win_over_texans, [
    'http://www.kearneyhub.com/sports/national/pittsburgh-steelers-cruise-to-win-over-texans/article_5a984248-ea63-11e7-b6b4-e7a0448030c5.html',
    'https://www.nytimes.com/2017/12/25/sports/football/pittsburgh-steelers-playoffs.html',
    'http://www.dailymail.co.uk/wires/pa/article-5212545/Pittsburgh-Steelers-enjoy-Christmas-cheer.html',
    'https://www.washingtonpost.com/sports/redskins/steelers-clinch-first-round-bye-with-34-6-win-over-texans/2017/12/25/cef9456c-e9d5-11e7-956e-baea358f9725_story.html?utm_term=.f98fe018784d'
])
## science
add_article(Category.science, Topic.unspecific, Event.possible_meteor_lights_up_night_sky_in_new_england, [
    'https://www.nytimes.com/aponline/2017/12/27/us/ap-us-new-england-fireball.html',
    'https://www.rt.com/usa/414380-dazzling-meteor-new-england/',
    'https://www.washingtonpost.com/national/health-science/fireball-lights-up-social-media-evening-sky-in-new-england/2017/12/27/d6348a38-eb0d-11e7-956e-baea358f9725_story.html?utm_term=.e120302926af',
    'http://www.cetusnews.com/news/Possible-meteor-lights-up-night-sky-in-New-England.r1o8Lm-QG.html'
])
add_article(Category.science, Topic.unspecific, Event.elon_musk_reveals_red_tesla_roadster_bound_for_mars, [
    'https://www.usatoday.com/story/tech/nation-now/2017/12/27/spacex-red-tesla-roadster-bound-mars/983669001/',
    'https://www.rt.com/news/411715-spacex-tesla-mars-falcon-heavy/',
    'http://www.dailymail.co.uk/sciencetech/article-5216485/Elon-Musk-send-car-Mars.html',
    'http://www.dailymail.co.uk/news/article-5139761/Elon-Musk-send-Tesla-Roadster-Mars.html',
    'http://www.dailymail.co.uk/sciencetech/article-5238433/Elon-Musk-SpaceX-launch-Falcon-Heavy-rocket-month.html',
    'http://money.cnn.com/2017/12/02/technology/elon-musk-spacex-falcon-heavy-launch/index.html',
    'https://www.fool.com/investing/2017/12/17/elon-musk-is-sending-a-tesla-to-mars.aspx',
    'https://www.cbsnews.com/news/elon-musk-tesla-will-launch-roadster-to-orbit-mars/'

])
add_article(Category.science, Topic.unspecific, Event.smoke_rings_spotted_in_the_ocean_from_space, [
    'https://news.liverpool.ac.uk/2017/12/11/smoke-rings-spotted-in-the-ocean-from-space/',
    'https://www.ndtv.com/world-news/smoke-rings-spotted-in-the-ocean-from-space-1792708',
    'http://www.dailymail.co.uk/sciencetech/article-5168793/The-Hyperloop-sea-Smoke-rings-spotted.html',
    'https://tecake.in/scientists-spotted-smoke-rings-satellite-surprising',
    'http://indianexpress.com/article/technology/science/smoke-rings-spotted-in-the-ocean-from-space-5004094/'
])

# 30.12.2017 - 31.12.
## world
add_article(Category.world, Topic.unspecific,
            Event.north_korea_received_oil_from_russia_in_violation_of_un_sanctions_report, [
            'http://www.foxnews.com/world/2017/12/30/north-korea-received-oil-from-russia-in-violation-un-sanctions-report.html',
            'http://edition.cnn.com/2017/12/28/politics/president-donald-trump-china-north-korea-oil/index.html',
            'http://edition.cnn.com/videos/world/2017/12/29/ship-seized-selling-oil-to-nkorea.cnn',
            'https://www.nytimes.com/2017/12/29/world/asia/south-korea-ship-seized.html',
            'https://www.npr.org/sections/thetwo-way/2017/12/29/574508075/south-korea-seizes-ship-suspected-of-at-sea-oil-transfer-to-benefit-north-korea',
            'https://www.thesun.co.uk/news/5222989/china-secretly-transferring-oil-kim-jong-un-ships/',
            'https://www.rt.com/usa/414485-caught-red-handed-china/',
            'https://www.rt.com/newsline/414356-china-korea-sanctions-oil/',
            'https://www.washingtonpost.com/business/china-promises-to-deal-seriously-with-sanctions-violators/2018/01/05/fa7f96ee-f1fc-11e7-95e3-eff284e71c8d_story.html?utm_term=.07edf6896eb5',
            'https://www.washingtonpost.com/world/asia_pacific/trump-said-china-was-caught-red-handed-selling-oil-to-north-korea-beijing-denies-it-did-anything-wrong/2017/12/29/89bc3a22-ec73-11e7-891f-e7a3c60a93de_story.html?utm_term=.fb71d2e88053',
            'http://www.chinadaily.com.cn/newsrepublic/2017-12/29/content_35412308.htm'

            ])
add_article(Category.world, Topic.unspecific,
            Event.egypts_mohammed_morsi_sentenced_to_3_years_in_prison_for_insulting_judiciary, [
            'https://www.cbsnews.com/news/egypts-mohammed-morsi-sentenced-to-3-years-in-prison-for-insulting-judiciary/',
            'http://www.dpa-international.com/topic/egypts-morsi-sentenced-3-years-jail-insulting-judiciary-171230-99-450945',
            'http://www.dailymail.co.uk/wires/afp/article-5222793/Egypts-Morsi-sentenced-three-years-prison.html'
            ])
add_article(Category.world, Topic.unspecific,
            Event.berlin_sets_up_new_years_eve_safe_zone_for_women_amid_sexual_assault_concerns, [
            'https://www.washingtonpost.com/news/worldviews/wp/2017/12/30/berlin-sets-up-new-years-eve-safe-zone-for-women-amid-sexual-assault-concerns/?utm_term=.c6b140b9b058',
            'https://www.nytimes.com/aponline/2017/12/30/world/europe/ap-eu-germany-new-year-sexual-assaults.html',
            'https://www.nytimes.com/2017/12/29/world/europe/germans-will-ring-in-new-year-with-extra-security-especially-for-women.html',
            'https://www.npr.org/sections/thetwo-way/2017/12/31/574778306/germany-takes-steps-to-guard-women-against-sexual-assault-as-they-ring-in-new-ye',
            'https://www.thesun.co.uk/news/5232365/berlin-new-year-party-safe-zones-women-sex-attacks/',
            'http://www.dailymail.co.uk/wires/reuters/article-5221423/Berlin-New-Years-Eve-party-sets-safe-zone-women.html',
            'https://www.rt.com/news/414587-berlin-women-safety-zone/',
            'https://www.washingtonpost.com/world/europe/german-police-union-chief-slams-nye-safe-zone-for-women/2017/12/30/b801eb92-ed64-11e7-956e-baea358f9725_story.html?utm_term=.5d3beb67aafd'
            ])

## business, [])
add_article(Category.business, Topic.unspecific, Event.police_arrest_alleged_nigerian_prince_email_scammer_in_louisiana,
            [
                'https://www.usatoday.com/story/news/nation-now/2017/12/30/nigerian-prince-email-scammer-louisiana/992073001/',
                'http://www.dailymail.co.uk/news/article-5223953/Louisiana-man-67-middle-man-Nigerian-prince-scam.html',
                'https://www.rt.com/usa/414640-nigerian-prince-arrested-louisiana/',
                'https://www.washingtonpost.com/858b258e-edd2-11e7-956e-baea358f9725_story.html?utm_term=.de12c2f6a40e'
            ])
add_article(Category.business, Topic.unspecific,
            Event.digital_currency_ripple_soars_nearly_56_percent_becomes_second_largest_cryptocurrency_by_market_cap,
            [
                'https://www.cnbc.com/2017/12/29/ripple-soars-becomes-second-biggest-cryptocurrency-by-market-cap.html'
            ])
add_article(Category.business, Topic.unspecific, Event.goldman_sachs_feels_tax_bills_burn_with_5b_charge, [
        'https://www.usnews.com/news/economy/articles/2017-12-29/goldman-sachs-feels-tax-bills-burn-with-5b-charge',
        'https://www.nytimes.com/2017/12/29/business/goldman-sachs-taxes.html',
        'https://www.bloomberg.com/news/articles/2017-12-29/goldman-sachs-takes-one-time-5-billion-hit-from-u-s-tax-bill',
        'http://money.cnn.com/2017/12/29/news/goldman-sachs-tax/index.html',
        'https://www.nytimes.com/2017/12/29/business/goldman-sachs-taxes.html',
        'http://www.dailymail.co.uk/news/article-5220701/Goldman-Sachs-expects-5-billion-hit-tax-overhaul-4Q.html',
        'https://www.washingtonpost.com/business/goldman-sachs-expects-5-billion-hit-from-tax-overhaul-in-4q/2017/12/29/f2afddb4-ec90-11e7-956e-baea358f9725_story.html?utm_term=.c0b45784b735',
        'https://www.washingtonpost.com/business/goldman-sachs-citing-recent-tax-overhaul-in-us-expects-to-take-a-5-billion-hit-to-profits-this-quarter/2017/12/29/562ce198-ec8c-11e7-956e-baea358f9725_story.html?utm_term=.893884d04aa4'
])
## technology, [])
add_article(Category.technology, Topic.unspecific, Event.chicagos_apple_store_has_a_falling_ice_problem, [
        'http://fortune.com/2017/12/29/apple-store-chicago-snow-ice/',
        'http://www.dailymail.co.uk/sciencetech/article-5233443/Apple-blames-roof-warming-software-icy-Chicago-store.html'
])
## entertainment, [])
add_article(Category.entertainment, Topic.unspecific,
            Event.tamar_braxton_slams_ex_vincent_herbert_for_having_a_baby_with_other_woman, [])

add_article(Category.entertainment, Topic.unspecific,
            Event.asking_if_kendall_jenner_is_pregnant_is_the_wrong_response_to_her_latest_selfie, [
        'https://www.bustle.com/p/asking-if-kendall-jenner-is-pregnant-is-the-wrong-response-to-her-latest-selfie-7739187',
     #   'https://www.msn.com/en-us/tv/celebrity/check-out-the-pic-that-has-fans-asking-if-kendall-jenner-is-pregnant/ar-BBHwtr2',
        'http://www.mirror.co.uk/3am/celebrity-news/kendall-jenner-pregnant-too-fans-11769536',
        'https://www.elitedaily.com/p/tweets-about-kendall-jenners-instagram-pregnancy-picture-are-completely-uncalled-for-7739109'
            ])
add_article(Category.entertainment, Topic.unspecific,
            Event.black_mirror_uss_callister_how_the_shatner_impression_surprise_cameo_and_flawless_production_happened,
            [
                'http://www.indiewire.com/2017/12/black-mirror-uss-callister-behind-the-scenes-aaron-paul-shatner-spoilers-1201912123/',
                'http://news.stamfordglobal.com/daily/black-mirror-uss-callister-how-the-shatner-impression-surprise-cameo-and-flawless-production-happened-indiewire'
            ])
## sport, [])

# not very sure what this event is....
add_article(Category.sports, Topic.unspecific,
            Event.uscs_cotton_bowl_loss_was_a_wake_up_call_and_not_just_for_sam_darnold, [])


add_article(Category.sports, Topic.unspecific, Event.packers_sign_center_linsley_to_contract_extension, [
    'https://www.foxsports.com/wisconsin/story/green-bay-packers-corey-linsley-contract-extension-123017',
])

## science, [])
add_article(Category.science, Topic.unspecific,
            Event.the_broken_berg_stunning_nasa_image_captures_newly_created_iceberg_cracking_into_20_pieces, [
            'http://www.ibtimes.co.uk/shattered-antarctic-iceberg-four-times-size-manhattan-captured-stunning-new-image-1653217',
            'http://www.dailymail.co.uk/sciencetech/article-5221735/NASA-captures-newly-created-iceberg-cracking-pieces.html'
            ])

# there are actually two event bus happened on the same days about the same thing
add_article(Category.science, Topic.unspecific, Event.russian_space_experts_regain_control_of_1st_angola_satellite, [
    'http://abcnews.go.com/Technology/wireStory/russian-space-experts-regain-control-1st-angola-satellite-52044233',
    'http://www.foxnews.com/world/2017/12/29/russian-space-experts-regain-control-1st-angola-satellite.html',
    'https://timesofindia.indiatimes.com/home/science/russian-space-experts-regain-control-of-1st-angola-satellite/articleshow/62298457.cms',
    'https://www.rt.com/newsline/414349-angolan-satellite-contact-lost/',
    'https://www.rt.com/newsline/414511-russia-contact-angola-satellite/',
    'https://www.rt.com/on-air/414286-angola-satellite-launch-baikonur/',
    'https://timesofindia.indiatimes.com/home/science/russian-space-experts-regain-control-of-1st-angola-satellite/articleshow/62298457.cms'
])
add_article(Category.science, Topic.unspecific,
            Event.january_will_bring_two_supermoons_a_blue_moon_and_a_total_lunar_eclipse, [
        'https://qz.com/1168320/how-to-watch-two-supermoons-a-blue-moon-and-a-total-lunar-eclipse-this-january/',
        'https://www.thesun.co.uk/tech/5232103/blue-moon-supermoon-song-lyrics-manchester-city/',
        'http://www.dailymail.co.uk/news/article-5227497/Cities-United-States-lit-supermoon.html',
        'https://www.rt.com/news/414549-first-supermoon-january-2018/',
        'https://www.washingtonpost.com/national/health-science/sky-watch-january-is-packed-with-action/2017/12/30/d9621528-ecab-11e7-b698-91d4e35920a3_story.html?utm_term=.868357587b06'
            ])

# 01.01.2018
## world
add_article(Category.world, Topic.unspecific, Event.kim_jong_un_offers_rare_olive_branch_to_south_korea, [
    'http://edition.cnn.com/2017/12/31/asia/kim-jong-un-new-year-address-nuclear/index.html',
    'https://storia.me/en/@WeirdAndWonderful/kim-jong-un-offers-2yo7ba',
    'https://www.nytimes.com/reuters/2017/12/31/world/asia/31reuters-northkorea-missiles-kimjongun.html',
    'http://www.dailymail.co.uk/news/article-5230517/Trump-Kim-My-nuke-button-bigger-talks-dismissed.html',
    'http://www.chinadaily.com.cn/2017-11/07/content_34243617.htm'
])
add_article(Category.world, Topic.unspecific, Event.new_york_family_of_5_among_12_killed_in_costa_rica_plane_crash, [
    'https://www.thedenverchannel.com/news/national/new-york-family-of-5-among-12-killed-in-costa-rica-plane-crash',
    'https://www.huffingtonpost.com/entry/costa-rica-plane-crash_us_5a49474ee4b06d1621b9a206',
    'http://edition.cnn.com/2017/12/31/americas/costa-rica-plane-crash/index.html',
    'http://edition.cnn.com/2018/01/01/americas/costa-rica-plane-crash-family-identified/index.html',
    'https://www.nytimes.com/2018/01/01/world/americas/costa-rica-plane-crash.html',
    'https://www.npr.org/templates/search/index.php?searchinput=Costa+Rica+plane+crash',
    'http://www.dailymail.co.uk/wires/pa/article-5225115/Plane-12-believed-aboard-crashes-Costa-Rica.html',
    'http://www.dailymail.co.uk/wires/reuters/article-5225261/At-12-die-Costa-Rica-plane-crash-government-department.html',
    'https://www.rt.com/news/414714-costa-rica-plane-crash-guanacaste/',
    'http://www.thehindu.com/news/international/10-americans-among-12-killed-in-costa-rica-plane-crash/article22342043.ece',
    'http://www.thehindu.com/todays-paper/tp-international/10-americans-2-pilots-killed-in-costa-rica-air-crash/article22348898.ece',
    'http://www.chinadaily.com.cn/kindle/2018-01/02/content_35425601.htm',
    'https://www.washingtonpost.com/world/the_americas/10-us-citizens-2-locals-killed-in-costa-rica-plane-crash/2017/12/31/0e6191a4-ee87-11e7-95e3-eff284e71c8d_story.html?utm_term=.c55fb5b8c542',
    'https://www.washingtonpost.com/world/the_americas/plane-with-12-believed-aboard-crashes-in-costa-rica/2017/12/31/94038cdc-ee68-11e7-95e3-eff284e71c8d_story.html?utm_term=.e52f8203b852'
])
add_article(Category.world, Topic.unspecific, Event.israel_indicts_palestinian_teenage_girl_who_punched_soldier_army,
            [
                'https://www.reuters.com/article/us-israel-palestinians-teen/israel-indicts-palestinian-teenage-girl-who-punched-soldier-army-idUSKBN1EQ13Y',
                'https://www.nytimes.com/reuters/2018/01/01/world/middleeast/01reuters-israel-palestinians-teen.html',
                'https://www.nytimes.com/aponline/2018/01/01/world/middleeast/ap-ml-israel-palestinians.html',
                'http://www.dailymail.co.uk/wires/ap/article-5226509/Israel-indicts-teenage-Palestinian-girl-slapped-soldiers.html',
                'http://www.dailymail.co.uk/wires/reuters/article-5226607/Israel-indicts-Palestinian-teenage-girl-punched-soldier-army.html',
                'https://www.washingtonpost.com/national/israel-indicts-teenage-palestinian-girl-who-slapped-soldiers/2018/01/01/3e137e9e-ef0e-11e7-95e3-eff284e71c8d_story.html?utm_term=.c54d9ffdebff',
                'https://www.washingtonpost.com/national/palestinian-girl-who-hit-soldiers-could-get-long-sentence/2018/01/03/40113f18-f0c8-11e7-95e3-eff284e71c8d_story.html?utm_term=.32cc2e08143c'
            ])
add_article(Category.world, Topic.unspecific, Event.thousands_flee_fireworks_explosion_at_australia_beach, [
    'http://www.bbc.com/news/world-australia-42531996',
    'https://www.rt.com/news/414726-australia-beach-fireworks-injured/',
    'http://www.straitstimes.com/asia/australianz/2-injured-thousands-flee-as-fireworks-malfunction-at-australian-beach',
    'http://www.news.com.au/national/nsw-act/news/two-injured-thousands-evacuated-following-new-years-eve-fireworks-disaster-at-terrigal-beach/news-story/3f087a3867cf26a0ca90544cb180943b',
    'https://www.ctvnews.ca/world/thousands-flee-after-beach-fireworks-celebration-turns-to-chaos-1.3741340'
])
##_business
add_article(Category.business, Topic.unspecific,
            Event.time_travel_hawaiian_airlines_flight_takes_off_in_2018_lands_in_2017, [
        'http://kdvr.com/2018/01/01/time-travel-hawaiian-airlines-flight-takes-off-in-2018-lands-in-2017/',
        'http://www.popularmechanics.com/flight/airlines/a14524197/hawaiian-air-time-travel/',
        'http://www.hawaiinewsnow.com/story/37170223/passengers-on-a-hawaiian-airlines-flight-got-to-ring-in-2018-twice',
        'http://dfw.cbslocal.com/2018/01/02/time-travel-flight-2017-2018-auckland-hawaii/',
        'https://www.rt.com/news/414702-hawaiian-airlines-time-travel-auckland/',
        'https://www.npr.org/2018/01/01/574932110/hawaiian-airlines-flight-takes-off-in-2018-but-lands-in-2017'
            ])
add_article(Category.business, Topic.unspecific, Event.how_a_small_bird_managed_to_take_over_a_delta_flight, [
    'https://www.washingtonpost.com/news/dr-gridlock/wp/2017/12/31/how-a-small-bird-managed-to-take-over-a-delta-flight/?utm_term=.1ab4164ae5ad',
    'http://www.sfgate.com/news/article/A-small-bird-managed-to-take-over-a-Delta-flight-12464765.php',
    'https://www.denverpost.com/2018/01/01/delta-flight-detroit-atlanta-taken-over-by-bird/',
    'http://www.detroitnews.com/story/news/local/detroit-city/2017/12/30/bird-delta-flight-return-detroit/109033712/'
])
##_technology
add_article(Category.technology, Topic.unspecific,
            Event.samsung_acknowledges_galaxy_note_8_battery_problems_says_very_few_phones_are_affected, [
        'http://bgr.com/2018/01/01/galaxy-note-8-battery-drain-issue/',
            ])
## entertainment
add_article(Category.entertainment, Topic.unspecific, Event.jessica_alba_and_cash_warren_welcome_son_hayes_alba, [
    'http://people.com/babies/jessica-alba-cash-warren-welcome-third-child-son-hayes/',
    'http://www.india.com/showbiz/jessica-alba-gives-birth-to-baby-boy-2823794/',
    'https://www.thesun.co.uk/tvandshowbiz/5247896/jessica-alba-gives-birth-to-a-baby-boy-and-his-name-fits-with-her-daughters-haven-and-honor/'
])
add_article(Category.entertainment, Topic.unspecific, Event.sun_fun_flowers_as_129th_rose_parade_rolls_in_california,
            [
                'http://usa.chinadaily.com.cn/a/201801/02/WS5a4af1f1a31008cf16da49bb.html',
                'https://www.timesunion.com/entertainment/article/Flowers-and-sunshine-greet-thousands-for-129th-12465519.php',
                'http://www.thedailytimes.com/entertainment/flowers-and-sunshine-greet-thousands-for-th-rose-parade/article_159d3bf1-c0e8-5914-a11b-2ea2a5804cdb.html',
                'http://www.telegram.com/news/20180101/sun-fun-flowers-as-129th-rose-parade-rolls-in-california',
                'http://www.thedailytimes.com/entertainment/flowers-and-sunshine-greet-thousands-for-th-rose-parade/article_159d3bf1-c0e8-5914-a11b-2ea2a5804cdb.html',
                'http://www.telegram.com/news/20180101/sun-fun-flowers-as-129th-rose-parade-rolls-in-california'
            ])
## sport
add_article(Category.sports, Topic.unspecific, Event.chicago_bears_fire_coach_john_fox_after_5_11_season, [
    'http://www.nfl.com/news/story/0ap3000000901544/article/chicago-bears-fire-coach-john-fox-after-511-season',
    'https://www.foxsports.com/nfl/story/chicago-bears-fire-coach-john-fox-after-5-11-season-010118',
    'https://www.washingtonpost.com/sports/redskins/chicago-bears-fire-coach-john-fox-after-5-11-season/2018/01/01/8846af80-ef14-11e7-95e3-eff284e71c8d_story.html?utm_term=.d264a21b24bb',
   # 'http://www.nydailynews.com/newswires/sports/chicago-bears-fire-coach-john-fox-5-11-season-article-1.3731136'
])
add_article(Category.sports, Topic.unspecific,
            Event.bruce_arians_emotional_in_announcing_retirement_from_coaching_cites_family, [
        'http://abcnews.go.com/Sports/bruce-arians-emotional-announcing-retirement-coaching-cites-family/story?id=52085405',
        'https://www.nytimes.com/reuters/2018/01/02/sports/football/02reuters-football-nfl-ari-palmer.html',
        'http://www.dailymail.co.uk/sport/nfl/article-5227259/Cardinals-Arians-makes-tearful-retirement-announcement.html',
        'https://www.washingtonpost.com/sports/redskins/cardinals-qb-carson-palmer-retires-after-15-nfl-seasons/2018/01/02/3db31b54-f020-11e7-95e3-eff284e71c8d_story.html?utm_term=.f6c7174faeaf',
        'https://www.washingtonpost.com/sports/redskins/arians-announces-retirement-after-5-seasons-in-arizona/2018/01/01/6f32f7cc-ef20-11e7-95e3-eff284e71c8d_story.html?utm_term=.826d8ad68a7e'
            ])
##_science
add_article(Category.science, Topic.unspecific, Event.china_promises_the_moon, [
    'https://spectrum.ieee.org/aerospace/robotic-exploration/china-promises-the-moon',
    'https://www.theguardian.com/science/2017/dec/31/china-mission-to-far-side-of-the-moon-space-discovery',
    'https://sciexaminer.com/news/space/china-launch-lunar-mission-far-side-moons-surface-3220.html',
    'https://sputniknews.com/science/201712311060451579-china-change4-moon-landing/',
    'http://www.dailymail.co.uk/sciencetech/article-5226529/China-set-2018-mission-far-moon.html'
])
add_article(Category.science, Topic.unspecific,
            Event.chinas_tiangong_1_space_station_is_out_of_control_and_will_soon_fall_to_earth, [
        'http://www.jreasn.com/chinas-tiangong-1-space-station-is-out-of-control-and-will-soon-fall-to-earth/',
        'https://www.theverge.com/2017/12/31/16830890/chinese-space-station-tiangong-1-debris-falling-to-earth',
        'http://www.independent.co.uk/life-style/gadgets-and-tech/news/china-space-station-tiangong-1-out-of-control-earth-danger-agency-latest-a8148416.html',
        'https://www.theguardian.com/science/2017/oct/13/tiangong-1-chinese-space-station-will-crash-to-earth-within-months',
        'https://www.express.co.uk/news/science/902498/tiangong-1-when-will-chinese-space-station-crash-into-earth'
            ])
add_article(Category.science, Topic.unspecific, Event.astronauts_identify_unknown_microbes_in_space_for_first_time, [
    'https://www.ndtv.com/world-news/astronauts-identify-unknown-microbes-in-space-for-first-time-1794572',
    'http://www.insightsonindia.com/2018/01/03/insights-daily-current-affairs-03-january-2018/astronauts-identify-unknown-microbes-in-space-for-first-time/',
    'https://www.sciencealert.com/nasa-identified-unknown-microbes-in-space-first-time-international-space-station',
    'https://www.nasa.gov/feature/genes-in-space-3-successfully-identifies-unknown-microbes-in-space'
])

add_article(Category.world, Topic.legancy, Event.china_boy_well, [
    "http://www.bbc.com/news/world-asia-china-37906226",
    "http://www.bbc.com/news/world-asia-china-37946716",
    "http://www.dailymail.co.uk/news/article-3916560/Dramatic-footage-shows-rescuers-using-eighty-diggers-save-boy-fell-130ft-deep-picking-cabbages-Chinese-farm.html",
    "http://www.dailymail.co.uk/news/article-3923808/Mystery-Chinese-boy-fell-deep-massive-rescue-operation-involving-80-diggers-chute-empty.html"
])

add_article(Category.sports, Topic.legancy, Event.cubs_win_championship, [
    "https://www.theguardian.com/sport/2016/nov/03/world-series-game-7-chicago-cubs-cleveland-indians-mlb",
    "https://www.washingtonpost.com/sports/believe-it-chicago-cubs-win-classic-game-7-to-win-first-world-series-since-1908/2016/11/03/99cfc9c2-a0b3-11e6-a44d-cc2898cfab06_story.html",
    "https://www.thesun.co.uk/sport/othersports/2106710/chicago-cubs-win-world-series-hillary-clinton-bill-murray-and-barack-obama-lead-celebrations-as-cubs-end-108-year-curse/",
    "http://nypost.com/2016/11/03/cubs-end-drought-in-chaotic-epic-world-series-finale/",
    "http://www.bbc.com/sport/baseball/37857919",
    "https://www.washingtonpost.com/sports/nationals/you-knew-it-couldnt-come-easy-but-the-cubs-are-world-series-champions/2016/11/03/a4487ade-a0b3-11e6-a44d-cc2898cfab06_story.html",
    "http://www.telegraph.co.uk/baseball/2016/11/03/chicago-cubs-break-108-year-curse-of-the-billy-goat-winning-worl/",
    "http://www.mirror.co.uk/sport/other-sports/american-sports/chicago-cubs-win-world-series-9185077",
    "http://www.standard.co.uk/sport/other-sports/chicago-cubs-win-world-series-to-end-108year-curse-and-earn-invite-from-barack-obama-a3386411.html",
    "http://www.independent.co.uk/sport/us-sport/major-league-baseball/world-series-chicago-cubs-cleveland-indians-108-year-title-drought-a7394706.html",
    "http://www.independent.co.uk/sport/us-sport/major-league-baseball/chicago-cubs-fans-celebrate-world-series-title-a7394736.html",
    "http://www.dailymail.co.uk/news/article-3899956/Chicago-Cubs-win-World-Series-epic-Game-7-showdown-Cleveland.html",
    "http://www.usatoday.com/story/sports/ftw/2016/11/03/sports-world-reacts-to-the-chicago-cubs-winning-their-first-world-series-since-1908/93225730/"
])

add_article(Category.sports, Topic.legancy, Event.f1_crash, [
    "http://www.dailymail.co.uk/sport/formulaone/article-3932890/Max-Verstappen-amazes-Red-Bull-principal-Christian-Horner-performance-Brazil-witnessed-special.html",
    "https://www.thesun.co.uk/sport/2177804/felipe-massa-retires-f1-legend-makes-a-very-emotional-farewell-after-crashing-in-his-last-home-race-in-brazil/",
    "http://www.dailymail.co.uk/sport/sportsnews/article-3934424/Formula-One-star-Max-Verstappen-shows-nerves-steel-avoid-accident.html",
    "http://www.mirror.co.uk/sport/formula-1/red-bull-boss-christian-horner-9254708",
    "http://www.dailymail.co.uk/sport/formulaone/article-3932386/F1-legend-Felipe-Massa-makes-emotional-farewell-crashing-Brazil-Grand-Prix-Interlagos.html",
    "https://www.thesun.co.uk/sport/2177105/lewis-hamilton-wins-the-brazilian-grand-prix-after-two-red-flags/",
    "http://www.standard.co.uk/sport/brazilian-grand-prix-redflagged-after-dramatic-kimi-raikkonen-crash-a3394411.html",
    "http://www.telegraph.co.uk/formula-1/2016/11/13/max-verstappen-even-stuns-his-dad-by-storming-home-into-third-pl/",
    "http://www.usatoday.com/story/sports/motor/formula1/2016/11/13/brazils-massa-crashes-but-gets-warm-farewell-at-home-gp/93771246/",
    "http://www.dailymail.co.uk/sport/formulaone/article-3932252/Brazilian-Grand-Prix-thrown-chaos-Kimi-Raikkonen-accident-brings-red-flag-Sebastian-Vettel-fumes-stupid-conditions-mad.html",
    "http://www.express.co.uk/sport/f1-autosport/731858/Max-Verstappen-avoids-crash-Kimi-Raikkonen-Brazilian-Grand-Prix-wet",
    "http://www.mirror.co.uk/sport/formula-1/brazilian-f1-grand-prix-riddled-9253267"
])

add_article(Category.world, Topic.legancy, Event.croydon_tram_trash, [
    "http://www.standard.co.uk/news/transport/croydon-tram-derailment-people-trapped-after-tram-overturns-in-at-sandilands-a3390796.html",
    "http://www.nytimes.com/2016/11/10/world/europe/tram-derails-croydon-london.html",
    "http://www.dailymail.co.uk/wires/pa/article-3919284/Five-trapped-40-injured-tram-overturns-tunnel.html",
    "https://www.theguardian.com/uk-news/2016/nov/09/croydon-tram-crash-kills-at-least-seven-and-injures-more-than-50",
    "http://www.mirror.co.uk/news/uk-news/huge-rescue-operation-sandilands-station-9226276",
    "http://www.telegraph.co.uk/news/2016/11/10/croydon-tram-crash-police-check-drivers-mobile-phone-records/",
    "http://www.express.co.uk/news/uk/730639/Croydon-tram-crash-carnage-survivor-derailment-seven-dead",
    "http://www.usatoday.com/story/news/2016/11/09/least-7-killed-tram-accident-south-london/93549248/",
    "http://www.bbc.com/news/uk-england-london-37919658",
    "http://nypost.com/2016/11/09/several-dead-and-dozens-injured-after-tram-overturns-in-london/",
    "http://www.independent.co.uk/news/uk/home-news/five-trapped-40-injured-after-tram-overturns-south-london-croydon-a7406496.html"
])

add_article(Category.world, Topic.legancy, Event.Benghazi_US_consulate_attack, [
    "http://www.telegraph.co.uk/news/2016/11/10/taliban-attack-german-consulate-in-northern-afghan-city-of-mazar/",
    "http://www.express.co.uk/news/world/731052/German-consulate-explosion-gunfire-Afghanistan",
    "https://www.theguardian.com/world/2016/nov/10/taliban-attack-german-consulate-mazar-i-sharif-afghanistan-nato-airstrikes-kunduz",
    "http://www.bbc.com/news/world-asia-37944115",
    "http://www.nytimes.com/2016/11/11/world/asia/taliban-strike-german-consulate-in-afghan-city-of-mazar-i-sharif.html?_r=0",
    "http://www.independent.co.uk/news/world/middle-east/german-consulate-afghanistan-attacked-bomb-suicide-taliban-revenge-mazar-i-sharif-kunduz-attack-two-a7410746.html",
    "https://www.thesun.co.uk/news/2162467/taliban-suicide-bomber-truck-german-consulate-afghanistan-killing-two/amp/",
    "http://www.nytimes.com/2016/11/11/world/asia/taliban-strike-german-consulate-in-afghan-city-of-mazar-i-sharif.html?_r=0",
    "http://www.bbc.com/news/world-asia-37944115"
])

add_article(Category.world, Topic.legancy, Event.north_Korea_Launches_satellite, [
    'http://edition.cnn.com/2016/02/07/asia/gallery/north-korea-missile-launch/index.html',
    'http://www.nytimes.com/2013/01/31/world/asia/on-3d-try-south-korea-launches-satellite-into-orbit.html',
    'https://www.npr.org/2015/09/15/440443821/north-korea-says-its-ready-to-launch-satellites-aboard-rockets',
    'http://www.dailymail.co.uk/wires/afp/article-4322652/Japan-launches-latest-North-Korea-spy-satellite.html',
    'http://www.thehindu.com/news/international/north-korea-to-launch-satellites-to-mark-party-anniversary/article7654457.ece',
    'http://www.chinadaily.com.cn/world/2016-02/07/content_23426008.htm',
    'https://www.washingtonpost.com/world/north-korea-launches-satellite-sparks-fears-about-long-range-missile-program/2016/02/06/0b6084e5-afd1-42ec-8170-280883f23240_story.html'
])

add_article(Category.world, Topic.legancy, Event.NewYearsEveSexualAssaultsGermany, [
    'http://www.chinadaily.com.cn/opinion/2016-01/11/content_23017934.htm',
    'http://www.dailymail.co.uk/news/article-3411720/A-staggering-359-sexual-assaults-migrants-reported-Cologne-police-New-Year-s-Eve-mob-went-rampage-causing-821-complaints.html',
    'https://www.npr.org/2016/01/06/462114345/migrants-in-germany-accused-of-coordinated-sexual-assaults',
    'https://www.npr.org/sections/parallels/2016/01/05/462059765/mass-sexual-assaults-in-cologne-germany-renew-tensions-over-migrants'
])

add_article(Category.world, Topic.legancy, Event.truck_attack_in_nice, [
    'http://edition.cnn.com/2016/07/14/europe/nice-france-truck/index.html',
    'http://edition.cnn.com/2016/07/14/world/nice-attack-witness-accounts/index.html',
    'https://www.nytimes.com/2016/07/16/world/europe/truck-attack-nice-france.html',
    'https://www.nytimes.com/2016/07/15/world/europe/nice-france-truck-bastille-day.html',
    'https://www.npr.org/2016/07/14/486097589/more-than-70-people-killed-in-truck-attack-in-nice-france',
    'https://www.npr.org/2016/07/14/486095754/president-obama-briefed-on-truck-attack-in-nice-france',
    'https://www.thesun.co.uk/news/1447619/at-least-77-dead-and-100-injured-as-lorry-crashes-into-crowd-of-revellers-celebrating-in-france-terror-attack/',
    'http://www.dailymail.co.uk/wires/afp/article-3692450/Tunisians-Algerians-dead-Nice-attack.html',
    'http://www.thehindu.com/news/84-killed-in-France-as-terror-truck-ploughs-through-crowd/article14491015.ece',
    'http://www.thehindu.com/news/international/Truck-attacker-in-Nice-kills-84-celebrating-Bastille-Day/article14490871.ece',
    'http://www.chinadaily.com.cn/world/2016-08/05/content_26355611.htm',
    'http://europe.chinadaily.com.cn/world/2016-07/15/content_26095924.htm',
    'http://usa.chinadaily.com.cn/epaper/2016-07/15/content_26104748.htm'
])

add_article(Category.world, Topic.legancy, Event.harambe, [
    'http://edition.cnn.com/2016/03/18/health/seaworld-blackfish-effect-circuses-zoos/index.html',
    'https://www.npr.org/sections/thetwo-way/2016/05/29/479919582/gorilla-killed-to-save-boy-at-cincinnati-zoo',
    'https://www.thesun.co.uk/news/1230550/hear-the-dramatic-moment-little-isiahs-mum-calls-for-help-after-her-son-falls-into-gorilla-enclosure-at-zoo/',
    'http://www.dailymail.co.uk/news/article-3614480/Small-child-falls-gorilla-enclosure-zoo.html',
    'http://www.thehindu.com/news/international/Ohio-zoo-kills-gorilla-to-protect-small-child-in-enclosure/article14347705.ece',
    'http://usa.chinadaily.com.cn/world/2016-05/30/content_25527063.htm',
    'https://www.washingtonpost.com/news/post-nation/wp/2016/05/29/it-could-have-been-very-bad-gorilla-killed-after-boy-falls-into-cincinnati-zoo-exhibit/?tid=a_inl',
    'https://www.rt.com/news/344746-cincinnati-zoo-gorilla-killed/'
])

add_article(Category.world, Topic.legancy, Event.boko_haram_21_schoolgirls_freed, [
    'http://edition.cnn.com/2016/10/13/africa/nigeria-chibok-girls-released/index.html',
    'https://www.nytimes.com/2016/10/14/world/africa/boko-haram-nigeria.html',
    'https://www.npr.org/sections/thetwo-way/2016/10/13/497803083/nigeria-says-21-schoolgirls-abducted-by-boko-haram-have-been-released',
    'https://www.thesun.co.uk/news/1971191/isis-splinter-group-boko-haram-release-21-kidnapped-nigerian-schoolgirls-in-exchange-for-four-jailed-militants/',
    'http://www.dailymail.co.uk/wires/afp/article-3836078/Boko-Haram-releases-21-Chibok-girls-Nigerian-official.html',
    'http://www.thehindu.com/news/international/21-abducted-Chibok-schoolgirls-freed/article15513701.ece',
    'http://www.thehindu.com/news/international/21-abducted-Chibok-schoolgirls-freed-in-Nigeria/article16070198.ece',
    'http://africa.chinadaily.com.cn/world/2017-05/09/content_29261603.htm',
    'https://www.washingtonpost.com/world/boko-haram-militants-free-21-captive-chibok-schoolgirls-amid-talks-with-nigeria/2016/10/13/9e94610a-0ed3-4a26-96f1-6c5d7cccfdcd_story.html'
])

add_article(Category.world, Topic.legancy, Event.panama_papers, [
    'http://edition.cnn.com/2016/04/04/opinions/panama-papers-ghitis/index.html',
    'http://edition.cnn.com/2016/04/04/world/panama-papers-explainer/index.html',
    'https://www.nytimes.com/2017/11/06/world/bank-of-utah-leonid-mikhelson.html',
    'https://www.npr.org/sections/thetwo-way/2016/04/04/472985787/heres-what-you-need-to-know-so-far-about-panama-papers',
    'https://www.npr.org/sections/parallels/2016/05/04/476745041/panama-rises-despite-dents-to-its-reputation-from-papers-leaks',
    'http://www.dailymail.co.uk/wires/afp/article-3523948/Big-China-presence-Panama-Papers-law-firm.html',
    'http://www.dailymail.co.uk/wires/afp/article-3522970/African-leaders-relatives-named-Panama-Papers.html',
    'http://www.dailymail.co.uk/wires/afp/article-3523775/Panama-Papers-revelations-trigger-global-probes.html',
    'https://www.rt.com/news/338270-panama-papers-corruption-report/',
    'https://www.rt.com/op-edge/338388-putin-western-media-leaks/',
    'http://www.chinadaily.com.cn/cndy/2016-04/05/content_24280080.htm',
    'https://www.washingtonpost.com/opinions/where-have-russias-billions-gone/2016/04/04/44ebd46a-fa9a-11e5-80e4-c381214de1a3_story.html',
    'https://www.washingtonpost.com/world/the_americas/where-the-papers-got-their-name/2016/04/09/f088582e-fcf8-11e5-813a-90ab563f0dde_story.html',
    'https://www.washingtonpost.com/world/as-panama-leaks-spread-chinas-red-nobility-would-rather-not-talk-about-it/2016/04/07/ab5ab28e-fc4d-11e5-813a-90ab563f0dde_story.html'
])

#
# raw data set
# add_article(Category.science_tech, Topic.hack, Event.hack_equifax_breach,  [])
add_article(Category.technology, Topic.legancy, Event.hack_equifax_breach, [
    "https://www.wsj.com/articles/equifax-earnings-drop-27-in-quarter-marred-by-cyberattack-1510268187",
    "https://www.bloomberg.com/news/articles/2017-11-14/how-much-will-equifax-pay",
    "https://gizmodo.com/equifax-seized-138-scammy-lookalike-domains-instead-of-1820450580",
    'https://www.nytimes.com/2017/09/27/your-money/equifax-credit-freeze-lock-apology.html',
    'https://www.nytimes.com/2017/10/02/business/equifax-breach.html',
    'https://www.npr.org/sections/thetwo-way/2017/09/19/552124551/equifax-confirms-another-security-incident',
    'https://www.thesun.co.uk/news/4425740/cyber-attack-equifax-data-stolen-brits/',
    'https://www.thesun.co.uk/tech/4475843/equifax-admits-that-400000-british-peoples-private-info-was-accessed-during-major-cybersecurity-incident/',
    'https://www.thesun.co.uk/news/4657635/credit-company-equifax-says-new-security-attack-means-that-almost-700000-brits-have-had-personal-details-stolen-by-cyber-hackers/',
    'http://www.dailymail.co.uk/news/article-4942344/Equifax-2-5-million-Americans-affected-hack.html',
    'http://www.dailymail.co.uk/news/article-4863648/Credit-agency-Equifax-info-143-million-stolen.html',
    'https://www.rt.com/shows/boom-bust/402559-hurricane-harvey-irma-damage/'
])

add_article(Category.world, Topic.legancy, Event.las_vegas_shooting, [
    'http://edition.cnn.com/videos/us/2017/10/02/vegas-witness-crowd-running.cnn',
    'http://edition.cnn.com/2017/10/02/us/gallery/las-vegas-shooting/index.html',
    'http://edition.cnn.com/videos/tv/2017/10/02/exp-tsr-elam-las-vegas-concert-mass-shooting.cnn',
    'http://edition.cnn.com/videos/us/2017/10/02/donald-trump-entire-las-vegas-shooting-address-sot.cnn',
    'https://www.nytimes.com/2017/10/02/us/stephen-paddock-vegas-shooter.html',
    'https://www.nytimes.com/interactive/2017/10/02/us/mandalay-bay-vegas-shooting.html',
    'https://www.rt.com/usa/405321-las-vegas-shooting-panic/',
    'https://www.rt.com/shows/news-with-ed-schultz/405483-news-with-ed-october2/',
    'https://www.rt.com/usa/405409-isis-responsibility-vegas-shooting/',
    'http://www.thehindu.com/news/international/las-vegas-shooting-deadliest-in-us-several-killed-injured/article19787232.ece',
    'http://www.thehindu.com/news/international/live-updates-las-vegas-strip-shooting/article19784319.ece',
    'http://usa.chinadaily.com.cn/world/2017-10/03/content_32789696.htm',
    'http://www.chinadaily.com.cn/cndy/2017-10/03/content_32789038.htm',
    'http://usa.chinadaily.com.cn/world/2017-10/03/content_32788252.htm'

])

add_article(Category.world, Topic.legancy, Event.north_Korea_hokkaido_missile, [
    'https://www.huffingtonpost.com/entry/un-condemns-north-korea-missile-test_us_59a681e0e4b00795c2a2ba10',
    'https://www.huffingtonpost.com/entry/north-korea-missile-guam_us_59a5ff61e4b084581a14339c',
    'https://www.huffingtonpost.com/entry/north-korea-missile-japan_us_59a4874fe4b050afa90c1eab',
    'http://edition.cnn.com/2017/09/15/asia/japan-north-korea-missile-reaction/index.html',
    'http://edition.cnn.com/2017/09/14/asia/north-korea-missile-launch/index.html',
    'https://www.nytimes.com/2016/09/06/world/asia/north-korea-japan-missile-test.html',
    'https://www.nytimes.com/2017/07/29/world/asia/us-south-korea-north-korea-missile-test.html',
    'https://www.nytimes.com/2017/08/28/world/asia/north-korea-missile.html',
    'https://www.npr.org/sections/thetwo-way/2017/09/14/551095592/north-korea-fires-another-missile-over-japan',
    'https://www.npr.org/sections/thetwo-way/2017/08/28/546888551/north-korea-launches-another-missile-this-one-over-japan',
    'https://www.thesun.co.uk/news/4469623/north-korea-missile-launch-pyonyang-japan-guam-latest/',
    'https://www.thesun.co.uk/news/4348423/north-korea-missile-launch-japan-latest-russia-evacauation-kim-jong-un/',
    'http://www.dailymail.co.uk/news/article-5053125/Trump-samurai-Japan-shot-North-Korean-missiles.html',
    'http://www.dailymail.co.uk/wires/reuters/article-4995834/Nowhere-hide--N-Korean-missiles-spur-anxiety-Japan-fishing-town.html',
    'https://www.rt.com/usa/403383-mattis-korea-missile-japan-cover/',
    'https://www.rt.com/news/403380-north-korea-pyongyang-missile/',
    'http://www.thehindu.com/news/international/north-korea-fires-missile-over-japan-in-aggressive-test/article19577734.ece',
    'http://www.thehindu.com/todays-paper/tp-international/n-korea-fires-missile-over-japan/article19695124.ece',
    'http://www.thehindu.com/news/international/north-korea-fires-missile-over-japan-on-tuesday/article19585240.ece',
    'http://europe.chinadaily.com.cn/world/2017-09/15/content_32047139.htm',
    'http://africa.chinadaily.com.cn/world/2017-09/15/content_32041310.htm',
    'http://www.chinadaily.com.cn/world/2017-09/15/content_32021877.htm'
])



#
# new
#

add_article(Category.entertainment, Topic.unspecific, Event.Top_Female__Recording_Academy, [
   'https://www.rollingstone.com/music/news/top-female-music-execs-academy-woefully-out-of-touch-w516375',
    'http://variety.com/2018/biz/news/female-execs-from-universal-warner-sony-issue-letter-slamming-recording-academy-1202687485/',
    'http://ew.com/music/2018/02/05/grammys-woefully-out-of-touch-female-music-execs-letter/',
    'https://www.nytimes.com/2018/02/05/arts/music/neil-portnow-recording-academy-women-letter.html',
    'http://www.latimes.com/entertainment/la-et-entertainment-news-updates-2018-female-music-execs-protest-gender-bias-1517873932-htmlstory.html'
])

add_article(Category.entertainment, Topic.unspecific, Event.The_New_Infinity_War_Trailer, [
    'http://variety.com/2018/film/news/avengers-infinity-war-super-bowl-52-1202682183/',
    'http://www.businessinsider.com/avengers-infinity-war-super-bowl-trailer-2018-2?IR=T',
    'https://www.nytimes.com/2017/11/29/movies/avengers-infinity-war-trailer-robert-downey-jr-chadwick-boseman.html',
    'http://www.dailymail.co.uk/tvshowbiz/article-5351817/Avengers-Infinity-War-Super-Bowl-trailer.html'

])
add_article(Category.entertainment, Topic.unspecific, Event.Quentin_Tarantino_Uma_Thurman_car_crash, [
    'http://www.indiewire.com/2018/02/quentin-tarantino-responds-uma-thurman-car-crash-abuse-kill-bill-1201925124/',
    'http://abcnews.go.com/GMA/Culture/quentin-tarantino-sounds-off-uma-thurmans-kill-bill/story?id=52871322',
    'http://www.bbc.com/news/entertainment-arts-42958525',
    'https://www.nytimes.com/2018/02/03/opinion/sunday/this-is-why-uma-thurman-is-angry.html',
    'http://deadline.com/2018/02/quentin-tarantino-uma-thurman-harvey-weinstein-kill-bill-car-crash-new-york-times-1202278988/',
    'http://edition.cnn.com/2018/02/03/entertainment/uma-thurman-harvey-weinstein/index.html',
    'https://www.washingtonpost.com/national/uma-thurman-levels-accusations-against-weinstein-tarantino/2018/02/03/eb678d32-090e-11e8-aa61-f3391373867e_story.html?utm_term=.3cf88126a82d'
])
add_article(Category.entertainment, Topic.unspecific, Event.Justin_Timberlake_halftime_show, [
    'https://www.usatoday.com/story/life/entertainthis/2018/02/05/compared-prince-justin-timberlakes-halftime-show-hilariously-bad/307243002/',
    'https://www.washingtonpost.com/news/arts-and-entertainment/wp/2018/02/04/this-is-how-justin-timberlake-lost-the-super-bowl/?utm_term=.a60d786e8c79',
    'https://www.newyorker.com/culture/culture-desk/justin-timberlakes-super-bowl-halftime-show-reviewed',
    'https://edition.cnn.com/2018/02/04/entertainment/gallery/super-bowl-2018-halftime-show/index.html',
    'https://www.theguardian.com/culture/2018/feb/04/justin-timberlake-super-bowl-halftime-show-review'
])
add_article(Category.entertainment, Topic.unspecific, Event.Sarah_Silverman_and_Michael_Sheen_Break_Up, [
    'http://www.eonline.com/news/911725/sarah-silverman-and-michael-sheen-break-up',
    'https://www.usatoday.com/story/life/people/2018/02/06/sarah-silverman-michael-sheen-split-after-four-years/310195002/',
    'https://edition.cnn.com/2018/02/06/entertainment/sarah-silverman-michael-sheen-split/index.html',
    'https://www.cbsnews.com/news/sarah-silverman-michael-sheen-call-it-quits/',
    'https://www.huffingtonpost.com/entry/sarah-silverman-michael-sheen-split_us_5a78cf80e4b0164659c72da3',
    'http://www.dailymail.co.uk/tvshowbiz/article-5355017/Sarah-Silverman-Michael-Sheen-split-four-years.html',
    'https://www.thesun.co.uk/tvandshowbiz/5508158/michael-sheen-and-sarah-silverman-split-four-years/',
    'http://www.nydailynews.com/entertainment/gossip/sarah-silverman-michael-sheen-split-years-article-1.3800922'
])


add_article(Category.science, Topic.unspecific, Event.First_Falcon_Heavy_launch, [
    'https://spaceflightnow.com/2018/02/05/first-falcon-heavy-launch-blends-spacex-style-raw-power-and-the-unknown/',
    'https://www.nytimes.com/2018/02/06/science/falcon-heavy-spacex-launch.html',
    'https://www.npr.org/sections/thetwo-way/2018/02/05/582464054/spacex-set-to-launch-worlds-most-powerful-rocket',
    'http://www.dailymail.co.uk/sciencetech/article-5238433/Elon-Musk-SpaceX-launch-Falcon-Heavy-rocket-month.html',
    'https://www.rt.com/usa/417934-spacex-falcon-heavy-rocket/',
    'https://www.washingtonpost.com/national/energy-environment/spacex-bucks-launch-tradition-in-1st-flight-of-new-rocket/2018/02/05/30a52ade-0ab4-11e8-998c-96deb18cca19_story.html?utm_term=.0feab7a60538',
    'https://www.washingtonpost.com/national/health-science/spacexs-hot-new-monster-rocket-ready-for-first-test-flight/2018/02/04/0e7f682c-09cc-11e8-998c-96deb18cca19_story.html?utm_term=.94124d7a5e6b'
])

add_article(Category.science, Topic.unspecific, Event.fossil_sheds_light_on_origins_of_spiders, [

])

add_article(Category.science, Topic.unspecific, Event.first_planets_outside_the_Milky_Way, [
    'https://www.washingtonpost.com/news/speaking-of-science/wp/2018/02/05/scientists-discover-the-first-planets-outside-the-milky-way/?utm_term=.2d11f789bb28',
    'http://www.dailymail.co.uk/sciencetech/article-5346873/Scientists-spot-planets-galaxies-Milky-Way.html',
    'https://www.rt.com/usa/417984-exoplanets-chandra-x-ray/',
    'http://www.independent.co.uk/news/science/planets-far-beyond-galaxy-discovered-first-time-astrophysicists-nasa-university-oklahoma-a8193531.html',
    'https://www.nbcnews.com/mach/science/first-planets-beyond-milky-way-may-have-been-discovered-ncna844861'
])


add_article(Category.technology, Topic.unspecific, Event.Apple_removed_Telegram, [
   # 'https://www.theverge.com/2018/2/5/16974710/apple-telegram-ios-app-store-removal-explanation-child-pornography-distribution',
    'https://www.theinquirer.net/inquirer/news/3025811/apple-removed-telegram-from-app-store-due-to-child-pornographyc',
    'http://www.telegraph.co.uk/technology/2018/02/01/apple-removes-encrypted-messaging-app-telegram-app-store/',
    'https://www.usatoday.com/story/tech/news/2018/02/01/apple-removes-secretive-telegram-messaging-app-app-store/1086302001/',
    'https://www.thetimes.co.uk/article/apple-removes-telegram-app-accused-of-being-haven-for-terrorists-shv735jvt',
    'http://www.bbc.com/news/technology-42904198'
])
add_article(Category.technology, Topic.unspecific, Event.Google_enables_Pixel_Visual_Core, [
    'https://gadgetstouse.com/news/google-pixel-visual-core-pixel-2/96002',
    'https://www.theverge.com/circuitbreaker/2018/2/5/16973286/google-pixel-visual-core-pixel-2-app',
    'https://www.cnet.com/news/google-pixel-2-photos-get-ai-better-digital-zoom/',
    'https://www.xda-developers.com/google-pixel-visual-core-instagram-snapchat-whatsapp/',
    'https://www.wired.com/story/google-pixel-visual-core/',
    'https://www.blog.google/products/pixel/use-pixel-2-better-photos-instagram-whatsapp-and-snapchat/'

])
add_article(Category.technology, Topic.unspecific, Event.former_Facebook_and_Apple_employees, [
    'http://uk.pcmag.com/asana/93196/news/facebook-google-vets-form-coalition-to-fight-tech-addiction',
    'https://www.usatoday.com/story/tech/2018/02/05/just-say-no-addicting-kids-technology-former-facebook-google-employees-investors-urge/307529002/',
    'http://www.businessinsider.de/ex-facebook-and-google-employees-launch-anti-tech-addiction-campaign-2018-2?r=US&IR=T',
    'https://www.nytimes.com/2018/02/04/technology/early-facebook-google-employees-fight-tech.html',
    'https://www.cnbc.com/2018/02/04/early-facebook-and-google-employees-form-coalition-to-fight-what-they-built.html',
    'https://www.theguardian.com/technology/2018/feb/05/tech-addiction-former-facebook-google-employees-campaign',
    'http://www.bbc.com/news/technology-42959848',
    'http://www.telegraph.co.uk/news/2018/02/05/ex-google-facebook-staff-warn-social-media-dangers/',
    'https://www.thetimes.co.uk/article/social-media-pioneers-reject-their-creation-x7mp2mjsw'
])
add_article(Category.technology, Topic.unspecific, Event.Intel_smart_glass, [
    'https://techcrunch.com/2018/02/05/intel-wants-smart-glasses-to-be-a-thing/',
    'https://www.thetimes.co.uk/article/intels-subtle-smart-glasses-avoid-google-glass-blind-spot-w368svbph',
    'http://bgr.com/2018/02/05/intel-vaunt-smart-glasses-release-date-features/',
    'https://www.theinquirer.net/inquirer/news/3026063/intels-vaunt-smart-glasses-are-a-long-way-from-google-glass',
    #'https://www.theverge.com/2018/2/5/16966530/intel-vaunt-smart-glasses-announced-ar-video',
    'https://www.engadget.com/2018/02/06/the-morning-after-intel-attempts-smartglasses/',
    'https://www.cnet.com/news/intel-vaunt-smart-glasses-prototype/'
])


add_article(Category.technology, Topic.unspecific, Event.PS4_System_Update_5_50, [
    'https://www.thesun.co.uk/tech/5350839/ps4-update-beta-sign-up/',
    'http://www.playstationlifestyle.net/2018/02/06/ps4-system-update-5-50-features-fully-detailed/',
    'https://www.gamespot.com/articles/ps4-550-updates-features-detailed-heres-what-it-do/1100-6456595/',
    'https://blog.eu.playstation.com/2018/02/06/ps4-system-software-5-50-out-today-key-features-revealed/',
    'https://www.psu.com/news/ps4-5-50-update-new-features/',
    'https://www.dailystar.co.uk/tech/gaming/679642/PS4-Update-5-50-Sony-release-new-system-upgrade-here-s-what-it-does'
])

add_article(Category.technology, Topic.unspecific, Event.Broadcom_Raises_Its_Qualcomm_Offer_to_121, [
    'https://www.nytimes.com/2018/02/05/business/dealbook/broadcom-qualcomm-deal.html?partner=rss&emc=rss',
    'http://www.warringtonguardian.co.uk/news/national/15920573.Broadcom_raises_Qualcomm_bid_to_more_than_121_billion_US_dollars/',
    'https://www.usatoday.com/story/tech/news/2018/02/05/broadcom-increases-qualcomm-offer-more-than-121-billion/306382002/',
    'https://www.bloomberg.com/news/articles/2018-02-05/broadcom-is-said-planning-to-boost-qualcomm-bid-to-120-billion',
    'https://www.wsj.com/articles/broadcom-raises-offer-for-qualcomm-to-over-121-billion-1517833668',
    'http://www.post-gazette.com/business/tech-news/2018/02/05/Broadcom-raises-its-bid-for-Qualcomm-offering-121-billion/stories/201802050205',
    'https://uk.reuters.com/article/us-qualcomm-m-a-broadcom/broadcom-unveils-121-billion-best-and-final-offer-for-qualcomm-idUKKBN1FP1KX',
    'https://www.japantimes.co.jp/?post_type=news&p=1352777',
])
add_article(Category.technology, Topic.unspecific, Event.Bitcoin_drops, [
    'https://www.nytimes.com/2018/02/05/technology/virtual-currency-regulation.html',
    'https://www.express.co.uk/finance/city/911809/Bitcoin-price-value-worth-latest-today-buy-USD-XRP-Ripple-cryptocurrency-Seoul-trade-video',
    'https://www.theguardian.com/technology/2018/feb/06/bitcoin-price-crackdown-bis-cryptocurrency',
    'https://www.coindesk.com/bitcoin-slumps-to-12-week-low-below-6k/',
    'https://www.express.co.uk/finance/city/915014/Bitcoin-price-live-latest-fall-news-ripple-ethereum-cash-dow-buttcoin',
    'http://www.businessinsider.de/bitcoin-is-getting-smashed-2018-2?r=US&IR=T',
    'http://www.forexlive.com/cryptocurrency/!/bitcoin-touches-usd-6000-as-the-tumble-continues-20180206',
    'http://bgr.com/2018/02/06/bitcoin-price-today-6000-dow/',
    'https://themerkle.com/bitcoin-price-records-small-bounce-after-dropping-to-6000/'
])


if __name__ == '__main__':
    # crawling itself
    for index, info_article_list in enumerate(articles):
        url = info_article_list['Url']

        info_article = copy.deepcopy(info_article_list)
        del info_article['Url']
        dId = hashlib.sha224(url.encode('utf-8')).hexdigest()

        print(url)

        if not file_exist_has_content('data_raw', dId + '.json'):
            try:
                article = NewsPlease.from_url(url)

                # this is an dict
                article_dict = article.get_dict()

                article_dict['dId'] = dId
                article_dict['newsCluster'] = info_article

                # datetime-datetime-not-json-serializable bugfix"
                if article_dict.get('date_publish'):
                    article_dict['date_publish'] = article_dict['date_publish'].isoformat()
                if article_dict.get('date_download'):
                    article_dict['date_download'] = article_dict['date_download'].isoformat()

                check_image(article_dict)
                write_json('data_raw', article_dict['dId'], article_dict)

            except http.client.RemoteDisconnected as e:
                print(e)
            except urllib.error.HTTPError as e:
                print(e)
        else:
            print('skipped, newsCluster updated')
            path = 'data_raw' + '/' + dId + '.' + 'json'
            with open(path, encoding='utf-8') as data_file:
                data = json.load(data_file)
                check_image(data)
                data['newsCluster'] = info_article
            with open(path, encoding='utf-8', mode='w') as data_file:
                data_file.write(json.dumps(data, sort_keys=False, indent=2))

    # preprocess into data
    for f in glob.glob('data/*'):
        os.remove(f)
    for f in glob.glob('data_damaged/*'):
        os.remove(f)

    for filepath in glob.glob('data_raw/*.json'):
        with open(filepath, encoding='utf-8') as data_file:
            try:
                data = json.load(data_file)
                target = None

                # giveme5w(and enhancer) needs at least these 3 fields to work proper
                if data.get('date_publish') is not None and data.get('title') is not None and data.get(
                        'text') is not None:
                    target = 'data'
                else:
                    target = 'data_damaged'

                outfile = open(target + '/' + data['dId'] + '.json', 'w')
                outfile.write(json.dumps(data, sort_keys=False, indent=2))
                outfile.close()
            except json.decoder.JSONDecodeError:
                print('skipped:' + filepath)



