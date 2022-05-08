# pylint: disable=line-too-long
from os import environ


channels = {
  'HELP': environ['CHANNEL_HELP_ID'],
  'TO_DELETE': environ['CHANNEL_TO_DELETE_ID'],
  'ANTISPAMERS': environ['CHANNEL_ANTISPAMERS_ID']
}

reactions = {
  'REGEX': 'check|2020|completed|peacock|reasonable|mary_cheek',
  'TO_DELETE': [
    'bug',
    'uh19_check',
    'alexes_check',
    'heavy_check_mark',
    'white_check_mark',
    'agetnors_check',
    'blue_heavy_check',
    'canc_noj',
    'andrewss_check'
  ]
}

admins = [
  'U3FHTMNQY',
  'U2PS59CC8',
  'U2NSN0X26',
  'U018Q2S3KFA',
  'U3VMF71PU',
  'U35GJA25B',
  'U03C8Q4L2CR',
  'U03BL66ABD4',
  'U03BV5V60Q4'
]

TASK_ID_REGEX = r"(?<=\/task\/)\d+(?=\||>|\?)"
PROFILE_LINK_REGEX = r"(?<=<)[A-Za-z:\/]+znanija\.com\/((app\/profile\/)|(profil\/\w+-)|(users\/(user_content|redirect_user)\/))\d+"
DELETE_REASON_REGEX = r"(?<=\|)[А-Яа-я0-9]+|.+(?=<)|(?<=>)(.|\n)+?[А-Яа-я0-9\s]+"
