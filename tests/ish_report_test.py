import unittest
import datetime
import pytz
import math
from ish_parser import ish_report, ish_reportException

class ish_report_test(unittest.TestCase):

  def test_solar_irradiance(self):
    noaa_string = """0104724666999992004042720009+39567-104850NSRDB+179399999V020999999999999999999999999999+99999+99999999999ADDGM1006010140690989029013102999999GP10060100702008098902015012202008GQ100600268919729GR100601203913489"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(len(weather.solar_irradiance), 1) # verify only one row
    self.assertEqual(weather.solar_irradiance[0]['time_period'], 60)
    print(weather.formatted())
    
  def test_kord_single_day(self):
    noaa_string = """0296725300948462015010900397+41995-087934FM-16+0205KORD V0202205N00725006105MN0032195N5-01065-01395999999ADDAA101000021AU110030015AU225030015AW1275AW2715GA1085+006105999GD14991+0061059GE19MSL   +99999+99999GF199999999999006101999999MA1100955098525OC101135OD149901491220REMMET12301/08/15 18:39:01 SPECI KORD 090039Z 22014G22KT 2SM -SN BLSN OVC020 M11/M14 A2981 RMK AO2 PK WND 22029/2356 P0000 T11061139"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(len(weather.sky_cover_summation), 1)
    print(weather.formatted())

  def test_cloud_coverage_multiple_layers(self):
    ''' test a report that has GA1 and GA2 '''
    noaa_string = """0275726430149202015010114537+43879-091253FM-15+0200KLSE V0302105N00465022865MN0160935N5-00835-01285101565ADDAA101000095GA1075+022865999GA2085+027435999GD13991+0228659GD24991+0274359GE19MSL   +99999+99999GF199999999999022861999999MA1101355098975MD1590029+9999REMMET11301/01/15 08:53:02 METAR KLSE 011453Z 21009KT 10SM BKN075 OVC090 M08/M13 A2993 RMK AO2 SLP156 T10831128 55002 (JK)"""
    wx = ish_report()
    wx.loads(noaa_string)
    self.assertEqual(type(wx.sky_cover), list)
    self.assertEqual(len(wx.sky_cover), 2) #should have two
    self.assertIn('coverage', wx.sky_cover[1].keys())
    self.assertIn('base_height', wx.sky_cover[1].keys())

    # make sure we're handling the GF1 ok
    self.assertIn('total_coverage', wx.sky_condition_observation[0])

  def test_kync_single_date(self):
    # 1:51 AM,61.0,51.1,70,29.97,10.0,WNW,4.6,-,N/A,,Clear,290,2014-09-18 05:51:00
    noaa_string = """0185725053947282014091806517+40779-073969FM-15+0048KNYC V0309999V002152200059N0160935N5+01615+01065101455ADDAA101000095GA1005+999999999GD10991+9999999GF100991999999999999999999MA1101565100985REMMET09009/18/14 01:51:02 METAR KNYC 180651Z VRB04KT 10SM CLR 16/11 A2999 RMK AO2 SLP145 T01610106"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.air_temperature.get_fahrenheit(), 61.0)
    self.assertEqual(weather.dew_point.get_fahrenheit(), 51.1)
    self.assertEqual(weather.sea_level_pressure.get_inches(), 29.96)
    self.assertEqual(weather.humidity, 70)

  def test_single_reading(self):
    noaa_string = """0243725300948462014010101087+41995-087934FM-16+0205KORD V0302905N00155004575MN0020125N5-01115-01445999999ADDAA101000231AU110030015AW1715GA1085+004575991GD14991+0045759GE19MSL   +99999+99999GF199999990990004571991991MA1102615100145REMMET10912/31/13 19:08:03 SPECI KORD 010108Z 29003KT 1 1/4SM -SN OVC015 M11/M14 A3030 RMK AO2 P0001 T11111144 $ (KLC)"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.datetime,
                      datetime.datetime(2014, 1, 1, 1, 8, tzinfo=pytz.UTC))
    self.assertEqual(weather.wban, '94846')
    self.assertEqual(weather.weather_station, '725300')
    self.assertEqual(weather.report_type, 'FM-16')
    self.assertEqual(weather.latitude, 41.995)
    self.assertEqual(weather.longitude, -87.934)
    self.assertEqual(weather.visibility_distance, 2012)
    self.assertEqual(weather.air_temperature, -11.1)
    self.assertEqual(weather.dew_point, -14.4)
    self.assertEqual(weather.humidity, 77)
    self.assertEqual(len(weather.precipitation), 1)
    precip = weather.precipitation[0]
    self.assertEqual(precip['hours'], 1)
    self.assertEqual(precip['depth'], 0.2)

  def test_crazy_aw6_report(self):
    noaa_string = """0482722589039912014100220237+33206-097199FM-16+0196KDTO V0203205N00775007325MN0004025N5+02005+01835999999ADDAA101018231AU107000025AU230070025AU320020035AU400002015AW1305AW2335AW3605AW4905AW5955AW6965GA1075+007325991GA2075+014025991GA3085+016765991GD13991+0073259GD23991+0140259GD34991+0167659GE19AGL   +99999+99999GF199999990990007321991991MA1100685098365MW1905OC101085OD149901591300REMMET17610/02/14 14:23:02 SPECI KDTO 022023Z 32015G21KT 1/4SM +TSGRRA FG BKN024 BKN046 OVC055 20/18 A2973 RMK AO2 PK WND 30031/2013 WSHFT 2003 LTG DSNT ALQDS GRB13 P0072 T02000183 (DT)EQDD01      0ADE735"""
    weather = ish_report()
    weather.loads(noaa_string)

  def test_zeroonezero_bad_report(self):
    noaa_string = """039499999903098201406012300I+39483-106734CRN05+262399999V02099999999999999999N999999999+01781+99999999999ADDAA101000091AO105000091CF1118910CF2000010CG1+0441710CG2+0438310CG3+0443810CN1013410012910999990CN2+999990+0263100010CN30149971001753210CN40100000104001018010CO199-07CR10610110CT1+017810CT2+017810CT3+017810CU1+999990000710CU2+999990000610CU3+999990000610CV1+017810999990+020010999990CV2+017810999990+019910999990CV3+017810999990+019910999990CW112090103001010KA1010M+01991KA2010N+01781KF1+01891"""
    weather = ish_report()
    weather.loads(noaa_string)

  def test_random_failed_report(self):
    noaa_string = """0505725560149412014063014567+41986-097435FM-15+0473KOFK V0303405N01395007325MN0012075N5+01785+01615100525ADDAA101005196AA203000392AU107000025AU230020035AU300001015AU400000215AW1105AW2185AW3635AW4905AW5951GA1045+003055991GA2075+007325991GA3085+009145991GD12991+0030559GD23991+0073259GD34991+0091459GE19MSL   +99999+99999GF199999990990003051991991MA1100645095125MD1390074+9999OC102635OD149999990320REMMET18606/30/14 08:56:02 METAR KOFK 301456Z 34027G51KT 3/4SM +TSRA BR SQ SCT010 BKN024 OVC030 18/16 A2972 RMK AO2 PK WND 32051/1450 LTG DSNT ALQDS RAB51 TSB37 SLP052 P0001 60001 T01780161 53007EQDQ01  00028PRCP03"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.report_type, 'FM-15')

  def test_another_ob1_error(self):
    noaa_string = """052199999953149201411200500I+38303-111294CRN05+189199999V0209999R002119999999N999999999-00201+99999999999ADDAA101000091AO105000091CB105+0000010CF1097310CF2114010CF3098510CG1+0124710CG2+0127310CG3+0129310CH105-002110063410CI1-002210-00151000002100000810CN1012810012410011610CN2-002010-0056100010CN30149991051488010CO199-07CR10242410CT1-002010CT2-002010CT3-002010CU1+999990000210CU2+999990000210CU3+999990000210CV1-002210999990-001510999990CV2-002210999990-001510999990CV3-002210999990-001510999990CW111580102992010GH10000010000001000000100000010IB2-002110000210KA1010M-00151KA2010N-00221KF1-00191OB10600028109999000029109999990"""
    weather = ish_report()
    weather.loads(noaa_string)

  def test_present_weather(self):
    noaa_string = """0281725300948462014010508237+41995-087934FM-16+0205KORD V0303505N00625005795MN0020125N5-00565-00835999999ADDAA101000531AU110030015AW1715GA1025+003355991GA2085+005795991GD11991+0033559GD24991+0057959GE19MSL   +99999+99999GF199999990990003351991991MA1101665099215REMMET11601/05/14 02:23:02 SPECI KORD 050823Z 35012KT 1 1/4SM -SN FEW011 OVC019 M06/M08 A3002 RMK AO2 P0002 T10561083 $ (MJF)"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.present_weather,
                      ['Light Snow'])
    self.assertEqual(weather.precipitation, [{'depth': 0.5, 'hours': 1}])

  def test_report_with_big_quality_section(self):
    noaa = """0177330580999991970050200004+52050+033950FM-12+999999999V0201401N00621220001CN0190001N9+01501+00611100651ADDAA199000091AY121999GA1021+003009079GA2999+999999099GF199999999999999999001001MD1710041+9999EQDQ01+000002SCOTCVQ02+000002SCOTLCQ03+000002SCOLCGQ04+000992SCOLCBQ05    003SCCGA2"""
    weather = ish_report()
    weather.loads(noaa)
    self.assertEqual(weather.datetime,
                      datetime.datetime(1970, 5, 2, 0, 0, tzinfo=pytz.UTC))

  def test_fm15(self):
    noaa_string = """0250725300948462014010100517+41995-087934FM-15+0205KORD V0302505N00155005795MN0024145N5-01115-01445102735ADDAA101000895AU110030015AW1715GA1085+005795991GD14991+0057959GE19MSL   +99999+99999GF199999990990005791991991MA1102575100115REMMET11612/31/13 18:51:03 METAR KORD 010051Z 25003KT 1 1/2SM -SN OVC019 M11/M14 A3029 RMK AO2 SLP273 P0003 T11111144 $ (KLC)"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.datetime,
                      datetime.datetime(2014, 1, 1, 0, 51, tzinfo=pytz.UTC))
    self.assertEqual(weather.wban, '94846')
    self.assertEqual(weather.weather_station, '725300')
    self.assertEqual(weather.report_type, 'FM-15')
    self.assertEqual(weather.elevation, 205)
    self.assertEqual(weather.wind_speed, 1.5)
    self.assertEqual(weather.wind_speed.get_MilesPerHour(), 3.3554)
    self.assertEqual(weather.wind_direction, 250)
    self.assertEqual(weather.sky_ceiling, 579)
    self.assertEqual(weather.air_temperature, -11.1)
    self.assertEqual(weather.air_temperature.get_fahrenheit(), 12.0)
    self.assertEqual(weather.sea_level_pressure, 1027.3)

  def test_fm15_json(self):
    noaa_string = """0250725300948462014010100517+41995-087934FM-15+0205KORD V0302505N00155005795MN0024145N5-01115-01445102735ADDAA101000895AU110030015AW1715GA1085+005795991GD14991+0057959GE19MSL   +99999+99999GF199999990990005791991991MA1102575100115REMMET11612/31/13 18:51:03 METAR KORD 010051Z 25003KT 1 1/2SM -SN OVC019 M11/M14 A3029 RMK AO2 SLP273 P0003 T11111144 $ (KLC)"""
    expected_json = '{"weather_station": "725300", "latitude": 41.995, "longitude": -87.934, "elevation": 205, "time": "2014-01-01T00:51:00+00:00", "air_temperature": {"value": -11.1, "quality": "5"}, "dew_point": {"value": -14.4, "quality": "5"}, "wind_speed": {"value": 1.5, "quality": "5"}, "wind_direction": {"value": "250", "quality": "5"}, "sea_level_pressure": {"value": 1027.3, "quality": ""}, "sky_ceiling": {"value": 579, "quality": "5"}, "visibility_distance": {"value": 2414, "quality": "5"}, "liquid_precip": [{"hours": 1, "depth": 0.8}], "weather_occurence": [{"intensity": "Light", "precipitation": "Snow"}], "weather_condition": [{"present_weather_condition": "Snow, slight"}], "sky_cover_condition": [{"coverage": 8.0, "base_height": 579.0, "cloud_type": "59"}]} != {"weather_station": "725300", "latitude": 41.995, "longitude": -87.934, "elevation": 205, "time": "2014-01-01T00:51:00+00:00", "air_temperature": {"value": -11.1, "quality": "5"}, "dew_point": {"value": -14.4, "quality": "5"}, "wind_speed": {"value": 1.5, "quality": "5"}, "wind_direction": {"value": "250", "quality": "5"}, "sea_level_pressure": {"value": 1027.3, "quality": ""}, "sky_ceiling": {"value": 579, "quality": "5"}, "visibility_distance": {"value": 2414, "quality": "5"}, "liquid_precip": [{"hours": 1, "depth": 0.8}], "weather_occurence": [{"intensity": "Light", "precipitation": "Snow"}]}'
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(expected_json, weather.toJson())


  def test_json(self):
    noaa_string = "0093010010999992021010103004+70939-008669FM-12+001099999V0203371N0104199999999999999999-00421-00891101731ADDKA1010M-00431KA2010N-00451MA1999999101611MD1210021+9999OC101981OD190101251999REMSYN004BUFR"
    expected_json = '{"weather_station": "010010", "latitude": 70.939, "longitude": -8.669, "elevation": 10, "time": "2021-01-01T03:00:00+00:00", "air_temperature": {"value": -4.2, "quality": "1"}, "dew_point": {"value": -8.9, "quality": "1"}, "wind_speed": {"value": 10.4, "quality": "1"}, "wind_direction": {"value": "337", "quality": "1"}, "sea_level_pressure": {"value": 1017.3, "quality": ""}, "sky_ceiling": {"value": 99999, "quality": "9"}, "visibility_distance": {"value": 999999, "quality": "9"}, "extreme_temperature": [{"hours": 10, "code": "M", "temperature": {"value": -4.3, "quality": "1"}}, {"hours": 10, "code": "N", "temperature": {"value": -4.5, "quality": "1"}}]}'
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(expected_json, weather.toJson())

  def test_austin(self):
    string = """0190722540139042014042819537+30183-097680FM-15+0151KAUS V0203505N004152200059N0160935N5+03175+00065100325ADDAA101000095GA1005+999999999GD10991+9999999GF100991999999999999999999MA1100445098655REMMET09504/28/14 13:53:02 METAR KAUS 281953Z 35008KT 10SM CLR 32/01 A2966 RMK AO2 SLP032 T03170006 (JP)"""
    weather = ish_report()
    weather.loads(string)
    self.assertRaises(BaseException, weather.get_additional_field, 'AJ1')

  def test_boston(self):
    string = """0253725090147392005010101547+42361-071011FM-15+0009KBOS V0202305N00675018295MN0160935N5+00785+00335102175ADDAA101000025GA1075+018295999GA2085+025915999GD13991+0182959GD24991+0259159GF108991999999999999999999MA1102175102065MW1001REMMET12112/31/04 20:54:26 METAR KBOS 010154Z 23013KT 10SM BKN060 OVC085 08/03 A3017 RMK AO2 RAB23E32 SLP217 P0000 T00780033 (ETM)"""
    weather = ish_report()
    weather.loads(string)
    self.assertEqual(weather.air_temperature.get_fahrenheit(), 46.0)
    self.assertEqual(weather.wind_speed, 6.7)
    self.assertEqual(weather.report_type, 'METAR Aviation routine weather report')
    self.assertEqual(weather.wind_direction, 230)

  def test_snowfall(self):
    string = """0479725300948462014010105517+41995-087934FM-15+0205KORD V0300105N00465007015MN0028165N5-01225-01565102655ADDAA101001095AA206005691AJ100089500007694AU110030015AW1715GA1075+007015991GA2075+011285991GA3085+016765991GD13991+0070159GD23991+0112859GD34991+0167659GE19MSL   +99999+99999GF199999990990007011991991KA1060M-01111KA2060N-01221KA3240M-01111KA4240N-01671MA1102515100045MD1690154+9999REMMET17012/31/13 23:51:03 METAR KORD 010551Z 01009KT 1 3/4SM -SN BKN023 BKN037 OVC055 M12/M16 A3027 RMK AO2 SLP265 4/003 P0005 60022 T11221156 11111 21122 411111167 56015 $ (SMN)EQDQ01  00558PRCP06"""
    weather = ish_report()
    weather.loads(string)
    self.assertEqual(weather.wind_direction, 10)
    self.assertEqual(weather.datetime,
                      datetime.datetime(2014, 1, 1, 5, 51, tzinfo=pytz.UTC))
    self.assertEqual(weather.snow_depth, [{'depth': 8, 'quality': '5', 'condition': '9'}])
    self.assertEqual(len(weather.precipitation), 2)

  def test_random_sod_file(self):
    noaa_string = """0141725300948462008020205596+41986-087914SOD  +0205KORD V030999999999999999999999999999+99999+99999999999ADDAA124003691AJ100159199999999AN1024008999KA1025M-00111KA2025N-00441MG1098959999999OE11240116234099999OE22240093906099999OE33240045699999999"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.datetime,
                      datetime.datetime(2008, 2, 2, 5, 59, tzinfo=pytz.UTC))
    precip = weather.precipitation[0]
    self.assertEqual(precip['hours'], 24)
    self.assertEqual(precip['depth'], 3.6)

  def test_another_random_string(self):
    noaa_string = """041572530094846198002081200C+41983-087900SAO  +0201ORD  V02099959000050076249N0128005N1-00565-00785103405ADDAA101000095AG12000AJ100089199999999AY121999GA1999+007624064GD14085+9999999GD20995+9999999GD30995+9999999GD40995+9999999GF108085081051008001999999KA1999M-00171KA2999N-00561MA1103321100815MD1510001+9999MW1021WG199190199999EQDQ01    003PRSWM1N01 00000JPWTH 1QNNE11 1 00610E11 1 00099E11 1 00099E11 1 00099G11 1 00025H11 1 15025K11 1 00018L11 1 00800M11 1 29770N11 1 00000Q11 1 10340S11 1 00022V11 1 01010X11 1 00000"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.datetime,
                      datetime.datetime(1980, 2, 8, 12, 0, tzinfo=pytz.UTC))

  def test_crazy_remarks(self):
    noaa_string = """1434725300948462006030105596+41986-087914SOM  +0205KORD V030999999999999999999999999999+99999+99999999999ADDAB10045799AD10030291516999999999AE1079039019019AK1002531299999AM1003091111999999995AN1672006499KB1672N-06675KB2672M+02395KB3672A-02115KC1N9-02161899995KC2M9+01331499995KD1672H10246KD2672C00005KE1079009289019MH109925U101799MK1104171810215100070305395REMSOM882PCP MTOT:1.80 DEPNRM:+0.2 PCP GT 24HRS:1.19 DATE(S):15-16 DAYS W/PCP >=.01:7  DAYS W/PCP >=.10:3  DAYS W/ PCP >=.50:1 DAYS W/PCP >=1.00:1 MSDP AMTS W/DATE-TIME TAGS:MIN:5 0.00    /     MIN:10 0.00    /     MIN:15 0.00    /     MIN:20 0.00    /     MIN:30 0.00    /     MIN:45 0.00    /     MIN:60 0.00    /     MIN:80 0.00    /     MIN:100 0.00    /     MIN:120 0.00    /     MIN:150 0.00    /     MIN:180 0.00    /     SN GT DP ON GRND:1 DATE(S):12 SN GT IN 24HRS:1.2 DATE(S): 11SN MTOT:2.5 AVG DLY MIN:20.0  AVG DLY MAX:36.3  AVG MLY TMP:28.2  DEP NORM:1.2   MIN TMP:-7 DATE(S):18 MAX TMP:56  DATE(S):14 DAYS MAX <=32:7 DAYS MAX >=90:0  DAYS MIN <=32:28 DAYS MIN  <=0:1  AVG STP:29.305 LWST SLP:29.55 DATE/TIME:030539 HGST SLP:30.76 DATE/TIME:181021 HDD MTH TOT:1024 DEP NORM:-51 SEASON(JUL 1-JUN 30):4259 DEP NORM:-587 CDD MTH TOT:0 DEP NORM: 0 SEASON(JAN 1-DEC 31):0 DEP NORM: 0EQDR01  1.807ABP070R02  1.197ADP081R03     17AE2103R04  0.007A01001R05  0.007A02007R06  0.007A03013R07  0.007A04019R08  0.007A05026R09  0.007A06033R10  0.007A07039R11  0.007A08046R12  0.007A09052R13  0.007A10058R14  0.007A11065R15  0.007A12071R16   2.57ANS075R17  10247KDH045R18     17KE4041"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.datetime,
                      datetime.datetime(2006, 3, 1, 5, 59, tzinfo=pytz.UTC))

  def test_with_crazy_metar_in_remarks(self):
    """ this one has some crazy double remarks thing going on """
    noaa_string = """033072530094846197301312200C+41983-087900SAO  +0201ORD  V0201405N00525004574MN0096005N1+00395+00115101305ADDAA101000095GD14995+0045099GD20995+9999999GD30995+9999999GD40995+9999999GF108085999999999999999999MA1101251098815MW1041MW2051MW3445REMAWY012VA?ORD C1/78MET005?1/30EQDN01 07200JPWTH 1QNNE11 1 00699E11 1 00099E11 1 00099E11 1 00099G11 1 00015K11 1 00034L11 1 00600M11 1 29180N11 1 07200Q11 1 10130S11 1 00039V11 1 01010X11 1 14010"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEqual(weather.wind_direction, 140)
    self.assertEqual(weather.datetime,
                      datetime.datetime(1973, 1, 31, 22, 0, tzinfo=pytz.UTC))

  def test_Weird_old_report(self):
    noaa = """0078035480999991943070121004+52467+000950FM-12+004699999V0209991N00671999991CN0040001N9+99999+99999999999ADDAY121999GA1081+999999999GF199999071051004501999999MW1051EQDQ01+000072SCOTCV"""
    ish = ish_report()
    ish.loads(noaa)
    self.assertEqual(ish.air_temperature, 999.9)
    self.assertEqual(ish.wind_speed, 6.7)
    self.assertEqual(str(ish.wind_direction), 'MISSING')
    self.assertEqual(ish.wind_direction, 999)
    self.assertEqual(str(ish.sky_ceiling), 'MISSING')
    self.assertEqual(ish.air_temperature.get_fahrenheit(), 'MISSING')
    self.assertEqual(str(ish.sea_level_pressure), 'MISSING')

  def test_bad_length(self):
    noaa_string = """1243725300948462014010101087+41995-087934FM-16+0205KORD V0302905N00155004575MN0020125N5-01115-01445999999ADDAA101000231AU110030015AW1715GA1085+004575991GD14991+0045759GE19MSL   +99999+99999GF199999990990004571991991MA1102615100145REMMET10912/31/13 19:08:03 SPECI KORD 010108Z 29003KT 1 1/4SM -SN OVC015 M11/M14 A3030 RMK AO2 P0001 T11111144 $ (KLC)"""
    self.assertRaises(ish_reportException,
                      ish_report().loads, noaa_string)

  def test_old_ord(self):
    ''' test an old ORD record from 1946 that has a bunch of missing fields '''
    noaa = """0066725300948461946100109004+41983-087900SAO  +0186ORD  V02099999999992200019N0032001N9+99999+99999999999ADDGA1001+999999999GF100991999999999999999999MA1999999100341MW1111"""
    ish = ish_report()
    ish.loads(noaa)
    self.assertEqual(ish.datetime,
                      datetime.datetime(1946, 10, 1, 9, tzinfo=pytz.UTC))
    self.assertEqual(str(ish.air_temperature), 'MISSING')
    self.assertEqual(str(ish.wind_speed), 'MISSING')
    self.assertEqual(ish.sky_ceiling, 22000)
    self.assertEqual(str(ish.sea_level_pressure), 'MISSING')

  def test_string_that_caused_infinite_recursion(self):
    noaa = """0059035480999991943070124004+52467+000950FM-12+004699999V0200501N00461220001CN0040001N9+99999+99999999999ADDAY121999GA1001+999999999GF108991081051004501999999MW1051"""
    ish = ish_report()
    ish.loads(noaa)
    self.assertEqual(ish.datetime,
                      datetime.datetime(1943, 7, 2, 0, 0, tzinfo=pytz.UTC))
    self.assertEqual(ish.air_temperature.get_fahrenheit(), 'MISSING')
    self.assertEqual(ish.sea_level_pressure, 9999.9)
    self.assertEqual(str(ish.sea_level_pressure), 'MISSING')
    self.assertEqual(str(ish.sky_ceiling), '22000')

  def test_string_for_get_numeric_implementation(self):
      noaa = """0059035480999991943070124004+52467+000950FM-12+004699999V0200501N00461220001CN0040001N9+99999+99999999999ADDAY121999GA1001+999999999GF108991081051004501999999MW1051"""
      ish = ish_report()
      ish.loads(noaa)
      self.assertEqual(ish.datetime,
                       datetime.datetime(1943, 7, 2, 0, 0, tzinfo=pytz.UTC))
      self.assertTrue(math.isnan(ish.air_temperature.get_numeric()))
      self.assertTrue(math.isnan(ish.humidity.get_numeric()))
      self.assertEqual(ish.wind_direction.get_numeric(), 50)
      self.assertEqual(ish.wind_speed.get_numeric(), 4.6)
      self.assertEqual(ish.visibility_distance.get_numeric(), 4000)
      self.assertEqual(ish.sky_ceiling.get_numeric(), 22000)
