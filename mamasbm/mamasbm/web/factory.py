import calendar
import transaction

from mamasbm.models import DBSession, Profile, MessageProfile, Message
from mamasbm.web.csv_handler import CsvImporter


def build_message_profiles(name, temp_file, profile_uuid):
    with transaction.manager:
        profile = DBSession.query(Profile).get(profile_uuid)
        num_days = len(profile.get_send_days())
        days = CsvImporter(num_days).import_csv(temp_file)
        for k, v in days.items():
            day_name = calendar.day_name[k]
            msg_profile = MessageProfile(name='%s - %s' % (name, day_name))
            messages = [
                Message(week=wk, text=txt)
                for wk, txt in v.items()
            ]
            msg_profile.messages.extend(messages)
            profile.message_profiles.append(msg_profile)
